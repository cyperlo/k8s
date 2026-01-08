# 03 - Service 服务暴露

## 📖 概念介绍

Service 是 Kubernetes 中用于暴露应用的抽象层，它为一组 Pod 提供稳定的网络访问入口。

### 为什么需要 Service？

想象一下这个场景：
- 你有 3 个 Nginx Pod，它们的 IP 地址是动态的（Pod 重启后 IP 会变）
- 前端应用需要访问这些 Nginx Pod
- 如果直接用 Pod IP，Pod 重启后前端就找不到了

**Service 解决的问题：**
- ✅ 提供稳定的访问入口（固定的 ClusterIP）
- ✅ 自动负载均衡到多个 Pod
- ✅ 服务发现（通过 DNS 名称访问）
- ✅ 对外暴露服务（NodePort、LoadBalancer）

## 🎯 Service 类型

| 类型 | 使用场景 | 访问方式 |
|------|---------|---------|
| **ClusterIP** | 集群内部访问 | 只能在集群内访问 |
| **NodePort** | 开发测试环境 | 通过节点 IP + 端口访问 |
| **LoadBalancer** | 生产环境（云平台） | 通过云厂商负载均衡器访问 |
| **ExternalName** | 访问外部服务 | 通过 DNS CNAME 记录 |

## 📝 实战例子

### 例子 1：ClusterIP - 集群内部访问（最常用）

**场景：** 前端 Pod 需要访问后端 API

```yaml
# 1. 先部署后端应用
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: api
        image: nginx:1.21
        ports:
        - containerPort: 80

---
# 2. 创建 Service 暴露后端
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP  # 默认类型，可以省略
  selector:
    app: backend  # 选择带有 app=backend 标签的 Pod
  ports:
  - protocol: TCP
    port: 8080        # Service 的端口
    targetPort: 80    # Pod 的端口
```

**如何访问：**
```bash
# 在集群内的任何 Pod 中，可以通过以下方式访问：
curl http://backend-service:8080
curl http://backend-service.default.svc.cluster.local:8080

# 查看 Service
kubectl get svc backend-service
```

### 例子 2：NodePort - 从外部访问（开发测试）

**场景：** 你在本地开发，想通过浏览器访问集群中的 Web 应用

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80          # Service 端口
    targetPort: 80    # Pod 端口
    nodePort: 30080   # 节点端口（30000-32767）
```

**如何访问：**
```bash
# 获取节点 IP
kubectl get nodes -o wide

# 通过浏览器访问
# http://<节点IP>:30080

# 如果使用 Minikube
minikube service web-service --url
```

### 例子 3：多端口 Service

**场景：** 一个应用同时提供 HTTP 和 HTTPS 服务

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
spec:
  selector:
    app: web
  ports:
  - name: http      # 端口必须有名称
    protocol: TCP
    port: 80
    targetPort: 8080
  - name: https
    protocol: TCP
    port: 443
    targetPort: 8443
```

### 例子 4：命名端口

**场景：** Pod 使用命名端口，Service 引用端口名称

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-named-ports
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:1.21
        ports:
        - name: web-port      # 给端口命名
          containerPort: 80
        - name: metrics-port
          containerPort: 9090

---
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
  - name: web
    port: 80
    targetPort: web-port     # 引用端口名称
  - name: metrics
    port: 9090
    targetPort: metrics-port
```

### 例子 5：Headless Service - 直接访问 Pod

**场景：** 需要直接访问每个 Pod（如数据库集群）

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database-headless
spec:
  clusterIP: None  # 设置为 None 就是 Headless Service
  selector:
    app: database
  ports:
  - port: 3306
    targetPort: 3306
```

**特点：**
- 不分配 ClusterIP
- DNS 返回所有 Pod 的 IP 地址
- 用于 StatefulSet

## 🚀 实践步骤

### 完整示例：部署一个 Web 应用并暴露

```bash
# 1. 创建 Deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-web
  template:
    metadata:
      labels:
        app: my-web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
EOF

# 2. 创建 Service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: my-web-service
spec:
  type: NodePort
  selector:
    app: my-web
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
EOF

# 3. 查看 Service
kubectl get svc my-web-service

# 4. 查看 Endpoints（Service 关联的 Pod IP）
kubectl get endpoints my-web-service

# 5. 测试访问
curl http://localhost:30080  # 如果是本地集群
```

