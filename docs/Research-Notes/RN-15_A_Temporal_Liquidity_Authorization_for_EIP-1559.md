---
id: RN-15
title: "A Temporal Liquidity Authorization for EIP-1559"
subtitle: "Making the base fee a midpoint rather than a floor"
version: "2.5"
status: "Public draft - research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-06"
license: "CC-BY-4.0"
---

# RN-15 v2.5

# A Temporal Liquidity Authorization for EIP-1559

## Making the base fee a midpoint rather than a floor

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-15**  
**Version:** 2.5  
**Status:** Public draft - research note, offered in good faith for comment.  
**Scope:** One slot, one existing block, no new protocol state. No deferral instrument. The mechanism clears against Ethereum's scalar gas accounting
**Date:** 6 September 2026  

> **Licence.** CC BY 4.0, as with the rest of the research programme. If this mechanism is submitted as an Ethereum Improvement Proposal, the EIP will be written as a separate document under CC0, since EIP-1 requires every EIP to be in the public domain. This note is not that document and does not waive rights.

---

## Abstract

Under EIP-1559 the base fee is a floor. Every included transaction pays at least `base_fee` per gas, a sender cannot offer to take a later position in exchange for paying less, and a transaction whose `max_fee` falls below the block base fee is not includable in that block.

This note adds one signed field, a **Temporal Liquidity Authorization** (`TLA`), and lets the base fee sit in the middle. The field has deliberately asymmetric semantics. A positive `TLA` is a maximum lump-sum authorization in wei: the consumer funds the block-local pool and seeks earlier position. A negative `TLA` is not a subsidy request or financial cap; its sign opts into provider treatment and its magnitude commits the transaction to a later ordering quantum if included. A provider sets `max_fee < block.base_fee`, which is not includable under the current validity rule, and is included here because the consumer pool covers its **shortfall**, `base_fee + p_i - max_fee_i` per gas.

Denominating the consumer authorization in money rather than per gas removes consumer gas uncertainty from clearing. A provider's need still depends on realised gas and is handled by reserving against the provider's gas limit and settling against realised gas. Pool solvency, not negative-TLA magnitude, bounds the subsidy.

**The central question concerns the provider tip.** A provider's `max_priority_fee` authorises a maximum tip, and the builder may select an effective `p_i` within that authorisation. Raising `p_i` raises the provider's shortfall and uses more pool capacity, while increasing builder revenue on the funded transaction. With abundant identical providers, no displacement cost and a continuous approximation, builder tip revenue rises and provider inclusion falls with `p_i`. A heterogeneous counterexample shows that taking less than one provider's maximum can instead increase total builder revenue by allowing another provider to fit. The general builder optimum is unproved. **The builder chooses both the effective provider tip and the included set, within signed limits.**

---

## 1. What this note adds

The other notes are demand-side and structural. RN-01 and RN-02 give the demand representation and its verification, RN-05 the sub-slot substrate, RN-10 the economics of a two-sided market in flexibility, RN-11 the allocation problem whose dual is the term structure. None proposes a fee mechanism, and RN-10 says so directly.

This note proposes one at the smallest scope the argument admits: a single slot, an existing block, no new state. The base fee rule and the burn are untouched.

Two things change beyond arithmetic, and both are stated in sec. 9. EIP-1559 rejects `max_fee < block.base_fee` when validating a transaction for inclusion; this mechanism admits it when the same block's pool covers the shortfall. And `max_fee` stops bounding everything a transaction can pay, because the temporal authorisation is a second, separately signed number.

---

## 2. The mechanism

### 2.1 The field and the two sides

Each transaction carries one signed integer `TLA`. Its semantics are asymmetric across the sign boundary: positive units are wei of maximum consumer authorization, while negative magnitude is a temporal ordering commitment mapped to later quanta. It is not a fee per gas.

```text
c_i  =  max(TLA_i, 0)        maximum consumer authorisation in wei
k_i  = -min(TLA_i, 0)        provider later-quantum commitment index
```

| | `max_fee` | `TLA` | position | pays |
|---|---|---|---|---|
| **provider** of temporal liquidity | `< base_fee` | `< 0` | later | its own `max_fee` per gas, below `base_fee` |
| neutral | `>= base_fee` | `= 0` | unchanged | as today |
| **consumer** of temporal liquidity | `>= base_fee` | `> 0` | earlier | its ordinary fee, plus a share of `c_i` |

Provider treatment requires both `TLA_i < 0` and `max_fee_i < base_fee`. A negative TLA is the opt-in flag; the below-base-fee condition creates the shortfall. A transaction able to pay the base fee has no shortfall to close and is not subsidized as a provider merely because it declares a negative TLA.

What a consumer buys is earlier relative position. What a provider supplies is later position, and what it receives is **conditional inclusion funding**: it is included only if the pool covers its shortfall, and excluded otherwise. So the mechanism allocates position on one side and both position and inclusion on the other, and it is not accurate to say inclusion is untraded.

Both sides remain subject to the same base fee in the same slot. A provider receives no favorable base-fee update or separate base-fee class; consumer authorization only closes the provider's transaction-specific payment shortfall. The negative side exists nowhere today, and it is why the base fee has to stop being a floor: an offer to take a later position is worth nothing if the discount cannot reach the part of the fee that made the transaction unaffordable. RN-14 sec. 11 identifies the peak base fee, not the tip, as what excludes low-value payment traffic during congestion. A mechanism redistributing only the tip leaves that barrier standing.

`TLA` is the Temporal Execution Profile of RN-01 and RN-02 collapsed to one signed scalar with two branches. A full TEP carries a deadline and a decay function, and one number cannot separate financial authorization from temporal preference cleanly. Version 2.3 therefore states the asymmetry rather than treating negative magnitude as money. RN-10 and RN-11 call the same partition *supplier* and *taker*.

### 2.2 Why the authorisation is money and the shortfall is a rate

Earlier versions expressed both sides as a fee per gas and multiplied by one gas scalar. That confounded two objects.

