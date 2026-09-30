---
id: RN-15
title: "A Temporal Liquidity Authorization for EIP-1559"
subtitle: "Early-region service, below-floor providers, second-price settlement and separate metering"
version: "3.1"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-30"
license: "All rights reserved"
---

# RN-15 v3.1

# A Temporal Liquidity Authorization for EIP-1559

## Early-region service, below-floor providers, second-price settlement and separate metering

**Temporal Liquidity Market (TLM) Research Program**
**Research Note RN-15**
**Version:** 3.1 (supersedes v3.0)
**Scope:** One slot, one block. No state carried between slots.
**Date:** 30 September 2026

---

## Abstract

Under EIP-1559 the base fee is a floor, and a fee bid buys no enforceable position in the block. This note adds one signed field, a Temporal Liquidity Authorization (`TLA`). A consumer signs a positive `TLA`, a lump sum in wei, and if selected is guaranteed to complete within an early region of the block, ranked among selected consumers by `TLA` per unit of gas limit. A provider signs a negative `TLA`, sets its fee cap below the base fee, and accepts execution after that region; it is admitted when consumer payments cover its shortfall.

Two rules carry the design. **Consumers are charged a second price**: each selected consumer pays the density of the next bid below it in the selection order, so rank cannot be bought at a price set by others; the surplus over provider funding is burned. **Funded provider gas is excluded from the base-fee controller's input** and bounded by an allowance: counted in the controller, it raises the base fee and displaces ordinary demand; excluded, the ordinary allocation and base fee are unchanged and total utilization rises above the target.

**Protected service is sold only against provider supply**: the consumer gas allowance in a block is proportional to the funded provider gas, so a block without funded providers selects no consumers, and thin provider supply makes early service scarce.

The mechanism requires protocol support. A numerical study of consumer bidding under the second-price rule (sec. 3.5) finds that shading falls as competition for protected position rises, and that the consumer floor sets revenue when competition is thin.

---

## 1. What changes

Three things change relative to EIP-1559, and nothing else.

1. **Validity.** A transaction with `max_fee < base_fee` can be included when it opts into the provider branch and the block's consumer payments cover its shortfall.
2. **Ordering.** Validators check two positional constraints: selected consumers complete within an early region, ranked by authorization density; funded providers start after it. All other ordering stays with the builder.
3. **Metering.** The base-fee controller measures ordinary gas only. Funded provider gas is counted against the block gas limit but not against the target, and is capped separately.

The burn, the base-fee update rule, and the treatment of transactions that do not use the field are unchanged.

---

## 2. The mechanism

### 2.1 The field

Each transaction may carry one signed value `TLA_i`.

```text
TLA_i > 0    consumer: lump-sum authorization c_i in wei, seeks early-region service
TLA_i = 0    neutral: ordinary EIP-1559 treatment
TLA_i < 0    provider: opts into later execution; only the sign is used
```

The magnitude of a negative `TLA` has no effect on shortfall, settlement, funding or ordering. Only the sign selects the provider branch.

### 2.2 Consumers: selection and service

Let `L_i` be consumer `i`'s gas limit. Its **authorization density** is

```text
rho_i = c_i / L_i
```

Two quantities bound selection. A protocol parameter `K_C = kappa_C * K`, with `K_C <= E`, is the most consumer gas that can ever be selected. The **consumer allowance** of the block is

```text
A_C  =  min( K_C , theta * G_P )
```

where `G_P` is the realized gas of the funded providers (sec. 2.5) and `theta` is a protocol parameter. Candidates must first be valid EIP-1559 transactions (`max_fee >= base_fee`) included in the block. They are processed in decreasing density, ties broken by transaction hash, and each is added to the selected set `C*` if its gas limit fits the remaining `A_C`; otherwise it is skipped. A consumer that is not selected stays in the block as an ordinary transaction.

A selected consumer receives:

- **completion within the early region** `E = chi * K`, measured in cumulative charged gas: its execution ends before the block's cumulative gas crosses `E`;
- **rank among selected consumers by density**: removing every transaction outside `C*` from the block leaves them in decreasing `rho_i`.

