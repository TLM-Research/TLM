
# Related Work

**Version:** 2.0
**Release:** TLM Public Release 1 (Draft Revision)
**Status:** Living Document

---

# Purpose

Temporal Liquidity Market (TLM) is not intended as another isolated Ethereum proposal.

Instead, it sits at the intersection of several mature research disciplines that have studied how scarce resources are allocated under heterogeneous demand.

Ethereum provides the motivating application, but the intellectual foundations of TLM extend well beyond blockchain.

This document organizes the literature by research community rather than by protocol feature.

---

# 1. Distributed Systems and Scheduling

Long before blockchain, distributed systems researchers recognized that execution timing is itself a resource.

Research in:

- real-time scheduling,
- deadline scheduling,
- slack and laxity,
- queueing systems,
- operating systems,

demonstrates that different jobs possess different temporal characteristics.

## Relationship to TLM

TLM inherits the observation that execution timing has economic and computational significance.

Its research question differs, however:

> **What temporal information should decentralized participants communicate before scarce execution opportunities are allocated?**

Rather than importing scheduling policies directly into blockchain, TLM investigates whether decentralized execution markets require new abstractions for representing temporal demand.

---

# 2. Network Resource Allocation

Network protocols have long explored whether applications should communicate richer information about their traffic.

Representative themes include:

- congestion control,
- Quality of Service (QoS),
- IntServ and RSVP,
- DiffServ,
- deadline-aware networking,
- network utility maximization.

These systems illustrate both the benefits and costs of exposing application-level information to network infrastructure.

## Relationship to TLM

This literature provides an important caution as well as inspiration.

TLM does not assume that more protocol-visible information is always better.

Instead it asks:

- Which temporal information is economically meaningful?
- Which information should remain private?
- What level of expressiveness preserves scalability and decentralization?

---

# 3. Mechanism Design and Market Design

Mechanism design studies how strategic participants communicate information before resources are allocated.

Auction theory, revelation mechanisms, incentive compatibility, and market design all investigate the relationship between information, incentives, and efficient allocation.

## Relationship to TLM

TLM builds upon this tradition by asking whether **temporal information** should become part of the protocol-visible message space.

This shifts attention from purely price-based communication toward richer—but carefully constrained—expressions of demand.

Truthful revelation of temporal preferences remains an open research question rather than an assumption.

### Transaction Fee Mechanism Design (Roughgarden)

The most direct formal anchor is Tim Roughgarden's framework for **transaction fee mechanism design** (Roughgarden, 2021; JACM 2024; and the 2020 economic analysis of EIP-1559). Stated in its terms, TLM is a proposal to enlarge the **message space** of the fee mechanism — from a scalar bid to a structured object that also carries temporal characteristics — which makes Roughgarden's framework the natural home for evaluating it.

Three elements transfer directly:

- **Incentive-compatibility vocabulary.** Roughgarden evaluates mechanisms against dominant-strategy incentive compatibility (DSIC), myopic miner incentive compatibility (MMIC), and off-chain-agreement (OCA) proofness. TLM's core concern — that revealing temporal flexibility invites extraction — is precisely the question of whether a temporally augmented mechanism remains DSIC and OCA-proof. This gives the "truthful revelation" open question above an exact formal statement.
- **Evaluation criteria.** He proves EIP-1559 is DSIC (outside demand spikes), MMIC, and OCA-proof. These are the yardstick against which any future TLM mechanism should be measured, and they supply the evaluation criteria the Foundation Statement calls for.
- **Impossibility as discipline.** His results show these guarantees are already in tension for a one-dimensional fee. Enlarging the message space with temporal information can make simultaneous DSIC / MMIC / OCA-proofness harder rather than easier — the formal counterpart to the caution (from the networking literature above) that more protocol-visible information is not automatically beneficial.

In this framing, TLM is a **multidimensional transaction fee mechanism**: extending fee-market design from pricing one resource (blockspace, by willingness-to-pay) to coordinating a demand vector that also expresses when and in what order execution is wanted. This connects TLM's *execution priority* dimension to Roughgarden's analysis of tips and block-producer incentives — where ordering is exactly where MMIC and OCA-proofness bind, and where an ordering side-market such as Arbitrum's Timeboost (§5) tends toward centralization. Roughgarden's line is complementary to TLM (it evaluates mechanisms; TLM proposes what to coordinate), not competing.

