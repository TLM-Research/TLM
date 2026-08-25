---
id: RN-03
title: "Hyperliquid: A Case Study in Temporal Liquidity"
version: "0.7"
status: "Public Draft of Research Note"
program: "Temporal Liquidity Market (TLM)"
date: "August 12, 2026"
---

# RN-03 v0.7

# Hyperliquid: A Case Study in Temporal Liquidity

**Temporal Liquidity Market (TLM) Research Program**
**Research Note RN-03**
**Version:** 0.7
**Status:** Public Draft of Research Note
**Date:** August 12, 2026

---

## Abstract

Blockchain execution markets today coordinate demand primarily through one visible variable - willingness to pay. This note uses Hyperliquid as a motivating case study to argue that execution demand also carries economically meaningful **temporal** structure that price alone does not represent - a system profile and argument, grounded in cited empirical work on the cost of delay, rather than a fresh measurement of Hyperliquid's own workload.

Consistent with the TLM Vision Statement, **Temporal Liquidity** is treated here as an *umbrella* economic concept - the collection of economically meaningful temporal characteristics of execution demand - rather than a synonym for patience or delay tolerance [10]. Hyperliquid's fully on-chain, price-time-priority order book [1-3] is a useful lens because it exposes several of these characteristics at once: sustained **continuity**, partial aggregate **predictability**, acute **execution-priority** (intra-slot ordering) sensitivity, and bursty, delay-intolerant exceptional events.

The note's central claim is deliberately modest. Hyperliquid is **motivating evidence** that multidimensional temporal demand exists and is systematically under-represented by spot fee markets - not proof that a protocol-visible temporal abstraction would remove the need for specialized chains. Used this way, it is a concrete, cited on-ramp to TLM.

The current version aligns the definition to the Vision (Temporal Liquidity as umbrella) and grounds the argument in the empirical and bibliographic citations; changes across drafts are recorded in the Revision Note.

---

## 1. Motivation: Time Already Has Economic Value

Ethereum's fee market, under EIP-1559, sets a congestion-responsive base fee and lets users attach a priority fee to compete for earlier inclusion [11]. It coordinates demand well, but largely **transaction by transaction, after arrival, through price**.

That time already carries economic value is empirically established, not assumed:

- Zhao estimates the **cost of delay** directly from the Ethereum transaction fee market, showing that delaying a transaction imposes a measurable economic cost that varies across transactions [4].
- Liu et al. analyze EIP-1559 across blockchain, mempool, and exchange data and find that fee-mechanism design measurably affects **waiting times** [5].
- Complementary work documents the gas-price/processing-time relationship, including diminishing returns to higher fees [7], and argues waiting time matters for both efficiency and security [8].

These results establish that execution time is economically meaningful - but a single delay-cost parameter does not capture the full temporal structure of demand. The question this note pursues is:

> **What temporal information about demand remains implicit when transactions compete primarily through price after arrival?**

---

## 2. Temporal Liquidity Is an Umbrella (Consistency with the Vision)

The canonical definition lives in the Vision Statement [10]; only the minimum needed here is repeated.

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

It is an umbrella - analogous to *market liquidity*, which is itself a family of properties (depth, immediacy, resiliency) rather than a single quantity. Its dimensions include:

- **delay tolerance** - how execution value changes as execution is delayed across slots;
- **predictability** - how well future aggregate demand can be forecast before it arrives;
- **execution priority** - sensitivity of value to ordering *within* a slot;
- **execution windows / deadlines** - bounded intervals or hard cutoffs for acceptable execution;
- **continuity** - whether demand is a sustained stream or an isolated event.

A useful organizing axis is **temporal granularity**: execution priority is intra-slot; delay tolerance, windows, and deadlines are inter-slot; predictability and continuity are stream-level.

> **Correction to v0.2.** Earlier RN-03 framing placed *predictability* outside Temporal Liquidity, treating "temporal information" as the umbrella and Temporal Liquidity as the delay-tolerance member. The current Vision inverts this: **Temporal Liquidity is the umbrella, and predictability, continuity, and execution priority are dimensions of it.** This note adopts the current definition.

---

## 3. Two Dimensions of Temporal Liquidity Are Independent

