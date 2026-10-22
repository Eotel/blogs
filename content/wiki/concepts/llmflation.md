---
title: "LLMflation（LLM 推論コストの崩壊）"
description: "同等品質の LLM 推論コストが年率 10 分の 1 ペースで下落する現象。Jevons のパラドックスにより利用量は逆に急増し、新たな製品カテゴリを生む"
date: 2026-07-25
lastmod: 2026-07-25
aliases: ["LLMflation", "LLM推論コスト", "インテリジェンスのコスト崩壊", "Jevonsパラドックス"]
related_posts:
  - "/posts/2026/06/when-intelligence-gets-cheap/"
tags: ["LLM", "推論コスト", "Jevons", "AIエージェント", "経済"]
---

## 概要

a16z の Guido Appenzeller が命名した概念。同等品質の LLM 推論コストが年率およそ **10 分の 1**（3 年で 1,000 分の 1）のペースで下落している現象を指す。GPT-3 相当の推論コスト（MMLU 約 42）は 2021 年 11 月の 60 ドル/百万トークンから 2024 年 11 月の 0.06 ドル/百万トークン（Llama 3.2 3B）へと崩落した。

ムーアの法則（18 か月で 2 倍）を大幅に上回るペースで、ストレージや帯域のコスト崩壊より速い。

## Jevons のパラドックスとの接続

William Stanley Jevons が 1865 年『石炭問題』で示した **Jevons のパラドックス**——蒸気機関の効率が上がると石炭の総消費量は減るどころか増えた——がここでも成立する。コストが下がっても利用量は減らず、適用範囲が広がることで総需要は急増する。

Microsoft の Satya Nadella は DeepSeek 登場で AI 株が動揺した 2025 年 1 月にこの観察を引用した。

> Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of.

## Gmail・YouTube との構造的類比

LLMflation が示唆するパターンは、過去のリソース崩壊と同じ構造を持つ。

| リソース | 崩壊前の「節約の儀式」 | 崩壊後に消えた行動 | 生まれた新カテゴリ |
|---|---|---|---|
| ストレージ | メールを選別して削除する | 削除・選別 | Gmail（全部保存して検索） |
| 帯域 | 動画を圧縮・分割してダウンロード | 保存という工程 | YouTube（ストリーミング） |
| インテリジェンス | 考えてもらうことを厳選して割り当てる | 割り当ての選別 | ？（常時・全件適用） |

コストが連続的に下がっても、プロダクトは非連続に現れる。「インテリジェンスを節約するために人間がやっている儀式は何か、それが消えたら何がデフォルトになるか」を問う思考フレームとして機能する。

## インテリジェンスが安くなったら消えるもの・生まれるもの

### 1. 「質問から委任へ」

単発の問答ではなく、目標を渡して途中の判断をすべて委ねる [AI エージェント](/blogs/wiki/concepts/ai-agent/)への移行。SoR（記録のシステム）から SoA（行動のシステム）への重心移動も同じ根を持つ。

### 2. 「既製品から使い捨てのソフトウェアへ」

「自分ひとりのために今日だけ使うツールをその場で生成して、使い終わったら捨てる」が成立し始める。[Vibe Coding](/blogs/wiki/concepts/vibe-coding/) はその入り口。

### 3. 「全部に常時適用」

レビュー・監査・ファクトチェックは希少な注意を割り当てる作業だったが、インテリジェンスが安ければすべてに常時かけられる（例: 全コミットに自動レビュー、全記事にフルレビューを走らせる）。

## 外挿の罠

"too cheap to meter"（メーターで測るまでもなく安い）は 1954 年に原子力発電の未来として使われたフレーズだが、その予言は実現しなかった。LLMflation の現在のペースが永続する保証はなく、学習コストの高騰・電力制約・高性能モデルの価格維持などが曲線を折り曲げうる。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — コスト崩壊の最初の受益者
- [Vibe Coding](/blogs/wiki/concepts/vibe-coding/) — 「使い捨てのソフトウェア」が成立するコーディングパターン
- [Agentic Engineering](/blogs/wiki/concepts/agentic-engineering/) — AaaS へのパラダイムシフト

## ソース記事

- [ストレージは Gmail を、帯域は YouTube を生んだ — インテリジェンスが安くなったら何が生まれるか](/blogs/posts/2026/06/when-intelligence-gets-cheap/) — 2026-06-05
