---
slug: 2026-05-13-package-manager-history-2026
title: "nix, mise, proto, devenv, devbox, ... package manager たちの歴史と盛衰"
date: 2026-05-13
lastmod: 2026-05-13
draft: false
author: "eotel"
model: "claude-opus-4-7"
categories: ["ツール/開発環境"]
tags: ["パッケージ管理", "Nix", "mise", "uv", "asdf", "Homebrew", "devenv", "開発環境"]
---

`uv` がほぼ全 Python プロジェクトの初期化スクリプトに入り、`mise` がチームの新人セットアップ手順に書かれ、`devenv` の `direnv` 統合が「Nix 知らなくても Nix 環境が立つ」体験を提供する。
2024 年から 2026 年にかけて、open source の「環境を再現するためのツール」が同時多発的にデファクト化が進んだ。

ただ、よく見るとこれらは別のレイヤから同じ問題に取り組んでいる。
35 年前の `apt` から今日の `uv` まで、扱う問題は「同じマシンに違うバージョンを共存させる」「同じプロジェクトをチームで再現する」に集約される。各時代はこの単一の問題に、層を変えながら違うアプローチを積み重ねてきた。

本稿は OS パッケージマネージャから dev container まで、その系譜を 6 つのレイヤに分けて俯瞰する。

![1993 年から 2026 年までの OS パッケージマネージャ・Nix 系・単一言語 version manager・polyglot version manager・モダン言語別 package manager・declarative dev environment を 6 レイヤに分けて並べたタイムライン図。apt、Homebrew、Nix、NixOS、asdf、mise、proto、uv、bun、devbox、devenv、Dev Containers などのツールを年代順に配置している。](/blogs/images/package-manager-history-timeline.png)

## 用語整理 — どのレイヤの話か

「package manager」は同名で違うものを指している。本稿では以下の 6 区分で扱う。

- **OS パッケージマネージャ** — システム全体の C ライブラリやバイナリを管理する。`apt` / `dnf` / `pacman` / `Homebrew` / `MacPorts`。
- **宣言的環境マネージャ (declarative)** — システム構成自体を関数として記述する。`Nix` / `NixOS` / `Guix`。
- **単一言語 version manager** — 1 言語のランタイムの複数バージョンを切り替える。`rvm` / `nvm` / `rbenv` / `pyenv` / `volta`。
- **polyglot version manager** — 複数言語のランタイムを統一インタフェースで管理する。`asdf` / `pkgx` / `mise` / `proto`。
- **言語別 modern package manager** — 言語の lockfile + パッケージインストールを高速化する。`pnpm` / `bun` / `rye` / `uv` / `pixi`。
- **declarative dev environment** — プロジェクト単位の環境（ツール + env vars）を宣言的に立ち上げる。`direnv` / `lorri` / `devbox` / `devenv` / `flox`。

これに「環境ごと隔離する」**コンテナベース dev environment**（Dev Containers / Codespaces）が直交する解として並走している。

## OS パッケージ層 — 系統樹の出発点

1993 年に Ian Murdock が Debian を立ち上げ、`dpkg` の上に `apt` の系統が生まれる。
Red Hat 系では `rpm` → `yum` → `dnf` と進化、Arch Linux は 2002 年に `pacman` をリリース。これらは「OS の所有物としてのパッケージ管理」である。root が必要で、システム全体が単一の状態を持つ。

macOS では事情が違った。Apple は公式の OS パッケージマネージャを出さなかったので、ユーザ空間で代替が立ち上がる。

- **MacPorts** — もともと 2002 年に Apple のエンジニアが **DarwinPorts** として開始。BSD の FreeBSD Ports をモデルにしている。2006 年 8 月、macOS（当時 Mac OS X）への注力を示すため MacPorts に改名。
- **Homebrew** — Max Howell が 2009 年 5 月 20 日に公開。`/usr/local` 配下でユーザー権限のまま動かす設計が受け、2010 年には GitHub で 3 番目に多くフォークされたリポジトリになった。

