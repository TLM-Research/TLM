# Temporal Liquidity

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public
**Last Updated:** July 3, 2026

---

## Definition

**Temporal Liquidity** is the **economic flexibility of demand with respect to execution time**.

It characterizes how a transaction's utility changes as its execution is delayed. Transactions with different objectives naturally exhibit different degrees of Temporal Liquidity.

Unlike traditional fee markets, which primarily capture a user's willingness to pay, Temporal Liquidity captures a transaction's economic flexibility with respect to execution time.

---

## Motivation

Blockchain protocols have significantly advanced decentralized resource allocation through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS).

These innovations have substantially improved price discovery, blockspace allocation, decentralized block construction, and protocol robustness.

However, current fee markets primarily coordinate demand through **price**.

In practice, users differ not only in **how much** they are willing to pay, but also in **when** they require execution.

Some transactions lose nearly all value if delayed by a single block, while others can tolerate minutes or even hours of delay with little reduction in utility.

These differences reveal another important economic characteristic of demand: **Temporal Liquidity**.

---

## Temporal Liquidity versus Time Preference

**Time Preference** is a well-established concept in economics that describes how individuals value present benefits relative to future benefits.

TLM adopts a protocol-oriented perspective.

Rather than modeling preferences in the abstract, TLM focuses on the **economic flexibility of individual transactions with respect to execution time**.

Time Preference motivates Temporal Liquidity, but the two concepts are not identical.

Temporal Liquidity is intended as a protocol-level abstraction that can be represented, communicated, and coordinated within decentralized execution markets.

---

## Examples

| Transaction Type    | Temporal Liquidity |
| ------------------- | ------------------ |
| MEV Arbitrage       | Very Low           |
| Liquidation         | Low                |
| DEX Swap            | Medium             |
| NFT Mint            | Medium to High     |
| Treasury Transfer   | High               |
| Periodic Settlement | Very High          |

Transactions with **low Temporal Liquidity** require prompt execution because their value deteriorates rapidly over time.

Transactions with **high Temporal Liquidity** can tolerate delay while preserving much of their economic utility.

---

## Protocol Perspective

Today's blockchain fee markets primarily coordinate demand through **price**.

TLM investigates whether protocols can also coordinate demand through **Temporal Liquidity**.

Rather than treating execution as an immediate-or-never decision, users may communicate richer temporal information that reflects the economic flexibility of their transactions.

The protocol does not seek to optimize users' utility directly.

Instead, it provides decentralized market mechanisms through which participants may voluntarily express Temporal Liquidity while preserving participant neutrality, market incentives, and protocol simplicity.

---

## Protocol Representation

Temporal Liquidity is an **economic property**.

Protocols require a concrete representation of that property.

TLM investigates protocol-visible representations—including Temporal Preference Curves and related abstractions—that allow transactions to communicate execution flexibility while remaining compatible with decentralized protocol design.

The exact representation remains an active area of research.

---

## Research Questions

Temporal Liquidity raises several open questions.

* How should Temporal Liquidity be represented at the protocol level?
* What temporal information should become protocol-visible?
* How should blockchain protocols coordinate both price and Temporal Liquidity?
* How can richer temporal information improve builder optimization while preserving participant neutrality?
* Can protocol-visible Temporal Liquidity reduce congestion, timing games, and other inefficiencies?
* What new incentive or manipulation vectors emerge when Temporal Liquidity becomes part of protocol design?

These questions form part of the broader TLM research agenda.

---

## Guiding Principle

Ethereum made **price** a protocol-visible economic signal through protocol-managed fee markets.

Temporal Liquidity Market (TLM) investigates whether **Temporal Liquidity** can likewise become a protocol-visible economic signal, enabling blockchain protocols to coordinate both **price** and **time** while preserving decentralized market principles.

---

## Position within TLM

Temporal Liquidity is the foundational concept of the Temporal Liquidity Market framework.

It provides the economic basis for subsequent work on temporal preference representation, protocol-visible temporal information, builder optimization, and future mechanism proposals.

This document establishes the conceptual foundation for the TLM project and serves as a reference for future public releases.
