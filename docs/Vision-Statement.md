# Temporal Liquidity Market (TLM)

## Vision Statement

**Version:** 1.3 (Draft)
**Release:** TLM Public Release 2 (PR2)
**Status:** Public Draft
**Last Updated:** July 2026

---

## A Vision for Temporal Market Design in Blockchain Protocols

# Background

Ethereum has transformed blockchain protocol economics through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS). These developments demonstrate that protocol design can improve decentralized coordination by making economically meaningful information visible through simple, deterministic protocol rules.

Temporal Liquidity Market (TLM) asks whether decentralized execution markets can benefit from making economically meaningful temporal characteristics of demand, in addition to price, visible through protocol-defined abstractions.

Rather than replacing Ethereum's architecture, TLM explores the next stage of decentralized market design.

---

# Beyond Price

Today's execution markets primarily coordinate demand through price.

Execution demand also possesses temporal characteristics that influence resource allocation.

**Temporal Liquidity** is intentionally used as an umbrella economic concept analogous to **market liquidity**.

Just as market liquidity encompasses multiple dimensions (depth, immediacy, resiliency, etc.), Temporal Liquidity encompasses the collection of economically meaningful temporal characteristics of execution demand that may influence decentralized market coordination.

These characteristics may include:

- delay tolerance
- predictability
- execution priority
- execution windows
- continuity of demand
- deadlines
- other temporal properties

Individual research notes may investigate individual dimensions without implying separate top-level concepts.

The central question becomes:

> Can simple, protocol-visible temporal abstractions improve decentralized coordination while preserving neutrality and simplicity?

---

# A Historical Perspective

Internet QoS demonstrated both the promise and the limitations of protocol-visible information.

Highly expressive reservation approaches (IntServ/RSVP) proved difficult to deploy at Internet scale, while lightweight traffic classifications (DiffServ) improved coordination within administrative domains but encountered strategic marking, incentive misalignment, and limited inter-domain trust.

Permissionless blockchains inherit similar challenges under stronger adversarial assumptions.

However, blockchain protocols introduce cryptoeconomic tools—including staking, auctions, and mechanism design—that were largely unavailable during the evolution of Internet QoS.

TLM asks whether these new tools fundamentally change what protocol-visible abstractions can achieve.

---

# Research Vision

TLM investigates Temporal Liquidity as a new dimension of decentralized market design.

Its objective is to establish a conceptual framework for understanding, representing, and evaluating economically meaningful temporal characteristics of execution demand rather than prescribing a particular protocol mechanism.

---

# Why Better Market Design Can Create Social Surplus

TLM is not motivated by transferring value from one participant to another, nor by asking the network to sacrifice efficiency in order to accommodate patient users.

Instead, the central hypothesis is that existing execution markets cannot fully coordinate certain economically valuable transactions because they expose only a limited set of demand information—primarily price.

As a result, some execution demand remains **unrealized**, not because the network lacks capacity, but because the market lacks sufficient expressiveness to coordinate it efficiently.

By allowing participants to communicate simple, protocol-visible temporal characteristics of demand, an improved market design may enable execution opportunities that would otherwise never occur.

The resulting social surplus comes from **unlocking previously unrealized demand through better coordination**, rather than redistributing value among existing participants.

This distinction is fundamental to the TLM research program.

---

# Guiding Principles

- Build upon Ethereum's protocol evolution.
- Preserve decentralization and participant neutrality.
- Keep protocol rules simple, deterministic, and transparent.
- Separate protocol-visible information from protocol control.
- Increase overall social surplus rather than merely redistribute existing value.
- Evaluate ideas under strategic, permissionless assumptions.

---

# Open Research Questions

- Which temporal characteristics belong within Temporal Liquidity?
- Which should become protocol-visible?
- How coarse should protocol-visible abstractions be?
- Under what conditions does temporal information create social surplus?
- How economically significant is temporally flexible demand?
- Can cryptoeconomic mechanisms overcome historical limitations observed in Internet QoS?
- Can protocol-visible temporal abstractions remain robust against strategic manipulation?

---

# Conclusion

Ethereum demonstrated that protocol-visible economic information can improve decentralized coordination.

TLM extends that direction by asking whether **Temporal Liquidity**, understood as the collection of economically meaningful temporal characteristics of execution demand, can become another foundation for decentralized market design.

The project advances this as an open research agenda rather than a predetermined conclusion.
