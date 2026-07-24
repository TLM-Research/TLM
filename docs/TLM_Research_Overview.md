# Temporal Liquidity Market (TLM)

# Research Overview (PR3)

**Release:** TLM Public Release 3
**Status:** Public Draft — research outreach
**Last Updated:** July 2026

---

## Can decentralized execution markets coordinate more than price?

Ethereum has shown that protocol design can improve decentralized market infrastructure. EIP-1559 turned fee-setting into a protocol-governed mechanism [1]; Proposer–Builder Separation and the move toward Enshrined PBS (EIP-7732) restructured how blocks are built and ordering value is captured [2, 3]. Each step made an economically meaningful variable — congestion, block construction — legible to the protocol through simple, deterministic rules.

These mechanisms coordinate one economic variable exceptionally well: **price**. This raises a prior question, before any new mechanism is proposed:

> **Should decentralized execution markets coordinate only price, or also the economically meaningful *temporal* characteristics of demand?**

Temporal Liquidity Market (TLM) is an open research program investigating that question. It is deliberately **model-first**: it defines and measures the economic object before designing any mechanism.

---

## The idea, in one figure

```text
                Today's execution market

        ┌────────────────────────────────┐
        │           User demand           │
        │   Price               ✓ visible │
        │   Temporal structure  ✗ implicit│
        └───────────────┬────────────────┘
                        │  (compressed into one scalar fee, after arrival)
                        ▼
                Resource allocation ──► Blockspace


                Temporal Liquidity Market

        ┌────────────────────────────────┐
        │           User demand           │
        │   Price                         │
        │   Temporal Liquidity (umbrella):│
        │     • execution priority        │  intra-slot (ordering)
        │     • delay tolerance           │  inter-slot
        │     • execution window / deadline
        │     • predictability            │  stream-level
        │     • continuity                │
        └───────────────┬────────────────┘
                        │  simple, protocol-neutral, extraction-resistant?
                        ▼
             Richer market coordination
                        │
        Previously unrealized mutually-beneficial executions
                        │
                 Social surplus?  (falsifiable hypothesis)
```

---

## The core concept: Temporal Liquidity

TLM introduces **Temporal Liquidity** as an *umbrella* economic concept — deliberately analogous to **market liquidity**, which is not one quantity but a family of properties (depth, immediacy, resiliency) [4, 5]. In the same spirit:

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

Its dimensions can be organized by temporal granularity: **execution priority** (intra-slot ordering), **delay tolerance / windows / deadlines** (inter-slot), and **predictability / continuity** (stream-level). Some are *declared preferences* a market would price; others are *observed properties* that can only earn a coordination benefit if verified. At the transaction level, Temporal Liquidity is the demand-side dual of the **cost of delay** — how much value an application forgoes as execution is postponed [6].

This is not a claim to a new economic idea. Time-differentiated demand is a mature feature of real market systems — peak-load and congestion pricing, electricity demand response, cloud reserved-vs-spot markets, and payment-system settlement tiering (real-time gross settlement vs deferred net settlement). **The novelty is the setting**: coordinating this demand under permissionless, adversarial, decentralized, neutrality-constrained conditions.

---

## What is already known (and what TLM inherits)

TLM sits at the intersection of four mature literatures, and it aims to *inherit their results*, not restate their questions.

**Financial economics — liquidity and the cost of time.** Market liquidity is understood as multidimensional [4, 5], and demand's sensitivity to execution timing is a *price-elasticity*-like object. Empirically, delay carries real, heterogeneous cost: Zhao estimates the cost of delay directly from the Ethereum fee market [6]. TLM treats Temporal Liquidity as the demand-side counterpart to that cost, and asks whether it can be priced without being expropriated.

**Mechanism and market design.** Formally, TLM proposes to enlarge the **message space** of the transaction fee mechanism — from a scalar bid to a vector that also carries temporal characteristics. Roughgarden's transaction-fee-mechanism framework supplies the evaluation criteria (DSIC, myopic-miner incentive compatibility, off-chain-agreement proofness) and shows EIP-1559 satisfies them outside demand spikes [7]. His impossibility results are a discipline, not a footnote: enlarging the message space can make these guarantees *harder* to hold jointly, which tells TLM exactly which trade-offs to test. The revelation principle and signaling theory frame whether agents will report temporal information truthfully at all. Closest of all is the *tiered* fee mechanism of Kiayias, Koutsoupias, Lazos & Panagiotakos, which prices one temporal dimension — urgency — keeping low-urgency transactions cheap and admitting more diverse traffic than EIP-1559 without sacrificing revenue [15]; TLM generalizes that single-axis result to the full umbrella of temporal characteristics.

**Networking and QoS — the cautionary precedent.** The Internet already ran this experiment. Rich per-flow reservation (IntServ/RSVP) failed to scale, while coarse, stateless class marking (DiffServ) deployed [8, 9]. The deeper lesson is that expressive service differentiation is achievable *without* per-flow state in the core — core-stateless fair queueing being the canonical demonstration [10] — and the end-to-end argument warns against pushing application semantics into the network [11]. TLM takes this as a design constraint: any protocol-visible temporal abstraction must be coarse, stateless-friendly, and neutral, or it will not survive.

