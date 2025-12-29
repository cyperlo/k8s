# Kubernetes 故障排查指南

## 常见问题与解决方案

### 1. Pod 一直处于 Pending 状态

#### 问题现象
```bash
kubectl get pods
# NAME            READY   STATUS    RESTARTS   AGE
# my-first-pod    0/1     Pending   0          2m
```

#### 排查步骤
```bash
# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### 常见原因

**1. 资源不足**
```
Events:
  Warning  FailedScheduling  pod didn't fit on any node
```

解决方案：
```bash
# 查看节点资源
kubectl top nodes
kubectl describe nodes

# 减少资源请求或增加节点
```

**2. 节点选择器不匹配**
```yaml
spec:
  nodeSelector:
    disktype: ssd  # 如果没有匹配的节点会 Pending
```

---

### 2. 镜像拉取失败（ContainerCreating）

#### 问题现象
```bash
kubectl describe pod my-first-pod

Events:
  Warning  FailedCreatePodSandBox  Failed to create pod sandbox: 
    failed to pull image "rancher/mirrored-pause:3.6": 
    dial tcp 108.160.163.112:443: i/o timeout
```

这是**最常见的问题**，特别是在国内网络环境下。

#### 解决方案

##### 方案 1：配置镜像加速器（推荐）

**对于 K3s：**

```bash
# 1. 创建 containerd 配置目录
sudo mkdir -p /etc/rancher/k3s

# 2. 创建镜像仓库配置
sudo tee /etc/rancher/k3s/registries.yaml > /dev/null <<EOF
mirrors:
  docker.io:
    endpoint:
      - "https://docker.mirrors.ustc.edu.cn"
      - "https://hub-mirror.c.163.com"
      - "https://mirror.baidubce.com"
  registry.k8s.io:
    endpoint:
      - "https://registry.aliyuncs.com/google_containers"
EOF

# 阿里云
sudo tee /etc/rancher/k3s/registries.yaml > /dev/null <<EOF
> mirrors:
>   docker.io:
>     endpoint:
>       - "https://registry.cn-hangzhou.aliyuncs.com"
>       - "https://mirror.ccs.tencentyun.com"
> EOF

# 3. 重启 K3s
sudo systemctl restart k3s

# 4. 验证配置
sudo cat /var/lib/rancher/k3s/agent/etc/containerd/config.toml | grep -A 5 "mirrors"
```

**对于 Minikube：**

```bash
# 启动时指定镜像仓库
minikube start \
  --image-mirror-country='cn' \
  --registry-mirror='https://docker.mirrors.ustc.edu.cn'
```

**对于 Docker（如果使用 Docker 作为容器运行时）：**

```bash
# 编辑 Docker 配置
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
EOF

# 重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

##### 方案 2：手动拉取镜像

```bash
# 1. 在节点上手动拉取镜像
sudo k3s crictl pull docker.io/rancher/mirrored-pause:3.6

# 或使用国内镜像源
sudo k3s crictl pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.6

# 2. 给镜像打标签
sudo k3s ctr images tag \
  registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.6 \
  docker.io/rancher/mirrored-pause:3.6

# 3. 删除并重新创建 Pod
kubectl delete pod my-first-pod
kubectl apply -f 01-basic-pod.yaml
```

##### 方案 3：使用国内镜像

修改 YAML 文件，使用国内镜像源：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
  labels:
    app: demo
spec:
  containers:
  - name: nginx
    # 使用阿里云镜像
    image: registry.cn-hangzhou.aliyuncs.com/google_containers/nginx:1.21
    ports:
    - containerPort: 80
```

##### 方案 4：配置 HTTP 代理（如果有代理）

```bash
# 编辑 K3s 服务配置
sudo mkdir -p /etc/systemd/system/k3s.service.d
sudo tee /etc/systemd/system/k3s.service.d/http-proxy.conf > /dev/null <<EOF
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
EOF

# 重启 K3s
sudo systemctl daemon-reload
sudo systemctl restart k3s
```

#### 验证解决

```bash
# 查看 Pod 状态
kubectl get pods -w

# 应该看到：
# NAME            READY   STATUS    RESTARTS   AGE
# my-first-pod    1/1     Running   0          30s

# 查看镜像拉取情况
kubectl describe pod my-first-pod | grep -A 5 "Events"
```

---

### 3. Pod 处于 CrashLoopBackOff 状态

#### 问题现象
```bash
kubectl get pods
# NAME            READY   STATUS             RESTARTS   AGE
# my-app          0/1     CrashLoopBackOff   5          5m
```

#### 排查步骤
```bash
# 查看日志
kubectl logs <pod-name>

# 查看上一次运行的日志
kubectl logs <pod-name> --previous

# 查看详细信息
kubectl describe pod <pod-name>
```

#### 常见原因

**1. 应用程序错误**
- 启动命令错误
- 配置文件错误
- 依赖服务不可用

**2. 健康检查失败**
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3
  failureThreshold: 3  # 失败 3 次后重启
```

解决方案：
- 增加 `initialDelaySeconds`
- 调整 `failureThreshold`
- 检查健康检查路径是否正确

---

### 4. Service 无法访问

#### 问题现象
```bash
# Service 存在但无法访问
kubectl get svc
curl http://<service-ip>  # 超时或拒绝连接
```

#### 排查步骤

