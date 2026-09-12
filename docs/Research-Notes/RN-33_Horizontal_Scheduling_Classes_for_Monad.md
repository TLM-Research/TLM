---
id: RN-33
title: "Horizontal Scheduling Classes for Monad"
subtitle: "A class and scheduling architecture, its capacity model, and the experiments that would settle it"
version: "0.4"
status: "Working draft. Architecture and hypotheses. No encoding, no parameters, no pricing mechanism."
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-11"
license: "CC-BY-4.0"
---

# RN-33 v0.4

# Horizontal Scheduling Classes for Monad

## A class and scheduling architecture, its capacity model, and the experiments that would settle it

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-33**  
**Version:** 0.4  
**Status:** Working draft. It fixes objects, a capacity model and a candidate class architecture. It fixes no encoding, no class parameters, no prices, and no market mechanism.  
**Date:** 11 September 2026

---

## Abstract

Monad's short blocks, asynchronous execution and optimistic parallel execution may make protocol-visible cadence, deadlines and flexibility more useful than they are in a single serial queue. This note sets out the architecture that would be needed to find out.

Three objects are kept separate: the **Temporal Stream Profile** a sender declares, the **scheduling class** the protocol implements, and the **mapping** between them, which is guidance and not protocol. Two choices carry most of the architecture. **A class share denominated in declared gas limit is an enforceable proxy, not the capacity being optimised**, because under optimistic parallel execution the conflict structure of what was admitted determines the work performed. And **for a stream member the per-transaction mark is derived from conformance to a rate contract rather than declared**, which is what DiffServ does with drop precedence and what makes a declaration checkable against many observations rather than one.

Four claims are stated as hypotheses rather than results, each with the experiment that would settle it: that contention on this architecture is horizontal; that declared temporal slack improves completed work under optimistic execution; that a small class set separates demand a fee scalar cannot; and that compensated temporal supply adds value over uncompensated yielding. **The fourth is the one the programme most wants and is furthest from having**, because compensation requires a pre-market entitlement this note cannot define. A stream declaring that it tolerates delay has not shown that moving it released capacity, or that it held a position it could sell.

RFC 8622's Lower Effort is the case against the market. It is a below-best-effort behaviour that nothing compensates, and senders mark it anyway. Whether that incentive transfers here is the cheapest experiment in this note.

---

## 1. Scope, and the division of work

RN-12 states the conceptual mechanism for Ethereum without committing to an encoding, and RN-33 was intended to play that role for Monad. Review of v0.2 and v0.3 showed the mechanism cannot be stated yet, because the resource, the scheduler's verifiable obligations, the default guarantee and the settlement timeline are not defined. This version defines those and stops there.

| Note | Owns |
|---|---|
| **RN-33** | the class and scheduling architecture, the capacity model, the default guarantee, the simulation design |
| **RN-34** | transaction-level encoding, and immediate temporal authorization for a transaction belonging to no stream |
| **RN-35** | stream contracts, conformance, reservations, and any two-leg market |

**Fixed here.** The three objects. The resource vector and which component is enforceable. That the per-transaction mark is derived from stream conformance. A candidate minimal class set, and the tuple each class must fill to be a class. The separation of private position sensitivity from ordering externality. What a leader can be required to do and what a validator can verify.

**Not fixed here.** Any encoding. The number of classes, their parameters, the meter constants. Any price, payer, recipient, clearing rule or refund rule. Whether a market is needed at all.

**Assumed from RN-26, and tested in sec. 3.** That contention on this architecture is horizontal. Nothing below assumes the hypothesis has been confirmed.

---

## 2. Dated Monad facts

Monad's public parameters have changed across revisions, and a class architecture derived from one mutable block-time value would not survive the next. Every parameter used below is pinned to a source and a date.

| Fact | Value | Source and date |
|---|---|---|
| Base-fee input `block_gas` | **sum of declared transaction gas limits**, not realised gas | Category Labs, October 2025 |
| Base-fee target | 80% of the block gas limit | Category Labs, October 2025 |
| Controller state | exponentially smoothed trend and second moment around target | Category Labs, October 2025 |
| Block interval used in calibration | 400 ms | Category Labs, October 2025 |
| Min block time | 300 ms | Monad documentation, MonadBFT, September 2026 |
| Finality | 2 rounds, 600 ms; speculative finality 1 round, 300 ms | Monad documentation, MonadBFT, September 2026 |
| Delayed Merkle-root parameter | `D = 3` | Monad documentation, asynchronous execution |
| Execution model | optimistic parallel execution, sequential merge in canonical order | Monad documentation, parallel execution |
| Block production | **one leader per round, who builds and proposes its own block**; no proposer-builder separation | Monad documentation, MonadBFT |
| Leader schedule | stake-weighted and deterministic, over fixed epochs of 50,000 blocks | Monad documentation |
| Mempool | **local to each validator**; RPC forwards transactions to the next several scheduled leaders, rather than gossiping to a global pool | Monad documentation |

