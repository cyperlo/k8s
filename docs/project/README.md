# 完整微服务应用 Demo

这是一个完整的微服务应用示例，包含前端、后端 API、数据库和缓存。

## 📐 架构图

```
                    Internet
                       |
                   [Ingress]
                       |
        +--------------+---------------+
        |                              |
   [Frontend]                    [Backend API]
   (Nginx静态页面)                (Flask Python)
        |                              |
        +-------------+----------------+
                      |
              +-------+--------+
              |                |
          [MySQL]          [Redis]
         (数据库)          (缓存)
```

## 🎯 功能说明

- **前端**：简单的 HTML 页面，展示用户列表
- **后端 API**：Flask REST API，提供用户 CRUD 操作
- **MySQL**：存储用户数据
- **Redis**：缓存热点数据
- **Ingress**：统一入口，路由分发

## 📁 文件结构

```
demo-microservice/
├── README.md                    # 本文件
├── app/                         # 应用代码
│   ├── backend/                 # 后端代码
│   │   ├── app.py              # Flask 应用
│   │   ├── requirements.txt    # Python 依赖
│   │   └── Dockerfile          # 后端镜像
│   └── frontend/               # 前端代码
│       ├── index.html          # 前端页面
│       ├── nginx.conf          # Nginx 配置
│       └── Dockerfile          # 前端镜像
├── k8s/                        # Kubernetes 配置
│   ├── 01-namespace.yaml       # 命名空间
│   ├── 02-configmap.yaml       # 配置
│   ├── 03-secret.yaml          # 密钥
│   ├── 04-mysql.yaml           # MySQL 部署
│   ├── 05-redis.yaml           # Redis 部署
│   ├── 06-backend.yaml         # 后端部署
│   ├── 07-frontend.yaml        # 前端部署
│   └── 08-ingress.yaml         # Ingress 配置
└── scripts/                    # 辅助脚本
    ├── build-images.sh         # 构建镜像
    ├── deploy.sh               # 部署应用
    ├── cleanup.sh              # 清理资源
    └── test-api.sh             # 测试 API
```

## 🚀 快速开始

### 前置要求

- 已安装 Docker
- 已安装 kubectl
- 已启动 Minikube 或其他 K8s 集群
- 已启用 Ingress 插件：`minikube addons enable ingress`

### 步骤 1：构建 Docker 镜像

```bash
# 进入项目目录
cd demo-microservice

# 构建镜像（使用 Minikube 的 Docker 环境）
eval $(minikube docker-env)

# 执行构建脚本
chmod +x scripts/*.sh
./scripts/build-images.sh
```

### 步骤 2：部署应用

```bash
# 部署所有资源
./scripts/deploy.sh

# 或手动部署
kubectl apply -f k8s/
```

### 步骤 3：验证部署

```bash
# 查看所有资源
kubectl get all -n demo-app

# 查看 Pod 状态
kubectl get pods -n demo-app

# 查看服务
kubectl get services -n demo-app

# 查看 Ingress
kubectl get ingress -n demo-app
```

### 步骤 4：访问应用

```bash
# 获取 Minikube IP
minikube ip

# 配置 hosts（将 IP 替换为实际的 Minikube IP）
echo "$(minikube ip) demo.local" | sudo tee -a /etc/hosts

# 访问前端
curl http://demo.local/

# 访问后端 API
curl http://demo.local/api/users

# 或在浏览器中打开
# http://demo.local/
# http://demo.local/api/users
```

### 步骤 5：测试 API

```bash
# 使用测试脚本
./scripts/test-api.sh

# 或手动测试
# 创建用户
curl -X POST http://demo.local/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com"}'

# 获取所有用户
curl http://demo.local/api/users

# 获取单个用户
curl http://demo.local/api/users/1

# 更新用户
curl -X PUT http://demo.local/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@updated.com"}'

# 删除用户
curl -X DELETE http://demo.local/api/users/1
```

## 📊 监控和调试

### 查看日志

```bash
# 查看后端日志
kubectl logs -f -n demo-app -l app=backend

# 查看前端日志
kubectl logs -f -n demo-app -l app=frontend

# 查看 MySQL 日志
kubectl logs -f -n demo-app -l app=mysql

# 查看 Redis 日志
kubectl logs -f -n demo-app -l app=redis
```

### 进入容器

```bash
# 进入后端容器
kubectl exec -it -n demo-app deployment/backend -- /bin/bash

# 进入 MySQL 容器
kubectl exec -it -n demo-app deployment/mysql -- mysql -uroot -prootpassword

# 进入 Redis 容器
kubectl exec -it -n demo-app deployment/redis -- redis-cli
```

### 查看资源使用

```bash
# 查看节点资源
kubectl top nodes

# 查看 Pod 资源
kubectl top pods -n demo-app
```

## 🧪 测试场景

### 1. 测试服务发现

