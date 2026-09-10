---
id: RN-16
title: "A Two-Leg Temporal Liquidity Reserve for EIP-1559"
subtitle: "Carrying temporal-liquidity funding across slots, and naming the supply it must meet"
version: "1.0"
status: "Working draft - mechanism specified, controller and simulation not yet run"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-09"
license: "CC-BY-4.0"
---

# RN-16 v1.0

# A Two-Leg Temporal Liquidity Reserve for EIP-1559

## Carrying temporal-liquidity funding across slots, and naming the supply it must meet

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-16**  
**Version:** 1.0  
**Status:** Working draft. The mechanism is specified; the controller and the simulation program in sec. 10 have not been run.  
**Date:** 9 September 2026

---

## Abstract

RN-15 clears a Temporal Liquidity Authorization within one block. Positive TLA is a maximum monetary authorization in wei. Negative TLA opts a below-base-fee transaction into provider treatment and commits it to a later execution band. Consumers fund provider shortfalls, unused consumer authorization is refunded, and the block ends in exact financial balance.

This note asks what changes when the money is allowed to persist past the block. It adds **one** new object, a **Temporal Liquidity Funding Leg** carrying unspent consumer money as protocol state, and gives a name to one that already exists, the **Temporal Liquidity Supply Leg**, which in the baseline is nothing more than valid negative-TLA provider transactions sitting in ordinary transaction pools.

The asymmetry between them is the finding. Funding is money in wei, fungible across slots, and it can be held in consensus state. Supply is a set of pending transactions held by builders and nodes, is not consensus state, and need not be the same set for two builders. There is no meaningful signed total of the two. They meet only through allocation and settlement.

The sharpest limit is that the value of carrying funding depends on a quantity nobody has measured: how much consumer authorization RN-15 actually leaves unmatched per block. Section 10 makes that measurement Stage 0, because one of its two possible answers makes the rest of the programme unnecessary.

---

## 1. Scope

This note assumes EIP-1559 execution fees and base-fee burn; proposer-builder separation or an ePBS-like block market; RN-15's asymmetric TLA semantics; transaction-level Temporal Execution Profiles; several adjacent slots without forward reservation of named slots; and no stream-level TSP aggregation.

It changes RN-15 in two ways. Unspent positive-TLA funding may remain available after the block. And unfunded negative-TLA providers may remain candidates in later slots while their transactions remain pending, visible to a builder, and valid.

Nothing here promises execution in a specific future slot. A retained provider offer may remain eligible for later scheduling; it has no protocol-guaranteed persistence, queue position, or claim on future capacity. Stream-level declarations, named future slots and a term structure belong to RN-17.

---

## 2. One new leg, and one that already exists

Positive and negative TLA have different semantics, and the two legs they generate are not parallel constructs. Saying so plainly is more useful than the symmetry the name suggests.

### 2.1 The Funding Leg is new protocol state

For consumer `i`, `c_i = max(TLA_i, 0)` is a maximum monetary authorization in wei. Let `F_t` be funding carried into slot `t`.

**The quantity that enters the leg is the amount charged, not the amount authorized.** Under RN-15 a consumer is charged pro rata to realized provider settlement and the remainder is refunded, so authorized and charged differ by exactly the amount this note wants to carry. Writing `A_t` for the total charged to consumers in slot `t`, `S_t` for provider subsidies settled, and `W_t` for authorized withdrawals, expiries or refunds:

```text
available before settlement    F_t^avail = F_t + A_t

carry rule                     F_{t+1}  = F_t + A_t - S_t - W_t

solvency                       0 <= S_t + W_t <= F_t + A_t
```

How much of each consumer's authorization becomes `A_t` rather than being refunded is exactly the ownership question in sec. 8, and the identity above is stated in charged terms so that the choice cannot enter through the accounting by accident.

This leg is money. It may be added across slots.

### 2.2 The Supply Leg is a name for something clients already do

For provider `j`, negative TLA is not negative money. It supplies a later-position commitment and opts a below-base-fee transaction into conditional funding.

For builder or node `B`, its local Supply Leg is the set of pending provider offers it can observe and considers valid in slot `t`, containing transaction records rather than a scalar balance. Each record carries at least `(L_j, max_fee_j, max_priority_fee_j, TLA_j, TEP_j)`. Given base fee `b_t` and a builder-selected tip `p_{j,t}`, its current shortfall and reservation are recomputed each slot:

```text
s_j,t = b_t + p_j,t - max_fee_j
R_j,t = L_j * s_j,t
```

The set evolves by retention, revalidation, and removal of executed, expired, replaced, cancelled, invalidated or evicted offers.

**None of that is new machinery.** Retention, revalidation against the current base fee, eviction and same-nonce replacement are what every client already does with every pending transaction. A sender amends or withdraws an offer by broadcasting a valid same-nonce replacement, which also replaces the signed TLA declaration; propagation and retention are client policy, not consensus guarantees.

