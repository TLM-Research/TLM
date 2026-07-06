# TLM Research Note RN-01

# Temporal Execution Profiles (TEP)

## A Richer Way to Express Transaction Execution Preferences in Blockchain Markets

Project: Temporal Liquidity Market (TLM)

Status: Public Draft

Version: 0.1

Date: July 2026

---

# Positioning

Blockchain execution markets have made remarkable progress during the past several years.

Ethereum has evolved from first-price transaction auctions to EIP-1559, Proposer-Builder Separation (PBS), and ongoing research into Enshrined PBS (ePBS), execution tickets, slot auctions, and related execution-market proposals.

These developments primarily investigate how scarce execution opportunities should be allocated more efficiently.

This research note investigates a complementary question.

> **Before improving allocation mechanisms, should blockchain markets first improve how applications communicate their execution preferences?**

The Temporal Liquidity Market (TLM) project studies this question from the perspective of demand representation.

This note introduces **Temporal Execution Profiles (TEPs)** as one possible way for applications to communicate richer transaction execution preferences to blockchain markets.

Rather than proposing another auction or scheduling algorithm, this note focuses on the information that applications provide before allocation begins.

---

# Abstract

Blockchain applications increasingly exhibit heterogeneous temporal requirements.

Some transactions derive value only from immediate execution. Others remain economically valuable over seconds, minutes, hours, or even days.

Current blockchain fee markets primarily allow applications to communicate willingness to pay through a small number of fee parameters.

Consequently, many temporal execution preferences remain implicit and are handled outside the protocol through application-specific logic.

This note introduces **Temporal Execution Profiles (TEPs)** as a richer way for applications to express transaction execution preferences.

A TEP does not prescribe any particular protocol mechanism or mathematical model.

Instead, it provides a protocol-visible description of an application's temporal execution preferences, allowing future execution markets to explore richer allocation mechanisms while remaining compatible with existing blockchain architectures.

Ethereum serves as the primary case study throughout this note because of its mature execution market and active protocol research, although the underlying ideas are intended to apply more broadly to blockchain execution markets.

---

# 1. Motivation

Consider four transactions arriving at approximately the same time.

| Transaction | Example Application | Desired Execution Behavior |
|-------------|---------------------|----------------------------|
| A | Liquidation | Execute immediately |
| B | DEX Swap | Execute within approximately one minute |
| C | Treasury Settlement | Execute before market close |
| D | Oracle / NAV Update | Execute before the next reporting cycle |

From the application's perspective, these transactions are fundamentally different.

A liquidation transaction may lose nearly all value after a single block.

A treasury settlement may tolerate considerable delay provided it completes before business close.

An oracle update derives value primarily from satisfying an external reporting schedule.

A decentralized exchange swap often lies somewhere between these extremes.

Yet today's fee market primarily receives information through

    maxFeePerGas

    maxPriorityFeePerGas

These parameters communicate willingness to pay, but they communicate relatively little about *when* execution creates value.

Applications therefore compensate through additional logic outside the blockchain protocol.

Examples include

- gas estimation,
- transaction replacement,
- retry policies,
- batching,
- rollup scheduling,
- oracle update scheduling,
- private order flow,
- application-specific execution strategies.

The widespread use of these techniques suggests that applications already possess sophisticated temporal execution models.

The protocol simply does not observe them directly.

This observation motivates the central question of this research note.

> **Can blockchain execution markets benefit from allowing applications to communicate richer execution preferences before allocation begins?**

---

# 2. Temporal Execution Profiles

This note proposes the concept of a **Temporal Execution Profile (TEP).**

## Definition

A **Temporal Execution Profile** is a protocol-visible description of an application's temporal preferences across alternative execution options.

Rather than describing only willingness to pay, a TEP describes how an application values different execution possibilities.

Depending on the protocol, these preferences may include

- execution urgency,
- acceptable delay,
- execution windows,
- preferred execution ordering,
- confirmation requirements,
- or other protocol-defined temporal attributes.

Importantly, a TEP is **not** an allocation mechanism.

