---
id: RN-08
title: "Modern Blockchains Through the Lens of TLM in a 3-layer Architecture: Common Components, Differentiated Features, and the Case for Decoupling Execution from Control"
version: v0.4 (merged - v0.3 narrative + full depth of the original draft; definitive)
status: "Public draft, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: July 27, 2026
---

# RN-08 - Modern Blockchains Through the Lens of TLM in a 3-layer Architecture

## Abstract

Modern chains are usually compared on throughput, latency, finality, compatibility, and decentralization. This note instead uses two tools - the TLM lens (execution as scheduling over time) and a **three-layer architecture**: *demand description -> control engine -> execution engine* - to ask a structural question: across Ethereum, Aptos, Monad, and HyperCore, what is genuinely **common**, and what is **truly differentiated**?

Read this way, the four chains share the same components - consensus and settlement, ordering, an execution engine, a state store, a fee market - and each re-implements the entire stack, fusing consensus, control, and execution into one sovereign system. The result of that pattern, repeated across hundreds of Layer-1s, is duplicated security and fragmented liquidity and state. The study therefore reaches a conclusion rather than starting from one: for the health of blockchain development - to avoid wasted resources and fragmentation - the productive move is to **decouple the execution engine from the control engine**, share one consensus and settlement base, and let execution be differentiated above it. Which existing chain is best positioned to serve as that shared base is a corollary of the same common-vs-differentiated analysis, addressed at the end.

---

## 0. Relationship to the other TLM notes, and terminology

This note is the *comparative survey*; it draws on earlier notes rather than re-deriving them. The Monad analysis is condensed here and developed in **RN-06**; the layered control-plane framing is **RN-07**; demand representations are **RN-01/RN-02** and service classes **RN-04**; the execution lattice is **RN-05**; and the Hyperliquid / HyperCore case is **RN-03**.

Terminology: "temporal profile" means a stream-level instance of the RN-01 Temporal Execution Profile, under the umbrella definition - execution priority; delay tolerance / windows / deadlines; predictability / continuity. Its three stream dimensions map as: duration -> continuity, intensity -> capacity, execution-time variability -> delay tolerance and predictability.

---

## 1. Motivation: fragmentation and the health of the ecosystem

The ecosystem has produced hundreds of Layer-1 chains. Many were created not because an application needed a different consensus algorithm, but because it needed different *execution* properties - lower latency, specialized ordering, a custom fee model, dedicated throughput. But the only way to obtain those has been to build an entire chain: a validator set, staking and economic security, governance, and operational tooling.

Repeated across the ecosystem, that pattern has a cost. Each new chain duplicates consensus and security, and splits liquidity, state, and composability across sovereign silos connected only by bridges. This is waste at the level of the whole system, even when each individual chain is well-built. The question this note asks is therefore not "which chain is fastest," but: **what do modern chains actually share, what truly differentiates them, and what does that imply for a healthier architecture?**

## 2. The analytical foundation: the TLM lens and a three-layer architecture

Two tools structure the study.

**The TLM lens.** TLM treats execution as a scheduling problem over time, not only a next-block inclusion problem. Demand is heterogeneous in time - some urgent, some patient, some periodic - and that heterogeneity (temporal liquidity) is information a protocol can use. A conventional fee market evaluates whether a transaction is valid and whether its fee clears; time enters only indirectly (a priority fee raises the odds of earlier inclusion; congestion raises the price; users resubmit or postpone). TLM proposes that time become a first-class dimension of demand: a generalized request may specify an earliest execution time, a preferred window, a latest acceptable time, persistence across slots, expected intensity, tolerance for timing variability, recurrence, and fallback. Ordinary immediate transactions stay simple; the richer object is available when an application can beneficially reveal temporal information. (The representations are RN-01/02; the service classes RN-04; the lattice RN-05; the layered control plane RN-07.)

**A three-layer architecture.** Any execution system can be read as three layers:

```text
Demand description   - what work wants to run, and with what temporal needs   (RN-01/02)
        v
Control engine       - admit, price, order, and schedule the work            (control plane; RN-04/RN-07)
        v
Execution engine     - run the ordered work and commit state                 (data plane; RN-06)
```

The control engine *describes, admits, prices, and schedules* demand; the execution engine *orders, executes, and commits* it. The move TLM enables - and the one the rest of this note builds toward - is **separating the control engine from the execution engine** (the layered control plane of RN-07). Today's chains fuse all three layers into one sovereign stack. Holding the layers apart is what makes shared consensus with differentiated execution possible.

