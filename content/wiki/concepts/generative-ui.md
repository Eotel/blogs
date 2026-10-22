---
title: "Generative UI"
description: "LLMの出力に応じてUIを動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の4パターンで制御と自由度のトレードオフを整理する"
date: 2026-06-27
lastmod: 2026-06-27
aliases: ["Generative UI", "ジェネレーティブUI", "AI Generated UI"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "llm", "frontend", "UI"]
---

## 概要

**Generative UI** は、LLM の推論出力に応じて UI を動的に組み立てるアプローチ。静的なテンプレートに値を流し込むのではなく、LLM がレイアウト・構造・あるいはコードそのものを生成し、フロントエンドがそれを受け取って表示する。

実装パターンは「LLM がどこまで UI 定義の権限を持つか」で連続したスペクトラムを形成する。右に行くほど LLM の自由度が上がり、開発者の制御が下がる。

## 4 パターンのスペクトラム

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義のコンポーネント） | 低 |
| **Declarative** | UI 構造の宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等） | サンドボックス実行基盤 | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホストはサンドボックスを提供するだけ） | 高 |

### Static

LLM が返した値を、事前定義のコンポーネントに当てはめるだけ。表示は完全に開発者の管理下。ミッションクリティカルな業務 UI や一貫した UX が必須の本番アプリに適する。

### Declarative

LLM に「カード」「リスト」「フォーム」のような UI 構造を JSON などで宣言させ、フロントエンドが自前コンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。動的ダッシュボード・フォーム生成・マルチプラットフォーム描画に向く。CopilotKit が "The Three Types of Generative UI" で整理した分類の一つ。

### Dynamic（第4のパターン）

Hono 作者 yusukebe が 2026 年 6 月に提案した新しいポジション。Declarative の「制御可能だが表現力に上限がある」と Open-ended の「自由だが制御不能」の間を取る。

- LLM に **抽象化されたコード（JSX 等）** を生成させる（生 HTML ではない）
- 生成コードを **サーバー側サンドボックスで動的ロード・実行** し、結果を UI として返す
- 実行基盤として **Cloudflare Dynamic Workers**（V8 isolate）を使う

宣言的スペックでは表現できないロジックやインタラクションをコードで書かせつつ、フレームワークの抽象とサンドボックスの境界という二重の枠に収める。

### Open-ended

LLM が HTML/CSS/JavaScript を丸ごと生成し、sandbox 化された iframe で実行する。AI の表現力は最大になるが、一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピングや実験的ツールに向く。Claude Artifacts がこの代表例。

## どのパターンを選ぶか

| パターン | 向いているケース |
|---|---|
| Static | 本番業務 UI、一貫した UX が必須 |
| Declarative | 動的ダッシュボード、フォーム生成 |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたいとき |
| Open-ended | プロトタイピング、実験的ツール |

## 周辺の動向

Generative UI 周辺では標準化も進行中。

- **A2UI**（Google）、**AG-UI**、**MCP Apps** — AI とフロントエンドの間の契約抽象度を定義するプロトコル
- **Cloudflare Code Mode**（2025 年 9 月）— エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶ方がよいというコンセプト。動的コード実行のトークン使用量 81% 削減を報告

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [microsandbox](/blogs/wiki/tools/microsandbox/) — microVM ベースの代替サンドボックス実行基盤
- [microVM](/blogs/wiki/concepts/microvm/) — isolate vs. microVM のトレードオフ
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — LLM が UI を生成する文脈の上位概念
- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — エージェントとフロントエンドをつなぐプロトコル層

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
