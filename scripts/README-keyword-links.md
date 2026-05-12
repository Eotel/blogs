# Keyword auto-linking (PoC)

はてなブログのキーワードリンクに似た、Wiki ページ / タグページへの自動内部リンクを
Hugo ビルド後の HTML に注入するポストプロセス。

## 構成

| ファイル | 役割 |
| --- | --- |
| `scripts/build_keyword_index.py` | `content/wiki/**/*.md` のフロントマター（title, aliases, description）と `public/tags/*/` から `.claude/temp/keywords.json` を生成 |
| `scripts/inject_keyword_links.py` | `public/posts/**/index.html` と `public/wiki/**/index.html` を BeautifulSoup でパースし、初出 1 回ずつ `<a class="kw-link">` を埋め込む |
| `static/css/keyword-links.css` | 注入されたリンクの見た目（点線下線 + ホバーで実線） |
| `layouts/partials/extend_head.html` | PaperMod の head フックから上記 CSS を読み込む |
| `.claude/keyword-stoplist.txt` | リンクから除外したいキーワード（1 行 1 語） |

## 依存

```
pip install -r requirements.txt
```

`tomllib` は Python 3.11+ 標準。

## ローカル実行

```
hugo --gc
python3 scripts/build_keyword_index.py
python3 scripts/inject_keyword_links.py public/
# 仕上がり確認
python3 -m http.server -d public 8080
```

`--dry-run` を渡すと書き込みせずに件数だけ報告する。
`hugo.toml` の `baseURL` に合わせて既定では `/blogs/` から始まる URL を注入するため、
`python3 -m http.server -d public 8080` で直に確認する場合は
`python3 scripts/inject_keyword_links.py public/ --prefix /` を使う。

## ポリシー

- **辞書ソース**: Wiki ページ（title + aliases）と Hugo 生成のタグページ
- **優先度**: Wiki > Tag、同 type 内は title > alias、section 優先度、target_id の順で決定
- **リンク化**: ページごとに target ID 単位で初出 1 回のみ
- **除外要素**: `<a>`, `<code>`, `<pre>`, `<h1>-<h6>`, `<script>`, `<style>`, `<nav>`, `<aside>`, `<figcaption>`, `.toc`, `.highlight`, `.post-meta`, `.breadcrumbs`, `.post-tags`, `#TableOfContents`
- **境界**: ASCII のみのキーワードは前後が英数字でないことを要求。日本語混じりは部分一致
- **セルフリンク防止**: Wiki single ページは自分の target_id を事前に「使用済み」にする
- **コンテンツ範囲**: `div.post-content` の中だけ走査（リスト系ページは自動スキップ）

## 既知の制約

- PoC につき CI 未統合。本番化するときは `.github/workflows/deploy.yml` の build → upload の間に 2 ステップ挟む
- `description` を `title` 属性に入れているので、長文 description はそのままツールチップになる（適宜短くする運用）
- 大量キーワード × 全 HTML の正規表現スキャンになるので、数百〜千ページ規模を前提
