---
id: RN-16
title: "A Two-Leg Temporal Liquidity Reserve for EIP-1559"
subtitle: "Carrying temporal-liquidity funding and supply across slots without a forward curve"
version: "0.9"
status: "Working draft - mechanism and controller not yet validated"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-07"
license: "CC-BY-4.0"
---

# RN-16 v0.9

# A Two-Leg Temporal Liquidity Reserve for EIP-1559

## Carrying temporal-liquidity funding and supply across slots without a forward curve

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-16**  
**Version:** 0.9  
**Status:** Working draft. The two-leg state, scheduling rule and base-fee interaction remain to be simulated.  
**Date:** 7 September 2026

---

## Abstract

RN-15 clears a Temporal Liquidity Authorization within one block. Positive TLA is a maximum monetary authorization in wei. Negative TLA opts a below-base-fee transaction into provider treatment and commits it to a later execution band. Consumers fund provider shortfalls, unused consumer authorization is refunded, and the block ends in exact financial balance.

This note extends that mechanism across slots while retaining EIP-1559 and an ePBS setting. It introduces a Temporal Liquidity Reserve with two economic legs that must not be netted. The **Temporal Liquidity Funding Leg** carries unused positive-TLA money as protocol state. The **Temporal Liquidity Supply Leg** consists, in the baseline, of valid negative-TLA provider transactions retained in builders' or nodes' transaction pools. The Funding Leg is measured in wei. The Supply Leg is an off-chain candidate set and need not be identical across builders. They are opposite sides of an exchange, not positive and negative quantities in one unit or two consensus-state balances.

RN-16 remains a short-horizon TEP mechanism. It does not reserve named future slots, post a term structure, or aggregate stream-level Temporal Service Profiles. Those questions belong to RN-17. RN-16 asks a narrower systems question: can carried funding, locally retained provider offers and source-aware gas accounting improve congestion control over several adjacent slots without destabilizing EIP-1559?

The target result is not higher utilization alone. It is a better target-utilization frontier at fixed bounds on urgent expiry, physical headroom, base-fee volatility, builder incentives and reserve depletion.

---

## 1. Scope

This note assumes:

- EIP-1559 execution fees and base-fee burn;
- proposer-builder separation or an ePBS-like block market;
- RN-15's asymmetric TLA semantics;
- transaction-level Temporal Execution Profiles;
- several adjacent slots, without forward reservation of named slots;
- no stream-level TSP aggregation.

It changes RN-15 in two ways:

1. unused positive-TLA funding may remain available after the block; and
2. unfunded negative-TLA providers may remain candidates in later slots while their transactions remain pending, visible to a builder and valid.

Nothing in this note promises execution in a specific future slot. A locally retained provider offer may remain eligible for later scheduling; it has no protocol-guaranteed persistence, queue position or claim on future capacity.

---

## 2. Why the reserve has two legs

Positive and negative TLA have different semantics.

### 2.1 Temporal Liquidity Funding Leg

For consumer (i),

\[
c_i=\max(TLA_i,0)
\]

is a maximum monetary authorization in wei. When admitted under RN-16, the authorized or charged amount enters the funding leg according to the settlement policy.

Let:

\[
F_t
\]

be funding carried into slot (t), and let:

\[
C_t^{new}=\sum_{i\in C_t}c_i^{accepted}
\]

be new positive-TLA funding accepted in the slot. Funding available before provider settlement is:

\[
\boxed{
F_t^{avail}=F_t+C_t^{new}.
}
\]

If provider subsidies settled in slot (t) equal (S_t), then the simplest carry rule is:

\[
\boxed{
F_{t+1}=F_t+C_t^{new}-S_t-W_t,
}

where (W_t) represents authorized withdrawals, expiries or refunds under the eventual ownership policy. The solvency condition is:

\[
0\le S_t+W_t\le F_t+C_t^{new}.
\]

The shorthand proposed for the mechanism is:

\[
TLA^{fund}_{t+1}
=
TLA^{fund,leftover}_t
+
TLA^{fund,new}_t
-
\text{settled subsidies and withdrawals}.
\]

This leg is money and may be added across slots.

### 2.2 Temporal Liquidity Supply Leg

For provider (j), negative TLA is not negative money. It supplies a later-position commitment and opts a below-base-fee transaction into conditional funding.

For builder or node (B), let:

\[
\mathcal P_t^B
\]

be its local Temporal Liquidity Supply Leg: the set of pending provider offers it can observe and considers valid in slot (t). It contains transaction records, not a scalar balance. Different builders may have different sets:

\[
\mathcal P_t^{B_1}\ne\mathcal P_t^{B_2}.
\]

Each record includes at least:

\[
(L_j,\operatorname{maxFee}_j,
\operatorname{maxPriorityFee}_j,TLA_j,TEP_j).
\]

Given base fee (b_t) and builder-selected provider tip (p_{j,t}), its current shortfall and reservation are recomputed:

\[
s_{j,t}=b_t+p_{j,t}-\operatorname{maxFee}_j,
\]

\[
R_{j,t}=L_j s_{j,t}.
\]

The Supply Leg evolves as a locally retained and revalidated candidate set:

\[
\boxed{
\mathcal P_{t+1}^{B}
=
\operatorname{Revalidate}_{t+1}
\left[
\operatorname{Retain}^{B}
(\mathcal P_t^{B}\setminus\mathcal X_t)
\cup
\mathcal P_{t+1}^{B,new}
\right],
}

where \(\mathcal X_t\) contains executed, expired, replaced, cancelled, invalidated or locally evicted offers. Retaining an offer does not preserve its old subsidy quote because the base fee, selected tip and relevant execution state may change.

Under ordinary Ethereum transaction handling, a sender can amend or withdraw an offer by broadcasting a valid same-nonce replacement. Replacing the transaction also replaces its signed TLA declaration. The replacement must reach the builder concerned; transaction-pool propagation and retention are not consensus guarantees.

This leg is temporal service supply. It cannot be added to or subtracted from (F_t).

Here, **supply** means the supply of temporal liquidity: willingness to accept later treatment. It does not mean physical execution capacity. Every transaction in the Supply Leg still consumes gas and other execution resources when admitted.

### 2.3 The TLR mechanism and its state boundary

The two-leg economic mechanism is:

\[
\boxed{
TLR_t^B=(F_t,\mathcal P_t^B).
}

This notation does not mean that both components are stored in consensus state. In the compatibility baseline:

\[
\boxed{TLR_t^{protocol}=F_t,}
\]

while \(\mathcal P_t^B\) is builder- or node-local transaction-pool state.

The two legs are opposite in market role:

| Leg | What enters | Unit | What leaves |
|---|---|---|---|
| Temporal Liquidity Funding | accepted positive TLA | wei | provider subsidy, withdrawal or expiry |
| Temporal Liquidity Supply | locally visible valid negative-TLA offers | pending transactions with gas and TEP | execution, replacement, cancellation, expiry, invalidation or eviction |

There is no meaningful signed total \(F_t-\mathcal P_t^B\). They meet only through allocation and settlement. A protocol-registered Supply Leg would provide common persistence but would require new registration, cancellation, storage and anti-spam rules; it is outside the baseline.

---

## 3. Slot transition

At the beginning of slot (t), the builder observes or derives:

- current base fee (b_t);
- funding balance (F_t);
- locally visible provider set \(\mathcal P_t^B\);
- new positive-, zero- and negative-TLA transactions;
- the physical gas target (T), operating cap (H), and hard limit (L).

A minimal transition is:

1. construct the ordinary and positive-TLA candidate set;
2. add accepted positive-TLA funding to (F_t^{avail});
3. merge new negative-TLA providers into the builder's local \(\mathcal P_t^B\);
4. recompute each provider's shortfall and gas-limit reservation at (b_t);
5. select a provider subset subject to funding and physical capacity;
6. execute, reserve against gas limit, and settle against realized gas;
7. carry unused funding in protocol state, while builders or nodes may retain and revalidate still-pending provider offers for (t+1);
8. update the base fee under the selected experimental rule.

The block remains verifiable from funding pre-state, included transactions, execution results and the deterministic settlement rule. Candidate offers omitted from the block are not globally visible and do not become protocol state. ePBS therefore leaves a builder-observability problem that this note does not solve.

---

## 4. Congestion control

### 4.1 The gas-only mismatch

EIP-1559 observes realized gas:

\[
G_t=G_t^O+G_t^P,
\]

where (G_t^O) is ordinary and consumer gas and (G_t^P) is funded-provider gas. It does not observe that provider gas was admitted through a separate funding condition.

In RN-15, no current consumer funding means no provider inclusion. In RN-16, carried funding can admit a provider even when the current slot has no new consumer. Provider admission is still bounded by a finite funding stock, but the stock can sustain gas across several slots. RN-16 must therefore control both reserve drawdown and physical provider gas explicitly; it cannot rely only on same-slot matching.

### 4.2 A bounded provider region

Let:

\[
T\le H<L,
\]

where:

- (T) is the ordinary EIP-1559 target;
- (H) is the maximum operating level available to TLR-funded providers;
- (L) is the hard gas limit.

Require:

\[
G_t^O+G_t^P\le H
\]

for the TLR allocation, leaving (L-H) as physical headroom. This makes the use of the elasticity region an explicit protocol experiment rather than an accidental consequence of funding.

The provider settlement must also satisfy:

\[
S_t\le F_t+C_t^{new}.
\]

A release limit can prevent one slot from draining the entire funding leg:

\[
S_t\le q(F_t),
\qquad
0\le q(F_t)\le F_t+C_t^{new}.
\]

### 4.3 Source-aware base-fee signal

RN-15 motivates a first source-aware signal:

\[
G_t^{BF}
=
G_t^O+
\min\{G_t^P,\max(0,T-G_t^O)\}.
\]

Provider gas counts enough to prevent an inappropriate base-fee decrease when it fills unused target capacity, but its marginal contribution above target is zero. Ordinary and consumer gas above target still raises the base fee.

RN-16 should test this rule, not assume it. Because carried funding can support providers for several slots, the experiment must pair it with (H), reserve-release limits, and deficit constraints. The standard all-gas update remains the baseline.

### 4.4 Positive TLA as an indicator

Positive TLA adds information unavailable in gas alone. Let:

\[
C_t=\text{accepted positive authorization},
\]

\[
A_t=\text{positive TLA actually charged}.
\]

For a normalized signal (u_t), test:

\[
u_t,\qquad
\Delta u_t,\qquad
\Delta^2u_t
\]

as indicators of temporal-pressure level, direction and acceleration. Authorization is timely but may be cheap to inflate when unused. Actual charge is costlier but depends on matching. Both should be compared.

The indicators first belong in a shadow forecast of next-slot independently eligible demand. They should affect a live base-fee update only after predictive value, manipulation cost and closed-loop stability are measured.

### 4.5 Twelve-second feedback

Realized gas in slot (t) sets the base fee for slot (t+1). With twelve-second Ethereum slots, a one-block update delay is about twelve seconds when the next slot contains a block and longer after a missed slot. EIP-1559 can perform well on average while responding slowly to bursts or oscillating under some demand and parameter regimes.

TLA does not remove consensus causality. It classifies the current block's demand. TLR carries the Funding Leg in protocol state, while builders may retain and revalidate Supply Leg offers through existing transaction-pool behavior. Together they may give the next scheduler and experimental base-fee controller more information than undifferentiated realized gas, although only the Funding Leg is common protocol state in the baseline.

---

## 5. Scheduling without a forward curve

RN-16 does not post prices for named future slots or reserve future block space. It makes a current-slot decision using carried funding and the provider transactions visible to the current builder.

A provider can remain pending over several slots, but each slot repeats:

- validity checking;
- shortfall calculation;
- funding reservation;
- physical-capacity admission;
- builder selection.

The TEP may state transaction-level constraints such as an expiry or acceptable delay, but RN-16 does not aggregate those declarations into a forward curve. The scheduler chooses among currently valid transactions and locally retained offers. It cannot assume that all builders observe the same supply set.

This keeps the mechanism close to current EIP-1559 and ePBS. It also limits what RN-16 can promise: no user receives a guaranteed future slot, and an unincluded provider may be replaced, cancelled, invalidated, evicted or simply unavailable to a later builder.

### 5.1 Exploratory option: a one-slot deferral voucher

A possible extension is to let a funded provider defer execution by one slot in exchange for a transaction-bound voucher. This option is not part of the mechanism specified in this note. It is retained only as a placeholder for later study.

The option would apply only when:

1. a provider has already qualified for funding from consumer TLA in the current slot;
2. the provider has signed an explicit willingness to defer if offered a voucher; and
3. the builder replaces it with an ordinary transaction that independently satisfies EIP-1559.

The builder would not create eligibility. It could choose the settlement form only after the provider had qualified for funded current-slot execution. If the builder exercised the option, the provider's allocated funding would become a wei-denominated voucher usable against that same transaction's recomputed shortfall in the next slot. Its face value could not exceed the funding already allocated to the provider. The operation would therefore postpone an existing funded obligation rather than create new funding.

This construction might recognize voluntary waiting, extend temporal liquidity across one slot boundary, and let a builder use the released position for ordinary positive-tip demand. It nevertheless introduces substantial unresolved problems. The protocol would have to preserve transaction-specific state, prove that the provider qualified before builder discretion was exercised, bind the voucher to a later execution, determine expiry and refund treatment, and prevent repeated deferral or collusion among builders, providers and replacement transactions. The provider's realized gas and the next slot's base fee would also be unknown when the voucher was issued.

For these reasons, RN-16 does not include a deferral voucher in its formal state transition, accounting identities, or simulation baseline. Future work may revisit whether a strictly one-slot, non-transferable claim can be made simple, funded, verifiable and resistant to manipulation.

---

## 6. Expiring and outside-option demand

A rigid opportunity may disappear after exclusion:

\[
v_i(t)>0,
\qquad
v_i(t+1)=0.
\]

It may also move to another chain, rollup or centralized venue. Gas and backlog then understate unsatisfied demand. RN-14's cross-chain activity comparison motivates this counterfactual but does not establish that latency or fees caused individual migration.

TLA gives rigid demand a protocol-level monetary authorization for temporal service. The Supply Leg gives less rigid transactions a way to accept later treatment. TLR carries funding as protocol state; pending supply offers persist only where transaction pools retain and propagate them. The benchmark must still distinguish:

- queued demand;
- expired demand;
- cancelled demand;
- outside-option demand;
- executed demand by temporal class.

A lower backlog is not a gain if it results from more expiry or exit.

---

## 7. ePBS and builder choice

The builder chooses:

- which positive-TLA consumers enter the block;
- which provider offers are considered;
- effective provider tips within signed limits;
- the funded subset;
- ordering within permitted bands.

Carried funding can increase the value of controlling the candidate set because current providers may be paid from earlier consumers. Proposer bids reward monetizable block value, not automatically temporal welfare, provider count or reserve preservation.

Required verification includes:

- funding pre-state and post-state;
- provider gas-limit reservation;
- realized-gas settlement;
- release-limit compliance;
- operating cap (H);
- TLA-band ordering;
- transaction expiry and cancellation;
- no withdrawal beyond the funding leg.

Private order flow and omitted transactions remain outside complete protocol observation.

---

## 8. Ownership of the funding leg

Carrying unused positive TLA changes an authorization into a balance with intertemporal ownership. RN-16 must eventually choose among:

1. sender-specific balances withdrawable by their owners;
2. expiring authorizations valid for a fixed number of slots;
3. a pooled protocol balance with stated refund rights;
4. irrevocable contributions once accepted.

These alternatives have different solvency and governance properties. Version 0.9 leaves the choice open and represents withdrawals and expiries by (W_t). A simulator must select one explicit policy for each run.

---

## 9. What RN-16 does not contain

RN-16 does not contain:

- a forward reservation curve;
- named future-slot ownership;
- a term structure of temporal prices;
- stream-level periodic service guarantees;
- TSP aggregation;
- a proof of controller stability;
- a truthful-reporting result;
- a complete ePBS candidate-visibility mechanism;
- protocol-guaranteed persistence, age or inclusion rights for Supply Leg offers;
- a consensus-registered provider queue.

These omissions are scope boundaries, not claims that the problems are unimportant.

---

## 10. Simulation program

Compare, under common arrivals:

1. EIP-1559 with all-gas base-fee updates;
2. RN-15 block-local funding and refund;
3. RN-15 with a source-aware shadow base-fee signal;
4. RN-16 with carried funding but standard base-fee updates;
5. RN-16 with carried funding, provider scheduling and source-aware updates.

Traffic models should include independent Poisson arrivals, persistent burst states, common shocks, within-slot arrivals, bid replacement, local transaction-pool eviction and unequal builder visibility.

Sweep:

- (T/L) and (H/L);
- reserve release limits;
- funding ownership and expiry rules;
- consumer and provider arrival balance;
- positive-TLA level and changes;
- provider gas-limit slack;
- builder objectives;
- burst duration and twelve-second response delay.

Report:

- physical and signal utilization;
- ordinary, consumer and provider gas;
- funding balance and drawdown;
- local provider-set size, observed age, replacement, eviction, expiry and execution;
- positive-TLA authorization and actual charge;
- base-fee path, overshoot, oscillation and convergence time;
- urgent inclusion and expiry;
- queued and outside-option demand;
- builder and proposer revenue;
- burn, consumer payments and provider subsidy;
- hard-limit and operating-cap violations;
- reserve deficit probability.

The result sought is an outward movement of the target-utilization frontier at a fixed reliability vector, not maximum average gas.

---

## 11. Relation to RN-15 and RN-17

**RN-15** is block-local. Positive authorization and provider need must meet in one block, and unused authorization is refunded. It introduces the asymmetric TLA field, block-local ordering, provider funding, and the first source-aware base-fee experiment.

**RN-16** is transaction-level and inter-slot. It carries the Temporal Liquidity Funding Leg as protocol state. Builders may retain still-valid provider transactions as a local Temporal Liquidity Supply Leg and repeat allocation over several adjacent slots. RN-16 remains based on TEP, does not make the Supply Leg consensus state, and does not reserve future slots.

**RN-17** is the stream-level extension. TSP represents periodic or continuing demand and can support deadline-based curves, future service classes, term structure and explicit multi-horizon commitments. Those objects should not be imported into RN-16.

---

## 12. Open questions

1. What ownership and expiry rule applies to carried positive-TLA funding?
2. How much divergence among builder-local Supply Legs can the mechanism tolerate, and is a later commitment mechanism necessary?
3. How should the reserve release limit depend on funding balance and physical headroom?
4. Does source-aware base-fee updating improve congestion control or invite builder substitution?
5. Do positive-TLA level and changes predict future independently eligible demand?
6. Can two coupled controllers remain stable at twelve-second sampling intervals?
7. How much provider gas can be admitted below (H) without increasing validator concentration?
8. Can ePBS verification constrain builder use of carried funding without a common mempool?
9. Does TLR retain rigid demand or merely subsidize activity that would otherwise wait?

---

## References

- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
- Leonardos, S., Monnot, B., Reijsbergen, D., Skoulakis, S. & Piliouras, G. “Dynamical Analysis of the EIP-1559 Ethereum Fee Market.” arXiv:2102.10567. https://arxiv.org/abs/2102.10567
- Reijsbergen, D., Sridhar, S., Monnot, B., Leonardos, S., Skoulakis, S. & Piliouras, G. “Transaction Fees on a Honeymoon: Ethereum's EIP-1559 One Month Later.” arXiv:2110.04753. https://arxiv.org/abs/2110.04753
- *EIP-4396: Time-Aware Base Fee Calculation.* https://eips.ethereum.org/EIPS/eip-4396
- Ethereum Foundation. â€œProof-of-stake.â€ https://ethereum.org/developers/docs/consensus-mechanisms/pos/
- TLM Research Notes: RN-01, RN-02, RN-10, RN-11, RN-12, RN-13 Part II, RN-14, RN-15 and RN-17.
