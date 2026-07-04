# Temporal Liquidity Market (TLM)

# Foundation Statement — Part II: Conceptual Framework

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public Draft
**Last Updated:** July 2026

---

# Part II — Conceptual Framework

Part I introduced the motivation for Temporal Liquidity Market (TLM) and established **Temporal Liquidity** as the central economic concept of the framework.

This part describes how TLM views decentralized execution markets, the responsibilities of blockchain protocols, and the conceptual principles that guide future protocol design.

Rather than prescribing specific mechanisms, this framework establishes the architectural principles upon which future mechanisms may be developed.

---

# 5. Design Principles

The TLM framework is guided by several fundamental principles.

## 5.1 Participant Neutrality

Blockchain protocols should remain economically neutral with respect to individual participants.

Users, searchers, builders, proposers, validators, and future protocol participants should continue optimizing according to their own objectives.

The protocol should facilitate coordination rather than prescribe behavior.

---

## 5.2 Protocol Neutrality

TLM is designed as an extension of decentralized market infrastructure rather than a replacement for existing Ethereum architecture.

The framework seeks to complement protocol evolution—including EIP-1559, PBS, and ePBS—without assuming a particular market structure or implementation.

---

## 5.3 Information Principle

The primary role of the protocol is to make economically meaningful information visible rather than to make economic decisions on behalf of participants.

Participants remain responsible for optimization.

The protocol's responsibility is to provide trustworthy, decentralized mechanisms through which richer information can be communicated and coordinated.

TLM proposes that **Temporal Liquidity** should be viewed as one such protocol-visible economic signal.

---

## 5.4 Decentralization

Temporal coordination should strengthen decentralized markets rather than centralize decision making.

No participant should gain privileged control over execution decisions merely because additional temporal information becomes available.

---

## 5.5 Simplicity

Protocol rules should remain deterministic, transparent, and understandable.

Additional temporal information should increase market expressiveness without introducing unnecessary protocol complexity.

---

## 5.6 Positive-Sum Design

TLM seeks to expand the overall economic opportunity available to participants rather than merely redistribute existing value.

By allowing transactions with different degrees of Temporal Liquidity to express richer execution preferences, blockchain protocols may increase overall market participation, improve resource utilization, and unlock previously suppressed demand.

The objective is to **grow the market rather than reallocate it**.

---

# 6. Framework Overview

The preceding sections introduced the motivation for Temporal Liquidity and established the design principles that guide the TLM framework.

This section presents the conceptual model through which TLM views decentralized execution markets.

Unlike many protocol proposals that begin by introducing a new mechanism, TLM adopts a **model-first methodology**. Rather than asking what new protocol mechanism should be built, TLM first seeks to understand the underlying economic system that blockchain protocols coordinate.

The objective is to identify the fundamental economic variables that participate in decentralized execution markets, determine which of those variables are already represented by existing blockchain protocols, and investigate whether additional variables should become protocol-visible.

Only after this conceptual model has been established does TLM investigate protocol mechanisms that coordinate those variables.

This separation between **economic concepts**, **protocol representations**, and **mechanism design** is one of the defining characteristics of the TLM framework.

---

## 6.1 Model-first Methodology

Engineering disciplines typically begin by constructing an appropriate model before designing mechanisms.

For example, communication networks model bandwidth, latency, congestion, and packet loss before developing congestion-control algorithms. Operating systems distinguish processes, scheduling policies, and resource allocation before implementing schedulers. Financial markets model supply, demand, liquidity, and information before designing exchanges and auction mechanisms.

Blockchain protocols should be viewed similarly.

Rather than beginning with protocol rules, TLM begins by modeling the decentralized execution market itself.

This methodology asks four sequential questions.

1. **What economic variables influence decentralized execution?**
2. **Which of these variables are already represented by existing blockchain protocols?**
3. **Which economically meaningful variables remain largely implicit?**
4. **What protocol mechanisms could coordinate those variables while preserving decentralization?**

This methodology separates the scientific question of **modeling the market** from the engineering question of **implementing protocol mechanisms**.

---

## 6.2 Economic Variables and Protocol Evolution

Blockchain protocols coordinate economic activity by exposing selected economic variables through protocol-defined representations.

Ethereum already illustrates this principle.

For example,

