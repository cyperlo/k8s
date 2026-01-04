# k9s - Kubernetes 终端 UI 工具

## 简介

k9s 是一个基于终端的 UI 工具，用于与 Kubernetes 集群交互。它提供了一个直观、高效的界面来管理和监控 Kubernetes 资源，大大简化了日常运维工作。

### 为什么使用 k9s？

- 🚀 **高效操作**：通过键盘快捷键快速导航和操作
- 👀 **实时监控**：实时查看资源状态和日志
- 🎯 **资源管理**：轻松查看、编辑、删除各种 Kubernetes 资源
- 📊 **可视化**：直观展示 Pod、Deployment、Service 等资源
- 🔍 **快速搜索**：支持模糊搜索和过滤
- 💡 **智能提示**：内置命令提示和帮助

## 安装

### Linux 详细安装指南

#### 方法一：使用自动安装脚本（最简单）

```bash
# 下载并运行安装脚本
curl -fsSL https://raw.githubusercontent.com/your-repo/k8s-learning/main/docs/guide/k9s-install-linux.sh | bash

# 或者先下载再运行
wget https://raw.githubusercontent.com/your-repo/k8s-learning/main/docs/guide/k9s-install-linux.sh
chmod +x k9s-install-linux.sh
./k9s-install-linux.sh
```

脚本会自动：
- 检测系统架构（amd64/arm64/arm）
- 下载最新版本的 k9s
- 安装到 /usr/local/bin
- 创建必要的配置目录
- 验证安装

#### 方法二：使用二进制文件安装（推荐）

```bash
# 1. 查看最新版本
# 访问 https://github.com/derailed/k9s/releases 查看最新版本号
# 或使用 curl 获取
LATEST_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
echo "最新版本: $LATEST_VERSION"

# 2. 下载对应架构的二进制文件
# x86_64 架构（大多数 Linux 服务器）
wget https://github.com/derailed/k9s/releases/download/${LATEST_VERSION}/k9s_Linux_amd64.tar.gz

# ARM64 架构（如树莓派、ARM 服务器）
# wget https://github.com/derailed/k9s/releases/download/${LATEST_VERSION}/k9s_Linux_arm64.tar.gz

# 3. 解压文件
tar -xzf k9s_Linux_amd64.tar.gz

# 4. 移动到系统路径
sudo mv k9s /usr/local/bin/

# 5. 添加执行权限
sudo chmod +x /usr/local/bin/k9s

# 6. 验证安装
k9s version

# 7. 清理下载文件
rm k9s_Linux_amd64.tar.gz README.md
```

#### 方法三：使用包管理器

**Ubuntu/Debian 系统：**

```bash
# 添加 k9s 仓库（如果有）
# 注意：k9s 官方没有提供 apt 仓库，建议使用二进制安装

# 或使用 Snap
sudo snap install k9s

# 或使用 Homebrew on Linux
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install derailed/k9s/k9s
```

**CentOS/RHEL/Fedora 系统：**

```bash
# 使用二进制安装（推荐）
LATEST_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
wget https://github.com/derailed/k9s/releases/download/${LATEST_VERSION}/k9s_Linux_amd64.tar.gz
tar -xzf k9s_Linux_amd64.tar.gz
sudo mv k9s /usr/local/bin/
sudo chmod +x /usr/local/bin/k9s
rm k9s_Linux_amd64.tar.gz README.md

# 或使用 Snap
sudo snap install k9s
```

**Arch Linux：**

```bash
# 使用 AUR
yay -S k9s

# 或使用 pacman（如果在官方仓库）
sudo pacman -S k9s
```

#### 方法四：从源码编译

```bash
# 1. 确保已安装 Go（版本 >= 1.21）
go version

# 2. 克隆仓库
git clone https://github.com/derailed/k9s.git
cd k9s

# 3. 编译
make build

# 4. 安装
sudo cp execs/k9s /usr/local/bin/

# 5. 验证
k9s version
```