A recurring confusion is to treat "temporal" as one axis. Hyperliquid shows at least two are orthogonal: **delay tolerance** (patience) and **predictability** (forecastability).

| | Delay-tolerant | Delay-intolerant (low latency) |
|---|---|---|
| **Predictable** | treasury batches, rollup posting | **order-book quote stream (Hyperliquid)** |
| **Unpredictable** | opportunistic rebalancing | liquidation cascade, arbitrage |

Hyperliquid's routine market-making traffic sits in the top-right cell: it demands consistently low latency **yet is statistically forecastable in aggregate**. That combination is invisible to a market that reads only willingness-to-pay. Delay tolerance is a *declared preference* of the demand; predictability is an *observed property* others can verify - a distinction that matters for how each could be represented and priced.

---

## 4. Latency ≠ Urgency ≠ Predictability ≠ Priority

Hyperliquid's order book makes clear that several temporal notions must not be collapsed.

- **Latency** is a systems quantity (submission-to-execution time).
- **Urgency** is how fast value decays if execution waits - a property of application state.
- **Predictability** is how forecastable aggregate demand is.
- **Execution priority** is sensitivity to ordering *within* a block.

The last one is directly visible in Hyperliquid because its book matches by **price-time priority**: for equally priced orders, arrival time sets queue position, so ordering changes fill probability, adverse selection, and realized value [1-2]. Execution priority is therefore not a restatement of willingness-to-pay - it is a genuinely temporal characteristic (position in time).

This connects to active work on pricing time-as-priority. Arbitrum's **Timeboost** auctions an express lane, granting the winner immediate sequencing while others incur a fixed delay; Capponi & Zhu analyze this as *auctioning time to mitigate latency races*, arguing an explicit time-priority market can reduce wasteful latency competition [9]. More generally, the coupling of "pay more -> execute sooner" is a **mechanism artifact** of spot auctions, not a physical law - a point that follows from transaction-fee-mechanism analysis [12] and the delay-cost evidence above [4,5]. A different market design could preserve price competition while representing some temporal characteristics explicitly.

---

## 5. Why Predictability and Continuity Have Economic Value

That predictable, sustained demand is economically distinct from bursty spot demand is not an assertion; it follows from standard theory.

- **Queueing.** Waiting time depends not only on average load but on its *variability*. The Pollaczek-Khinchine relation makes this precise for one channel - but for the second moment of *service time*, not of arrivals: in an M/G/1 queue, high service-time variance raises expected wait at equal utilization [6]. The demand-side claim this note cares about is a separate object and needs its own model: bursty or correlated *arrivals* lengthen waits (a G/G/1 rather than M/G/1 effect), and *predictability* is not a variance term in P-K at all - it helps only through a scheduler that acts on the forecast, and only up to its forecast error. So P-K establishes that variability is costly; that predictable, low-variance demand is served at lower delay rests on arrival structure and forecast-aware scheduling - the statistical-multiplexing point below - not on P-K alone. Either way, two workloads with identical average load can impose very different scheduling costs.
- **Statistical multiplexing.** Shared systems gain efficiency by combining heterogeneous flows whose peaks do not coincide; credible information distinguishing baseline, bounded bursts, and deferrable work improves that gain.
- **Reservation vs spot.** Cloud and transportation markets combine reservations (commitment/predictability in exchange for price stability) with spot allocation (absorbing residual uncertainty). This shows predictability can be valuable **independently of patience** - a stream can need immediate service per request while still supplying valuable advance information about aggregate demand.

The TLM hypothesis is not central scheduling. It is that limited, credible temporal information may let decentralized markets coordinate shared capacity better than undifferentiated spot bidding - and that the resulting surplus comes from *unlocking suppressed demand and removing coordination waste*, not redistribution.

---

## 6. The Hyperliquid System, and Why It Is Motivation Rather Than Proof

### 6.1 The system: HyperCore and HyperEVM

Hyperliquid runs two execution environments on one HyperBFT consensus (a HotStuff-family protocol with one-block finality), so the case study rests on a concrete architecture rather than an abstraction [1, 3, 14].

