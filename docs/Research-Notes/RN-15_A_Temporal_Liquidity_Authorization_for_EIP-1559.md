---
id: RN-15
title: "A Temporal Liquidity Authorization for EIP-1559"
subtitle: "Early-region service, below-floor providers, pay-as-bid settlement, a provider fee-cap floor and tip cap, and separate metering"
version: "3.4"
program: "Temporal Liquidity Market (TLM)"
date: "2026-10-05"
license: "All rights reserved"
---

# RN-15 v3.4

# A Temporal Liquidity Authorization for EIP-1559

## Early-region service, below-floor providers, pay-as-bid settlement, a provider fee-cap floor and tip cap, and separate metering

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-15**  
**Version:** 3.4 (supersedes v3.1)  
**Scope:** One slot, one block. No state carried between slots.  
**Date:** 5 October 2026

---

## Abstract

Under EIP-1559 the base fee is a floor, and a fee bid buys no enforceable position in the block. This note adds one signed field, a Temporal Liquidity Authorization (`TLA`). A consumer signs a positive `TLA`, a lump sum in wei, and, if selected, is guaranteed to complete within an early region of the block, ranked among selected consumers by `TLA` per unit of realized gas. A provider signs a negative `TLA`, sets its fee cap below the base fee, and accepts execution after that region; it is admitted when consumer payments cover its shortfall.

Selected consumers use **pay-as-bid settlement**: each pays its signed positive `TLA` in full when selected, and an unselected consumer pays no temporal charge. Provider shortfalls are funded from those payments and the surplus is burned. A provider's fee cap must be at least a fixed share of the base fee, and the tip a builder may take from it is at most a fixed share of that fee cap. Part of what a provider pays therefore always goes to the base fee. Under pay-as-bid no inserted consumer bid can raise another consumer's charge, and a builder that inserts its own provider loses on it. These are direct self-supply properties. The note does not claim MMIC, the property of Roughgarden (2024) that a builder never gains by inserting transactions of its own.

**Protected service is sold only against provider supply**: the consumer allowance is proportional to funded provider gas. A block without funded providers selects no consumers, and thin provider supply makes early service scarce. Funded provider gas is excluded from the base-fee controller's input and bounded by an allowance: counting it in the controller raises the base fee and displaces ordinary demand; excluding it preserves the ordinary allocation and base fee while allowing higher total utilization.

---

## 1. What changes

Relative to EIP-1559, validity, ordering and metering change.

1. **Validity.** A transaction with `max_fee < base_fee` can be included when it opts into the provider branch and the block's consumer payments cover its shortfall. In that branch the fee cap is at least a share `nu` of the base fee, and the effective tip is at most a share `1 - eta` of the fee cap.
2. **Ordering.** Validators check two positional constraints: selected consumers complete within an early region, ranked by authorization density; funded providers start after it. All other ordering stays with the builder.
3. **Metering.** The base-fee controller measures ordinary gas only. Funded provider gas is counted against the block gas limit but not against the target, and is capped separately.

The base-fee burn, the base-fee update rule, and the treatment of transactions that do not use the field are unchanged. Any consumer payment not allocated to funded provider shortfalls is burned in this one-slot design (sec. 3.1).

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

Let `L_i` be consumer `i`'s signed gas limit and `g_i` its realized charged gas in the final executed block, with `0 < g_i <= L_i`. Its **authorization density** is

```text
rho_i = c_i / g_i
```

Two quantities bound selection. A protocol parameter `K_C = kappa_C * K`, with `K_C <= E`, is the most consumer gas that can ever be selected. The **consumer allowance** of the block is

```text
A_C  =  min( K_C , theta * G_P )
```

where `G_P` is the realized gas of the funded providers (sec. 2.6) and `theta` is a protocol parameter. Candidates must first be valid EIP-1559 transactions (`max_fee >= base_fee`) included in the block. They are processed in decreasing density, ties broken by transaction hash, and each is added to the selected set `C*` if its realized gas fits the remaining `A_C`; otherwise it is skipped. A consumer that is not selected stays in the block as an ordinary transaction.

A selected consumer receives:

