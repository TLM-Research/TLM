---
id: RN-09
title: "Virtual Chains: Decoupling Execution Sovereignty from Consensus Sovereignty"
version: v0.2 (revision of the Virtual Blockchains draft)
status: "Public draft - research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: August 2, 2026
---

# RN-09 - Virtual Chains

## Abstract

New Layer-1 blockchains are often created not to run a different consensus algorithm, but to obtain application-specific *execution* properties: low latency, specialized ordering, a custom fee model, or dedicated throughput. Obtaining those properties today means bootstrapping a whole chain - validator set, staking, economic security, governance, and operational tooling - which duplicates security and fragments liquidity.

This note proposes **Virtual Chains**: multiple logically independent execution domains that coexist on a shared host chain, each with its own execution policy, ordering rules, fee model, runtime, and temporal service guarantees, while inheriting the host's consensus and settlement security. Virtual Chains are the blockchain analog of **network slicing** - SLA-differentiated logical networks over one physical substrate - and they are the natural home for the temporal service classes of RN-04 and the layered control plane of RN-07. The aim is to virtualize *execution* sovereignty while keeping *consensus* sovereignty shared.

---

## 1. Motivation: applications need execution sovereignty, not consensus sovereignty

**RN-08 reaches this note's premise as its conclusion.** A comparative study of modern chains shows that each re-implements the whole stack - consensus, control, and execution fused - so obtaining a new execution property has meant a new chain, which duplicates security and fragments liquidity and state. The healthy direction is to decouple execution from control. RN-09 builds that architecture.

The ecosystem has produced hundreds of Layer-1 chains. Many exist because an application needed lower latency, predictable execution, specialized ordering, dedicated throughput, or a custom fee policy - not because it needed its own consensus. But the only way to get those properties has been to rebuild the entire stack: a validator network, staking and economic security, governance, and operational infrastructure. That path duplicates security and splits liquidity and state across chains.

The observation this note builds on is simple: **applications often need execution sovereignty, not consensus sovereignty.** The exit of order-book and perpetuals venues to their own chains (RN-06 sec. 3.3) is the evidence - they left for ordering and execution control, and paid for consensus sovereignty they did not actually want.

## 2. Sovereignty is separable

"Sovereignty" bundles several independent dimensions: consensus, execution, ordering, fee policy, governance, monetary policy, and state management. A conventional Layer-1 fuses all of them into one indivisible system. Virtual Chains separate them along one seam: **execution policy becomes programmable while consensus stays shared.** An application takes only the sovereignty it needs (the *minimum necessary sovereignty* principle, sec. 10) and inherits the rest from the host.

## 3. The host chain

A host chain supplies the shared foundation: the validator network, consensus and finality, economic security, global settlement, and resource accounting. Every Virtual Chain inherits these, so its security approximates the host's rather than that of a small, separately bootstrapped validator set:

```text
Security(Virtual Chain)  ≈  Security(Host Chain)
      ( not )            Security(small independent validator network)
```

This is the RN-07 host/control-plane substrate viewed from the deployment side: the host prices and secures physical resources; the layers above decide how execution is differentiated.

## 4. Virtual Chains

A Virtual Chain is a logical execution domain that can define its own scheduling policy, execution priorities, ordering semantics, fee policy, runtime, temporal service guarantees, state namespace, and governance over execution behavior - without standing up a new validator network. Some illustrative domains:

- **Exchange domain** - ultra-low latency, price-time priority.
- **Settlement domain** - patient execution, reserved capacity.
- **General smart-contract domain** - EVM compatibility, an ordinary fee market.
- **Institutional domain** - deterministic execution windows and service-level guarantees.

These are the RN-04 temporal service classes (Continuous State, Protected Window, Scheduled, Best-Effort) instantiated as full domains rather than lanes within a single chain.

## 5. Virtual Chains as network slicing

The cleanest way to see the proposal is by analogy to modern networking, which RN-06 sec. 2.2 and RN-07 already draw on. **A Virtual Chain is a network slice for blockchain execution.** In 5G, network slicing runs multiple SLA-differentiated logical networks over one shared physical infrastructure; each slice has its own service policy, but the transport and hardware are shared. Virtual Chains do the same over shared consensus: many differentiated execution domains, one settlement substrate. The generalization from RN-04 is that a slice can carry not just a temporal class but a whole runtime and fee model - while the host still enforces isolation and neutrality.

## 6. Programmable virtual validators

A single, uniform shared-validator model becomes a bottleneck if every validator must run every runtime and workload. Instead, each physical validator can instantiate several **virtual validator roles**, specialized by temporal class, runtime, hardware capability, latency, reliability, or state locality:

```text
Physical Validator
+-- Low-latency exchange validator
+-- General EVM validator
+-- Patient settlement validator
```

Consensus and accountability remain with the host protocol; execution work is mapped to specialized virtual-validator groups under verifiable, accountable rules. This is horizontal specialization without new validator networks - the systems counterpart to RN-06's observation that a fast forwarding plane still needs a policy layer above it.

## 7. Temporal channels and execution objects

Demand is classified into **temporal channels** derived from the demand representations of RN-01/RN-02 - for example immediate, reserved, patient, burst, and periodic. Each channel is an execution service; virtual validators subscribe to the channels they are equipped to serve.