* transaction fees represent willingness to pay for execution;
* gas limits represent computational resource requirements;
* builder bids summarize the economic value of block construction under PBS;
* signed execution payload commitments under ePBS represent builder commitments and settlement guarantees.

These examples reveal a broader architectural pattern.

Ethereum has progressively transformed economically meaningful information into **protocol-visible objects** that enable decentralized coordination.

Each step has expanded the protocol's ability to coordinate participants without requiring centralized decision making.

TLM investigates whether **Temporal Liquidity** should be viewed as another candidate economic variable within this evolutionary process.

Importantly, introducing a new economic variable differs fundamentally from introducing a new protocol mechanism.

Economic variables describe the decentralized market itself.

Protocol mechanisms merely coordinate those variables.

---

## 6.3 Five-layer Conceptual Model

TLM organizes decentralized execution markets into five conceptual layers.

Each layer transforms information from one form into another as transactions move from private economic objectives toward realized execution.

### Economic Layer

Every transaction originates from an underlying economic objective that exists independently of the blockchain protocol.

An arbitrage transaction, a liquidation, a decentralized exchange swap, a rollup batch, and a treasury transfer each pursue different objectives and therefore possess different economic characteristics.

One such characteristic is **Temporal Liquidity**—the economic flexibility of demand with respect to execution time.

This layer describes economic reality rather than protocol implementation.

---

### Representation Layer

Protocols cannot coordinate information that remains hidden.

Economic variables must therefore be represented through protocol-visible objects.

Ethereum already represents several economic properties through transaction fees, gas limits, builder bids, and execution commitments.

TLM asks whether Temporal Liquidity should likewise possess a standardized representation.

Candidate representations—including temporal preference curves, execution windows, probabilistic timing preferences, and future abstractions—remain active research topics.

Importantly, the representation itself is **not** Temporal Liquidity; it is merely a protocol-visible description of that underlying economic property.

---

### Market Coordination Layer

Ethereum functions as a decentralized coordination system.

Users, wallets, searchers, builders, proposers, validators, relays, and future protocol participants coordinate using protocol-visible information.

Today this coordination occurs primarily through prices, bids, and commitments.

TLM proposes extending this coordination framework by allowing participants to coordinate using Temporal Liquidity in addition to price.

The protocol continues to provide rules for interaction rather than centralized scheduling.

---

### Protocol Layer

The protocol defines the rules under which decentralized coordination occurs.

It governs communication, commitments, settlement, and consensus.

Importantly, protocols should govern **how** information is coordinated rather than determine **what** decisions participants should make.

This distinction is evident throughout Ethereum's evolution.

EIP-1559 does not determine the correct transaction fee.

PBS does not determine the optimal block.

ePBS does not determine the winning builder.

Each mechanism establishes deterministic rules through which decentralized participants optimize independently.

TLM extends this philosophy.

Its objective is not to optimize execution centrally but to investigate whether additional protocol-visible information can improve decentralized coordination.

---

### Execution Layer

The final layer realizes decentralized coordination through transaction execution.

Execution introduces an important distinction among multiple notions of time.

Physical time reflects wall-clock arrival and network latency.

Protocol time reflects slots, epochs, and block production.

Execution time reflects when transactions are ultimately executed.

These notions frequently diverge.

Two transactions arriving milliseconds apart may execute several blocks apart, while transactions arriving seconds apart may execute within the same block.

TLM therefore focuses on **execution opportunity** rather than simply wall-clock arrival time.

Temporal Liquidity concerns the economic flexibility of execution, not merely the passage of physical time.

---

## 6.4 Implications

Viewing decentralized execution markets through this layered model yields several important consequences.

First, protocol evolution becomes easier to reason about because economic concepts remain distinct from protocol representations and implementation mechanisms.

Second, different protocol mechanisms can be evaluated against the same conceptual model without changing the underlying economics.

Third, new economic variables may be introduced incrementally without redesigning the entire protocol architecture.

Temporal Liquidity represents the first major candidate introduced by TLM, but the methodology itself is intentionally more general.

Future research may identify additional economic variables that likewise deserve protocol-visible representation.

---

## 6.5 Summary

The framework presented in this section establishes a model-first methodology for protocol evolution.

