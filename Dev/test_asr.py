import json
import sys
import time
import requests
import urllib3
from pathlib import Path

# 禁用证书警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 定义 API 配置
URL = "https://asr.aggpf.gpu-k8s.cloudcore-tu.net/v1/audio/transcriptions"
MODEL_NAME = "Qwen/Qwen3-ASR-1.7B"

def test_asr_with_url(audio_url, language=None):
    """
    使用音频URL测试ASR服务。
    
    Args:
        audio_url: 音频文件的URL
        language: 指定语言（可选，如 "Chinese", "English" 等）
    
    Returns:
        转录的文本和检测到的语言
    """
    try:
        # 下载音频文件
        print(f"正在下载音频: {audio_url}")
        audio_resp = requests.get(audio_url, timeout=30)
        audio_resp.raise_for_status()
        audio_data = audio_resp.content
        
        # 准备请求
        files = {
            'file': ('audio.wav', audio_data, 'audio/wav'),
        }
        data = {
            'model': MODEL_NAME,
        }
        if language:
            data['language'] = language
        
        print(f"正在发送ASR请求...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    URL,
                    files=files,
                    data=data,
                    timeout=300,
                    verify=False
                )
                resp.raise_for_status()
                result = resp.json()
                
                text = result.get('text', '')
                detected_language = result.get('language', 'unknown')
                
                return text, detected_language
                
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return f"ASR请求失败: {str(e)}", None
                    
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None, None

def test_asr_with_openai_sdk(audio_url):
    """
    使用OpenAI SDK风格测试ASR服务（多模态chat completions API）。
    
    Args:
        audio_url: 音频文件的URL
    
    Returns:
        转录的文本
    """
    chat_url = "https://asr.aggpf.gpu-k8s.cloudcore-tu.net/v1/chat/completions"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "audio_url",
                        "audio_url": {
                            "url": audio_url
                        }
                    }
                ]
            }
        ],
        "max_tokens": 256
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = requests.post(chat_url, json=payload, timeout=300, verify=False)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            
            return content
            
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return f"ASR请求失败: {str(e)}"

def main():
    """主测试函数"""
    print("=" * 60)
    print("Qwen3-ASR-1.7B 测试脚本")
    print("=" * 60)
    
    # 测试音频URL（官方示例）
    test_audios = [
        {
            "url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav",
            "name": "英语语音识别",
            "expected_language": "English"
        },
        {
            "url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_zh.wav",
            "name": "中文语音识别",
            "expected_language": "Chinese"
        }
    ]
    
    print("\n--- 测试 1: OpenAI Transcription API ---")
    for audio_info in test_audios:
        print(f"\n测试: {audio_info['name']}")
        print(f"音频URL: {audio_info['url']}")
        
        text, detected_lang = test_asr_with_url(
            audio_info['url'], 
            language=audio_info.get('expected_language')
        )
        
        if text:
            print(f"✓ 识别结果: {text}")
            if detected_lang:
                print(f"✓ 检测语言: {detected_lang}")
        else:
            print(f"✗ 识别失败")
    
    print("\n" + "=" * 60)
    print("--- 测试 2: OpenAI Chat Completions API (多模态) ---")
    for audio_info in test_audios:
        print(f"\n测试: {audio_info['name']}")
        
        result = test_asr_with_openai_sdk(audio_info['url'])
        
        if result and not result.startswith("ASR请求失败"):
            print(f"✓ 识别结果: {result}")
        else:
            print(f"✗ {result}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
