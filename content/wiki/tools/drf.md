---
title: "Django REST Framework (DRF)"
description: "Django で RESTful API を構築するフレームワーク"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["DRF", "django-rest-framework"]
related_posts:
  - "/posts/2021/04/2021-04-24-16261462f740c7681a19e6310d5b8115/"
  - "/posts/2023/03/2023-03-24-780eabebc7de7ffe9b5f62bd8a59565e/"
  - "/posts/2023/04/2023-04-05-2a96d9bd7e7cfb5224360179f0656020/"
  - "/posts/2023/04/2023-04-23-47edb4831ff832dadd5ce77b563b5cc5/"
  - "/posts/2023/04/2023-04-29-46723c4fa2639b9bc78fe52cdad903b0/"
  - "/posts/2023/05/2023-05-12-2299ed5cf019576fb2675b14afe30f92/"
  - "/posts/2023/08/2023-08-22-92c5eb49f98b8e7a52ab4afc7801ed92/"
  - "/posts/2026/02/2026-02-24-5d604ad7617c043a1bb80b6a43ffbb48/"
tags: ["Django", "API", "REST", "Python"]
---

## 概要

ModelSerializer で ORM↔API マッピング自動化。ViewSet で CRUD 一括定義。Content Negotiation、Pagination、Filtering、Permission クラスで機能実装。

## 関連ページ

- [FastAPI](/blogs/wiki/tools/fastapi/) — Python の別の API フレームワーク
- [CloudFront → ALB → Django の HTTPS 判定](/blogs/wiki/guides/cloudfront-alb-https/) — Django デプロイ時の典型的なプロキシ問題
- [django-mptt から django-tree-queries への移行](/blogs/wiki/guides/django-tree-migration/) — Django ツリー構造ライブラリの選択

## ソース記事

- [DRF: CSVを送信するするときに WindowsだとBOMをつけないとExcelで文字化けする問題](/blogs/posts/2021/04/2021-04-24-16261462f740c7681a19e6310d5b8115/) — 2021-04-24
- [Django:OpenAPI(Swagger) Scheme を出力して Pydatic クラスを生成できるようにする](/blogs/posts/2023/03/2023-03-24-780eabebc7de7ffe9b5f62bd8a59565e/) — 2023-03-24
- [Django: model から DRF ModelSerializer を参照する](/blogs/posts/2023/04/2023-04-05-2a96d9bd7e7cfb5224360179f0656020/) — 2023-04-05
- [DRF: Userを所属グループで検索](/blogs/posts/2023/04/2023-04-23-47edb4831ff832dadd5ce77b563b5cc5/) — 2023-04-23
- [DRF: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list](/blogs/posts/2023/04/2023-04-29-46723c4fa2639b9bc78fe52cdad903b0/) — 2023-04-29
- [DRF: Content Negotiation](/blogs/posts/2023/05/2023-05-12-2299ed5cf019576fb2675b14afe30f92/) — 2023-05-12
- [DRF: DataFrame を使って CSV エクスポート](/blogs/posts/2023/08/2023-08-22-92c5eb49f98b8e7a52ab4afc7801ed92/) — 2023-08-22
- [# CloudFront → ALB → Django 構成で API レスポンスの URL スキームが http:// になる問題と解決策](/blogs/posts/2026/02/2026-02-24-5d604ad7617c043a1bb80b6a43ffbb48/) — 2026-02-24