### TFM impossibility and the cryptographic escape hatch (Chung & Shi)

The second pillar of formal TFM theory is Chung & Shi, *Foundations of Transaction Fee Mechanism Design* (ePrint 2021/1474; SODA 2023). Their central result is an **impossibility**: under contention, no fee mechanism can jointly satisfy user incentive-compatibility (UIC), miner incentive-compatibility (MIC), and side-contract-proofness (SCP, i.e. resistance to miner–user collusion) for any coalition size c ≥ 1; and any mechanism incentive-compatible against miner–user coalitions must have *zero* miner revenue. This sharpens the "impossibility as discipline" point above and — because it is centered on **collusion / side-contracts** — bears directly on TLM's extraction concern: enlarging the message space with temporal information only makes these joint guarantees harder.

Crucially for TLM's answer to that problem, Shi, Chung & Wu, *What Can Cryptography Do for Decentralized Mechanism Design?* (ITCS 2023; arXiv:2209.14462), show that **cryptography** (commitments, MPC, trusted hardware) can *circumvent* several of these plain-model impossibilities, enabling mechanisms that are otherwise unattainable. This is the closest prior work to TLM's own extraction-resistance thesis — making disclosure safe with cryptography so a richer, temporally expressive mechanism becomes feasible. TLM inherits this line directly: the impossibility results bound what a plain temporal mechanism can achieve, and the cryptographic results are the template for escaping those bounds.

---

# 4. Financial Economics and Time-Differentiated Demand

Many economic systems already coordinate heterogeneous temporal preferences.

Examples include:

- congestion pricing,
- peak-load pricing,
- electricity demand response,
- interruptible-load contracts,
- cloud spot and preemptible computing markets.

These markets demonstrate that users frequently exchange temporal flexibility for economic benefit.

## Relationship to TLM

Temporal Liquidity is conceptually closest to these markets.

Rather than introducing a new economic principle, TLM investigates how similar ideas may apply within decentralized execution markets while respecting blockchain-specific constraints.

---

# 5. Ethereum Execution Markets

Ethereum provides the primary motivating environment for TLM.

Relevant work includes:

- EIP-1559 and transaction fee markets,
- PBS and builder specialization,
- ePBS,
- MEV and execution markets,
- execution rights and future block markets,
- intents and richer order expression,
- account abstraction,
- time-based transaction ordering and latency auctions (e.g., Arbitrum Timeboost),
- empirical studies of execution delay.

## Relationship to TLM

TLM complements these developments by stepping back one level.

Rather than proposing another execution mechanism, it asks:

> **What economically meaningful temporal information should applications communicate before execution opportunities are allocated?**

Existing Ethereum research explores increasingly sophisticated execution mechanisms.

TLM focuses on the economic information those mechanisms may eventually coordinate.

### Time as Execution Priority: Arbitrum Timeboost

Arbitrum's **Timeboost** is the closest existing instance of pricing *time itself* as a protocol-visible execution variable. In each round, a sealed-bid second-price auction sells control of an "express lane"; the winning controller is sequenced immediately, while all other transactions receive a fixed artificial delay (200 ms) before sequencing. Priority is therefore not merely willingness-to-pay — it is literally a **time advantage**, i.e. sensitivity of execution value to intra-slot ordering position.

Timeboost is directly relevant to TLM in two opposite ways, and both should be carried honestly:

- **Validation.** Capponi & Zhu (2026), *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains*, argue that auctioning a time advantage can **reduce the wasteful latency arms race** (deadweight spending on colocation and faster hardware). This is a concrete, cited instance of temporal coordination creating social surplus by removing waste rather than redistributing value — the strongest available empirical support for TLM's positive-sum hypothesis. It also establishes that intra-slot ordering is an economically meaningful temporal characteristic of demand, distinct from delay-tolerance across slots.
- **Caution.** Independent empirical analysis of Timeboost (*The Express Lane to Spam and Centralization*, arXiv:2509.22143) reports that the express lane drove spam and centralization, with a sophisticated controller dominating the lane. This is a live instance of the central risk in TLM's threat model: exposing a protocol-visible temporal variable can advantage the participants best able to exploit it. Timeboost thus demonstrates both that time-as-priority is real and valuable, and that naive coordination of it can centralize.

