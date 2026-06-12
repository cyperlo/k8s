# Kubernetes Linux 环境搭建完整指南

本指南适用于 Ubuntu/Debian 和 CentOS/RHEL 系统。

---

## 📋 系统要求

- **操作系统**：Ubuntu 18.04+、Debian 10+、CentOS 7+、RHEL 7+
- **CPU**：2 核心或以上
- **内存**：2GB 或以上（推荐 4GB）
- **磁盘空间**：20GB 或以上
- **网络**：可访问互联网

---

## 🔧 方案一：使用 Minikube（推荐新手）

### 1. 安装 Docker

#### Ubuntu/Debian
```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker

# 验证安装
docker --version
docker run hello-world
```

#### CentOS/RHEL
```bash
# 安装依赖
sudo yum install -y yum-utils

# 添加 Docker 仓库
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker

# 验证安装
docker --version
docker run hello-world
```

### 2. 安装 kubectl

```bash
# 下载最新稳定版本
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 验证二进制文件（可选）
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

# 安装 kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 验证安装
kubectl version --client --output=yaml
```

### 3. 安装 Minikube

```bash
# 下载 Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# 安装
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 清理下载文件
rm minikube-linux-amd64

# 验证安装
minikube version
```

### 4. 启动 Minikube 集群

```bash
# 使用 Docker 驱动启动（推荐）
minikube start --driver=docker --cpus=2 --memory=2048

# 如果需要更多资源
minikube start --driver=docker --cpus=4 --memory=4096

# 验证集群
kubectl cluster-info
kubectl get nodes

# 查看 Minikube 状态
minikube status
```

### 5. 启用常用插件

```bash
# 启用 Dashboard（Web UI）
minikube addons enable dashboard

# 启用 Metrics Server（用于 HPA 和资源监控）
minikube addons enable metrics-server

# 启用 Ingress Controller
minikube addons enable ingress

# 查看所有插件
minikube addons list

# 访问 Dashboard
minikube dashboard
```

### 6. 配置 kubectl 自动补全

```bash
# 对于 Bash
echo 'source <(kubectl completion bash)' >>~/.bashrc
echo 'alias k=kubectl' >>~/.bashrc
echo 'complete -o default -F __start_kubectl k' >>~/.bashrc
source ~/.bashrc

# 对于 Zsh
echo 'source <(kubectl completion zsh)' >>~/.zshrc
echo 'alias k=kubectl' >>~/.zshrc
source ~/.zshrc
```

---

## 🔧 方案二：使用 Kind（Kubernetes in Docker）

Kind 更轻量，适合 CI/CD 和快速测试。

### 1. 安装 Kind

```bash
# 下载 Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64

# 安装
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# 验证安装
kind version
```

### 2. 创建集群

```bash
# 创建单节点集群
kind create cluster --name my-cluster

# 创建多节点集群
cat <<EOF | kind create cluster --name multi-node --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF

# 查看集群
kind get clusters
kubectl cluster-info --context kind-my-cluster

# 删除集群
kind delete cluster --name my-cluster
```

---

## 🔧 方案三：使用 K3s（轻量级生产级 K8s）

K3s 适合资源受限的环境和边缘计算。

### 1. 安装 K3s

```bash
# 安装 K3s（自动启动）
curl -sfL https://get.k3s.io | sh -
# 国内源使用这个
curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | INSTALL_K3S_MIRROR=cn sh -

# 检查状态
sudo systemctl status k3s

# 配置 kubectl 访问
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config

# 验证
kubectl get nodes
```

### 2. 卸载 K3s

```bash
# 卸载 K3s
/usr/local/bin/k3s-uninstall.sh
```

---

## 🔧 方案四：使用 Kubeadm（生产环境多节点集群）

适合学习生产级部署，需要至少 2 台机器。

### 1. 准备工作（所有节点）

```bash
# 关闭 swap
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# 加载内核模块
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 设置网络参数
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

### 2. 安装容器运行时（containerd）

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y containerd

# 配置 containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
sudo systemctl enable containerd
```

### 3. 安装 kubeadm、kubelet、kubectl

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

### 4. 初始化 Master 节点

```bash
# 在 Master 节点执行
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# 配置 kubectl
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 安装网络插件（Flannel）
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# 验证
kubectl get nodes
kubectl get pods -n kube-system
```

### 5. 加入 Worker 节点

```bash
# 在 Worker 节点执行（token 从 master 节点的 kubeadm init 输出获取）
sudo kubeadm join <master-ip>:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
```

---

## 🛠️ 常用工具安装

### 安装 Helm（Kubernetes 包管理器）

```bash
# 下载安装脚本
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 验证安装
helm version

# 添加常用仓库
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### 安装 k9s（终端 UI）

```bash
# 下载最新版本
curl -sS https://webinstall.dev/k9s | bash

# 或使用包管理器
# Ubuntu/Debian
curl -sS https://webi.sh/k9s | sh

# 运行
k9s
```

### 安装 kubectx 和 kubens（上下文切换工具）

```bash
# 下载
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens

# 使用
kubectx                 # 列出所有上下文
kubectx <context-name>  # 切换上下文
kubens                  # 列出所有命名空间
kubens <namespace>      # 切换命名空间
```

---

## 🧪 验证安装

创建一个测试文件 `test-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-test
spec:
  replicas: 2
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
---
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

运行测试：

```bash
# 应用配置
kubectl apply -f test-deployment.yaml

# 查看资源
kubectl get deployments
kubectl get pods
kubectl get services

# 访问服务（Minikube）
minikube service nginx-service

# 清理
kubectl delete -f test-deployment.yaml
```

---

## 🔍 故障排查

### Minikube 启动失败

```bash
# 查看日志
minikube logs

# 删除并重新创建
minikube delete
minikube start --driver=docker

# 如果 Docker 驱动有问题，尝试其他驱动
minikube start --driver=none  # 需要 root 权限
```

### kubectl 连接失败

```bash
# 检查配置
kubectl config view

# 检查集群状态
kubectl cluster-info

# 重置 kubeconfig
minikube update-context
```

### Pod 无法启动

```bash
# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>

# 查看事件
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 📚 推荐配置

### 创建别名（~/.bashrc 或 ~/.zshrc）

```bash
# kubectl 别名
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kga='kubectl get all'
alias kdp='kubectl describe pod'
alias kl='kubectl logs'
alias kex='kubectl exec -it'

# Minikube 别名
alias mk='minikube'
alias mks='minikube start'
alias mkst='minikube status'
alias mkd='minikube dashboard'
```

### 配置 vim 编辑 YAML

```bash
# 创建 ~/.vimrc
cat <<EOF > ~/.vimrc
set tabstop=2
set shiftwidth=2
set expandtab
set autoindent
syntax on
EOF
```

---

## 🎯 下一步

1. 完成环境搭建后，进入 `k8s-practice/` 目录开始实践
2. 按顺序学习每个示例文件
3. 尝试 `demo-microservice/` 完整项目
4. 查看 `k8s-learning-roadmap.md` 系统学习

祝你学习顺利！🚀