**Four latencies are distinct and this note keeps them apart.**

```text
D = 3                  delayed state-root commitment parameter
execution completion   when a transaction's result is known
consensus finality     when the ordering is irreversible
receipt latency        when a user can observe the outcome
```

"Execution lags by three blocks" compresses these and is avoided below. `D = 3` is a state-root commitment parameter, not a universal three-block execution-completion delay.

**Two block-time figures appear above and they are not the same quantity.** The 400 ms is the calibration interval of the October 2025 base-fee design; the 300 ms is the current documented minimum. Any claim resting on block timing must say which it uses, and be re-pinned before it is made.

**The role is a leader, not a proposer.** Monad has no proposer-builder separation: the leader of a round selects a payload from its own mempool, builds the block and proposes it. This note therefore says *leader* throughout, and any argument that assumes a separate building market does not transfer from Ethereum.

---

## 3. The horizontal-contention hypothesis

RN-26 argues that Monad's binding scarcity is which class of work obtains capacity rather than who is placed first. Stated that way it is not falsifiable, and the two scarcities are not exclusive: any allocation among classes also determines which transactions are admitted and often their relative timing, and fee ordering changes the workload composition of a block.

**The hypothesis, stated so that it can fail:**

> At equal physical capacity and under a fixed default-service constraint, a class-aware allocation improves deadline success, cadence error, or completed work relative to fee-only ordering.

If that comparison shows no improvement, the architecture below is aimed at the wrong scarcity and an RN-15 analogue is the right instrument. Section 15 gives the experiment.

**"Shared sub-block space" is dropped.** Monad commits a linearly ordered block and does not expose protocol-defined sub-block class partitions. Describing one as though it existed assumed the mechanism this note is trying to evaluate.

---

## 4. Three objects, and why the stream is the unit

Rate, cadence, jitter and burstiness are properties estimated or contracted over a sequence of transactions. They cannot be observed from one transaction alone.

The distinction this supports is not between verifiable and unverifiable preference. A sender's urgency is private and no protocol verifies private utility. What a protocol can do is bind a declaration to consequences: a payment, an expiry, a conformance penalty. **Separate truth verification, which is unavailable, from enforceable authorization, which is what the mechanism needs.** A sender declaring "one update every five blocks, jitter within one block" has stated something the chain can measure against the stream's realised behaviour and penalise on departure, whatever the sender privately wants.

Three objects follow, and they must not be conflated.

- **Temporal Stream Profile.** What a sender declares about its own demand: rate, cadence, envelope, footprint, and the tolerance vector of sec. 6.2. A demand object.
- **Scheduling class.** What the protocol does with a stream that selects it. A supply object, named for the treatment rather than the workload.
- **The mapping.** Which profiles should select which class. Guidance, and not protocol.

The term *scheduling class* is borrowed from operating systems, where a scheduling class names the discipline applied, as in first-in-first-out, round-robin or idle, and never the program that asked for it. That is the rule RN-04 sec. 4.1 states: classes specify protocol-defined execution semantics, not application identities.

---

## 5. DiffServ as a source of questions

DiffServ defines a small set of forwarding treatments and a large codepoint space, with classification at the network edge and simple forwarding in the core. It is the one differentiated-service design that reached production at scale, which makes it a useful source of design questions. It is not evidence that an execution analogue follows.

**What transfers.**

**Classes are characterised, not enumerated.** RFC 4594 describes twelve service classes by traffic shape, being packet size distribution, constant or variable rate, elastic or inelastic, bursty or not, and flow duration, crossed with tolerance to loss, delay and jitter. Applications are mapped in as examples, so that a future application with similar properties lands in an existing class without a standards change.

**Jitter is a separate axis from delay.** Multimedia Streaming tolerates medium delay and is marked "yes" to jitter; Broadcast Video tolerates medium delay and requires low jitter. Same delay budget, opposite jitter requirement, different class. A scalar urgency field cannot express that difference.

**The vocabulary is larger than the deployment.** Sixty-four codepoints, four behaviour families, twelve documented classes, and a recommendation that operators "start off with three or four service classes for user traffic and add others as the need arises."

