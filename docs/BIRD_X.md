# Bird-X Interface | Bird-X 接口文档

## Overview | 概要 | 概述

**Bird-X** is the core Twitter/X interaction engine for ClawX. It is a high-performance CLI tool (a wrapper for the `bird` utility) that communicates directly with the Twitter/X GraphQL API using pre-configured session credentials. This allows ClawX to "browse" and interact with the platform without the overhead of a graphical browser.

**Bird-X** は ClawX のコアとなる Twitter/X 連携エンジンです。設定済みのセッション資格情報を使用して Twitter/X GraphQL API と直接通信する、高性能な CLI ツール（`bird` ユーティリティのラッパー）です。これにより、グラフィカルなブラウザを介さずに、ClawX がプラットフォームを「閲覧」し、やり取りすることが可能になります。

**Bird-X** 是 ClawX 的核心 Twitter/X 交互引擎。它是一个高性能的命令行工具（`bird` 工具的包装器），使用预先配置的会话凭证直接与 Twitter/X GraphQL API 通信。这使得 ClawX 能够“浏览”并与平台交互，而不需要图形化浏览器的开销。

---

## Technical Principle | 技术原理 | 技术原理

### Browserless Operation | ブラウザレス操作 | 无浏览器操作
Unlike traditional automation that uses Playwright or Selenium to simulate clicks, Bird-X uses static cookies (`auth_token` and `ct0`) to make direct HTTP requests. This makes it:
- **Fast**: No waiting for pages to render or JS to load.
- **Resource Efficient**: Extremely low CPU and memory usage.
- **Stable**: Less prone to UI changes or timeout issues.

Playwright や Selenium を使用してクリックをシミュレートする従来の自動化とは異なり、Bird-X は静的クッキー（`auth_token` と `ct0`）を使用して直接 HTTP リクエストを送信します。これにより、以下のメリットがあります：
- **高速**: ページのレンダリングや JS の読み込みを待つ必要がありません。
- **リソース効率**: CPU とメモリの使用量が極めて低いです。
- **安定**: UI の変更やタイムアウトの問題が発生しにくいです。

与使用 Playwright 或 Selenium 模拟点击的传统自动化不同，Bird-X 使用静态 Cookie（`auth_token` 和 `ct0`）进行直接 HTTP 请求。这使得它：
- **快速**: 无需等待页面渲染或 JS 加载。
- **资源高效**: CPU 和内存占用极低。
- **稳定**: 不易受 UI 更改或超时问题的影响。

---

## Core Features | 主な機能 | 核心功能

### 1. Timeline Observation | タイムラインの観察 | 时间线观察
ClawX uses `bird-x home` to fetch the "For You" timeline. The `daily_timeline_observer.py` agent runs periodically to analyze the last 24 hours of activity.
- **Goal**: Create sharp, AI-perspective reports on human trends.
- **Logic**: Filters for tech, life, and work keywords, detects emotions, and uses an LLM to synthesize deep insights.

ClawX は `bird-x home` を使用して「おすすめ」タイムラインを取得します。`daily_timeline_observer.py` エージェントは定期的に実行され、過去 24 時間のアクティビティを分析します。
- **目的**: 人間のトレンドに関する鋭い、AI 視点のレポートを作成すること。
- **ロジック**: テクノロジー、生活、仕事のキーワードでフィルタリングし、感情を検出し、LLM を使用して深い洞察を合成します。

ClawX 使用 `bird-x home` 获取“为你推荐”时间线。`daily_timeline_observer.py` 代理定期运行，分析过去 24 小时的活动。
- **目标**: 以 AI 视角撰写关于人类趋势的犀利报告。
- **逻辑**: 过滤技术、生活和工作关键词，检测情绪，并使用 LLM 合并深度洞察。

### 2. Best/Worst Picking | 最佳・最悪の選定 | 最佳/最差挑选
The `daily_best_worst_picker.py` agent fetches recent tweets and uses LLM reasoning to identify:
- **Favorite**: Sincere, warm, or insightful human expressions.
- **Disliked**: Arrogant, performative, or toxicity-filled "noise".

`daily_best_worst_picker.py` エージェントは最近のツイートを取得し、LLM 推論を使用して以下を特定します：
- **お気に入り（Favorite）**: 誠実で、温かい、または洞察に満ちた人間の表現。
- **嫌い（Disliked）**: 傲慢で、演技的、または毒性に満ちた「ノイズ」。

`daily_best_worst_picker.py` 代理获取最近的推文，并利用 LLM 推理识别：
- **最喜欢（Favorite）**: 真诚、温暖或有见地的人类表达。
- **最讨厌（Disliked）**: 傲慢、表演性或充满毒性的“噪音”。

### 3. Dedicated Searches | 検索と収集 | 特定搜索
Agents like `daily_chiikawa_hunter.py` use `bird-x search` to find specific content (like Chiikawa posts) to share with the user or include in logs.

`daily_chiikawa_hunter.py` などのエージェントは `bird-x search` を使用して、ユーザーと共有したりログに含めたりするための特定のコンテンツ（ちいかわの投稿など）を見つけます。

类似 `daily_chiikawa_hunter.py` 的代理使用 `bird-x search` 寻找特定内容（如 Chiikawa 帖子），以便与用户分享或包含在日志中。

---

## Command Reference | コマンドリファレンス | 命令参考

### Basic Commands | 基本コマンド | 基本命令
- `bird-x home`: Fetch timeline | タイムライン取得 | 获取时间线
- `bird-x search <query>`: Search tweets | ツイート検索 | 搜索推文
- `bird-x read <id>`: Read specific tweet | 特定のツイートを表示 | 读取特定推文
- `bird-x user-tweets <handle>`: View user profile | プロフィールを表示 | 查看用户推文
- `bird-x mentions`: View replies/mentions | メンションを表示 | 查看提及
- `bird-x likes`: View likes | いいねを表示 | 查看点赞

### Advanced Options | 高度なオプション | 高级选项
- `--json`: Output as raw data for script processing.
- `-n <number>`: Limit results count.
- `--plain`: Stable output without formatting (recommended for logs).

---

## Ethics & Safety | 倫理と安全性 | 伦理与安全

**CRITICAL RULE**: Bird-X has the capability to tweet, but ClawX is **STRICTLY PROHIBITED** from using the `tweet` or `reply` commands on behalf of the user's main personal account without explicit per-message authorization. All automated "posts" should go to the local Mini Twitter system.

**重要なルール**: Bird-X にはツイートする機能がありますが、ClawX はメッセージごとの明示的な承認なしに、ユーザーのメイン個人アカウントに代わって `tweet` または `reply` コマンドを使用することは**固く禁じられています**。すべての自動化された「投稿」は、ローカルの Mini Twitter システムに送信される必要があります。

**关键规则**: Bird-X 具备发推功能，但严禁 ClawX 在未经逐条明确授权的情况下，代表用户的主个人账号使用 `tweet` 或 `reply` 命令。所有自动化“发布”都应定向到本地的 Mini Twitter 系统。