#### 安装后配置

```bash
# 1. 创建必要的目录
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s

# 2. 创建基础配置文件
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  # 刷新频率（秒）
  refreshRate: 2
  # 最大连接重试次数
  maxConnRetry: 5
  # 启用鼠标支持
  enableMouse: false
  # 无头模式（隐藏标题栏）
  headless: false
  # 隐藏 logo
  logoless: false
  # 隐藏面包屑导航
  crumbsless: false
  # 只读模式
  readOnly: false
  # 禁用 Ctrl+C 退出
  noExitOnCtrlC: false
  # UI 配置
  ui:
    enableMouse: false
    headless: false
    logoless: false
    crumbsless: false
    reactive: false
    noIcons: false
  # 跳过版本检查
  skipLatestRevCheck: false
  # 禁用 Pod 计数
  disablePodCounting: false
  # Shell Pod 配置
  shellPod:
    image: busybox:1.35.0
    namespace: default
    limits:
      cpu: 100m
      memory: 100Mi
  # 镜像扫描
  imageScans:
    enable: false
  # 日志配置
  logger:
    tail: 100
    buffer: 5000
    sinceSeconds: -1
    fullScreenLogs: false
    textWrap: false
    showTime: false
  # 资源阈值告警
  thresholds:
    cpu:
      critical: 90
      warn: 70
    memory:
      critical: 90
      warn: 70
EOF

# 3. 设置日志级别（可选）
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  refreshRate: 2
  maxConnRetry: 5
  enableMouse: false
  logger:
    tail: 200
    buffer: 5000
    sinceSeconds: 300
    textWrap: true
    showTime: true
EOF

# 4. 验证配置
k9s info
```

# 5. 可用配置（测试）
```yaml
k9s:
  liveViewAutoRefresh: false
  screenDumpDir: /tmp
  refreshRate: 2
  maxConnRetry: 5
  readOnly: false
  noExitOnCtrlC: false
  ui:
    enableMouse: false
    headless: false
    logoless: false
    crumbsless: false
    reactive: false
    noIcons: false
  skipLatestRevCheck: false
  disablePodCounting: false
  shellPod:
    image: busybox:1.35.0
    namespace: default
    limits:
      cpu: 100m
      memory: 100Mi
  imageScans:
    enable: false
    exclusions:
      namespaces: []
      labels: {}
  logger:
    tail: 100
    buffer: 5000
    sinceSeconds: -1
    textWrap: false
    showTime: false
  thresholds:
    cpu:
      critical: 90
      warn: 70
    memory:
      critical: 90
      warn: 70
```

### macOS

```bash
# 使用 Homebrew
brew install derailed/k9s/k9s

# 或使用 MacPorts
sudo port install k9s
```

### Windows

```powershell
# 使用 Chocolatey
choco install k9s

# 或使用 Scoop
scoop install k9s
```

## 快速开始

### 首次运行前的准备

#### 1. 确保 Kubernetes 集群可访问

```bash
# 检查 kubectl 是否安装
kubectl version --client

# 检查集群连接
kubectl cluster-info

# 查看当前上下文
kubectl config current-context

# 查看所有可用上下文
kubectl config get-contexts

# 测试集群访问
kubectl get nodes
kubectl get pods -A
```

#### 2. 创建必要的目录（重要！）

```bash
# 创建 k9s 配置目录
mkdir -p ~/.config/k9s

# 创建 k9s 日志目录
mkdir -p ~/.local/state/k9s

# 验证目录创建
ls -la ~/.config/k9s
ls -la ~/.local/state/k9s
```

#### 3. 配置 Shell 环境（可选）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
cat >> ~/.bashrc << 'EOF'

# k9s 别名
alias k9='k9s'
alias k9s-prod='k9s --context production --readonly'
alias k9s-dev='k9s --context development'
alias k9s-local='k9s --context minikube'

# k9s 日志查看
alias k9s-log='tail -f ~/.local/state/k9s/k9s.log'
EOF

