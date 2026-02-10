import subprocess
import os

def run_opencode_task(prompt, model="kimi-k2.5-free"):
    """
    通用 opencode 辅助函数，封装了绝对路径和提供者前缀。
    """
    # 确保模型 ID 包含 opencode/ 前缀
    if '/' not in model:
        model_id = f"opencode/{model}"
    else:
        model_id = model

    # 使用绝对路径运行 opencode
    opencode_path = "/home/tetsuya/.opencode/bin/opencode"
    
    print(f"🤖 Opencode Agent: Running task with model {model_id}...")
    
    try:
        result = subprocess.run(
            [opencode_path, 'run', '--model', model_id],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"❌ Opencode failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"⚠️ Opencode error: {e}")
        return None