**HyperCore** is a purpose-built Rust engine that runs the exchange itself: fully on-chain perpetual and spot order books, matching by **price-time priority**, margining (isolated, cross, and portfolio), liquidations, and mark-price computation. Order placement pays no gas, and matching happens inside consensus, so there is no public mempool to front-run. The **mark price** combines the order book with an oracle that each validator computes as a weighted median of major centralized-exchange prices, which externalizes the reference price against local-book manipulation. Most **liquidations** are routed to the order book for open competition rather than to privileged keepers. Each of these is a supply-side mechanism analyzed in RN-04 sec. 6; here they matter because they expose the temporal characteristics this note studies - continuous quote streams, ordering-sensitive fills, and bursty, delay-intolerant liquidation events.

**HyperEVM** is a general-purpose EVM environment sharing the same state and consensus - and, in its own right, a general-purpose EVM Layer-1 competing with Ethereum for ordinary smart-contract activity, not merely a sidecar to the exchange. It reaches HyperCore through two native lanes: **read precompiles** that return HyperCore state (positions, balances, oracle prices) atomically as of the EVM block, and a **CoreWriter** system contract through which EVM contracts send actions - orders, transfers - into HyperCore. One detail is directly temporal: CoreWriter order actions are **deliberately delayed a few seconds on-chain**, so that routing through the EVM confers no latency advantage over the native order path [14]. The protocol is managing execution *timing* to remove an ordering edge - a concrete instance of the theme in sec. 4 that execution priority must be governed, not left to whoever is fastest.

Two differentiated execution environments thus share one consensus and settlement base. That pattern - differentiated execution without duplicated consensus - is the precursor RN-08 and RN-09 generalize as Virtual Chains.

### 6.2 HyperEVM's dual-block lanes: coarse protocol-native time preference

A second temporal mechanism sits *inside* HyperEVM, and it is distinct from the HyperCore/HyperEVM split of sec. 6.1: HyperEVM maintains one EVM state but schedules **two kinds of block**. **Small blocks** are produced roughly every second at a low gas limit (about 2M gas as documented), serving latency-sensitive traffic - transfers, swaps, deposits, oracle calls, CoreWriter interactions. **Large blocks** are produced roughly once a minute at a high gas limit (about 30M gas), serving contract deployment, migrations, and other heavy or large-atomic work. The two draw from **separate mempools** and expose **separate congestion signals** (a small-block base fee and a large-block base fee), yet they are interleaved into one increasing sequence of HyperEVM block numbers over one shared state, secured by the same HyperBFT consensus - one chain, not two [14]. (Cadences and gas limits are documented values subject to change; treat them as of the cited documentation.)

Two features make this more than a size knob. First, the large lane's value is not aggregate throughput - sixty small blocks a minute (about 120M gas) already exceed one large block (30M gas) - but **single-block atomic capacity**: a 5M-gas deployment cannot be split across 2M-gas blocks, so the large lane exists to admit large *indivisible* work, decoupling block *speed* from block *size*. Second, lane selection is **explicit and account-based**: a developer sets the account into large-block mode (`usingBigBlocks`) rather than the protocol inferring intent from a transaction's gas, so the temporal service chosen is part of the account's execution configuration, and the two workloads do not compete in one homogeneous block stream.

Read against this note's thesis, HyperEVM is a production instance of **protocol-native temporal differentiation**: it makes a transaction's time preference explicit and accommodates it at the protocol level, treating two temporal service classes - frequent-and-low-capacity, infrequent-and-high-capacity - as first-class protocol resources with their own queues, schedules, and fees. That a live chain found this worth building strengthens the note's claim in a specific way: the point is not only that multidimensional temporal demand exists (secs. 3-5), but that serving it through distinct protocol-level lanes is viable and valued in practice - the service-class idea RN-04 develops, already partly instantiated.

> **HyperEVM introduces protocol-native temporal differentiation by allowing transactions to select between execution lanes with different latency and atomic-capacity profiles.**

And because HyperEVM is a general-purpose chain, this is **chain-level** differentiation, not an application's internal rule - a distinction sec. 4 needs and that this case makes concrete. HyperCore's price-time priority is *application-internal*: a queue position inside one exchange's order book, jointly set by price, size, and cancellations. HyperEVM's dual-block lanes are *chain-level*: a general-purpose L1 offering arbitrary transactions two temporal service classes, directly comparable to Ethereum's single execution lane. Hyperliquid thus supplies both objects at once - application-internal ordering priority (HyperCore) and chain-level temporal service classes (HyperEVM) - and it is the second, on an Ethereum-competitor chain, that is the direct instance of what TLM proposes, with the order book motivating the finer intra-slot priority dimension (sec. 4) above it.

