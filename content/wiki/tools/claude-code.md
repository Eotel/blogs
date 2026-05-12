---
title: "Claude Code"
description: "Anthropic 公式の CLI ベース AI コーディングエージェント"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["claude-code"]
related_posts:
  - "/posts/2026/04/claude-code-context-compression/"
  - "/posts/2026/04/claude-code-silent-degradation/"
  - "/posts/2026/04/karpathy-llm-wiki/"
  - "/posts/2026/04/claude-thinking-nerfed/"
  - "/posts/2026/04/2026-04-15-claude-code-routines/"
  - "/posts/2026/04/2026-04-15-claude-code-routines-desktop-update/"
  - "/posts/2026/04/2026-04-16-claude-code-team-onboarding/"
  - "/posts/2026/04/2026-04-17-claude-caveman-token-reduction/"
  - "/posts/2026/04/2026-04-17-claude-code-context-rot-session-management/"
  - "/posts/2026/04/2026-04-17-video-use-claude-code-video-editing/"
  - "/posts/2026/04/2026-04-21-claude-code-level5/"
  - "/posts/2026/04/2026-04-21-claude-code-auto-memory-skills/"
  - "/posts/2026/04/2026-04-21-claude-code-zero-handwritten-code-49-features/"
  - "/posts/2026/04/2026-04-21-claude-code-45-tasks-automation-student/"
  - "/posts/2026/04/2026-04-23-claude-code-plan-mode-cost-reduction/"
  - "/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/"
  - "/posts/2026/04/2026-04-27-claude-code-creator-setup/"
  - "/posts/2026/04/2026-04-27-claude-code-kabukicho-ai-simulation/"
  - "/posts/2026/04/2026-04-27-claude-code-stock-trading-automation/"
  - "/posts/2026/04/2026-04-23-claude-code-sns-automation-affiliate/"
  - "/posts/2026/02/2026-02-04-540f79d12ee4c647af939ae154414543/"
  - "/posts/2026/02/2026-02-11-a8d22576ec3097e23c32dc62ae462283/"
  - "/posts/2026/02/2026-02-12-d2377c34eeb26795b9a84ea66a52085d/"
  - "/posts/2026/02/2026-02-16-379ef1d0f7e4f25c111d78ccd122bd28/"
  - "/posts/2026/02/2026-02-24-13fd92bc6f4e4dc0fd61c6dcbc4e1639/"
  - "/posts/2026/02/2026-02-26-5017f19e6544b679fb98156a068b72d5/"
  - "/posts/2026/02/2026-02-26-645cb8ae55f5ddde7d6aba4ec1c5a550/"
  - "/posts/2026/02/2026-02-26-7d1b02f7130f2fe523f3fee58d5b916f/"
  - "/posts/2026/02/2026-02-26-c1db35eaecd83c70628736440deba71a/"
  - "/posts/2026/02/2026-02-27-02719a7b094aeefede425b78ceff298e/"
  - "/posts/2026/02/2026-02-27-0f8bcfd264198a7d0296732af95aa99e/"
  - "/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/"
  - "/posts/2026/02/2026-02-27-5fcb10cb6bcc6b0c29f2b1e01d1c0855/"
  - "/posts/2026/02/2026-02-27-684a996d9a2c6387677a4d392faa8f89/"
  - "/posts/2026/02/2026-02-27-87849fbebf1c8203df69aec7619b12c0/"
  - "/posts/2026/02/2026-02-27-efad95152b5d282330300019d1d8572a/"
  - "/posts/2026/02/2026-02-27-fb664679cf44fad6134bf9ff360ec7c1/"
  - "/posts/2026/02/2026-02-28-5bb00c66d810da610c91ff83b0b8bed8/"
  - "/posts/2026/03/2026-03-01-0656510b5b52763f3cddcefd3edf0e1f/"
  - "/posts/2026/03/2026-03-01-0ee19b59603fd68d6a0295e4e94ac6f9/"
  - "/posts/2026/03/2026-03-01-0f8f4e791ffdc6f04b19e54918192cb3/"
  - "/posts/2026/03/2026-03-01-1a7265c8ba51f09a06687b88ffe260e9/"
  - "/posts/2026/03/2026-03-01-1bb26b9160fdf10ca297ad57b11b4530/"
  - "/posts/2026/03/2026-03-01-35c961de99305ae852fa808d6fd3680d/"
  - "/posts/2026/03/2026-03-01-4457cb14c47c0bd0ebff91f3a6a2d287/"
  - "/posts/2026/03/2026-03-02-0248d4f7dad745c12a44f107f17dee96/"
  - "/posts/2026/03/2026-03-02-12f83bb3b6d488806a8396e9b2c8305a/"
  - "/posts/2026/03/2026-03-02-1d6854d8bc646392d41a556f4d931021/"
  - "/posts/2026/03/2026-03-02-65552c1aa85911e32ab34518c0488130/"
  - "/posts/2026/03/2026-03-02-67f7657965c1f660dfbad9b0e88d0414/"
  - "/posts/2026/03/2026-03-02-6c41ec635f51d851c9fe02fd83a0d8d9/"
  - "/posts/2026/03/2026-03-02-7313515ac133e6a70b7f9f153ee8e2f5/"
  - "/posts/2026/03/2026-03-02-92b49bf68845650deef06cbe4f8913e7/"
  - "/posts/2026/03/2026-03-02-98030f822bb6964976415ace53716c0b/"
  - "/posts/2026/03/2026-03-02-98b91df087ccd64d04b0417b217f7cd0/"
  - "/posts/2026/03/2026-03-02-c249818561b78d80a9c2fc799d171a5e/"
  - "/posts/2026/03/2026-03-02-ee1116a854021058fe7293ef2ccb57bb/"
  - "/posts/2026/03/2026-03-02-f5f7afe224494ea830b0e01b607fbbc8/"
  - "/posts/2026/03/2026-03-03-3e4439ecefa6b85e164145183dead0da/"
  - "/posts/2026/03/2026-03-03-49217ac30b52677a7872c3008e38ed9a/"
  - "/posts/2026/03/2026-03-03-7276db2810dcd2906c299fa0a1874b44/"
  - "/posts/2026/03/2026-03-03-8feec16470c6e442ce0b999e472ec095/"
  - "/posts/2026/03/2026-03-03-91ce402f4341983abe89cff8bd4989fd/"
  - "/posts/2026/03/2026-03-03-c6757cc9fa558f456eb0920dea2f76e1/"
  - "/posts/2026/03/2026-03-03-db0f59b8d75be3b932868c101207fbc8/"
  - "/posts/2026/03/2026-03-03-eccd6b7eeb61d1f6278961cf6717e3ec/"
  - "/posts/2026/03/2026-03-03-ece550332a70ae51c56ab3e35bb1772c/"
  - "/posts/2026/03/2026-03-03-fd36299e0751373fd17f0ab90d49bf98/"
  - "/posts/2026/03/2026-03-04-14eeecd540a136f4a5f87371a03f8145/"
  - "/posts/2026/03/2026-03-04-2fb1416daa8c7baf370c69d0b1649625/"
  - "/posts/2026/03/2026-03-04-400b78c2f6a4ec11b0ec5ddc3ed2d938/"
  - "/posts/2026/03/2026-03-04-43baeed6a433f7f961aefedcf9bb4201/"
  - "/posts/2026/03/2026-03-04-4a6596b99ae8da9028f432e6c8d0b7f5/"
  - "/posts/2026/03/2026-03-04-5681ba524366e175aa03f28ba194d17c/"
  - "/posts/2026/03/2026-03-04-5f7b16f99352ba53b24d23586231ff59/"
  - "/posts/2026/03/2026-03-04-6648ce53fd0768e75cefc260e48fbbf6/"
  - "/posts/2026/03/2026-03-04-774a8959bf6ba55b4609f9658d3b8d9a/"
  - "/posts/2026/03/2026-03-04-797ce8bd21e6176bfd761e2f003dc580/"
  - "/posts/2026/03/2026-03-04-8df722451a54a64ee778169b6c2f6c07/"
  - "/posts/2026/03/2026-03-04-8f5e0a0647a6c9d12ab70b9f59856e71/"
  - "/posts/2026/03/2026-03-04-9c65e3a8bc648a1493bf0a8fe0fa3bb8/"
  - "/posts/2026/03/2026-03-04-a0e7a789ef7534c7cb6136d7fb00572e/"
  - "/posts/2026/03/2026-03-04-b22606904c5d5f513556e6a58c3b4657/"
  - "/posts/2026/03/2026-03-04-b87ea2c5a866e42db6678c582963a6c5/"
  - "/posts/2026/03/2026-03-04-bcecef951ac3e3bd81aafaa2c836b37a/"
  - "/posts/2026/03/2026-03-04-d84f897e8825bef6ac3f28ad5a982740/"
  - "/posts/2026/03/2026-03-04-db1fa7dce7e319be15057b655e03d099/"
  - "/posts/2026/03/2026-03-04-e5839407fe23c117b54ce5ed77dac5fa/"
  - "/posts/2026/03/2026-03-04-ee3017a7e8bcfbb995b93b8884cec258/"
  - "/posts/2026/03/2026-03-04-f7bad4476f8bec3e58bcf01848bfb807/"
  - "/posts/2026/03/2026-03-05-00a5a21b56da09807d7c114573cbcf14/"
  - "/posts/2026/03/2026-03-05-101618cbfc2f38b7321f85297a65da72/"
  - "/posts/2026/03/2026-03-05-1f81385148befa3ee0e980408c174676/"
  - "/posts/2026/03/2026-03-05-2b18749e88b9e71b16a4fe6f5947011b/"
  - "/posts/2026/03/2026-03-05-4716b0356dc37a6ecff5ffdc4cd9b5cd/"
  - "/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/"
  - "/posts/2026/03/2026-03-05-788d211750014f243a3b9f0c56e7192c/"
  - "/posts/2026/03/2026-03-05-79be6da14ac16c7e51167d5a9747228f/"
  - "/posts/2026/03/2026-03-05-946ec0898ef07511328522277fd9ecfa/"
  - "/posts/2026/03/2026-03-05-b03527dbe6ad00bfac9b4b431248b524/"
  - "/posts/2026/03/2026-03-05-b33112efb8463209afbeadaf568ec58d/"
  - "/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/"
  - "/posts/2026/03/2026-03-05-bf2e6519b561967327735da3f05142be/"
  - "/posts/2026/03/2026-03-05-c412a36c7b360f30945b91a52f510103/"
  - "/posts/2026/03/2026-03-06-9023009193920fd0ad17eda629351b18/"
  - "/posts/2026/03/2026-03-06-e053dfb0c2bee4f36f609060b3dfd487/"
  - "/posts/2026/03/2026-03-08-anti-hallucination-protocol/"
  - "/posts/2026/03/2026-03-09-claude-code-daily-business/"
  - "/posts/2026/03/2026-03-09-claude-code-security-risk-prompt/"
  - "/posts/2026/03/2026-03-09-claude-code-security/"
  - "/posts/2026/03/2026-03-09-claude-frontend-design-skill/"
  - "/posts/2026/03/2026-03-09-impeccable-ai-design-skills/"
  - "/posts/2026/03/2026-03-10-claude-code-spec-driven-dev/"
  - "/posts/2026/03/2026-03-10-freee-mcp-claude-code/"
  - "/posts/2026/03/2026-03-11-ai-coding-assistant-vscode-installs/"
  - "/posts/2026/03/2026-03-11-claude-code-skill-creator/"
  - "/posts/2026/03/2026-03-11-claude-code-vs-codex/"
  - "/posts/2026/03/2026-03-11-claude-code-vs-openclaw/"
  - "/posts/2026/03/2026-03-12-claude-code-auto-mode/"
  - "/posts/2026/03/2026-03-12-claude-code-non-engineer-adhd-singularity/"
  - "/posts/2026/03/2026-03-12-claude-code-skills-training/"
  - "/posts/2026/03/2026-03-12-claude-code-sqlite-duckdb/"
  - "/posts/2026/03/2026-03-12-claude-md-improver/"
  - "/posts/2026/03/2026-03-12-codified-context/"
  - "/posts/2026/03/2026-03-12-geo-seo-claude/"
  - "/posts/2026/03/2026-03-13-claude-code-chief-of-staff/"
  - "/posts/2026/03/2026-03-13-claude-code-local-llm-kv-cache/"
  - "/posts/2026/03/2026-03-13-claude-code-sales-mtg-prep/"
  - "/posts/2026/03/2026-03-14-anthropic-ai-academy/"
  - "/posts/2026/03/2026-03-14-solo-tax-accountant-claude-code/"
  - "/posts/2026/03/2026-03-15-ai-driven-dev-domain-knowledge/"
  - "/posts/2026/03/2026-03-16-claude-code-overnight-tasks/"
  - "/posts/2026/03/2026-03-17-anthropic-claude-certification-exam/"
  - "/posts/2026/03/2026-03-17-claude-code-auto-mode/"
  - "/posts/2026/03/2026-03-17-claude-code-commands/"
  - "/posts/2026/03/2026-03-17-claude-code-setup-for-non-engineers/"
  - "/posts/2026/03/2026-03-17-claude-code-skills-lessons/"
  - "/posts/2026/03/2026-03-21-claude-code-channels/"
  - "/posts/2026/03/2026-03-22-claude-code-hooks-commands-subagents/"
  - "/posts/2026/03/2026-03-23-claude-code-7-security-settings/"
  - "/posts/2026/03/2026-03-23-claude-code-design-tool-steve-schoger/"
  - "/posts/2026/03/2026-03-23-claude-code-stock-trading-paper-trade/"
  - "/posts/2026/03/2026-03-23-claude-desktop-preview-dom-select/"
  - "/posts/2026/03/2026-03-24-renoise-claude-code-seedance/"
  - "/posts/2026/03/2026-03-25-aws-agent-plugins-claude-code/"
  - "/posts/2026/03/2026-03-25-claude-code-expert-agents/"
  - "/posts/2026/03/2026-03-25-claude-code-skip-permissions-to-auto/"
  - "/posts/2026/03/2026-03-25-claude-subconscious/"
  - "/posts/2026/03/2026-03-26-ai-fatigue-claude-code-simplicity/"
  - "/posts/2026/03/2026-03-26-claude-code-auto-mode-agi/"
  - "/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-automation/"
  - "/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-lessons/"
  - "/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-plan/"
  - "/posts/2026/03/2026-03-30-ai-agents-40-failure/"
  - "/posts/2026/03/2026-03-30-claude-code-best-practice-repo/"
  - "/posts/2026/03/2026-03-31-claude-code-self-hosted-runner-auto-mode/"
  - "/posts/2026/03/2026-03-31-claude-code-source-map-leak/"
  - "/posts/2026/03/2026-03-31-claude-code-worktree-permission/"
  - "/posts/2026/04/2026-04-06-claude-code-token-optimization/"
  - "/posts/2026/04/2026-04-07-claude-code-chaos-engineer-agent/"
  - "/posts/2026/04/2026-04-07-rtk-rust-token-killer-claude-code/"
  - "/posts/2026/04/2026-04-09-exbrain-claude-code-obsidian-ai-brain/"
  - "/posts/2026/04/2026-04-11-mercari-claude-code-org-security/"
  - "/posts/2026/04/2026-04-12-claude-code-shopify-ai-toolkit/"
  - "/posts/2026/04/2026-04-14-claude-code-world-ai-simulator/"
  - "/posts/2026-03-09-ai-agent-qa/"
  - "/posts/2026-03-09-harness-engineering/"
  - "/posts/2026-03-10-claude-code-review/"
  - "/posts/2026-03-10-openclaw-claude-code-setup/"
  - "/posts/2026/03/2026-03-01-7b83b0c9049f181c85636073365e406a/"
  - "/posts/2026/03/2026-03-02-9cef5b3013c2cdaa3ec1d190b4d5f90f/"
  - "/posts/2026/03/2026-03-03-95278de03de967bcc74ff8b320222044/"
  - "/posts/2026/03/2026-03-04-b8b0f06e9ac13cce154f50e510c2fdc7/"
  - "/posts/2026/03/2026-03-17-claude-cowork-initial-setup/"
  - "/posts/2026/03/2026-03-18-ai-design-workflow/"
  - "/posts/2026/02/2026-02-27-61e0abd5ba76e70dabc257c5f0e6560b/"
  - "/posts/2026/04/2026-04-14-2026-ai-engineer-roadmap/"
