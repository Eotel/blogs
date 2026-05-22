---
title: "gsap-skills"
description: "GreenSock 公式の GSAP（GreenSock Animation Platform）向け Agent Skills 集。Claude Code / Cursor / Codex など 40+ エージェントに、useGSAP・ScrollTrigger・プラグインの正しい使い方と最新ライセンス事情を教える 8 つの SKILL.md"
date: 2026-05-22
lastmod: 2026-05-22
aliases: ["GSAP Skills", "GreenSock Skills", "greensock/gsap-skills"]
related_posts:
  - "/blogs/posts/2026/05/2026-05-21-gsap-skills/"
tags: ["gsap", "skills", "greensock", "webflow", "animation"]
---

## 概要

`greensock/gsap-skills` は GreenSock が公式に出している GSAP（GreenSock Animation Platform）向けの [Agent Skills](/blogs/wiki/concepts/agent-skills-format/) 集。**ライブラリベンダー自身が公式の Skills を出した代表事例** で、AI コーディングエージェントが GSAP を生成・修正するときの正しい型を 8 つの `SKILL.md` で提示する。ライセンスは MIT、配布は GitHub。

`npx skills add https://github.com/greensock/gsap-skills` 一発で Claude Code / Cursor / Codex / Windsurf / Copilot / Google Antigravity など [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI 対応の 40+ エージェントに同じ skill 群が入る。

## 8 つの SKILL.md と llms.txt

| Skill | カバー範囲 |
|---|---|
| `gsap-core` | `gsap.to()` / `from()` / `fromTo()`、easing、duration、stagger、defaults、transform エイリアス、`gsap.matchMedia()`（レスポンシブ・`prefers-reduced-motion`） |
| `gsap-timeline` | `gsap.timeline()`、position parameter、labels、ネスト、再生制御 |
| `gsap-scrolltrigger` | スクロール連動アニメーション、pinning、scrub、`ScrollTrigger.batch()`、`scrollerProxy()`、v3.12+ の `clamp()` |
| `gsap-plugins` | ScrollToPlugin / ScrollSmoother / Flip / Draggable / Inertia / Observer / SplitText / ScrambleText / MorphSVG / DrawSVG / MotionPath / CustomEase / EasePack / GSDevTools |
| `gsap-utils` | `gsap.utils` の clamp / mapRange / normalize / interpolate / random / snap / toArray / wrap / pipe |
| `gsap-react` | `useGSAP()` フック、refs、`gsap.context()`、cleanup、SSR |
| `gsap-performance` | transform を優先する設計、`will-change`、batch read/write、`gsap.quickTo()` |
| `gsap-frameworks` | Vue / Svelte などフレームワーク横断のライフサイクル整理 |

加えて `skills/llms.txt` がエージェント用のフラットなインデックスとして置かれ、各 skill の `description` と **trigger 語** を一覧化している。

## 設計の特徴

### API リファレンスではなく "落とし穴の地図"

各 `SKILL.md` は GSAP の API ドキュメントを書き写したものではなく、エージェントが間違えやすいところを先回りで矯正するための指示が主軸になっている。

- `gsap-react`: `useEffect` で書かず `useGSAP()` を使う、selector に必ず `scope` を渡す、SSR で `gsap.*` を呼ばない
- `gsap-scrolltrigger`: `ScrollTrigger.batch()` を `IntersectionObserver` の代替として推奨、Lenis 等の smooth scroll には `scrollerProxy()` を組む、pin がジャンプするときの `pinType: "fixed" | "transform"`
- `gsap-plugins`: プラグイン使用時は必ず `gsap.registerPlugin()` を呼ぶ、`gsap.context()` には `ctx.revert()` を返す

### LLM 既知バイアスを上書きするためのパッチ

`gsap-plugins/SKILL.md` の "Licensing & Install (important)" セクションは、エージェントに対する明示的な禁止リストになっている。

- ✅ 全プラグインを `npm install gsap` から入れる（import 経路は `gsap/SplitText`、`gsap/MorphSVGPlugin` 等）
- ❌ `.npmrc` に GreenSock auth token を書かせない
- ❌ `npm.greensock.com` の private registry を提案させない
- ❌ Club GSAP メンバーシップへのサインアップを促さない

これは Webflow 買収（2024-10-15）以降、2025-04 に GSAP が全プラグイン含めて 100% 無料・商用利用可になったことに合わせた矯正パッチ。LLM の学習データには Club GSAP 前提の古い記事や StackOverflow 回答が大量に蓄積されているため、それを SKILL.md で上書きしている。

### trigger 語の戦略的設計

`skills/llms.txt` の `gsap-plugins` セクションには次のような trigger 語が並んでいる。

> Triggers: ... Club GSAP, GSAP membership, GSAP license, GSAP free, GSAP paid, GSAP commercial, bonus plugins, GreenSock auth token, .npmrc GSAP, private GSAP registry, Webflow GSAP.

「Club GSAP」「`.npmrc` auth token」「private registry」など、**過去のライセンス時代に染みついた誤った前提語** を trigger に組み込むことで、エージェントがそれらに触れた瞬間に確実に skill を発火させる作りになっている。

## ライセンス（2025-04 以降）

- 全プラグインを含めて GSAP は **100% 無料・商用利用可**
- `npm install gsap` だけで SplitText / MorphSVG / DrawSVG / MotionPath / Inertia / ScrollSmoother / CustomEase 等すべて入る
- ただし [Standard License](https://gsap.com/community/standard-license/) には **「Webflow と競合するビジュアルアニメーションビルダーツール内での使用は禁止」** という除外条項が明示的に存在する。ノーコードで Web アニメーションを構築させる UI を提供するプロダクトを開発する場合は最新文面を要確認。

## インストール経路

```bash
# 推奨: vercel-labs/skills CLI 経由（エージェント自動検出）
npx skills add https://github.com/greensock/gsap-skills

# エージェント明示
npx skills add https://github.com/greensock/gsap-skills --agent antigravity

# Claude Code 単体: plugin marketplace
/plugin marketplace add greensock/gsap-skills
```

手動配置時の skill ディレクトリ:

| エージェント | skill ディレクトリ |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| OpenAI Codex | `~/.codex/skills/` |
| Google Antigravity | `~/.gemini/antigravity/skills/`（global）または `.agent/skills/`（workspace） |

GitHub Copilot だけは Skills フォーマットではなく `.github/copilot-instructions.md` を読む流儀のため、リポジトリ内の `.github/copilot-instructions.md` と `.github/instructions/` 配下のパス別指示を対象リポジトリに転記する。

## 関連ページ

- [Skills フォーマット（SKILL.md 互換層）](/blogs/wiki/concepts/agent-skills-format/) — `SKILL.md` の発祥と相互運用層としての位置づけ
- [Claude Code](/blogs/wiki/tools/claude-code/) — gsap-skills を入れて呼び出すホスト
- [Strands Agents](/blogs/wiki/tools/strands-agents/) — 同じく Skills を読み込むランタイム

## ソース記事

- [GSAP Skills でできること — AI コーディングエージェントに公式 GSAP の作法を教える Skills 集](/blogs/posts/2026/05/2026-05-21-gsap-skills/) — 2026-05-21
