---
id: RN-17
title: "Temporal Stream Profiles and Future Execution Tickets for Ethereum"
version: "0.6"
status: "Working draft - research agenda, not a protocol proposal"
program: "Temporal Liquidity Market (TLM)"
date: "September 9, 2026"
---

# RN-17 v0.6

# Temporal Stream Profiles and Future Execution Tickets for Ethereum

## Standing multi-slot bids, stream commitments, and temporal liquidity curves

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-17**  
**Version:** 0.6  
**Status:** Working draft. Research agenda, not a protocol proposal.  
**Date:** 9 September 2026

---

## Abstract

Ethereum sells execution one block at a time. EIP-1559 prices current gas and proposer-builder separation allocates construction of the current block. Neither lets an application stand at time `t` and bid for service over future slots: a deadline, a cadence, a recurring reservation, or a bounded delay for a stream of related transactions.

This note studies that object. Its unit of demand is the **Temporal Stream Profile**, a declaration for a stream whose members are related across time, carrying cadence, admissible windows, deadlines, value decay, reliability and dependencies.

Two claims are worth defending. **Funding and supply cannot be collapsed into one signed reserve**, and over a horizon this matters more than in RN-16, because money is fungible across maturities and deliverable capacity is not. And **the seller determines the horizon**: within the proposer lookahead a known party can commit, which is what preconfirmation markets already do on one side only; beyond it no party holds a position to sell against, which is where an execution-ticket architecture would be required.

The sharpest limit is that second point. Beyond roughly one epoch, this note describes a market with a demand side and no established seller, and it does not assume Ethereum will supply one.

---

## 1. Position in the TLM research program

The three notes address different horizons and should not be merged into one mechanism.

| Note | Demand object | Horizon | Main object | Intended path |
|---|---|---:|---|---|
| **RN-15** | TEP on each transaction | one slot | signed TLA and in-block settlement | narrow EIP-track experiment compatible with EIP-1559 and ePBS |
| **RN-16** | TEP on each transaction | adjacent slots | two-leg TLR: funding leg and supply leg | advanced EIP-track study of scheduling, utilization, and base-fee feedback |
| **RN-17** | TSP for a related stream, with member TEPs where needed | multiple future slots | standing bids, future service claims, and maturity curves | longer-horizon research connected to possible future execution-ticket architecture |

**RN-15** adds a second declaration beside the ordinary fee parameters. Positive TLA authorizes a monetary contribution; negative TLA opts a transaction into the supply side and commits it to later in-slot treatment. It is local to one block, and that narrowness is intentional.

**RN-16** carries temporal state across adjacent slots while preserving the different semantics of the two sides. The funding leg is an amount in wei that can remain after settlement. The supply leg is a set of still-valid provider transactions whose shortfalls must be recomputed each slot. It creates no forward curve and allocates no named future slot.

**RN-17** studies a participant acting now and requesting service over a future horizon: one execution before a deadline, one execution in any of the next `k` slots, one execution every five slots for an hour, an urgent update followed by summaries at 1, 5, 10 and 15 minutes, a group of dependent transactions that must retain order, or a recurring stream accepting interruptible service for a lower temporal price. These are Temporal Stream Profiles, and they cannot be represented by repeating an independent scalar on every transaction.

---

## 2. Congestion is a mismatch in time as well as quantity

Congestion occurs when demand for service at a particular time exceeds the service available at that time. If execution supply is scarce, some demand must adapt, and the mechanism should help demand reveal how it can.

**Fee willingness is not temporal rigidity.** The current fee market observes willingness to pay for inclusion. It does not observe whether a transaction must execute now, can wait several slots, loses value smoothly, expires at a hard deadline, or belongs to a stream where cadence matters more than any one member. A flexible transaction may pay a large tip because its wallet policy is simple or because it fears uncertainty. A rigid transaction may have a finite value ceiling. Ordering demand by money need not order it by temporal loss.