A **provider's need is inherently per gas**, because the burn it must cover is `g_i * base_fee`. Nothing about the denomination changes that.

A **consumer's contribution need not be per gas at all.** It is funding, not a price for its own execution. Making it a lump sum removes consumer gas from the clearing entirely: the pool is what senders authorised, not what their transactions happened to burn. Section 7.6 measures what that is worth, and sec. 2.7 states what it costs.

### 2.3 The consumer side

A consumer pays its ordinary EIP-1559 charge, unchanged:

```text
exec_i  =  g_i * ( base_fee + min( max_fee_i - base_fee , max_priority_fee_i ) )
```

and in addition a share `a_i <= c_i` of its authorisation, allocated by the clearing. Its total is `exec_i + a_i`. **The temporal amount does not vary with `g_i`.**

Unused authorisation is not charged: `c_i` is a maximum, not a commitment. RN-15 refunds the unmatched amount at block settlement; RN-16 considers retaining value in a Temporal Liquidity Reserve.

TLA purchases relative position rather than successful application execution. An included consumer therefore remains liable for its allocated temporal charge if EVM execution reverts or runs out of gas, provided the block honoured its signed band. This prevents a consumer from obtaining position and then avoiding the temporal charge through deliberate failure.

### 2.4 The provider side

A provider's `max_fee` is below the block base fee, so it is not includable under the current EIP-1559 validity rule. Let `p_i` be the effective provider tip selected by the builder within the sender's signed limits:

```text
0 <= p_i <= min(max_priority_fee_i, max_fee_i)
```

The **shortfall** is

```text
s_i(p_i)  =  base_fee + p_i - max_fee_i                wei per gas
```

The provider's own capped payment `g_i * max_fee_i` divides into `g_i * p_i` to the builder and `g_i * (max_fee_i - p_i)` toward the burn. The pool supplies the remaining `g_i * s_i`. Section 7.1 shows the identity closing on a worked block.

**Scheme A** is the `p_i = 0` endpoint, where `s_i = base_fee - max_fee_i` and the builder receives nothing from providers. **Scheme B**, used here, permits `p_i > 0` up to the signed maximum. A funded provider pays the selected `p_i` to the builder per unit of realised gas.

`max_priority_fee` remains the signed maximum tip authorisation, not a guaranteed payment. The builder may choose a lower effective tip when doing so reduces the shortfall enough to fund more providers or improve total block revenue.

### 2.5 Reserve and settle

The subsidy depends on realised gas, which is unknown before execution. The mechanism does not estimate it. It reserves against the gas limit and settles against realised gas:

```text
reserve   R_i = L_i * s_i(p_i)      before execution
settle    S_i = g_i * s_i(p_i)      after execution
release   R_i - S_i                 back to the pool
```

Since `g_i <= L_i`, reservation against the consumer pool keeps settlement solvent without a gas estimate. Negative TLA does not cap the subsidy. The selected tip and complete gas-limit reservation must instead fit the sender's fee limits and remaining pool:

```text
admissible only if   0 <= p_i <= min(max_priority_fee_i, max_fee_i)
                     L_i * (base_fee + p_i - max_fee_i) <= A_remaining
```

The cost is conservative admission: a transaction with a loose gas limit reserves more than it needs, and the release is not reallocated within the block. Settlement uses the protocol-metered gas charged to the sender after the applicable gas-refund rules. A provider remains eligible for subsidy when execution reverts because it still supplied later position and consumed charged gas. An out-of-gas execution normally consumes its available gas and can settle at the reservation; in every case `g_i <= L_i`, so it cannot overdraw the reserved pool amount (sec. 7.3).

### 2.6 Clearing and ordering

The two relevant orders are different. **Provider funding selection uses shortfall. Execution ordering uses TLA.** Negative TLA opts the transaction into provider treatment and commits it to the corresponding later quantum; it does not state or cap the subsidy.

For each provider, let the effective builder tip be `p_i`, where

```text
0 <= p_i <= max_priority_fee_i
shortfall_i = s_i(p_i) = base_fee + p_i - max_fee_i
```

The builder considers providers in ascending order of this full shortfall and admits them only while the running gas-limit reservation remains within the pool `A = sum of c_i`. Full shortfall is the relevant selection key because the effective priority fee is part of the subsidy requirement: two providers with the same `base_fee - max_fee` but different `p_i` do not make the same claim on the pool. The lower-shortfall provider is considered first.

Within an equal-shortfall group the builder retains selection discretion. All else equal, a provider allowing a higher tip gives the builder a larger feasible payment, but the builder need not take the maximum. The sorting key is a per-gas rate and does not directly use transaction size, while reservation is `L_i * s_i(p_i)`, so a large gas limit may still crowd out several smaller providers. **The note does not claim this rule is efficient**; sec. 12 records that no welfare objective has been chosen.

Consumers are charged pro rata to their authorisations, summing to realised provider settlement. Unmatched consumer authorisation is refunded at block settlement. Consumers excluded from the block contribute nothing.

The positional rule is separate. Let `tla_tick` be a protocol constant and define

```text
band_i = floor(TLA_i / tla_tick)
```

using signed floor division. Blocks order bands from larger to smaller: positive-TLA consumers occupy earlier quanta, neutral transactions occupy the zero region, and funded negative-TLA providers occupy later quanta. More-negative TLA is an enforceable commitment to a later quantum if included. It is not rewarded with a larger subsidy; the consequence of the declaration is the later position itself. Builders retain ordering freedom within each band. A richer declaration of windows or deadlines belongs to a fuller TEP rather than this one-field mechanism.

### 2.7 Where `TLA` sits relative to `max_fee`

`TLA` is a **separate payment**. `max_fee` caps the EIP-1559 gas component exactly as today; the `TLA` field caps the temporal component. A sender's balance must cover `L_i * max_fee_i + c_i`.

