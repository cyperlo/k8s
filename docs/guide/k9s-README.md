# k9s 文档说明

本目录包含 k9s（Kubernetes 终端 UI 工具）的完整文档。

## 文档列表

### 1. k9s-guide.md - 完整指南
**适合人群**：初学者和需要详细了解 k9s 的用户

**内容包括**：
- 详细的安装说明（Linux/macOS/Windows）
- 首次运行配置
- 完整的快捷键列表
- 常用操作示例
- 高级功能（配置、插件、主题）
- 详细的故障排查指南
- 最佳实践

**使用场景**：
- 第一次使用 k9s
- 需要了解高级功能
- 遇到问题需要排查

### 2. k9s-cheatsheet.md - 快速参考手册
**适合人群**：已经熟悉 k9s 基础，需要快速查询的用户

**内容包括**：
- 快捷键速查表
- 常用命令列表
- 配置文件模板
- 常见操作流程
- 故障排查要点

**使用场景**：
- 忘记某个快捷键
- 需要快速查找命令
- 作为日常参考

### 3. k9s-install-linux.sh - 自动安装脚本
**适合人群**：Linux 用户

**功能**：
- 自动检测系统架构
- 下载最新版本
- 自动安装和配置
- 创建必要的目录

**使用方法**：
```bash
# 直接运行
curl -fsSL https://raw.githubusercontent.com/your-repo/k8s-learning/main/docs/guide/k9s-install-linux.sh | bash

# 或下载后运行
wget https://raw.githubusercontent.com/your-repo/k8s-learning/main/docs/guide/k9s-install-linux.sh
chmod +x k9s-install-linux.sh
./k9s-install-linux.sh
```

## 学习路径建议

### 新手入门
1. 阅读 `k9s-guide.md` 的"简介"和"安装"部分
2. 使用 `k9s-install-linux.sh` 安装（Linux 用户）
3. 阅读"快速开始"部分，完成首次配置
4. 学习"核心快捷键"中的基础操作
5. 实践"常用操作示例"

### 进阶使用
1. 学习"高级功能"部分
2. 自定义配置文件
3. 创建自己的插件
4. 优化工作流程

### 日常使用
1. 将 `k9s-cheatsheet.md` 作为快速参考
2. 遇到问题查看"故障排查"部分
3. 定期查看官方文档了解新功能

## 快速链接

- [k9s 官方网站](https://k9scli.io/)
- [k9s GitHub](https://github.com/derailed/k9s)
- [官方文档](https://k9scli.io/topics/install/)
- [快捷键文档](https://k9scli.io/topics/commands/)
- [插件示例](https://github.com/derailed/k9s/tree/master/plugins)

## 常见问题

### Q: 我应该先看哪个文档？
A: 如果是第一次使用，建议从 `k9s-guide.md` 开始。如果已经熟悉基础，可以直接使用 `k9s-cheatsheet.md` 作为参考。

### Q: 安装脚本安全吗？
A: 安装脚本是开源的，你可以先下载查看内容再运行。建议不要直接通过 curl | bash 的方式运行未知脚本。

### Q: 配置文件在哪里？
A: 
- 主配置：`~/.config/k9s/config.yaml`
- 快捷键：`~/.config/k9s/hotkey.yml`
- 插件：`~/.config/k9s/plugin.yml`
- 主题：`~/.config/k9s/skin.yml`
- 日志：`~/.local/state/k9s/k9s.log`

### Q: 如何更新 k9s？
A: 重新运行安装脚本，或者手动下载新版本替换旧的二进制文件。

### Q: k9s 支持哪些 Kubernetes 版本？
A: k9s 支持 Kubernetes 1.18 及以上版本。建议使用最新版本的 k9s 以获得最佳兼容性。

## 贡献

如果你发现文档有错误或需要改进的地方，欢迎提交 Issue 或 Pull Request。

## 许可

本文档遵循项目的开源许可协议。
