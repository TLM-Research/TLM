---
id: RN-15
title: "A Temporal Liquidity Fee for EIP-1559"
version: "0.5"
status: "Public draft - research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: "2026-08-31"
license: "CC-BY-4.0"
---

# RN-15 v0.5

# A Temporal Liquidity Fee for EIP-1559

## Pricing execution position within a single slot

**Temporal Liquidity Market (TLM) Research Program**
**Research Note RN-15**
**Version:** 0.5
**Status:** Public draft - research note, offered in good faith for comment.
**Scope:** One slot, one existing block, no new protocol state. Prices position within the block. Does not defer a transaction to a later slot and does not act on congestion.
**Date:** 31 August 2026

> **Licence.** CC BY 4.0, as with the rest of the research programme. If this mechanism is submitted as an Ethereum Improvement Proposal, the EIP will be written as a separate document under CC0, since EIP-1 requires every EIP to be in the public domain. This note is not that document and does not waive rights.

---

## Abstract

RN-14 sec. 8.3 identifies what Ethereum's fee market cannot express. The priority fee is a bid for inclusion, with nothing attached about position: a sender cannot bid for inclusion at an earlier position within the slot, and cannot offer to take a later one in exchange for paying less. Position inside the block is not addressable, though it is traded out-of-band by parties other than the sender, and the protocol could not check a position commitment if one were made.

This note adds a signed **temporal liquidity fee** (`TLF`) to the transaction, assessed against the gas-weighted mean of the declared fees over the block. Deviations from that mean sum to zero by construction, so premiums paid by transactions bidding for an earlier position fund discounts to transactions taking a later one, with no external funding source and no protocol-held balance. The fee also sets intra-slot ordering, which is what makes declaring it consequential and what the protocol can verify afterwards.

**The scope is one slot.** Nothing here defers a transaction to a later slot or acts on congestion; the base fee continues to do that alone.

Two results are worth separating. Budget balance is a construction and holds by arithmetic, given a cap set as a fraction of the prevailing base fee, and sec. 2.3 shows why that cap cannot be an absolute constant. The claim that the scheme attracts the workloads RN-14 describes is a conjecture, and sec. 8 gives the reasons to doubt it.

Being two-sided and budget-balanced, the mechanism cannot also be incentive compatible and efficient. Section 10 gives up incentive compatibility, on the ground that EIP-1559's priority fee already is not.

Section 12 records an identity: this mechanism is the case of a more general one in which a reserve is held at exactly zero every block. Letting that reserve move is a larger change, worked out separately.

Judge it as a proposal for an incremental change rather than a completed mechanism. The binding rule of sec. 2.4 is named but not fixed, sec. 4.1 states the condition the whole construction rests on, and sec. 11 lists what is unresolved.

---

## 1. What this note adds

The other notes are demand-side and structural. RN-01 and RN-02 give the demand representation and its verification, RN-05 gives the sub-slot substrate, RN-10 gives the economics of a two-sided market in flexibility, and RN-11 states the allocation problem whose dual is the term structure. None proposes a fee mechanism, and RN-10 says so directly.

This note proposes one, at the smallest scope the argument admits: a single slot, an existing block, no new state. The design goal is that it change EIP-1559 as little as possible. The base fee rule is untouched, the burn is untouched, aggregate builder revenue from the tip field is untouched, and the transaction format gains one signed integer.

---

## 2. The mechanism

### 2.1 The field

Each transaction carries `TLF`, a signed integer number of ticks, bounded by a cap:

```text
-TLF_MAX  <=  TLF_i  <=  TLF_MAX          TLF_i integer
```

A tick is a fixed protocol constant in wei per gas. The declaration is coarse by design (sec. 2.4).

**The cap is a fraction of the prevailing base fee, not an absolute constant:**

```text
TLF_MAX  =  floor( r * base_fee / tick )        r < 1/2
```

Section 2.3 gives the reason: any fixed constant is unsafe at some base fee. Safety forces the proportional form, and it is also the form to prefer on other grounds. The expressible temporal range widens when execution is expensive and narrows when it is cheap, which is the right direction, since flexibility about position is worth more when position is expensive. And the specification carries no magic number: `r` is a ratio, and the number of available bands stays roughly constant as the base fee moves.

The sign is a marker of which side of the market the transaction is on, fixed at submission:

