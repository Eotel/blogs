---
title: "投機的 TTS（Speculative TTS）"
description: "LLM 用の Speculative Decoding を音声合成に持ち込み、AR codec language model の推論を 1.4〜5 倍速くする手法群。VADUSA / Llasa+ / SSD / PCG が主な代表作。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["Speculative TTS", "speculative decoding for TTS", "投機的デコード TTS", "VADUSA", "Llasa+", "SSD speech speculative decoding"]
related_posts:
  - "/posts/2026/05/2026-05-12-speculative-tts-acceleration-2026/"
tags: ["TTS", "音声合成", "投機的デコード", "推論高速化"]
---

## 概要

**投機的 TTS（Speculative TTS）** は、LLM 高速化で実績のある投機的デコード（Speculative Decoding）を **AR codec language model 型の音声合成** に転用する手法群を指す。Draft モデル（または draft head）が次の数トークンを並列に提案し、Target モデルが 1 回の forward でまとめて検証する基本構図は LLM 用と同じだが、TTS 固有の「音響トークンは交換可能な候補が多い」性質を踏まえて **tolerance sampling** や **音響的 sparse tree** などの拡張が加えられているのが特徴。2024〜2026 にかけて VADUSA / Llasa+ / SSD / PCG が立て続けに登場し、AR TTS を **1.4〜5 倍** 速くしている。

LLM 側の投機的デコード（[DFlash](/blogs/wiki/tools/dflash/) など）と発想は同じだが、accept rate を確保するために **判定基準を緩める** 工夫が要る点が音声側固有の難所。

## 仕組み — Draft → Verify → Tolerance accept

1. **Draft**: 軽量モデルまたは backbone に追加した複数 head（Medusa 流）が、`K` 個の音響トークン候補 `ỹ_{t+1..t+K}` を tree attention 上に並列で出す。
2. **Verify**: Target モデルが 1 forward で `K` 位置の確率分布を一括取得。
3. **Accept**: 通常の rejection sampling
   `accept する確率 = min(1, p(ỹ_i | ·) / q(ỹ_i | ·))`
   を **tolerance 付き** に置き換えて、「target の確率比が閾値以上」なら採用する。これにより、音響的にほぼ同等の代替トークンを取りこぼさず accept できる。
4. **Reject 時**: 不一致箇所まで rollback し、Target が 1 トークン補完して再開。

擬似コードは次のとおり。

```python
def tolerance_accept(draft_token, target_logits, *, threshold=0.6):
    target_p = softmax(target_logits)
    p_self = target_p[draft_token]
    top_p, top_token = max(target_p), argmax(target_p)
    if p_self >= threshold * top_p:
        return True, draft_token        # accept (draft 採用)
    return False, top_token             # reject → target で 1 token 補完
```

`threshold = 0.5〜0.7` が経験則。LLM 流の厳密 rejection sampling だと accept rate が二桁台に落ち込み、せっかくの並列予測が活きない。

## 主要手法

| 手法 | 出典 | 加速 | 余分なモデル | 特徴 |
| --- | --- | --- | --- | --- |
| **VADUSA** | [arXiv:2410.21951](https://arxiv.org/abs/2410.21951) | 〜 5× | Medusa 流 draft head ×N（同居） | tolerance sampling + TTS 向け sparse tree |
| **Llasa+** | [arXiv:2508.06262](https://arxiv.org/abs/2508.06262) / [ASLP-lab/LLaSA_Plus](https://github.com/ASLP-lab/LLaSA_Plus) | 1.48× | MTP head ×2（同居） | frozen backbone + self-verify、streaming 内包 |
| **SSD** (Speech Speculative Decoding) | [arXiv:2505.15380](https://arxiv.org/abs/2505.15380) | 1.4× | 別 draft モデル | LLM 用古典 2 モデル方式の TTS 版 |
| **PCG** (Principled Coarse-Grained Acceptance) | [arXiv:2511.13732](https://arxiv.org/abs/2511.13732) | acceptance rate 改善 | — | tolerance sampling の理論一般化 |

実装難度・追加学習コスト・既存モデルへの後付けやすさで使い分ける:

- **frozen な Llasa を温存したまま速くしたい** → Llasa+
- **VALL-E 系の codec LM をフルにチューニング可** → VADUSA
- **既存 2 モデル投機を流用** → SSD
- **accept rate を理屈で詰めたい** → PCG

## TTS 高速化の中での位置づけ

投機的 TTS は **AR codec LM 系統** の高速化を担う 1 つの象限に過ぎず、他の 3 象限と組み合わせると効果が掛け算で乗る。

| 系統 | 中核アイデア | 代表 |
| --- | --- | --- |
| **AR codec LM × 投機的 TTS** | 1 step に複数トークン | VADUSA / Llasa+ / SSD |
| **NAR Flow Matching × step 削減** | サンプリング NFE を 1〜4 まで圧縮 | F5-TTS / DMOSpeech 2 / FlashSpeech |
| **システム最適化** | 推論エンジン / 量子化 | TensorRT-LLM / FP8 KV cache / AWQ |
| **ストリーミング設計** | first-packet を削る | CosyVoice 2 / VoXtream |

「投機的 TTS で 1.5× → TensorRT-LLM で 4× → 合計 6× 弱」のように積めるのが実運用上のうま味。

## 関連ページ

- [リアルタイム音声モデル（TTS / STT / S2S）](/blogs/wiki/concepts/realtime-voice-model/) — 製品・ライセンス・レイテンシ軸でのモデル選定。
- [DFlash](/blogs/wiki/tools/dflash/) — LLM 側の投機的デコード（Block Diffusion）実装。
- [ローカル LLM 比較](/blogs/wiki/concepts/local-llm-comparison/) — 投機的デコードを採用したローカル LLM の使い分け。

## ソース記事

- [投機的 TTS は本当に効くのか — VADUSA / Llasa+ / SSD で読む 2026 年 TTS 高速化マップ](/blogs/posts/2026/05/2026-05-12-speculative-tts-acceleration-2026/) — 2026-05-12
