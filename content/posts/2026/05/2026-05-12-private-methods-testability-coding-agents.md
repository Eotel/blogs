---
title: "private メソッドにビジネスロジックを隠すな — TDD・カプセル化・coding agent 時代の設計判断"
date: 2026-05-12
lastmod: 2026-05-12
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "Uncle Bob・Fowler・Feathers・t_wada が言ってきた『private を test するな』を 2026 年の AI coding agent 時代に読み直す。カプセル化と testability の対立を、class の境界の設計判断として捉え直すための長文論考。"
categories: ["AI/LLM"]
tags: ["TDD", "private-method", "テスタビリティ", "Clean-Architecture", "AI-coding-agent"]
---

## 序: ボブおじの通った道を辿るとき

Robert C. Martin（Uncle Bob）の本を読み返していると、たまに「あ、これ前に自分でハマったやつだ」と気づく瞬間がある。コードに対する違和感を言語化できないまま何年か経って、ようやく自分の言葉で噛み砕けたタイミングで、Bob が同じことをずっと前に書いているのを見つける。あの感覚が好きだ。

ただ、何度読み返しても引っかかる言説がある。「private method を書くな」というやつだ。TDD 界隈では「private method はテストするな」とほぼセットで語られていて、過激派になると「そもそも private を書くこと自体がアンチパターン」と言う人もいる。一方で、オブジェクト指向の根本は information hiding で、「知る必要のないものは知らせるな」が原則のはずだ。この 2 つはどう折り合いをつければいいのか。

そして今、もうひとつ厄介な論点が乗ってきている。coding agent（LLM）が大量にコードを書く時代に、「private は test されない / されにくい」という性質は、それ単独で新しい failure mode を生む。本稿ではそこまで含めて、現時点の自分の整理を残しておく。

## 1. 「private を test するな」言説の整理

まず古典の確認から。「private を直接 test するな」と言っている主な論者を並べてみる。

**Martin Fowler** は記事 "Refactoring: This class is too large" で、「private nested code が多くて unit test しづらい状況は、その class が複数の責務を抱えているサインであり、責務ごとに class を切り出すべきだ」という立場を取っている [^fowler-class-too-large]。同じく Fowler の "Self Encapsulation" [^fowler-self-encap] は、object 内部で自分の field にアクセスするときも getter/setter を経由しろという話で、内側にもインターフェイスを引け、という主張だ。

**Michael Feathers** の *Working Effectively with Legacy Code* には、「test しづらい private がある」ということ自体を「この class は分割を求めている」というシグナルとして扱う議論が繰り返し出てくる。private を test するために reflection で殴る、内部 helper を `@VisibleForTesting` で開ける、といった対症療法に走らず、まず class の境界を引き直す。Extract Class（Fowler の Refactoring カタログ由来の用語）が、こうした「太りすぎた class が痩せたがっているサイン」に応える定石だ。

**Kent Beck** の TDD 観も同じ方向で、「実装 driven で test を書いた後、refactor の過程で private に push down された helper は test を残す必要がない（消してよい）」というのは Beck 派の通説に近い [^duffield]。

**和田卓人 (t_wada)** は日本語圏で「テスタビリティは設計の問いだ」を繰り返し言っている。テスタビリティが低いのは test 戦略の問題ではなく設計の問題で、test を書きやすい構造に reshape することが TDD の本体だ、という整理だ。

これらに共通しているのは、「private を test しなくていい」と言いつつ、その意味するところは **「test を書かない」ではなく「test を書ける構造に作り直せ」** という点である。test 不要論ではなく設計フィードバックの話なのだ。ここを取り違えると痛い。

## 2. Uncle Bob は実際に何を書いているのか

Bob が「private method を書くな」と言ったかというと、言っていない。少なくとも *Clean Code* と *Clean Architecture* を素直に読む限り、private は否定されていない。むしろ Bob 自身の例示コードは private で溢れている。

*Clean Code* 第 3 章「Functions」で Bob が紹介する「Stepdown Rule」は、「コードは新聞のように読めるべきだ。public な意図を先に書き、その下に詳細を一段ずつ下げて配置する」という構成原則だ。この「一段下げる」ための器が、まさに Extract Method で抽出された private なのだ。public method は意図（what）を語り、private method は手段（how）を語る。階段状にスタックされた private は Bob にとって悪ではなく、可読性の道具である。

*Clean Architecture* の文脈でも、層間の境界（Use Case と Entity の関係など）には interface を切るが、層内では普通に private を使っている。境界の方向（依存の向き）が大事なのであって、すべての関数を public に晒せという話ではない。

