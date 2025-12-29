# Kubernetes 实践示例

这个目录包含了 Kubernetes 学习过程中的实践示例配置文件。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `01-basic-pod.yaml` | 基础 Pod 配置 |
| `02-deployment.yaml` | Deployment 部署示例 |
| `03-service.yaml` | Service 服务暴露 |
| `04-configmap-secret.yaml` | ConfigMap 和 Secret 配置管理 |
| `05-persistent-volume.yaml` | 持久化存储配置 |
| `06-health-checks.yaml` | 健康检查探针配置 |
| `07-ingress.yaml` | Ingress 流量管理 |
| `08-namespace.yaml` | Namespace 和资源配额 |
| `09-hpa.yaml` | 水平自动扩缩容 |

## 🚀 使用方法

### 1. 应用配置
```bash
# 应用单个文件
kubectl apply -f 01-basic-pod.yaml

# 应用整个目录
kubectl apply -f .

# 应用特定文件
kubectl apply -f 02-deployment.yaml -f 03-service.yaml
```

### 2. 查看资源
```bash
# 查看所有 Pod
kubectl get pods

# 查看 Deployment
kubectl get deployments

# 查看 Service
kubectl get services

# 查看所有资源
kubectl get all

# 详细信息
kubectl describe pod <pod-name>
```

### 3. 删除资源
```bash
# 删除单个资源
kubectl delete -f 01-basic-pod.yaml

# 删除所有资源
kubectl delete -f .

# 按类型删除
kubectl delete deployment nginx-deployment
kubectl delete service nginx-service
```

## 📝 学习顺序建议

1. **01-basic-pod.yaml** - 从最简单的 Pod 开始
2. **02-deployment.yaml** - 学习如何管理多副本应用
3. **03-service.yaml** - 了解服务发现和负载均衡
4. **04-configmap-secret.yaml** - 配置管理
5. **05-persistent-volume.yaml** - 数据持久化
6. **06-health-checks.yaml** - 健康检查机制
7. **08-namespace.yaml** - 资源隔离
8. **07-ingress.yaml** - 流量管理（需要先安装 Ingress Controller）
9. **09-hpa.yaml** - 自动扩缩容（需要 Metrics Server）

## 🔧 前置要求

### 安装 Ingress Controller（用于 07-ingress.yaml）
```bash
# Minikube
minikube addons enable ingress

# 或使用 Helm 安装 nginx-ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx
```

### 安装 Metrics Server（用于 09-hpa.yaml）
```bash
# Minikube
minikube addons enable metrics-server

# 或手动安装
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

## 💡 常用命令速查

```bash
# 查看日志
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 实时查看

# 进入容器
kubectl exec -it <pod-name> -- /bin/bash

# 端口转发
kubectl port-forward <pod-name> 8080:80

# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp

# 查看资源使用
kubectl top nodes
kubectl top pods

# 编辑资源
kubectl edit deployment <deployment-name>

# 扩缩容
kubectl scale deployment <deployment-name> --replicas=5

# 滚动更新
kubectl set image deployment/<deployment-name> <container-name>=<new-image>

# 回滚
kubectl rollout undo deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
```

## 🎯 实践建议

1. **逐个文件学习**：不要一次性应用所有文件，按顺序逐个学习
2. **修改参数**：尝试修改配置参数，观察变化
3. **查看日志**：使用 `kubectl describe` 和 `kubectl logs` 了解详情
4. **故意制造错误**：比如使用错误的镜像名，学习如何排查问题
5. **清理资源**：学习完记得删除资源，避免占用系统资源

## 📚 相关文档

- [Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/home/)
- [kubectl 命令参考](https://kubernetes.io/docs/reference/kubectl/)
- [API 参考](https://kubernetes.io/docs/reference/kubernetes-api/)
