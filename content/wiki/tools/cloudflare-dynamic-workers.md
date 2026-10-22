---
title: "Cloudflare Dynamic Workers"
description: "Worker の中から実行時に与えたコードで新しい Worker を専用サンドボックス付きで動的に生成できる Cloudflare の API。V8 isolate ベースでミリ秒起動・省メモリが特徴"
date: 2026-06-07
lastmod: 2026-06-07
aliases: ["Dynamic Workers", "Worker Loader API", "Cloudflare Worker Loader"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare", "cloudflare-workers", "sandboxing", "generative-ui", "V8 isolate"]
---

## 概要

Cloudflare が 2026 年 3 月 24 日のブログ "Sandboxing AI agents, 100x faster"（Kenton Varda、Sunil Pai、Ketan Gupta）で発表した機能（現在オープンベータ）。Worker の中から実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的に生成できる** API（Worker Loader binding）。

## 技術的特徴

- **V8 isolate ベース**: サンドボックスの実体はコンテナや VM ではなく V8 の isolate。ミリ秒単位で起動し、数メガバイトのメモリで動く。Cloudflare によれば典型的なコンテナ比で起動約 100 倍高速、メモリ効率 10〜100 倍
- **能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` を指定すればインターネットアクセスを遮断できる（デフォルトは親 Worker のネットワークアクセスを継承）
- **Code Mode の系譜**: 2025 年 9 月に Cloudflare が提示した「エージェントにコードを書かせてそのコードで API を呼ぶ方が、ツール呼び出しの連発より良い」という Code Mode コンセプトの実行基盤。MCP サーバーを TypeScript API に変換して複雑なタスクに適用すると、トークン使用量を最大 81% 削減できたと報告

## 使用例（擬似コード）

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード文字列
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null,               // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

## セキュリティモデルとトレードオフ

V8 の脆弱性はハイパーバイザーより高頻度で見つかる。isolate は専用カーネルを持つ [microVM](/blogs/wiki/concepts/microvm/) より分離の壁が薄い分、起動が桁違いに速い。Cloudflare は V8 パッチの即日デプロイや二層目のサンドボックスなど多層防御で補う設計を採用している。

| | V8 isolate (Dynamic Workers) | microVM (Firecracker / libkrun) |
|---|---|---|
| 起動時間 | ミリ秒単位 | ~100ms 前後 |
| メモリ効率 | 数 MB | ~数十 MB |
| 分離の強さ | 薄い（V8 の脆弱性が攻撃面） | 強い（専用カーネル、ハードウェア境界） |
| 向いているケース | リクエストごとに大量起動する UI 生成 | 長期実行・より強い保証が必要な AI コード実行 |

## Generative UI での用途

[Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターンの実行基盤として適している。LLM が生成した抽象化コード（JSX 等）を受け取り、リクエストごとにサンドボックスを立てて UI を実行して返す——という高頻度・短命なワークロードに isolate の軽さが効く。

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic パターンの全体像
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要な場合の比較対象
- [microsandbox](/blogs/wiki/tools/microsandbox/) — self-hosted な microVM サンドボックス
- [MCP（Model Context Protocol）](/blogs/wiki/concepts/mcp/) — Code Mode の起点となるプロトコル
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Dynamic Workers が提供するサンドボックスの主要利用者

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
