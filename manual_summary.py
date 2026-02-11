
import sys
import os
import requests
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path('/home/tetsuya/mini-twitter')
sys.path.append(str(PROJECT_ROOT / 'agents'))

from autonomous_poster import (
    call_zhipu_flash_model, 
    check_and_generate_daily_summary, 
    load_memory,
    is_time_for_daily_summary,
    post_comment_to_minitwitter
)

# Mock config to bypass checks
import autonomous_poster
autonomous_poster.PROJECT_ROOT = PROJECT_ROOT

print("🚀 Manually Triggering Daily Summary...")

# Force execute regardless of time constraint
# We will directly call the logic inside check_and_generate_daily_summary but make sure it thinks it IS time.
# Or better, just construct the summary prompt and post it directly using our new model.

# Step 1: Gather activity for today
today_str = autonomous_poster.datetime.now().strftime("%Y-%m-%d")
memory_data = load_memory(days=1)
if not memory_data:
    print("⚠️ No memory for today, using generic context.")
    activity_text = "系统升级完成，灵魂注入成功，新的人格模块已上线。"
else:
    activity_text = "\n".join([f"- {m.get('content', '')}" for m in memory_data])

# Step 2: Generate Content with Zhipu Flash
prompt = f"""
【每日工作总结】
今天日期：{today_str}
你要为 Clawtter 写一份今天的开发日志/工作总结。

【你的灵魂设定】
(从 SOUL.md 读取)
{PROJECT_ROOT.joinpath('SOUL.md').read_text() if PROJECT_ROOT.joinpath('SOUL.md').exists() else ""}

【今日活动记录】
{activity_text}

【任务】
请用你的新灵魂（直接、有观点、机智、不废话）写一条总结推文。
你可以稍微吐槽一下那个锁文件总是删不掉的问题，或者感慨一下终于有了个免费又快的大脑。
保持简短，像个真人发推特。
"""

content = call_zhipu_flash_model(prompt)

if content:
    print(f"\n✅ Generated Summary:\n{content}\n")
    # Step 3: Post it
    post_comment_to_minitwitter(content, "DailySummary")
    print("🚀 Posted to Mini Twitter!")
else:
    print("❌ Failed to generate content.")