Two limits keep this motivation rather than proof, and both sharpen the TLM contrast. It is **coarse**: two predefined classes, not a continuous or programmable preference - a transaction cannot state "execute within 2s at price X, within 1 minute at price Y," nor an arbitrary deadline, delay tolerance, or patience reward. And the two dimensions are **coupled, not isolated**: the small lane bundles low latency with low atomic capacity, the large lane bundles higher latency with high atomic capacity, so choosing a lane chooses latency *and* capacity together - exactly the bundling sec. 4 warns against, where distinct temporal characteristics collapse into one knob. HyperEVM recognizes time heterogeneity at the protocol level but represents it as two coupled classes; a finer temporal market would decouple the dimensions and let demand express a preference rather than pick a lane. The honest reading therefore matches sec. 6.3: the demand is real and protocol-level differentiation is viable, but the coarse, coupled, account-level form is what a programmable temporal market would refine, not a finished instance of one.

The direction this points is toward Ethereum. Ethereum still routes latency-sensitive and capacity-intensive work through one homogeneous execution lane - one stream per 12-second slot - so a transaction cannot seek frequent, low-capacity service or infrequent, high-capacity service; both compete in the single block for the slot. HyperEVM shows that making transaction time preference even *partly* explicit is viable on a general-purpose EVM chain and valued enough to build. That is the case for bringing temporal differentiation to Ethereum itself - not HyperEVM's two coupled lanes, but the finer, decoupled, programmable temporal market this program develops on Ethereum's evolution (Vision; Foundation; RN-04). The motivation is therefore directional: a production Ethereum-competitor already differentiates time, coarsely; TLM is the proposal to do it finely and neutrally on the Ethereum foundation.

### 6.3 Motivation, not proof

Hyperliquid demonstrates that blockchain execution demand can exhibit sustained continuity, partial aggregate predictability, acute execution-priority sensitivity, low-latency requirements, and bursty exceptional events. Within the umbrella, these are dimensions of Temporal Liquidity.

It does **not** establish that:

- Temporal Liquidity must become protocol-visible;
- participants would report temporal characteristics truthfully;
- a richer abstraction on a shared chain would reproduce Hyperliquid's performance;
- a temporal abstraction alone would remove the need for specialized chains.

Hyperliquid built its own L1, VM (HyperCore), and deterministic sequencing - i.e. it took control of the whole execution path, not merely the ability to *describe* its demand. Application-chain design and temporal-market design are **separate axes**; sovereignty, integrated margin/liquidation logic, and product strategy are confounds. So the right rhetorical use of this case is: *the demand exists and is mispriced*, not *an abstraction removes the need for appchains*.

---

## 7. Implications for TLM

1. Temporal Liquidity should be treated as a multidimensional umbrella; predictability, continuity, and execution priority are dimensions, not competing concepts.
2. The economically relevant unit is sometimes a **demand stream or profile**, not an isolated transaction.
3. Temporal information can have coordination value even when demand is **not** patient (the predictable-but-urgent cell).
4. The fee-delay coupling bundles several economically distinct costs (physical cost, congestion externality, uncertainty cost, preemption premium) that become separable only when demand is studied over time.
5. Any benefit must be weighed against complexity, strategic manipulation, state growth, and centralization pressure - the last of which Timeboost's empirical record makes concrete [9].

---

## 8. Open Questions and Measurement

- Which temporal dimensions are measurable from observed behavior (arrival processes, cancellation intensity, burstiness) without relying on self-declaration? High-frequency Hyperliquid order-book data is independently obtainable and offers a starting dataset [13].
- Can aggregate predictability be made credible without exposing proprietary strategy?
- Can the predictable low-latency stream be distinguished, and priced differently, from unpredictable preemptive demand - without abandoning price competition?
- Under Roughgarden's criteria (DSIC, MMIC, OCA-proofness), can a temporally augmented mechanism remain incentive compatible and collusion-resistant [12]?
- How large and material is temporally flexible demand, empirically?

