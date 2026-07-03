# Temporal Liquidity

## Definition

**Temporal Liquidity** is the **economic flexibility of demand with respect to execution time**.

It characterizes how a transaction's utility changes as its execution is delayed. Transactions with different objectives naturally exhibit different degrees of temporal liquidity.

Unlike traditional fee markets, which primarily capture a user's willingness to pay, Temporal Liquidity captures a user's willingness to wait.

---

## Motivation

Ethereum has significantly improved blockspace allocation through protocol innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS).

These mechanisms enable efficient price discovery for scarce blockspace.

However, they largely assume that demand can be represented by a single economic dimension: **price**.

In reality, users differ not only in how much they are willing to pay, but also in **when** they require execution.

Examples include:

* An arbitrage transaction that loses nearly all value if delayed by one block.
* A decentralized exchange swap that can tolerate a short delay in exchange for lower fees.
* A treasury transfer that remains valuable even after minutes or hours of delay.

These differences reveal another important economic characteristic of demand: **Temporal Liquidity**.

---

## Temporal Liquidity versus Time Preference

The concept of **time preference** is well established in economics and generally refers to how individuals value present consumption relative to future consumption.

TLM adopts a different perspective.

Rather than focusing on individual preferences in the abstract, it focuses on the **economic flexibility of individual transactions** within a decentralized execution market.

Temporal Liquidity therefore provides a protocol-oriented abstraction that can be observed, represented, and coordinated during blockspace allocation.

Time preference motivates Temporal Liquidity, but the two concepts are not identical.

---

## Examples

| Transaction Type    | Temporal Liquidity |
| ------------------- | ------------------ |
| MEV arbitrage       | Very Low           |
| Liquidation         | Low                |
| DEX swap            | Medium             |
| NFT mint            | Medium to High     |
| Treasury transfer   | High               |
| Periodic settlement | Very High          |

Transactions with low Temporal Liquidity require prompt execution because their value deteriorates rapidly over time.

Transactions with high Temporal Liquidity can tolerate delay with relatively small reductions in utility.

---

## Protocol Perspective

Current blockchain fee markets primarily coordinate demand through **price**.

TLM proposes that protocols may also coordinate demand through **Temporal Liquidity**.

Rather than treating execution as an immediate-or-never decision, users may communicate richer temporal information that reflects their economic flexibility.

The protocol does not seek to optimize users' utility directly.

Instead, it provides market participants with mechanisms for expressing Temporal Liquidity while preserving decentralized incentives and participant neutrality.

---

## Protocol Representation

Temporal Liquidity is an economic property.

Protocols require a concrete representation of that property.

TLM investigates protocol-visible representations, including temporal preference curves and related abstractions, that allow users to communicate execution flexibility without sacrificing protocol simplicity or decentralization.

The exact representation remains an active area of research.

---

## Research Questions

The concept of Temporal Liquidity raises several open questions.

* How should Temporal Liquidity be represented at the protocol level?
* What temporal information should become protocol-visible?
* How should protocols coordinate both price and Temporal Liquidity?
* How can richer temporal information improve builder optimization while preserving participant neutrality?
* Can protocol-visible Temporal Liquidity reduce congestion, timing games, and other inefficiencies?
* What new incentive or manipulation vectors arise when Temporal Liquidity becomes part of protocol design?

These questions form part of the broader TLM research agenda.

---

## Guiding Principle

Ethereum made **price** a protocol-visible economic signal through protocol-managed fee markets.

Temporal Liquidity Market (TLM) investigates whether **Temporal Liquidity** can likewise become a protocol-visible economic signal, enabling blockchain protocols to coordinate both **price** and **time** while preserving decentralized market principles.