The alternative is to fold `TLA` inside `max_fee` by dividing the authorisation by the gas limit, so `tip_i = min(max_fee_i - base_fee, max_priority_fee_i + c_i/L_i)` and the whole payment stays under `max_fee`. That form is not taken, and sec. 7.6 gives the measurement:

| Property | `TLA` inside `max_fee` | `TLA` as separate payment |
|---|---|---|
| Unit of `TLA` | wei authorisation converted to wei/gas | wei |
| `max_fee` caps | entire per-gas payment | EIP-1559 gas component only |
| Maximum balance reservation | `L_i * max_fee_i` | `L_i * max_fee_i + c_i` |
| Actual consumer credit | depends on `g_i` | independent of `g_i` |
| Credit known before execution | no | yes |
| Unused gas reduces the temporal payment | yes | no |
| `max_fee` can clip `TLA` | yes | no |
| Gas limit affects the temporal price | yes | no |
| Represents total position value | indirectly | directly |
| Compatible with existing fee intuition | more closely | requires a separate authorisation |
| Provider funding certainty | lower | higher |
| Main risk | gas-dependent underfunding | payment beyond `max_fee` |

The deciding row is provider funding certainty. Under the inside treatment, whether a provider is funded depends on how much gas *other* transactions burned; under the separate treatment the pool is what senders authorised. A provider can price the second and cannot price the first.

What this costs is stated in sec. 9: `max_fee` no longer bounds everything a transaction can pay.

---

## 3. Budget balance

Over the included set, what consumers pay in temporal charges equals what providers were short, exactly:

```text
sum of a_i   =   sum over funded providers of  g_i * s_i(p_i)
```

by construction of the apportionment, over realised gas. The burn is unchanged, no balance is carried between slots, and no external funding enters. Consumer TLA authorization and each sender's fee caps are respected separately; positivity follows from `max_fee > 0`, and the reservation rule keeps the pool solvent.

The reference implementation reported no violation of this identity or the other listed invariants across 60,000 randomized clearings under three tip policies (sec. 7.7). This is an implementation check rather than a proof or an economic-performance result.

Two things the identity does not say. Aggregate builder tip is not thereby favourable to the builder, which is sec. 8. And unmatched authorisation is not charged, so `c_i` is a maximum; sec. 12 carries the alternative reading.

---

## 4. Why the payment rule alone is not sufficient

**Proposition.** Suppose `TLA` enters the payment rule but not selection or ordering. Then no transaction gains from `c_i > 0`: it pays more and occupies the position it would have occupied anyway, so authorising is dominated by not authorising. Every consumer authorises nothing, the pool is empty, and no provider is funded. The field is inert.

The mechanism redistributes payments only if it also redistributes positions. The *form* of the binding is a later question; whether there is one is not open.

### 4.1 The corresponding failure mode

The binding must be enforced, not merely offered. If the ordering rule is advisory, or if builders can route around it by selling position out-of-band, the proposition applies directly. There is no partial-credit regime: a scheme that can be routed around by the parties who build blocks binds only as long as those parties choose. This is item 3 of sec. 12, and it is separate from sec. 8: there the builder has no reason to act, here it has a reason to route around.

---

## 5. Verification and reducibility

RN-02 argues that declared temporal characteristics must be verified against realised behaviour. RN-14 sec. 8.3 observes that supplied temporal liquidity is one temporal claim the protocol can check after the fact: where a transaction landed is recorded, while whether it privately needed early execution is a counterfactual.

The candidate rule in sec. 2.6 assigns `band_i = floor(TLA_i / tla_tick)` and requires the sequence of bands in the block to be non-increasing. Validators recompute each band from signed TLA. Positive values buy earlier quanta; negative values commit funded providers to later quanta. Negative magnitude is not checked as a subsidy cap.

Provider funding is verified separately. The builder must publish its effective `p_i` for each provider in consensus-visible block data. Validators check `0 <= p_i <= max_priority_fee_i`, recompute `s_i(p_i) = base_fee + p_i - max_fee_i`, and verify ascending-shortfall selection and gas-limit reservations against the consumer pool. A private builder choice is insufficient because shortfall, burn funding and builder payment all depend on `p_i`.

These checks are linear in block size and need no additional state. Builders retain freedom within the consumer and neutral regions and among providers with equal shortfall. Bundle adjacency therefore survives only when all required members can occupy a region in an order consistent with these checks; bundles spanning regions or wrapping a third-party transaction are not guaranteed.

The check verifies relative region and provider-selection order, not a precise percentile, inclusion probability or delay guarantee. A consumer pays for access to the early region; a provider receives conditional inclusion funding and accepts the later region. EVM success is not the verification event: an included transaction that reverts still occupied its region and remains subject to TLA settlement.

This local rule is reducible in RN-11's sense: it compiles to a per-block ordering check without coordination during execution. It is one example in which verification cost is independent of the number of bands. It does not establish RN-05's broader claim about the minimum useful quantum size.

---

## 6. What this serves

**Trading.** Early intra-slot position is what latency-sensitive execution wants, and RN-14 sec. 8.3 argues trading is the workload most likely to return if execution improves, since its participants move for execution reasons. The mechanism gives that demand a protocol-visible instrument for what it currently buys out-of-band.

**Payments.** RN-14 sec. 8.3 argues stablecoin transfers are indifferent to position, are not worth front-running, and are the natural occupants of positions nobody competes for. Today nobody chooses that position: a transaction lands at the back by failing to outbid. Here it is chosen, priced, and paid for, and because the subsidy reaches below the base fee it can reach a transfer that could not otherwise be included.

**Oracle updates, the best case rather than another example.** A price update is one event read by a population that wants it at different times. Liquidation engines, arbitrage and perpetual funding need the freshest value and authorise positively. Periodic rebalancing, net-asset-value calculations and slow-moving collateral revaluation need a value within minutes and authorise negatively. Both classes descend from the same event, so **they arrive in the same blocks**, which is the condition under which a block has depth on both sides at once. Elsewhere that ratio is a property of chain-wide traffic; here it is a property of the application.