- **`TLF` < 0, the temporal-liquidity provider.** Offers to take inclusion at a later position within the slot, and receives a discount. Inclusion is unchanged: the transaction is in the same block, later in it, and nothing is deferred to a later slot. This is the supplier of RN-10 sec. 8.1.
- **`TLF` > 0, the temporal-liquidity consumer.** Bids for inclusion at an earlier position within the slot, and pays a premium. This is the taker.
- **`TLF` = 0**, the default, is neither and reproduces current behaviour.

**`TLF` is the Temporal Execution Profile, collapsed to one number.** RN-01 and RN-02 define the TEP as a transaction's declaration of its own temporal characteristics. This note takes the smallest version of that object which is still useful: a single signed scalar, whose magnitude is what the sender will pay or accept and whose **sign is a flag for the direction of temporal liquidity**. Positive consumes it, negative supplies it.

A full TEP carries a deadline and a decay function, and those are different things: a transaction with a hard deadline and one whose value falls smoothly are not interchangeable, and one number cannot separate them. Nothing here recovers that distinction. The claim is only that the one-number form is enough to open a second side of the market inside an existing block, and that the richer object belongs with the stream-level TSP in later work on inter-slot temporal liquidity.

The two sides are the substance of the proposal. Under EIP-1559 the priority fee bids for inclusion with no qualifier attached, so there is no position market in the protocol at all, on either side; position is traded anyway, out-of-band, which is the subject of sec. 7. The signed field attaches the qualifier and lets it run in both directions:

```text
today       bid for inclusion
TLF > 0     bid for inclusion, earlier position within the slot
TLF < 0     offer of inclusion, later position within the slot
```

Inclusion is common to both sides and is not what is traded. Position within the slot is. The negative side is the one that exists nowhere today.

RN-10 and RN-11 use *supplier* and *taker* for the same partition. The vocabularies should be reconciled across the notes rather than left to run in parallel.

### 2.2 The reference

For the included set `S` of a block, with `g_i` the gas used by transaction `i`:

```text
base_TLF  =  ( sum_{j in S} g_j * TLF_j ) / ( sum_{j in S} g_j )
```

The gas weighting matters. An unweighted mean balances in units of price rather than in ETH, and the transfer would not close.

The division must be fully specified, as integer division with a stated rounding rule, so that every validator computing `base_TLF` from the same block obtains the same value. Any residual left by rounding must be assigned by a stated rule, or the deviations will not sum to zero and the balance of sec. 3 will not hold at the last wei. This is a consensus requirement rather than an accounting nicety.

Define the deviation `d_i = TLF_i - base_TLF`. Then by construction:

```text
sum_{i in S} g_i * d_i  =  0
```

### 2.3 The payment rule

```text
tip_i  =  min( max_fee_i - base_fee , max_priority_fee_i )  +  d_i

payment_i  =  g_i * ( base_fee + tip_i )
burn_i     =  g_i * base_fee
```

No transaction may be paid to transact, so the realised total must stay positive. That requirement is what fixes the cap rule of sec. 2.1, and the two must be stated together.

**Why a floor would not do.** Imposing `base_fee + tip_i >= 0` as a clipping rule is the obvious way to enforce it, and it destroys the balance of sec. 3. When the clip binds, the deviation actually applied to that transaction's payment is no longer `d_i`, so the applied deviations no longer sum to zero and the block runs a deficit against the burn with no party covering it. The rounding discipline of sec. 2.2 would be holding the balance to the last wei while a far larger hole opened here.

**The cap rule removes the case instead.** Since `tip0_i >= 0` and `base_TLF >= -TLF_MAX`, the worst deviation any transaction can carry is `d_i >= -2 * TLF_MAX`, so:

```text
base_fee + tip_i  >=  base_fee - 2 * TLF_MAX
```

With `TLF_MAX = r * base_fee / tick` and `r < 1/2`, the right-hand side is strictly positive for every transaction in every block. No clipping rule is needed, nothing is ever paid to transact, and the deviations that enter payments are exactly the deviations that sum to zero. The worst case is constructed rather than sampled, since random blocks essentially never produce the adversarial composition: a lone provider at `-TLF_MAX` in a block of consumers, where `base_TLF` approaches `+TLF_MAX`. At `r = 0.45` the worst realised fee is 10.06 per gas, at `r = 0.49` it is 2.07, at `r = 0.5` it is 0.07, and at `r = 0.6` it is negative. A fixed cap does reach the boundary: at a base fee of 5 with `TLF_MAX` of 25, a third of transactions clip. See `sims/rn15_tlf_balance.py`.

