---
title: "投機的 TTS は本当に効くのか — VADUSA / Llasa+ / SSD で読む 2026 年 TTS 高速化マップ"
date: 2026-05-12
lastmod: 2026-05-12
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "投機的デコード（Speculative Decoding）を音声合成に応用した VADUSA / Llasa+ / SSD を中心に、Flow Matching 蒸留（F5-TTS, DMOSpeech 2）・TensorRT-LLM・ストリーミング設計まで、2026 年の TTS 推論高速化を 1 本に整理する。"
categories: ["AI/LLM"]
tags: ["TTS", "音声合成", "投機的デコード", "推論高速化", "flow-matching", "VADUSA", "Llasa", "F5-TTS"]
---

LLM 高速化の主役だった **投機的デコード（Speculative Decoding）** が、ここ 1 年で音声合成（TTS）側にも降りてきた。VADUSA、Llasa+、SSD と立て続けに「**投機的 TTS（Speculative TTS）**」を名乗る論文が並び、AR codec language model の生成を 1.4〜5 倍速くしている。

一方で TTS 推論高速化には別系統の潮流もある。F5-TTS や FlashSpeech のように **Flow Matching の step 数を蒸留で削る** 系列、TensorRT-LLM や FP8 KV cache のような **システム最適化**、そして first-packet latency を切り詰める **ストリーミング設計** だ。本稿はこの 4 つの軸を一度に整理し、「自分の TTS パイプラインのどこを攻めれば速くなるか」が分かる地図を残しておく。

![TTS 推論高速化の 4 象限マップ。AR 投機的 TTS（VADUSA / Llasa+ / SSD）／ NAR Flow Matching 蒸留（F5-TTS / DMOSpeech 2）／ システム最適化（TensorRT-LLM / FP8 KV cache）／ ストリーミング設計（CosyVoice 2 / VoXtream）を代表手法と共に俯瞰した図。](/blogs/images/tts-acceleration-map.svg)

## なぜ "TTS の推論速度" が再び熱いのか

ボイスエージェント・リアルタイム翻訳・ゲーム NPC のような **対話用途** が広がったことで、TTS は「正確に読めれば良い」フェーズを抜けて「**話し始めるまでの時間**」と「**喋り続けられる帯域**」を競うフェーズに入った。評価指標も 3 つに分かれて使われる。

| 指標 | 定義 | 主な用途 |
| --- | --- | --- |
| **RTF**（Real-Time Factor） | 1 秒の音声を生成するのに何秒かかるか | バッチ・オフライン合成 |
| **TTFA**（Time to First Audio） | リクエストから最初の音が出るまで | UI 体感・遅延感 |
| **First-packet latency** | streaming で **最初の音声チャンク** が出るまで | full-duplex 会話 |

RTF は良いが TTFA は遅い、というモデルは珍しくない（NFE が多い NAR 系がこの形になりやすい）。本稿の数値も、それぞれどの指標を見ているかに注意してほしい。なお NFE は **Number of Function Evaluations**（拡散・フローマッチング系で必要な順伝播回数）で、サンプリング step 数と同義に使う。

## TTS 推論アーキテクチャの 2 大潮流

現在の TTS は大きく 2 つの設計に収束している。

1. **AR codec language model**：テキストから **音響トークン列**（EnCodec / SoundStream / X-Codec2 などの離散コード）を **自己回帰的に** 1 トークンずつ出して、最後に codec decoder で波形に戻す。VALL-E、Llasa、CosyVoice 2、Spark-TTS が代表格。LLM と同じ next-token prediction なので、**LLM の推論最適化がほぼそのまま使える**。
2. **NAR flow matching / diffusion**：拡散モデルやフローマッチングを使って **メルスペクトログラム（または latent）を非自己回帰的に** 一気に生成する。F5-TTS、Matcha-TTS、VoiceFlow-TTS が典型。生成 step 数（NFE）が速度を直接決める。

この 2 系統で「速くする方向」がまったく違う。AR 系は **「1 step あたりの出力を増やす」** で、NAR 系は **「step 数そのものを減らす」** だ。前者の代表が投機的 TTS、後者の代表が consistency / distribution matching distillation。

## 投機的デコードとは — LLM での仕組み復習

投機的 TTS に入る前に、LLM 版の投機的デコードを 1 段だけ復習しておく。

