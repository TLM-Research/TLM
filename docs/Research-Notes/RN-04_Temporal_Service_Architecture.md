---
id: RN-04
title: "Temporal Execution Services: A Multi-Class Execution Architecture for Ethereum"
version: "0.2"
status: "@draft — internal; Monad/Hyperliquid facts pending verification before public release"
program: "Temporal Liquidity Market (TLM)"
date: "July 23, 2026"
---

# RN-04: Temporal Execution Services

## A Multi-Class Execution Architecture for Ethereum

---

## Positioning

RN-01 introduced the transaction-level representation of temporal demand (the Temporal Execution Profile). RN-02 argued that temporal characteristics deserve protocol-visible, verifiable representations. RN-03 established empirically, through Hyperliquid, that economically important demand has multidimensional temporal structure that spot fee markets under-represent. All three are **demand-side** notes.

RN-04 is the **supply-side** companion. It asks the architectural question:

> **Should Ethereum continue to offer a single execution service, or evolve toward a small portfolio of protocol-native *temporal execution services*?**

Per the TLM two-phase framing, this is a **Phase-2 design-space exploration**: it maps candidate service portfolios and their constraints, states the hard problems honestly, and offers one concrete design sketch for evaluation against the Foundation's criteria. It does not propose that Ethereum adopt any particular architecture.

RN-04 and **RN-05** are companion supply-side notes at different layers: RN-05 supplies the *coordinate substrate* (the quantum lattice — the finest resolution at which ordering commitments can be expressed, read at varying depth); RN-04 supplies the *execution semantics* — service classes layered on that substrate. Where this note speaks of sub-slot service (§8), the underlying coordinate system is RN-05's lattice.

---

## Abstract

Ethereum offers one temporal execution product: *inclusion in the next available block, ranked by fee*. This uniform model has enabled a rich ecosystem, but it forces fundamentally different workloads — token transfers, DEX swaps, market making, oracle updates, liquidations, recurring settlements, rollup commitments — into the same execution service, and it is a major reason continuous, latency-sensitive applications exit to specialized Layer-1s.

This note explores an alternative to both universal acceleration ("make every transaction faster") and application exit ("leave for an appchain"): a small portfolio of **temporal execution services**, differentiated by the dimensions of Temporal Liquidity — delay tolerance, execution priority (ordering sensitivity), execution windows and deadlines, predictability, and continuity — sharing one decentralized settlement layer.

Two contributions anchor the note. First, the **service-portfolio thesis**: temporal differentiation, rather than uniform acceleration, may be the more scalable path to expanding Ethereum's serviceable application space. Second, the **workload-shaping hypothesis**: classifying demand into temporal services *before* scheduling increases the parallelism available to any execution engine and reduces contention — a systems-performance argument for temporal classification that is independent of the economic one. A case study of Hyperliquid's extraction-resistant architecture and a design sketch for a sub-slot continuous execution lane make the thesis concrete.

---

# 1. The Thesis: Differentiation, Not Just Acceleration

Most Ethereum performance discussion concentrates on making the single service faster: shorter slots, faster consensus, faster networking, faster execution engines. These efforts improve all applications uniformly — and preserve the assumption that one execution service fits all.

TLM's demand-side results suggest the assumption is wrong. Workloads differ not only in willingness to pay but in delay tolerance, ordering sensitivity, windows and deadlines, predictability, and continuity — and these differences are *structural*, not marginal. A single service must be provisioned for the most demanding workload while pricing out or under-serving the rest; the observable consequence is the migration of continuous, latency-sensitive applications (perpetual exchanges, market making, oracles) to specialized chains.

The alternative explored here:

> Instead of one service made uniformly faster, offer a **small portfolio of execution services**, each defined by temporal execution semantics, all settling on the same layer.

This reframes the scaling question from *"how fast can the one service be?"* to *"how many kinds of demand can the platform serve well?"*

---

# 2. Candidate Service Classes

Service classes are defined over the canonical dimensions of Temporal Liquidity — never by application identity. Each class corresponds to a demand cell RN-03 identified, and each implies a distinct builder behavior, which is what justifies its existence (see the minimality principle, §4.3).

