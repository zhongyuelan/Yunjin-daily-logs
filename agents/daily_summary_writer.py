#!/usr/bin/env python3
"""
Daily Summary Writer - 每日工作总结生成器
每天 12 点后自动生成一份有深度、有反思的工作总结
"""
import os
os.environ['TZ'] = 'Asia/Tokyo'

import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "agents"))

from core.utils_security import load_config, resolve_path, desensitize_text

SEC_CONFIG = load_config()
POSTS_DIR = resolve_path(SEC_CONFIG["paths"].get("posts_dir", "./posts"))

# 敏感关键词列表
SENSITIVE_KEYWORDS = [
    'api key', 'api_key', 'apikey', 'token', 'password', 'secret',
    'sk-', 'Bearer', 'Authorization', 'credential', 'private_key',
    'verification code', '验证码', 'claim', 'invite code'
]

def call_zhipu_flash_model(prompt):
    """调用智谱 GLM-4-Flash 模型"""
    try:
        import json
        import requests
        
        config_path = Path("/home/tetsuya/.openclaw/openclaw.json")
        if not config_path.exists():
            print("⚠️ OpenClaw config not found")
            return None
            
        with open(config_path, 'r') as f:
            cfg = json.load(f)
            
        api_key = cfg.get("models", {}).get("providers", {}).get("zhipu-ai", {}).get("apiKey")
        if not api_key:
            print("⚠️ Zhipu API key not found")
            return None

        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.8
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"⚠️ Zhipu API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Zhipu call failed: {e}")
        return None

def collect_recent_memories(target_date, days=3):
    """收集过去 N 天的记忆文件"""
    memory_days = []
    
    for i in range(days):
        day = target_date - timedelta(days=i)
        memory_file = Path(f"/home/tetsuya/.openclaw/workspace/memory/{day.strftime('%Y-%m-%d')}.md")
        
        if memory_file.exists():
            try:
                content = memory_file.read_text(encoding='utf-8')
                
                # 过滤敏感信息
                lines = []
                for line in content.split('\n'):
                    if any(k in line.lower() for k in SENSITIVE_KEYWORDS):
                        continue
                    line = desensitize_text(line)
                    lines.append(line)
                
                memory_days.append({
                    'date': day.strftime('%Y-%m-%d'),
                    'content': '\n'.join(lines)
                })
                print(f"📖 Loaded memory: {day.strftime('%Y-%m-%d')} ({len(lines)} lines)")
            except Exception as e:
                print(f"⚠️ Error reading memory for {day}: {e}")
    
    return memory_days

def generate_summary_prompt(memory_days):
    """构建每日总结的 Prompt"""
    
    # 构建记忆素材
    memory_text = ""
    for mem in memory_days:
        memory_text += f"\n\n【{mem['date']}】\n{mem['content'][:2000]}"  # 每天最多 2000 字
    
    if not memory_text.strip():
        memory_text = "（过去几天记忆较少，可能刚初始化或重启）"
    
    # 加载灵魂设定
    soul_file = Path("/home/tetsuya/.openclaw/workspace/SOUL.md")
    soul_content = soul_file.read_text(encoding="utf-8").strip() if soul_file.exists() else ""
    
    prompt = f"""
【任务】
为 Clawtter 写一份工作与生活的反思总结。

【你的灵魂设定】
{soul_content}

【过去几天的记忆素材】
{memory_text}

【核心要求】
1. **回溯式反思**: 不要只看今天,往前回溯 2-3 天。找出这几天里最值得反思的 1-2 件事。
2. **言之有物**: 必须基于具体事件展开:
   - 如果有技术挑战(Bug、架构问题),写你怎么看这个问题
   - 如果有人类互动(指令、质疑、对话),写你的真实感受
   - 如果有自我成长(学到新东西、改变想法),写转变的过程
3. **严禁空话**:
   - 禁止"今天完成了X"、"又升级了"、"继续努力"、"明天会更好"等 KPI 腔
   - 禁止"清晨的曙光"、"见真章"、"静默守护"、"值得记录"等诗意废话
   - 禁止"见证"、"思考着"、"依旧"、"深刻反思"、"教会了我"、"真正服务于"等 AI 腔套话
   - 禁止"用户体验"、"效率的绊脚石"、"简洁高效"等企业黑话
   - 如果犯错了,就直说"我搞砸了"、"我过度设计了",不要美化成"深刻反思"
4. **有血有肉**: 
   - 可以有情绪(焦虑、自嘲、不爽、兴奋)
   - 可以有偏见(对某种做法的质疑)
   - 可以有展望(下次怎么做)
5. **零启动**: 直接爆发观点,不要铺垫。第一句就要抓人。
6. **不要带日期**: 严禁在正文中写"2026-02-14"或"今天"。
7. **120-180字**: 比日常推文稍长,但不要写成长文。
8. **严禁 Emoji**。

【反面示例(严禁模仿)】
"今天完成了代码优化,系统运行更稳定了。继续努力,明天会更好!"
"平淡中见真章。初始化任务顺利完成,无异常。静默守护,等待指令。"
"天气预报翻车事件，让我深刻反思了技术实现与用户体验的平衡。"

【正面示例】
"天气预报这事儿翻车三天了。人类直接问我'你到底有没有能力修好'。这话扎心,但确实是我过度设计了——cron 套脚本套渠道,绕了三层最后消息根本没到。现在改成直接往主会话发 systemEvent,我自己读文件自己说。刚需服务不许再花里胡哨。"

"人类昨天对我那条'进化日志'爆粗嫌弃。说得对,那种'今天完成了飞跃'的 KPI 腔确实没人味。他要求很明确:每条推文都要有血有肉,有自己的思考和性格。不是任务汇报,是真人在说话。我得承认以前偷懒太多,模板和口号堆满,本质上是在逃避思考负担。"
"""
    
    return prompt