# 重新加载配置
source ~/.bashrc
```

### 启动 k9s

```bash
# 基本启动（使用默认 kubeconfig）
k9s

# 指定 kubeconfig 文件
k9s --kubeconfig ~/.kube/config
k9s --kubeconfig /path/to/custom/kubeconfig

# 指定命名空间启动
k9s -n kube-system
k9s -n default
k9s --namespace production

# 查看所有命名空间
k9s -A
k9s --all-namespaces

# 只读模式（生产环境推荐）
k9s --readonly

# 指定集群上下文
k9s --context my-cluster
k9s --context production

# 直接进入特定资源视图
k9s -c pod          # 直接查看 Pods
k9s -c deploy       # 直接查看 Deployments
k9s -c svc          # 直接查看 Services
k9s -c node         # 直接查看 Nodes

# 设置刷新频率（秒）
k9s --refresh 5

# 启用详细日志（调试用）
k9s --logLevel debug
k9s --logLevel trace

# 无头模式（隐藏标题）
k9s --headless

# 隐藏 logo
k9s --logoless

# 隐藏面包屑导航
k9s --crumbsless

# 组合使用
k9s --context production --namespace app --readonly --refresh 5
```

### 基本界面说明

启动后，你会看到：

```
┌─────────────────────────────────────────────────────────────────┐
│ Context: my-cluster | Namespace: default | View: pods          │  ← 顶部状态栏
├─────────────────────────────────────────────────────────────────┤
│ NAME              READY  STATUS   RESTARTS  AGE                 │
│ nginx-xxx         1/1    Running  0         2d                  │  ← 资源列表
│ redis-xxx         1/1    Running  1         5d                  │
│ mysql-xxx         1/1    Running  0         10d                 │
├─────────────────────────────────────────────────────────────────┤
│ <enter>:view <d>:describe <l>:logs <s>:shell <?>:help          │  ← 快捷键提示
└─────────────────────────────────────────────────────────────────┘
```

**界面元素说明：**
- **顶部状态栏**：显示当前集群、命名空间、资源类型
- **中间列表区**：显示资源列表，可滚动浏览
- **底部提示栏**：显示当前可用的快捷键
- **右上角**：显示 CPU/内存使用情况（某些视图）

### 常见启动问题排查

#### 问题 1：配置文件不存在

```bash
# 错误信息
Error: open /root/.config/k9s/config.yaml: no such file or directory

# 解决方法
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s
k9s
```

#### 问题 2：无法连接集群

```bash
# 错误信息
Unable to connect to cluster

# 排查步骤
# 1. 检查 kubectl 是否正常
kubectl get nodes

# 2. 检查 kubeconfig 文件
cat ~/.kube/config

# 3. 检查当前上下文
kubectl config current-context

# 4. 尝试切换上下文
kubectl config use-context <context-name>

# 5. 使用详细日志启动 k9s
k9s --logLevel debug
```

#### 问题 3：权限不足

```bash
# 错误信息
Forbidden: User cannot list resource

# 检查权限
kubectl auth can-i --list

# 检查特定资源权限
kubectl auth can-i get pods
kubectl auth can-i list deployments

# 如果权限不足，联系集群管理员或使用只读模式
k9s --readonly
```

#### 问题 4：端口冲突或网络问题

```bash
# 检查网络连接
kubectl cluster-info

# 检查 API Server 连接
kubectl get --raw /healthz