The delayed class is not a degraded service. A monthly valuation computed against a price fifteen minutes old is correct, not merely tolerable, which is the distinction a conventionally delayed market-data feed already sells.

Tiering a service by speed is old, from postal tiers to delayed market data; what is new is that the tiers clear against each other rather than being priced by a vendor. And one problem remains untouched: an oracle update serves many readers who cannot be charged individually. A `TLA` transfer moves value between urgency classes. It does not attribute a shared output to those who read it.

---

## 7. Simulation results

From one run of `sims/rn15_report.py`, recorded in `sims/results/rn15_report.txt`, built on `sims/rn15_tla.py`. `base_fee = 30` wei per gas throughout. The published figures are asserted as tests in `sims/tests/test_rn15_tla.py`.

### 7.1 A block under TLA

Pool `A = 600,000`; reserved 360,000; settled 190,000; released 170,000.

| side | `max_fee` | `TLA` | shortfall | temporal | total paid | per gas |
|---|---:|---:|---:|---:|---:|---:|
| consumer | 60 | 400,000 | 0 | +126,667 | 5,826,667 | 38.8 |
| consumer | 45 | 200,000 | 0 | +63,333 | 3,033,333 | 33.7 |
| neutral | 50 | 0 | 0 | 0 | 1,600,000 | 32.0 |
| provider | 29 | -200,000 | 1 | -40,000 | 1,160,000 | **29.0** |
| provider | 25 | -400,000 | 5 | -150,000 | 750,000 | **25.0** |

Consumers above the base fee, providers at their own `max_fee` below it, neutral untouched. Each provider pays exactly `max_fee` per gas, whatever else is in the block.

### 7.2 Against the withdrawn v0.6 rule

Two transactions asking to be paid, one declaring nothing, under the gas-weighted mean. `base_TLF = -5.3`.

| `max_fee` | declaration | `d_i` | pays per gas | |
|---:|---:|---:|---:|---|
| 60 | 0 | +5.3 | 43.3 | declaring nothing is not neutral |
| 40 | -5 | +0.3 | 35.3 | **a transaction asking to be paid is charged** |
| 40 | -11 | -5.7 | 29.3 | |

Under v2.3 none of the three is a provider: all set `max_fee` above the base fee, so none has a shortfall. The v0.6 "provider" was never below the base fee at all. It took a discount on the tip while the barrier sat in the burn.

### 7.3 Reserve and settle

Provider with gas limit 100,000, `max_fee` 25 and selected shortfall 5, against a consumer pool with at least 500,000 available.

| realised gas | reserved | settled | released | pays per gas |
|---:|---:|---:|---:|---:|
| 21,000 | 500,000 | 105,000 | 395,000 | 25.0 |
| 50,000 | 500,000 | 250,000 | 250,000 | 25.0 |
| 80,000 | 500,000 | 400,000 | 100,000 | 25.0 |
| 100,000 | 500,000 | 500,000 | **0** | 25.0 |

The last row represents an out-of-gas case in the simulation. It settles at its reservation and releases nothing, so it cannot overdraw the pool reservation.

### 7.4 Negative TLA is an ordering commitment, not a subsidy ceiling

Hold the provider's fee fields, gas limit and selected tip fixed, so its required reservation remains 500,000. Vary only negative TLA. With `tla_tick = 100,000`:

| `TLA` | provider band | required reservation | subsidy if gas is unchanged |
|---:|---:|---:|---:|
| -200,000 | -2 | 500,000 | unchanged |
| -400,000 | -4 | 500,000 | unchanged |
| -500,000 | -5 | 500,000 | unchanged |
| -900,000 | -9 | 500,000 | unchanged |

Every row is financially admissible when the consumer pool covers the 500,000 reservation. More-negative TLA obtains no larger subsidy; it commits the transaction to a later verified band. The field therefore carries temporal ordering on the provider side rather than subsidy authorization.

### 7.5 Raising the provider tip

Pool 1,000, normalised gas 1, minimum shortfall 5, tip authorised up to 5.

| tip `p` | need each | funded | builder revenue | pool to shortfalls |
|---:|---:|---:|---:|---:|
| 0 | 5 | **200** | 0 | 1,000 |
| 1 | 6 | 166 | 166 | 830 |
| 2 | 7 | 142 | 284 | 710 |
| 3 | 8 | 125 | 375 | 625 |
| 4 | 9 | 111 | 444 | 555 |
| 5 | 10 | **100** | **500** | 500 |

For these identical providers, revenue rises and inclusion falls monotonically, with **no interior optimum in the displayed range**. This result does not extend generally to heterogeneous providers.

For the heterogeneous example in sec. 8, the pool is 1,000. The large provider has `L = 100`, realised `g = 20`, minimum shortfall 5 and maximum priority fee 5. The small provider has `L = g = 20`, the same minimum shortfall and maximum priority fee 4.

| large-provider tip | funded providers | funding order | builder provider-tip revenue | reserved |
|---:|---:|---|---:|---:|
| 5 | 1 | small | 80 | 180 |
| 3 | 2 | large, small | **140** | 980 |

At the maximum tip, the small provider has lower full shortfall and is considered first; the large provider then does not fit. Reducing the large provider's tip to 3 lets both fit and raises builder revenue from 80 to 140.

### 7.6 Inside `max_fee`, against a separate payment

One authorisation of 500,000 wei, `max_fee` 40, gas limit 200,000.

| realised gas | inside `max_fee` | separate |
|---:|---:|---:|
| 21,000 | 52,500 | 500,000 |
| 150,000 | 375,000 | 500,000 |

Four consumers each authorising 500,000, one provider needing 300,000:

| consumer gas | inside: pool | funded | separate: pool | funded |
|---:|---:|---|---:|---|
| 21,000 | 210,000 | **no** | 2,000,000 | yes |
| 60,000 | 600,000 | yes | 2,000,000 | yes |
| 150,000 | 1,500,000 | yes | 2,000,000 | yes |

### 7.7 Randomized invariant checks

