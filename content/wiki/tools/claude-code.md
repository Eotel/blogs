---
title: "Claude Code"
description: "Anthropic 公式の CLI ベース AI コーディングエージェント"
date: 2026-04-06
lastmod: 2026-05-09
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
