---
title: "Cloudflare Dynamic Workers"
description: "Worker 内から実行時に与えたコードで新しい Worker を専用サンドボックス付きで動的生成できる Cloudflare の API。V8 isolate ベースでミリ秒起動・省メモリが特徴"
date: 2026-06-27
lastmod: 2026-06-27
aliases: ["Dynamic Workers", "Worker Loader API", "Cloudflare Worker Loader"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare-workers", "dynamic-workers", "サンドボックス", "AIエージェント", "frontend"]
---

## 概要

**Cloudflare Dynamic Workers** は、Worker の中から実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的生成できる** API（Worker Loader binding）。2026 年 3 月 24 日の Cloudflare ブログ「Sandboxing AI agents, 100x faster」（Kenton Varda、Sunil Pai、Ketan Gupta 共著）で発表され、オープンベータとして提供されている。

AI が生成した untrusted コードをその場でサンドボックス実行する用途に設計されており、[Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターン実行基盤として注目されている。

## 基本的な使い方

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード文字列
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null, // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

`env.LOADER` は Worker Loader binding。`agentCode` は LLM が生成したコード文字列を渡す。

## 設計の 3 つのポイント

**起動の速さ**: サンドボックスの実体は V8 isolate。コンテナや VM と異なりミリ秒単位で起動し、数メガバイトのメモリで動く。Cloudflare は「典型的なコンテナ比で約 100 倍高速、メモリ効率は 10〜100 倍」と説明する。リクエストごとにサンドボックスを立てる使い方が現実的になる。

**能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` を指定すれば外向き通信（`fetch()` 等）を遮断できる。デフォルトは親 Worker のネットワークアクセスを継承する点に注意。

**Code Mode の系譜**: Cloudflare は 2025 年 9 月に [Code Mode](https://blog.cloudflare.com/code-mode/) のコンセプト（エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶ方がよい）を提示し、MCP サーバーを TypeScript API に変換してコードを書かせると、ツール呼び出し方式比でトークン使用量 81% 削減を報告した。Dynamic Workers は「エージェントが書いたコードをどこで安全に実行するか」への解答。

## microVM との比較

AI 生成コードの実行基盤としては [microsandbox](/blogs/wiki/tools/microsandbox/) や E2B のような [microVM](/blogs/wiki/concepts/microvm/) ベースの選択肢もある。

| | V8 isolate (Dynamic Workers) | microVM (microsandbox 等) |
|---|---|---|
| 起動速度 | ミリ秒 | 数百 ms〜（専用カーネル起動） |
| メモリ | 数 MB | 数十〜数百 MB |
| 分離の強さ | V8 境界（ハイパーバイザーより薄い） | ハードウェア仮想化（KVM 等） |
| 脆弱性頻度 | V8 バグの頻度はハイパーバイザーより高い | 実績ある隔離モデル |

「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。リクエストごとに UI コードを実行する Generative UI の文脈では isolate の軽さが効く。Cloudflare は V8 パッチの即日デプロイと二層目サンドボックスによる多層防御で対応している。

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic Workers を実行基盤に使う Dynamic パターン
- [microVM](/blogs/wiki/concepts/microvm/) — ハードウェア仮想化による強い分離の代替
- [microsandbox](/blogs/wiki/tools/microsandbox/) — libkrun 製の microVM サンドボックス
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 信頼できないコードを動的実行するユースケース

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
