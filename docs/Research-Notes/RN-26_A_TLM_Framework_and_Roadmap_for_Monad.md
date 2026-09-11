---
id: RN-26
title: "A TLM Framework and Roadmap for Monad"
subtitle: "Where temporal contention relocates under short blocks, and a roadmap for RN-33, RN-34 and RN-35"
version: "0.7"
status: "Working note - framework and roadmap. Conceptual; the specification is RN-33."
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-10"
license: "CC-BY-4.0"
---

# RN-26 v0.7

# A TLM Framework and Roadmap for Monad

## Where temporal contention relocates under short blocks, and a roadmap for RN-33, RN-34 and RN-35

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-26**  
**Version:** 0.7. Supersedes v0.2 through v0.6.  
**Architecture details current as of:** 10 September 2026, from Monad's published documentation.  
**Date:** 10 September 2026

---

## Abstract

RN-06 found that Monad performed the control and data plane decoupling, built an excellent data plane, and left the control plane thin: it computes a transaction order and a scalar fee and nothing else. This note establishes the frame for that control plane on Monad's own parameters and sequences the work that follows. RN-04 and RN-12 supply the programme-level discipline. It sets out where the contention sits, along which axes service can differ, what a second price would have to attach to, how a candidate would be judged, and what has to be simulated to judge it. **These are concepts rather than a specification**, and the specification is RN-33's work.

Four claims. Short blocks **relocate the temporal question outward**, since one Ethereum slot spans about thirty Monad blocks, so the intra-block dimension compresses while an inter-block dimension acquires resolution Ethereum cannot express. Parallel execution **erodes vertical differentiation**, because non-conflicting transactions execute concurrently and "earlier" thins as a service distinction. What remains is **horizontal**: contention over which class obtains capacity in a shared sub-block space, needing a price the priority fee does not supply. And a fine block time **does not remove temporal heterogeneity; it makes it resolvable while leaving it invisible to the protocol and the fee market**, because a twelve-second slot is a low-pass filter on demand, a 400-millisecond one is not, and Monad inherited Ethereum's envelope and scalar fee market either way.

Latency-sensitive traffic is not one class. It is heterogeneous on two independent axes: **in scale**, spanning three orders of magnitude within the urgency dimension alone, and **in requirement**, since being time-sensitive means value depends on execution time rather than that earlier is better, and deadlines, windows, cadence and dependencies are satisfied by placement rather than by haste. Both mechanisms therefore have material to work with here: **a crossing needs dispersion in the marginal value of earlier service, not a patient population**, and that dispersion is what a short block time makes visible. Which mechanism to build is a comparison of payoff against cost, not a structural precondition, and it is RN-33's question.

---

## 1. Starting point and framework

RN-06's architectural finding:

> Monad has already performed the decoupling. Deferred execution is a control and data plane split. Architecturally Monad is an SDN-era data plane running a pre-SDN control plane, one that computes a transaction order and a scalar EIP-1559 fee, but no classes, windows, reservations, or temporal differentiation.

It drew the networking lineage that names what such a plane computes, and closed on multi-timescale control: a slow global plane for capacity and policy, a fast local one for per-slot adaptation, a deterministic data plane kept out of the slow loops. It did not ask where Monad's own parameters put the contention.

Two notes supply the frame, neither Monad-specific.

**RN-04 gives the service-class discipline** from Internet QoS. Classes specify protocol-defined execution semantics rather than application identities; they stay coarse, few and stable; each must earn its place with a distinct demand cell *and* a distinct scheduler behavior; a class differing only in price belongs in the fee layer; admission needs a cost binding, or every transaction claims the best class and the classes collapse; the default class must remain untouched.

**RN-12 gives the two-sided mechanism**, in which flexibility is supplied, demanded, verified and cleared against a neutral baseline. A supplier is compensated only for surrendering a position it actually held, and establishing that baseline is the hardest prerequisite.

The two fail differently. Classes fail at marking, which is an economic problem. Crossing fails at the baseline, which is an institutional one.

