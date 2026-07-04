# Foundation Statement — Part I

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public Draft
**Last Updated:** July 2026

---

# 0. Abstract

Ethereum has become one of the world's leading platforms for research in decentralized protocol economics. Over the past several years, innovations such as **EIP-1559**, **Proposer-Builder Separation (PBS)**, and the ongoing development of **Enshrined PBS (ePBS)** have substantially improved fee market efficiency, decentralized block construction, and protocol market infrastructure. At the same time, active research on execution markets, builder optimization, execution latency, future execution rights, and protocol evolution continues to deepen our understanding of decentralized execution.

This Foundation Statement builds upon these developments.

It proposes **Temporal Liquidity** as a conceptual framework for studying the economic flexibility of demand with respect to execution time and investigates whether this property should become a protocol-visible economic variable within future decentralized execution markets.

Rather than advocating a single protocol mechanism, TLM develops a model-first methodology for understanding decentralized execution markets and explores how richer economic information may enable more expressive forms of decentralized coordination while preserving neutrality, decentralization, and open competition.

---

# 1. Introduction & Motivation

Blockchain protocols have undergone a remarkable evolution.

Early blockchain systems primarily focused on achieving decentralized consensus and secure transaction execution. As adoption increased, attention gradually shifted toward the economic allocation of scarce blockspace. This evolution gave rise to major advances in fee market design, decentralized block construction, execution markets, and protocol economics.

Research surrounding EIP-1559, PBS, ePBS, MEV, execution markets, and related protocol innovations has fundamentally reshaped how decentralized execution is understood.

Rather than viewing these developments as isolated protocol improvements, TLM views them as successive steps in the evolution of decentralized execution markets.

Collectively, these efforts have substantially improved how blockchain protocols coordinate **price**.

Yet one important aspect of demand remains largely implicit.

Users differ not only in how much they are willing to pay for execution, but also in **when** execution is valuable and **how much flexibility** they possess regarding execution time.

An arbitrage opportunity may lose nearly all value after a single block.

A decentralized exchange swap may willingly wait several blocks if execution cost decreases.

A treasury transfer may remain economically unchanged after many minutes.

These transactions differ not merely in price, but also in the relationship between **economic value** and **execution time**.

This observation motivates the central question of TLM:

> **Should the economic flexibility of demand with respect to execution time become a protocol-visible economic variable for decentralized execution markets?**

This Foundation Statement does not attempt to answer that question definitively.

Instead, it establishes a conceptual framework through which the question may be investigated.

---

# 2. Temporal Liquidity

Research across Ethereum protocol economics has demonstrated that execution timing possesses genuine economic significance.

Fee market research studies how users express urgency through prices.

Execution market research investigates transaction ordering and builder optimization.

Empirical studies have examined the economic consequences of execution delay.

Protocol proposals such as Execution Tickets and Slot Auctions increasingly consider execution opportunities extending across future blocks.

These developments motivate a broader conceptual question.

How should the economic flexibility of execution time itself be understood?

This Foundation Statement proposes the term **Temporal Liquidity** to describe:

> **The economic flexibility of demand with respect to execution time.**

Temporal Liquidity is proposed as an **economic property**, not a protocol mechanism.

It exists independently of any particular protocol representation, transaction format, or scheduling algorithm.

The purpose of TLM is to investigate whether this property should become protocol-visible and how decentralized markets might coordinate using richer temporal information.

---

# 3. Scope

TLM deliberately focuses on one question:

> **How should decentralized execution markets represent and coordinate heterogeneous temporal preferences?**

Accordingly, this work assumes Ethereum's existing protocol architecture and builds upon ongoing developments including EIP-1559, PBS, ePBS, execution markets, and related protocol research.

TLM does not begin by proposing a replacement protocol.

Instead, it develops a conceptual framework within which multiple future protocol mechanisms may be evaluated.

Mechanism proposals—including temporal queues, execution windows, adaptive pricing, Temporal Liquidity Reserve (TLR), or future protocol designs—should therefore be viewed as potential implementations rather than defining characteristics of the framework itself.

---

# 4. Relationship to Existing Work

Temporal Liquidity Market builds upon a broad body of existing research.

Research in Ethereum fee markets has significantly advanced the understanding of congestion pricing, incentive compatibility, and decentralized market efficiency.

PBS introduced specialization into decentralized block construction, enabling builders and proposers to optimize distinct aspects of block production.

Ongoing work on ePBS continues this architectural evolution by incorporating builder commitments into protocol rules while strengthening decentralized coordination.

Research into execution latency, future execution rights, Execution Tickets, Slot Auctions, and related protocol proposals demonstrates increasing attention to execution across time.

Empirical studies of transaction delay further illustrate that execution timing already possesses measurable economic value.

TLM does not replace these contributions.

Instead, it seeks to provide a conceptual framework through which these developments may be understood collectively.

Its primary contribution is the proposal to study **Temporal Liquidity** as a candidate economic variable describing the flexibility of demand with respect to execution time, and to investigate whether this property should become protocol-visible as decentralized execution markets continue to evolve.
