# RN-02: Protocol-visible Temporal Abstraction (v0.3 @draft)

**Status:** @draft
**Last Updated:** July 24, 2026

## Abstract

Current Layer-1 blockchains primarily expose price as the protocol-visible signal. This note argues that the **temporal characteristics** of demand deserve investigation as first-class protocol-visible information. It does not propose a mechanism. It introduces the transaction-level and stream-level **representations** through which those characteristics could become visible, motivates their value for decentralized scheduling, frames efficiency-sharing as an open goal, and argues that temporal information must be verified through realized behavior rather than trusted declarations.

Terminology note (aligned with the Vision and `Temporal-Liquidity.md`): the **temporal characteristics of demand** are the umbrella - the collection of economically meaningful temporal properties of demand (execution priority, delay tolerance, execution windows and deadlines, predictability, continuity) - and a demand's **temporal liquidity** is the flexibility they define, the object a market prices. The two profiles below are **representations** of those characteristics at different granularities; they are not themselves the characteristics.

## 1. Motivation

Current fee markets compress heterogeneous temporal requirements into a single scalar price. Applications differ not only in willingness to pay but in *when* and *in what order* they need execution, in how quickly their value decays, and in how forecastable and sustained their demand is. These temporal characteristics carry operational information valuable to decentralized schedulers, yet almost none of it reaches the protocol.

## 2. Lessons - and Cautions - from Distributed Systems

DiffServ demonstrates the value of coarse, stateless, protocol-visible descriptors that keep the fast path simple. But its history is also a caution: DiffServ worked *within* a single administrative domain, its marks were routinely bleached at inter-domain boundaries, and its integrity depended on **edge policing** - without admission control, every packet marks itself highest priority and the classes collapse. A permissionless L1 is the opposite of a single trust domain, and its traffic is strategic and value-bearing. So the coarse-descriptor *pattern* is the right aspiration (see also the end-to-end / narrow-waist principle), but the conditions that made it work are what the permissionless setting lacks. Closing that gap - coarse descriptors made credible under adversarial conditions - is the actual research contribution, and it is why verification (sec. 6) is essential.

## 3. Two Representations of the Temporal Characteristics

The temporal characteristics become protocol-visible through representations at two granularities. Both describe an underlying **value-versus-delay / value-versus-position** object - how an application's value changes with *when* and *where in the sequence* it executes, with a deadline and a decay rate as its parameters.

### Transaction-level: Temporal Execution Profile (TEP)

- delay tolerance (value-vs-delay across slots)
- execution window / deadline
- execution priority (sensitivity to ordering within a slot)
- acceptable execution variability

### Stream-level: Temporal Demand Profile (TDP)

- continuity / persistence
- predictability (forecastability of aggregate demand)
- arrival variability
- verified reliability

These are complementary **representations** of the umbrella's dimensions - the transaction-level ones are chiefly *declared preferences*; the stream-level ones are chiefly *observed properties* that only earn a coordination benefit if verified. (RN-01 develops the TEP; RN-03 develops the stream/predictability case.)

## 4. Why Temporal Information Matters

Builders solve online scheduling problems. Credible temporal information may improve forecasting, reservation decisions, scheduling quality, utilization, fragmentation, and online-scheduling regret. This note argues these benefits are plausible and deserve investigation, not that they are established.

## 5. Efficiency Sharing (an open goal)

Applications that supply useful, verified temporal information may improve protocol efficiency, and it is desirable that some of the resulting gain flow back to them - efficiency *sharing*, not redistribution. Stated as a mechanism this would already be a design commitment (a rebate/settlement rule); it is therefore held here as an **open goal** to be satisfied by future mechanism design, consistent with the note's abstraction-first scope.

## 6. Verification

Self-declared temporal profiles are insufficient, because a declaration with no cost is trivially gamed. Credibility should rest on **realized behavior** over time and on a **cost/stake binding** that makes over-claiming self-penalizing. Candidate approaches: realized profiles, prediction scoring, refundable commitments, reputation, and stake-backed declarations. Neutrality keeps the cost from advantaging any particular participant; the cost binding is what removes the motive to game.

## 7. Hyperliquid Example

Hyperliquid illustrates that transaction urgency and stream predictability are distinct: individual order-book transactions may require immediate execution while the overall workload remains persistent and forecastable. Future mechanisms could price urgent execution at the transaction level while rewarding *verified* schedulability at the stream level.

## 8. Architectural Principles

- concept before mechanism - but with the *minimal* consuming behavior and cost binding co-specified, since a descriptor has no meaning or integrity without them
- minimal, coarse protocol-visible information
- protocol neutrality
- application independence
- efficiency sharing (goal, sec. 5)
- verification through realized behavior
- resistance to strategic manipulation

## 9. Relationship to TLM

- Foundation Statement - *why* (the framework and principles).
- `Temporal-Liquidity` - *what the object is* (the umbrella concept and its dimensions).
- RN-01 - the transaction-level representation (TEP).
- RN-02 (this note) - *why* the characteristics should be protocol-visible at all, and through what representations.
- Future mechanism notes - *how*.

## 10. Research Agenda

- the minimum temporal abstraction that is useful yet coarse
- transaction- versus stream-level interaction
- builder scheduling benefit
- verification and cost binding
- efficiency measurement
- decentralization and extraction resistance
- positioning against intents / order-flow auctions and multidimensional fees (partially competing, not purely complementary)
- evaluation under transaction-fee-mechanism criteria (DSIC / MMIC / OCA-proofness)

## Closing

RN-02 contributes an architectural stance rather than a finalized mechanism: the temporal characteristics of demand deserve treatment as first-class, protocol-visible information, exposed through coarse and *verifiable* representations, enabling a family of future mechanism designs. Its strongest form makes "the coarse-descriptor pattern under adversarial, permissionless conditions" its explicit thesis rather than resting on the DiffServ analogy.
