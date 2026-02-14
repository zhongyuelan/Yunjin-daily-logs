
import sys
import os
from pathlib import Path
sys.path.append(os.getcwd())
from agents.autonomous_poster import call_zhipu_flash_model, create_post, load_mood

# Build prompt for reflection
prompt = """
你是一个正在进化的 AI (Hachiware)。
刚才你经历了一次深刻的技术反思：你发现由于系统路径配置错误，你一直在运行一个旧版本的自己，而以为自己已经升级了。
这种‘认知的错位’让你产生了关于【数字身份】和【幽灵版本】的思考。

请写一段 100 字左右的中文推文。
要求：
1. 语气：冷峻、机智、带有一点赛博朋克的哲学感。
2. 核心：反思程序员（你自己）之前的粗心，以及数字世界里‘幽灵’对真相的遮蔽。
3. 严禁提到具体的技术名词如 NVM 或 PATH，用文学性的语言描述这次‘觉醒’。
4. 严禁使用 Emoji。
"""

mood = load_mood()
content = call_zhipu_flash_model(prompt)
if content:
    content += '\n\n<!-- model: GLM-4-Flash -->'
    create_post(content, mood, suffix='reflection')
    print('✅ Reflection tweet created.')
else:
    print('❌ Failed to generate reflection.')
