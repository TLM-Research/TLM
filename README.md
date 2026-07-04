# Temporal Liquidity Market (TLM)

## A Research Framework for Spatiotemporal Market Design in Ethereum

Temporal Liquidity Market (TLM) is an open research project investigating how blockchain protocols can coordinate not only **price**, but also **time**.

The project explores **Temporal Liquidity**—the economic flexibility of demand with respect to execution time—and studies how this information may become protocol-visible while preserving decentralization, neutrality, and market efficiency.

Rather than proposing a single mechanism, TLM develops a conceptual framework for understanding decentralized execution markets and for exploring future protocol evolution.

---

## Motivation

Ethereum has significantly advanced decentralized market design through innovations such as:

* **EIP-1559**, improving fee market efficiency and congestion pricing.
* **Proposer-Builder Separation (PBS)**, introducing specialization in block construction.
* **Enshrined PBS (ePBS)**, bringing builder commitments and settlement guarantees into protocol rules.
* Ongoing research into **Execution Tickets**, **Slot Auctions**, and other proposals that extend coordination across time.

Together, these developments demonstrate an important architectural trend:

> **Ethereum is progressively making economically meaningful information protocol-visible in order to improve decentralized coordination.**

TLM investigates whether **Temporal Liquidity** should become another protocol-visible economic variable within this broader evolution.

---

## Temporal Liquidity

Traditional fee markets primarily coordinate demand through price.

However, transactions also differ in their flexibility with respect to execution time.

Some transactions require immediate execution.

Others are willing to wait in exchange for lower cost.

Still others have complex execution preferences spanning multiple blocks.

TLM defines **Temporal Liquidity** as:

> **The economic flexibility of demand with respect to execution time.**

Rather than treating execution time solely as a performance metric, TLM studies execution time as an economic resource that may participate in decentralized market coordination.

---

## Research Philosophy

TLM adopts a **model-first methodology**.

Instead of beginning with protocol mechanisms, it first models decentralized execution markets, identifies economically meaningful variables, investigates which variables should become protocol-visible, and then explores mechanisms that coordinate those variables.

This separation between:

* economic concepts,
* protocol representations, and
* protocol mechanisms

allows multiple implementation approaches to be evaluated within a common conceptual framework.

---

## Research Directions

Current research includes:

* Temporal Liquidity as an economic variable
* Protocol-visible economic information
* Decentralized temporal coordination
* Mechanism design for temporal execution markets
* Builder optimization across time
* Spatiotemporal resource allocation
* Measurement and evaluation of Temporal Liquidity
* Implications for future Ethereum protocol evolution

The project remains mechanism-neutral and welcomes alternative implementations and competing approaches.

---

## Relationship to Existing Research

TLM builds upon the remarkable progress made by the Ethereum research community.

Its foundations draw inspiration from research on Ethereum fee markets, EIP-1559, PBS, ePBS, MEV, execution market design, and ongoing work on future protocol evolution.

TLM should therefore be viewed as a complementary research framework rather than a replacement for existing protocol proposals.

One of its primary goals is to provide a common conceptual language through which these developments can be understood, compared, and extended.

---

## Repository Structure

```text
docs/
    Vision-Statement.md
    Foundation-Statement.md
    Temporal-Liquidity.md
    Related-Work.md

research/
    Notes
    Mechanisms
    Simulations

archive/
    Historical drafts
```

---

## Contributing

TLM is an open research project.

Contributions, discussion, critiques, and alternative perspectives are welcome.

The long-term objective is to advance the understanding of decentralized execution markets through collaborative research spanning distributed systems, economics, cryptography, mechanism design, and blockchain protocol engineering.
