---
title: "CanIRun.ai"
description: "ローカル LLM の動作可否を GPU スペックから即座に判定するブラウザツール。VRAM・RAM・量子化レベルを入力してモデルの実行可能性を確認"
date: 2026-05-09
lastmod: 2026-05-09
aliases: ["CanIRun", "ローカルLLMチェッカー"]
related_posts:
  - "/posts/2026/04/2026-04-22-canirun-ai-local-model-checker/"
tags: ["ローカルLLM", "GPU", "VRAM", "ツール", "LLM"]
---

## 概要

CanIRun.ai はブラウザで使えるローカル LLM 動作チェッカー。GPU の VRAM と量子化レベルを入力すると、Llama 3・Qwen・Gemma などの代表的なモデルが動くかどうかを即座に判定する。「このモデルを試したいが自分の PC で動くか」を素早く確認できる。

## 使い方

1. [canirun.ai](https://canirun.ai) にアクセス
2. GPU モデルを選択（または VRAM 容量を手動入力）
3. 量子化レベル（Q4_K_M など）を選択
4. 対象モデルを選択
5. 判定結果（動く/動かない + 推奨設定）が表示される

## 判定で使われる主な指標

| 指標 | 内容 |
|------|------|
| **VRAM** | モデルの重みをロードするのに必要なグラフィックメモリ |
| **量子化** | Q4_K_M（4bit）・Q8（8bit）などで必要 VRAM が変わる |
| **コンテキスト長** | 128k トークン vs 8k で必要メモリが大きく変わる |
| **RAM** | VRAM が足りない場合にメインメモリ（CPU オフロード）が必要 |

## 量子化の目安

| 量子化 | 品質 | VRAM 消費 |
|--------|------|----------|
| Q2_K | 最低（精度大幅低下） | 最小 |
| Q4_K_M | 実用品質（推奨） | 中 |
| Q8_0 | ほぼオリジナル品質 | 大 |
| F16 | オリジナル品質 | 最大 |

## 関連ページ

- [Ollama](/blogs/wiki/tools/ollama/) — ローカル LLM の実行環境
- [Claude Code](/blogs/wiki/tools/claude-code/) — vLLM 経由でローカル LLM と接続可能

## ソース記事

- [CanIRun.ai — ローカル LLM が自分の PC で動くか即座にチェック](/blogs/posts/2026/04/2026-04-22-canirun-ai-local-model-checker/) — 2026-04-22