- **completion within the early region** `E = chi * K`, measured in cumulative charged gas: its execution ends before the block's cumulative gas crosses `E`;
- **rank among selected consumers by density**: removing every transaction outside `C*` from the block leaves them in decreasing `rho_i`.

`A_C` decides how many consumers are served; `E` decides where they must finish. `E` is fixed, so what a consumer buys is the same in every block: completion before the block's cumulative gas crosses `E`, whatever the number of consumers selected. Neutral transactions may appear anywhere, including before or between selected consumers in the early region, at the builder's discretion.

Density and payment use realized charged gas. The signed gas limit remains an EIP-1559 validity and liability bound, but does not determine TLM rank or payment. The allowance keeps a large number of nominal authorizations from all qualifying.

### 2.3 Providers: admission below the floor

A provider signs `TLA_i < 0`, sets `max_fee = m_i` with `nu * b <= m_i < b`, and must begin after `E`. The builder selects an effective tip `p_i` within the tip cap of sec. 2.4, and the provider's per-gas **shortfall** is

```text
s_i = b + p_i - m_i.
```

For realized gas `g_i`, the provider pays `g_i * m_i`, consumer payments cover `g_i * s_i`, the protocol burns `g_i * b`, and the builder receives `g_i * p_i`. The base fee is fully burned; what changes is who pays it.

### 2.4 The fee-cap floor and the tip cap

**The fee-cap floor.** A provider is eligible only if

```text
nu * b  <=  m_i  <  b,        0 < nu < 1,
```

where `nu` is a dimensionless protocol parameter. The lower bound is checked against the base fee of the including block, like the consumer floor. It decides eligibility and not what the provider pays, which is never more than `g_i * m_i`.

**The tip cap.** The provider branch retains the signed relation `max_priority_fee <= max_fee` and adds a cap on the effective tip that the builder selects:

```text
0  <=  p_i  <=  min( max_priority_fee_i , (1 - eta) * m_i ),        0 < eta < 1,
```

where `eta` is a dimensionless protocol parameter. The cap is a clamp, as the ordinary EIP-1559 effective tip is. A provider that signs a larger tip cap is still eligible, and the builder takes less than it authorized. It follows that

```text
m_i - p_i  >=  eta * m_i  >=  eta * nu * b                      the provider's own payment toward the base fee, per gas
s_i  =  b + p_i - m_i  <=  b - eta * m_i  <=  (1 - eta * nu) * b      the shortfall is bounded
```

- **At least a share `eta` of what a provider pays goes to the base fee,** and the provider itself pays at least `eta * nu` of the base fee.
- **The shortfall is at most `b - eta * m_i`.**
- **The tip cap is checked on the published effective tip and two signed fields.** It does not depend on the base fee of the including block.
- **A builder that inserts its own provider loses at least `eta * nu * b` per gas** (sec. 3.2).

**The value of `eta`.** `eta` is a bound and is not fitted to traffic. It leaves the builder a tip of up to `1 - eta` of a provider's fee cap, and it makes a provider pay at least `eta * nu` of the base fee itself. At `eta = 0` the only limit is the EIP-1559 relation `max_priority_fee <= max_fee`, as in v3.1. A provider can then pay its whole fee cap as tip, the pool pays the whole base fee, and a builder's own provider costs the builder nothing. A small positive `eta` closes that case and stays close to the tip a builder may take today. The simulations use `eta = 1/4` with `nu = 1/2`. The builder may then take up to three quarters of a provider's fee cap, and the pool pays at most seven eighths of the base fee for a provider. A builder's own provider costs it at least one eighth of the base fee per gas.

Two other forms were considered and set aside. One is a co-burn: an extra payment of `eta * b` per gas by the provider, burned and not reimbursed. It leaves the shortfall unchanged and burns the extra payment, and its size depends on the base fee at inclusion, so a provider would owe an amount it did not sign. The other is a cap on the signed field, `max_priority_fee <= (1 - eta) * m_i`. That gives the same bounds and makes a provider with a generous signed tip cap ineligible for no gain.

### 2.5 Reference-preserving admission