---

## Summary

Hyperliquid exposes execution demand that price alone describes poorly: a sustained, forecastable, low-latency, ordering-sensitive stream punctuated by unpredictable bursts. Under the current definition, these are multiple dimensions of **Temporal Liquidity**. The case does not prove any mechanism, and it does not show that specialized chains are unnecessary. It supports a narrower, defensible conclusion:

> **Economically important blockchain applications generate multidimensional temporal demand that today's spot fee markets under-represent - enough to motivate measuring and market-design study of Temporal Liquidity.**

---

## References

[1] Hyperliquid. "About Hyperliquid." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs
[2] Hyperliquid. "Order Book." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs/trading/order-book
[3] Hyperliquid. "HyperCore Overview." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview
[4] Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper No. 4436697 (posted 14 May 2023; last revised 15 June 2026).
[5] Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. "Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security." *Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security (CCS '22),* 2099-2113. https://doi.org/10.1145/3548606.3559341
[6] Kleinrock, L. *Queueing Systems, Volume 1: Theory.* Wiley, 1975 (Pollaczek-Khinchine mean-value formula).
[7] Pacheco, M., Oliva, G. A., Rajbahadur, G. K. & Hassan, A. E. "Is My Transaction Done Yet? An Empirical Study of Transaction Processing Times in the Ethereum Blockchain Platform." 2022. https://arxiv.org/abs/2206.08959
[8] Zhang, L. & Zhang, F. "Understand Waiting Time in Transaction Fee Mechanism: An Interdisciplinary Perspective." 2023. https://arxiv.org/abs/2305.02552
[9] Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN Working Paper, 2026. See also *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost,* arXiv:2509.22143, for the centralization evidence.
[10] TLM Research Program. *Vision Statement.* Canonical definition and motivation for Temporal Liquidity (umbrella concept).
[11] Buterin, V., Conner, E., Dudley, R., Slipper, M., Norden, I. & Bakhta, A. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals, 2019. https://eips.ethereum.org/EIPS/eip-1559
[12] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *Journal of the ACM,* 2024. (DSIC / MMIC / OCA-proofness framework.)
[13] Albers, J. "Level 4 Order Book Data from the Hyperliquid Exchange." SSRN Working Paper No. 6465720, 2026.
[14] Hyperliquid. "Interacting with HyperCore" (HyperEVM read precompiles, CoreWriter system contract, CoreWriter action delay) and "Oracle." *Hyperliquid Documentation.* https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/hyperevm/interacting-with-hypercore *(verified July 2026).*

---

## Revision Note

*Substantive changes only - claims added, qualified, or withdrawn, so that anyone citing an earlier version can see what has changed. Editorial, formatting, and metadata changes are in the repository history.*

**Version 0.7**

- **Reframes the note from an *empirical* case study to a *motivating* one.** The note describes Hyperliquid's architecture and cites adjacent empirical work; it does not measure Hyperliquid's own workload. Earlier phrasing overstated this, and the "empirical case study" description should not be cited.
- **Qualifies the sec. 5 queueing claim.** Pollaczek-Khinchine concerns service-time variance, not arrival forecastability; predictability lowers delay only given a forecast-aware scheduler and a stated error.
- **Adds sec. 6.2, HyperEVM's dual-block lanes**, as a production instance of coarse protocol-native temporal differentiation, with its limits stated: two predefined classes, account-based selection, and latency coupled to atomic capacity.

**Version 0.6**

- **Adds the system as actually built (sec. 6.1)** - HyperCore and HyperEVM, including CoreWriter's deliberate delay as a temporal mechanism - and frames two execution environments under one consensus as the RN-08 / RN-09 precursor.

**Version 0.5**

- **Aligns the definition to the Vision: Temporal Liquidity is the umbrella**, with predictability, continuity, and execution priority as its dimensions. v0.2 placed predictability outside Temporal Liquidity; that framing should not be cited.
- **Adds execution priority as a dimension**, grounded in Hyperliquid's price-time-priority book.
- **Does not adopt v0.3 / v0.4's extended exchange-architecture comparison**, which broadened scope beyond the note's motivating purpose.
