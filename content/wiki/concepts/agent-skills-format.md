---
title: "Skills フォーマット（SKILL.md 互換層）"
description: "Anthropic 発の SKILL.md フォーマットが Microsoft APM・AWS Agent Toolkit にも採用され、エージェントハーネス間の事実上の互換層に育っている"
date: 2026-05-11
lastmod: 2026-05-11
aliases: ["Agent Skills", "SKILL.md", "Skills format", "Agent Skills format"]
related_posts:
  - "/posts/2026/03/2026-03-10-claude-code-skills-guide/"
  - "/posts/2026/04/2026-04-17-apm-agent-package-manager/"
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
tags: ["skills", "agent", "interop", "claude", "aws"]
---

## 概要

`SKILL.md`（YAML フロントマター + 段階的に読み込まれる本体 + 補助ファイル）を基本単位とするエージェント手順書の仕様。もともと Anthropic が Claude 向けに [The Complete Guide to Building Skills for Claude](https://claude.com/blog/complete-guide-to-building-skills-for-claude) で公開したものだが、2026 年に入って Microsoft の APM、AWS の Agent Toolkit for AWS も同じフォーマットを採用し、**異なるハーネス間で同じ手順書を持ち回せる相互運用層** に育ちつつある。

## ファイル構造

```
my-skill/
├── SKILL.md          # メイン指示（必須）
├── scripts/          # 補助スクリプト
├── references/       # 参考資料
└── assets/           # アセット
```

`SKILL.md` の冒頭 YAML フロントマターには最低限 `name` と `description` を書く。description は **「何をするか」+「いつ使うか」** の 2 要素を含めるのが定石。

## プログレッシブディスクロージャー

スキルの読み込みは 3 段階で進む。

| Level | 内容 | 読み込みタイミング |
|---|---|---|
| 1 | YAML フロントマター（name / description） | 常時（50〜100 トークン） |
| 2 | `SKILL.md` 本体 | 関連すると判断したとき |
| 3 | scripts / references / assets | 必要に応じて発見・読み込み |

この階層により、多数のスキルを登録してもコンテキストウィンドウを圧迫しない。

## 採用ベンダーの比較

| 提供元 | 配布物 | 配布フォーマット | 主な接続層 |
|---|---|---|---|
| Anthropic | Claude Code Skills | `SKILL.md`（個別フォルダ） | Claude.ai / Claude Code / API |
| Microsoft | [APM (apm.yml)](https://github.com/microsoft/apm) | `apm.yml` で `SKILL.md` 群を依存解決 | GitHub Copilot / Claude Code / Cursor / Codex CLI |
| AWS | [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) | `SKILL.md` + MCP Server + Plugins | Strands Agents / Bedrock AgentCore / MCP 互換クライアント |

Anthropic は **オーサリングの最小単位**、Microsoft は **配布と依存解決**、AWS は **業務特化の手順書 + AWS API 接続口** と、それぞれの強みが噛み合う構図になっている。

## 「互換層」としての意味

同じ `SKILL.md` をリポジトリに置いておけば、APM で取り込みつつ Claude Code でも Cursor でも Strands Agents でも実行できる。ハーネスを乗り換えても Skills 資産が捨てなくて済む — これが「Skills as interop layer」と呼ばれる現象。

ハーネスとメモリのロックイン問題と対になる議論で、Skills を共通フォーマットで書いておくこと自体が、エージェント運用のベンダーロックイン回避策にもなる。

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — `SKILL.md` の発祥ハーネス
- [Strands Agents](/blogs/wiki/tools/strands-agents/) — AgentSkills プラグインで `SKILL.md` を読み込む
- [Agent Toolkit for AWS](/blogs/wiki/tools/agent-toolkit-for-aws/) — AWS 業務向け公式 Skills 集
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — Skills は 4 層構造のワークフロー層に相当
- [エージェントメモリのロックイン](/blogs/wiki/concepts/agent-memory-lock-in/) — Skills の共通化が回避策になる文脈

## ソース記事

- [Claude Code Skills 構築完全ガイド](/blogs/posts/2026/03/2026-03-10-claude-code-skills-guide/) — 2026-03-10
- [APM（Agent Package Manager）](/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/) — 2026-04-17
- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