**Treatments are separated from mapping, and the document statuses record it.** RFC 4594 is *Informational* and says of itself that it "does not specify an Internet standard of any kind". The toolkit is standards track: the DS field is RFC 2474, Assured Forwarding RFC 2597, Expedited Forwarding RFC 3246, Lower Effort RFC 8622. What the network does is specified; which traffic should ask for what is advice. That is sec. 4's three-object split, reached by a standards body over a decade of deployment.

**A meter can compute what a sender would otherwise declare**, which sec. 9 takes up.

**What does not transfer.**

- A chain is not an administrative domain in the networking sense. There is no edge at which an operator classifies traffic under an agreement.
- Leaders and validators do not necessarily share one policy or one candidate set, which sec. 10 makes a constraint rather than an assumption.
- Assured Forwarding's drop precedence is not equivalent to priority-fee ordering. One is a scheduler input the network computes; the other is a payment a sender chooses.
- A scheduling class is not a per-hop forwarding behaviour. There is one hop.
- Economic settlement does not imply that every class needs a separate market price.
- Lower Effort's incentive may not transfer, because delay, expiry and fee liability differ between a dropped packet and a pending transaction.

---

## 6. Characterising execution demand

The method transfers. The contents do not.

### 6.1 Traffic characteristics

| Characteristic | Packet networks | Execution |
|---|---|---|
| Size | packet size distribution | declared gas limit per member |
| Rate | constant or variable emission | arrival rate and its constancy |
| Periodicity | implicit in rate | explicit cadence, and its tolerance |
| Elasticity | reacts to loss by reducing rate | reacts to price by reducing rate |
| Burstiness | self-correlated arrivals | correlation with common events, which is stronger |
| Duration | flow lifetime | stream persistence and renewal |
| **Footprint** | not modelled in classification | **state accessed, read and write** |

The last row is the largest difference. Packets do create state in a network, in flow tables, caches and middleboxes, so the defensible statement is not that footprint is absent but that **DiffServ classification does not model it**, while EVM transactions expose persistent shared-state dependencies central to execution semantics. Two transactions of identical declared gas may conflict or not, and under optimistic parallel execution that changes the work performed.

### 6.2 The tolerance vector

| Axis | DiffServ | Execution |
|---|---|---|
| Exclusion | loss | fraction of members never included, or expiring |
| Delay | delay | time from submission to inclusion |
| Jitter | jitter | variance of the realised inclusion interval |

The three carry over intact. Jitter matters here for the reason it matters for voice: a stream with a cadence requirement is harmed more by irregularity than by a uniformly longer interval.

### 6.3 Position is two concepts, and only one belongs in a profile

Earlier versions added position exposure as a fourth tolerance axis and treated an oracle publication as position-exposed because others trade against it. That conflates two things.

**Private position sensitivity.** The sender's own value depends on its order relative to other transactions. An order-book cancel has this: a cancel landing after the trade it was meant to prevent is a quote picked off, and the loss is the sender's.

**Ordering externality.** Others are harmed by the stream's predictable placement. An oracle publication has this: the loss from front-running the update falls on protocols and traders consuming it. The publisher's own value depends on freshness, and its position relative to any particular transaction is not something it has a private reason to price.

**Only private position sensitivity belongs in the TSP.** A first-person declaration cannot carry a third party's externality, and treating it as though it could would invite publishers to claim protection they have no private reason to want. The externality is real and belongs to protocol scheduling policy, encrypted order flow, or another externality-control mechanism, none of which this note specifies.

The two also differ in kind from the other axes. Exclusion, delay and jitter describe service the stream itself experiences. An ordering externality describes the effect of the stream's placement on everyone else.

---

## 7. Capacity and conflict

A class share has to be denominated in something a protocol can enforce and something the analysis can reason about, and these are not the same quantity.

**The resource a transaction consumes is a vector.**

```text
r_i = ( L_i        declared gas limit, the consensus admission unit
        g_i        protocol-charged gas
        w_cpu_i    execution work
        w_io_i     state read and write cost
        c_i        conflict and re-execution cost
        s_i )      persistent state added
```

Monad's base-fee design sums `L_i` over the block, per sec. 2. That is the enforceable quantity: known before execution, signed by the sender, and available to consensus. **A class share should therefore be metered in declared gas limit, and this note labels that the enforceable proxy rather than the capacity being optimised.**

**The proxy and the objective diverge.** Optimistic re-execution is a real cost that does not appear as additional charged gas. A class whose members touch disjoint state converts its share efficiently; one concentrated on a hot account converts the same share into more re-execution and less completed work. A share is a claim on admitted declared gas, not on completed work, and the gap between them is a property of the class's footprint.

