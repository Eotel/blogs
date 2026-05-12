---
title: "Amazon Bedrock AgentCore"
description: "本番運用向けの AWS マネージドエージェント基盤。CodeZip による直接コードデプロイで Strands 等の任意フレームワークを動かせる"
date: 2026-05-11
lastmod: 2026-05-12
aliases: ["Bedrock AgentCore", "AgentCore", "AgentCore Runtime"]
related_posts:
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
tags: ["aws", "bedrock", "agent", "runtime", "deployment"]
---

## 概要

Amazon Bedrock の上で、AI エージェントを本番運用するためのマネージド基盤。スケーラビリティ・信頼性・セキュリティを AWS 側が引き受け、開発者はエージェントのコード・依存関係を持ち込むだけで稼働させられる。ランディングは [aws.amazon.com/bedrock/agentcore](https://aws.amazon.com/bedrock/agentcore/)。

## Direct Code Deployment（CodeZip）

AgentCore Runtime のデプロイモードの 1 つで、エージェントコードと依存関係を `.zip` で固めて S3 にアップロードするだけで稼働する。コンテナイメージのビルドや管理が不要で、後続のアップデートも高速。セッション作成レート 25 sessions/sec まで耐える。

| マネージドランタイム | サポート開始 |
|---|---|
| Python | 2025 年 11 月 4 日（GA） |
| Node.js | [2026 年 4 月 28 日](https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-bedrock-agentcore-runtime/) |

Strands Agents や Claude Agent SDK など任意のフレームワークで書かれたエージェントを CodeZip でそのまま乗せられる。TypeScript のコードは JS に事前コンパイルする必要がある。

## Skills との相性

CodeZip 構成は、Skills を別プロセス（MCP Server）として持たずファイルシステムから直接読み込むスタイルと相性が良い。MCP Server を立てるとコンテナ化が必要になり CodeZip の利点が失われるため、Skills だけをローカルロードして AgentCore 上で動かす運用パターンが定石になりつつある。

## エージェント Inspector

`agentcore dev` コマンドで起動する **Web UI**（agent inspector）が同梱されており、デプロイ済みのエージェントに対するチャットボット形式の検証が可能。CLI 自身ではなくブラウザで開く Python venv ベースの開発用 UI で、Skills を入れる前後での回答品質の差分を直接見られる。

## 関連ページ

- [Strands Agents](/blogs/wiki/tools/strands-agents/) — AgentCore 上で動かす代表的な SDK
- [Agent Toolkit for AWS](/blogs/wiki/tools/agent-toolkit-for-aws/) — AgentCore 上のエージェントへ食わせる Skills の供給源
- [Skills フォーマット](/blogs/wiki/concepts/agent-skills-format/) — 互換層としての `SKILL.md`
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — マネージドクラウド型基盤の一例

## ソース記事

- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
