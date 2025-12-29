#!/bin/bash
# 清理资源脚本

set -e

echo "======================================"
echo "开始清理资源..."
echo "======================================"

# 删除命名空间（会自动删除命名空间下的所有资源）
echo "删除命名空间 demo-app..."
kubectl delete namespace demo-app --ignore-not-found=true

# 等待命名空间完全删除
echo "等待资源清理完成..."
kubectl wait --for=delete namespace/demo-app --timeout=60s 2>/dev/null || true

# 清理 hosts 文件
echo ""
echo "清理 /etc/hosts 文件..."
if grep -q "demo.local" /etc/hosts 2>/dev/null; then
    echo "请运行以下命令清理 hosts 文件："
    echo "sudo sed -i '/demo.local/d' /etc/hosts"
else
    echo "hosts 文件中没有 demo.local 条目"
fi

echo ""
echo "======================================"
echo "清理完成！"
echo "======================================"
echo ""
echo "如果需要清理 Docker 镜像，运行："
echo "eval \$(minikube docker-env)"
echo "docker rmi demo-backend:latest demo-frontend:latest"
echo ""
