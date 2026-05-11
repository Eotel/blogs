---
title: "vLLM"
description: "高速 LLM 推論・サービングライブラリ。OpenAI 互換 API サーバーとして動作し Claude Code などのツールをローカル LLM で代替できる"
date: 2026-05-09
lastmod: 2026-05-09
aliases: ["vllm", "ローカルLLM推論"]
related_posts:
  - "/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/"
tags: ["ローカルLLM", "GPU", "OpenAI互換", "Python", "コスト削減"]
---

## 概要

vLLM はオープンソースの高速 LLM 推論・サービングライブラリ（UC Berkeley 発）。PagedAttention アルゴリズムにより、従来の推論フレームワークより高スループット・低レイテンシで LLM を動かせる。OpenAI 互換の API サーバーとして起動できるため、OpenAI SDK や Claude Code など `OPENAI_BASE_URL` を設定できるツールと組み合わせやすい。

## Claude Code との組み合わせ

`ANTHROPIC_BASE_URL` を vLLM のエンドポイントに向けることで、Claude Code をローカル LLM で動作させ API コストをゼロにできる:

```bash
# vLLM サーバーを起動（例: MiniMax-M2.7）
python -m vllm.entrypoints.openai.api_server \
  --model MiniMax/MiniMax-M2.7-Vision \
  --api-key dummy \
  --port 8000

# Claude Code の API エンドポイントを向ける
export ANTHROPIC_BASE_URL=http://localhost:8000
claude
```

## 対応モデル（代表例）

| モデル | 特徴 |
|--------|------|
| MiniMax-M2.7 | Mixture-of-Experts、コーディング性能が高い |
| Llama 3.3 70B | Meta の汎用高性能モデル |
| Qwen 2.5-Coder | コーディング特化、中・小サイズから選択可 |
| DeepSeek Coder V2 | コスパに優れるコーディングモデル |

## トレードオフ

| メリット | デメリット |
|---------|-----------|
| API コストゼロ | GPU ハードウェアが必要 |
| データがローカルに留まる | セットアップの手間 |
| オフライン動作可 | Claude Sonnet/Opus に比べ性能差がある |
| レイテンシがネットワーク依存しない | 量子化による品質低下 |

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — vLLM と組み合わせて API コストゼロで動作
- [CanIRun.ai](/blogs/wiki/tools/canirun-ai/) — GPU スペックの動作可否チェック
- [Ollama](/blogs/wiki/tools/ollama/) — より簡単なローカル LLM 実行環境

## ソース記事

- [Claude Code をローカル LLM（vLLM + MiniMax-M2.7）で動かして API コストをゼロにする](/blogs/posts/2026/04/2026-04-23-claude-code-local-llm-vllm/) — 2026-04-23
