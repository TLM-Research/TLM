---
id: RN-09
title: "Chain Virtualization: A Conceptual Frame for Diversified Project Types on a Shared Fast L1"
status: "Public draft - conceptual research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: August 12, 2026
---

# RN-09 - Chain Virtualization

## Abstract

New Layer-1 blockchains are often created not to run a different consensus algorithm, but to obtain application-specific *execution* properties - low latency, specialized ordering, a custom fee model, dedicated throughput, or a project's own token and governance. Obtaining these today usually means bootstrapping a whole chain, which duplicates security and fragments liquidity and state.

This note develops a concept: **Virtual Chains** - logically independent, software-defined execution domains that coexist on a shared host chain, each with its own execution policy and, where a project needs it, its own token and governance, while inheriting the host's consensus, settlement, and shared state. It sits alongside two conceptual dimensions of differentiation: **time** (when execution happens, RN-01/04/05) and a per-project **execution class** (what policy a project runs under, this note).

This is a conceptual note, and its limits are stated up front. It does **not** specify how virtualization is realized - the marking, scheduling, isolation, and enforcement mechanism is deferred to a planned mechanism note. Terms borrowed from networking, such as traffic class and Differentiated Services, are used to convey the idea, not to fix an implementation. And Virtual Chains are **not** proposed as the only way to support many application-chains: they do not replace Layer-2 rollups or sovereign app-chain frameworks such as Cosmos, which serve needs a shared L1 does not. The aim is to enhance Ethereum's ecosystem - to let a faster, temporally-aware Ethereum serve project types that today leave - not to build a greenfield chain.

---

## 1. Theme and boundary

**Theme.** A block today prices one thing: inclusion now. The TLM program asks what a fee market looks like with more than one handle - **time** (when execution happens) and a per-project **execution class** (what policy it runs under) - so that one fast, neutral L1 can serve project types that currently leave for their own chains. A **Virtual Chain** is the execution-class idea: a software-defined domain over shared consensus, settlement, and state, with its own ordering, fee model, runtime, and optionally its own token and governance. This is service differentiation applied to blockchain execution. It is a concept, not a new chain and not a claim to a new paradigm; the contribution, if it holds, is a way to make an existing fast L1's market carry more.

**The boundary.** The idea lives on one boundary, and defining it is most of the work still to do.

- **Shared - the host provides:** consensus, settlement finality, one shared state, atomic composability, and the base accounting that prices physical capacity.
- **Virtualized - a project defines in software:** execution policy, ordering, runtime, fee model, and optionally token, governance, and monetary policy.
- **The open edge:** how far per-project economic sovereignty can go before it fragments the shared state it sits on. A project token with its own monetary policy is a unit-of-account boundary that pulls against shared liquidity. What such a token can control while the state stays unified is not yet settled - it is the question the mechanism will have to answer.

**In and out of scope.** In scope: projects that want execution and economic differentiation *and* shared state and composability on a fast L1. Out of scope, by design: projects that need their own consensus or full monetary sovereignty (a sovereign chain fits better), and workloads that need to leave the L1's execution budget (a rollup fits better). Virtual Chains complement both.

## 2. Two conceptual dimensions: time and execution class

The frame has two axes, offered as concepts rather than as a chosen design.

- **Time.** When execution happens: immediate, reserved, patient, scheduled, periodic. This is the temporal-liquidity axis of RN-01, the service classes of RN-04, and the quantum-indexed lattice of RN-05.
- **Execution class.** Which execution policy a unit of work runs under - its runtime, ordering, fee model, and the project domain (Virtual Chain) it belongs to.

Networking offers a precedent worth borrowing as intuition. Differentiated Services (DiffServ) differentiates traffic by a class marking applied at the edge, so the network can offer different service without per-flow setup in its core; this contrasts with per-flow reservation (IntServ/RSVP). The intuition is that class-based differentiation can scale where per-instance provisioning does not - and standing up a separate chain per project resembles per-instance provisioning. That is the analogy's whole use here. This note does **not** claim that execution differentiation should be implemented in a DiffServ-like way, nor that "class" is the right unit; how differentiation is marked, scheduled, and enforced is a mechanism question, deferred to a later note.

**The two axes are not independent.** They are drawn apart for intuition, but both draw on one shared resource pool, and a domain's own policy bounds the temporal guarantees feasible inside it: a low-latency exchange domain and a patient settlement domain make different temporal promises realizable, and every reservation on the time axis consumes host capacity the class axis also competes for. A joint treatment belongs to the mechanism note; the point here is that the two axes meet at the host's resources and cannot promise independently.

## 3. The host chain: a fast, EVM-compatible L1

