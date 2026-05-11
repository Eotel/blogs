---
title: "Agent Toolkit for AWS"
description: "AWS 公式の MCP Server / Skills / Plugins / Rules files を束ねたエージェント開発キット。AWS 業務の手順を SKILL.md 形式で提供する"
date: 2026-05-11
lastmod: 2026-05-11
aliases: ["agent-toolkit-for-aws", "AWS Agent Toolkit"]
related_posts:
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
tags: ["aws", "agent", "mcp", "skills", "toolkit"]
---

## 概要

AWS が公式に提供する、AI エージェントを AWS の上で開発・運用するためのツールキット。AWS API 呼び出し用の MCP Server、AWS 業務のための手順書 (`SKILL.md`)、各エージェント向けのプラグイン、AWS 利用方針の宣言ファイル (Rules files) を一式で提供する。

ランディングページは [aws.amazon.com/products/developer-tools/agent-toolkit-for-aws](https://aws.amazon.com/products/developer-tools/agent-toolkit-for-aws/)。

## 4 つの構成要素

| 要素 | 役割 |
|---|---|
| MCP Server | AWS API 呼び出しやドキュメント検索を MCP 経由で提供 |
| Skills | 特定タスク用の手順書セット（`SKILL.md` ベース） |
| Plugins | 各エージェント（Claude Code、Strands 等）向けのパッケージ |
| Rules files | AWS 利用方針の宣言ファイル |

## 並走する 2 つの公式リポジトリ

現時点で AWS 系列は 2 つのリポジトリが並走している。

### `aws/agent-toolkit-for-aws`

[`aws/agent-toolkit-for-aws`](https://github.com/aws/agent-toolkit-for-aws) は "Official, AWS-supported MCP servers, skills, and plugins" として最も上流に位置する。Skills の配置は以下の通り。

- `skills/core-skills/` — 13 カテゴリ（amazon-bedrock、aws-cdk、aws-cloudformation、aws-containers、aws-iam、aws-observability、aws-serverless 等）
- `skills/specialized-skills/` — 9 カテゴリ（analytics-skills、database-skills、ec2-skills、networking-and-content-delivery-skills、security-and-identity-skills 等）
- `plugins/aws-agents/skills/` — AI エージェント開発専用の平坦構成 7 個（agents-build、agents-connect、agents-debug、agents-deploy、agents-get-started、agents-harden、agents-optimize）

### `awslabs/agent-plugins`

[`awslabs/agent-plugins`](https://github.com/awslabs/agent-plugins) は AWS Labs 側で先行していたプラグイン群。amazon-location-service、aws-amplify、aws-serverless、deploy-on-aws、migration-to-aws、sagemaker-ai など「製品横断のシナリオ」寄りの Skills が並ぶ。

## Skills 単独でローカル取り込みする運用

MCP Server を立てずに Skills だけを Strands SDK の AgentSkills プラグインに直接渡せば、Bedrock AgentCore の CodeZip デプロイにそのまま乗せられる軽量構成になる。`git clone --filter=blob:none --sparse` で必要な subtree のみ持ってくれば zip サイズも抑えられる。

## 関連ページ

- [Strands Agents](/blogs/wiki/tools/strands-agents/) — Skills を読み込む側の SDK
- [Amazon Bedrock AgentCore](/blogs/wiki/tools/bedrock-agentcore/) — 主要なデプロイ先
- [Skills フォーマット](/blogs/wiki/concepts/agent-skills-format/) — `SKILL.md` 仕様の業界横断的な位置付け
- [MCP](/blogs/wiki/concepts/mcp/) — Toolkit が提供する MCP Server の基盤プロトコル

## ソース記事

- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
