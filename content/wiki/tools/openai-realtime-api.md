---
title: "OpenAI Realtime API"
description: "OpenAI が提供する音声・テキスト・ツール呼び出しを一元化した低遅延双方向 API。2026-05 に gpt-realtime-2 / gpt-realtime-translate / gpt-realtime-whisper の 3 モデルが揃った。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["gpt-realtime", "gpt-realtime-2", "gpt-realtime-whisper", "gpt-realtime-translate", "OpenAI Realtime", "Realtime API"]
related_posts:
  - "/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/"
tags: ["OpenAI", "Realtime API", "TTS", "STT", "音声AI"]
---

## 概要

OpenAI Realtime API は、音声・テキスト・ツール呼び出しを単一の双方向接続で扱う API。WebSocket または WebRTC で接続し、聴く・考える・喋るを 1 つの session 上で同時並行する **full-duplex** の voice agent を構築できる。2026-05-07 のアップデートで、reasoning 内蔵モデル `gpt-realtime-2` と、streaming STT・同時翻訳の 2 兄弟が出揃った。

## モデル群（2026-05 時点）

| モデル | 役割 | 価格 | 主な特徴 |
|---|---|---|---|
| **gpt-realtime-2** | S2S / TTS / STT (統合) | 入力 $32 / M tokens（cached $0.40 / M）、出力 $64 / M tokens | GPT-5 級 reasoning、128K context、reasoning effort を `minimal / low / medium / high / very-high` で調整、barge-in、並列ツール呼び出し |
| **gpt-realtime-translate** | STT + 同時翻訳 | $0.034 / 分 | 70+ 入力言語 → 13 出力言語に話速を保ったままライブ翻訳 |
| **gpt-realtime-whisper** | streaming STT | $0.017 / 分 | 音声が来た瞬間に部分書き起こしを返す。latency / accuracy のトレードオフを開発者側で調整可 |

3 モデルとも Realtime API の WebSocket / WebRTC エンドポイントから利用する。従来の `/v1/audio/transcriptions` (バッチ) とは別経路。

## gpt-realtime-2 の更新点

前世代 `gpt-realtime` 1.5 からの主要な変化:

- **context window**: 32K → **128K tokens**。長い multi-turn と複雑なエージェントタスクを 1 session に詰められる
- **reasoning effort**: 5 段階で「考える深さ」を切り替え。デフォルトは `low`
- **進捗の言語化**: ツール呼び出し中に "checking your calendar" のように口頭でステータスを漏らす設計。「考えるあいだの沈黙」が消える
- **parallel tool calls**: 複数ツールを並列に発火できる
- ベンチ: Big Bench Audio (high effort) で前世代比 +15.2 ポイント、Zillow が adversarial call-success rate を 69% → 95% に改善と報告

## API スタイル

接続例:

```
wss://api.openai.com/v1/realtime?model=gpt-realtime-2
```

または WebRTC 経由で `/v1/realtime/calls`。クライアント側からは音声フレームを送りつつ、サーバから interleaved な「部分書き起こし」「ツール呼び出し」「音声応答」「テキスト応答」が同じストリームで降ってくる。

## 関連ページ

- [リアルタイム音声モデル（TTS / STT / S2S）](/blogs/wiki/concepts/realtime-voice-model/) — 業界全体での位置づけ
- [Cartesia](/blogs/wiki/tools/cartesia/) — 低レイテンシ TTS の対抗馬
- [ElevenLabs](/blogs/wiki/tools/elevenlabs/) — Conversational AI で voice agent オーケストレーション層を提供
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — voice agent の上位概念

## ソース記事

- [TTS/STT モデル最前線 2026-05: gpt-realtime-2 / Whisper Streaming と双方向系 voice model 群雄割拠](/blogs/posts/2026/05/2026-05-12-tts-stt-frontier-2026-05/) — 2026-05-12