Provider admission must not remove ordinary transactions. The builder proceeds in two stages.

1. **Reference block.** Build the block from neutral transactions and consumers as it would be built without providers. Call its realized gas `H^0`.
2. **Providers.** Add providers without removing any transaction in the reference block, subject to

```text
sum over funded providers of  g_j * s_j   <=   R            (funding, sec. 3)
sum over funded providers of  g_j         <=   A = min( P_bar , K - H^0 )
```

where `P_bar` is the provider-gas allowance and `R` the total consumer charge of sec. 3. Both constraints are evaluated on realized gas. Which eligible providers are funded is the builder's choice; a reference implementation scans them in increasing shortfall. A provider below the base fee is in a block only if it is funded, so the block holds no record of candidates that were passed over. A priority rule among providers therefore cannot be checked without a protocol-visible list of candidates (sec. 7).

**Every transaction in the reference block is retained, and providers are added only in residual capacity.** The block is physically feasible, and its realized gas rises by the funded provider gas.

### 2.6 Linking consumer service to provider supply

Consumer service and provider funding determine each other through two quantities: the consumer allowance `A_C` depends on the funded provider gas `G_P`, and which providers can be funded depends on the consumer charges `R`. A provider's shortfall `s_j = b + p_j - m_j` depends only on its own fields.

Every consumer candidate is in the reference block whether or not it is selected, so the set of transactions in the block does not depend on selection. Their order can. Selected consumers must complete within `E` in density order, and a transaction's realized gas can depend on what runs before it. Density, eligibility and the allowance use the realized gas of the block as proposed.

Validators do not search for the pair of sets, the selected consumers `C*` and the funded providers. They check that the pair in the block is consistent:

1. the selected consumers are those that the rule of sec. 2.2 selects from the eligible candidates in the block, in decreasing density with skipping, under `A_C = min(K_C, theta * G_P)`;
2. each selected consumer is charged its authorization, and no other consumer is charged (sec. 3.1);
3. the funded providers meet the fee-cap floor and the tip cap (sec. 2.4) and satisfy `sum of g_j * s_j <= R` and `sum of g_j <= A` (sec. 2.5), with `G_P = sum of g_j`;
4. selected consumers complete within `E` in density order, and funded providers start after `E`.

A builder can find a consistent pair with a monotone procedure. It starts from all eligible consumers and providers and alternates: select consumers under the current allowance, compute `R`, fund providers against `R`, recompute `A_C`, and repeat, never restoring a candidate it has removed. With realized gas held fixed the allowance can only fall, so the procedure ends. The empty pair, with no consumer selected and no provider funded, always passes the checks, so a builder can always produce a valid block. Realized gas can change when the block is reordered, and extending the procedure to that case is remaining work (sec. 7).

All quantities are **realized**. The builder has simulated the block, and validators check it after execution, as they check gas used. A provider that signs a large gas limit but uses little gas adds only what it uses to `G_P` and to the funding check, so it can neither enlarge the consumer allowance nor tie up the pool. The same holds for a consumer: it takes allowance only by the gas it uses.

`theta` sets how much consumer gas each unit of funded provider gas supports. With `theta = 1`, one unit of early-region consumer gas requires one unit of provider gas that executes after `E`.

---

## 3. Settlement: pay-as-bid charges

### 3.1 The rule

A consumer candidate is eligible only if its signed authorization meets the consumer floor:

```text
c_i >= beta * b * g_i
```

where `b` is the base fee and `beta > 0` is a dimensionless protocol parameter. After the consistent consumer and provider sets are determined under sec. 2.6, every selected consumer pays its own signed authorization:

```text
a_i = c_i,       i in C*
R   = sum over selected consumers of a_i
```

A selected consumer therefore pays its bid in full; an unselected consumer pays no temporal charge and continues as an ordinary EIP-1559 transaction if included. The authorization is a conditional commitment: it is charged only if the consumer is selected into a provider-backed crossing. There is no refund of unused positive TLA for a selected consumer. A consumer therefore knows its temporal charge when it signs: `c_i` if it is selected, and nothing otherwise. A selected consumer whose transaction reverts has still completed within `E`, and pays.