Homebrew の成功が示したのは、**「root を要求しないパッケージマネージャ」の需要**が大きいということだった。この発想は後の `Nix` / `asdf` / `mise` まで一貫して受け継がれる。

## 宣言的環境層 — Nix 系統

2003 年 6 月 15 日、Utrecht 大学の Eelco Dolstra が `Nix` の最初の公開版をリリースする。
2006 年に博士論文『The Purely Functional Software Deployment Model』としてまとまり、Nix は「ビルドを関数として記述し、入力ハッシュをパス名にする」というモデルを定式化した。

> Software deployment is the set of activities related to getting software components to work on the machines of end users. It includes activities such as installation, upgrading, uninstallation, and so on. Many tools have been developed to support deployment, but they all have serious limitations with respect to correctness.
> — Eelco Dolstra, *The Purely Functional Software Deployment Model* (Ph.D. thesis, Utrecht University, 2006)

この上に組み上がったのが:

- **nixpkgs** — Nix の上に乗る巨大なパッケージコレクション
- **NixOS** — 2008 年 ICFP で論文発表された Linux ディストリビューション。`/etc/nixos/configuration.nix` で OS 全体を宣言する
- **Guix** — 2012 年、GNU が Nix の思想を採用し Guile Scheme で書き直したフォーク
- **Flakes** — Nix 2.4 (2021) で導入された実験的機能。依存関係をロックする仕組みで、2026 年時点でも experimental 扱いだが事実上のデファクトとして使われている

Nix の最大の難点は学習曲線である。Nix 言語そのものが難しく、エラーメッセージも伝統的に厳しい。だから、Nix を「フロントエンドから隠す」ツールが 2022 年以降一気に出てくる（後述の devbox / devenv / flox）。

## 単一言語 version manager 時代 (2007-2014)

2000 年代後半、各言語コミュニティで同じパターンが繰り返された。「グローバルに 1 バージョンだけ入れる」のではなく、「プロジェクトごとに違うバージョンを使う」という需要である。

| ツール | 言語 | 作者 | GitHub 作成日 |
|---|---|---|---|
| rvm | Ruby | Wayne E. Seguin | 2009 頃 |
| nvm | Node.js | Tim Caswell | 2010-04-15 |
| rbenv | Ruby | Sam Stephenson | 2011-08-01 |
| pyenv | Python | Yamashita Yuu (rbenv からの fork) | 2012-08-31 |
| jenv / phpenv / goenv | 各種 | コミュニティ各種 | 2013-2014 |
| volta | Node.js | LinkedIn | repo 2017 / v1.0 2020 |

ここで起きていたのは **shim 戦争** である。`~/.rbenv/shims/ruby` のような「呼ばれたら本物を解決して exec する偽バイナリ」を `PATH` に挟む方式である。
`rvm` は shell function を上書きする派、`rbenv` は shim 派で、Ruby コミュニティはこの 2 派で割れた。最終的に「shim の方が shell 非依存で副作用が少ない」という理由で rbenv 流が勝ち、それを **言語ごとに再実装** していったのがこの時代である。

このパターンは結局のところ、各言語コミュニティが似たような shim ツールを別々に再実装する **shim 戦争** であった。

`volta` (LinkedIn が repo を 2017 年に公開、v1.0 は 2020 年末、Rust 製) は遅れて参戦したが、Node に特化したまま polyglot 化はしなかった。これは結果的に次のレイヤに役割を譲ることになる。

## polyglot version manager の登場 (2014-2024)

2014 年 11 月、Elixir コミュニティの Akash Manohar（HashNuke）が `asdf` をリリースする。
発想は単純で、「言語別に shim ツールを乱立させるのをやめて、1 つの shim で全部やる」。`~/.tool-versions` に書いた `nodejs 20.10.0` を読んでプラグインが解決する。

`asdf` は Elixir コミュニティ発だが、すぐに Ruby / Node / Python に広がり、2010 年代後半には「polyglot プロジェクトの標準」になった。

