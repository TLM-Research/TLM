# Foundation Statement - Part III: Future Research

**Version:** 1.3
**Status:** Public Draft
**Last Updated:** August 6, 2026

Part III closes the Foundation by turning the framework into a research program: the market that gives the program its name, a mechanism-design *space* (not a mechanism), an agenda for *measuring* Temporal Liquidity, explicit non-goals, and the conditions under which the program could be confirmed, refined, or rejected.

---

# 9. The Temporal Liquidity Market

Naming the temporal characteristics of demand is one part of the program; the other is the **market**. Once those characteristics are made protocol-visible variables, the question becomes how to coordinate them, and the direction TLM pursues is a two-sided market for **temporal liquidity**: impatient execution demand that needs particular timing *takes* it, and patient, flexible demand *provides* it, the two clearing into a *price of time*.

Read at that scale, a blockchain is less a transaction-processing engine than an **execution-capital market** - one that allocates execution capacity across time and finances a diverse set of projects, including the timing-sensitive ones that today leave for sovereign chains. The price of time takes the form of a **term structure of block-fee-rates**, constructed by analogy to the bond market and made mutually consistent under no-arbitrage, with the allocation problem's dual as a welfare benchmark against which the market curve can be judged. The economics of this market are developed in RN-10, and its formal foundation - the term structure and the execution-capital allocation problem - in RN-11. Designing the protocol and market mechanism that would clear it is the subject of the design space below and of the upcoming mechanism-design notes.

---

# 10. Mechanism Design Space

The central contribution of TLM is the conceptual framework and the market it defines, not any single mechanism. Future mechanisms - temporal queues, execution windows, adaptive pricing, reserve-based designs, multi-horizon markets, future-slot instruments, and others - are candidate points in a design space, to be compared against the common evaluation criteria stated in Part II (sec. 9) rather than judged in isolation. This design space already has worked reference points: the tiered urgency-based fee mechanism of Kiayias, Koutsoupias, Lazos & Panagiotakos (2023) - an IOG/Cardano research design, not (as far as we know) a deployed one - which coordinates a single temporal dimension and which TLM treats as the urgency-axis precedent it generalizes; and, within the program, a first candidate two-sided clearing mechanism to be developed in the mechanism-design notes (RN-12 onward). Because the criteria attach to the framework and not to any one design, multiple candidates can be evaluated without redefining the underlying concept of temporal liquidity.

---

# 11. Measuring Temporal Liquidity

A central research direction is whether the temporal characteristics of demand - and their individual dimensions (delay tolerance, predictability, execution priority, continuity) - can be measured empirically. This is best viewed as an **identification problem**, not a data-collection problem: observed fees reveal behavior *under today's mechanism*, not the latent temporal characteristics of demand, so inferring the underlying value-versus-delay structure is a causal-inference problem (endogeneity, selection, strategic bidding), not merely a matter of gathering traces.

The methodology has direct precedents worth inheriting - the estimation of the *value of time* in transportation economics and of *demand elasticity* in electricity markets both recover latent temporal preferences from behavior, and the `Related-Work` document collects these. Candidate approaches include revealed-preference analysis, natural experiments, agent-based simulation, and controlled protocol experiments. Candidate datasets include public mempool traces, transaction-inclusion delays, MEV-Boost relay data, rollup sequencing data, and application-specific execution histories. The objective is not to collect data for its own sake, but to determine whether temporally flexible demand exists in economically meaningful quantities - the minimal empirical test the whole program rests on.

---

# 12. Protocol Evolution

The Foundation intentionally avoids prescribing Ethereum's roadmap; it offers a lens through which future evolution may be interpreted. It is nonetheless worth naming the architectural developments that would make protocol-visible temporal information *cheap to add*, since they bound what is practical: ePBS commitment slots and inclusion lists (which create places to attach or honor forward commitments), blob-style multidimensional fee pricing (which shows a new protocol-visible resource dimension can be introduced), and extended proposer lookahead (which is what would let anyone credibly speak for future slots). A market for temporal liquidity is one candidate direction that such developments could support, not a predetermined destination.

---

# 13. Non-goals

TLM is **not** a new consensus protocol, a replacement for PBS or EIP-1559, a proposal for a single mandatory mechanism, an attempt to maximize execution speed, or a complete execution-market solution. They are echoed in the Part I scope, so that a reader of either document encounters them.

---

# 14. Falsifiability

A useful research framework must name the observations that would weaken or invalidate its central hypothesis. For TLM these include: empirical evidence that temporally flexible demand is economically negligible; an inability to identify useful temporal information from observable behavior; protocol-visible temporal information consistently reducing welfare or decentralization; and no measurable scheduling benefit despite richer temporal information. None is an expected outcome.

---

# 15. Relationship to the Research Notes

The Foundation establishes the agenda; the Research Notes investigate individual questions in depth, which keeps the Foundation stable while the notes evolve. The thirteen notes to date span both sides of the market and the market itself:

- **RN-01 - Temporal Execution Profile.** The transaction-level representation of temporal demand.
- **RN-02 - Protocol-visible Temporal Abstraction.** How temporal characteristics can be made visible to the protocol, and the declared-versus-verified distinction.
- **RN-03 - Hyperliquid: A Case Study in Temporal Liquidity.** An application study of multidimensional temporal demand.
- **RN-04 - Temporal Execution Services.** A multi-class execution architecture for Ethereum - the service and supply side.
- **RN-05 - Supply-side Heterogeneity and Temporal Granularity.** A quantum lattice for blockspace: sub-slot granularity and heterogeneous supply.
- **RN-06 - Monad Through the Temporal-Liquidity Lens.** A host analysis - motivation, novelty, and limits.
- **RN-07 - A Layered Control Architecture for Temporal Liquidity.** Multi-timescale, reducible control for blockchain execution markets.
- **RN-08 - Modern Blockchains Through the Lens of TLM.** A three-layer architecture, and the case for decoupling execution from control.
- **RN-09 - Chain Virtualization.** A conceptual frame for diversified project types on a shared fast L1.
- **RN-10 - The Economics of the Temporal Liquidity Market.** How TLM expands the blockchain economy: the blockchain as an execution-capital market (with a companion follow-up research-questions note).
- **RN-11 - The Term Structure and Allocation of Execution Capital.** The term structure of block-fee-rates, and the execution-capital allocation problem and its dual.
- **RN-12 - The Temporal Liquidity Market: Protocol and Mechanism Design.** A first candidate mechanism for clearing the market. In draft.
- **RN-13 - Toward a Mathematical Theory of Execution Capacity.** Multi-user demand, temporal resolution, information, and fundamental limits. In draft.

---

# 16. Conclusion

The Foundation began by naming the economically meaningful *temporal characteristics* of execution demand - delay tolerance, predictability, execution priority, execution windows and deadlines, and continuity - and arguing that a scalar fee throws them away.

The thesis is not one more variable but a **market**: one in which impatient demand takes temporal liquidity and patient, flexible demand provides it, clearing into a price of time. If it works, a blockchain can economically support a wider and more diverse set of projects.

What the Foundation supplies is the conceptual framework, the research questions, the evaluation criteria, and the conditions under which the program may be confirmed, refined, or rejected. The argument has since carried through to the economics of the market (RN-10) and its formal foundation (RN-11). The protocol and market design that would realize it is next.
