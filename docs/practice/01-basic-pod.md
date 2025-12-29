# 01 - 基础 Pod 配置

## 📖 概念介绍

Pod 是 Kubernetes 中最小的部署单元，一个 Pod 可以包含一个或多个容器。Pod 中的容器共享网络命名空间和存储卷。

### 核心概念

- **Pod**：Kubernetes 中最小的可部署单元
- **Container**：Pod 中运行的容器
- **Label**：用于标识和选择资源的键值对
- **Port**：容器暴露的端口

## 📝 配置文件

```yaml
# 基础 Pod 示例
apiVersion: v1
kind: Pod
metadata:
  name: my-first-pod
  labels:
    app: demo
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

## 🔍 配置说明

| 字段 | 说明 |
|------|------|
| `apiVersion: v1` | API 版本，Pod 使用 v1 |
| `kind: Pod` | 资源类型为 Pod |
| `metadata.name` | Pod 的名称，在命名空间内唯一 |
| `metadata.labels` | 标签，用于标识和选择 Pod |
| `spec.containers` | 容器列表 |
| `containers[].name` | 容器名称 |
| `containers[].image` | 容器镜像 |
| `containers[].ports` | 容器暴露的端口 |

## 🚀 部署步骤

### 1. 创建 Pod

```bash
# 应用配置文件
kubectl apply -f 01-basic-pod.yaml

# 查看 Pod 状态
kubectl get pods

# 查看详细信息
kubectl describe pod my-first-pod
```

### 2. 验证 Pod

```bash
# 查看 Pod 日志
kubectl logs my-first-pod

# 进入 Pod 容器
kubectl exec -it my-first-pod -- /bin/bash

# 在容器内测试 Nginx
curl localhost
```

### 3. 端口转发访问

```bash
# 将本地端口 8080 转发到 Pod 的 80 端口
kubectl port-forward my-first-pod 8080:80

# 在另一个终端访问
curl http://localhost:8080
```

## 🧪 实践练习

### 练习 1：修改镜像版本

尝试将 Nginx 版本从 1.21 改为 1.22：

```yaml
containers:
- name: nginx
  image: nginx:1.22  # 修改版本
  ports:
  - containerPort: 80
```

### 练习 2：添加环境变量

为容器添加环境变量：

```yaml
containers:
- name: nginx
  image: nginx:1.21
  env:
  - name: MY_ENV
    value: "Hello Kubernetes"
  ports:
  - containerPort: 80
```

### 练习 3：多容器 Pod

创建一个包含两个容器的 Pod：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
  - name: busybox
    image: busybox
    command: ['sh', '-c', 'while true; do echo "Hello from busybox"; sleep 10; done']
```

## 🔧 常用命令

```bash
# 查看所有 Pod
kubectl get pods

# 查看 Pod 详细信息
kubectl describe pod <pod-name>

# 查看 Pod 日志
kubectl logs <pod-name>

# 实时查看日志
kubectl logs -f <pod-name>

# 进入 Pod 容器
kubectl exec -it <pod-name> -- /bin/bash

# 删除 Pod
kubectl delete pod <pod-name>

# 或使用配置文件删除
kubectl delete -f 01-basic-pod.yaml
```

## 🐛 故障排查

### Pod 一直处于 Pending 状态

```bash
# 查看详细信息
kubectl describe pod my-first-pod

# 常见原因：
# 1. 资源不足（CPU、内存）
# 2. 镜像拉取失败
# 3. 节点选择器不匹配
```

### Pod 处于 CrashLoopBackOff 状态

```bash
# 查看日志
kubectl logs my-first-pod

# 查看上一次运行的日志
kubectl logs my-first-pod --previous

# 常见原因：
# 1. 容器启动命令错误
# 2. 应用程序崩溃
# 3. 配置错误
```

### 镜像拉取失败

```bash
# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 常见原因：
# 1. 镜像名称错误
# 2. 网络问题
# 3. 私有镜像需要认证
```

## 📚 扩展阅读

- [Pod 官方文档](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/)
- [Pod 生命周期](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/)
- [容器探针](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)

## ✅ 学习检查

- [ ] 理解 Pod 的概念和作用
- [ ] 能够创建和删除 Pod
- [ ] 会查看 Pod 日志和状态
- [ ] 能够进入 Pod 容器进行调试
- [ ] 理解 Pod 的生命周期

## 🎯 下一步

完成本节学习后，继续学习 [02 - Deployment 部署](./02-deployment.md)，了解如何管理多副本应用。
