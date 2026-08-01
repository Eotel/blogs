---
title: "microVM"
description: "専用カーネルを持つ軽量仮想マシン。コンテナの共有カーネルより強い分離を、VM より速い起動で実現する"
date: 2026-05-25
lastmod: 2026-05-25
aliases: ["micro-VM", "マイクロVM", "microVM"]
related_posts:
  - "/posts/2026/05/2026-05-25-microsandbox-microvm-isolation-for-ai-agents/"
  - "/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/"
tags: ["microvm", "セキュリティ", "仮想化", "サンドボックス"]
---

## 概要

各インスタンスが**自分専用の Linux カーネル**を持つ軽量な仮想マシン。ホストとの境界は namespace ではなく CPU のハードウェア仮想化機能（Linux なら KVM）で引かれる。フル仮想化のオーバーヘッドを削ぎ落とし、コンテナに近い起動速度（ものによっては 100ms 前後）と VM 並みの分離を両立させる発想。

## コンテナとの違い

| | コンテナ（Docker 等） | microVM |
|---|---|---|
| カーネル | ホストと**共有** | インスタンスごとに**専用** |
| 境界 | namespace / cgroup | ハードウェア仮想化（KVM） |
| 攻撃面 | コンテナ脱出・カーネルエクスプロイトの余地 | 一段厚い壁 |
| 起動 | 速い | 専用カーネルゆえ本来は遅いが、microVM は最適化で高速化 |

共有カーネルは、カーネルに脆弱性があるとコンテナの壁を越えてホストや他コンテナへ侵入されうる。untrusted code（AI エージェントが生成したコード等）を実行する文脈では、この共有カーネルが無視できない攻撃面になる。

## 代表的な実装

- **Firecracker** — AWS が公開した microVM。AWS Lambda / Fargate を支える。E2B などのクラウドサンドボックスが採用
- **libkrun** — 軽量な仮想化ランタイム。[microsandbox](/blogs/wiki/tools/microsandbox/) が採用

## AI エージェントのコード実行サンドボックスでの位置づけ

2026 年時点、AI エージェントに untrusted code を実行させる用途で microVM ベースのサンドボックスが増えている。代表的な選択肢の隔離技術とホスティング:

| ツール | 隔離技術 | ホスティング |
|---|---|---|
| [microsandbox](/blogs/wiki/tools/microsandbox/) | libkrun の microVM | self-hosted / embeddable |
| E2B | Firecracker の microVM | マネージドクラウド |
| Daytona | Docker コンテナ | マネージド / セルフ |

「コードを外部に出せない」なら self-host できる microVM、「インフラを管理したくない」ならマネージド型、「状態を持ち越したい」ならコンテナ型、と用途で選ぶ。

## V8 isolate との比較

[Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) が AI コード実行に V8 isolate を採用しているように、分離の強さと起動コストにはトレードオフがある。

| | V8 isolate（Dynamic Workers 等） | microVM（Firecracker / libkrun） |
|---|---|---|
| 分離の実体 | V8 プロセス内隔離 | 専用カーネル（ハードウェア仮想化） |
| 起動速度 | ミリ秒 | 数十〜100ms 程度 |
| 分離の強さ | V8 脆弱性の影響を受けうる | コンテナ脱出・カーネルエクスプロイトに対して一段厚い壁 |

リクエストごとに UI コードを実行する [Generative UI](/blogs/wiki/concepts/generative-ui/) の Dynamic パターンでは isolate の軽さが効く。セキュリティ要件が高い untrusted code の実行では microVM が選ばれる。

## 関連ページ

- [microsandbox](/blogs/wiki/tools/microsandbox/) — libkrun の microVM を使う self-hosted サンドボックス
- [Cloudflare Dynamic Workers](/blogs/wiki/tools/cloudflare-dynamic-workers/) — V8 isolate ベースの軽量サンドボックス（比較対象）
- [Generative UI](/blogs/wiki/concepts/generative-ui/) — AI コード実行基盤として microVM / isolate を比較する文脈
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — microVM サンドボックスの主要ユースケース
- [プロンプトインジェクション](/blogs/wiki/concepts/prompt-injection/) — サンドボックスが実効的防御になる攻撃

## ソース記事

- [microsandbox の仕組み — libkrun の microVM で AI エージェントのコードを隔離実行する](/blogs/posts/2026/05/2026-05-25-microsandbox-microvm-isolation-for-ai-agents/) — 2026-05-25
- [Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン](/blogs/posts/2026/06/2026-06-07-generative-ui-dynamic-pattern/) — 2026-06-07
