---
title: "Cloudflare Dynamic Workers"
description: "Worker の中から実行時にコードを与えて新しい Worker を専用サンドボックス付きで動的生成できる Cloudflare の API。V8 isolate ベースでミリ秒起動・省メモリが特徴"
date: 2026-07-18
lastmod: 2026-07-18
aliases:
  - "Dynamic Workers"
  - "Worker Loader API"
  - "cloudflare worker loader"
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare-workers", "dynamic-workers", "サンドボックス", "V8", "frontend"]
---

## 概要

Cloudflare が 2026 年 3 月 24 日のブログ "Sandboxing AI agents, 100x faster"（Kenton Varda, Sunil Pai, Ketan Gupta）で発表した仕組み。Worker の中から、実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的に生成できる Worker Loader API** を提供する。現在オープンベータ。

## 基本的な使い方

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード文字列
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null,                // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

## 主な特徴

- **ミリ秒起動・省メモリ**: サンドボックスは V8 の isolate ベース。典型的なコンテナと比べて起動が約 100 倍高速、メモリ効率は 10〜100 倍。リクエストごとにサンドボックスを起動する使い方が現実的になる。
- **能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` で外向き通信（`fetch()` 等）を遮断できる（デフォルトは親 Worker のネットワークアクセスを継承する点に注意）。
- **Code Mode の系譜**: 2025 年 9 月に Cloudflare が提唱した「AI エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶほうがよい」という Code Mode コンセプトの実行基盤。MCP サーバーを TypeScript API に変換してコードを書かせると、従来のツール呼び出し比でトークン使用量を 81% 削減できたと報告されている。

## セキュリティ特性

V8 isolate の分離の壁は、専用カーネルを持つ [microVM](/blogs/wiki/concepts/microvm/) より薄い。Cloudflare は V8 パッチの即日デプロイや二層目のサンドボックスなど多層防御で補う設計を取る。「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。リクエストごとに UI コードを実行する [Generative UI](/blogs/wiki/concepts/generative-ui/) の文脈では isolate の軽さが効く。

## 主なユースケース

- **Generative UI の Dynamic パターン** — LLM が生成した JSX 等のコードをサンドボックスで動的実行して UI を返す（yusukebe 提案）
- **AI エージェントのコード実行** — エージェントが書いたコードを安全に実行する隔離環境

## microVM との比較

| 観点 | Dynamic Workers (V8 isolate) | microVM（libkrun 等） |
|---|---|---|
| 起動速度 | ミリ秒 | 100ms 前後〜 |
| メモリ | 数 MB | 数十〜数百 MB |
| 分離強度 | V8 の脆弱性リスクあり | 専用カーネルで強固 |
| 適用場面 | リクエストごとに UI 生成など高頻度 | 長時間エージェント実行など |

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic Workers を実行基盤とするパターン
- [microVM](/blogs/wiki/concepts/microvm/) — 代替の隔離実行手段（専用カーネル）
- [microsandbox](/blogs/wiki/tools/microsandbox/) — libkrun ベースの microVM サンドボックス

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