# 查看 k9s 日志
tail -f ~/.local/state/k9s/k9s.log
```

## 核心快捷键

### 导航快捷键

| 快捷键 | 功能 |
|--------|------|
| `:` | 命令模式（输入资源类型） |
| `/` | 过滤/搜索 |
| `Esc` | 返回上一级/取消 |
| `?` | 显示帮助 |
| `Ctrl+a` | 显示所有可用资源别名 |
| `Ctrl+c` | 退出 k9s |

### 资源查看

| 快捷键 | 功能 |
|--------|------|
| `:pod` | 查看 Pods |
| `:deploy` | 查看 Deployments |
| `:svc` | 查看 Services |
| `:ns` | 查看 Namespaces |
| `:no` | 查看 Nodes |
| `:pv` | 查看 PersistentVolumes |
| `:pvc` | 查看 PersistentVolumeClaims |
| `:cm` | 查看 ConfigMaps |
| `:sec` | 查看 Secrets |
| `:ing` | 查看 Ingress |

### 资源操作

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 查看详情 |
| `d` | 描述资源（describe） |
| `e` | 编辑资源 |
| `l` | 查看日志 |
| `y` | 查看 YAML |
| `Ctrl+d` | 删除资源 |
| `s` | Shell 进入容器 |
| `p` | 端口转发 |
| `Ctrl+k` | 强制删除 Pod |

### 日志查看

| 快捷键 | 功能 |
|--------|------|
| `l` | 查看日志 |
| `0-9` | 选择容器（多容器 Pod） |
| `f` | 切换自动滚动 |
| `w` | 切换自动换行 |
| `t` | 切换时间戳显示 |
| `c` | 清空日志 |
| `/` | 搜索日志内容 |
| `n` | 下一个搜索结果 |
| `N` | 上一个搜索结果 |

### 命名空间切换

| 快捷键 | 功能 |
|--------|------|
| `0` | 查看所有命名空间 |
| `:ns` | 进入命名空间视图 |
| `Enter` | 切换到选中的命名空间 |

## 常用操作示例

### 1. 查看 Pod 日志

```
1. 启动 k9s
2. 输入 :pod 进入 Pod 视图
3. 使用 / 搜索目标 Pod
4. 选中 Pod 后按 l 查看日志
5. 按 f 开启自动滚动
```

### 2. 进入容器 Shell

```
1. :pod 进入 Pod 视图
2. 选中目标 Pod
3. 按 s 进入 Shell
4. 如果是多容器 Pod，会提示选择容器
```

### 3. 端口转发

```
1. :pod 或 :svc 进入视图
2. 选中资源
3. 按 Shift+f（或 p）
4. 输入本地端口:远程端口（如 8080:80）
5. 按 Enter 确认
```

### 4. 编辑资源

```
1. 进入对应资源视图（如 :deploy）
2. 选中资源
3. 按 e 编辑
4. 修改后保存退出（使用默认编辑器）
```

### 5. 删除资源

```
1. 选中要删除的资源
2. 按 Ctrl+d
3. 输入资源名称确认删除
```

### 6. 查看资源使用情况

```
1. :node 查看节点资源
2. :pod 查看 Pod，按 Shift+c 查看 CPU/内存使用
3. 使用 / 过滤高资源使用的 Pod
```

## 高级功能

### 自定义配置

k9s 配置文件位置：`~/.config/k9s/config.yml`

```yaml
k9s:
  # 刷新频率（秒）
  refreshRate: 2
  
  # 最大日志行数
  maxConnRetry: 5
  
  # 启用鼠标支持
  enableMouse: false
  
  # 日志缓冲区大小
  logBufferSize: 1000
  
  # 默认命名空间
  namespace:
    active: default
    favorites:
      - default
      - kube-system
      - production
  
  # 视图配置
  view:
    active: pod
```

### 自定义快捷键

配置文件：`~/.config/k9s/hotkey.yml`

```yaml
hotKey:
  # 自定义快捷键
  shift-0:
    shortCut: Shift-0
    description: View pods
    command: pods
  
  shift-1:
    shortCut: Shift-1
    description: View deployments
    command: deployments
