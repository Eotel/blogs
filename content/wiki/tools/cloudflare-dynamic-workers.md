---
title: "Cloudflare Dynamic Workers"
description: "Worker の中から実行時に与えたコードで新しい Worker を専用 V8 isolate サンドボックス付きで動的生成できる Cloudflare の API。ミリ秒起動・省メモリで AI 生成コードの安全な実行基盤になる"
date: 2026-08-01
lastmod: 2026-08-01
aliases: ["Dynamic Workers", "Worker Loader API", "cloudflare-dynamic-workers"]
related_posts:
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["cloudflare-workers", "dynamic-workers", "AIエージェント", "サンドボックス"]
---

## 概要

Cloudflare が 2026 年 3 月 24 日のブログ「Sandboxing AI agents, 100x faster」（Kenton Varda・Sunil Pai・Ketan Gupta 共著）で発表したサンドボックス機能。Worker の中から、実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的に生成**できる Worker Loader API。現在オープンベータ。

## 仕組み

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null,                // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

`env.LOADER` が Worker Loader binding、`agentCode` は LLM が生成したコード文字列。

## 主な特性

- **ミリ秒起動**: サンドボックスの実体はコンテナや VM ではなく V8 isolate。典型的なコンテナ比で約 100 倍高速、メモリ効率は 10〜100 倍（Cloudflare 発表値）。リクエストごとにサンドボックスを立てる使い方が現実的になる
- **能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` で外向き通信を遮断できる（デフォルトは親 Worker のネットワークアクセスを継承する点に注意）
- **Code Mode の系譜**: Cloudflare が 2025 年 9 月に提唱した「エージェントはツール呼び出しより、コードを書いて API を呼ぶ方がよい」という Code Mode のコンセプトの延長。MCP サーバーを TypeScript API に変換させてコードを書かせた場合、従来のツール呼び出し方式と比べてトークン使用量を最大 81% 削減できたと報告されている

## microVM との比較

AI が生成した untrusted code の実行基盤としては [microVM](/blogs/wiki/concepts/microvm/)（[microsandbox](/blogs/wiki/tools/microsandbox/)・E2B 等）も選択肢だが、分離の強さと起動コストにはトレードオフがある。

| | Cloudflare Dynamic Workers | microVM（Firecracker / libkrun） |
|---|---|---|
| 分離の実体 | V8 isolate | 専用カーネル（ハードウェア仮想化） |
| 起動速度 | ミリ秒 | 数十〜100ms 程度 |
| 分離の強さ | V8 脆弱性の影響を受けうる（多層防御で補う） | コンテナ脱出・カーネルエクスプロイトに対して一段厚い壁 |
| 前提インフラ | Cloudflare Workers エコシステム | KVM 対応 Linux / Apple Silicon |

リクエストごとに UI コードを実行する Generative UI の文脈では isolate の軽さが効く。「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ。

Cloudflare 自身も V8 の脆弱性がハイパーバイザーより高頻度で見つかることを認めた上で、V8 パッチの即日デプロイや二層目のサンドボックスなど多層防御で補う設計を取っている。

## 活用パターン

### Generative UI（Dynamic パターン）

[Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターンで実行基盤として使われる。LLM が生成した JSX 等のコードをリクエストごとにサンドボックスで実行し、UI として返す。

### AI エージェントのコード実行

エージェントが生成した untrusted code を、ホストから隔離した環境で実行する。外向きネットワーク制御と能力の最小化でサンドボックスの脱出リスクを低減する。

## 関連ページ

- [Generative UI](/blogs/wiki/concepts/generative-ui/) — Dynamic Workers を実行基盤とする Dynamic パターンを含む Generative UI の全体像
- [microVM](/blogs/wiki/concepts/microvm/) — より強い分離が必要な場合の代替実行基盤
- [microsandbox](/blogs/wiki/tools/microsandbox/) — libkrun ベースの self-hosted microVM サンドボックス
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — untrusted code 実行が課題になるシステム

## ソース記事

- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