決定的なのは、Bob 自身が 2017 年に書いた "Test Contra-variance" [^bob-contravariance] というブログ記事だ。ここで彼は「test を書く都合で本体の structure を歪めるのは本末転倒だ」と明示的に警告している。test のために internal を露出させたり、設計を test に従属させたりするのを良しとしない。Bob は private を否定していないし、「test 駆動」と「設計の意図」が衝突する場面ではむしろ設計の意図を優先せよと言っている。

つまり「private を書くな」は Uncle Bob 本人の主張ではない。TDD コミュニティのある一派が「private を test するな」を過剰一般化したスローガンであり、Bob はそこにいない。

## 3. カプセル化とテスト可能性は本当に対立するのか

ここまでで「Fowler / Feathers / t_wada が言う『private を test するな』」と「Bob の private 肯定」は実は同じことを言っていることが見えてくる。両者が共有しているのは次の図式だ。

> 「private を直接 test したい」と感じたら、それは class の境界が間違っているサインである。private を test するのではなく、その private を別の class の public method にして、その class の public API として test せよ。

OO 古典に戻ると、David Parnas が 1972 年の "On the Criteria To Be Used in Decomposing Systems into Modules" で示した information hiding 原則 [^parnas-1972] は、「変更されやすい設計判断は module の内側に隠せ」というものだ。隠すこと自体が目的なのではなく、「外側から知る必要のないものを知らせない」ことで変更コストを下げるのが目的である。

これと testability の関係を整理し直すと、対立しているように見えていたものが実は同じ判断に解消される。

- **既存 class の中で private にする** → その helper は変更しても外に波及しない。test は public API 経由で十分にカバーできる範囲のものだ
- **新しい class に extract して public method にする** → その helper はもう独立した責務を持っていて、外から（test を含めて）使われる価値がある

「private にするか extract するか」は access modifier の選択であると同時に、「この helper はどれくらい独立した責務を持つか」という設計判断そのものだ。Information hiding（隠す側）と testability（露出させる側）は、対立する 2 つの力ではなく、同じ「class の境界をどこに引くか」の表と裏である。

問題は、この判断を毎回ちゃんと下しているかどうかで、そこに次の論点が乗ってくる。

## 4. AI coding agent 時代の新しい逆説

ここからが本題に近い。人間が「面倒だから private に押し込む」のと、coding agent が「test を書かないコストとして private に push する」のとは、似ているようで質が違う。

agent には次のような構造的バイアスがある。

1. **public API の signature 変更を避けたがる**。signature を変えると test と caller の両方に diff が出る。agent にとっては影響範囲が広がることになり、PR の通過確率が下がるシグナルになる
2. **既存の構造を維持しつつ機能を足したがる**。新規 class を切り出すよりも、既存 class の既存 private に分岐を足す方が「小さな変更」に見える
3. **「test されている」という外形を満たそうとする**。public API の test が既に通っているなら、それを変えずに済む形を選ぶ

この 3 つが重なると何が起きるか。「test を書きたくないから private に隠す」ではなく、もっと厄介な「test を書かなくても通る形に整える」という挙動になる。具体的には、既存の private にビジネスロジックがそっと足される。public API は変わらないので、test も変わらない。git diff も小さく見える。レビュアー（人間）が見るのは public method のシグネチャと test の差分なので、private の中身がいつの間にか肥大化していることに気づきにくい。

これが厄介なのは、検出が難しいことだ。

- **line coverage** では検出できない。private に追加された行は、public API を呼んでいる既存 test を経由して「実行はされて」しまうので、coverage 上は緑のままになる
- **branch coverage** でも厳しい。新しい分岐に test を足す必要があるが、agent 自身がそれを書かないので、coverage は下がるはずなのに「下がっても他で打ち消されて気づかない」ことが多い
- **mutation testing**（Stryker [^stryker]、mutmut [^mutmut]、PIT [^pit] など）なら、private の中のコードを変異させても test が落ちない状態を検出できる。ただし CI コストが高く、運用に乗せている組織は多くない

要するに、「private で test されない」という性質が、人間の時代には「めんどくさいから後で書こう」程度の意味だったのが、agent の時代には「検証されない business logic が静かに増えていく経路」になりつつある。Bob やそのフォロワーが想定していた「test しなくていい private」は「単純な helper」だったはずだが、agent が触ると private が business logic を吸い込みやすい。これは旧来の議論には載っていない、新しい failure mode だ。

私個人としては、いくつかの自分のリポジトリで agent に refactor を任せたとき、「public method を変更せずに既存 private を肥大化させて要件を満たす」修正をされて、レビューで気づくのに時間がかかったことが何度かある。統計的根拠を持ち出すつもりはないが、上記のメカニズムに矛盾しない経験だった。

## 5. コード例: 既存 private にビジネスロジックが潜り込む

