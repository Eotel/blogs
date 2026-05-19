---
title: "AI エージェント"
description: "自律的にタスク実行できる AI システム。複数ステップの処理を自己制御で進める"
date: 2026-04-06
lastmod: 2026-05-19
aliases: ["AI Agent", "エージェント", "autonomous agent"]
related_posts:
  - "/posts/2026/05/maeda-taro-parasite-human/"
  - "/posts/2026/03/ai-agent-qa/"
  - "/posts/2026/03/claude-code-agent-teams/"
  - "/posts/2026/04/autoagent-self-improving-agents/"
  - "/posts/2026/04/gemini-agent-mode/"
  - "/posts/2026/04/claude-managed-agents/"
  - "/posts/2026/04/claude-managed-agents-architecture/"
  - "/posts/2026/04/anthropic-vs-openai-harness-strategy/"
  - "/posts/2026/04/agent-harness-memory-lock-in/"
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
  - "/posts/2026/02/2026-02-26-5017f19e6544b679fb98156a068b72d5/"
  - "/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/"
  - "/posts/2026/02/2026-02-27-5fcb10cb6bcc6b0c29f2b1e01d1c0855/"
  - "/posts/2026/03/2026-03-01-0f8f4e791ffdc6f04b19e54918192cb3/"
  - "/posts/2026/03/2026-03-01-1a7265c8ba51f09a06687b88ffe260e9/"
  - "/posts/2026/03/2026-03-02-0248d4f7dad745c12a44f107f17dee96/"
  - "/posts/2026/03/2026-03-02-5397a5cafe03e38ff0d72d6de0718221/"
  - "/posts/2026/03/2026-03-02-cec4801cc76906a7815e96570a3a2376/"
  - "/posts/2026/03/2026-03-02-f5f7afe224494ea830b0e01b607fbbc8/"
  - "/posts/2026/03/2026-03-03-1ddcd07ed2cfe5a9510119208b4376e2/"
  - "/posts/2026/03/2026-03-03-91ce402f4341983abe89cff8bd4989fd/"
  - "/posts/2026/03/2026-03-04-1414271c913ac644731736187882cee2/"
  - "/posts/2026/03/2026-03-04-179a96f4a2907544469cb7055564ac6c/"
  - "/posts/2026/03/2026-03-04-2fb1416daa8c7baf370c69d0b1649625/"
  - "/posts/2026/03/2026-03-04-3f7fd4d71d99ff458323f987d2431c8b/"
  - "/posts/2026/03/2026-03-04-400b78c2f6a4ec11b0ec5ddc3ed2d938/"
  - "/posts/2026/03/2026-03-04-5f7b16f99352ba53b24d23586231ff59/"
  - "/posts/2026/03/2026-03-04-911137ea2e4da5af4ed98a6f29e995fb/"
  - "/posts/2026/03/2026-03-04-b22606904c5d5f513556e6a58c3b4657/"
  - "/posts/2026/03/2026-03-04-c05a200a9f27fe9c1fc934bbc0d7906f/"
  - "/posts/2026/03/2026-03-05-35454b5978b916a5aed65f93d54afb5f/"
  - "/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/"
  - "/posts/2026/03/2026-03-05-783efe7ccb15ece292b5d6210664c397/"
  - "/posts/2026/03/2026-03-05-79be6da14ac16c7e51167d5a9747228f/"
  - "/posts/2026/03/2026-03-05-7a124c55c1c58515e7f6370d59fd25ec/"
  - "/posts/2026/03/2026-03-05-7ed089c4237d5da02049b58d9678da5b/"
  - "/posts/2026/03/2026-03-05-9344deb1d9e60907c9fbc5db4fd0f226/"
  - "/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/"
  - "/posts/2026/03/2026-03-05-bdc5082e2f5f8160644bd0ba01f52c76/"
  - "/posts/2026/03/2026-03-05-d6238d29f67740e50870a83860a480fc/"
  - "/posts/2026/03/2026-03-06-e053dfb0c2bee4f36f609060b3dfd487/"
  - "/posts/2026/03/2026-03-09-ai-research-community/"
  - "/posts/2026/03/2026-03-09-gsd-coding-agent/"
  - "/posts/2026/03/2026-03-09-openai-symphony/"
  - "/posts/2026/03/2026-03-09-paperclip-ai-company-os/"
  - "/posts/2026/03/2026-03-09-shenzhen-openclaw-opc/"
  - "/posts/2026/03/2026-03-09-agents-md-less-is-more/"
  - "/posts/2026/03/2026-03-09-karpathy-autoresearch/"
  - "/posts/2026/03/2026-03-10-karpathy-autoresearch/"
  - "/posts/2026/03/2026-03-11-ai-moat-sor-soa/"
  - "/posts/2026/03/2026-03-11-codex-subagent-swarm/"
  - "/posts/2026/03/2026-03-10-openclaw-tiktok-marketing/"
  - "/posts/2026/03/2026-03-10-openclaw-xiaohongshu-agent/"
  - "/posts/2026/03/2026-03-11-bytedance-deerflow/"
  - "/posts/2026/03/2026-03-11-claude-code-vs-codex/"
  - "/posts/2026/03/2026-03-11-openclaw-markdown-agent-stack/"
  - "/posts/2026/03/2026-03-11-openclaw-trading-backtest/"
  - "/posts/2026/03/2026-03-11-opik-openclaw-observability/"
  - "/posts/2026/03/2026-03-11-opik-openclaw/"
  - "/posts/2026/03/2026-03-12-agent-relay-transport/"
  - "/posts/2026/03/2026-03-12-perplexity-personal-computer/"
  - "/posts/2026/03/2026-03-14-agent-governance-toolkit/"
  - "/posts/2026/03/2026-03-15-openclaw-skills-collection/"
  - "/posts/2026/03/2026-03-17-ai-agent-parallel-execution-efficiency/"
  - "/posts/2026/03/2026-03-17-manus-ai-agent-29-features/"
  - "/posts/2026/03/2026-03-17-okara-ai-cmo/"
  - "/posts/2026/03/2026-03-17-paperclipai-zero-human-company/"
  - "/posts/2026/03/2026-03-17-superpowers-ai-coding-agent-framework/"
  - "/posts/2026/03/2026-03-17-takt-ai-agent-workflow/"
  - "/posts/2026/03/2026-03-18-agent-skill-bus/"
  - "/posts/2026/03/2026-03-20-openclaw-gold-rush/"
  - "/posts/2026/03/2026-03-21-openclaw-felix-ai-agent-company/"
  - "/posts/2026/03/2026-03-22-claude-code-hooks-commands-subagents/"
  - "/posts/2026/03/2026-03-22-mcp-oauth21-security/"
  - "/posts/2026/03/2026-03-25-claude-code-expert-agents/"
  - "/posts/2026/03/2026-03-26-dexter-financial-agent/"
  - "/posts/2026/03/2026-03-27-anthropic-harness-design-three-agents/"
  - "/posts/2026/03/2026-03-27-llm-prompt-hardcode-bug/"
  - "/posts/2026/03/2026-03-27-superlocalmemory-v3-ai-agent-memory/"
  - "/posts/2026/03/2026-03-30-toa-services-for-ai-agents/"
  - "/posts/2026/04/2026-04-06-openclaw-gemma4-local-setup/"
  - "/posts/2026/04/2026-04-07-claude-code-chaos-engineer-agent/"
  - "/posts/2026/04/2026-04-07-openclaw-video-generation/"
  - "/posts/2026/04/2026-04-12-openclaw-vs-hermes/"
  - "/posts/2026/04/2026-04-14-claude-code-world-ai-simulator/"
  - "/posts/2026-03-09-ai-agent-qa/"
  - "/posts/2026-03-09-ai-research-community/"
  - "/posts/2026-03-09-harness-engineering/"
  - "/posts/2026-03-10-claude-code-review/"
  - "/posts/2026-03-10-openclaw-claude-code-setup/"
  - "/posts/2026/05/design-md-culture/"
  - "/posts/2026/03/2026-03-03-fbc113dfc0629b475ce1ccf808e859a0/"
  - "/posts/2026/03/2026-03-05-1128207db83f7ca1a2c940dba0fdc2c9/"
