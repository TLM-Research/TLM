# Foundation Statement — Part II: Conceptual Framework

**Version:** 1.2
**Status:** Public Draft

Part II is the intellectual core of the Foundation. It sets out the principles that discipline the inquiry and the model-first methodology that orders it. It proposes no mechanism; it establishes how any future mechanism will be reasoned about. Throughout, **Temporal Liquidity** is the umbrella concept defined in Part I §2 and elaborated in the [Temporal Liquidity](./Temporal-Liquidity.md) note.

---

# 5. Design Principles

## 5.1 Participant and protocol neutrality

The protocol should treat participants symmetrically and remain neutral across applications. Where temporal characteristics are priced differently, the differentiation must be across the *characteristic* (a public, deterministic rule, as the EIP-1559 base fee is a deterministic function of congestion), never across *identity*. Neutral-but-differentiated is the load-bearing property: horizons or urgency classes may be priced differently; participants may not.

## 5.2 Information before decisions — a bounded claim

TLM distinguishes exposing protocol-visible *information* from making decentralized *decisions*. This distinction is real but **not absolute**: the choice of what becomes visible is itself part of the protocol's message space, and in mechanism design the message space is part of the mechanism (the revelation principle). Choosing a representation for a temporal characteristic already privileges some strategies. TLM therefore adopts a bounded claim rather than a clean dichotomy:

> Protocol evolution should expose economically meaningful information while minimizing unnecessary intervention in decentralized participant optimization — acknowledging that the representation is itself a design choice with incentive consequences.

## 5.3 Positive-sum: creation, not redistribution

The framework claims a positive-sum effect only in a specific sense, and separates two channels that are easily conflated. **Surplus creation** — improved scheduling and utilization, and the accommodation of previously suppressed flexible demand — is what the principle asserts. **Surplus redistribution** — intertemporal price discrimination and transfers among existing participants — is not. Only creation motivates the principle, and whether measurable creation exists is a research hypothesis, not an assumption.

## 5.4 Simplicity and coarseness

The Internet already ran this experiment: per-flow reservation state (IntServ/RSVP) failed to scale, while coarse, stateless class marking (DiffServ) deployed, and core-stateless designs later showed that expressive service differentiation is achievable without per-flow state in the core. TLM inherits the lesson and favors **coarse, protocol-simple** temporal abstractions over application-specific semantics. One honest tension: coarseness is cleanest at the *transaction* level (a small descriptor), whereas *stream-level* characteristics such as predictability and continuity may require carrying more state. Reconciling stream-level richness with the coarseness principle is an explicit open problem, not a solved one.

## 5.5 Decentralization

Any exposed information or mechanism must preserve permissionless participation and must not systematically advantage the actors best able to forecast or exploit temporal demand — a risk made concrete by production time-priority markets that centralized around sophisticated participants.

---

# 6. Model-first Methodology

TLM proceeds in a deliberate order — concepts before mechanisms:

1. **Model** the market's economically meaningful variables.
2. **Decide** which of them merit protocol visibility.
3. **Design representations** for the ones that do.
4. **Design mechanisms** that coordinate those representations.

A five-layer model organizes the discussion — Economic → Representation → Coordination → Protocol → Execution — but it is an **analytical lens, not a fixed architecture**; its boundaries may evolve as protocol research progresses, and (as the OSI-vs-TCP/IP history warns) layered models leak.

---

# 7. Three Notions of Time

Precision requires distinguishing three times. **Physical time** is wall-clock ("execute before market close"). **Protocol time** is the discrete structure of slots and blocks. **Execution time** is the realized opportunity at which a transaction is included and ordered. Temporal characteristics are defined over *execution opportunities*, but applications express their needs in *physical* time, and the mapping between them is stochastic — congestion-dependent and subject to reorganization. This distinction (which Part I forward-references) is why "urgency" and "latency" are not interchangeable, and why execution priority — position *within* a slot — is a distinct characteristic from delay tolerance across slots.

---

# 8. Relationship to Transaction Fee Mechanism Design

Stated formally, exposing temporal characteristics **enlarges the message space** of the transaction fee mechanism — from a scalar bid to a vector that also carries temporal information. Roughgarden's transaction-fee-mechanism framework is therefore the natural apparatus for evaluating any TLM mechanism: its incentive-compatibility notions (dominant-strategy incentive compatibility, myopic-miner incentive compatibility, off-chain-agreement proofness) give the "truthful revelation" question an exact statement, and its impossibility results are a discipline — a larger message space can make these guarantees *harder* to hold jointly, not easier. In this sense TLM is a **multidimensional transaction fee mechanism** problem: extending fee-market design from pricing one resource to coordinating a demand vector that also expresses when and in what order execution is wanted.

The closest existing instance is the *tiered* transaction-fee mechanism of Kiayias, Koutsoupias, Lazos & Panagiotakos (2023, arXiv:2304.06014): it prices a single temporal dimension — urgency — keeps low-urgency transactions inclusive without sacrificing revenue, and shows that EIP-1559 is not inclusive. TLM credits this as the formal urgency-axis precedent and generalizes it to the multidimensional umbrella; where it extends the work is in the other temporal dimensions, in the create-versus-redistribute distinction (their revenue-neutrality runs through price discrimination, while the admitted diversity is created surplus), and in the extraction-resistance problem they do not treat. That last gap is specific: the tiered analysis covers incentive-compatibility around price, inclusion, and off-chain-agreement collusion, but not the front-running / MEV surface created by the *observability* of the disclosed urgency — a surface that grows with the expressiveness of the signal, and that TLM therefore treats as a first-class constraint rather than a downstream concern.

The formal backbone here is the second pillar of TFM theory, Chung & Shi's *Foundations of Transaction Fee Mechanism Design* (SODA 2023): under contention, no fee mechanism jointly satisfies user- and miner-incentive-compatibility and collusion- (side-contract-) proofness, and incentive-compatibility against miner–user coalitions forces zero revenue. That impossibility bounds how much a *plain* temporal mechanism can achieve. TLM's answer follows Shi, Chung & Wu, *What Can Cryptography Do for Decentralized Mechanism Design?* (ITCS 2023): cryptography can circumvent several plain-model impossibilities — the template for making temporal disclosure safe enough to price, and the closest prior work to TLM's own extraction-resistance approach.

---

# 9. Evaluation Criteria

Future mechanisms should be judged against common criteria rather than in isolation: economic efficiency, decentralized-coordination quality, protocol simplicity, participant neutrality, incentive compatibility, resistance to strategic manipulation, privacy, and deployability. These criteria are what let the framework adjudicate between candidate designs; Part III develops the empirical and falsification methodology that accompanies them.

---

# 10. The Counter-Thesis and the Central Question

Making more information protocol-visible does **not** automatically improve markets. The information-economics literature shows the opposite can hold — public information can destroy gains from trade (Hirshleifer; Milgrom–Stokey) — and in an adversarial mempool, revealing a temporal characteristic early is exactly what exposes it to extraction. Additional information may improve coordination, but it may also reduce privacy, increase strategic behavior, concentrate the market, or add protocol complexity. The framework therefore does not ask "how much temporal information can we expose," but:

> **Which economically meaningful temporal information should become protocol-visible, under what guarantees, and with what tradeoffs?**

The concrete representations this implies — transaction-level and stream-level temporal profiles — are developed in the Research Notes before being folded back into the Foundation, so the constitutional document stays ahead of unsettled terminology rather than pinned to it.