## 3. Evaluation dimensions

Each chain is examined with the same questions, grouped by layer:

- **Consensus and settlement.** What security and finality substrate is provided? Is execution tied to a broadly shared settlement layer? Does specialized execution require separate consensus sovereignty?
- **Execution engine.** Sequential, parallel, speculative, pipelined, or specialized? How are conflicts discovered and resolved? General-purpose or domain-specific?
- **Demand representation.** What can a user express beyond validity and gas price - deadlines, persistence, flexibility? Is the scheduling unit a stateless transaction, or can it be a stream or execution object?
- **Resource allocation.** Is capacity allocated one block at a time, or can applications reserve or borrow future capacity? Does the protocol distinguish urgent, patient, periodic, and sustained demand?
- **Fee architecture.** One generalized fee market, or application-specific policies? Can urgent users pay for immediacy while flexible users receive a price benefit?
- **Execution sovereignty.** Must an application create a new chain for specialized execution, or can one consensus support multiple execution domains?

## 4. Common components vs differentiated features

Every modern chain, however marketed, is built from the same parts:

+------------------------------------------------------------------------------------------------------+
| Common component     | What it does                    | Where chains actually differ                |
|----------------------|---------------------------------|---------------------------------------------|
| Consensus + finality | agree on an ordered history     | speed, validator-set size, finality latency |
| Settlement / state   | hold and update global state    | store design, access cost                   |
| Ordering / mempool   | choose the transaction sequence | public vs private, PBS, FIFO                |
| Execution engine     | run the ordered transactions    | sequential / parallel / specialized         |
| Fee market           | price scarce capacity           | scalar (EIP-1559) vs domain-specific        |
+------------------------------------------------------------------------------------------------------+

These are **commodity** for our purpose: every chain has them, and differences here are performance, not kind. What separates the four candidates is the **differentiated feature** each adds on top:

- **Ethereum** - credible neutrality, decentralization at scale, a deep composable ecosystem, and EIP-1559 as the reference fee market. Differentiator: *neutrality and network effects*, not performance.
- **Aptos** - **Block-STM**, a dynamic speculative parallel executor, plus **Move**'s resource-oriented (typed) state semantics. Differentiator: *a programmable parallel data plane with typed state*.
- **Monad** - EVM equivalence at high performance, with asynchronous (deferred) execution, optimistic parallelism, and a purpose-built state DB (RN-06). Differentiator: *performance without leaving the EVM*.
- **HyperCore** - an application-specialized execution environment (on-chain order book, margin, liquidations) that already coexists with a general runtime (HyperEVM) under one HyperBFT consensus. Differentiator: *differentiated execution already sharing one consensus*.

## 5. The four chains through the three-layer lens

### 5.1 Ethereum - the neutral settlement base

Ethereum's contribution is not execution speed; it is a widely shared, credibly-neutral settlement layer with proof-of-stake validation, general-purpose (sequential) EVM execution, open EIP governance, a deep composable ecosystem, and EIP-1559. It separates consensus and execution conceptually, but mainnet presents one broadly uniform execution service: transactions consume gas and compete for inclusion in the next block, with a base fee that adjusts to congestion and a priority fee (tip) that buys earlier inclusion.

A user's temporal levers are only indirect. A higher tip buys *immediacy* - sooner inclusion - but expresses nothing about later, scheduled, or reserved execution. A contract can enforce a *deadline* (a transaction reverts if included after some block or timestamp), but that only invalidates late execution; it does not tell the protocol how to schedule the transaction before then. An account's *nonce* fixes the order of that account's own transactions (replay protection and per-sender sequencing), which is not a scheduling preference at all. There is no protocol abstraction for allocating future execution capacity - windows, reservations, patient queues, or demand streams.

All three layers are fused, and Ethereum's differentiated strength sits at the consensus/settlement layer, not execution.

**Strength:** the strongest neutral settlement foundation and the richest context for generalized fee-mechanism research.
**Limit through this lens:** it prices current block congestion, not structured temporal demand, and exposes no native market for execution across future time.

### 5.2 Aptos - the programmable parallel data plane

