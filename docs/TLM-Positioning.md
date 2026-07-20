# TLM Positioning — Exchange Designer, Not Exchange

**Status:** Public Draft — positioning statement (reusable as outreach preamble)
**Last Updated:** July 2026

---

## Where TLM's contribution lies

Temporal Liquidity Market (TLM) is a research program in **temporal market design** for decentralized execution. Its contribution is deliberately *upstream* of any auction or protocol mechanism. TLM's work is to:

- **Define the object** — Temporal Liquidity, the collection of economically meaningful temporal characteristics of execution demand, precise enough to be measured.
- **Establish the information model** — which temporal characteristics could become protocol-visible, and how.
- **State the constraints** — neutrality, extraction-resistance, simplicity, incentive-compatibility, and decentralization — that *any* mechanism coordinating this demand must satisfy.
- **Measure that the demand is real** — through empirical work (e.g. the Hyperliquid case study and the economics of delay).

It is **not** TLM's role to build the auction that clears this demand. That is the domain of the actors who live in it — builders, proposers, searchers — and of the mechanism- and auction-design community.

## The analogy: we design exchanges; we are not an exchange

An exchange designer specifies the tradable object, the information the market reveals, and the rules the market must honor. Traders devise strategies within those rules. In the same way, TLM specifies *what temporal information a market could coordinate, and under what constraints*; builders and proposers optimize within it, and auction researchers design the clearing mechanism.

This mirrors how durable market institutions are built: the market designer writes the rules; the participants trade. TLM is in the designer's seat, one layer above the auction.

| Layer | Owner | Question |
|---|---|---|
| Commodity + information model + constraints | **TLM** | *What temporal demand exists, what should be visible, under what rules?* |
| Clearing / allocation mechanism | Auction & mechanism designers | *How is it matched and priced?* |
| Strategy within the market | Builders, proposers, searchers | *How do I optimize given the rules?* |

## Model-first is logical priority, not timidity

A market cannot auction a commodity that has not been defined. Naming and measuring the object is *prior to* — and enabling of — mechanism design. This is how new fields form: the object is named and measured before the mechanisms arrive. Asymmetric information was named before the contract theory it launched; market liquidity's dimensions were characterized before the mechanisms that priced them; congestion pricing named the externality decades before its deployments.

TLM's ambition is to found the analogous field for decentralized execution — **temporal market design**. The contribution is to make a latent, real, and hard problem *legible and well-posed*, which is precisely what unlocks a design space for others to fill.

## Where concrete mechanisms fit

Model-first does not forbid concrete mechanisms; it *orders* them. A candidate mechanism is most valuable as an **existence proof** — a demonstration that the design problem is solvable in principle, offered as one point in the space rather than as the answer. Such candidates live in dated Research Notes, where they establish feasibility (and authorship) without turning the program into advocacy for a single design.

A well-posed problem *and* one constructive result is far more credible than either alone: the problem shows the work matters; the existence proof shows it is not hopeless. TLM's own origin includes such a candidate — a network-level reserve for incentivizing diversified temporal demand and its supply-side allocation — which is developed in the Research Notes as a feasibility demonstration, not as the program's thesis.

## The invitation

TLM therefore asks the mechanism-design, market-design, networking, and financial-economics communities not to adopt a particular protocol, but to help pose and solve a newly legible problem: whether, and how, decentralized execution markets should coordinate the *temporal structure* of demand alongside its price.