Rather than beginning with protocol mechanisms, TLM begins by modeling decentralized execution markets, identifying their fundamental economic variables, and investigating which of those variables should become protocol-visible.

Mechanisms are then viewed as implementations of this conceptual model rather than as the starting point of the research.

In this framework, **Temporal Liquidity should be understood as a candidate economic variable—not as a protocol mechanism.**

This distinction enables TLM to evolve as a long-term research framework while remaining compatible with multiple future protocol designs.
---

# 7. Protocol-visible Economic Information

The previous section introduced a model-first methodology for understanding decentralized execution markets. One consequence of this methodology is that protocol design should begin by identifying the economically meaningful variables participating in the market before proposing mechanisms to coordinate them.

This naturally raises an important question:

> **Which economic variables should become protocol-visible?**

This section argues that Ethereum's evolution can be understood as a progressive expansion of protocol-visible economic information. TLM investigates whether **Temporal Liquidity** should become the next candidate economic variable in that evolution.

---

## 7.1 Why Information Matters

Markets coordinate through information.

Participants make decisions based on the information available to them. Prices, bids, commitments, inventories, and order books all exist because they communicate economically meaningful information that enables decentralized coordination.

Blockchain protocols are no different.

Although blockchains are often viewed as transaction execution systems, they are equally information systems. Protocol rules determine not only how transactions are executed, but also which information becomes visible, trustworthy, and actionable to decentralized participants.

When economically meaningful information remains hidden, market coordination becomes less efficient.

For example, private order flow limits visibility into pending demand. Exclusive order-flow arrangements may prevent competing builders from observing economically valuable transactions. Similarly, hidden execution preferences force users to compress multiple economic objectives into a single observable signal such as transaction fees.

The quality of decentralized coordination therefore depends directly upon the quality of protocol-visible information.

---

## 7.2 Ethereum's Evolution

Ethereum's protocol evolution demonstrates a recurring architectural pattern.

Rather than centralizing market decisions, Ethereum has progressively incorporated economically meaningful information into protocol rules.

EIP-1559 introduced the Base Fee as a deterministic protocol variable that reflects network congestion. Rather than requiring wallets to estimate prevailing gas prices independently, the protocol itself now communicates an important component of market conditions.

Proposer-Builder Separation (PBS) introduced another protocol-visible economic representation. Instead of requiring proposers to perform sophisticated MEV optimization, builders summarize the economic value of complete execution payloads through competitive bids.

Enshrined PBS (ePBS) extends this progression further by incorporating builder commitments and payment guarantees into protocol rules. Information that was previously managed through trusted middleware becomes increasingly governed by the protocol itself.

Viewed together, these developments reveal a broader architectural trend.

> **Ethereum has progressively transformed economically meaningful information into protocol-visible objects that enable decentralized coordination while preserving decentralized decision making.**

TLM investigates whether this evolution naturally extends to Temporal Liquidity.

---

## 7.3 Information versus Decisions

A central principle of TLM is that protocols should expose information rather than make economic decisions.

This distinction is fundamental.

Ethereum already follows this philosophy.

EIP-1559 does not determine the correct transaction fee. Users decide what fees to offer.

PBS does not determine the optimal execution payload. Builders compete to construct valuable blocks.

ePBS does not determine which builder deserves to win. It establishes rules through which decentralized competition can occur securely.

In every case, the protocol governs the market rather than replacing it.

TLM adopts the same principle.

The objective is not for the protocol to decide which transactions deserve priority.

Instead, the protocol should investigate whether additional economic information can be represented and coordinated without reducing participant autonomy.

Participant optimization remains decentralized.

Protocol coordination remains deterministic.

---

## 7.4 Temporal Liquidity as a Candidate Economic Variable

Current blockchain protocols represent willingness to pay effectively.

However, willingness to pay is not the only economically meaningful characteristic of demand.

Transactions also differ in their flexibility with respect to execution time.

An arbitrage opportunity may lose nearly all of its value after a single block.

A decentralized exchange swap may willingly wait several blocks if transaction cost decreases.

A treasury transfer may remain economically unchanged after many minutes.

These transactions differ not simply in urgency, but in the shape of their economic value over time.

TLM refers to this property as **Temporal Liquidity**.

Importantly, TLM does not argue that protocols should infer this property automatically or optimize it centrally.

