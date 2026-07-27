---
id: RN-08
title: "Modern Blockchains Through the Lens of TLM: Common Components, Differentiated Features, and the Case for Decoupling Execution from Control"
version: v0.3 (supersedes v0.2)
status: "Public draft, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: July 27, 2026
---

# RN-08 Modern Blockchains Through the Lens of TLM

## Abstract

Modern chains are usually compared on throughput, latency, finality, compatibility, and decentralization. This note instead uses two tools - the TLM lens (execution as scheduling over time) and a **three-layer architecture**: *demand description -> control engine -> execution engine* - to ask a structural question: across Ethereum, Aptos, Monad, and HyperCore, what is genuinely **common**, and what is **truly differentiated**?

Read this way, the four chains share the same components - consensus and settlement, ordering, an execution engine, a state store, a fee market - and each re-implements the entire stack, fusing consensus, control, and execution into one sovereign system. The result of that pattern, repeated across hundreds of Layer-1s, is duplicated security and fragmented liquidity and state. The study therefore reaches a conclusion rather than starting from one: for the health of blockchain development - to avoid wasted resources and fragmentation - the productive move is to **decouple the execution engine from the control engine**, share consensus and settlement, and let execution be differentiated above them. That decoupling is what TLM provides, and it points toward **virtualization** (Virtual Chains, RN-09) as the healthy architecture. Which existing chain is best positioned to become such a host is a corollary of the same common-vs-differentiated analysis, addressed at the end.

---

## 0. Relationship to the other TLM notes, and terminology

This note is the *comparative survey*; it references the rest of the series rather than re-deriving it. The Monad analysis is condensed here and developed in **RN-06**; the control/data-plane and multi-timescale framing is **RN-06 sec. 2.2** and **RN-07**; service classes and execution objects are **RN-04**; the execution lattice is **RN-05**; the Hyperliquid / HyperCore case is **RN-03**; and the virtualization architecture this note concludes toward is **RN-09**.

Terminology: "temporal profile" means a stream-level instance of the RN-01 Temporal Execution Profile, under the umbrella definition - execution priority; delay tolerance / windows / deadlines; predictability / continuity.

---

## 1. Motivation: fragmentation and the health of the ecosystem

The ecosystem has produced hundreds of Layer-1 chains. Many were created not because an application needed a different consensus algorithm, but because it needed different *execution* properties - lower latency, specialized ordering, a custom fee model, dedicated throughput. But the only way to obtain those has been to build an entire chain: a validator set, staking and economic security, governance, and operational tooling.

Repeated across the ecosystem, that pattern has a cost. Each new chain duplicates consensus and security, and splits liquidity, state, and composability across sovereign silos connected only by bridges. This is waste at the level of the whole system, even when each individual chain is well-built. The question this note asks is therefore not "which chain is fastest," but: **what do modern chains actually share, what truly differentiates them, and what does that imply for a healthier architecture?**

## 2. The analytical foundation: the TLM lens and a three-layer architecture

Two tools structure the study.

**The TLM lens.** TLM treats execution as a scheduling problem over time, not only a next-block inclusion problem. Demand is heterogeneous in time - some urgent, some patient, some periodic - and that heterogeneity (temporal liquidity) is information a protocol can use. The demand representations (RN-01/02), service classes (RN-04), lattice (RN-05), and layered control plane (RN-07) are developed elsewhere; this note uses them.

**A three-layer architecture.** Any execution system can be read as three layers:

```text
Demand description   - what work wants to run, and with what temporal needs   (RN-01/02)
        v
Control engine       - admit, price, order, and schedule the work            (control plane; RN-04/RN-07)
        v
Execution engine     - run the ordered work and commit state                 (data plane; RN-06)
```

The move TLM enables - and the one the rest of this note builds toward - is **separating the control engine from the execution engine** (control-plane/data-plane decoupling; RN-06 sec. 2.2, RN-07). Today's chains fuse all three layers into one sovereign stack. Holding the layers apart is what makes shared consensus with differentiated execution possible.

## 3. Common components vs differentiated features

Every modern chain, however marketed, is built from the same parts:

| Common component | What it does | Where chains actually differ |
|---|---|---|
| Consensus + finality | agree on an ordered history | speed, validator-set size, finality latency |
| Settlement / state | hold and update global state | store design, access cost |
| Ordering / mempool | choose the transaction sequence | public vs private, PBS, FIFO |
| Execution engine | run the ordered transactions | sequential / parallel / specialized |
| Fee market | price scarce capacity | scalar (EIP-1559) vs domain-specific |

These are **commodity** for our purpose: every chain has them, and differences here are performance, not kind. What separates the four candidates is the **differentiated feature** each adds on top:

- **Ethereum** - credible neutrality, decentralization at scale, a deep composable ecosystem, and EIP-1559 as the reference fee market. Differentiator: *neutrality and network effects*, not performance.
- **Aptos** - **Block-STM**, a dynamic speculative parallel executor, plus **Move**'s resource-oriented (typed) state semantics. Differentiator: *a programmable parallel data plane with typed state*.
- **Monad** - EVM equivalence at high performance, with asynchronous (deferred) execution, optimistic parallelism, and a purpose-built state DB (RN-06). Differentiator: *performance without leaving the EVM*.
- **HyperCore** - an application-specialized execution environment (on-chain order book, margin, liquidations) that already coexists with a general runtime (HyperEVM) under one HyperBFT consensus. Differentiator: *differentiated execution already sharing one consensus*.