Providers are funded from `R`, with total funded shortfall

```text
S = sum over funded providers of g_j * s_j <= R.
```

The surplus

```text
R - S
```

is burned in this one-slot design. Thus every consumer payment is either used to cover a provider shortfall or burned; no balance is carried across slots. RN-16 considers carrying this surplus in a Temporal Liquidity Reserve.

### 3.2 What pay-as-bid does and does not protect

The builder earns the tips of the providers it funds, and consumer payments decide how many are funded. A rule under which one bid can set another's charge therefore gives the builder a reason to insert bids of its own.

**No bid sets another consumer's charge.** The second-price rule of v3.1 let the next bid in the order, selected or skipped, set a consumer's charge. A builder could place a bid of its own just below a selected consumer and raise that consumer's payment. Its cost was the base fee on its own small transaction, and its gain was the tips of the extra providers that the higher charge funded. Under pay-as-bid a consumer's charge is its own authorization, and no inserted bid changes it.

**An inserted provider loses.** By the tip cap, `p_j <= (1 - eta) * m_j`, and by the fee-cap floor, `m_j >= nu * b`. A builder that controls the provider's sender pays `g_j * m_j` and receives `g_j * p_j`:

```text
g_j * (p_j - m_j)  <=  - eta * g_j * m_j  <=  - eta * nu * b * g_j  <  0.
```

**An inserted consumer funded from its own payment loses.** A provider's tip is below its shortfall, since `s_j - p_j = b - m_j > 0`. Of each unit a builder pays into the pool through a consumer bid, less than one unit can return as tips, and the bid also burns the base fee on its gas. The bid must meet the consumer floor and fit the allowance like any other. When the allowance is full it displaces a consumer, whose payment then leaves the pool.

**What remains: residual funding.** Suppose the selected consumers' payments leave an amount `R_0` from which no remaining provider can be funded, and a provider `j` needs `Delta = g_j * s_j - R_0 > 0` more. A builder can add a consumer bid of about `Delta`, fund that provider, and collect its tip. With `g_F` the gas of the inserted transaction, its net is at most

```text
g_j * p_j  -  Delta  -  b * g_F.
```

This is positive only when `R_0` is close to the provider's cost. It is bounded by one provider's tip, which is at most `(1 - eta) * g_j * m_j`. If the inserted consumer fits without displacing a selected consumer, every other selected consumer keeps its charge and one more provider is funded; the amount `R_0`, which would have been burned, goes toward that provider's shortfall instead. If it displaces one, that consumer is no longer charged or served, and the pool changes with it.

When the allowance link binds, funding one more provider also enlarges the consumer allowance, and the consumers admitted as a result pay part of that provider's cost. Sec. 6 finds that the gain is large in that case when tips are close to fee caps, and that only a tight tip cap limits it.

The protocol cannot tell whether the marginal consumer is independent or affiliated with the builder. The bid meets the same conditions and pays the same charge either way. The rule is still not MMIC (myopic miner incentive compatibility) in the sense of Roughgarden (2024), where the miner is the block producer, here the builder. That property asks that a builder never gain by inserting transactions of its own, whoever else is affected. This note claims the statements above and not that property.

### 3.3 Budget feasibility

```text
sum over selected consumers of a_i  =  R  =  S + burn,
S = sum over funded providers of g_j * s_j.
```

No external funding enters and no balance is carried between slots. If no provider is funded, `G_P = 0`, hence `A_C = 0`; no consumer is selected and no temporal payment is charged.

### 3.4 Bidding under pay-as-bid

The rule is not truthful. A consumer gains by bidding below its value, as far as it can and still be selected, and its best bid depends on bids it does not see. Where bids are visible before the block, rivals can also outbid one another in steps and then drop back, as in early first-price auctions for search advertising (Edelman and Ostrovsky 2007). Pay-as-bid has the exposure of a first-price rule. EIP-1559's priority fee is also paid as bid, but it buys no enforceable position, and under EIP-1559 the posted base fee does the rationing when blocks are not full, which is what keeps bidding simple there (Roughgarden 2024). The temporal charge has no posted price beyond the consumer floor.

