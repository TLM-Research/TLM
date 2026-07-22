# TLM Positioning — Exchange Designer, Not Exchange

**Status:** Public Draft — positioning statement (reusable as outreach preamble)
**Last Updated:** July 2026

---

## Where TLM's contribution lies

Temporal Liquidity Market (TLM) is a research program in **temporal market design** for decentralized execution, pursued in two phases.

**Phase 1 — foundations (model-first).** TLM's first work is upstream of any auction:

- **Define the object** — Temporal Liquidity, the collection of economically meaningful temporal characteristics of execution demand, precise enough to be measured.
- **Establish the information model** — which temporal characteristics could become protocol-visible, and how.
- **State the constraints** — neutrality, extraction-resistance, simplicity, incentive-compatibility, and decentralization — that *any* mechanism coordinating this demand must satisfy.
- **Measure that the demand is real** — through empirical work (e.g. the Hyperliquid case study and the economics of delay).

**Phase 2 — market mechanisms.** Building on that foundation, TLM develops and evaluates **candidate market mechanisms** that coordinate this demand against the Phase-1 constraints — while actively welcoming competing and complementary proposals from the mechanism-design, market-design, builder, and proposer communities.

What TLM is *not* is a live trading venue or a market participant. It sits in the market **designer's** seat, which is exactly why the ordering matters: the commodity and its rules are defined before the mechanism that clears them.

## The analogy: we design exchanges; we are not an exchange

An exchange designer specifies the tradable object, the information the market reveals, the rules the market must honor, and the mechanism that clears it. Traders devise strategies within those rules. In the same way, TLM specifies *what temporal information a market could coordinate, under what constraints* (Phase 1), and then designs and evaluates the mechanisms that coordinate it (Phase 2); builders, proposers, and searchers optimize within the resulting rules.

This mirrors how durable market institutions are built: the market designer writes the rules and the mechanism; the participants trade. TLM is in the designer's seat — not a trading venue.

| Layer | Owner | Question |
|---|---|---|
| Commodity + information model + constraints *(Phase 1)* | **TLM** | *What temporal demand exists, what should be visible, under what rules?* |
| Market mechanism / clearing rules *(Phase 2)* | **TLM**, with the mechanism- and market-design community | *How is it matched and priced?* |
| Strategy within the market | Builders, proposers, searchers | *How do I optimize given the rules?* |

## Model-first is logical priority, not timidity

A market cannot auction a commodity that has not been defined. Naming and measuring the object is *prior to* — and enabling of — mechanism design. This is how new fields form: the object is named and measured before the mechanisms arrive. Asymmetric information was named before the contract theory it launched; market liquidity's dimensions were characterized before the mechanisms that priced them; congestion pricing named the externality decades before its deployments.

TLM's ambition is to found the analogous field for decentralized execution — **temporal market design**. The contribution is to make a latent, real, and hard problem *legible and well-posed*, then to build candidate mechanisms on it — unlocking a design space the project and the wider community fill together.

## Where concrete mechanisms fit

Model-first does not forbid concrete mechanisms; it *orders* them. A candidate mechanism is most valuable as an **existence proof** — a demonstration that the design problem is solvable in principle, offered as one point in the space rather than as the answer. Such candidates live in dated Research Notes, where they establish feasibility (and authorship) without turning the program into advocacy for a single design.

A well-posed problem *and* one constructive result is far more credible than either alone: the problem shows the work matters; the existence proof shows it is not hopeless. TLM's own work includes such a candidate, developed privately as a feasibility demonstration rather than presented as the program's thesis, and introduced publicly only once the problem it addresses is sufficiently established.

## The invitation

TLM therefore asks the mechanism-design, market-design, networking, and financial-economics communities not to adopt a particular protocol, but to help pose and solve a newly legible problem: whether, and how, decentralized execution markets should coordinate the *temporal structure* of demand alongside its price.
