# Foundation Statement — Part I: Introduction

**Version:** 1.2
**Status:** Public Draft

# 0. Abstract

Ethereum has transformed decentralized execution through innovations such as EIP-1559, PBS, and emerging ePBS research. These advances have significantly improved how decentralized protocols coordinate **price**, block construction, and execution markets.

Temporal Liquidity Market (TLM) asks whether another dimension of demand deserves similar study: the economically meaningful **temporal characteristics** of execution demand — how much timing, ordering, and predictability matter, beyond willingness to pay.

Rather than proposing a new protocol mechanism, this Foundation Statement introduces **Temporal Liquidity** as a conceptual framework for studying these characteristics. Its purpose is to investigate whether some of this temporal information should become a protocol-visible economic variable, and whether exposing it could improve decentralized coordination while preserving neutrality, decentralization, and open competition.

The usefulness of the framework is ultimately an empirical question, to be evaluated through analysis, simulation, and future mechanism research.

------------------------------------------------------------------------

# 1. Introduction & Motivation

Blockchain protocols have evolved from solving decentralized consensus to designing increasingly sophisticated execution markets. Research on EIP-1559, PBS, ePBS, execution markets, and MEV has fundamentally improved how scarce blockspace is allocated. Viewed collectively, these developments progressively improve the protocol's ability to coordinate **price**.

Demand, however, differs along more than price. Users differ not only in *how much* they are willing to pay, but in *when* and *in what order* they need execution, in *how much their value erodes as execution is delayed*, and in *how forecastable and sustained* their demand is. These are distinct economic properties that a single scalar fee compresses away.

The most studied of them is the **value-versus-delay relationship** — how an application's realized value changes as execution is postponed. In economics it resembles intertemporal valuation; in scheduling theory, the value of slack or lateness; in blockchain, how value evolves across future execution opportunities. TLM does not claim these fields are identical, but builds on their shared intuition. Importantly, this relationship need not be a single scalar: it may depend on market state, execution environment, and interactions with other transactions, and it generally has both a *deadline* and a *decay rate*.

Expressing such a relationship is not trivial, because physical-time requirements ("execute before market close") must map onto discrete, congestion-dependent, and probabilistically reorganizable slots. That mapping is stochastic, and Part II's distinction among physical, protocol, and execution time is what makes it precise; Part I flags it rather than treating it as given.

The practical motivation is strongest for applications with significant temporal flexibility — recurring settlement, treasury operations, rollup batch publication, scheduled payments, and machine-to-machine workloads. By contrast, arbitrage and liquidation transactions typically have very low flexibility; they remain important boundary cases, but are not the primary motivation.

This leads to the central research question:

> **Should the economically meaningful temporal characteristics of demand become protocol-visible economic variables for decentralized execution markets?**

That temporal preferences are currently *implicit* does **not** by itself imply they should become *explicit*. Simplicity, privacy, and strategic considerations may argue otherwise. The objective of TLM is therefore not to advocate protocol changes, but to provide a framework within which this question can be rigorously evaluated.

------------------------------------------------------------------------

# 2. Temporal Liquidity

This Foundation Statement adopts the term **Temporal Liquidity** as an *umbrella* for the temporal structure of demand:

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

Its dimensions are **execution priority**, **delay tolerance**, **execution windows and deadlines**, **predictability**, and **continuity**. Temporal Liquidity is an **economic property, not a protocol mechanism** — independent of any transaction format, pricing rule, or scheduling algorithm — and it is distinct from any particular *representation* of it (descriptor, curve, profile); both representation and mechanism are intentionally left to later research.

The concept note **[Temporal Liquidity](./Temporal-Liquidity.md)** is the canonical exposition: it develops the market-liquidity analogy, the granularity ordering of the dimensions, the deadline-versus-decay structure of delay tolerance, the declared-versus-observed distinction, and the worked examples. This section states only the definition the rest of the Foundation relies on; the elaboration is not repeated here.

------------------------------------------------------------------------

# 3. Scope

TLM focuses on a single architectural question:

> **How should decentralized execution markets represent and coordinate heterogeneous temporal characteristics of demand?**

Specific mechanisms — temporal queues, execution windows, adaptive pricing, reserve-based designs, or future protocol designs — are treated as candidate implementations to be evaluated against the framework, not as defining features of it.

------------------------------------------------------------------------

# 4. Relationship to Existing Work

The underlying intuition is not new. Scheduling theory has long studied deadline flexibility and slack; economics studies intertemporal choice and the value of delay; distributed systems have explored delay-tolerant communication and quality-of-service abstractions; and financial economics studies liquidity as a multidimensional property and prices demand across time through forward and spot markets. TLM does not attempt to replace these bodies of work.

Its contribution is to investigate whether these ideas can be adapted to **permissionless decentralized execution markets**, where incentive compatibility, strategic behavior, and protocol neutrality become first-order constraints. TLM also builds directly on Ethereum research — EIP-1559, PBS, ePBS, execution markets, future execution rights, empirical studies of transaction delay, and tiered transaction-fee mechanisms (Kiayias et al., 2023, which price the urgency dimension and which TLM generalizes) — seeking to understand them through the common lens of temporal demand rather than to replace them.

The standalone `Related-Work` document is the canonical map of these literatures and carries the specific inherited-or-challenged results and citations; this section is only a brief pointer. Later parts of the Foundation examine whether protocol-visible temporal information provides measurable benefits for decentralized scheduling and market coordination.