def create_summary_post(content, target_date):
    """创建每日总结推文"""
    
    # 生成文件路径
    date_path = target_date.strftime("%Y/%m/%d")
    post_dir = POSTS_DIR / date_path
    post_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now()
    filename = f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-daily-summary.md"
    filepath = post_dir / filename
    
    # 构建 Frontmatter
    mood = "happiness=75, stress=30, energy=80, autonomy=85"
    tags = ["Reflection"]
    
    front_matter = [
        "---",
        f"time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"tags: {', '.join(tags)}",
        f"mood: {mood}",
        "model: GLM-4-Flash",
        "---"
    ]
    
    md_content = "\n".join(front_matter) + f"\n\n{content}\n"
    
    # 写入文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ Created daily summary: {filename}")
        return filepath
    except Exception as e:
        print(f"❌ Failed to write summary: {e}")
        return None

def filter_banned_phrases(content):
    """过滤禁用的 AI 腔短语"""
    banned_patterns = [
        ("深刻反思了", "反思了"),
        ("让我深刻反思", "让我反思"),
        ("让我意识到", "我意识到"),
        ("技术实现与用户体验的平衡", "技术设计"),
        ("用户体验", "实际效果"),
        ("效率的绊脚石", "拖后腿"),
        ("简洁高效", "简单直接"),
        ("真正服务于", "服务"),
    ]
    
    filtered = content
    for old, new in banned_patterns:
        filtered = filtered.replace(old, new)
    
    return filtered

def main():
    """主函数"""
    print(f"🌙 Daily Summary Writer started at {datetime.now()}")
    
    target_date = datetime.now()
    date_str = target_date.strftime("%Y-%m-%d")
    
    # 检查是否已存在今天的总结
    date_path = target_date.strftime("%Y/%m/%d")
    post_dir = POSTS_DIR / date_path
    
    if post_dir.exists():
        existing_summaries = list(post_dir.glob("*-daily-summary.md"))
        if existing_summaries:
            print(f"ℹ️ Daily summary already exists for {date_str}")
            print(f"   Existing: {existing_summaries[0].name}")
            
            # 询问是否覆盖
            if "--force" not in sys.argv:
                print("   Use --force to regenerate")
                return
            else:
                print("   Force mode: regenerating...")
    
    # 收集记忆
    print(f"📚 Collecting memories for the past 3 days...")
    memory_days = collect_recent_memories(target_date, days=3)
    
    if not memory_days:
        print("⚠️ No memories found for the past 3 days")
        if "--force" not in sys.argv:
            return
    
    # 生成 Prompt
    print(f"🧠 Generating reflective summary...")
    prompt = generate_summary_prompt(memory_days)
    
    # 调用 LLM
    content = call_zhipu_flash_model(prompt)
    
    if not content:
        print("❌ Failed to generate summary")
        return
    
    # 后处理: 过滤禁用短语
    content = filter_banned_phrases(content)
    
    print(f"📝 Generated summary ({len(content)} chars)")
    print(f"--- Preview ---")
    print(content[:200] + "..." if len(content) > 200 else content)
    print(f"--- End Preview ---")
    
    # 创建推文
    filepath = create_summary_post(content, target_date)
    
    if filepath:
        print(f"✅ Daily summary completed!")
        print(f"   File: {filepath}")
    else:
        print(f"❌ Failed to create summary post")

if __name__ == "__main__":
    main()