`A_C` decides how many consumers are served; `E` decides where they must finish. `E` is fixed, so what a consumer buys is the same in every block: completion before the block's cumulative gas crosses `E`, whatever the number of consumers selected. Neutral transactions may appear anywhere, including before or between selected consumers in the early region, at the builder's discretion.

Density uses the signed gas limit, so padding `L_i` lowers a consumer's rank and raises its charge. The allowance keeps a large number of nominal authorizations from all qualifying.

### 2.3 Providers: admission below the floor

A provider signs `TLA_i < 0`, sets `max_fee = m_i < b`, and must begin after `E`. For an effective tip `p_i` with `0 <= p_i <= max_priority_fee_i`, its per-gas **shortfall** is

```text
s_i = b + p_i - m_i
```

For realized gas `g_i`, the provider pays `g_i * m_i`, the consumer payments cover `g_i * s_i`, the protocol burns `g_i * b`, and the builder receives `g_i * p_i`. The base fee is fully burned; what changes is who pays it.

### 2.4 Reference-preserving admission

Provider admission must not remove ordinary transactions. The builder proceeds in two stages.

1. **Reference block.** Build the block from neutral transactions and consumers as it would be built without providers. Call its realized gas `H^0`.
2. **Providers.** Add providers without removing any transaction in the reference block, subject to

```text
sum over funded providers of  g_j * s_j   <=   R            (funding, sec. 3)
sum over funded providers of  g_j         <=   A = min( P_bar , K - H^0 )
```

where `P_bar` is the provider-gas allowance and `R` the total consumer charge of sec. 3. Both constraints are evaluated on realized gas. A reference implementation scans eligible providers in increasing shortfall.

**Every transaction in the reference block is retained, and providers are added only in residual capacity.** The block is physically feasible, and its realized gas rises by exactly the funded provider gas.

### 2.5 Linking consumer service to provider supply

Consumer service and provider funding determine each other only through two quantities: the consumer allowance `A_C` depends on the funded provider gas `G_P`, and which providers can be funded depends on the consumer charges `R`. A provider's shortfall `s_j = b + p_j - m_j` depends only on its own fields, and every consumer candidate is in the reference block whether or not it is selected, so the physical block does not depend on selection.

Validators do not solve for the pair. They check that the block's pair of sets is consistent:

1. the selected consumers are the greedy density prefix of the eligible candidates under `A_C = min(K_C, theta * G_P)`;
2. consumer charges follow sec. 3.1 on that selection order;
3. the funded providers satisfy `sum of g_j * s_j <= R` and `sum of g_j <= A` (sec. 2.4), with `G_P = sum of g_j`;
4. selected consumers complete within `E` in density order, and funded providers start after `E`.

A builder finds a consistent pair by starting from all eligible consumers and providers and trimming alternately: select consumers under the current allowance, compute `R`, fund providers against `R`, recompute `A_C`, and repeat. Each step can only shrink the sets, so the procedure ends after a few rounds.

All quantities are **realized**. The builder has simulated the block, and validators check it after execution, as they check gas used. A provider that signs a large gas limit but uses little gas adds only what it uses to `G_P` and to the funding check, so it can neither enlarge the consumer allowance nor tie up the pool.

`theta` sets how much consumer gas each unit of funded provider gas supports. With `theta = 1`, one unit of early-region consumer gas requires one unit of provider gas moved after `E`.

---

## 3. Settlement: second-price charges

### 3.1 The rule

Eligible candidates are processed in decreasing density, as in sec. 2.2, and each is selected if it fits the remaining `A_C`. Every selected consumer `k` pays the density of the **next eligible transaction after it in that processing order**, whether that transaction was selected or skipped:

```text
a_k  =  max( rho_next(k) , beta * b ) * L_k
```

If no eligible transaction follows `k`, it pays the consumer floor. Only candidates with `rho_i >= beta * b` are eligible, where `b` is the block's base fee and `beta` is a dimensionless protocol parameter. Density and base fee are both in wei per gas, so the consumer floor `beta * b` is a density; in wei the condition reads `c_i >= beta * b * L_i`. Candidates skipped by the allowance stay in the block as ordinary transactions, so validators can see the prices they set. The next transaction in processing order never has a higher density than `k`, so `0 <= a_k <= c_k` for every selected consumer.