tags: ["claude-code", "claude", "anthropic", "AIエージェント"]
---

## 概要

Anthropic が開発する CLI ベースの AI コーディングエージェント。ターミナル上で対話しながらコードの読み書き、ファイル操作、git 操作、テスト実行などを行える。

## 主な特徴

- **CLI ネイティブ**: ターミナルで直接対話（IDE 拡張版も提供）
- **ツール統合**: ファイル読み書き、Bash 実行、Grep/Glob 検索、Web 検索等
- **CLAUDE.md**: プロジェクトごとのルール・設定ファイル（圧縮後も再読み込みされる）
- **サブエージェント**: 複雑なタスクを並列エージェントに委任可能
- **スキル/フック**: カスタムワークフローの定義と自動化

## コンテキスト管理

5段階の圧縮カスケードでコンテキストウィンドウを管理する:
Microcompact → Context Collapse → Session Memory → Full Compact → PTL Truncation

詳細: [コンテキスト圧縮](/blogs/wiki/concepts/context-compression/)

## LLM Wiki との関連

Karpathy は Claude Code を LLM Wiki の実行環境として使用。「左画面に Claude Code、右画面に Obsidian」というワークフローを実践。

## 思考深度のサイレント・ダウングレード問題

2026年4月、AMD のシニア AI ディレクターが約 6,852 セッション分のログ分析で発見した問題。2026年3月8日以降、Claude Code の思考の中央値が約 2,200 文字から約 600 文字（**67%減**）に低下していた。Anthropic は「アダプティブ・シンキング」による変更を認め、`/effort max` コマンドで高い思考深度を維持できると説明した。

