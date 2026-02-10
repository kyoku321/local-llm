import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://glm.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
MODEL_NAME = "glm-4.7-flash"


def send_test_prompt_with_timing(prompt, enable_thinking=True, temperature=0.7, top_p=1.0, max_new_tokens=4096):
    """
    发送测试提示词并记录响应时间和结果。

    Args:
        prompt: 测试提示词
        enable_thinking: 是否启用思考模式
        temperature: 温度参数
        top_p: top_p 参数
        max_new_tokens: 最大生成 token 数

    Returns:
        tuple: (回复内容, 耗时)
    """
    print(f"\n[Config] Thinking: {enable_thinking} | Temp: {temperature}")
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_new_tokens,
        "temperature": temperature,
        "top_p": top_p,
    }

    if enable_thinking:
        payload["extra_body"] = {"chat_template_kwargs": {"enable_thinking": True}}
    else:
        payload["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}

    try:
        start_time = time.time()
        resp = requests.post(URL, json=payload, timeout=300, verify=False)
        resp.raise_for_status()
        end_time = time.time()

        data = resp.json()
        content = data["choices"][0]["message"]["content"]

        elapsed = end_time - start_time
        print(f"[Response] Time: {elapsed:.2f}s")
        print(content)

        return content, elapsed
    except Exception as e:
        print(f"Error: {e}")
        return None, 0.0


if __name__ == "__main__":
    prompt_logic = "9.11 和 9.9 哪个数值更大？请详细解释你的比较过程。"

    print("\n" + "="*60)
    print("对比测试：GLM 模型 Thinking ON vs OFF")
    print("="*60)

    print("\n[测试 1] Thinking ON")
    print("-" * 60)
    result_on, time_on = send_test_prompt_with_timing(prompt_logic, enable_thinking=True)

    print("\n[测试 2] Thinking OFF")
    print("-" * 60)
    result_off, time_off = send_test_prompt_with_timing(prompt_logic, enable_thinking=False)

    print("\n" + "="*60)
    print("测试结果对比")
    print("="*60)
    print(f"Thinking ON  | 耗时: {time_on:.2f}s")
    print(f"Thinking OFF | 耗时: {time_off:.2f}s")
    print(f"时间差异: {abs(time_on - time_off):.2f}s")
    print("\n" + "-"*60)
    print("回复内容对比:")
    print("-"*60)
    print("Thinking ON:")
    print(result_on)
    print("\nThinking OFF:")
    print(result_off)
