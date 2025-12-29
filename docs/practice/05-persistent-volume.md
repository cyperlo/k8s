# 05 - 持久化存储

## 📖 概念介绍

PersistentVolume (PV) 和 PersistentVolumeClaim (PVC) 提供了持久化存储的抽象，使数据能够在 Pod 重启后保留。

### 核心概念

- **PersistentVolume (PV)**：集群级别的存储资源
- **PersistentVolumeClaim (PVC)**：用户对存储的请求
- **StorageClass**：动态存储供应
- **AccessModes**：访问模式（ReadWriteOnce、ReadOnlyMany、ReadWriteMany）

## 📝 配置文件

```yaml
# PersistentVolume 示例
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: "/mnt/data/mysql"

---
# PersistentVolumeClaim 示例
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: manual

---
# 使用 PVC 的 MySQL Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "rootpassword"
        - name: MYSQL_DATABASE
          value: "mydb"
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
```

## 🔍 访问模式

| 模式 | 说明 |
|------|------|
| ReadWriteOnce (RWO) | 单节点读写 |
| ReadOnlyMany (ROX) | 多节点只读 |
| ReadWriteMany (RWX) | 多节点读写 |

## 🚀 部署步骤

```bash
# 1. 创建 PV 和 PVC
kubectl apply -f 05-persistent-volume.yaml

# 2. 查看 PV 和 PVC
kubectl get pv
kubectl get pvc

# 3. 查看绑定状态
kubectl describe pvc mysql-pvc

# 4. 部署 MySQL
kubectl apply -f 05-persistent-volume.yaml

# 5. 验证数据持久化
kubectl exec -it <mysql-pod> -- mysql -uroot -prootpassword -e "CREATE DATABASE testdb;"
kubectl delete pod <mysql-pod>
# Pod 重建后数据仍然存在
```

## 💡 最佳实践

1. **使用 StorageClass 动态供应**
2. **设置合适的回收策略**
3. **定期备份重要数据**
4. **监控存储使用情况**

## 📚 扩展阅读

- [PersistentVolume 官方文档](https://kubernetes.io/zh-cn/docs/concepts/storage/persistent-volumes/)
- [StorageClass](https://kubernetes.io/zh-cn/docs/concepts/storage/storage-classes/)

## ✅ 学习检查

- [ ] 理解 PV 和 PVC 的关系
- [ ] 掌握不同的访问模式
- [ ] 能够配置持久化存储

## 🎯 下一步

继续学习 [06 - 健康检查探针](./06-health-checks.md)。

---

[📥 下载完整 YAML 文件](/k8s-practice/05-persistent-volume.yaml)
