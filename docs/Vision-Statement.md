# Temporal Liquidity Market (TLM)

## Vision Statement

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public
**Last Updated:** July 2026

---

## A Vision for Temporal Market Design in Blockchain Protocols

### Background

Blockchain protocols have made remarkable progress in decentralized resource allocation through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS).

These advances have significantly improved price discovery, decentralized block construction, protocol robustness, and market efficiency.

Together, they transformed blockspace allocation from a simple fee auction into an increasingly sophisticated protocol-managed marketplace.

---

## The Remaining Dimension

Despite these advances, today's blockchain protocols primarily coordinate demand through **price**.

However, users differ not only in how much they are willing to pay, but also in **when** they require execution.

An arbitrage transaction may lose nearly all of its value if delayed by a single block.

A decentralized exchange swap may willingly wait several blocks in exchange for lower transaction costs.

A treasury transfer may remain equally valuable after minutes or even hours.

These differences reveal an important economic characteristic that today's fee markets only partially capture.

---

## Temporal Liquidity

TLM introduces the concept of **Temporal Liquidity**.

> **Temporal Liquidity is the economic flexibility of demand with respect to execution time.**

Just as conventional liquidity reflects economic flexibility with respect to price, Temporal Liquidity reflects economic flexibility with respect to execution time.

Transactions therefore differ not only in willingness to pay, but also in the amount of Temporal Liquidity they possess.

Current blockchain protocols largely treat this information as implicit.

TLM investigates whether Temporal Liquidity can become a **protocol-visible economic signal**.

---

## Vision

The long-term vision of TLM is to enable blockchain protocols to coordinate both **price** and **time** through decentralized market mechanisms.

Rather than treating execution as an immediate-or-never decision, users should be able to communicate richer temporal information that reflects the economic flexibility of their transactions.

Builders, proposers, validators, and users can then coordinate using both economic dimensions while preserving decentralized incentives and protocol neutrality.

The objective is not to replace decentralized markets, but to make them more expressive.

---

## Building Upon Ethereum

TLM is not intended to replace Ethereum's existing protocol architecture.

Instead, it builds upon the foundations established by:

* EIP-1559
* Proposer-Builder Separation (PBS)
* Enshrined PBS (ePBS)
* Future Ethereum protocol evolution

TLM should therefore be viewed as a complementary research framework rather than an alternative fee market.

---

## Guiding Principles

The project is guided by several principles.

* Preserve decentralized market incentives.
* Preserve participant neutrality.
* Make richer temporal information protocol-visible rather than protocol-controlled.
* Keep protocol rules deterministic, transparent, and simple.
* Build upon existing Ethereum protocol evolution.
* Encourage positive-sum outcomes by increasing overall market participation and ecosystem efficiency.

---

## Research Direction

TLM investigates questions including:

* How should Temporal Liquidity be represented at the protocol level?
* What temporal information should become protocol-visible?
* How can builders utilize richer temporal information during block construction?
* Can protocol-visible Temporal Liquidity improve congestion management and reduce timing inefficiencies?
* How should future protocol mechanisms balance simplicity, efficiency, decentralization, and incentive compatibility?

The project does not assume that any particular mechanism represents the final solution.

Instead, it provides an open framework for exploring temporal market design in blockchain protocols.

---

## Long-Term Goal

Ethereum demonstrated that **price** can become a protocol-visible economic signal through protocol-managed fee markets.

Temporal Liquidity Market (TLM) explores whether **Temporal Liquidity** can likewise become a protocol-visible economic signal, enabling blockchain protocols to coordinate both **price** and **time** while preserving decentralized market principles.

The long-term objective is not merely to improve one fee mechanism, but to establish a broader framework for temporal market design that may contribute to the next generation of blockchain protocol economics.
