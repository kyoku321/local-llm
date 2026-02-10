import json
import sys
import time
import requests
import yaml
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://step.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
MODEL_NAME = "step3p5-flash"

def test_math_reasoning():
    """测试数学推理能力 - 针对 AIME/HMMT 水平的题目"""
    prompt = """
你是一个数学专家。请仔细分析以下数学问题，并给出完整的解题过程。

问题：设实数 x, y 满足 x² + y² = 1，求表达式 x⁴ + y⁴ + x²y² 的最大值和最小值。

要求：
1. 详细展示解题思路和步骤
2. 使用多种方法验证结果
3. 给出最终答案
"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.3,
    }
    
    try:
        resp = requests.post(URL, json=payload, timeout=120, verify=False)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def test_coding_agent():
    """测试编程和智能体能力 - 针对 SWE-bench 水平的任务"""
    prompt = """
你是一个专业的 Python 开发者。请完成以下任务：

任务：编写一个函数，实现快速排序算法，并对其进行优化：
1. 使用三数取中法选择枢轴
2. 对小数组使用插入排序优化
3. 添加尾递归优化
4. 提供完整的单元测试

要求：
1. 代码必须有完整的文档字符串
2. 使用类型提示
3. 考虑边界情况
"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 8192,
        "temperature": 0.3,
    }
    
    try:
        resp = requests.post(URL, json=payload, timeout=120, verify=False)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def test_long_context():
    """测试长上下文处理能力 - 256K context"""
    # 生成一个较长的上下文
    long_context = "\n".join([f"第{i}段：这是测试文本的第{i}段内容，用于测试模型的长上下文处理能力。" for i in range(1, 201)])
    
    prompt = f"""
你是一个文档分析师。请分析以下长文档，并回答问题。

文档内容：
{long_context}

问题：请总结这篇文章的主要内容，并列出关键要点。
"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.3,
    }
    
    try:
        resp = requests.post(URL, json=payload, timeout=120, verify=False)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def test_chinese_nlp():
    """测试中文自然语言处理能力"""
    prompt = """
你是一个专业的中文编辑。请完成以下任务：

1. 阅读以下中文文章
2. 提取文章的核心观点
3. 分析文章的写作手法
4. 评价文章的思想深度

文章：
"在人工智能快速发展的今天，我们见证了技术从工具走向伙伴的转变。Step 3.5 Flash 的发布，标志着开源模型在推理能力和效率上达到了新的高度。它采用稀疏 MoE 架构，每 token 只激活 11B 参数，却能实现媲美闭源大模型的推理深度。这种"智能密度"的提升，不仅降低了推理成本，更为本地化部署提供了可能。技术的进步最终要服务于人类，期待更多开发者能够利用这类开源模型，推动 AI 应用的普及和创新。"
"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.5,
    }
    
    try:
        resp = requests.post(URL, json=payload, timeout=120, verify=False)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def test_parallel_thinking():
    """测试并行思维（Parallel Thinking）能力"""
    prompt = """
请仔细思考以下悖论问题：

"一个时间旅行者回到过去，在他父亲出生之前杀死了他祖父。那么，这个时间旅行者是否还存在？如果不存在，他又如何完成这个行为？"

请：
1. 从逻辑学角度分析
2. 从时间悖论理论角度分析
3. 提出你自己的解决方案
4. 讨论这个问题对自由意志的启示
"""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
    }
    
    try:
        resp = requests.post(URL, json=payload, timeout=120, verify=False)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("=" * 60)
    print("Step 3.5 Flash 模型核心能力测试")
    print("=" * 60)
    
    tests = [
        ("数学推理测试", test_math_reasoning),
        ("编程智能体测试", test_coding_agent),
        ("长上下文测试", test_long_context),
        ("中文NLP测试", test_chinese_nlp),
        ("并行思维测试", test_parallel_thinking),
    ]
    
    for name, test_func in tests:
        print(f"\n{'=' * 60}")
        print(f"[{name}]")
        print(f"{'=' * 60}\n")
        
        start_time = time.time()
        result = test_func()
        elapsed_time = time.time() - start_time
        
        print(f"耗时: {elapsed_time:.2f}秒")
        print(f"\n结果:\n{result}")
        print("\n")
