# TLM Research Note RN-01

# Temporal Execution Profiles (TEP)

## A Richer Way to Express Transaction Execution Preferences in Blockchain Markets

**Project:** Temporal Liquidity Market (TLM)

**Status:** Public Draft

**Version:** 0.2

**Date:** July 2026

---

# Positioning

Blockchain execution markets have advanced rapidly during the past several years.

Ethereum has evolved from first-price transaction auctions to EIP-1559, Proposer-Builder Separation (PBS), and ongoing research into Enshrined PBS (ePBS), execution tickets, slot auctions, and related execution-market proposals. These developments primarily investigate how scarce execution capacity should be allocated more efficiently.

This research note investigates a complementary question.

> **Before improving allocation mechanisms, should blockchain markets first improve how applications communicate their transaction execution preferences?**

The Temporal Liquidity Market (TLM) research program explores this question from the perspective of demand-side market design.

This note introduces **Temporal Execution Profiles (TEPs)** as a richer way for applications to communicate transaction execution preferences to blockchain execution markets.

Rather than proposing another auction, scheduler, or queueing mechanism, this note focuses on the information exchanged between applications and execution markets before allocation begins.

---

# Abstract

Blockchain execution markets have steadily evolved through better pricing and allocation mechanisms. This note explores a complementary question: can blockchain execution markets also evolve by allowing applications to communicate richer transaction execution preferences?

Blockchain applications increasingly exhibit heterogeneous execution requirements.

Some transactions derive value only from immediate execution. Others remain valuable across much broader execution windows. Current blockchain fee markets primarily communicate willingness to pay through a small number of fee parameters, leaving much of an application's temporal execution preference implicit.

This note introduces the concept of a **Temporal Execution Profile (TEP)**.

A TEP provides a richer way for applications to communicate transaction execution preferences without prescribing a particular market mechanism or mathematical representation.

The objective is not to propose a new fee mechanism, but to investigate whether richer protocol-visible execution preferences may enable future blockchain execution markets to better match heterogeneous application demand with heterogeneous execution options.

Ethereum serves as the primary case study because of its mature execution market and active protocol research. The underlying concepts are intended to apply more broadly to decentralized execution systems and thus warrant parallel studies in other Layer-1 eco-systems.

---

# 1. Motivation

Consider four transactions arriving at approximately the same time.

| Transaction | Example Application | Desired Execution |
|-------------|---------------------|-------------------|
| A | Liquidation | Execute immediately |
| B | DEX Swap | Execute within approximately one minute |
| C | Treasury Settlement | Execute before market close |
| D | Oracle / NAV Update | Execute before the next reporting cycle |

Although these transactions compete for the same blockchain resource, they possess fundamentally different temporal requirements.

A liquidation transaction may lose nearly all value after a single block.

A treasury settlement may tolerate substantial delay provided that settlement occurs before business close.

An oracle update derives value primarily from satisfying an external reporting schedule.

A decentralized exchange swap often lies somewhere between these extremes.

Today's Ethereum fee market primarily receives

```
maxFeePerGas
maxPriorityFeePerGas
```

These parameters communicate willingness to pay, but communicate relatively little about *when* execution creates value.

Consequently, applications frequently implement temporal optimization outside the protocol through

- gas estimation,
- transaction replacement,
- retry policies,
- batching,
- rollup scheduling,
- oracle update scheduling,
- private order flow,
- application-specific execution logic.

The widespread use of these techniques suggests that applications already possess sophisticated temporal execution models.

The protocol simply does not observe them directly.

This motivates the central question of this note.

> **Can blockchain execution markets benefit from allowing applications to communicate richer transaction execution preferences before allocation begins?**

---

# 2. Temporal Execution Profiles

This note proposes the concept of a **Temporal Execution Profile (TEP).**

## Definition

A **Temporal Execution Profile (TEP)** is a protocol-visible description of an application's temporal preferences across alternative execution options.

Rather than describing only willingness to pay, a TEP describes how an application values different execution options that may be offered by the execution market.

Examples may include preferences regarding

- execution urgency,
- acceptable execution delay,
- execution windows,
- preferred execution ordering,
- confirmation requirements,
- or other protocol-defined temporal attributes.

Importantly, a TEP is **not** an allocation mechanism.

Nor does it prescribe how a blockchain should schedule or price transactions.

Instead, it describes **what** the application prefers, leaving **how** those preferences are represented and utilized to future protocol designs.