Aptos is built around high-throughput execution, the Move language, and **Block-STM**, which executes a canonically ordered block speculatively in parallel while preserving the deterministic result of that order: it runs transactions concurrently, detects state conflicts, and re-executes when speculative reads become invalid. Parallel execution does not eliminate ordering - transactions keep a canonical order; concurrency is *discovered* within it. Block-STM answers one question:

> Given an ordered block of transactions, how can the system safely exploit available concurrency?

TLM asks an earlier one:

> Which demands should be admitted to which block or window, and what temporal service should each receive?

**Block-STM as a data-plane mechanism.** These questions compose cleanly. A TLM control engine forms sets - an immediate low-latency channel, a reserved-capacity channel, a patient background channel, periodic settlement batches, or groups chosen for state locality - and orders each set; Block-STM then executes it in parallel. TLM need not prescribe low-level speculative execution; it can rely on an engine like Block-STM for that. The pipeline:

```text
Application or transaction stream
        v
Temporal profile (duration, intensity, variability)
        v
Admission, pricing, and future-capacity allocation   <- TLM control engine
        v
Execution window or temporal channel
        v
Canonical transaction ordering
        v
Block-STM speculative parallel execution              <- data plane
        v
State commitment and consensus
```

**Concurrency is not temporal liquidity.** The two are orthogonal. Parallelism asks whether transactions can execute simultaneously without breaking deterministic semantics; temporal liquidity asks how far a demand can move across execution time and keep its value. A state-heavy settlement transaction may be safely delayed thirty blocks (high temporal liquidity) yet conflict with many others once it runs (low parallelism); thousands of independent urgent payments may be the reverse.

| Dimension | Core question |
|-----------|---------------|
| Execution parallelism | Can these transactions execute concurrently? |
| Temporal liquidity    | Can this demand move to another execution time? |

A complete scheduler uses both. This yields a two-level optimization: (1) **temporal allocation** - move flexible demand away from congested periods or into reserved windows; (2) **parallel-execution optimization** - within each selected window, exploit concurrency and manage conflicts. Move's typed, resource-oriented state may *help estimate* conflicts when forming windows (declared/inferred state access, module relationships, historical conflict rates), but TLM should not depend on perfect static prediction - Block-STM exists precisely because conflicts are discovered dynamically.

**Stream-aware demand.** Aptos, like most chains, receives individual transactions; TLM adds a persistent demand abstraction - a payment app expecting recurring volume for an hour, an oracle announcing periodic updates, a game reserving capacity around an event, a settlement process willing to run anytime within a window. A stream profile can be a capacity envelope or reservation commitment, with concrete execution objects arriving later.

**As a host:** Aptos already treats execution as a sophisticated systems problem, and is freer to innovate without strict EVM behavioral compatibility. That makes it the cleanest programmable data plane to prototype a temporal control engine over. Its limit through the lens of TLM: the parallel executor does not by itself create a market for future windows, stream persistence, urgency classes, or reservations. Put strategically: *Aptos extracts concurrency from a selected order; TLM extracts scheduling flexibility from demand across time.*

### 5.3 Monad - the EVM-compatible performance host

Monad targets high performance while preserving EVM equivalence, via optimistic parallel execution, asynchronous (deferred) execution, a pipelined consensus/execution design, and a purpose-built state DB (full analysis in **RN-06**). One distinction matters here: Monad's **asynchronous execution is not deferred user scheduling**. It decouples consensus from execution in the *implementation* pipeline - the order is fixed, execution runs behind it - whereas TLM's temporal scheduling is a *demand-side service choice* (now vs later, reserve, price urgency, compensate patience). Both use time, at different layers - and, usefully, Monad's async design already makes the consensus/execution seam explicit, which is where a control engine would attach. **As a host:** the least-friction EVM-compatible performance substrate; single-runtime and EVM-bound, and it does not itself expose temporal service.

### 5.4 HyperCore - the working multi-domain precursor

HyperCore is Hyperliquid's specialized execution component (on-chain perpetual and spot order books, margin, matching, liquidations), secured by the same HyperBFT consensus as HyperEVM, with the two able to interact (RN-03). It demonstrates that important applications need execution semantics a generic runtime does not provide - consistent ordering, low jitter, cancellation responsiveness, liquidation priority - and, crucially, that **two materially different execution environments can already share one consensus.** It is the one candidate that already **partly decouples**: two differentiated execution engines on a single control-and-consensus base. Its temporal semantics are embedded in the application rather than exposed as a general interface, and its specialization is built around one domain - so it is the *existence proof* that execution can be differentiated on one consensus, not yet a general host. HyperCore also motivates **specialized validators**: rather than every validator running every runtime, a physical validator could expose several roles (low-latency exchange, general EVM, patient settlement) under accountable rules.

