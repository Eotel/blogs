---
slug: 2026-05-11-aws-agent-toolkit-strands-skills
title: "AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
categories: ["AI/LLM"]
tags: ["aws", "strands-agents", "bedrock-agentcore", "skills", "agent-harness"]
---

TIS 株式会社の [@nasuvitz](https://qiita.com/nasuvitz) 氏が Qiita に [「Agent Toolkit for AWS が持つ 50 種類の Skills を Strands Agents から実行する」](https://qiita.com/nasuvitz/items/fd1be5f3be4170a11a44) を公開した（2026-05-10）。AWS 公式の Agent Toolkit に同梱される多数の `SKILL.md` を、Amazon Bedrock AgentCore 上で動く Strands Agents から **MCP を介さずローカルから直接ロード** する実装ハウツーで、コード量も少なく即取り込めるレシピになっている。

本ブログでは元記事の実装ポイントを整理した上で、**`SKILL.md` フォーマットが Anthropic 固有仕様からハーネスをまたぐ事実上の互換層に変わりつつある** という業界の動きにも触れる。

## Skills フォーマットが「ハーネスの互換層」になりつつある

`SKILL.md`（YAML フロントマター + 段階的に読み込まれる本体 + 補助ファイル）の形式は、もともと Anthropic が Claude 向けに [「The Complete Guide to Building Skills for Claude」](https://claude.com/blog/complete-guide-to-building-skills-for-claude) で公開した仕様だった。本ブログでは既に以下を取り上げている。

- [Claude Code Skills 構築完全ガイド](/blogs/posts/2026/03/2026-03-10-claude-code-skills-guide/) — Anthropic 公式 33 ページの要点
- [APM（Agent Package Manager）](/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/) — Microsoft 製の横断パッケージマネージャー

ここに今回 AWS が **同じ `SKILL.md` 形式** で公式のスキル集を整備し、しかも自社の SDK（Strands Agents）から自然に読み込めるプラグインを用意して合流した格好になる。提供元はバラバラでもフォーマットが揃っているため、`apm.yml` で AWS の Skills を取り込み、Strands でも Claude Code でも同じ手順書として走らせる — そんな相互運用が現実的になってきた。

## 元記事 — Strands Agents から AWS 公式 Skills を呼ぶ

著者らは「TechAdvisor」という社内向け AI エージェントを開発しており、AWS の設計・運用・セキュリティ・コスト・AI 利用に関する最新の手順をモデル知識だけに任せず、**公式手順書をその場で読み込ませて回答品質を底上げ** したいというモチベーションを持っている。一般的な LLM の知識に依存すると「古い手順や不完全な判断に基づいた回答」になりやすいという課題感は、AWS のように更新頻度の高い領域では特に切実だ。

実装方針の要点は以下のとおり。

- MCP は使わず、ローカルから Skills だけを直接読み込む
- AgentCore の **CodeZip デプロイ** にそのまま乗る軽量構成
- TechAdvisor は AWS 操作権限を持たない設計で、Skills は設計・調査・トラブルシューティングの手順提示専用として用途を制限

## Agent Toolkit for AWS の構成

[Agent Toolkit for AWS](https://aws.amazon.com/products/developer-tools/agent-toolkit-for-aws/) は AWS が公式に提供する「エージェントを AWS の上で開発・運用するためのキット」で、主な構成要素は次の 4 つに整理できる。

| 要素 | 役割 |
|---|---|
| MCP Server | AWS API 呼び出しやドキュメント検索を MCP 経由で提供 |
| Skills | 特定タスク用の手順書セット（`SKILL.md` ベース） |
| Plugins | 各エージェントに合わせたパッケージ |
| Rules files | AWS 利用方針の宣言ファイル |

GitHub 上の関連リポジトリは少しややこしい。`gh api` で確認すると現時点で 2 つの公式系列が並走している。

- [`aws/agent-toolkit-for-aws`](https://github.com/aws/agent-toolkit-for-aws) — "Official, AWS-supported MCP servers, skills, and plugins"。`skills/` 配下に `core-skills/` と `specialized-skills/` の 2 階層構成、`plugins/aws-agents/skills/` には平坦な構成の 7 個（agents-build / agents-connect / agents-debug / agents-deploy / agents-get-started / agents-harden / agents-optimize）が並ぶ。
- [`awslabs/agent-plugins`](https://github.com/awslabs/agent-plugins) — AWS Labs 側で先行していたプラグイン群。`amazon-location-service`、`aws-amplify`、`aws-serverless`、`deploy-on-aws`、`migration-to-aws`、`sagemaker-ai` など、より「製品横断のシナリオ」寄りのスキルを束ねている。

元記事が「50 種類」と呼んでいるのは、これらのリポジトリから著者が自分の用途に合わせて選んで束ねた数で、内訳は `aws/`（Compute / Database / Storage / Security / Operations / Networking / Analytics / Developer Tools / Management / Generative AI ほか）と `aws-agents/`（AI エージェント開発専用、7 個）。

## なぜ MCP ではなく「ローカル直接読み込み」を選んだのか

公式キットは MCP Server も提供しているが、元記事はそちらを使わず Skills だけをファイルシステムから直接読む構成を選んだ。理由は CodeZip との相性に集約される。

- **Bedrock AgentCore Runtime の Direct Code Deployment（CodeZip）** は、コード + 依存を `.zip` で固めて S3 にアップロードするだけで動く。Python は 2025 年 11 月に GA、Node.js は [2026 年 4 月にサポート追加](https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-bedrock-agentcore-runtime/) と歴史が浅いが、コンテナイメージのビルドを省略できる。
- MCP Server を別途立てるとコンテナや別プロセスの管理が必要になり、CodeZip のシンプルさが崩れる。
- Strands 標準で `AgentSkills` プラグインが用意されており、**ディレクトリのパスを渡すだけで Skills を扱える**。MCP を経由しないぶんレイテンシも余計な権限線引きも要らない。

## 実装の核 — `rglob("SKILL.md")` で SKILL.md を集める

元記事の Python コードはほぼそのまま動くシンプルな構造だ。

```python
from pathlib import Path
from strands import Agent
from strands.vended_plugins.skills import AgentSkills

AWS_AGENTS_SKILLS_DIR = Path(__file__).parent / "skills" / "aws-agents"
AWS_SKILLS_DIR = Path(__file__).parent / "skills" / "aws"


def _get_skill_sources() -> list[Path]:
    skill_sources: list[Path] = []
    if AWS_AGENTS_SKILLS_DIR.exists():
        # 平坦構成: ディレクトリそのものを渡せる
        skill_sources.append(AWS_AGENTS_SKILLS_DIR)
    if AWS_SKILLS_DIR.exists():
        # カテゴリ階層あり: SKILL.md を再帰検出して親ディレクトリを集める
        skill_sources.extend(
            sorted(
                skill_md.parent
                for skill_md in AWS_SKILLS_DIR.rglob("SKILL.md")
            )
        )
    return skill_sources


agent_skills = AgentSkills(skills=_get_skill_sources())
agent = Agent(plugins=[agent_skills], ...)
```

ポイントは 2 つある。

1. `aws-agents/` は平坦、`aws/` は 2 階層という Skills ディレクトリ構造の差異を `rglob("SKILL.md")` 一発で吸収していること。新しいカテゴリが増えてもコード側は変更不要。
2. Skills 取得段では、リポジトリ全体ではなく必要な subtree だけを `git clone --filter=blob:none --sparse` で持ってくる省サイズな同期スクリプトを使う設計。CodeZip の zip サイズと起動時間に効く。

[`AgentSkills` プラグイン](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.agent_skills/) は Anthropic の Agent Skills 仕様に準拠したものだ。起動時にはスキルのメタデータ（name と description）だけをシステムプロンプトに XML ブロックとして注入し、エージェントが必要だと判断したときに本体を専用ツール経由でロードする — まさに **プログレッシブディスクロージャー** をそのまま実装している。

## 設計の眼目 — 「権限を持たないエージェント」

元記事で個人的に重要だと感じたのは、コードよりもむしろシステムプロンプトの書き方だ。TechAdvisor は AWS の実行権限（mcp-proxy 経由の API 実行など）を意図的に持たず、Skills の用途も次のように制限されている：

> For design, research, validation, troubleshooting guidance, and step-by-step procedure drafting only.

つまり「設計・調査・検証・トラブル対応・手順ドラフトの提示」までで、自分で API を叩くことは禁じる。実行権限ではなく **ドキュメントと指示で振る舞いを縛る** スタイルで、本ブログで何度か取り上げている [「ルールファイルを超えたハーネス設計」](/blogs/posts/2026/04/2026-04-23-harness-engineering-beyond-rule-files/) の議論ともよく噛み合う。MCP Server をあえて外したことで「権限がそもそも存在しない」状態が物理的に保証されているのも、レビューが楽になるという副次効果がある。

## 比較 — Anthropic / Microsoft / AWS の Skills 接続点

ここまでの整理を踏まえると、Skills 周辺のエコシステムは次のように位置付けられる。

| 提供元 | 配布物 | 配布フォーマット | 主な接続層 |
|---|---|---|---|
| Anthropic | Claude Code Skills | `SKILL.md`（個別フォルダ） | Claude.ai / Claude Code / API |
| Microsoft | [APM (apm.yml)](https://github.com/microsoft/apm) | `apm.yml` で `SKILL.md` 群を依存解決 | GitHub Copilot / Claude Code / Cursor / Codex CLI |
| AWS | [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws) | `SKILL.md` ＋ MCP Server ＋ Plugins | Strands Agents / Bedrock AgentCore / MCP 互換クライアント |

形式は揃いつつも、各社の重心は明らかに異なる。Anthropic は **オーサリングの最小単位** としての `SKILL.md` を提供し、Microsoft は **配布と依存解決** のレイヤーを APM で提供する。AWS は **AWS 業務に特化した手順書 + AWS API への接続口** をワンセットで配り、Strands SDK で取り回しまでカバーする。`SKILL.md` を共通項として、それぞれの強みが噛み合うようになってきた、というのが現状の構図だ。

## まとめ

`SKILL.md` が Anthropic 単独仕様の段階から、Microsoft の APM、AWS の Agent Toolkit へと裾野を広げ、**異なるハーネス間で同じ手順書を持ち回せる相互運用層** に進化しつつある。元記事の Strands Agents × AWS Skills の組み合わせは、その流れを実装で実感できる好例だ。

導入のハードルも `rglob("SKILL.md")` 数行と CodeZip デプロイで済む。AWS 上でエージェントを運用しているチームは、まず公式 Skills の中身を眺めて、自社の利用方針 (Rules files) と組み合わせて取り込んでみる価値が大いにある。

## 関連 Wiki

- [Claude Code Skills 構築完全ガイド](/blogs/posts/2026/03/2026-03-10-claude-code-skills-guide/)
- [APM — Agent Package Manager](/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/)
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/)
- [AI エージェント](/blogs/wiki/concepts/ai-agent/)
- [MCP（Model Context Protocol）](/blogs/wiki/concepts/mcp/)

## 参考リンク

- 元記事: [Agent Toolkit for AWS が持つ 50 種類の Skills を Strands Agents から実行する — @nasuvitz](https://qiita.com/nasuvitz/items/fd1be5f3be4170a11a44)
- [Agent Toolkit for AWS（公式）](https://aws.amazon.com/products/developer-tools/agent-toolkit-for-aws/)
- [`aws/agent-toolkit-for-aws`（GitHub）](https://github.com/aws/agent-toolkit-for-aws)
- [`awslabs/agent-plugins`（GitHub）](https://github.com/awslabs/agent-plugins)
- [Strands Agents SDK](https://strandsagents.com/)
- [`AgentSkills` プラグインリファレンス](https://strandsagents.com/docs/api/python/strands.vended_plugins.skills.agent_skills/)
- [Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/bedrock/agentcore/)