One order does both jobs. Selection walks down the processing order, and each consumer's price is the bid immediately below it in that order: the lowest density at which it would still come before that rival. A skipped transaction therefore prices the consumer that displaced it. Example: `K_C = 10`; A (density 10, gas limit 6) is selected, B (8, 6) is skipped because only 4 remains, C (5, 4) is selected, D (3, 4) is rejected. A pays `8 * 6 = 48`, since bidding below 8 would let B in first and leave no room for A. C pays `max(3, beta * b) * 4`. Pricing against the next selected consumer instead would charge A only `5 * 6 = 30`, below what it takes to keep its place, and would raise less to fund providers.

The consumer floor matters only when the allowance is slack. When `A_C` binds, the lowest-ranked selected consumer is priced by a skipped or rejected rival, as in a standard second-price auction. When it is slack, every eligible consumer is served and the last pays the consumer floor, so a lone consumer does not obtain protected position for free. The consumer floor scales with congestion through `b`. Two alternatives were considered and rejected. Charging the last consumer its own density makes its bid set its own price; since that price is also the charge of the consumer above it, shading by the last consumer lowers every charge in the block. Leaving the last eligible consumer unserved as the price setter keeps every price second price, but raises less than the consumer floor in every slack block, serves one fewer consumer, and lets a consumer obtain free service by adding a near-zero bid below itself.

Let `R = sum of a_k`. Then:

- providers are funded from `R`, with total funded shortfall `S <= R`;
- the surplus `R - S` is **burned**;
- each consumer's unused authorization `c_k - a_k` is refunded.

### 3.2 Properties

- **A consumer's own declaration does not set its own charge.** Its charge is set by the next density down.
- **Taking a rank costs the displaced consumer's bid**: outranking a rival means paying the rival's density on one's own gas limit.
- **No consumer pays more than it authorized**: `0 <= a_k <= c_k`.
- **Early service is never free.** Charges depend on the bids and the consumer floor, not on provider funding. When no provider is funded, `A_C = 0` and no consumer is selected; when few are funded, few consumers are selected and rejected rivals set their prices.
- **No party gains from the surplus.** Burning it removes the builder's reason to insert fake consumer bids, the consumers' reason to inflate declarations to recover it, and a provider's reason to exist only to absorb it.
- **Validators can recompute every charge** from the signed declarations, the gas limits, `K_C`, `theta`, the funded provider gas, the base fee and `beta`, by repeating the selection over the eligible transactions in the block.

The rule is the generalized second-price rule of position auctions, applied to a knapsack-constrained selection with a funding obligation attached. Like that rule, it is not truthful: a consumer can gain by bidding below value. Sec. 3.5 measures how much.

### 3.3 Budget feasibility

```text
sum of a_k   =   R   =   S   +   burn,       S = sum over funded providers of g_j * s_j
```

No balance is carried between slots and no external funding enters. Burning is the one destination for the surplus that no participant can game: paid to the builder, it rewards fake bids that raise charges; paid to providers as a rebate, it rewards fake providers that only use gas; returned to consumers, it makes a consumer's price depend on its own bid again. Carrying the surplus into a reserve that funds later provider shortfalls (RN-16) is the alternative that keeps it within the mechanism; self-supply stays unprofitable there, because a provider's net is `g * (p - m) <= 0`.

### 3.4 Why the proportional rule was withdrawn

Versions up to 2.10 charged consumers pro rata to their authorizations, `a_i = c_i * S / C` with `C = sum of c_i`, and refunded `C - S`. That rule is budget-balanced but lets rank be bought cheaply. A consumer's charge rises with `c_i` but never exceeds `S`, which is fixed by providers, not by the consumer. Any consumer that values its rank above `S` gains by inflating its declaration, and when no provider is funded (`S = 0`) every charge is zero whatever is declared. Declarations then rank consumers by the balance they can lock up, not by the value of early execution. The second-price rule removes this: outranking costs the rival's declaration, with no ceiling.

The cost is funding. Since `a_k <= c_k`, `R <= C`, so blocks in which providers need more than `R` fund fewer providers than the proportional rule would. Sec. 3.6 measures it in a simplified model and compares a variant that recovers part of it.

