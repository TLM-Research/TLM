# Temporal Liquidity Market (TLM)

**An open research program on temporal liquidity and its role in blockchain protocols.**

Temporal Liquidity Market (TLM) is an open research project investigating whether decentralized execution markets should coordinate not only **price**, but also the economically meaningful **temporal characteristics of demand** — *when*, *in what order*, and *how predictably* execution is needed.

The name carries two contributions. **Temporal Liquidity** is a first-degree, protocol-visible variable, alongside price: the timing structure of demand that a scalar fee compresses away. **Market** is what coordinating that variable creates — a *two-sided* market, with demand that needs execution at a particular time or order (takers) on one side, and the supply of execution capacity across blockchain time, including flexibility that patient demand can release (suppliers), on the other. TLM studies both the variable and the market that clears it.

It is **model-first**: concepts, representations, and evaluation criteria come first. It then follows with **conceptual mechanism design** and a **foundational evaluation framework**, so that candidate mechanisms for coordinating Temporal Liquidity can be stated and assessed rather than only motivated.

---

## The question

Ethereum has repeatedly improved decentralized coordination by making an economically meaningful variable protocol-visible — congestion through **EIP-1559**, block construction through **PBS** and **ePBS**. Each step coordinated **price** better. TLM asks the prior question:

> **Should decentralized execution markets coordinate only price, or also the economically meaningful temporal characteristics of demand?**

---

## Temporal Liquidity

**Temporal Liquidity** is used as an *umbrella* concept — analogous to **market liquidity**, which is itself a family of properties (depth, immediacy, resiliency) rather than a single quantity:

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

Its dimensions, by temporal granularity:

- **execution priority** — sensitivity to ordering *within* a slot
- **delay tolerance**, **execution windows**, **deadlines** — across slots
- **predictability**, **continuity** — across a stream of demand

The canonical exposition — the market-liquidity analogy, the deadline-versus-decay structure, and worked examples — lives in [`docs/Temporal-Liquidity.md`](docs/Temporal-Liquidity.md).

---

## The two sides of the market

Naming the variable is the demand side. Coordinating it requires a supply side and a price, and the research notes develop both:

- **Demand** — the economic object is not the transaction but the *project*: a long-lived source of execution demand with a temporal profile — a perpetual exchange, an oracle network, a payment network, a rollup, a game world (RN-01, RN-03, RN-10).
- **Supply** — capacity per unit of blockchain time is roughly uniform, but demand is not; temporal liquidity is supplied when patient demand releases its claim on a contended quantum for time-sensitive work to use, and how that supply is organized — differentiated service classes over a sub-slot granularity — is developed in RN-04 and RN-05.
- **Price** — the two sides meet in a *term structure of block-fee-rates*, which RN-11 develops by analogy to the bond market: bootstrapped from future-slot instruments, with the allocation problem's dual as its efficiency benchmark (RN-10, RN-11).

Seen this way (RN-10), a blockchain is less a transaction-processing engine than an **execution-capital market** that finances a diverse ecosystem of projects by allocating capacity across time — and a market in temporal liquidity is what makes that allocation expressible.

---

## Positioning — exchange designer, not exchange

TLM begins *upstream* of any auction: it defines the temporal commodity, the information a market makes visible, and the constraints — neutrality, extraction-resistance, simplicity, incentive-compatibility — that any mechanism must satisfy. It then builds on that foundation toward **candidate market mechanisms**, evaluated against those constraints and developed within the project — while actively welcoming competing and complementary mechanism proposals from the builder, proposer, and auction- and mechanism-design community. See [`docs/TLM-Positioning.md`](docs/TLM-Positioning.md).

---

## Approach — model-first foundations, then market mechanisms

1. Model the market's economically meaningful variables.
2. Determine which are already protocol-visible.
3. Investigate which additional variables merit protocol-visible representation.
4. Design and evaluate **market mechanisms** that coordinate them — separating **concept**, **representation**, and **mechanism**.

Steps 1–3 are the model-first foundation. Step 4 is under way at the conceptual level, developed in-project and open to contributions and competing proposals from the community.

---

## An interdisciplinary program

TLM sits at the intersection of four mature literatures and aims to *inherit their results* rather than restate their questions:

- **Financial economics** — liquidity as a multidimensional property; the cost of time.
- **Mechanism & market design** — TLM as a *multidimensional transaction fee mechanism*, evaluated under DSIC / MMIC / OCA-proofness.
- **Networking & QoS** — the IntServ/DiffServ lesson; coarse, stateless descriptors.
- **Empirical execution-timing economics** — the cost of delay; time-as-priority (Arbitrum Timeboost).

The full literature map is in [`docs/Related-Work.md`](docs/Related-Work.md).

---

## Status — September 2026

Published: **RN-01 to RN-17**, plus **RN-26** and **RN-33**.

RN-01 to RN-14 build the concept, its representation, and the economics. **RN-15 to RN-17 are the first mechanism proposals, and Ethereum is the primary target**: a temporal liquidity authorization for EIP-1559, a two-leg reserve across neighbouring slots, and a shift of the unit from the transaction to the stream. They are proposals offered for comment.

RN-26 and RN-33 begin a second line, applying the framework to a fast L1 where short blocks and parallel execution change what temporal liquidity is worth. RN-33 is stated as an architecture with hypotheses and experiments rather than as a specification. Work on other fast L1s, L2s, and oracle networks is in progress and not yet published.

---

## Repository map

```text
docs/
    Vision-Statement.md          — the umbrella concept and guiding principles
    TLM-Research-Overview.md     — outward-facing research invitation
    TLM-Positioning.md           — where TLM's contribution lies
    Foundation-Outline.md        — structure of the Foundation Statement
    Foundation-1-Introduction.md — Part I: introduction & the concept
    Foundation-2-Framework.md    — Part II: principles & model-first methodology
    Foundation-3-Future-Research.md — Part III: research agenda & falsifiability
    Temporal-Liquidity.md        — canonical concept exposition
    Related-Work.md              — interdisciplinary literature map
    Research-Notes/
        RN-01, RN-02   Temporal Execution Profile; protocol-visible temporal abstraction
        RN-03, RN-14   Evidence: Hyperliquid; the demand Ethereum does not serve
        RN-04, RN-05   Service classes for Ethereum; supply-side granularity
        RN-06 – RN-09  Host analysis, layered control, comparative survey, chain virtualization
        RN-10, RN-11   The execution-capital market; its term structure via the bond-market mapping
        RN-12, RN-13   Conceptual mechanism design; capacity and welfare
        RN-15 – RN-17  Ethereum mechanisms: TLA for EIP-1559, two-leg reserve, stream profiles and tickets
        RN-26, RN-33   Monad: a TLM framework and roadmap; horizontal scheduling classes
```

---

## Where to start

- **New here?** Read the [Research Overview](docs/TLM-Research-Overview.md).
- **Want the concept?** [Temporal Liquidity](docs/Temporal-Liquidity.md).
- **Want the framework?** The Foundation Statement — [Part I](docs/Foundation-1-Introduction.md) · [Part II](docs/Foundation-2-Framework.md) · [Part III](docs/Foundation-3-Future-Research.md).
- **Want the evidence?** [RN-03: Hyperliquid](docs/Research-Notes/RN-03_Hyperliquid_A_Case_Study_in_Temporal_Liquidity.md).
- **Want the market view?** [RN-10: Temporal Liquidity and the Blockchain Economy](docs/Research-Notes/RN-10_Temporal_Liquidity_and_the_Blockchain_Economy.md).
- **Want a mechanism?** [RN-15: A Temporal Liquidity Authorization for EIP-1559](docs/Research-Notes/RN-15_A_Temporal_Liquidity_Authorization_for_EIP-1559.md).
- **Want the fast-L1 case?** [RN-33: Horizontal Scheduling Classes for Monad](docs/Research-Notes/RN-33_Horizontal_Scheduling_Classes_for_Monad.md).

---

## Contributing

TLM is an open research project. Critique, discussion, and alternative or competing approaches are welcome — especially from distributed systems, networking, mechanism and market design, and financial economics. The primary question is not whether a particular mechanism should be adopted, but whether **protocol-visible temporal characteristics of demand** are a worthwhile direction for decentralized execution markets — and, if so, what the right abstraction and the binding impossibilities are.
