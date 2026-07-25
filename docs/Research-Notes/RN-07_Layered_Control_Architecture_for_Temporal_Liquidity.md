---
id: RN-07
title: "A Layered Control Architecture for Temporal Liquidity: Multi-Timescale Control for Blockchain Execution Markets"
version: v0.1
status: "Public draft — research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: July 24, 2026
sourcing: >
  Networking precedents verified July 2026 against the O-RAN literature (Polese et al.,
  IEEE COMST 2023) and the multi-timescale optimization-decomposition line. Corrections
  and primary-source pointers welcome.
---

# RN-07 — A Layered Control Architecture for Temporal Liquidity

## 0. Thesis, in one line

Temporal Liquidity is inherently a **multi-timescale** problem: some decisions (capacity, forward pricing, reserves) are optimized *globally over many slots*, while execution must remain *simple and deterministic within one slot*. Borrowing a single control/data-plane split (as networking did with SDN) is not enough. The right structure is the one modern networking has since evolved into — **temporally layered control**: a slow global control plane, a fast local control layer, and a deterministic data plane, closed by a feedback loop. This note proposes that architecture for TLM and states the invariant that makes it deployable.

---

## 1. Why TLM needs an architecture, not just a mechanism

The TLM notes so far supply a demand object (Temporal Liquidity), demand representations (RN-01/02), execution services (RN-04), a supply substrate (RN-05), and a supply-side case study (RN-06). What they have not yet stated is *where each decision lives*. That gap matters because TLM's decisions span very different timescales:

- **Multi-slot / global.** How much capacity to allocate to a class over the next N slots; the forward-vs-spot price curve; a temporal-liquidity reserve's budget; horizon admission.
- **Per-slot / local.** Which transactions to admit into which class this slot; class assignment; a preconfirmation or commitment.
- **Intra-slot / real-time.** The actual ordering and execution of transactions under strict slot constraints.

A design that computes a global, multi-slot optimum but then demands global coordination *inside* a slot will not survive: it re-imports the latency, centralization, and extraction surface that TLM exists to avoid. The architecture must keep the fast path simple while still coordinating slow, global structure. That is a control-systems problem, and it has a known shape.

---

## 2. The four planes

```
        Demand-description plane            applications declare temporal
        (intent / TEP / TDP)                characteristics: duration,
                 |                          intensity, variability,
                 v                          flexibility, deadline
   +-----------------------------+
   |      CONTROL PLANE          |
   |                             |
   |   Slow / global control     |   multi-slot: capacity allocation,
   |   (many slots)              |   forward/spot curve, reserve,
   |          |                  |   fee-parameter setting, admission
   |          v                  |
   |   Fast / local control      |   per-slot / few-slot: admission,
   |   (one / few slots)         |   class assignment, commitments
   +-----------------------------+
                 |  (per-slot parameters only)
                 v
        Execution / data plane              builders & validators:
        (one slot, deterministic)           immediate ordering + execution
                 |                          under strict slot constraints
                 v
        Realized delay / congestion / capacity
                 |  (telemetry, closed loop)
                 +----------------> back to the control plane
```