### 3.5 Bidding under the rule

A consumer's own bid does not set its own charge, but it decides its rank and so which rival sits below it. Bidding lower can move a consumer below a rival and lower its charge while keeping it selected. The same holds in the generalized second-price auctions used for search advertising, where equilibria with bids below value are known (Edelman, Ostrovsky and Schwarz 2007; Varian 2007).

We measured the shading in a simplified version of the rule. Consumers have equal gas limits and `K_C` holds five of them. The base fee is fixed within the block, so the consumer floor `beta * b` is a constant; values per unit of gas are uniform on [0, 1] in units where `beta * b = 0.1`. Position value is either flat, where each selected consumer values selection equally, or ranked, where it falls linearly with rank from 1 at the top place to 0.2 at the fifth. Each consumer bids a common fraction of its value, and the fraction is found by iterating best responses. Revenue is the sum of consumer charges per block, the amount available to fund providers.

| consumers | flat: shading | flat: revenue | ranked: shading | ranked: revenue | revenue, bids at value |
|---|---|---|---|---|---|
| 3 (allowance slack) | 0.79 | 0.19 | 0.58 | 0.38 | 0.84 |
| 6 | 0.75 | 0.51 | 0.33 | 1.45 | 2.16 |
| 10 | 0.33 | 2.13 | 0.38 | 1.99 | 3.18 |
| 20 | 0.08 | 3.74 | 0.20 | 3.24 | 4.05 |

- **Shading falls as competition for the allowance rises.** With four consumers per place, revenue is 80 to 92 percent of revenue with bids at value.
- **When the allowance is slack or barely binding, bids fall toward the consumer floor**, and the floor then provides a large share of revenue. Without a floor, revenue in these blocks falls close to zero.
- **Selection and rank are unchanged.** Proportional shading preserves the order of values, so in this model the same consumers are selected in the same order as under truthful bidding; only charges fall.
- **The alternatives compare as follows.** Charging the last consumer its own bid gives similar shading when the allowance binds (0.27 with ten consumers and 0.09 with twenty, flat values), but its revenue in slack blocks falls close to zero. Leaving the last consumer unserved as the price setter raises less revenue than the floor rule at every demand level tested, with bids at value.

The study restricts bids to a common proportional shading and gives consumers equal gas limits. The next step is an equilibrium computation with general bid functions, unequal gas limits and the funding link (sec. 7).

### 3.6 A variant under study: combined second-price and pro-rata charges

Second-price settlement admits providers against `R`, the sum of charges, which is below the sum of authorizations `C`. A variant recovers funding by adding a pro-rata term:

```text
a_k  =  L_k * max( rho_next(k) , beta * b , rho_k * S / C )
providers admitted against C
```

The pro-rata terms alone sum to `S`, so any funded shortfall up to `C` is covered, and the surplus is burned. Each term is at most `rho_k`, so `a_k <= c_k`. The pro-rata term rises with density, so a higher-ranked consumer never pays less per gas than a lower-ranked one. Outranking a rival still costs at least the rival's density, so inflating a declaration buys nothing. When no provider is funded, `S = 0` and the rule is second price. The cost is that when the pro-rata term decides a charge, the consumer's own bid sets that charge, so consumers shade more when providers are plentiful.

We compared the two rules in the model of sec. 3.5 (ranked position values, five places), adding `q` providers per block with unit gas limits and shortfalls uniform on [0.1, 0.6] on the same scale, admitted in ascending shortfall while the pool allows. Funded shortfall per block:

| consumers | providers | shading: second price / combined | funded: second price / combined | funded, bids at value: second price / combined |
|---|---|---|---|---|
| 6 | 3 | 0.31 / 0.38 | 0.94 / 1.01 | 1.02 / 1.05 |
| 6 | 8 | 0.31 / 0.38 | 1.28 / 1.52 | 1.87 / 2.38 |
| 6 | 15 | 0.31 / 0.46 | 1.33 / 1.34 | 1.97 / 2.63 |
| 10 | 8 | 0.34 / 0.43 | 1.84 / 1.83 | 2.57 / 2.72 |
| 10 | 15 | 0.34 / 0.43 | 1.90 / 1.89 | 2.95 / 3.39 |
| 20 | 8 | 0.18 / 0.20 | 2.70 / 2.74 | 2.79 / 2.80 |
| 20 | 15 | 0.18 / 0.20 | 3.06 / 3.19 | 3.79 / 4.02 |

