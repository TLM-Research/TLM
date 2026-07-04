# Temporal Liquidity

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public Draft
**Last Updated:** July 2026

---

# Temporal Liquidity

## Motivation

Blockchain protocols have made remarkable progress in improving decentralized execution markets.

Research on Ethereum fee markets, **EIP-1559**, **Proposer-Builder Separation (PBS)**, **Enshrined PBS (ePBS)**, Maximal Extractable Value (MEV), builder markets, execution latency, and future execution rights has significantly advanced our understanding of how scarce blockspace is allocated through decentralized market mechanisms.

These efforts have collectively demonstrated that transaction execution is not merely a technical scheduling problem. It is fundamentally an economic coordination problem.

One important aspect of demand, however, remains largely implicit:

> **How economically flexible is a transaction with respect to execution time?**

This document proposes **Temporal Liquidity** as a conceptual framework for studying this question.

---

# Relationship to Existing Research

Temporal Liquidity should not be viewed as an alternative to existing Ethereum research.

Rather, it builds upon a growing body of work in fee market design, protocol economics, execution markets, and decentralized coordination.

Previous research has addressed important questions including:

* efficient fee market design;
* congestion pricing;
* builder specialization through PBS;
* protocol evolution through ePBS;
* execution rights and future block markets;
* execution latency and transaction inclusion;
* empirical studies on the economic value of execution delay.

These contributions provide much of the motivation for Temporal Liquidity.

TLM asks a complementary question:

> **Should the economic flexibility of demand with respect to execution time itself become a protocol-visible economic variable?**

---

# Definition

Temporal Liquidity is defined as:

> **The economic flexibility of demand with respect to execution time.**

More precisely, it describes how the economic value of executing a transaction changes as execution is delayed.

Transactions differ not only in how much they are willing to pay for execution, but also in how sensitive they are to execution timing.

Some transactions lose value almost immediately when delayed.

Others remain economically valuable over much longer periods.

Temporal Liquidity provides a conceptual language for describing these differences.

Importantly, Temporal Liquidity is an **economic property**, not a protocol mechanism.

It exists independently of how blockchain protocols choose to represent or coordinate it.

---

# Examples

Different applications naturally exhibit different levels of Temporal Liquidity.

### Arbitrage

An arbitrage transaction often derives value from temporary price discrepancies.

Its value may disappear after a single block.

Such transactions exhibit **low Temporal Liquidity** because their economic value declines rapidly with execution delay.

---

### Liquidations

Liquidation opportunities frequently involve direct competition among participants.

Execution timing significantly influences expected value.

These transactions similarly exhibit relatively low Temporal Liquidity.

---

### Decentralized Exchange Swaps

Many swaps remain economically valuable after modest execution delays, particularly when users are willing to trade execution speed for lower transaction cost.

These transactions often possess moderate Temporal Liquidity.

---

### Rollup Batch Submission

Rollups typically optimize throughput and cost across many transactions.

Execution often remains economically valuable over a broader execution window.

These transactions may therefore exhibit relatively high Temporal Liquidity.

---

### Treasury Transfers

Treasury operations frequently prioritize reliability over immediate execution.

Execution delays of several minutes or even longer may have little economic consequence.

Such transactions generally possess high Temporal Liquidity.

---

These examples illustrate that execution timing is not uniformly important.

Different applications naturally exhibit different temporal characteristics.

---

# Why Temporal Liquidity Matters

Current blockchain fee markets primarily coordinate demand through **price**.

However, economic demand contains additional dimensions beyond willingness to pay.

Execution time represents one such dimension.

Meanwhile, Ethereum protocol research increasingly explores execution across time through developments including:

* Enshrined PBS;
* Execution Tickets;
* Slot Auctions;
* shorter slot times;
* builder optimization;
* execution market design.

These developments suggest that execution time is becoming an increasingly important aspect of blockchain protocol evolution.

Temporal Liquidity provides one possible economic framework for understanding this broader trend.

Rather than treating execution time solely as a performance metric, it treats execution time as an economically meaningful property of decentralized demand.

---

# Relationship to Protocol Mechanisms

Temporal Liquidity should be carefully distinguished from protocol mechanisms.

Temporal Liquidity is **not**:

* a temporal queue;
* Execution Tickets;
* Slot Auctions;
* Temporal Liquidity Reserve (TLR);
* adaptive pricing mechanisms;
* any specific transaction format.

Instead, these should be viewed as potential mechanisms through which Temporal Liquidity might eventually be represented or coordinated.

The economic concept exists independently of any particular implementation.

This distinction separates economic theory from protocol engineering and allows multiple mechanisms to be evaluated within a common conceptual framework.

---

# Research Directions

Temporal Liquidity raises numerous research questions.

Examples include:

* How should Temporal Liquidity be represented?
* Can Temporal Liquidity be measured empirically?
* Which temporal information should become protocol-visible?
* How should builders utilize temporal information?
* Can richer temporal coordination improve market efficiency?
* How should privacy and strategic behavior be balanced against greater expressiveness?
* Can decentralized execution markets coordinate heterogeneous temporal preferences without increasing centralization?

These questions remain intentionally open.

TLM proposes a framework for investigating them rather than prescribing immediate answers.

---

# Summary

Temporal Liquidity is proposed as an economic property describing the flexibility of demand with respect to execution time.

Rather than prescribing any particular protocol mechanism, it provides a conceptual foundation for investigating how decentralized execution markets may represent, communicate, and coordinate heterogeneous temporal preferences.

As Ethereum continues to evolve through advances in fee markets, PBS, ePBS, execution markets, and future protocol innovations, Temporal Liquidity offers one possible framework for understanding execution time as an economically meaningful dimension of decentralized market design.

**Temporal Liquidity plays a role analogous to price elasticity: it characterizes how economic demand responds to flexibility in execution time rather than changes in price.**
