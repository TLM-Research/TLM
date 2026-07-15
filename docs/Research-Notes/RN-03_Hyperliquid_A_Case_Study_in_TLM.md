# RN-03 v0.1

# Hyperliquid: A Case Study in Temporal Execution Markets

**Temporal Liquidity Market (TLM) Research Program**\
**Research Note RN-03**\
**Version:** 0.1 (Working Draft)\
**Status:** Internal Research Note\
**Date:** July 2026

------------------------------------------------------------------------

# Abstract

This research note records observations arising from the study of
Hyperliquid as a decentralized exchange built on its own Layer-1
blockchain.

The purpose of this note is **not** to evaluate Hyperliquid as a
product, nor to propose a new protocol mechanism. Instead, Hyperliquid
is treated as an empirical case study that reveals execution
characteristics not explicitly represented in current blockchain
execution markets.

Several observations emerged during this study:

-   low latency and execution urgency are distinct concepts;
-   predictable execution demand has economic value;
-   sustained temporal demand differs fundamentally from unpredictable
    spot demand;
-   application-specific temporal requirements may explain why
    specialized Layer-1 blockchains continue to emerge.

These observations are archived here as motivation for future TLM
research.

------------------------------------------------------------------------

# 1. Hyperliquid as an Observation

Hyperliquid is a decentralized perpetual futures exchange implemented on
its own specialized Layer-1 blockchain.

Unlike many decentralized exchanges built on Ethereum, Hyperliquid
emphasizes:

-   fully on-chain order books;
-   deterministic order sequencing;
-   sustained low execution latency;
-   high transaction throughput;
-   low transaction cost.

Hyperliquid's documentation states that HyperCore includes “fully onchain
perpetual futures and spot order books” and that “every order, cancel,
trade, and liquidation happens transparently” [1]. Its order-book
documentation further states that orders are matched using “price-time
priority” [1]. These statements establish that order placement,
cancellation, matching, trading, and liquidation are part of the
on-chain execution path rather than an external matching service.

The important observation is not its performance numbers.

The important observation is that Hyperliquid chose to build an
independent execution environment rather than operate as an application
on an existing general-purpose blockchain.

This naturally raises the question:

> What execution characteristics were unavailable in current blockchain
> execution markets?

This note records observations related to that question.

------------------------------------------------------------------------

# 2. Temporal Characteristics

Instead of describing Hyperliquid by TPS or hardware performance, we
describe it using temporal characteristics.

  Property             Observation
  -------------------- ---------------------
  Latency              Very low
  Throughput           Sustained high
  Ordering             Deterministic
  Demand Pattern       Continuous
  Aggregate Volume     Very large
  Exceptional Events   Bursty liquidations

These temporal characteristics appear to influence system architecture
more directly than raw throughput. Hyperliquid reports that mainnet
supports “approximately 200k orders/sec” [1]. That figure is relevant
because it is reported as order-processing capacity for a fully on-chain
order-book system, not merely as generic token-transfer throughput.

------------------------------------------------------------------------

# 3. Two Classes of Execution Demand

## 3.1 Continuous Execution

Examples include:

-   order book updates;
-   order modifications;
-   market synchronization.

Characteristics:

-   continuous;
-   predictable;
-   long duration;
-   high aggregate volume;
-   low latency requirement.

Although individual transactions require low latency, their arrival
pattern is largely predictable over time.

## 3.2 Event-driven Execution

Examples include:

-   liquidation cascades;
-   arbitrage opportunities;
-   emergency transactions.

Characteristics:

-   bursty;
-   unpredictable;
-   immediate execution;
-   high willingness to pay.

Unlike continuous execution, these transactions arise spontaneously and
compete for execution capacity without prior coordination.

------------------------------------------------------------------------

# 4. Low Latency, Low Cost, and the Ethereum Fee–Delay Relationship

A commonly stated reason that a Hyperliquid-style fully on-chain order
book is difficult to build directly on Ethereum is cost. Every order
placement, cancellation, modification, trade, and liquidation would
consume blockspace and incur gas-related execution costs. At the
transaction frequency required by an active order book, those costs
would be borne by the exchange, market makers, or traders and could
become economically prohibitive.