So the baseline adds nothing structural on the supply side. What it adds is a name, so that the thing carried funding has to meet can be reasoned about. **RN-16 introduces one new object and names one existing one.** A protocol-registered Supply Leg would give common persistence and would require new registration, cancellation, storage and anti-spam rules; it is outside the baseline, and whether the mechanism works without it is sec. 12's first question.

Here *supply* means the supply of temporal liquidity, a willingness to accept later treatment. It does not mean physical execution capacity. Every transaction in the Supply Leg still consumes gas when admitted.

### 2.3 The state boundary

```text
TLR_t^B         = ( F_t , P_t^B )      the economic mechanism
TLR_t^protocol  = F_t                  what is actually in consensus state
```

`P_t^B` is builder- or node-local transaction-pool state and may differ between builders.

| Leg | What enters | Unit | Consensus state | What leaves |
|---|---|---|---|---|
| Funding | consumer amounts charged | wei | yes | provider subsidy, withdrawal, expiry |
| Supply | locally visible valid negative-TLA offers | pending transactions with gas and TEP | no | execution, replacement, cancellation, expiry, invalidation, eviction |

There is no meaningful signed total `F_t - P_t^B`. The legs meet only through allocation and settlement.

---

## 3. Slot transition

At the start of slot `t` the builder observes the base fee `b_t`, the funding balance `F_t`, its local provider set, new TLA transactions, and the physical gas target `T`, operating cap `H` and hard limit `L`. A minimal transition:

1. construct the ordinary and positive-TLA candidate set;
2. add amounts charged to consumers to `F_t^avail`;
3. merge new negative-TLA providers into the local supply set;
4. recompute each provider's shortfall and gas-limit reservation at `b_t`;
5. select a provider subset subject to funding and physical capacity;
6. execute, reserve against gas limit, settle against realized gas;
7. carry unspent funding in protocol state, while builders or nodes may retain and revalidate still-pending offers for `t+1`;
8. update the base fee under the selected experimental rule.

The block remains verifiable from funding pre-state, included transactions, execution results and the deterministic settlement rule. Candidate offers omitted from the block are not globally visible and do not become protocol state, so ePBS leaves a builder-observability problem this note does not solve.

---

## 4. Congestion control

### 4.1 The gas-only mismatch

EIP-1559 observes realized gas `G_t = G_t^O + G_t^P`, where `G_t^O` is ordinary and consumer gas and `G_t^P` is funded-provider gas. It does not observe that provider gas was admitted through a separate funding condition.

In RN-15, no current consumer funding means no provider inclusion. In RN-16, carried funding can admit a provider when the current slot has no new consumer. Provider admission is still bounded by a finite funding stock, but the stock can sustain gas across several slots, so RN-16 must control both reserve drawdown and physical provider gas explicitly.

### 4.2 A bounded provider region

With `T <= H < L`, where `H` is the maximum operating level available to funded providers, require `G_t^O + G_t^P <= H`, leaving `L - H` as physical headroom. This makes use of the elasticity region an explicit experiment rather than an accidental consequence of funding.

Settlement must satisfy `S_t <= F_t + A_t`, and a release limit `S_t <= q(F_t)` can prevent one slot from draining the leg.

### 4.3 Accumulation must also be bounded

A drain limit without a growth limit is only half a constraint. If consumers persistently authorize and are charged more than providers draw, `F_t` grows without limit and the protocol accumulates ETH.

Under sustained one-sided demand the failure mode is therefore not insolvency but unbounded accumulation, and it is a different problem with different remedies: expiry of aged funding, a cap above which further authorization is refused or refunded, or scheduled return to senders. Protocol-held value also brings custody, governance and capture questions that RN-13 Part II sec. 13 lists. A design that specifies `q(F_t)` and leaves growth unbounded has not finished.

### 4.4 Source-aware base-fee signal

RN-15 sec. 7.11 proposes a source-aware signal, and this is that rule carried forward rather than a new one:

```text
G_t^BF = G_t^O + min( G_t^P , max( 0 , T - G_t^O ) )
```

Provider gas counts enough to prevent an inappropriate base-fee decrease when it fills unused target capacity, and its marginal contribution above target is zero. Ordinary and consumer gas above target still raises the base fee.

RN-16 should test the rule, not assume it. Because carried funding can support providers for several slots, the experiment must pair it with `H`, release limits, the accumulation bound, and deficit constraints. The standard all-gas update remains the baseline.

### 4.5 Positive TLA as an indicator

Positive TLA adds information unavailable in gas alone. Let `C_t` be accepted positive authorization and `A_t` the amount actually charged. For a normalized signal `u_t`, test level, first difference and second difference as indicators of temporal-pressure level, direction and acceleration. Authorization is timely but may be cheap to inflate when unused; the charged amount is costlier but depends on matching. Both should be compared.

