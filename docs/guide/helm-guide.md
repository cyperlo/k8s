# Helm 完整指南

## 什么是 Helm？

Helm 是 Kubernetes 的包管理器，就像 apt/yum 对于 Linux，npm 对于 Node.js 一样。它帮助你定义、安装和升级复杂的 Kubernetes 应用。

### 核心概念

- **Chart**: Helm 的打包格式，包含运行应用所需的所有 Kubernetes 资源定义
- **Release**: Chart 的一个运行实例，每次安装 Chart 都会创建一个新的 Release
- **Repository**: 存储和分享 Chart 的地方

## 安装 Helm

### macOS
```bash
brew install helm
```

### Linux
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Windows
```bash
choco install kubernetes-helm
```

### 验证安装
```bash
helm version
```

## Helm 基础命令

### 仓库管理

```bash
# 添加官方稳定仓库
helm repo add stable https://charts.helm.sh/stable

# 添加 Bitnami 仓库（推荐）
helm repo add bitnami https://charts.bitnami.com/bitnami

# 更新仓库
helm repo update

# 列出所有仓库
helm repo list

# 搜索 Chart
helm search repo nginx

# 删除仓库
helm repo remove stable
```

### Chart 操作

```bash
# 搜索 Chart
helm search repo mysql

# 查看 Chart 信息
helm show chart bitnami/mysql
helm show values bitnami/mysql

# 下载 Chart
helm pull bitnami/mysql
helm pull bitnami/mysql --untar
```

### Release 管理

```bash
# 安装 Chart
helm install my-release bitnami/nginx

# 指定命名空间安装
helm install my-release bitnami/nginx -n production --create-namespace

# 使用自定义值安装
helm install my-release bitnami/nginx -f values.yaml

# 设置单个值
helm install my-release bitnami/nginx --set service.type=NodePort

# 列出所有 Release
helm list
helm list -A  # 所有命名空间

# 查看 Release 状态
helm status my-release

# 升级 Release
helm upgrade my-release bitnami/nginx

# 回滚 Release
helm rollback my-release 1  # 回滚到版本 1

# 卸载 Release
helm uninstall my-release

# 保留历史记录卸载
helm uninstall my-release --keep-history
```

## 创建自己的 Chart

### 创建 Chart 结构

```bash
helm create myapp
```

这会创建以下结构：
```
myapp/
├── Chart.yaml          # Chart 元数据
├── values.yaml         # 默认配置值
├── charts/             # 依赖的 Chart
├── templates/          # Kubernetes 资源模板
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl   # 模板辅助函数
│   └── NOTES.txt      # 安装后显示的信息
└── .helmignore        # 打包时忽略的文件
```

### Chart.yaml 示例

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0"
keywords:
  - myapp
  - web
maintainers:
  - name: Your Name
    email: your.email@example.com
```

### values.yaml 示例

```yaml
replicaCount: 2

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: "nginx"
  hosts:
    - host: myapp.local
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

### Deployment 模板示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

## Helm 模板语法

### 基本语法

```yaml
# 访问值
{{ .Values.replicaCount }}

# 访问 Chart 信息
{{ .Chart.Name }}
{{ .Chart.Version }}

# 访问 Release 信息
{{ .Release.Name }}
{{ .Release.Namespace }}

# 条件判断
{{- if .Values.ingress.enabled }}
# ingress 配置
{{- end }}

# 循环
{{- range .Values.hosts }}
- {{ . }}
{{- end }}

# 使用辅助函数
{{ include "myapp.fullname" . }}

# 缩进
{{- toYaml .Values.resources | nindent 12 }}
```

### 常用函数

```yaml
# 字符串操作
{{ .Values.name | upper }}
{{ .Values.name | lower }}
{{ .Values.name | quote }}
{{ .Values.name | default "default-value" }}

# 类型转换
{{ .Values.port | toString }}
{{ .Values.enabled | ternary "yes" "no" }}

# 列表操作
{{ .Values.list | join "," }}

# 字典操作
{{ .Values.config | toYaml }}
{{ .Values.config | toJson }}
```

## 测试和调试

### 模板渲染测试

```bash
# 渲染模板但不安装
helm template my-release ./myapp

# 渲染并显示值
helm template my-release ./myapp --debug

# 使用自定义值渲染
helm template my-release ./myapp -f custom-values.yaml

# 只渲染特定模板
helm template my-release ./myapp -s templates/deployment.yaml
```

### 语法检查

```bash
# 检查 Chart 语法
helm lint ./myapp

# 详细检查
helm lint ./myapp --strict
```

### 模拟安装

```bash
# 模拟安装（不实际创建资源）
helm install my-release ./myapp --dry-run --debug
```

## 依赖管理

### Chart.yaml 中定义依赖

```yaml
dependencies:
  - name: mysql
    version: "9.3.4"
    repository: "https://charts.bitnami.com/bitnami"
    condition: mysql.enabled
  - name: redis
    version: "17.3.7"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

### 管理依赖

```bash
# 下载依赖
helm dependency update ./myapp

# 列出依赖
helm dependency list ./myapp

# 构建依赖
helm dependency build ./myapp
```

## 打包和分发

### 打包 Chart

```bash
# 打包 Chart
helm package ./myapp

# 指定版本打包
helm package ./myapp --version 1.0.0

