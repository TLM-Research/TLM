# Temporal Liquidity Market (TLM)

## Vision Statement (Version 4.2)

### A Vision for Temporal Market Design in Blockchain Protocols

---

## Background

Blockchain protocols have made remarkable progress in decentralized resource allocation through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS).

These advances have significantly improved price discovery, market efficiency, decentralized block construction, and protocol robustness.

Together, they transformed blockspace allocation from a simple fee auction into an increasingly sophisticated protocol-managed marketplace.

---

## The Remaining Dimension

Despite these advances, today's blockchain fee markets primarily coordinate demand through **price**.

However, users differ not only in how much they are willing to pay, but also in **when** they require execution.

An arbitrage transaction may lose nearly all of its value if delayed by one block.

A decentralized exchange swap may tolerate a short delay in exchange for lower transaction cost.

A treasury transfer may remain equally valuable after minutes or even hours.

These transactions express fundamentally different forms of economic flexibility with respect to execution time.

---

## Temporal Liquidity

TLM introduces the concept of **Temporal Liquidity**.

> **Temporal Liquidity is the economic flexibility of demand with respect to execution time.**

Just as conventional liquidity reflects flexibility with respect to price, Temporal Liquidity reflects flexibility with respect to time.

Transactions therefore differ not only in their willingness to pay, but also in the amount of Temporal Liquidity they possess.

Current blockchain protocols largely treat this information as implicit.

TLM investigates whether Temporal Liquidity can become a protocol-visible economic signal.

---

## Vision

The long-term vision of TLM is to enable blockchain protocols to coordinate both **price** and **time** through decentralized market mechanisms.

Rather than treating execution as an immediate-or-never decision, users should be able to communicate richer temporal information that reflects the economic flexibility of their transactions.

Protocol participants—including users, builders, proposers, and validators—may then coordinate using both economic dimensions while preserving decentralized incentives.

---

## Building Upon Ethereum

TLM is not intended to replace Ethereum's existing economic architecture.

Instead, it seeks to build upon the foundations established by:

* EIP-1559
* Proposer-Builder Separation (PBS)
* Enshrined PBS (ePBS)
* Future Ethereum protocol evolution

TLM should therefore be viewed as a complementary research direction rather than an alternative fee market.

---

## Guiding Principles

The project is guided by several principles.

* Preserve participant neutrality.
* Preserve decentralized market incentives.
* Keep protocol rules deterministic and transparent.
* Build upon existing Ethereum protocol evolution.
* Improve coordination through richer protocol-visible information rather than centralized decision making.
* Favor positive-sum market outcomes that increase participation and overall ecosystem efficiency.

---

## Research Direction

TLM investigates questions including:

* How should Temporal Liquidity be represented at the protocol level?
* What temporal information should become protocol-visible?
* How can builders utilize richer temporal information during block construction?
* Can protocol-visible Temporal Liquidity improve congestion management and reduce timing inefficiencies?
* How should future protocol mechanisms balance simplicity, efficiency, and decentralization?

The project does not assume that any particular mechanism is the final answer.

Instead, it provides an open framework for exploring temporal market design.

---

## Long-Term Goal

Ethereum demonstrated that **price** can become a protocol-visible economic signal through protocol-managed fee markets.

TLM explores whether **Temporal Liquidity** can likewise become a protocol-visible economic signal, enabling blockchain protocols to coordinate both **price** and **time** while preserving decentralized market principles.

The objective is not merely to improve one fee mechanism, but to establish a broader framework for temporal market design that may contribute to the next generation of blockchain protocol economics.