The entries below are **violation counts**, not values of payments, inclusion, burn or welfare. The simulator generated 20,000 random blocks for each provider-tip policy, using base fees from 1 to 1,000, gas limits from 21,000 to 1,000,000, and realised gas no greater than each limit. Thus `0 / 20,000` means that the stated invariant was not violated in any generated block under that policy.

| invariant checked | `p = 0` violations | `p` maximal violations | `p` capped at 2 violations |
|---|---:|---:|---:|
| provider payment differs from `g_i * max_fee_i` | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| provider tip exceeds signed authorization | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| provider shortfall, reservation or settlement is inconsistent | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| ordinary execution fee exceeds `max_fee` | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| consumer temporal charge exceeds positive `TLA` | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| neutral transaction receives a temporal charge | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| a live transaction has a negative payment | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| pool reservation or settlement exceeds available funding | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| consumer temporal charges differ from provider subsidies used | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| funded-provider sequence violates ascending shortfall | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |
| execution sequence violates non-increasing TLA bands | 0 / 20,000 | 0 / 20,000 | 0 / 20,000 |

These checks test whether the reference implementation preserves the stated accounting and ordering invariants over the generated inputs. They do not prove the invariants for all valid inputs and do not establish welfare, incentive compatibility, equilibrium behaviour or deployment safety. Several checks verify properties imposed by construction—for example, exact budget balance tests the integer apportionment implementation rather than independently demonstrating that the payment rule is economically desirable.

### 7.8 Benchmark extension: target utilization

The preceding experiments test one-block accounting and builder choice. They do not yet measure the system-level question posed by RN-13 Part II: whether temporal information improves the target-utilization frontier.

For RN-15, the first benchmark is deliberately limited. Providers and consumers face the same `base_fee` in the same slot. Provider admission does not weaken the EIP-1559 price signal; it uses consumer authorization to close identified provider shortfalls. The block may nevertheless use more gas than the baseline because transactions that fail the ordinary fee-cap validity condition can become conditionally includable. That additional gas affects the next base fee in the ordinary way.

The simulation suite should therefore add paired baseline/TLA runs over identical demand traces and report:

```text
u_hard,t     = gas_used_t / gas_limit_t
u_target,t   = gas_used_t / gas_target_t
headroom_t   = gas_limit_t - gas_used_t
added_gas_t  = gas used by funded providers not admitted in the baseline
displaced_t  = baseline gas or value removed by the TLA allocation
```

It should also report admitted requests and declared value by class, next-block base fee, base-fee volatility, burn, builder revenue, consumer charges, provider subsidies, reservation efficiency, and the share of additional provider gas that uses otherwise idle capacity rather than displacing ordinary demand.

Three regimes must remain separate: underfilled blocks, blocks near the EIP-1559 target, and blocks near the hard gas limit. A rise in `u_target` is not by itself a gain. It is useful only when the added service exceeds displacement and real execution costs without unacceptable loss of headroom or worse fee dynamics. RN-15 can measure a one-slot admission and ordering gain. It cannot establish that Ethereum can safely adopt a higher long-run target ratio, because it neither carries liquidity nor defers demand across slots. That stronger test belongs to RN-16.

### 7.9 Base-fee-only baseline and preliminary multi-slot result

The target-utilization simulator first disables TLA and runs ordinary EIP-1559 over Poisson arrivals, a persistent mempool and heterogeneous fee caps. At the 50 percent target, the base fee moves after each block from the parent block's gas use. Under low offered load, utilization remains below target because the controller cannot create demand. As offered load rises, average utilization approaches the target; it need not equal it in every finite run because transactions are indivisible, fee caps are heterogeneous and some requests expire.

The RN-15 comparison uses the same arrivals and a conservative fill-only builder. It preserves the baseline ordinary block and funds providers only from included consumer TLA and otherwise unused gas. This rules out direct displacement by construction. The preliminary synthetic runs show why a multi-slot benchmark is still necessary: RN-15 can admit additional provider gas in slot (t), that gas can raise (b_{t+1}), and the higher base fee can exclude or delay transactions in later slots. A current-slot admission gain may therefore become later congestion even though providers and consumers faced the same base fee in the original slot.

This is not evidence against RN-15. It identifies its boundary. RN-15 supplies an intra-slot price and funding mechanism, not inter-slot demand smoothing. The result to carry into RN-16 is that a reserve must do more than retain unmatched money: temporal feedback must move flexible demand away from constrained slots, or additional funding can amplify the next base-fee update.

The literature gives a reason to test that interaction. Leonardos et al. model EIP-1559 as a discrete dynamical system, derive conditions sufficient for convergence, and show periodic or chaotic base-fee and occupancy behavior outside stable regimes. Reijsbergen et al. report that EIP-1559 achieved its objective on average in its first month while adjusting slowly during demand bursts and exhibiting substantial short-run occupancy variation. Ethereum's twelve-second slot converts every one-block update lag into wall-clock delay, but slot duration alone does not establish instability: the adjustment step, valuation distribution, demand elasticity, mempool policy and shock persistence also matter.



---

## 8. The provider tip and builder selection

A provider chooses `max_priority_fee` when signing the transaction. Under Scheme B, the builder may select an effective `p_i` between zero and that signed maximum. A funded provider pays the selected amount per unit of realised gas. The builder therefore chooses both the effective tip and the included provider set, within the transaction's fee and TLA limits.

For identical providers with gas (g), minimum shortfall (d), abundant supply, no displacement cost and a continuous approximation, a pool (A) funds approximately

\[
n(p) \approx \frac{A}{g(d+p)}
\]

providers, and aggregate provider-tip revenue is

\[
R(p) \approx A\frac{p}{d+p}.
\]

In that model, selecting higher effective tips gives builders more revenue per funded provider while the pool funds fewer providers. Section 7.5 illustrates the result and then gives a heterogeneous counterexample. It is not a general theorem or an equilibrium result. With indivisible providers, finite supply, heterogeneous gas limits and shortfalls, displaced ordinary tips, MEV, bundles or state conflicts, the builder's joint tip-and-subset optimum can differ.

