---
home: true
title: 首页
heroImage: /images/k8s-hero.png
heroText: Kubernetes 学习指南
tagline: 从零开始，系统学习 Kubernetes 容器编排技术
actions:
  - text: 开始学习 →
    link: /guide/learning-roadmap
    type: primary
  - text: 环境搭建
    link: /guide/linux-setup
    type: secondary

features:
  - title: 🗺️ 完整学习路线
    details: 4-6 周系统化学习计划，从基础到进阶，循序渐进掌握 Kubernetes
  - title: 🐧 多平台支持
    details: 支持 Ubuntu、Debian、CentOS 等主流 Linux 发行版，提供 Minikube、Kind、K3s 等多种环境方案
  - title: 🛠️ 实践为主
    details: 9 个循序渐进的实践示例，涵盖 Pod、Deployment、Service、ConfigMap 等核心概念
  - title: 🏗️ 完整项目
    details: 包含前后端、数据库、缓存的完整微服务应用，学习生产级部署实践
  - title: 📚 丰富文档
    details: 详细的配置说明、故障排查指南、最佳实践建议
  - title: 🚀 持续更新
    details: 跟随 Kubernetes 生态发展，持续更新内容和最佳实践

footer: MIT Licensed | Copyright © 2024
---

## 📊 学习统计

<div style="display: flex; justify-content: space-around; margin: 40px 0; flex-wrap: wrap;">
  <div style="text-align: center; padding: 20px;">
    <div style="font-size: 3em; color: #3eaf7c; font-weight: bold;">5</div>
    <div style="color: #666;">学习指南</div>
  </div>
  <div style="text-align: center; padding: 20px;">
    <div style="font-size: 3em; color: #3eaf7c; font-weight: bold;">9</div>
    <div style="color: #666;">实践示例</div>
  </div>
  <div style="text-align: center; padding: 20px;">
    <div style="font-size: 3em; color: #3eaf7c; font-weight: bold;">1</div>
    <div style="color: #666;">完整项目</div>
  </div>
</div>

## 🎯 快速开始

### 第一步：了解学习路线

查看 [Kubernetes 学习路线](/guide/learning-roadmap)，了解完整的学习计划和知识体系。

### 第二步：搭建学习环境

按照 [Linux 环境搭建指南](/guide/linux-setup) 配置本地 Kubernetes 集群。

### 第三步：动手实践

跟随 [实践示例](/practice/) 逐步学习 Kubernetes 核心概念。

### 第四步：挑战完整项目

部署 [微服务应用 Demo](/project/)，体验生产级应用部署。

## 💡 学习建议

::: tip 动手实践最重要
每学一个概念都要亲自操作，不要只看不练。Kubernetes 是一个实践性很强的技术。
:::

::: tip 从简单开始
先掌握核心概念（Pod、Deployment、Service），再深入高级特性（Ingress、HPA、StatefulSet）。
:::

::: tip 多看官方文档
官方文档是最权威、最准确的信息来源，遇到问题优先查阅官方文档。
:::

::: tip 加入社区
遇到问题可以在 Kubernetes 中文社区、Stack Overflow 等平台寻求帮助。
:::

## 🔗 推荐资源

- [Kubernetes 官方文档](https://kubernetes.io/zh-cn/docs/home/) - 最权威的学习资源
- [Kubernetes 中文社区](https://www.kubernetes.org.cn/) - 中文技术交流平台
- [Play with Kubernetes](https://labs.play-with-k8s.com/) - 免费在线实验环境
- [CNCF 云原生全景图](https://landscape.cncf.io/) - 了解云原生生态

## 📝 文档结构

```
├── 入门指南
│   ├── Kubernetes 学习路线
│   └── Linux 环境搭建
├── 实践示例
│   ├── 01 - 基础 Pod 配置
│   ├── 02 - Deployment 部署
│   ├── 03 - Service 服务暴露
│   ├── 04 - ConfigMap 和 Secret
│   ├── 05 - 持久化存储
│   ├── 06 - 健康检查探针
│   ├── 07 - Ingress 流量管理
│   ├── 08 - Namespace 资源隔离
│   └── 09 - 水平自动扩缩容
└── 完整项目
    └── 微服务应用 Demo
```

## 🎓 适合人群

- 有一定 Linux 基础的开发者
- 了解 Docker 容器技术
- 希望学习容器编排和微服务部署
- 准备从事云原生相关工作

## 🚀 下一步

完成基础学习后，可以继续深入：

- **服务网格**：Istio、Linkerd
- **无服务器**：Knative
- **安全加固**：RBAC、Pod Security Policy
- **多集群管理**：Federation
- **云原生生态**：探索 CNCF 项目

祝你学习顺利！🎉