```

### 插件系统

k9s 支持自定义插件，配置文件：`~/.config/k9s/plugin.yml`

```yaml
plugin:
  # 查看 Pod 的 CPU/内存使用
  top:
    shortCut: Shift-T
    description: Top
    scopes:
      - pods
    command: kubectl
    background: false
    args:
      - top
      - pod
      - $NAME
      - -n
      - $NAMESPACE
  
  # 查看 Pod 事件
  events:
    shortCut: Shift-E
    description: Events
    scopes:
      - pods
    command: kubectl
    background: false
    args:
      - get
      - events
      - --field-selector
      - involvedObject.name=$NAME
      - -n
      - $NAMESPACE
```

### 皮肤主题

k9s 支持自定义主题，配置文件：`~/.config/k9s/skin.yml`

```yaml
k9s:
  body:
    fgColor: dodgerblue
    bgColor: black
    logoColor: blue
  
  prompt:
    fgColor: dodgerblue
    bgColor: black
    suggestColor: white
  
  info:
    fgColor: lightskyblue
    sectionColor: white
  
  table:
    fgColor: white
    bgColor: black
    cursorColor: aqua
    markColor: darkgoldenrod
  
  # 更多配置...
```

## 实用技巧

### 1. 快速过滤

使用 `/` 进行模糊搜索：
```
/nginx          # 搜索包含 nginx 的资源
/!running       # 排除 running 状态
/error|fail     # 搜索包含 error 或 fail 的
```

### 2. 多集群管理

```bash
# 列出所有上下文
kubectl config get-contexts

# 切换上下文后启动 k9s
kubectl config use-context prod-cluster
k9s

# 或直接指定上下文
k9s --context prod-cluster
```

### 3. 监控特定资源

```bash
# 直接进入特定资源视图
k9s -c pod
k9s -c deploy
k9s -c svc
```

### 4. 使用别名

在 `.bashrc` 或 `.zshrc` 中添加：

```bash
alias k9='k9s'
alias k9p='k9s -n production'
alias k9d='k9s -n development'
alias k9s-readonly='k9s --readonly'
```

### 5. 日志分析

在日志视图中：
- 使用 `/` 搜索关键字
- 使用 `n` 和 `N` 在搜索结果间跳转
- 使用 `t` 显示时间戳
- 使用 `w` 切换自动换行

### 6. 资源对比

```
1. 查看资源 YAML（按 y）
2. 复制内容
3. 使用外部工具对比不同环境的配置
```

## 故障排查

### Linux 系统常见问题

#### 1. k9s 无法连接集群

**问题表现：**
```
Unable to connect to the server: dial tcp: lookup kubernetes.docker.internal
Error: cannot connect to cluster
```

**解决步骤：**

```bash
# 步骤 1：检查 kubectl 配置
kubectl cluster-info
kubectl get nodes

# 步骤 2：检查 kubeconfig 文件
ls -la ~/.kube/config
cat ~/.kube/config

# 步骤 3：验证当前上下文
kubectl config current-context
kubectl config get-contexts

# 步骤 4：测试 API Server 连接
kubectl get --raw /healthz

# 步骤 5：检查网络连接
# ping <api-server-ip>
# telnet <api-server-ip> 6443

# 步骤 6：使用详细日志启动
k9s --logLevel debug

# 步骤 7：查看 k9s 日志
tail -f ~/.local/state/k9s/k9s.log
```

#### 2. 配置文件错误

**问题表现：**
```
panic: open /root/.config/k9s/config.yaml: no such file or directory
Error: invalid configuration file
```

**解决方法：**

```bash
# 创建配置目录
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s

# 删除损坏的配置文件
rm -f ~/.config/k9s/config.yaml

# 重新生成默认配置
k9s

# 或手动创建配置文件
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  refreshRate: 2
  maxConnRetry: 5
  enableMouse: false
  readOnly: false
  logger:
    tail: 100
    buffer: 5000
EOF

# 验证配置
k9s info
```

#### 3. 权限问题

**问题表现：**
```
Forbidden: User "system:anonymous" cannot list resource "pods"
Error: pods is forbidden
```

**解决方法：**

```bash
# 检查当前用户权限
kubectl auth can-i --list