---

## 2. The unit of time changes by a factor of thirty

Monad targets roughly 400-millisecond blocks against Ethereum's twelve-second slot, so one Ethereum slot spans about thirty Monad blocks. That ratio, not throughput, moves the problem.

**Inside the block, value compresses and the sign is unsettled.** Shorter blocks make latency and sub-slot placement more decisive, and also cut waiting time and the value of marginal priority. Which dominates depends on propagation delay against block interval, auction cadence, and finality, and RN-06 sec. 4(b) leaves it open. Either way, **this is the dimension where Monad and Ethereum differ least in kind and most in scale**, and where a mechanism designed for twelve seconds has least room.

**Across blocks, a dimension Ethereum cannot express acquires resolution.** A ten-second deadline is less than one Ethereum slot, so the protocol can represent it only as "this block or not." On Monad it spans twenty-five blocks, a schedulable interval with interior structure. Short blocks do not merely subdivide the existing question; they make an inter-block question expressible that Ethereum's slot time collapses, at the timescale applications reason in.

**The stream becomes the primary demand object.** At 2.5 blocks per second a transaction's profile is thin, being which of the next several blocks is acceptable, while rate, cadence, jitter and burstiness have many samples per second. **On Monad, TSP is the primary representation and TEP is the member-level detail**, which reverses the programme's development order.

---

## 3. Parallel execution erodes vertical differentiation

Ethereum executes serially, so position is a total order and "earlier" is always exclusive and meaningful.

Monad executes optimistically in parallel and commits in canonical order. Two transactions touching disjoint state are, in the dimension a user cares about, simultaneous. Order still determines the committed result and extraction opportunities, but as a *service* distinction between non-conflicting transactions it thins.

What does not thin is conflict structure. RN-06 sec. 2.3: the singleton ledger means all demand contends on one shared state, so throughput is bounded by the workload's conflict structure rather than only by implementation speed, and optimistic execution discovers conflicts after ordering rather than removing them.

Service outcome is therefore determined by three things in descending importance: whether the transaction is in the block, whether it conflicts with what else is there, and where it sits in the order. **Ethereum's temporal market prices the third. Monad's contention lives in the first two.**

---

## 4. Horizontal differentiation

**Vertical** differentiation is by position in time: a total order over a shared queue, which is what a priority fee prices and what RN-15 trades. **Horizontal** differentiation is by type of service over a shared sub-block space: which class obtains capacity, under what guarantee, with what cadence. The partition runs across the substrate rather than along it, and the classes need not be ranked against each other at all.

**Why contention lands horizontally.** Section 2 compresses vertical value without eliminating it; section 3 weakens vertical position as a service distinction; RN-06 sec. 2.3 shows conflict structure binding instead. The scarce thing is then capacity within a class and freedom from conflict, not the front of the queue. A burst of trading traffic that fills a block crowds out oracle updates and payments **regardless of how the block is ordered**, because those classes are not competing for position but for room.

**Hypothesis, not resolved here: on a fast parallel chain over a singleton state, the binding temporal contention is horizontal rather than vertical.** It is falsifiable. If value differences between positions within a block are large relative to differences between classes of admitted work, the hypothesis fails and an RN-15 analogue is the right instrument. Section 8 gives the test.

**The networking precedent is exact and RN-06 already named it.** Slicing is horizontal differentiation: a slice is a share of a substrate with its own guarantee, not an earlier place in a queue. GMPLS is horizontal across granularities. DiffServ classes are horizontal by construction, which is why admission control at the edge, not ordering in the core, is what made them work. RN-06 offered slicing as one item in a lineage; sections 2 and 3 argue it is the item the architecture selects.

**The second price.** A priority fee prices vertical position and cannot express how much of the substrate a class holds or who may enter it. A horizontal design needs a second price alongside it, not instead of it. Two inherited constraints: it must attach to a distinct scheduler behavior, or it is a fee-layer distinction wearing a service-layer label; and it must bind, since a costless class declaration is gamed immediately, which makes the second price also the admission control. What it attaches to is RN-33's question.

