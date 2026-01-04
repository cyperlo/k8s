# Telepresence - Kubernetes 本地开发工具

## 简介

Telepresence 是一个开源工具，允许你在本地运行单个服务，同时将该服务连接到远程 Kubernetes 集群。这使得开发者可以在本地快速迭代开发，同时访问集群中的其他服务、配置和资源。

### 为什么使用 Telepresence？

- 🚀 **快速开发迭代**：在本地修改代码立即生效，无需重新构建镜像和部署
- 🔗 **无缝集群集成**：本地服务可以访问集群内的数据库、缓存、其他微服务
- 🐛 **真实环境调试**：使用本地 IDE 调试器调试运行在集群环境中的代码
- 💰 **节省资源**：无需在集群中频繁部署测试版本
- 🔄 **双向通信**：集群中的服务可以调用你本地运行的服务
- 🎯 **选择性拦截**：可以只拦截特定的流量到本地

## 核心概念

### 工作模式

Telepresence 有两种主要工作模式：

#### 1. Intercept（拦截模式）

将集群中某个服务的流量拦截到本地，本地服务替代集群中的服务处理请求。

```
集群流量 → Telepresence Agent → 本地服务
```

**使用场景：**
- 开发和调试微服务
- 测试新功能而不影响其他开发者
- 在真实环境中调试问题

#### 2. Connect（连接模式）

将本地网络连接到集群网络，可以直接访问集群内的服务。

```
本地应用 → Telepresence → 集群服务
```

**使用场景：**
- 本地运行需要访问集群资源的应用
- 测试与集群服务的集成
- 访问集群内的数据库、缓存等

## 安装

### 前置要求

- Kubernetes 集群（本地或远程）
- kubectl 已配置并可以访问集群
- 集群管理员权限（用于安装 Traffic Manager）

### Linux 安装

```bash
# 下载最新版本
sudo curl -fL https://app.getambassador.io/download/tel2/linux/amd64/latest/telepresence -o /usr/local/bin/telepresence

# 添加执行权限
sudo chmod +x /usr/local/bin/telepresence

# 验证安装
telepresence version
```

### macOS 安装

```bash
# 使用 Homebrew
brew install datawire/blackbird/telepresence

# 验证安装
telepresence version
```

### Windows 安装

```powershell
# 使用 Chocolatey
choco install telepresence

# 或下载二进制文件
# 访问 https://www.telepresence.io/docs/latest/install/
```

### 验证安装

```bash
# 检查版本
telepresence version

# 应该看到类似输出
# Client: v2.x.x
# Root Daemon: not running
# User Daemon: not running
```

## 快速开始

### 1. 连接到集群

```bash
# 连接到当前 kubectl 上下文的集群
telepresence connect

# 指定命名空间
telepresence connect --namespace my-namespace

# 查看连接状态
telepresence status
```

**输出示例：**
```
Connected to context my-cluster (https://api.cluster.example.com)
Telepresence Daemons are running
```

### 2. 列出可拦截的服务

```bash
# 查看所有可以拦截的工作负载
telepresence list

# 指定命名空间
telepresence list --namespace production
```

**输出示例：**
```
web-service    : ready to intercept (traffic-agent not yet installed)
api-service    : ready to intercept (traffic-agent not yet installed)
auth-service   : ready to intercept (traffic-agent not yet installed)
```

### 3. 创建拦截

```bash
# 基本拦截（拦截所有流量）
telepresence intercept <service-name> --port <local-port>:<remote-port>

# 示例：拦截 web-service，本地 8080 端口对应远程 80 端口
telepresence intercept web-service --port 8080:80

# 拦截特定命名空间的服务
telepresence intercept api-service --port 3000:8080 --namespace production
```

### 4. 运行本地服务

```bash
# 在另一个终端启动你的本地服务
# 例如：
cd my-service
npm start  # 或 python app.py, go run main.go 等
```

### 5. 测试拦截

```bash
# 从集群内或通过 Ingress 访问服务
# 流量会被路由到你的本地服务

# 查看拦截状态
telepresence list

# 应该看到
# web-service: intercepted
#   Intercept name: web-service
#   State         : ACTIVE
#   Destination   : 127.0.0.1:8080
```

