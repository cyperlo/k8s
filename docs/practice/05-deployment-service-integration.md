# Deployment + Service 完整实战

## 📖 核心概念

### 三者关系

```
Deployment（部署控制器）
    ↓ 创建和管理
Pod（应用实例）
    ↑ 通过标签选择
Service（服务暴露）
```

**简单理解：**
- **Deployment**：负责创建和管理 Pod（保证有 3 个 Nginx 在运行）
- **Pod**：实际运行的应用容器（3 个 Nginx 实例）
- **Service**：提供统一的访问入口（一个固定的地址访问这 3 个 Nginx）

## 🔗 如何关联

### 关键：标签（Label）

Deployment 和 Service 通过**标签**关联：

```yaml
# Deployment 给 Pod 打标签
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    metadata:
      labels:
        app: web  # ← 这是关键！
    spec:
      containers:
      - name: nginx
        image: nginx

---
# Service 通过标签选择 Pod
apiVersion: v1
kind: Service
spec:
  selector:
    app: web  # ← 选择 app=web 的 Pod
  ports:
  - port: 80
```

## 🎯 实战案例 1：简单 Web 应用

### 场景
部署一个 Nginx Web 应用，3 个副本，通过 NodePort 暴露

### 完整配置

```yaml
# 1. Deployment：管理 Pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-web
spec:
  replicas: 3  # 3 个 Pod
  selector:
    matchLabels:
      app: web  # 必须和下面的 labels 一致
  template:
    metadata:
      labels:
        app: web  # Pod 的标签
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80

---
# 2. Service：暴露 Pod
apiVersion: v1
kind: Service
metadata:
  name: my-web-service
spec:
  type: NodePort
  selector:
    app: web  # 选择 app=web 的 Pod
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

### 部署步骤

```bash
# 1. 应用配置
kubectl apply -f my-web.yaml

# 2. 查看 Deployment
kubectl get deployment my-web
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# my-web   3/3     3            3           10s

# 3. 查看 Pod
kubectl get pods -l app=web
# NAME                      READY   STATUS    RESTARTS   AGE
# my-web-5d4f8c9b7d-abc12   1/1     Running   0          10s
# my-web-5d4f8c9b7d-def34   1/1     Running   0          10s
# my-web-5d4f8c9b7d-ghi56   1/1     Running   0          10s

# 4. 查看 Service
kubectl get svc my-web-service
# NAME             TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# my-web-service   NodePort   10.96.123.45    <none>        80:30080/TCP   10s

# 5. 查看 Endpoints（Service 找到的 Pod）
kubectl get endpoints my-web-service
# NAME             ENDPOINTS                                   AGE
# my-web-service   10.244.0.5:80,10.244.0.6:80,10.244.0.7:80   10s

# 6. 访问服务
curl http://localhost:30080
```

### 验证关联

```bash
# 查看 Service 选择了哪些 Pod
kubectl describe svc my-web-service
# Selector:          app=web
# Endpoints:         10.244.0.5:80,10.244.0.6:80,10.244.0.7:80

# 查看 Pod 的标签
kubectl get pods --show-labels
# NAME                      READY   STATUS    LABELS
# my-web-5d4f8c9b7d-abc12   1/1     Running   app=web,pod-template-hash=5d4f8c9b7d
```

## 🎯 实战案例 2：前后端分离

### 场景
- 前端：Nginx，2 个副本，NodePort 暴露
- 后端：API，3 个副本，ClusterIP（内部访问）
- 前端通过 Service 名称调用后端

### 架构图

```
外部用户
   ↓
NodePort (30090)
   ↓
Frontend Service (ClusterIP)
   ↓
Frontend Pod × 2
   ↓
Backend Service (ClusterIP)
   ↓
Backend Pod × 3
```

### 完整配置

```yaml
# 后端 Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
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
        image: hashicorp/http-echo
        args: ["-text=Backend API Response"]
        ports:
        - containerPort: 5678

---
# 后端 Service（ClusterIP）
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP  # 只在集群内访问
  selector:
    app: backend
  ports:
  - port: 8080
    targetPort: 5678

---
# 前端 Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_URL
          value: "http://backend-service:8080"  # 通过 Service 名称访问

---
# 前端 Service（NodePort）
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30090
```

### 测试步骤

```bash
# 1. 部署
kubectl apply -f frontend-backend.yaml

# 2. 查看所有资源
kubectl get all

# 3. 测试后端（集群内）
kubectl run test --rm -it --image=busybox --restart=Never -- \
  wget -O- http://backend-service:8080

# 4. 进入前端 Pod，测试调用后端
kubectl exec -it deployment/frontend -- sh
# 在 Pod 内：
curl http://backend-service:8080

# 5. 访问前端（外部）
curl http://localhost:30090
```

## 🔍 工作原理详解

### 1. 标签选择器

```yaml
# Deployment 的选择器
spec:
  selector:
    matchLabels:
      app: web  # Deployment 管理带有这个标签的 Pod

# Service 的选择器
spec:
  selector:
    app: web  # Service 转发流量到带有这个标签的 Pod
```

### 2. 端口映射

```
外部请求:30080
    ↓
Service:80 (port)
    ↓
