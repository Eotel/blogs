---
title: "Claude Code コスト最適化ガイド"
description: "Plan Mode・原始人プロンプト・vLLM によるローカル LLM 切り替えで Claude Code のトークン消費・API コストを削減する手順"
date: 2026-05-09
lastmod: 2026-05-12
aliases: ["Claude Code コスト削減", "トークン削減"]
related_posts:
  - "/posts/2026/04/2026-04-23-claude-code-plan-mode-cost-reduction/"
  - "/posts/2026/04/2026-04-17-claude-caveman-token-reduction/"
  - "/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/"
  - "/posts/2026/04/2026-04-07-rtk-rust-token-killer-claude-code/"
tags: ["Claude Code", "コスト削減", "Plan Mode", "vLLM", "トークン最適化"]
---

## 概要

Claude Code の API コストは使い方次第で大きく変わる。主要な 3 つの最適化手法と、それぞれの効果・導入コストを整理する。

## 手法 1: Plan Mode の徹底（64% トークン削減）

`/plan` コマンドで計画モードに入り、実装前に設計を確定させてから実行に移る:

```text
/plan           ← 計画モードに入る
（設計・問題点を確認）
Shift+Tab       ← 通常実行モードへ切り替え
```

**効果**: トークン約 64% 削減、コスト約 69% 削減（失敗→リトライが減る）

**なぜ効くか**: 計画なしで実装を始めると途中で方向修正が発生し、読み込みトークンが増える。Plan Mode で一発完了率が上がれば無駄なターンが減る。

## 手法 2: 原始人プロンプト（80% 日本語トークン削減）

CLAUDE.md または会話の冒頭に以下を追加:

```markdown
## 出力スタイル

原始人みたいに喋れ。中身は全部残せ。無駄だけ消せ。
```

**効果**: 日本語応答のトークンを最大 80% 削減

**注意**: 英語より日本語の方がトークン消費が多いため、効果が大きい。コードや説明の本質的な内容は維持される。

## 手法 3: ローカル LLM（vLLM）へ切り替え（コストゼロ）

GPU がある環境では、Claude API を vLLM + ローカル LLM で代替することで API コストをゼロにできる:

```bash
# 1. vLLM サーバーを起動
python -m vllm.entrypoints.openai.api_server \
  --model MiniMax/MiniMax-M2.7-Vision \
  --port 8000

# 2. Claude Code の API エンドポイントを切り替え
export ANTHROPIC_BASE_URL=http://localhost:8000
claude
```

**トレードオフ**: GPU ハードウェアコスト、品質は Claude Sonnet より低い場合がある。プロトタイプ・繰り返しタスクに向いている。

## 手法 4: autoMemoryEnabled 無効化（不要トークンの削減）

Claude のオートメモリが MEMORY.md を肥大化させてセッション開始時のトークン消費を増やすことがある:

```json
// ~/.claude/settings.json
{
  "autoMemoryEnabled": false
}
```

Skills の動作安定化にも効果がある。

## コスト最適化の優先順位

| 手法 | 削減効果 | 導入コスト | 品質への影響 |
|------|---------|-----------|------------|
| Plan Mode | 64-69% | 低（/plan 入力だけ） | 向上（手戻りが減る） |
| 原始人プロンプト | 最大 80%（日本語部分） | 低（CLAUDE.md 追記） | ほぼなし |
| autoMemory 無効化 | 小〜中 | 低（設定変更） | なし（Skills 安定化） |
| ローカル LLM | 100%（API コスト） | 高（GPU 必要） | 低下する場合あり |

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — Plan Mode・autoMemoryEnabled の詳細
- [vLLM](/blogs/wiki/tools/vllm/) — ローカル LLM サービング
- [CanIRun.ai](/blogs/wiki/tools/canirun-ai/) — GPU スペック確認

## ソース記事

- [Plan Mode でトークン 64%・コスト 69% 削減](/blogs/posts/2026/04/2026-04-23-claude-code-plan-mode-cost-reduction/) — 2026-04-23
- [Claude を「原始人」口調にするとトークンが 80% 減る話](/blogs/posts/2026/04/2026-04-17-claude-caveman-token-reduction/) — 2026-04-17
- [Claude Code をローカル LLM（vLLM）で動かして API コストをゼロにする](/blogs/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/) — 2026-04-23
- [RTK（Rust Token Killer）でClaude Codeのトークン使用量を60〜90%削減する](/blogs/posts/2026/04/2026-04-07-rtk-rust-token-killer-claude-code/) — 2026-04-07