---

## 5. Latency-sensitive is not one class

### 5.1 A fine block time resolves heterogeneity; the protocol and the fee market still do not see it

Speed does not remove the problem. Three things are distinct:

- whether the heterogeneity **exists** in the demand;
- whether the block interval is fine enough for it to be **resolvable** rather than aliased;
- whether it is **visible to the protocol and the fee market**, so that a sender can declare it and a scheduler can act on it.

On Ethereum every timing distinction finer than twelve seconds is unresolvable at protocol level. A transaction needing execution within 50 milliseconds and one needing 8 seconds send identical messages and receive identical treatment. **The slot time is a low-pass filter on temporal demand**, and all structure below it is aliased into a single bid.

At 400 milliseconds much more of the spectrum survives the sampling:

```text
order-book quote and cancel      microseconds
arbitrage against a moving price sub-block, under 400 ms
liquidation                      one to a few blocks, around 1 s
funding and oracle update        seconds
settlement and reconciliation    minutes
```

Six or seven orders of magnitude, of which Ethereum's slot renders roughly the top four indistinguishable.

**Monad has this temporal heterogeneity. It is visible in neither the protocol nor the fee-market design.** The demand is there and the block interval is fine enough to resolve it, but Monad inherited Ethereum's transaction envelope and its scalar fee market, so a sender still cannot declare a requirement and the scheduler still cannot act on one.

Monad therefore has **more resolvable structure and the same protocol and fee market**, which widens the gap between what the demand contains and what either can see. That gap is RN-06's missing control plane.

### 5.2 Heterogeneous on two axes

RN-06 sec. 3.2 found Monad's roster concentrated in latency- and throughput-sensitive trading, meaning concentration of activity and value rather than of the directory. **That describes which application categories are active. It does not describe their temporal requirements.**

A chain populated entirely by trading applications is heterogeneous on two independent axes.

**Heterogeneous in scale.** Within the urgency dimension alone, requirements span the range in sec. 5.1: microseconds for quote and cancel, sub-block for arbitrage, about a second for liquidation, seconds for funding and oracle updates, minutes for settlement. Three orders of magnitude of dispersion sit inside what a twelve-second slot renders as a single bid.

**Heterogeneous in requirement.** Urgency is one dimension among several. **Time-sensitive does not mean speed-seeking.** That value depends on execution time says nothing about the shape of the dependence:

- value decaying continuously with delay, as for an arbitrage;
- a deadline cliff, where every time before the bound is equivalent and after it the value is zero;
- a window with an earliest bound as well as a latest one, since RN-01's profile carries both, and a transaction landing before its precondition holds is not early but wrong;
- a cadence requirement, where regular spacing matters more than latency and jitter is what hurts;
- an ordering dependency, where the requirement is to follow something rather than to precede everything.

Only the first is "wants to be fast." The rest are satisfied by placement rather than by haste, and two of them can be harmed by early execution, since landing early exposes intent and invites the extraction the sender was avoiding.

Two assumptions fail here: that latency-sensitive demand is one class, and that being time-sensitive means wanting to be first. Both are artifacts of observing this demand only through a twelve-second filter that renders every sub-slot requirement as the same bid.

### 5.3 Dispersion, not opposition, is what a crossing needs

A roster concentrated in latency-sensitive trading can still supply the flexible side of a two-sided market, for two reasons.

First, much of this demand is not speed-seeking (sec. 5.2). A deadline, a window, a cadence or a dependency is a constraint on placement, and a transaction meeting it has no use for the positions it does not need. Flexibility is not something such a sender has to be persuaded into; it is what the requirement already permits.

Second, and this holds even for the part that does want to be fast: **a crossing requires dispersion in the marginal value of earlier service, not a sign change.** If one transaction loses most of its value within 400 milliseconds and another loses a few per cent, the second can supply flexibility to the first while both remain, in any ordinary sense, urgent. The compensation the second requires is small relative to what the first will pay, so there are gains from trade. Nothing in the construction needs a patient counterparty in absolute terms; it needs someone whose marginal value of earlier service is lower, and "lower" is a relative statement within whatever distribution exists.

