# 09 - 水平自动扩缩容

## 📖 概念介绍

HorizontalPodAutoscaler (HPA) 根据 CPU、内存或自定义指标自动调整 Pod 副本数量。

### 核心概念

- **HPA**：水平自动扩缩容
- **Metrics Server**：指标收集服务
- **扩缩容策略**：控制扩缩容速度

## 📝 配置文件

```yaml
# HorizontalPodAutoscaler 示例 - 自动扩缩容
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # CPU 使用率超过 70% 时扩容
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # 内存使用率超过 80% 时扩容
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 缩容前等待 5 分钟
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60  # 每分钟最多缩容 50%
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30  # 每 30 秒最多扩容 100%
```

## 🚀 部署步骤

```bash
# 1. 安装 Metrics Server（Minikube）
minikube addons enable metrics-server

# 2. 创建 Deployment
kubectl apply -f 02-deployment.yaml

# 3. 创建 HPA
kubectl apply -f 09-hpa.yaml

# 4. 查看 HPA 状态
kubectl get hpa
kubectl describe hpa nginx-hpa

# 5. 模拟负载测试
kubectl run -it load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://nginx-service; done"

# 6. 观察扩容
kubectl get hpa -w
kubectl get pods -w
```

## 🧪 实践练习

### 简单 HPA 配置

```bash
# 使用命令行创建 HPA
kubectl autoscale deployment nginx-deployment --min=2 --max=10 --cpu-percent=70
```

## 💡 最佳实践

1. **设置合理的阈值**
2. **配置稳定窗口**
3. **监控扩缩容行为**
4. **结合资源限制使用**

## 📚 扩展阅读

- [HPA 官方文档](https://kubernetes.io/zh-cn/docs/tasks/run-application/horizontal-pod-autoscale/)

## ✅ 学习检查

- [ ] 理解 HPA 的工作原理
- [ ] 会配置基于 CPU/内存的 HPA
- [ ] 了解扩缩容策略

## 🎯 恭喜完成

你已经完成了所有实践示例！接下来可以挑战 [完整项目](/project/)。

---

[📥 下载完整 YAML 文件](/k8s-practice/09-hpa.yaml)