Any allocation rule treating shares as interchangeable assumes away the architecture's defining feature, and any throughput claim stated in terms of shares has to say which component of `r_i` it means.

---

## 8. A minimal class set

### 8.1 What a class must specify

A class is not named by the workload that uses it and is not distinguished by price. RN-04 sec. 4.3 forbids a class differing only in price: that belongs in the fee layer. To be a class rather than a parameter setting, a candidate must fill six slots differently from every other class.

```text
class = ( eligibility     who may select it, and what they must declare
          capacity rule   how much of the block it may hold
          placement rule  where inside the permitted region members go
          expiry rule     what happens when the window or interval closes
          payment rule    what is charged, and for what
          failure rule )  what the protocol owes on non-delivery
```

**Merge any two classes whose tuples differ only by parameter values.** Applying that to v0.2's six-class set collapses it. Expedited and Assured both give fast admission subject to a cap or rate; Assured and Cadenced both reserve capacity over an interval; Deferrable and Lower Effort both yield current capacity. "Next block or not at all" is a deadline parameter and an exclusion rule, not a discipline.

### 8.2 The candidate minimal set

Four, with a fifth posed as a question.

| Class | Eligibility | Capacity rule | Placement rule | Expiry rule |
|---|---|---|---|---|
| **Baseline** | no declaration | sec. 11's guarantee | leader policy, unchanged | none |
| **Cadenced** | an interval and a jitter bound | reserved quota per interval | chosen within the interval | quota does not accumulate across intervals |
| **Bounded** | a deadline within a stated horizon | what other classes leave, up to a cap | anywhere before the deadline | deferred to Baseline or dropped, per declaration |
| **Residual** | willingness to yield, no deadline | no reservation | after other classes | none |

Payment and failure rules are left empty on purpose. Section 13 says why: they depend on which pricing variant is chosen, and none has been selected.

**Whether an expedited class is needed is open.** Racing work, being arbitrage, liquidation and mint, wants to be early. Earlier versions concluded it needs no class because the priority fee already prices position, but sec. 10 shows that premise does not hold. The remaining test is sec. 8.1's: **add an expedited class only if its handling cannot be represented as a short deadline plus a capacity cap.** This is the most consequential open item in the class set, because racing is the largest value concentration on the roster.

### 8.3 Residual, and the case against compensation

RFC 8622 standardises a below-best-effort behaviour and **nothing compensates traffic for marking it.** Senders use it because during congestion unmarked traffic competes and loses while Lower Effort traffic passes in the gaps.

If that incentive transfers, a supply of scheduling flexibility exists with no transfer of value, and the compensation machinery a two-sided crossing needs is unnecessary for this class. **This is the strongest argument in the note against its own market**, and the cheapest thing here to test, since it needs no entitlement, no baseline and no transfer.

Whether it transfers is not obvious. A dropped packet is retransmitted by a protocol the sender does not manage; a delayed transaction stays pending, keeps its fee liability, and may expire. Delay, expiry and fee exposure all differ.

### 8.4 Mapping profiles to classes

Guidance, and not protocol. A profile qualifies by its declared characteristics, never by the name of the application that produced it. The workload examples illustrate and bind nothing, and application identity is not a reliable profile: some payments are flexible and some are point-of-sale or liquidation-driven and are not.

| Stream characterisation | Exclusion | Delay | Jitter | Private position | Candidate class |
|---|---|---|---|---|---|
| constant cadence, inelastic, widely-read state | low | medium | **very low** | low | Cadenced |
| loose cadence, tiny envelope, very high rate | high | very low | medium | medium | Cadenced, or expedited if sec. 8.2 resolves |
| bursty, shock-correlated, inelastic, short-lived | very low | very low | n/a | **very high** | unresolved, per sec. 8.2 |
| low rate, hard cutoff, indifferent to placement before it | very low | high until the bound | high | low | Bounded |
| high count, largely disjoint state, elastic, wide window | low | high | high | low | Bounded or Residual |
| low rate, no deadline in horizon, elastic | medium | very high | very high | very low | Residual |
| undeclared | | | | | Baseline |

**Three worked cases.**

**An order book is two streams, not one.** Quote posts are roughly cadenced, bursty on news, near-neutral on private position. Cancels follow the event rather than a clock and are strongly position-sensitive, because a cancel that lands late is a quote picked off. The same application runs two streams with different profiles, and an application may declare as many streams as it has distinct requirements. A single per-application classification would average them and serve neither.