A bid above value does not pay. The withdrawn pro-rata rule charged a consumer a share of the funded shortfall, so a high declaration bought rank at a price set by others. Here a consumer that declares more pays more, one for one. Competition under the provider-linked allowance decides which consumers receive protected service, and the consumer floor keeps service from being nearly free when the allowance is slack.

An equilibrium of pay-as-bid declarations is remaining work: general bid functions, unequal realized gas, bid splitting, rebidding, and the interaction between consumer competition and provider supply (sec. 7).

### 3.5 Why the second-price rule was replaced

v3.0 and v3.1 charged each selected consumer the next bid in the order, so that a consumer's own bid would never set its own charge. What followed changed the choice.

- **It was not truthful in practice.** A consumer's bid still sets its rank, and so which bid lies below it. In the traffic model of sec. 6, 94 percent of selected consumers gain by bidding lower under the next-bid rule, by 30 percent of their value on average.
- **It funds no more providers once consumers respond.** When every selected consumer pays the lowest charge at which it is still selected, the two rules fund the same provider gas (sec. 6).
- **It lets one bid set another's charge** (sec. 3.2). Second-price rules are the standard case of a builder gaining from inserted bids (Roughgarden 2024). A first-price rule does not have that channel.

The cost of the change is the one every first-price rule carries: a bid that is too high is paid in full.

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

**Separate metering** feeds only ordinary gas, `G_t = O_t`. At the fixed point `O* = T`, so the ordinary allocation and base fee are those of the baseline, and with reference-preserving admission (sec. 2.5) total utilization is

```text
U*  =  (T + P*) / K   >   T / K
```

Funded provider gas raises utilization above the target without taking target space from ordinary demand. It remains bounded by `P_bar` and by the hard limit `K`.

### 4.2 What separate metering assumes

Excluding funded gas from the controller is safe only if that gas cannot be disguised ordinary demand. Here it is admitted only below the floor, only when funded, only after `E`, and only up to `P_bar`, so an ordinary sender that could pay the base fee gains nothing by imitating a provider except a later position and a dependence on funding. Testing this under strategic senders is remaining work (sec. 7).

The target exists partly to bound node load and leave room for bursts. Higher sustained utilization uses that room. `P_bar` and `K` bound it, and the note does not claim that a higher long-run utilization is safe for Ethereum.

### 4.3 Calibration

Formula (4.1) is sensitive to `epsilon`, which is the long-run response of ordinary demand to the base fee. The smaller it is, the larger the naive-metering increase, and the stronger the case for separate metering. No estimate of this quantity is used here; the simulations use a synthetic elasticity and indicate direction only.

---

## 5. Incentives and scope of the safety claim

**Scope.** Pay-as-bid prevents a builder-inserted consumer from increasing another consumer's charge. The fee-cap floor and the tip cap make a builder-controlled provider loss-making in direct protocol-fee terms. These are direct self-supply properties. They do not establish MMIC against the builder's choice of candidates, affiliated consumers, private ordering value, or the use of residual funding.

**A builder's own provider.** A builder that controls a funded provider's sender pays `g_i * m_i` and receives `g_i * p_i`. By the tip cap and the fee-cap floor its payoff is at most `- eta * nu * b * g_i`, for every effective tip the builder may select.

**A builder's own provider, used to enlarge the consumer allowance.** Each unit of such provider gas costs the builder at least `eta * nu * b`, and it draws its shortfall from consumer payments that would otherwise fund other providers. This does not rule out a builder accepting that cost for private ordering value or for an affiliated consumer's placement.

**A builder's own consumer bid.** By sec. 3.2 it changes no other consumer's charge, and it loses when funded from its own payment. It can gain only by completing the funding of one provider from payments already in the pool or, when the allowance link binds, from consumers admitted as the allowance grows. The gain is bounded by that provider's tip, and no other participant pays more than its own bid. There is no consensus-visible test for affiliation, and the note does not claim MMIC.

**Which providers are funded.** Validators check each funded provider's eligibility, fee-cap floor, tip cap, shortfall, settlement and placement, and the aggregate funding and provider-gas bounds. Which eligible providers are funded is the builder's choice (sec. 2.5).