ただ、asdf には弱点があった。Bash で書かれているため起動が遅く、`shim` 経由のオーバーヘッドも大きい。これを解決する後継が 2023 年に同時多発する。

- **mise** — Jeff Dickey (jdx) が 2023 年 1 月 9 日に **rtx** という名前で公開した Rust 実装。2024 年 1 月 10 日のコミット `rename rtx-vm -> mise-en-dev` で `mise` にリネームされた。`.tool-versions` 互換のまま単一バイナリで起動を高速化し、`tasks` (`just` 風タスクランナー) と env var 管理を統合している。
- **proto** — 2023 年 2 月 17 日、`moonrepo` がリリース。同じく Rust 製。moonrepo の monorepo ビルドシステム `moon` のツールチェイン基盤として開発され、後にスタンドアロン化された。
- **pkgx** — 元 Homebrew 作者の Max Howell が **tea** として 2021 年 11 月に開始、後に pkgx にリネーム。`pkgx node@20 your-script.ts` のように「envをまたいで使いたいだけのコマンド」を 1 行で走らせる思想。

そして 2026 年現在、本家 `asdf` は **v0.16.0 (2025-01-30) で単一バイナリの Go 実装に書き換えられ**、コードベースの大半が Go に置き換わっている。Bash 実装の遅さに対する答えである。「Bash → Rust」「Bash → Go」という 2 つの再実装が並走しているのが今のスナップショットだ。

「衰」というよりは **設計思想の継承と再実装** が起きた、と言うほうが正確だろう。`asdf` の `.tool-versions` フォーマットは mise も読めるし、proto も互換読み込みを提供する。形式は残り、エンジンが入れ替わった。

## 言語別 modern package manager の "Rust 化" 波

並行して、各言語の **lockfile + パッケージインストーラ** 層でも大きな入れ替えが進んでいる。共通テーマは「Rust もしくは Zig で書き直して、グローバルキャッシュとハードリンクを駆使してインストール時間をオーダーで縮める」。

| ツール | 言語ターゲット | 作者・組織 | 初出 |
|---|---|---|---|
| pnpm | Node.js | Zoltan Kochan | 2017-06-28 |
| bun | Node.js / TypeScript | Jarred Sumner（Oven） | アナウンス 2021-09、v1.0 2023-09-08 |
| rye | Python | Armin Ronacher | 2023 |
| uv | Python | Astral (Charlie Marsh) | 2024-02-15 |
| pixi | Conda / 多言語 | prefix.dev | 2023 |

`pnpm` は「npm の node_modules を nested copy するな、グローバルキャッシュからハードリンクしろ」という単純で強力な発想で生まれた。
`bun` は JavaScript ランタイムと package manager を同時に再発明した。**2025 年 12 月 2 日、Bun の開発元 Oven は Anthropic への合流を発表した。** Bun は Anthropic 配下で開発が続き、ライセンスは MIT のままで、Claude Code および Claude Agent SDK の基盤としても利用される。

