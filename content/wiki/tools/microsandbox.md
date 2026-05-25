---
title: "microsandbox"
description: "libkrun ベースの microVM で AI エージェントの untrusted code を隔離実行する self-hosted な OSS サンドボックス"
date: 2026-05-25
lastmod: 2026-05-26
aliases: ["microsandbox", "msb"]
related_posts:
  - "/posts/2026/05/2026-05-25-microsandbox-microvm-isolation-for-ai-agents/"
tags: ["microsandbox", "microvm", "libkrun", "AI エージェント", "セキュリティ"]
---

## 概要

AI エージェントが生成した untrusted code を安全かつ高速に実行するための、[microVM](/blogs/wiki/concepts/microvm/) ベースのサンドボックス。libkrun を採用し、各サンドボックスに専用カーネルを与えてハードウェアレベルの分離を行う。クラウドサービスへコードを送らず自分のインフラで完結する self-hosted / embeddable な設計で、Apache License 2.0 の OSS（Y Combinator バッキング）。執筆時点 v0.4.6（2026-05-13）で beta。

## 主な特徴

- **ハードウェア分離**: microVM 技術で各サンドボックスが専用カーネルを持つ。共有カーネルのコンテナより攻撃面（コンテナ脱出・カーネルエクスプロイト）が狭い
- **高速起動**: 平均起動時間 100 ミリ秒未満（"Average boot times under 100 milliseconds."）
- **embeddable / daemon 不要**: 常駐サーバや daemon を立てず、アプリのコードから SDK 経由で microVM を直接起動する（"No server to set up. No lingering daemon. It is all embedded and rootless!"）
- **OCI 互換**: Docker Hub / GHCR などの標準コンテナイメージをそのまま起動できる
- **シークレットが漏れない**: 後述の通り、本物のクレデンシャルを VM の外に置く
- **エージェント連携**: MCP サーバと Agent Skills でエージェントが自分でサンドボックスを起動できる

## アーキテクチャ

仮想化ランタイムに **libkrun**、ネットワークスタックに Rust 製ユーザー空間 TCP/IP スタックの **smoltcp** を用いる（README が謝辞で両者に言及。smoltcp は Cargo 依存、libkrun はシステムライブラリ依存）。フル仮想化のオーバーヘッドを抑えつつ KVM によるハードウェア分離を提供し、ネットワークの出入りをホスト側で握ることが、下記のシークレット注入の制御点になっている。

要件は「Linux with KVM enabled, or macOS with Apple Silicon」。

## シークレットをネットワーク層で守る

microsandbox の最大の差別化点。本物のクレデンシャルはホスト側に置き、VM 内のプロセスにはプレースホルダだけを渡す。VM が**承認済みの TLS 宛先**に通信するときに限り、ホスト側で本物の値を差し込む（公式は「シークレットは VM に入らず、承認済みの宛先にのみ供給される」と説明）。

このため、VM 内の悪意あるコードが環境変数を読んでも本物の鍵はなく、許可外の宛先（攻撃者のサーバ等）へ送り出そうとしても注入対象外で持ち出し（exfiltration）が成立しない。[プロンプトインジェクション](/blogs/wiki/concepts/prompt-injection/)でエージェントが乗っ取られた場合のシークレット流出を構造的に防ぐ実行レイヤの対策にあたる。

## 使い方（最小）

```sh
# ワンショット実行
npx microsandbox run debian

# 名前付きサンドボックスの作成・実行・一覧・統計
msb create --name my-app python
msb exec my-app -- python -c "import this"
msb ls
msb metrics my-app
```

SDK は Rust / Python / TypeScript / Go 向けに提供（`cargo add microsandbox` / `uv add microsandbox` / `npm i microsandbox` / `go get github.com/superradcompany/microsandbox/sdk/go`）。MCP 連携は `claude mcp add --transport stdio microsandbox -- npx -y microsandbox-mcp`。

## 他サンドボックスとの位置づけ

self-host したいチーム向けのオープンソース選択肢。マネージドクラウド型の E2B（Firecracker ベース）や Docker コンテナ型の Daytona と異なり、コードを外部に出さず自社インフラで完結する点が強み。ただし beta であり、フル機能の開発環境ではなく実行コアにフォーカスしている。詳しい比較軸は [microVM](/blogs/wiki/concepts/microvm/) を参照。

## 関連ページ

- [microVM](/blogs/wiki/concepts/microvm/) — microsandbox が採用する隔離技術の概念
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — untrusted code 実行が課題になるシステム
- [プロンプトインジェクション](/blogs/wiki/concepts/prompt-injection/) — シークレット注入が防ぐ攻撃
- [AI エージェント時代のシークレット管理](/blogs/wiki/guides/ai-agent-secret-management/) — 供給側の対策と補完関係
- [MCP](/blogs/wiki/concepts/mcp/) — エージェントから microsandbox を呼ぶプロトコル

## ソース記事

- [microsandbox の仕組み — libkrun の microVM で AI エージェントのコードを隔離実行する](/blogs/posts/2026/05/2026-05-25-microsandbox-microvm-isolation-for-ai-agents/) — 2026-05-25
