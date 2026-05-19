---
title: "パラサイトヒューマン"
description: "前田太郎が 2000 年代から展開する、人間の感覚運動ループに寄生する共生型ウェアラブル計算機の構想"
date: 2026-05-19
lastmod: 2026-05-19
aliases: ["Parasite Human", "Parasitic Humanoid", "パラサイトヒューマンネット", "PHN", "PH"]
related_posts:
  - "/posts/2026/05/maeda-taro-parasite-human/"
tags: ["パラサイトヒューマン", "前田太郎", "テレイグジスタンス", "agent", "身体性AI"]
---

## 概要

**パラサイトヒューマン (PH)** は、前田太郎が 2000 年代から展開している共生型ウェアラブル計算機の設計思想。装着者の感覚・運動情報をモニタリングしながら行動モデルを学習し、ユーザーが**意識しないレベル**で支援・誘導・操作を返す。「寄生」はキャッチコピーではなく、**計算機が独立した身体を持たず、宿主としての人間の身体を存在基盤として使う**という構造の比喩。

ネットワーク版である **パラサイトヒューマンネット (PHN)** は、PH 同士を結んで五感情報通信・行動誘導・体験共有を行う多対多インフラ。現行 CREST (2025–2030) では人と AI・AI 同士・多主体間の非言語ネットワークへ再定式化されている。

## 詳細

### 寄生の対象（層構造）

| 層 | 内容 |
|---|---|
| 身体・姿勢・視点 | HMD と位置姿勢センサで一人称座標系を共有 |
| 感覚・運動ループ | 触覚・前庭刺激で意識下に支援 |
| 意図・つもり | 「つもり」検出・伝送による随意性拡張 |
| 体験・記憶 | 一人称体験の計測・記録・再生・共有 |
| 社会的協働 | 群衆誘導、人と AI の非言語ネットワーク |

### 研究史（一次資料ベース）

- **1990 年代前半**: 東京大学・舘暲研、テレイグジスタンス系
- **2000–2003 年度**: JST さきがけ「人間共生型インターフェイス」(JST-PROJECT-7700000639)
- **2002 年**: 論文 *Wearable robotics as a behavioral interface – The Study of the Parasitic Humanoid* (ISWC 2002)
- **2004–2005 年度**: NTT コミュニケーション科学基礎研究所、前庭電気刺激
- **2007–2012 年度**: JST CREST「パラサイトヒューマンネット」(先進的統合センシング技術領域、課題番号 JPMJCR07A3)
- **2007 年度〜**: 大阪大学、視野共有システムによる技能伝達
- **2010–2012**: KAKEN「『つもり』の検出と伝送」(運動意図の伝送、Agency)
- **2015–2017**: KAKEN「バーチャルサイボーグ」(第三の腕、身体所有感、Ownership)
- **2019–2023**: KAKEN「身体意識の拡張技術」
- **2025–2030**: JST CREST「人とAIの共生・協働を促進する非言語情報伝達チャネルの構築」(maeda-crest.com)

### 近接概念との切り分け

- **拡張**: 能力の幅を広げる一般概念
- **補助**: ユーザーの目標を前提に手助け
- **代行**: システムが仕事を引き受ける
- **操縦**: 明示的な操作命令で外部装置を動かす
- **誘導**: システムがユーザーの行動方向を変える
- **寄生（PH）**: 宿主の身体・知覚運動情報に常時接続し、明示命令なしに予測・支援・共有

### 通常のウェアラブルとの差

通常のウェアラブルは「ユーザーが身につける携帯型計算機」で、端末性が中心。PH は「人が操作する道具」ではなく、**人の行動を先読みして身体の一部のように働くふるまい**を志向する。装着者は機械を運ぶのではなく、**機械の側が宿主としての身体を利用する**。

### 寄生 vs 共生（symbiosis）

生物学では symbiosis に mutualism / commensalism / parasitism が含まれる。PH の「寄生」は、計算機が自前の身体を持たず宿主に依存するという点で parasitism に近い一方、設計が成功すれば**フィードバックで宿主の行為能力を高める相利共生**へ移行することを目指す。データ収奪・過剰誘導・主体感の侵食が起きると harmful な寄生へ戻る。

### 設計倫理

「自然にそうしたくなる支援」と「操作」の境界は同じ回路上にあるため、PH 的システムには次の倫理原則が要請される。

- 目標の明示
- 介入の可逆性
- 無視可能性
- 誤り時の即時停止
- 監査ログ
- ローカル優先
- 最終承認を人間に残す

主体感 (sense of agency) と身体所有感 (sense of ownership) が共に保たれることが、共生と支配を分ける条件になる。

### 現代 AI エージェントとの接続

PH 構想を 2020 年代後半の AI エージェントへ重ねると、寄生対象に応じて 3 つの分化として読める。

- **身体寄生型**: Apple Vision Pro、Ray-Ban Meta（装着型知覚デバイス）
- **認知寄生型**: Rewind「Your Second Brain」、ChatGPT メモリ（記憶・会話履歴）
- **文脈寄生型**: GitHub Copilot cloud agent（リポジトリ・作業環境）

ローカル LLM (Ollama) や Apple Private Cloud Compute のような privacy-first 設計は、「宿主が自分の境界を管理できる」状態を保つという意味で PH 倫理の現代的延長線上にある。

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — PH を「身体寄生型 AI エージェントの前史」として位置づけ
- [Agent memory architecture](/blogs/wiki/concepts/agent-memory-architecture/) — 認知寄生型 AI の記憶レイヤ
- [Agent memory lock-in](/blogs/wiki/concepts/agent-memory-lock-in/) — 宿主依存性のロックイン問題
- [Harness engineering](/blogs/wiki/concepts/harness-engineering/) — 文脈寄生型 AI のランタイム設計

## 一次資料

- [前田太郎 CiNet ページ](https://cinet.jp/japanese/people/2014299/)
- [現行 CREST プロジェクト (maeda-crest.com)](https://maeda-crest.com/)
- [JST PROJECT 25147334（現行 CREST）](https://projectdb.jst.go.jp/grant/JST-PROJECT-25147334/)
- [JST PROJECT 7700000639（さきがけ）](https://projectdb.jst.go.jp/grant/JST-PROJECT-7700000639/)
- [NII Researcher 1000000260521 (KAKEN 連動)](https://nrid.nii.ac.jp/ja/nrid/1000000260521/)
- [IEEE Xplore: Wearable Robotics as a Behavioral Interface (ISWC 2002)](https://ieeexplore.ieee.org/document/1167236/)
- [前田太郎氏インタビュー (dentsu-ho)](https://dentsu-ho.com/articles/4753)

## ソース記事

- [前田太郎のパラサイトヒューマン ── 寄生する計算機から現代 AI エージェントへ](/blogs/posts/2026/05/maeda-taro-parasite-human/) — 2026-05-19