The binding constraint is therefore `r < 1/2`, and it is the reason the cap cannot be an absolute constant. A constant chosen to be safe during congestion becomes unsafe when the base fee falls, which is when provider traffic is most likely to be present.

The adjustment sits outside the `min`. Placing it inside, as `min(max_fee_i - base_fee + d_i, max_priority_fee_i)`, preserves `max_fee` as a hard cap but breaks exact balance: for transactions where the priority-fee branch binds, `d_i` does not enter the payment, and the deviations no longer sum to zero over what is actually paid. Most mainnet transactions set `max_fee` well above `base_fee` for headroom, so that branch binds often enough for the leakage to be material. The variant is recorded here because the `max_fee` semantics it preserves are a real property to give up; sec. 10 lists the choice as open.

Under the rule as stated, `tip_i` can be negative when `d_i < 0`. The transaction then pays less than the base fee, and the shortfall against the burn is covered by the positive side of the same block. This is the mechanism's answer to RN-14's funding question.

### 2.4 The binding rule

The declaration must bind on something. Section 4 shows that a `TLF` entering only the payment rule is inert, so the field has to purchase or cost something real. What it binds on is left open here; the leading candidate is intra-slot position.

**The tick is the quantum index.** Because `TLF` is a coarse integer, transactions sharing a value form a band, and a band is a quantum in the sense of RN-05: position is fixed *across* bands and free *within* one. Under a descending sort on `TLF`, a builder retains full ordering freedom inside each band. That freedom is what keeps bundles workable, since a backrun must sit immediately after its target and no scalar sort key can express adjacency. Coarseness is therefore a requirement, not a simplification. A near-continuous `TLF` would determine the order completely and make adjacency impossible for everyone.

Coarseness also gives determinism. Integer ticks with a stated tie-break admit exactly one ordering, which is what validators in a geographically distributed set need in order to agree without further messages.

RN-05 supplies the quanta this rule assigns, and this rule supplies RN-05's quantum an economic meaning: the band a transaction occupies is the one it paid or was paid to occupy. The mechanism needs no particular quantum size and needs quanta to carry commitment rather than consensus, which is RN-05 sec. 5.2, Option B.

Under a sort, the priority fee remains the bid for **inclusion**, and **coarse position** becomes addressable for the first time, through `TLF`. The priority fee continues to determine order within a band. Whether a sort is the right binding, or whether eligibility windows or some other construction serves better, is left to later work.

---

## 3. Budget balance

Summing over the block, with the payment rule of sec. 2.3:

```text
sum_{i in S} g_i * tip_i  =  sum_{i in S} g_i * min( max_fee_i - base_fee , max_priority_fee_i )
                             +  sum_{i in S} g_i * d_i

                          =  sum_{i in S} g_i * min( max_fee_i - base_fee , max_priority_fee_i )
```

Aggregate tip revenue is what it would have been without the field. The burn is unchanged. No balance is carried between slots. Premiums paid by the early side equal discounts received by the late side, in ETH, within the block.

**The balance is exact given the cap rule of sec. 2.1, not unconditionally.** The identity above holds over the deviations as declared. It transfers to the deviations as *paid* only if no transaction's payment is adjusted after the fact, which is what `r < 1/2` guarantees by keeping every realised total strictly positive without a clipping rule. Any variant that reintroduces clipping, or that raises `r` to or above one half, reintroduces the deficit. The cap is therefore part of the balance result rather than a separate parameter choice.

This answers RN-14 sec. 8.3 in a way the note does not anticipate. A credit to the provider and a debit on the consumer are the same instrument once the funding source is the other side of the same block. The question RN-14 leaves open dissolves rather than being answered on one side.

---

## 4. Why the payment rule alone is not sufficient

The ordering rule of sec. 2.4 is not an addition to the payment rule. Without it the mechanism does nothing.

**Proposition.** Suppose `TLF` enters the payment rule but not the selection or ordering of transactions. Then for any set `S`, the aggregate tip is independent of `{TLF_i}` (sec. 3), so a revenue-maximising builder selects the same block it would have selected without the field, and every transaction occupies the position it would have occupied. No transaction gains anything from `TLF_i > 0`, so declaring a positive charge is dominated. All declarations fall to `-TLF_MAX`, `base_TLF` equals `-TLF_MAX`, every `d_i` is zero, and the field is inert.

The mechanism redistributes payments only if it also redistributes positions. Coupling the two is what makes a positive declaration worth making and what gives the protocol something to verify.