**Rigid demand does not necessarily persist.** An unadmitted urgent transaction is not guaranteed to return next slot. The opportunity may expire, move to another venue, or be abandoned. Persistence is an unreliable proxy for urgency, and the two tails are easy to confuse: repeated bidding may indicate rigid demand, or flexible demand that can afford to wait. RN-14 presents evidence consistent with temporally sensitive activity choosing lower-latency venues, which motivates the hypothesis without establishing that fees or slot timing caused any particular migration.

TLM therefore treats two dimensions as related but distinct: how much execution resource is consumed, and when, within what window, and with what reliability it should be served. Gas and fee caps address the first directly. TLA adds a narrow temporal declaration in RN-15 and RN-16. TSP generalizes it over a stream and a horizon.

This is an information claim, not an efficiency theorem. A richer declaration helps only if it is credible, priced, verifiable, and used by an allocation rule that improves outcomes after strategic behavior.

---

## 3. The Temporal Stream Profile

A TSP is a priced declaration made by or for a stream of related execution requests. It is not a statistical description of past traffic.

### 3.1 Candidate fields

| Field | Meaning |
|---|---|
| stream identifier | links related requests and settlement state |
| start and end | horizon over which the declaration applies |
| quantity or cadence | requested executions or resource envelope per interval |
| admissible windows | slots or intervals in which service is acceptable |
| deadline rule | hard cutoff or probability of completion by a time |
| value-decay rule | loss as delay increases |
| reliability class | firm, best-effort, or interruptible |
| dependency rule | ordering, adjacency, or all-or-nothing relations among members |
| authorization | maximum monetary commitment for the requested service |
| cancellation and renewal | how the stream changes or exits |

This list is deliberately larger than a proposed wire format. A deployable mechanism should seek the smallest subset that produces measurable value.

### 3.2 Relationship between TSP and TEP

RN-17 is TSP-based. A TEP remains useful as the description of an individual member where a stream contains heterogeneous transactions. For stream `s`, write its contract as

```text
Theta_s = ( H_s, Q_s, W_s, D_s, V_s, R_s, C_s )

  H_s   horizon                 D_s   deadline rule      R_s   reliability class
  Q_s   quantity or cadence     V_s   delay-value rule   C_s   dependency constraints
  W_s   admissible windows
```

A member transaction `i` may carry its own TEP `theta_i`, and the allocation is evaluated against both `theta_i` and `Theta_s`.

The distinction prevents two errors: treating recurring demand as independent transactions and losing cadence and relationship information, and flattening heterogeneous members into a stream average that hides individual deadlines.

### 3.3 Verification boundary

The protocol can verify declarations and realized service, not private urgency. It can check that a funded authorization was signed and escrowed, that a member executed inside its admissible window, that a cadence or deadline was met, that a cancellation followed the stated rule, and that settlement used the committed prices and quantities.

It cannot verify that a user truthfully reported private value decay. Truthfulness must come from payment and allocation consequences rather than from inspection.

---

## 4. Standing now and bidding over future execution

The defining RN-17 action is a bid at current time `t` for service at one or more future maturities `t+k`. Write `qD_s(k)` for stream `s`'s requested service at horizon `k` and `qP_r(k)` for seller `r`'s offered flexibility or capacity at that horizon. A clearing process may then produce a temporal price

```text
pi_t(k),    k = 0, 1, ..., H
```

and the vector of those prices is a **temporal term structure**. It may price a claim on a slot, a window, a cadence, or a reliability class. These are not equivalent and should not be reduced to one scalar.

### 4.1 Who can sell, and at what horizon

The demand side of that market is easy to specify: a stream declares and pays. **The supply side is where the design either holds or fails, and it is horizon-dependent.** A seller must hold a position it can deliver against, and on Ethereum three regimes follow.

**The current slot.** The builder is selecting the block. This is RN-15's setting, and the supply side is the set of transactions willing to accept later in-block position.