With no providers the two rules coincide, and with few providers they are nearly identical. With many providers and bids at value, the combined rule funds up to 33 percent more. Consumers then shade more under the combined rule, and most of that advantage disappears: at equilibrium it funds between the same and 19 percent more. The combined rule burns much less, because more of the charges go to providers. Second price therefore remains the rule of this note; the combined rule is a variant to revisit if provider funding proves to be the binding constraint.

### 3.7 Provider-linked selection: simulation

We compared a fixed allowance (`A_C = K_C`) with the provider-linked allowance (`A_C = min(K_C, theta * G_P)`, `theta = 1`) in the model of sec. 3.5 and 3.6: unit gas limits, up to five consumer places, ranked position values, a consumer floor of 0.1, and `q` providers with unit gas and shortfalls uniform on [0.1, 0.6]. The consistent pair is found by the trimming procedure of sec. 2.5, and each consumer bids a common fraction of its value found by iterating best responses. Figures are per block.

| consumers | providers | consumers served: fixed / linked | shading: fixed / linked | charge per served consumer: fixed / linked | funded shortfall: fixed / linked |
|---|---|---|---|---|---|
| 10 | 0 | 5.00 / 0 | 0.34 / - | 0.42 / - | 0 / 0 |
| 10 | 1 | 5.00 / 0.99 | 0.34 / 0.00 | 0.42 / 0.82 | 0.35 / 0.34 |
| 10 | 3 | 5.00 / 2.96 | 0.34 / 0.18 | 0.42 / 0.60 | 1.04 / 1.03 |
| 10 | 8 | 5.00 / 4.91 | 0.34 / 0.34 | 0.42 / 0.42 | 1.84 / 1.83 |
| 20 | 1 | 5.00 / 1.00 | 0.18 / 0.00 | 0.66 / 0.90 | 0.35 / 0.35 |
| 20 | 3 | 5.00 / 3.00 | 0.18 / 0.15 | 0.66 / 0.73 | 1.05 / 1.05 |
| 20 | 8 | 5.00 / 5.00 | 0.18 / 0.18 | 0.66 / 0.66 | 2.70 / 2.70 |

- **Without providers no early service is sold;** with a fixed allowance, five places are sold and the charges burned.
- **Thin provider supply makes early service scarce.** With one to three providers, fewer consumers are served, each pays more, and shading falls because more rivals compete for each place. With a single place the rule is a second-price auction and bids equal values.
- **Provider funding is unchanged.** The highest-density consumers remain selected and cover the same shortfall; the funded amount is within 3 percent of the fixed allowance with ten or more consumers, and within 8 percent with six.
- **With ample providers the two rules coincide.**

The study uses unit gas limits and `theta = 1`; unequal gas limits and the choice of `theta` are remaining work (sec. 7).

---

## 4. Metering: which gas the controller should see

### 4.1 The fixed point

The EIP-1559 update is

```text
b_{t+1} = b_t * [ 1 + gamma * (G_t - T) / T ]
```

At any positive fixed point, `G_t = T`.

**Naive metering** feeds all gas to the controller, `G_t = O_t + P_t`, with `O_t` ordinary (neutral and consumer) gas and `P_t` funded provider gas. At the fixed point `O + P = T`: **funded provider gas takes target space that would otherwise go to ordinary transactions.** The base fee rises until ordinary demand contracts by `P`.

With constant-elasticity ordinary demand `D(b)` of elasticity `epsilon` and funded gas `F = phi * T`, the fixed-point base fee rises by

```text
b_1 / b_0  =  (1 - phi)^(-1/epsilon)
```

**Separate metering** feeds only ordinary gas, `G_t = O_t`. At the fixed point `O* = T`, so the ordinary allocation and base fee are those of the baseline, and with reference-preserving admission (sec. 2.4) total utilization is

```text
U*  =  (T + P*) / K   >   T / K
```

Funded provider gas raises utilization above the target without taking target space from ordinary demand. It remains bounded by `P_bar` and by the hard limit `K`.

