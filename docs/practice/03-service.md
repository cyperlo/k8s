# 03 - Service 服务暴露

## 📖 概念介绍

Service 是 Kubernetes 中用于暴露应用的抽象层，它为一组 Pod 提供统一的访问入口和负载均衡。

### 核心概念

- **Service**：为 Pod 提供稳定的网络访问
- **ClusterIP**：集群内部访问（默认）
- **NodePort**：通过节点端口访问
- **LoadBalancer**：云平台负载均衡器
- **Selector**：选择要暴露的 Pod

## 📝 配置文件

```yaml
# Service 示例 - 暴露 Nginx 服务
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  type: NodePort
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    # nodePort: 30080  # 可选：指定 NodePort 端口（范围 30000-32767）
```

## 🔍 Service 类型

### 1. ClusterIP（默认）

集群内部访问，适合内部服务通信：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

### 2. NodePort

通过节点 IP + 端口访问：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080  # 30000-32767
```

### 3. LoadBalancer

云平台负载均衡器（需要云平台支持）：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-lb
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

## 🚀 部署步骤

### 1. 创建 Service

```bash
# 先确保有 Deployment
kubectl apply -f 02-deployment.yaml

# 创建 Service
kubectl apply -f 03-service.yaml

# 查看 Service
kubectl get services
kubectl get svc  # 简写
```

### 2. 访问 Service

```bash
# 查看 Service 详情
kubectl describe service nginx-service

# 获取 Service 的 Endpoints
kubectl get endpoints nginx-service

# Minikube 访问 NodePort Service
minikube service nginx-service

# 或手动访问
# NodePort 方式：http://<node-ip>:<node-port>
```

## 🧪 实践练习

### 练习 1：ClusterIP Service

创建集群内部服务：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-internal
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - port: 8080
    targetPort: 80
```

测试访问：

```bash
# 创建测试 Pod
kubectl run test-pod --image=busybox --rm -it -- sh

# 在 Pod 内访问
wget -O- http://nginx-internal:8080
```

### 练习 2：多端口 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
spec:
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: https
    port: 443
    targetPort: 8443
```

## 🔧 常用命令

```bash
# 查看 Service
kubectl get services
kubectl get svc

# 查看详细信息
kubectl describe service <service-name>

# 查看 Endpoints
kubectl get endpoints <service-name>

# 删除 Service
kubectl delete service <service-name>

# 通过标签选择 Service
kubectl get svc -l app=nginx
```

## 📚 扩展阅读

- [Service 官方文档](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/)
- [DNS for Services](https://kubernetes.io/zh-cn/docs/concepts/services-networking/dns-pod-service/)

## ✅ 学习检查

- [ ] 理解 Service 的作用
- [ ] 掌握三种 Service 类型
- [ ] 能够创建和访问 Service
- [ ] 理解 Selector 和 Endpoints

## 🎯 下一步

继续学习 [04 - ConfigMap 和 Secret](./04-configmap-secret.md)。