The proposition bounds what sec. 2.4 can leave open. The *form* of the binding is a later question: a sort, an eligibility window, or a quantum assignment rule may all serve. Whether there is a binding at all is not open. A version of this proposal carrying only the payment rule is degenerate, and stating the mechanism without naming what `TLF` buys would leave it so.

### 4.1 The corresponding failure mode

The proposition also states the way this mechanism fails in deployment, and it is worth naming here rather than leaving it in the open questions.

The binding has to be *enforced*, not merely offered. If the ordering rule is advisory, or if it is a validity rule that builders can route around by selling position out-of-band, then position is no longer determined by `TLF` and the proposition applies directly: positive declarations buy nothing, every declaration falls to the floor, `base_TLF` reaches `-TLF_MAX`, every deviation is zero, and the field is inert while remaining in the transaction format.

This is not a limitation to be traded off against others. It is a binary condition on which the whole construction rests, and the mechanism has no partial-credit regime: a scheme that binds most of the time transfers value most of the time, but a scheme that can be routed around by the parties who build blocks binds only as long as those parties choose. Whether it can be enforced against out-of-band position sales is question 6 of sec. 11, and it is the question that decides whether the rest of this note describes anything.

---

## 5. Verification and reducibility

RN-02 argues that declared temporal characteristics must be verified against realised behaviour. RN-14 sec. 8.3 observes that supplied temporal liquidity is the one temporal claim a protocol can check after the fact, because where a transaction landed is a fact about the chain while whether it needed to be early is a private counterfactual.

Only one side needs checking, and it is the side that can be. A declaration of a later position within the slot is a claim about where the transaction lands, which the block records. A declaration of an earlier position is a claim about need, which nothing can certify, and the mechanism does not attempt it: that side pays, which is check enough.

Here the check is a monotonicity test on the block: the sequence of `TLF` values over the included transactions must be non-increasing. It is linear in block size, requires no state, and its cost does not depend on quantum size.

The test constrains the band a transaction lands in and nothing finer. Order within a band is unchecked, which is what leaves the builder the freedom sec. 2.4 requires. The verified claim is therefore coarse: the transaction occupied the quantum it declared, not that it occupied any particular offset inside it.

That last property bears on RN-05 sec. 4.3, which claims the lower bound on quantum size is set by commitment and verification cost rather than by consensus latency. Section 4.3 is a claim rather than a result. This mechanism is one case where the verification cost is provably negligible and independent of granularity. It does not establish the general claim, and RN-05 should cite it as an instance rather than as support.

The ordering rule also satisfies RN-11's reducibility constraint (RN-07): it compiles to a per-slot local parameter that a builder applies deterministically, with no coordination inside the slot.

---

## 6. What this serves

**Trading.** Early intra-slot position is what latency-sensitive execution wants, and RN-14 sec. 8.3 argues that trading is the workload most likely to come back if execution improves, since its participants move for execution reasons. The mechanism gives that demand a protocol-visible instrument for the thing it currently buys out-of-band.

**Payments.** RN-14 sec. 8.3 argues that stablecoin transfers are indifferent to their position in the block, are not worth front-running, and are therefore the natural occupants of positions nobody competes for. Under the current mechanism nobody chooses that position: a transaction lands at the back by failing to outbid. Here it is chosen, priced, and paid for.

**Oracle updates, which are the best case for this mechanism and not merely another example.** A price update is one event read by a population that wants it at different times. Liquidation engines, arbitrage and perpetual funding need the freshest value and behave like trading, so they declare positive `TLF`. Periodic rebalancing, net-asset-value and reporting calculations, and slow-moving collateral revaluation need a value within minutes rather than now, behave like payments, and declare negative. The transfer runs from the first class to the second.

What makes this the strongest case is that **both classes descend from the same event, so they arrive in the same blocks**. Section 8 records that the credit available to a provider thins as the provider share of a block rises, which is inherent to balancing inside one block. That objection is about the two sides arriving independently. Here the ratio between them is a property of the application rather than of chain-wide traffic, which is the condition under which a block has depth on both sides at once.

The delayed class is also not a degraded service. A monthly valuation computed against a price fifteen minutes old is correct, not merely tolerable. This is the same distinction sec. 7.2 cites from market data, where a conventionally delayed feed carries identical information at a fraction of the price, moved from the data layer to the execution layer.

