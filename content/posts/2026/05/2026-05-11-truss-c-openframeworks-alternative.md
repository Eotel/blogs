---
title: "TrussC: openFrameworks に着想を得た sokol ベースの C++ クリエイティブコーディングフレームワーク"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "TrussC は openFrameworks に着想を得た sokol ベースの C++20 クリエイティブコーディングフレームワーク。OpenGL 非依存、MCP サーバのコア組み込み、シーングラフ＝アプリ本体、ホットリロード自動分割など、コードを読まないと見えない独自性まで踏み込んで整理する。"
categories: ["ツール/開発環境"]
tags: ["truss-c", "openframeworks", "c++", "creative-coding", "sokol", "webgpu", "mcp"]
---

## TL;DR

[TrussC](https://github.com/TrussC-org/TrussC) は openFrameworks に着想を得つつ、レンダリングを [sokol](https://github.com/floooh/sokol) に寄せて作り直された C++ クリエイティブコーディングフレームワークだ。OpenGL に依存せず、macOS では Metal、Windows では DirectX、Linux では Vulkan、Web では WebGPU で動く。C++20・ヘッダオンリー中心・MIT ライセンス。

ただし表層の「oF 代替」だけでは見落とすポイントがいくつもある。`App` クラスがシーングラフのルート、MCP サーバがコアに組み込まれていて起動するだけで AI から操作できる、ホットリロードがマクロ 1 行で有効化される、Color が OKLab/OKLCH を含む 5 つの色空間を標準装備する、など、リポジトリの中を見てはじめて見える設計判断が並ぶ。

## きっかけ: Image Cast #255

Podcast [Image Cast](https://podcasts.apple.com/ga/podcast/255-trussc%E3%81%A8%E3%81%84%E3%81%86%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F-%E4%BB%8A%E5%B9%B4%E8%B2%B7%E3%81%A3%E3%81%A6%E8%89%AF%E3%81%8B%E3%81%A3%E3%81%9F%E3%82%82%E3%81%AE/id1542436827?i=1000742819000) の第 255 回は「今年買って良かったもの」を扱う年末回だが、その中で開発者本人が自作フレームワーク TrussC を紹介している。openFrameworks の経験がある人にとっては気になる立ち位置のプロジェクトなので、本記事では公式情報に加えてリポジトリのコードを実際に読みながら整理する。

## openFrameworks との表層差分

まずよく宣伝されている話から。[公式サイト](https://trussc.org/ja/) のキャッチコピー「GPU ネイティブなクリエイティブコーディング。sokol ベース。」が端的に物語っている。

- **OpenGL 非依存**: 描画は [sokol_gfx](https://github.com/floooh/sokol) を経由して、macOS の Metal / Windows の DirectX / Linux の Vulkan / Web の WebGPU といったモダンなグラフィックス API に直接乗る。
- **C++20 / ヘッダオンリー中心**: 主要機能はヘッダだけで使える。`sokol`、`stb`、`miniaudio`、`nlohmann/json`、`pugixml`、`cpp-httplib` など依存はすべて `core/include/` に同梱されており、別途パッケージ管理は不要。
- **CMake + GUI プロジェクトジェネレータ**: VSCode / Cursor / Xcode / Visual Studio 向けのプロジェクトを GUI からクリック操作で生成できる。
- **`TAU` を第一級に**: 円定数は `TAU (τ = 2π)` が標準。`PI` を使うと `[[deprecated]]` 属性によりコンパイラ警告が出る。
- **MIT ライセンス**: 依存ライブラリも MIT / zlib / Public Domain に揃えてあり、商用利用の互換性に配慮している。

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

## コードを開いて気づく独自性

ここからが本題。`core/include/` を実際に読むと、oF とはずいぶん性格の違うフレームワークだということが見えてくる。

### 1. `App` はシーングラフのルートノード

`core/include/tcBaseApp.h` の冒頭にこう書かれている。

```cpp
// App - Application base class
// Inherits from tc::RectNode and functions as scene graph root node
// Size is synchronized with window size
class App : public RectNode {
public:
    virtual ~App() = default;
    void setSize(float w, float h) override { ... }
    virtual void keyPressed(int key)   { (void)key; }
    virtual void mousePressed(Vec2 pos, int button) { ... }
    ...
};
```

oF の `ofApp` は単独クラスで、独自のシーングラフを使いたければ自作する必要があるが、TrussC は **`App` 自体がシーングラフのルート** になっている。`tcNode.h` ベースで `std::shared_ptr<Node>` を子に持ち、`drawTree()` / `updateTree()` で再帰呼び出し、マウス入力はノードへ自動 dispatch する。Unity の `MonoBehaviour` ルートに近い感覚で、コールバック名は oF と揃いつつも内部構造はまったく別物だ。

### 2. MCP サーバがコアに組み込まれている

最大の特徴がこれ。`core/include/tc/utils/tcMCP.h` の冒頭にはこうある。

```cpp
// tcMCP.h - Model Context Protocol (MCP) Server Implementation
// HTTP transport via cpp-httplib. Requests arrive on a worker thread and are
// forwarded to the main (GL) thread through ThreadChannel + promise so that
// tool handlers can safely access graphics state.
namespace trussc { namespace mcp {
    struct ToolArg { std::string name, type, description; bool required = true; };
    class Tool {
    public:
        std::string name;
        std::function<json(const json&)> handler;
        ...
    };
}}
```

ユーザは自分のアプリ関数を MCP ツールとして登録するだけで、**TrussC アプリ自体が AI から JSON-RPC で叩ける MCP サーバになる**。受信は worker thread、グラフィックスステートへのアクセスは `ThreadChannel + promise` で main(GL) thread にディスパッチされる、というスレッド境界まで設計されている。openFrameworks にも Processing にも cinder にもない、明らかに 2025〜2026 年向けの設計判断だ。

### 3. ホットリロードがマクロ 1 行

`core/include/tc/app/tcHotReload.h` にはホットリロード用のマクロが用意されていて、ユーザのコードは以下の 2 行で済む。

```cpp
// MyApp.cpp
TC_HOT_RELOAD(MyApp);     // .dylib/.so を生成

// main.cpp
return TC_RUN_APP(MyApp, settings);
```

CMake 側でソースを全 scan し、`TC_HOT_RELOAD` マクロを検出すると Host (EXE) + Guest (dylib/so) に**自動でビルドを分割**して `dlopen/dlsym` でロードするしくみ。サポートは macOS/Linux で、Windows/Web/iOS/Android は静的フォールバックという棲み分けになっている。oF の追加プラグインで頑張る世界とはまったく違う方向だ。

### 4. Color は 5 つの色空間を持つ

`core/include/tcColor.h` の冒頭コメント:

```
Color (sRGB) ↔ ColorLinear ↔ ColorOKLab ↔ ColorOKLCH
        ColorHSB (sRGB-based)
```

sRGB / Linear に加えて、知覚的に均等な補間ができる **OKLab / OKLCH** を標準で持つ。`srgbToLinear` / `linearToSrgb` のガンマ変換、`fromBytes` / `fromHex` などのファクトリも同ファイルに揃っている。oF の `ofColor` は基本 RGB/HSB なので、ここはかなり踏み込んだ近代化だ。

### 5. TAU と PI のコードレベルの扱い

`core/include/tcMath.h` の実装はそのまま読むのが早い。

```cpp
constexpr float TAU = 6.28318530717958647693f;
constexpr float HALF_TAU = TAU / 2.0f;
constexpr float QUARTER_TAU = TAU / 4.0f;
[[deprecated("Use TAU instead. PI = TAU/2, but TAU is more intuitive for rotations.")]]
constexpr float PI = HALF_TAU;
```

`PI` は互換のために残してあるが `[[deprecated]]` 属性付きで、使うとコンパイラから警告が飛ぶ。`deg2rad(deg) = deg * TAU / 360`、`rad2deg(rad) = rad * 360 / TAU` といったヘルパも TAU ベースで書かれていて、設計思想がコード全体で一貫している。

### 6. 3D は PBR + IES まで踏み込んでいる

`core/include/tc/3d/` を見ると、`tcEasyCam.h`（oF の `ofEasyCam` 互換コメント明記）、`tcMaterial.h`、`tcLight.h`、`tcEnvironment.h`、`tcMeshPbrPipeline.h`、`tcIesProfile.h`（IES 光源プロファイル）まである。3D は「あとから足された機能」というよりは、PBR ベースのライティングが前提になった設計に見える。

### 7. `trusscli` 自身が TrussC アプリ

プロジェクトジェネレータの実体は `tools/` ディレクトリにある。`tools/CMakeLists.txt` を読むと:

```cmake
project(trusscli)
include(${TRUSSC_DIR}/cmake/trussc_app.cmake)
add_compile_definitions(TRUSSC_SHOW_CONSOLE)
trussc_app(NAME trusscli DISPLAY_NAME "TrussC Project Generator")
```

つまり、TrussC のプロジェクトを作るための GUI ツールが、**TrussC 自身で書かれている**（C++ の自己ホスト構成）。Python スクリプトでもシェルスクリプトでもなく、ドッグフーディングとして TrussC で TrussC のツールを書いている。

ユーザプロジェクト側の CMakeLists も同じ仕組みで、

```cmake
include(${TRUSSC_DIR}/cmake/trussc_app.cmake)
trussc_app()
```

の 2 行で済む。内部では C++20 強制、`src/**/*.{cpp,h,mm,m}` の自動収集、`.glsl` を検出したら sokol-shdc を自動起動、Xcode/VS の source_group 設定までやってくれる。CMake を書きたくない世界観だ。

## 対応プラットフォーム

公式サイト時点では以下のように示されている。

| プラットフォーム | バックエンド | ステータス |
| --- | --- | --- |
| macOS 14+ | Metal | 対応 |
| Windows | DirectX | 対応 |
| Linux | Vulkan | 対応 |
| Web | WebGPU | 対応 |
| iOS | Metal | 計画中 |

## 同梱アドオンと周辺リポジトリ

`addons/` 配下に同梱されているアドオンは現状以下の 12 個。命名規約は oF の `ofx*` と一対一対応の `tcx*`。

- `tcxBox2d`、`tcxCurl`、`tcxGltf`、`tcxHap`、`tcxImGui`、`tcxLua`、`tcxLut`、`tcxObj`、`tcxOsc`、`tcxQuadWarp`、`tcxTls`、`tcxWebSocket`

これらは oF と違って **各アドオンが自分の `CMakeLists.txt` と `addon.json` を持つ自己完結 CMake target** になっている。例えば `addons/tcxImGui/CMakeLists.txt` ではプラットフォーム別の `imgui_impl_*.{mm,cpp}` を切り替え、`target_link_libraries(tcxImGui PUBLIC TrussC)` で TrussC コアにリンクしている。

[TrussC-org](https://github.com/orgs/TrussC-org/repositories) には、上記同梱とは別に以下の周辺リポジトリが並んでいる:

- `tcxOpenCV`、`tcxNDI`、`tcxGPT`、`tcxAruco` — 外部依存が大きめのアドオン群
- `TrussSketch` — TrussC 上の何らかのアプリ（要追跡）
- `TrussC_Development_Skill` — Claude Code 等向けの開発スキル配布
- `trussc-addons` — 公式アドオンレジストリ的なリポジトリ
- `trussc.org` — ランディングサイト本体

`tcxGPT` という名前のアドオンがある時点で、AI 連携がコア機能だけでなく周辺にも広がっているのが分かる。

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

ぱっと見は「sokol ベースの oF 代替」だが、コードを開くと印象が大きく変わる。`App` がシーングラフのルートを兼ね、MCP サーバがコアに組み込まれ、ホットリロードがマクロ 1 行で有効化される — これらは「openFrameworks をモダン化した」ではなく、**「2025〜2026 年に新しく作るならこう書く」を真面目に詰めた結果** に見える。

oF 互換 API という入口を残しつつ、AI 連携や色空間といった現代的な要求を最初から飲み込んでいる。`tcxGPT` のように AI 連携のアドオンが周辺に置かれているところを見ても、TrussC は「アプリ自体が AI から操作されることを前提にしたクリエイティブコーディング基盤」というポジションを目指していそうだ。実装の安定度や周辺エコシステムはこれからだが、設計判断としては触っておく価値が十分にある。

## 関連リンク

- [TrussC GitHub](https://github.com/TrussC-org/TrussC)
- [公式サイト（日本語）](https://trussc.org/ja/)
- [API リファレンス](https://trussc.org/reference/)
- [examples 一覧](https://trussc.org/examples/)
- [Discord](https://discord.gg/7MRRny56VQ)
- [Image Cast #255](https://podcasts.apple.com/ga/podcast/255-trussc%E3%81%A8%E3%81%84%E3%81%86%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%9F-%E4%BB%8A%E5%B9%B4%E8%B2%B7%E3%81%A3%E3%81%A6%E8%89%AF%E3%81%8B%E3%81%A3%E3%81%9F%E3%82%82%E3%81%AE/id1542436827?i=1000742819000)
- [sokol](https://github.com/floooh/sokol) — TrussC が採用するグラフィックスバックエンド
