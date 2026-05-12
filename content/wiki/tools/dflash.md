---
title: "DFlash"
description: "Apple Silicon 向け MLX フレームワークで動作するブロック拡散型投機的デコード実装。Qwen3-4B BF16 を最大 4.6 倍高速化"
date: 2026-04-23
lastmod: 2026-05-12
aliases: ["dflash-mlx", "Block Diffusion Flash Speculative Decoding"]
related_posts:
  - "/posts/2026/04/2026-04-15-dflash-mlx-apple-silicon-llm/"
  - "/posts/2026/05/2026-05-12-speculative-tts-acceleration-2026/"
tags: ["Apple Silicon", "MLX", "ローカルLLM", "推論高速化", "推測デコード"]
---

## 概要

DFlash（Block Diffusion for Flash Speculative Decoding）は投機的デコードを発展させた推論加速技術の MLX 実装（[dflash-mlx](https://github.com/Aryagm/dflash-mlx)）。デフォルトの Qwen3-4B BF16 で **最大 4.6 倍**（4028 トークン生成時、2048 トークンで 4.2 倍）のスループット向上を達成。精度を落とさない exact speculative decoding（ロスレス）。Qwen3.5-4B 用ターゲットも実験的にサポートされるが、現状は Qwen3 経路より速度が出ない（hybrid attention の rollback が未最適化）。

## 仕組み

通常の推測デコードは小さなドラフトモデルが 1 トークンずつ予測するのに対し、DFlash はドラフトモデルが **16 トークンを並列生成**。ターゲットモデルが 1 回のフォワードパスでまとめて検証するため大幅なスループット向上を実現。Apple 独自の Metal カーネルでロールバック処理を実装しオーバーヘッドを最小化。

## インストール

```bash
git clone https://github.com/aryagm/dflash-mlx.git
cd dflash-mlx
uv sync
uv run dflash-mlx --max-new-tokens 128
```

## 関連ページ

- [ローカル LLM 比較](/blogs/wiki/concepts/local-llm-comparison/)
- [投機的 TTS（Speculative TTS）](/blogs/wiki/concepts/speculative-tts/) — 同じ Speculative Decoding を音声合成（AR codec LM）に応用した系統

## ソース記事

- [MacのローカルLLMが4.1倍速に！Apple Silicon向け新技術「DFlash」](/blogs/posts/2026/04/2026-04-15-dflash-mlx-apple-silicon-llm/) — 2026-04-15
- [投機的 TTS は本当に効くのか — VADUSA / Llasa+ / SSD で読む 2026 年 TTS 高速化マップ](/blogs/posts/2026/05/2026-05-12-speculative-tts-acceleration-2026/) — 2026-05-12
