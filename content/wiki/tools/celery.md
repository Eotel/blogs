---
title: "Celery"
description: "分散タスクキュー。非同期処理と定期タスク実行を実現"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["celery"]
related_posts:
  - "/posts/2026/03/2026-03-30-claude-code-celery-orchestration/"
  - "/posts/2023/04/2023-04-11-78b54a5cbcfdc5b5710bcd664c6d76e0/"
  - "/posts/2023/04/2023-04-12-91decc44392237a42510180061261903/"
  - "/posts/2023/04/2023-04-12-e5690198c788d5e603c954253ac2f65f/"
  - "/posts/2023/04/2023-04-12-fcf2fccad526d38b08a0aacc67d1b3d1/"
  - "/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/"
tags: ["Python", "Django", "タスクキュー", "Redis"]
---

## 概要

Redis や RabbitMQ をブローカーに、非同期タスク実行・定期タスク（beat）を実現。ECS Fargate 上では worker/beat を独立タスクとして実行。ログは CloudWatch Logs に出力。

## 関連ページ

- [Redis](/blogs/wiki/tools/redis/) — Celery のブローカー/バックエンド

## ソース記事

- [Claude Code + Celery: LLM が決定論的処理を動的に委譲するオーケストレーション](/blogs/posts/2026/03/2026-03-30-claude-code-celery-orchestration/) — 2026-03-30
- [Celery: eager モード (同期モード)](/blogs/posts/2023/04/2023-04-11-78b54a5cbcfdc5b5710bcd664c6d76e0/) — 2023-04-11
- [Celery: タスクの結果をMySQLで確認する](/blogs/posts/2023/04/2023-04-12-91decc44392237a42510180061261903/) — 2023-04-12
- [Celery: supervisord](/blogs/posts/2023/04/2023-04-12-e5690198c788d5e603c954253ac2f65f/) — 2023-04-12
- [Celery: Singleton Task](/blogs/posts/2023/04/2023-04-12-fcf2fccad526d38b08a0aacc67d1b3d1/) — 2023-04-12
- [Celery AWS ECS](/blogs/posts/2023/07/2023-07-13-9b947258d31059c56fec5000faa190ca/) — 2023-07-13