Pod:80 (targetPort = containerPort)
    ↓
容器内应用
```

```yaml
# Deployment
containers:
- containerPort: 80  # 容器监听的端口

# Service
ports:
- port: 80           # Service 的端口
  targetPort: 80     # 转发到 Pod 的端口
  nodePort: 30080    # 外部访问端口
```

### 3. Endpoints 自动更新

```bash
# 初始状态：3 个 Pod
kubectl get endpoints my-web-service
# 10.244.0.5:80,10.244.0.6:80,10.244.0.7:80

# 扩容到 5 个
kubectl scale deployment my-web --replicas=5

# Endpoints 自动更新
kubectl get endpoints my-web-service
# 10.244.0.5:80,10.244.0.6:80,10.244.0.7:80,10.244.0.8:80,10.244.0.9:80
```

## 🧪 实践练习

### 练习 1：部署一个完整应用

1. 创建 Deployment，3 个 Nginx 副本
2. 创建 NodePort Service
3. 验证可以访问
4. 扩容到 5 个副本
5. 验证负载均衡

### 练习 2：前后端应用

1. 部署后端 API（ClusterIP）
2. 部署前端 Web（NodePort）
3. 前端调用后端
4. 测试服务发现

### 练习 3：故障恢复

```bash
# 1. 部署应用
kubectl apply -f my-web.yaml

# 2. 删除一个 Pod
kubectl delete pod <pod-name>

# 3. 观察 Deployment 自动创建新 Pod
kubectl get pods -w

# 4. Service 自动更新 Endpoints
kubectl get endpoints my-web-service
```

## 🐛 常见问题

### 问题 1：Service 无法访问

**症状：** 访问 Service 超时或拒绝连接

**排查步骤：**

```bash
# 1. 检查 Service 是否存在
kubectl get svc

# 2. 检查 Endpoints 是否有 Pod IP
kubectl get endpoints <service-name>

# 如果 Endpoints 为空，说明 Service 没有找到 Pod

# 3. 检查标签是否匹配
kubectl get pods --show-labels
kubectl describe svc <service-name>  # 查看 Selector

# 4. 检查 Pod 是否正常运行
kubectl get pods
kubectl describe pod <pod-name>
```

### 问题 2：标签不匹配

**错误示例：**

```yaml
# Deployment
template:
  metadata:
    labels:
      app: web  # ← 标签是 web

# Service
spec:
  selector:
    app: webapp  # ← 选择器是 webapp（不匹配！）
```

**正确做法：** 确保标签一致

### 问题 3：端口配置错误

```yaml
# 容器监听 8080
containers:
- containerPort: 8080

# Service 转发到 80（错误！）
ports:
- targetPort: 80  # 应该是 8080
```

## 💡 最佳实践

### 1. 使用有意义的标签

```yaml
labels:
  app: web
  tier: frontend
  version: v1.0
  environment: production
```

### 2. 一个文件管理相关资源

```yaml
# my-app.yaml
---
apiVersion: apps/v1
kind: Deployment
# ...

---
apiVersion: v1
kind: Service
# ...
```

### 3. 使用命名端口

```yaml
# Deployment
ports:
- name: http
  containerPort: 80

# Service
ports:
- port: 80
  targetPort: http  # 引用端口名称
```

### 4. 配置健康检查

```yaml
containers:
- name: app
  livenessProbe:
    httpGet:
      path: /health
      port: 80
  readinessProbe:
    httpGet:
      path: /ready
      port: 80
```

### 5. 设置资源限制

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

## 🔧 常用命令速查

```bash
# 部署
kubectl apply -f app.yaml

# 查看资源
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get endpoints

# 查看详情
kubectl describe deployment <name>
kubectl describe svc <name>

# 查看标签
kubectl get pods --show-labels

# 按标签筛选
kubectl get pods -l app=web

# 扩缩容
kubectl scale deployment <name> --replicas=5

# 测试访问
kubectl run test --rm -it --image=busybox --restart=Never -- wget -O- http://<service-name>

# 进入 Pod
kubectl exec -it <pod-name> -- sh

# 查看日志
kubectl logs <pod-name>

# 删除资源
kubectl delete -f app.yaml
```

## 📊 配置模板

### 标准 Web 应用模板

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
spec:
  replicas: 3
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      labels:
        app: <app-name>
    spec:
      containers:
      - name: <container-name>
        image: <image>
        ports:
        - containerPort: <port>
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: <app-name>-service
spec:
  type: NodePort
  selector:
    app: <app-name>
  ports:
  - port: <port>
    targetPort: <port>
    nodePort: <30000-32767>
```

## ✅ 学习检查

- [ ] 理解 Deployment、Pod、Service 的关系
- [ ] 掌握通过标签关联资源
- [ ] 能够部署完整的应用
- [ ] 理解端口映射关系
- [ ] 会排查连接问题
- [ ] 掌握服务发现机制

## 🎯 下一步

完成本节学习后，你已经掌握了 Kubernetes 的核心概念！接下来可以学习：
- ConfigMap 和 Secret（配置管理）
- Ingress（更优雅的服务暴露）
- StatefulSet（有状态应用）
- PersistentVolume（持久化存储）