### 6. 停止拦截

```bash
# 停止特定拦截
telepresence leave web-service

# 停止所有拦截并断开连接
telepresence quit
```

## 高级功能

### 选择性拦截（Preview URLs）

只拦截特定的流量，其他流量继续发送到集群中的服务。

```bash
# 使用 header 匹配拦截
telepresence intercept web-service \
  --port 8080:80 \
  --http-match=x-dev-user=alice

# 现在只有包含 header "x-dev-user: alice" 的请求会被拦截到本地
# 其他请求继续发送到集群中的服务
```

**测试选择性拦截：**

```bash
# 会被拦截到本地
curl -H "x-dev-user: alice" http://web-service.example.com

# 继续发送到集群
curl http://web-service.example.com
```

### 环境变量注入

Telepresence 可以将集群中 Pod 的环境变量注入到本地进程。

```bash
# 拦截并获取环境变量
telepresence intercept web-service \
  --port 8080:80 \
  --env-file=.env

# 查看生成的 .env 文件
cat .env

# 使用环境变量运行本地服务
source .env
npm start
```

### 挂载远程卷

```bash
# 挂载集群中的卷到本地
telepresence intercept web-service \
  --port 8080:80 \
  --mount=/tmp/tel-mount

# 现在可以在 /tmp/tel-mount 访问远程卷的内容
ls /tmp/tel-mount
```

### 多服务拦截

```bash
# 同时拦截多个服务
telepresence intercept service-a --port 8080:80
telepresence intercept service-b --port 8081:80
telepresence intercept service-c --port 8082:80

# 查看所有拦截
telepresence list
```

### 使用不同的 Docker 镜像

```bash
# 指定 traffic-agent 镜像
telepresence intercept web-service \
  --port 8080:80 \
  --docker-run \
  --docker-build /path/to/dockerfile
```

## 实际使用场景

### 场景 1：微服务开发

**背景：** 你正在开发一个订单服务，需要调用集群中的用户服务和支付服务。

```bash
# 1. 连接到集群
telepresence connect

# 2. 拦截订单服务
telepresence intercept order-service --port 3000:8080

# 3. 在本地启动订单服务
cd order-service
npm run dev

# 4. 本地服务现在可以：
#    - 接收来自集群的请求
#    - 调用集群中的 user-service 和 payment-service
#    - 访问集群中的数据库和缓存
```

### 场景 2：调试生产问题

**背景：** 生产环境出现问题，需要在真实环境中调试。

```bash
# 1. 连接到生产集群（只读模式）
telepresence connect --namespace production

# 2. 使用 header 匹配只拦截你的测试流量
telepresence intercept api-service \
  --port 8080:80 \
  --http-match=x-debug-session=debug-123

# 3. 在本地启动服务并附加调试器
# 在 IDE 中设置断点
npm run debug

# 4. 发送带有特定 header 的请求
curl -H "x-debug-session: debug-123" https://api.example.com/endpoint

# 5. 本地断点会被触发，可以调试
```

### 场景 3：前端开发

**背景：** 前端开发需要调用集群中的后端 API。

```bash
# 1. 连接到集群（不拦截，只访问）
telepresence connect

# 2. 在本地启动前端开发服务器
cd frontend
npm run dev

# 3. 前端代码可以直接访问集群服务
# 例如：fetch('http://api-service.default.svc.cluster.local:8080/api/users')
```

### 场景 4：集成测试

**背景：** 运行集成测试，需要访问集群中的真实服务。

```bash
# 1. 连接到测试集群
telepresence connect --namespace test

# 2. 运行集成测试
npm run test:integration

# 测试代码可以访问集群中的服务
# 例如：
# const response = await fetch('http://user-service:8080/users');
```


## 配置文件

### 全局配置

配置文件位置：`~/.config/telepresence/config.yml`