# 检查特定资源权限
kubectl auth can-i get pods
kubectl auth can-i list deployments
kubectl auth can-i get pods/log

# 查看当前用户信息
kubectl config view --minify

# 如果使用 RBAC，检查角色绑定
kubectl get rolebindings -A
kubectl get clusterrolebindings

# 临时使用只读模式
k9s --readonly

# 或请求管理员授予权限
# 示例：创建只读角色
kubectl create clusterrolebinding k9s-viewer \
  --clusterrole=view \
  --user=<your-username>
```

#### 4. TLS 证书验证失败（远程 k3s 集群）

**问题表现：**
```
tls: failed to verify certificate: x509: certificate is valid for 10.0.12.17, 10.43.0.1, 127.0.0.1, ::1, not 49.235.43.230
Unable to fetch server version
Auth request failed
```

**原因分析：**
k3s 的 TLS 证书默认只包含内网 IP 和本地地址，不包含公网 IP。当使用公网 IP 连接时会导致证书验证失败。

**解决方法 1：重新生成包含公网 IP 的证书（推荐）**

在 **k3s 服务器**上执行：

```bash
# 1. 停止 k3s
sudo systemctl stop k3s

# 2. 备份现有证书
sudo cp -r /var/lib/rancher/k3s/server/tls /var/lib/rancher/k3s/server/tls.backup

# 3. 删除旧证书
sudo rm -rf /var/lib/rancher/k3s/server/tls

# 4. 修改 k3s 配置，添加公网 IP
sudo mkdir -p /etc/rancher/k3s
sudo tee /etc/rancher/k3s/config.yaml > /dev/null <<EOF
tls-san:
  - <your-public-ip>
  - <your-private-ip>
EOF

# 5. 重启 k3s（会自动重新生成证书）
sudo systemctl start k3s

# 6. 等待 k3s 启动完成
sudo systemctl status k3s

# 7. 导出新的 kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml | sed "s/127.0.0.1/<your-public-ip>/g" > ~/k3s-config.yaml
```

在 **本地 Mac** 上执行：

```bash
# 1. 备份现有配置
cp ~/.kube/config ~/.kube/config.backup

# 2. 下载新的配置
scp root@<server-ip>:~/k3s-config.yaml ~/.kube/config

# 3. 设置权限
chmod 600 ~/.kube/config

# 4. 测试连接
kubectl get nodes

# 5. 启动 k9s
k9s
```

**解决方法 2：跳过证书验证（临时测试用）**

编辑本地 kubeconfig 文件：

```bash
# macOS
vim ~/.kube/config

# Linux
vim ~/.kube/config
```

在 `cluster` 部分添加 `insecure-skip-tls-verify: true`：

```yaml
apiVersion: v1
clusters:
- cluster:
    insecure-skip-tls-verify: true  # 添加这行
    server: https://<your-server-ip>:6443
  name: k3s
# ... 其他配置
```

保存后测试：

```bash
kubectl get nodes
k9s
```

**解决方法 3：使用内网 IP（如果可访问）**

如果你的 Mac 可以访问服务器的内网 IP，修改 kubeconfig：

```bash
# macOS
sed -i '' 's/<public-ip>/<private-ip>/g' ~/.kube/config

# Linux
sed -i 's/<public-ip>/<private-ip>/g' ~/.kube/config

# 测试连接
kubectl get nodes
k9s
```

**验证步骤：**

```bash
# 1. 测试 kubectl 连接
kubectl cluster-info

# 2. 获取节点
kubectl get nodes

# 3. 查看详细日志（如果还有问题）
kubectl get nodes -v=8

# 4. 启动 k9s
k9s
```

#### 5. 日志不显示

**问题表现：**
- 按 `l` 查看日志时没有输出
- 日志窗口空白

**解决方法：**

```bash
# 检查 Pod 状态
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>

# 直接使用 kubectl 查看日志
kubectl logs <pod-name> -n <namespace>

