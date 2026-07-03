# Temporal Liquidity Market (TLM)

**An open framework for temporal market design in blockchain protocols, with Ethereum as the initial research platform.**

---

## Start Here

If you are new to the project, we recommend reading the documents in the following order:

1. **Vision Statement** — Why temporal market design matters.
2. **Foundation Statement** — The conceptual framework, principles, and research agenda of TLM.
3. **Temporal Liquidity** — The foundational concept introduced by TLM.
4. **Mechanism Proposals** *(future)* — Candidate protocol designs and implementation ideas.
5. **Research Notes** — Ongoing observations, literature reviews, and evolving ideas.

---

## Overview

Blockchain protocols have made significant advances in decentralized resource allocation through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS).

These innovations have substantially improved price discovery, decentralized block construction, and protocol robustness.

However, one important aspect of user demand remains largely implicit:

> **Temporal Liquidity.**

Users differ not only in how much they are willing to pay, but also in **when** they require execution and **how much delay they are willing to tolerate**.

TLM defines **Temporal Liquidity** as:

> **The economic flexibility of demand with respect to execution time.**

Temporal Liquidity Market (TLM) investigates how Temporal Liquidity can become a **protocol-visible economic signal**, enabling blockchain protocols to coordinate both **price** and **time** while preserving decentralized market principles.

---

## Project Goals

TLM explores how decentralized protocols can better represent, communicate, and coordinate temporal information while preserving:

* Decentralization
* Participant neutrality
* Market efficiency
* Protocol simplicity
* Incentive compatibility

The project builds upon existing Ethereum protocol research rather than replacing it.

---

## Repository Structure

```text
docs/
    Vision-Statement.md
    Foundation-Outline.md
    Foundation-Statement.md
    Temporal-Liquidity.md
    Architecture.md
    Roadmap.md
    Open-Questions.md

research_notes/
    Research journal and evolving ideas

literature/
    Reading notes and related work

simulations/
    Future prototypes and experiments

archive/
    Historical materials (future)
```

---

## Current Status

**Version:** TLM Public Release 1 (PR1)

Current work focuses on establishing the conceptual foundations of temporal market design for blockchain protocols, including:

* Temporal Liquidity
* Ethereum fee markets
* Proposer-Builder Separation (PBS)
* Enshrined PBS (ePBS)
* Protocol economics
* Builder optimization
* Mechanism design
* Distributed systems

---

## Research Philosophy

TLM is an open research framework rather than a completed protocol proposal.

The project aims to establish a common conceptual foundation for temporal market design, encouraging rigorous discussion, experimentation, and collaboration.

Specific protocol mechanisms—including Temporal Liquidity Reserve (TLR) and future proposals—should be viewed as candidate implementations of this broader framework rather than final solutions.

---

## Contributing

Thoughtful discussion, constructive criticism, literature recommendations, and collaborative research are welcome.

---

## Guiding Question

> **How should blockchain protocols represent, communicate, and coordinate Temporal Liquidity while preserving decentralized market principles?**