**Within the proposer lookahead.** Ethereum's proposer schedule for an epoch is known in advance, currently on the order of one epoch, so a party that knows it proposes slot `t+k` holds something real to sell. **This is the regime in which forward temporal service is already being sold.** Preconfirmation designs have a known proposer commit to including a transaction in a coming slot, backed by restaked collateral and slashing for failure to honour it, and the gateway or proposer takes the delivery risk.

RN-17's addition here is not the commitment machinery, which exists, but the second side. A preconfirmation buys a commitment about position, and nothing in those designs pays a sender for offering to take a later one. **Preconfirmation markets are one-sided in exactly the way RN-15 is two-sided.** A TSP layered on the same collateral and slashing substrate would let a stream sell flexibility across a window rather than only buy priority at a point. That is a concrete, near-term research question with an existing counterparty and an existing enforcement mechanism, and it does not depend on any new protocol object.

**Beyond the lookahead.** No party holds a position to sell against. A builder does not know it will build, and a validator does not know it will propose. A promise about slot `t+500` is either uncollateralized or backed by something other than a proposing right. This is where an execution-ticket architecture would be needed, and where RN-17's dependence on it is genuine rather than optional.

The note does not assume Ethereum will adopt execution tickets. The consequence is that **beyond roughly one epoch, RN-17 currently describes a market with a demand side and no established seller.** That is the sharpest limit on the whole direction and it should be read as the first thing to resolve, not as a detail.

### 4.2 Rolling horizon

The market may clear repeatedly. At each slot, existing commitments roll one step toward maturity; new funding and supply declarations enter; invalid, expired or cancelled claims leave under stated rules; future service is cleared or repriced; and current-slot obligations pass to the execution-allocation mechanism.

This gives a path from RN-16 to RN-17 without pretending they are the same design. RN-16 carries adjacent-slot inventory. RN-17 adds explicit maturities and service promises.

### 4.3 Window claims are not point claims

A request for any one of slots `t+2` through `t+6` supplies more temporal flexibility than a request for `t+4` specifically. A width statistic alone is insufficient, because window location, shape, value scale and dependencies all matter. The clearing rule must preserve enough information to distinguish non-substitutable windows.

### 4.4 Conditional rather than unconditional reservation

A future claim need not be a guarantee. Candidate classes are **firm**, where a protocol or bonded counterparty owes service or compensation; **probabilistic**, completion by a deadline at a stated reliability; **best effort**, a scheduling preference with no compensation for failure; and **interruptible**, displaceable under defined conditions in return for a discount or payment.

Reliability is part of the product. A unit of probable future execution is not a unit of firm execution.

---

## 5. Separate funding and supply books by maturity

RN-16's two-leg distinction becomes more important over a longer horizon, not less. The names are RN-16's: the **funding leg** and the **supply leg**.

**The funding book** holds monetary authorizations and settled balances. Write `F_t(k,c)` for funding available at horizon `k` for service class `c`, measured in wei, including new authorization, carried balances, and amounts already encumbered against matched obligations.

**The supply book** holds service offers and commitments. Write `P_t(k,c)` for offered temporal flexibility or execution capacity at horizon `k` and class `c`. It is not money. Its unit may be transactions, gas envelopes, resource vectors, or probabilistic completion obligations.

### 5.1 Why the legs cannot be netted

Positive monetary authorization and a temporal commitment have different semantics and units. Their signs do not place them on one numerical line. A clearinghouse may match them and record a monetary liability against a service obligation, but it must retain both books, because raw netting would hide which maturities are underfunded, which service promises lack deliverable capacity, whether firm and interruptible claims were mixed, whether one side is concentrated among a few actors, and whether a current positive balance is offset by larger future obligations.

### 5.2 Solvency is asymmetric across the two books

RN-16's reserve is adjacent-slot state. Over a horizon it becomes a maturity ledger, and solvency cannot be read off one scalar balance. The funding condition is the easy direction:

```text
available funding at maturity k  >=  funded liabilities due at k
```

