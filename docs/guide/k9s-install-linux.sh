#!/bin/bash
# k9s 自动安装脚本 - Linux 系统
# 用法: bash k9s-install-linux.sh

set -e

echo "=========================================="
echo "k9s 自动安装脚本"
echo "=========================================="

# 检测系统架构
ARCH=$(uname -m)
case $ARCH in
    x86_64)
        ARCH="amd64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
    armv7l)
        ARCH="arm"
        ;;
    *)
        echo "错误: 不支持的架构 $ARCH"
        exit 1
        ;;
esac

echo "检测到系统架构: $ARCH"

# 获取最新版本
echo "正在获取最新版本..."
LATEST_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_VERSION" ]; then
    echo "错误: 无法获取最新版本信息"
    echo "请检查网络连接或手动指定版本"
    exit 1
fi

echo "最新版本: $LATEST_VERSION"

# 下载 URL
DOWNLOAD_URL="https://github.com/derailed/k9s/releases/download/${LATEST_VERSION}/k9s_Linux_${ARCH}.tar.gz"
TEMP_DIR=$(mktemp -d)
DOWNLOAD_FILE="${TEMP_DIR}/k9s.tar.gz"

echo "下载地址: $DOWNLOAD_URL"
echo "正在下载..."

# 下载文件
if command -v wget &> /dev/null; then
    wget -q --show-progress -O "$DOWNLOAD_FILE" "$DOWNLOAD_URL"
elif command -v curl &> /dev/null; then
    curl -L -o "$DOWNLOAD_FILE" "$DOWNLOAD_URL"
else
    echo "错误: 需要 wget 或 curl 来下载文件"
    exit 1
fi

# 解压
echo "正在解压..."
tar -xzf "$DOWNLOAD_FILE" -C "$TEMP_DIR"

# 安装
echo "正在安装..."
if [ -w /usr/local/bin ]; then
    mv "$TEMP_DIR/k9s" /usr/local/bin/
    chmod +x /usr/local/bin/k9s
else
    echo "需要 sudo 权限来安装到 /usr/local/bin"
    sudo mv "$TEMP_DIR/k9s" /usr/local/bin/
    sudo chmod +x /usr/local/bin/k9s
fi

# 清理
echo "正在清理临时文件..."
rm -rf "$TEMP_DIR"

# 创建配置目录
echo "正在创建配置目录..."
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s

# 验证安装
echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
k9s version

echo ""
echo "配置目录已创建:"
echo "  - ~/.config/k9s"
echo "  - ~/.local/state/k9s"
echo ""
echo "使用方法:"
echo "  k9s              # 启动 k9s"
echo "  k9s --help       # 查看帮助"
echo "  k9s -n default   # 指定命名空间"
echo ""
echo "首次运行建议:"
echo "  1. 确保 kubectl 已配置: kubectl cluster-info"
echo "  2. 启动 k9s: k9s"
echo "  3. 按 ? 查看帮助"
echo ""