**Deadline work is elastic supply to the scheduler.** Settlement, expiry-driven work and cross-chain relay declare a deadline and little else. In Bounded that gives the leader a pool it can move, which is the input sec. 14.1 tests. Whether the pool can also be compensated is sec. 13's question, and the answer there is not yet.

**The oracle pair is not one workload.** A real-time feed is tightly cadenced and carries the ordering externality of sec. 6.3. A derived interval product, being a candle or average over a closed interval, cannot be finalised before the interval closes. Earlier versions called the second one ideal filler, which is too strong: after close it may be urgent because downstream protocols depend on timely publication, its computation may be maintainable incrementally before close, and it shares hot state with the feed, which makes it poor filler during the same event burst. **State earliest finalisation, deadline, incremental-computation option and destination dependency separately, and treat suitability as empirical.**

---

## 9. Stream identity and the conformance meter

### 9.1 What the meter does

Within Assured Forwarding the part that varies per packet is the drop precedence, and RFC 2697 and RFC 2698 specify how it is set: a token-bucket meter measures the flow against its committed rate and marks each packet by conformance. **The sender does not choose the mark.** It chooses the class and accepts a rate contract; the mark follows from whether the stream keeps to it.

```text
declared   TSP   = class + rate contract + tolerance vector
observed         = realised arrivals, declared gas, state footprint
derived    TEP_i = f( TSP , conformance of the stream at i )
```

On the Internet the binding is administrative: an edge router distrusts the endpoint's marking and re-marks by policy. A chain has no such point, because the sender signs and nobody can re-mark. A deterministic meter computed from declared terms and observed history is the substitute, with **members beyond contract degraded to a lower class rather than refused**, which keeps the failure proportional to the breach.

The manipulation surface this closes is specific. A sender who cannot set the per-transaction mark cannot inflate it per transaction. What remains misreportable is the stream contract, one declaration covering many transactions, checkable against many observations rather than one. That is what RN-02 requires of a declaration and what a single transaction cannot supply.

### 9.2 What the meter does not do

**A conformance meter enforces a rate contract.** It does not verify urgency, deadline value, position sensitivity, or that the sender chose the class honestly. A stream can conform perfectly to a contract it selected strategically.

So "the meter makes it bind" is too broad a claim. It makes a rate envelope enforceable. The economic binding, being whatever makes a class costly enough that not every stream claims the best one, is a separate problem, and sec. 13 does not solve it either.

### 9.3 Open before a meter can be specified

- how a stream is identified, without building an identity system;
- who owns the stream state, and whether several accounts may share a stream;
- how token-bucket state is updated under reorgs;
- what stops a sender splitting one stream into several to escape a contract it is breaching;
- whether unused quota is transferable;
- whether conformance is measured in transaction count, declared gas limit, or a vector including write footprint;
- what per-stream state costs, against the per-transaction declaration it replaces.

These belong to RN-35. None is answered here, and the class architecture is not implementable until they are.

---

## 10. Leader policy, and what a validator can verify

This section replaces two claims earlier versions made and should not have.

**The priority fee is not an enforceable price of intra-block position.** Monad's published base-fee material says that fee per gas affects whether a transaction is included. It does not establish a consensus rule requiring a leader to sort the block by priority fee. Bundles, dependencies, private submission and implementation policy can all determine ordering, and a validator checks validity rather than revenue-maximising sort order.

**Four outcomes have to be kept apart:**

```text
1  validity at the prevailing base fee
2  probability of inclusion
3  ordinal position inside the block
4  application-level outcome after execution
```

A priority fee influences 2. It does not guarantee 3, and 4 depends on the state the transaction meets. Earlier versions assigned racing work to no class on the ground that the fee already supplies the position service, which assumed 3. Section 8.2 reopens that question in consequence.

**There is no shared candidate set, by design.** Monad has no global mempool. Each validator keeps a local pool, and RPC nodes forward transactions directly to the next several scheduled leaders instead of gossiping them to the network, which is what removes propagation latency from the critical path. A leader therefore builds from a pool that no other node is guaranteed to hold. Three consequences follow, and each removes something an earlier version relied on.

- **A class-aware selection rule is not recomputable from a globally known candidate set.** A validator cannot invalidate a block for omitting a transaction it saw, absent an inclusion-list or availability mechanism the protocol does not have.
- **"First come" is not globally defined.** A distributed mempool has no consensus arrival time, so neither a class nor a default guarantee may be specified in terms of arrival order.
- **Leader omission is in the threat model.** A leader can withhold demand or supply from any allocation or clearing, and private order flow can bypass it entirely.

