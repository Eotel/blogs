---
title: "sokol"
description: "Andre Weissflog (floooh) が開発する C 言語のクロスプラットフォーム軽量ライブラリ群。グラフィックス（Metal / DirectX / Vulkan / WebGPU / OpenGL）・オーディオ・入力をヘッダオンリーで提供"
date: 2026-05-11
lastmod: 2026-05-12
aliases: ["sokol", "sokol_gfx", "floooh/sokol"]
related_posts:
  - "/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/"
tags: ["c", "creative-coding", "graphics", "webgpu", "metal", "vulkan", "directx", "cross-platform"]
---

## 概要

[sokol](https://github.com/floooh/sokol) は Andre Weissflog（floooh）が開発する、C 言語ヘッダオンリーのクロスプラットフォーム・ライブラリ群。プラットフォーム抽象を最小コストで提供することを目的としており、**1 つのコードベースから Metal / D3D11 / Vulkan / WebGPU / GLCORE / GLES3 に直接コンパイルできる**点が特徴。**zlib ライセンス**で公開され、C99 互換、依存ゼロ。

## モジュール構成

| ヘッダ | 役割 |
|--------|------|
| `sokol_gfx.h` | グラフィックス（Metal / D3D11 / Vulkan / GLCORE / GLES3 / WebGL2 / WebGPU 抽象） |
| `sokol_app.h` | ウィンドウ・入力・イベントループ |
| `sokol_audio.h` | 低レイテンシオーディオ出力 |
| `sokol_time.h` | 高精度タイマー |
| `sokol_glue.h` | sokol_app と sokol_gfx の接続 |
| `sokol_debugtext.h` / `sokol_gl.h` | デバッグテキスト・即時モード GL ライク描画 |

各ヘッダは単一ファイルで、`SOKOL_IMPL` を定義した翻訳単位で実装が展開される（stb 系と同じ流儀）。

## 採用先

- [TrussC](/blogs/wiki/tools/trussc/) — sokol_gfx をバックエンドに据えた C++ クリエイティブコーディングフレームワーク
- [Bevy](https://bevy.org/) の一部ツール、[Oryol](https://github.com/floooh/oryol)（floooh 自身の上位フレームワーク）など
- WebAssembly 出力時の Web 向けゲーム/可視化プロジェクトでよく採用される

## 関連ツール: sokol-shdc

shader をプラットフォーム別に事前コンパイルする CLI ツール。`.glsl` から HLSL / MSL / SPIR-V / WGSL を生成する。TrussC では CMake 側が `.glsl` を検出すると自動で起動するように仕込まれている。

## 関連ページ

- [TrussC](/blogs/wiki/tools/trussc/) — sokol を採用した代表的なフレームワーク

## ソース記事

- [TrussC: openFrameworks に着想を得た sokol ベースの C++ クリエイティブコーディングフレームワーク](/blogs/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/) — 2026-05-11
