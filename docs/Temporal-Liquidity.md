
# Temporal Liquidity

**Version:** 2.1 (umbrella realignment)
**Release:** TLM Public Release (Draft Revision)
**Status:** Public Draft

> This note is the **canonical exposition** of Temporal Liquidity. The Foundation Statement states the one-sentence definition; this note owns the analogy, the dimensions, the deadline-versus-decay structure, the declared-versus-observed distinction, and the worked examples. Other documents reference it rather than restating them.

---

## A Broader Question

Ethereum execution markets have evolved from simple fee markets toward increasingly sophisticated systems for decentralized resource allocation. EIP-1559, PBS, ePBS, builder markets, execution rights, and related research all improve how scarce execution opportunities are coordinated.

These developments motivate a broader question.

> **Does demand contain economically meaningful temporal information beyond willingness to pay?**

TLM proposes that this question should be investigated before proposing new protocol mechanisms. **Temporal Liquidity** is the name this project gives to that information.

---

# Definition

Temporal Liquidity is used, deliberately, as an **umbrella** economic concept — analogous to **market liquidity**, which is not a single quantity but a family of related properties (depth, immediacy, resiliency).

> **Temporal Liquidity is the collection of economically meaningful temporal characteristics of execution demand.**

Two clarifications keep the analogy precise:

- Temporal Liquidity characterizes **demand** (the properties of transactions and streams), whereas market liquidity characterizes a **market or asset**. The parallel is structural — both are umbrellas — not literal.
- Unlike market liquidity's dimensions, which tend to co-move as facets of a single underlying property, the temporal characteristics below may be **largely independent**. Temporal Liquidity is therefore a *category* of related-but-distinct properties, not one multidimensional measure.

"Execution opportunity," used throughout, is intentionally broader than wall-clock time: in blockchain systems demand is coordinated across future execution opportunities such as blocks, slots, or other protocol-defined execution events.

---

# The Dimensions

Temporal Liquidity spans several characteristics, usefully organized by **temporal granularity**:

| Scale | Characteristic | Question it answers |
|-------|----------------|---------------------|
| Intra-slot | **execution priority** — sensitivity of value to ordering *within* a slot | *Where in the sequence must I be?* |
| Inter-slot | **delay tolerance**, **execution windows**, **deadlines** | *How long can I wait, and until when?* |
| Multi-slot / stream | **predictability**, **continuity** | *How forecastable and sustained is my demand?* |

A second distinction cuts across the table: some characteristics are **declared preferences** the demand states (delay tolerance, windows, deadlines, priority), while others are **observed properties** others verify about the demand (predictability, continuity). They are represented and priced differently — declared preferences are what a market charges for; observed properties can earn a coordination benefit only if verified. Individual research notes may investigate a single dimension without implying it is a separate top-level concept.

---

# The Delay-Tolerance Axis and the Elasticity Analogy

The delay-tolerance dimension is where an **elasticity** analogy is tightest, and it is worth stating precisely because it is the most studied.

Where price elasticity characterizes how demand responds to changes in **price**, delay tolerance characterizes how demand responds to changes in **execution timing** — its *movability in time without loss of value*, the temporal counterpart of financial liquidity's "movability without price impact." At the transaction level, the operational object is how economic value changes as execution opportunities are delayed.

This axis itself has **two independent parameters**, which a scalar cannot capture:

- a **deadline** — a hard cutoff after which value drops sharply; and
- a **decay rate** — how quickly value erodes *before* the cutoff.

Fast-decaying arbitrage (steep decay, near-immediate) and a treasury transfer with a hard end-of-day deadline (little decay, then a cliff) are not points on one line — they differ on both parameters. Any representation that assumes a single "flexibility" number will misfit deadline-with-cliff demand.

---

# Concept, Representation, and Mechanism

TLM deliberately distinguishes three layers.

```
Temporal Liquidity            (the economic concept / umbrella)
      ↓
Temporal Representation        (Execution Profile, Temporal Bid, curve, ...)
      ↓
Protocol Mechanism             (how exposed information is coordinated)
```

Temporal Liquidity is the economic concept; temporal representations describe it in protocol-visible form; mechanisms determine how such information, if exposed, is coordinated. Separating the layers lets multiple representations and mechanisms be evaluated without redefining the underlying concept.

---

# Transaction and Stream Perspectives

Temporal characteristics exist at more than one level. A **single execution request** may exhibit a particular delay tolerance, window, deadline, or ordering sensitivity. A **recurring stream** may exhibit predictability and continuity — aggregate structure that cannot be observed from individual transactions alone. Some dimensions (execution priority, delay tolerance) are naturally per-transaction; others (predictability, continuity) are naturally per-stream. Both belong to Temporal Liquidity.

---

# Examples

These examples illustrate the concept rather than define application categories. Temporal Liquidity is a property of a transaction **in its economic context**, not a permanent property of an application.

- **Arbitrage** — very low delay tolerance; value may disappear after one execution opportunity, and it is highly ordering-sensitive (execution priority).
- **Liquidations** — low delay tolerance and unpredictable (bursty), yet acutely urgent.
- **DEX swaps** — may tolerate modest delay depending on market conditions and slippage tolerance.
- **Rollup batch submission** — broader execution windows; predictable, continuous stream demand.
- **Treasury transfers** — remain valuable across many execution opportunities; often carry a hard deadline with little prior decay.

---

# Grounding in Existing Markets

Time-differentiated demand is not new; the novelty is the permissionless, adversarial, neutrality-constrained setting. The dimensions above have mature analogues that the `Related-Work` document develops in full: **peak-load and congestion pricing**; **electricity demand response and interruptible-load** contracts (the closest sibling of delay-tolerant, shiftable demand); **cloud reserved-vs-spot** markets (trading temporal flexibility for price); and the **term structure of interest rates** (a spot-vs-forward curve whose shape reflects aggregate time preferences) as the analogue for pricing demand across an execution horizon.

---

# Open Research Questions

- Which temporal characteristics are economically meaningful, and at what granularity?
- Which should become protocol-visible, and which should remain application-private?
- Which representations preserve simplicity, privacy, and extraction-resistance?
- Can Temporal Liquidity be measured empirically (an identification problem, not merely a data problem)?
- Can participants truthfully reveal declared characteristics, and can observed ones be verified credibly?
- How should transaction-level and stream-level characteristics interact?
- Under what conditions does richer temporal information improve decentralized coordination?

These questions define the research agenda rather than assume its answers.

---

# Summary

Temporal Liquidity is the **umbrella** for the economically meaningful temporal characteristics of execution demand — delay tolerance (with its deadline and decay parameters), predictability, execution priority, execution windows and deadlines, and continuity. Rather than prescribing mechanisms, TLM first identifies these characteristics, investigates appropriate representations, and only then explores decentralized mechanisms that might coordinate them.

In this sense, Temporal Liquidity is not the end of the research program — it is its starting point.
