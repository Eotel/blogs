---
title: "TrussC: openFrameworks に着想を得た sokol ベースの C++ クリエイティブコーディングフレームワーク"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "TrussC は openFrameworks に着想を得た sokol ベースの C++20 クリエイティブコーディングフレームワーク。OpenGL 非依存で Metal/DirectX/Vulkan/WebGPU に対応し、GUI プロジェクトジェネレータも備える。概要・特徴・始め方を整理する。"
categories: ["ツール/開発環境"]
tags: ["truss-c", "openframeworks", "c++", "creative-coding", "sokol", "webgpu"]
---

## TL;DR

[TrussC](https://github.com/TrussC-org/TrussC) は openFrameworks に着想を得つつ、レンダリングを [sokol](https://github.com/floooh/sokol) に寄せて作り直された C++ クリエイティブコーディングフレームワークだ。OpenGL に依存せず、macOS では Metal、Windows では DirectX、Linux では Vulkan、Web では WebGPU で動く。C++20・ヘッダオンリー中心・MIT ライセンス。

## きっかけ: Image Cast #255

Podcast [Image Cast](https://podcasts.apple.com/ga/podcast/255-trussc%E3%81%A8%E3%81%84%E3%81%86%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F-%E4%BB%8A%E5%B9%B4%E8%B2%B7%E3%81%A3%E3%81%A6%E8%89%AF%E3%81%8B%E3%81%A3%E3%81%9F%E3%82%82%E3%81%AE/id1542436827?i=1000742819000) の第 255 回は「今年買って良かったもの」を扱う年末回だが、その中で開発者本人が自作フレームワーク TrussC を紹介している。openFrameworks の経験がある人にとっては気になる立ち位置のプロジェクトなので、本記事では公式情報をもとに概要を整理する。

## openFrameworks と何が違うのか

[公式サイト](https://trussc.org/ja/) のキャッチコピー「GPU ネイティブなクリエイティブコーディング。sokol ベース。」が端的に物語っている。

- **OpenGL 非依存**: 描画は [sokol_gfx](https://github.com/floooh/sokol) を経由して、macOS の Metal / Windows の DirectX / Linux の Vulkan / Web の WebGPU といったモダンなグラフィックス API に直接乗る。
- **C++20 / ヘッダオンリー中心**: 主要機能はヘッダだけで使える。`sokol`、`stb`、`miniaudio` などの依存は `core/include/` に同梱されており、別途パッケージ管理は不要。
- **CMake + GUI プロジェクトジェネレータ**: VSCode / Cursor / Xcode / Visual Studio 向けのプロジェクトを、GUI からクリック操作で生成できる（もちろん CMake preset (`macos` / `windows` / `linux` / `web`) で CLI から直接実行することもできる）。
- **`TAU` を第一級に**: 円定数は `TAU (τ = 2π)` が標準。`PI` を使うと `[[deprecated]]` 属性によりコンパイラ警告が出る。`rotate(TAU * 0.25f)` で 1/4 回転、`rotate(TAU)` で 1 回転、と単位円のイメージにそのまま対応する。
- **MIT ライセンス**: 依存ライブラリも MIT / zlib / Public Domain に揃えてあり、商用利用の互換性に配慮した構成になっている。

oF を触ったことがあるなら、最小コードはほぼ素直に読める（以下は公式 README のサンプルそのまま）。

```cpp
#include "TrussC.h"
using namespace std;
using namespace tc;

class MyApp : public App {
    void draw() override {
        clear(0.1);  // Clear to dark gray
        setColor(1.0, 0.4, 0.4);
        drawCircle(getWindowWidth() / 2, getWindowHeight() / 2, 100);
    }
};

int main() {
    WindowSettings settings;
    settings.setSize(960, 600);
    settings.setTitle("My App");
    return runApp<MyApp>(settings);
}
```

## 対応プラットフォーム

公式サイト時点では以下のように示されている。

| プラットフォーム | バックエンド | ステータス |
| --- | --- | --- |
| macOS 14+ | Metal | 対応 |
| Windows | DirectX | 対応 |
| Linux | Vulkan | 対応 |
| Web | WebGPU | 対応 |
| iOS | Metal | 計画中 |

## 同梱依存とアドオン

- **同梱**: sokol、stb、miniaudio などが `core/include/` 配下に直接入っている。
- **Dear ImGui** は `tcxImGui` アドオンとして提供。`tcxOpenCV` / `tcxNdi` といった周辺アドオンも `TrussC-org` 配下に並ぶ。
- 派生プロジェクトとして `TrussC-dll`、`sokol-dll-trussc`、`TrussC-nim` といったリポジトリもあり、他言語からの利用や DLL 配布を意識した広がり方になっている。

## 始め方

公式 README では、プロジェクトジェネレータ経由と CMake 直接実行の 2 通りが提示されている。

```bash
git clone https://github.com/TrussC-org/TrussC.git
cd TrussC

# 1) GUI プロジェクトジェネレータ（推奨）
# macOS
tools/build_mac.command
# Linux: tools/build_linux.sh
# Windows: tools/build_win.bat

# 2) CMake で example を直接ビルド（macOS の例）
cd examples/graphics/graphicsExample
cmake --preset macos    # windows / linux / web も同様
cmake --build build-macos --parallel
```

`examples/` 配下と [trussc.org/examples](https://trussc.org/examples/) で 50 以上のサンプルが公開されている。API リファレンスは [trussc.org/reference](https://trussc.org/reference/)。

## 開発体制

- 主開発: [**tettou771 (Toru Takata)**](https://github.com/tettou771) — 東京在住、個人ブログは [tettou771.com](http://tettou771.com/)。
- コミュニティ: [Discord](https://discord.gg/7MRRny56VQ)。
- リポジトリ: [TrussC-org/TrussC](https://github.com/TrussC-org/TrussC)（MIT、2025-12-14 公開）。

## 所感

openFrameworks の書き味は好きだが、OpenGL 縛りやプロジェクト作成まわりの古さに引っかかっていた、という人にとって、TrussC の「sokol で受け止め直す」方針は率直に魅力的に映る。`TAU` を第一級に置くといった設計の決め方も含めて、2025〜2026 年に新規でクリエイティブコーディング基盤を組むならこういう輪郭になるはず、というモダン C++ 寄りの宣言として読める。実装の安定度や Linux/Web の成熟度はこれからだが、新しいおもちゃとして触っておく価値は十分にありそうだ。

## 関連リンク

- [TrussC GitHub](https://github.com/TrussC-org/TrussC)
- [公式サイト（日本語）](https://trussc.org/ja/)
- [API リファレンス](https://trussc.org/reference/)
- [examples 一覧](https://trussc.org/examples/)
- [Discord](https://discord.gg/7MRRny56VQ)
- [Image Cast #255](https://podcasts.apple.com/ga/podcast/255-trussc%E3%81%A8%E3%81%84%E3%81%86%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F-%E4%BB%8A%E5%B9%B4%E8%B2%B7%E3%81%A3%E3%81%A6%E8%89%AF%E3%81%8B%E3%81%A3%E3%81%9F%E3%82%82%E3%81%AE/id1542436827?i=1000742819000)
- [sokol](https://github.com/floooh/sokol) — TrussC が採用するグラフィックスバックエンド