---

# 3. Two Time Domains

Applications and blockchain protocols naturally reason using different notions of time.

## Physical Time

Applications define execution requirements using business or wall-clock time.

Examples include

- before market close,
- within thirty seconds,
- before an oracle update expires,
- after payment confirmation.

These requirements originate from application logic rather than blockchain consensus.

## Blockchain Time

Blockchain protocols allocate execution using logical blockchain events.

Examples include

- block height,
- transaction ordering,
- execution position,
- confirmation,
- finality.

Applications therefore solve an implicit translation problem.

```
Application Intent

        │

Physical Time

        │

        ▼

Temporal Execution Profile (TEP)

        │

        ▼

Execution Options

        │

        ▼

Allocation Mechanism

        │

        ▼

Execution Outcome
```

Today much of this translation occurs outside the protocol.

TLM investigates whether part of this translation should become protocol-visible through Temporal Execution Profiles.

---

# 4. Representing Temporal Execution Profiles

A Temporal Execution Profile intentionally separates **execution preferences** from their mathematical representation.

Different blockchain protocols may choose different representations while conveying equivalent temporal preferences.

Possible representations include

- Temporal Bid Functions,
- execution deadlines,
- acceptable delay intervals,
- discrete execution classes,
- piecewise value schedules,
- protocol-specific encodings,
- or future representations yet to be explored.

Throughout the TLM research program, **Temporal Bid Functions** are investigated as one natural mathematical representation of a Temporal Execution Profile.

The TLM framework intentionally remains representation-neutral.

The abstraction is the **Temporal Execution Profile**.

The representation is an implementation choice.

This separation allows representations and protocol mechanisms to evolve independently while preserving a common conceptual foundation.
# 5. Economic Motivation for Temporal Execution Profiles

Temporal Execution Profiles are motivated by a simple economic observation.

Applications possess heterogeneous execution preferences, while blockchain execution markets possess heterogeneous execution capabilities.

A market functions effectively only when participants can communicate sufficient information for efficient matching.

Current blockchain fee markets communicate willingness to pay, but communicate only a limited portion of an application's execution preferences.

Temporal Execution Profiles investigate whether richer communication between applications and execution markets may improve this matching before any allocation mechanism is applied.

The objective is not to increase throughput.

Nor is it to replace existing fee markets.

Instead, the objective is to improve how execution markets understand the diversity of application demand that already exists today.

---

## 5.1 Demand-side Motivation

Applications today often purchase essentially the same execution service despite having very different temporal requirements.

Returning to the examples introduced earlier,

| Application | Primary Requirement |
|--------------|--------------------|
| Liquidation | Execute immediately |
| DEX Swap | Execute within approximately one minute |
| Treasury Settlement | Execute before market close |
| Oracle / NAV Update | Execute before the next reporting cycle |

These applications clearly possess different Temporal Execution Profiles.

However, today's blockchain fee market observes only a limited portion of those profiles.

As a consequence, applications frequently perform temporal optimization outside the blockchain protocol through techniques such as

- gas estimation,
- retry strategies,
- transaction replacement,
- batching,
- rollup scheduling,
- oracle update policies,
- private order flow,
- application-specific scheduling logic.

These techniques are evidence that applications already understand their own temporal execution preferences.

The protocol simply does not observe them directly.

Temporal Execution Profiles investigate whether part of this information should become protocol-visible.

The objective is not to guarantee execution.

Nor is it to reduce fees for every participant.

Rather, the objective is to allow applications to communicate richer execution preferences so that economically feasible demand has a greater opportunity to be accepted by the execution market.

In this sense, TEPs seek to reduce information loss between applications and blockchain execution markets.

---

## 5.2 Supply-side Motivation

Execution providers also possess heterogeneous capabilities.

Builders, validators, sequencers, and future execution providers are capable of supporting different execution options.

Current blockchain fee markets, however, primarily optimize immediate transaction inclusion using scalar fee bids.

Consequently, today's execution market effectively offers one dominant execution option:

> Execute as soon as possible.

Temporal Execution Profiles make it possible to explore richer execution options.

Illustrative examples include

- immediate execution,
- execution within a specified number of blocks,
- execution before an application deadline,
- preferred execution position,
- flexible execution windows.

These examples are intended only to illustrate the concept.

The broader objective is to allow execution markets to better match heterogeneous application demand with heterogeneous execution options.

