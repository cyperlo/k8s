# 08 - Namespace 资源隔离

## 📖 概念介绍

Namespace 提供了一种在单个集群中隔离资源的机制，适用于多租户、多环境场景。

### 核心概念

- **Namespace**：命名空间，资源隔离
- **ResourceQuota**：资源配额限制
- **LimitRange**：默认资源限制

## 📝 配置文件

```yaml
# Namespace 示例
apiVersion: v1
kind: Namespace
metadata:
  name: development

---
apiVersion: v1
kind: Namespace
metadata:
  name: production

---
# ResourceQuota - 限制命名空间资源使用
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: development
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "50"

---
# LimitRange - 设置默认资源限制
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limit-range
  namespace: development
spec:
  limits:
  - default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 100m
      memory: 128Mi
    type: Container
```

## 🚀 部署步骤

```bash
# 1. 创建 Namespace
kubectl apply -f 08-namespace.yaml

# 2. 查看 Namespace
kubectl get namespaces

# 3. 在指定 Namespace 中创建资源
kubectl apply -f deployment.yaml -n development

# 4. 查看资源配额
kubectl describe quota dev-quota -n development

# 5. 切换默认 Namespace
kubectl config set-context --current --namespace=development
```

## 💡 最佳实践

1. **使用 Namespace 隔离环境**
2. **设置资源配额**
3. **配置默认限制**
4. **使用 RBAC 控制访问**

## 📚 扩展阅读

- [Namespace 官方文档](https://kubernetes.io/zh-cn/docs/concepts/overview/working-with-objects/namespaces/)

## ✅ 学习检查

- [ ] 理解 Namespace 的作用
- [ ] 会创建和管理 Namespace
- [ ] 了解资源配额和限制

## 🎯 下一步

继续学习 [09 - 水平自动扩缩容](./09-hpa.md)。

---

[📥 下载完整 YAML 文件](/k8s-practice/08-namespace.yaml)
