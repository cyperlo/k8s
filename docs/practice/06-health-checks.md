# 06 - 健康检查探针

## 📖 概念介绍

Kubernetes 提供三种探针来检查容器的健康状态，确保应用的高可用性。

### 核心概念

- **Liveness Probe**：存活探针，检查容器是否还在运行
- **Readiness Probe**：就绪探针，检查容器是否准备好接收流量
- **Startup Probe**：启动探针，检查容器是否已启动

## 📝 配置文件

```yaml
# 健康检查示例
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-probes
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: nginx:1.21
        ports:
        - containerPort: 80
        
        # 存活探针 - 检查容器是否还在运行
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15  # 容器启动后等待 15 秒
          periodSeconds: 10         # 每 10 秒检查一次
          timeoutSeconds: 3         # 超时时间 3 秒
          failureThreshold: 3       # 失败 3 次后重启容器
        
        # 就绪探针 - 检查容器是否准备好接收流量
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 2
          successThreshold: 1       # 成功 1 次即认为就绪
          failureThreshold: 3
        
        # 启动探针 - 检查容器是否已启动（适用于启动慢的应用）
        startupProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 30      # 最多等待 150 秒（5*30）
        
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

## 🔍 探针类型

### 1. HTTP GET
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
    httpHeaders:
    - name: Custom-Header
      value: Awesome
```

### 2. TCP Socket
```yaml
livenessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 15
  periodSeconds: 10
```

### 3. Exec Command
```yaml
livenessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 🚀 部署步骤

```bash
# 1. 部署应用
kubectl apply -f 06-health-checks.yaml

# 2. 查看 Pod 状态
kubectl get pods

# 3. 查看探针状态
kubectl describe pod <pod-name>

# 4. 模拟失败
kubectl exec <pod-name> -- rm /usr/share/nginx/html/index.html
# 观察 Pod 被重启
```

## 💡 最佳实践

1. **始终配置健康检查**
2. **合理设置延迟和超时**
3. **区分存活和就绪探针**
4. **避免探针过于频繁**

## 📚 扩展阅读

- [容器探针官方文档](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)

## ✅ 学习检查

- [ ] 理解三种探针的区别
- [ ] 会配置不同类型的探针
- [ ] 理解探针参数的含义

## 🎯 下一步

继续学习 [07 - Ingress 流量管理](./07-ingress.md)。

---

[📥 下载完整 YAML 文件](/k8s-practice/06-health-checks.yaml)