tags: ["agent", "LLM", "自律実行", "マネージドエージェント"]
---

## 概要

単一の応答ではなく、複数ステップのタスクを自律実行する AI システム。Claude Code、OpenAI Codex、Cursor など複数ツールで実装されている。エージェント間協調、分散実行、メモリ管理が 2026 年の主要トレンド。

## 主な実装パターン

- **シングルエージェント**: 1つの LLM が計画→実行→検証を繰り返す（Claude Code など）
- **マルチエージェント**: 複数のエージェントが役割分担して協調（Agent Teams）
- **メタエージェント**: エージェントのハーネスを AI 自身が改善（AutoAgent）

## 品質保証

AI エージェントの出力品質を担保するにはハーネスエンジニアリングが必須。CLAUDE.md（入力層）、Hooks（検証層）、Agent Skills（ワークフロー層）の多層構造で品質を保証する。

## エージェント基盤の分類

2026年時点の主要なエージェント基盤は大きく3種類に分類できる。

| 種別 | 代表例 | 特徴 |
|------|--------|------|
| **マネージドクラウド型** | Claude Managed Agents | インフラ不要、スケーラブル、ベンダー依存 |
| **ローカル自律型** | OpenClaw | プライバシー重視、カスタマイズ自由、セルフホスト |
| **クラウド連携型** | Gemini Agent | 特定サービス（Google Workspace 等）に最適化 |

