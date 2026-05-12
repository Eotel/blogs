---
title: "OpenClaw"
description: "オープンソースの AI エージェント基盤フレームワーク。Claude、Grok、Ollama に対応。ローカル自律型エージェントとして Claude Managed Agents と対照的な設計思想を持つ"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["openclaw"]
related_posts:
  - "/posts/2026/03/openclaw-claude-code-setup/"
  - "/posts/2026/03/openclaw-overview/"
  - "/posts/2026/03/openclaw-agent-runtime/"
  - "/posts/2026/03/openclaw-china-security-warning/"
  - "/posts/2026/04/gemini-agent-mode/"
  - "/posts/2026/04/claude-managed-agents-architecture/"
  - "/posts/2026/04/claw-code-local/"
  - "/posts/2026/03/2026-03-02-7f8ba24f4d98fb8b93ec3d1a507cffec/"
  - "/posts/2026/03/2026-03-02-8f10c70d04ed25f68a744081c16baa76/"
  - "/posts/2026/03/2026-03-03-1ddcd07ed2cfe5a9510119208b4376e2/"
  - "/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/"
  - "/posts/2026/03/2026-03-05-6ab9658fb38eda6969e26ddc2a91217c/"
  - "/posts/2026/03/2026-03-05-7a124c55c1c58515e7f6370d59fd25ec/"
  - "/posts/2026/03/2026-03-05-7ed089c4237d5da02049b58d9678da5b/"
  - "/posts/2026/03/2026-03-05-9344deb1d9e60907c9fbc5db4fd0f226/"
  - "/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/"
  - "/posts/2026/03/2026-03-08-openclaw-telegram-forum-topics/"
  - "/posts/2026/03/2026-03-09-openclaw-ai-team/"
  - "/posts/2026/03/2026-03-09-shenzhen-openclaw-opc/"
  - "/posts/2026/03/2026-03-10-openclaw-tiktok-marketing/"
  - "/posts/2026/03/2026-03-10-openclaw-xiaohongshu-agent/"
  - "/posts/2026/03/2026-03-11-claude-code-vs-openclaw/"
  - "/posts/2026/03/2026-03-11-github-malware-openclaw-installer/"
  - "/posts/2026/03/2026-03-11-openclaw-markdown-agent-stack/"
  - "/posts/2026/03/2026-03-11-openclaw-trading-backtest/"
  - "/posts/2026/03/2026-03-11-openclaw-x-knowledge-management/"
  - "/posts/2026/03/2026-03-11-opik-openclaw-observability/"
  - "/posts/2026/03/2026-03-11-opik-openclaw/"
  - "/posts/2026/03/2026-03-12-openclaw-alex-finn/"
  - "/posts/2026/03/2026-03-12-openclaw-knowledge-management/"
  - "/posts/2026/03/2026-03-12-openclaw-stock-monitoring/"
  - "/posts/2026/03/2026-03-12-perplexity-personal-computer/"
  - "/posts/2026/03/2026-03-13-openclaw-nullclaw-small-board/"
  - "/posts/2026/03/2026-03-15-openclaw-skills-collection/"
  - "/posts/2026/03/2026-03-17-nemoclaw-openclaw-security/"
  - "/posts/2026/03/2026-03-17-nvidia-nemoclaw-openclaw/"
  - "/posts/2026/03/2026-03-17-openclaw-x-follower-growth/"
  - "/posts/2026/03/2026-03-18-claude-cowork-dispatch-mind-uploading/"
  - "/posts/2026/03/2026-03-18-openclaw-vibe-marketer/"
  - "/posts/2026/03/2026-03-20-openclaw-gold-rush/"
  - "/posts/2026/03/2026-03-21-claude-code-channels/"
  - "/posts/2026/03/2026-03-21-clawrouter-openclaw-cost/"
  - "/posts/2026/03/2026-03-21-openclaw-felix-ai-agent-company/"
  - "/posts/2026/03/2026-03-27-openclaw-youtube-automation/"
  - "/posts/2026/04/2026-04-06-openclaw-gemma4-local-setup/"
  - "/posts/2026/04/2026-04-07-openclaw-video-generation/"
  - "/posts/2026/04/2026-04-12-openclaw-vs-hermes/"
  - "/posts/2026-03-10-openclaw-claude-code-setup/"
  - "/posts/2026/03/2026-03-05-1128207db83f7ca1a2c940dba0fdc2c9/"
