# Qwen3-TTS TTS 服务修复计划

## TL;DR

> **目标**: 修复 TTS Pod 启动失败问题（transformers 架构不识别错误）
>
> **方案**: 切换为 `vllm/vllm-openai:v0.14.0` 基础镜像，启动时从源码安装 vllm-omni
>
> **修改范围**: 仅修改 `HelmChart/custom-chart/values.yaml`，不碰 template 和 Dockerfile
>
> **启动时间**: 预计 2-5 分钟（克隆仓库 + pip 安装）
>
> **并行执行**: NO（单文件修改）

---

## 上下文

### 问题现象
```
The checkpoint you are trying to load has model type `qwen3_tts` but Transformers does not recognize this architecture.
```

### 问题根因
1. 当前使用 `vllm/vllm-omni:v0.14.0rc1` 预发布镜像，版本不稳定
2. `bootstrap: "pip install -U transformers flash-attn"` 导致 transformers 升级到 5.0.0，与 vllm 0.14.0 不兼容
3. vllm-omni 需要**从源码安装**，pip 安装的 vllm-omni 包版本不匹配

### 解决方案
使用稳定版 `vllm/vllm-openai:v0.14.0` 镜像，启动时执行：
1. 克隆 vllm-omni 仓库
2. pip install -e 安装 vllm-omni
3. 安装 qwen-tts 和 flash-attn

---

## Work Objectives

### Core Objective
修复 TTS 服务配置，使 Qwen3-TTS-12Hz-1.7B-CustomVoice 模型能正常加载和提供服务

### Concrete Deliverables
- 修改 `HelmChart/custom-chart/values.yaml` 中的 TTS 服务配置

### Definition of Done
- [ ] Pod 成功启动且不再报 transformers 架构错误
- [ ] 服务能通过 8006 端口响应请求

### Must Have
- 使用 vllm/vllm-openai:v0.14.0 稳定版镜像
- 从源码安装 vllm-omni
- 安装 qwen-tts 包注册 qwen3_tts 架构

### Must NOT Have
- 不修改 template 文件
- 不创建 Dockerfile
- 不使用 vllm-omni 预发布镜像

---

## 执行策略

### 依赖矩阵
| 任务 | 依赖 | 并行 | 说明 |
|------|------|------|------|
| 1 | None | No | 单文件修改，无需并行 |

---

## TODOs

### 任务 1: 更新 TTS 服务配置

**优先级**: High

**修改内容**:
```yaml
# HelmChart/custom-chart/values.yaml 第 264-301 行

tts:
  enabled: true
  image:
    repository: "vllm/vllm-openai"  # 从 vllm/vllm-omni 改为 vllm/vllm-openai
    tag: "v0.14.0"                   # 从 v0.14.0rc1 改为 v0.14.0 稳定版
    pullPolicy: Always
  bootstrap: |                       # 多行命令安装依赖
    echo "Cloning vllm-omni repository..."
    git clone --depth 1 https://github.com/vllm-project/vllm-omni.git /tmp/vllm-omni
    
    echo "Installing vllm-omni from source..."
    pip install -e /tmp/vllm-omni --no-deps 2>/dev/null || pip install -e /tmp/vllm-omni
    
    echo "Installing qwen-tts..."
    pip install qwen-tts
    
    echo "Installing flash-attn..."
    pip install -U flash-attn --no-build-isolation
    
    echo "Bootstrap complete!"
  replicaCount: 1
  model:
    name: "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
    path: "/models/Qwen3-TTS-12Hz-1.7B-CustomVoice"
  resources:
    limits:
      nvidia.com/gpu: 1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: memorysize
            operator: In
            values:
            - 16GB
  service:
    port: 8006
  extraArgs:
    - "--tensor-parallel-size"
    - "1"
    - "--gpu-memory-utilization"
    - "0.85"
    - "--max-model-len"
    - "4096"
    - "--max-num-seqs"
    - "128"
    - "--trust-remote-code"
    - "--dtype"
    - "float16"
```

**关键变更说明**:
1. **镜像**: `vllm/vllm-omni:v0.14.0rc1` → `vllm/vllm-openai:v0.14.0`
   - 从预发布版切换到稳定版
2. **bootstrap**: 多行命令字符串
   - 克隆 vllm-omni 仓库（--depth 1 加速）
   - pip install -e 从源码安装
   - 安装 qwen-tts 注册模型架构
   - 安装 flash-attn 优化推理

**文件路径**: `/Users/kyoku/Documents/GCC/local-llm/HelmChart/custom-chart/values.yaml`

**行号范围**: 264-301

**Acceptance Criteria**:
- [ ] 镜像和标签正确更新
- [ ] bootstrap 字段改为多行 YAML 字符串格式（使用 `|` 管道符）
- [ ] 包含完整的安装步骤（clone → install vllm-omni → install qwen-tts → install flash-attn）
- [ ] 文件语法验证通过（无 YAML 格式错误）

**测试验证步骤**:
1. 保存文件后手动验证 YAML 语法：
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('HelmChart/custom-chart/values.yaml'))" && echo "YAML valid!"
   ```
2. 部署后查看 Pod 日志，确认安装流程正常：
   ```bash
   kubectl logs -f deployment/local-llm-tts
   ```
   应看到输出：
   ```
   Cloning vllm-omni repository...
   Installing vllm-omni from source...
   Installing qwen-tts...
   Installing flash-attn...
   Bootstrap complete!
   ```
3. 等待模型加载完成（可能需要 3-5 分钟）
4. 测试服务可用性：
   ```bash
   curl http://<pod-ip>:8006/health
   ```

**Commit**: YES
- 消息: `fix(tts): switch to base vllm-openai image with source-install vllm-omni`
- 文件: `HelmChart/custom-chart/values.yaml`

---

## Commit Strategy

| 任务 | Commit 消息 | 修改文件 |
|------|-------------|----------|
| 1 | `fix(tts): switch to base vllm-openai image with source-install vllm-omni` | `HelmChart/custom-chart/values.yaml` |

---

## 部署命令

修改完成后，执行：

```bash
# 1. 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('HelmChart/custom-chart/values.yaml'))" && echo "YAML valid!"

# 2. 应用 Helm 更新（在仓库根目录执行）
helm upgrade local-llm ./HelmChart/custom-chart -f ./HelmChart/custom-chart/values.yaml

# 3. 等待 Pod 重启并查看日志
kubectl get pods -w
kubectl logs -f deployment/local-llm-tts

# 4. 验证服务（等模型加载完成后）
curl http://tts-service-url:8006/health
```

---

## Rollback Plan

如果修复后出现问题，快速回滚：

```bash
# 查看 Helm 历史版本
helm history local-llm

# 回滚到上一个版本
helm rollback local-llm <previous-revision-number>
```

---

## 预期启动流程

Pod 启动后会看到类似日志：

```
Running bootstrap command: echo "Cloning vllm-omni repository..."
...
Cloning vllm-omni repository...
Installing vllm-omni from source...
Installing qwen-tts...
Installing flash-attn...
Bootstrap complete!
vllm serve /models/Qwen3-TTS-12Hz-1.7B-CustomVoice ...
INFO 01-31 06:12:34 gpu_executor.py:85] # GPU blocks: 1234, # CPU blocks: 567
INFO 01-31 06:12:35 model_runner.py:1234] Successfully loaded model Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
```

**启动时间**: ~2-5 分钟（取决于网络速度和 GitHub 连接）

**注意**: 首次启动需要下载和编译，可能需要耐心等待。
