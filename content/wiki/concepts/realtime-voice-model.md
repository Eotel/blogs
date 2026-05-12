---
title: "リアルタイム音声モデル（TTS / STT / S2S）"
description: "音声を低遅延で扱う AI モデルの分類軸。TTS（合成）/ STT（認識）/ 双方向 (S2S, full-duplex) に分けて、レイテンシ・双方向性・提供形態の 3 つの軸で整理する。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["TTS", "STT", "speech-to-speech", "S2S", "full-duplex voice", "voice model", "音声モデル", "リアルタイム音声"]
related_posts:
  - "/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/"
  - "/posts/2026/03/2026-03-30-mistral-voxtral-tts/"
  - "/posts/2026/03/2026-03-25-insanely-fast-whisper/"
  - "/posts/2026/03/2026-03-04-1a39b3cc62c29543a5e6de566017beeb/"
tags: ["TTS", "STT", "音声AI", "Realtime API", "voice-agent"]
---

## 概要

音声を扱う AI モデルは、入出力の向きと処理の同時性によって 3 種類に分かれる:

- **TTS (Text-to-Speech)** — テキストを音声に変換する一方向モデル
- **STT (Speech-to-Text)** — 音声をテキストに書き起こす一方向モデル
- **S2S (Speech-to-Speech / full-duplex)** — 聴きながら喋る双方向モデル。1 つの session 上で発話・推論・応答を同時並行する

2024〜2026 にかけて、各役割で「リアルタイム対話に耐える」レイテンシ帯（端末〜サーバ往復込みで概ね 300 ms 以下）に到達したモデルが出揃い、voice agent の実装は **モデルを束ねる組み合わせ問題** に変わった。

## 選定の 3 つの軸

| 軸 | 内容 | 目安 |
|---|---|---|
| **レイテンシ** | TTFA (Time To First Audio) / モデル単体 / end-to-end のどれを指すか必ず確認 | 会話の閾値は ~100 ms、対話可能ラインは ~300 ms |
| **双方向性** | TTS / STT 単方向か、聴きながら喋る full-duplex (S2S) か | full-duplex なら barge-in (中断) 対応も必須 |
| **提供形態** | クラウド API、オープンウェイト、on-device の 3 区分 | プライバシー要件・推論コスト・カスタマイズ性で選ぶ |

レイテンシ表記は **指標の意味が揃っていない** のが現状の落とし穴。ベンダーが「~75 ms」と書いていてもそれがモデル単体か TTFA か end-to-end か、必ず一次情報で確認する。

## 主要プレイヤー（2026-05 時点）

### TTS 中心

- [OpenAI Realtime API](/blogs/wiki/tools/openai-realtime-api/) — gpt-realtime-2 系列。TTS / STT / S2S を 1 モデルで賄う統合型
- [Cartesia](/blogs/wiki/tools/cartesia/) — Sonic-3。state-space model 系で **モデル単体 <100 ms**
- [ElevenLabs](/blogs/wiki/tools/elevenlabs/) — Flash v2.5 (~75 ms) / Eleven v3 (70+ 言語) / Scribe v2 Realtime STT
- Deepgram Aura-2 — pronunciation control 付きエンタープライズ TTS
- Mistral [Voxtral TTS](/blogs/posts/2026/03/2026-03-30-mistral-voxtral-tts/) — オープンウェイト 4B、9 言語
- 日本語特化: irodori-TTS-500M-v2（MIT、絵文字で感情制御）、Qwen3-TTS（[QwenVoice](/blogs/posts/2026/03/2026-03-04-1a39b3cc62c29543a5e6de566017beeb/) で Mac オフライン実行）

### STT 中心

- OpenAI **gpt-realtime-whisper** — streaming partial transcript、$0.017 / 分
- OpenAI **gpt-realtime-translate** — 70+ 入力 → 13 出力言語の同時翻訳 STT、$0.034 / 分
- Deepgram Nova-3 — $0.0048 / 分 streaming、騒音下に強い
- ElevenLabs Scribe v2 Realtime — ~150 ms、90+ 言語
- バッチ用途: [insanely-fast-whisper](/blogs/posts/2026/03/2026-03-25-insanely-fast-whisper/) — Whisper large-v3 + Flash Attention 2 で 150 分音声を 98 秒

### S2S / full-duplex

- OpenAI **gpt-realtime-2** — GPT-5 級 reasoning 内蔵、128K context、barge-in / 並列ツール呼び出し
- Kyutai **Moshi** — OSS、理論 160 ms / 実測 200 ms、Apple Silicon (iPhone / Mac) で on-device 推論
- Sesame **CSM** — Apache-2.0、Llama backbone + Mimi decoder。会話履歴（音声含む）で prosody を条件付け
- Hume **EVI 3** — 30 種の感情・スタイルを生成、9 種中 8 種の感情を識別。2025-05-29 リリース
- Google **Gemini Live API** — Gemini 2.5 Flash Native Audio。音声 + 画像のマルチモーダル S2S、70 言語、barge-in
- Deepgram **Voice Agent API** — STT + LLM + TTS をラップ。$0.075 / 分 (= $4.50 / 時) LLM 利用料込み

## 用途別の選び方

| 要件 | 第一候補 |
|---|---|
| 日本語の表現品質を最優先 | irodori-TTS-500M-v2 / gpt-realtime-2 / Gemini Live |
| 最短 TTFA | ElevenLabs Flash v2.5 / Cartesia Sonic-3 |
| クラウド S2S が必要 | gpt-realtime-2 |
| OSS / on-device S2S | Moshi / Sesame CSM |
| 感情解釈付き対話 | Hume EVI 3 |
| 音声 + 画像のマルチモーダル | Gemini Live |
| パッケージ運用 (繋ぎ込み不要) | Deepgram Voice Agent API / ElevenLabs Conversational AI |

## 関連ページ

- [OpenAI Realtime API](/blogs/wiki/tools/openai-realtime-api/) — gpt-realtime-2 / Translate / Whisper を含む統合 API
- [Cartesia](/blogs/wiki/tools/cartesia/) — 低レイテンシ TTS の本命
- [ElevenLabs](/blogs/wiki/tools/elevenlabs/) — Flash / Eleven v3 / Scribe / Conversational AI
- [投機的 TTS（Speculative TTS）](/blogs/wiki/concepts/speculative-tts/) — AR codec LM の推論を 1.4〜5× 速くする手法群
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — voice agent はその音声 I/O 版
- [Video Use](/blogs/wiki/tools/video-use/) — ElevenLabs Scribe を使った動画編集ワークフロー

## ソース記事

- [TTS/STT モデル最前線 2026-05: gpt-realtime-2 / Whisper Streaming と双方向系 voice model 群雄割拠](/blogs/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/) — 2026-05-12
- [Mistral Voxtral TTS: ElevenLabs に匹敵するオープンウェイト音声AI](/blogs/posts/2026/03/2026-03-30-mistral-voxtral-tts/) — 2026-03-30
- [insanely-fast-whisper: 150分の音声を98秒で文字起こしする CLI ツール](/blogs/posts/2026/03/2026-03-25-insanely-fast-whisper/) — 2026-03-25
- [QwenVoice — Mac でボイスクローニング・感情表現・音声デザインを完全オフラインで実現する Qwen3-TTS アプリ](/blogs/posts/2026/03/2026-03-04-1a39b3cc62c29543a5e6de566017beeb/) — 2026-03-04
