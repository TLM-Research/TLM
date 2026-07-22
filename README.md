# Temporal Liquidity Market (TLM)

**A research program in temporal market design for decentralized execution.**

Temporal Liquidity Market (TLM) is an open research project investigating whether decentralized execution markets should coordinate not only **price**, but also the economically meaningful **temporal characteristics of demand** — *when*, *in what order*, and *how predictably* execution is needed.

It is deliberately **model-first**: it defines and measures the economic object before proposing any mechanism. In market-design terms, TLM designs the market's information layer; it is not itself a market mechanism.

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

## Positioning — exchange designer, not exchange

TLM's contribution is deliberately *upstream* of any auction. It defines the temporal commodity and the information a market makes visible, and states the constraints — neutrality, extraction-resistance, simplicity, incentive-compatibility — that any mechanism coordinating this demand must satisfy. The clearing mechanism is left to the actors who live in it (builders, proposers, searchers) and to the mechanism- and auction-design community. See [`docs/TLM-Positioning.md`](docs/TLM-Positioning.md).

---

## Model-first methodology

1. Model the market's economically meaningful variables.
2. Determine which are already protocol-visible.
3. Investigate which additional variables merit protocol-visible representation.
4. Only then design and evaluate mechanisms — separating **concept**, **representation**, and **mechanism**.

---

## An interdisciplinary program

TLM sits at the intersection of four mature literatures and aims to *inherit their results* rather than restate their questions:

- **Financial economics** — liquidity as a multidimensional property; the cost of time.
- **Mechanism & market design** — TLM as a *multidimensional transaction fee mechanism*, evaluated under DSIC / MMIC / OCA-proofness.
- **Networking & QoS** — the IntServ/DiffServ lesson; coarse, stateless descriptors.
- **Empirical execution-timing economics** — the cost of delay; time-as-priority (Arbitrum Timeboost).

The full literature map is in [`docs/Related-Work.md`](docs/Related-Work.md).

---

## Repository map

```text
docs/
    Vision-Statement.md          — the umbrella concept and guiding principles
    TLM_Research_Overview.md     — outward-facing research invitation
    TLM-Positioning.md           — where TLM's contribution lies
    Foundation-Outline.md        — structure of the Foundation Statement
    Foundation-1-Introduction.md — Part I: introduction & the concept
    Foundation-2-Framework.md    — Part II: principles & model-first methodology
    Foundation-3-Future-Research.md — Part III: research agenda & falsifiability
    Temporal-Liquidity.md        — canonical concept exposition
    Related-Work.md              — interdisciplinary literature map
    Research-Notes/
        RN-01 — Temporal Execution Profiles (transaction-level representation)
        RN-02 — Protocol-visible Temporal Abstraction
        RN-03 — Hyperliquid: A Case Study in Temporal Liquidity
```

---

## Where to start

- **New here?** Read the [Research Overview](docs/TLM_Research_Overview.md).
- **Want the concept?** [Temporal Liquidity](docs/Temporal-Liquidity.md).
- **Want the framework?** The Foundation Statement — [Part I](docs/Foundation-1-Introduction.md) · [Part II](docs/Foundation-2-Framework.md) · [Part III](docs/Foundation-3-Future-Research.md).
- **Want the evidence?** [RN-03: Hyperliquid](docs/Research-Notes/RN-03_Hyperliquid_A_Case_Study_in_Temporal_Liquidity.md).

---

## Contributing

TLM is an open research project. Critique, discussion, and alternative or competing approaches are welcome — especially from distributed systems, networking, mechanism and market design, and financial economics. The primary question is not whether a particular mechanism should be adopted, but whether **protocol-visible temporal characteristics of demand** are a worthwhile direction for decentralized execution markets — and, if so, what the right abstraction and the binding impossibilities are.
