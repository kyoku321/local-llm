# Update Model Configuration Plan

## TL;DR

更新 `oh-my-opencode.json` 配置文件，根据模型能力将三个模型分配到相应角色。

**修改内容**:
- **kimi-k2p5**: 核心决策 + 复杂执行 (sisyphus, oracle, ultrabrain, unspecified-high)
- **qwen3-coder-next**: 代码专家 (frontend-ui-ux-engineer, librarian, visual-engineering)
- **glm-4.7-flash**: 快速响应 (其他所有角色和分类)

---

## Context

### Original Request
根据模型能力分配角色，优化配置文件的性能。

### Model Capabilities
- **kimi-k2p5**: 最强的推理能力和综合能力，适合复杂任务和架构设计
- **qwen3-coder-next**: 代码专用模型，擅长编程和前端开发
- **glm-4.7-flash**: 快速响应模型，适合轻量级并行任务

---

## Work Objectives

### Core Objective
优化模型分配，使每个角色使用最适合的模型。

### Concrete Deliverables
- 更新后的 `~/.config/opencode/oh-my-opencode.json`

### Definition of Done
- [ ] 配置文件已更新
- [ ] JSON 格式验证通过
- [ ] 所有角色已正确分配

---

## TODOs

- [ ] 1. 备份原配置文件

  **What to do**:
  - 复制原文件到备份位置
  
  **Command**:
  ```bash
  cp ~/.config/opencode/oh-my-opencode.json ~/.config/opencode/oh-my-opencode.json.backup
  ```

  **Acceptance Criteria**:
  - [ ] 备份文件已创建
  - [ ] `ls ~/.config/opencode/oh-my-opencode.json.backup` 成功

  **Commit**: NO

---

- [ ] 2. 更新 agents 配置

  **What to do**:
  - 修改 JSON 文件中的 agents 部分
  - 保持当前配置（已经合理）:
    - sisyphus: local-kimi/kimi-k2p5
    - oracle: local-kimi/kimi-k2p5
    - frontend-ui-ux-engineer: local-qwen/qwen3-coder-next
    - librarian: local-qwen/qwen3-coder-next
    - explore: local-glm/glm-4.7-flash
    - multimodal-looker: local-glm/glm-4.7-flash
    - prometheus: local-glm/glm-4.7-flash
    - metis: local-glm/glm-4.7-flash
    - momus: local-glm/glm-4.7-flash
    - atlas: local-glm/glm-4.7-flash

  **Acceptance Criteria**:
  - [ ] agents 部分更新完成

  **Commit**: NO

---

- [ ] 3. 更新 categories 配置

  **What to do**:
  - 修改 categories 部分的模型分配:
    - visual-engineering: local-qwen/qwen3-coder-next (前端工程需要代码能力)
    - ultrabrain: local-kimi/kimi-k2p5 (深度推理需要最强模型)
    - artistry: local-glm/glm-4.7-flash (创意任务)
    - quick: local-glm/glm-4.7-flash (快速响应)
    - unspecified-low: local-glm/glm-4.7-flash (简单任务)
    - unspecified-high: local-kimi/kimi-k2p5 (复杂任务)
    - writing: local-glm/glm-4.7-flash (写作任务)

  **Acceptance Criteria**:
  - [ ] categories 部分更新完成

  **Commit**: NO

---

- [ ] 4. 验证 JSON 格式

  **What to do**:
  - 使用 Python 验证 JSON 格式
  
  **Command**:
  ```bash
  python3 -c "import json; json.load(open('~/.config/opencode/oh-my-opencode.json')); print('JSON valid')"
  ```

  **Acceptance Criteria**:
  - [ ] JSON 格式验证通过
  - [ ] 输出显示 "JSON valid"

  **Commit**: NO

---

- [ ] 5. 清理备份文件

  **What to do**:
  - 删除备份文件

  **Command**:
  ```bash
  rm ~/.config/opencode/oh-my-opencode.json.backup
  ```

  **Acceptance Criteria**:
  - [ ] 备份文件已删除

  **Commit**: NO

---

## Updated Configuration

```json
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  "agents": {
    "sisyphus": {
      "model": "local-kimi/kimi-k2p5"
    },
    "oracle": {
      "model": "local-kimi/kimi-k2p5"
    },
    "frontend-ui-ux-engineer": {
      "model": "local-qwen/qwen3-coder-next"
    },
    "librarian": {
      "model": "local-qwen/qwen3-coder-next"
    },
    "explore": {
      "model": "local-glm/glm-4.7-flash"
    },
    "multimodal-looker": {
      "model": "local-glm/glm-4.7-flash"
    },
    "prometheus": {
      "model": "local-glm/glm-4.7-flash"
    },
    "metis": {
      "model": "local-glm/glm-4.7-flash"
    },
    "momus": {
      "model": "local-glm/glm-4.7-flash"
    },
    "atlas": {
      "model": "local-glm/glm-4.7-flash"
    }
  },
  "categories": {
    "visual-engineering": {
      "model": "local-qwen/qwen3-coder-next"
    },
    "ultrabrain": {
      "model": "local-kimi/kimi-k2p5"
    },
    "artistry": {
      "model": "local-glm/glm-4.7-flash"
    },
    "quick": {
      "model": "local-glm/glm-4.7-flash"
    },
    "unspecified-low": {
      "model": "local-glm/glm-4.7-flash"
    },
    "unspecified-high": {
      "model": "local-kimi/kimi-k2p5"
    },
    "writing": {
      "model": "local-glm/glm-4.7-flash"
    }
  }
}
```

---

## Success Criteria

### Final Checklist
- [ ] 配置文件已更新
- [ ] JSON 格式验证通过
- [ ] 所有角色分配合理
- [ ] 备份已清理
