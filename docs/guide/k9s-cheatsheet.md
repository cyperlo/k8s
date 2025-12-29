# k9s 快速参考手册

## 快速启动

```bash
k9s                    # 启动 k9s
k9s -n <namespace>     # 指定命名空间
k9s -A                 # 所有命名空间
k9s --readonly         # 只读模式
k9s --context <ctx>    # 指定上下文
k9s -c pod             # 直接进入 Pod 视图
```

## 核心快捷键

### 导航

| 快捷键 | 功能 |
|--------|------|
| `:` | 命令模式 |
| `/` | 过滤/搜索 |
| `Esc` | 返回/取消 |
| `?` | 帮助 |
| `Ctrl+a` | 显示所有资源别名 |
| `Ctrl+c` | 退出 |

### 资源视图

| 快捷键 | 资源 |
|--------|------|
| `:pod` | Pods |
| `:deploy` | Deployments |
| `:svc` | Services |
| `:ns` | Namespaces |
| `:no` | Nodes |
| `:cm` | ConfigMaps |
| `:sec` | Secrets |
| `:ing` | Ingress |
| `:pv` | PersistentVolumes |
| `:pvc` | PersistentVolumeClaims |

### 资源操作

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 查看详情 |
| `d` | Describe |
| `e` | 编辑 |
| `l` | 查看日志 |
| `y` | 查看 YAML |
| `s` | Shell 进入容器 |
| `p` | 端口转发 |
| `Ctrl+d` | 删除 |
| `Ctrl+k` | 强制删除 Pod |

### 日志操作

| 快捷键 | 功能 |
|--------|------|
| `l` | 查看日志 |
| `0-9` | 选择容器 |
| `f` | 自动滚动 |
| `w` | 自动换行 |
| `t` | 显示时间戳 |
| `c` | 清空日志 |
| `/` | 搜索 |
| `n` | 下一个结果 |
| `N` | 上一个结果 |

### 命名空间

| 快捷键 | 功能 |
|--------|------|
| `0` | 所有命名空间 |
| `:ns` | 命名空间视图 |
| `Enter` | 切换命名空间 |

## 常用命令

### 查看资源

```
:pod                   # 查看 Pods
:deploy                # 查看 Deployments
:svc                   # 查看 Services
:no                    # 查看 Nodes
:events                # 查看事件
:pulse                 # 集群健康状况
```

### 过滤搜索

```
/nginx                 # 搜索包含 nginx
/!running              # 排除 running 状态
/error|fail            # 搜索 error 或 fail
```

## 配置文件

### 主配置文件

位置：`~/.config/k9s/config.yaml`

```yaml
k9s:
  refreshRate: 2
  maxConnRetry: 5
  enableMouse: false
  readOnly: false
  logger:
    tail: 100
    buffer: 5000
```

### 快捷键配置

位置：`~/.config/k9s/hotkey.yml`

```yaml
hotKey:
  shift-0:
    shortCut: Shift-0
    description: View pods
    command: pods
```

### 插件配置

位置：`~/.config/k9s/plugin.yml`

```yaml
plugin:
  top:
    shortCut: Shift-T
    description: Top
    scopes:
      - pods
    command: kubectl
    args:
      - top
      - pod
      - $NAME
      - -n
      - $NAMESPACE
```

## 常见操作流程

### 查看 Pod 日志

```
1. :pod
2. / 搜索 Pod 名称
3. 选中 Pod
4. 按 l 查看日志
5. 按 f 开启自动滚动
```

### 进入容器

```
1. :pod
2. 选中 Pod
3. 按 s 进入 Shell
4. 多容器时选择容器编号
```

### 端口转发

```
1. :pod 或 :svc
2. 选中资源
3. 按 p
4. 输入 本地端口:远程端口
5. Enter 确认
```

### 编辑资源

```
1. 进入资源视图
2. 选中资源
3. 按 e 编辑
4. 修改后保存退出
```

### 删除资源

```
1. 选中资源
2. 按 Ctrl+d
3. 输入资源名称确认
```

## 故障排查

### 无法连接集群

```bash
kubectl cluster-info
kubectl config current-context
k9s --logLevel debug
```

### 配置文件错误

```bash
mkdir -p ~/.config/k9s
mkdir -p ~/.local/state/k9s
rm -f ~/.config/k9s/config.yaml
k9s
```

### 权限不足

```bash
kubectl auth can-i --list
k9s --readonly
```

### 查看日志

```bash
tail -f ~/.local/state/k9s/k9s.log
```

## Shell 别名

添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
alias k9='k9s'
alias k9p='k9s -n production'
alias k9d='k9s -n development'
alias k9ro='k9s --readonly'
alias k9log='tail -f ~/.local/state/k9s/k9s.log'
```

## 环境变量

```bash
export EDITOR=vim              # 设置编辑器
export K9S_CONFIG_DIR=~/.config/k9s
export K9S_LOG_DIR=~/.local/state/k9s
```

## 与 kubectl 对比

| kubectl | k9s |
|---------|-----|
| `kubectl get pods` | `:pod` |
| `kubectl logs pod-name` | 选中 Pod 按 `l` |
| `kubectl exec -it pod-name -- sh` | 选中 Pod 按 `s` |
| `kubectl edit deploy name` | 选中资源按 `e` |
| `kubectl delete pod name` | 选中资源按 `Ctrl+d` |
| `kubectl port-forward pod 8080:80` | 选中资源按 `p` |
| `kubectl get pod name -o yaml` | 选中资源按 `y` |
| `kubectl describe pod name` | 选中资源按 `d` |

## 学习资源

- 官方文档：https://k9scli.io/
- GitHub：https://github.com/derailed/k9s
- 快捷键：https://k9scli.io/topics/commands/
- 插件：https://github.com/derailed/k9s/tree/master/plugins

## 提示

1. 按 `?` 随时查看帮助
2. 使用 `/` 快速过滤资源
3. 生产环境使用 `--readonly` 模式
4. 定期查看 `:events` 了解集群状态
5. 使用 `:pulse` 查看集群健康状况
6. 多练习快捷键提高效率
7. 自定义配置和插件适应工作流