## 6. Synthesis

Two cross-cutting points sharpen the reading. First, **parallelism raises effective capacity within a window; temporal scheduling moves flexible demand across windows** - complementary, not competing. A simple capacity model makes it precise: with execution capacity C_t in slot t and demand D_t, congestion occurs when D_t > C_t. Parallel execution (Aptos, Monad) increases effective C_t; temporal scheduling (TLM) moves flexible parts of D_t to neighboring slots with spare capacity.

```text
Increase effective capacity within each window   (parallel execution)
                     +
Move flexible demand across windows              (temporal scheduling)
                     =
Higher temporal economic throughput
```

Second, the right yardstick is not TPS but **Temporal Economic Throughput (TET)** - how much economically useful demand is satisfied over time, weighting deadline success, delay, predictability, capacity utilization, and value preserved by correct timing. Two hosts with equal TPS can have very different TET; one that protects time-critical demand while deferring flexible work scores higher.

The structural observation is the one that matters most. Every chain re-implements the full three-layer stack and ships it as a sovereign system. That is why obtaining a new execution property has meant a new chain - and why the ecosystem duplicates security and fragments liquidity and state. HyperCore is the crack in that assumption: it shows differentiated execution can share one consensus.

## 7. A reference prototype: a control engine over a parallel data plane

A concrete research prototype places a TLM control engine above a parallel execution data plane (Aptos-like or Monad-like):

```text
+-----------------------------------------------+
| Applications and transaction streams          |
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| Temporal-profile and execution-object layer   |  duration, intensity, variability, deadlines
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| TLM control engine                            |  admission, pricing, reservation, scheduling
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| Temporal channels / future windows            |  immediate, reserved, periodic, patient, burst
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| Ordered block construction                    |  canonical deterministic order
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| Parallel execution data plane (Block-STM etc.)|  speculative parallel execution and retries
+----------------------+------------------------+
                       v
+-----------------------------------------------+
| State commitment, consensus, and finality     |
+-----------------------------------------------+
```

An **execution object** carries a payload reference plus temporal fields (earliest slot, preferred window, latest slot, stream id, expected intensity, variability tolerance, temporal class, runtime, fee policy, reservation mode, fallback); several fields may be commitments, ranges, or forecasts rather than exact declarations. The **scheduler** validates temporal requests, prevents profile manipulation, estimates future capacity, preserves a minimum service for ordinary transactions, allocates reserved and best-effort capacity, chooses transactions for each block, publishes realized service outcomes, updates prices or credits, and passes canonically ordered blocks to the executor. It should not assume temporal flexibility implies conflict freedom - the data plane still does dynamic dependency management - but it may use historical conflict data to improve block composition.

**Neutrality and anti-gaming** must be designed in: false urgency, capacity hoarding, under-reported intensity, unused reservations, strategic deadlines, denial of service against patient queues, validator discrimination among channels. Candidate protections: prepaid reservation deposits, usage-based reconciliation, penalties for chronic forecast error, standardized profile classes, transparent scheduling rules, protocol-published service metrics, and a minimum capacity guarantee for ordinary traffic.

## 8. Fee mechanisms across the four chains

Ethereum's EIP-1559 base fee answers "what should users pay for current scarce block capacity?" TLM broadens it to "what should users pay for different temporal execution services across a future horizon?" A generalized temporal fee curve could distinguish immediate, bounded-delay, reserved, patient best-effort, and recurring service: urgent demand pays an urgency premium; flexible demand receives a lower price or a patience credit for releasing immediate capacity. "Patience yield" should be understood as compensation for giving the scheduler useful flexibility, not a guaranteed return independent of resource value.

This points to a broader possibility once execution is decoupled from one shared consensus: each execution domain could set its own user-facing fee policy - an exchange domain on maker/taker, a settlement domain on reserved-capacity subscriptions, a general domain on EIP-1559-style gas - with the host translating all of them into common resource accounting. Such a policy is admissible only where it compiles down to the host's per-slot accounting (the RN-07 reducibility invariant).

## 9. Conclusion: decouple execution from control