# 签名打包
helm package ./myapp --sign --key mykey
```

### 创建仓库索引

```bash
# 创建索引文件
helm repo index ./charts

# 合并现有索引
helm repo index ./charts --merge existing-index.yaml
```

## 实战示例

### 示例 1: 部署 WordPress

```bash
# 添加仓库
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 创建自定义值文件
cat > wordpress-values.yaml <<EOF
wordpressUsername: admin
wordpressPassword: MySecurePassword123
wordpressEmail: admin@example.com
service:
  type: NodePort
persistence:
  enabled: true
  size: 10Gi
mariadb:
  auth:
    rootPassword: MyDBPassword123
    database: wordpress
EOF

# 安装 WordPress
helm install my-wordpress bitnami/wordpress -f wordpress-values.yaml

# 查看状态
helm status my-wordpress

# 获取访问信息
kubectl get svc my-wordpress
```

### 示例 2: 部署 MySQL

```bash
# 创建配置文件
cat > mysql-values.yaml <<EOF
auth:
  rootPassword: MyRootPassword123
  database: myapp
  username: myuser
  password: MyUserPassword123
primary:
  persistence:
    enabled: true
    size: 20Gi
metrics:
  enabled: true
EOF

# 安装 MySQL
helm install my-mysql bitnami/mysql -f mysql-values.yaml -n database --create-namespace

# 连接到 MySQL
kubectl run mysql-client --rm -it --image=mysql:8.0 -- mysql -h my-mysql.database.svc.cluster.local -u myuser -p
```

### 示例 3: 创建微服务 Chart

```bash
# 创建 Chart
helm create microservice

# 编辑 values.yaml
cat > microservice/values.yaml <<EOF
replicaCount: 3

image:
  repository: myapp/backend
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix

env:
  - name: DATABASE_HOST
    value: mysql.database.svc.cluster.local
  - name: DATABASE_NAME
    value: myapp

secrets:
  DATABASE_PASSWORD: base64encodedpassword

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
EOF

# 安装
helm install backend ./microservice -n production --create-namespace
```

## 高级特性

### Hooks

Helm Hooks 允许在 Release 生命周期的特定时刻执行操作。

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-migration
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: migration
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        command: ["./migrate.sh"]
      restartPolicy: Never
```

可用的 Hook 类型：
- `pre-install`: 安装前执行
- `post-install`: 安装后执行
- `pre-delete`: 删除前执行
- `post-delete`: 删除后执行
- `pre-upgrade`: 升级前执行
- `post-upgrade`: 升级后执行
- `pre-rollback`: 回滚前执行
- `post-rollback`: 回滚后执行

### 子 Chart

```yaml
# 在父 Chart 的 values.yaml 中配置子 Chart
mysql:
  enabled: true
  auth:
    database: myapp
    username: myuser

redis:
  enabled: false
```

### 命名模板

在 `_helpers.tpl` 中定义可重用的模板：

```yaml
{{/*
生成完整名称
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
通用标签
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## 最佳实践

### 1. 值文件组织

```bash
# 按环境组织
values-dev.yaml
values-staging.yaml
values-prod.yaml

# 安装时指定
helm install myapp ./chart -f values-prod.yaml
```

### 2. 版本管理

- Chart 版本遵循语义化版本（SemVer）
- 每次修改都应更新版本号
- 使用 `appVersion` 标识应用版本

### 3. 文档化

- 在 `README.md` 中说明 Chart 用途
- 在 `values.yaml` 中添加详细注释
- 使用 `NOTES.txt` 提供安装后的使用说明

### 4. 安全性

```yaml
# 使用 Secret 存储敏感信息
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "myapp.fullname" . }}
type: Opaque
data:
  password: {{ .Values.password | b64enc | quote }}
```

### 5. 资源限制

始终为容器设置资源请求和限制：

```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

### 6. 健康检查

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 常见问题

### 1. Release 已存在

```bash
# 错误: release already exists
# 解决: 使用 upgrade --install
helm upgrade --install my-release ./myapp
```

### 2. 模板渲染错误

```bash
# 使用 --debug 查看详细信息
helm install my-release ./myapp --debug --dry-run

# 使用 lint 检查语法
helm lint ./myapp
```

### 3. 依赖更新失败

```bash
# 清理依赖缓存
rm -rf charts/
helm dependency update
```

### 4. 回滚失败

```bash
# 查看历史版本
helm history my-release

# 回滚到特定版本
helm rollback my-release 2
```

### 5. 值覆盖不生效

```bash
# 检查值的优先级
# 命令行 --set > -f 文件 > values.yaml

# 查看最终合并的值
helm get values my-release
```

## 有用的资源

- [Helm 官方文档](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/) - 查找 Helm Charts
- [Helm Chart 最佳实践](https://helm.sh/docs/chart_best_practices/)
- [Helm GitHub](https://github.com/helm/helm)

## 总结

Helm 是管理 Kubernetes 应用的强大工具，掌握它可以：

- 简化复杂应用的部署
- 实现配置的版本化管理
- 轻松回滚和升级应用
- 复用和分享应用配置
- 管理应用的生命周期

从简单的 Chart 开始，逐步掌握模板语法和高级特性，你就能高效地管理 Kubernetes 应用了。
