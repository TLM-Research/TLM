# Foundation Statement — Part III: Future Research

**Version:** 1.2
**Status:** Public Draft

Part III closes the Foundation by turning the framework into a research program: a mechanism-design *space* (not a mechanism), an agenda for *measuring* Temporal Liquidity, explicit non-goals, and the conditions under which the program could be confirmed, refined, or rejected. Its posture is to begin the discussion, not conclude it.

---

# 9. Mechanism Design Space

The central contribution of TLM is the conceptual framework, not any single mechanism. Future mechanisms — temporal queues, execution windows, adaptive pricing, reserve-based designs, multi-horizon markets, and others — are candidate points in a design space, to be compared against the common evaluation criteria stated in Part II (§9) rather than judged in isolation. This design space already has at least one worked proposal: the tiered urgency-based fee mechanism of Kiayias, Koutsoupias, Lazos & Panagiotakos (2023) — an IOG/Cardano research design, not (as far as we know) a deployed one — which coordinates a single temporal dimension and which TLM treats as the urgency-axis precedent it generalizes. Because the criteria attach to the framework and not to any one design, multiple candidates can be evaluated without redefining the underlying concept of Temporal Liquidity.

---

# 10. Measuring Temporal Liquidity

A central research direction is whether Temporal Liquidity — and its individual dimensions (delay tolerance, predictability, execution priority, continuity) — can be measured empirically. This is best viewed as an **identification problem**, not a data-collection problem: observed fees reveal behavior *under today's mechanism*, not the latent temporal characteristics of demand, so inferring the underlying value-versus-delay structure is a causal-inference problem (endogeneity, selection, strategic bidding), not merely a matter of gathering traces.

The methodology has direct precedents worth inheriting — the estimation of the *value of time* in transportation economics and of *demand elasticity* in electricity markets both recover latent temporal preferences from behavior, and the `Related-Work` document collects these. Candidate approaches include revealed-preference analysis, natural experiments, agent-based simulation, and controlled protocol experiments. Candidate datasets include public mempool traces, transaction-inclusion delays, MEV-Boost relay data, rollup sequencing data, and application-specific execution histories. The objective is not to collect data for its own sake, but to determine whether temporally flexible demand exists in economically meaningful quantities — the minimal empirical test the whole program rests on.

---

# 11. Protocol Evolution

The Foundation intentionally avoids prescribing Ethereum's roadmap; it offers a lens through which future evolution may be interpreted. It is nonetheless worth naming the architectural developments that would make protocol-visible temporal information *cheap to add*, since they bound what is practical: ePBS commitment slots and inclusion lists (which create places to attach or honor forward commitments), blob-style multidimensional fee pricing (which shows a new protocol-visible resource dimension can be introduced), and extended proposer lookahead (which is what would let anyone credibly speak for future slots). Temporal Liquidity is one candidate direction that such developments could support, not a predetermined destination.

---

# 12. Non-goals

TLM is **not** a new consensus protocol, a replacement for PBS or EIP-1559, a proposal for a single mandatory mechanism, an attempt to maximize execution speed, or a complete execution-market solution. These non-goals are load-bearing — they prevent the most common misreadings — and are echoed in the Part I scope so that a reader of any single document encounters them.

---

# 13. Falsifiability

A useful research framework must name the observations that would weaken or invalidate its central hypothesis. For TLM these include: empirical evidence that temporally flexible demand is economically negligible; an inability to identify useful temporal information from observable behavior; protocol-visible temporal information consistently reducing welfare or decentralization; and no measurable scheduling benefit despite richer temporal information. None is an expected outcome, but stating them establishes that TLM makes testable claims rather than unfalsifiable assertions.

---

# 14. Relationship to the Research Notes

The Foundation establishes the agenda; the Research Notes investigate individual questions in depth, which keeps the Foundation stable while the notes evolve. Current and planned notes include RN-01 (temporal information), RN-02 (protocol-visible temporal abstraction), RN-03 (the Hyperliquid case study of multidimensional temporal demand), and further empirical notes on measuring temporal flexibility, builder-scheduling simulations, and candidate mechanisms.

---

# 15. Conclusion

Temporal Liquidity is proposed as an umbrella for the economically meaningful temporal characteristics of execution demand — delay tolerance, predictability, execution priority, execution windows and deadlines, and continuity. The Foundation deliberately stops short of prescribing mechanisms; instead it establishes a conceptual framework, identifies research questions, proposes evaluation criteria, and defines the conditions under which the framework may ultimately be confirmed, refined, or rejected. In that sense it is intended not as the conclusion of the TLM project, but as the beginning of a broader research program.