Two caveats. Tiering a service by speed is old, from postal tiers to couriers to delayed market data, and nothing here should claim novelty for it; what is new is that the tiers can clear against each other rather than being priced administratively by a vendor. And the funding of oracle updates has a second problem this does not solve: one update serves many readers who cannot be charged individually, which is a public-good problem rather than a temporal one. A `TLF` transfer moves value between urgency classes. It does not attribute a shared output to those who read it.

A separate note in preparation treats the oracle case at length and sets out what holding such a position forward would require.

---

## 7. Where the funding comes from

Section 3 shows the tip field is conserved, which makes the mechanism look revenue-neutral for proposers and builders. That reading is incomplete, but so is the opposite one.

Intra-slot position is already sold, out-of-band. RN-14 cites Franco and Rogozinski on the concentration of block value at the top of the block, in arbitrage legs, liquidations and oracle-sensitive trades. That value currently reaches proposers through builder bids.

**Position revenue splits rather than moves.** Under the ordering rule, `TLF` determines which band a transaction occupies and the priority fee determines position within it (sec. 2.4). So the payment for position divides between two fields with different destinations: the band premium enters the tip field as a deviation and is transferred to the negative side, while the within-band competition remains a priority-fee auction whose proceeds are retained as they are today.

Which half carries the value depends on where the cap binds, and sec. 8 answers that: transactions valuing top-of-block position above `TLF_MAX` all declare `TLF_MAX`, so at the top of the block the mechanism reduces to the current auction with ties resolved on the priority fee. Since that is where the concentration cited above sits, **most of the contested value stays in the retained half.** What is redirected is the premium for coarse position in the middle of the block, which by the same citation carries considerably less.

The statement is therefore narrower than a claim that ordering revenue is redirected wholesale. The mechanism moves band-level position revenue and leaves top-of-block competition roughly where it is. That bounds the security-budget question rather than answering it: the redirected amount is the band premium below the cap, and nobody has measured it. Estimating it is the prerequisite for any claim about validator revenue in either direction, and it is listed in sec. 11.

One consequence survives unchanged. Builders retain a reason to route position sales around the rule wherever the rule is advisory rather than enforced, and sec. 4 shows what happens if they succeed: declarations fall to the floor and the field goes inert.

---

## 8. Limits

**It does not address congestion.** The base fee continues to be the only instrument acting on congestion. Reordering within a slot moves no demand between slots, so aggregate per-slot demand is unchanged and no peak is lowered.

This is a sharper limitation than it first appears, because RN-14 sec. 11 identifies the *peak* base fee as what makes a low-value transfer unincludable during congestion rather than merely late, and sec. 8.3 states that a patient transfer pays a price set by the most impatient participant in the block. Neither is touched here. The barrier RN-14 names as excluding payment traffic is left standing, and only the position-pricing half of the argument is addressed.

**The base fee is a floor, and the discount cannot reach past it.** The credit is bounded by `TLF_MAX`, which is `r * base_fee` with `r < 1/2`, so a provider still pays more than half the base fee under ordinary block composition and cannot pay less than `(1 - 2r) * base_fee` under any composition. The transfer runs entirely inside the tip field, and the base fee is burned and untouched by design.

The two pools are not the same pool, and that is what limits the mechanism where sec. 6 most wants it to work. For a low-value transfer, what makes the transaction unaffordable is the base fee rather than the tip, and the base fee is the one thing this mechanism is built not to change. A sender who cannot afford to transact at the prevailing base fee is not brought in by a fraction off it. So the workload most able to take a later position is the one least able to collect the payment for taking it. This does not follow from the choice of `r`. It follows from redistributing the tip while the barrier sits in the burn, and no setting of `r` below one half changes it.

**The credit thins as the mechanism succeeds.** The credit available to a provider is bounded by `base_TLF + TLF_MAX`. As the provider share of a block rises, the gas-weighted mean falls toward the floor and the per-transaction credit falls with it. The benefit to payment traffic declines in proportion to how much payment traffic the mechanism attracts. This is inherent to budget balance: a block of pure providers has no consumers to fund it. The magnitude of the discount under realistic block composition has not been estimated and should be, since the growth argument depends on it.

**The workload it serves best is not the one RN-14 values most.** RN-14 sec. 8.3 argues payment users are not making an execution decision at all, that their habits are held in place by counterparties, and that they would have to move together to move. An instrument that improves execution quality lands on demand that responds to execution quality, which is trading. The defensible claim is that this serves the taker side directly and the supplier side conditionally.