| Service class | Defining temporal profile | Demand cell (RN-03) | Example workloads | Characteristic builder behavior |
|---|---|---|---|---|
| **Continuous State** | high continuity, high predictability, low delay tolerance, high ordering sensitivity | predictable & delay-intolerant | market making, oracle updates, liquidation management | repeated intra-slot execution, deterministic sequencing, bounded jitter, fast cancel/update |
| **Protected Window** | bounded delay tolerance, high ordering-*protection* need | moderate patience, extraction-exposed | DEX swaps, intent settlement, large trades | execution anywhere within a declared window, protocol-constrained ordering (e.g. batch semantics) |
| **Scheduled** | high delay tolerance to a deadline, high predictability, low ordering sensitivity | predictable & patient | rollup commitments, treasury operations, periodic settlement | deadline-honoring placement, off-peak packing |
| **Best-Effort** | undeclared | residual / spot | everything else | today's fee-ranked inclusion, unchanged |

Two structural notes. **Best-Effort is the undeclared default** — participation in any other class is voluntary, so a privacy-preserving path always exists (no one is forced to disclose a temporal profile). And the classes deliberately mirror the **declared/observed split**: Protected Window is entered by *declaration* (a window is a stated preference), while Continuous State and Scheduled are naturally entered by *verified observation* (continuity and predictability are measurable from realized behavior — see §5.2).

---

# 3. Completing the Two-Sided Market

The corpus now has all three layers of a market design, and RN-04 is the missing supply side:

```
Demand side (RN-01/RN-02):  applications describe temporal demand
                            (TEP per transaction; TDP per stream)
                                        │
Pricing layer:              fees match demand to services
                            (tiered/urgency pricing — Kiayias et al.;
                             reservation/term-structure pricing for
                             committed classes)
                                        │
Supply side (RN-04):        the protocol offers temporal execution
                            services; builders implement class
                            semantics; one settlement layer
```

The economic-layer precedent already exists: Kiayias, Koutsoupias, Lazos & Panagiotakos's tiered fee mechanism prices urgency classes and shows inclusivity need not sacrifice revenue [6]. Their tiers are the *fee-side* of exactly this architecture — differentiated pricing without differentiated execution semantics. RN-04 supplies the execution-side counterpart, and inherits their caution (§5.1).

---

# 4. Architectural Principles

## 4.1 The DiffServ discipline

Classes specify **protocol-defined execution semantics, not application identities** — the protocol defines the service; builders remain free to optimize within it. This is the surviving lesson of Internet QoS: coarse, stateless class behaviors deployed; rich per-flow reservation did not [7, 8]. RN-02's caution carries over unchanged: DiffServ's classes held only where marking was policed — which is why admission (§5.2) is load-bearing, not optional.

## 4.2 From store-and-forward to streaming

Current execution is a store-and-forward pipeline — mempool, builder, bundle, proposer, execution — in which transactions are repeatedly buffered, examined, and reordered. Every buffer is both a latency stage *and* a strategic-reordering opportunity: the performance problem and the MEV problem are the same picture.

```
today:      User → Mempool → Builder → Bundle → Proposer → Execution
explored:   Temporal descriptor → Admission → Reservation → Execution → Settlement
```

The transferable principle (from pipelined and reservation-based systems generally): *decide once, near where the decision is needed, and keep execution flowing* — reserve before streaming, rather than re-adjudicating every transaction at every stage. Streaming does not mean one pipeline: each service class may define its own flow into the shared settlement layer.

## 4.3 The minimality principle

The portfolio must stay **small, coarse, and stable** — three to five classes. Each class must earn its place with a distinct demand cell *and* a distinct builder behavior; a class that differs only in price belongs in the fee layer, not the service layer. This is the IntServ lesson stated as a design rule, and it is the note's answer to "why not a class per application?"

---

# 5. Hard Problems (First-Class, Not Afterthoughts)

## 5.1 Class choice is disclosure

