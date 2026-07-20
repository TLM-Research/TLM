---
id: RN-03
title: "Hyperliquid: A Case Study in Temporal Liquidity"
version: "0.5"
status: "Public Draft of Research Note"
program: "Temporal Liquidity Market (TLM)"
date: "July 2026"
---

# RN-03 v0.5

# Hyperliquid: A Case Study in Temporal Liquidity

**Temporal Liquidity Market (TLM) Research Program**
**Research Note RN-03**
**Version:** 0.5
**Status:** Internal Research Note
**Date:** July 2026

---

## Abstract

Blockchain execution markets today coordinate demand primarily through one visible variable — willingness to pay. This note uses Hyperliquid as an empirical case study to argue that execution demand also carries economically meaningful **temporal** structure that price alone does not represent.

Consistent with the TLM Vision Statement, **Temporal Liquidity** is treated here as an *umbrella* economic concept — the collection of economically meaningful temporal characteristics of execution demand — rather than a synonym for patience or delay tolerance [10]. Hyperliquid's fully on-chain, price-time-priority order book [1–3] is a useful lens because it exposes several of these characteristics at once: sustained **continuity**, partial aggregate **predictability**, acute **execution-priority** (intra-slot ordering) sensitivity, and bursty, delay-intolerant exceptional events.

The note's central claim is deliberately modest. Hyperliquid is **motivating evidence** that multidimensional temporal demand exists and is systematically under-represented by spot fee markets — not proof that a protocol-visible temporal abstraction would obviate specialized chains. Used this way, it is a concrete, cited on-ramp to TLM.

This version (v0.5) builds on the lean framing of v0.2, but corrects two gaps: it aligns the definition to the latest Vision (Temporal Liquidity as umbrella), and it restores the empirical and bibliographic citations that v0.2 omitted.

---

## 1. Motivation: Time Already Has Economic Value

Ethereum's fee market, under EIP-1559, sets a congestion-responsive base fee and lets users attach a priority fee to compete for earlier inclusion [11]. It coordinates demand well, but largely **transaction by transaction, after arrival, through price**.

That time already carries economic value is empirically established, not assumed:

- Zhao estimates the **cost of delay** directly from the Ethereum transaction fee market, showing that delaying a transaction imposes a measurable economic cost that varies across transactions [4].
- Liu et al. analyze EIP-1559 across blockchain, mempool, and exchange data and find that fee-mechanism design measurably affects **waiting times** [5].
- Complementary work documents the gas-price/processing-time relationship, including diminishing returns to higher fees [7], and argues waiting time matters for both efficiency and security [8].

These results establish that execution time is economically meaningful — but a single delay-cost parameter does not capture the full temporal structure of demand. The question this note pursues is:

> **What temporal information about demand remains implicit when transactions compete primarily through price after arrival?**

---

## 2. Temporal Liquidity Is an Umbrella (Consistency with the Vision)

The canonical definition lives in the Vision Statement [10]; only the minimum needed here is repeated.

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

It is an umbrella — analogous to *market liquidity*, which is itself a family of properties (depth, immediacy, resiliency) rather than a single quantity. Its dimensions include:

- **delay tolerance** — how execution value changes as execution is delayed across slots;
- **predictability** — how well future aggregate demand can be forecast before it arrives;
- **execution priority** — sensitivity of value to ordering *within* a slot;
- **execution windows / deadlines** — bounded intervals or hard cutoffs for acceptable execution;
- **continuity** — whether demand is a sustained stream or an isolated event.

A useful organizing axis is **temporal granularity**: execution priority is intra-slot; delay tolerance, windows, and deadlines are inter-slot; predictability and continuity are stream-level.

> **Correction to v0.2.** Earlier RN-03 framing placed *predictability* outside Temporal Liquidity, treating "temporal information" as the umbrella and Temporal Liquidity as the delay-tolerance member. The current Vision inverts this: **Temporal Liquidity is the umbrella, and predictability, continuity, and execution priority are dimensions of it.** This note adopts the current definition.

---

## 3. Two Dimensions of Temporal Liquidity Are Independent

A recurring confusion is to treat "temporal" as one axis. Hyperliquid shows at least two are orthogonal: **delay tolerance** (patience) and **predictability** (forecastability).