**The cap binds where the value is.** Every transaction that values top-of-block position above `TLF_MAX` declares `TLF_MAX`, and ties resolve on the priority fee. At the top of the block the mechanism therefore reduces to the current auction. This is what bounds the revenue redirection of sec. 7, and it cuts both ways: the scheme is least disruptive where it would otherwise be most contested, and least effective there too. Raising `r` widens the expressible range and also widens the scope for moving the mean, and it cannot pass one half without reintroducing the deficit of sec. 2.3.

**Bundle adjacency survives, conditionally.** A backrun must sit immediately after its target, and no scalar sort key expresses adjacency. Coarse ticks resolve this by leaving order free within a band (sec. 2.4), so a bundle whose members share a band is unaffected. The condition is that the members can share a band, which holds when the searcher controls all of them and fails when the bundle wraps a third party.

The composition of MEV bears on how much this matters. One 2026 breakdown of lifetime extraction gives arbitrage roughly 35%, sandwich attacks roughly 30%, liquidations roughly 25%, and other categories roughly 10%; another reports the sandwich share declining as private mempools and protected routing spread. Arbitrage and liquidations are searcher-initiated and want early position, so their transactions are consumers under this scheme and their bundles sit in a high band the searcher chooses. That is around 60% of extraction by value, and for it the scheme is close to neutral. Both figures are from secondary sources without stated methodology and should be replaced with a direct measurement.

Sandwiching is the case that does not fit, and sec. 9 treats it.

---

## 9. Threat model

**Fee predictability, and why it is smaller than it looks.** `base_TLF` is computed over the realised block, so a sender cannot know their exact fee at submission. EIP-1559 was designed to make fees knowable in advance, so this is a regression against that goal.

The regression is bounded, and the bound is tight enough to change the conclusion. Since `base_TLF` lies in `[-TLF_MAX, TLF_MAX]`, a sender knows at submission that `d_i` lies within `TLF_MAX` of `TLF_i`, so the uncertainty in the realised fee never exceeds `2 * TLF_MAX`. Under the cap rule of sec. 2.1 that is at most `2r * base_fee`, with `r < 1/2`, so the uncertainty is bounded by the base fee itself and is computable in advance from a quantity the sender already knows. What a sender loses is an exact figure; what they keep is a hard bound, which is more than EIP-1559 gives them on the priority fee, where the competing bids are unknown and unbounded.

That reframes the design choice. The alternative is to compute `base_TLF` from the previous slot, which restores an exact figure and breaks exact balance, since the deviations of this block no longer sum to zero against last block's reference. RN-10 sec. 8.6 argues that a lagged reference inherits the overshoot and slow convergence of delayed feedback control, which applies here as well. Given that the contemporaneous form is bounded rather than unbounded, the lagged variant is buying a smaller improvement than it first appears and paying exact balance for it. This is a parameter question about `r` rather than the main fork in the design, and the contemporaneous reference should be the default.

**Moving the mean.** Filler transactions can shift `base_TLF`. The cost is partly self-limiting, since a filler declaring a charge on one side pays the deviation it creates on that side, but this has not been worked through and the bound is not established. `TLF_MAX` limits the reach of any single transaction and is the main defence.

**Builder choice of the included set.** With a contemporaneous reference, the builder chooses `S` and therefore chooses `base_TLF`, and with it the split of the transfer. Balance holds for any `S`, so there is no direct profit, but the builder can favour particular senders by composition. Whether this violates RN-11's neutrality constraint needs checking.

**The scheme subsidises sandwiching of providers.** A sandwich needs the attacker's two legs adjacent to a target the attacker does not control, so both legs must sit in the target's band. The attacker's declaration is therefore pinned to the target's rather than chosen. When the target is a provider taking a discount, both attacker legs land in a band below `base_TLF` and receive the discount as well. The mechanism pays the attacker to attack the flow it is trying to recruit.

The magnitude is small against the extracted value, and the attacker still pays the priority fee, so this is unlikely to change whether an attack happens. The direction is the problem: a scheme that recruits provider flow and then credits those who prey on it has an argument to answer. Two partial defences are available and neither is worked out. Providers can route through a protected RPC, which is where much retail flow already goes and which removes the target from the public mempool. Or the discount can be made conditional on some property the attacker's legs fail, though nothing obvious presents itself, since the attacker does occupy the late band it declared.

One offsetting effect: pinning removes the searcher's freedom to buy early position and sandwich a mid-block target at the same time. A searcher must choose.

