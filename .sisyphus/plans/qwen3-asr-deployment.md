# Qwen3-ASR-1.7B 模型 Helm Chart 配置

## TL;DR

> 在现有的 vLLM Helm Chart 基础上追加 Qwen3-ASR-1.7B 自动语音识别模型服务配置。参照现有服务模式，在 `values.yaml` 中添加新的服务定义，无需修改模板文件。

> **Deliverables**:
> - `values.yaml` 中添加 `asr` 服务配置
> - 服务端口：8005
> - GPU 配置：2x GPU (32GB)
> - 不启用 Forced Aligner（轻量部署）

> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential
> **Critical Path**: Task 1 (values.yaml 修改)

---

## Context

### Original Request
在本地 vLLM 项目基础上追加 Qwen3-ASR-1.7B 模型部署，参照现有文档并修改 `values.yaml`。

### Interview Summary
**Key Discussions**:
- GPU 资源：选择 2x GPU (32GB) 以获得更稳定的运行环境
- Forced Aligner：选择不启用，仅部署 ASR 功能（轻量部署）
- 端口选择：使用 8005（延续现有端口编号）
- 模型路径：`/models/Qwen3-ASR-1.7B`

**Research Findings**:
- Qwen3-ASR-1.7B 是 vLLM 原生支持的 ASR 模型
- 需要 `vllm[audio]` 依赖（标准 vLLM 镜像已包含）
- 基本部署命令：`vllm serve Qwen/Qwen3-ASR-1.7B`
- 使用 OpenAI 兼容 API 接口

**vLLM-Omni Clarification** (Exploration Agent Findings):
- **Critical Discovery**: "vllm-omni" term does NOT appear anywhere in the codebase
- Standard vLLM (vllm/vllm-openai:v0.12.0) already supports Qwen3-ASR-1.7B natively
- vLLM-Omni is for multimodal models (text+image+audio), not required for ASR-only models
- Standard vLLM serves audio models with same command structure: `vllm serve <model_path>`
- No breaking changes or migration needed - use standard vLLM deployment

### Metis Review
**Identified Gaps** (addressed):
- 无需额外依赖：vLLM 标准镜像已支持音频模型
- 模板适配：现有 Deployment 和 Service 模板已支持多服务配置
- 配置一致性：参照 `kimi` 服务的配置模式（2x GPU + nightly 镜像）
- vLLM-Omni 误解：确认标准 vLLM 足够，无需 vLLM-Omni

---

## Work Objectives

### Core Objective
在 Helm Chart 的 `values.yaml` 中添加 Qwen3-ASR-1.7B 模型服务的完整配置。

### Concrete Deliverables
- `values.yaml` 文件中新增 `asr` 服务配置段
- 服务启用标志 `enabled: true`
- 完整的资源配置、亲和性、服务端口和参数

### Definition of Done
- [ ] `values.yaml` 包含 `asr` 服务配置
- [ ] 服务端口配置为 8005
- [ ] GPU 资源配置为 2x (32GB)
- [ ] 模型路径为 `/models/Qwen3-ASR-1.7B`
- [ ] 配置格式与现有服务保持一致

### Must Have
- 服务配置必须遵循 Helm Chart 模板规范
- 所有必需字段（model, resources, service, extraArgs）必须完整
- GPU 资源配置必须明确（limits.nvidia.com/gpu: 2）

### Must NOT Have (Guardrails)
- **不修改** `deployment.yaml` 或 `service.yaml` 模板文件
- **不添加** Forced Aligner 相关配置（用户已明确选择不启用）
- **不修改** `ingress.yaml`（除非用户明确要求添加 Ingress）
- **不添加** 额外的依赖或 bootstrap 命令

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES (Helm Chart 配置文件)
- **User wants tests**: N/A (配置修改任务，无需测试)
- **Framework**: Manual verification

### Manual QA Procedures

**Configuration Validation**:
- [ ] 使用 `helm template` 验证 YAML 语法正确性
- [ ] 检查 `asr` 服务配置段格式正确
- [ ] 验证所有必需字段存在且类型正确

**Configuration Consistency Check**:
- [ ] 对比 `asr` 配置与现有服务（如 `kimi`）的结构一致性
- [ ] 验证端口编号（8005）未与现有端口冲突
- [ ] 验证 GPU 配置符合用户需求（2x GPU）

**Helm Template Rendering**:
- [ ] 运行 `helm template test . --values values.yaml`
- [ ] 检查生成的 Deployment 资源是否正确
- [ ] 检查生成的 Service 资源是否正确

**Evidence Required**:
- [ ] `helm template` 命令输出（复制粘贴）
- [ ] 配置对比截图（可选）

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: 修改 values.yaml 添加 asr 服务配置
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | None | None (single task) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1 | delegate_task(category="quick", load_skills=["git-master"], ...) |

---

## TODOs

- [ ] 1. 修改 values.yaml 添加 asr 服务配置

  **What to do**:
  - 在 `values.yaml` 的 `services` 字段下添加新的 `asr` 服务配置段
  - 参照现有服务的配置模式（特别是 `kimi` 服务）