**What a validator can check** is the committed block against rules stated over its contents: that a class label is consistent with the stream's metered conformance, that a reserved quota was not exceeded, that a declared deadline was not violated by the placement chosen. **Verification of included-order validity is available; verification of candidate-set completeness is not.** Every rule above is written to need only the first.

---

## 11. Default service

**A default must exist and must require no declaration.** RN-15 gives the reason: a sender declaring nothing should not be made worse off, or participation is not voluntary in the ordinary sense.

Earlier versions said Default receives "current treatment, unchanged" and also proposed a protected floor share. Those are inconsistent, since a reserved floor is itself a change. More seriously, a per-transaction guarantee of no degradation is probably impossible once differentiated classes hold capacity under contention: reserving share for Cadenced work can delay an undeclared transaction that was never explicitly reordered.

**The guarantee is therefore statistical, and stated against a replayed counterfactual.** Two forms, either measurable:

```text
inclusion form   Pr( T_i <= d | i undeclared ) >= s      for a stated d and s

tail form        p95 and p99 delay of undeclared traffic <= baseline + e,
                 where baseline is the same workload replayed
                 under fee-only ordering
```

The counterfactual matters as much as the bound. "No worse than today" is not a metric until "today" names a scheduling rule, and per sec. 10 it cannot name arrival order.

What is fixed is the constraint rather than the constant: **neutrality is a constraint on the mechanism, not a metric to trade against.** A design improving aggregate service while degrading undeclared traffic has failed whatever its other numbers.

---

## 12. The settlement timeline

Earlier versions claimed the horizontal mechanism settles in the block and carries no state across the execution lag. That holds only for a charge based entirely on the committed class label or order, and the services proposed here are not all of that kind: cadence spans intervals, committed rates and burst allowances span streams, Bounded placement spans blocks, conformance is a history, and Residual completion is open-ended.

**Five events, which must not be collapsed:**

| Event | When it is known | What can settle on it |
|---|---|---|
| Class assignment | at consensus on the block | a label, a share consumed |
| Inclusion and ordering | at consensus on the block | placement within a declared bound |
| Execution completion | after execution, per sec. 2 | anything depending on realised gas |
| Interval or deadline fulfilment | at interval close or deadline expiry | cadence error, deadline success |
| Financial settlement | after the above, per the payment rule | compensation, refund, penalty |

**Consensus can commit a class label immediately. It cannot know at that time whether a multi-block contract was fulfilled.** The architecture therefore needs persistent state, expiry rules, cancellation rules and non-performance rules, whatever `D` is. Service-contract duration and execution lag are different problems, and only the second is what RN-15 was built to avoid.

This removes what v0.2 called the sharpest practical advantage over an RN-15 analogue. What survives is narrower: **the components that settle at consensus are a larger fraction here than on a chain where every temporal claim depends on realised gas.**

---

## 13. Pricing and allocation variants

No mechanism is selected here. Three variants are stated so RN-35 can compare them, and the condition that separates them is stated first.

**The entitlement problem.** Compensating a stream for yielding requires knowing what it yielded. A declaration that a stream tolerates delay does not establish that moving it released capacity, or that it held a position it could have sold. A transaction that would not have been included cannot sell deferral from an inclusion position it never had, and a leader could assign a favourable position and then call its movement supply. This is the counterfactual-ownership problem RN-12, RN-15 and the RN-16 review all identify, and this note does not solve it.

**Until a pre-market reference allocation is defined, Bounded and Residual are scheduler inputs, not market supply.** That is how sec. 8 describes them.

| Variant | What it requires | What it would show |
|---|---|---|
| **Uncompensated yielding** | a class label and a discipline, nothing more | whether RFC 8622's incentive transfers, per sec. 8.3 |
| **Protocol-priced reservation with rebate** | a posted or controller-set price, a reservation contract, a refund rule | whether one-sided pricing allocates class capacity adequately |
| **Two-leg crossing** | a baseline entitlement, measurable additionality, a clearing rule, budget balance | whether compensated supply beats both, and by how much |

**The case for the third is not established, and earlier versions overstated it.** A posted price that is temporarily wrong produces misclassification or excess demand; calling that an arbitrage does not show that two-sided clearing is required, and dynamic posted pricing is itself a price-discovery process. The conditions under which an explicit supply leg adds value can be stated, and each is a measurement:

1. a credible baseline entitlement exists;
2. the capacity is rival, so that yielding releases something;
3. the release is additional relative to the baseline;
4. participation on the supply side is compensation-sensitive, which sec. 8.3 questions;
5. budget balance is achievable without subsidy.

**Two further cautions.** Temporal liquidity is **state-dependent**: under the base-fee target of sec. 2 blocks are often not at the limit, and when there is room, deferral releases nothing. Any supply side therefore bids in a subset of blocks, and **whether a class market has useful depth is open.** And the goods are not one good. Earlier admission, intra-block position, class capacity share, cadence reservation and multi-block deferral are distinct, and a single crossing cannot price them until substitutability is defined.

**Naming.** What v0.2 called the "second price" is renamed the **class-capacity price**. "Second price" collides with second-price auction, and the count was wrong in any case: there are three economic quantities, being the base fee for resource admission, the priority fee for leader compensation and inclusion preference, and any class-capacity payment. Whether the third is an additional payment, a transfer, a rebate, or a component inside an existing cap is not decided here.

**One constraint carries from RFC 3246.** Expedited Forwarding must be policed and rate-limited, because unpoliced EF starves every other class. **A price bounds willingness to pay and never bounds quantity.** Whatever variant is chosen, the highest class needs an explicit capacity cap in addition to whatever it charges.

---

## 14. Two hypotheses about the scheduler

### 14.1 Placement freedom under optimistic execution

A class carrying a window gives the leader a choice it does not have. If a transaction has declared that any of several blocks is acceptable, the leader may place it where it conflicts least rather than where it arrived.

**This is the note's main experiment, not a result.** The sign is not automatic. Monad preserves a canonical order and merges sequentially, so an executor may schedule work independently of canonical adjacency; grouping conflicting transactions can expose a serial chain rather than improve parallelism; and interleaving disjoint transactions may help worker utilisation. **Moving a transaction also changes application outcomes and not only execution cost**, which for trades and liquidations is economically material and not a second-order effect.

Ethereum's serial execution is a comparison, but the earlier claim was too strong. Temporal movement there can still affect state access, caching, witness generation and block building. What is absent under serial execution is **the specific optimistic-retry channel**, which is what this hypothesis is about.

The predictor is the second limit. Monad cannot see conflict structure in advance, since access lists are optional in the inherited transaction model, so declared slack is usable only with one. Candidates are historical conflict rates per contract or account, a learned model, optional declared access sets, and **stream footprint stability**, which would be available from public history with no new field. Whether footprints are stable enough across a stream's members is measurable on Monad today and has not been measured.

### 14.2 The base-fee link, corrected

RN-26 finds that Monad's controller carries a variance term. Two corrections to how v0.2 stated it.

**The controller input is declared gas limits, not realised gas.** Per sec. 2, `block_gas` is the sum of transaction gas limits. The distinction runs in this note's favour: a stream's declared envelope interacts with the controller's actual input even when realised execution differs.

**A cadence declaration is not the same statistical quantity as the controller's moment.** It is a conditional forecast from one stream; the controller smooths an aggregate. TSP features are therefore **candidate predictors to evaluate against trend and moment**, not replacements for them.

One constraint is fixed. Letting declarations reach the controller makes the base fee depend on what senders choose, and RN-15 identifies making the base fee strategic as the regression to avoid. **A declaration may inform the controller only once it binds**, which is what sec. 9 is for, and a shadow comparison should precede any live coupling.

---

## 15. Simulation design

Every claim above stated as a hypothesis is settled by one of these, on RN-26's framework with a conflict model.

**Experiment 1, horizontal contention.** Class-aware allocation against fee-only ordering, at equal physical capacity under the default constraint of sec. 11. Report deadline success, cadence error and completed work. This is sec. 3's test and everything else is conditional on it.

**Experiment 2, orderings.** Compare arrival order, fee order, random order, predicted-conflict-aware order, perfect-information conflict-aware order, and class-aware movement across blocks. **Measure retries, wall-clock execution time, deadline success and changed application outcomes separately**, because a scheduling gain paid for in altered outcomes is not a gain.

**Experiment 3, footprint stability.** Group the historical transaction set by sender and target and measure how stable the read and write footprint is across a group's members. This decides whether sec. 14.1's predictor exists without a new field.

**Experiment 4, Lower Effort transfer.** Does an uncompensated residual class attract volume? Per sec. 8.3 this is the cheapest experiment and the one that could remove the case for a market.

**Experiment 5, class separation.** For each candidate class, does some service parameter exist whose experienced quality it is sensitive to and other classes are not? The measures differ by class: cadence error for Cadenced, deadline success for Bounded, completion for Residual. None is currently instrumented.