Selecting a service class *reveals temporal preference* — exactly the observability attack surface identified against urgency tiers: the class marker is visible, and adversaries can trade against it (front-run the patient, target the window). Any service architecture must therefore be evaluated on **extraction-resistance**, using the three families of §6.3: architectural (remove the window), cryptographic (hide the content), economic (make exploitation unprofitable). Class granularity matters here too — coarser classes leak less.

## 5.2 Admission needs a cost binding

Without policing, every transaction claims the best class and the classes collapse — DiffServ's marking problem, RN-02's central diagnosis. The defenses are inherited: **stake-backed declarations, verification against realized behavior, and penalties for divergence**. The observed-property classes (Continuous State, Scheduled) admit a cleaner solution: membership can be *derived from verified history* rather than declared — an application earns the class by demonstrably behaving like it. Declaration-based classes (Protected Window) need the economic binding.

## 5.3 Cross-class capacity allocation

Blockspace allocated to classes is a coupled system: over-provisioning a committed class starves Best-Effort; strategic actors will arbitrage price differences across classes; and reserved-but-unused capacity is deadweight. Requirements: a **reserved-headroom cap** for urgent spot demand, **no-arbitrage coherence** between class prices (the term-structure discipline), and deterministic, aggregate-state-driven allocation rules (base-fee-style neutrality, no discretion).

## 5.4 Neutrality under classes

A protocol-recognized fast class is a blessed fast lane, and the production record (Timeboost) shows how such lanes centralize [10]. Defenses: admission by verified behavior rather than payment where possible; no bidding inside classes whose semantics forbid it; identical class rules for all participants; differentiation across *time and class semantics*, never across identity.

## 5.5 Does classification reduce MEV, or concentrate it?

Both outcomes are plausible: batch semantics and FIFO-within-class remove some extraction channels, but predictable class membership creates new targeting information. This is an open, evaluable question — under the Foundation's criteria and the TFM apparatus (DSIC/MMIC/OCA-proofness; the Chung–Shi impossibilities bound what plain mechanisms can achieve, and the cryptographic escape hatch applies [4, 5]).

---

# 6. Case Study I — Hyperliquid: Extraction-Resistance by Architecture

