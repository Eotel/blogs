---
title: "TrussC"
description: "openFrameworks に着想を得た sokol ベースの C++20 クリエイティブコーディングフレームワーク。OpenGL 非依存・MCP サーバのコア組み込み・シーングラフ＝App・ホットリロード自動分割が特徴"
date: 2026-05-11
lastmod: 2026-05-11
aliases: ["TrussC", "trussc", "tcx"]
related_posts:
  - "/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/"
tags: ["truss-c", "creative-coding", "c++", "openframeworks", "sokol", "webgpu", "mcp"]
---

## 概要

[TrussC](https://github.com/TrussC-org/TrussC) は openFrameworks（oF）に着想を得つつ、レンダリングを [sokol](/blogs/wiki/tools/sokol/) に寄せて作り直された C++20 クリエイティブコーディングフレームワーク。OpenGL に依存せず、macOS では Metal、Windows では DirectX、Linux では Vulkan、Web では WebGPU で動く。**MIT ライセンス、ヘッダオンリー中心、依存ライブラリすべて同梱**で、2025-12-14 に公開された。主開発者は tettou771（東京）。

## 表層の差分（oF 比）

- **OpenGL 非依存**: 描画は sokol_gfx 経由でモダンなグラフィックス API に直接乗る
- **C++20 / ヘッダオンリー中心**: `core/include/` に sokol、stb、miniaudio、nlohmann/json、pugixml、cpp-httplib などを同梱、別パッケージ管理は不要
- **CMake + GUI プロジェクトジェネレータ**: VSCode / Cursor / Xcode / Visual Studio 向けプロジェクトを GUI から生成
- **`TAU` が第一級**: 円定数は `TAU (τ = 2π)` 標準、`PI` は `[[deprecated]]` でコンパイラ警告
- **MIT ライセンス**: 依存も MIT / zlib / Public Domain に揃えて商用互換性に配慮

最小コードは oF とほぼ同じ感覚で書ける:

```cpp
#include "TrussC.h"
using namespace tc;

class MyApp : public App {
    void draw() override {
        clear(0.1);
        setColor(1.0, 0.4, 0.4);
        drawCircle(getWindowWidth()/2, getWindowHeight()/2, 100);
    }
};

int main() {
    WindowSettings settings;
    settings.setSize(960, 600);
    return runApp<MyApp>(settings);
}
```

## コードを読まないと見えない独自性

### App がシーングラフのルートノード

`tcBaseApp.h` で `class App : public RectNode` と定義されており、`App` 自体がシーングラフのルート。oF の `ofApp` は単独クラスだが、TrussC は `drawTree()` / `updateTree()` で子ノードへ再帰呼び出し、マウス入力もノードへ自動 dispatch する。Unity の `MonoBehaviour` ルートに近い感覚。

### MCP サーバがコアに組み込まれている

`tc/utils/tcMCP.h` に [MCP](/blogs/wiki/concepts/mcp/)（Model Context Protocol）サーバ実装が同梱されており、**ユーザがアプリ関数を MCP ツールとして登録するだけで、TrussC アプリ自体が AI から JSON-RPC で叩けるサーバになる**。HTTP transport は cpp-httplib、worker thread での受信を `ThreadChannel + promise` で main(GL) thread にディスパッチする設計まで作り込まれている。openFrameworks / Processing / cinder にはない 2025〜2026 年向けの設計判断。

### ホットリロードがマクロ 1 行

```cpp
TC_HOT_RELOAD(MyApp);              // .dylib/.so を生成
return TC_RUN_APP(MyApp, settings);
```

CMake 側がソースを scan して `TC_HOT_RELOAD` を検出すると、Host (EXE) + Guest (dylib/so) に**自動でビルドを分割**して `dlopen/dlsym` でロード。macOS/Linux でサポート、Windows/Web/iOS/Android は静的フォールバック。

### Color が 5 つの色空間を持つ

`tcColor.h` は `Color (sRGB) ↔ ColorLinear ↔ ColorOKLab ↔ ColorOKLCH` に加え `ColorHSB` を標準装備。知覚的均等補間の OKLab / OKLCH まで含む点が `ofColor` との大きな差。

### trusscli 自身が TrussC アプリ

プロジェクトジェネレータ `trusscli` は `tools/CMakeLists.txt` で `trussc_app(NAME trusscli ...)` と書かれており、**TrussC で書かれている**（ドッグフーディング）。ユーザプロジェクト側も `trussc_app()` の 1 行で C++20 強制・ソース自動収集・`.glsl` 検出時の sokol-shdc 自動起動などが効く。

## 対応プラットフォーム

| プラットフォーム | バックエンド | ステータス |
|------------------|--------------|------------|
| macOS 14+ | Metal | 対応 |
| Windows | DirectX | 対応 |
| Linux | Vulkan | 対応 |
| Web | WebGPU | 対応 |
| iOS | Metal | 計画中 |

## 同梱アドオン

oF の `ofx*` と一対一対応の `tcx*` 命名規約。現状 12 個:

`tcxBox2d` / `tcxCurl` / `tcxGltf` / `tcxHap` / `tcxImGui` / `tcxLua` / `tcxLut` / `tcxObj` / `tcxOsc` / `tcxQuadWarp` / `tcxTls` / `tcxWebSocket`

各アドオンが自分の `CMakeLists.txt` と `addon.json` を持つ自己完結 CMake target になっている点が oF との差。周辺リポジトリには `tcxOpenCV` / `tcxNDI` / `tcxGPT` / `tcxAruco` などがある。

## 始め方

```bash
git clone https://github.com/TrussC-org/TrussC.git
cd TrussC

# 1) GUI プロジェクトジェネレータ
tools/build_mac.command     # macOS
# tools/build_linux.sh / tools/build_win.bat

# 2) CMake で example を直接ビルド
cd examples/graphics/graphicsExample
cmake --preset macos
cmake --build build-macos --parallel
```

`examples/` 配下と [trussc.org/examples](https://trussc.org/examples/) に 50 以上のサンプル。API リファレンスは [trussc.org/reference](https://trussc.org/reference/)。

## 関連ページ

- [sokol](/blogs/wiki/tools/sokol/) — TrussC が採用するグラフィックス／プラットフォーム抽象ライブラリ
- [MCP](/blogs/wiki/concepts/mcp/) — TrussC のコアに組み込まれている AI 連携プロトコル

## ソース記事

- [TrussC: openFrameworks に着想を得た sokol ベースの C++ クリエイティブコーディングフレームワーク](/blogs/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/) — 2026-05-11