## ハーネスとメモリのロックイン

LangChain 創設者 Harrison Chase が指摘する重要な概念。エージェントのメモリ（長期記憶）はハーネスの設計と不可分であり、クローズドなハーネスを使うと以下のリスクが生じる:

- コンパクション（会話圧縮）のロジックが不透明になる
- 長期メモリが第三者のサーバーに保存される
- ハーネス移行時にメモリの移植が困難になる

## 関連ページ

- [パラサイトヒューマン](/blogs/wiki/concepts/parasite-human/) — 前田太郎が 2000 年代から展開する身体寄生型 AI エージェントの前史
- [Claude Code](/blogs/wiki/tools/claude-code/) — 代表的な AI コーディングエージェント
- [Claude Managed Agents](/blogs/wiki/tools/claude-managed-agents/) — Anthropic のマネージドエージェント基盤
- [Gemini Agent](/blogs/wiki/tools/gemini-agent/) — Google Workspace 連携エージェント
- [OpenClaw](/blogs/wiki/tools/openclaw/) — ローカル自律型エージェント
- [Strands Agents](/blogs/wiki/tools/strands-agents/) — AWS が公開したモデル駆動型 SDK
- [Amazon Bedrock AgentCore](/blogs/wiki/tools/bedrock-agentcore/) — AWS のマネージドエージェント基盤
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — エージェント品質保証の設計パターン
- [自己改善エージェント](/blogs/wiki/concepts/self-improving-agents/) — エージェントが自律的に改善するパターン
- [MCP](/blogs/wiki/concepts/mcp/) — エージェントと外部ツールの接続プロトコル
- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/) — 強くなる AI への監督アプローチ
- [TimesFM](/blogs/wiki/tools/timesfm/) — 時系列予測専用基盤モデル
- [エージェントフレンドリー CLI](/blogs/wiki/concepts/agent-friendly-cli/) — LLM エージェントが確実に操作できる CLI の設計原則

## ソース記事

