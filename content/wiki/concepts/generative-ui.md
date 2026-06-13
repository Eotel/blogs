---
title: "Generative UI（生成 UI パターン）"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチの 4 パターン分類: Static / Declarative / Dynamic / Open-ended。制御と自由度のトレードオフで選ぶ"
date: 2026-06-13
lastmod: 2026-06-13
aliases: ["Generative UI", "生成UI", "AIによるUI生成", "Dynamic パターン"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "LLM", "frontend", "cloudflare-workers", "dynamic-workers"]
---

## 概要

Generative UI は LLM の出力に応じて UI を動的に組み立てるアプローチの総称。実装は **制御と自由度のトレードオフ**に沿って 4 パターンに分類される。CopilotKit が "The Three Types of Generative UI" として 3 分類を整理し、Hono 作者の yusukebe（和田裕介）がフロントエンド・PHPカンファレンス北海道2026（2026 年 6 月）の発表「AI時代のUIはどこへ行く？その2！」で第 4 の「Dynamic パターン」を提案した。

## 4 パターンのスペクトラム

右に行くほど AI の自由度が上がり、開発者の制御が下がる。

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義コンポーネント） | 低 |
| **Declarative** | UI 構造の宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等） | サーバーサイドサンドボックスで動的実行 | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホストはサンドボックスを提供するだけ） | 高 |

## 各パターンの特徴

**Static** は LLM が返した値を事前定義の UI に当てはめる。最も本番向きで一貫した UX を保てる。チャットボットのレスポンスに構造化カードを埋め込む用途などが典型。

**Declarative** は LLM に「カード」「リスト」「フォーム」のような構造を JSON 等で宣言させ、フロントエンドが自前のコンポーネントで描画する。AI がレイアウトを選べるが、最終権限はフロントエンドに残る。表現力の上限はスペック設計に依存する。

**Dynamic（第 4 のパターン、yusukebe 提案）** は LLM に JSX 等の抽象化されたコードを書かせて、サーバー側サンドボックス（[Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) 等）で動的に実行する。Declarative の構造化と Open-ended の自由の中間を狙う。実行基盤の整備が前提になる。

**Open-ended** は LLM が HTML/CSS/JavaScript 全体を生成し、サンドボックス化された iframe の中で実行する。表現力最大だが一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピングや実験的ツール向き。

## ユースケース別の選択

| パターン | 向いているケース | 注意点 |
|---|---|---|
| Static | ミッションクリティカルな業務 UI | AI の関与が薄く、体験は保守的 |
| Declarative | 動的ダッシュボード、フォーム生成、マルチプラットフォーム描画 | スペックの表現力が上限 |
| Dynamic | AI にロジック・インタラクションを組ませたいとき | 実行基盤（サンドボックス）の整備が前提 |
| Open-ended | プロトタイピング、実験的ツール | 一貫性・安全性の保証が難しい |

## 周辺のプロトコル動向

「AI とフロントエンドの間の契約をどの抽象度で結ぶか」のプロトコル標準化が進行中。Google A2UI、AG-UI、MCP Apps などが並行して動いており、Dynamic パターンはこの文脈で「宣言的スペック」と「生 HTML」の間に**抽象化されたコード + サンドボックス実行**というポジションを置く提案として位置づけられる。

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — AI と UI の間の契約プロトコル
- [microVM](/blogs/wiki/concepts/microvm/) — Dynamic パターンに使える別の隔離基盤
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — UI を生成する AI の担い手

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