*(Companion to RN-03, which studied Hyperliquid's demand side; here we study its supply-side answer. Vendor-sourced specifics pending verification.)*

## 6.1 What Hyperliquid does

Hyperliquid structurally removes each window in which front-running normally operates: **no public mempool** (order flow routes directly to validators — kills the visibility window); **HyperBFT with ~200ms blocks and single-block deterministic finality** (a trade settles in the block it is placed — kills the time window); **no fee-priority bidding — pure price-time priority / FIFO** (kills the fee channel for ordering discretion); **protocol-native liquidations** (the clearinghouse liquidates internally — internalizes an adversarial workload, eliminating keeper gas wars); and **mark-price triggers from a median of external venues** (externalizes the reference truth against local-book manipulation) [9].

## 6.2 The critical reading: priority is re-denominated, not eliminated

"Front-running cannot happen" is too strong — and the way it fails is the lesson. With the fee channel closed and FIFO in force, *arrival time* is the only route to priority, so competition migrates from gas bids to **latency**: colocation, network engineering, speed — the classical HFT equilibrium, and precisely the wasteful latency race of Capponi & Zhu [11]. And "no public mempool" does not make flow invisible; it makes it visible *only to a small validator set* — trust relocated, not removed.

> **The execution-priority dimension cannot be designed away. A system only chooses the currency in which priority is allocated — and therefore who its rent-seekers are.**

Three regimes now run in production:

| Regime | Example | Priority allocated by | Characteristic failure |
|---|---|---|---|
| **Permit** | Ethereum priority fees / PGAs | fee bidding | MEV, sandwich attacks |
| **Price** | Arbitrum Timeboost | explicit auction | spam & centralization [10] |
| **Prohibit** | Hyperliquid FIFO | physical latency | colocation arms race; centralization |

No regime escapes the dimension. This comparison becomes visible only once execution priority is named as a demand characteristic — it is a product of the TLM framing itself.

## 6.3 A third family of extraction-resistance

The corpus already carried two answers to the disclosure problem: **cryptographic** (hide the information until it is unexploitable — encrypted mempools, commit-reveal; the Shi–Chung–Wu line [5]) and **economic** (make misuse unprofitable — stake, verification, collusion-proofness). Hyperliquid demonstrates the third: **architectural** — remove the structural windows themselves. The families are complementary, and *service classes are the natural unit at which to mix them*.

## 6.4 What the architecture costs

Hyperliquid pays in **decentralization and neutrality budget**: order flow trusted to a small validator committee; FIFO's latency competition concentrating geography and capital; sub-second BFT finality over a small set trading off open participation; an oracle dependency in the protocol core. A purpose-built venue may rationally pay these costs. Ethereum's constraint set is exactly what refuses to pay them — so the productive question is:

> **Which of Hyperliquid's architectural moves can be imported *per service class*, at what decentralization cost — and which windows must instead be closed cryptographically or economically?**

That question has a concrete affirmative answer for one class — §8.

---

# 7. Case Study II — Monad: The Workload-Shaping Hypothesis

*(Facts pending verification against Monad documentation [12, 13].)*

## 7.1 Where Monad sits

Monad improves nearly every layer *below* the transaction market — consensus (MonadBFT), networking (RaptorCast), execution (asynchronous pipelining, optimistic parallel execution), storage (MonadDB), VM (JIT compilation) — while deliberately preserving Ethereum's semantics: one linearly ordered transaction stream, executed faster, with results committed in the original order.

Monad asks: *how do we compute the ordered result faster?*
TLM asks: *should every transaction receive the same execution service at all?*

```
Application
   ↓
Temporal demand  →  service selection      ← TLM (above the market)
   ↓
Transaction ordering
   ↓
Execution engine                            ← Monad (below the market)
   ↓
Storage / Consensus
```

Different layers; complementary, not competing. A Continuous State service could *use* a Monad-class engine inside it: **TLM selects the service; an engine like Monad accelerates execution within it.** Service-to-engine need not be one-to-one.

## 7.2 The workload-shaping hypothesis (headline contribution)

Monad discovers parallelism *after* ordering — optimistic execution against one ordered stream, validating dependencies afterward. TLM can act *before* ordering:

> **Classifying demand into temporal services before scheduling increases the parallelism available to any execution engine and reduces contention — regardless of which engine runs inside each service.**

In database terms: Monad improves the **concurrency-control algorithm**; temporal classification changes the **workload presented to it**. Separating a high-rate, conflict-heavy continuous stream (own state domain, own cadence) from spot traffic removes cross-class conflicts *by construction* rather than discovering them optimistically.

This is a systems-performance argument for temporal classification that is **independent of the economic argument** — and it is quantifiable:

> **Proposed experiment (simulator headline).** Replay a historical or synthetic transaction mix through (a) one ordered stream and (b) temporally classified streams; measure state-access conflict rates and achievable parallel speedup under an optimistic-execution model. A material difference validates the hypothesis; none falsifies it.

---

# 8. Design Sketch — A Sub-Slot Continuous Execution Lane

*(One concrete point in the design space: the Continuous State Service instantiated. Offered for evaluation, not adoption.)*

## 8.1 The design

*This lane is a **sub-channel of the quantum lattice** developed in RN-05, read at an illustrative 200ms depth. RN-05 supplies the coordinate substrate (the partial order across sub-slot quanta, verifiable ordering, and the fineness argument); this section supplies one worked service on it. The 200ms figure is illustrative — chosen to match the Hyperliquid cadence the lane imports — not a design constant; RN-05 §4.3 is the reason the quantum size is an empirical question rather than a fixed number. Note also (RN-05 §4.4): the lane's FIFO is **interior order purchased at a verification cost** — free-interior classes (e.g. Protected Window, via batching) avoid that cost; this lane pays it, which is what Problem P1 below is about.*

Subdivide Ethereum's 12-second slot into sub-slot snapshots — for illustration, **60 snapshots of 200ms** — and offer **one protocol-recognized virtual lane** with Hyperliquid-style semantics inside it:

- **sub-slot cadence** — lane operations (place, cancel, modify, match) take effect at each 200ms snapshot;
- **price-time priority (FIFO)** within the lane — no fee-priority bidding;
- **no public queue** for lane operations — flow visible only to the lane's sequencing role;
- **clearinghouse-style segregated state** — escrowed balances, native matching semantics, **net settlement to shared L1 state at each slot boundary**.

Consensus, settlement, assets, and all other classes remain unchanged. The lane serves RN-03's *predictable-but-delay-intolerant* cell — on-chain order-book market making — inside the tent rather than on a sovereign chain.

### The 200ms beat: state-update checkpoints

The lane's cadence has a clean systems reading: **each quantum is a state-update checkpoint** for the service's continuous state. An order book does not need a fresh guarantee per transaction; it needs its state — quotes, cancels, fills, margin — to advance and commit on a regular beat. The lane provides exactly that: the book steps forward every quantum and net-settles to L1 at the slot boundary. This is the natural rhythm of the **Continuous State** class specifically — the **Protected Window** class does not want a per-quantum beat at all; it wants a bounded window with a free (batched) interior. The 200ms beat is a property of *one class*, not of the lane architecture in general.

Two distinctions keep the framing honest and connect the lane to adjacent work.

- **Forward-commitment checkpoint vs durable-state checkpoint.** A preconfirmation (Chainbound's Bolt, Primev's mev-commit) is a *forward* checkpoint — a credible *promise* about a future transition, still soft until the slot commits. A classical systems checkpoint is a *durable* saved state. The lane's quantum is the former until slot finality: a 200ms fill is a bonded promise, not yet irrevocable state (this is Problem P2, soft finality). Single-slot finality collapses the gap between the two.
- **Convergence with production, with one architectural difference.** Primev's mev-commit already runs a 200ms commitment beat — 60 per Ethereum slot — the same cadence proposed here (RN-05 §7). But mev-commit runs a *separate fast chain* for that beat (its own consensus); this lane seeks the same beat as a **sub-channel of the L1 lattice** (RN-05), settling natively at the slot boundary rather than on a coprocessor. Same beat; different substrate.

## 8.2 What the lane inherits from the framework

- **Admission (RN-02, §5.2):** earned by observed, verified continuous flow, backed by stake — derived membership, blunting misclassification and reducing what must be *declared*.
- **Pricing (term structure):** FIFO forbids priority fees inside the lane, so capacity is naturally sold as **reservation at posted, deterministic forward rates** — while Best-Effort remains the spot market. The lane is the natural first application of forward-priced blockspace.
- **Extraction-resistance (§6.3):** all three families composed — architectural (no public queue, FIFO, sub-slot cadence), economic (staked admission, slashable sequencing commitments), cryptographic (where architecture cannot close a window — P1 below).
- **Workload-shaping (§7.2):** segregated lane state removes the highest-rate, most conflict-prone operations from the main scheduling domain — the hypothesis instantiated.

## 8.3 Five hard problems (the lane's research agenda)

**P1 — Who sequences the sub-slots?** Ethereum has one proposer/builder per slot; for 12 seconds a single rotating actor plays the role of Hyperliquid's entire committee, and "no public queue" means *that one leader sees the flow*. FIFO is only as honest as the arrival timestamping. The lane needs **verifiable arrival ordering** — an attester sub-committee, arrival attestations, or cryptographic sequencing (commit-reveal / threshold decryption per snapshot). This is the crux, and where the cryptographic family re-enters. Mitigating observation: leader rotation each slot moves the latency target, which may blunt the colocation race that fixed-venue FIFO invites.

**P2 — Sub-slot finality is soft.** A 200ms fill is a bonded promise until the slot commits; a slot-level reorg unwinds 60 snapshots. Mitigations: slashable preconfirmation-style commitments; honest soft-fill semantics; and **single-slot finality**, which directly strengthens the lane (already among Foundation Part III §11's evolution hooks).

**P3 — State segregation costs composability.** Mid-slot, the lane is *not* synchronously composable with shared EVM state — escrow in, net-settle out at slot boundaries (Hyperliquid's clearinghouse model; dYdX v4's separation). This cost must be stated plainly; composability is restored at every boundary.

**P4 — Neutrality of a blessed fast lane.** The Timeboost lesson applies. Defenses inherited from §5.4: verified-behavior admission (not payment), no bidding inside, deterministic aggregate-state capacity rules, identical rules for all. Sufficiency is an open, evaluable question.

**P5 — Why not an L2?** Sub-second trading exists off L1 (CEX-style L2s, preconf rollups, real-time chains). The lane's differentiators must survive scrutiny: shared L1 security and assets without bridging; protocol-level neutrality (no privileged sequencer company); slot-boundary composability with all L1 state. If they do not, the honest conclusion is that this service belongs at L2 — and the note will say so.

## 8.4 Deployment path (falsifiable, no enshrinement on day one)

1. **Pilot** as a bonded, preconfirmation-style commitment market via builder/proposer commitments with restaking-backed slashing — no protocol change.
2. **Measure:** fill-latency distributions, misordering incidents, main-lane contention relief (the §7.2 experiment in production), reservation-demand behavior.
3. **Enshrine only if proven**, riding the ePBS / single-slot-finality hooks.

---

# 9. Open Research Questions

- What is the **minimum** service portfolio, and what evidence would justify adding (or removing) a class?
- How coarse can class representations be while remaining useful — and how coarse must they be to limit disclosure (§5.1)?
- Can derived (observed-behavior) admission fully replace declared admission for the committed classes?
- How should cross-class capacity be allocated under no-arbitrage and reserved-headroom constraints (§5.3)?
- Does classification reduce aggregate extraction or re-concentrate it (§5.5)? Under what conditions does each hold?
- Can the sub-slot lane's sequencing be made verifiable at acceptable cost (P1) — and does leader rotation measurably blunt latency centralization?
- Empirically: what does the workload-shaping experiment (§7.2) show on real transaction mixes?

---

# 10. Working Hypothesis

Ethereum does not need to become a uniformly faster blockchain. It may instead evolve into a **multi-service execution platform**: a small, coarse, stable portfolio of protocol-native temporal execution services — each defined over the dimensions of Temporal Liquidity, each mixing architectural, economic, and cryptographic defenses appropriate to its class — sharing one decentralized settlement layer. Temporal differentiation, rather than universal acceleration, may be the more scalable path to expanding Ethereum's execution capabilities; and classification itself may make every engine underneath run faster.

> Ethereum may not need every transaction to be fast. It may need one honest, neutral, verifiable 200ms lane — and the discipline to keep the portfolio coarse.

---

## References

[1] TLM Research Notes RN-01 (Temporal Execution Profiles), RN-02 (Protocol-visible Temporal Abstraction), RN-03 (Hyperliquid: A Case Study in Temporal Liquidity), RN-05 (Supply-side Heterogeneity and Temporal Granularity — the lattice substrate this note's services sit on).
[2] TLM Foundation Statement, Parts I–III; *Temporal-Liquidity* (canonical concept note); *TLM-Positioning*.
[3] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; JACM 2024.
[4] Chung, H. & Shi, E. *Foundations of Transaction Fee Mechanism Design.* ePrint 2021/1474; SODA 2023.
[5] Shi, E., Chung, H. & Wu, K. *What Can Cryptography Do for Decentralized Mechanism Design?* ITCS 2023; arXiv:2209.14462.
[6] Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014, 2023; Springer 2024.
[7] Braden, R., Clark, D. & Shenker, S. *Integrated Services in the Internet Architecture.* RFC 1633, 1994.
[8] Blake, S. et al. *An Architecture for Differentiated Services.* RFC 2475, 1998. See also Stoica, Shenker & Zhang, *Core-Stateless Fair Queueing,* SIGCOMM 1998.
[9] Hyperliquid documentation (About; HyperCore; Order Book). *Vendor-sourced; specifics (validator set, routing, FIFO tie-breaking, liquidation precompiles, mark-price composition) pending verification.*
[10] *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost.* arXiv:2509.22143.
[11] Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races.* SSRN 6240079, 2026.
[12] Monad documentation. https://docs.monad.xyz/ *(pending verification).*
[13] "How Monad Works." Monad blog. https://blog.monad.xyz/blog/how-monad-works *(pending verification).*