Latency is the second commonly stated constraint. An order-book exchange
must process and disseminate state changes quickly enough to support
price-time priority, order cancellation, automated strategies, and an
experience comparable to centralized exchanges. HyperCore's own
description is direct: its order book works similarly to centralized
exchanges, is fully on-chain, and matches orders in price-time priority
[1]. Hyperliquid also reports approximately 200,000 orders per second
[1]. These claims show that low-latency order processing is a primary
architectural requirement rather than a secondary optimization.

This differs from the dominant Ethereum DeFi exchange architecture.
Uniswap describes an automated market maker as a decentralized exchange
that operates “not [with] order books” and instead uses smart contracts
to price trades automatically [4]. Its developer documentation states
that Uniswap manages liquidity pools containing reserves of two tokens
and updates prices from pool state [4]. Thus, Uniswap's core exchange
mechanism is a liquidity-pool-based AMM rather than a continuously
updated central limit order book. This produces a different execution
model and trader experience from order-book venues such as Binance.

The usual framing treats Hyperliquid's two objectives as jointly
difficult:

-   very low execution latency;
-   very low cost per order action.

Under Ethereum's current transaction-fee mechanism, users seeking faster
inclusion generally attach a higher priority fee or otherwise submit a
more competitive fee bid. Zhao explicitly models an auction that “links
users' transaction fee bidding to time preference” [2]. The paper
therefore treats fee bidding and delay tolerance as economically linked,
rather than as unrelated transaction attributes.

Liu et al. likewise study EIP-1559 through the joint behavior of fees and
waiting time. Their empirical conclusion is that EIP-1559 reduced users'
waiting times but had “only a small effect on gas fee levels” [3]. This
is important for RN-03: the mechanism improved waiting-time performance
without establishing a general low-cost, low-latency service for
high-volume application traffic.

This establishes an observed relationship:

Higher Fee Bid

        │
        ▼
Higher Inclusion Priority

        │
        ▼
Lower Expected Delay

Equivalently, lower fees are normally associated with a willingness to accept longer and less certain waiting times.

That relationship is real within the current spot fee market, but it should not be treated as a physical law of blockchain execution. It arises from a mechanism in which transactions reveal demand individually, after arrival, and compete for scarce near-term blockspace. The mechanism largely interprets willingness to pay as urgency.

The Hyperliquid case exposes the limitation of this framing. A sustained stream of order-book actions may require consistently low latency while also being:

- forecastable;
- high-volume;
- long-duration;
- bounded by a known traffic profile;
- economically valuable in aggregate.

Such traffic need not impose the same scheduling uncertainty as an unexpected liquidation cascade. Its low-latency requirement does not necessarily imply a high urgency premium for every transaction.

The research issue is therefore not simply whether users can pay more to reduce delay. It is whether a blockchain can separate:

1. the cost of providing a low-latency service;
2. the cost imposed by unpredictable and bursty demand;
3. the base physical cost of computation, bandwidth, storage, and validation;
4. the premium for displacing or preempting already planned execution.

This distinction is central to the Hyperliquid case. Hyperliquid seeks low latency and low unit cost simultaneously. Ethereum's present spot fee market tends to couple low delay with higher payment. Temporal Liquidity asks whether credible information about sustained demand can relax that coupling.

------------------------------------------------------------------------

# 5. Latency and Urgency

One important observation from the Hyperliquid study is that latency and
urgency are different concepts.

Order book updates require extremely low latency.

However, their arrival pattern is largely predictable.

Liquidation events also require extremely low latency.

Their arrival pattern is highly unpredictable.

Therefore,

> **Low latency does not necessarily imply high execution urgency.**

The distinguishing characteristic is not latency itself, but the
predictability of demand.

------------------------------------------------------------------------

# 6. Predictability as Economic Value

Predictable execution demand provides information that is economically
valuable to the network.

An application capable of expressing:

-   expected execution rate;
-   execution duration;
-   aggregate transaction volume;
-   acceptable burst limits;

reduces scheduling uncertainty.

This information allows execution capacity to be planned rather than
allocated solely through reactive spot bidding.

Predictability therefore possesses economic value independent of
transaction size or execution latency.

------------------------------------------------------------------------

# 7. Unit Cost versus Aggregate Value

Continuous execution streams may consist of millions of transactions.