## 🔍 Service 工作原理

```
用户请求
   ↓
Service (ClusterIP: 10.96.0.10:80)
   ↓
负载均衡
   ↓
┌─────────┬─────────┬─────────┐
│ Pod 1   │ Pod 2   │ Pod 3   │
│ 10.1.1.1│ 10.1.1.2│ 10.1.1.3│
└─────────┴─────────┴─────────┘
```

**关键点：**
1. Service 通过 `selector` 选择 Pod
2. Service 创建 Endpoints 对象，记录所有匹配的 Pod IP
3. kube-proxy 配置 iptables/ipvs 规则实现负载均衡

## 🔧 常用命令

```bash
# 查看所有 Service
kubectl get svc
kubectl get services

# 查看 Service 详情
kubectl describe svc <service-name>

# 查看 Service 关联的 Pod
kubectl get endpoints <service-name>

# 查看 Service 的 DNS 记录
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>

# 测试 Service 连通性
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://<service-name>:<port>

# 删除 Service
kubectl delete svc <service-name>

# 暴露现有 Deployment 为 Service
kubectl expose deployment <deployment-name> --type=NodePort --port=80
```

## 🧪 实践练习

### 练习 1：创建一个简单的 Web Service

1. 部署 3 个 Nginx Pod
2. 创建 ClusterIP Service
3. 在集群内测试访问

### 练习 2：使用 NodePort 暴露服务

1. 修改上面的 Service 为 NodePort 类型
2. 通过浏览器访问

### 练习 3：验证负载均衡

```bash
# 1. 创建一个返回主机名的应用
kubectl create deployment echo --image=hashicorp/http-echo --replicas=3 -- -text="Hello from Pod"

# 2. 暴露服务
kubectl expose deployment echo --port=5678 --type=NodePort

# 3. 多次访问，观察负载均衡
for i in {1..10}; do curl http://localhost:<nodePort>; done
```

## 🐛 故障排查

### Service 无法访问

```bash
# 1. 检查 Service 是否存在
kubectl get svc

# 2. 检查 Endpoints 是否有 Pod IP
kubectl get endpoints <service-name>

# 3. 检查 Pod 标签是否匹配
kubectl get pods --show-labels
kubectl describe svc <service-name>  # 查看 Selector

# 4. 检查 Pod 是否正常运行
kubectl get pods

# 5. 测试 Pod 直接访问
kubectl port-forward pod/<pod-name> 8080:80
curl http://localhost:8080
```

### Endpoints 为空

**原因：** Service 的 selector 没有匹配到任何 Pod

```bash
# 检查 Pod 标签
kubectl get pods --show-labels

# 检查 Service selector
kubectl describe svc <service-name>

# 确保标签匹配
```

## 💡 最佳实践

1. **使用有意义的名称**：Service 名称会成为 DNS 记录
2. **ClusterIP 用于内部通信**：微服务之间的调用
3. **NodePort 仅用于开发测试**：生产环境使用 Ingress 或 LoadBalancer
4. **使用命名端口**：提高可读性和灵活性
5. **配置健康检查**：确保只有健康的 Pod 接收流量

## 📊 Service 类型对比

| 特性 | ClusterIP | NodePort | LoadBalancer |
|------|-----------|----------|--------------|
| 集群内访问 | ✅ | ✅ | ✅ |
| 集群外访问 | ❌ | ✅ | ✅ |
| 负载均衡 | ✅ | ✅ | ✅ |
| 固定 IP | ✅ | ✅ | ✅ |
| 需要云平台 | ❌ | ❌ | ✅ |
| 生产推荐 | 内部服务 | ❌ | ✅ |

## 📚 扩展阅读

- [Service 官方文档](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
- [DNS for Services](https://kubernetes.io/zh-cn/docs/concepts/services-networking/dns-pod-service/)
- [Ingress](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/)

## ✅ 学习检查

- [ ] 理解 Service 的作用和工作原理
- [ ] 掌握 ClusterIP、NodePort 的使用
- [ ] 能够创建和管理 Service
- [ ] 理解 Service 和 Pod 的关联关系
- [ ] 会排查 Service 访问问题

## 🎯 下一步

完成本节学习后，继续学习 [04 - ConfigMap 和 Secret](./04-configmap-secret.md)，了解如何管理配置和敏感信息。