**Consumer selection.** Candidate-set selection is unconstrained, as under EIP-1559 today. A builder can favour an affiliate by omitting a higher-density consumer. The mechanism makes the resulting allocation and settlement checkable, but does not remove the builder's general ordering discretion outside the stated constraints.

**Participation.** A consumer participates only if early-region service is worth its charge to it. A provider participates only if funded execution after `E` beats its outside options: raising its fee cap, waiting, or another venue.

**Enforcement.** Validators execute the block and recompute realized gas, consumer selection, charges, provider funding, the fee-cap floor, the tip cap, and the early-region ordering constraints. If a check fails, the block is invalid.

---

## 6. Simulation

**The traffic model.** Blocks have a gas limit of 60 million and a target of 30 million. Offered gas is 7/15 neutral, 1/5 consumer and 1/3 provider. `K_C = 0.10 K`, `E = 0.20 K`, `P_bar = 0.20 K`, `beta = 0.10` and `theta = 1`. Fee caps follow a capped Pareto distribution. A consumer's authorization is its realized gas times a uniform factor on [4, 12], against a base fee near 28.5. Provider fee caps are uniform on [17, 28] and their tips on [0.25, 2]. Providers are funded cheapest shortfall first. `eta = 1/4` and `nu = 1/2`. Both are bounds and are not fitted to this traffic. Neither binds here: the model's tips are at most 12 percent of fee caps, and its fee caps are above half the base fee. The main comparison therefore does not test the two provider rules; the stress case below does. There are twenty seeds of 400 blocks each after warm-up, and the comparisons below use every fourth block. The model is synthetic and uncalibrated. Declarations are drawn; consumers do not choose them.

**Pay-as-bid against the next-bid rule of v3.1.** Both use realized gas and separate metering.

| per block | next bid | pay-as-bid |
|---|---|---|
| consumers selected | 16.5 | 16.5 |
| funded provider gas, declarations as drawn | 10.88M | 11.05M |
| funded provider gas, every selected consumer at its lowest charge | 8.97M | 8.97M |
| consumer payments burned, declarations as drawn | 5.8% | 6.9% |
| selected consumers that gain by bidding lower | 94% | all above the cut-off |
| blocks in which an inserted consumer bid pays the builder | 0.35% (a partial search) | none in 2,000 |

- **The two rules fund the same providers once consumers respond.** A consumer's lowest charge is the lowest payment at which it is still selected when the others keep their declarations. At those charges both rules fund 8.97M of provider gas.
- **Total utilization is about 68 percent at the drawn declarations and 65 percent at the lowest charges,** against 50 percent without the mechanism. Ordinary gas and the base fee are the same in every case. The first figure depends on how consumers bid, which the model does not determine.
- **Inserted consumer bids.** Under pay-as-bid the test lets the builder fund any unfunded provider and insert the cheapest consumer bid that completes its funding. A gain is counted net of that bid and of the base fee it burns. No insertion gained in the 2,000 sampled blocks, nor in 2,000 blocks of each of three other settings: a provider allowance of `0.30 K`, and consumer shares of 10 and 33 percent. This reports the sample. The residual case of sec. 3.2 needs unspent payments close to one provider's cost, which did not occur. Under the next-bid rule a search over bids placed just under each selected consumer, which is not exhaustive, found a gain in 0.35 percent of blocks.

**The provider rules under stress.** With tips ten times larger and no tip cap, tips are close to fee caps and the pool pays nearly the whole base fee for a provider. The builder then gains from an inserted consumer bid in 81 percent of blocks, by 3.2 percent of its revenue on average. The gain comes through the allowance link: funding one more provider enlarges the consumer allowance, and the consumers then admitted pay part of the provider's cost. How much of this the cap removes depends on `eta`. At `eta = 1/4`, the value used here, the figures are unchanged. At 0.5 they are 80 percent of blocks and 3.1 percent of revenue, at 0.65 they are 64 percent and 1.7 percent, and at 0.8 they are 3.8 percent and 0.02 percent. With tips five times larger and no cap the figures are 18.5 percent of blocks and 0.10 percent of revenue. A cap tight enough to remove this case takes most of the tip from the builder. `eta = 1/4` is set for the bounds of sec. 2.4 and does not address it. The case needs provider tips near fee caps, which the model's traffic does not have. What tips competition for funding would produce is remaining work.