Applications submit not just transactions but **execution objects** (the RN-04 / RN-08 scheduling unit): a payload plus a temporal profile, execution window, runtime, required validator capability, fee policy, reservation terms, verification mode, and fallback. Execution objects are placed on the host's execution lattice (RN-05) - indexed by execution quantum, temporal class, capacity allocation, and validator capability - and the scheduler decides *where*, *when*, and *by whom* each object executes.

## 8. Fee and runtime virtualization

The host chain prices *physical* resources; each Virtual Chain sets its own *user-facing* fee policy, and the host translates between them.

| Virtual Chain | User-facing fee policy |
|---|---|
| Exchange | maker / taker |
| Settlement | reserved-capacity subscription |
| Gaming | flat periodic fee |
| Institutional | reserved capacity |
| General EVM | EIP-1559-style gas |

This is **fee virtualization** - heterogeneous service models mapped onto one shared resource-accounting model - rather than many isolated fee markets. It satisfies the RN-07 reducibility invariant only if each policy compiles down to the host's per-slot resource accounting; policies that cannot are not admissible. Runtimes are virtualized the same way: different domains may run the EVM, Move, an exchange engine, a settlement engine, or a domain-specific runtime, all scheduled under one consensus.

## 9. Cross-domain execution and fault isolation

Because Virtual Chains share one settlement layer, they retain atomic interaction, shared liquidity, unified state, and low-risk cross-domain communication - the composability that independent Layer-1s give up. Each domain runs inside an isolated execution context, so failures stay local; the host provides resource, execution, and accounting isolation plus validator accountability.

## 10. Design principles

- **Consensus non-duplication.** Do not recreate consensus merely to change execution behavior.
- **Minimum necessary sovereignty.** An application should take only the sovereignty it actually needs.
- **Shared security.** Virtual Chains inherit the host's security.
- **Programmable execution.** Execution policy is programmable; consensus is not.
- **Temporal awareness.** Time is a first-class scheduling resource (RN-01, RN-05, RN-07).
- **Economic neutrality.** The host prices resources; Virtual Chains choose service models; differentiation is by declared characteristic, never by identity.

## 11. Relationship to existing systems and to the TLM notes

Several systems already show pieces of this. **Hyperliquid's HyperCore** (RN-03, RN-08 sec. 7) runs a specialized exchange execution environment alongside HyperEVM under one HyperBFT consensus - a concrete two-domain precursor. **Monad** (RN-06) is a high-performance EVM execution substrate a host could use inside a domain. **Aptos** (RN-08 sec. 5) contributes Block-STM, a parallel data-plane executor beneath a temporal control plane. **Ethereum** supplies the neutral shared settlement and fee-market foundation. Virtual Chains generalize the HyperCore pattern - differentiated execution under shared consensus - into a programmable framework, with the **Temporal Liquidity Market as the control plane** (RN-07) that admits, prices, and schedules across domains.

Within the TLM notes, RN-09 is the *system-architecture* view: RN-01/02 supply the demand representations, RN-04 the service classes, RN-05 the lattice substrate, RN-06 an execution engine and the networking framing, RN-07 the layered control plane, and RN-08 the comparative survey that motivates the design. (See the note below on numbering.)

## 12. Open problems

Validator assignment and capability discovery; proof generation and verification overhead; cross-domain atomicity across different runtimes and fee policies; temporal scheduling algorithms; the fee compiler (reducing each domain's policy to host accounting); runtime interoperability; resource and fault isolation guarantees; execution-object encoding; fairness and minimum service for ordinary traffic; incentive compatibility and truthful profile revelation; and centralization risk from specialized (rare-hardware) virtual validators.

## 13. Positioning

The framing shifts the question from *"how many Layer-1 chains should exist?"* to *"how much sovereignty does an application actually need?"* An application that needs only execution differentiation should inherit shared consensus and obtain a programmable execution environment as a Virtual Chain. TLM is not another Layer-1; it is the control plane that makes this virtualization possible.

---

## References

[1] TLM Research Notes: RN-01 (Temporal Execution Profiles), RN-02 (Protocol-visible Temporal Abstraction), RN-03 (Hyperliquid case study), RN-04 (Temporal Execution Services / service classes), RN-05 (Supply-side granularity; the execution lattice), RN-06 (Monad; the OS->networking framing and network-slicing analogy), RN-07 (Layered control architecture), RN-08 (Modern blockchains through the TLM lens).

[2] Hyperliquid documentation - HyperCore / HyperEVM under shared HyperBFT consensus. https://hyperliquid.gitbook.io/hyperliquid-docs

[3] Network slicing over SDN/NFV (5G) - SLA-differentiated logical networks over shared infrastructure. (See RN-06 [8].)

[4] Monad documentation (execution substrate). https://docs.monad.xyz/ | Aptos documentation (Block-STM). https://aptos.dev/

---

*Note on numbering (not part of the note).* This is **RN-09** in the actual series (RN-01...RN-08 as listed in [1]). An earlier "My Comments" draft proposed a different RN-01...RN-08 mapping (e.g., "RN-02 = Temporal Liquidity," "RN-08 = Virtual Chains"); that mapping does not match the existing notes and has been dropped to avoid renumbering. If a re-organization of the series is wanted, it should be decided deliberately and applied across all notes at once.
