---
title: "Cloudflare Dynamic Workers"
description: "Worker の中から実行時に与えたコードで新しい Worker を専用サンドボックス付きで動的生成する Cloudflare の API。V8 isolate ベースでミリ秒起動・省メモリが特徴"
date: 2026-07-25
lastmod: 2026-07-25
aliases: ["Dynamic Workers", "Worker Loader API", "Cloudflare Worker Loader"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare-workers", "sandbox", "generative-ui", "AI エージェント", "V8"]
---

## 概要

Cloudflare が 2026 年 3 月 24 日のブログ "Sandboxing AI agents, 100x faster"（Kenton Varda、Sunil Pai、Ketan Gupta 共著）で発表した仕組み。Worker の中から、実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的に生成できる** API（Worker Loader API）。現在オープンベータとして提供。

AI エージェントが生成したコードや、LLM が出力した UI コードを安全に実行する「サンドボックスとしての Cloudflare Edge」を実現する。

## 主な特徴

### 起動速度とメモリ効率

サンドボックスの実体はコンテナや VM ではなく **V8 isolate**。Cloudflare はミリ秒単位で起動し数メガバイトのメモリで動くと説明しており、典型的なコンテナと比較して約 100 倍高速・メモリ効率は 10〜100 倍とされる。

UI 生成のリクエストごとにサンドボックスを立てる [Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターンを現実的にする特性。

### 能力の最小化（Capability Restriction）

動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` を指定すれば `fetch()` などの外向き通信も遮断できる（デフォルトは親 Worker のネットワークアクセスを継承する点に注意）。

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null, // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

### Code Mode の系譜

Cloudflare は 2025 年 9 月に「AI エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶ方がよい」という **Code Mode** のコンセプトを提示。MCP サーバーを TypeScript API に変換してエージェントにコードを書かせると、従来のツール呼び出し方式と比べて複雑なタスクでトークン使用量を 81% 削減できたと報告している。Dynamic Workers は「エージェントが書いたコードをどこで安全に実行するか」への解答として位置づけられる。

## セキュリティモデル

V8 isolate の分離は専用カーネルを持つ [microVM](/blogs/wiki/concepts/microvm/)（Firecracker や libkrun）より壁が薄い。Cloudflare 自身も V8 の脆弱性がハイパーバイザーより高頻度で見つかることを認めており、V8 パッチの即日デプロイや二層目のサンドボックスなど多層防御で補う設計。

「どこまでの分離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。リクエストごとに UI コードを実行する Generative UI の文脈では isolate の軽さが効く。

## ユースケース

- **Generative UI の Dynamic パターン**: LLM が生成した JSX / React コードをサーバー側でサンドボックス実行し UI を返す
- **AI エージェントのコード実行**: エージェントが書いたスクリプトをサンドボックスで分離実行
- **プラグインシステム**: 信頼できないサードパーティコードを安全に実行する基盤

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic Workers を実行基盤にする UI 生成パターン
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要なケースの代替（Firecracker / libkrun）
- [microsandbox](/blogs/wiki/tools/microsandbox/) — self-hosted な microVM サンドボックス
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Dynamic Workers のコード実行ユースケース
- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — エージェントとツールを繋ぐプロトコル

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