- **Draft モデル `q`**：軽量で速い。`K` 個のトークン列 `ỹ_{t+1..t+K}` を提案する。
- **Target モデル `p`**：本来出したい大きいモデル。**1 回の forward** で `K` 個のトークン位置の確率分布を一括で得て、Draft の提案を順に検証する。

各位置 `i` で次の Bernoulli を引いて accept / reject を決めるのが古典的な **rejection sampling** だ。

> accept する確率 = `min(1, p(ỹ_i | ·) / q(ỹ_i | ·))`

Reject されたらその位置以降を捨て、Target が **1 トークンだけ** 自分の分布から再サンプルして繋ぐ。Medusa はこの構図をさらに進めて、**Draft を本体モデル末尾の追加 head（multi-head）に置き換え**、tree attention で `K` 通りの候補ツリーを 1 forward で検証する。EAGLE 系は draft 側に隠れ状態を持たせて accept rate を底上げする派生だ。

LLM の世界で **2〜3 倍の wall-clock 加速** は当たり前になっており、Anthropic / OpenAI / NVIDIA のサーブもこの上に積まれている。— では、これを音響トークンに持ち込むと何が起きるのか。

## 投機的 TTS の難所と解法

LLM 用の枠組みを TTS にそのまま当てると、**意外にも accept rate が上がりにくい**。音響トークンは LLM のテキストトークンと違って **「ほぼ同じ意味の代替候補」が多数ある** からだ。Target 分布が `(コード 137: 0.18, コード 138: 0.17, コード 139: 0.16, …)` のように **裾の広い分布になり、最尤候補に確率が集中しない**。そのため厳密な確率比だけで accept すると素通りしてくれない。

![投機的 TTS のパイプライン図: 入力テキスト → Codec LM backbone → Target head と Draft heads × K に分岐 → Draft の候補ツリーを Target が 1 forward で並列検証 → tolerance sampling で accept、不一致は rollback、accept トークン列が Codec decoder で 24/48 kHz 波形に変換されるまでの流れ。](/blogs/images/speculative-tts-pipeline.svg)

ここに対する解法が 2024〜2026 で 3 種類出てきた。

### VADUSA — TTS 用 tolerance sampling と sparse tree

