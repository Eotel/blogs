---
title: "Celery"
description: "分散タスクキュー。非同期処理と定期タスク実行を実現"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["celery"]
related_posts:
  - "/posts/2026/03/2026-03-30-claude-code-celery-orchestration/"
  - "/posts/2023/04/2023-04-07-bfe76b81c50797270ccec6b441c406b4/"
  - "/posts/2023/04/2023-04-11-78b54a5cbcfdc5b5710bcd664c6d76e0/"
  - "/posts/2023/04/2023-04-12-91decc44392237a42510180061261903/"
  - "/posts/2023/04/2023-04-12-e5690198c788d5e603c954253ac2f65f/"
  - "/posts/2023/04/2023-04-12-fcf2fccad526d38b08a0aacc67d1b3d1/"
  - "/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/"
tags: ["Python", "Django", "タスクキュー", "Redis"]
---

## 概要

Redis や RabbitMQ をブローカーに、非同期タスク実行・定期タスク（beat）を実現。ECS Fargate 上では worker/beat を独立タスクとして実行。ログは CloudWatch Logs に出力。

## Django + Redis セットアップ

```bash
poetry add "celery[redis]" django-celery-results django-redis
```

- `django-celery-results` — Django ORM/Cache をタスク結果バックエンドに使用
- `django-redis` — Redis キャッシュバックエンド

定期タスクは `django-celery-beat` で管理。[Periodic Tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html) 参照。

### MySQL タイムゾーン問題

`Database returned an invalid datetime value` が出る場合は tzinfo を MySQL に投入する:

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo/ | mysql -u root mysql
```

## テストと Singleton

- eager モード（`CELERY_TASK_ALWAYS_EAGER=True`）でユニットテストを高速化
- Singleton Task（同時実行数 1 制限）は Redis ロックで実装。[レシピ](https://docs.celeryq.dev/en/latest/tutorials/task-cookbook.html)参照

## 関連ページ

- [Redis](/blogs/wiki/tools/redis/) — Celery のブローカー/バックエンド

## ソース記事

- [Claude Code + Celery: LLM が決定論的処理を動的に委譲するオーケストレーション](/blogs/posts/2026/03/2026-03-30-claude-code-celery-orchestration/) — 2026-03-30
- [Python: ジョブキューイング](/blogs/posts/2023/04/2023-04-07-bfe76b81c50797270ccec6b441c406b4/) — 2023-04-07
- [Celery: eager モード (同期モード)](/blogs/posts/2023/04/2023-04-11-78b54a5cbcfdc5b5710bcd664c6d76e0/) — 2023-04-11
- [Celery: タスクの結果をMySQLで確認する](/blogs/posts/2023/04/2023-04-12-91decc44392237a42510180061261903/) — 2023-04-12
- [Celery: supervisord](/blogs/posts/2023/04/2023-04-12-e5690198c788d5e603c954253ac2f65f/) — 2023-04-12
- [Celery: Singleton Task](/blogs/posts/2023/04/2023-04-12-fcf2fccad526d38b08a0aacc67d1b3d1/) — 2023-04-12
- [Celery AWS ECS](/blogs/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/) — 2023-07-13