**A large provider can make a lower tip revenue-maximising.** Selection is ordered by the per-gas shortfall, but solvency is consumed by the reservation `L_i * s_i(p_i)`, while realised builder revenue is `g_i * p_i`. Increasing `p_i` by one unit therefore consumes `L_i` additional wei of pool authorization and produces only `g_i` additional wei of realised tip. When `g_i/L_i` is low, taking the full priority authorization can be a poor use of the pool.

For example, let the pool be 1,000, and let both providers have minimum shortfall 5. Provider 1 has `L_1 = 100`, expected `g_1 = 20`, and `max_priority_fee_1 = 5`. Provider 2 has `L_2 = g_2 = 20` and `max_priority_fee_2 = 4`. At `p_1 = 5`, Provider 1 reserves 1,000 by itself and yields expected tip revenue 100; if Provider 2 is considered first by its lower full shortfall, Provider 1 does not fit and revenue is only 80. At `p_1 = 3`, Provider 1 reserves 800 and Provider 2 reserves 180, so both fit; expected builder revenue is `20*3 + 20*4 = 140`. The revenue-maximising builder therefore selects less than Provider 1's authorized maximum. The example also shows why per-gas ordering does not eliminate gas-size effects: `L_i` enters the funding constraint even though it does not enter the ranking key.

The proposer-auction conclusion is also conditional. If two builders face the same ordinary block value, costs and constraints, but one realises more provider-tip revenue, it can submit a higher proposer bid. A highest-monetary-bid auction then favours the more monetisable allocation. It does not directly reward the number or execution value of additional providers.

This is not a selfish builder against a public-spirited one. Both use rules the mechanism permits. The useful terms are **inclusion-maximising** and **revenue-maximising**, and the difficulty is that the proposer auction rewards one objective while the network may care about the other.

**Scheme A, `p_i = 0`, directs the pool to minimum shortfalls** and funds the most identical providers in the simplified model. In an underfilled block, admitting them need not displace tip-paying gas. In a full block, however, a zero-tip provider displaces positive-tip gas and reduces builder revenue. A builder can avoid that loss by supporting the transaction type but admitting no providers, so mere implementation need not cost it while use of the provider side does.

**Scheme B gives the builder provider-tip revenue** but uses more pool capacity per provider and generally reduces inclusion. The reduction is not in exact proportion under indivisibility or heterogeneous gas. The simulation's maximum-tip case divides its particular pool equally between minimum shortfalls and provider-authorised tips; that ratio is not universal.

**The unresolved problem is joint tip and subset selection.** Providers choose signed tip ceilings; builders choose effective tips and the included subset. Alternatives include requiring the full signed tip, imposing a protocol cap or rule, proposer scoring on inclusion as well as payment, or a cleared provider-tip rate. None of those alternatives is selected here.

**What the builder does if denied.** A builder can sell provider inclusion out-of-band. Coinbase-transfer bundle payments are not tips, so no rule here constrains them, and reordering for extraction sits outside the fee fields entirely. That outcome should be expected rather than treated as abuse, and nothing in this design bounds it.

---

## 9. Limits

**Below-base-fee inclusion changes consensus validity and block construction.** EIP-1559 requires `max_fee >= block.base_fee` for a transaction included in a valid block. Retention and gossip below the current base fee are client txpool policies, not the consensus rule. Under TLA, a provider with `max_fee < block.base_fee` becomes valid only if the same block contains enough consumer authorisation and the reservation and settlement rules hold. Includability therefore depends jointly on block composition. Clients need explicit policies for storing, propagating and selecting these conditional transactions.

**`max_fee` no longer bounds the complete fee liability.** It continues to cap the EIP-1559 execution-gas price. Positive TLA separately caps the temporal charge. A consumer must be able to cover `L_i * max_fee_i + c_i`, excluding attached value and any other fee dimensions. Its realised fee payment is at most `g_i * max_fee_i + a_i`, where `a_i <= c_i`. Wallets must display both authorisations.

**The mechanism carries no inter-slot deferral instrument.** Negative TLA purchases a later intra-block band and conditional inclusion funding; it does not schedule execution for a named future slot. The base fee remains the principal price acting on demand across blocks. RN-15 can change one block's utilization and therefore the next base fee, but it cannot smooth demand over several slots or justify a smaller EIP-1559 elasticity reserve. Inter-block retention, feedback and that target-utilization question belong to the TLR mechanism in RN-16.

**Funding is bounded and prioritised, not confined to near-marginal demand.** Total provider subsidy cannot exceed charged consumer TLA. Cheapest-full-shortfall-first accounts for both the base-fee deficiency and the selected provider tip. It prioritises the least expensive complete subsidy claims per gas, but a deeply excluded provider can still be funded if the consumer pool covers its reservation. A block containing only providers funds none under RN-15.

**Gas-limit reservation creates intra-block funding slack.** A loose gas limit may reserve substantially more than realised subsidy. The unused reservation is released and ultimately refunded to consumers, but without a second clearing pass it cannot fund another provider in the same block. The resulting loss is unused matching capacity, not lost money.

**Base-fee and burn effects are conditional.** EIP-1559 adjusts the next base fee from parent-block gas used relative to target, not from transaction count. If TLA only changes the composition of an already-full block, gas used, burn and the next base-fee signal may be unchanged. If it fills gas that would otherwise remain unused and pushes usage above target, the next base fee rises; if usage remains below target, it still falls, though by less. A higher future base fee may then suppress demand and enlarge later provider shortfalls. Total burn need not rise monotonically over the adjustment path.

**Additional burn is not builder revenue.** Burned ETH is destroyed rather than transferred to the builder, proposer or existing holders. Any holder benefit through lower net issuance is diffuse and uncertain and is shared with parties that did not adopt TLA. It is therefore not a reliable builder incentive. Additional execution improves network welfare only when its value exceeds execution, validation, state-growth, mechanism and strategic costs, none of which this note estimates.

