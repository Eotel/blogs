---
title: "microsandbox の仕組み — libkrun の microVM で AI エージェントのコードを隔離実行する"
slug: "2026-05-25-microsandbox-microvm-isolation-for-ai-agents"
date: 2026-05-25
lastmod: 2026-05-25
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "AI エージェントが生成したコードをどう安全に走らせるか。microsandbox は libkrun ベースの microVM で各サンドボックスに専用カーネルを与え、シークレットを VM の外に置いたまま実行する self-hosted な OSS だ。仕組み・セキュリティモデル・E2B / Firecracker / Docker との違いを掘り下げる。"
categories: ["AI/LLM"]
tags: ["microsandbox", "microvm", "libkrun", "ai-agent", "security"]
---

AI エージェントにコードを書かせる時代になって、次に問題になるのは「**そのコードをどこで走らせるか**」だ。エージェントが生成したスクリプトには、依存パッケージのインストールから任意のシェルコマンド実行まで何でも入りうる。これをホスト上でそのまま走らせるのは論外だが、Docker コンテナに閉じ込めれば十分かというと、2026 年の感覚ではもう心もとない。

[microsandbox](https://github.com/superradcompany/microsandbox) は、この「untrusted code を安全かつ高速に実行する」課題に対して、**libkrun ベースの microVM** という解答を出している OSS だ。本記事では紹介よりも一歩踏み込んで、なぜ microVM なのか・シークレットをどう守るのか・既存の選択肢と何が違うのかを掘り下げる。

> 本記事は外部 OSS の調査記事です。執筆時点で microsandbox は beta（v0.4.6, 2026-05-13 リリース）であり、API やコマンドは変わりうる点に注意してください。

![ホストマシン1台の上に、半透明のガラス壁で隔離された複数のマイクロVMの箱が浮かび、各箱の中で小さなAIエージェントが専用のミニコンピュータとターミナルを操作している概念図](/blogs/images/microsandbox-microvm-isolation-for-ai-agents-hero.png)

## microsandbox とは何か

公式リポジトリは microsandbox を一言でこう説明する。

> the easiest way to give your agent their own computer

プロジェクトサイト [microsandbox.dev](https://microsandbox.dev/) のヘッドラインはさらに端的だ。

> Every agent deserves a computer.

「エージェントごとに 1 台のコンピュータを与える」というのが設計思想の中心にある。位置づけを整理すると次のようになる。

- **self-hosted / local-first** — 自分のマシン（あるいは自社インフラ）の上で動く。クラウドサービスへコードを送らない
- **embeddable** — アプリケーションのコードから直接 microVM を起動する。SDK が Rust / Python / TypeScript / Go 向けに用意されている
- **OCI 互換** — Docker Hub や GHCR などの標準コンテナイメージをそのまま起動できる
- **ライセンス** — Apache License 2.0
- **バッキング** — Y Combinator

公式 README は「why microsandbox」として以下の特徴を挙げている（逐語）。

> - Hardware Isolation: Hardware-level isolation with microVM technology.
> - Instant Startup: Average boot times under 100 milliseconds.
> - Embeddable: Spawn VMs right within your code. No setup server. No long-running daemon.
> - Secrets That Can't Leak: Unexploitable secret keys that never enter the VM.
> - OCI Compatible: Runs standard container images from Docker Hub, GHCR, or any OCI registry.
> - Long-Running: Sandboxes can run in detached mode. Great for long-lived sessions.
> - Agent-Ready: Your agents can create their own sandboxes with our Agent Skills and MCP server.

ここで効いてくるのが、上から 1 番目（ハードウェア分離）と 4 番目（シークレットが漏れない）の 2 点だ。この記事ではこの 2 つを中心に見ていく。

## なぜコンテナではなく microVM なのか

### 共有カーネルという攻撃面

Docker のような通常のコンテナは、ホスト OS の**カーネルを共有**し、namespace と cgroup で見える範囲とリソースを区切っているだけだ。アプリケーション同士は分かれて見えても、その下のカーネルは 1 つしかない。つまりカーネルに穴（脆弱性）があれば、コンテナの壁を越えてホストや他のコンテナへ侵入する余地が残る。

エージェントが生成した untrusted code を実行する文脈では、この「共有カーネル」が無視できない攻撃面になる。コンテナ脱出（container escape）・カーネルエクスプロイト・権限昇格は、実際に攻撃シナリオとして成立する。

### microVM は専用カーネルを持つ

microVM は、各サンドボックスが**自分専用の Linux カーネル**を持つ軽量な仮想マシンだ。ホストとの境界はソフトウェアの namespace ではなく、CPU のハードウェア仮想化機能（Linux なら KVM）で引かれる。これが README の言う "Hardware-level isolation"（ハードウェアレベルの分離）の意味であり、コンテナ脱出やカーネルエクスプロイトに対する壁がコンテナより一段厚くなる。

この microVM という発想自体は新しくない。AWS Lambda や Fargate を支える [Firecracker](https://github.com/firecracker-microvm/firecracker) が同じアプローチを取っており、「強い分離を保ちつつ VM の起動を極限まで速くする」という方向性は業界で実績がある。microsandbox はこの系譜に連なりつつ、Firecracker ではなく **libkrun** を採用している点が技術的な特色だ（README は依存として libkrun と smoltcp を明示している）。

### 「VM なのに速い」をどう成立させているか

microVM の弱点はコンテナより起動が遅いことだが、microsandbox は公式に次の数字を掲げる。

> Average boot times under 100 milliseconds.

平均 100 ミリ秒未満という起動時間は、エージェントが「実行のたびに使い捨ての箱を立てる」というワークロードに耐えるレベルだ。これを支えているのが libkrun という軽量な仮想化ランタイムで、フル仮想化のオーバーヘッドを抑えつつハードウェア分離を提供する。

ネットワークスタックに [smoltcp](https://github.com/smoltcp-rs/smoltcp)（Rust 製のユーザー空間 TCP/IP スタック）を使っているのもポイントで、これが後述するシークレット注入の制御点にもなっている。

## アーキテクチャ：daemon もサーバもいらない

microsandbox が E2B のようなクラウド型サンドボックスと一線を画すのは、**常駐サーバや daemon を前提にしない**点だ。README は embeddable の項目でこう言い切っている。

> No server to set up. No lingering daemon. It is all embedded and rootless!

つまり、別プロセスのデーモンを常時動かしておく必要も、root 権限を要求することもない。アプリケーションのプロセスから SDK 経由で microVM を直接起動し、使い終わったら畳む。インフラのセットアップなしに「コードの中で VM を起動する」体験が、self-hosted で完結する。

起動するイメージは OCI 互換なので、`python` でも `debian` でも Docker Hub / GHCR の標準イメージをそのまま指定できる。新しいフォーマットを覚える必要はない。

## セキュリティの核：シークレットを VM に入れない

microsandbox の機能のうち、もっとも差別化されているのがシークレットの扱いだ。README はこう謳う。

> Secrets That Can't Leak: Unexploitable secret keys that never enter the VM.

エージェントに API キーを使わせたいが、生成コードに API キーを直接渡すのは怖い、という状況を考えてほしい。素朴に環境変数で渡せば、エージェントが書いた（あるいは注入された）コードが環境変数を読むだけで鍵を抜き取れてしまう。プロンプトインジェクションでエージェントが乗っ取られた場合、これは即座にシークレット流出につながる。

microsandbox のアプローチは「**シークレットを VM の中に入れない**」というものだ。プロジェクトサイトは機能をこう表現している。

> Inject secrets only for approved TLS destinations

すなわち、本物のクレデンシャルはホスト側に置いたままにし、VM 内のプロセスからは見えないプレースホルダだけを渡す。VM が**許可された宛先への TLS 接続**を行うときに限り、ホスト側で本物の値を差し込む。こうすると、VM 内の悪意あるコードが環境変数を読んでも、そこには本物の鍵がない。許可されていない宛先（攻撃者のサーバなど）へ向けて鍵を送り出そうとしても、注入対象外なので持ち出し（exfiltration）が成立しない。

これは、前述の smoltcp によるユーザー空間ネットワークスタックを microsandbox が握っているからこそ成立する設計だ。ネットワークの出入りをホスト側で握っているので、「どの宛先に対してだけシークレットを実体化するか」を VM の外から決められる。

> シークレット管理の一般論（平文 `.env` の危うさ、just-in-time 供給）については [AI エージェント時代のシークレット管理](/blogs/wiki/guides/ai-agent-secret-management/) も参照。microsandbox は「実行サンドボックス側でネットワーク層から守る」アプローチで、1Password Unified Access のような「供給側で just-in-time に渡す」アプローチと補完関係にある。

## 使い方 — CLI と SDK で動かす（最小ハンズオン）

仕組みを押さえたところで、最小限の動かし方を見ておく。要件は次のとおり（逐語）。

> Linux with KVM enabled, or macOS with Apple Silicon.

### CLI で試す

CLI（`msb`）のインストールと最初の一発:

```sh
# インストールせずにワンショットで試す
npx microsandbox run debian

# あるいは msb をインストールして実行
msb run python -- python3 -c "print('Hello from a microVM!')"
```

名前付きサンドボックスを作って、コマンドを投げ、状態を見る一連の流れ:

```sh
msb create --name my-app python      # サンドボックスを作成
msb exec my-app -- python -c "import this"
msb ls                               # サンドボックス一覧
msb metrics my-app                   # CPU / メモリ / ネットワークの統計
```

### SDK から埋め込む

各言語の SDK 追加コマンドは README にまとまっている（逐語）。

```sh
cargo add microsandbox                                   # 🦀 Rust
uv add microsandbox                                      # 🐍 Python
npm i microsandbox                                       # 🟦 TypeScript
go get github.com/superradcompany/microsandbox/sdk/go    # 🐹 Go
```

Python SDK の最小例（README より）。`Sandbox.create` で microVM を起動し、コマンドを実行して、使い終わったら `stop_and_wait` で畳む:

```python
import asyncio
from microsandbox import Sandbox

async def main():
    sandbox = await Sandbox.create(
        "my-sandbox",
        image="python",
        cpus=1,
        memory=512,
    )

    output = await sandbox.exec("python", ["-c", "print('Hello from a microVM!')"])

    print(output.stdout_text)

    await sandbox.stop_and_wait()

asyncio.run(main())
```

「アプリのコードから VM を起動する」という embeddable の感覚が、この数行に凝縮されている。

## エージェントに繋ぐ：MCP サーバと Agent Skills

microsandbox は最初から「エージェントが自分でサンドボックスを立てる」ことを想定している。手段は 2 つ用意されている。

[MCP](/blogs/wiki/concepts/mcp/)（Model Context Protocol）サーバとして登録すれば、Claude Code などの MCP 対応エージェントから、サンドボックスのライフサイクル・コマンド実行・ファイルアクセス・モニタリングを構造化されたツール呼び出しとして扱える:

```sh
claude mcp add --transport stdio microsandbox -- npx -y microsandbox-mcp
```

Agent Skills 経由で組み込むこともできる:

```sh
npx skills add superradcompany/skills
```

README によれば、対応エージェントは Claude Code・Cursor・Codex・Gemini CLI・GitHub Copilot などをカバーする。エージェント側から見れば、「コードを安全に実行する箱」をツールとして手に入れることになる。

## E2B / Firecracker / Docker との違い

サンドボックス系の選択肢は 2026 年時点で増えている。代表的なものとの違いを整理する。

| | 隔離技術 | ホスティング | 性格 |
|---|---|---|---|
| **microsandbox** | libkrun の microVM（専用カーネル） | self-hosted / embeddable | 自社インフラで完結。シークレットをネットワーク層で守る OSS |
| **E2B** | Firecracker の microVM | マネージドクラウド | ephemeral な実行に強い。インフラ管理が不要な代わりにコードを外に出す |
| **Daytona** | Docker コンテナ | マネージド / セルフ | 状態保持（インストール済みパッケージや文脈の維持）に強い |
| **自前 Firecracker** | microVM | 自前運用 | 最も柔軟だが、ネットワーク・イメージ・ライフサイクルを自作する必要がある |

ざっくりした使い分けはこうだ。

- **コードを外部に出せない / 自社インフラで動かしたい** → microsandbox の self-host が効く
- **インフラを管理したくない・スケールをベンダーに任せたい** → E2B のようなマネージド型
- **エージェントが状態を持ち越したい（パッケージや文脈を維持）** → Daytona のような永続コンテナ型
- **細部まで自分で握りたい** → 自前 Firecracker（ただし構築コストは高い）

複数の比較記事でも、microsandbox は「self-host したいチーム向けのオープンソース選択肢の 1 つ」として扱われている（[Beam](https://www.beam.cloud/blog/best-e2b-alternatives) / [Northflank](https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes) など）。ただし Beam は microsandbox を "experimental software" と位置づけ、「セキュアな実行コアとしては魅力的だが、フル機能の開発環境ではなく機能不足や粗い部分がある」と慎重に評価している点は補足しておく（前述のとおり公式自身も beta を明言している）。なお E2B は Firecracker ベースで起動が速い一方、マネージドゆえの制約（セッションが短命という整理）がある、と語られている。

## 注意点

最後に現実的な注意を 2 つ。

1. **beta である** — README は明示的にこう警告している。

   > Microsandbox is still beta software. Expect breaking changes, missing features, and rough edges.

   本番採用では API・コマンドの変更を前提に、バージョンを固定して追従する運用が要る。

2. **要件がある** — KVM が有効な Linux、または Apple Silicon の macOS が必要だ。KVM の使えない環境（一部のクラウド VM やネステッド仮想化が無効なホスト）では動かせない。

## まとめ

microsandbox は「AI エージェントに untrusted code を実行させる」という 2026 年的な課題に対して、

- **libkrun の microVM** で専用カーネルによるハードウェア分離を与え、
- **平均 100ms 未満**の起動でコンテナ並みの体験に近づけ、
- **シークレットを VM の外に置く**ことでプロンプトインジェクション経由の鍵流出を構造的に防ぎ、
- **daemon もサーバも不要**な self-hosted / embeddable な形で提供する、

という設計を取っている。「クラウドにコードを出したくないが、コンテナの共有カーネルでは不安」という層にとって、self-host できる microVM サンドボックスの有力な選択肢だ。beta である点だけは織り込みつつ、エージェント基盤の「実行レイヤ」をどう固めるかを考えるうえで、一度触っておく価値がある。

## 関連 Wiki

- [MCP（Model Context Protocol）](/blogs/wiki/concepts/mcp/) — エージェントと外部ツール（microsandbox サーバ含む）を繋ぐプロトコル
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 自律実行する AI システムの全体像
- [AI エージェント時代のシークレット管理](/blogs/wiki/guides/ai-agent-secret-management/) — シークレットを平文で渡さないための対策

## 出典

- [microsandbox（GitHub）](https://github.com/superradcompany/microsandbox)
- [microsandbox.dev（公式サイト）](https://microsandbox.dev/)
- [Best E2B Alternatives — Beam](https://www.beam.cloud/blog/best-e2b-alternatives)
- [Daytona vs E2B — Northflank](https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes)
