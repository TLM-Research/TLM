# Related Work

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Living Document

---

# Related Work

Temporal Liquidity Market (TLM) is built upon the remarkable progress made by the Ethereum research community over the past several years.

Rather than replacing existing protocol proposals, TLM seeks to provide a conceptual framework through which many of these developments can be understood, connected, and extended.

This document summarizes major areas of related work and explains how they relate to the goals of TLM.

It is intended as a living literature map rather than a comprehensive bibliography.

---

# 1. Ethereum Fee Markets

## Motivation

Ethereum's fee market has evolved substantially from first-price auctions toward more efficient and predictable market mechanisms.

Perhaps the most significant milestone is **EIP-1559**, which introduced protocol-level congestion pricing through the Base Fee mechanism.

Subsequent economic analyses—particularly those by **Tim Roughgarden** and collaborators—have significantly advanced the understanding of blockchain fee markets, auction design, incentive compatibility, and market efficiency.

## Relationship to TLM

TLM builds directly upon this body of work.

Where EIP-1559 improves **price discovery**, TLM investigates whether decentralized execution markets should also coordinate another economic dimension:

**execution time.**

Temporal Liquidity should therefore be viewed as complementary to existing fee-market research rather than an alternative to it.

---

# 2. Proposer-Builder Separation (PBS)

## Motivation

PBS represents a major architectural evolution within Ethereum.

Rather than requiring validators to perform increasingly sophisticated block construction, PBS introduces specialization by separating block construction from block proposal.

Builders compete through market mechanisms while proposers remain focused on consensus responsibilities.

This separation improves scalability while preserving decentralized competition.

## Relationship to TLM

TLM assumes PBS as an important foundation rather than a competing architecture.

The specialization introduced by PBS provides an environment within which richer temporal coordination may eventually emerge.

TLM investigates how builders might utilize additional protocol-visible economic information without changing the fundamental separation introduced by PBS.

---

# 3. Enshrined PBS (ePBS)

## Motivation

Enshrined PBS continues the evolution of Ethereum's execution markets by incorporating builder commitments directly into protocol rules.

Research by **Barnabé Monnot** and other Ethereum researchers has emphasized the role of the protocol as market infrastructure, reducing reliance on trusted intermediaries while strengthening decentralized coordination.

ePBS also introduces temporal separation between commitment, payload reveal, execution validation, and settlement.

## Relationship to TLM

ePBS demonstrates that protocol evolution increasingly involves coordinating information across time.

TLM views this as an important architectural direction.

Rather than focusing solely on commitment timing, TLM investigates whether **Temporal Liquidity** itself may become protocol-visible economic information within future protocol evolution.

---

# 4. Execution Rights and Future Block Markets

## Motivation

Current Ethereum research explores several mechanisms that extend coordination beyond the current block.

These include proposals such as:

* Execution Tickets
* Slot Auctions
* Future execution rights
* Research into shorter slot times and execution latency

Although these proposals pursue different objectives, they all recognize that execution opportunities extend beyond a single block.

## Relationship to TLM

TLM views these developments as evidence that execution time is becoming an increasingly important aspect of protocol design.

Rather than studying these mechanisms individually, TLM provides a conceptual framework in which they may all be interpreted as different approaches to coordinating execution across time.

---

# 5. MEV and Execution Markets

## Motivation

Research surrounding Maximal Extractable Value (MEV), Flashbots, private order flow, builder markets, and execution optimization has fundamentally changed our understanding of blockchain execution.

Execution is no longer viewed as simple transaction ordering but as a sophisticated decentralized marketplace.

## Relationship to TLM

TLM assumes the existence of execution markets and does not attempt to eliminate MEV.

Instead, it investigates whether richer temporal information may improve coordination within existing decentralized execution markets while preserving market competition.

---

# 6. Economic Value of Delay

## Motivation

Several recent studies have investigated the economic value associated with execution delay.

This includes empirical work examining how transaction value changes as execution is delayed and how users express urgency through transaction fees and tips.

These studies demonstrate that execution delay already possesses measurable economic significance.

## Relationship to TLM

TLM builds upon this empirical observation.

Rather than asking whether delay has economic value, TLM asks whether the **economic flexibility of demand with respect to execution time** should itself become a protocol-visible economic variable.

In this sense, empirical studies of delay provide supporting evidence for the motivation behind Temporal Liquidity.

---

# 7. Mechanism Design and Market Design

## Motivation

Blockchain protocols increasingly draw upon ideas from mechanism design, auction theory, market microstructure, and distributed systems.

These disciplines provide theoretical foundations for understanding decentralized coordination under strategic behavior.

## Relationship to TLM

TLM should be viewed as an extension of this broader research tradition.

Its contribution is not a replacement for existing mechanism design, but a conceptual framework for investigating whether temporal information represents another economically meaningful variable for decentralized market coordination.

---

# 8. Position of TLM

The preceding work has collectively transformed Ethereum into an increasingly sophisticated decentralized execution market.

TLM seeks to build upon this evolution by introducing a model-first methodology for decentralized execution markets.

Rather than beginning with protocol mechanisms, TLM begins by modeling the underlying economic system, identifying economically meaningful variables, investigating which variables should become protocol-visible, and then exploring mechanisms that coordinate those variables.

Within this framework, **Temporal Liquidity** is proposed as a candidate economic variable describing the economic flexibility of demand with respect to execution time.

TLM therefore complements existing research in fee markets, PBS, ePBS, execution markets, and mechanism design while providing a broader conceptual framework through which these developments may be understood collectively.

---

# Future Updates

This document is intentionally incomplete.

Future versions will include:

* Formal references and bibliography.
* Links to Ethereum Improvement Proposals (EIPs).
* Academic papers and technical reports.
* Empirical studies related to execution timing.
* Additional work contributed by the Ethereum research community.

As TLM evolves, this document will continue to serve as a living map of the research landscape and an acknowledgment of the work upon which TLM is built.
