# Kubernetes (K8s) 快速入门学习路线

## 📚 学习路线概览

这是一个为期 4-6 周的 Kubernetes 学习计划，适合有基础 Linux 和 Docker 知识的开发者。

---

## 第一周：基础概念与环境搭建

### 1. 理解容器化基础
- **Docker 基础回顾**（如果不熟悉）
  - 容器 vs 虚拟机
  - Docker 镜像和容器
  - Dockerfile 编写

### 2. Kubernetes 核心概念
- **什么是 Kubernetes？**
  - 容器编排的必要性
  - K8s 的优势和应用场景
  - K8s 架构概览

- **核心组件**
  - Master 节点：API Server、Scheduler、Controller Manager、etcd
  - Worker 节点：Kubelet、Kube-proxy、Container Runtime

### 3. 本地环境搭建
选择一个工具开始实践：
- **Minikube**（推荐新手）
- **Kind** (Kubernetes in Docker)
- **Docker Desktop** 内置 K8s
- **K3s**（轻量级）

### 实践任务 - Linux 环境搭建

#### 安装 kubectl
```bash
# 下载最新版本
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 添加执行权限
chmod +x kubectl

# 移动到系统路径
sudo mv kubectl /usr/local/bin/

# 验证安装
kubectl version --client
```

#### 安装 Minikube
```bash
# 下载 Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# 安装
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 验证安装
minikube version
```

#### 启动 Kubernetes 集群
```bash
# 启动集群（使用 Docker 驱动）
minikube start --driver=docker

# 如果没有 Docker，可以使用 VirtualBox
# minikube start --driver=virtualbox

# 验证集群状态
kubectl cluster-info
kubectl get nodes

# 查看 Minikube 状态
minikube status

# 启用常用插件
minikube addons enable dashboard
minikube addons enable metrics-server
minikube addons enable ingress
```

#### 配置 kubectl 自动补全（可选但推荐）
```bash
# Bash
echo 'source <(kubectl completion bash)' >>~/.bashrc
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
source ~/.bashrc

# Zsh
echo 'source <(kubectl completion zsh)' >>~/.zshrc
echo 'alias k=kubectl' >>~/.zshrc
source ~/.zshrc
```

---

## 第二周：核心资源对象

### 1. Pod - 最小部署单元
- Pod 的概念和生命周期
- 单容器 vs 多容器 Pod
- Pod 的创建和管理

### 2. Deployment - 应用部署
- 声明式部署
- 滚动更新和回滚
- 副本管理

### 3. Service - 服务发现
- ClusterIP、NodePort、LoadBalancer
- 服务暴露和访问
- DNS 解析

### 实践任务
创建一个简单的 Web 应用：

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-demo
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
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: NodePort
```

```bash
# 部署应用
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 查看资源
kubectl get pods
kubectl get deployments
kubectl get services

# 访问应用
minikube service nginx-service
```

---

## 第三周：配置与存储

### 1. ConfigMap - 配置管理
- 配置与代码分离
- 创建和使用 ConfigMap
- 环境变量注入

### 2. Secret - 敏感信息管理
- Secret 类型
- 创建和使用 Secret
- 最佳实践

### 3. Volume - 数据持久化
- Volume 类型
- PersistentVolume (PV)
- PersistentVolumeClaim (PVC)
- StorageClass

### 实践任务
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "mysql://db:3306"
  log_level: "info"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  password: cGFzc3dvcmQxMjM=  # base64 编码

---
# deployment-with-config.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-config
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
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: database_url
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: password
```

---

## 第四周：高级特性

### 1. Namespace - 资源隔离
- 多租户管理
- 资源配额
- 网络策略

### 2. Ingress - 流量管理
- Ingress Controller
- 路由规则
- TLS/SSL 配置

### 3. 健康检查
- Liveness Probe（存活探针）
- Readiness Probe（就绪探针）
- Startup Probe（启动探针）

### 4. 资源管理
- Resource Requests
- Resource Limits
- HPA（水平自动扩缩容）

### 实践任务
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prod
  template:
    metadata:
      labels:
        app: prod
    spec:
      containers:
      - name: app
        image: nginx:1.21
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## 第五周：实战项目

### 项目：部署一个完整的微服务应用

**架构组成：**
1. 前端服务（Nginx 静态页面）
2. 后端 API（Python Flask）
3. 数据库（MySQL）
4. Redis 缓存
5. Ingress 统一入口

**要求：**
- 使用 Deployment 部署所有服务
- 配置 Service 实现服务间通信
- 使用 ConfigMap 和 Secret 管理配置
- 配置 PV/PVC 持久化数据库数据
- 使用 Ingress 暴露服务
- 配置健康检查和资源限制

**详细实现请查看 `demo-microservice/` 目录**

---

## 第六周：运维与最佳实践

### 1. 日志与监控
- kubectl logs 查看日志
- Prometheus + Grafana 监控
- ELK/EFK 日志收集

### 2. 故障排查
```bash
# 常用调试命令
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- /bin/bash
kubectl get events
kubectl top nodes
kubectl top pods
```

### 3. 最佳实践
- 使用声明式配置（YAML）
- 版本控制所有配置文件
- 使用 Namespace 隔离环境
- 设置资源限制
- 实施安全策略
- 定期备份 etcd

### 4. CI/CD 集成
- GitOps 工作流
- ArgoCD / Flux
- Helm 包管理

---

## 📖 推荐学习资源

### 官方文档
- [Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/home/)
- [Kubernetes 中文社区](https://www.kubernetes.org.cn/)

### 在线教程
- [Kubernetes 官方交互式教程](https://kubernetes.io/zh-cn/docs/tutorials/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

### 书籍推荐
- 《Kubernetes in Action》
- 《Kubernetes 权威指南》
- 《深入剖析 Kubernetes》

### 视频课程
- B站搜索 "Kubernetes 入门"
- YouTube: "Kubernetes Tutorial for Beginners"

---

## 🎯 学习检查清单

### 基础知识
- [ ] 理解容器和容器编排
- [ ] 了解 K8s 架构和核心组件
- [ ] 成功搭建本地 K8s 环境

### 核心概念
- [ ] 创建和管理 Pod
- [ ] 使用 Deployment 部署应用
- [ ] 配置 Service 暴露服务
- [ ] 理解 Label 和 Selector

### 配置管理
- [ ] 使用 ConfigMap 管理配置
- [ ] 使用 Secret 管理敏感信息
- [ ] 配置 Volume 持久化数据

### 高级特性
- [ ] 使用 Namespace 隔离资源
- [ ] 配置 Ingress 管理流量
- [ ] 设置健康检查
- [ ] 配置资源限制和 HPA

### 实战能力
- [ ] 独立部署完整应用
- [ ] 能够排查常见问题
- [ ] 理解 K8s 最佳实践

---

## 💡 学习建议

1. **动手实践最重要**：每学一个概念都要亲自操作
2. **从简单开始**：先掌握核心概念，再深入高级特性
3. **多看官方文档**：最权威、最准确的信息来源
4. **加入社区**：遇到问题可以在社区寻求帮助
5. **做笔记**：记录常用命令和配置模板
6. **持续学习**：K8s 生态在不断发展，保持学习

---

## 🚀 下一步

完成基础学习后，可以继续深入：
- **服务网格**：Istio、Linkerd
- **无服务器**：Knative
- **安全加固**：RBAC、Pod Security Policy
- **多集群管理**：Federation
- **云原生生态**：CNCF 项目

祝你学习顺利！🎉