The host supplies the shared foundation: validators, consensus and finality, economic security, global settlement, shared state, and resource accounting. A Virtual Chain would inherit these, so its security can approach the host's rather than that of a small, separately bootstrapped validator set - but conditionally. Consensus and settlement are inherited directly; inheritance of *execution* security depends on how a domain's runtime is validated - whether every validator executes it, a committee attests to it, or a proof verifies it (§7). Where that validation path is left undefined, the security claim is not yet earned.

The host this note has in mind is a faster, temporally-aware Ethereum: EVM-compatible, with execution performance in the range Monad (RN-06) and Aptos (RN-08) have shown is achievable, and with the RN-05 lattice as scheduling structure. The goal is an ecosystem of Ethereum - its neutral settlement layer and developer base, made fast and temporally expressive enough to keep project types that today leave. This is a host-side premise, not a new chain.

## 4. What a Virtual Chain is

A Virtual Chain is a logical execution domain that could define its own scheduling policy, execution priorities, ordering, fee policy, runtime, state namespace, token, and governance - without a new validator network. Illustrative domains, EVM-compatible by default:

- **Exchange** - low latency, price-time priority, maker/taker fees, order-book runtime.
- **Settlement** - patient execution, reserved capacity, subscription pricing.
- **General smart-contract** - EVM, an EIP-1559-style fee market.
- **Institutional** - deterministic execution windows and service-level guarantees.

These are the RN-04 service classes seen as full domains rather than lanes within one chain. How a domain is instantiated, isolated, and scheduled is not specified here (§7).

## 5. Cross-domain execution and shared state

The property that distinguishes this concept from the alternatives in §6 is shared state. Because Virtual Chains would share one settlement layer and one state substrate, they retain atomic interaction, shared liquidity, and unified state - the composability that independent Layer-1s and separately-bridged rollups give up. That property is also the concept's hardest constraint, and it forces a choice on which the rest of this note's coherence depends.

**The triangle.** Three things cannot all be strong at once: **execution sovereignty** (a domain choosing its own ordering and runtime), **atomic shared state** (domains composing atomically over one state), and **host-wide validation** (the host enforcing correctness). Independent ordering over one atomically-mutated state requires a root rule that serializes conflicting cross-domain accesses - and that rule is a shared control plane, so full ordering sovereignty is exactly what it costs. A design must say which two legs it keeps strong and what weakens in the third; keeping all three strong is what would make a Virtual Chain a property bundle rather than an architecture.

**A candidate point, offered for the mechanism note to test.** Keep atomic shared state and host validation strong, and bound sovereignty: a domain is sovereign over ordering and runtime *within its own state namespace*, but a transaction touching state shared with another domain yields to a host-imposed serialization - a root commit order over cross-domain-touching transactions, as a database serializes conflicting transactions while leaving independent ones concurrent. Sovereignty is then full where state is disjoint and host-serialized where it is shared - coherent, but conceding that a domain does not control the ordering of its cross-domain interactions. Whether that concession is acceptable, and whether the serialization can be made cheap, is the mechanism question (§7); the point here is that a coherent point on the triangle exists and can be named.

**Failure isolation is therefore only partial.** Domains that do not interact keep failures local, but an atomic cross-domain call couples them: if a transaction spans domains A and B and B's transition fails, the atomic transaction rolls back across both - liveness and rollback are shared along exactly the composability the concept exists to keep. The honest statement is not that failures stay local, but that they stay local except along atomic cross-domain calls, which roll back together.

This shared-state property is also the one most in tension with per-project tokens (§1); the two are reconciled only by defining the boundary, which is open.

## 6. Prior art: situational fit and lessons

Each existing approach works well in a situation and leaves a lesson. The aim is to place Virtual Chains among them, not above them.

| Approach | Works well when | Lesson |
|---|---|---|
| **Cosmos** (sovereign app-chains, IBC) | a project needs its own consensus, validators, or monetary sovereignty (dYdX v4) | sovereignty is real but costs composability; interop stays asynchronous; do not reproduce consensus for differentiation obtainable another way |
| **Polkadot** (shared security; Agile Coretime) | many chains want one security root without each bootstrapping validators | shared security does not by itself create demand; allocation terms decide uptake (slot-auction failure, coretime fix); a capacity market prices the pipe but leaves state siloed |
| **L2 rollups** (shared settlement, sovereign execution) | a workload needs to scale execution off the host while inheriting its security | the closest match - the market wants shared security with its own execution; siloed state fragments liquidity; native rollups (EIP-8079) and shared sequencing are converging toward host-verified execution, which suggests the direction is sound |

Read together: security can be shared, and execution can be sovereign, and both are proven in production. The property none of these delivers by default is shared state with atomic composability under sovereign execution - and that is the one thing Virtual Chains take as a substrate rather than recover after the fact. That is the concept's claim, and its limit. On the mechanism side, the shared lesson from Polkadot and Cosmos is plain: offering shared security is not enough; the terms on which differentiation is offered decide whether anyone uses it - which is why the deferred mechanism, not the concept, is where this stands or falls. Figure 1 places the four approaches across these axes.