Instead, TLM asks a narrower research question:

> **Should Temporal Liquidity become a protocol-visible economic variable that users may voluntarily express and market participants may utilize during decentralized coordination?**

This distinction separates the economic concept from any particular mechanism for representing or utilizing it.

---

## 7.5 Opportunities

If Temporal Liquidity becomes protocol-visible, several new opportunities may emerge.

Builders may optimize across a richer economic landscape than price alone.

Users whose transactions are economically flexible may reduce transaction costs without sacrificing utility.

Demand that is currently suppressed because it cannot express execution flexibility may become economically viable.

Protocols may coordinate congestion over both price and time rather than price alone.

Future research may explore multi-period optimization in which present execution decisions interact with projected future demand.

These possibilities remain hypotheses rather than established conclusions.

Their purpose is to motivate further investigation rather than prescribe protocol behavior.

---

## 7.6 Risks and Tradeoffs

Making additional economic information protocol-visible also introduces new risks.

Temporal information may reveal user intentions and reduce privacy.

Builders may obtain strategic advantages through superior interpretation of temporal information.

Exclusive access to temporal signals could reinforce existing concerns regarding private order flow and market concentration.

Richer information may increase protocol complexity, introduce new attack surfaces, or enable strategic manipulation through false signaling.

Furthermore, different applications may require different representations of execution flexibility, making standardized protocol representations difficult.

These concerns are fundamental to the TLM research agenda.

The objective is not simply to expose more information, but to determine **which information should become protocol-visible, under what protocol guarantees, and at what cost**.

---

## 7.7 Open Questions

The discussion above naturally raises several research questions.

* Which aspects of Temporal Liquidity should become protocol-visible?
* What representations best communicate execution flexibility while remaining protocol-simple?
* At which protocol layer should temporal information become visible?
* Who should observe temporal information, and at what stage of execution?
* How should public mempools and private order flow differ in their treatment of temporal information?
* Can privacy-preserving techniques enable temporal coordination without revealing sensitive user intentions?
* How should builder optimization incorporate Temporal Liquidity while preserving participant neutrality?
* Can Temporal Liquidity improve decentralized coordination without introducing unacceptable complexity or centralization?

These questions remain intentionally open.

The purpose of TLM is not to answer them prematurely, but to establish the conceptual framework within which they may be investigated.

---

# 8. Decentralized Temporal Coordination

The previous sections introduced a model-first methodology for decentralized execution markets and argued that blockchain protocols evolve by making economically meaningful information protocol-visible.

This naturally leads to the next question:

> **Once richer economic information becomes protocol-visible, how should decentralized participants coordinate using that information?**

TLM distinguishes **coordination** from **control**.

The objective is not for the protocol to determine the correct execution outcome. Rather, the protocol should establish trustworthy rules through which independent participants coordinate according to their own objectives.

This distinction preserves the decentralized philosophy underlying Ethereum while allowing protocol evolution to improve market coordination.

---

## 8.1 Coordination Rather than Control

Ethereum has consistently evolved by improving decentralized coordination rather than introducing centralized decision making.

EIP-1559 coordinates congestion pricing without determining what users should pay.

PBS coordinates block construction without determining which transactions builders should include.

ePBS coordinates commitments between builders and proposers without determining how builders construct execution payloads.

In each case, the protocol governs the interaction among participants while leaving optimization to decentralized markets.

TLM adopts the same philosophy.

Its objective is not to schedule transactions centrally, but to investigate whether richer economic information may enable better decentralized coordination.

---

## 8.2 Communication Enables Coordination

Coordination requires communication.

Participants cannot coordinate using information that cannot be expressed, represented, or observed.

Ethereum already demonstrates this principle.

Users communicate willingness to pay through transaction fees.

Builders communicate block value through competitive bids.

ePBS introduces protocol-visible builder commitments that reduce trust assumptions while improving coordination.

TLM asks whether Temporal Liquidity should similarly become communicable through standardized protocol representations.

If users can voluntarily express execution flexibility, builders may incorporate this information into optimization while remaining fully decentralized.

The protocol therefore facilitates communication rather than prescribing outcomes.

---

## 8.3 From Spatial to Spatiotemporal Coordination

Historically, blockchain protocols have focused on allocating scarce **blockspace**.