- 配置内容：
     ```yaml
     asr:
       enabled: true
       replicaCount: 1
       model:
         name: "Qwen/Qwen3-ASR-1.7B"
         path: "/models/Qwen3-ASR-1.7B"
       resources:
         limits:
           nvidia.com/gpu: 2
       affinity:
         nodeAffinity:
           requiredDuringSchedulingIgnoredDuringExecution:
             nodeSelectorTerms:
             - matchExpressions:
               - key: memorysize
                 operator: In
                 values:
                 - 32GB
       service:
         port: 8005
       extraArgs:
         - "--tensor-parallel-size"
         - "2"
         - "--gpu-memory-utilization"
         - "0.9"
         - "--max-model-len"
         - "4096"
         - "--max-num-seqs"
         - "128"
         - "--trust-remote-code"
         - "--dtype"
         - "bfloat16"
     ```

     **Image Configuration** (Standard vLLM - confirmed via exploration):
     ```yaml
     image:
       repository: "vllm/vllm-openai"
       tag: "v0.12.0"
       pullPolicy: IfNotPresent
     ```
     **Note**: vLLM-Omni is not required for ASR-only models. Standard vLLM (vllm-openai) natively supports Qwen3-ASR-1.7B.
  - 在 `ingress` 配置中添加对应的 host 和 service 路径：
    ```yaml
    - host: asr.aggpf.gpu-k8s.cloudcore-tu.net
      paths:
        - path: /
          pathType: Prefix
          serviceName: asr
    ```

  **Must NOT do**:
  - 不修改 `deployment.yaml` 或 `service.yaml` 模板文件
  - 不添加 Forced Aligner 相关配置
  - 不修改其他服务的配置

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单的 YAML 配置修改任务，无需复杂推理
  - **Skills**: [`git-master`]
    - `git-master`: 熟悉 Git 和文件修改的最佳实践，确保配置格式正确
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: 不适用（后端配置任务）
    - `playwright`: 不适用（无 UI 交互）

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (single task)
  - **Blocks**: None
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL):

  **Pattern References** (现有代码模式):
  - `values.yaml:179-224` (`kimi` 服务配置) - 参照此结构配置 `asr` 服务
  - `values.yaml:24-61` (`llm` 服务配置) - 参照基本服务结构
  - `values.yaml:62-95` (`embedding` 服务配置) - 参照多 GPU 配置模式

  **API/Type References** (Kubernetes 资源):
  - `templates/deployment.yaml:1-80` - Deployment 模板，了解如何渲染服务配置
  - `templates/service.yaml:1-22` - Service 模板，了解端口配置方式

  **Documentation References**:
  - `HelmChart/custom-chart/Chart.yaml` - Helm Chart 元数据
  - `HelmChart/custom-chart/values.yaml` - 配置文件本身

  **WHY Each Reference Matters**:
  - `values.yaml:179-224` (kimi 服务): 作为最佳参照，展示 2x GPU 配置、affinity、extraArgs 的完整格式
  - `templates/deployment.yaml`: 确认模板会正确渲染新增的 `asr` 服务
  - `templates/service.yaml`: 确认 Service 会正确暴露 8005 端口

  **Acceptance Criteria**:

  **Manual Execution Verification**:

  *Configuration Syntax Check*:
  - [ ] 运行 `helm template test . --values values.yaml`
  - [ ] 验证输出无 YAML 语法错误
  - [ ] 验证 `asr` 服务配置段存在

  *Configuration Validation*:
  - [ ] 检查 `asr.enabled` 为 `true`
  - [ ] 检查 `asr.service.port` 为 `8005`
  - [ ] 检查 `asr.resources.limits.nvidia.com/gpu` 为 `2`
  - [ ] 检查 `asr.model.path` 为 `/models/Qwen3-ASR-1.7B`

  *Helm Template Rendering*:
  - [ ] 运行 `helm template test . --values values.yaml | grep -A 50 "name: test-asr"`
  - [ ] 验证生成的 Deployment 包含 `vllm-api` 容器
  - [ ] 验证生成的 Service 包含端口 `8005`
  - [ ] 验证生成的 Service 选择器包含 `app: custom-chart, service: asr`

  *Configuration Consistency*:
  - [ ] 对比 `asr` 配置与 `kimi` 配置的结构一致性
  - [ ] 验证端口编号 8005 未与其他服务冲突

  **Evidence Required**:
  - [ ] `helm template` 命令输出（完整输出或关键部分）
  - [ ] 配置对比截图（可选，用于验证一致性）

  **Commit**: YES
  - Message: `chore(chart): add Qwen3-ASR-1.7B service configuration`
  - Files: `HelmChart/custom-chart/values.yaml`
  - Pre-commit: `helm template test . --values values.yaml`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `chore(chart): add Qwen3-ASR-1.7B service configuration` | values.yaml | `helm template test . --values values.yaml` |

---

## Success Criteria

### Verification Commands
```bash
# 1. 验证 YAML 语法
helm template test . --values values.yaml

# 2. 验证 asr 服务配置存在
helm template test . --values values.yaml | grep -A 5 "name: test-asr"

# 3. 验证端口配置
helm template test . --values values.yaml | grep -E "port: 8005"

# 4. 验证 GPU 配置
helm template test . --values values.yaml | grep -E "nvidia.com/gpu: 2"
```

### Final Checklist
- [ ] All "Must Have" present
  - [ ] `asr` 服务配置段存在于 `values.yaml`
  - [ ] 服务端口配置为 8005
  - [ ] GPU 资源配置为 2x
  - [ ] 模型路径正确
- [ ] All "Must NOT Have" absent
  - [ ] 未修改 `deployment.yaml` 或 `service.yaml`
  - [ ] 未添加 Forced Aligner 配置
  - [ ] 未修改其他服务配置
- [ ] Helm template 渲染无错误
- [ ] 配置格式与现有服务保持一致