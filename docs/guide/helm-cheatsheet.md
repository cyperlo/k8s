# Helm 快速参考

## 常用命令速查

### 仓库管理

```bash
# 添加仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable

# 更新仓库
helm repo update

# 列出仓库
helm repo list

# 删除仓库
helm repo remove bitnami

# 搜索 Chart
helm search repo nginx
helm search hub wordpress
```

### 安装和管理

```bash
# 安装 Chart
helm install my-release bitnami/nginx

# 指定命名空间安装
helm install my-release bitnami/nginx -n production

# 使用自定义配置安装
helm install my-release bitnami/nginx -f values.yaml

# 设置单个值
helm install my-release bitnami/nginx --set service.type=NodePort

# 查看安装状态
helm status my-release

# 列出所有 Release
helm list
helm list -A  # 所有命名空间

# 升级 Release
helm upgrade my-release bitnami/nginx

# 回滚到上一版本
helm rollback my-release

# 回滚到指定版本
helm rollback my-release 2

# 卸载 Release
helm uninstall my-release
```

### Chart 开发

```bash
# 创建新 Chart
helm create mychart

# 验证 Chart
helm lint mychart

# 打包 Chart
helm package mychart

# 模板渲染（不安装）
helm template my-release mychart

# 调试安装（模拟）
helm install my-release mychart --dry-run --debug
```

### 查看信息

```bash
# 查看 Chart 信息
helm show chart bitnami/nginx

# 查看默认配置
helm show values bitnami/nginx

# 查看所有信息
helm show all bitnami/nginx

# 查看 Release 历史
helm history my-release

# 获取 Release 的配置值
helm get values my-release

# 获取 Release 的清单
helm get manifest my-release
```

## 实用技巧

### 1. 覆盖配置值

```bash
# 方式一：使用 values 文件
helm install my-app ./mychart -f custom-values.yaml

# 方式二：命令行设置
helm install my-app ./mychart \
  --set image.tag=v2.0 \
  --set replicas=3

# 方式三：多个 values 文件（后面的覆盖前面的）
helm install my-app ./mychart \
  -f values.yaml \
  -f values-prod.yaml
```

### 2. 命名空间管理

```bash
# 创建命名空间并安装
helm install my-app bitnami/nginx \
  --namespace production \
  --create-namespace

# 查看特定命名空间的 Release
helm list -n production
```

### 3. 版本管理

```bash
# 查看历史版本
helm history my-app

# 回滚到指定版本
helm rollback my-app 3

# 升级并保留历史
helm upgrade my-app bitnami/nginx --history-max 10
```

### 4. 依赖管理

```bash
# 更新依赖
helm dependency update mychart

# 列出依赖
helm dependency list mychart

# 构建依赖
helm dependency build mychart
```

## 常见使用场景

### 场景 1：安装 MySQL

```bash
# 添加仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 查看可配置项
helm show values bitnami/mysql

# 创建自定义配置
cat > mysql-values.yaml <<EOF
auth:
  rootPassword: "mypassword"
  database: "mydb"
primary:
  persistence:
    size: 10Gi
EOF

# 安装
helm install my-mysql bitnami/mysql -f mysql-values.yaml
```

### 场景 2：安装 Redis

```bash
# 安装 Redis
helm install my-redis bitnami/redis \
  --set auth.password=redis123 \
  --set master.persistence.size=5Gi
```

### 场景 3：安装 Nginx Ingress Controller

```bash
# 添加仓库
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# 安装
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

### 场景 4：安装监控栈（Prometheus + Grafana）

```bash
# 添加仓库
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 安装
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

## 故障排查

### 查看详细日志

```bash
# 安装时查看详细信息
helm install my-app ./mychart --debug

# 模拟安装（不实际部署）
helm install my-app ./mychart --dry-run --debug
```

### 检查 Release 状态

```bash
# 查看状态
helm status my-app

# 查看历史
helm history my-app

# 获取实际部署的资源
helm get manifest my-app
```

### 常见问题

**问题 1：Release 已存在**
```bash
# 错误：cannot re-use a name that is still in use
# 解决：使用不同的名称或先卸载
helm uninstall my-app
helm install my-app ./mychart
```

**问题 2：Chart 依赖缺失**
```bash
# 错误：found in Chart.yaml, but missing in charts/ directory
# 解决：更新依赖
helm dependency update ./mychart
```

**问题 3：配置值错误**
```bash
# 使用 --dry-run 验证
helm install my-app ./mychart -f values.yaml --dry-run --debug
```

## 最佳实践

1. **使用版本控制**：将 values.yaml 纳入 Git 管理
2. **环境分离**：为不同环境创建不同的 values 文件
3. **命名规范**：使用有意义的 Release 名称
4. **定期更新**：保持 Chart 和仓库更新
5. **测试先行**：使用 --dry-run 测试后再部署
6. **备份配置**：保存重要的配置值
7. **文档化**：记录自定义配置的原因

## 相关资源

- [Helm 官方文档](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/) - Chart 搜索
- [Bitnami Charts](https://github.com/bitnami/charts)
- [Helm Charts GitHub](https://github.com/helm/charts)