- **Demand-description plane.** Applications communicate temporal characteristics — stream duration, intensity, arrival variability, execution flexibility, deadline/delay tolerance. This is the intent interface (RN-01's Temporal Execution Profile, RN-02's protocol-visible representation).
- **Control plane, slow/global layer.** Optimizes structure that only makes sense across many slots: capacity allocation per class, the forward/spot price curve, the temporal-liquidity reserve's budget, admission over a horizon, fee-parameter setting.
- **Control plane, fast/local layer.** Bounded, near-term decisions: admit this transaction, assign it a class, issue a per-slot commitment/preconfirmation — under policy handed down by the slow layer.
- **Execution/data plane.** Builders and validators order and execute within one slot, deterministically, under strict constraints (RN-05's substrate). It carries *no* global policy.
- **Feedback.** Realized delay, congestion, and capacity are measured and returned to the control plane, closing the loop. This is what makes TLM a control system rather than a one-shot pipeline.

---

## 3. The precedent: networking evolved past control/data separation

The two-plane control/data split (RN-06 §2.2) was not the end of networking's architecture; it was a stage. The field has since converged on **multi-timescale, hierarchical control**, which is the structure above.

**O-RAN's control hierarchy** [1] is the clearest instance. It defines three control loops by timescale:

| Layer | O-RAN component | Timescale | Role |
|---|---|---|---|
| Slow / global | **Non-RT RIC** | ≥ 1 s | policy, optimization, ML training over many elements |
| Fast / local | **Near-RT RIC** | 10 ms – 1 s | closed-loop control: resource management, **slicing** |
| Real-time | **DU scheduler / dApps** | < 10 ms (per-TTI) | deterministic scheduling, kept *out* of the slow loops |

The key detail: O-RAN **deliberately excludes** per-TTI scheduling from the closed control loops, because real-time decisions "are not compatible with closed-loop control." That is the discipline TLM needs — *slot-level ordering must not depend on global, multi-slot coordination.*

**A formal backbone.** The pattern is not merely operational. "Optimization decomposition across timescales" [2] formalizes it: decompose a global control problem *temporally* into a slow centralized controller (global view, aggregate flow level) and fast local controllers (data-stream level), each solving a local problem — with data-plane fast mechanisms bridging to slow convergence. TLM's slow/fast control split is an instance of this decomposition.

**Ethereum already has a degenerate case.** EIP-1559's base fee is a *slow controller emitting a single per-block scalar*: a congestion signal integrated over recent blocks, applied locally by each block with no in-slot coordination. TLM generalizes this one-parameter controller to a richer, multi-dimensional control plane — but the compilation pattern (slow control → per-slot scalar) is already in production and proven neutral.

---

## 4. Mapping the notes onto the planes

| Plane | TLM component | Existing note |
|---|---|---|
| Demand-description | Temporal Execution Profile / protocol-visible temporal representation | RN-01, RN-02 |
| Slow / global control | capacity allocation, forward/spot curve, temporal-liquidity reserve, fee-parameter setting | Overview (open problems); reserve is an open research direction |
| Fast / local control | temporal service classes, admission, class assignment, preconfirmation/commitment | RN-04 |
| Execution / data plane | quantum lattice, deterministic sub-slot ordering, per-slot execution | RN-05 |
| Cross-cutting | supply-side substrate & engine (Monad-class), the OS→networking framing | RN-06 |

The architecture is thus not new machinery; it is the **frame that unifies the notes already written** — and it tells us which plane each future mechanism belongs in.

---

## 5. The central result: the reducibility (compilation) invariant

The architecture is only useful if it has a sharp admissibility criterion. Here it is:

> **Reducibility invariant.** A control decision computed over multiple slots is *admissible* only if it compiles to a bounded set of **per-slot parameters** that the data plane applies **locally, deterministically, and without global coordination within the slot.**

Equivalently: every slow, global TLM mechanism must expose a **compilation target** — the per-slot scalar, codepoint, quota, or commitment the builder/validator applies with no further global computation. If a mechanism cannot be reduced to such a target, it is not deployable as a neutral protocol feature, because it would require in-slot global coordination — reintroducing latency, centralization, and extraction surface.

**Why this is the right invariant.** It is the union of three established lessons: the **end-to-end argument** (keep application semantics out of the fast path), **core-stateless fair queueing** (rich differentiation without per-flow state in the core), and O-RAN's **exclusion of real-time scheduling from closed loops**. All three say the same thing: the data plane stays simple; intelligence lives in slower layers and reaches the fast path only as a compiled parameter.

**Compilation examples (the invariant is constructive, not just a filter):**

| Slow/global decision | Compiles to (per-slot, local) |
|---|---|
| Forward capacity curve | a per-slot target / base-fee scalar (EIP-1559-style) |
| Temporal service class (policy) | a per-transaction codepoint the builder applies (DiffServ / SRv6 analog) |
| Temporal-liquidity reserve (multi-slot budget) | a per-slot surcharge/subsidy scalar; budget balance enforced over the horizon by the slow layer |
| Horizon admission | a per-slot admission quota / token |

**A feasibility filter for the reserve.** This gives the temporal-liquidity reserve — the project's furthest-reaching supply-side idea — a concrete deployability test: *design the slow, multi-slot optimization, then prove it reduces to a per-slot surcharge/subsidy parameter with horizon-level budget balance.* If it does, it is architecturally admissible; if it does not, it is (as stated) not yet deployable, and the research task is to find a reduction. The invariant converts an open-ended mechanism question into a well-posed one.

---

## 6. The design question, restated as a partition

RN-06 §2.2 posed the question: *which TLM decisions must be computed globally over many slots, and which must be executable locally within one slot?* The architecture answers it as a partition, disciplined by the invariant:

- **Global / slow (control plane, Non-RT-analog):** anything whose optimum depends on state across many slots — capacity, forward pricing, reserves, horizon admission. Output: per-slot parameters only.
- **Local / fast (control plane, Near-RT-analog):** anything decidable within one or a few slots from handed-down policy — admission, class assignment, commitments.
- **Real-time (data plane):** ordering and execution, deterministic, policy-free.

The partition is not a matter of taste: a decision belongs in the slowest layer whose timescale its optimum requires, and it may cross into the fast path **only** as a compiled parameter (the invariant). This is the formulation RN-06 gestured at — and it is materially stronger than borrowing DiffServ vocabulary, because it yields a testable admissibility criterion for every proposed mechanism.

---

## 7. Why this matters

- **It gives TLM a structural foundation.** The demand object, representations, classes, substrate, and reserve are now one architecture with defined interfaces, not a set of related ideas.
- **It preserves neutrality and simplicity where they must be preserved.** By construction the data plane stays deterministic and policy-free; all expressiveness is pushed to slower layers and reaches execution only as coarse, local parameters — the same discipline that let DiffServ and SRv6 deploy.
- **It disciplines mechanism design.** Every Phase-2 mechanism (generalized tiered fees, temporal auctions, the reserve) now has a home plane and a reducibility test before it is taken seriously.
- **It is honest about feasibility.** Some attractive global optima may have no per-slot reduction; the invariant surfaces that early, rather than after a mechanism is proposed.

---

## 8. Open problems

- **Reduction theorems.** For which classes of multi-slot objectives does a per-slot compilation exist, and with what approximation loss? (The core theoretical question the invariant raises.)
- **Reserve reduction.** Does a budget-balanced temporal-liquidity reserve admit a per-slot surcharge/subsidy compilation with bounded horizon error?
- **Stability of the closed loop.** With realized-metric feedback, when is the control system stable (no oscillation) — the temporal analog of EIP-1559's known base-fee dynamics?
- **Interface minimality.** What is the smallest per-slot parameter set (the "codepoint budget") that supports the service classes of RN-04 without bloating the data plane?
- **Incentive compatibility across planes.** Do the slow/fast layers' decisions remain incentive-compatible and OCA-proof when compiled to local parameters, or do the impossibilities bind at the compilation boundary?

---

## 9. Relationship to other notes

RN-07 is the architectural spine. RN-01/02 populate the demand-description plane; RN-04 populates the fast-local control layer (service classes) and RN-05 the data plane (the substrate on which per-slot ordering is deterministic); RN-06 analyzes a supply-side engine (Monad) that sits inside the data plane and motivates the OS→networking framing this note completes. The temporal-liquidity reserve (Overview open problems) is the flagship slow-global mechanism whose admissibility this note makes testable.

---

## References

[1] Polese, M., Bonati, L., D'Oro, S., Basagni, S. & Melodia, T. *Understanding O-RAN: Architecture, Interfaces, Algorithms, Security, and Research Challenges.* IEEE Communications Surveys & Tutorials 25(2), 2023. arXiv:2202.01032. *(Non-RT RIC ≥1s; Near-RT RIC 10ms–1s; per-TTI scheduling kept out of closed loops.)*

[2] *Thinking Fast and Slow: Optimization Decomposition Across Timescales.* arXiv:1704.07785. *(Temporal decomposition of a global control problem into slow-global and fast-local controllers.)*

[3] Blake, S. et al. *An Architecture for Differentiated Services (DiffServ).* RFC 2475, 1998. — coarse, stateless, in-band service marking.

[4] Stoica, I., Shenker, S. & Zhang, H. *Core-Stateless Fair Queueing.* ACM SIGCOMM, 1998. — rich differentiation without per-flow state in the core.

[5] Saltzer, J. H., Reed, D. P. & Clark, D. D. *End-to-End Arguments in System Design.* ACM TOCS 2(4), 1984.

[6] Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals, 2019. — base fee as a slow controller emitting a per-block scalar.

[7] TLM Research Notes: RN-01 (Temporal Execution Profiles), RN-02 (Protocol-visible Temporal Abstraction), RN-04 (Temporal Execution Services), RN-05 (Supply-side Heterogeneity and Temporal Granularity), RN-06 (Monad Through the Temporal-Liquidity Lens).

*Sourcing note: networking precedents cited to the survey/primary literature; corrections and primary-source pointers welcome.*
