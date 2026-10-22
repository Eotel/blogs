---
title: "Generative UI"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の 4 パターンに分類される"
date: 2026-07-18
lastmod: 2026-07-18
aliases:
  - "generative UI"
  - "Generative UI パターン"
  - "Dynamic パターン"
  - "AI UI generation"
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "frontend", "llm", "cloudflare-workers", "dynamic-workers"]
---

## 概要

LLM の出力に応じて UI を動的に組み立てるアプローチの総称。「AI が UI を生成する」パターンとも呼ばれる。CopilotKit が整理した 3 分類に、Hono 作者の yusukebe（Cloudflare）が提案した **Dynamic パターン**を加えた 4 つの実装スペクトラムとして整理されつつある。

## 4 つの実装パターン

**右に行くほど AI の自由度が上がり、開発者の制御が下がるスペクトラム。**

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義のコンポーネント） | 低 |
| **Declarative** | UI 構造の宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中低 |
| **Dynamic** | 抽象化されたコード（JSX 等）+ サンドボックス実行 | フレームワーク境界 + サンドボックス境界 | 中高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホストはサンドボックスを提供するだけ） | 高 |

### Static

LLM が返した値を事前に定義された UI コンポーネントに当てはめる。表示は完全に開発者の管理下で、本番アプリに最も使いやすい。AI の関与は「データの供給者」に留まる。

### Declarative

LLM に「カード」「リスト」「フォーム」のような構造を JSON などで宣言させ、フロントエンドが自前のコンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。スペックの表現力が上限になる。

### Dynamic（yusukebe 提案）

Declarative の「制御できるが表現力に上限がある」と Open-ended の「自由だが制御不能」の中間を取るポジション。LLM に JSX 等の抽象化されたコードを書かせ、**サーバー側のサンドボックスで動的にロード・実行**して結果を UI として返す。

実行基盤として [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) を使い、リクエストごとに V8 isolate を起動する。Declarative では表現できないロジック・インタラクションをコードとして書かせつつ、フレームワークの抽象とサンドボックスの境界で制御を保つ。

### Open-ended

LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe で実行する。AI の表現力は最大だが、一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピングや実験的ツールに向く。

## どのパターンを選ぶか

| パターン | 向いているケース |
|---|---|
| Static | ミッションクリティカルな業務 UI、一貫した UX が必須 |
| Declarative | 動的なダッシュボード、フォーム生成、マルチプラットフォーム描画 |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたい |
| Open-ended | プロトタイピング、実験的ツール |

## ストリーミング体験

パターンによってストリーミング時の体験（UI が描画されていく過程）が大きく異なる。Static は値が揃ってから一度に表示、Open-ended は HTML が流れるにつれてブラウザが逐次レンダリングする。Dynamic の体験は実装依存で設計の余地が広い。

## 関連プロトコル

Generative UI 周辺では標準化も進行中：

- **A2UI** — Google が提案する AI と UI の契約レイヤー
- **AG-UI** — エージェントと UI フレームワーク間のプロトコル
- **MCP Apps** — MCP をベースにした UI 生成拡張

「AI とフロントエンドの間の契約をどの抽象度で結ぶか」は現在進行中の論点。

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [microVM](/blogs/wiki/concepts/microvm/) — AI 生成コードの隔離実行（microVM ベースの代替）
- [microsandbox](/blogs/wiki/tools/microsandbox/) — microVM ベースのサンドボックス実行環境
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Generative UI を生成する主体

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