under a stated stress model. **The supply side does not admit the same treatment, and the asymmetry is the operational reason the two books stay separate.** Money is fungible across maturities: a shortfall at `k` can be met from a balance held for `k+10`, and the constraint is arithmetic. Deliverable capacity is not fungible that way. A seller that has oversold slot `t+50` cannot borrow capacity from `t+80`, because the obligation is dated and the capacity at `t+50` is whatever it is. Capacity is also workload-dependent by sec. 9 below, so the quantity being tested is itself uncertain at the time the promise is made.

Overbooking is therefore not a variant of undercollateralization but a different failure with no monetary remedy, and it is worst exactly when many claims mature together. Section 12 carries it as a main risk; the point here is that the feasibility test it requires has to be built into the ledger rather than added as a check afterwards.

---

## 6. Relationship to preconfirmations and execution tickets

Section 4.1 places these two bodies of work at different horizons. This section states what each supplies and what it does not.

### 6.1 Preconfirmations: the near-horizon case, one-sided

Preconfirmation research already provides a commitment about a coming slot from a party that knows it holds the proposing right, with restaked collateral and a slashing condition behind it. RN-05 sec. 7 treats this and identifies the gap: sub-slot coordinates and enforcement exist, and a negative side does not. Nothing in a preconf design pays a sender for offering to take a later position.

RN-17's near-horizon question is whether a TSP can be layered on that substrate: a stream selling flexibility across a window, enforced by the same collateral, rather than only buying priority at a point.

### 6.2 Execution tickets: the far-horizon substrate

Ethereum research uses **execution ticket** for a supply-side right: a protocol-sold ticket giving its holder a chance or right to propose a future execution block, separating execution proposing from beacon proposing, and possibly resaleable. It is orthogonal to PBS, since a future execution proposer may still run a just-in-time builder auction.

RN-17 treats that work as an architectural opening, not as an existing demand-side market. A TSP claim is a request for temporal execution service; an execution ticket is a right on the block-production side. They are not the same asset.

A ticket holder could sell service claims to streams before its slot is reached, connecting protocol allocation of proposal rights, provider commitments against those rights, and application bids for windows, cadence or reliability. That composition would make a far-horizon promise credible because the seller holds a recognized position. It also creates ticket concentration, over-selling, correlated failure, censorship, and integration between ticket holders and order-flow intermediaries.

### 6.3 Do not overload the term "ticket"

Three distinct objects need three names:

- **execution-proposer ticket:** a right or lottery position associated with proposing a future execution block;
- **temporal service claim:** an application-side claim on an execution window or service class;
- **matched temporal contract:** the obligation created when a claim clears against a seller.

The research question is whether these layers compose safely, not whether one word can cover all three.

### 6.4 Current-time bids are strategically important

Research on future proposal rights already identifies timing games: participants may bid early to secure supply or late to use better information. TSP markets inherit this. A standing bid should therefore specify when it becomes binding, what information was available then, whether it may be amended, how amendments are ordered, what collateral backs it, and how cancellation is priced.

---

## 7. Instrument space

These form a research ladder rather than a package, and listing them is not an endorsement. **Whether derivatives over execution service are desirable is not settled here**, and a mechanism that prices temporal risk without delivering service may attract volume that the underlying market cannot support.

- **Spot temporal allocation.** RN-15 is the endpoint: a current-block authorization affects allocation and settlement inside one slot. RN-16 carries unmatched state into adjacent slots.
- **Forward service claim.** A stream pays or posts collateral now for service at a future slot or window, priced at trade time or indexed to a future clearing rate.
- **Multi-slot reservation.** A stream buys a schedule, such as one execution every five slots for `N` periods. The contract must specify missed-service treatment, substitution across windows, and whether unused reservations can be released or resold.
- **Fixed-for-floating temporal swap.** A stream pays a fixed temporal rate and receives the realized floating rate, or the reverse. This hedges variation without guaranteeing execution, so a separate deliverability rule is needed if the instrument is meant to secure service.
- **Perpetual stream contract.** A recurring application maintains a continuously settled position until it closes. This fits an indefinite TSP and creates margin, governance and oracle questions.
- **Firm and interruptible capacity.** Some sellers may offer capacity only when it is otherwise idle, which is relevant where proving or computation shares hardware. Interruptible service must be priced and measured separately, or the mechanism will overstate reliable supply.