**Metering.** Simulations of earlier settlement rules gave the directions of sec. 4. Naive metering raises the base fee and reduces ordinary gas at unchanged total utilization. Separate metering with a provider allowance keeps ordinary gas and the base fee at baseline and raises total utilization above the target.

Not modelled: declarations chosen by consumers, rebidding, realized gas that depends on order, and affiliation between a builder and a consumer or provider.

---

## 7. Remaining work

1. **Strategic pay-as-bid declarations.** Bid shading, bid splitting, rebidding and unequal realized gas under provider-linked selection.
2. **Funding and burn incidence.** How often pay-as-bid revenue exceeds provider shortfalls, and the one-slot burn against the Temporal Liquidity Reserve of RN-16.
3. **The effective provider tip, the tip cap and the fee-cap floor.** When the builder selects `p_i` below the cap, tip revenue and the number of funded providers trade off. The next step is the builder's optimum and the choice of `eta` and `nu`.
4. **Inserted bids, affiliation and collusion.** A protocol-visible list of provider candidates, which a priority rule among providers would need (sec. 2.5). Agreements between a builder and consumers or providers outside the protocol, for which the burned surplus is a motive, and deviations that use several transactions.
5. **Calibration and parameters.** The elasticity of ordinary demand, and `chi`, `kappa_C`, `theta`, `P_bar`, `beta`, `eta` and `nu`, which are model parameters.
6. **The consistent pair.** The monotone procedure under unequal gas and realistic transaction mixes, and its extension to realized gas that depends on order.

---

## 8. Relationship to other notes

RN-12 gives the general two-sided mechanism. RN-16 carries temporal-liquidity funding across adjacent slots through a reserve, rather than burning the one-slot surplus of sec. 3. RN-17 moves the unit from the transaction to the stream.

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- Edelman, B. & Ostrovsky, M. "Strategic Bidder Behavior in Sponsored Search Auctions." *Decision Support Systems* 43(1), 2007.
- Roughgarden, T. "Transaction Fee Mechanism Design." *Journal of the ACM*, 2024. arXiv 2106.01340.

---

## Revision note

*Substantive changes only.*

**Version 3.4** (5 October 2026)

- **Pay-as-bid settlement** (sec. 3). A selected consumer pays its signed positive `TLA`, an unselected consumer pays no temporal charge, and the one-slot surplus is burned. No bid sets another consumer's charge. This replaces the second-price settlement of v3.0 and v3.1 (sec. 3.5).
- **Gas used on the consumer side** (sec. 2.2). Consumer density, eligibility, allowance and rank use realized gas. Gas limits remain EIP-1559 validity and liability bounds.
- **A provider fee-cap floor and a tip cap** (sec. 2.4): `nu * b <= m_i < b` and `p_i <= min(max_priority_fee_i, (1 - eta) * m_i)`. A builder's own provider loses at least `eta * nu * b` per gas.
- **The scope of the incentive claim** (sec. 3.2, 5): what holds for inserted providers and consumer bids, the residual-funding case with its bound, and that MMIC is not claimed.

**Versions 3.0 and 3.1** (29 and 30 September 2026)

These versions withdrew the proportional consumer settlement and the band ordering of v2.x. They introduced what v3.4 keeps. For consumers: selection by authorization density under a consumer allowance, a consumer floor, and completion within an early region `E`. For providers: a start after `E`, reference-preserving admission with a provider-gas allowance, separate metering, and the link between the consumer allowance and funded provider gas. Their second-price settlement is replaced in v3.4. The settlement rules of v2.x, v3.0 and v3.1 should not be relied on.

Earlier versions are in the repository history.

---

## Licence

Copyright (c) 2026 Duanyang (Dan) Guo / TLM Research. All rights reserved.