```bash
# 1. 检查 Service
kubectl get svc <service-name>
kubectl describe svc <service-name>

# 2. 检查 Endpoints
kubectl get endpoints <service-name>

# 3. 检查 Pod 标签
kubectl get pods --show-labels

# 4. 测试 Pod 直接访问
kubectl get pods -o wide
curl http://<pod-ip>
```

#### 常见原因

**1. Selector 不匹配**
```yaml
# Service
spec:
  selector:
    app: nginx  # 标签不匹配

# Pod
metadata:
  labels:
    app: web  # 应该是 nginx
```

**2. 端口配置错误**
```yaml
spec:
  ports:
  - port: 80        # Service 端口
    targetPort: 8080  # 容器端口（必须匹配）
```

**3. 没有健康的 Pod**
```bash
kubectl get pods
# 所有 Pod 都不是 Running 状态
```

---

### 5. Ingress 404 错误

#### 问题现象
```bash
curl http://myapp.example.com
# 404 Not Found
```

#### 排查步骤

```bash
# 1. 检查 Ingress Controller 是否运行
kubectl get pods -n ingress-nginx

# 2. 检查 Ingress 配置
kubectl get ingress
kubectl describe ingress <ingress-name>

# 3. 检查后端 Service
kubectl get svc

# 4. 查看 Ingress Controller 日志
kubectl logs -n ingress-nginx <ingress-controller-pod>
```

#### 常见原因

**1. Ingress Controller 未安装**
```bash
# Minikube
minikube addons enable ingress

# K3s（默认已安装 Traefik）
kubectl get pods -n kube-system | grep traefik
```

**2. hosts 文件未配置**
```bash
# 添加到 /etc/hosts
echo "$(minikube ip) myapp.example.com" | sudo tee -a /etc/hosts
```

**3. Service 名称或端口错误**
```yaml
backend:
  service:
    name: frontend-service  # 必须存在
    port:
      number: 80  # 必须匹配 Service 的 port
```

---

### 6. PVC 一直处于 Pending 状态

#### 问题现象
```bash
kubectl get pvc
# NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS
# mysql-pvc   Pending                                      manual
```

#### 排查步骤
```bash
kubectl describe pvc <pvc-name>
```

#### 常见原因

**1. 没有匹配的 PV**
```bash
# 查看可用的 PV
kubectl get pv

# 创建 PV
kubectl apply -f pv.yaml
```

**2. StorageClass 不存在**
```bash
# 查看 StorageClass
kubectl get storageclass

# 使用默认 StorageClass
# 在 PVC 中不指定 storageClassName
```

**3. 访问模式不匹配**
```yaml
# PV
accessModes:
  - ReadWriteOnce

# PVC（必须匹配或更严格）
accessModes:
  - ReadWriteOnce
```

---

## 常用调试命令

### 查看资源状态
```bash
# 查看所有资源
kubectl get all

# 查看特定资源
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get ingress

# 查看详细信息
kubectl describe pod <pod-name>
kubectl describe node <node-name>
```

### 查看日志
```bash
# 查看 Pod 日志
kubectl logs <pod-name>

# 实时查看日志
kubectl logs -f <pod-name>

# 查看上一次运行的日志
kubectl logs <pod-name> --previous

# 查看多容器 Pod 的特定容器日志
kubectl logs <pod-name> -c <container-name>
```

### 进入容器调试
```bash
# 进入容器
kubectl exec -it <pod-name> -- /bin/bash

# 执行单个命令
kubectl exec <pod-name> -- ls /app

# 多容器 Pod
kubectl exec -it <pod-name> -c <container-name> -- /bin/bash
```

### 端口转发
```bash
# 转发到本地
kubectl port-forward <pod-name> 8080:80

# 转发 Service
kubectl port-forward svc/<service-name> 8080:80
```

### 查看事件
```bash
# 查看所有事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 查看特定命名空间的事件
kubectl get events -n <namespace>

# 实时查看事件
kubectl get events -w
```

### 查看资源使用
```bash
# 查看节点资源
kubectl top nodes

# 查看 Pod 资源
kubectl top pods

# 查看特定命名空间
kubectl top pods -n <namespace>
```

---

## 网络问题排查

### 测试 Pod 间通信
```bash
# 创建测试 Pod
kubectl run test-pod --image=busybox --rm -it -- sh

# 在 Pod 内测试
ping <pod-ip>
wget -O- http://<service-name>
nslookup <service-name>
```

### 测试 DNS 解析
```bash
# 创建测试 Pod
kubectl run test-dns --image=busybox --rm -it -- sh

# 测试 DNS
nslookup kubernetes.default
nslookup <service-name>.<namespace>.svc.cluster.local
```

---

## 推荐工具

### k9s - 终端 UI
```bash
# 安装
curl -sS https://webi.sh/k9s | sh

# 运行
k9s
```

### kubectx/kubens - 上下文切换
```bash
# 安装
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens

# 使用
kubectx  # 切换集群
kubens   # 切换命名空间
```

---

## 参考资料

- [Kubernetes 官方故障排查](https://kubernetes.io/zh-cn/docs/tasks/debug/)
- [Pod 调试](https://kubernetes.io/zh-cn/docs/tasks/debug/debug-application/debug-pods/)
- [Service 调试](https://kubernetes.io/zh-cn/docs/tasks/debug/debug-application/debug-service/)