---

## 8. Forward information and congestion control

EIP-1559 updates the base fee from realized gas in the previous block, so the control input is aggregate and lagging. RN-15 sec. 7.10 and 7.11 study composition signals within one slot, and RN-16 sec. 4 studies inter-slot feedback and the source-aware question. RN-17 does not restate either.

Its own contribution is one step further out. **A credible book of future commitments exposes demand before it reaches the current slot**, which would let a controller respond to a forecast rather than only to the last block. That is the first forward-looking input the fee market could have, and it arrives with a new attack surface, since strategic actors can submit and cancel claims to move expectations.

Any use of TSP data in base-fee reform must therefore separate unbacked indications, collateralized but unmatched bids, matched commitments, and executed obligations. Only the last three have direct economic consequences, and even those need different weights.

The generalized version of RN-15's question is whether scheduled, conditionally funded, firm and interruptible gas should contribute differently to a congestion forecast. The answer cannot be to ignore any of it: all of it consumes real execution capacity and affects safety. The distinction concerns the economic controller and the persistence forecast, not physical block accounting.

---

## 9. Capacity is workload-, horizon- and reliability-dependent

RN-13 Part II treats execution capacity as more than a scalar block gas limit, and RN-17 needs that richer view because it sells claims over time. A useful capacity object is conditional on workload mix and state-access pattern, degree of parallelism, latency deadline, reliability requirement, scheduling policy, hardware and network conditions, and the horizon over which service is promised.

**Realized cost may be knowable only after execution.** RN-13 Part II sec. 16.3 asks for wall-clock, cache-locality and state-access measurement separately from protocol gas. Independent metering reported in the ethresear.ch discussion of RN-13 found that instruction mixes executing identical step counts differed in real cost by more than an order of magnitude, with the dominant variable being where a datum lands rather than which opcode runs. If that carries to this substrate, a declared scalar resource requirement is not recoverable statically, which bears directly on what a seller can promise.

**Fragile parallel workloads.** For a parallel, low-latency job whose completion requires all `N` tasks to finish, mean worker throughput is insufficient and the tail of the slowest required task controls success. Adaptive replication raises completion probability and consumes further capacity. A seller should not issue firm claims from nominal capacity that disappears in the relevant completion tail.

**Dynamic and interruptible supply.** Execution or proving supply available only while hardware is idle is state-dependent and interruptible, and belongs in a separate service class rather than added to firm capacity.

**Capacity oracles.** A capacity oracle for RN-17 would report a curve rather than a number, giving available service by horizon and reliability class with uncertainty bounds. The oracle then becomes part of the mechanism's trust and manipulation surface.

---

## 10. Workload examples

### 10.1 Oracle updates

The delayed class is usually not the same data at lower quality. **It is often a derived product**, a TWAP, an aggregate, a risk statistic or a reporting mark, whose correct semantic interval is itself delayed. That is what makes oracle delivery the clearest TSP case rather than another instance of the RN-15 two-population argument: the classes are different products computed over different intervals from one event, not one product delivered at two speeds.

| Class | Requirement | Candidate TSP |
|---|---|---|
| urgent | freshest feasible observation for liquidation or trading | low-latency, high-reliability stream |
| delayed raw | same underlying observation delivered later | bounded-delay or best-effort stream |
| interval-derived | summary over 1, 5, 10 or 15 minutes | periodic cadence with interval deadline |

This structure can supply both temporal funding and temporal flexibility, but co-arrival does not guarantee balanced quantities at each maturity, and the market must measure whether both sides have depth.

### 10.2 Trading, payments, and computation

**Trading** demand often has steep value decay and a real outside option, so a missed execution may vanish rather than become backlog. A TSP can express repeated opportunities or a strategy horizon while individual orders keep their TEPs.

