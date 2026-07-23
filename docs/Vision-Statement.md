# Temporal Liquidity Market (TLM)

## Vision Statement

**Version:** 1.4 (Draft)
**Release:** TLM Public Release 2 (PR2)
**Status:** Public Draft
**Last Updated:** July 2026

---

## A Vision for Temporal Market Design in Blockchain Protocols

# Background

Ethereum has transformed blockchain protocol economics through innovations such as EIP-1559 (Buterin et al., 2019), Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS; EIP-7732). These developments demonstrate that protocol design can improve decentralized coordination by making economically meaningful information visible through simple, deterministic protocol rules.

Temporal Liquidity Market (TLM) asks whether decentralized execution markets can benefit from making economically meaningful temporal characteristics of demand, in addition to price, visible through protocol-defined abstractions.

Rather than replacing Ethereum's architecture, TLM explores the next stage of decentralized market design.

---

# Beyond Price

Today's execution markets primarily coordinate demand through price.

Execution demand also possesses temporal characteristics that influence resource allocation.

**Temporal Liquidity** is intentionally used as an umbrella economic concept analogous to **market liquidity**.

Just as market liquidity is not a single quantity but a family of related properties (depth, immediacy, resiliency, and so on), Temporal Liquidity refers to the collection of economically meaningful temporal characteristics of execution demand that may influence decentralized market coordination.

Two clarifications keep the analogy precise:

- Temporal Liquidity characterizes **demand** (the properties of transactions and streams), whereas market liquidity characterizes a **market or asset**. The parallel is structural — both are umbrellas — not literal.
- Unlike market liquidity's dimensions, which tend to co-move as facets of a single underlying property, the temporal characteristics below may be **largely independent**. Temporal Liquidity is therefore best understood as a *category* of related-but-distinct properties rather than a single multidimensional measure.

These characteristics may include:

- **delay tolerance** — how execution value changes as execution is delayed across slots
- **predictability** — the degree to which future demand can be forecast before it arrives
- **execution priority** — sensitivity of execution value to ordering *within* a slot
- **execution windows** — bounded intervals in which execution is acceptable
- **continuity of demand** — sustained versus one-shot (spot) demand
- **deadlines** — hard cutoffs after which value drops sharply
- other temporal properties

A useful way to organize these is by **temporal granularity**:

| Scale | Characteristic | Question it answers |
|-------|----------------|---------------------|
| Intra-slot | execution priority / ordering | *Where in the sequence must I be?* |
| Inter-slot | delay tolerance, deadlines, execution windows | *How long can I wait, and until when?* |
| Multi-slot / stream | predictability, continuity | *How forecastable and sustained is my demand?* |

A second structural distinction cuts across the table: some characteristics are **declared preferences** the demand states (delay tolerance, windows, deadlines, priority), while others are **observed properties** others verify about the demand (predictability, continuity). These are represented and incentivized differently — declared preferences are what a market prices; observed properties are what can earn a coordination discount only if verified.

Individual research notes may investigate individual dimensions without implying separate top-level concepts.

The central question becomes:

> Can simple, protocol-visible temporal abstractions improve decentralized coordination while preserving neutrality and simplicity?

---

# Empirical Grounding

The premise that timing carries real, heterogeneous economic value is not assumed but empirically supported.

Zhao, in *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market*, estimates the cost of delaying transactions in the Ethereum fee market and shows that delay imposes a **measurable economic cost that varies across transactions**. This is direct evidence that delay tolerance is a real and heterogeneous temporal characteristic of demand rather than a modeling convenience — and it is an important validation for the TLM premise that temporal flexibility differs meaningfully across execution demand.

Complementary empirical work on EIP-1559 (Liu, Lu, Nayak, Zhang, Zhang & Zhao, 2022) shows that transaction-fee mechanism design measurably affects waiting times. Existing markets therefore already couple price and time — but only implicitly, compressed into a single scalar fee. TLM's question is whether making temporal characteristics *explicit* can coordinate that relationship more efficiently than pricing alone.

Together with the latency-race evidence discussed below, these results give TLM two independent empirical anchors — the cost of delay and the cost of ordering — rather than a single supporting case.

---

# Time as Execution Priority