**VADUSA**（Bohan Li 他、SJTU X-LANCE、[arXiv:2410.21951](https://arxiv.org/abs/2410.21951)、"Fast and High-Quality Auto-Regressive Speech Synthesis via Speculative Decoding"）は AR TTS（VALL-E 系）に **Medusa 流の draft heads を複数枚** 追加した最初期の研究。重要な工夫は 2 つある。

- **Tolerance sampling**：accept 判定を「厳密な確率比」ではなく「**音響的距離が一定以下なら採用する**」緩い基準に置き換える。音声コードは元々 quantize された粒度の粗い表現なので、許容を入れても聴感品質は崩れない。
- **TTS 向け sparse tree**：tree attention の候補ツリーを、TTS のトークン遷移傾向に合わせて作り直す（LLM 流の汎用ツリーは音声では候補が密になりすぎる）。

論文値で **AR TTS を最大 5× 加速**、品質指標（WER・SECS）は維持以上、と報告されている。

### Llasa+ — Frozen backbone × MTP self-verify

**Llasa+**（[arXiv:2508.06262](https://arxiv.org/abs/2508.06262)、"Llasa+: Free Lunch for Accelerated and Streaming Llama-Based Speech Synthesis"、[ASLP-lab/LLaSA_Plus](https://github.com/ASLP-lab/LLaSA_Plus)）は、LLaMA ベースの zero-shot TTS である Llasa を **完全に凍結したまま**、後段に **MTP（Multi-Token Prediction）モジュール 2 枚** を plug-and-play で追加する設計。

VADUSA との一番の違いは、**Draft モデルを別途用意しない** 点だ。frozen backbone 自身に複数 head を生やし、本体の forward の中で MTP 出力を生成 → 同じ本体で self-verify する。draft 訓練のコストもメモリ二重持ちも要らない。

著者らは LibriTTS のみで学習して **1.48× 加速**、品質劣化なし、しかも **streaming 互換** を報告している。zero-shot voice cloning を壊さずに plug-in できるのは実装側にとってありがたい。

### SSD — 古典的 2 モデル投機を AR TTS に

**SSD（Speech Speculative Decoding、Zijian Lin 他、[arXiv:2505.15380](https://arxiv.org/abs/2505.15380)、"Accelerating Autoregressive Speech Synthesis Inference With Speech Speculative Decoding"、Interspeech 2025）** は、LLM で古くからある **2 モデル方式**（小さい draft + 大きい target）を AR speech synthesis にそのまま適用したベースライン研究。draft はターゲットの一部パラメータを fine-tune した軽量モデルで、報告速度は **1.4×**、主観評価で similarity / naturalness は本体と同等。

VADUSA / Llasa+ がモデル内部の構造変更を必要とするのに対し、SSD は **外から 2 つ目のモデルを足すだけ** で済む。「とりあえず投機的 TTS を効かせたい」場合の最初の選択肢になる。

### 補助線: tolerance sampling の擬似コード

VADUSA 系の判定を最小限のコードに落とすと、こんな雰囲気になる。

```python
def tolerance_accept(draft_token, target_logits, *, threshold=0.6):
    target_p = softmax(target_logits)
    # 1) draft トークン自身の target 確率
    p_self = target_p[draft_token]
    # 2) target で最尤のトークン
    top_p, top_token = max(target_p), argmax(target_p)
    # 3) 音響的に "ほぼ同等" なら accept
    if p_self >= threshold * top_p:
        return True, draft_token        # accept (draft 採用)
    return False, top_token             # reject → target で 1 token 補完
```

ポイントは閾値 `threshold` を 1 未満に設定すること。LLM 用の厳密 rejection sampling だと音声では **accept rate が二桁台に落ちる** ことがあり、`threshold = 0.5〜0.7` あたりで accept rate を引き上げ、WER を維持するチューニングが必要になる。**PCG（Principled Coarse-Grained Acceptance、[arXiv:2511.13732](https://arxiv.org/abs/2511.13732)）** は、この閾値の選び方を **音響的等価クラス** の上で理論化した一般化案だ。

### 数値まとめ

| 手法 | base モデル | 加速 | 余分なモデル | 備考 |
| --- | --- | --- | --- | --- |
| VADUSA | VALL-E 系 AR TTS | **〜 5×** | head × N（同居） | tolerance + sparse tree |
| Llasa+ | Llasa (frozen) | **1.48×** | MTP head × 2（同居） | streaming 内包 |
| SSD | AR speech LM 全般 | **1.4×** | 別 draft モデル | 既存実装に外付け可 |
| PCG | 任意の draft / target | acceptance rate 改善 | — | tolerance の一般化 |

## 対比 ①: NAR 系 Flow Matching で step を減らす

ここからは NAR 系の高速化。flow matching / diffusion 系の TTS は **NFE が速度を直接支配** するので、「step を減らす」一択で攻める。流派は 3 つに分かれる。

### ベース flow matching（NFE 10〜20）

- **F5-TTS**（[arXiv:2410.06885](https://arxiv.org/abs/2410.06885)、"A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching"、[SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)）：DiT + conditional flow matching、duration model も text encoder も要らないシンプル設計。Sway Sampling 込みで **NFE 16** あたりで実用品質。
- **Matcha-TTS**（[arXiv:2309.03199](https://arxiv.org/abs/2309.03199)）：OT-CFM ベース、NFE 10 以下で破綻しない初期世代。
- **VoiceFlow-TTS**（[arXiv:2309.05027](https://arxiv.org/abs/2309.05027)）：rectified flow を 2 回適用して **2 step でも崩れない** 経路を学習。

### 訓練不要の NFE 削減

- **Fast F5-TTS（EPSS）**（[arXiv:2505.19931](https://arxiv.org/abs/2505.19931)）：訓練なしで F5-TTS の NFE を **7 まで削減**、3090 で **RTF 0.030**（≒ 約 4× 速）。プラグイン的に既存デプロイへ後付けできるのが強い。

### 蒸留（1〜4 step）

- **CoMoSpeech**（[arXiv:2305.06908](https://arxiv.org/abs/2305.06908)）：consistency distillation で **1-step** 生成、A100 で **real-time の 150 倍**。
- **FlashSpeech**（[arXiv:2404.14700](https://arxiv.org/abs/2404.14700)）：latent consistency + GAN、1–2 step で **既存比 〜 20×**。
- **DMOSpeech 2**（[arXiv:2410.11097](https://arxiv.org/abs/2410.11097)、[yl4579/DMOSpeech2](https://github.com/yl4579/DMOSpeech2)）：distribution matching distillation を TTS に適用、**4 step で F5-TTS の teacher を超える** クォリティ。

ざっくりの相場感は、**F5-TTS に EPSS を当てて訓練不要で約 4× → さらに DMOSpeech 2 系の蒸留で 4 step まで圧縮** が現実解。1-step まで詰めたければ FlashSpeech / CoMoSpeech 系を学習しなおす投資が要る。

## 対比 ②: システム最適化（推論エンジン / 量子化）

ここまでは **モデルの構造** を変える話。一方でモデルをいじらずに、**推論ランタイムだけで** 速度を稼ぐ層がある。

- **TensorRT-LLM + Triton** で CosyVoice 2 を回すと、Hugging Face 素の実装比で **〜 4×** 加速、first-packet latency も縮む（[NVIDIA 公式: Speculative Decoding in TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM/advanced/speculative-decoding.html)）。投機的 TTS と組み合わせるのも当然できる。
- **FP8 KV cache** や **FlashAttention-3** は AR codec LM の token 生成帯域を底上げする。Llasa 系の大きい backbone ほど効く。
- **AWQ / INT8** などのウェイト量子化は、エッジ側の TTS（Parler-TTS / XTTS / Kitten-TTS 系）で VRAM を半減させ、ノートでも回るようになる。

重要なのは、**この層はモデル設計（投機的 TTS / 蒸留）と直交して掛け算で効く** ことだ。「投機的 TTS で 1.5× → TensorRT-LLM で 4× → 合計 6× 弱」のように積める。

## 対比 ③: ストリーミング設計

RTF が良くても、**最初のチャンクが出るまで** が遅ければ会話用途では失格になる。ここを最適化するのが streaming 設計だ。

- **CosyVoice 2 streaming**（[arXiv:2412.10117](https://arxiv.org/abs/2412.10117)、[FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)）：first-packet **〜 150 ms** を実現する代表実装。
- **VoXtream**（[arXiv:2509.15969](https://arxiv.org/abs/2509.15969)、"Full-Stream Text-to-Speech with Extremely Low Latency"）：limited lookahead つき phoneme→audio token の monotonic alignment で **GPU 上 102 ms** の initial delay。
- **SpeakStream**（[arXiv:2505.19206](https://arxiv.org/html/2505.19206v1)）：interleaved window で「読み終わってから喋り始める」遅延を吸収する設計。
- **Llasa+** は streaming も内包しており、VADUSA / SSD が踏み込めなかった ④ ストリーミング領域に投機的 TTS を持ち込んだ唯一の手法でもある。

ここは **モデル側の構造設計**（causal attention / lookahead window / chunk size）にがっつり踏み込む話なので、外付けの量子化やエンジン交換では基本届かない。

## どれを使えばいいか — 用途別チートシート

| 困りごと | 第一手 | 第二手 |
| --- | --- | --- |
| AR codec LM（Llasa / CosyVoice 2）を **そのまま** 速くしたい | **投機的 TTS（Llasa+ / VADUSA / SSD）** | TensorRT-LLM + FP8 KV cache |
| F5-TTS / Matcha 系の NAR を速くしたい | **Fast F5-TTS / EPSS（訓練不要 NFE 削減）** | DMOSpeech 2 / FlashSpeech で蒸留 |
| **first-packet latency** を切り詰めたい | streaming + lookahead（VoXtream / CosyVoice 2 streaming） | Llasa+ の MTP streaming |
| GPU コストを半減したい | FP8 KV cache + AWQ | 蒸留で 1-step まで詰める |
| エッジ・ノート PC で動かしたい | AWQ / INT8 量子化 | Spark-TTS 系の codec-direct 設計 |

「**まずモデル設計（投機的 TTS / 蒸留）でゲインを取ってから、システム最適化と streaming で残りを削る**」が無難な順序になる。最初にシステム側を詰めても、設計側の枷で天井が決まる。

## まとめ

TTS の高速化は **投機的 TTS（AR）／ Flow Matching 蒸留（NAR）／ システム最適化／ streaming** の 4 象限で整理できる。とくに 2024–2026 の最大の変化は、これまで LLM 専用だった **投機的デコードが TTS 側に確かに刺さる** ことが、VADUSA / Llasa+ / SSD によって実証された点だ。MoE や long context の話題に隠れがちだが、ボイスエージェント時代を支える地味だが重要な土台が、いま静かに整いつつある。

## 未開拓ネタ / 展望

- **Draft = AR + Verify = NAR flow matching のハイブリッド**：draft 側を高速な AR codec LM、verify 側を NAR flow matching に分ける構成は理論上は可能だが、執筆時点で公開実装は見当たらない。
- **EAGLE-3 / Medusa-2 の TTS 移植**：accept rate を底上げする LLM 用の派生はそのまま speech token にも効くはずだが、これも論文として未公開。
- **音響的等価類の自動学習**：tolerance sampling の閾値を手で決めずに、codec の量子化セルから等価クラスを学習で抽出する方向。PCG が踏み出した先。

このあたりは半年〜1 年で公開実装が次々に出てくる気配があるので、投機的 TTS と flow matching 蒸留のハイブリッドはこのブログでも追い続けたい。

## 関連 Wiki / 関連記事

- [DFlash（Apple Silicon 向け Block Diffusion 投機的デコード）](/blogs/wiki/tools/dflash/) — LLM 側の投機的デコードの実装事例。
- [MacのローカルLLMが4.1倍速に！Apple Silicon向け新技術「DFlash」](/blogs/posts/2026/04/2026-04-15-dflash-mlx-apple-silicon-llm/)
- [Mistral Voxtral TTS: ElevenLabs に匹敵するオープンウェイト音声AI](/blogs/posts/2026/03/2026-03-30-mistral-voxtral-tts/) — 同時期に公開された TTS 製品の事例。

## 参考リンク

- VADUSA: [arXiv:2410.21951](https://arxiv.org/abs/2410.21951)
- Llasa+: [arXiv:2508.06262](https://arxiv.org/abs/2508.06262) / [ASLP-lab/LLaSA_Plus](https://github.com/ASLP-lab/LLaSA_Plus)
- SSD (Speech Speculative Decoding): [arXiv:2505.15380](https://arxiv.org/abs/2505.15380)
- PCG (Principled Coarse-Grained Acceptance): [arXiv:2511.13732](https://arxiv.org/abs/2511.13732)
- F5-TTS: [arXiv:2410.06885](https://arxiv.org/abs/2410.06885) / [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)
- Fast F5-TTS / EPSS: [arXiv:2505.19931](https://arxiv.org/abs/2505.19931)
- Matcha-TTS: [arXiv:2309.03199](https://arxiv.org/abs/2309.03199) / [shivammehta25/Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS)
- VoiceFlow-TTS: [arXiv:2309.05027](https://arxiv.org/abs/2309.05027) / [X-LANCE/VoiceFlow-TTS](https://github.com/X-LANCE/VoiceFlow-TTS)
- CoMoSpeech: [arXiv:2305.06908](https://arxiv.org/abs/2305.06908) / [zhenye234/CoMoSpeech](https://github.com/zhenye234/CoMoSpeech)
- FlashSpeech: [arXiv:2404.14700](https://arxiv.org/abs/2404.14700)
- DMOSpeech 2: [arXiv:2410.11097](https://arxiv.org/abs/2410.11097) / [yl4579/DMOSpeech2](https://github.com/yl4579/DMOSpeech2)
- CosyVoice 2: [arXiv:2412.10117](https://arxiv.org/abs/2412.10117) / [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- Spark-TTS: [arXiv:2503.01710](https://arxiv.org/abs/2503.01710) / [SparkAudio/Spark-TTS](https://github.com/SparkAudio/Spark-TTS)
- VoXtream: [arXiv:2509.15969](https://arxiv.org/abs/2509.15969)
- SpeakStream: [arXiv:2505.19206](https://arxiv.org/abs/2505.19206)
- Speculative Decoding Survey: [arXiv:2502.19732](https://arxiv.org/abs/2502.19732)
- Medusa: [FasterDecoding/Medusa](https://github.com/FasterDecoding/Medusa)
- EAGLE: [SafeAILab/EAGLE](https://github.com/SafeAILab/EAGLE)
- TensorRT-LLM Speculative Decoding: [公式ガイド](https://nvidia.github.io/TensorRT-LLM/advanced/speculative-decoding.html)
