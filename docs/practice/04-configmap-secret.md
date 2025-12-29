# 04 - ConfigMap 和 Secret

## 📖 概念介绍

ConfigMap 和 Secret 用于将配置信息与应用代码分离，实现配置的集中管理。

### 核心概念

- **ConfigMap**：存储非敏感配置数据
- **Secret**：存储敏感信息（密码、密钥等）
- **环境变量注入**：将配置作为环境变量传递给容器
- **文件挂载**：将配置作为文件挂载到容器

## 📝 配置文件

```yaml
# ConfigMap 示例
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    database.host=mysql-service
    database.port=3306
    log.level=info
  APP_ENV: "production"
  MAX_CONNECTIONS: "100"

---
# Secret 示例
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  # 使用 base64 编码：echo -n 'mypassword' | base64
  db-password: bXlwYXNzd29yZA==
  api-key: c2VjcmV0a2V5MTIz

---
# 使用 ConfigMap 和 Secret 的 Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-config
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:1.21
        env:
        # 从 ConfigMap 读取环境变量
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_ENV
        # 从 Secret 读取环境变量
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: db-password
        # 挂载 ConfigMap 为文件
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: config-volume
        configMap:
          name: app-config
```

## 🚀 部署步骤

### 1. 创建 ConfigMap

```bash
# 方法 1：从 YAML 文件创建
kubectl apply -f 04-configmap-secret.yaml

# 方法 2：从命令行创建
kubectl create configmap app-config \
  --from-literal=APP_ENV=production \
  --from-literal=MAX_CONNECTIONS=100

# 方法 3：从文件创建
kubectl create configmap app-config \
  --from-file=app.properties

# 查看 ConfigMap
kubectl get configmap
kubectl describe configmap app-config
```

### 2. 创建 Secret

```bash
# 方法 1：从 YAML 文件创建
kubectl apply -f 04-configmap-secret.yaml

# 方法 2：从命令行创建
kubectl create secret generic app-secret \
  --from-literal=db-password=mypassword \
  --from-literal=api-key=secretkey123

# 方法 3：从文件创建
kubectl create secret generic app-secret \
  --from-file=./password.txt

# 查看 Secret
kubectl get secrets
kubectl describe secret app-secret

# 查看 Secret 内容（base64 解码）
kubectl get secret app-secret -o jsonpath='{.data.db-password}' | base64 --decode
```

### 3. 使用配置

```bash
# 部署应用
kubectl apply -f 04-configmap-secret.yaml

# 验证环境变量
kubectl exec -it <pod-name> -- env | grep APP_ENV

# 验证文件挂载
kubectl exec -it <pod-name> -- cat /etc/config/app.properties
```

## 🧪 实践练习

### 练习 1：Base64 编码

```bash
# 编码
echo -n 'mypassword' | base64
# 输出：bXlwYXNzd29yZA==

# 解码
echo 'bXlwYXNzd29yZA==' | base64 --decode
# 输出：mypassword
```

### 练习 2：更新 ConfigMap

```bash
# 编辑 ConfigMap
kubectl edit configmap app-config

# 或使用 patch
kubectl patch configmap app-config -p '{"data":{"APP_ENV":"staging"}}'

# 注意：需要重启 Pod 才能生效
kubectl rollout restart deployment app-with-config
```

### 练习 3：挂载多个配置

```yaml
volumeMounts:
- name: config-volume
  mountPath: /etc/config
- name: secret-volume
  mountPath: /etc/secrets
  readOnly: true
volumes:
- name: config-volume
  configMap:
    name: app-config
- name: secret-volume
  secret:
    secretName: app-secret
```

## 🔧 常用命令

```bash
# ConfigMap
kubectl create configmap <name> --from-literal=key=value
kubectl get configmap
kubectl describe configmap <name>
kubectl edit configmap <name>
kubectl delete configmap <name>

# Secret
kubectl create secret generic <name> --from-literal=key=value
kubectl get secrets
kubectl describe secret <name>
kubectl get secret <name> -o yaml
kubectl delete secret <name>
```

## 💡 最佳实践

1. **使用 Secret 存储敏感信息**：密码、密钥、证书等
2. **不要在代码中硬编码配置**：使用 ConfigMap/Secret
3. **使用命名空间隔离**：不同环境使用不同的 ConfigMap
4. **定期轮换密钥**：更新 Secret 并重启应用
5. **限制 Secret 访问权限**：使用 RBAC 控制访问

## 📚 扩展阅读

- [ConfigMap 官方文档](https://kubernetes.io/zh-cn/docs/concepts/configuration/configmap/)
- [Secret 官方文档](https://kubernetes.io/zh-cn/docs/concepts/configuration/secret/)

## ✅ 学习检查

- [ ] 理解 ConfigMap 和 Secret 的区别
- [ ] 会创建和使用 ConfigMap
- [ ] 会创建和使用 Secret
- [ ] 理解环境变量注入和文件挂载

## 🎯 下一步

继续学习 [05 - 持久化存储](./05-persistent-volume.md)。

---

[📥 下载完整 YAML 文件](/k8s-practice/04-configmap-secret.yaml)
