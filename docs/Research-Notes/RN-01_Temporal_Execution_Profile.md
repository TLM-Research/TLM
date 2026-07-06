# TLM Research Note RN-01

# Temporal Execution Profiles (TEP)

## A Demand-Side Communication Model for the Temporal Liquidity Market

**Project:** Temporal Liquidity Market (TLM)\
**Status:** Public Draft\
**Version:** 0.3 (Complete Draft)\
**Date:** July 2026

------------------------------------------------------------------------

# Abstract

Blockchain execution markets have evolved significantly through advances
in pricing and execution allocation. This research note investigates a
complementary direction: improving how applications communicate
transaction execution preferences before allocation begins.

Blockchain applications increasingly exhibit heterogeneous execution
requirements. Some transactions derive value only from immediate
execution, while others remain economically valuable across broader
execution windows. Current blockchain fee markets primarily communicate
willingness to pay through a small number of fee parameters, leaving
much of an application's temporal execution preference implicit.

This note introduces the concept of a **Temporal Execution Profile
(TEP)** as the demand-side communication model within the Temporal
Liquidity Market (TLM). Applications formulate execution requirements in
**Physical Time**, while blockchain protocols allocate execution in
**Blockchain Time**. The role of the Temporal Liquidity Market is to
economically coordinate these two temporal domains through market
allocation.

Although Ethereum serves as the primary case study throughout this note,
the broader concepts are intended to encourage comparative investigation
across other Layer-1 blockchain ecosystems.

------------------------------------------------------------------------

# 1. Introduction

Ethereum has evolved from first-price auctions through EIP-1559 and PBS
toward current research on ePBS, execution tickets and slot auctions.
These developments primarily improve **pricing and allocation**.

This note asks a complementary question:

> Before improving allocation mechanisms, should blockchain execution
> markets first improve how applications communicate their execution
> preferences?

The TLM research program studies this demand-side question.

------------------------------------------------------------------------

# 2. Motivation

Applications possess heterogeneous temporal requirements.

  Application           Desired Execution
  --------------------- -----------------------------
  Liquidation           Immediate
  DEX Swap              Within about one minute
  Treasury Settlement   Before market close
  Oracle / NAV Update   Before next reporting cycle

Current fee markets primarily observe:

``` text
maxFeePerGas
maxPriorityFeePerGas
```

These parameters reveal willingness to pay but reveal relatively little
about **when execution creates value**.

Applications therefore implement retries, gas estimation, batching,
oracle scheduling, rollup scheduling and private order flow outside the
protocol.

------------------------------------------------------------------------

# 3. Temporal Execution Profiles

A **Temporal Execution Profile (TEP)** is a protocol-visible description
of **how an application's economic value varies with alternative
execution outcomes over Blockchain Time.**

A TEP captures application demand without prescribing either the
mathematical representation or the allocation mechanism.

Execution remains the responsibility of the **Temporal Liquidity
Market**.

This separates

-   application intent,
-   demand representation,
-   market allocation,
-   protocol implementation.

------------------------------------------------------------------------

# 4. Physical Time and Blockchain Time

Applications derive economic value in **Physical Time**.

Blockchain protocols allocate execution in **Blockchain Time**.

Ethereum realizes Blockchain Time through protocol slots, blocks
produced within slots, and execution ordering inside blocks.

Different Layer-1 systems may realize Blockchain Time differently while
serving the same conceptual role.

**Figure 1:** `figures/rn01/fig1_tlm_architecture_v0_3.svg`

The Temporal Liquidity Market economically coordinates these two
temporal domains.

------------------------------------------------------------------------

# 5. Representing Temporal Execution Profiles

A TEP is independent of its mathematical representation.

Possible representations include:

-   Temporal Bid Functions
-   execution deadlines
-   delay intervals
-   execution classes
-   piecewise value schedules
-   protocol-specific encodings

Within TLM, **Temporal Bid Functions** are investigated as one natural
representation rather than the definition of a TEP itself.

------------------------------------------------------------------------

# 6. Economic Motivation

The motivation for TEP is economic rather than algorithmic.

Markets function efficiently when participants can communicate
economically meaningful preferences.

Current blockchain execution markets observe price well, but only
partially observe temporal preferences.

The objective of TEP is therefore not to replace existing fee markets,
but to improve communication between applications and execution markets
before allocation begins.

## 6.1 Demand-side

Applications already maintain sophisticated temporal models internally.

Those models remain largely invisible to blockchain protocols.

Making part of this information protocol-visible may allow economically
feasible demand that is currently suppressed or inefficiently expressed
to participate more effectively.

The objective is **not** to guarantee execution.

The objective is to improve the expression of heterogeneous demand.

## 6.2 Supply-side

Execution providers likewise possess heterogeneous capabilities.

Today's markets effectively offer one dominant execution service:

> Execute as soon as possible.

A richer demand language creates opportunities for future execution
markets to offer richer execution options while remaining
protocol-neutral.

Illustrative examples include:

-   immediate execution,
-   execution before a deadline,
-   execution within a delay window,
-   preferred execution ordering.

The purpose is not simply to redistribute existing blockspace, but to
expand the economically serviceable market for both applications and
execution providers.

------------------------------------------------------------------------

# 7. Relationship to Ethereum Research

This work is complementary to ongoing Ethereum execution-market
research.

Where EIP-1559 improved pricing and PBS improved supply-side
specialization, TEP investigates richer communication from the demand
side.

Current research on ePBS, execution tickets and slot auctions primarily
studies allocation mechanisms.

This work instead investigates the information available before
allocation begins.

Ethereum serves as the initial case study because of its mature
execution market.

The concepts introduced here are intended to encourage comparative
studies across other Layer-1 blockchain ecosystems.

------------------------------------------------------------------------

# 8. Current Research Directions

The TLM project is currently investigating several related directions.

  Research Direction            Current Focus
  ----------------------------- -------------------------------------
  Temporal Execution Profiles   Demand-side communication
  Temporal Bid Functions        Mathematical representation
  Urgency Pricing               Explicit urgency expression
  Patience Incentives           Revealing temporal flexibility
  Temporal Liquidity Reserve    Protocol-managed temporal balancing
  Temporal Market Feedback      Learning from realized execution
  Execution Option Markets      Differentiated execution services
  Builder Optimization          Optimization over TEPs

These represent active research directions rather than finalized
protocol proposals.

------------------------------------------------------------------------

# 9. Conclusion

The central contribution of this note is not a new auction mechanism.

Instead, it proposes that blockchain execution markets distinguish
between

1.  how applications communicate execution preferences; and
2.  how execution markets allocate blockspace.

Temporal Execution Profiles address the first question.

The broader Temporal Liquidity Market research program investigates the
second.

------------------------------------------------------------------------

# Research Philosophy

TLM is developed as an open research program.

Research Notes introduce conceptual ideas.

Mechanism Notes investigate concrete protocol designs.

Foundation documents define the long-term conceptual framework.

Public publication establishes a transparent record of the project's
evolution while inviting collaboration from researchers across Ethereum
and other Layer-1 ecosystems.