It does **not** prescribe how a blockchain should schedule or price transactions.

Instead, it provides additional information that future execution markets may use when designing allocation mechanisms.

The purpose of a TEP is therefore similar to many protocol interfaces in distributed systems:

to allow participants to communicate richer information before coordination decisions are made.

---

# 3. Two Time Domains

Applications and blockchain protocols naturally reason using different notions of time.

Applications typically define execution requirements using physical or business time.

Examples include

- before market close,
- within thirty seconds,
- before an oracle update expires,
- after payment confirmation.

Blockchain protocols, however, allocate execution using logical blockchain events.

Examples include

- block height,
- execution order,
- execution position,
- confirmation,
- finality.

Applications therefore solve an implicit translation problem.

              Business Intent

                     │

             Physical Time

                     │

                     ▼

      Temporal Execution Profile

                     │

                     ▼

     Blockchain Execution Options

                     │

                     ▼

        Allocation Mechanism

Today much of this translation occurs outside the protocol.

TLM investigates whether part of this translation should become protocol-visible.

---

# 4. Representing Temporal Execution Profiles

A Temporal Execution Profile intentionally separates **execution preferences** from their mathematical representation.

Different blockchain protocols may choose different representations.

Possible representations include

- temporal bid functions,
- execution deadlines,
- delay intervals,
- execution classes,
- piecewise value schedules,
- protocol-specific encodings,
- or future representations yet to be explored.

Throughout the TLM research program, **Temporal Bid Functions** are investigated as one natural mathematical representation of a Temporal Execution Profile.

The TLM framework intentionally remains representation-neutral.

The abstraction is the profile.

The function is only one possible representation.
# 5. Economic Motivation for Temporal Execution Profiles

Temporal Execution Profiles are motivated by a simple economic observation.

Applications possess heterogeneous temporal execution preferences, while blockchain execution providers possess heterogeneous execution capabilities.

A market functions most effectively when both sides can communicate sufficient information for efficient matching.

Current blockchain fee markets primarily observe willingness to pay, but observe only a limited portion of an application's temporal execution preferences.

Temporal Execution Profiles investigate whether richer protocol-visible execution preferences may improve this economic matching before allocation mechanisms are applied.

The objective is not to increase throughput.

Nor is it to replace existing fee markets.

Rather, it is to allow blockchain execution markets to better understand the diversity of execution demand already present in today's applications.

---

## 5.1 Demand-side Motivation

Applications today often purchase essentially the same execution service despite having very different execution requirements.

Returning to the examples introduced earlier,

| Application | Primary Requirement |
|-------------|--------------------|
| Liquidation | Immediate execution |
| DEX Swap | Execute within approximately one minute |
| Treasury Settlement | Execute before market close |
| Oracle / NAV Update | Execute before the next reporting deadline |

These applications clearly possess different temporal preferences.

However, much of this information remains invisible to the protocol.

Instead, applications implement temporal optimization themselves through

- gas estimation,
- transaction replacement,
- retry strategies,
- batching,
- rollup scheduling,
- oracle update policies,
- private execution channels,
- application-specific scheduling logic.

These techniques indicate that temporal execution preferences already exist.

They simply remain outside the blockchain execution market.

Temporal Execution Profiles investigate whether part of this information should become protocol-visible.

The objective is not to guarantee execution.

Rather, it is to allow applications to communicate richer execution preferences so that economically feasible demand has a greater opportunity to be accepted.

In this sense, TEPs seek to reduce information loss rather than merely reduce transaction fees.

---

## 5.2 Supply-side Motivation

Execution providers also possess heterogeneous capabilities.

Builders, validators, sequencers, and future execution providers are capable of serving different execution opportunities.

Current fee markets, however, largely optimize over scalar fee bids and immediate transaction inclusion.

Consequently, today's blockchain execution market effectively offers one dominant execution product:

> Immediate execution.

Temporal Execution Profiles create the possibility of supporting richer execution products.

Illustrative examples include

