# RN-02: Protocol-visible Temporal Abstraction (v0.4 @draft)

**Status:** @draft
**Last Updated:** August 19, 2026

## Abstract

Current Layer-1 blockchains primarily expose price as the protocol-visible signal. This note argues that the **temporal characteristics** of demand deserve investigation as first-class protocol-visible information. It does not propose a mechanism. It introduces the transaction-level and stream-level **representations** through which those characteristics could become visible, motivates their value for decentralized scheduling, frames efficiency-sharing as an open goal, and argues that temporal information is made credible primarily by pricing each class at its marked market rate (the fee-market own-rate developed in RN-10/RN-11), with realized-behavior verification playing a narrower part. It is an early-stage stance. The questions it raises (when a class selection should be revealed, how far marked pricing neutralizes advantage, and what minimal consuming behavior a class needs) are posed here as open research, not resolved.

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

These are complementary **representations** of the umbrella's dimensions - the transaction-level ones are chiefly *declared preferences*; the stream-level ones are chiefly *observed properties*. Because a class is charged at its marked rate when consumed (sec. 6), a stream earns no benefit that a one-shot transaction cannot also buy at the same price; a persistent identity is useful mainly for **load forecasting**, not as a gate on eligibility. (RN-01 develops the TEP; RN-03 develops the stream/predictability case.)

**Visibility has a timing dimension.** "Protocol-visible" does not by itself settle *when* a selection becomes visible to others, and that timing governs extraction: a class choice exposed in a public mempool before ordering can be priced against or front-run, while one committed but revealed only after sequencing, or encrypted until execution, can still inform scheduling without inviting extraction. When to reveal a selection is a design lever, and an open question (sec. 10), not something this note settles.

## 4. Why Temporal Information Matters

Builders solve online scheduling problems. Credible temporal information may improve forecasting, reservation decisions, scheduling quality, utilization, fragmentation, and online-scheduling regret. This note argues these benefits are plausible and deserve investigation, not that they are established.

## 5. Efficiency Sharing (an open goal)

Applications that supply useful, verified temporal information may improve protocol efficiency, and it is desirable that some of the resulting gain flow back to them - efficiency *sharing*, not redistribution. Stated as a mechanism this would already be a design commitment (a rebate/settlement rule); it is therefore held here as an **open goal** to be satisfied by future mechanism design, consistent with the note's abstraction-first scope.

## 6. Integrity: marked pricing first, verification where it applies

A declaration with no cost is trivially gamed, so a temporal class must carry a cost. The primary integrity mechanism is **marked pricing**: a selected class is charged at its prevailing market-clearing rate, repriced continuously with demand (the fee-market own-rate developed in RN-10 and RN-11). Because the price tracks demand moment to moment, there is no accumulated, unpriced advantage to capture: a class costs what it is worth when consumed, for a recognized stream and a one-shot transaction alike. This neutralizes advantage at large (to a degree) for fair use, and it locates the choice with the user, who selects a class and bears its marked cost, rather than with a supply side that must vet who deserves a lane. Neutrality is thus provisioned by open, marked-price selection.

Realized-behavior verification is secondary and bounded. **Private value is never verifiable**: a missed deadline is observable, but the counterfactual value of a different execution time is not, so no scheme can certify a user's true urgency. Marked pricing is what makes that unnecessary. Where a representation is used to grant something not directly paid for, an observed-behavior check (realized profiles, prediction scoring, refundable commitments) has a role, but a narrow one. How far marked pricing neutralizes advantage, and where verification is genuinely needed, are open questions (sec. 10).

## 7. Hyperliquid Example

Hyperliquid illustrates that transaction urgency and stream predictability are distinct: individual order-book transactions may require immediate execution while the overall workload remains persistent and forecastable. Future mechanisms could price urgent execution at the transaction level while rewarding *verified* schedulability at the stream level.

## 8. Architectural Principles

- concept before mechanism - but with the *minimal* consuming behavior and cost binding co-specified, since a descriptor has no meaning or integrity without them (illustratively: a TEP consumed by a deadline-aware ordering rule, a TDP consumed by a capacity-forecast / reservation rule - sketches, not commitments)
- minimal, coarse protocol-visible information
- protocol neutrality via open, marked-price selection
- application independence
- efficiency sharing (goal, sec. 5)
- marked pricing as the primary integrity mechanism; realized-behavior verification where a benefit is not directly priced
- resistance to strategic manipulation

## 9. Relationship to TLM

- Foundation Statement - *why* (the framework and principles).
- `Temporal-Liquidity` - *what the object is* (the umbrella concept and its dimensions).
- RN-01 - the transaction-level representation (TEP).
- RN-02 (this note) - *why* the characteristics should be protocol-visible at all, and through what representations.
- Future mechanism notes - *how*.

These are open problems. RN-02 takes a stance; it does not claim to resolve them.

- the minimum credible descriptor whose scheduling gain exceeds its disclosure and extraction cost (the note's central question)
- revelation timing of a class selection, and its effect on extraction
- the reach of marked pricing in neutralizing advantage, and where verification is genuinely needed
- minimal consuming behavior for each representation (the TEP and TDP sketches in sec. 8, made precise)
- transaction- versus stream-level interaction
- builder scheduling benefit
- efficiency measurement (a counterfactual for the sharing goal, sec. 5)
- decentralization and extraction resistance
- positioning against intents / order-flow auctions and multidimensional fees (partially competing, not purely complementary)
- evaluation under transaction-fee-mechanism criteria (DSIC / MMIC / OCA-proofness)

## Closing

RN-02 contributes an architectural stance rather than a finalized mechanism: the temporal characteristics of demand deserve treatment as first-class, protocol-visible information, exposed through coarse representations and priced at marked rates. Its sharpest form is not "temporal information is first-class" but a cost-benefit question: **which minimum credible descriptor yields a scheduling gain that exceeds its disclosure and extraction cost**, under adversarial, permissionless conditions. The note poses that question and the open problems around it (sec. 10); it does not claim to have answered them.
