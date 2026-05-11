---
title: "Strands Agents"
description: "AWS が 2025 年に OSS 公開したモデル駆動型の AI エージェント SDK。Python と TypeScript を提供し、Bedrock AgentCore 等への本番デプロイに対応する"
date: 2026-05-11
lastmod: 2026-05-11
aliases: ["Strands Agents SDK", "strands-agents"]
related_posts:
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
tags: ["aws", "agent", "sdk", "open-source", "bedrock"]
---

## 概要

AWS が 2025 年 5 月に OSS で公開したモデル駆動型の AI エージェント SDK。`@tool` デコレータで Python 関数をそのままツール化でき、数行のコードでエージェントを構築できる。Python と TypeScript の両言語に対応し、Bedrock AgentCore、Lambda、Fargate、EKS、Docker、Kubernetes など主要なデプロイ先に持っていける。

公式リポジトリは [`strands-agents/sdk-python`](https://github.com/strands-agents/sdk-python)、ドキュメントは [strandsagents.com](https://strandsagents.com/)。Amazon Q Developer、AWS Glue、VPC Reachability Analyzer など AWS 内の本番エージェントが既に Strands で動いている。

## 主要機能

| 機能 | 内容 |
|------|------|
| モデル抽象 | Amazon Bedrock / Anthropic / OpenAI / Gemini / Ollama / LiteLLM / llama.cpp などを 1 行で切替 |
| ツール | `@tool` デコレータで任意の Python 関数をツール化。組み込みの 20 種類超のサンプルツールも同梱 |
| MCP 互換 | 任意の MCP サーバーをそのままツールとして接続可能 |
| マルチエージェント | Swarm / Graph / Workflow パターンを標準で提供 |
| 可観測性 | OpenTelemetry を組み込みでサポート |

## AgentSkills プラグイン

Strands SDK には [`strands.vended_plugins.skills.AgentSkills`](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.agent_skills/) という Skills 読み込みプラグインが標準で含まれている。Anthropic の Agent Skills 仕様に準拠し、起動時はスキルの name / description だけをシステムプロンプトに XML ブロックとして注入し、エージェントが必要だと判断したときに本体を専用ツール経由でロードする — プログレッシブディスクロージャーをそのまま実装している。

ディレクトリのパスを渡すだけで Skills を取り込めるため、AWS 公式の Agent Toolkit for AWS など外部 Skills 集を MCP 経由なしで直接読み込める。

## Strands Labs

2026 年 3 月に AWS は **Strands Labs** を開設し、本体に取り込む前のフロンティアプロジェクトを公開している。初期リリースは「AI Functions」（自然言語仕様から実行時にコード生成）と「Strands Robots」（VLA モデルで LLM をハードウェアに接続）の 2 つ。

## 関連ページ

- [Amazon Bedrock AgentCore](/blogs/wiki/tools/bedrock-agentcore/) — Strands の主要デプロイ先
- [Agent Toolkit for AWS](/blogs/wiki/tools/agent-toolkit-for-aws/) — Strands から読み込める AWS 公式 Skills 集
- [Skills フォーマット](/blogs/wiki/concepts/agent-skills-format/) — AgentSkills プラグインが扱う共通仕様
- [MCP](/blogs/wiki/concepts/mcp/) — Strands がツールとして接続するプロトコル
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Strands が属するエージェント基盤群

## ソース記事

- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
