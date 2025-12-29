# 使用 Nginx 作为基础镜像
FROM nginx:1.25-alpine

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制前端文件
COPY index.html /usr/share/nginx/html/

# 暴露端口
EXPOSE 80

# Nginx 会自动启动
CMD ["nginx", "-g", "daemon off;"]