**Payments** may have wide admissible windows and stable cadence, making them plausible suppliers of flexibility. They still require reliability: "can wait" does not mean "may be dropped indefinitely."

**Proof and computation streams** may be scheduled over longer horizons, have multidimensional capacity, and may be interruptible, which makes them a useful test of reliability-priced service.

---

## 11. Benchmarking the design

Raw utilization is not a sufficient objective, since a mechanism could fill blocks with low-value or manipulatively generated work while worsening user outcomes. RN-17 should evaluate a **target-utilization frontier**: the best combinations achievable under physical and safety constraints.

The metrics that carry the argument are deadline-weighted admitted value, completion reliability by service class, physical utilization including multidimensional bottlenecks, base-fee level and variance, expiry and venue loss, and reserve solvency and unmatched exposure by maturity. Payments, seller compensation, builder and proposer revenue, burn, fairness and concentration, and protocol cost are reported alongside. Burn is an ETH monetary transfer and a supply-policy effect, not a one-for-one addition to social welfare.

Simulations should compare current EIP-1559 with no temporal field, RN-15-style one-slot TLA, RN-16-style adjacent-slot carry, TSP scheduling without base-fee reform, TSP scheduling with a conservative source-aware controller, and an ideal scheduler with truthful profiles as an upper benchmark rather than an implementable mechanism.

Stress cases: persistent overload, sudden bursts with correlated expiry, one-sided funding or supply markets, mass cancellation, seller failure, capacity-estimation error, ticket concentration, strategic false flexibility, strategic false urgency, and oscillation between the base-fee and temporal controllers.

Traffic models should go beyond Poisson, which is useful for checking accounting and limiting cases and is not a realistic burst model. Regime-switching and self-exciting arrival models fit the observed pattern of bursts following a common event and propagating for several slots. Such models forecast; they do not establish truthful urgency, choose a clearing rule, or guarantee controller stability.

---

## 12. Main mechanism-design risks

**Misreporting.** A participant may declare artificial urgency to obtain service or artificial flexibility to obtain compensation. Pricing, collateral and realized-service settlement must make false declarations costly.

**Overbooking and correlated failure.** Sellers may promise more than their rights or operational capacity support, and the failure has no monetary remedy (sec. 5.2). It is most dangerous when many claims mature together.

**Liquidity fragmentation.** Separate maturities, windows and reliability classes create thin markets. Coarse classes improve depth and lose information, and the tradeoff should be measured.

**Market concentration.** Future proposal rights and stream order flow may concentrate in the same intermediaries, and a temporal market could deepen that integration unless access, collateral and resale rules are designed against it.

**Controller interaction.** A base-fee controller, a temporal clearing process and a reserve policy may respond to the same event at different delays. Individually stable rules can oscillate when coupled, so joint stability is a first-order requirement.

**State and griefing cost.** Long-lived declarations consume protocol state and can be used for denial of service. Fees or deposits must cover storage, update, verification and cancellation.

---

## 13. Research sequence

**Stage 1, measurement.** Estimate persistence, expiry, cancellation and venue-switching after non-inclusion; measure within-slot arrival and rebid behavior; identify recurring streams and cadence; test whether oracle temporal classes co-arrive in usable proportions; estimate capacity and completion tails by workload.

**Stage 2, off-chain market model.** Define a minimal TSP schema; clear standing bids over a rolling horizon; maintain separate funding and supply books; simulate maturity-specific prices and failures; compare spot, window and cadence claims.

**Stage 3, commitment layer.** Specify collateral and cancellation; define verifiable service outcomes; model seller default and replacement; test composition with preconfirmation collateral first, since it exists, and with candidate execution-ticket architectures second.

**Stage 4, protocol integration study.** Identify the minimum consensus-visible state; bound verification and storage cost; analyze censorship and concentration; prove accounting conservation and solvency conditions; analyze joint stability with base-fee feedback.

No EIP claim should precede these results. RN-15 and RN-16 remain the nearer EIP-track notes.

---

## 14. The questions that gate the rest

