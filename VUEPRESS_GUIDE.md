# VuePress 文档站点使用指南

## ✅ 已完成

VuePress 文档站点已成功搭建！

## 🌐 访问地址

开发服务器已启动，访问：

- **本地访问**: http://localhost:8081/
- **网络访问**: http://192.168.0.56:8081/

## 📁 项目结构

```
k8s/
├── docs/                           # VuePress 文档目录
│   ├── .vuepress/
│   │   ├── config.js              # 站点配置（导航、侧边栏等）
│   │   └── public/                # 静态资源（图片等）
│   ├── README.md                  # 首页
│   ├── guide/                     # 学习指南
│   │   ├── learning-roadmap.md   # 学习路线
│   │   └── linux-setup.md        # 环境搭建
│   ├── practice/                  # 实践示例
│   │   ├── README.md
│   │   ├── 01-basic-pod.md
│   │   ├── 02-deployment.md
│   │   ├── 03-service.md
│   │   └── ...
│   └── project/                   # 完整项目
│       └── README.md
├── k8s-practice/                  # 原始 YAML 文件
├── demo-microservice/             # 微服务 Demo
├── package.json
└── README.md
```

## 🎨 主要功能

### 1. 首页
- Hero 区域展示
- 特性卡片
- 快速开始指南
- 学习统计

### 2. 导航栏
- 首页
- 学习路线
- 环境搭建
- 实践教程（下拉菜单）
- 参考资料（外部链接）

### 3. 侧边栏
- 自动生成目录结构
- 分类清晰（入门指南、实践示例、完整项目）

### 4. 内置功能
- ✅ 搜索功能
- ✅ 深色模式切换
- ✅ 响应式设计
- ✅ 代码高亮
- ✅ Markdown 增强
- ✅ 最后更新时间

## 🛠️ 常用命令

### 启动开发服务器
```bash
npm run docs:dev
```

### 构建生产版本
```bash
npm run docs:build
```

构建产物在 `docs/.vuepress/dist/` 目录。

### 停止开发服务器
在终端按 `Ctrl + C`

## 📝 如何编辑文档

### 1. 修改首页
编辑 `docs/README.md`

### 2. 添加新文档
在对应目录下创建 `.md` 文件，例如：
```bash
# 添加新的实践示例
touch docs/practice/10-new-topic.md
```

然后在 `docs/.vuepress/config.js` 的 sidebar 中添加：
```js
sidebar: {
  '/practice/': [
    {
      text: '实践示例',
      children: [
        // ... 其他文件
        '/practice/10-new-topic.md',
      ],
    },
  ],
}
```

### 3. 修改导航栏
编辑 `docs/.vuepress/config.js` 中的 `navbar` 配置

### 4. 修改侧边栏
编辑 `docs/.vuepress/config.js` 中的 `sidebar` 配置

### 5. 添加图片
将图片放到 `docs/.vuepress/public/images/` 目录，然后在 Markdown 中引用：
```markdown
![图片描述](/images/your-image.png)
```

## 🎨 自定义样式

### 修改主题颜色
创建 `docs/.vuepress/styles/palette.scss`：
```scss
// 主题色
$accentColor: #3eaf7c;
$textColor: #2c3e50;
$borderColor: #eaecef;
$codeBgColor: #282c34;
```

### 添加自定义样式
创建 `docs/.vuepress/styles/index.scss`：
```scss
// 自定义样式
.custom-class {
  color: red;
}
```

## 📦 部署

### 部署到 GitHub Pages

1. 修改 `docs/.vuepress/config.js`：
```js
export default defineUserConfig({
  base: '/your-repo-name/',  // 仓库名称
  // ...
})
```

2. 构建：
```bash
npm run docs:build
```

3. 部署到 gh-pages 分支：
```bash
cd docs/.vuepress/dist
git init
git add -A
git commit -m 'deploy'
git push -f git@github.com:username/repo.git main:gh-pages
```

### 部署到 Vercel/Netlify

1. 连接 GitHub 仓库
2. 设置构建命令：`npm run docs:build`
3. 设置输出目录：`docs/.vuepress/dist`

## 💡 Markdown 增强功能

### 提示框
```markdown
::: tip 提示
这是一个提示
:::

::: warning 警告
这是一个警告
:::

::: danger 危险
这是一个危险警告
:::
```

### 代码块高亮
```markdown
\`\`\`js{1,3-5}
// 第 1 行和第 3-5 行会高亮
const a = 1
const b = 2
const c = 3
const d = 4
const e = 5
\`\`\`
```

### 自定义容器
```markdown
::: details 点击展开
这是详细内容
:::
```

## 🔧 故障排查

### 端口被占用
如果 8080 端口被占用，VuePress 会自动使用下一个可用端口（如 8081）。

### 修改默认端口
在 `docs/.vuepress/config.js` 中：
```js
export default defineUserConfig({
  port: 3000,  // 自定义端口
  // ...
})
```

### 清除缓存
```bash
rm -rf docs/.vuepress/.cache docs/.vuepress/.temp
```

### Git 警告
如果看到 git 相关警告，可以忽略，或者提交一次代码：
```bash
git add .
git commit -m "Initial commit"
```

## 📚 参考资料

- [VuePress 官方文档](https://v2.vuepress.vuejs.org/zh/)
- [VuePress 默认主题](https://v2.vuepress.vuejs.org/zh/reference/default-theme/)
- [Markdown 扩展](https://v2.vuepress.vuejs.org/zh/guide/markdown.html)

## 🎯 下一步

1. ✅ 访问 http://localhost:8081/ 查看站点
2. ✅ 浏览各个页面，熟悉结构
3. ✅ 尝试编辑 Markdown 文件，实时预览
4. ✅ 添加自己的内容和图片
5. ✅ 自定义主题颜色和样式
6. ✅ 部署到线上

---

祝你使用愉快！🎉
