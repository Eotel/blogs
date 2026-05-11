---
title: "Celery"
description: "分散タスクキュー。非同期処理と定期タスク実行を実現"
date: 2026-04-06
lastmod: 2026-04-06
aliases: ["celery"]
related_posts:
  - "/posts/2026/03/2026-03-30-claude-code-celery-orchestration/"
tags: ["Python", "Django", "タスクキュー", "Redis"]
---

## 概要

Redis や RabbitMQ をブローカーに、非同期タスク実行・定期タスク（beat）を実現。ECS Fargate 上では worker/beat を独立タスクとして実行。ログは CloudWatch Logs に出力。

## 関連ページ

- [Redis](/blogs/wiki/tools/redis/) — Celery のブローカー/バックエンド

## ソース記事

- [Claude Code + Celery: LLM が決定論的処理を動的に委譲するオーケストレーション](/blogs/posts/2026/03/2026-03-30-claude-code-celery-orchestration/) — 2026-03-30