Four questions decide whether the direction is worth pursuing. The remaining open items are consequences of their answers and are kept in a private working file.

1. **Who is the seller at horizon `k`, and what backs the promise?** Within the proposer lookahead there is an answer and a deployed enforcement mechanism. Beyond it there is neither, unless an execution-ticket architecture supplies one (sec. 4.1).

2. **What exactly is promised?** Inclusion, ordering, gas availability, completion by a deadline, or only compensation after failure. Every other design choice depends on which of these a claim is.

3. **Can funding and supply curves be matched without creating an undercollateralized clearinghouse?** The funding side is arithmetic; the supply side needs a feasibility test against capacity that is itself uncertain when the promise is made (sec. 5.2).

4. **How often does rigid demand expire or leave Ethereum rather than persist as backlog?** This is measurable now, it does not depend on any mechanism existing, and it sets the size of the prize. If unserved urgent demand simply waits, the case for the whole direction is much weaker.

---

## 15. Claims and non-claims

**Claimed here.** A transaction-only fee market omits economically relevant temporal structure. Stream-level service requires a TSP rather than repeated independent scalar declarations. Funding and supply have different units and must remain separate by maturity, and their solvency conditions are not symmetric. Preconfirmation markets are one-sided and their substrate could carry a second side. A credible book of future commitments may contain information unavailable to a gas-only lagging controller. Evaluation requires a multi-metric frontier rather than raw utilization.

**Not claimed here.** That execution tickets will be adopted by Ethereum; that a TSP market should be part of an execution-ticket proposal; that derivatives over execution service are desirable; that more block utilization is always better; that provider-funded gas is physically cheaper; that burn equals social welfare; that richer declarations are automatically truthful; that any particular temporal price curve is stable or incentive compatible; or that anything here is ready for an EIP.

---

## 16. Summary

RN-17 is the stream-level and forward-looking branch of TLM research. The demand object is the TSP: cadence, windows, deadlines, value decay, reliability and relationships among executions. Member transactions may keep their TEPs, but the market contract belongs to the stream.

The settlement architecture must keep separate funding and supply books by maturity, because money and temporal commitment are not one signed quantity, and because a monetary shortfall can be met from another maturity while an oversold slot cannot.

The horizon is set by the seller. Within the proposer lookahead, preconfirmation markets already sell forward commitments with collateral behind them, and what they lack is a side that pays a sender for accepting later service. Beyond the lookahead no party holds a position to sell against, and an execution-ticket architecture would be required. Since this note does not assume Ethereum will build one, the far-horizon market currently has a demand side and no established seller. Resolving that is the first task, not a detail.

---

## References

- Ethereum Research. **Execution Tickets** (2023). https://ethresear.ch/t/execution-tickets/17944
- Ethereum Research. **MEV resistant dynamic pricing auction of execution proposal rights** (2024). https://ethresear.ch/t/mev-resistant-dynamic-pricing-auction-of-execution-proposal-rights/20024
- Ethereum Research. **Exploring Sophisticated Execution Proposers for Ethereum** (2025). https://ethresear.ch/t/exploring-sophisticated-execution-proposers-for-ethereum/21386
- Ethereum Research. **On block-space distribution mechanisms** (2024). https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764
- Ethereum Improvement Proposals. **EIP-1559: Fee Market Change for ETH 1.0 Chain.** https://eips.ethereum.org/EIPS/eip-1559
- R. F. Engle. **Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation.** *Econometrica* 50(4), 1982.
- R. F. Engle and J. R. Russell. **Autoregressive Conditional Duration: A New Model for Irregularly Spaced Transaction Data.** *Econometrica* 66(5), 1998.
- TLM Research Program: RN-01 and RN-02 (TEP and TSP); RN-05 (temporal execution quanta, and preconfirmation comparison in sec. 7); RN-11 and RN-12 (allocation and mechanism design); RN-13 Part II (capacity and benchmarks); RN-14 (demand and venue choice); RN-15 (one-slot TLA); RN-16 (two-leg adjacent-slot TLR).