| | Delay-tolerant | Delay-intolerant (low latency) |
|---|---|---|
| **Predictable** | treasury batches, rollup posting | **order-book quote stream (Hyperliquid)** |
| **Unpredictable** | opportunistic rebalancing | liquidation cascade, arbitrage |

Hyperliquid's routine market-making traffic sits in the top-right cell: it demands consistently low latency **yet is statistically forecastable in aggregate**. That combination is invisible to a market that reads only willingness-to-pay. Delay tolerance is a *declared preference* of the demand; predictability is an *observed property* others can verify — a distinction that matters for how each could be represented and priced.

---

## 4. Latency ≠ Urgency ≠ Predictability ≠ Priority

Hyperliquid's order book makes clear that several temporal notions must not be collapsed.

- **Latency** is a systems quantity (submission-to-execution time).
- **Urgency** is how fast value decays if execution waits — a property of application state.
- **Predictability** is how forecastable aggregate demand is.
- **Execution priority** is sensitivity to ordering *within* a block.

The last one is directly visible in Hyperliquid because its book matches by **price-time priority**: for equally priced orders, arrival time sets queue position, so ordering changes fill probability, adverse selection, and realized value [1–2]. Execution priority is therefore not a restatement of willingness-to-pay — it is a genuinely temporal characteristic (position in time).

This connects to active work on pricing time-as-priority. Arbitrum's **Timeboost** auctions an express lane, granting the winner immediate sequencing while others incur a fixed delay; Capponi & Zhu analyze this as *auctioning time to mitigate latency races*, arguing an explicit time-priority market can reduce wasteful latency competition [9]. More generally, the coupling of "pay more → execute sooner" is a **mechanism artifact** of spot auctions, not a physical law — a point that follows from transaction-fee-mechanism analysis [12] and the delay-cost evidence above [4,5]. A different market design could preserve price competition while representing some temporal characteristics explicitly.

---

## 5. Why Predictability and Continuity Have Economic Value

That predictable, sustained demand is economically distinct from bursty spot demand is not an assertion; it follows from standard theory.

- **Queueing.** Waiting time depends not only on average load but on its *variability*: in an M/G/1 queue, the Pollaczek–Khinchine relation ties expected wait to the second moment of service, so forecastable low-variance demand achieves lower delay at equal utilization [6]. Two workloads with identical average load can impose very different scheduling costs.
- **Statistical multiplexing.** Shared systems gain efficiency by combining heterogeneous flows whose peaks do not coincide; credible information distinguishing baseline, bounded bursts, and deferrable work improves that gain.
- **Reservation vs spot.** Cloud and transportation markets combine reservations (commitment/predictability in exchange for price stability) with spot allocation (absorbing residual uncertainty). This shows predictability can be valuable **independently of patience** — a stream can need immediate service per request while still supplying valuable advance information about aggregate demand.

The TLM hypothesis is not central scheduling. It is that limited, credible temporal information may let decentralized markets coordinate shared capacity better than undifferentiated spot bidding — and that the resulting surplus comes from *unlocking suppressed demand and removing coordination waste*, not redistribution.

---

## 6. Hyperliquid as Motivation, Not Proof

Hyperliquid demonstrates that blockchain execution demand can exhibit sustained continuity, partial aggregate predictability, acute execution-priority sensitivity, low-latency requirements, and bursty exceptional events. Within the umbrella, these are dimensions of Temporal Liquidity.

It does **not** establish that:

- Temporal Liquidity must become protocol-visible;
- participants would report temporal characteristics truthfully;
- a richer abstraction on a shared chain would reproduce Hyperliquid's performance;
- a temporal abstraction alone would remove the need for specialized chains.

Hyperliquid built its own L1, VM (HyperCore), and deterministic sequencing — i.e. it took control of the whole execution path, not merely the ability to *describe* its demand. Application-chain design and temporal-market design are **separate axes**; sovereignty, integrated margin/liquidation logic, and product strategy are confounds. So the right rhetorical use of this case is: *the demand exists and is mispriced*, not *an abstraction obviates appchains*.

---

## 7. Implications for TLM