The dispersion Ethereum cannot resolve is the dispersion a crossing would trade on, so a chain that resolves three orders of magnitude of it may have **more** gains from trade available, not fewer.

RN-01 and RN-02 treat execution priority, delay tolerance, windows and deadlines, predictability and continuity as independent dimensions, and a stream profile carries all of them. "All urgent" is a one-axis summary of a multi-axis object.

The demand shape therefore does not select the mechanism. **Payoff against cost does**: for a crossing, the gains scale with dispersion and with how often both sides co-occur in a window, against the baseline and settlement costs of secs. 1 and 7; for horizontal classes, the gains scale with how separable service requirements are and how much conflict reduction separation buys, against class design, admission control, the second price, and a thicker control plane. Neither comparison follows from the demand distribution alone. Section 4's hypothesis rests on the architecture, not on this section.

---

## 6. The demand a fast chain could host

A market does not require these populations (sec. 5.3). They would widen the dispersion it trades on and add axes it can differentiate along, and Monad's EVM compatibility makes two large flows portable in principle.

**Ethereum's patient, high-value work.** Treasury operations, vault rebalancing, collateral management, net-asset-value calculation, reconciliation, governance execution, large-value settlement. Value-dense and deadline-tolerant: it must happen correctly within an interval and gains little from being early. It sits on Ethereum for security, liquidity and institutional acceptance rather than execution characteristics.

**Tron's payment flow.** High count, low unit value, wide admissible windows. RN-14 treats Tron as a candidate payment case, and the classification remains a hypothesis pending direct stablecoin-transfer data.

Parallel execution suits both structurally: payment transfers largely touch disjoint state, which is the workload optimistic execution handles best, and patient work can be placed where it conflicts least because it does not need a particular position. A class-based design should include one shaped for this: **settled within a bounded window, no ordering guarantee, low price, high assurance.** It earns its place under RN-04 because both its demand cell and its scheduler behavior are distinct.

A wider demand distribution raises the payoff of both mechanisms, and neither is blocked by the current mix. **The mix sets the size of the gain, not whether a mechanism is possible**, which is what sec. 9's sweep over traffic composition measures.

**Network effects.** They accrue to the venue that hosts the most heterogeneous demand simultaneously without one class degrading another. Ethereum cannot differentiate, so its classes interfere: RN-14 sec. 11 identifies the peak base fee, not the tip, as what excludes low-value payment traffic during congestion, which is one class priced out by another's burst. The claim is not that throughput wins. **Throughput is necessary and not sufficient, and differentiation is the missing term.**

Four counterarguments have force. Solana and Tron are the natural experiment: both have had throughput for years without displacing Ethereum's capital. Network effects are self-reinforcing and capital is sticky for reasons outside execution entirely. RN-14's evidence does not identify causality and says so. And RN-06 sec. 4(g) notes that EVM-equivalence is a strategic ceiling as well as a feature, so **the property that would let Monad attract Ethereum's traffic cheaply is the property that obstructs the differentiation layer**. A temporal layer lives in the transaction envelope and the scheduler rather than in bytecode semantics, so this is resolvable, but it constrains how such a layer could be introduced.

The argument is a conditional to test, not a prediction.

---

## 7. Deferred execution constrains where a mechanism can settle

Monad decouples agreement from state computation. A block proposal carries no state root, each block carries a delayed Merkle root as a consistency check, and execution lags consensus by a fixed number of blocks, documented as k = 3.

Settlement depending only on the committed order, such as class assignment or delivery of a position, is decidable when consensus completes. Settlement depending on realized gas is decidable only k blocks later, so such a mechanism must hold state across the lag.