These indicators belong first in a shadow forecast of next-slot independently eligible demand. They should affect a live base-fee update only after predictive value, manipulation cost and closed-loop stability are measured. RN-15 sec. 7.10 states the same caution for the one-slot case and the reasoning is not repeated here.

---

## 5. Scheduling without a forward curve

RN-16 posts no prices for named future slots and reserves no future block space. It makes a current-slot decision using carried funding and the provider transactions visible to the current builder.

A provider can remain pending over several slots, but each slot repeats validity checking, shortfall calculation, funding reservation, physical-capacity admission and builder selection. A TEP may state transaction-level constraints such as an expiry or acceptable delay, but RN-16 does not aggregate declarations into a forward curve, and it cannot assume all builders observe the same supply set.

No user receives a guaranteed future slot, and an unincluded provider may be replaced, cancelled, invalidated, evicted, or simply unavailable to a later builder.

### 5.1 Exploratory option: a one-slot deferral voucher

A possible extension would let a funded provider defer execution by one slot in exchange for a transaction-bound voucher. **This is not part of the mechanism specified here.** It is retained as a placeholder for later study.

The option would apply only when a provider has already qualified for funding from consumer TLA in the current slot, has signed an explicit willingness to defer if offered a voucher, and is replaced by an ordinary transaction that independently satisfies EIP-1559. The builder would not create eligibility; it could choose the settlement form only after the provider had qualified. The provider's allocated funding would become a wei-denominated voucher usable against that same transaction's recomputed shortfall in the next slot, with face value no greater than the funding already allocated. The operation would postpone an existing funded obligation rather than create new funding.

It nevertheless introduces unresolved problems: transaction-specific protocol state, proof that the provider qualified before builder discretion was exercised, binding the voucher to a later execution, expiry and refund treatment, and prevention of repeated deferral or collusion among builders, providers and replacement transactions. The provider's realized gas and the next slot's base fee would also be unknown at issue.

RN-16 therefore excludes the voucher from its state transition, accounting identities and simulation baseline.

---

## 6. Expiring and outside-option demand

A rigid opportunity may disappear after exclusion, worth something now and nothing one slot later. It may also move to another chain, rollup or centralized venue, in which case gas and backlog understate unsatisfied demand. RN-14's cross-chain activity comparison motivates this counterfactual without establishing that latency or fees caused individual migration.

TLA gives rigid demand a protocol-level monetary authorization for temporal service, and the Supply Leg gives less rigid transactions a way to accept later treatment. The benchmark must still distinguish queued, expired, cancelled, outside-option and executed demand by temporal class. **A lower backlog is not a gain if it results from more expiry or exit.**

---

## 7. ePBS and builder choice

The builder chooses which positive-TLA consumers enter the block, which provider offers are considered, effective provider tips within signed limits, the funded subset, and ordering within permitted bands.

Carried funding increases the value of controlling the candidate set, because current providers may be paid from earlier consumers. Proposer bids reward monetizable block value, not temporal welfare, provider count or reserve preservation.

Required verification includes funding pre-state and post-state, provider gas-limit reservation, realized-gas settlement, release-limit and accumulation-bound compliance, the operating cap `H`, TLA-band ordering, transaction expiry and cancellation, and no withdrawal beyond the funding leg. Private order flow and omitted transactions remain outside complete protocol observation.

---

## 8. Ownership of the funding leg

Carrying unspent positive TLA turns an authorization into a balance with intertemporal ownership. **The four candidates are four different mechanisms, not settings of one.**

1. **Sender-specific balances**, withdrawable by their owners. The protocol becomes a custodian, with per-sender state, withdrawal paths and griefing surface.
2. **Expiring authorizations**, valid for a fixed number of slots. Expiry is a policy lever with its own incidence, and it doubles as the accumulation bound of sec. 4.3.
3. **A pooled protocol balance** with stated refund rights. Simplest to account for, hardest to govern.
4. **Irrevocable contributions** once accepted. A consumer then pays for service it may never receive.

Two consequences must be stated rather than deferred.

**The simulation cannot produce one answer.** Section 10 compares configurations; under an open ownership choice it would be comparing four mechanisms. **Option 2, expiring authorizations, is the provisional baseline for simulation**, because it bounds accumulation without requiring per-sender custody, and because its single parameter is the natural thing to sweep.

**The choice propagates backwards into RN-15.** RN-15 sec. 11 argues participation is voluntary in the ordinary sense partly because unmatched authorization is refunded. Option 4 removes that, so adopting it would weaken a claim RN-15 currently makes. Options 1 to 3 preserve it in different degrees.

---

## 9. What RN-16 does not contain

