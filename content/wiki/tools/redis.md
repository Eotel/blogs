---
title: "Redis"
description: "高速インメモリデータストア。キャッシュ・セッション・キューイング・分散ロックに利用"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["redis"]
related_posts:
  - "/posts/2026/03/redis-fenced-lock-python/"
  - "/posts/2026/03/redis-shared-state-antipattern/"
  - "/posts/2015/04/2015-04-21-ecf1cb51339d7447a19e/"
  - "/posts/2023/05/2023-05-05-6f0abad12df8bc996fece3fef54f29e1/"
  - "/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/"
  - "/posts/2023/07/2023-07-14-0e2885fa164ec64417cf750beafb9e04/"
  - "/posts/2023/11/2023-11-06-44e397ac03deaa013c125c49c0d33904/"
  - "/posts/2024/01/2024-01-05-c45b85d58be2dac1c4375750d75b0904/"
  - "/posts/2026/03/2026-03-02-92ce5b95cd28ffb9ca25100b1991d6d3/"
tags: ["Redis", "キャッシュ", "データストア", "Django"]
---

## 概要

インメモリストレージで、Memcached より豊富なデータ構造（List・Set・Sorted Set・Stream）対応。Django キャッシング・Celery ブローカー・セッションストアとして広く活用。ElastiCache クラスターモードでシャーディング・高可用性確保。

## 分散ロック

Lua スクリプトによる複数コマンドのアトミック実行で競合状態を回避。フェンシングトークンで堅牢なロック実装が可能。

## 関連ページ

- [分散ロック](/blogs/wiki/concepts/distributed-lock/) — Redis を使った排他制御
- [Celery](/blogs/wiki/tools/celery/) — Redis をブローカーとして利用

## ソース記事

- [Redis フェンシングロック](/blogs/posts/2026/03/redis-fenced-lock-python/) — 2026-03
- [Redis Windows](/blogs/posts/2015/04/2015-04-21-ecf1cb51339d7447a19e/) — 2015-04-21
- [redis](/blogs/posts/2023/05/2023-05-05-6f0abad12df8bc996fece3fef54f29e1/) — 2023-05-05
- [Celery AWS ECS](/blogs/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/) — 2023-07-13
- [redis](/blogs/posts/2023/07/2023-07-14-0e2885fa164ec64417cf750beafb9e04/) — 2023-07-14
- [Redis キーの作成時刻](/blogs/posts/2023/11/2023-11-06-44e397ac03deaa013c125c49c0d33904/) — 2023-11-06
- [django-redis: lock](/blogs/posts/2024/01/2024-01-05-c45b85d58be2dac1c4375750d75b0904/) — 2024-01-05
- [Redis Pub/Sub から Streams への移行で帯域 99% 削減 --- 同時接続 30 万超チャットの実践記録](/blogs/posts/2026/03/2026-03-02-92ce5b95cd28ffb9ca25100b1991d6d3/) — 2026-03-02