**Centralisation.** Arbitrum's Timeboost is the closest deployed instrument, and the evidence on it is negative: the express lane drove spam and centralisation. Capponi and Zhu give the theory. The differences here are that the mechanism is two-sided, budget-balanced, and does not create an exclusive lane. Whether those differences are enough to avoid the same outcome is open, and it is the question a reviewer should press hardest.

---

## 10. Which property is given up

A two-sided budget-balanced mechanism cannot have everything, and the note should say which thing it surrenders rather than leave it to a reader to discover.

**The obstruction.** Myerson and Satterthwaite show that for bilateral trade with private values, no mechanism is simultaneously incentive compatible, individually rational, budget balanced and ex-post efficient. Section 3 fixes budget balance by construction, and participation is voluntary, so individual rationality holds trivially: declaring `TLF = 0` reproduces current behaviour and is always available. That leaves incentive compatibility and efficiency, and at most one of them survives.

**This mechanism gives up incentive compatibility.** The `TLF` field is a bid, not a report. A sender pays `TLF_i - base_TLF`, and `base_TLF` is not known at submission, so the optimal declaration depends on a belief about the rest of the block. There is no dominant strategy and shading is rational. The mechanism is not DSIC and should not be described as though the declaration were truthful.

**The defence is that EIP-1559 already gave this up.** The priority fee is effectively a first-price bid: a sender pays close to their own cap, so they must estimate what others will pay, and misestimating costs them. Adding a second field with the same character does not introduce a defect that was absent; it extends one that is already there. What would be a regression is a mechanism that made the *base fee* strategic, and this does not, since the base fee rule is untouched.

**Large transactions pay less per tick than small ones.** Because a transaction's own gas contributes to the gas-weighted reference, its marginal cost of a tick is `g_i * (1 - g_i / G)` rather than `g_i`. A transaction moving the reference in proportion to its own size pays less per tick of priority than a small one:

| Gas used | Share of block | Cost per tick, relative | Effective discount |
|---:|---:|---:|---:|
| 21,000 | 0.1% | 0.999 | 0.1% |
| 500,000 | 1.7% | 0.983 | 1.7% |
| 3,000,000 | 10.0% | 0.900 | 10.0% |
| 6,000,000 | 20.0% | 0.800 | 20.0% |

The advantage equals the transaction's share of block gas. For ordinary transfers it is negligible. For a single transaction consuming a fifth of the block it is a fifth off the price of priority, which is a size advantage the protocol does not currently grant and which sits uneasily with RN-11's neutrality constraint, since the allocation would then depend on something other than declared characteristics alone. Whether it is small enough to accept, or wants a correction that excludes a transaction's own gas from its reference, is open.

Excluding own-gas has a cost: each transaction would face a slightly different reference, the deviations would no longer sum to zero against a single `base_TLF`, and the balance of sec. 3 would have to be re-derived or abandoned. The trade is neutrality against exact balance, which is the same trade sec. 2.3 and sec. 9 make in other places, and it is not obvious it should be settled the same way each time.

---

## 11. What is unresolved

Four things would change the design if answered differently. The rest of the parameter and follow-up work is tracked separately.

1. **The value of `r`.** It sets the expressible range, bounds the fee uncertainty of sec. 9, and limits the scope for moving the mean. It cannot reach one half without reintroducing the deficit of sec. 2.3, and no principle fixes it below that.

2. **Whether the ordering rule can be enforced against out-of-band position sales.** Section 4.1 shows the mechanism is inert if it cannot. This is a condition on the whole construction rather than a parameter.

3. **Whether the own-gas advantage should be corrected.** Section 10 shows a transaction's marginal cost per tick is `g_i * (1 - g_i / G)`, so a large transaction pays less per tick than a small one. Excluding own-gas from the reference removes the advantage and breaks the single-reference balance of sec. 3. The trade is neutrality against exact balance.

4. **The magnitude of the credit under realistic block composition.** Section 8 shows it thins as the provider share rises. Whether what remains is large enough to attract the workloads of sec. 6 is unmeasured, and the payments argument depends on it.

## 12. The reserve this note holds at zero

Suppose the reference were a price `P_t` posted in protocol state rather than computed from the block. Then the block's net flow is

```text
sum_{i in S} g_i * d_i  =  sum_{i in S} g_i * TLF_i  -  P_t * sum_{i in S} g_i
```

