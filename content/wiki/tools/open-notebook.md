---
title: "Open-notebook"
description: "NotebookLM のオープンソース代替。ローカルまたは Ollama 経由のローカル LLM で動作するセルフホスト型 AI ナレッジベース"
date: 2026-05-09
lastmod: 2026-05-09
aliases: ["open-notebook", "NotebookLM OSS代替"]
related_posts:
  - "/posts/2026/04/2026-04-22-open-notebook-notebooklm-oss/"
tags: ["OSS", "NotebookLM", "ナレッジ管理", "ローカルLLM", "Ollama", "セルフホスト"]
---

## 概要

Open-notebook は Google NotebookLM のオープンソース代替プロジェクト。Docker でセルフホストでき、Ollama 経由のローカル LLM にも対応する。ドキュメントをアップロードして質問・要約・ポッドキャスト生成などを行える。

## 特徴

- **セルフホスト**: Docker Compose で即起動、データが手元に残る
- **ローカル LLM 対応**: Ollama 経由で Llama 3・Gemma・Mistral 等を使用可能（API コストゼロ）
- **複数ドキュメント**: PDF・Web ページ・テキストを組み合わせてナレッジベースを構築
- **ポッドキャスト生成**: NotebookLM の目玉機能に相当するオーディオ概要を生成

## NotebookLM との比較

| 観点 | Google NotebookLM | Open-notebook |
|------|------------------|---------------|
| データの場所 | Google サーバー | 自分のサーバー |
| LLM | Gemini（固定） | 設定可能（Ollama / OpenAI / Anthropic）|
| コスト | 無料〜有料 | セルフホスト費用のみ |
| オフライン | 不可 | Ollama なら可 |
| カスタマイズ | 不可 | OSS なので改修可能 |

## セットアップ

```bash
git clone https://github.com/lfnovo/open-notebook
cd open-notebook
cp .env.example .env   # API キーや Ollama 設定を記入
docker compose up -d
```

`http://localhost:8502` にアクセスして使用開始。

## 関連ページ

- [Obsidian](/blogs/wiki/tools/obsidian/) — ドキュメント管理・ナレッジベースとして組み合わせ可能
- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/) — ナレッジベース構築の概念的背景
- [Ollama](/blogs/wiki/tools/ollama/) — ローカル LLM の実行環境

## ソース記事

- [Open-notebook — NotebookLM のオープンソース代替をローカルで動かす](/blogs/posts/2026/04/2026-04-22-open-notebook-notebooklm-oss/) — 2026-04-22
