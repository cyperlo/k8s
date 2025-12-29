# 02 - Deployment 部署

## 📖 概念介绍

Deployment 是 Kubernetes 中用于管理无状态应用的控制器，它提供了声明式的应用部署和更新能力。

### 核心概念

- **Deployment**：管理 Pod 副本的控制器
- **ReplicaSet**：确保指定数量的 Pod 副本运行
- **滚动更新**：零停机更新应用
- **回滚**：快速恢复到之前的版本

### 为什么使用 Deployment？

- ✅ 自动管理 Pod 副本数量
- ✅ 支持滚动更新和回滚
- ✅ 自动重启失败的 Pod
- ✅ 声明式配置，易于管理

## 📝 配置文件

```yaml
# Deployment 示例 - 部署 3 个副本的 Nginx
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

## 🔍 配置说明

| 字段 | 说明 |
|------|------|
| `apiVersion: apps/v1` | API 版本 |
| `kind: Deployment` | 资源类型 |
| `spec.replicas` | Pod 副本数量 |
| `spec.selector` | 选择器，匹配要管理的 Pod |
| `spec.template` | Pod 模板 |
| `resources.requests` | 资源请求（最小保证） |
| `resources.limits` | 资源限制（最大使用） |

## 🚀 部署步骤

### 1. 创建 Deployment

```bash
# 应用配置文件
kubectl apply -f 02-deployment.yaml

# 查看 Deployment
kubectl get deployments

# 查看 ReplicaSet
kubectl get rs

# 查看 Pod
kubectl get pods
```

### 2. 查看部署状态

```bash
# 查看 Deployment 详情
kubectl describe deployment nginx-deployment

# 查看滚动更新状态
kubectl rollout status deployment/nginx-deployment

# 查看滚动更新历史
kubectl rollout history deployment/nginx-deployment
```

## 🔄 滚动更新

### 更新镜像版本

```bash
# 方法 1：使用 kubectl set image
kubectl set image deployment/nginx-deployment nginx=nginx:1.22

# 方法 2：编辑 Deployment
kubectl edit deployment nginx-deployment

# 方法 3：修改 YAML 文件后重新应用
# 修改 image: nginx:1.22
kubectl apply -f 02-deployment.yaml

# 查看更新过程
kubectl rollout status deployment/nginx-deployment

# 查看 Pod 变化
kubectl get pods -w
```

### 回滚到上一个版本

```bash
# 回滚到上一个版本
kubectl rollout undo deployment/nginx-deployment

# 回滚到指定版本
kubectl rollout undo deployment/nginx-deployment --to-revision=2

# 查看历史版本
kubectl rollout history deployment/nginx-deployment
```

## 📊 扩缩容

### 手动扩缩容

```bash
# 扩容到 5 个副本
kubectl scale deployment nginx-deployment --replicas=5

# 查看 Pod 数量变化
kubectl get pods

# 缩容到 2 个副本
kubectl scale deployment nginx-deployment --replicas=2
```

### 自动扩缩容（HPA）

```bash
# 创建 HPA（需要 metrics-server）
kubectl autoscale deployment nginx-deployment --min=2 --max=10 --cpu-percent=80

# 查看 HPA
kubectl get hpa
```

## 🧪 实践练习

### 练习 1：修改副本数量

将副本数量改为 5：

```yaml
spec:
  replicas: 5  # 修改副本数
```

### 练习 2：添加环境变量

```yaml
containers:
- name: nginx
  image: nginx:1.21
  env:
  - name: ENVIRONMENT
    value: "production"
```

### 练习 3：配置健康检查

```yaml
containers:
- name: nginx
  image: nginx:1.21
  ports:
  - containerPort: 80
  livenessProbe:
    httpGet:
      path: /
      port: 80
    initialDelaySeconds: 3
    periodSeconds: 3
  readinessProbe:
    httpGet:
      path: /
      port: 80
    initialDelaySeconds: 5
    periodSeconds: 5
```

## 🔧 常用命令

```bash
# 查看 Deployment
kubectl get deployments
kubectl get deploy  # 简写

# 查看详细信息
kubectl describe deployment <deployment-name>

# 查看 Deployment 管理的 Pod
kubectl get pods -l app=nginx

# 扩缩容
kubectl scale deployment <deployment-name> --replicas=<number>

# 更新镜像
kubectl set image deployment/<deployment-name> <container-name>=<new-image>

# 查看更新状态
kubectl rollout status deployment/<deployment-name>

# 暂停更新
kubectl rollout pause deployment/<deployment-name>

# 恢复更新
kubectl rollout resume deployment/<deployment-name>

# 回滚
kubectl rollout undo deployment/<deployment-name>

# 删除 Deployment
kubectl delete deployment <deployment-name>
```

## 🐛 故障排查

### Pod 无法启动

```bash
# 查看 Deployment 事件
kubectl describe deployment nginx-deployment

# 查看 Pod 状态
kubectl get pods
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>
```

### 滚动更新卡住

```bash
# 查看更新状态
kubectl rollout status deployment/nginx-deployment

# 查看 ReplicaSet
kubectl get rs

# 回滚到上一个版本
kubectl rollout undo deployment/nginx-deployment
```

## 💡 最佳实践

1. **始终设置资源限制**：避免单个 Pod 占用过多资源
2. **使用健康检查**：确保只有健康的 Pod 接收流量
3. **保留历史版本**：方便快速回滚
4. **使用标签**：便于管理和选择 Pod
5. **声明式配置**：使用 YAML 文件而不是命令行

## 📚 扩展阅读

- [Deployment 官方文档](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/deployment/)
- [滚动更新策略](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/deployment/#strategy)
- [ReplicaSet](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/replicaset/)

## ✅ 学习检查

- [ ] 理解 Deployment 的作用
- [ ] 能够创建和管理 Deployment
- [ ] 掌握滚动更新和回滚操作
- [ ] 会进行手动扩缩容
- [ ] 理解资源请求和限制

## 🎯 下一步

完成本节学习后，继续学习 [03 - Service 服务暴露](./03-service.md)，了解如何暴露和访问应用。