```bash
# 进入后端 Pod
kubectl exec -it -n demo-app deployment/backend -- /bin/bash

# 测试连接 MySQL
ping mysql-service

# 测试连接 Redis
ping redis-service
```

### 2. 测试负载均衡

```bash
# 扩容后端服务
kubectl scale deployment backend -n demo-app --replicas=3

# 查看 Pod
kubectl get pods -n demo-app -l app=backend

# 多次请求，观察负载分配
for i in {1..10}; do
  curl http://demo.local/api/health
done
```

### 3. 测试滚动更新

```bash
# 更新后端镜像
kubectl set image deployment/backend -n demo-app \
  backend=demo-backend:v2

# 查看滚动更新过程
kubectl rollout status deployment/backend -n demo-app

# 查看历史
kubectl rollout history deployment/backend -n demo-app

# 回滚
kubectl rollout undo deployment/backend -n demo-app
```

### 4. 测试自愈能力

```bash
# 删除一个 Pod
kubectl delete pod -n demo-app -l app=backend --force --grace-period=0

# 观察 Pod 自动重建
kubectl get pods -n demo-app -w
```

### 5. 测试数据持久化

```bash
# 进入 MySQL，创建数据
kubectl exec -it -n demo-app deployment/mysql -- mysql -uroot -prootpassword

# 在 MySQL 中执行
USE demo_db;
INSERT INTO users (name, email) VALUES ('测试用户', 'test@example.com');
SELECT * FROM users;
exit

# 删除 MySQL Pod
kubectl delete pod -n demo-app -l app=mysql

# 等待 Pod 重建后，再次查询数据
kubectl exec -it -n demo-app deployment/mysql -- mysql -uroot -prootpassword -e "SELECT * FROM demo_db.users;"
```

## 🔧 配置说明

### ConfigMap 配置项

- `MYSQL_HOST`: MySQL 服务地址
- `MYSQL_DATABASE`: 数据库名称
- `REDIS_HOST`: Redis 服务地址
- `LOG_LEVEL`: 日志级别

### Secret 配置项

- `mysql-root-password`: MySQL root 密码
- `mysql-password`: MySQL 应用用户密码

### 资源限制

| 服务 | CPU Request | CPU Limit | Memory Request | Memory Limit |
|------|-------------|-----------|----------------|--------------|
| Frontend | 50m | 100m | 64Mi | 128Mi |
| Backend | 100m | 200m | 128Mi | 256Mi |
| MySQL | 250m | 500m | 512Mi | 1Gi |
| Redis | 100m | 200m | 128Mi | 256Mi |

## 🛠️ 故障排查

### Pod 无法启动

```bash
# 查看 Pod 详情
kubectl describe pod -n demo-app <pod-name>

# 查看日志
kubectl logs -n demo-app <pod-name>

# 查看事件
kubectl get events -n demo-app --sort-by=.metadata.creationTimestamp
```

### 服务无法访问

```bash
# 检查 Service
kubectl get svc -n demo-app

# 检查 Endpoints
kubectl get endpoints -n demo-app

# 检查 Ingress
kubectl describe ingress -n demo-app demo-ingress
```

### 数据库连接失败

```bash
# 检查 MySQL 是否运行
kubectl get pods -n demo-app -l app=mysql

# 测试数据库连接
kubectl exec -it -n demo-app deployment/backend -- \
  python -c "import pymysql; pymysql.connect(host='mysql-service', user='demo_user', password='demo_password', database='demo_db')"
```

## 🧹 清理资源

```bash
# 使用脚本清理
./scripts/cleanup.sh

# 或手动清理
kubectl delete namespace demo-app

# 清理 hosts 文件
sudo sed -i '/demo.local/d' /etc/hosts
```

## 📚 学习要点

通过这个 Demo，你将学习到：

1. **多服务部署**：如何部署和管理多个相互依赖的服务
2. **服务发现**：服务之间如何通过 DNS 相互访问
3. **配置管理**：使用 ConfigMap 和 Secret 管理配置
4. **数据持久化**：使用 PV/PVC 持久化数据库数据
5. **流量管理**：使用 Ingress 统一入口和路由
6. **健康检查**：配置 Liveness 和 Readiness 探针
7. **资源管理**：设置资源请求和限制
8. **滚动更新**：零停机更新应用
9. **故障排查**：如何调试和解决问题

## 🎓 进阶练习

1. **添加 HPA**：为后端服务配置自动扩缩容
2. **添加监控**：集成 Prometheus 和 Grafana
3. **添加日志收集**：使用 EFK 栈收集日志
4. **配置 TLS**：为 Ingress 配置 HTTPS
5. **实现 CI/CD**：使用 GitLab CI 或 GitHub Actions 自动部署
6. **多环境部署**：配置 dev、staging、production 环境
7. **服务网格**：集成 Istio 实现高级流量管理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License
