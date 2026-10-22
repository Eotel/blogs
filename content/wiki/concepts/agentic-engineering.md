---
title: "Agentic Engineering（エージェンティックエンジニアリング）"
description: "コードを「決定ロジックの担い手」から「使い捨ての道具」へ変える、AI エージェント中心のソフトウェア開発パラダイム。配信モデルは SaaS から AaaS へ"
date: 2026-06-09
lastmod: 2026-06-20
aliases: ["Agentic Engineering", "エージェンティックエンジニアリング", "Agent-as-a-Service", "AaaS"]
related_posts:
  - "/posts/2026/06/end-of-software-engineering/"
  - "/posts/2026/06/when-intelligence-gets-cheap/"
tags: ["AIエージェント", "ソフトウェアエンジニアリング", "LLM"]
---

## 概要

Agentic Engineering は、LLM を主たる推論エンジンに据え、コードを実行時に動的生成しては捨てる「使い捨ての道具」として扱うソフトウェア開発パラダイム。従来のソフトウェアエンジニアリングが **コード = 決定ロジックの担い手** だったのに対し、エージェントシステムでは決定ロジックは事前に書かれず実行時に生成され、残るのはエージェントの *能力* であって中間成果物（コード）ではない。

提唱者は Cisco の Renuka Kumar と Prashanth Ramagopal で、2026 年 4 月の LangChain ブログ寄稿記事 "Agentic Engineering: How Swarms of AI Agents Are Redefining Software Engineering" で定式化された（LangChain は掲載媒体であって提唱組織ではない点に注意）。彼らは「AI コーディングエージェント（単一セッション内で意図をコードに翻訳する）」より一段上の抽象として、チーム横断ワークフローを束ね長期記憶と状態・トレーサビリティを管理する **コントロールプレーン** だと位置づけた。

## 従来の SE との違い

| 次元 | 従来の SE | Agentic Engineering |
|---|---|---|
| 中核成果物 | ソースコード（静的） | エージェントシステム（動的） |
| 制御の中心 | 人間のエンジニア | LLM の推論エンジン |
| 決定機構 | 事前設計されたロジック | 実行時生成の推論 |
| 人間の役割 | コードの著者 | 意図のアーキテクト・調整役・監査役 |
| 複雑性の天井 | 人間の認知（一定） | モデル容量（計算量とともに成長） |
| 進化 | 手動リファクタリング | 自己修正 |

人間の差別化要因は「正しいコードを書く能力」から、**意図の明確化・アーキテクチャの監督・品質のキャリブレーション・倫理的ガバナンス** へ移るとされる。

## 配信モデルの三世代: Local → SaaS → AaaS

ソフトウェア配信史は「複雑性をエンドユーザーから誰が引き取るか」の累進的移転として整理できる。

| 世代 | 複雑性の所有者 | 収益モデル | 例 |
|---|---|---|---|
| Software 1.0（ローカル） | エンドユーザー | ライセンス販売 | Microsoft, Oracle |
| Software 2.0（SaaS） | ベンダー | サブスクリプション | Salesforce, AWS |
| Software 3.0（AaaS） | エージェント | 成果ベース | OpenAI, Anthropic |

SaaS が企業をサーバールームから解放したように、**Agent-as-a-Service (AaaS)** は「どう作るか（how）」の指定からユーザーを解放し、「何が欲しいか（what）」だけを言えばよくする。ソフトウェアではなく **成果（outcomes）が納品される**。

## 4 段階ロードマップ

| 段階 | 時期 | 人間の役割 | 代表システム |
|---|---|---|---|
| I. Tool-Augmented | 2023–2025 | 著者＋レビュアー | GitHub Copilot, Claude Code |
| II. Single-Task Autonomous | 2025–2027 | 意図のアーキテクト＋監査役 | Devin, OpenHands |
| III. Multi-Agent Teams | 2026–2029 | PM＋アーキテクト＋監査役 | LangChain orchestration, MetaGPT |
| IV. Self-Evolving Ecosystems | 2028+ | ゴール設定者＋倫理ガバナー | （展望） |

## 現在地と限界

理論的な約束（複雑性スケーリングからの第一原理）とは別に、実証面では明確な壁がある。継続的なソフトウェア進化（コミット履歴をまたぎエラーが累積する設定）を測る EvoClaw ベンチマークでは、孤立タスクで 80% 超の成功率が **継続設定では最大 38% まで崩落** する。背後にはコンテキストドリフト・エラー伝播・技術的負債への無自覚・検証の忠実度という 4 課題がある。

このため現時点の現実は「完全自律」ではなく **拡張（augmentation）パラダイム** であり、本番で信頼できる自律開発にはあと数年の研究が必要とされる。「完全自律」を謳うプロダクトは、まずこの継続設定での性能を問うのが実務的な物差しになる。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Agentic Engineering の構成単位
- [自己改善エージェント](/blogs/wiki/concepts/self-improving-agents/) — Stage IV（自己進化）に対応するパターン
- [マルチエージェント調整パターン](/blogs/wiki/concepts/multi-agent-coordination-patterns/) — Stage III の協調を支える設計パターン
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — エージェントの出力品質を担保する設計層
- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/) — 人間が監査役に退いたときの監督問題

## ソース記事

- [「ソフトウェアエンジニアリングの終わり」を読む — コードが「使い捨ての道具」になる世界の見取り図](/blogs/posts/2026/06/end-of-software-engineering/) — 2026-06-09
- [ストレージは Gmail を、帯域は YouTube を生んだ — インテリジェンスが安くなったら何が生まれるか](/blogs/posts/2026/06/when-intelligence-gets-cheap/) — 2026-06-05