Note the two references are distinct: Capponi & Zhu is the theory-and-evidence paper; the "Express Lane to Spam and Centralization" analysis is by a separate group. TLM treats Timeboost as a **mechanism instance** that prices one temporal characteristic (execution priority); the framework's concern is the underlying demand characteristic and its representation, not the specific auction.

### Tiered / urgency-differentiated fees: the closest formal precedent

Kiayias, Koutsoupias, Lazos & Panagiotakos, *Tiered Mechanisms for Blockchain Transaction Fees* (arXiv:2304.06014, 2023; Springer, 2024), is the closest existing formalization of TLM's core intuition. They model blockchain traffic diversity, argue that EIP-1559 is **not inclusive**, and give a tiered pricing mechanism that keeps prices low for **low-urgency** transactions — admitting a more diverse set of transaction types — while showing that revenue need not fall, because the lower low-urgency prices can be covered from high-urgency ones through the mechanism's price-discrimination ability.

In TLM's language this is a **mechanism for a single temporal dimension — urgency (delay-tolerance)**: effectively a worked "Phase 2" instance of the TLM thesis on one axis. TLM credits it as prior art and builds on it in three ways.

- **From one axis to the umbrella.** Their tiering prices urgency; Temporal Liquidity is the umbrella over *several* temporal characteristics — predictability, execution priority, execution windows, continuity — of which urgency/delay-tolerance is one. TLM's contribution is the multidimensional object, and the model-first framing that precedes any single mechanism.
- **Creation vs redistribution, made precise.** Their revenue-neutrality runs through *price discrimination* (high-urgency covering low-urgency) — a redistribution channel — while the *inclusivity / diverse traffic entering* is created surplus. TLM leads with the creation claim and acknowledges the discrimination channel; their result is useful evidence that the two coexist.
- **Extraction-resistance (the key gap).** Their analysis covers incentive-compatibility around price, inclusion, revenue, and off-chain-agreement collusion (OCA-proofness), but not the attack surface created by the *observability* of the disclosed urgency — front-running / MEV, or collusion around the visible tier. (Their remark that users choose from a menu "without revealing their value" is the revelation-principle sense — not shielding the choice from adversarial observation in the mempool.) That surface grows with the *expressiveness* of the disclosure, so it is more acute for TLM's richer, multidimensional signals than for coarse price-based tiers — which is exactly why TLM makes extraction-resistance a first-class constraint rather than a downstream concern.

TLM therefore positions this work not as a competitor but as the formal urgency-axis foundation it generalizes — and a natural point of collaboration.

---

# 6. Position of TLM

The contribution of TLM is not another scheduler, auction, or fee mechanism.

Its proposed contribution is a conceptual framework connecting ideas that have historically evolved in separate research communities.

| Research Area | Traditional Question | TLM Perspective |
|---------------|----------------------|-----------------|
| Distributed Systems | Which job should run first? | What temporal information should jobs communicate? |
| Network QoS | Which flows deserve priority? | Which temporal preferences belong in the protocol? |
| Mechanism Design | What messages should agents send? | Which temporal information is economically meaningful? |
| Financial Economics | How do markets value flexibility over time? | Can decentralized execution markets coordinate that flexibility? |
| Ethereum | How should execution markets allocate blockspace? | Should protocol-visible temporal information become part of that allocation? |

---

# Positioning

TLM should therefore be viewed neither as a replacement for Ethereum research nor as a direct extension of any single discipline.

Instead, it is an interdisciplinary research program positioned at the intersection of:

- distributed systems,
- network resource allocation,
- mechanism design,
- financial economics,
- blockchain protocol research.

Ethereum serves as the motivating application through which these ideas can be investigated, evaluated, and potentially translated into future protocol mechanisms.

---

# Future Work

Future revisions of this document will include:

- formal academic citations,
- Ethereum Improvement Proposals (EIPs),
- primary papers from each discipline,
- complementary versus competing approaches,
- annotated bibliography,
- historical timeline of related ideas.

This document is intended to remain the canonical literature map for the TLM project.