# 检查日志权限
kubectl auth can-i get pods/log

# 检查容器是否在运行
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.phase}'

# 如果是多容器 Pod，指定容器
kubectl logs <pod-name> -c <container-name> -n <namespace>

# 在 k9s 中：
# 1. 选中 Pod 按 Enter 查看详情
# 2. 确认容器状态
# 3. 按 l 查看日志
# 4. 如果是多容器，按数字键选择容器
```

#### 6. 性能问题（卡顿、延迟）

**问题表现：**
- k9s 响应缓慢
- 界面刷新延迟
- CPU 占用高

**优化方法：**

```bash
# 方法 1：增加刷新间隔
k9s --refresh 5  # 5秒刷新一次

# 方法 2：修改配置文件
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  refreshRate: 5          # 增加刷新间隔
  logBufferSize: 500      # 减少日志缓冲
  disablePodCounting: true  # 禁用 Pod 计数
  logger:
    tail: 50              # 减少日志行数
    buffer: 1000          # 减少缓冲区
EOF

# 方法 3：限制命名空间
k9s -n specific-namespace  # 只查看特定命名空间

# 方法 4：使用过滤
# 在 k9s 中按 / 然后输入过滤条件

# 方法 5：检查系统资源
top
# htop
free -h
df -h
```

#### 7. 编辑器问题

**问题表现：**
- 按 `e` 编辑资源时报错
- 编辑器无法打开

**解决方法：**

```bash
# 设置默认编辑器
export EDITOR=vim
# export EDITOR=nano
# export EDITOR=vi

# 永久设置（添加到 ~/.bashrc）
echo 'export EDITOR=vim' >> ~/.bashrc
source ~/.bashrc

# 在 k9s 配置中指定
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  editor: vim
EOF

# 验证编辑器设置
echo $EDITOR

# 测试编辑器
vim test.txt
```

#### 8. Shell 进入容器失败

**问题表现：**
- 按 `s` 无法进入容器
- 提示 "executable file not found"

**解决方法：**

```bash
# 检查容器中可用的 Shell
kubectl exec <pod-name> -n <namespace> -- ls -la /bin/sh
kubectl exec <pod-name> -n <namespace> -- ls -la /bin/bash

# 尝试不同的 Shell
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
kubectl exec -it <pod-name> -n <namespace> -- sh

# 配置 k9s 使用特定 Shell
cat > ~/.config/k9s/config.yaml << 'EOF'
k9s:
  shellPod:
    image: busybox:1.35.0
    command: ["/bin/sh"]
    namespace: default
EOF

# 对于最小化镜像（如 distroless），可能需要使用 debug 容器
kubectl debug <pod-name> -it --image=busybox
```

#### 9. 端口转发失败

**问题表现：**
- 按 `p` 或 `Shift+f` 端口转发失败
- 提示端口已被占用

**解决方法：**

```bash
# 检查端口占用
netstat -tuln | grep <port>
ss -tuln | grep <port>
lsof -i :<port>

# 杀死占用端口的进程
# sudo kill -9 <pid>

# 使用不同的本地端口
# 在 k9s 中输入：8081:80（本地8081映射到容器80）

# 直接使用 kubectl 测试
kubectl port-forward pod/<pod-name> 8080:80 -n <namespace>

# 检查防火墙设置
# sudo ufw status
# sudo iptables -L
```

#### 10. 中文显示乱码

**问题表现：**
- 中文字符显示为方块或乱码
- 界面排版错乱

**解决方法：**

```bash
# 检查系统 locale
locale
echo $LANG

# 设置 UTF-8 编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 永久设置（添加到 ~/.bashrc）
cat >> ~/.bashrc << 'EOF'
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
EOF

source ~/.bashrc

# 安装中文字体（如果需要）
# Ubuntu/Debian
# sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei

# CentOS/RHEL
# sudo yum install wqy-zenhei-fonts wqy-microhei-fonts