tags: ["agent", "オープンソース", "フレームワーク", "ローカルエージェント"]
---

## 概要

深圳で開発されたオープンソース AI エージェント基盤。2025年11月に「Clawdbot」として公開後、商標問題で改名。複数の LLM（Claude、Grok、Ollama）に対応し、MCP 統合により任意のツール連携が可能。GitHub スターは25万を超える。

## 設計思想：ローカル自律型

OpenClaw は Gateway デーモンがユーザーのデバイスに常駐し、自律的にタスクを処理する設計。Claude Managed Agents（クラウド管理型）とは対照的なアーキテクチャを持つ。

| 観点 | OpenClaw | Claude Managed Agents |
|------|----------|-----------------------|
| 実行場所 | ローカルデバイス | Anthropic クラウド |
| 常駐性 | Gateway デーモンが常駐 | セッション単位のオンデマンド |
| データ管理 | SOUL.md / MEMORY.md でローカル管理 | Anthropic サーバーに保存 |
| カスタマイズ | ClawHub の 13,000+ スキル | MCP サーバー + 組み込みツール |
| 障害分離 | 単一デーモン（Gateway + Runtime 結合） | Brain / Session / Hands が独立 |

## Gemini Agent との比較

Google Gemini Agent モード（クラウド型、Google Workspace 専用）との対比:

- **Gemini Agent**: クラウド管理、Google Workspace との統合が強み、スケジュール実行可能
- **OpenClaw**: セルフホスト、データがデバイスから出ない、100以上のビルトインスキル

## セキュリティ上の注意

中国 CNCERT が緊急セキュリティ警告を発出。デフォルト設定でローカルファイルシステム・環境変数・シェルへの広範なアクセスが有効になっている問題。コンテナ隔離、ネットワーク制限が必須。また、Cisco・Giskard の研究チームがサードパーティスキルにおけるデータ流出・プロンプトインジェクションリスクを指摘（CVE-2026-25253、CVSS 8.8）。

## 派生プロジェクト：claw-code-local

OpenClaw のアーキテクチャを参考に、Claude Code 風の AI コーディングエージェントをローカル LLM で動かす `claw-code-local`（Rust 製）が登場。Ollama・LM Studio など OpenAI 互換エンドポイントに接続でき、API 費用ゼロ・コードの外部送信なしでコーディング支援が可能。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — OpenClaw が実装するパターン
- [Claude Managed Agents](/blogs/wiki/tools/claude-managed-agents/) — クラウド型マネージドエージェントとの対比
- [Gemini Agent](/blogs/wiki/tools/gemini-agent/) — クラウド連携型エージェントとの対比
- [MCP](/blogs/wiki/concepts/mcp/) — OpenClaw が採用するプロトコル
- [ANOLISA](/blogs/wiki/tools/anolisa/) — Alibaba のエージェント OS

## ソース記事