- immediate execution,
- execution within a specified delay,
- execution before an application deadline,
- preferred execution position,
- future execution windows.

These examples are intentionally illustrative rather than prescriptive.

The broader objective is to allow execution providers to better match heterogeneous execution demand with heterogeneous execution opportunities.

Rather than simply reallocating existing blockspace, richer execution products may expand the economically serviceable market for both applications and execution providers.

This perspective shifts the discussion from competition over a single execution product toward a market offering differentiated execution services.

---

# 6. Relationship to Ethereum's Evolution

Ethereum has continuously improved execution market design.

Early fee markets focused primarily on transaction pricing.

EIP-1559 significantly improved price discovery and fee predictability.

Proposer-Builder Separation (PBS) improved supply-side specialization and execution efficiency.

Current research—including Enshrined PBS (ePBS), execution tickets, slot auctions, and related proposals—continues this evolution by investigating improved execution allocation.

This research note investigates a complementary direction.

Rather than asking

> "How should execution opportunities be allocated?"

it asks

> "How should applications communicate execution preferences before allocation begins?"

Temporal Execution Profiles therefore complement existing execution-market research.

They neither assume nor require any particular allocation mechanism.

Instead, they investigate whether richer execution preference information may enable future allocation mechanisms to make better economic decisions.

Ethereum serves as the initial case study because it represents one of the world's most sophisticated blockchain execution markets.

The underlying ideas are expected to apply more broadly to blockchain execution systems.

---

# 7. Current Research Directions

This note introduces **Temporal Execution Profiles (TEPs)** as a conceptual foundation for the Temporal Liquidity Market (TLM) research program.

Building upon this foundation, the project is currently investigating several complementary research directions.

These represent active research rather than finalized protocol proposals.

| Research Direction | Current Objective |
|--------------------|-------------------|
| **Temporal Execution Profiles** | Richer protocol-visible communication of transaction execution preferences. |
| **Temporal Bid Functions** | Mathematical representations of Temporal Execution Profiles. |
| **Urgency Pricing** | Mechanisms through which highly time-sensitive demand may explicitly express urgency. |
| **Patience Incentives** | Incentives encouraging flexible demand to reveal temporal flexibility. |
| **Temporal Liquidity Reserve (TLR)** | Protocol-managed temporal balancing mechanisms based on deterministic feedback rules. |
| **Temporal Market Feedback** | Protocol feedback using observed temporal execution behavior. |
| **Execution Opportunity Markets** | Markets supporting differentiated execution options across time and ordering. |
| **Builder Optimization** | Builder optimization using Temporal Execution Profiles rather than scalar fee bids alone. |

These directions are published to document the current research trajectory of TLM.

Their purpose is not to claim finalized solutions, but to encourage discussion, collaboration, and independent investigation.

Individual mechanisms are expected to evolve as the research progresses.

---

# 8. Conclusion

Ethereum has demonstrated that improvements in market design can significantly improve blockchain execution markets.

This note proposes that another opportunity now exists.

Rather than focusing exclusively on allocation mechanisms, future execution markets may also benefit from richer communication of transaction execution preferences.

Temporal Execution Profiles represent one possible direction toward that objective.

Whether they ultimately lead to new pricing models, execution products, scheduling policies, or protocol mechanisms remains an open research question.

The central hypothesis of this note is modest:

> Richer communication of execution preferences may enable richer execution markets.

---

# Research Philosophy

The Temporal Liquidity Market (TLM) project is developed as an open research program.

It distinguishes between

- Foundation Documents,
- Research Notes,
- Mechanism Notes,
- and Protocol Implementations.

Research Notes introduce conceptual ideas rather than finalized protocol proposals.

Mechanism Notes investigate candidate protocol realizations built upon those concepts.

Public publication serves two complementary purposes.

First, it establishes a transparent, timestamped record of the project's evolution.

Second, it encourages constructive discussion and collaboration within the broader blockchain research community.

Mechanisms may evolve.

Implementations may change.

The objective of the TLM project is to progressively refine its conceptual foundations through open research and community feedback.