**Failure semantics are positional.** An included consumer remains liable for allocated TLA when execution reverts because it received the signed band. A funded provider remains eligible for subsidy on protocol-metered gas charged after refund rules because it supplied its later band and incurred a burn shortfall. Out-of-gas execution cannot exceed the gas-limit reservation. These rules prevent application-level failure from avoiding a temporal obligation, but their strategic effects remain unmeasured.

**Bundle adjacency survives only within bands.** Builders retain freedom inside a band, so a bundle whose required members share one band may preserve adjacency. Bundles spanning bands or wrapping a third-party transaction may fail.

---

## 10. Threat model

**Fee predictability.** A provider's payment is not uncertain: `g_i * max_fee_i` if funded, not included otherwise. What it faces is inclusion risk rather than fee risk, the same exposure a low-tip transaction faces today. A consumer's temporal charge lies between zero and `c_i`, a number it chose.

**Builder substitution into channels the mechanism cannot see.** The threat with the clearest incentive behind it, and sec. 8 gives its shape. Coinbase-transfer bundles and reordering both sit outside the fee fields, so no rule here reaches them.

**Strategic lateness declarations.** A more-negative TLA produces no larger subsidy but commits the provider to a later quantum. A provider should therefore choose the least costly band consistent with its temporal preference, but no truthful-reporting result is established. Separately, lowering `max_fee` increases the subsidy requirement and reduces funding probability; no equilibrium is derived for either choice.

**Filler manipulation of the pool.** A transaction can enlarge the pool to fund an affiliate provider, or crowd others out with cheap shortfalls. Enlarging the pool costs real payment and is partly self-limiting; crowding is cheap and the bound is not derived.

**Builder choice of the included set.** The builder chooses which candidates enter the clearing, and therefore the pool, the shortfalls, and which providers are funded. Balance holds for any set, so there is no direct arbitrage, but the builder can favour particular senders by composition. Whether this violates RN-11's neutrality constraint needs checking.

**Sandwiching of providers.** Both attacker legs must sit in the target's TLA band. An attacker must therefore sign a similar negative TLA and, if it is also a provider, qualify for funding from the same pool. It takes on the target's inclusion risk and competes for funding with the flow it preys on. The attack is not excluded; whether the cost is large enough to matter is unestimated.

**Centralisation.** Arbitrum's Timeboost is the closest deployed instrument and the evidence is negative: the express lane drove spam and centralisation. This mechanism is two-sided, budget-balanced, and creates no exclusive lane. Whether that is enough is open, and it is the question a reviewer should press hardest.

---

## 11. Which property is given up

**This mechanism is not incentive compatible.** A consumer's realised price per unit of position depends on the rest of the block, so the optimal authorisation depends on a belief about what else arrives. There is no dominant strategy and shading is rational. The authorisation is a bid, not a report.

**EIP-1559 already gave this up.** The priority fee is effectively a first-price bid: a sender pays close to their own cap, must estimate what others will pay, and misestimating costs them. A second field with the same character extends a defect rather than introducing one. What would be a regression is making the base fee strategic, and this does not.

**Two properties earlier versions lacked are present.** Declaring `TLA = 0` leaves payment and position untouched regardless of block composition, so participation is voluntary in the ordinary sense; under the v0.6 mean rule a zero declaration was charged (sec. 7.2). And the consumer contribution no longer depends on the transaction's own gas.

Version 0.6 deduced from Myerson and Satterthwaite that fixing budget balance and individual rationality forces a choice between incentive compatibility and efficiency. That deduction is withdrawn: this is not a bilateral-trade mechanism with a neutral outside option and an exogenous participant set, since inclusion is endogenous and the builder chooses the candidate set.

---

## 12. What is unresolved

1. **The equilibrium provider tip and builder selection rule** (sec. 8). Providers sign `max_priority_fee`; builders choose and publish an effective `p_i` within that authorization and choose the included subset. The simplified model and simulations show a trade-off between tip revenue and provider count; the provider bidding equilibrium and general builder subset optimum remain open.

2. **What objective the provider allocation should serve.** Cheapest-shortfall-first maximises the count funded; builder revenue favours positive-tip gas; temporal allocation should arguably depend on position-sensitive value. **The note states no welfare function**, so it can establish accounting properties but cannot call any ordering efficient. The rule in sec. 2.6 is illustrative.

2a. **Whether one asymmetric TLA scale is the correct band key.** In v2.3 positive magnitude is monetary authorization while negative magnitude is temporal commitment. One signed ordering scale is easy to verify but does not have symmetric economic units. Alternative mappings from each branch into common bands may produce different allocations and manipulation surfaces.

3. **Whether the ordering rule can be enforced against out-of-band position sales** (sec. 4.1). The mechanism is inert if it cannot.

4. **How often ordinary paying demand fills the gas limit on mainnet.** This helps determine whether Scheme A providers use idle gas or displace positive-tip transactions, and it is unmeasured. Blocks sitting near the gas target rather than the limit suggest spare capacity may be common, but that is an inference.

5. **Whether wallets leave enough `max_fee` headroom** that folding `TLA` inside it would rarely clip. This is measurable from mainnet today and decides how much the choice in sec. 2.7 actually costs.

6. **Whether a later mechanism should retain unmatched authorisation across blocks.** RN-15 refunds unmatched authorisation and carries no balance. RN-16 studies retention through a Temporal Liquidity Reserve and must specify ownership, solvency and withdrawal.

7. **How low a provider should set `max_fee`**, trading subsidy size against probability of funding. No equilibrium is derived.

8. **Whether the release from over-reservation should be reallocated** within the block, and what a second pass would cost.

9. **The magnitude of the transfer under realistic block composition.** Nobody has measured how often the two sides meet in one block on mainnet.