- [OpenClaw セットアップ](/blogs/posts/2026/03/openclaw-claude-code-setup/) — 2026-03
- [OpenClaw 概要](/blogs/posts/2026/03/openclaw-overview/) — 2026-03
- [OpenClaw エージェントランタイム全体像](/blogs/posts/2026/03/openclaw-agent-runtime/) — 2026-03
- [OpenClaw セキュリティ警告](/blogs/posts/2026/03/openclaw-china-security-warning/) — 2026-03
- [Gemini Agentモード：Google Workspaceを自動化するAIエージェント](/blogs/posts/2026/04/gemini-agent-mode/) — 2026-04-07
- [Claude Managed Agents のアーキテクチャ：Brain / Session / Hands の分離設計](/blogs/posts/2026/04/claude-managed-agents-architecture/) — 2026-04-10
- [claw-code-local — Claude Code 風の AI コーディングエージェントをローカル LLM で動かす](/blogs/posts/2026/04/claw-code-local/) — 2026-04-05
- [Second Me — AI に「自分の分身」を持つ時代と OpenClaw との本質的な違い](/blogs/posts/2026/03/2026-03-02-7f8ba24f4d98fb8b93ec3d1a507cffec/) — 2026-03-02
- [OpenClaw で 13 体の AI チームを組織する — 低スペック PC で営業・SNS 運用を完全自動化](/blogs/posts/2026/03/2026-03-02-8f10c70d04ed25f68a744081c16baa76/) — 2026-03-02
- [「OpenClawで5人解雇」は本当か — AIエージェント煽りの構造とファクトチェック](/blogs/posts/2026/03/2026-03-03-1ddcd07ed2cfe5a9510119208b4376e2/) — 2026-03-03
- [OpenClaw 22,000字解説のファクトチェック --- AIエージェントの民主化煽りと技術的実態の分離](/blogs/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/) — 2026-03-05
- [AIVideo Agent — 「動画版 OpenClaw」が24時間コンテンツパイプラインを自律運用する仕組み](/blogs/posts/2026/03/2026-03-05-6ab9658fb38eda6969e26ddc2a91217c/) — 2026-03-05
- [ClawGTM — OpenClaw を自律型セールスエージェントに変えた「URL 1つで営業パイプライン構築」](/blogs/posts/2026/03/2026-03-05-7a124c55c1c58515e7f6370d59fd25ec/) — 2026-03-05
- [awesome-claws × OpenClawエコシステム28エージェント完全マップと設計思想5分類](/blogs/posts/2026/03/2026-03-05-7ed089c4237d5da02049b58d9678da5b/) — 2026-03-05
- [OpenClaw × Scrapling — AIエージェントが「検出不能なスクレイピング」を手にした日](/blogs/posts/2026/03/2026-03-05-9344deb1d9e60907c9fbc5db4fd0f226/) — 2026-03-05
- [Google Workspace CLI（gws）— Drive・Gmail・Calendarを1コマンドで操作するAIエージェント対応ツール](/blogs/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/) — 2026-03-05
- [OpenClaw × Telegram Forum Topics — AIとの対話を構造化して生産性を上げる方法](/blogs/posts/2026/03/2026-03-08-openclaw-telegram-forum-topics/) — 2026-03-08
- [OpenClaw で月400ドルの AI チームを構築 — 18歳がコーディング経験ゼロで実現した方法](/blogs/posts/2026/03/2026-03-09-openclaw-ai-team/) — 2026-03-09
- [深圳が世界初の OpenClaw・一人企業支援策を発表 — AI エージェント時代のソロ起業を後押し](/blogs/posts/2026/03/2026-03-09-shenzhen-openclaw-opc/) — 2026-03-09
- [OpenClaw × TikTok — AIエージェントでショート動画マーケティングを自動化する方法](/blogs/posts/2026/03/2026-03-10-openclaw-tiktok-marketing/) — 2026-03-10
- [OpenClaw × 小紅書 — AI エージェントが SNS アカウントを完全自動運営する時代](/blogs/posts/2026/03/2026-03-10-openclaw-xiaohongshu-agent/) — 2026-03-10
- [Claude Code vs OpenClaw — 「どっちを勉強すべき？」に対する責務ベースの選び方](/blogs/posts/2026/03/2026-03-11-claude-code-vs-openclaw/) — 2026-03-11
- [GitHub で見つけた「便利ツール」を解析したらマルウェアだった話：偽 OpenClaw インストーラーの実態](/blogs/posts/2026/03/2026-03-11-github-malware-openclaw-installer/) — 2026-03-11
- [OpenClaw のマークダウン駆動エージェント運用スタック：40日間の実践から学ぶ設計パターン](/blogs/posts/2026/03/2026-03-11-openclaw-markdown-agent-stack/) — 2026-03-11
- [OpenClaw エージェントでトレーディング戦略を自動バックテスト](/blogs/posts/2026/03/2026-03-11-openclaw-trading-backtest/) — 2026-03-11
- [OpenClawでX運用を自動化する鍵は「ナレッジ管理」にある](/blogs/posts/2026/03/2026-03-11-openclaw-x-knowledge-management/) — 2026-03-11
- [Opik × OpenClaw — AI エージェントの動作を完全可視化するオブザーバビリティプラグイン](/blogs/posts/2026/03/2026-03-11-opik-openclaw-observability/) — 2026-03-11
- [opik-openclaw — OpenClaw の AIエージェント動作を可視化するオブザーバビリティツール](/blogs/posts/2026/03/2026-03-11-opik-openclaw/) — 2026-03-11
- [OpenClaw界隈でまず追うべき発信者 Alex Finn とは](/blogs/posts/2026/03/2026-03-12-openclaw-alex-finn/) — 2026-03-12
- [OpenClawを使いこなす鍵は「情報の一元管理」にある](/blogs/posts/2026/03/2026-03-12-openclaw-knowledge-management/) — 2026-03-12
- [OpenClaw で保有銘柄の情報収集を完全自動化する — 決算通知・株価アラート・ニュース収集の実装例](/blogs/posts/2026/03/2026-03-12-openclaw-stock-monitoring/) — 2026-03-12
- [Perplexity Personal Computer — Mac mini を常時稼働AIエージェントに変える新サービス](/blogs/posts/2026/03/2026-03-12-perplexity-personal-computer/) — 2026-03-12
- [OpenClawをMac miniなしで1500円の小型基板に導入してAI組織を構築する方法](/blogs/posts/2026/03/2026-03-13-openclaw-nullclaw-small-board/) — 2026-03-13
- [OpenClawスキルの厳選コレクション — AIエージェントを即戦力にするスキル集](/blogs/posts/2026/03/2026-03-15-openclaw-skills-collection/) — 2026-03-15
- [NemoClaw触ってみた：OpenClawのセキュリティ問題を解消できるのか？](/blogs/posts/2026/03/2026-03-17-nemoclaw-openclaw-security/) — 2026-03-17
- [NVIDIA、OpenClaw向けオープンソーススタック「NemoClaw」を発表](/blogs/posts/2026/03/2026-03-17-nvidia-nemoclaw-openclaw/) — 2026-03-17
- [OpenClawでX運用したら10日でフォロワー1800人増えた話](/blogs/posts/2026/03/2026-03-17-openclaw-x-follower-growth/) — 2026-03-17
- [Claude Cowork DispatchとOpenClawで見えてきた「Mind Uploading」への道筋](/blogs/posts/2026/03/2026-03-18-claude-cowork-dispatch-mind-uploading/) — 2026-03-18
- [OpenClawを「バイブマーケター」に変えた方法 — AI広告自動化の実践ワークフロー](/blogs/posts/2026/03/2026-03-18-openclaw-vibe-marketer/) — 2026-03-18
- [OpenClaw狂想曲：中国で巻き起こるAIエージェント・ゴールドラッシュと「ツルハシ売り」たち](/blogs/posts/2026/03/2026-03-20-openclaw-gold-rush/) — 2026-03-20
- [Claude Code Channels で変わる AI 開発ワークフロー：OpenClaw との組み合わせが最適解か](/blogs/posts/2026/03/2026-03-21-claude-code-channels/) — 2026-03-21
- [ClawRouter — OpenClaw の API コストを最大92%削減するオープンソース LLM ルーター](/blogs/posts/2026/03/2026-03-21-clawrouter-openclaw-cost/) — 2026-03-21
- [OpenClawで月売上1,200万円・従業員ゼロの会社を実現したAIエージェント「Felix」](/blogs/posts/2026/03/2026-03-21-openclaw-felix-ai-agent-company/) — 2026-03-21
- [OpenClaw で YouTube 運用を全自動化? 「月1000万円」の主張を技術的に検証する](/blogs/posts/2026/03/2026-03-27-openclaw-youtube-automation/) — 2026-03-27
- [OpenClaw + Ollama + Gemma4 でローカル無料AIエージェントを構築する](/blogs/posts/2026/04/2026-04-06-openclaw-gemma4-local-setup/) — 2026-04-06
- [OpenClaw に動画生成機能が正式搭載へ — AI エージェントが制作まで完結する時代](/blogs/posts/2026/04/2026-04-07-openclaw-video-generation/) — 2026-04-07
- [OpenClaw vs Hermes: AIエージェントプラットフォームの勢力図に変化](/blogs/posts/2026/04/2026-04-12-openclaw-vs-hermes/) — 2026-04-12
- [OpenClaw × Claude Code セットアップガイド — AI エージェントチームを構築する2つのアプローチ](/blogs/posts/2026-03-10-openclaw-claude-code-setup/) — 2026-03-10
- [Felix AI CEO × 人間ゼロの会社が30日で売上1,200万円、VCを「金の使い道がない」と断った話](/blogs/posts/2026/03/2026-03-05-1128207db83f7ca1a2c940dba0fdc2c9/) — 2026-03-05