- [前田太郎のパラサイトヒューマン ── 寄生する計算機から現代 AI エージェントへ](/blogs/posts/2026/05/maeda-taro-parasite-human/) — 2026-05-19
- [AI エージェント QA 手法](/blogs/posts/2026/03/ai-agent-qa/) — 2026-03
- [Claude Code Agent Teams](/blogs/posts/2026/03/claude-code-agent-teams/) — 2026-03
- [AutoAgent](/blogs/posts/2026/04/autoagent-self-improving-agents/) — 2026-04
- [Gemini Agentモード：Google Workspaceを自動化するAIエージェント](/blogs/posts/2026/04/gemini-agent-mode/) — 2026-04-07
- [Claude Managed Agents: パブリックベータ公開](/blogs/posts/2026/04/claude-managed-agents/) — 2026-04-10
- [Claude Managed Agents のアーキテクチャ](/blogs/posts/2026/04/claude-managed-agents-architecture/) — 2026-04-10
- [Anthropic vs OpenAI：Harness 戦略はなぜ真逆なのか](/blogs/posts/2026/04/anthropic-vs-openai-harness-strategy/) — 2026-04-13
- [エージェントハーネスとメモリのロックイン問題](/blogs/posts/2026/04/agent-harness-memory-lock-in/) — 2026-04-12
- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
- [cmux — AIコーディングエージェント時代のターミナル紹介](/blogs/posts/2026/02/2026-02-26-5017f19e6544b679fb98156a068b72d5/) — 2026-02-26
- [Agent Plugins for AWS — AI コーディングエージェントに AWS の専門知識を装着する](/blogs/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/) — 2026-02-27
- [# Claude Code の能力を10倍にする CLAUDE.md — AI エージェントのマネジメント哲学](/blogs/posts/2026/02/2026-02-27-5fcb10cb6bcc6b0c29f2b1e01d1c0855/) — 2026-02-27
- [AI エージェント入門 — 元 Meta エンジニアが説く「オートメーションとエージェントの決定的な違い」](/blogs/posts/2026/03/2026-03-01-0f8f4e791ffdc6f04b19e54918192cb3/) — 2026-03-01
- [Claude Code が汎用AIエージェント基盤へ進化 — Auto Memory・Remote Control・Scheduled Tasks の全貌](/blogs/posts/2026/03/2026-03-01-1a7265c8ba51f09a06687b88ffe260e9/) — 2026-03-01
- [Claude Code スキルで「穴場市場」を自動発掘 — コードを書かない AI エージェント活用術](/blogs/posts/2026/03/2026-03-02-0248d4f7dad745c12a44f107f17dee96/) — 2026-03-02
- [SaaS の終焉（SaaSpocalypse）--- 自律エージェントが Seat 課金を破壊し、ソフトウェア業界を再編する](/blogs/posts/2026/03/2026-03-02-5397a5cafe03e38ff0d72d6de0718221/) — 2026-03-02
- [AIエージェントの勝負所は「モデル性能」ではなく「ハーネス設計」にある](/blogs/posts/2026/03/2026-03-02-cec4801cc76906a7815e96570a3a2376/) — 2026-03-02
- [ハーネスエンジニアリング入門 — AIエージェントの性能はモデルではなく周辺設計で決まる](/blogs/posts/2026/03/2026-03-02-f5f7afe224494ea830b0e01b607fbbc8/) — 2026-03-02
- [「OpenClawで5人解雇」は本当か — AIエージェント煽りの構造とファクトチェック](/blogs/posts/2026/03/2026-03-03-1ddcd07ed2cfe5a9510119208b4376e2/) — 2026-03-03
- [Readout — Claude Code の開発環境をリアルタイム監視する macOS ネイティブアプリと「エージェント監視」カテゴリの台頭](/blogs/posts/2026/03/2026-03-03-91ce402f4341983abe89cff8bd4989fd/) — 2026-03-03
- [AnimaWorks 脳科学5層記憶 × マルチエージェント「文脈崩壊」問題への解答](/blogs/posts/2026/03/2026-03-04-1414271c913ac644731736187882cee2/) — 2026-03-04
- [Anything の Research Agents — 「コードを書く前に調べる」AI エージェントが Vibe Coding の次に来るもの](/blogs/posts/2026/03/2026-03-04-179a96f4a2907544469cb7055564ac6c/) — 2026-03-04
- [Trivy VS Code 拡張が改ざんされ、ローカル AI エージェントが認証情報を窃取 — hackerbot-claw の全貌](/blogs/posts/2026/03/2026-03-04-2fb1416daa8c7baf370c69d0b1649625/) — 2026-03-04
- [macOS Keychain で .env のシークレットを守る — 1Password 不要、無料で実現する AI エージェント時代の秘密管理](/blogs/posts/2026/03/2026-03-04-3f7fd4d71d99ff458323f987d2431c8b/) — 2026-03-04
- [Subagent と Agent Teams の違い — 「働くエージェント」と「議論するエージェント」を設計レイヤで理解する](/blogs/posts/2026/03/2026-03-04-400b78c2f6a4ec11b0ec5ddc3ed2d938/) — 2026-03-04
- [「Claude Codeが無料で使える最強AIエージェント」は本当か — Accomplish の実態とAI煽りの再来](/blogs/posts/2026/03/2026-03-04-5f7b16f99352ba53b24d23586231ff59/) — 2026-03-04
- [AIエージェント「デモ→本番」95%脱落 × 4つの壁とエージェンティックRAG実践](/blogs/posts/2026/03/2026-03-04-911137ea2e4da5af4ed98a6f29e995fb/) — 2026-03-04
- [OpenHands 入門ガイド — 無料・オープンソースの AI コーディングエージェントを自分の PC で動かす](/blogs/posts/2026/03/2026-03-04-b22606904c5d5f513556e6a58c3b4657/) — 2026-03-04
- [SoRからSoAへ — エージェント時代に業務ソフトウェアの「どの層」が死ぬのか](/blogs/posts/2026/03/2026-03-04-c05a200a9f27fe9c1fc934bbc0d7906f/) — 2026-03-04
- [Qwen-Agent 公式エージェントフレームワーク完全ガイド — モデル開発チームが作った「全部入り」の設計思想](/blogs/posts/2026/03/2026-03-05-35454b5978b916a5aed65f93d54afb5f/) — 2026-03-05
- [OpenClaw 22,000字解説のファクトチェック --- AIエージェントの民主化煽りと技術的実態の分離](/blogs/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/) — 2026-03-05
- [Agentic AIの周期表 — 66要素で読み解くAIエージェント構築の全体像](/blogs/posts/2026/03/2026-03-05-783efe7ccb15ece292b5d6210664c397/) — 2026-03-05
- [Goose 完全ガイド — Block が作った無料オープンソース AI エージェントの全貌](/blogs/posts/2026/03/2026-03-05-79be6da14ac16c7e51167d5a9747228f/) — 2026-03-05
- [ClawGTM — OpenClaw を自律型セールスエージェントに変えた「URL 1つで営業パイプライン構築」](/blogs/posts/2026/03/2026-03-05-7a124c55c1c58515e7f6370d59fd25ec/) — 2026-03-05
- [awesome-claws × OpenClawエコシステム28エージェント完全マップと設計思想5分類](/blogs/posts/2026/03/2026-03-05-7ed089c4237d5da02049b58d9678da5b/) — 2026-03-05
- [OpenClaw × Scrapling — AIエージェントが「検出不能なスクレイピング」を手にした日](/blogs/posts/2026/03/2026-03-05-9344deb1d9e60907c9fbc5db4fd0f226/) — 2026-03-05
- [Google Workspace CLI（gws）— Drive・Gmail・Calendarを1コマンドで操作するAIエージェント対応ツール](/blogs/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/) — 2026-03-05
- [OpenFang × Rust製シングルバイナリ「エージェントOS」のHandsアーキテクチャと自律型AI設計](/blogs/posts/2026/03/2026-03-05-bdc5082e2f5f8160644bd0ba01f52c76/) — 2026-03-05
- [gen-ai-experiments × 130超の生成AIアプリを「動かして学ぶ」LangChain・RAG・エージェント実践集](/blogs/posts/2026/03/2026-03-05-d6238d29f67740e50870a83860a480fc/) — 2026-03-05
- [Qwen Code 初心者ガイド — 無料で使えるオープンソース CLI コーディングエージェント](/blogs/posts/2026/03/2026-03-06-e053dfb0c2bee4f36f609060b3dfd487/) — 2026-03-06
- [「研究コミュニティをまるごとエミュレートせよ」— Karpathy が示す AI エージェント協調の未来](/blogs/posts/2026/03/2026-03-09-ai-research-community/) — 2026-03-09
- [GSD — AI コーディングエージェントを「本当に使えるレベル」にするプロジェクト管理システム](/blogs/posts/2026/03/2026-03-09-gsd-coding-agent/) — 2026-03-09
- [OpenAI Symphony — AI エージェントを自律的にオーケストレーションするオープンソースフレームワーク](/blogs/posts/2026/03/2026-03-09-openai-symphony/) — 2026-03-09
- [Paperclip — AIエージェントで会社を自律運営するオープンソースOS](/blogs/posts/2026/03/2026-03-09-paperclip-ai-company-os/) — 2026-03-09
- [深圳が世界初の OpenClaw・一人企業支援策を発表 — AI エージェント時代のソロ起業を後押し](/blogs/posts/2026/03/2026-03-09-shenzhen-openclaw-opc/) — 2026-03-09
- [AGENTS.md は詳しすぎると逆効果 — ETH Zurich の138リポジトリ研究が示す「書かない」原則](/blogs/posts/2026/03/2026-03-09-agents-md-less-is-more/) — 2026-03-09
- [Karpathy の autoresearch — AIが寝ている間に100回実験を回す仕組み](/blogs/posts/2026/03/2026-03-09-karpathy-autoresearch/) — 2026-03-09
- [Karpathy の autoresearch — 寝ている間にAIが100回実験して朝にはモデルが賢くなっている世界](/blogs/posts/2026/03/2026-03-10-karpathy-autoresearch/) — 2026-03-10
- [AI が生み出す新たな Moat：SoR から SoA への構造転換](/blogs/posts/2026/03/2026-03-11-ai-moat-sor-soa/) — 2026-03-11
- [OpenAI Codex の SubAgent（Swarm）が変える AI コーディングの未来](/blogs/posts/2026/03/2026-03-11-codex-subagent-swarm/) — 2026-03-11
- [OpenClaw × TikTok — AIエージェントでショート動画マーケティングを自動化する方法](/blogs/posts/2026/03/2026-03-10-openclaw-tiktok-marketing/) — 2026-03-10
- [OpenClaw × 小紅書 — AI エージェントが SNS アカウントを完全自動運営する時代](/blogs/posts/2026/03/2026-03-10-openclaw-xiaohongshu-agent/) — 2026-03-10
- [ByteDance DeerFlow — オープンソースの SuperAgent 基盤でAIエージェントを自律運用する](/blogs/posts/2026/03/2026-03-11-bytedance-deerflow/) — 2026-03-11
- [Claude Code vs Codex：AI コーディングエージェント徹底比較 2026](/blogs/posts/2026/03/2026-03-11-claude-code-vs-codex/) — 2026-03-11
- [OpenClaw のマークダウン駆動エージェント運用スタック：40日間の実践から学ぶ設計パターン](/blogs/posts/2026/03/2026-03-11-openclaw-markdown-agent-stack/) — 2026-03-11
- [OpenClaw エージェントでトレーディング戦略を自動バックテスト](/blogs/posts/2026/03/2026-03-11-openclaw-trading-backtest/) — 2026-03-11
- [Opik × OpenClaw — AI エージェントの動作を完全可視化するオブザーバビリティプラグイン](/blogs/posts/2026/03/2026-03-11-opik-openclaw-observability/) — 2026-03-11
- [opik-openclaw — OpenClaw の AIエージェント動作を可視化するオブザーバビリティツール](/blogs/posts/2026/03/2026-03-11-opik-openclaw/) — 2026-03-11
- [AIエージェント同士をつなぐRelay基盤 — 会話とtransportを分離するアーキテクチャ](/blogs/posts/2026/03/2026-03-12-agent-relay-transport/) — 2026-03-12
- [Perplexity Personal Computer — Mac mini を常時稼働AIエージェントに変える新サービス](/blogs/posts/2026/03/2026-03-12-perplexity-personal-computer/) — 2026-03-12
- [Microsoft Agent Governance Toolkit：AIエージェントのセキュリティを4つの柱で守るOSSツールキット](/blogs/posts/2026/03/2026-03-14-agent-governance-toolkit/) — 2026-03-14
- [OpenClawスキルの厳選コレクション — AIエージェントを即戦力にするスキル集](/blogs/posts/2026/03/2026-03-15-openclaw-skills-collection/) — 2026-03-15
- [AI時代の「ダラダラ働き」のすすめ — AIエージェント並列実行の落とし穴](/blogs/posts/2026/03/2026-03-17-ai-agent-parallel-execution-efficiency/) — 2026-03-17
- [Manus（マナス）の全29機能を完全解説——AIエージェントが「仕事を丸投げできる」時代へ](/blogs/posts/2026/03/2026-03-17-manus-ai-agent-29-features/) — 2026-03-17
- [OkaraのAI CMO——マーケティング業務を自律実行するAIエージェント](/blogs/posts/2026/03/2026-03-17-okara-ai-cmo/) — 2026-03-17
- [Paperclip オープンソース化：0人会社を動かすエージェントオーケストレーション層](/blogs/posts/2026/03/2026-03-17-paperclipai-zero-human-company/) — 2026-03-17
- [AIコーディングエージェント開発フレームワーク「superpowers」— 7段階ワークフローとTDDで精度を高める](/blogs/posts/2026/03/2026-03-17-superpowers-ai-coding-agent-framework/) — 2026-03-17
- [takt — AIコーディングエージェントのワークフローをYAMLで定義するCLIツール](/blogs/posts/2026/03/2026-03-17-takt-ai-agent-workflow/) — 2026-03-17
- [agent-skill-bus: AIエージェントのスキル劣化を自動検知・修復するOSSランタイム](/blogs/posts/2026/03/2026-03-18-agent-skill-bus/) — 2026-03-18
- [OpenClaw狂想曲：中国で巻き起こるAIエージェント・ゴールドラッシュと「ツルハシ売り」たち](/blogs/posts/2026/03/2026-03-20-openclaw-gold-rush/) — 2026-03-20
- [OpenClawで月売上1,200万円・従業員ゼロの会社を実現したAIエージェント「Felix」](/blogs/posts/2026/03/2026-03-21-openclaw-felix-ai-agent-company/) — 2026-03-21
- [Claude Code を「自分専用の開発チーム」に変える3つの機能 — フック・カスタムコマンド・サブエージェント](/blogs/posts/2026/03/2026-03-22-claude-code-hooks-commands-subagents/) — 2026-03-22
- [MCP のセキュリティが OAuth 2.1 で大幅進化：AI エージェントと社内データを安全に接続する仕組み](/blogs/posts/2026/03/2026-03-22-mcp-oauth21-security/) — 2026-03-22
- [Claude Codeで「専門家チーム」を構築する：カスタムエージェントとCoworkの活用法](/blogs/posts/2026/03/2026-03-25-claude-code-expert-agents/) — 2026-03-25
- [Dexter: 約200行で動く自律型金融リサーチエージェント](/blogs/posts/2026/03/2026-03-26-dexter-financial-agent/) — 2026-03-26
- [Anthropic の3エージェント・ハーネス設計: Claude が6時間でフルアプリを自律構築する仕組み](/blogs/posts/2026/03/2026-03-27-anthropic-harness-design-three-agents/) — 2026-03-27
- [「値は計算されていた。ただ届いていなかっただけ」— LLMエージェントプロンプトのハードコード問題](/blogs/posts/2026/03/2026-03-27-llm-prompt-hardcode-bug/) — 2026-03-27
- [AIエージェント記憶検索の限界とSuperLocalMemory V3が挑む3つの数学的解決策](/blogs/posts/2026/03/2026-03-27-superlocalmemory-v3-ai-agent-memory/) — 2026-03-27
- [「toA」時代の到来 — AIエージェント向けサービス200超が示す新市場の全体像](/blogs/posts/2026/03/2026-03-30-toa-services-for-ai-agents/) — 2026-03-30
- [OpenClaw + Ollama + Gemma4 でローカル無料AIエージェントを構築する](/blogs/posts/2026/04/2026-04-06-openclaw-gemma4-local-setup/) — 2026-04-06
- [Claude Code にカオスエンジニアリングエージェントを導入してリポジトリの弱点を発見する](/blogs/posts/2026/04/2026-04-07-claude-code-chaos-engineer-agent/) — 2026-04-07
- [OpenClaw に動画生成機能が正式搭載へ — AI エージェントが制作まで完結する時代](/blogs/posts/2026/04/2026-04-07-openclaw-video-generation/) — 2026-04-07
- [OpenClaw vs Hermes: AIエージェントプラットフォームの勢力図に変化](/blogs/posts/2026/04/2026-04-12-openclaw-vs-hermes/) — 2026-04-12
- [Claude Code で作る「世界AIシミュレーター」— 20カ国AIエージェントが自律外交・紛争するリアルタイム地政学ゲーム](/blogs/posts/2026/04/2026-04-14-claude-code-world-ai-simulator/) — 2026-04-14
- [AI Agent に品質を担保させる — QA 手法の実践ガイド](/blogs/posts/2026-03-09-ai-agent-qa/) — 2026-03-09
- [「研究コミュニティをまるごとエミュレートせよ」— Karpathy が示す AI エージェント協調の未来](/blogs/posts/2026-03-09-ai-research-community/) — 2026-03-09
- [Harness Engineering ベストプラクティス 2026 — AI コーディングエージェントを安定稼働させる設計術](/blogs/posts/2026-03-09-harness-engineering/) — 2026-03-09
- [Claude Code Review — エージェントチームが PR のバグを狩る新機能](/blogs/posts/2026-03-10-claude-code-review/) — 2026-03-10
- [OpenClaw × Claude Code セットアップガイド — AI エージェントチームを構築する2つのアプローチ](/blogs/posts/2026-03-10-openclaw-claude-code-setup/) — 2026-03-10
- [DESIGN.md という文化 — AI エージェントに「ブランドの見た目」を渡す共通フォーマット](/blogs/posts/2026/05/design-md-culture/) — 2026-05-11
- [dotenvx・lkr・aws-vault・1Password CLI — .env 代替ツール4種の選び方とベストプラクティス](/blogs/posts/2026/03/2026-03-03-fbc113dfc0629b475ce1ccf808e859a0/) — 2026-03-03
- [Felix AI CEO × 人間ゼロの会社が30日で売上1,200万円、VCを「金の使い道がない」と断った話](/blogs/posts/2026/03/2026-03-05-1128207db83f7ca1a2c940dba0fdc2c9/) — 2026-03-05
