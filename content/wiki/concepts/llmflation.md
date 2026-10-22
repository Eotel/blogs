---
title: "LLMflation — インテリジェンスのコスト崩壊"
description: "LLM 推論コストが年率 10 倍のペースで下落する現象。ストレージが Gmail を、帯域が YouTube を生んだように、インテリジェンスの低価格化が何を生むかを問う"
date: 2026-06-20
lastmod: 2026-06-20
aliases: ["LLMflation", "intelligence cost collapse", "インテリジェンスコスト崩壊", "Jevonsパラドックス"]
related_posts:
  - "/posts/2026/06/when-intelligence-gets-cheap/"
tags: ["LLM", "AIエージェント", "Jevons paradox", "LLMflation", "推論コスト"]
---

## 概要

LLM 推論コストが**年率約 10 倍のペースで下落**する現象。a16z の Guido Appenzeller が "LLMflation" と名付けた（2024 年）。GPT-3 相当品質（MMLU 約 42）のコストは 2021〜2024 年の 3 年で 100 万トークンあたり 60 ドル → 0.06 ドル、約 1,000 分の 1 まで下落した（年率 10 倍の 3 乗）。

Sam Altman（2025 年）:
> The cost to use a given level of AI falls about 10x every 12 months, and lower prices lead to much more use.

ムーアの法則（18 か月で 2 倍）と比べても桁が異なる下落ペースであり、ストレージや帯域が辿った道よりも急だ。

## Gmail・YouTube との類比

リソースのコスト崩壊がデフォルト行動を非連続に変えるパターンは過去 2 回起きている。

| リソース | 希少時代の行動 | 潤沢化で消えた行動 | 新しいデフォルト |
|---|---|---|---|
| ストレージ | 容量管理・メール選別 | 削除・選別 | 全部保存して検索（Gmail, 2004） |
| 帯域 | 圧縮・ダウンロード・保存 | 保存という工程 | ストリームして見る（YouTube, 2005） |
| インテリジェンス | どこに注意を割り当てるか選ぶ | 注意の割り当て儀式 | すべてに常時適用（？） |

重要な観察: リソースの値下がり（連続的変化）が、行動の消滅（非連続な変化）に翻訳される形でプロダクトが生まれた。

## ジェヴォンズのパラドックス

William Stanley Jevons が 1865 年の『石炭問題』で示した経済観察——蒸気機関の効率改善で石炭消費効率が上がると、石炭の**総消費量は増えた**。効率化はリソースを節約しない、適用範囲を広げる。

Satya Nadella（2025 年 1 月、DeepSeek の登場で AI 株が動揺した際）:
> Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of.

## 「注意の割り当て」が消えたあとに来るもの

インテリジェンスが安くなると消えていくのは「限られたインテリジェンスをどこに割り当てるかを人間が選ぶ」という儀式。これが消えたあとに現れると予測される変化:

1. **質問から委任へ** — 単発の問答から、目標を渡して途中の判断をすべて委ねる [AI エージェント](/blogs/wiki/concepts/ai-agent/)への移行。業務ソフトウェアの重心が記録のシステム（SoR）から行動のシステム（SoA）へ移る
2. **既製品から使い捨てへ** — 「今日だけ使うツールをその場で生成して捨てる」が成立。[Vibe Coding](/blogs/wiki/concepts/vibe-coding/) はその入り口。ソフトウェアは出版物ではなく会話の産物に近づく
3. **選んで適用 → 全部に常時適用** — レビュー・監査・ファクトチェックが全記事・全コミット・全契約書・全診療記録に常時かかる

## 注意点: 外挿の罠

「too cheap to meter」（メーターで測るまでもなく安い）は 1954 年に原子力発電で言われた予言で、実現しなかった。インテリジェンスについてもコスト曲線が永続する保証はなく、以下が折り曲げうる要因として存在する:

- 学習コストの高騰（より高性能なモデルを作るコストが増大）
- 電力やデータセンターの制約
- 高性能モデルの価格維持（競合が減れば下落ペースが鈍る）

それでも「同等品質の推論コスト」に限れば、過去 3 年の実績は年率 10 倍の下落を示している。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — LLMflation の恩恵を受けて普及が加速するシステム
- [Vibe Coding](/blogs/wiki/concepts/vibe-coding/) — インテリジェンスが安くなることで広がる「使い捨てソフトウェア」の入り口
- [Agentic Engineering](/blogs/wiki/concepts/agentic-engineering/) — AaaS（成果課金）へのパラダイムシフト。配信コストが崩壊する先にある姿

## ソース記事

- [ストレージは Gmail を、帯域は YouTube を生んだ — インテリジェンスが安くなったら何が生まれるか](/blogs/posts/2026/06/when-intelligence-gets-cheap/) — 2026-06-05