Execution priority illustrates why these characteristics are genuinely *temporal* rather than merely restatements of willingness-to-pay.

Arbitrum's **Timeboost** makes the point concretely: it auctions control of an "express lane," and the winner is sequenced immediately while all other transactions incur a fixed artificial delay before sequencing. Here priority *is* time — a latency advantage — and the underlying demand characteristic is the sensitivity of a transaction's value to its ordering position within a slot.

TLM draws a deliberate line here. The **demand characteristic** (how much a transaction values being earlier in the sequence) belongs to Temporal Liquidity. The **auction that prices it** is a *mechanism*, one instantiation on a later rung of the concept → representation → mechanism ladder. Timeboost is thus a mechanism instance, not the concept itself; conflating the two would collapse execution priority back into price, since in Timeboost priority is literally purchased.

Timeboost is instructive in two opposite directions, and TLM carries both:

- It offers early evidence that coordinating temporal priority can **create surplus by reducing waste** — auctioning a time advantage can dampen the latency arms race rather than merely transfer value (Capponi & Zhu, 2026, *Auctioning Time to Mitigate Latency Races*).
- It also shows the hazard: independent analysis reports that the express lane drove spam and centralization, a concrete example of how exposing a protocol-visible temporal variable can advantage the participants best positioned to exploit it.

Both lessons motivate studying temporal characteristics carefully rather than exposing them naively.

---

# A Historical Perspective

Internet QoS demonstrated both the promise and the limitations of protocol-visible information.

Highly expressive reservation approaches (IntServ/RSVP) proved difficult to deploy at Internet scale, while lightweight traffic classifications (DiffServ) improved coordination within administrative domains but encountered strategic marking, incentive misalignment, and limited inter-domain trust.

Permissionless blockchains inherit similar challenges under stronger adversarial assumptions.

However, blockchain protocols introduce cryptoeconomic tools—including staking, auctions, and mechanism design—that were largely unavailable during the evolution of Internet QoS. Timeboost is one early demonstration that time itself can be coordinated through such tools, with both the benefits and the centralization risks that follow.

TLM asks whether these new tools fundamentally change what protocol-visible abstractions can achieve.

---

# Research Vision

TLM investigates Temporal Liquidity as a new dimension of decentralized market design.

Its objective is to establish a conceptual framework for understanding, representing, and evaluating economically meaningful temporal characteristics of execution demand rather than prescribing a particular protocol mechanism.

---

# Relationship to Transaction Fee Mechanism Design

TLM is, formally, a proposal to enrich the **message space** of Ethereum's transaction fee mechanism — from a scalar bid (fee/tip) to a structured object that also carries temporal characteristics. Tim Roughgarden's framework for transaction fee mechanism design (Roughgarden, 2021) is therefore the natural formal home for evaluating it, and it contributes three things TLM needs.

- **A vocabulary for truthful revelation.** Roughgarden evaluates fee mechanisms against dominant-strategy incentive compatibility (DSIC), myopic miner incentive compatibility (MMIC), and off-chain-agreement (OCA) proofness. TLM's central worry — that revealing temporal flexibility invites extraction — is precisely the question of whether a temporally augmented mechanism remains DSIC and OCA-proof. Roughgarden gives that worry an exact statement.
- **Ready-made evaluation criteria.** He shows EIP-1559 is DSIC (outside demand spikes), MMIC, and OCA-proof. Any TLM mechanism should be held to the same standard; these are the yardstick the framework's evaluation agenda calls for.
- **A discipline on optimism.** His impossibility results show these guarantees are already in tension for a *one-dimensional* fee. Enlarging the message space with temporal information can make simultaneous DSIC / MMIC / OCA-proofness harder, not easier — the formal counterpart to the caution that "more protocol-visible information is not automatically better," and a map of exactly which trade-offs to expect.

Seen this way, TLM is a **multidimensional transaction fee mechanism**: extending fee-market design from pricing one resource (blockspace, by willingness-to-pay) to coordinating a demand vector that also expresses *when* and *in what order* execution is wanted. Execution priority connects directly to Roughgarden's treatment of tips and block-producer incentives, where ordering is exactly where MMIC and OCA-proofness bite — which is also why an ordering side-market such as Timeboost tends toward centralization.

---