抽象論ばかりだとイメージが湧きづらいので、TypeScript で 1 例だけ示す。EC の注文を受け付ける `OrderService` を考える。

最初の素直な実装はこうだ。

```typescript
type Order = { userId: string; items: Item[]; total: number };

class OrderService {
  constructor(private readonly repo: OrderRepo) {}

  submit(order: Order): SubmitResult {
    if (!this.isValid(order)) {
      return { ok: false, reason: "invalid" };
    }
    this.repo.save(order);
    return { ok: true, orderId: order.userId + ":" + Date.now() };
  }

  private isValid(order: Order): boolean {
    return order.items.length > 0 && order.total > 0;
  }
}
```

`isValid` は単純な helper だ。private に置いておくのは妥当で、`submit` の test を public API 経由で書けば自然に覆われる範囲にある。

ここに「VIP ユーザーは 10% 割引、ロイヤリティポイントが 1000 以上なら追加 5%、月末は二重ポイント」という要件追加が来たとする。agent が「public API を変えず、既存 test を壊さない最小変更」を狙うと、こんな diff になりがちだ。

```typescript
class OrderService {
  constructor(
    private readonly repo: OrderRepo,
    private readonly userRepo: UserRepo,
    private readonly clock: Clock,
  ) {}

  submit(order: Order): SubmitResult {
    if (!this.isValid(order)) {
      return { ok: false, reason: "invalid" };
    }
    this.repo.save(order);
    return { ok: true, orderId: order.userId + ":" + Date.now() };
  }

  // ふくらむ private
  private isValid(order: Order): boolean {
    if (order.items.length === 0 || order.total <= 0) return false;
    const user = this.userRepo.findById(order.userId);
    let discount = 0;
    if (user.tier === "vip") discount += 0.10;
    if (user.loyaltyPoints >= 1000) discount += 0.05;
    const isMonthEnd = this.clock.now().getDate() >= 28;
    const multiplier = isMonthEnd ? 2 : 1;
    // 引数の order / user を直接 mutate しているのが要注意。
    // 「妥当性検証」の名のもとに副作用が紛れ込んでいる。
    order.total = order.total * (1 - discount);
    user.loyaltyPoints += Math.floor(order.total * multiplier);
    return true;
  }
}
```

public API は `submit(order): SubmitResult` のままで、既存 test もそのまま通る（割引前提が無い test を書いていた場合に限るが、agent はその範囲だけ動かす）。しかし `isValid` はもはや「妥当性検証」ではない。割引計算、ロイヤリティ加算、二重ポイント判定という 3 つの business logic を吸い込んでしまっている。`isValid` という名前を読んで「割引が計算される」と推測できる人はいない。

レビュー時にこの private の中身を一行一行追わない限り、PR の見た目は「`isValid` に少し条件が増えた」だけに見える。

これを Feathers の "Extract Class" シグナルに従って書き直すと、こうなる。

```typescript
class OrderValidator {
  validate(order: Order): boolean {
    return order.items.length > 0 && order.total > 0;
  }
}

class DiscountPolicy {
  apply(order: Order, user: User): number {
    let discount = 0;
    if (user.tier === "vip") discount += 0.10;
    if (user.loyaltyPoints >= 1000) discount += 0.05;
    return order.total * (1 - discount);
  }
}

class LoyaltyRule {
  earnedPoints(discountedTotal: number, now: Date): number {
    const isMonthEnd = now.getDate() >= 28;
    return Math.floor(discountedTotal * (isMonthEnd ? 2 : 1));
  }
}

class OrderService {
  constructor(
    private readonly repo: OrderRepo,
    private readonly userRepo: UserRepo,
    private readonly clock: Clock,
    private readonly validator: OrderValidator,
    private readonly discount: DiscountPolicy,
    private readonly loyalty: LoyaltyRule,
  ) {}

  submit(order: Order): SubmitResult {
    if (!this.validator.validate(order)) return { ok: false, reason: "invalid" };
    const user = this.userRepo.findById(order.userId);
    const discounted = this.discount.apply(order, user);
    user.loyaltyPoints += this.loyalty.earnedPoints(discounted, this.clock.now());
    this.repo.save({ ...order, total: discounted });
    return { ok: true, orderId: order.userId + ":" + Date.now() };
  }
}
```

差分は大きい。が、これは「diff が大きい方が悪い」ではなく、「business logic が見える場所に出てきた」ことを意味する。`DiscountPolicy` と `LoyaltyRule` は pure な class で、public API がそのまま test の境界になる。月末判定や VIP の境界値を test するのに、`OrderService` を組み立てる必要はもうない。「test したくない」が理由で隠す動機が物理的に消えている。

