---
title: "Generative UI（生成 UI）"
description: "LLM の出力に応じて UI を動的に組み立てるアプローチ。Static / Declarative / Dynamic / Open-ended の 4 パターンのスペクトラムで整理できる"
date: 2026-06-07
lastmod: 2026-06-07
aliases: ["Generative UI", "生成 UI", "Dynamic パターン", "generative-ui"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["generative-ui", "LLM", "frontend", "cloudflare-workers"]
---

## 概要

LLM の出力に応じて UI を動的に組み立てるアプローチの総称。「AI が UI を生成する」パターンで、実装の自由度によって 4 つのスペクトラムに整理できる（CopilotKit による分類 + yusukebe が提案した Dynamic パターン）。

右に行くほど AI の自由度が上がり、開発者の制御が下がる。

## 4 パターンのスペクトラム

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義コンポーネント） | 低 |
| **Declarative** | UI の宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Dynamic** | 抽象化されたコード（JSX 等）+ サーバーサイドサンドボックス | サーバー（LLM コード + 実行基盤） | 中〜高 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホスト側はサンドボックスを提供するだけ） | 高 |

## Static パターン

LLM が返した値を事前定義されたコンポーネントに当てはめる。本番アプリで最も安全で扱いやすい。表示は完全に開発者の管理下にある。

## Declarative パターン

LLM に「カード」「リスト」「フォーム」のような構造を JSON などで宣言させ、フロントエンドが自前のコンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る。マルチプラットフォーム描画に強い。

## Dynamic パターン（第 4 の提案）

Hono 作者 yusukebe（和田裕介）が 2026 年 6 月のフロントエンド・PHPカンファレンス北海道 2026 で提案した第 4 のパターン。

アイデアの骨子:
1. LLM に生の HTML/CSS/JavaScript ではなく、**抽象化されたコード**（React/JSX 等）を書かせる
2. 生成されたコードを**サーバー側のサンドボックスで動的にロードして実行**し、結果を UI として返す
3. 実行基盤には [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/)（Worker Loader API）を使う

Declarative の「構造化されているが表現力に上限がある」と Open-ended の「自由だが制御不能」の間を取るポジション。宣言的スペックでは表現できないロジックやインタラクションをコードとして書かせつつ、フレームワークの抽象とサンドボックスの境界という二重の枠に収める。

## Open-ended パターン

LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe 内で実行する。AI の表現力は最大になるが、一貫性・安全性・アクセシビリティの保証が難しい。プロトタイピングや実験的ツール向け。

## 使い分けの指針

| パターン | 向いているケース |
|---|---|
| Static | ミッションクリティカルな業務 UI、一貫した UX が必須 |
| Declarative | 動的ダッシュボード、フォーム生成、マルチプラットフォーム描画 |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたいとき |
| Open-ended | プロトタイピング、実験的なツール |

## 周辺の標準化動向（2026 年時点）

Google A2UI、AG-UI、MCP Apps など「AI とフロントエンドの間の契約をどの抽象度で結ぶか」のプロトコル標準化が同時並行で進んでいる。Dynamic パターンはその契約を「宣言的スペック」と「生 HTML」の間に位置する「抽象化されたコード＋サンドボックス実行」に置く提案として注目される。

## 関連ページ

- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — Dynamic パターンの実行基盤
- [MCP（Model Context Protocol）](/blogs/wiki/concepts/mcp/) — AI とフロントエンドをつなぐプロトコル標準化の流れ
- [microVM](/blogs/wiki/concepts/microvm/) — より強い隔離が必要な場合の比較対象（isolate vs microVM のトレードオフ）
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — UI を受け取り・生成するエージェント

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
