---
title: "LLMflation（LLM 推論コスト崩壊）"
description: "同等品質の LLM 推論コストが年率約 10 分の 1 で下落する現象。ジェヴォンズのパラドックスと組み合わせると「インテリジェンスが安くなったら何が消えるか」を予測できる"
date: 2026-06-05
lastmod: 2026-06-05
aliases: ["LLMflation", "推論コスト崩壊", "intelligence too cheap to meter", "Jevonsパラドックス"]
related_posts:
  - "/posts/2026/06/when-intelligence-gets-cheap/"
tags: ["LLM", "推論コスト", "AIエージェント", "LLMflation"]
---

## 概要

同等品質の LLM 推論コストが年率約 10 分の 1 で下落する現象。a16z の Guido Appenzeller が命名した。GPT-3 相当（MMLU 約 42）のコストは 2021 年 11 月の 100 万トークンあたり 60 ドル（GPT-3）から 2024 年 11 月の 0.06 ドル（Llama 3.2 3B）へ、3 年で約 1,000 分の 1 に下落した。ムーアの法則「18 か月で 2 倍」と比べて桁が違う速さだ。

Sam Altman は 2025 年のブログ "Three Observations" でこの観察を言語化している。

> The cost to use a given level of AI falls about 10x every 12 months, and lower prices lead to much more use.

## ジェヴォンズのパラドックスとの関係

William Stanley Jevons が 1865 年の『石炭問題』で示したパラドックス——蒸気機関の効率が上がって石炭消費効率が改善すると、石炭の総消費量は減るどころか増えた。**効率化はリソースを節約しない。適用範囲を広げる。**

DeepSeek 登場で AI 株が揺れた 2025 年 1 月、Microsoft の Satya Nadella がこの言葉を引いた。

> Jevons paradox strikes again! As AI gets more efficient and accessible, we will see its use skyrocket, turning it into a commodity we just can't get enough of.

## コスト崩壊が「消す」もの

ストレージが安くなったら Gmail が「メールを消す行動」を消し、帯域が安くなったら YouTube が「ダウンロードする行動」を消したように、リソースの潤沢化は節約の儀式を消し去り、新しいデフォルトを生む。

| リソース | 希少時代の儀式 | 消えた行動 | 新しいデフォルト |
|---|---|---|---|
| ストレージ | メールを選別して削除 | 削除・選別 | 全部保存して検索（Gmail） |
| 帯域 | 圧縮・分割してダウンロード | 保存という工程 | 見たいときにストリーム（YouTube） |
| インテリジェンス | 限られた注意をどこに割くかを選ぶ | ? | すべてに常時適用するデフォルト |

インテリジェンスが安くなると消えるのは「**限られたインテリジェンスをどこに割り当てるかを人間が選ぶ**」という儀式だと考えられる。

具体的な兆候として 3 つの方向が見えている:

1. **質問から委任へ** — 単発の問答から、目標を丸ごと渡す [AI エージェント](/blogs/wiki/concepts/ai-agent/) へ
2. **既製品から使い捨てへ** — 万人向けソフトウェアから、個人が今日だけ使うツールをその場で生成する [Vibe Coding](/blogs/wiki/concepts/vibe-coding/) へ
3. **選んで適用から全部に常時適用へ** — 重要箇所だけのレビューから、全コミット・全記録への AI 常時適用へ

## "Too Cheap to Meter"

Sam Altman は 2024 年 7 月、GPT-4o mini リリース時に「towards intelligence too cheap to meter」と投稿した。「メーターで測るまでもなく安いインテリジェンス」というフレーズは、1954 年の Lewis Strauss 米原子力委員長の演説「子どもたちはメーターで測るまでもなく安い電力を家庭で享受するだろう」を下敷きにしている。原子力の予言は外れたが、LLM についてはここ 3 年の実績が年率 10 倍下落を示している。

外挿の罠には注意が必要だ。学習コストの高騰・電力制約・高性能モデルの価格維持など、曲線を折り曲げうる要因は実在する。それでも方向性として「桁が変わる」トレンドは続いている。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 安いインテリジェンスの最初の受け皿
- [Vibe Coding](/blogs/wiki/concepts/vibe-coding/) — 使い捨てソフトウェアへの移行の入り口
- [Agentic Engineering](/blogs/wiki/concepts/agentic-engineering/) — コストが崩壊した先の開発パラダイム

## ソース記事

- [ストレージは Gmail を、帯域は YouTube を生んだ — インテリジェンスが安くなったら何が生まれるか](/blogs/posts/2026/06/when-intelligence-gets-cheap/) — 2026-06-05