## Routines — クラウド上での自動実行

2026年4月14日リリースの **Claude Code Routines** により、PC をオフラインにしたままでもクラウド上でエージェントをスケジュール実行できるようになった。トリガー: cron / API コール / GitHub イベント。

## 新 Desktop — 複数セッション並列管理

同日リリースの新 Desktop では複数セッションの同時管理が可能になった。リポジトリ・Issue を並列で扱い、コンテキストを保持したまま別タスクに移行できる。

## /team-onboarding コマンド

過去 30 日のセッション履歴を分析してチーム向けオンボーディング資料を自動生成するコマンド。作業タイプの割合・よく使うスキル・MCP 接続使用回数を Markdown 形式で出力し、Notion や GitHub Wiki にコピペできる。

## トークン削減: 原始人プロンプト

システムプロンプトに `原始人みたいに喋れ。中身は全部残せ。無駄だけ消せ。` を追加するだけで日本語応答のトークンを最大 80% 削減できる（英語版 Caveman テクニックの日本語版）。CLAUDE.md に追記するだけで適用できる。

## Context Rot 管理

Claude Code のコンテキストウィンドウは 100 万トークン。長いセッションでは Context Rot（コンテキスト劣化）が発生する。5 つのセッション管理選択肢（Continue / Rewind / /clear / /compact / Subagent）を使い分けることで性能を維持できる。

詳細: [Context Rot](/blogs/wiki/concepts/context-rot/)

## Level 5 カスタマイズフレームワーク

Claude Code のカスタマイズは 5 段階の階層で理解できる:

| Level | 機能 | 内容 |
|-------|------|------|
| 1 | デフォルト | 設定なし、素の Claude Code |
| 2 | **CLAUDE.md** | プロジェクトルール・禁止事項・コンテキスト定義 |
| 3 | **Skills**（スラッシュコマンド） | `/blog`・`/wiki-ingest` など再利用可能なワークフロー |
| 4 | **Hooks** | PreToolUse/PostToolUse による自動検証・変換 |
| 5 | **Agents**（サブエージェント） | 専門化した AI の並列実行・委譲 |

Level が上がるほど設定コストは増えるが、出力の一貫性と品質が向上する。

## Plan Mode（計画モード）によるコスト削減

`/plan` コマンドで実装前に設計だけを行う「計画モード」に入り、確認後に `Shift+Tab` で実行モードに切り替える。事前設計を挟むことで:

- トークン消費: 約 **64% 削減**
- コスト: 約 **69% 削減**

計画モードでタスク全体像と制約を洗い出してから実行することで、手戻りを減らし一発完了率が上がる。

## autoMemoryEnabled を無効化してSkillsの挙動を固定する

`~/.claude/settings.json` に以下を追加することで、Claude のオートメモリ（自動記憶）によって Skills の動作が意図せず変化する問題を防げる:

```json
{
  "autoMemoryEnabled": false
}
```

Claude は会話の中で学習した内容を自動的に記憶し、次のセッションの挙動に反映させることがある。Skills を定義した場合に「なぜかスキルが期待通りに動かなくなる」という問題の原因になりやすい。

## Boris Cherny の実績（Claude Code 作者）

Claude Code の作者 Boris Cherny は Claude Code 自体を使って Claude Code を開発しており、「手書きコードゼロで 49 本の PR をマージした」と公表している（2026年4月）。作者自身のワークフロー:

1. **Plan Mode で設計** → 実装方針を固める
2. **CLAUDE.md にフィードバック** → ミスをルール化して同じ失敗を防ぐ
3. **検証ループ** → 実装後に必ず動作確認してから次に進む

品質の差は「プロンプトの巧さ」ではなく「計画→実行→検証の設計」で決まる、というのが作者の主張。

## 活用事例

- **Claude Code × vLLM**: `ANTHROPIC_BASE_URL` を vLLM エンドポイントに向け、MiniMax-M2.7 等のローカル LLM で動作させることで API コストをゼロにする
- **大規模マルチエージェントシミュレーション**: 1,255 体の AI ペルソナを並列実行し、歌舞伎町の夜 4 時間をシミュレーション（ぼったくり被害率 11.5%・予算超過 53.7% が創発）
- **株式自動売買**: Alpaca API と組み合わせた期待値ベースの米国株自動売買（3 週間で月次リターン 4.19% の事例）
- **学生による自動化**: GitHub Actions の cron ジョブ 45 本を Claude Code で構築
- **SNS/アフィリエイト自動化**: 投稿生成、スケジューリング、ASP 案件管理、成果分析を組み合わせた収益化パイプラインの構築

## 関連ページ