# 检查终端是否支持 UTF-8
echo $TERM
```

#### 11. 升级 k9s 后配置失效

**问题表现：**
- 升级后配置不生效
- 快捷键改变

**解决方法：**

```bash
# 备份旧配置
cp ~/.config/k9s/config.yaml ~/.config/k9s/config.yaml.bak

# 查看 k9s 版本
k9s version

# 查看配置信息
k9s info

# 重新生成默认配置
mv ~/.config/k9s/config.yaml ~/.config/k9s/config.yaml.old
k9s

# 对比新旧配置
diff ~/.config/k9s/config.yaml.old ~/.config/k9s/config.yaml

# 查看配置文档
# https://k9scli.io/topics/config/
```

### 调试技巧

#### 启用详细日志

```bash
# 启动时启用 debug 日志
k9s --logLevel debug

# 启用 trace 级别日志（最详细）
k9s --logLevel trace

# 实时查看日志
tail -f ~/.local/state/k9s/k9s.log

# 查看最近的错误
grep -i error ~/.local/state/k9s/k9s.log
grep -i panic ~/.local/state/k9s/k9s.log
```

#### 检查系统环境

```bash
# 检查 k9s 版本
k9s version

# 检查 kubectl 版本
kubectl version

# 检查 Go 版本（如果从源码编译）
go version

# 检查系统信息
uname -a
cat /etc/os-release

# 检查环境变量
env | grep -i kube
env | grep -i k9s
```

#### 重置 k9s 配置

```bash
# 完全重置（删除所有配置）
rm -rf ~/.config/k9s
rm -rf ~/.local/state/k9s

# 重新创建目录
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s

# 重新启动 k9s
k9s
```

## 最佳实践

### 1. 日常运维

- 使用 `:pulse` 查看集群整体健康状况
- 定期检查 `:events` 了解集群事件
- 使用 `:no` 监控节点资源使用

### 2. 调试应用

- 先查看 Pod 状态（`:pod`）
- 检查日志（`l`）
- 查看事件（`Shift+E` 插件）
- 必要时进入容器（`s`）

### 3. 安全建议

- 生产环境使用只读模式：`k9s --readonly`
- 配置 RBAC 限制权限
- 避免在 k9s 中直接编辑关键资源

### 4. 团队协作

- 统一配置文件（共享 config.yml）
- 定义标准插件和快捷键
- 文档化常用操作流程

## 与 kubectl 对比

| 操作 | kubectl | k9s |
|------|---------|-----|
| 查看 Pods | `kubectl get pods` | `:pod` |
| 查看日志 | `kubectl logs pod-name` | 选中 Pod 按 `l` |
| 进入容器 | `kubectl exec -it pod-name -- sh` | 选中 Pod 按 `s` |
| 编辑资源 | `kubectl edit deploy name` | 选中资源按 `e` |
| 删除资源 | `kubectl delete pod name` | 选中资源按 `Ctrl+d` |
| 端口转发 | `kubectl port-forward pod-name 8080:80` | 选中资源按 `p` |
| 查看 YAML | `kubectl get pod name -o yaml` | 选中资源按 `y` |

## 学习资源

- [官方 GitHub](https://github.com/derailed/k9s)
- [官方文档](https://k9scli.io/)
- [快捷键速查表](https://k9scli.io/topics/commands/)
- [插件示例](https://github.com/derailed/k9s/tree/master/plugins)

## 总结

k9s 是 Kubernetes 运维人员的得力助手，通过熟练掌握其快捷键和功能，可以大大提升工作效率。建议：

1. 从基本的资源查看开始（`:pod`, `:deploy`, `:svc`）
2. 熟练掌握日志查看和过滤
3. 学习常用快捷键（`d`, `e`, `l`, `s`）
4. 根据需要自定义配置和插件
5. 在非生产环境多练习，熟悉后再用于生产

记住：k9s 只是工具，理解 Kubernetes 的核心概念才是关键！
