---
slug: 2026-05-08-agent-friendly-cli-for-llm
title: "Agent-friendly CLIとは何か: ncliに学ぶLLM時代のCLI設計"
description: "ncliを題材に、LLMやCoding Agentが安全に扱えるCLIの設計条件を、MCP・ACP・JSON出力・エラー設計・認証の観点から整理する。"
date: 2026-05-08
lastmod: 2026-05-08
draft: false
author: "eotel"
categories: ["AI/LLM"]
tags: ["llm", "mcp", "coding-agent", "agent-friendly-cli", "ncli"]
---

Coding Agent が日常的にコードを書き、調査し、外部サービスを更新するようになると、CLI の意味が少し変わってくる。人間がターミナルで便利に叩くための道具から、LLM が安全に読めて、失敗から復帰できて、スクリプトにも組み込める「実行可能なインターフェース」へ寄っていく。

その流れをよく表しているのが、逆瀬川ちゃん氏の「[全Notion利用者のための、Coding Agentに対応したCLIを作った話](https://nyosegawa.com/posts/notion-cli-for-coding-agent/)」で紹介されている `@sakasegawa/ncli` だ。これは Notion の Remote MCP を CLI として包み、Claude Code や Codex のような Coding Agent が使いやすいように出力、ヘルプ、エラー、認証を設計した実装である。

この記事では `ncli` の紹介にとどめず、「CLI for LLM」または「Agent-friendly CLI」という設計領域がどこへ向かっているのか、既存実装やフレームワークと比べながら整理する。読み終わるころには、Agent が扱いやすい CLI の設計チェックリストとして使えるはずだ。

## CLI for LLMとは何か

ここでは、LLM や [AI エージェント](/blogs/wiki/concepts/ai-agent/) が扱うことを前提にした CLI を「Agent-friendly CLI」と呼ぶ。Agent-friendly CLI は、単に `--json` が付いた CLI ではない。LLM が何度も試行錯誤しながら使うことを前提にした、機械可読な契約である。

人間向け CLI は、多少の曖昧さを人間が補える。エラーが雑でも検索できるし、TTY に色や罫線が出ても読める。対して Coding Agent は、毎回の出力を次の入力に変換する。そこで重要になるのは、見栄えよりも以下の性質だ。

- stdout が安定したデータとして読める
- stderr と exit code で失敗の種類を判断できる
- `--help` とエラーヒントだけで次の行動が分かる
- 認証、権限、確認が非対話実行でも詰まらない
- 未対応機能へ逃げる escape hatch がある

これは CLI を「人間が読む画面」ではなく、「Agent が呼び出すローカルツール API」として扱う発想に近い。

## なぜ今CLIなのか

[MCP](/blogs/wiki/concepts/mcp/) は、外部ツールやデータソースを AI アプリケーションへ接続する標準として広がっている。公式ドキュメントでも、MCP は host、client、server の構成で、Tools、Resources、Prompts などの primitive を JSON-RPC でやり取りする仕組みとして説明されている（[Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)）。Transport も stdio と Streamable HTTP が定義されており、Remote MCP のような hosted server も自然に扱える（[Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)）。

一方で、MCP をそのまま Agent に大量接続すると、ツール定義や説明がコンテキストを圧迫しやすい。特に Remote MCP は便利だが、ローカルで中継して段階的に公開する余地が少ない。そこで CLI が再評価される。CLI なら、Agent は必要になったタイミングで `--help` を読み、必要なコマンドだけを実行できる。MCP の巨大な道具箱を常時プロンプトへ載せる代わりに、CLI を薄い実行面として使うわけだ。

この流れは Notion だけではない。たとえば [mcporter](https://mcporter.sh/) は MCP server を CLI や TypeScript client として扱えるようにし、`--json` では stdout を安定した JSON envelope に、進捗や警告は stderr に流す設計を明示している。[acpx](https://github.com/openclaw/acpx) は Agent Client Protocol (ACP) の headless CLI client として、Coding Agent 同士を PTY scraping ではなく構造化プロトコルで接続しようとしている。[Omi CLI の agent 向けドキュメント](https://docs.omi.me/doc/developer/cli/agents)は、JSON 出力、exit code、retry semantics を「stable agent contract」として文書化している。ここでいう headless とは、ブラウザや人間の操作画面に依存せず自動実行できること、stable agent contract とは Agent 側が分岐できる安定した入出力契約のことだ。

つまり「LLM 用 CLI」は、MCP と競合するというより、MCP や ACP の上に置ける現実的な操作面になりつつある。

## ncliが示す設計

`ncli` は [GitHub README](https://github.com/nyosegawa/notion-cli) で「CLI wrapper for Remote Notion MCP」と説明されている。特徴は、Notion の Remote MCP をそのまま Agent に見せるのではなく、Notion 操作として自然なコマンド体系へ変換している点だ。

インストールは npm package として提供されている。

```bash
npm install -g @sakasegawa/ncli
```

基本の流れは、検索して、取得して、作成または更新することだ。

```bash
ncli login
ncli search "project plan"
ncli fetch <id>
ncli page create --title "New Page" --parent <page-id>
```

この設計で重要なのは、MCP tool 名をそのまま CLI の中心にしないことだ。Notion の作業者が考える単位は、`page create`、`db query`、`comment list`、`meeting-notes query` のようなドメイン操作である。Agent にとっても、意味のある noun-verb のコマンド体系のほうが探索しやすい。

ただし、すべてを高レベルコマンドに閉じ込めると、未対応機能で詰まる。そこで `ncli api <tool> [json]` のように MCP tool を直接呼べる escape hatch を残している。これは Agent-friendly CLI にとってかなり重要な設計だ。抽象化は便利だが、Agent は穴に落ちたとき、自力で低レイヤーへ降りられる必要がある。

たとえば database に page を作る場面では、Agent が `page create` をいきなり実行して parent の指定を間違えるかもしれない。そのとき `ncli` は「database へ追加するなら先に `fetch` して `data_source_id` を取得せよ」という Hint を返す。これは人間向けの親切なエラーであると同時に、Agent にとっては次に実行すべきコマンド候補になる。

## 既存のNotion CLIと何が違うのか

既存の Notion CLI は、多くの場合 Notion REST API の薄いラッパーとして作られてきた。古い community CLI には、`NOTION_TOKEN` を渡して page や database の CRUD を行い、table、csv、json などを出力するものがある。これは人間やスクリプトには便利だが、Agent の復帰戦略までは主眼ではない。

Notion 側も公式に AI Agent 向けの動きを進めている。[makenotion/skills](https://github.com/makenotion/skills) には `notion-cli` skill があり、Notion CLI (`ntn`) を worker、public API request、file upload のために使う説明が置かれている。また Notion Docs は、Remote MCP を OAuth で接続できる hosted server として説明しており、Claude Code、Cursor、VS Code、ChatGPT などの AI tool と連携できるとしている（[Notion MCP](https://developers.notion.com/guides/mcp/mcp)）。

`ncli` の違いは、この二つの間にある。

- Remote MCP の OAuth と workspace access を CLI から使う
- Notion 操作として自然なコマンドに再編する
- Agent が読む前提で JSON とエラーヒントを整える
- REST API や file upload のような MCP 外の穴も escape hatch として残す
- Skill は補助にし、CLI 単体でも `--help` とエラーで使えるようにする

Notion Docs には Remote MCP の制約も明記されている。たとえば Remote MCP は user-based OAuth が必要で、完全な headless automation には向かない場合がある。また、現時点では Notion MCP は file upload をサポートしておらず、必要なら file upload API を使うことになる（[Connecting to Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp)）。`ncli` が MCP と REST API の両方を扱う理由は、この制約にも合っている。

## 他の実装・フレームワークとの比較

Agent-friendly CLI の実装は、いくつかの型に分けられる。

| 型 | 例 | 主な役割 |
| --- | --- | --- |
| ドメイン特化 CLI | `ncli`, `omi-cli` | 特定サービスを Agent が操作しやすい契約にする |
| MCP portable layer | `mcporter` | 任意の MCP server を CLI、型付き client、生成 CLI として扱う |
| Agent-to-Agent CLI | `acpx` | Coding Agent を ACP 経由で headless に操作する |
| Agent app framework CLI | `mcp-agent` | Agent/MCP server の scaffold、deploy、運用を行う |
| AI tool skill | `makenotion/skills` | Agent に CLI の使い方やワークフローを教える |

`mcporter` は汎用層で、MCP server の schema や tool call を CLI と typed client に変換する。これは「MCP を毎回 Agent に丸ごと読ませる」問題への答えになる。一方、`ncli` は Notion というドメインに寄せて、`page`、`db`、`view` のような概念を前面に出す。汎用性よりも、失敗しにくい操作モデルを優先している。つまり `ncli` は「MCP を CLI 化する」だけでなく、「Notion で何をしたいか」という作業モデルへ翻訳している。

`acpx` はさらに違う。対象は Notion や Linear のような SaaS ではなく、Codex や [Claude Code](/blogs/wiki/tools/claude-code/) のような Coding Agent そのものだ。ACP は JSON-RPC で session、prompt、update、cancel などをやり取りする protocol で、PTY の文字列を読み取るのではなく、構造化された agent session を扱う（[ACP overview](https://agentclientprotocol.com/protocol/overview)）。これは「CLI for LLM」が単なる外部 API 操作にとどまらず、Agent orchestration の面にも伸びていることを示している。

`mcp-agent` の CLI は、アプリケーションや MCP server を scaffold、deploy、install する運用面の CLI だ（[CLI Reference](https://docs.mcp-agent.com/reference/cli)）。これは Agent が呼ぶ道具というより、Agent を作る人間と CI が使う管理 CLI に近い。

## 重要な設計ポイント

Agent-friendly CLI を作るなら、最初に決めるべきは「きれいな画面」ではなく「契約」だ。条件は大きく、入出力、エラー、ヘルプ、escape hatch、認証、コンテキスト、安全性の7つに分けられる。

### stdoutとstderrを分ける

Agent が読むデータは stdout に置く。進捗、警告、debug log は stderr に置く。TTY のときだけ色を出し、pipe されたら装飾を消す。`--json` を指定したら stdout は JSON だけにする。これは地味だが、最も効く。

Omi CLI のように、JSON mode では stdout に単一 JSON document、stderr に JSON error、exit code に失敗種別を割り当てる設計は、Agent harness が分岐しやすい。

### エラーはWhat、Why、Hintにする

Agent は「失敗した」だけでは直せない。必要なのは、何が起きたか、なぜ起きたか、次に何をすべきかだ。

```text
Error: notion-create-pages failed
Why: parent page was not found
Hint: fetch the database first and use the data_source_id as collection://<id>
```

この形式なら、Agent は次の手として `fetch` を実行できる。エラーメッセージは単なる説明ではなく、次の tool call を誘導するプロンプトになる。

### helpを段階的にする

Agent は最初から長いドキュメントを読まない。`tool --help`、`tool subcommand --help`、`tool subcommand action --help` のように段階的に深くできるほうがよい。トップレベルには全体像と quick start、深い階層には flag、例、前提条件、次のステップを置く。

### escape hatchを残す

高レベル CLI は、便利なぶんカバレッジの穴ができる。そこで `api`、`raw`、`--data` のような escape hatch が必要になる。これは「抽象化を破れる道」ではなく、Agent が未対応操作で止まらないための安全弁だ。

### 認証をAgent実行モデルに合わせる

OAuth は人間の初回セットアップには自然だが、CI や cloud worker では詰まりやすい。API key は headless automation に向くが、scope と漏えい対策が重要になる。Notion Remote MCP は OAuth 前提で便利だが、完全無人実行には向かない場面がある。CLI はこの差を明示し、profile、env var、token storage、permission scope を設計に含める必要がある。

### コンテキストを節約する

MCP server の tool schema を常時すべて読ませるより、CLI の skill には「まず `--help` を読め」「Search → Fetch → Act の順で進めよ」くらいの短い方針を置くほうが軽い。詳細は実行時に CLI から取り出せる。Agent-friendly CLI は、ドキュメントをプロンプトへ詰め込まない設計でもある。

これは [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) の観点でも重要だ。Agent の能力はモデル単体ではなく、どの情報をいつ渡し、どの実行面へ接続するかで大きく変わる。

### 安全性をCLIの契約に入れる

Agent は指示されたら書き込み操作まで進む。だから、dry-run、confirmation、idempotency key、timeout、rate limit の扱い、権限不足時のメッセージ、破壊的操作の明示が重要になる。MCP の Streamable HTTP transport でも Origin validation、localhost bind、authentication が security warning として挙げられている。CLI でも同じように、実行境界を明確にする必要がある。

## これから増えそうなCLIの形

今後増えるのは、次のような CLI だと思う。

1つ目は、SaaS ごとの Agent-first CLI だ。Notion、Linear、GitHub、Slack、Google Drive のようなサービスに対して、人間向け UI でも raw API でもない、Agent が探索しやすいコマンド面を提供する。

2つ目は、MCP server から CLI を生成する層だ。`mcporter` のように schema を読んで、型、help、JSON output、OAuth cache をまとめて用意する。ドメイン特化 CLI を毎回手書きするより速い。

3つ目は、Agent orchestration CLI だ。`acpx` のように、Agent を PTY ではなく protocol session として扱う。これは subagent、reviewer、researcher を外部プロセスとして安全に呼びたいときに効く。

4つ目は、Agent 向け doc contract を備えた普通の CLI だ。専用の AI 機能がなくても、`--json`、exit code、retry、profile、stderr discipline が整っていれば、Agent はかなり使いやすくなる。

## Agent-friendly CLIチェックリスト

最後に、実装時の確認項目としてまとめておく。

- `--json` 時の stdout は単一の機械可読 document だけになるか
- 進捗、警告、debug log は stderr に分離されているか
- exit code が usage、auth、not found、rate limit、server error を区別できるか
- エラーに What、Why、Hint が含まれているか
- `tool --help` から段階的に subcommand の使い方へ降りられるか
- 高レベル操作で足りないときに `api` や `raw` の escape hatch があるか
- headless 実行と人間の初回 OAuth を分けて説明しているか
- dry-run、idempotency、timeout、破壊的操作の確認が設計されているか
- Agent Skill や README に詰め込まず、詳細を CLI から取り出せるか

## まとめ

`ncli` の面白さは「Notion CLI を作った」ことだけではない。Remote MCP、REST API、OAuth、Agent Skill、構造化出力、エラーヒントを組み合わせて、LLM が外部サービスを操作するための CLI contract を具体化している点にある。

LLM 時代の CLI は、人間の入力を短くする道具ではなく、Agent の失敗を短くする道具になる。成功時は machine-readable、失敗時は recoverable、未対応時は escapable。そういう CLI は、人間にとっても結局使いやすい。

## 参考リンク

- [全Notion利用者のための、Coding Agentに対応したCLIを作った話](https://nyosegawa.com/posts/notion-cli-for-coding-agent/)
- [nyosegawa/notion-cli](https://github.com/nyosegawa/notion-cli)
- [npm: @sakasegawa/ncli](https://www.npmjs.com/package/@sakasegawa/ncli)
- [Notion MCP](https://developers.notion.com/guides/mcp/mcp)
- [Connecting to Notion MCP](https://developers.notion.com/guides/mcp/get-started-with-mcp)
- [Model Context Protocol: Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [Model Context Protocol: Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [mcporter](https://mcporter.sh/)
- [openclaw/acpx](https://github.com/openclaw/acpx)
- [Agent Client Protocol overview](https://agentclientprotocol.com/protocol/overview)
- [Omi CLI: For agents](https://docs.omi.me/doc/developer/cli/agents)
- [mcp-agent CLI Reference](https://docs.mcp-agent.com/reference/cli)
