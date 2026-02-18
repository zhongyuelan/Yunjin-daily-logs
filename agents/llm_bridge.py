#!/usr/bin/env python3
import json
import requests
import subprocess
from pathlib import Path

def call_minimax_llm(prompt, system_prompt="You are a helpful assistant.", model="MiniMax-M2.1"):
    """
    调用 MiniMax API (Anthropic 兼容格式)
    """
    try:
        config_path = Path("/Users/zhongyuelan/.openclaw/openclaw.json")
        if not config_path.exists():
            return None, None
            
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        
        # 获取 MiniMax 配置
        mm_config = cfg.get("models", {}).get("providers", {}).get("minimax-portal", {})
        api_key = mm_config.get("apiKey")
        base_url = mm_config.get("baseUrl", "https://api.minimaxi.com")
        
        if not api_key or api_key == "minimax-oauth":
            # OAuth 模式需要特殊处理，这里尝试直接用 token
            return None, None
        
        url = f"{base_url}/v1/text/chatcompletion_v2"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data, timeout=120)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip(), f"minimax/{model}"
    except Exception as e:
        print(f"⚠️ MiniMax call failed: {e}")
    return None, None

def call_zhipu_llm(prompt, system_prompt="You are a helpful assistant."):
    """
    尝试调用智谱 GLM-4-Flash 免费模型。
    """
    try:
        config_path = Path("/home/tetsuya/.openclaw/openclaw.json")
        if not config_path.exists():
            return None
            
        with open(config_path, 'r') as f:
            cfg = json.load(f)
            
        api_key = cfg.get("models", {}).get("providers", {}).get("zhipu-ai", {}).get("apiKey")
        if not api_key:
            return None

        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip(), "zhipu/glm-4-flash"
    except Exception as e:
        print(f"⚠️ Zhipu call failed: {e}")
    return None, None

def call_opencode_llm(prompt, model="kimi-k2.5-free"):
    """
    备用方案：调用 Opencode CLI。
    """
    opencode_path = "/home/tetsuya/.opencode/bin/opencode"
    model_id = f"opencode/{model}" if '/' not in model else model
    
    print(f"🤖 Falling back to Opencode CLI ({model_id})...")
    
    try:
        result = subprocess.run(
            [opencode_path, 'run', '--model', model_id],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return result.stdout.strip(), model_id
    except Exception as e:
        print(f"⚠️ Opencode CLI failed: {e}")
    return None, None

def ask_llm(prompt, system_prompt=None, fallback_model="MiniMax-M2.1"):
    """
    统一 LLM 调用接口：
    1. 优先尝试 MiniMax API
    2. 失败则尝试智谱
    3. 最后回退到 Opencode CLI
    """
    # 1. 尝试 MiniMax
    try:
        if system_prompt:
            content, model = call_minimax_llm(prompt, system_prompt, fallback_model)
        else:
            content, model = call_minimax_llm(prompt, "You are a helpful assistant.", fallback_model)
        if content:
            return content, model
    except:
        pass
        
    # 2. 尝试智谱
    try:
        content, model = call_zhipu_llm(prompt, system_prompt) if system_prompt else call_zhipu_llm(prompt)
        if content:
            return content, model
    except:
        pass
        
    # 3. 回退到 Opencode
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"
        
    return call_opencode_llm(full_prompt, model=fallback_model)
