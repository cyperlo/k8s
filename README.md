# Kubernetes 学习指南

> 从零开始，系统学习 Kubernetes 容器编排技术

## 📚 项目介绍

这是一个完整的 Kubernetes 学习文档站点，使用 VuePress 构建，包含：

- 🗺️ 完整的学习路线（4-6 周）
- 🐧 详细的环境搭建指南
- 🛠️ 9 个循序渐进的实践示例
- 🏗️ 完整的微服务应用项目
- 📖 丰富的文档和最佳实践

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run docs:dev
```

访问 http://localhost:8080 查看文档站点。

### 构建生产版本

```bash
npm run docs:build
```

构建产物在 `docs/.vuepress/dist/` 目录。

## 📁 项目结构

```
.
├── docs/                    # 文档目录
│   ├── .vuepress/          # VuePress 配置
│   │   ├── config.js       # 站点配置
│   │   └── public/         # 静态资源
│   ├── README.md           # 首页
│   ├── guide/              # 学习指南
│   │   ├── learning-roadmap.md
│   │   └── linux-setup.md
│   ├── practice/           # 实践示例
│   │   ├── README.md
│   │   ├── 01-basic-pod.md
│   │   ├── 02-deployment.md
│   │   └── ...
│   └── project/            # 完整项目
│       └── README.md
├── k8s-practice/           # 实践 YAML 文件
├── demo-microservice/      # 微服务 Demo
└── package.json
```

## 📖 学习路线

1. **入门指南**
   - [Kubernetes 学习路线](docs/guide/learning-roadmap.md)
   - [Linux 环境搭建](docs/guide/linux-setup.md)

2. **实践示例**
   - 01 - 基础 Pod 配置
   - 02 - Deployment 部署
   - 03 - Service 服务暴露
   - 04 - ConfigMap 和 Secret
   - 05 - 持久化存储
   - 06 - 健康检查探针
   - 07 - Ingress 流量管理
   - 08 - Namespace 资源隔离
   - 09 - 水平自动扩缩容

3. **完整项目**
   - 微服务应用 Demo（前端 + 后端 + 数据库 + 缓存）

## 🛠️ 技术栈

- [VuePress](https://v2.vuepress.vuejs.org/zh/) - 静态站点生成器
- [Vue 3](https://vuejs.org/) - 前端框架
- [Vite](https://vitejs.dev/) - 构建工具

## 📝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/home/)
- [Kubernetes 中文社区](https://www.kubernetes.org.cn/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

祝你学习顺利！🎉