Rather than simply redistributing existing demand, richer execution options may expand the economically serviceable market for both applications and execution providers.

This shifts the discussion from competition over a single execution service toward a market capable of supporting differentiated execution services.

---

# 6. Relationship to Ethereum's Evolution

Ethereum has continuously improved its execution market through advances in both pricing and allocation.

Early fee markets focused primarily on transaction pricing.

EIP-1559 significantly improved fee predictability and price discovery.

Proposer-Builder Separation (PBS) introduced supply-side specialization, improving execution efficiency.

Current research—including Enshrined PBS (ePBS), execution tickets, slot auctions, and related proposals—continues this evolution by investigating improved allocation mechanisms.

This research note investigates a complementary direction.

Rather than asking

> "How should execution options be allocated?"

it asks

> "How should applications communicate execution preferences before allocation begins?"

Temporal Execution Profiles are proposed as one possible answer to this question.

Accordingly, this work should be viewed as complementary to ongoing Ethereum execution-market research rather than as an alternative to it.

Ethereum serves as the initial case study because it represents one of today's most advanced blockchain execution markets.

The underlying concepts are expected to apply more broadly to future blockchain execution systems.

---

# 7. Current Research Directions

This note introduces **Temporal Execution Profiles (TEPs)** as the conceptual foundation for the Temporal Liquidity Market (TLM) research program.

Building upon this foundation, the project is currently investigating several complementary research directions.

These represent active research topics rather than finalized protocol proposals.

| Research Direction | Current Focus |
|--------------------|---------------|
| **Temporal Execution Profiles (TEP)** | Richer communication of transaction execution preferences. |
| **Temporal Bid Functions** | Mathematical representations of Temporal Execution Profiles. |
| **Urgency Pricing** | Mechanisms allowing highly time-sensitive demand to communicate urgency more explicitly. |
| **Patience Incentives** | Mechanisms encouraging flexible demand to reveal temporal flexibility. |
| **Temporal Liquidity Reserve (TLR)** | Protocol-managed temporal balancing mechanisms based on deterministic feedback. |
| **Temporal Market Feedback** | Protocol feedback using observed temporal execution behavior. |
| **Execution Option Markets** | Markets supporting differentiated execution options across time and execution ordering. |
| **Builder Optimization** | Builder optimization using Temporal Execution Profiles rather than scalar fee bids alone. |

These directions document the current research trajectory of the TLM project.

Their purpose is to encourage discussion, invite collaboration, and provide context for future Research Notes and Mechanism Notes.

Individual mechanisms are expected to evolve as the research progresses.

---

# 8. Conclusion

Blockchain execution markets have made remarkable progress in improving pricing and execution allocation.

This note explores another complementary direction.

Rather than focusing exclusively on allocation mechanisms, future execution markets may also benefit from improving how applications communicate execution preferences.

Temporal Execution Profiles provide one possible framework for communicating those preferences.

Whether TEPs ultimately lead to new pricing models, execution services, scheduling policies, or protocol mechanisms remains an open research question.

The central hypothesis of this work is intentionally modest:

> Better communication of transaction execution preferences may enable better blockchain execution markets.

While this note focuses on Ethereum, the broader research question is independent of any single blockchain architecture. We hope this work encourages parallel studies across other Layer-1 ecosystems, where different execution models, consensus mechanisms, and application communities may reveal new insights into temporal execution markets. Comparative studies across blockchain platforms may ultimately prove as valuable as the mechanisms proposed within any individual ecosystem. Ultimately, we hope Temporal Execution Profiles evolve into a common vocabulary for discussing transaction execution preferences across blockchain ecosystems, enabling researchers to compare execution markets using a shared conceptual framework while exploring different protocol realizations
---

# Research Philosophy

The Temporal Liquidity Market (TLM) project is developed as an open research program.

It distinguishes between

- Foundation Documents,
- Research Notes,
- Mechanism Notes,
- Protocol Implementations.

Research Notes introduce conceptual ideas.

Mechanism Notes investigate candidate protocol designs built upon those ideas.

Public publication serves two complementary purposes.

First, it establishes a transparent, timestamped record of the project's evolution.

Second, it encourages constructive discussion and collaboration within the broader blockchain research community.

Mechanisms may evolve.

Representations may evolve.

The conceptual foundations are expected to mature through open research, experimentation, and community feedback.
