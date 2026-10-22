---
title: "LLMflation（LLM推論コストの崩壊）"
description: "LLM推論コストが年率10倍ペースで下落する現象。ジェヴォンズのパラドックスにより利用量は増大し、インテリジェンスが「ストレージ」「帯域」に続く第3のコモディティになる"
date: 2026-06-27
lastmod: 2026-06-27
aliases: ["LLMflation", "LLM推論コスト", "インテリジェンスのコモディティ化", "too cheap to meter"]
related_posts:
  - "/posts/2026/06/when-intelligence-gets-cheap/"
tags: ["LLM", "AIエージェント", "Jevonsパラドックス", "LLMflation", "推論コスト"]
---

## 概要

**LLMflation** は、a16z の Guido Appenzeller が定義した概念で、同等品質の LLM 推論コストが急速に下落する現象を指す。GPT-3 相当の品質（MMLU 約 42）を得るコストは 2021 年〜2024 年の 3 年間で **100 万トークンあたり 60 ドル → 0.06 ドル**（1,000 分の 1）に下落した。年率にすると約 10 倍の速度。

Sam Altman も 2025 年 2 月のブログ「Three Observations」で同様に観測している。

> The cost to use a given level of AI falls about 10x every 12 months, and lower prices lead to much more use.

ムーアの法則（18 か月で 2 倍）と比較すると桁が違う。ストレージや帯域のコスト崩壊が 10 年単位で進んだのに対し、インテリジェンスは年単位だ。

## Gmail/YouTube アナロジー

リソースのコスト崩壊とプロダクト変化の関係は過去 2 回観測されている。

| リソース | 希少だった時代の行動 | 潤沢になって消えた行動 | 新しいデフォルト |
|---|---|---|---|
| ストレージ | 容量を管理し、メールを選別して消す | 削除・選別 | 全部保存して検索する（Gmail） |
| 帯域 | 圧縮・分割してダウンロードし、保存する | 保存という工程 | 見たいときにストリームする（YouTube） |
| インテリジェンス | 注意の割り当てを人間が選ぶ | ？ | ？ |

Gmail の発明は「1GB の容量」ではなく「削除しなくていい」という新しいデフォルト。YouTube の発明はストリーミング技術ではなく「保存しなくていい」というデフォルト。安いリソースは行動を変えるのではなく、**節約の儀式を消す**。

## ジェヴォンズのパラドックス

William Stanley Jevons が 1865 年に観察した経済法則。蒸気機関の効率改善で石炭消費効率が上がると、総消費量は減るどころか増えた。効率化はリソースを節約せず、適用範囲を広げる。

Microsoft の Satya Nadella は 2025 年 1 月（DeepSeek 登場で AI 株が動揺した局面）にこう述べた。

> Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of.

LLMflation もこの構造で動く。推論コストが下がるほど、それまで「高すぎて試さなかった」適用場面が爆発的に広がる。

## "Too cheap to meter" との距離

Sam Altman は「towards intelligence too cheap to meter」（メーターで測るまでもなく安いインテリジェンスへ）という言葉を使った。元ネタは 1954 年に米国原子力委員会委員長 Lewis Strauss が原子力電力について語った言葉で、**この予言は実現しなかった**。

LLMflation が現在の年率 10 倍ペースを維持し続ける保証はない。学習コストの高騰、電力・データセンターの制約、高性能モデルの価格維持などが曲線を折り曲げうる。ただし仮にペースが半分に鈍化しても、数年で桁が変わることに変わりはない。

## インテリジェンスが安くなると消える「儀式」

インテリジェンスを節約するために人間が行っている儀式の候補。

1. **質問の厳選** → 1,000 回の試行錯誤を丸ごと委ねる [AI エージェント](/blogs/wiki/concepts/ai-agent/)へ
2. **既製品ソフトウェアの採用** → 自分だけのために今日だけ使うツールをその場で生成（[Vibe Coding](/blogs/wiki/concepts/vibe-coding/)）
3. **重要箇所だけのレビュー** → 全コミット・全記事・全契約に常時 AI レビューを適用

消えていくのは「限られたインテリジェンスをどこに割り当てるかを人間が選ぶ」という行動。人間の仕事は「何を考えてもらうか」から「何を採用するか（判断と責任）」へ寄っていく。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — インテリジェンスの委任先
- [Vibe Coding](/blogs/wiki/concepts/vibe-coding/) — 使い捨てソフトウェアの入口
- [Agentic Engineering](/blogs/wiki/concepts/agentic-engineering/) — AaaS として成果を納品するパラダイム

## ソース記事

- [ストレージは Gmail を、帯域は YouTube を生んだ — インテリジェンスが安くなったら何が生まれるか](/blogs/posts/2026/06/when-intelligence-gets-cheap/) — 2026-06-05
