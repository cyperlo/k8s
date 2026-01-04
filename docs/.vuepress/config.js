import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { defineUserConfig } from 'vuepress'
import { searchPlugin } from '@vuepress/plugin-search'

export default defineUserConfig({
  lang: 'zh-CN',
  title: 'Kubernetes 学习指南',
  description: '从零开始，系统学习 Kubernetes 容器编排技术',
  
  bundler: viteBundler(),
  
  theme: defaultTheme({
    logo: '/images/k8s-logo.png',
    
    navbar: [
      { text: '首页', link: '/' },
      { text: '学习路线', link: '/guide/learning-roadmap' },
      { text: '环境搭建', link: '/guide/linux-setup' },
      {
        text: '实践教程',
        children: [
          { text: '基础实践', link: '/practice/' },
          { text: '完整项目', link: '/project/' },
        ],
      },
      {
        text: '工具指南',
        children: [
          { text: 'k9s 完整指南', link: '/guide/k9s-guide' },
          { text: 'k9s 快速参考', link: '/guide/k9s-cheatsheet' },
          { text: '故障排查', link: '/guide/troubleshooting' },
          { text: 'Telepresence', link: '/guide/telepresence-guide'}

        ],
      },
      {
        text: '参考资料',
        children: [
          { text: 'Kubernetes 官方文档', link: 'https://kubernetes.io/zh-cn/docs/home/' },
          { text: '官方交互式教程', link: 'https://kubernetes.io/zh-cn/docs/tutorials/' },
          { text: 'Play with K8s', link: 'https://labs.play-with-k8s.com/' },
        ]
      },
    ],
    
    sidebar: {
      '/guide/': [
        {
          text: '入门指南',
          children: [
            '/guide/learning-roadmap.md',
            '/guide/linux-setup.md',
            '/guide/k9s-guide.md',
            '/guide/k9s-cheatsheet.md',
            '/guide/troubleshooting.md',
            '/guide/telepresence-guide.md',
          ],
        },
      ],
      '/practice/': [
        {
          text: '实践示例',
          children: [
            '/practice/README.md',
            '/practice/01-basic-pod.md',
            '/practice/02-deployment.md',
            '/practice/03-service.md',
            '/practice/04-configmap-secret.md',
            '/practice/05-persistent-volume.md',
            '/practice/06-health-checks.md',
            '/practice/07-ingress.md',
            '/practice/08-namespace.md',
            '/practice/09-hpa.md',
          ],
        },
      ],
      '/project/': [
        {
          text: '完整项目',
          children: [
            '/project/README.md',
          ],
        },
      ],
    },
    
    // 编辑链接
    editLink: false,
    
    // 最后更新时间
    lastUpdated: true,
    lastUpdatedText: '最后更新',
    
    // 贡献者
    contributors: false,
    
    // 页面滚动
    smoothScroll: true,
  }),
  
  // 插件配置
  plugins: [
    searchPlugin({
      // 搜索框占位符
      locales: {
        '/': {
          placeholder: '搜索文档',
        },
      },
      // 热键
      hotKeys: ['s', '/'],
      // 最大搜索建议数
      maxSuggestions: 10,
      // 是否在页面的标题中搜索
      isSearchable: (page) => page.path !== '/',
      // 获取页面的搜索索引
      getExtraFields: (page) => page.frontmatter.tags ?? [],
    }),
  ],
  
  // 端口配置
  port: 8080,
  
  // 开发服务器配置
  host: '0.0.0.0',
})
