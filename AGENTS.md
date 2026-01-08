# Local LLM Testing Repository - Agent Guidelines

## 项目概述

本项目是一个 Python 3.12 项目，用于测试本地 LLM API（OpenAI 兼容端点）。包含针对各种 LLM 模型（GPT-OSS、Qwen、GLM）和嵌入模型的测试脚本。

## 构建命令

- **Docker 构建**: `docker build -f Dev/Dockerfile .`
- **Python 脚本执行**: `python3 Dev/script_name.py`

## 测试命令

- **运行单个测试**: `python3 Dev/test_llm.py`
- **运行所有测试**: `python3 Dev/test_*.py`（手动逐个运行）
- **当前无 pytest/unittest 框架**

## 代码风格指南

### 基础规范

- Python 版本: 3.12+
- 文件编码: UTF-8

### 命名约定

- 函数和变量使用 `snake_case`: `get_article_text()`
- 模块常量使用 `UPPER_SNAKE_CASE`: `MODEL_NAME`, `URL`
- 类名使用 `PascalCase`（如有需要）

### 导入组织

```python
# 标准库导入
import json
import sys
import time
from pathlib import Path

# 第三方库导入
import requests
import yaml
import numpy as np

# 本地模块导入（如有）
# from .module import func
```

### 错误处理

- 使用 `try/except` 进行异常捕获
- 添加重试逻辑（通常 3 次重试，5 秒间隔）
- 打印错误信息并返回合理的默认值
- 示例:

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error on attempt {attempt + 1}: {e}")
        if attempt < max_retries - 1:
            time.sleep(5)
        else:
            return default_value
```

### Docstring 要求

所有函数必须包含 docstring，说明功能、参数和返回值:

```python
def process_article_with_local_llm(title, link):
    """
    使用本地模型生成翻译后的标题、摘要和标签。

    Args:
        title: 文章标题
        link: 文章链接

    Returns:
        tuple: (翻译标题, 摘要, 标签列表)
    """
```

### 类型提示

- 不强制要求，但推荐使用
- 保持与现有代码一致的风格

## Kubernetes/Helm 规范

- 遵循 `HelmChart/custom-chart/` 中的现有模式
- 使用 `templates/` 目录存放 K8s 资源清单
- 配置修改更新 `values.yaml`
- 模板使用 Jinja2 语法

## 当前无 Lint 命令

建议后续添加:
- **Ruff**: `ruff check .` 和 `ruff format .`
- **Black**: `black .`
- **Flake8**: `flake8 .`

## 依赖管理

- 当前无 `requirements.txt`
- 项目依赖包括: `requests`, `pyyaml`, `numpy`, `beautifulsoup4`
- 建议添加 `requirements.txt` 或 `pyproject.toml`

## 注意事项

1. 测试脚本包含硬编码的 API 端点 URL
2. 部分脚本禁用 SSL 证书验证（`verify=False`），生产环境需注意
3. 遵循现有代码的函数结构和错误处理模式