**Experiment 6, strategic declaration.** Does the derived mark survive a sender who shapes arrivals to stay in contract while timing the members that matter, or who splits one stream across addresses?

---

## 16. What this leaves open

1. **Whether contention is horizontal.** Experiment 1.
2. **Whether an expedited class is needed**, or whether a short deadline plus a cap represents it, per sec. 8.2.
3. **Whether a pre-market entitlement can be defined.** Without it, sec. 13's third variant is unavailable and Bounded and Residual stay scheduler inputs.
4. **Whether uncompensated yielding attracts supply**, per sec. 8.3, which would make a market unnecessary for that class.
5. **Whether a class market has useful depth**, given the state-dependence of sec. 13.
6. **Whether placement freedom improves completed work**, and at what cost in changed application outcomes. Experiment 2.
7. **Whether footprint stability supplies a predictor.** Experiment 3.
8. **How a stream is identified**, and the rest of sec. 9.3.
9. **What the default guarantee's constants should be**, and which of sec. 11's two forms to use.
10. **Whether class labels can be made verifiable** under sec. 10's constraint that candidate-set completeness cannot be checked.
11. **Whether the derived mark survives an adversarial sender.** Experiment 6.
12. **Whether any of this generalises** beyond Monad. Short blocks, optimistic parallel execution and a singleton state motivate it here; which is doing the work is not established, and across chains the boundary problem that limited DiffServ returns in full.

---

## 17. What comes next

**RN-34** takes the transaction level: the encoding, the window and role semantics, and the admission binding for a transaction belonging to no stream. **RN-35** takes the stream level: the rate contract, stream identity, the meter, and any two-leg market, which sec. 13 makes conditional on an entitlement RN-35 would have to define.

Both must support their conclusions by simulation on RN-26's framework including its conflict model, reported against RN-26's benchmark. A design claim about a parallel-execution chain that has not been run against a conflict-aware simulator is not evidence.

---

## References

- TLM Research Program. **RN-01: Temporal Execution Profile.** **RN-02: Protocol-Visible Temporal Abstraction.** **RN-04: Temporal Execution Services: A Multi-Class Execution Architecture for Ethereum.** **RN-06: Monad Through the Temporal-Liquidity Lens.**
- TLM Research Program. **RN-12: The Temporal Liquidity Market: A Conceptual Mechanism Design.** **RN-13 Part II: Capacity and Welfare in Blockchain Execution Systems.** **RN-15: A Temporal Liquidity Authorization for EIP-1559.** **RN-16: A Two-Leg Temporal Liquidity Reserve for EIP-1559.** **RN-26: A TLM Framework and Roadmap for Monad.**

Internet standards documents, with IETF status. The per-hop behaviours are standards track; the architecture, the markers and the workload mapping are informational.

- **RFC 2474** (standards track), Nichols, K., Blake, S., Baker, F. & Black, D. *Definition of the Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers.* December 1998.
- **RFC 2475** (informational), Blake, S. et al. *An Architecture for Differentiated Services.* December 1998.
- **RFC 2597** (standards track), Heinanen, J., Baker, F., Weiss, W. & Wroclawski, J. *Assured Forwarding PHB Group.* June 1999.
- **RFC 2697** (informational), Heinanen, J. & Guerin, R. *A Single Rate Three Color Marker.* September 1999.
- **RFC 2698** (informational), Heinanen, J. & Guerin, R. *A Two Rate Three Color Marker.* September 1999.
- **RFC 3246** (standards track), Davie, B. et al. *An Expedited Forwarding PHB.* March 2002.
- **RFC 4594** (informational), Babiarz, J., Chan, K. & Baker, F. *Configuration Guidelines for DiffServ Service Classes.* August 2006. https://www.rfc-editor.org/rfc/rfc4594.html
- **RFC 8622** (standards track), Bless, R. *A Lower-Effort Per-Hop Behavior (LE PHB) for Differentiated Services.* June 2019.

Monad architecture. Each fact used above is pinned in sec. 2 to one of these and to its date.

- Milionis, J. & Heimbach, L., Category Labs. **Redesigning a Base Fee for Monad.** October 2025. https://www.category.xyz/blogs/redesigning-a-base-fee-for-monad
- Monad Developer Documentation. **Asynchronous Execution.** https://docs.monad.xyz/monad-arch/consensus/asynchronous-execution
- Monad Developer Documentation. **Parallel Execution.** https://docs.monad.xyz/monad-arch/execution/parallel-execution
