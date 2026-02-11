
import sys
import os
import requests
import json
from pathlib import Path

# Add imports
PROJECT_ROOT = Path('/home/tetsuya/mini-twitter')
sys.path.append(str(PROJECT_ROOT / 'agents'))

# Import Zhipu caller
from autonomous_poster import call_zhipu_flash_model

def post_tweet(content, tags="DailySummary"):
    """简约版发推函数"""
    # 这里我们直接模拟发推逻辑，或者如果你想真的发，需要把 autonomous_poster 里的 post_comment... 拷过来
    # 为了省事，我直接用 autonomous_poster 里的逻辑
    today_str = "2026-02-11" # 假定今天
    post_file = PROJECT_ROOT / f"posts/{today_str}_manual_summary.md"
    
    md_content = f"""---
date: {today_str}
tags: {tags}
---

{content}
"""
    post_file.write_text(md_content, encoding="utf-8")
    print(f"✅ Tweet saved to {post_file}")
    
    # 尝试更新 index.html? 
    # 可以调用 render.py 但有点麻烦。这里先把文件写进去。
    # 如果想推送到 GitHub... 需要 git 操作。
    # 这里我们只生成文件。

# Soul Loading
soul = (PROJECT_ROOT / "SOUL.md").read_text() if (PROJECT_ROOT / "SOUL.md").exists() else ""

prompt = f"""
【任务】
用你的新灵魂写一条工作总结。

【你的灵魂】
{soul}

【背景】
今天我们干掉了那些废话连篇的企业规则，换上了这套直接、有观点的新灵魂。
顺便把大模型换成了免费又快的智谱 Flash，虽然过程中那个锁文件有点烦人。
但现在一切正常。

【要求】
短小精悍。带点机智的自嘲。可以直接喷那个锁文件。
"""

print("🚀 Generating with Zhipu Flash...")
content = call_zhipu_flash_model(prompt)

if content:
    print(f"\n📝 Generated:\n{content}\n")
    post_tweet(content)
else:
    print("❌ Generation failed.")