# Why Better Market Design Can Create Social Surplus

TLM is not motivated by transferring value from one participant to another, nor by asking the network to sacrifice efficiency in order to accommodate patient users.

Instead, the central hypothesis is that existing execution markets cannot fully coordinate certain economically valuable transactions because they expose only a limited set of demand information—primarily price.

As a result, some execution demand remains **unrealized**, not because the network lacks capacity, but because the market lacks sufficient expressiveness to coordinate it efficiently.

Surplus can arise through two complementary channels:

- **Unlocking suppressed demand** — allowing participants to communicate simple, protocol-visible temporal characteristics may enable execution opportunities that would otherwise never occur.
- **Removing coordination waste** — making a temporal characteristic explicit can dampen destructive competition for it. The latency arms race is the clearest example: participants currently spend real resources racing for ordering advantage, and coordinating time-as-priority can convert part of that deadweight loss into surplus (Capponi & Zhu, 2026).

There is already formal support for the first channel. Kiayias, Koutsoupias, Lazos & Panagiotakos (2023) show that a *tiered* fee mechanism, pricing by urgency, keeps low-urgency transactions cheap and admits a more diverse set of transactions than EIP-1559 — without necessarily sacrificing revenue. That is, in effect, the *urgency dimension* of Temporal Liquidity worked out as a mechanism; TLM generalizes it across the full set of temporal characteristics. Their result also sharpens the distinction below: the revenue-neutrality runs through price discrimination (a redistribution channel), while the *inclusion of diverse demand* is the created surplus.

In both cases the resulting social surplus comes from **better coordination**, rather than redistributing value among existing participants.

This distinction is fundamental to the TLM research program.

---

# Guiding Principles

- Build upon Ethereum's protocol evolution.
- Preserve decentralization and participant neutrality.
- Keep protocol rules simple, deterministic, and transparent.
- Separate protocol-visible information from protocol control.
- Distinguish a demand characteristic from the mechanism that prices it.
- Increase overall social surplus rather than merely redistribute existing value.
- Evaluate ideas under strategic, permissionless assumptions.

---

# Open Research Questions

- Which temporal characteristics belong within Temporal Liquidity?
- Which should become protocol-visible?
- How coarse should protocol-visible abstractions be?
- How should declared preferences and observed (verifiable) properties be treated differently?
- Under what conditions does temporal information create social surplus?
- How economically significant is temporally flexible demand?
- Can cryptoeconomic mechanisms overcome historical limitations observed in Internet QoS?
- Can protocol-visible temporal abstractions remain robust against strategic manipulation and centralization pressure?

---

# Conclusion

Ethereum demonstrated that protocol-visible economic information can improve decentralized coordination.

TLM extends that direction by asking whether **Temporal Liquidity**, understood as the collection of economically meaningful temporal characteristics of execution demand, can become another foundation for decentralized market design.

The project advances this as an open research agenda rather than a predetermined conclusion.

---

## References

- Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* Working paper, SSRN abstract 4436697 (updated 15 June 2026).
- Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. (2022). *Empirical Analysis of EIP-1559: Transaction Fees, User Experience, and Security.* Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (CCS '22), 2099–2113. arXiv:2201.05574.
- Roughgarden, T. (2021). *Transaction Fee Mechanism Design.* arXiv:2106.01340; Journal of the ACM (2024). See also Roughgarden (2020), *Transaction Fee Mechanism Design for the Ethereum Blockchain: An Economic Analysis of EIP-1559.*
- Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. (2023). *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014; in *Mathematical Research for Blockchain Economy* (Springer, 2024).
- Buterin, V., Conner, E., Dudley, R., Slipper, M., Norden, I. & Bakhta, A. (2019). *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals. eips.ethereum.org/EIPS/eip-1559.
- *Proposer-Builder Separation (PBS).* Ethereum protocol roadmap; Flashbots MEV-Boost.
- *EIP-7732: Enshrined Proposer-Builder Separation (ePBS).* Ethereum Improvement Proposals. eips.ethereum.org/EIPS/eip-7732.
- Capponi, A. & Zhu, B. (2026). *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN 6240079.
- *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost.* arXiv:2509.22143.
- Arbitrum Timeboost documentation. Offchain Labs.