No forward reservation curve; no named future-slot ownership; no term structure of temporal prices; no stream-level periodic service guarantees; no TSP aggregation; no proof of controller stability; no truthful-reporting result; no complete ePBS candidate-visibility mechanism; no protocol-guaranteed persistence, age or inclusion rights for Supply Leg offers; and no consensus-registered provider queue.

These are scope boundaries, not claims that the problems are unimportant.

---

## 10. Simulation program

### Stage 0: does carrying funding matter at all?

Before anything else, measure the distribution of **unmatched consumer authorization per block under RN-15**, across provider-to-consumer arrival ratios. RN-15's existing simulator produces this with a histogram and no new mechanism.

Two regimes, with opposite conclusions:

- if the RN-15 pool is usually **exhausted**, provider demand exceeds funding, there is little to carry, and RN-16 changes little;
- if the pool is usually **unspent**, carrying helps, but funding was not the binding constraint and any gain must be attributed accordingly.

**If the first regime holds, most of what follows need not be run.** This measurement costs a day and gates the rest of the note.

### Stages 1 and beyond

Compare, under common arrivals:

1. EIP-1559 with all-gas base-fee updates;
2. RN-15 block-local funding and refund;
3. RN-15 with a source-aware shadow base-fee signal;
4. RN-16 with carried funding but standard base-fee updates;
5. RN-16 with carried funding, provider scheduling and source-aware updates.

Traffic models should include independent Poisson arrivals, persistent burst states, common shocks, within-slot arrivals, bid replacement, local transaction-pool eviction and unequal builder visibility.

Sweep `T/L` and `H/L`; reserve release limits and the accumulation bound; the expiry parameter of the baseline ownership rule; consumer and provider arrival balance; positive-TLA level and changes; provider gas-limit slack; builder objectives; and burst duration against the twelve-second response delay.

Report physical and signal utilization; ordinary, consumer and provider gas; funding balance, drawdown and accumulation; local provider-set size, observed age, replacement, eviction, expiry and execution; positive-TLA authorization against amount charged; base-fee path, overshoot, oscillation and convergence time; urgent inclusion and expiry; queued and outside-option demand; builder and proposer revenue; burn, consumer payments and provider subsidy; hard-limit and operating-cap violations; and reserve deficit probability.

The result sought is an outward movement of the target-utilization frontier at a fixed reliability vector, not maximum average gas.

---

## 11. Relation to RN-15 and RN-17

**RN-15** is block-local. Positive authorization and provider need must meet in one block, and unmatched authorization is refunded. It introduces the asymmetric TLA field, block-local ordering, provider funding, and the first source-aware base-fee experiment.

**RN-16** is transaction-level and inter-slot. It carries the Funding Leg as protocol state and names the Supply Leg that funding must meet, while leaving that leg in ordinary transaction pools.

**RN-17** is the stream-level extension. It studies standing multi-slot bids, a term structure, and who can sell service at a given horizon, and it observes that within the proposer lookahead preconfirmation markets already sell forward commitments on one side only. Those objects should not be imported here.

---

## 12. Open questions

1. **Can the mechanism work while the Supply Leg has no protocol persistence?** How much divergence among builder-local supply sets is tolerable before allocation becomes arbitrary, and does a registered queue become necessary?
2. What ownership and expiry rule applies to carried funding, and does the provisional baseline in sec. 8 survive simulation?
3. How should the release limit and the accumulation bound jointly depend on funding balance and physical headroom?
4. Does source-aware base-fee updating improve congestion control or invite builder substitution?
5. Do positive-TLA level and changes predict future independently eligible demand?
6. Can two coupled controllers remain stable at twelve-second sampling intervals?
7. How much provider gas can be admitted below `H` without increasing validator concentration?
8. Can ePBS verification constrain builder use of carried funding without a common mempool?
9. Does the reserve retain rigid demand, or merely subsidize activity that would otherwise wait?

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- Leonardos, S., Monnot, B., Reijsbergen, D., Skoulakis, S. & Piliouras, G. "Dynamical Analysis of the EIP-1559 Ethereum Fee Market." arXiv:2102.10567. https://arxiv.org/abs/2102.10567
- Reijsbergen, D., Sridhar, S., Monnot, B., Leonardos, S., Skoulakis, S. & Piliouras, G. "Transaction Fees on a Honeymoon: Ethereum's EIP-1559 One Month Later." arXiv:2110.04753. https://arxiv.org/abs/2110.04753
- *EIP-4396: Time-Aware Base Fee Calculation.* https://eips.ethereum.org/EIPS/eip-4396
- Ethereum Foundation. "Proof-of-stake." https://ethereum.org/developers/docs/consensus-mechanisms/pos/
- TLM Research Notes: RN-01, RN-02, RN-10, RN-11, RN-12, RN-13 Part II, RN-14, RN-15 and RN-17.
