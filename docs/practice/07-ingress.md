# 07 - Ingress 流量管理

## 📖 概念介绍

Ingress 是 Kubernetes 中用于管理外部访问集群服务的 API 对象，提供 HTTP/HTTPS 路由功能。

### 核心概念

- **Ingress**：定义路由规则
- **Ingress Controller**：实现路由规则的控制器
- **路径路由**：基于 URL 路径分发流量
- **主机路由**：基于域名分发流量

## 📝 配置文件

```yaml
# Ingress 示例 - HTTP 路由
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8080

---
# Ingress with TLS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress-tls
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

## 🚀 部署步骤

```bash
# 1. 安装 Ingress Controller（Minikube）
minikube addons enable ingress

# 2. 创建 Ingress
kubectl apply -f 07-ingress.yaml

# 3. 查看 Ingress
kubectl get ingress
kubectl describe ingress app-ingress

# 4. 配置 hosts
echo "$(minikube ip) myapp.example.com" | sudo tee -a /etc/hosts

# 5. 访问应用
curl http://myapp.example.com/
curl http://myapp.example.com/api
```

## 💡 最佳实践

1. **使用 TLS 加密**
2. **配置合理的超时时间**
3. **使用注解自定义行为**
4. **监控 Ingress 性能**

## 📚 扩展阅读

- [Ingress 官方文档](https://kubernetes.io/zh-cn/docs/concepts/services-networking/ingress/)

## ✅ 学习检查

- [ ] 理解 Ingress 的作用
- [ ] 会配置路径和主机路由
- [ ] 了解 TLS 配置

## 🎯 下一步

继续学习 [08 - Namespace 资源隔离](./08-namespace.md)。

---

[📥 下载完整 YAML 文件](/k8s-practice/07-ingress.yaml)