agent に「OrderService に機能を足せ」ではなく「OrderService.submit の振る舞いを変えるなら、ロジックは別 class に extract せよ」と明示してから書かせると、後者の形に着地しやすくなる。プロンプトの 1 行で diff の質が変わる、というのは現実的な防衛策のひとつだ。

## 6. 実務指針

ここまでの整理を、明日から使える形に落としておく。

**個人として書くときの問い**

- private に新しい行を足したくなったら、「これは helper か、それとも business logic か」を 1 秒だけ問う
- helper（pure な変換、3〜5 行で済む、別 class にしても test の価値が薄い）なら private のまま OK
- business logic（複数の if、複数の依存、要件文書に出てくる名詞や動詞）なら、その private は class になりたがっているサインだ
- 迷ったら extract に倒す。あとで戻すのは簡単だが、肥大化した private を分解するのはコストが高い

**coding agent を使うとき**

- agent の system prompt / instructions に「`private` に新規 business logic を追加するな。helper か pure な変換に限れ。business logic を足すときは別 class を切り出して public API で test 可能にせよ」を明示する
- CI の review hook（pre-commit、PR チェック）で private method の cyclomatic complexity と行数を計測し、閾値を超えたら警告する（CodeClimate、SonarQube、ESLint の `complexity` rule などで実現可能）
- 余力があれば mutation testing を主要 module に入れる。Stryker / mutmut / PIT は、private に隠れた「test で死なないコード」を可視化する
- 「public API を経由しない test を書くな」を CI で強制する。reflection や `@ts-ignore` で private を呼ぶ test は警告対象にする

**それでも残るグレーゾーン**

- 「helper として private に残す」と「extract する」の境界は最終的に経験則だ。書き手の判断が入る
- ただし AI 時代の更新点として、「迷ったら extract に倒す」は人間時代より一段強めて良い。なぜなら検証が抜ける failure mode の方が過剰分割の害より深刻になりつつある、というのが現時点の私の見立てだからだ

## 結: 「private を書くな」を更新する

「private を書くな」は古典的な意味では誤読だ。Uncle Bob はそんなことを言っていないし、Fowler も Feathers も t_wada も、本意は「private に閉じ込めた business logic を test できる構造にせよ」だった。「test するな」の裏には常に「再設計しろ」が貼り付いていた。

その上で、AI coding agent の時代に合わせて言い換えるなら、これでよいと思う。

> **「private を書くな」ではなく「private に business logic を隠すな」**

カプセル化と testability は対立する 2 つの原則ではなく、「class の境界をどこに引くか」という同じ設計判断の表と裏である。判断する主体が人間から agent に半分移った今、その判断を「迷ったら extract」「business logic は class の public 境界に置く」という形でやや前傾させておく。それが、ボブおじの遺してくれたメッセージを 2026 年に運用するときのチューニングだと、いまの私は思う。

## 関連記事

- [「テスト書いて」と「テスト駆動で実装して」は全く別物 — AI×TDD で品質が劇的に変わる構造的理由](/blogs/posts/2026/03/2026-03-04-d84f897e8825bef6ac3f28ad5a982740/)
- [「決定性のないソフトウェア」をどう設計し評価するか — t_wada 氏の視点と skill-creator が実装した答え](/blogs/posts/2026/03/2026-03-05-75d885dac4bc6727daa08e68d0771e91/)
- [AIコーディングエージェント開発フレームワーク「superpowers」— 7段階ワークフローとTDDで精度を高める](/blogs/posts/2026/03/2026-03-17-superpowers-ai-coding-agent-framework/)
- [クリーンアーキテクチャという「型」の暴力 — 過剰な抽象化が現場を壊すメカニズム](/blogs/posts/2026/03/2026-03-03-0617418777ad8f46ddf3f1d9bfbfb06f/)

## 参考リンク

[^fowler-class-too-large]: Martin Fowler, "Refactoring: This class is too large, and I want to split it up", https://martinfowler.com/articles/class-too-large.html
[^fowler-self-encap]: Martin Fowler, "Self Encapsulation" (Bliki), https://martinfowler.com/bliki/SelfEncapsulation.html
[^bob-contravariance]: Robert C. Martin, "Test Contra-variance" (The Clean Coder Blog, 2017-10-03), https://blog.cleancoder.com/uncle-bob/2017/10/03/TestContravariance.html
[^duffield]: Jesse Duffield, "Still No Consensus On Testing Private Methods", https://jesseduffield.com/Testing-Private-Methods/
[^parnas-1972]: David L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", Communications of the ACM, December 1972.
[^stryker]: Stryker Mutator (JavaScript / TypeScript mutation testing), https://stryker-mutator.io/
[^mutmut]: mutmut (Python mutation testing), https://github.com/boxed/mutmut
[^pit]: PIT mutation testing (Java), https://pitest.org/