Mechanisms such as EIP-1559 improved the efficiency of this spatial allocation by enabling more effective price discovery for limited execution capacity.

Ethereum's recent evolution suggests that protocol research is increasingly extending beyond the allocation of blockspace alone.

Research on ePBS introduces temporal separation between commitments, payload reveal, and execution validation.

Execution Tickets and Slot Auction proposals investigate mechanisms through which future execution opportunities themselves become economically meaningful protocol resources.

Research into shorter slot times explores how execution latency influences protocol performance and user experience.

Meanwhile, many emerging blockchain platforms emphasize lower latency and faster finality as key competitive advantages.

Although these developments pursue different objectives, they share a common direction:

> **Execution time is becoming an increasingly important dimension of blockchain protocol design.**

TLM views these developments as evidence that decentralized execution markets are gradually evolving from **spatial resource allocation** toward **spatiotemporal resource allocation**, in which both blockspace and execution time become economically meaningful resources requiring decentralized coordination.

Importantly, TLM is not primarily concerned with making execution faster.

Rather, it investigates how protocols may coordinate heterogeneous economic preferences regarding execution time while preserving decentralized market principles.

---

## 8.4 Specialization and Protocol Evolution

As decentralized markets become more expressive, coordination naturally becomes more sophisticated.

Ethereum has already demonstrated this evolutionary pattern.

Early blockchain systems relied on a single participant—the miner—to perform nearly every function associated with block production.

PBS introduced specialization by separating block construction from block proposal, allowing builders to focus on optimization while proposers focused on consensus responsibilities.

ePBS further strengthens this architectural direction by incorporating builder commitments into protocol rules.

TLM views this progression as part of a broader trend.

As protocols coordinate richer economic information across both space and time, decentralized markets may naturally develop additional forms of specialization.

Builders may optimize over longer execution horizons.

Future participants may specialize in forecasting temporal demand, managing execution opportunities across multiple blocks, or developing new forms of decentralized market infrastructure.

Importantly, TLM does not advocate specialization as an objective.

Rather, it proposes that richer protocol-visible economic information enables decentralized markets to discover efficient forms of specialization naturally.

---

## 8.5 Growing the Coordination Space

Current execution markets primarily coordinate along one economic dimension: price.

Temporal Liquidity introduces the possibility of coordinating across both **price** and **execution time**.

This additional dimension expands the space within which decentralized participants may express heterogeneous economic objectives.

Rather than forcing all users into a common execution model, protocols may eventually accommodate a broader diversity of applications and execution requirements.

Consequently, richer temporal coordination may increase market participation, improve resource utilization, and enable economic activities that cannot be efficiently expressed through price alone.

This perspective shifts the objective from merely redistributing existing blockspace toward increasing the overall economic capacity of decentralized execution markets.

---

## 8.6 Risks and Open Questions

Expanding decentralized coordination also introduces new challenges.

Additional protocol-visible information may increase strategic behavior, privacy concerns, protocol complexity, and opportunities for market concentration.

Temporal information may be misrepresented.

Builders may gain advantages through superior interpretation of temporal signals.

Future protocol designs must therefore carefully balance expressiveness against simplicity, transparency, and decentralization.

Accordingly, TLM does not conclude that additional information necessarily improves coordination.

Instead, it poses a broader research question:

> **Which economically meaningful information should become protocol-visible in order to improve decentralized coordination while preserving participant neutrality, protocol simplicity, and decentralized market competition?**

Temporal Liquidity represents one candidate answer to this question.

The broader methodology remains applicable to future protocol evolution.

---

## 8.7 Summary

This section completes the conceptual framework established in Part II.

TLM proposes that protocol evolution should be understood as the progressive improvement of decentralized coordination rather than centralized optimization.

Beginning with a model of decentralized execution markets, TLM identifies economically meaningful variables, investigates which should become protocol-visible, and explores how decentralized participants may coordinate using richer information.

Within this framework, Temporal Liquidity is not merely a mechanism for improving fee markets.

It is a candidate economic variable within a broader transition toward **spatiotemporal market design**, where both blockspace and execution time become first-class dimensions of decentralized resource allocation.

The remaining sections of the Foundation Statement build upon this conceptual framework to explore research directions, design implications, and future protocol evolution.

