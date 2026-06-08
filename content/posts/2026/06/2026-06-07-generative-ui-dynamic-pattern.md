---
title: "Generative UI に第 4 の選択肢 — yusukebe「AI時代のUIはどこへ行く？その2！」が提案する Dynamic パターン"
slug: "2026-06-07-generative-ui-dynamic-pattern"
date: 2026-06-07
lastmod: 2026-06-07
draft: false
author: "eotel"
model: "claude-opus-4-8"
description: "Hono 作者 yusukebe さんがフロントエンド・PHPカンファレンス北海道2026で発表した「AI時代のUIはどこへ行く？その2！」を読み解く。Generative UI を Static / Declarative / Open-ended のスペクトラムとして整理し、Cloudflare Dynamic Workers を使った第 4 の Dynamic パターンを提案する内容だ。"
categories: ["AI/LLM"]
tags: ["generative-ui", "cloudflare-workers", "dynamic-workers", "llm", "frontend"]
---

2026 年 6 月 6 日に札幌で開催された[フロントエンド・PHPカンファレンス北海道2026](https://fortee.jp/frontend-phpcon-do-2026)で、[Hono](https://hono.dev/) の作者であり Cloudflare に勤務する和田裕介（[yusukebe](https://github.com/yusukebe)）さんが「[AI時代のUIはどこへ行く？その2！](https://speakerdeck.com/yusukebe/aishi-dai-nouihadokohexing-ku-sono2)」というタイトルで登壇した。タイトルの通り、2025 年 9 月のフロントエンドカンファレンス北海道2025 での発表「[AI時代のUIはどこへ行く？](https://speakerdeck.com/yusukebe/aishi-dai-nouihadokohexing-ku)」の続編にあたる。

全 127 枚のスライドの主題はひとつ。**Generative UI（LLM の出力に応じて UI を動的に組み立てるアプローチ）の実装パターンをスペクトラムとして整理し、その上で第 4 の「Dynamic パターン」を提案する**ことだ。本記事ではスライドの流れを追いながら、提案の土台になっている Cloudflare Dynamic Workers まで掘り下げる。

## 前作のおさらい — 「Web UI は不要になる」への反論

前作（その1）の文脈を先に押さえておくと続編が読みやすい。2025 年時点で「チャットがすべての入口になるなら、Web ページや GUI はいらなくなるのでは」という UI 不要論が盛り上がっていた。それに対して前作は、**AI 時代でも UI は依然として必要で、変わるのは「UI の実装のされ方」**だという立場を取った。その上で、AI と UI の関係を「UI の中で AI を使う」「AI が UI を生成する」「AI が UI を受け取る」という複数のパターンに分け、Claude Artifacts や MCP UI の実例とともに示した。

続編はこのうち「**AI が UI を生成する**」、つまり Generative UI の深掘りだ。

## Generative UI のスペクトラム — 3 つの実装パターン

スライドの前半では、Generative UI の実装が 3 つのパターンに整理される。この 3 分類は [CopilotKit が "The Three Types of Generative UI" として整理しているもの](https://www.copilotkit.ai/blog/the-three-kinds-of-generative-ui)とほぼ対応しており、コミュニティで共通理解になりつつある分類だ。

| パターン | LLM が返すもの | UI の所有者 | 自由度 |
|---|---|---|---|
| **Static** | データ（値） | フロントエンド（事前定義のコンポーネント） | 低 |
| **Declarative** | UI の構造を表す宣言的スペック（JSON 等） | フロントエンド（スペックを自前で描画） | 中 |
| **Open-ended** | HTML/CSS/JavaScript そのもの | LLM（ホスト側はサンドボックスを提供するだけ） | 高 |

- **Static** は、LLM が返した値を事前に定義された UI に当てはめるだけ。表示は完全に開発者の管理下にあり、本番アプリで最も使いやすい
- **Declarative** は、LLM に「カード」「リスト」「フォーム」のような構造を JSON などで宣言させ、フロントエンドが自前のコンポーネントで描画する。AI がレイアウトを選べるが、描画の最終権限はフロントエンドに残る
- **Open-ended** は、LLM が HTML/CSS/JavaScript を丸ごと生成し、サンドボックス化された iframe の中で実行するパターン。AI の表現力は最大になるが、一貫性や安全性は犠牲になる

スライドではこれを一列に並べて「**右に行くほど AI の自由度が上がり、開発者の制御が下がるスペクトラム**」として提示する。加えて、パターンごとにストリーミング時の体験（UI が描画されていく過程の見え方）が大きく異なることも論点になっている。

下図は、このスペクトラムに次節で扱う第 4 の Dynamic パターンを先取りして並べたものだ。

![Generative UI スペクトラムの概念図。横軸の左端が開発者の制御、右端が AI の自由度を表し、Static、Declarative、Dynamic、Open-ended の 4 つのパターンカードがスペクトラム上に並ぶ。Dynamic パターンには NEW バッジが付いている](/blogs/images/generative-ui-dynamic-pattern-spectrum.png)

## 第 4 の提案 — Dynamic パターン

ここからが本題だ。スライド後半で yusukebe さんは、3 パターンに対する自身のスタンスを「Open-ended の自由さは好き、ただし自由すぎる」と表明した上で、**第 4 のパターンとして「Dynamic パターン」を提案**する。

アイデアの骨子はこうだ。

1. LLM に生の HTML/CSS/JavaScript を丸ごと書かせるのではなく、**もう少し抽象化されたコード**（React/JSX のようなコンポーネントコード）を書かせる
2. 生成されたコードを、**サーバー側のサンドボックスで動的にロードして実行**し、結果を UI として返す
3. 実行基盤には Cloudflare の **Dynamic Workers**（Worker Loader API）を使う

つまり、Declarative の「構造化されているが表現力に上限がある」と Open-ended の「自由だが制御不能」の間を取るポジションだ。宣言的スペックでは表現できないロジックやインタラクションをコードとして書かせつつ、生成物は完全な野放しではなく、フレームワークの抽象とサンドボックスの境界という二重の枠に収める。

発表内のデモでは、観光地案内・旅行プランナー的なアプリケーションで、天気やレストラン情報のような UI を LLM が動的に組み立てる様子が示された。なお同じ週に yusukebe さんは「[Dynamic Workersについて](https://speakerdeck.com/yusukebe/dynamic-workersnituite)」という発表（2026-06-03 公開）も行っており、こちらは基盤側の解説としてセットで読める。

## 基盤技術: Cloudflare Dynamic Workers

Dynamic パターンの実行基盤になっている Dynamic Workers は、Cloudflare が 2026 年 3 月 24 日のブログ「[Sandboxing AI agents, 100x faster](https://blog.cloudflare.com/dynamic-workers/)」（Kenton Varda、Sunil Pai、Ketan Gupta 共著）で発表した仕組みで、現在オープンベータとして提供されている。Worker の中から、実行時に与えたコードで**新しい Worker を専用サンドボックス付きで動的に生成できる** API だ。

以下は概形を示す擬似コードだ（`env.LOADER` が Worker Loader binding、`agentCode` は LLM が生成したコード文字列）。

```javascript
let worker = env.LOADER.load({
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: {
    "agent.js": agentCode, // LLM が生成したコード
  },
  env: { CHAT_ROOM: chatRoomRpcStub }, // 渡したい API だけを明示的に注入
  globalOutbound: null, // インターネットアクセスを遮断
});

await worker.getEntrypoint().myAgent(param);
```

ポイントは 3 つある。

- **起動の速さ**: サンドボックスの実体はコンテナや VM ではなく V8 の isolate で、Cloudflare はミリ秒単位で起動し数メガバイトのメモリで動く（典型的なコンテナ比で約 100 倍高速、メモリ効率は 10〜100 倍）と説明している。UI 生成のリクエストごとにサンドボックスを立てる、という使い方が現実的になる
- **能力の最小化**: 動的 Worker には `env` で明示的に渡したバインディングしか見えない。`globalOutbound: null` を指定すれば `fetch()` などの外向き通信も遮断できる（デフォルトは親 Worker のネットワークアクセスを継承する点に注意）
- **Code Mode の系譜**: Cloudflare は 2025 年 9 月に「AI エージェントはツール呼び出しを連発するよりコードを書いて API を呼ぶ方がよい」という [Code Mode](https://blog.cloudflare.com/code-mode/) のコンセプトを提示し、MCP サーバーを TypeScript API に変換してコードを書かせると、従来のツール呼び出し方式と比べて複雑なタスクではトークン使用量を 81% 削減できたと報告している。Dynamic Workers はその「エージェントが書いたコードをどこで安全に実行するか」への解答であり、Dynamic パターンはこの仕組みを UI 生成に転用したものと位置づけられる

なお、AI が生成した untrusted code の実行基盤としては、[microsandbox](/blogs/wiki/tools/microsandbox/) や E2B のような [microVM](/blogs/wiki/concepts/microvm/) ベースの選択肢もある（詳しくは[過去記事](/blogs/posts/2026/05/2026-05-25-microsandbox-microvm-isolation-for-ai-agents/)で扱った）。isolate は専用カーネルを持つ microVM より分離の壁が薄い分、桁違いに軽い。

Cloudflare 自身も V8 の脆弱性がハイパーバイザーより高頻度で見つかることを認めた上で、V8 パッチの即日デプロイや二層目のサンドボックスなど多層防御で補う設計を取っている。「どこまでの隔離が必要か」と「どれだけ高頻度にサンドボックスを起動するか」のトレードオフで選ぶ話であり、リクエストごとに UI コードを実行する Generative UI の文脈では isolate の軽さが効く。

## どのパターンを選ぶか

スライドは「結局どのパターンが正解か」という問いに対して、**ユースケースで選べばいい**という現実的な答えを出している。4 パターンを並べ直すとこうなる。

| パターン | 向いているケース | リスク・コスト |
|---|---|---|
| Static | ミッションクリティカルな業務 UI、一貫した UX が必須の本番アプリ | AI の関与が薄く、体験は保守的 |
| Declarative | 動的なダッシュボード、フォーム生成、マルチプラットフォーム描画 | スペックの表現力が上限になる |
| Dynamic | 構造化を超えるロジック・インタラクションを AI に組ませたいとき | 実行基盤（サンドボックス）の整備が前提 |
| Open-ended | プロトタイピング、実験的なツール | 一貫性・安全性・アクセシビリティの保証が難しい |

Generative UI の周辺では、Google の A2UI、AG-UI、MCP Apps といったプロトコルの標準化も同時並行で動いており、「AI とフロントエンドの間の契約をどの抽象度で結ぶか」はまさに今動いている論点だ。Dynamic パターンは、その契約を「宣言的スペック」と「生 HTML」の間にある「**抽象化されたコード + サンドボックス実行**」に置く提案として面白い。

## まとめ

- 「AI時代のUIはどこへ行く？その2！」は、Generative UI を **Static / Declarative / Open-ended のスペクトラム**として整理し、第 4 の **Dynamic パターン**を提案する発表
- Dynamic パターンは、LLM に抽象化されたコード（JSX 等）を書かせて **Cloudflare Dynamic Workers のサンドボックスで動的実行**するアプローチで、Declarative の制御と Open-ended の自由のいいとこ取りを狙う
- 基盤の Dynamic Workers は V8 isolate ベースでミリ秒起動・省メモリが売り。Code Mode（エージェントにコードを書かせる）の系譜にあり、「リクエストごとにサンドボックスを立てて UI を生成する」を現実的にする
- どのパターンが正解かはユースケース次第。制御と自由度のトレードオフ軸を持っておくと、Generative UI 系のツールやプロトコル（A2UI / AG-UI / MCP Apps）を評価しやすくなる

スライドは最後に、AI 時代の UI について考えるきっかけになれば、というメッセージで締められている。フロントエンドエンジニアが「AI に UI を明け渡すか」ではなく「AI にどの抽象度で UI を任せるか」を設計する時代が、もう来ているということだろう。

## 参考リンク

- [AI時代のUIはどこへ行く？その2！ - Speaker Deck](https://speakerdeck.com/yusukebe/aishi-dai-nouihadokohexing-ku-sono2)
- [AI時代のUIはどこへ行く？ - Speaker Deck](https://speakerdeck.com/yusukebe/aishi-dai-nouihadokohexing-ku)（前作）
- [Dynamic Workersについて - Speaker Deck](https://speakerdeck.com/yusukebe/dynamic-workersnituite)
- [Sandboxing AI agents, 100x faster - Cloudflare Blog](https://blog.cloudflare.com/dynamic-workers/)
- [Code Mode: the better way to use MCP - Cloudflare Blog](https://blog.cloudflare.com/code-mode/)
- [Dynamic Workers - Cloudflare Docs](https://developers.cloudflare.com/dynamic-workers/)
- [The Three Types of Generative UI - CopilotKit Blog](https://www.copilotkit.ai/blog/the-three-kinds-of-generative-ui)
- [フロントエンド・PHPカンファレンス北海道2026](https://fortee.jp/frontend-phpcon-do-2026)

## 関連 Wiki

- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/)
- [microVM](/blogs/wiki/concepts/microvm/)
- [microsandbox](/blogs/wiki/tools/microsandbox/)
- [AI エージェント](/blogs/wiki/concepts/ai-agent/)
