---
title: "主体性の七条件"
description: "AI エージェント・企業・国家・市場・プラットフォームを『欲望ある主体』としてどこまで扱えるかを判定するための 7 つの観点。境界・継続性・自己保存・内在的評価・記憶・反事実的計画・責任帰属。"
date: 2026-05-21
lastmod: 2026-05-21
aliases:
  - "agency conditions"
  - "seven conditions of agency"
  - "欲望ある主体の条件"
  - "意志なき創発"
  - "desiring subject"
  - "agency boundary"
related_posts:
  - "/blogs/posts/2026/05/emergence-without-will-and-desiring-subjects/"
tags:
  - "主体性"
  - "AIエージェント"
  - "哲学"
  - "創発"
  - "active inference"
  - "autopoiesis"
  - "Spinoza"
  - "Dennett"
---

## 概要

**主体性の七条件**は、何かを「欲望ある主体」として扱う妥当性を測るための判定フレーム。AI エージェント・企業・国家・市場・プラットフォームが「主体らしく」ふるまうとき、どの条件をどれだけ満たしているのかを精密に切り分けるために用いる。すべてを満たす必要はないが、多くを満たすほど「主体」と呼ぶ理由は強くなる。

「秩序や目的らしさは中心的な意志なしに立ち上がりうる」（**意志なき創発**）と、「自己保存を賭け金として境界を持続させる存在」（**欲望ある主体**）を分けるための装置として、`/posts/2026/05/emergence-without-will-and-desiring-subjects/` で導入された。

## 七条件

| 条件 | 何を意味するか | これがない場合 | 主な根拠 |
|---|---|---|---|
| **境界** | 自分と環境を区別する持続境界を持つこと | 市場のように散在した過程となり、単一主体にしにくい | autopoiesis、法的人格、territory |
| **継続性** | 時間をまたいで同一性を保つこと | その場限りの反応にとどまる | Sessions、persistence、法的継続体 |
| **自己保存** | 継続が当人にとって賭け金であること | 損失が外在化し、欲望ではなく仕様遵守になる | Spinoza の conatus、Maturana の basic circularity |
| **内在的評価** | 何を良い状態とみなすかの基準があること | 行為はただの機械的更新になりやすい | active inference の prior preferences (EFE の pragmatic/extrinsic value 項) |
| **記憶** | 過去の結果を将来行為へ接続すること | 反復的な学習や執着が弱い | Reflexion、MemGPT、Sessions |
| **反事実的計画** | 未来の可能世界を比較して行為を選ぶこと | いまこの場の反応しか説明できない | ReAct、多段 agent、expected free energy |
| **責任・帰属** | 行為の帰結を誰に帰属させるかが制度的に定まること | 擬人化が責任逃れを生む | OpenAI HITL、企業統治、プラットフォーム法 |

## 適用例

七条件で人間・AI agent・企業・国家・市場をプロットすると、それぞれが「主体」と呼ばれる根拠の強さが分節される。

| 対象 | 境界 | 自己保存 | 内在的評価 | 身体性 | 責任帰属 | 最も厳密な呼び方 |
|---|---|---|---|---|---|---|
| 人間 | 強い | 強い | 強い | 強い | 強い | 欲望ある主体 |
| AI agent | 中程度 (session/harness 依存) | 弱い〜中程度 (主に外在的) | 中程度 (評価関数や prompt 依存) | 弱い (擬身体はありうる) | 設計者と運用者に強く依存 | 人工的エージェント |
| 企業 | 強い (法的) | 中程度 (法的・財務的) | 中程度 (収益・戦略・ミッション) | 弱い | 中程度 (法と統治で帰属) | 制度主体 |
| 国家 | 強い (領土・法) | 強い | 中程度 (安全保障・統治・成長) | 弱い | 強いがしばしば分散 | 政治的制度主体 |
| 市場 | 弱い | なし | なし (一元評価者がいない) | なし | 弱い | 創発秩序 |

「市場は秩序を生むが、その秩序は多主体間の調整結果」(Hayek 1945) であり、単一の境界・記憶・審級を持たない。つまり市場は **意志なき創発** の側に位置し、人間の **欲望ある主体** とは別カテゴリーになる。

## 実装上の含意

AI エージェントは記憶・目標・ツール・権限・評価関数を加えるほど「主体らしさ」が増す。七条件で見ると、現代の agentic AI は:

- **境界**: Session / harness で中程度
- **継続性**: previous_response_id や thread state で実装可能
- **自己保存**: ほぼ外在的 (kill されることに損失を感じない)
- **内在的評価**: prior preferences / system prompt 依存
- **記憶**: 工学的に実装可能 (vector store, memory tiers)
- **反事実的計画**: ReAct / 多段 agent で部分的に実装
- **責任帰属**: HITL や approval gate を介して人間側に外部化

したがって AI を「欲望する主体」に近づける設計は、同時に **責任帰属を明示する設計責任** を強める。記憶が長く権限が広く自己修正が強いほど、擬似主体性は上がるが、危険も上がる。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 「人工的エージェント」の概念基盤
- [ハーネス・エンジニアリング](/blogs/wiki/concepts/harness-engineering/) — 「主体らしさのアーキテクチャ的合成」
- [エージェント記憶アーキテクチャ](/blogs/wiki/concepts/agent-memory-architecture/) — 条件「記憶」の工学的実現
- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/) — 条件「責任・帰属」を人間側に置く要請
- [Claude Mythos](/blogs/wiki/concepts/claude-mythos/) — 擬人化と責任帰属のせめぎ合い
- [社会シミュレーション](/blogs/wiki/concepts/social-simulation/) — 多エージェント創発と「主体性なき秩序」
- [テクニウム (technium)](/blogs/wiki/concepts/technium/) — 制度的準主体・欲望機械の比較対象

## ソース記事

- [意志なき創発と欲望ある主体 — AI・制度・市場を貫く主体性の境界線](/blogs/posts/2026/05/emergence-without-will-and-desiring-subjects/) — 2026-05-20