RN-15's provider side is of the second kind, since its subsidy is a rate applied to consumed gas. **The block-local property that makes RN-15 minimal on Ethereum is therefore unavailable on Monad.** RN-06 sec. 4(d) notes that deferred execution moves a cost rather than removing it, and this is one place the cost lands. RN-06 sec. 4(e) notes that charging on declared rather than consumed gas is a pricing distortion; for a temporal mechanism it is also a convenience, since a declared quantity is available at consensus time.

---

## 8. Benchmark

Raw throughput fails twice here. RN-13 Part II shows utilization alone is insufficient anywhere. And under optimistic parallel execution, achieved throughput is a function of the workload's conflict structure, so **a TPS figure describes the benchmark workload as much as the chain, and workload shaping moves it directly.** Throughput cannot be the independent variable against which workload shaping is judged.

The benchmark is a frontier reported at a fixed reliability vector. Monad-specific rows are marked.

| Dimension | Measure |
|---|---|
| Admitted demand | requests and gas admitted, by temporal class and application type |
| Deadline service | satisfaction rate per class, delay distribution, expiry before inclusion |
| **Effective parallelism** | conflict rate, speculative aborts, re-execution work, achieved speedup |
| Physical utilization | resource use against limits, including multidimensional constraints |
| Economic incidence | payment by class, second-price revenue, validator revenue, burn |
| Fee behaviour | level, variance, predictability, burst response, recovery |
| Lost demand | expired, cancelled, abandoned and outside-option demand by class |
| Neutral-class protection | outcomes for transactions declaring nothing, against the pre-mechanism baseline |
| Extraction | realized extraction, sandwich incidence, private-order-flow share |
| **Settlement lag effects** | outcomes displaced by k blocks, and strategies exploiting the displacement |
| Access | distribution of service across senders; entry cost for small participants |
| Protocol cost | state, computation, bandwidth, verification, complexity |

Two reporting rules. The neutral class is a constraint rather than a metric to trade against: a scheme that improves aggregate service while degrading transactions which declared nothing fails RN-04's neutrality requirement whatever else it achieves. And gains must be net of the re-execution that reordering caused, which is accounting RN-15 does not need and Monad does.

---

## 9. Simulation framework

A simulator representing capacity as a scalar gas pool is adequate for Ethereum and useless here, because under optimistic parallel execution capacity is a function of the conflict graph. **The simulator must model state access and conflict.** The existing TLM simulations do not, so that is the first thing to build.

**Traffic types**, spanning the timescale range of sec. 5.1 and the conflict range of sec. 3:

| Type | Rate | Value horizon | State access |
|---|---|---|---|
| Order-book quote and cancel | very high, continuous | microseconds | hot, concentrated |
| Arbitrage | event-triggered bursts | sub-block | hot AMM pools |
| Liquidation | event-triggered | one to a few blocks | collateral and oracle state |
| Oracle update | periodic | urgent and derived classes differ | hot, widely read |
| Payment transfer | high count | wide window | largely disjoint |
| Patient high-value | low | minutes | moderate |
| Background maintenance | low | none within horizon | varied |

The mix is a parameter and must be swept, not fixed: results under the current urgent-heavy roster and under a mix including sec. 6's populations are different experiments and both are needed.

**Models.** Arrivals should include Poisson for accounting checks only, regime-switching for quiet and congested states, self-exciting processes for cascades, periodic processes for oracle cadence, and common-shock arrivals that make several types burst together, which is the case that matters and that independent processes miss. State access must be drawn with hot-key skew rather than uniformly, since a uniform model assumes the problem away; the skew parameter should be calibrated, not chosen. Execution is simulated optimistically with re-execution, so throughput is endogenous, and settlement carries the k-block lag.

**Comparison set.** RN-06 sec. 3.1 already specifies the core experiment and it has not been run: one ordered stream, conflict-aware scheduling, temporal classification, and joint scheduling. **Comparing classification against conflict-aware scheduling isolates the temporal contribution from the state-partitioning one.** Without that pair the result cannot be interpreted. Add current fee priority as status quo and an oracle allocation over simulated private values as a non-implementable upper bound.

