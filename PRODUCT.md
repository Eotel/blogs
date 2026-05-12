# Product

## Register

brand

## Users

日本語を読む技術者・エンジニア。検索流入や SNS シェア経由で 1 記事だけ読みに来る通行人と、Wiki 経由で関連知識を辿るリピーターが混在する。多くは仕事中・隙間時間にスマホかノート PC で開き、技術的な結論と裏付けを素早く拾いに来る。コードブロック、図、外部リンクを「読む」だけでなく「コピーする・追跡する」用途で消費する。

Job to be done:

- ある技術トピックの「現時点での実用的なまとめ」を、書き手の判断付きで手早く把握する。
- Wiki から concept / tool / guide の三層を行き来し、自分のメンタルモデルを更新する。
- 後で見返すために URL を保存する、または他者にシェアする。

## Product Purpose

Eotel が日々の業務・実験・読書から得た知見を、Gist と GitHub Issue を一次ソースに自動取り込みパイプラインで記事化し、Wiki と相互リンクされた長期ナレッジベースとして公開する「働いているノートブック (a working notebook)」。サイト名は **Eotel's Notebook**。

このサイトが成功している状態:

- 検索や SNS から流入した読者が、目当ての記事だけでなく Wiki / 関連 posts までナチュラルに辿れている。任意の 1 ページが網の中の 1 ノードであることが視覚的に伝わっている。
- 著者本人（Eotel）が「あの件はノートに書いてある」と URL を共有でき、過去記事を将来の自分の参照先として再利用できている。
- hdknr 由来の歴史的ストック (783 件) と、Eotel が新たに書く記事が、デザイン上ノイズなく共存している（移管された遺産を見せ消ししない）。
- 自動化パイプライン（`blog-batch.sh`、`/blog`、`/wiki-ingest` 等）の存在が、読者には透けず、UI ノイズにならない。
- digital garden / TIL / learn-in-public の系譜に属することが、デザインから読み取れる。「個人テックブログ」一般のテンプレに見えない。

## Brand Personality

3 words: **engineer-curious / hypertext-dense / quietly-beautiful**

- **Engineer-curious**: 一次情報・ソースコード・実測値に当たる態度。煽りや AI ハイプを排し、引用は明示する。
- **Hypertext-dense**: Scrapbox 並みのリンク密度を design intent として持つ。post / wiki / category / tag が網目を張り、読者は「網のどこからでも入って、どこへでも抜けられる」状態が常にある。リンクを増やすことで本文を支える、引くと崩れる。
- **Quietly-beautiful**: Medium 級の serif typography とフィルム grain がかかった warm parchment の地で、装飾を増やさずに「これは丁寧に組まれた notebook だ」と一目でわかる。派手さの逆方向に振り切った美しさ。

Voice: 日本語、敬体寄りだがやや砕けて良い。「個人の作業ログ」と「他人の役に立つ要約」の中間。誇張・感嘆符の連打・絵文字装飾は避ける。section ラベルや UI コピーは英語 (Recent Notes / Index / Linked from など) で組み、本文は日本語で組むバイリンガル運用が基本。

## Anti-references

- 巨大ヒーロー + アニメーション + グラデーション CTA で構成された SaaS ランディング風テックブログ。記事より「自分というブランド」が先に出るタイプ。
- Qiita / Zenn の記事一覧ページのような、カードが等間隔に敷き詰められて区別がつかない一覧。
- 夜のネオン / グリッチ風「ハッカー感」演出、緑単色ターミナル風の hero。本ブログは AI/LLM・セキュリティを扱うが、その手の category-reflex デザインには寄せない。
- 「AI ブログ」を主張するパステル紫グラデと光彩エフェクト。
- 装飾としてだけ存在する横ストライプボーダー、グラスモーフィズム、グラデーションテキスト（impeccable の Absolute bans に該当）。
- 過剰な広告枠・購読 CTA・追従ソーシャル共有ボタン。

## Design Principles

1. **本文ファースト、シェルは控えめ**: ナビ・サイドバー・フッターは小さく、本文（serif typography とコードブロック）が画面の主役。
2. **Hypertext-first**: 全ての post と Wiki page が双方向の網の中の 1 ノード。post 末尾には "Linked from / Related in Wiki / More in <category>" が常にあり、Wiki page も同様に「ここを参照している post」「関連 Wiki」を見せる。Scrapbox のように、リンクが背骨。
3. **Beautiful as a working notebook**: 古い paper のような warm off-white と film grain、Medium 級の serif typography、1 色だけのインク (Iron Sienna) というシグネチャ。「個人テックブログ」の category-reflex から距離を取る。
4. **日本語組版を優先する**: 行長・行間・約物処理・コードと地の文の混在を整える。serif body は Mincho 系 (Hiragino Mincho ProN / Yu Mincho / Noto Serif CJK JP) に綺麗にフォールバックさせる。
5. **出自を隠さない (Show provenance)**: 著者、日付、source_url、カテゴリ、関連 Wiki ページが視認可能。hdknr 由来 (2015–2023) の post には小さく "via hdknr" を付し、自動取り込み記事と手書き記事の境目を読者から隠さず、ただし煩く見せない。
6. **ジャンル反射に乗らない**: AI / セキュリティ / クラウドの category-reflex（ネオン、ダーク、紫グラデ等）を選ばない。サイト全体で 1 つのトーン (Iron Sienna + warm parchment + grain) で全カテゴリを束ねる。
7. **歴史的記事と共存する**: hdknr 由来の古い post も同じテンプレートで違和感なく成立すること。新規記事のためのデザインで遺産を壊さない。
8. **Card を捨てる**: 一覧は等寸 card を敷き詰めず、横罫線 + 縦余白だけのデンスな行リストで組む。Medium / Maggie Appleton / Andy Matuschak と同系統。記事カード文化 (Qiita / Zenn) との視覚的距離を確保する。

## Accessibility & Inclusion

- WCAG 2.1 AA を目標。本文と背景のコントラストはダーク / ライト両モードで 4.5:1 以上。
- 自動テーマ切替 (`defaultTheme = 'auto'`) を維持。ユーザー OS 設定を尊重し、強制ダークも強制ライトもしない。
- 日本語の長文を読む前提なので、行長は 38〜45 字（≒65〜75ch 相当）を超えないように制御する。
- コードブロックは行送り・行頭インデント・コピー操作を阻害しないこと。`ShowCodeCopyButtons = true` を維持。
- `prefers-reduced-motion` を尊重。スクロール演出・ホバーアニメは控えめに、または無効化可能に。
- 図はラスタライズ済み画像（drawio → PNG）で alt テキストを必ず持たせる方針が既に CLAUDE.md に存在。これを破らない。