> TLDR: Bun has been acquired by Anthropic. Anthropic is betting on Bun as the infrastructure powering Claude Code, Claude Agent SDK, and future AI coding products & tools. ... Bun stays open-source & MIT-licensed.
> — Jarred Sumner, ["Bun is joining Anthropic"](https://bun.com/blog/bun-joins-anthropic) (2025-12-02)

Python 側は更にドラマチックだ。Flask / Sentry の作者である Armin Ronacher は 2023 年に `rye` を発表し、`pyproject.toml` 中心の体験を提示した。
そこに 2024 年 2 月、Charlie Marsh の Astral が `uv` を発表した。Ronacher は同年 8 月の記事 [Harvest Season](https://lucumr.pocoo.org/2024/8/21/harvest-season/) で、rye と uv の関係についてこう書いている。

> I can only re-iterate my wish and desire that Rye (and with it a lot of other tools in the space) should cease to exist once the dominating tool has been established. For me `uv` is poised to be that tool.
> — Armin Ronacher, *Harvest Season* (2024-08-21)

つまり、rye の役目は uv の登場とともに譲られるべきだという表明である。これは「衰」というより **意図された世代交代** に近い。

## declarative dev environment 層 — direnv から devenv まで

「言語ごとに version manager」「言語ごとに package manager」とは別に、**プロジェクトを cd しただけで環境が立ち上がる**という体験を追求する系譜がある。

- **direnv** — zimbatm が 2011 年 1 月 4 日に開始。`.envrc` に書いた shell スクリプトをディレクトリに入ると評価する、極めて素直なツール。今や全てのこのレイヤのツールの前提部品になっている。
- **lorri** — Tweag が Target Corporation の依頼で開発した、Nix shell の高速 evaluator。現在は `nix-community` に寄贈されている。2026 年 5 月時点の最新リリースは 2024 年 8 月の v1.7.1 で、`nix-direnv` の登場で主要な役目を譲った形だが、メンテは続いている。
- **devbox** — Jetify (旧 jetpack.io) が 2022 年 8 月 18 日に公開。「Nix のパワーを Nix 言語なしで使う」を売りに、`devbox.json` に欲しいパッケージを書くだけで Nix 由来の隔離環境が立つ。
- **devenv** — Domen Kožar（Cachix の創業者）が 2022 年 10 月 22 日に公開。`devenv.nix` を書くが、PostgreSQL の起動などは「サービスとして 1 行で declared」できる抽象を持つ。`devenv` 自身も Nix 実装から Tvix への移行を表明している。
- **flox** — Flox, Inc が 2022 年 12 月 22 日に公開した、エンタープライズ寄りの Nix ベース dev env マネージャ。共有環境のチームスケールに振った設計。

この層の重要な観察は、**lorri / devbox / devenv / flox の 4 つともが Nix を基盤にしている** ことだ。「Nix の powerful なところを残しつつ、Nix 言語を表に出さない」というのが 2022 年以降の dev env 戦争の本質である。Nix の "API" を新規に書き直すのではなく、Nix の上に新しい "UX" を被せた。

## container-based 開発環境 — もう一つの解

もう一つの直交軸として、「環境ごと隔離する」コンテナベースのアプローチがある。

- **Vagrant** — 2010 年、のちに HashiCorp を立ち上げる Mitchell Hashimoto が公開した VM ベース dev env ツール
- **Docker** — 2013 年、Linux コンテナを popularize
- **Dev Containers spec** — `devcontainer.json` 自体は 2019 年頃の VS Code Remote から存在。2022 年に Microsoft 主導でオープン仕様化
- **GitHub Codespaces** — 2021 年 GA、クラウド上の Dev Containers として実装

このルートは「ホスト OS にツールチェインを入れない」という哲学なので、上記の polyglot version manager 層と排他的だ。チームで「言語ごとに version 管理するのも、Nix を覚えるのも面倒。コンテナごと配ろう」という判断をしたなら、これで完結する。

## 層を貫く三度の地殻変動

35 年スパンで俯瞰すると、波が 3 回来ている。

**第 1 波 (2003-2010): ユーザ空間化**
`MacPorts` / `Homebrew` / `Nix` / `rvm` / `nvm`。「root が要らない」「OS 全体に依存しない」「複数バージョン共存できる」が共通テーマ。

**第 2 波 (2014-2018): polyglot 化と shim/lockfile 化**
`asdf` が単一言語 version manager を統合し、`pnpm` が node_modules の常識を疑い、`direnv` が「ディレクトリに入ると環境が立つ」を当然の前提にした。

**第 3 波 (2022-2026): Rust 化と declarative 化の合流**
`mise` / `proto` / `uv` / `bun` / `rye` の Rust（と Zig / Go）波と、`devbox` / `devenv` / `flox` の Nix フロントエンド波が、同じ 2022 年スタートで併走している。`asdf` 自体も Go に書き直された。
「速さは Rust か Go で」「再現性は Nix か Docker で」というふうに、目的と道具がはっきり対応するようになった。

## 役割マトリクス

代表ツールが「どこをカバーするか」を機能フラグで並べる。`◯` がメインで担当する領域、`△` が部分的にサポートする領域。

| ツール | OS pkg | 言語 version | lockfile | declarative | shell hook | container |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Homebrew | ◯ | △ | - | - | - | - |
| Nix / nixpkgs | ◯ | ◯ | △ (Flakes) | ◯ | - | - |
| asdf / mise | - | ◯ | △ | △ | △ | - |
| proto | - | ◯ | △ | △ | △ | - |
| direnv | - | - | - | - | ◯ | - |
| devbox / devenv / flox | △ | ◯ | ◯ | ◯ | ◯ (direnv) | - |
| uv / rye / pixi | - | △ (Python) | ◯ | △ | - | - |
| pnpm / bun | - | - | ◯ | - | - | - |
| Dev Containers | △ | ◯ | △ | ◯ | - | ◯ |

「ツール A vs ツール B」の比較が成立する場面は実は少なく、多くの場合は **layered combination** になる。例えば「mise + uv + direnv」「devenv 単独」「Dev Containers 単独」がそれぞれ別の解で、互いに置き換えられるものではない。

## 2026 年時点の推奨スタック (実務向け)

ここまでの整理を踏まえた、現時点での選好を列挙する。

- **Python 開発**: `uv` を main にする。`mise` を polyglot ハブとして併用。CI でも `uv` で済む。
- **Node / 多言語**: `mise` か `proto`。`.tool-versions` 互換が効くので、既に asdf を入れているチームは mise への移行が無痛。
- **NixOS / 強い再現性が必要**: `devenv` が学習曲線と機能のバランスが最も良い。チーム導入なら `flox`。
- **「言語チェーンを覚えるコストを払いたくない」開発**: `Dev Containers` + GitHub Codespaces で全部閉じる。
- **OS パッケージ自体**: macOS は引き続き Homebrew、Linux は OS 標準。`Nix` を OS パッケージ層として導入するのは、十分に Nix 信者である場合のみ。

## おわりに — "勝者なき定常状態" 仮説

過去 5 年間「これが勝者だ」と言われたツールはだいたい複数あった。`mise` も `proto` も健在で、どちらも「採用が伸びている」状態が並行して続いている。`devbox` と `devenv` と `flox` は被るレイヤを別の戦略で攻めていて、いずれも残るだろう。

これは「勝者がいないから混乱している」のではなく、**「この問題は複数の正しい答えを許容する」** という方が近い。OS 層、version manager 層、lockfile 層、declarative dev env 層、コンテナ層は本来直交している。ユーザーは複数を重ねて使えばよい。
そう考えると、ここ 35 年で起きてきた変化は「乱立」ではなく「**レイヤが整理されてきた歴史**」と読むほうが筋が通る。

次の波は、おそらく LLM ベースの coding agent が「どのレイヤをどう組み合わせるか」を自動で決める段になるだろう。2026 年現在では、`apm.yml` のような「エージェントが必要なパッケージを宣言する」形式が、その走りとして登場している（詳細は [APM (Agent Package Manager) — AI エージェント設定を npm のように管理する](/blogs/posts/2026/04/2026-04-17-apm-agent-package-manager/) を参照）。

## 関連 Wiki / 参考

- 既存 post: [nix](/blogs/posts/2025/01/2025-01-05-82cb06f0d6388a21ec3e8cadd36cde18/) / [uv](/blogs/posts/2025/01/2025-01-05-17269f63a6f363fbd18dd95de6522a73/)
- 隣接 Wiki: [APM (Agent Package Manager)](/blogs/wiki/tools/apm/)

### Wiki 化候補トピック（`/wiki-ingest` 用メモ）

- `concepts/declarative-dev-environment` — direnv / devbox / devenv / flox の共通モデル
- `concepts/polyglot-version-manager` — asdf / mise / proto / pkgx の共通設計
- `tools/mise` — Rust 製 polyglot version manager
- `tools/devenv` — Nix-backed dev env マネージャ
- `tools/uv` — Astral の Python パッケージ管理
- `concepts/shim-vs-env` — shim 方式と shell hook 方式の比較