![Figure 1 - the design space: shared security versus sovereign execution](figures/rn09/RN-09_Fig1_design-space.svg)

## 7. Open problems

The constitutive one is the **consistency model** of §5: which point on the sovereignty / atomic-state / host-validation triangle the host enforces. That choice decides whether the concept is coherent and distinct at all, and it comes before pricing. After it comes the mechanism itself: **how virtualization is realized** - how a domain is marked, admitted, scheduled, isolated, and enforced; how each domain's fee and runtime reduce to the host's accounting - a translation from a domain's own token or fee into the host's single-numeraire pricing of physical capacity, with a basis and a default rule (RN-10 sec. 3.1); and the per-domain state-transition authority, validation path, and finality that complete the definition of §4. That is the subject of a planned mechanism note. One thing that note must settle empirically: whether virtualization *expands* the set of project types served or merely *partitions* existing host capacity - static domains may only partition, and any expansion has to come from conflict isolation, complementary resource profiles, parallelism, or statistical multiplexing, not from the label. Named alongside it: the **shared-versus-virtualized boundary** - what a per-project token, fee, and governance policy can control without fragmenting shared state (§1, §5); cross-domain atomicity across different runtimes; validator specialization and its centralization risk; fairness and minimum service for ordinary traffic; and truthful revelation of temporal and class profiles. Several have analogs in §6 - allocation and core scheduling in Polkadot, shared-sequencer coordination in the rollup ecosystem - which are sources of evidence rather than untried ground.

## 8. Relationship to the TLM notes

RN-09 is the *conceptual, system-architecture* view. RN-01/02 supply the demand representations, RN-04 the service classes, RN-05 the lattice, RN-06 an execution engine and the networking framing, RN-07 the layered control plane, and RN-08 the comparative survey that motivates the design. Precursors in the wild include Hyperliquid's HyperCore/HyperEVM under one consensus (RN-03), Monad as an execution substrate (RN-06), and Aptos's Block-STM (RN-08); Ethereum is the neutral settlement layer this note aims to enhance. The mechanism note will follow from here.

## 9. Positioning

The question shifts from "how many Layer-1 chains should exist?" to "how much sovereignty does an application need, and how much can be provided in software over a shared, fast L1?" A project that needs its own consensus should have its own chain, on Cosmos or elsewhere; a workload that needs to leave the L1's execution budget belongs on a rollup; a project that needs differentiation while keeping shared state can, if the mechanism can be defined, be served as a Virtual Chain. TLM is not another Layer-1. It is a demand-side control plane - conceived here at the level of concept and boundary - that could let a fast, EVM-compatible Ethereum serve more project types in-place, complementing the rollup and app-chain paths rather than replacing them.

---

## References

[1] TLM Research Notes RN-01 through RN-08 (see RN-08 for the full list).

[2] Hyperliquid documentation - HyperCore / HyperEVM under shared HyperBFT consensus. https://hyperliquid.gitbook.io/hyperliquid-docs

[3] Differentiated Services (DiffServ), IETF RFC 2474 / RFC 2475; contrast per-flow reservation (IntServ / RSVP, RFC 2205). Used as intuition only (§2).

[4] Monad documentation. https://docs.monad.xyz/ | Aptos / Block-STM. https://aptos.dev/

[5] Wood, G. *Polkadot: Vision for a Heterogeneous Multi-Chain Framework.* 2016. https://polkadot.com/papers/Polkadot-whitepaper.pdf

[6] Polkadot Fellowship. *RFC-1: Agile Coretime.* 2023 (activated September 2024). https://polkadot-fellows.github.io/RFCs/approved/0001-agile-coretime.html

[7] Cosmos SDK / IBC. https://docs.cosmos.network/ | Interchain Security. https://cosmos.github.io/interchain-security/

[8] Layer-2 rollup landscape, 2026 (rollup count, TVL, cross-rollup composability). Secondary coverage; replace with L2BEAT or equivalent primary data before publication.

[9] Espresso Systems / shared sequencing. https://docs.espressosys.com/

[10] Donno, L. and Drake, J. *EIP-8079: Native Rollups (EXECUTE precompile).* 2025. https://eips.ethereum.org/

---

*Changes from v0.3.* Synthesis folded into the opening (§1 Theme and boundary); prior-art trimmed to one section (§6) with a situational-fit-and-lessons table. Mechanism claims removed throughout: the note is explicitly conceptual, and how virtualization is realized - including whether a DiffServ-style class model is used at all - is deferred to a planned mechanism note (§7). "Traffic class" and DiffServ are framed as borrowed intuition, not a chosen design. Scope and complementarity with L2 and Cosmos retained from v0.3. References condensed; [8] still needs a primary data source.
