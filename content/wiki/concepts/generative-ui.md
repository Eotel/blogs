---
title: "Generative UI"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の 4 パターンスペクトラムで整理される"
date: 2026-07-25
lastmod: 2026-07-25
aliases: ["Generative UI", "生成UI", "AI UI生成"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "frontend", "LLM", "cloudflare-workers"]
---

## 概要

LLM の出力に応じて UI を動的に組み立てるアプローチの総称。実装パターンは **制御と自由度のトレードオフ** によって 4 つに分類される。CopilotKit が "The Three Types of Generative UI" として整理した 3 分類（Static / Declarative / Open-ended）に、Cloudflare の Hono 作者 yusukebe が提案した **Dynamic パターン**を加えた 4 段階スペクトラムが 2026 年時点の共通理解になりつつある。

## 4 つのパターン

| パターン | LLM が返すもの | UI の制御者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義コンポーネント） | 低 |
| **Declarative** | UI 構造を表す JSON 等の宣言的スペック | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等） | サーバーサイドのサンドボックス | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホストはサンドボックスを提供するだけ） | 高 |

### Static パターン

LLM が返した値を事前に定義された UI コンポーネントに当てはめる。表示は完全に開発者の管理下にある。本番アプリで最も安全・安定。

### Declarative パターン

LLM に「カード」「リスト」「フォーム」のような構造を JSON で宣言させ、フロントエンドが自前コンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。マルチプラットフォーム描画に向く。

### Dynamic パターン（第 4 の選択肢）

yusukebe が 2026 年 6 月に提案した新パターン。LLM に JSX のような抽象化されたコードを生成させ、**サーバー側のサンドボックスで動的にロードして実行**し、結果を UI として返す。実行基盤には [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) の Worker Loader API を使う。

- Declarative の「制御されているが表現力に上限がある」と Open-ended の「自由だが制御不能」の中間
- 宣言的スペックでは表現できないロジック・インタラクションをコードとして書かせつつ、フレームワークの抽象とサンドボックスの二重の枠に収める

### Open-ended パターン

LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe の中で実行する。AI の表現力は最大だが、一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピング・実験的ツール向け。

## パターン選択の目安

| パターン | 向いているケース | リスク・コスト |
|---|---|---|
| Static | ミッションクリティカルな業務 UI | AI の関与が薄く体験は保守的 |
| Declarative | 動的ダッシュボード、フォーム生成 | スペックの表現力が上限になる |
| Dynamic | ロジック・インタラクションを AI に組ませたいとき | サンドボックス基盤の整備が前提 |
| Open-ended | プロトタイピング、実験的ツール | 一貫性・安全性の保証が難しい |

## ストリーミング体験との関係

パターンごとに、UI が段階的に描画されていく過程（ストリーミング時の体験）が大きく異なる。Static は全データが揃ってから一括表示になりやすく、Open-ended は逐次的に HTML が出てくる体験に近い。

## 関連プロトコル・標準化動向

Generative UI 周辺では Google の A2UI、AG-UI、MCP Apps といったプロトコルの標準化が同時並行で進んでいる。「AI とフロントエンドの間の契約をどの抽象度で結ぶか」は 2026 年現在も動いている論点。

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — AI と UI を繋ぐプロトコルの文脈
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要なケースの代替基盤
- [microsandbox](/blogs/wiki/tools/microsandbox/) — self-hosted な microVM サンドボックス
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — UI 生成の主体となるエージェント

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
