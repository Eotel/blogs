---
title: "Generative UI パターン"
description: "LLM の出力に応じて UI を動的に組み立てる Generative UI の 4 実装パターン（Static / Declarative / Dynamic / Open-ended）と、Cloudflare Dynamic Workers を使った Dynamic パターンの技術基盤。"
date: 2026-07-04
lastmod: 2026-07-04
aliases: ["Generative UI", "Dynamic パターン", "AI UI", "generative-ui"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "cloudflare-workers", "llm", "frontend"]
---

## 概要

**Generative UI** は、LLM の出力に応じて UI を動的に組み立てるアプローチの総称。2026 年時点で 3 + 1 のパターンがコミュニティで共通理解になりつつある。CopilotKit の "The Three Types of Generative UI" が基本の 3 分類を整理し、Hono 作者の yusukebe（和田裕介）がフロントエンド・PHPカンファレンス北海道2026 の発表「AI時代のUIはどこへ行く？その2！」で第 4 の Dynamic パターンを提案した。

## 4 実装パターン

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義コンポーネント） | 低 |
| **Declarative** | UI 構造を表す宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等）| サーバーサイドサンドボックス | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホスト側はサンドボックス提供のみ） | 最高 |

右に行くほど AI の自由度が上がり、開発者の制御が下がるスペクトラムを形成する。

### Static

LLM が返した値を事前定義の UI コンポーネントに当てはめる。表示は開発者の完全管理下。ミッションクリティカルな業務 UI や一貫した UX が必須の本番アプリに適する。

### Declarative

LLM に「カード」「リスト」「フォーム」のような構造を JSON 等で宣言させ、フロントエンドが自前コンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。スペックの表現力が上限になる。

### Dynamic（第 4 の提案）

LLM に生の HTML ではなく、より抽象化されたコード（React/JSX 等のコンポーネントコード）を書かせ、**サーバー側のサンドボックスで動的ロード・実行**して結果を UI として返す。Declarative の制御と Open-ended の自由のいいとこ取りを狙う。

実行基盤として **Cloudflare Dynamic Workers**（Worker Loader API）を使う。V8 isolate ベースでミリ秒起動・省メモリが売りで、リクエストごとにサンドボックスを立てて UI を生成する使い方が現実的になる。

### Open-ended

LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe 内で実行する。表現力は最大だが、一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピングや実験的ツール向け。

## Cloudflare Dynamic Workers

Dynamic パターンの実行基盤。2026 年 3 月 Cloudflare がブログ "Sandboxing AI agents, 100x faster" で発表、現在オープンベータ。Worker の中から実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的生成**できる API。

主な特徴：

- **起動速度**: V8 isolate ベースでミリ秒単位起動、数 MB のメモリ（典型的なコンテナ比約 100 倍高速）
- **能力の最小化**: `env` で明示的に渡したバインディングしか動的 Worker から見えない。`globalOutbound: null` で外向き通信も遮断可能
- **Code Mode の系譜**: Cloudflare が 2025 年 9 月に提唱した「エージェントにツール呼び出しを連発させるよりコードを書かせる方がよい」というアプローチ（複雑なタスクでトークン使用量 81% 削減を報告）の実行基盤

隔離の強さは microVM（専用カーネルを持つ）よりも V8 isolate の方が薄いが、桁違いに軽い。「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。

## 関連プロトコル・標準

Generative UI 周辺では標準化も並走している：Google A2UI、AG-UI、MCP Apps。「AI とフロントエンドの間の契約をどの抽象度で結ぶか」は現在進行中の論点。

## ユースケース別の選択指針

| パターン | 向いているケース |
|---|---|
| Static | 本番業務アプリ、一貫 UX 必須 |
| Declarative | 動的ダッシュボード、フォーム生成、マルチプラットフォーム |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたい |
| Open-ended | プロトタイピング、実験的ツール |

## 関連ページ

- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — AI とフロントエンド間の契約プロトコル
- [microVM](/blogs/wiki/concepts/microvm/) — 隔離の代替手段（より強固だが重い）
- [microsandbox](/blogs/wiki/tools/microsandbox/) — microVM ベースの AI コード実行サンドボックス
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — UI を生成する側

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
