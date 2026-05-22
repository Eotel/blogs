---
title: "Skills フォーマット（SKILL.md 互換層）"
description: "Anthropic 発の SKILL.md フォーマットが Microsoft APM・AWS Agent Toolkit にも採用され、さらに GreenSock などのライブラリベンダーまで広がり、エージェントハーネス間の事実上の互換層に育っている"
date: 2026-05-11
lastmod: 2026-05-22
aliases: ["Agent Skills", "SKILL.md", "Skills format", "Agent Skills format"]
related_posts:
  - "/blogs/posts/2026/03/2026-03-10-claude-code-skills-guide/"
  - "/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/"
  - "/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
  - "/blogs/posts/2026/05/2026-05-21-gsap-skills/"
  - "/blogs/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/"
  - "/blogs/posts/2026/02/2026-02-27-fb664679cf44fad6134bf9ff360ec7c1/"
  - "/blogs/posts/2026/03/2026-03-04-5681ba524366e175aa03f28ba194d17c/"
  - "/blogs/posts/2026/03/2026-03-04-e5839407fe23c117b54ce5ed77dac5fa/"
  - "/blogs/posts/2026/03/2026-03-11-claude-code-skill-creator/"
tags: ["skills", "agent", "interop", "claude", "aws", "vendor-skills"]
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
| GreenSock | [gsap-skills](https://github.com/greensock/gsap-skills) | `SKILL.md` × 8（`gsap-core` / `timeline` / `scrolltrigger` / `plugins` / `utils` / `react` / `performance` / `frameworks`）+ `llms.txt` インデックス | `npx skills add` 経由で Claude Code / Cursor / Codex / Windsurf / Copilot / Antigravity ほか 40+ エージェント |

Anthropic は **オーサリングの最小単位**、Microsoft は **配布と依存解決**、AWS は **業務特化の手順書 + AWS API 接続口**、GreenSock は **ライブラリベンダー公式の API ガイド** と、それぞれの強みが噛み合う構図になっている。

## ライブラリベンダーによる採用（2026 年〜）

ハーネス側 / クラウド側だけでなく、JavaScript ライブラリのベンダーまで `SKILL.md` を公式の配布媒体として使い始めている。代表例が [GreenSock の `gsap-skills`](/blogs/wiki/tools/gsap-skills/)（2026 年初頭から公開、記事執筆時点で 3,600 stars 超）。

この層の使い方の特徴は次のとおり。

- **LLM 既知バイアスを上書きするためのパッチ**: gsap-skills の `gsap-plugins/SKILL.md` 冒頭は「`.npmrc` に GreenSock auth token を書かせるな」「`npm.greensock.com` の private registry を提案させるな」と明示的に書いている。LLM の学習データには Webflow 買収（2024-10-15）以前の Club GSAP 前提の古い情報が大量に蓄積されているため、SKILL.md でそれを矯正している。
- **API リファレンスではなく "落とし穴の地図"**: `useGSAP()` フックを scope なしで使うな、`ScrollTrigger.scrollerProxy()` の登録忘れに注意、といったエージェントが間違えやすい部分を先回りで潰す構成。
- **trigger 語の戦略的設計**: `skills/llms.txt` の trigger に「Club GSAP」「.npmrc GSAP」「private GSAP registry」など **古い前提語** を含め、検索や生成でそれらが現れた瞬間に確実に skill を発火させる。

ライブラリ作者自身が公式 Skill を出すと、サードパーティの記事や StackOverflow の古い回答よりも先にエージェントの参照先に滑り込める。「React 18 公式 docs が当時の検索順位を更新していった」のと同じ位置を、Skills がエージェントの参照経路で獲りに行こうとしている、と整理できる。

## 「互換層」としての意味

同じ `SKILL.md` をリポジトリに置いておけば、APM で取り込みつつ Claude Code でも Cursor でも Strands Agents でも実行できる。ハーネスを乗り換えても Skills 資産が捨てなくて済む — これが「Skills as interop layer」と呼ばれる現象。

ハーネスとメモリのロックイン問題と対になる議論で、Skills を共通フォーマットで書いておくこと自体が、エージェント運用のベンダーロックイン回避策にもなる。

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — `SKILL.md` の発祥ハーネス
- [Strands Agents](/blogs/wiki/tools/strands-agents/) — AgentSkills プラグインで `SKILL.md` を読み込む
- [Agent Toolkit for AWS](/blogs/wiki/tools/agent-toolkit-for-aws/) — AWS 業務向け公式 Skills 集
- [gsap-skills](/blogs/wiki/tools/gsap-skills/) — GreenSock 公式の JS アニメーションライブラリ向け Skills 集
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — Skills は 4 層構造のワークフロー層に相当
- [エージェントメモリのロックイン](/blogs/wiki/concepts/agent-memory-lock-in/) — Skills の共通化が回避策になる文脈

## ソース記事

- [Claude Code Skills 構築完全ガイド](/blogs/posts/2026/03/2026-03-10-claude-code-skills-guide/) — 2026-03-10
- [APM（Agent Package Manager）](/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/) — 2026-04-17
- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11
- [GSAP Skills でできること — AI コーディングエージェントに公式 GSAP の作法を教える Skills 集](/blogs/posts/2026/05/2026-05-21-gsap-skills/) — 2026-05-21
- [Agent Plugins for AWS — AI コーディングエージェントに AWS の専門知識を装着する](/blogs/posts/2026/02/2026-02-27-1f9912da7aa40da008ba4cb88d519c13/) — 2026-02-27
- [# 【2026年最新】世界一わかりやすい Agent Skills 完全ガイド — まとめ](/blogs/posts/2026/02/2026-02-27-fb664679cf44fad6134bf9ff360ec7c1/) — 2026-02-27
- [Claude Code Agent Skills を強化する三銃士 --- scripts / references / assets の使い分け](/blogs/posts/2026/03/2026-03-04-5681ba524366e175aa03f28ba194d17c/) — 2026-03-04
- [Anthropic 公式 skill-creator の設計を解剖する — Orchestration Skill という新しいスキル設計パターン](/blogs/posts/2026/03/2026-03-04-e5839407fe23c117b54ce5ed77dac5fa/) — 2026-03-04
- [Claude Code のスキルを作るなら skill-creator プラグインを使おう](/blogs/posts/2026/03/2026-03-11-claude-code-skill-creator/) — 2026-03-11