```yaml
timeouts:
  agentInstall: 2m
  intercept: 30s
  
logLevels:
  userDaemon: info
  rootDaemon: info
  
images:
  registry: docker.io/datawire
  agentImage: tel2:2.x.x
  
intercept:
  defaultPort: 8080
  useFtp: false
  
grpc:
  maxReceiveSize: 10Mi
```

### 项目配置

在项目根目录创建 `telepresence.yml`：

```yaml
workloads:
  - name: web-service
    intercepts:
      - handler: web-handler
        port: 8080:80
        service: web-service
        
  - name: api-service
    intercepts:
      - handler: api-handler
        port: 3000:8080
        service: api-service
        match:
          - http-header: x-dev-user=alice
```

使用配置文件：

```bash
# 使用配置文件中的拦截配置
telepresence intercept --config telepresence.yml
```

## 常用命令

### 连接管理

```bash
# 连接到集群
telepresence connect

# 连接到特定上下文
telepresence connect --context production

# 查看连接状态
telepresence status

# 断开连接
telepresence quit

# 完全卸载（包括 Traffic Manager）
telepresence uninstall --everything
```

### 拦截管理

```bash
# 列出可拦截的服务
telepresence list

# 创建拦截
telepresence intercept <service> --port <local>:<remote>

# 列出当前拦截
telepresence list --intercepts

# 停止拦截
telepresence leave <service>

# 停止所有拦截
telepresence leave --all
```

### 调试命令

```bash
# 查看详细日志
telepresence loglevel debug

# 查看守护进程状态
telepresence status

# 测试集群连接
telepresence test-vpn

# 收集诊断信息
telepresence gather-logs
```

## 故障排查

### 1. 无法连接到集群

**问题：** `telepresence connect` 失败

**解决方法：**

```bash
# 检查 kubectl 配置
kubectl cluster-info
kubectl get nodes

# 检查当前上下文
kubectl config current-context

# 查看详细错误
telepresence loglevel debug
telepresence connect

# 检查 Traffic Manager 是否安装
kubectl get svc -n ambassador

# 手动安装 Traffic Manager
telepresence helm install
```

### 2. 拦截不工作

**问题：** 流量没有被路由到本地

**解决方法：**

```bash
# 检查拦截状态
telepresence list

# 确认本地服务正在运行
netstat -tuln | grep <local-port>

# 检查 traffic-agent 是否安装
kubectl get pods -n <namespace>

# 查看 traffic-agent 日志
kubectl logs <pod-name> -c traffic-agent

# 重新创建拦截
telepresence leave <service>
telepresence intercept <service> --port <local>:<remote>
```

### 3. DNS 解析问题

**问题：** 无法解析集群内的服务名

**解决方法：**

```bash
# 测试 DNS 解析
nslookup my-service.default.svc.cluster.local

# 检查 VPN 状态
telepresence test-vpn

# 重启连接
telepresence quit
telepresence connect

# 检查系统 DNS 配置
cat /etc/resolv.conf
```

### 4. 权限问题

**问题：** 没有权限安装 Traffic Manager

**解决方法：**

```bash
# 检查权限
kubectl auth can-i create deployments -n ambassador
kubectl auth can-i create services -n ambassador

# 请求管理员安装 Traffic Manager
# 或使用已有的 Traffic Manager
telepresence connect --manager-namespace ambassador
```

### 5. 端口冲突

**问题：** 本地端口已被占用

**解决方法：**

```bash
# 查找占用端口的进程
lsof -i :<port>
netstat -tuln | grep <port>

# 使用不同的本地端口
telepresence intercept service --port 8081:80

# 或停止占用端口的进程
kill -9 <pid>
```

### 6. 性能问题

**问题：** 网络延迟高或连接不稳定

**解决方法：**

```bash
# 检查网络延迟
ping <cluster-api-server>

# 使用本地集群（如 minikube）
minikube start
telepresence connect

# 调整超时设置
# 编辑 ~/.config/telepresence/config.yml
timeouts:
  agentInstall: 5m
  intercept: 60s
```

## 最佳实践

### 1. 开发环境隔离

