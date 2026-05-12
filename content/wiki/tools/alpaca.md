---
title: "Alpaca（株式取引 API）"
description: "米国株・ETF・仮想通貨の自動売買 API を提供する証券会社。個人向け自動売買を Python から全操作できる唯一に近い選択肢"
date: 2026-05-09
lastmod: 2026-05-12
aliases: ["alpaca-py", "Alpaca Markets", "アルパカ証券"]
related_posts:
  - "/posts/2026/04/2026-04-27-claude-code-stock-trading-automation/"
tags: ["株式投資", "自動売買", "Python", "API", "米国株", "GitHub Actions"]
---

## 概要

Alpaca は米国の証券会社で、個人向けの株式・ETF・仮想通貨自動売買 API を提供する。日本の主要ネット証券（SBI・楽天・マネックス）は個人向け自動売買 API を公開していないため、米国株の自動売買を実現するうえでほぼ唯一の現実的な選択肢となっている。

## 主な特徴

- **全機能を Python から操作**: 注文・ポジション管理・履歴取得・マーケットデータ
- **Fractional Shares（端株）対応**: 少額から分散投資が可能
- **Paper Trading**: 本番前の仮想資金でのテスト環境が標準提供
- **無料**: 手数料無料（スプレッドで収益）
- **API**: 公式 SDK `alpaca-py` が提供される

## SDK のセットアップ

```bash
pip install alpaca-py
```

```python
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

client = TradingClient(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY",
    paper=True  # ペーパートレードで検証
)

# ポジション一覧
positions = client.get_all_positions()

# 成行注文
order = client.submit_order(
    MarketOrderRequest(
        symbol="AAPL",
        qty=1,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )
)
```

注意: 旧 SDK `alpaca_trade_api` は deprecated。`alpaca-py` に移行すること。

## 日本居住者の注意点

- **確定申告必須**: 特定口座が使えないため自分で損益計算が必要
- **PDT ルール**: 信用口座で 5 営業日に 4 回以上デイトレすると口座残高 $25,000 維持義務（**2026-06-04 以降、FINRA により最低 $2,000 + intraday margin 基準に置き換え予定**。証券会社は 2027-10-20 までに移行）
- **二重課税**: 米国課税 10% + 日本課税 20.315%（外国税額控除で調整可）
- **円→ドル送金コスト**: SBI 新生銀行経由などで圧縮

## Claude Code との組み合わせ

Claude Code で投資判断ロジックを言語化・コード化し、Alpaca API と接続することで自動売買システムを構築できる:

1. 投資ルールを期待値ベースで定義（例: -8% 損切り / +20% 利確）
2. Claude Code でルールをコードに落とす
3. GitHub Actions の cron で毎日自動実行
4. Slack Webhook で損益レポートを自動通知

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — 自動売買ロジックの実装環境
- [株式投資スタイル](/blogs/wiki/concepts/stock-trading-styles/) — トレードスタイルの概念整理

## ソース記事

- [Claude Code で株式投資を自動化する — Alpaca API + 期待値計算で 3 週間 4.19% の実績](/blogs/posts/2026/04/2026-04-27-claude-code-stock-trading-automation/) — 2026-04-27
