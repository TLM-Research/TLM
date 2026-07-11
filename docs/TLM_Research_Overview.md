# Temporal Liquidity Market (TLM)

## Research Overview (v0.3)

### A Question Motivated by Ethereum's Evolving Execution Markets

Ethereum has demonstrated that protocol design can fundamentally improve decentralized market infrastructure. Innovations such as **EIP-1559** and **Proposer-Builder Separation (PBS)** have significantly advanced how execution markets coordinate demand, improving efficiency while preserving openness and decentralization. Recent protocol evolution continues to refine this execution architecture.

At the same time, Ethereum is evolving beyond cryptocurrency transactions. Stablecoins, decentralized finance, and tokenized real-world assets are transforming blockchain networks into increasingly important financial infrastructure. As the diversity of applications grows, so does the diversity of their execution requirements.

This evolution motivates a simple question.

> **Should execution markets coordinate only prices, or should they also coordinate the temporal flexibility of demand?**

---

## Temporal Liquidity

This work introduces **Temporal Liquidity** as a new concept.

> **Temporal Liquidity is the economic flexibility of demand with respect to execution time.**

Not all transactions require immediate execution.

Some rapidly lose economic value if delayed.

Others remain economically useful across multiple execution opportunities.

Today's execution markets largely coordinate these heterogeneous demands through price alone. Temporal flexibility often exists but remains implicit throughout the execution process.

Rather than asking whether every participant should be treated identically, this work asks whether markets should be able to recognize and coordinate differences in temporal liquidity.

---

## A Different Question

The Temporal Liquidity Market (TLM) does not begin with a new protocol mechanism.

Instead, it begins with a communication question.

> **What temporal information, if any, should applications communicate before decentralized resource allocation begins?**

Applications may possess richer execution choices than current markets explicitly observe. Depending on the application, these choices may include acceptable execution windows, tolerance for delay, or alternative execution strategies under changing market conditions.

If such information were communicated through transparent, protocol-defined rules, could decentralized markets coordinate more effectively while preserving participant autonomy and protocol neutrality?

TLM is an open research framework for exploring that question.

```text
                 Application
                      │
      ┌───────────────┴───────────────┐
      │                               │
  Price Information          Temporal Liquidity
                                      │
                                      │
                     (revealed through temporal
                        execution choices)
      │                               │
      └───────────────┬───────────────┘
                      │
                      ▼
        Ethereum Execution Market
          (EIP-1559 • PBS • ...)
                      │
                      ▼
        Decentralized Resource Allocation
```

The objective is not to replace existing fee markets, but to investigate whether **Temporal Liquidity** can become another dimension of decentralized market coordination alongside price.

---

## An Open Research Program

Many questions naturally follow.

How should Temporal Liquidity be represented?

What temporal information should remain private, and what should become protocol-visible?

Under what conditions does temporal information improve efficiency, fairness, or market robustness?

How should future execution markets incorporate temporal information without compromising decentralization or creating undesirable incentives?

These questions motivate the TLM research program.

Ethereum provides the immediate context, but the underlying research question may extend to other decentralized execution markets and market-based resource allocation systems.

---

## Invitation

This document is intended as an invitation to discussion rather than a completed proposal.

I am seeking feedback from researchers in blockchain protocols, distributed systems, mechanism design, and financial economics.

My primary goal is to determine whether **Temporal Liquidity** represents a useful conceptual framework for understanding future execution markets, and whether this line of inquiry merits deeper theoretical and empirical investigation.