Although the network may charge a relatively low fee per transaction,
the aggregate economic value remains substantial because of sustained
volume over time.

Conversely, unpredictable spot transactions may pay very high fees
despite relatively small aggregate volume.

This suggests that:

> **Unit price and aggregate economic value should be considered
> separately.**

------------------------------------------------------------------------

# 8. Spot Demand versus Sustained Demand

Current blockchain execution markets primarily allocate execution
through spot transactions.

Each transaction competes independently for immediate execution.

The Hyperliquid case suggests another category of demand.

Long-duration execution streams possess characteristics that differ from
isolated spot transactions.

These characteristics include:

-   predictable arrival;
-   sustained execution rate;
-   stable aggregate demand.

The distinction between sustained temporal demand and spot temporal
demand appears significant and deserves further investigation.

------------------------------------------------------------------------

# 9. Specialized Layer-1 Chains

The Hyperliquid case suggests that specialized Layer-1 blockchains may
arise for reasons beyond raw throughput.

Applications may require execution characteristics such as:

-   deterministic ordering;
-   sustained low latency;
-   predictable execution cost;
-   continuous execution capacity.

These characteristics are temporal in nature.

Whether general-purpose blockchains can expose these execution
characteristics without requiring independent Layer-1 systems remains an
open research question.

------------------------------------------------------------------------

# 10. Implications for Temporal Liquidity Market

This case study suggests several observations relevant to TLM.

1.  Execution demand possesses temporal characteristics beyond
    transaction price.
2.  Predictability and latency are independent dimensions.
3.  Continuous execution and event-driven execution should not
    necessarily be treated identically.
4.  Execution markets currently emphasize spot allocation while
    providing limited representation of sustained temporal demand.
5.  Application-specific temporal execution characteristics may deserve
    to become protocol-visible information.

------------------------------------------------------------------------

# 11. Relationship to Temporal Execution Throughput (TET)

The Hyperliquid study also motivates further investigation of Temporal
Execution Throughput (TET).

Current execution markets often assume an inverse relationship among:

-   latency;
-   throughput;
-   execution cost.

The observations recorded here suggest that this relationship may be
more nuanced.

Predictable sustained demand may permit:

-   lower average execution cost;
-   sustained low latency;
-   higher effective throughput;

through improved temporal coordination rather than increased hardware
capacity.

This observation motivates future work on TET but does not attempt to
define it.

------------------------------------------------------------------------

# 12. Summary

1.  Hyperliquid demonstrates temporal execution characteristics
    different from those assumed by current blockchain execution
    markets.
2.  Continuous execution demand and event-driven execution demand
    possess fundamentally different temporal properties.
3.  Low latency and execution urgency are distinct concepts.
4.  Predictable demand has measurable economic value because it reduces
    scheduling uncertainty.
5.  Sustained temporal demand differs from isolated spot demand.
6.  Specialized Layer-1 systems may reflect missing temporal execution
    abstractions rather than throughput limitations alone.
7.  These observations motivate further investigation of Temporal
    Liquidity Market and Temporal Execution Throughput.

------------------------------------------------------------------------

# References

1. Hyperliquid Documentation, “About Hyperliquid,” “HyperCore Overview,”
   and “Order Book.” Cited for the fully on-chain order book, on-chain
   handling of orders, cancellations, trades, and liquidations,
   price-time priority, and reported order-processing throughput.

2. Yinhong Zhao, “Quantifying the Loss from Blockchain Network Delay:
   Evidence from Ethereum,” SSRN, revised 2024. Cited for the structural
   auction model linking transaction-fee bidding to users' time
   preferences and for the economic interpretation of delay cost.

3. Yulin Liu, Yuxuan Lu, Kartik Nayak, Fan Zhang, Luyao Zhang, and Yinhong
   Zhao, “Empirical Analysis of EIP-1559: Transaction Fees, Waiting Time,
   and Consensus Security,” ACM CCS, 2022. Cited for empirical findings
   on EIP-1559's effects on waiting time and gas-fee levels.

4. Uniswap Labs, “What Is an Automated Market Maker?” and Uniswap
   Developer Documentation, “How Uniswap Works.” Cited for the
   distinction between AMM-based liquidity pools and order-book exchange
   mechanisms.

------------------------------------------------------------------------

**End of RN-03 v0.1**