- [コンテキスト圧縮](/blogs/wiki/concepts/context-compression/) — Claude Code のコンテキスト管理戦略
- [Context Rot](/blogs/wiki/concepts/context-rot/) — コンテキスト劣化現象と 5 つの対処法
- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/) — Claude Code を活用した知識管理パターン
- [AutoAgent](/blogs/wiki/tools/autoagent/) — Claude Code をメタエージェントとして活用可能
- [dmux](/blogs/wiki/tools/dmux/) — Claude Code の並列実行環境を安全に管理するツール
- [Claude Managed Agents](/blogs/wiki/tools/claude-managed-agents/) — Anthropic のマネージドエージェント基盤
- [Video Use](/blogs/wiki/tools/video-use/) — Claude Code スキルとして動作する動画編集自動化ツール
- [Claude Harness](/blogs/wiki/tools/claude-harness/) — Claude Code の拡張機構をワンパッケージで提供する外装プラグイン
- [APM（Agent Package Manager）](/blogs/wiki/tools/apm/) — Claude Code 向けエージェントパッケージマネージャ
- [AI エージェント時代のシークレット管理](/blogs/wiki/guides/ai-agent-secret-management/) — Claude Code が .env にアクセスする問題への対策
- [pytest でカオスエンジニアリング](/blogs/wiki/guides/pytest-chaos-engineering/) — Claude Code 主導でテスト基盤を堅牢化するガイド
- [Claude Code コスト最適化ガイド](/blogs/wiki/guides/claude-code-cost-optimization/) — Plan Mode・原始人プロンプト・vLLM でトークン消費を削減
- [AIアフィリエイト自動化](/blogs/wiki/concepts/ai-affiliate-automation/) — SNS 投稿とアフィリエイト導線を AI エージェントで運用するパターン

## ソース記事