```bash
# 为每个开发者创建独立的命名空间
kubectl create namespace dev-alice
kubectl create namespace dev-bob

# 开发者连接到自己的命名空间
telepresence connect --namespace dev-alice
```

### 2. 使用选择性拦截

```bash
# 避免影响其他开发者，使用 header 匹配
telepresence intercept service \
  --port 8080:80 \
  --http-match=x-developer=$(whoami)

# 测试时带上 header
curl -H "x-developer: alice" http://service.example.com
```

### 3. 环境变量管理

```bash
# 导出环境变量到文件
telepresence intercept service \
  --port 8080:80 \
  --env-file=.env.telepresence

# 添加到 .gitignore
echo ".env.telepresence" >> .gitignore

# 使用 direnv 自动加载
echo "source .env.telepresence" > .envrc
direnv allow
```

### 4. 团队协作

创建团队配置文件 `telepresence.yml`：

```yaml
# 团队共享的拦截配置
workloads:
  - name: api-service
    intercepts:
      - handler: local-dev
        port: 8080:80
        match:
          - http-header: x-dev-user=${USER}
```

### 5. CI/CD 集成

```yaml
# .github/workflows/integration-test.yml
name: Integration Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Telepresence
        run: |
          sudo curl -fL https://app.getambassador.io/download/tel2/linux/amd64/latest/telepresence \
            -o /usr/local/bin/telepresence
          sudo chmod +x /usr/local/bin/telepresence
      
      - name: Connect to cluster
        run: |
          telepresence connect --namespace test
      
      - name: Run integration tests
        run: |
          npm run test:integration
      
      - name: Cleanup
        run: |
          telepresence quit
```

## 与其他工具对比

| 特性 | Telepresence | kubectl port-forward | Skaffold |
|------|--------------|---------------------|----------|
| 双向通信 | ✅ | ❌ | ✅ |
| 环境变量注入 | ✅ | ❌ | ❌ |
| 选择性流量拦截 | ✅ | ❌ | ❌ |
| 本地调试 | ✅ | ⚠️ | ✅ |
| 学习曲线 | 中等 | 简单 | 较高 |
| 资源消耗 | 低 | 极低 | 中等 |

## 安全考虑

### 1. 生产环境使用

```bash
# 使用只读模式
telepresence connect --namespace production --read-only

# 使用选择性拦截，避免影响真实用户
telepresence intercept service \
  --port 8080:80 \
  --http-match=x-debug-token=secret-token
```

### 2. 网络隔离

```bash
# 限制可访问的命名空间
telepresence connect --namespace dev --mapped-namespaces dev,test

# 不要在生产环境安装 Traffic Manager
# 使用专门的开发/测试集群
```

### 3. 凭证管理

```bash
# 不要在拦截时暴露敏感信息
# 使用环境变量文件，并添加到 .gitignore
telepresence intercept service --env-file=.env.local
echo ".env.local" >> .gitignore
```

## 学习资源

- [官方网站](https://www.telepresence.io/)
- [官方文档](https://www.telepresence.io/docs/latest/)
- [GitHub 仓库](https://github.com/telepresenceio/telepresence)
- [快速开始视频](https://www.youtube.com/telepresenceio)
- [社区 Slack](https://a8r.io/slack)

## 总结

Telepresence 是一个强大的 Kubernetes 本地开发工具，特别适合：

1. **微服务开发**：需要与集群中其他服务交互
2. **快速迭代**：频繁修改代码，不想每次都构建镜像
3. **真实环境调试**：在接近生产的环境中调试问题
4. **集成测试**：需要访问集群资源的测试

**关键优势：**
- 提高开发效率（无需重复构建和部署）
- 降低资源消耗（本地运行，不占用集群资源）
- 真实环境调试（使用本地 IDE 调试器）
- 灵活的流量控制（选择性拦截）

**使用建议：**
- 从简单的连接模式开始学习
- 在开发/测试环境练习拦截功能
- 使用选择性拦截避免影响他人
- 生产环境谨慎使用，建议只读模式

记住：Telepresence 是开发工具，不是部署工具。它的目标是让开发更快、更简单！
