---
title: "Cartesia"
description: "State-space model 系の低レイテンシ TTS を提供する音声 AI ベンダー。Sonic-3 / Sonic Turbo は公称モデル単体 100 ms 未満で 40+ 言語に対応、笑い・感情・抑揚を含めた表現を低遅延のまま吐ける。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["Cartesia AI", "Sonic", "Sonic-3", "Sonic Turbo", "sonic-3"]
related_posts:
  - "/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/"
tags: ["Cartesia", "TTS", "音声AI", "state-space-model", "voice-cloning"]
---

## 概要

[Cartesia](https://cartesia.ai/) は **state-space model (SSM) ベースの音声合成** を商用 API で提供するベンダー。フラグシップ TTS **Sonic-3** は公称 **モデル単体 < 100 ms** の超低遅延を保ったまま、笑い・感情・抑揚を含む自然な発話を生成する。リアルタイム voice agent の音声出力レイヤーとして広く採用されている。

## モデル: Sonic-3 / Sonic Turbo

| 項目 | Sonic-3 |
|---|---|
| レイテンシ（公称） | モデル単体 **< 100 ms**（"next best の 4 倍速い" / 別箇所では ~90 ms と表現） |
| 言語 | **40+ 言語**（9 言語のインド語族を含む） |
| API | WebSocket streaming、複数 SDK、Playground |
| 価格 | ~$0.030 / 分相当（実体は 1 文字 = 1 credit、Pro Voice Cloning は 1.5 credit / 文字） |
| voice cloning | **Instant Voice Cloning** 10 秒録音から / Professional は学習込み |
| 認証 | SOC 2 Type II / HIPAA / PCI Level 1 |

State-space model は流れるような音声生成に向く設計で、Transformer 系の TTS より低遅延・低メモリで動く。Cartesia はこのアーキテクチャをいち早く商用化した点が独特。

## 設計の特徴

- **笑い・抑揚・効果音までを単一モデルで** 生成。Filler 単語や感嘆詞も自然に挿入される
- **acronym 読み分け**: "API" を `エー・ピー・アイ` と読むか `アピ` と読むかを文脈で判断
- **streaming 前提**: WebSocket で送り続けつつ、頭から少しずつ音声を取得できる

## 競合との位置づけ

| 観点 | Cartesia Sonic-3 | ElevenLabs Flash v2.5 | OpenAI gpt-realtime-2 |
|---|---|---|---|
| レイテンシ（モデル単体） | < 100 ms | ~75 ms | reasoning 設定依存 |
| 双方向 (S2S) | 単方向 TTS | 単方向 TTS | full-duplex |
| 言語 | 40+ | 32 (Flash) / 70+ (v3) | 多言語 |
| 強み | SSM による低遅延 + 感情表現 | 文字単価の安さと UI 連携 | 推論内蔵 |

## 関連ページ

- [リアルタイム音声モデル（TTS / STT / S2S）](/blogs/wiki/concepts/realtime-voice-model/) — Cartesia の業界全体での位置づけ
- [ElevenLabs](/blogs/wiki/tools/elevenlabs/) — 同じ「低レイテンシ TTS」枠の競合
- [OpenAI Realtime API](/blogs/wiki/tools/openai-realtime-api/) — full-duplex 統合型の対抗軸

## ソース記事

- [TTS/STT モデル最前線 2026-05: gpt-realtime-2 / Whisper Streaming と双方向系 voice model 群雄割拠](/blogs/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/) — 2026-05-12