### 4.2 What separate metering assumes

Excluding funded gas from the controller is safe only if that gas cannot be disguised ordinary demand. Here it is admitted only below the floor, only when funded, only after `E`, and only up to `P_bar`, so an ordinary sender that could pay the base fee gains nothing by imitating a provider except a later position and a dependence on funding. Testing this under strategic senders is remaining work (sec. 7).

The target exists partly to bound node load and leave room for bursts. Higher sustained utilization uses that room. `P_bar` and `K` bound it, and the note does not claim that a higher long-run utilization is safe for Ethereum.

### 4.3 Calibration

Formula (4.1) is very sensitive to `epsilon`, which is the long-run response of ordinary demand to the base fee. The smaller it is, the larger the naive-metering increase, and the stronger the case for separate metering. No estimate of this quantity is used here; the simulations use a synthetic elasticity and should be read for direction, not magnitude.

---

## 5. Incentives

**Self-supply.** A block producer must not profit by inserting a provider it controls. It pays `g * m` as sender and receives `g * p` as builder, so its net is `g * (p - m) <= 0`, because EIP-1559 validity already requires `max_priority_fee <= max_fee`. The protection comes from the sender-paid fee cap and holds for any effective tip the builder selects.

**Buying allowance with own providers.** A consumer or builder can add providers it controls to enlarge `A_C`. Each unit of provider gas costs its sender `m` and draws the shortfall `s` from consumer charges, so the base fee on it is burned in full and only the tip returns to the builder. Enlarging the allowance by `g` therefore costs about `b * g / theta`, burned. Nobody profits, and the cost acts as a second floor on the price of early service.

**Consumer selection.** Candidate-set selection is unconstrained, as under EIP-1559 today. The allowance adds a motive: a builder can favour an affiliate by omitting a higher-density consumer. Settlement stays budget-feasible, so the gain is placement, not extraction.

**Price setters must be in the block.** A skipped or rejected rival sets a price only if it is included in the block as a valid EIP-1559 transaction, so validators can see its density. A candidate left out of the block sets no price; if no eligible transaction follows a selected consumer in processing order, that consumer pays the consumer floor. An included consumer that is not selected executes as an ordinary transaction: it pays the base fee on its gas used, which is burned, and its priority fee, pays no temporal charge, and has its authorization refunded.

A builder can insert a rival of its own just below a selected consumer to raise that consumer's price. To be skipped rather than selected, the fake needs a gas limit larger than the allowance left when its turn comes. It costs the builder the base fee on its gas used, at least `21,000 * b`, burned; its priority fee returns to the builder. It brings the builder nothing directly, because the higher charge goes to provider funding or the burn. The fake pays only if the extra charge funds additional providers whose tips exceed the base fee it burned. In the other direction, a builder can omit a real skipped or rejected rival to lower a consumer's price, for instance for an affiliate. That is a placement favour of the kind described under consumer selection, and the price cannot fall below the consumer floor.

**Participation.** A selected consumer takes part only if the value of its early-region rank covers its charge, and a provider only if funded execution after `E` beats its outside options (raising its fee cap, waiting, or another venue). With both conditions holding, the reference-preserving rule is a weak Pareto improvement over the reference block: neutral senders keep their inclusion and base fee, consumers and providers gain by their own choice, and each funded provider adds burn.

**Enforcement.** The ordering constraints must be checked by validators. If builders could sell position out of band and ignore the constraint, no consumer would pay for it. Builders already sell position privately, through bundles and priority fees, and a privately placed transaction may sit anywhere in `E`, including ahead of selected consumers. What TLA offers that a private sale does not is a guarantee checked by validators, access without a relationship with any builder, and a price set by competition among consumers. Whether consumers value that above a builder's private price is an empirical question (sec. 7).

---

## 6. Simulation

Synthetic simulations of the proportional-rule mechanism, with 20 seeds per mixture, give the directions stated in sec. 4: naive metering raises the base fee and reduces ordinary gas at unchanged total utilization; separate metering with a provider allowance keeps ordinary gas and base fee at baseline while raising total utilization above the target. Consumer bidding under second-price settlement is studied in sec. 3.5 and provider funding under the two settlement rules in sec. 3.6. The metering results under second-price settlement, and their sensitivity to the demand elasticity, are being rerun and will be reported in the next version.