**Empirical execution-timing economics.** Beyond the cost of delay [6], EIP-1559's effect on waiting time is measured [12], and *time-as-priority* now exists in production: Arbitrum's Timeboost auctions an express lane. Capponi & Zhu show such an auction can reduce wasteful latency races (a surplus argument) [13], while independent analysis finds it can also drive spam and centralization [14] — a live instance of the extraction risk TLM must confront.

---

## The central tension, stated plainly

Communicating temporal information *before* allocation is exactly what can expose it to extraction — front-running, and MEV more broadly. Any protocol-visible temporal abstraction must therefore be evaluated on **extraction-resistance**, not only coordination benefit. Reconciling early revelation with extraction resistance is a defining problem of this program, not a detail to defer.

---

## Why better market design could create value (not merely move it)

TLM is not about redistributing value or asking the network to subsidize patient users. The hypothesis is that price-only markets leave mutually beneficial executions *unrealized* because they express too little about demand. Surplus could arise through two channels: **unlocking suppressed demand** (executions that a more expressive market would enable), and **removing coordination waste** (e.g. dampening the latency arms race, per Timeboost's evidence [13]). Both are surplus *creation*. The claim is falsifiable: if temporally flexible demand proves negligible, unidentifiable, or brings no measurable coordination gain, the framework should be revised or abandoned.

---

## A model-first program

1. Identify economically meaningful variables.
2. Determine which are already protocol-visible.
3. Investigate whether additional variables merit protocol-visible representation.
4. Only then, design and evaluate mechanisms — separating **concept**, **representation**, and **mechanism**.

---

## Open problems I think are worth attacking

Stated as hard problems, not a wish list — these are where I would most value collaboration:

- **Extraction-resistant representation.** What temporal abstraction is expressive enough to be useful, yet coarse and private enough to resist front-running and preserve neutrality? (The DiffServ / core-stateless constraint [9, 10] meets the MEV constraint.)
- **Incentive-compatible revelation.** Under Roughgarden's criteria [7], can a temporally augmented fee mechanism remain DSIC and collusion-resistant, or is there an impossibility that bounds what temporal coordination can achieve?
- **A dynamic temporal-liquidity reserve.** Could a reserve funding time-based surcharges and subsidies improve coordination while staying incentive-compatible and approximately budget-balanced?
- **Measurement and identification.** Observed fees reveal behavior under today's mechanism, not latent temporal preference. What identification strategy (revealed preference, natural experiments, order-book data) recovers the underlying cost-of-delay and predictability structure?

---

## Where to go next

1. **Vision Statement** — the umbrella concept and guiding principles.
2. **Foundation Statement (I–III)** — conceptual framework, evaluation criteria, falsifiability.
3. **Related Work** — the inherited results from each discipline above.
4. **Research Notes** — focused investigations (e.g. RN-03, a cited Hyperliquid case study of multidimensional temporal demand).

---

## Invitation

This is an invitation to critique, not a proposal for adoption. I would especially value feedback from researchers in financial economics (liquidity and the cost of time), mechanism and market design, networking and QoS, and the empirical economics of execution delay. The primary question is not whether a particular mechanism should be adopted, but whether **protocol-visible temporal characteristics of demand** are a worthwhile direction for decentralized execution markets — and, if so, what the right abstraction and the binding impossibilities are.

**Project repository:** https://github.com/TLM-Research

---

## References

[1] Buterin, V., Conner, E., Dudley, R., Slipper, M., Norden, I. & Bakhta, A. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals, 2019.

[2] *Proposer–Builder Separation.* Ethereum protocol roadmap; Flashbots MEV-Boost.

[3] *EIP-7732: Enshrined Proposer–Builder Separation (ePBS).* Ethereum Improvement Proposals.

[4] Kyle, A. S. "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1985. (Market depth / liquidity dimensions.)

[5] Amihud, Y. & Mendelson, H. "Asset Pricing and the Bid–Ask Spread." *Journal of Financial Economics* 17(2), 1986.

[6] Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper 4436697 (rev. 15 June 2026).

[7] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *Journal of the ACM*, 2024.

[8] Braden, R., Clark, D. & Shenker, S. *Integrated Services in the Internet Architecture (IntServ).* RFC 1633, 1994.

[9] Blake, S. et al. *An Architecture for Differentiated Services (DiffServ).* RFC 2475, 1998.

[10] Stoica, I., Shenker, S. & Zhang, H. "Core-Stateless Fair Queueing: Achieving Approximately Fair Bandwidth Allocations in High-Speed Networks." *ACM SIGCOMM*, 1998.

[11] Saltzer, J. H., Reed, D. P. & Clark, D. D. "End-to-End Arguments in System Design." *ACM TOCS* 2(4), 1984.

[12] Liu, Y., Lu, Y., Nayak, K., Zhang, F., Zhang, L. & Zhao, Y. "Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time, and Consensus Security." *ACM CCS*, 2022.

[13] Capponi, A. & Zhu, B. *Auctioning Time to Mitigate Latency Races: Theory and Evidence from Blockchains.* SSRN Working Paper, 2026.

[14] *The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost.* arXiv:2509.22143.

[15] Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014, 2023; *Mathematical Research for Blockchain Economy* (Springer), 2024.
