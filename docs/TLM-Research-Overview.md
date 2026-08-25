# Temporal Liquidity Market (TLM)

# Research Overview (PR4)

**Status:** Public Draft - research outreach  
**Last Updated:** August 6, 2026

---

## Can decentralized execution markets coordinate more than price?

Ethereum's fee market coordinates one thing well: **price**. EIP-1559 made fee-setting a mechanism [1]; Proposer-Builder Separation and ePBS restructured block construction [2, 3]. But price is not the only economically meaningful thing about demand.

> **Should decentralized execution markets coordinate only price - or also the *temporal* characteristics of demand: when, in what order, and how predictably execution happens?**

---

## Why it matters: the highest-value flow is already leaving

The most sophisticated, latency-sensitive applications have left general-purpose chains. dYdX rebuilt as a Cosmos app-chain; Hyperliquid launched its own L1; Aevo moved matching off-chain [12]. Each gave up Ethereum's security, liquidity, and composability - a steep price - to get control over *timing and ordering*, which the shared market neither prices nor protects.

This is not a throughput story. A faster EVM chain such as Monad [13] removes the throughput reason to leave but not the timing one. Leaving timing unpriced costs a chain its highest-value flow and narrows the set of projects it can sustain. It is a coordination failure rather than a capacity limit: a price-only market leaves mutually beneficial executions unrealized because it says too little about demand.

---

## The idea

TLM introduces **temporal liquidity** to model the heterogeneous execution demands of a blockchain's projects through their *temporal characteristics* - when, in what order, and how predictably each needs to execute. It then makes these characteristics **protocol-level variables** - visible, coarse, and neutral - and builds the **protocol mechanism and market design** that coordinates them. Modeled this way, temporal demand can be served by fee mechanisms that a timing-blind scalar fee cannot match; designing them is one of the open questions this program takes on. The aim is a blockchain that can economically support a wider set of projects, including the timing-sensitive ones that today leave for sovereign chains.

---

## The hard problem, and insights from adjacent fields

Making temporal demand protocol-visible is hard because expressiveness fights three constraints at once: a decentralized network cannot hold rich per-transaction state (scalability), it must treat participants alike (neutrality), and revealing timing before execution invites front-running and MEV (extraction-resistance).

Two adjacent fields have faced similar tensions, and their solutions are instructive analogies; a decentralized, adversarial, neutrality-constrained chain is its own setting with its own mechanisms. **Networking QoS** met expressiveness against scalability with coarse, stateless, neutral service classes rather than per-flow reservation (DiffServ over IntServ, core-stateless fair queueing) [8-11] - an insight for how TLM *represents* temporal demand. **Quantitative finance** has long priced time and flexibility - the term structure of interest rates, liquidity priced by patience [4-6] - an insight TLM draws on to read blockspace as execution capital, give the price of time a *term structure of block-fee-rates* through the principle of no-arbitrage, and to model temporal liquidity as a two-sided market. In each case the analogy only points the way; the abstraction and the mechanisms are TLM's own. The contribution is to carry these insights into protocol and market design that coordinates temporal demand under the adversarial, extraction-resistant, decentralized conditions neither field faced.

---

## An invitation

This is an invitation to critique, not a proposal for adoption. The sharpest open questions sit exactly where these fields meet the blockchain constraint: what temporal abstraction is expressive enough to coordinate yet coarse and private enough to resist extraction; whether a temporally augmented fee mechanism can stay incentive-compatible under known transaction-fee-mechanism impossibilities; and when a decentralized market's price of time would match the efficient one.

I would especially value feedback from researchers in **networking and distributed systems**, in **mechanism and market design**, and in **quantitative finance**. The full development lives in our Vision and Foundation statements, the Related Work survey, and thirteen research notes (RN-01 through RN-13).

**Repository:** https://github.com/TLM-Research

---

## References

[1] *EIP-1559: Fee Market Change for ETH 1.0 Chain.* Ethereum Improvement Proposals, 2019.

[2] *Proposer-Builder Separation.* Ethereum protocol roadmap; Flashbots MEV-Boost.

[3] *EIP-7732: Enshrined Proposer-Builder Separation (ePBS).* Ethereum Improvement Proposals.

[4] Zhao, Y. *The Cost of Delay: Evidence from the Ethereum Transaction Fee Market.* SSRN Working Paper 4436697 (rev. 15 June 2026).

[5] Kyle, A. S. "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1985; Amihud, Y. & Mendelson, H. "Asset Pricing and the Bid-Ask Spread." *Journal of Financial Economics* 17(2), 1986. (Market liquidity as multidimensional; immediacy priced by patience.)

[6] Hull, J. C. *Options, Futures, and Other Derivatives.* (Term structure of interest rates; bootstrapping; swaps and swaptions.)

[7] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *Journal of the ACM*, 2024. (Evaluation criteria and impossibility results for fee mechanisms.)

[8] Braden, R., Clark, D. & Shenker, S. *Integrated Services in the Internet Architecture (IntServ).* RFC 1633, 1994.

[9] Blake, S. et al. *An Architecture for Differentiated Services (DiffServ).* RFC 2475, 1998.

[10] Stoica, I., Shenker, S. & Zhang, H. "Core-Stateless Fair Queueing." *ACM SIGCOMM*, 1998.

[11] Saltzer, J. H., Reed, D. P. & Clark, D. D. "End-to-End Arguments in System Design." *ACM TOCS* 2(4), 1984.

[12] Application-sovereignty exits: dYdX, *Announcing dYdX Chain* (2023); Hyperliquid (sovereign L1 perpetuals DEX); Aevo (off-chain matching with on-chain settlement).

[13] Monad - high-performance, EVM-equivalent Layer-1. https://docs.monad.xyz