**Calibration.** Monad traces give real access patterns and the current mix; Ethereum traces replayed at 400 ms give a mix containing the patient populations but the wrong latency expectations; synthetic traffic gives control at the cost of realism. No single source supports a welfare claim, so the first output should be a sensitivity analysis over all three.

---

## 10. Roadmap

This note fixes the frame: where contention sits (secs. 2 to 5), what demand the chain could host (sec. 6), what constrains settlement (sec. 7), how a candidate is judged (sec. 8), and what must be simulated (sec. 9). The conceptual material is here, including the two axes of sec. 4, the constraints on a second price, and the class shape sec. 6 argues for. What is not here is a specification: no class set is fixed, no price rule is chosen, no baseline is selected, no encoding is given. Three notes follow, each with a different burden of proof.

**RN-33, a conceptual mechanism with benchmark analysis.** The counterpart of RN-12's role for Ethereum, fixing objects rather than encoding: what the horizontal classes are and what makes them distinct in scheduler behavior; what the second price attaches to and what makes it bind; how the neutral default is protected; whether a vertical component is retained and what it trades; and what baseline a Monad crossing would need. It states which of RN-04's discipline and RN-12's crossing the architecture selects, which sec. 4's hypothesis and sec. 9's experiment settle.

RN-33 also carries the benchmark. Section 8 says what has to be measured; RN-33 applies it, comparing candidate designs against the frontier and against each other before any encoding is fixed. Section 6's application question enters as a sensitivity rather than a precondition, since the traffic mix changes the size of the gain and not whether a mechanism is possible.

**RN-34, a transaction-level mechanism, with simulation.** A TEP-based design over the near-block horizon: bounded windows, roles, admission binding, and sec. 7's settlement constraint. The instrument for the three-to-twenty-five-block range where sec. 2 says resolution now exists, and deliberately not an RN-15 port. **Its conclusions must be supported by simulation on the sec. 9 framework**, including the conflict model, since a design claim about a parallel-execution chain that has not been run against a conflict-aware simulator is not evidence.

**RN-35, a stream-level mechanism, with simulation.** A TSP-based design, which sec. 2 argues is the primary representation here rather than a long-horizon extension. Cadence, rate envelopes, recurring service, reliability classes. The oracle and order-book cases are both stream problems, and they are the two workloads the roster actually contains. **Its conclusions likewise rest on simulation**, and the stream case additionally requires the arrival models of sec. 9, since cadence and burst structure are the object under study rather than a background assumption.

The simulator of sec. 9 is therefore built for RN-33 and used by all three.

---

## References

- TLM Research Program. **RN-01: Temporal Execution Profile.** **RN-02: Protocol-Visible Temporal Abstraction.** **RN-04: Temporal Execution Services.** **RN-05: Supply-side Heterogeneity and Temporal Granularity.** **RN-06: Monad Through the Temporal-Liquidity Lens.**
- TLM Research Program. **RN-12: The Temporal Liquidity Market: A Conceptual Mechanism Design.** **RN-13 Part II: Capacity and Welfare in Blockchain Execution Systems.** **RN-14: The Demand Ethereum Does Not Serve.**
- TLM Research Program. **RN-15: A Temporal Liquidity Authorization for EIP-1559.** **RN-16: A Two-Leg Temporal Liquidity Reserve for EIP-1559.** **RN-17: Temporal Service Profiles and Future Execution Tickets.**
- TLM Research Program. **RN-33, RN-34, RN-35:** in preparation, per sec. 10.
- Monad Developer Documentation. **Asynchronous Execution.** https://docs.monad.xyz/monad-arch/consensus/asynchronous-execution
- Monad Developer Documentation. **Parallel Execution.** https://docs.monad.xyz/monad-arch/execution/parallel-execution
- Monad Foundation. **How Monad Works.** https://monad.xyz/blog/how-monad-works
- Category Labs. **Monad Initial Specification Proposal, Version 2.0.1.** https://category-labs.github.io/category-research/monad-initial-spec-proposal.pdf
