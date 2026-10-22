---
title: "Generative UI"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の 4 パターンスペクトラムで整理される"
date: 2026-08-01
lastmod: 2026-08-01
aliases: ["Generative UI", "生成UI", "generative ui"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "LLM", "frontend", "AI"]
---

## 概要

LLM の出力に応じて UI を動的に組み立てるアプローチ。「AI が UI を生成する」という考え方で、チャット一辺倒ではなく AI と UI を組み合わせる設計の一形態。実装方法は開発者の制御と AI の自由度のトレードオフによって連続的なスペクトラムを形成し、大きく 4 つのパターンに分類できる。

## 4 パターンのスペクトラム

CopilotKit の整理（"The Three Types of Generative UI"）をベースに、第 4 の Dynamic パターンを加えた分類。

| パターン | LLM が返すもの | UI の制御 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義のコンポーネント） | 低 |
| **Declarative** | UI 構造を表す宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等） | サーバーサイドサンドボックスで実行 | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホスト側はサンドボックスを提供するだけ） | 最高 |

右に行くほど AI の自由度が上がり、開発者の制御が下がる。

### Static パターン

LLM が返した値を事前定義の UI コンポーネントに当てはめる。表示は開発者の完全管理下にあり、本番アプリで最も使いやすい。AI の関与は薄いが、体験は保守的で一貫性が高い。

### Declarative パターン

LLM に「カード」「リスト」「フォーム」のような構造を JSON 等で宣言させ、フロントエンドが自前のコンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。動的なダッシュボード・フォーム生成・マルチプラットフォーム描画に向く。

### Dynamic パターン（第 4 の提案）

Hono 作者の yusukebe（和田裕介）が 2026 年 6 月の発表「AI時代のUIはどこへ行く？その2！」で提案したパターン。Declarative の制御と Open-ended の自由のいいとこ取りを狙う。

- LLM に生の HTML ではなく React/JSX のような**抽象化されたコード**を書かせる
- 生成されたコードを**サーバー側のサンドボックスで動的にロード・実行**し、UI として返す
- 実行基盤には [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/)（Worker Loader API）を使う

「構造化されているが表現力に上限がある Declarative」と「自由だが制御不能な Open-ended」の間を取るポジション。宣言的スペックでは表現できないロジックやインタラクションをコードとして書かせつつ、フレームワークの抽象とサンドボックスの境界という二重の枠に収める。

### Open-ended パターン

LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe の中で実行する。AI の表現力は最大だが、一貫性・安全性・アクセシビリティの保証が難しく、プロトタイピングや実験的ツール向け。

## ストリーミング時の体験

パターンごとに UI が描画されていく過程の見え方が大きく異なる。Static は値が揃ってから表示、Declarative はスペック確定後に描画、Dynamic/Open-ended はコード生成中も段階的に反映できる。

## 関連プロトコル・標準化

Generative UI 周辺では標準化も進行中。

- **A2UI** — Google が推進する AI から UI への契約
- **AG-UI** — エージェントと UI の間のプロトコル
- **MCP Apps** — [MCP](/blogs/wiki/concepts/mcp/) 経由で UI を提供するアプローチ

「AI とフロントエンドの間の契約をどの抽象度で結ぶか」が現在進行形の論点。Dynamic パターンは契約を「宣言的スペック」と「生 HTML」の間にある「抽象化されたコード + サンドボックス実行」に置く提案として位置づけられる。

## どのパターンを選ぶか

| パターン | 向いているケース |
|---|---|
| Static | ミッションクリティカルな業務 UI、一貫した UX が必須の本番アプリ |
| Declarative | 動的なダッシュボード、フォーム生成、マルチプラットフォーム描画 |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたいとき |
| Open-ended | プロトタイピング、実験的なツール |

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [MCP（Model Context Protocol）](/blogs/wiki/concepts/mcp/) — エージェントと外部ツール・UI をつなぐプロトコル
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要な場合の実行基盤（Dynamic Workers の V8 isolate と対比）
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Generative UI を組み込む自律システム

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
