---
title: "ElevenLabs"
description: "音声合成・音声認識・voice agent オーケストレーションを商用 API で提供する音声 AI ベンダー。Flash v2.5 (~75 ms TTS) / Eleven v3 (70+ 言語) / Scribe v2 Realtime STT / Conversational AI などのライン。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["11labs", "Eleven Labs", "Flash v2.5", "Eleven v3", "Scribe", "Scribe v2", "Conversational AI"]
related_posts:
  - "/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/"
  - "/posts/2026/04/2026-04-17-video-use-claude-code-video-editing/"
  - "/posts/2026/03/2026-03-30-mistral-voxtral-tts/"
tags: ["ElevenLabs", "TTS", "STT", "音声AI", "voice-cloning"]
---

## 概要

[ElevenLabs](https://elevenlabs.io/) は商用音声 AI ベンダー。TTS の Eleven v3 / Flash v2.5 / Turbo v2.5、STT の Scribe v2 / Scribe v2 Realtime、voice agent ラッパの Conversational AI、効果音生成、音楽生成までを単一の API スイートで提供する。低遅延 TTS と voice cloning の品質で広く採用されている。

## モデル群（2026-05 時点）

| モデル | 種別 | 主な特徴 | 用途 |
|---|---|---|---|
| **Eleven v3** | TTS（flagship） | 70+ 言語、5,000 文字までの長文、感情表現に強い | 朗読、podcast、long-form |
| **Eleven Multilingual v2** | TTS | 29 言語、最大 10,000 文字 | 多言語ナレーション |
| **Flash v2.5** | 低遅延 TTS | **~75 ms** (モデル単体)、32 言語、最大 40,000 文字 | リアルタイム voice agent |
| **Flash v2** | 低遅延 TTS (英語のみ) | ~75 ms、英語専用、30,000 文字 | 英語専用 agent |
| **Turbo v2.5 / v2** | 中遅延 TTS | 250〜300 ms。Flash と機能等価で非推奨化 | (Flash 推奨) |
| **Scribe v2** | バッチ STT | 90+ 言語、word-level timestamps | 文字起こし |
| **Scribe v2 Realtime** | streaming STT | **~150 ms**、90+ 言語 | リアルタイム書き起こし |
| **Eleven Music** | 音楽生成 | スタジオ品質 | BGM 生成 |
| **Text to Sound v2** | SFX 生成 | 効果音 | サウンドデザイン |

公式は Turbo を非推奨化し、低遅延が必要な全ケースで Flash v2.5 を推奨している。

## Conversational AI（voice agent ラッパ）

ElevenLabs 自身が提供する **voice agent オーケストレーション層**。STT (Scribe) + LLM (任意) + TTS (Flash) を 1 endpoint に束ね、barge-in や turn-taking を組み込み済みで提供する。Pipecat や LiveKit Agents を自前で組まなくても voice agent を立てられる、という立ち位置で [Deepgram Voice Agent API](#) と競合する。

## Scribe と動画ワークフロー

ElevenLabs Scribe は [Video Use](/blogs/wiki/tools/video-use/) などの動画編集ワークフローでも使われており、音声トランスクリプトを「LLM が動画を理解するための主インターフェース」として活用する設計パターンが広がっている。

## 関連ページ

- [リアルタイム音声モデル（TTS / STT / S2S）](/blogs/wiki/concepts/realtime-voice-model/) — TTS / STT / S2S の俯瞰
- [OpenAI Realtime API](/blogs/wiki/tools/openai-realtime-api/) — full-duplex S2S 側の対抗
- [Cartesia](/blogs/wiki/tools/cartesia/) — 低レイテンシ TTS のもう 1 つの本命
- [Video Use](/blogs/wiki/tools/video-use/) — ElevenLabs Scribe を使った動画編集スキル

## ソース記事

- [TTS/STT モデル最前線 2026-05: gpt-realtime-2 / Whisper Streaming と双方向系 voice model 群雄割拠](/blogs/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/) — 2026-05-12
- [Video Use — Claude Code で動画編集を完全自動化するオープンソーススキル](/blogs/posts/2026/04/2026-04-17-video-use-claude-code-video-editing/) — 2026-04-17
- [Mistral Voxtral TTS: ElevenLabs に匹敵するオープンウェイト音声AI](/blogs/posts/2026/03/2026-03-30-mistral-voxtral-tts/) — 2026-03-30