- [Claude Code のコンテキスト圧縮戦略](/blogs/posts/2026/04/claude-code-context-compression/) — 2026-04-02
- [Claude Code のサイレントな性能劣化を見逃すな](/blogs/posts/2026/04/claude-code-silent-degradation/) — 2026-04-03
- [Karpathy の LLM Wiki](/blogs/posts/2026/04/karpathy-llm-wiki/) — 2026-04-05
- [Claude の思考深度が 67% 低下？サイレント・ダウングレード問題](/blogs/posts/2026/04/claude-thinking-nerfed/) — 2026-04-13
- [Claude Code Routines リリース — 常駐しないエージェントという新しい設計思想](/blogs/posts/2026/04/2026-04-15-claude-code-routines/) — 2026-04-15
- [Claude Code、1日でアプデ3連発 — Routines・新 Desktop・ストリーム安定性](/blogs/posts/2026/04/2026-04-15-claude-code-routines-desktop-update/) — 2026-04-15
- [Claude Code の /team-onboarding コマンド](/blogs/posts/2026/04/2026-04-16-claude-code-team-onboarding/) — 2026-04-16
- [Claude を「原始人」口調にするとトークンが 80% 減る話](/blogs/posts/2026/04/2026-04-17-claude-caveman-token-reduction/) — 2026-04-17
- [Claude Code のコンテキスト管理術 — Context Rot を防ぐ 5 つの選択肢](/blogs/posts/2026/04/2026-04-17-claude-code-context-rot-session-management/) — 2026-04-17
- [Video Use — Claude Code で動画編集を完全自動化するオープンソーススキル](/blogs/posts/2026/04/2026-04-17-video-use-claude-code-video-editing/) — 2026-04-17
- [Claude Code の Level 5 カスタマイズフレームワーク](/blogs/posts/2026/04/2026-04-21-claude-code-level5/) — 2026-04-21
- [Claude Code の自動メモリ機能を無効化して Skills を安定させる](/blogs/posts/2026/04/2026-04-21-claude-code-auto-memory-skills/) — 2026-04-21
- [手書きコードゼロで 49 本の PR — Claude Code 作者 Boris Cherny の実績](/blogs/posts/2026/04/2026-04-21-claude-code-zero-handwritten-code-49-features/) — 2026-04-21
- [Claude Code で 45 本の GitHub Actions cron ジョブを自動構築した学生の話](/blogs/posts/2026/04/2026-04-21-claude-code-45-tasks-automation-student/) — 2026-04-21
- [Plan Mode でトークン 64%・コスト 69% 削減](/blogs/posts/2026/04/2026-04-23-claude-code-plan-mode-cost-reduction/) — 2026-04-23
- [Claude Code をローカル LLM（vLLM）で動かす](/blogs/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/) — 2026-04-23
- [Claude Code 作者直伝のワークフロー設計術](/blogs/posts/2026/04/2026-04-27-claude-code-creator-setup/) — 2026-04-27
- [Claude Code × 1,255 体の AI で歌舞伎町をシミュレーション](/blogs/posts/2026/04/2026-04-27-claude-code-kabukicho-ai-simulation/) — 2026-04-27
- [Claude Code で株式投資を自動化する — Alpaca API + 期待値計算](/blogs/posts/2026/04/2026-04-27-claude-code-stock-trading-automation/) — 2026-04-27
- [Claude Code で SNS 自動化×AI アフィリエイト](/blogs/posts/2026/04/2026-04-23-claude-code-sns-automation-affiliate/) — 2026-04-23
- [Ghostty + Claude Code 連携ガイド](/blogs/posts/2026/02/2026-02-04-540f79d12ee4c647af939ae154414543/) — 2026-02-04
- [iPhone から GitHub Issue を書くだけで Mac の Claude Code が自動実行される仕組みを作った — Self-hosted Runner + Claude Code CLI セットアップガイド](/blogs/posts/2026/02/2026-02-11-a8d22576ec3097e23c32dc62ae462283/) — 2026-02-11
- [Claude Code スキルで CloudWatch エラーレポートの Issue トリアージを自動化する](/blogs/posts/2026/02/2026-02-12-d2377c34eeb26795b9a84ea66a52085d/) — 2026-02-12
- [業務フローの設計にPowerPointではなくBPMNを使うべき理由 — Claude Code時代の詳細設計](/blogs/posts/2026/02/2026-02-16-379ef1d0f7e4f25c111d78ccd122bd28/) — 2026-02-16
- [Claude Code + tmux で GitHub Issue/PR をウィンドウ単位で管理する tmux-focus スキル](/blogs/posts/2026/02/2026-02-24-13fd92bc6f4e4dc0fd61c6dcbc4e1639/) — 2026-02-24
- [cmux — AIコーディングエージェント時代のターミナル紹介](/blogs/posts/2026/02/2026-02-26-5017f19e6544b679fb98156a068b72d5/) — 2026-02-26
- [コードレビューは CLAUDE.md / skills に書け — 同じ指摘を繰り返すな](/blogs/posts/2026/02/2026-02-26-645cb8ae55f5ddde7d6aba4ec1c5a550/) — 2026-02-26
- [Vibe Coding 2.0 — 「何を作らないか」を知る 18 のルール](/blogs/posts/2026/02/2026-02-26-7d1b02f7130f2fe523f3fee58d5b916f/) — 2026-02-26
- [Claude Code に重大な脆弱性 — リポジトリを開くだけで任意コード実行の恐れ](/blogs/posts/2026/02/2026-02-26-c1db35eaecd83c70628736440deba71a/) — 2026-02-26
- [# Claude Code 開発者が教える CLAUDE.md と実践 Tips](/blogs/posts/2026/02/2026-02-27-02719a7b094aeefede425b78ceff298e/) — 2026-02-27
- [# 三菱UFJ銀行におけるエンタープライズAI駆動開発のリアル](/blogs/posts/2026/02/2026-02-27-0f8bcfd264198a7d0296732af95aa99e/) — 2026-02-27
- [Agent Plugins for AWS — AI コーディングエージェントに AWS の専門知識を装着する](/blogs/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/) — 2026-02-27
- [# Claude Code の能力を10倍にする CLAUDE.md — AI エージェントのマネジメント哲学](/blogs/posts/2026/02/2026-02-27-5fcb10cb6bcc6b0c29f2b1e01d1c0855/) — 2026-02-27
- [# git-lrc — コミット時に AI が無料でコードレビューしてくれるツール](/blogs/posts/2026/02/2026-02-27-684a996d9a2c6387677a4d392faa8f89/) — 2026-02-27
- [# Anthropic 社内チームの Claude Code 活用 — マーケから法務まで、全部門が「自分で自動化」する時代](/blogs/posts/2026/02/2026-02-27-87849fbebf1c8203df69aec7619b12c0/) — 2026-02-27
- [# Claude Code の「YOLO モード」を安全に使う — dangerously-skip-permissions と Docker 活用](/blogs/posts/2026/02/2026-02-27-efad95152b5d282330300019d1d8572a/) — 2026-02-27
- [# 【2026年最新】世界一わかりやすい Agent Skills 完全ガイド — まとめ](/blogs/posts/2026/02/2026-02-27-fb664679cf44fad6134bf9ff360ec7c1/) — 2026-02-27
- [Claude Code の Auto Memory（MEMORY.md）を理解する — CLAUDE.md との使い分け](/blogs/posts/2026/02/2026-02-28-5bb00c66d810da610c91ff83b0b8bed8/) — 2026-02-28
- [Sentry を Claude Code で置き換えられるか — ランタイム計装と AI 分析の境界線](/blogs/posts/2026/03/2026-03-01-0656510b5b52763f3cddcefd3edf0e1f/) — 2026-03-01
- [MCP のトークン消費問題 — スキーマ注入で 55,000 トークン、CLI は 35 倍効率的](/blogs/posts/2026/03/2026-03-01-0ee19b59603fd68d6a0295e4e94ac6f9/) — 2026-03-01
- [AI エージェント入門 — 元 Meta エンジニアが説く「オートメーションとエージェントの決定的な違い」](/blogs/posts/2026/03/2026-03-01-0f8f4e791ffdc6f04b19e54918192cb3/) — 2026-03-01
- [Claude Code が汎用AIエージェント基盤へ進化 — Auto Memory・Remote Control・Scheduled Tasks の全貌](/blogs/posts/2026/03/2026-03-01-1a7265c8ba51f09a06687b88ffe260e9/) — 2026-03-01
- [非エンジニアでも安心！Claude Code を安全に使うための 2 つの設定ファイル（settings.local.json と CLAUDE.md）](/blogs/posts/2026/03/2026-03-01-1bb26b9160fdf10ca297ad57b11b4530/) — 2026-03-01
- [# 組織の課題管理から個人のタスク整理と優先度づけへ — Claude Code によるタスクトリアージ](/blogs/posts/2026/03/2026-03-01-35c961de99305ae852fa808d6fd3680d/) — 2026-03-01
- [Sentry × Claude Code で実現する AI デバッグワークフロー — エラー監視から自動修正まで](/blogs/posts/2026/03/2026-03-01-4457cb14c47c0bd0ebff91f3a6a2d287/) — 2026-03-01
- [Claude Code スキルで「穴場市場」を自動発掘 — コードを書かない AI エージェント活用術](/blogs/posts/2026/03/2026-03-02-0248d4f7dad745c12a44f107f17dee96/) — 2026-03-02
- [Claude Code 時代の .env 管理 — 「平文で置かない」秘密情報の新しい守り方](/blogs/posts/2026/03/2026-03-02-12f83bb3b6d488806a8396e9b2c8305a/) — 2026-03-02
- [Claude Code スキルの自動最適化 — テキスト勾配で「職人芸プロンプト」を工学に変える](/blogs/posts/2026/03/2026-03-02-1d6854d8bc646392d41a556f4d931021/) — 2026-03-02
- [Claude Ads で広告運用を186項目自動監査 --- Claude Code スキルが広告代理店の仕事を奪い始めた](/blogs/posts/2026/03/2026-03-02-65552c1aa85911e32ab34518c0488130/) — 2026-03-02
- [AIコーディングツール導入でMCC乗っ取り被害 — Antigravity・Claude Codeの脆弱性とシャドーAI対策](/blogs/posts/2026/03/2026-03-02-67f7657965c1f660dfbad9b0e88d0414/) — 2026-03-02
- [Claude Code ベストプラクティス — 成果を安定させる 7 つの鉄則と公式ガイドの設計思想](/blogs/posts/2026/03/2026-03-02-6c41ec635f51d851c9fe02fd83a0d8d9/) — 2026-03-02
- [Claude Code スキルで AI ワークフローを自動化する — Ralph Loop + YAML 宣言的定義の実践](/blogs/posts/2026/03/2026-03-02-7313515ac133e6a70b7f9f153ee8e2f5/) — 2026-03-02
- [生成AIで情報漏えいが増える本当の理由 — 「検索者がAIになった」時代の脅威モデルと3層防御](/blogs/posts/2026/03/2026-03-02-92b49bf68845650deef06cbe4f8913e7/) — 2026-03-02
- [Claude Code の「処理」と「ドメイン知識」をレイヤー分離する設計術](/blogs/posts/2026/03/2026-03-02-98030f822bb6964976415ace53716c0b/) — 2026-03-02
- [Claude Cowork 入門ガイド — プロンプトを頑張る時代の終わり、「仕組み化」で AI と働く新しいスタイル](/blogs/posts/2026/03/2026-03-02-98b91df087ccd64d04b0417b217f7cd0/) — 2026-03-02
- [Claude Code から Nano Banana 2 を呼ぶ — クロスモデル Skills 活用術](/blogs/posts/2026/03/2026-03-02-c249818561b78d80a9c2fc799d171a5e/) — 2026-03-02
- [Claude Code の /simplify と /batch — AIコーディングは「書く」から「整える・並列で移す」へ](/blogs/posts/2026/03/2026-03-02-ee1116a854021058fe7293ef2ccb57bb/) — 2026-03-02
- [ハーネスエンジニアリング入門 — AIエージェントの性能はモデルではなく周辺設計で決まる](/blogs/posts/2026/03/2026-03-02-f5f7afe224494ea830b0e01b607fbbc8/) — 2026-03-02
- [「上位 1% の Claude Skills 構築方法」を技術的に読み解く --- スキルの構造・設計パターン・組織展開](/blogs/posts/2026/03/2026-03-03-3e4439ecefa6b85e164145183dead0da/) — 2026-03-03
- [Claude Code に「目」を与える --- ローカル VLM で画像・動画をコンテキスト消費ゼロで理解させる](/blogs/posts/2026/03/2026-03-03-49217ac30b52677a7872c3008e38ed9a/) — 2026-03-03
- [.envの代わりにlkrでLLM APIキーを安全に管理する — セットアップからClaude Code連携まで](/blogs/posts/2026/03/2026-03-03-7276db2810dcd2906c299fa0a1874b44/) — 2026-03-03
- [MCP サーバーを増やしてもコンテキストを食わせない — Claude Code の Tool Search でトークン消費を95%削減](/blogs/posts/2026/03/2026-03-03-8feec16470c6e442ce0b999e472ec095/) — 2026-03-03
- [Readout — Claude Code の開発環境をリアルタイム監視する macOS ネイティブアプリと「エージェント監視」カテゴリの台頭](/blogs/posts/2026/03/2026-03-03-91ce402f4341983abe89cff8bd4989fd/) — 2026-03-03
- [.envの代わりにaws-vaultで安全に環境変数を与える — Claude Code時代のAWS認証情報管理](/blogs/posts/2026/03/2026-03-03-c6757cc9fa558f456eb0920dea2f76e1/) — 2026-03-03
- [dotenvx で暗号化、1Password CLI で注入 — .env 平文ゼロのローカル開発環境を構築する](/blogs/posts/2026/03/2026-03-03-db0f59b8d75be3b932868c101207fbc8/) — 2026-03-03
- [Claude Code / MCP を安全に使うための実践ガイド — settings.json の多層防御と deny の落とし穴](/blogs/posts/2026/03/2026-03-03-eccd6b7eeb61d1f6278961cf6717e3ec/) — 2026-03-03
- [AI が書いたコードに「なぜそうなったか」の記録はあるか --- git-memento と AI コード追跡の新標準](/blogs/posts/2026/03/2026-03-03-ece550332a70ae51c56ab3e35bb1772c/) — 2026-03-03
- [Claude Code サンドボックス完全解説 — chroot ではない、カーネルレベル隔離の仕組みと実践設定](/blogs/posts/2026/03/2026-03-03-fd36299e0751373fd17f0ab90d49bf98/) — 2026-03-03
- [ハーネスエンジニアリング実践知 — 「AIを使う人」と「AIを設計する人」の決定的な差](/blogs/posts/2026/03/2026-03-04-14eeecd540a136f4a5f87371a03f8145/) — 2026-03-04
- [Trivy VS Code 拡張が改ざんされ、ローカル AI エージェントが認証情報を窃取 — hackerbot-claw の全貌](/blogs/posts/2026/03/2026-03-04-2fb1416daa8c7baf370c69d0b1649625/) — 2026-03-04
- [Subagent と Agent Teams の違い — 「働くエージェント」と「議論するエージェント」を設計レイヤで理解する](/blogs/posts/2026/03/2026-03-04-400b78c2f6a4ec11b0ec5ddc3ed2d938/) — 2026-03-04
- [Claude Code の生成コードをローカル LLM でレビューする 3 つの構成パターン](/blogs/posts/2026/03/2026-03-04-43baeed6a433f7f961aefedcf9bb4201/) — 2026-03-04
- [「Figmaは100%不要」宣言の真意 --- Claude Codeが溶かすデザインとコードの境界](/blogs/posts/2026/03/2026-03-04-4a6596b99ae8da9028f432e6c8d0b7f5/) — 2026-03-04
- [Claude Code Agent Skills を強化する三銃士 --- scripts / references / assets の使い分け](/blogs/posts/2026/03/2026-03-04-5681ba524366e175aa03f28ba194d17c/) — 2026-03-04
- [「Claude Codeが無料で使える最強AIエージェント」は本当か — Accomplish の実態とAI煽りの再来](/blogs/posts/2026/03/2026-03-04-5f7b16f99352ba53b24d23586231ff59/) — 2026-03-04
- [「Claude Ads」の正体 — Anthropic 公式ではない個人開発スキルが日本でバズった構造を解剖する](/blogs/posts/2026/03/2026-03-04-6648ce53fd0768e75cefc260e48fbbf6/) — 2026-03-04
- [Claude Code で日常業務を「半自動化」する設計思想 — 経費精算から月末定常業務まで](/blogs/posts/2026/03/2026-03-04-774a8959bf6ba55b4609f9658d3b8d9a/) — 2026-03-04
- [「作れること」の価値が消えるAI時代に、SRE/プロダクション・エンジニアリングの重要性が上がる理由](/blogs/posts/2026/03/2026-03-04-797ce8bd21e6176bfd761e2f003dc580/) — 2026-03-04
- [Skills の自動最適化 — TextGrad を応用して提案書生成スキルを「学習」させる実験と過学習の発見](/blogs/posts/2026/03/2026-03-04-8df722451a54a64ee778169b6c2f6c07/) — 2026-03-04
- [Anthropic 公式「プロンプトのベストプラクティス」完全ガイド — Claude 4.6 時代の「宝の山」を読み解く](/blogs/posts/2026/03/2026-03-04-8f5e0a0647a6c9d12ab70b9f59856e71/) — 2026-03-04
- [Ollama で Qwen3 を動かす初心者ガイド — 日本語最強ローカルLLMを自分のPCで使う方法](/blogs/posts/2026/03/2026-03-04-9c65e3a8bc648a1493bf0a8fe0fa3bb8/) — 2026-03-04
- [Claude Code Skills × 自己完結スクリプト — MCP/CLIの先にある「トークン効率」設計](/blogs/posts/2026/03/2026-03-04-a0e7a789ef7534c7cb6136d7fb00572e/) — 2026-03-04
- [OpenHands 入門ガイド — 無料・オープンソースの AI コーディングエージェントを自分の PC で動かす](/blogs/posts/2026/03/2026-03-04-b22606904c5d5f513556e6a58c3b4657/) — 2026-03-04
- [Claude Code 起動画面のオレンジの生き物「Clawd」の正体 — カニ？タコ？誰も知らない公式マスコットの謎](/blogs/posts/2026/03/2026-03-04-b87ea2c5a866e42db6678c582963a6c5/) — 2026-03-04
- [Claude Cowork を最強にする 17 の方法 --- プロンプトではなく「設計」で差がつくシステム工学](/blogs/posts/2026/03/2026-03-04-bcecef951ac3e3bd81aafaa2c836b37a/) — 2026-03-04
- [「テスト書いて」と「テスト駆動で実装して」は全く別物 — AI×TDD で品質が劇的に変わる構造的理由](/blogs/posts/2026/03/2026-03-04-d84f897e8825bef6ac3f28ad5a982740/) — 2026-03-04
- [GitHub Copilot CLI の /research コマンド --- コミットログも Actions 履歴も全部調べてくれるディープリサーチ](/blogs/posts/2026/03/2026-03-04-db1fa7dce7e319be15057b655e03d099/) — 2026-03-04
- [Anthropic 公式 skill-creator の設計を解剖する — Orchestration Skill という新しいスキル設計パターン](/blogs/posts/2026/03/2026-03-04-e5839407fe23c117b54ce5ed77dac5fa/) — 2026-03-04
- [.env を AI に安心して触らせる — 1Password CLI ラッパー「opx」とプロセススコープ認証の設計](/blogs/posts/2026/03/2026-03-04-ee3017a7e8bcfbb995b93b8884cec258/) — 2026-03-04
- [ローカル LLM を社内業務に特化させる 4 段階カスタマイズ — Qwen3 を「より賢く」する仕組み](/blogs/posts/2026/03/2026-03-04-f7bad4476f8bec3e58bcf01848bfb807/) — 2026-03-04
- [Obsidian × Claude Code で「AIセカンドブレイン」を構築する — コンテキストがプロンプトに勝つ時代](/blogs/posts/2026/03/2026-03-05-00a5a21b56da09807d7c114573cbcf14/) — 2026-03-05
- [Claude Code が .env を読んでログに出した — MCC 乗っ取り8桁被害の原因が特定された](/blogs/posts/2026/03/2026-03-05-101618cbfc2f38b7321f85297a65da72/) — 2026-03-05
- [Claude-Native Designer — デザイナーが「作る人」になるFigma MCP × Claude Codeワークフロー](/blogs/posts/2026/03/2026-03-05-1f81385148befa3ee0e980408c174676/) — 2026-03-05
- [Everything Claude Code — Anthropic ハッカソン優勝者が作った「Claude Code 設定バイブル」の全貌](/blogs/posts/2026/03/2026-03-05-2b18749e88b9e71b16a4fe6f5947011b/) — 2026-03-05
- [「あなたは何者？」— 職能の境界が溶けた AI 時代に、認知パターンで自分を再定義する](/blogs/posts/2026/03/2026-03-05-4716b0356dc37a6ecff5ffdc4cd9b5cd/) — 2026-03-05
- [OpenClaw 22,000字解説のファクトチェック --- AIエージェントの民主化煽りと技術的実態の分離](/blogs/posts/2026/03/2026-03-05-630f39a50673da78f8e5114781f6c8ff/) — 2026-03-05
- [Claude Code に潜んでいた3つの脆弱性 — git clone だけで API キーが盗まれる仕組み](/blogs/posts/2026/03/2026-03-05-788d211750014f243a3b9f0c56e7192c/) — 2026-03-05
- [Goose 完全ガイド — Block が作った無料オープンソース AI エージェントの全貌](/blogs/posts/2026/03/2026-03-05-79be6da14ac16c7e51167d5a9747228f/) — 2026-03-05
- [Google Antigravity × Claude Code × Gemini × Nano Banana — AI時代の開発環境レイアウト設計](/blogs/posts/2026/03/2026-03-05-946ec0898ef07511328522277fd9ecfa/) — 2026-03-05
- [Claude Code 時代、UI デザイナーの仕事は軽くならない — 「整える仕事」の自動化と評価軸シフト](/blogs/posts/2026/03/2026-03-05-b03527dbe6ad00bfac9b4b431248b524/) — 2026-03-05
- [GitNexus × ゼロサーバーコード知能 --- ナレッジグラフで影響範囲を可視化する新しいコードリーディング](/blogs/posts/2026/03/2026-03-05-b33112efb8463209afbeadaf568ec58d/) — 2026-03-05
- [Google Workspace CLI（gws）— Drive・Gmail・Calendarを1コマンドで操作するAIエージェント対応ツール](/blogs/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/) — 2026-03-05
- [「Claude Code無料で無制限」は本当か × ollama launch claudeの実態と品質ギャップの正直な話](/blogs/posts/2026/03/2026-03-05-bf2e6519b561967327735da3f05142be/) — 2026-03-05
- [Shannon — 自律型AIペネトレーションテスターが「実証なき報告」を終わらせる](/blogs/posts/2026/03/2026-03-05-c412a36c7b360f30945b91a52f510103/) — 2026-03-05
- [Qwen Code ローカル運用実践記 — Mac Studio M3 Ultra で Ollama + qwen3-coder:30b を動かして分かったこと](/blogs/posts/2026/03/2026-03-06-9023009193920fd0ad17eda629351b18/) — 2026-03-06
- [Qwen Code 初心者ガイド — 無料で使えるオープンソース CLI コーディングエージェント](/blogs/posts/2026/03/2026-03-06-e053dfb0c2bee4f36f609060b3dfd487/) — 2026-03-06
- [Claude Codeのハルシネーション対策 — Anti-Hallucination Protocolという考え方](/blogs/posts/2026/03/2026-03-08-anti-hallucination-protocol/) — 2026-03-08
- [Claude Codeですべての日常業務を爆速化する — コーディング以外の活用術](/blogs/posts/2026/03/2026-03-09-claude-code-daily-business/) — 2026-03-09
- [Claude Code でツール実行前にセキュリティリスクをパーセンテージ表示させる CLAUDE.md 設定](/blogs/posts/2026/03/2026-03-09-claude-code-security-risk-prompt/) — 2026-03-09
- [Claude Code Security — AI がコードベースの脆弱性を発見・修正提案する新機能](/blogs/posts/2026/03/2026-03-09-claude-code-security/) — 2026-03-09
- [Claudeのデザインが急に良くなった理由 ― frontend-design スキルと「一般的」から離れるプロンプト](/blogs/posts/2026/03/2026-03-09-claude-frontend-design-skill/) — 2026-03-09
- [Impeccable — AI コーディングツールのフロントエンド設計を底上げするスキルライブラリ](/blogs/posts/2026/03/2026-03-09-impeccable-ai-design-skills/) — 2026-03-09
- [Claude Code時代の仕様書の役割 — ゼロトピック #337 から考える仕様駆動開発](/blogs/posts/2026/03/2026-03-10-claude-code-spec-driven-dev/) — 2026-03-10
- [freee MCP × Claude Code で確定申告の仕訳1,428件を20分で終わらせた話](/blogs/posts/2026/03/2026-03-10-freee-mcp-claude-code/) — 2026-03-10
- [VS Code AI コーディングアシスタントのインストール数推移：GitHub Copilot の急落と競合の台頭](/blogs/posts/2026/03/2026-03-11-ai-coding-assistant-vscode-installs/) — 2026-03-11
- [Claude Code のスキルを作るなら skill-creator プラグインを使おう](/blogs/posts/2026/03/2026-03-11-claude-code-skill-creator/) — 2026-03-11
- [Claude Code vs Codex：AI コーディングエージェント徹底比較 2026](/blogs/posts/2026/03/2026-03-11-claude-code-vs-codex/) — 2026-03-11
- [Claude Code vs OpenClaw — 「どっちを勉強すべき？」に対する責務ベースの選び方](/blogs/posts/2026/03/2026-03-11-claude-code-vs-openclaw/) — 2026-03-11
- [Claude Code に Auto Mode が登場 — 許可プロンプトなしで長時間タスクを実行](/blogs/posts/2026/03/2026-03-12-claude-code-auto-mode/) — 2026-03-12
- [非エンジニア(ADHD)が2ヶ月間Claude Codeに夢中になった結果、分身が生まれてシンギュラリティーに入った話](/blogs/posts/2026/03/2026-03-12-claude-code-non-engineer-adhd-singularity/) — 2026-03-12
- [Claude Code の Skills でプロンプト履歴を分析し、新人教育に活用する](/blogs/posts/2026/03/2026-03-12-claude-code-skills-training/) — 2026-03-12
- [Claude Codeで大量データを扱うならSQLite/DuckDBを使おう](/blogs/posts/2026/03/2026-03-12-claude-code-sqlite-duckdb/) — 2026-03-12
- [CLAUDE.mdを採点・改善してくれるClaude Code公式プラグイン claude-md-improver](/blogs/posts/2026/03/2026-03-12-claude-md-improver/) — 2026-03-12
- [Codified Context — 10万行規模の開発でもAIに一貫したコードを書かせる3層メモリ手法](/blogs/posts/2026/03/2026-03-12-codified-context/) — 2026-03-12
- [geo-seo-claude：AI検索時代のSEO最適化をClaude Codeで自動化するオープンソースツール](/blogs/posts/2026/03/2026-03-12-geo-seo-claude/) — 2026-03-12
- [Claude Codeで「AI チーフ・オブ・スタッフ」を構築する ― Jim Prosserの36時間実験](/blogs/posts/2026/03/2026-03-13-claude-code-chief-of-staff/) — 2026-03-13
- [Claude Code × ローカルLLM で KVキャッシュが毎回無効化される問題と対策](/blogs/posts/2026/03/2026-03-13-claude-code-local-llm-kv-cache/) — 2026-03-13
- [営業向けClaude Code活用術：/mtg-prepで商談準備が5分で終わる世界線](/blogs/posts/2026/03/2026-03-13-claude-code-sales-mtg-prep/) — 2026-03-13
- [Anthropic AI Academy: Claude を体系的に学べる無料公式コース](/blogs/posts/2026/03/2026-03-14-anthropic-ai-academy/) — 2026-03-14
- [スタッフ0人の税理士がClaude Codeで顧問先60社を1人で回す全手法](/blogs/posts/2026/03/2026-03-14-solo-tax-accountant-claude-code/) — 2026-03-14
- [AI駆動開発で変わるコスト構造：技術力からドメイン知識へのシフト](/blogs/posts/2026/03/2026-03-15-ai-driven-dev-domain-knowledge/) — 2026-03-15
- [寝る前の2分指示で3,000万円分の仕事をこなす Claude Code の衝撃](/blogs/posts/2026/03/2026-03-16-claude-code-overnight-tasks/) — 2026-03-16
- [Anthropic が Claude 専用の認定資格試験を公開 — AI アーキテクト認定でスキルを証明する時代へ](/blogs/posts/2026/03/2026-03-17-anthropic-claude-certification-exam/) — 2026-03-17
- [Claude Code 新機能「Auto Mode」完全解説](/blogs/posts/2026/03/2026-03-17-claude-code-auto-mode/) — 2026-03-17
- [Claude Code で使える神コマンド10選 — 知らないと時間を溶かす](/blogs/posts/2026/03/2026-03-17-claude-code-commands/) — 2026-03-17
- [非エンジニアでも1分で始められる Claude Code — CLAUDE.md 3行から始める仕事委任術](/blogs/posts/2026/03/2026-03-17-claude-code-setup-for-non-engineers/) — 2026-03-17
- [Claude Code スキル活用の知見：Anthropic 社内での実践から学んだこと](/blogs/posts/2026/03/2026-03-17-claude-code-skills-lessons/) — 2026-03-17
- [Claude Code Channels で変わる AI 開発ワークフロー：OpenClaw との組み合わせが最適解か](/blogs/posts/2026/03/2026-03-21-claude-code-channels/) — 2026-03-21
- [Claude Code を「自分専用の開発チーム」に変える3つの機能 — フック・カスタムコマンド・サブエージェント](/blogs/posts/2026/03/2026-03-22-claude-code-hooks-commands-subagents/) — 2026-03-22
- [Claude Codeを使うなら最低限やっておきたい「7つのセキュリティ設定」](/blogs/posts/2026/03/2026-03-23-claude-code-7-security-settings/) — 2026-03-23
- [Claude Codeをメインのデザインツールに：Tailwind CSSデザイナーSteve Schogerの1時間解説動画](/blogs/posts/2026/03/2026-03-23-claude-code-design-tool-steve-schoger/) — 2026-03-23
- [Claude Codeで東証の株取引を半自動化する【ペーパートレードで-19万円編】](/blogs/posts/2026/03/2026-03-23-claude-code-stock-trading-paper-trade/) — 2026-03-23
- [Claude Desktop Preview: 画面クリックでDOM要素を直接指定してUI修正できる新機能](/blogs/posts/2026/03/2026-03-23-claude-desktop-preview-dom-select/) — 2026-03-23
- [Renoise：Claude Code + Seedance 2.0 で動画広告制作を100倍スケールさせるAIツール](/blogs/posts/2026/03/2026-03-24-renoise-claude-code-seedance/) — 2026-03-24
- [Agent Plugins for AWS: Claude Code から AWS アーキテクチャ設計・デプロイまで一気通貫](/blogs/posts/2026/03/2026-03-25-aws-agent-plugins-claude-code/) — 2026-03-25
- [Claude Codeで「専門家チーム」を構築する：カスタムエージェントとCoworkの活用法](/blogs/posts/2026/03/2026-03-25-claude-code-expert-agents/) — 2026-03-25
- [Claude Code: dangerously-skip-permissions をやめて auto mode に移行する](/blogs/posts/2026/03/2026-03-25-claude-code-skip-permissions-to-auto/) — 2026-03-25
- [Claude Subconscious：Claude Code にセッション横断の記憶力を与える Letta AI のオープンソースツール](/blogs/posts/2026/03/2026-03-25-claude-subconscious/) — 2026-03-25
- [AI疲れへのアンサー: Claude Code のハーネス機能は本当に必要か](/blogs/posts/2026/03/2026-03-26-ai-fatigue-claude-code-simplicity/) — 2026-03-26
- [Claude Code の Auto Mode から見える AGI への道筋](/blogs/posts/2026/03/2026-03-26-claude-code-auto-mode-agi/) — 2026-03-26
- [Claude Code で Laravel→Django 全自動移行をやってみた（2/3）自動化基盤編](/blogs/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-automation/) — 2026-03-26
- [Claude Code で Laravel→Django 全自動移行をやってみた（3/3）実行結果・教訓編](/blogs/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-lessons/) — 2026-03-26
- [Claude Code で Laravel→Django 全自動移行をやってみた（1/3）計画編](/blogs/posts/2026/03/2026-03-26-claude-code-laravel-django-migration-plan/) — 2026-03-26
- [AI社員40人を作って1ヶ月で全部やめた話 — 壊れない設計のために知っておくべきこと](/blogs/posts/2026/03/2026-03-30-ai-agents-40-failure/) — 2026-03-30
- [Claude Codeベストプラクティス疲れに終止符 — claude-code-best-practiceリポジトリ一本で運用する方法](/blogs/posts/2026/03/2026-03-30-claude-code-best-practice-repo/) — 2026-03-30
- [Claude Code + Self-hosted Runner: 「Auto mode is unavailable for your plan」エラーの原因と対処](/blogs/posts/2026/03/2026-03-31-claude-code-self-hosted-runner-auto-mode/) — 2026-03-31
- [Claude Code のソースコードが npm のソースマップから全公開された件](/blogs/posts/2026/03/2026-03-31-claude-code-source-map-leak/) — 2026-03-31
- [Claude Code の sensitive file チェックを回避する — git worktree の配置場所を .claude/ の外に移す](/blogs/posts/2026/03/2026-03-31-claude-code-worktree-permission/) — 2026-03-31
- [Claude Code のデフォルト設定でトークンを無駄にしていた話](/blogs/posts/2026/04/2026-04-06-claude-code-token-optimization/) — 2026-04-06
- [Claude Code にカオスエンジニアリングエージェントを導入してリポジトリの弱点を発見する](/blogs/posts/2026/04/2026-04-07-claude-code-chaos-engineer-agent/) — 2026-04-07
- [RTK（Rust Token Killer）でClaude Codeのトークン使用量を60〜90%削減する](/blogs/posts/2026/04/2026-04-07-rtk-rust-token-killer-claude-code/) — 2026-04-07
- [Exbrain — Claude Code × Obsidian で「外付けAI脳」を構築する](/blogs/posts/2026/04/2026-04-09-exbrain-claude-code-obsidian-ai-brain/) — 2026-04-09
- [メルカリのClaude Code企業導入ガイド：セキュリティ設定と組織配布の実践戦略](/blogs/posts/2026/04/2026-04-11-mercari-claude-code-org-security/) — 2026-04-11
- [Claude CodeからShopifyストアを直接操作できる「Shopify AI Toolkit」](/blogs/posts/2026/04/2026-04-12-claude-code-shopify-ai-toolkit/) — 2026-04-12
- [Claude Code で作る「世界AIシミュレーター」— 20カ国AIエージェントが自律外交・紛争するリアルタイム地政学ゲーム](/blogs/posts/2026/04/2026-04-14-claude-code-world-ai-simulator/) — 2026-04-14
- [AI Agent に品質を担保させる — QA 手法の実践ガイド](/blogs/posts/2026-03-09-ai-agent-qa/) — 2026-03-09
- [Harness Engineering ベストプラクティス 2026 — AI コーディングエージェントを安定稼働させる設計術](/blogs/posts/2026-03-09-harness-engineering/) — 2026-03-09
- [Claude Code Review — エージェントチームが PR のバグを狩る新機能](/blogs/posts/2026-03-10-claude-code-review/) — 2026-03-10
- [OpenClaw × Claude Code セットアップガイド — AI エージェントチームを構築する2つのアプローチ](/blogs/posts/2026-03-10-openclaw-claude-code-setup/) — 2026-03-10
- [クラウド LLM の地政学リスクが顕在化 — ローカル LLM 移行を本気で考える時](/blogs/posts/2026/03/2026-03-01-7b83b0c9049f181c85636073365e406a/) — 2026-03-01
- [Claude Opus 4.6 がゼロデイ脆弱性を500件発見 — AI推論がセキュリティ業界を揺るがす](/blogs/posts/2026/03/2026-03-02-9cef5b3013c2cdaa3ec1d190b4d5f90f/) — 2026-03-02
- [AI が書いた CLAUDE.md は逆効果 --- 「コンテキストファイルの自動生成は精度を下げる」という研究](/blogs/posts/2026/03/2026-03-03-95278de03de967bcc74ff8b320222044/) — 2026-03-03
- [Anthropic、ChatGPT からの移行ツール提供開始 --- メモリインポートと App Store 1位の背景](/blogs/posts/2026/03/2026-03-04-b8b0f06e9ac13cce154f50e510c2fdc7/) — 2026-03-04
- [Claude Coworkを「完璧な右腕」に変える最強の初期設定](/blogs/posts/2026/03/2026-03-17-claude-cowork-initial-setup/) — 2026-03-17
- [デザイナーのためのAI活用術5選 — 制作スピードを劇的に上げる実践テクニック](/blogs/posts/2026/03/2026-03-18-ai-design-workflow/) — 2026-03-18
- [AI は会話が長くなるほど「迷子」になる — Microsoft × Salesforce の研究解説](/blogs/posts/2026/02/2026-02-27-61e0abd5ba76e70dabc257c5f0e6560b/) — 2026-02-27
- [2026年に求められるAIエンジニアのロードマップ — 350万インプレッション超の話題スレッドを解説](/blogs/posts/2026/04/2026-04-14-2026-ai-engineer-roadmap/) — 2026-04-14