## 4. The four chains through the three-layer lens

**Ethereum.** Demand description is minimal (a scalar bid; nonces; contract deadlines). The control engine is a scalar fee market that prices current block congestion, with no abstraction for future capacity. The execution engine is a single, general, sequential EVM. All three layers are fused, and its differentiated strength - neutrality, settlement, composability - sits at the consensus/settlement layer, not execution.

**Aptos.** Demand description is still transaction-level. The execution engine is the differentiator: Block-STM extracts concurrency from a canonically ordered block, and Move gives typed state. Ordering and control remain conventional. It fuses the layers, but its execution engine is a clean, sophisticated data plane - the layer most ready to sit *below* a separate control engine.

**Monad.** Like Ethereum in semantics, differentiated by an execution engine rebuilt for performance (optimistic parallelism, asynchronous/deferred execution, a purpose-built DB; RN-06). Its asynchronous design already makes the consensus/execution seam explicit - the exact place a control engine would attach - though the layers are still shipped as one chain.

**HyperCore.** The important case. HyperCore runs a specialized exchange execution environment *and* HyperEVM under one HyperBFT consensus (RN-03). It is the one candidate that already **partly decouples**: two differentiated execution engines share a single control-and-consensus base. Its temporal semantics are embedded in the application rather than exposed as a general interface, but structurally it is a two-domain proof that execution can be differentiated without duplicating consensus.

## 5. Synthesis

Two cross-cutting points sharpen the reading. First, **parallelism is not temporal liquidity** - they are orthogonal:

| Dimension | Question |
|---|---|
| Execution parallelism | can these transactions execute concurrently? |
| Temporal liquidity | can this demand move to another execution time? |

Parallelism (Aptos, Monad) raises effective capacity *within* a window; temporal scheduling (TLM) moves flexible demand *across* windows. They compose. Second, the right yardstick is not TPS but **Temporal Economic Throughput** - how much economically useful demand is satisfied over time, weighting deadline success, delay, predictability, and value preserved by correct timing.

The structural observation is the one that matters most. Every chain re-implements the full three-layer stack and ships it as a sovereign system. That is why obtaining a new execution property has meant a new chain - and why the ecosystem duplicates security and fragments liquidity and state. HyperCore is the crack in that assumption: it shows differentiated execution can share one consensus.

## 6. Conclusion: decouple execution from control

Separating what is common from what is differentiated leads to a clear conclusion. The common layer - consensus, settlement, ordering, execution, fee market - is shared by all four; re-building it for every new execution need is the source of the waste and fragmentation in sec. 1. The differentiated features - neutrality and settlement (Ethereum), a parallel typed data plane (Aptos), EVM-equivalent performance (Monad), and live multi-domain execution under one consensus (HyperCore) - are the parts worth keeping and combining.

The healthy direction, then, is to **decouple the execution engine from the control engine**: share one credibly-neutral consensus and settlement base, run a temporal control engine above it (RN-07), and let execution be differentiated - multiple engines, runtimes, ordering rules, and fee policies - without each one duplicating consensus. This is TLM's core move, and it is precisely **virtualization**: many differentiated execution domains on one host, which **RN-09 (Virtual Chains)** develops as an architecture. Virtualization is thus a conclusion of this comparative study, motivated by the health of the ecosystem, not an assumption made at the start.

The downstream question - *which existing chain is best positioned to become such a host* - follows from the same analysis. The four occupy complementary positions: **Ethereum** as the neutral settlement and neutrality anchor; **Monad** as the least-friction EVM-compatible performance host; **Aptos** as the cleanest programmable data plane to prototype a control engine over; and **HyperCore** as the existence proof that the pattern already works. No single chain is a complete host today; the ideal host combines Ethereum's neutrality and settlement, a high-performance parallel data plane, HyperCore's demonstrated multi-domain execution, and a temporal control engine with fee virtualization that respects the RN-07 reducibility invariant. That design, and the host question, are taken up in RN-09.

---

## References

[1] TLM Research Notes: RN-01 (Temporal Execution Profiles), RN-02 (Protocol-visible Temporal Abstraction), RN-03 (Hyperliquid / HyperCore case study), RN-04 (Temporal Execution Services), RN-05 (Supply-side granularity; execution lattice), RN-06 (Monad; OS->networking framing; control/data-plane decoupling), RN-07 (Layered control architecture; reducibility invariant), RN-09 (Virtual Chains).

[2] Aptos documentation - Execution; Block-STM. https://aptos.dev/network/blockchain/execution

[3] Monad documentation - Parallel Execution; Asynchronous Execution. https://docs.monad.xyz/

[4] Hyperliquid documentation - HyperCore; HyperEVM. https://hyperliquid.gitbook.io/hyperliquid-docs

[5] EIP-1559 - Fee Market Change for ETH 1.0 Chain. https://eips.ethereum.org/EIPS/eip-1559

*Editorial note: descriptions of deployed systems reflect publicly documented architecture as of July 2026; Monad and Hyperliquid facts are verified in RN-06 and RN-03.*
