#!/bin/bash
# 构建 Docker 镜像脚本

set -e

echo "======================================"
echo "开始构建 Docker 镜像..."
echo "======================================"

# 切换到 Minikube 的 Docker 环境
echo "配置 Docker 环境..."
eval $(minikube docker-env)

# 构建后端镜像
echo ""
echo "构建后端镜像..."
cd app/backend
docker build -t demo-backend:latest .
echo "✓ 后端镜像构建完成"

# 构建前端镜像
echo ""
echo "构建前端镜像..."
cd ../frontend
docker build -t demo-frontend:latest .
echo "✓ 前端镜像构建完成"

# 返回项目根目录
cd ../..

# 查看镜像
echo ""
echo "======================================"
echo "镜像列表："
echo "======================================"
docker images | grep demo-

echo ""
echo "======================================"
echo "镜像构建完成！"
echo "======================================"
