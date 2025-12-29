#!/bin/bash
# 部署应用脚本

set -e

echo "======================================"
echo "开始部署应用到 Kubernetes..."
echo "======================================"

# 检查 Minikube 是否运行
if ! minikube status &> /dev/null; then
    echo "错误: Minikube 未运行，请先启动 Minikube"
    echo "运行: minikube start"
    exit 1
fi

# 检查 Ingress 插件
echo "检查 Ingress 插件..."
if ! minikube addons list | grep ingress | grep enabled &> /dev/null; then
    echo "启用 Ingress 插件..."
    minikube addons enable ingress
fi

# 按顺序应用配置
echo ""
echo "1. 创建命名空间..."
kubectl apply -f k8s/01-namespace.yaml

echo ""
echo "2. 创建 ConfigMap..."
kubectl apply -f k8s/02-configmap.yaml

echo ""
echo "3. 创建 Secret..."
kubectl apply -f k8s/03-secret.yaml

echo ""
echo "4. 部署 MySQL..."
kubectl apply -f k8s/04-mysql.yaml

echo ""
echo "5. 部署 Redis..."
kubectl apply -f k8s/05-redis.yaml

echo ""
echo "等待数据库和缓存就绪..."
kubectl wait --for=condition=ready pod -l app=mysql -n demo-app --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis -n demo-app --timeout=60s

echo ""
echo "6. 部署后端服务..."
kubectl apply -f k8s/06-backend.yaml

echo ""
echo "7. 部署前端服务..."
kubectl apply -f k8s/07-frontend.yaml

echo ""
echo "8. 配置 Ingress..."
kubectl apply -f k8s/08-ingress.yaml

echo ""
echo "等待所有 Pod 就绪..."
kubectl wait --for=condition=ready pod --all -n demo-app --timeout=180s

# 配置 hosts
MINIKUBE_IP=$(minikube ip)
echo ""
echo "======================================"
echo "部署完成！"
echo "======================================"
echo ""
echo "Minikube IP: $MINIKUBE_IP"
echo ""
echo "请将以下内容添加到 /etc/hosts 文件："
echo "$MINIKUBE_IP demo.local"
echo ""
echo "运行以下命令添加："
echo "echo \"$MINIKUBE_IP demo.local\" | sudo tee -a /etc/hosts"
echo ""
echo "然后访问："
echo "  前端: http://demo.local/"
echo "  API:  http://demo.local/api/users"
echo ""
echo "查看资源："
echo "  kubectl get all -n demo-app"
echo ""