10. **The target-utilization effect of additional provider gas** (secs. 7.8 and 9). The effect is conditional on gas used relative to target and hard limit, displacement, and later demand response. Its distribution across newly included users, already-included users and ETH holders is not estimated. Nor does RN-15 establish that a higher long-run target ratio is safe.

11. **How the mechanism should account for MEV, bundles, state conflicts and displaced ordinary tips**, none of which the simulations model.

---

## 13. What one block cannot do

Two limitations share a cause. **Both sides must meet in one slot**, so a consumer and a provider that would trade at different slots do not trade at all, and thin blocks clear nothing. And **the builder cannot be paid except out of the consumer pool**, which is the trade-off of sec. 8.

Holding a balance across slots relaxes both. A block with surplus authorisation would retain it, a block short of it would draw, and a provider could be funded out of an earlier block's surplus. The constraint becomes intertemporal solvency rather than per-block balance, and value held over from one block can pay a builder in another without any single block extracting from its own consumers.

RN-16 develops this. It requires the protocol to hold a balance rather than only burn, adds temporal feedback coupled to the base-fee controller, and needs rules for sustained one-sided demand and reserve depletion. Its design goal is to combine the block elasticity reserve with a Temporal Liquidity Reserve so that flexible demand can be shifted across slots and the target-utilization frontier can be tested at fixed reliability. It also inherits the private-channel problem of sec. 8.

Carrying money alone does not move a transaction to another slot. RN-16 must pair the reserve with an inter-slot scheduling or deferral rule. Without that rule, additional funding may raise later base fees without smoothing demand.

---

## 14. Relation to other work

**Mini-blocks** (Franco and Rogozinski) auction sub-slot position through SSV-backed sub-slot auctions. The instrument is one-sided: position is sold and the proceeds accrue to the seller. This scheme is two-sided and budget-balanced, and the proceeds accrue to the demand that yields position. Whether the two compose is open, since there would be two prices over an overlapping good.

**Preconfirmations** already carry a target slot and round, so sub-slot coordinates exist in deployed systems. What they lack is a negative side: a preconf buys a commitment about position, and nothing pays anyone for offering to take a later one.

**Timeboost** sells a time advantage through an exclusive lane, with the centralisation and spam results cited in sec. 10.

**EIP-4844** is the precedent for adding a fee dimension to Ethereum in production, though the dimension it added is a resource rather than a temporal one (RN-14 sec. 7.3).

**EIP-1559 dynamics.** Leonardos et al. show that convergence depends on the adjustment step and demand environment; periodic and chaotic occupancy are possible outside stable regimes. Reijsbergen et al. find slow burst response and short-run occupancy variation despite acceptable average behavior. EIP-4396 separately shows how missed slots can make a following block signal a misleading demand spike. These results motivate the RN-16 comparison among base-fee-only, adaptive-base-fee and base-fee-plus-TLR designs; they do not establish that TLR is necessary or stable.

---

## 15. Relationship to the other notes

RN-14 sec. 8.3 poses the problem this note answers, and RN-14 sec. 11 identifies the base fee rather than the tip as the barrier, which forces the midpoint construction of sec. 2.1. RN-10 sec. 8 and sec. 9.5 give the two-sided structure; this is the intra-slot, quantum-indifferent grade of RN-10 sec. 9.5, and the delayable and callable grades need inter-slot state and are not addressed. RN-11 supplies the allocation problem and the constraints checked in secs. 5, 10 and 11, and its term structure is where a priced version of this mechanism would connect. RN-05 supplies the intra-slot positions the ordering rule assigns, and sec. 5 returns a case to RN-05 sec. 4.3. RN-01 and RN-02 supply the demand representation, of which `TLA` is the one-scalar collapse: it carries neither a deadline nor a decay function. Recovering that distinction, and pairing the transaction-level TEP with the stream-level TSP, is the subject of a separate note on inter-slot temporal liquidity.

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- *EIP-3529: Reduction in refunds.* https://eips.ethereum.org/EIPS/eip-3529
- *EIP-4844: Shard Blob Transactions.* https://eips.ethereum.org/EIPS/eip-4844
- Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM*, 2024.
- Leonardos, S., Monnot, B., Reijsbergen, D., Skoulakis, S. & Piliouras, G. “Dynamical Analysis of the EIP-1559 Ethereum Fee Market.” arXiv:2102.10567. https://arxiv.org/abs/2102.10567
- Reijsbergen, D., Sridhar, S., Monnot, B., Leonardos, S., Skoulakis, S. & Piliouras, G. “Transaction Fees on a Honeymoon: Ethereum's EIP-1559 One Month Later.” arXiv:2110.04753. https://arxiv.org/abs/2110.04753
- *EIP-4396: Time-Aware Base Fee Calculation.* https://eips.ethereum.org/EIPS/eip-4396
- Myerson, R. B. & Satterthwaite, M. A. "Efficient Mechanisms for Bilateral Trading." *Journal of Economic Theory* 29(2), 1983, 265-281.
- Franco, M. & Rogozinski, G. *Mini-Blocks: SSV-Backed Sub-Slot Auctions for Ethereum PBS.* Ethereum Research, May 2026. https://ethresear.ch/t/mini-blocks-ssv-backed-sub-slot-auctions-for-ethereum-pbs/24898
- Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN, 2026. See also *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost,* arXiv:2509.22143.
- Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper No. 4436697.
- Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. "Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security." *CCS '22*, 2099-2113.
- Nasdaq. *The Nasdaq Opening and Closing Crosses.* https://www.nasdaqtrader.com/trader.aspx?id=openclose
- NYSE. *Opening and Closing Auctions Fact Sheet* and *Imbalances* market data specification. https://www.nyse.com/market-data/real-time/imbalances
- Clearing rule: `sims/rn15_tla.py`. Accounting figures: `sims/rn15_report.py`. Target-utilization model: `rn15_target_utilization_frontier.py`, with design and generated aggregate results published alongside this note.
- TLM Research Notes: RN-01, RN-02, RN-05, RN-07, RN-10, RN-11, RN-13 Part II, RN-14, RN-16.