Separating what is common from what is differentiated leads to a clear conclusion. The common layer - consensus, settlement, ordering, execution, fee market - is shared by all four; re-building it for every new execution need is the source of the waste and fragmentation in sec. 1. The differentiated features - neutrality and settlement (Ethereum), a parallel typed data plane (Aptos), EVM-equivalent performance (Monad), and live multi-domain execution under one consensus (HyperCore) - are the parts worth keeping and combining.

The healthy direction, then, is to **decouple the execution engine from the control engine**: share one credibly-neutral consensus and settlement base, run a temporal control engine above it (RN-07), and let execution be differentiated - multiple engines, runtimes, ordering rules, and fee policies - without each one duplicating consensus. This is TLM's core move, and it is the conclusion of this comparative study, motivated by the health of the ecosystem, not an assumption made at the start. How such a shared-consensus, differentiated-execution architecture should actually be built is the natural next question.

The downstream question - *which existing chain is best positioned to serve as that shared base* - follows from the same analysis. The four occupy complementary positions: **Ethereum** as the neutral settlement and neutrality anchor; **Monad** as the least-friction EVM-compatible performance base; **Aptos** as the cleanest programmable data plane to prototype a control engine over; and **HyperCore** as the existence proof that differentiated execution on one consensus already works. No single chain is complete today; the strongest combination would join Ethereum's neutrality and settlement, a high-performance parallel data plane, HyperCore's demonstrated multi-domain execution, and a temporal control engine whose policies respect the RN-07 reducibility invariant.

## 10. Research agenda

Condensed; several items are shared with RN-07 sec. 8.

**Hypotheses.** (1) A scheduler that uses both conflict information and temporal flexibility beats one using only parallelism or only fee priority under bursty load. (2) Even imperfect stream-level forecasts improve future-capacity allocation over stateless per-transaction bidding. (3) Separating immediate, reserved, and patient demand reduces the degree to which urgent users force everyone to compete at urgent prices. (4) Specialized execution need not require separate consensus if isolation, verification, and validator accountability hold. (5) For some applications a bounded low-variability window beats best-effort minimum latency. (6) TLM's benefit grows as demand becomes more bursty, persistent, periodic, or deadline-heterogeneous.

**Experiments.** Trace-driven scheduler simulation (compare fee-priority, FCFS, deadline, and TLM channel/reservation scheduling on deadline success, tail delay, fee spend, utilization, fairness, TET); a control-engine-over-parallel-data-plane model (build windows/channels, then execute with a Block-STM-style engine; test whether temporal rescheduling yields blocks with better parallel efficiency); an EVM-compatible prototype (an execution-window abstraction on a Monad-like substrate, first via contracts / an external scheduler); an exchange workload (urgent cancels, liquidations, ordinary orders, periodic funding, patient settlement - test whether a general temporal profile represents the domain's service classes without hard-coding exchange semantics); and host-fitness scoring of candidate hosts on a common workload.

**Open problems.** Truthful profile revelation; stream identity and accountability without censorship or privacy loss; safe reservation limits for future capacity; where temporal scheduling sits under PBS and how it is verified; whether the scheduler should use predicted conflicts or stay separate from parallel execution; cross-domain atomicity across runtimes and fee policies; validator specialization without centralization; temporal neutrality (differentiation by declared characteristic, never identity); which realized metrics the protocol should publish; and the semantics of blockchain time (slots, blocks, epochs, wall-clock; reorgs and missed slots).

---

## References

[1] TLM Research Notes: RN-01 (Temporal Execution Profiles), RN-02 (Protocol-visible Temporal Abstraction), RN-03 (Hyperliquid / HyperCore case study), RN-04 (Temporal Execution Services), RN-05 (Supply-side granularity; execution lattice), RN-06 (Monad; OS->networking framing; control/data-plane decoupling), RN-07 (Layered control architecture; reducibility invariant).

[2] Aptos documentation - Execution; Block-STM. https://aptos.dev/network/blockchain/execution

[3] Monad documentation - Parallel Execution; Asynchronous Execution. https://docs.monad.xyz/

[4] Hyperliquid documentation - HyperCore; HyperEVM. https://hyperliquid.gitbook.io/hyperliquid-docs

[5] EIP-1559 - Fee Market Change for ETH 1.0 Chain. https://eips.ethereum.org/EIPS/eip-1559

*Editorial note: descriptions of deployed systems reflect publicly documented architecture as of July 2026; Monad and Hyperliquid facts are verified in RN-06 and RN-03.*
