# Kimi-K2.5 测试脚本

## 概述

这个目录包含用于测试 Kimi-K2.5 模型的 Python 脚本。

## 文件说明

- `test_kimi.py`: 主测试脚本，包含多种测试用例

## 使用方法

### 基础测试

```bash
python3 test_kimi.py
```

### 测试功能

1. **Thinking 模式测试**: 测试模型的推理能力
2. **Instant 模式测试**: 测试模型的快速响应能力
3. **多模态测试**: 测试图像理解能力（需要提供图像 URL）

### API 端点

- URL: `https://kimi.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions`
- 模型: `moonshotai/Kimi-K2.5`

### 参数说明

- `enable_thinking`: 是否启用 Thinking 模式（默认 True）
- `temperature`: 温度参数（Thinking 模式推荐 1.0，Instant 模式推荐 0.6）
- `top_p`: Top-p 采样参数（推荐 0.95）
- `max_tokens`: 最大生成 token 数（默认 4096）

### 示例

```python
from test_kimi import send_test_prompt

# Thinking 模式
send_test_prompt("9.11 和 9.9 哪个数值更大？", enable_thinking=True)

# Instant 模式
send_test_prompt("你好", enable_thinking=False)
```

## 特性

- 支持 Thinking 和 Instant 两种模式
- 自动显示推理过程（reasoning_content）
- 显示响应时间
- 支持多模态输入（图像）
- 完整的错误处理

## 注意事项

- 证书验证已禁用（`verify=False`）
- 超时时间设置为 300 秒
- 确保网络可以访问 API 端点