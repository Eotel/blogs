---
title: "Generative UI"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の 4 パターンで整理される"
date: 2026-06-20
lastmod: 2026-06-20
aliases: ["Generative UI", "ジェネレーティブUI", "generative-ui"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "フロントエンド", "LLM", "cloudflare-workers", "dynamic-workers"]
---

## 概要

LLM の出力に応じて UI を動的に組み立てるアプローチ。「AI が UI を生成する」とも表現される。実装パターンは制御と自由度のスペクトラムとして 4 つに分類される。Hono 作者 yusukebe が 2026 年 6 月の発表「AI時代のUIはどこへ行く？その2！」で整理・提案したフレームワーク。

## 4 つの実装パターン

| パターン | LLM が返すもの | 自由度 | 向いているケース |
|---|---|---|---|
| **Static** | データ（値） | 低 | ミッションクリティカルな業務 UI、一貫した UX が必須の本番アプリ |
| **Declarative** | 構造を表す宣言的スペック（JSON 等） | 中 | 動的ダッシュボード、フォーム生成、マルチプラットフォーム描画 |
| **Dynamic** | 抽象化されたコード（JSX 等） | 中〜高 | 複雑なロジック・インタラクションを AI に組ませたいとき |
| **Open-ended** | HTML/CSS/JavaScript そのもの | 高 | プロトタイピング、実験的なツール |

CopilotKit の "The Three Types of Generative UI"（Static / Declarative / Open-ended）にコミュニティで共通理解が形成されていたところに、yusukebe が **Dynamic パターン**を第 4 の選択肢として提案した。

## Dynamic パターンの詳細

Declarative の「構造化されているが表現力に上限がある」と Open-ended の「自由だが制御不能」の中間を狙う。

1. LLM に生の HTML/CSS/JavaScript を丸ごと書かせるのではなく、JSX のような**抽象化されたコード**を書かせる
2. 生成されたコードを**サーバー側のサンドボックスで動的にロードして実行**し、結果を UI として返す
3. 実行基盤には Cloudflare の **Dynamic Workers**（Worker Loader API）を使う

フレームワークの抽象とサンドボックスの二重の枠に収めることで、Open-ended の「野放し」を避けつつ表現力を確保する。

## Cloudflare Dynamic Workers

Dynamic パターンの実行基盤。Worker の中から実行時に与えたコードで新しい Worker を専用サンドボックス付きで動的に生成できる API。2026 年 3 月 24 日のブログ「Sandboxing AI agents, 100x faster」（Kenton Varda 他共著）で発表、オープンベータ提供中。

特徴:
- **V8 isolate ベース**: コンテナや VM ではなく V8 の isolate が実行単位。ミリ秒起動・数 MB メモリ（典型的なコンテナ比で約 100 倍高速、メモリ効率 10〜100 倍）
- **能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` でインターネットアクセスを遮断可能（デフォルトは親 Worker のネットワークアクセスを継承する点に注意）
- **Code Mode の系譜**: Cloudflare が 2025 年 9 月に提示した「エージェントにコードを書かせる」コンセプトの延長。従来のツール呼び出し方式と比べて複雑タスクでトークン使用量を 81% 削減できると報告

## 実行基盤の隔離強度トレードオフ

AI が生成した untrusted code の実行基盤を選ぶ主なトレードオフ:

| 実行基盤 | 隔離の強さ | 起動速度 | 向いている用途 |
|---|---|---|---|
| V8 isolate（Dynamic Workers 等） | 中（V8 脆弱性リスクあり、多層防御で補う） | ミリ秒 | リクエストごとに UI コードを実行する Generative UI |
| [microVM](/blogs/wiki/concepts/microvm/)（Firecracker, libkrun 等） | 強（専用カーネル、ハードウェア分離） | 〜100ms | 長時間実行・高セキュリティ要件の AI エージェント |

「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。

## 周辺の動き

Generative UI の周辺ではプロトコルの標準化も同時並行で進んでいる。Google A2UI、AG-UI、MCP Apps といった「AI とフロントエンドの間の契約をどの抽象度で結ぶか」をめぐる規格が動いており、Dynamic パターンはその契約を「宣言的スペック」と「生 HTML」の間にある「抽象化されたコード + サンドボックス実行」に置く提案として位置づけられる。

## 関連ページ

- [MCP](/blogs/wiki/concepts/mcp/) — エージェントと外部ツールの接続プロトコル。MCP Apps が Generative UI 標準化の一候補
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要な場合の代替実行基盤
- [microsandbox](/blogs/wiki/tools/microsandbox/) — microVM ベースの self-hosted サンドボックス（V8 isolate の代替）
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Generative UI の主な利用主体

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