which is zero exactly when `P_t` equals the gas-weighted mean of sec. 2.2. So the mechanism of secs. 2 and 3 is the general case with `P_t` re-chosen every block to hold the net flow at zero. There is a reserve in this design already. It is pinned to zero by construction, and that is what buys the exact balance of sec. 3.

Letting it move is a different proposal. It resolves the size advantage of sec. 10 and the composition dependence of sec. 8, because a posted price does not contain the transaction's own gas and does not depend on what else is in the block. It costs exact balance, requires the protocol to hold a balance rather than only burn, and adds a second controller alongside the base fee. That is a larger change than this note argues for, and a separate note develops it together with the feedback policy it would need.

Nothing about it moves a transaction to a later slot. The allocation stays inside one slot in both versions; what would cross a slot boundary is the money, not the transaction.

## 13. Relation to other work

**Mini-blocks** (Franco and Rogozinski) auction sub-slot position through SSV-backed sub-slot auctions. The instrument is one-sided: position is sold, and the proceeds accrue to the seller. The scheme here is two-sided and budget-balanced, and the proceeds accrue to the demand that yields position.

Whether the two compose is open. Both allocate sub-slot position, so there are two prices over an overlapping good: the auction price paid to the staking parties, and the `TLF` premium paid to providers. They may compose, with the auction deciding who fills a quantum and `TLF` deciding which transactions are eligible for it, in which case a winner has bought a chunk it can fill only with consumers. They may also conflict. Settling this requires reading the proposal against sec. 2.4 rather than reasoning from the summary, and it is not attempted here.

**Preconfirmations** already carry a target slot and a target round, so sub-slot coordinates exist in deployed systems. What they do not carry is a negative side. A preconf buys a commitment about position; nothing in the design pays anyone for offering to take a later one.

**Timeboost** sells a time advantage through an exclusive lane, with the centralisation and spam results cited in sec. 9.

**EIP-4844** is the precedent for adding a fee dimension to Ethereum in production, though the dimension it added is a resource rather than a temporal one (RN-14 sec. 7.3).

---

## 14. Relationship to the other notes

RN-14 sec. 8.3 poses the problem this note answers. RN-10 sec. 8 and sec. 9.5 give the two-sided structure; this is the intra-slot, quantum-indifferent grade of RN-10 sec. 9.5, and the two other grades, delayable and callable, need inter-slot state and are not addressed. RN-11 supplies the allocation problem and the three constraints checked in sec. 5, sec. 9 and sec. 10. RN-05 supplies the intra-slot positions the ordering rule assigns, and sec. 5 above returns a case to RN-05 sec. 4.3. RN-01 and RN-02 supply the demand representation, of which `TLF` is the one-scalar collapse set out in sec. 2.1: it carries neither a deadline nor a decay function, and the distinction between the two is lost. Recovering it, and pairing the transaction-level TEP with the stream-level TSP, is the subject of a separate note on inter-slot temporal liquidity.

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- *EIP-4844: Shard Blob Transactions.* https://eips.ethereum.org/EIPS/eip-4844
- Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM*, 2024.
- Myerson, R. B. & Satterthwaite, M. A. "Efficient Mechanisms for Bilateral Trading." *Journal of Economic Theory* 29(2), 1983, 265-281.
- Franco, M. & Rogozinski, G. *Mini-Blocks: SSV-Backed Sub-Slot Auctions for Ethereum PBS.* Ethereum Research, May 2026. https://ethresear.ch/t/mini-blocks-ssv-backed-sub-slot-auctions-for-ethereum-pbs/24898
- Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN, 2026. See also *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost,* arXiv:2509.22143.
- Balance, cap and own-gas simulation supporting secs. 2.1, 2.3, 3 and 10: `sims/rn15_tlf_balance.py`, with tests asserting the published numbers in `sims/tests/` and a dated run in `sims/results/rn15_tlf_balance.txt`.
- Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper No. 4436697.
- Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. "Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security." *CCS '22*, 2099-2113.
- Nasdaq. *The Nasdaq Opening and Closing Crosses.* https://www.nasdaqtrader.com/trader.aspx?id=openclose (Net Order Imbalance Indicator, disseminated from 3:50 p.m. ET at rising cadence; cited in sec. 12.3.)
- NYSE. *Opening and Closing Auctions Fact Sheet* and *Imbalances* market data specification. https://www.nyse.com/market-data/real-time/imbalances
- TLM Research Notes: RN-01, RN-02, RN-05, RN-07, RN-10, RN-11, RN-14.
