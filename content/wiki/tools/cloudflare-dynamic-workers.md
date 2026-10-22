---
title: "Cloudflare Dynamic Workers"
description: "V8 isolate ベースでリクエストごとに新 Worker を動的生成できる Cloudflare の実行基盤。AI が生成したコードをミリ秒起動のサンドボックスで安全に実行する（2026 年 3 月 オープンベータ）"
date: 2026-06-13
lastmod: 2026-06-13
aliases: ["Dynamic Workers", "Worker Loader API", "Worker Loader binding"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare-workers", "dynamic-workers", "AIエージェント", "sandboxing", "V8"]
---

## 概要

Cloudflare Dynamic Workers は、Worker の中から実行時に与えたコード文字列で**新しい Worker を専用 V8 isolate サンドボックス付きで動的生成できる** API（Worker Loader binding）。2026 年 3 月 24 日の Cloudflare ブログ "Sandboxing AI agents, 100x faster"（Kenton Varda、Sunil Pai、Ketan Gupta 共著）で発表され、オープンベータ提供中。[Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターンや AI エージェントが生成したコードを安全に実行するための基盤として設計されている。

## 主要な特性

- **ミリ秒起動** — サンドボックスの実体はコンテナや VM ではなく V8 isolate。典型的なコンテナ比で約 100 倍高速に起動し、メモリ効率は 10〜100 倍
- **能力の最小化** — 動的 Worker に渡せる API は `env` で明示したバインディングのみ。`globalOutbound: null` でインターネット外向き通信も遮断可能
- **Code Mode の系譜** — 2025 年 9 月に Cloudflare が「AI エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶ方が良い」という Code Mode コンセプトを提唱。MCP サーバーを TypeScript API に変換してコードを書かせると、ツール呼び出し方式比でトークン使用量を 81% 削減できたと報告。Dynamic Workers はその「AI が書いたコードをどこで安全に実行するか」への解答

## 擬似コード例

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: { "agent.js": agentCode }, // LLM が生成したコード
  env: { CHAT_ROOM: chatRoomRpcStub }, // 必要な API だけ注入
  globalOutbound: null,               // 外向き通信を遮断
});
await worker.getEntrypoint().myAgent(param);
```

## isolate vs microVM のトレードオフ

AI 生成コードの実行基盤として [microVM](/blogs/wiki/concepts/microvm/)（[microsandbox](/blogs/wiki/tools/microsandbox/)、E2B 等）も存在する。isolate は専用カーネルを持つ microVM より分離の壁が薄い分、桁違いに軽い。Cloudflare は V8 脆弱性の高頻度パッチ適用と二層目サンドボックスで補う多層防御を採用している。

| 基盤 | 分離の強さ | 起動速度 | メモリ効率 |
|---|---|---|---|
| V8 isolate（Dynamic Workers） | 中 | ミリ秒 | 高 |
| microVM（microsandbox 等） | 高 | 遅い | 低〜中 |

「どこまでの隔離が必要か」vs「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。リクエストごとに UI コードを実行する Generative UI の文脈では isolate の軽さが効く。

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic Workers を使った Dynamic パターン
- [microVM](/blogs/wiki/concepts/microvm/) — より強い隔離が必要な場合の選択肢
- [microsandbox](/blogs/wiki/tools/microsandbox/) — libkrun ベースの microVM 実装
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 動的コード実行が必要になるユースケース

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