---

## 7. Remaining work

1. **Bidding under second-price settlement.** Extend sec. 3.5 to general bid functions, unequal gas limits and the funding link, and test whether the value of early position rises with the base fee, as the consumer floor `beta * b` assumes.
2. **Funding loss.** How often `R` falls short of the shortfall that the proportional rule would have funded. A reserve carried across slots would recover it and is the subject of RN-16. The combined rule of sec. 3.6 is the within-block alternative; its comparison should be extended to unequal gas limits and realistic provider supply.
3. **The effective provider tip.** When the builder selects `p_i` below the signed maximum, tip revenue and the number of funded providers trade off; characterizing the builder's optimum is the next step.
4. **Imitation of the provider branch** by senders that could pay the base fee, and whether separate metering then under-signals real demand.
5. **Calibration.** The long-run elasticity of ordinary demand, and the share of mainnet demand that would take the provider side.
6. **Parameters.** `chi`, `kappa_C`, `theta`, `P_bar` and `beta` are model parameters, not proposed constants. The self-supply cost `b / theta` of sec. 5 overlaps with the consumer floor `beta * b`; one of the two may prove unnecessary.
7. **Provider-linked selection with unequal gas limits.** Extend sec. 3.7, and check how often the trimming procedure of sec. 2.5 takes more than one round.
8. **Competition with private position sales.** How the price of early-region service compares with what builders charge for top-of-block placement, and which consumers would use each.

---

## 8. Relationship to other notes

RN-12 gives the general two-sided mechanism. RN-16 carries funding and provider offers across adjacent slots, which addresses the funding loss of sec. 3.4. RN-17 moves the unit from the transaction to the stream.

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- Edelman, B., Ostrovsky, M. & Schwarz, M. "Internet Advertising and the Generalized Second-Price Auction." *American Economic Review* 97(1), 2007, 242-259.
- Varian, H. R. "Position Auctions." *International Journal of Industrial Organization* 25(6), 2007, 1163-1178.

---

## Revision note

*Substantive changes only.*

**Version 3.1** (30 September 2026)

- **Links consumer selection to provider supply**: the consumer allowance is `A_C = min(K_C, theta * G_P)`, so no consumer is selected without funded providers (sec. 2.2, 2.5). The early region `E` stays fixed.
- **States validity as a consistency check** on the pair of consumer and provider sets, with all quantities on realized gas (sec. 2.5).
- **Adds a simulation** comparing fixed and provider-linked allowances (sec. 3.7), and the self-supply cost of enlarging the allowance (sec. 5).
- **States why the surplus is burned** and names a cross-slot reserve as the alternative (sec. 3.3), and compares TLA with builders' private sale of position (sec. 5).

**Version 3.0** (29 September 2026)

- **Withdraws proportional consumer settlement** (v2.10 sec. 2.6 and sec. 3). It lets rank be bought at a cost bounded by the funded shortfall and is replaced by second-price charges with the surplus burned (sec. 3). Citations of v2.x settlement should not be relied on.
- **Replaces band ordering by lump-sum `TLA`** (v2.10 sec. 2.6, `band_i = floor(TLA_i / tla_tick)`) with selection by authorization density under a consumer allowance `K_C`, completion within an early region `E`, and density rank among selected consumers (sec. 2.2).
- **Negative `TLA` magnitude no longer commits to a later band;** only its sign is used, and providers start after `E` (sec. 2.1, 2.3).
- **Adds reference-preserving provider admission and a provider-gas allowance** (sec. 2.4).
- **Adds separate metering** of funded provider gas and the fixed-point analysis (sec. 4).
- **Adds a consumer floor `beta * b`** and a numerical study of bidding under the second-price rule (sec. 3.1, 3.5).
- **Records a combined second-price and pro-rata rule** as a variant under study, with a funding comparison (sec. 3.6).
- **Removes the v2.x simulation tables**, which measured the withdrawn rules; updated results will follow (sec. 6).

---

## Licence

Copyright (c) 2026 Duanyang (Dan) Guo / TLM Research. All rights reserved.