1. Temporal Liquidity should be treated as a multidimensional umbrella; predictability, continuity, and execution priority are dimensions, not competing concepts.
2. The economically relevant unit is sometimes a **demand stream or profile**, not an isolated transaction.
3. Temporal information can have coordination value even when demand is **not** patient (the predictable-but-urgent cell).
4. The fee–delay coupling bundles several economically distinct costs (physical cost, congestion externality, uncertainty cost, preemption premium) that become separable only when demand is studied over time.
5. Any benefit must be weighed against complexity, strategic manipulation, state growth, and centralization pressure — the last of which Timeboost's empirical record makes concrete [9].

---

## 8. Open Questions and Measurement

- Which temporal dimensions are measurable from observed behavior (arrival processes, cancellation intensity, burstiness) without relying on self-declaration? High-frequency Hyperliquid order-book data is independently obtainable and offers a starting dataset [13].
- Can aggregate predictability be made credible without exposing proprietary strategy?
- Can the predictable low-latency stream be distinguished, and priced differently, from unpredictable preemptive demand — without abandoning price competition?
- Under Roughgarden's criteria (DSIC, MMIC, OCA-proofness), can a temporally augmented mechanism remain incentive compatible and collusion-resistant [12]?
- How large and material is temporally flexible demand, empirically?

---

## Summary

Hyperliquid exposes execution demand that price alone describes poorly: a sustained, forecastable, low-latency, ordering-sensitive stream punctuated by unpredictable bursts. Under the current definition, these are multiple dimensions of **Temporal Liquidity**. The case does not prove any mechanism, and it does not show that specialized chains are unnecessary. It supports a narrower, defensible conclusion:

> **Economically important blockchain applications generate multidimensional temporal demand that today's spot fee markets under-represent — enough to motivate measuring and market-design study of Temporal Liquidity.**

---

## References

[1] Hyperliquid. "About Hyperliquid." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs
[2] Hyperliquid. "Order Book." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs/trading/order-book
[3] Hyperliquid. "HyperCore Overview." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview
[4] Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper No. 4436697 (posted 14 May 2023; last revised 15 June 2026).
[5] Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. "Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security." *Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (CCS '22),* 2099–2113. https://doi.org/10.1145/3548606.3559341
[6] Kleinrock, L. *Queueing Systems, Volume 1: Theory.* Wiley, 1975 (Pollaczek–Khinchine mean-value formula).
[7] Pacheco, M., Oliva, G. A., Rajbahadur, G. K. & Hassan, A. E. "Is My Transaction Done Yet? An Empirical Study of Transaction Processing Times in the Ethereum Blockchain Platform." 2022. https://arxiv.org/abs/2206.08959
[8] Zhang, L. & Zhang, F. "Understand Waiting Time in Transaction Fee Mechanism: An Interdisciplinary Perspective." 2023. https://arxiv.org/abs/2305.02552
[9] Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN Working Paper, 2026. See also *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost,* arXiv:2509.22143, for the centralization evidence.
[10] TLM Research Program. *Vision Statement.* Canonical definition and motivation for Temporal Liquidity (umbrella concept).
[11] Buterin, V., Conner, E., Dudley, R., Slipper, M., Norden, I. & Bakhta, A. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals, 2019. https://eips.ethereum.org/EIPS/eip-1559
[12] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *Journal of the ACM,* 2024. (DSIC / MMIC / OCA-proofness framework.)
[13] Albers, J. "Level 4 Order Book Data from the Hyperliquid Exchange." SSRN Working Paper No. 6465720, 2026.

---

## Revision Note

**Version 0.5** — builds on the lean structure of v0.2 and deliberately does *not* adopt v0.3/v0.4's extended exchange-architecture comparison (dYdX, Injective, Solana CLOBs), which broadened scope beyond this note's motivating purpose. Changes from v0.2:

- aligns the definition to the current Vision: **Temporal Liquidity is the umbrella**; predictability, continuity, and execution priority are its dimensions (v0.2 had predictability *outside* Temporal Liquidity);
- adds **execution priority** as a dimension, grounded in Hyperliquid's price-time-priority book and linked to Timeboost / Capponi–Zhu;
- **restores citations** omitted in v0.2 — Hyperliquid docs, Zhao (cost of delay), Liu et al. (EIP-1559), Capponi–Zhu (Timeboost), Kleinrock (queueing), Roughgarden (TFM), plus supporting empirical work;
- keeps the "motivation, not proof" discipline and the patience × predictability independence result.
