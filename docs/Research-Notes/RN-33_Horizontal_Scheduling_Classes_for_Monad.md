---
id: RN-33
title: "Horizontal Scheduling Classes for Monad"
subtitle: "Deriving a class system from DiffServ, and fixing what a class is, what the second price buys, and what makes a declaration bind"
version: "0.2"
status: "Working draft - conceptual mechanism. Objects and rules fixed; no encoding, no parameters."
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-11"
license: "CC-BY-4.0"
---

# RN-33 v0.2

# Horizontal Scheduling Classes for Monad

## Deriving a class system from DiffServ, and fixing what a class is, what the second price buys, and what makes a declaration bind

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-33**  
**Version:** 0.2. Absorbs the DiffServ derivation previously drafted separately.  
**Status:** Working draft. Conceptual mechanism, in RN-12's role for Ethereum. It fixes objects and rules and deliberately fixes no encoding, no class parameters and no prices.  
**Date:** 11 September 2026

---

## Abstract

RN-26 locates temporal contention on Monad and argues it is horizontal: the binding scarcity is which class of work obtains capacity in a shared sub-block space, not who is placed first. This note derives a class system for that scarcity, taking its model from **DiffServ**, the Internet's differentiated-services architecture and the one differentiated-service design that reached production at scale. RN-04 takes its class discipline from the same source.

The derivation supplies four things the programme lacked: a **characterisation method**, classes defined by traffic shape crossed with a tolerance vector rather than by application; a **fourth tolerance axis**, position exposure, with no Internet analogue because permuting a packet flow harms nobody and funds no one; a **derived transaction mark**, since DiffServ meters a flow against a rate contract and computes each packet's mark rather than accepting a declaration; and a **binding that is not a price**, because a price bounds willingness to pay and never bounds quantity.

Four decisions follow. A class is a **share of admitted capacity plus a placement discipline**. The **second price attaches to the share**, not to position, since the priority fee already prices position. **Admission binds through a conformance meter**, deterministic in protocol, with members beyond contract degraded rather than refused. The **vertical axis survives inside a class**, ordered by the priority fee that already exists.

Two consequences are specific to this architecture. A class assignment is a fact about the committed order, so settlement completes at consensus and nothing crosses the three-block execution lag. And a class carrying a window gives the scheduler placement freedom under parallel execution, which is a throughput claim rather than a welfare one and is the first thing to test.

---

## 1. What this note fixes

RN-12 plays this role for Ethereum: it states the conceptual mechanism without committing to an encoding. This note does the same for Monad.

**Fixed here.** What a class is and what distinguishes one from another. What the second price attaches to and what makes it bind. How the neutral default is protected. Whether the vertical axis survives and what it does. What settles at consensus and what cannot.

**Not fixed here.** Any encoding, whether a typed transaction, an envelope extension or a signed sidecar. The number of classes, their parameters, the price levels, the meter constants. Those belong to RN-34 and RN-35, which must also support their conclusions by simulation.

**Assumed from RN-26.** That contention on this architecture is horizontal rather than vertical, which that note states as a hypothesis and gives the test for. If the measurement goes the other way, this mechanism is aimed at the wrong scarcity and an RN-15 analogue is the right instrument. Nothing below assumes the hypothesis has been confirmed.

---

## 2. Three objects, and why the stream is the unit

A transaction has no rate. It has no cadence, no burstiness, no jitter, no elasticity and no duration. Those are properties of a sequence, and a sequence of one is not a sequence.

This determines what can be declared and what can be checked. A sender declaring "urgent" on a transaction states a preference nothing can verify. A sender declaring "one update every five blocks, jitter within one block" states a property of a stream the chain can observe over that stream's life, and can penalise when the stream departs from it.

Three objects follow and conflating them is the error to avoid.

- **Temporal Stream Profile.** What a sender declares about its own demand: rate, cadence, footprint, and the tolerance vector of sec. 4.2. A demand object.
- **Scheduling class.** What the protocol does with a stream that selects it: admit now or not at all, hold a cadence, place freely within a window, take residual capacity. A supply object, named for the treatment rather than the workload.
- **The mapping.** Which profiles should select which class. Guidance, and not protocol.

The term *scheduling class* is borrowed from operating systems rather than networking, where a scheduling class names the discipline applied, as in first-in-first-out, round-robin or idle, and never the program that asked for it. That is the rule RN-04 sec. 4.1 states: classes specify protocol-defined execution semantics, not application identities.

---

## 3. The model, and what its document statuses show

DiffServ defines a small set of forwarding treatments and a large codepoint space, with classification at the network edge and simple forwarding in the core. Four points from it carry.

**Classes are characterised, not enumerated.** IETF RFC 4594 defines twelve service classes and describes each by traffic shape, being packet size distribution, constant or variable rate, elastic or inelastic, bursty or not, and flow duration, crossed with tolerance to loss, delay and jitter. Applications are mapped in as examples. The stated reason is that characterising by shape and tolerance lets future applications with similar properties land in an existing class without a standards change.

**Jitter is a separate axis from delay**, and the separation carries content. Multimedia Streaming tolerates medium delay and is marked "yes" to jitter; Broadcast Video tolerates medium delay and requires low jitter. Same delay budget, opposite jitter requirement, different class. A scalar urgency field cannot express that difference.

**The vocabulary is larger than the deployment.** Sixty-four codepoints, four behaviour families, twelve documented classes, and a recommendation that operators "start off with three or four service classes for user traffic and add others as the need arises."

**The IETF separated treatments from mapping, and its document statuses record it.** RFC 4594 is *Informational* and says of itself that it "does not specify an Internet standard of any kind"; it describes itself as project plans for furniture built from a toolkit. The toolkit is standards track: the DS field is RFC 2474, Assured Forwarding RFC 2597, Expedited Forwarding RFC 3246, Lower Effort RFC 8622. **What the network does is specified; which traffic should ask for what is advice.** That is sec. 2's three-object split, reached by a standards body over a decade of deployment, and it is why the workload-flavoured names in RFC 4594 bind nothing.

---

## 4. Characterising execution demand

The method transfers. The contents do not, and substituting them is most of the work.

### 4.1 Traffic characteristics

| Characteristic | Packet networks | Execution |
|---|---|---|
| Size | packet size distribution | gas or resource envelope per member |
| Rate | constant or variable emission | arrival rate and its constancy |
| Periodicity | implicit in rate | explicit cadence, and its tolerance |
| Elasticity | reacts to loss by reducing rate | reacts to price by reducing rate |
| Burstiness | self-correlated arrivals | correlation with common events, which is stronger |
| Duration | flow lifetime | stream persistence and renewal |
| **Footprint** | none | **state accessed, read and write** |

The last row has no packet analogue and is the largest single difference. A packet's cost to the network is essentially its size. A transaction's cost depends on what it touches: two transactions of identical gas may conflict or not, and under parallel execution that changes the work performed. A stream repeatedly touching one hot account is a different object from one touching disjoint state at the same rate, and no traffic descriptor borrowed from networking captures it.

### 4.2 The tolerance vector needs a fourth axis

| Axis | DiffServ | Execution |
|---|---|---|
| Exclusion | loss | fraction of members never included, or expiring |
| Delay | delay | time from submission to inclusion |
| Jitter | jitter | variance of the realised inclusion interval |
| **Position exposure** | none | **sensitivity to placement relative to other transactions** |

The first three carry over intact. Jitter matters here for the reason it matters for voice: a stream with a cadence requirement is harmed more by irregularity than by a uniformly longer interval.

**The fourth has no Internet analogue and is not a refinement of delay.** Within a TCP flow, packet order is restored at the receiver and no party profits from permuting it. On a chain, placement relative to *other* transactions determines outcome and funds extraction. Two streams may agree on exclusion, delay and jitter tolerance and differ completely here: a periodic oracle update is position-exposed because others trade against it, while a payment stream at the same cadence is not.

A profile omitting this axis cannot distinguish the workloads that most need distinguishing.

---

## 5. The classes

### 5.1 A class is a share and a discipline

```text
class  =  ( share of admitted capacity ,  placement discipline )
```

The **share** is the capacity dimension: how much of a block's admitted gas the class may hold. The **discipline** is what the scheduler does with members inside that share.

Both are necessary. A class defined by share alone is a price tier wearing a service label, which RN-04 sec. 4.3 forbids: a class differing only in price belongs in the fee layer. A class defined by discipline alone has no capacity guarantee and collapses under contention.

### 5.2 Effective share is not nominal share

Under optimistic parallel execution the work the network performs depends on the conflict structure of what it admitted, so a class holding a given gas share does not deliver a fixed amount of completed work. A class whose members touch disjoint state converts its share efficiently; one concentrated on a hot account converts the same share into more re-execution and less throughput.

**A share is a claim on admitted gas, not on completed work**, and the gap between them is a property of the class's footprint. Any allocation rule treating shares as interchangeable assumes away the architecture's defining feature.

### 5.3 The candidate set

Named for what the protocol does, not for who uses it.

| Class | Discipline | Share treatment |
|---|---|---|
| **Expedited** | next block or not at all | capped, not merely priced |
| **Assured** | committed rate honoured; excess degraded, not refused | committed share plus burst allowance |
| **Cadenced** | declared interval held, variance minimised | reserved share sized to the cadence |
| **Deferrable** | placed anywhere inside a declared window | drawn from what other classes leave |
| **Lower Effort** | residual capacity only, yields under contention | no reservation |
| **Default** | current treatment, unchanged | protected floor, sec. 8 |

Two have no clean DiffServ counterpart and both are specific to execution. **Cadenced** exists because jitter and delay tolerance separate more sharply here than in packet networks, where Expedited Forwarding bundles them, and because at 400 milliseconds a cadence over twenty-five blocks is a schedulable object where a cadence over a twelfth of an Ethereum slot is not. **Deferrable** exists because placement freedom is worth something to the scheduler under parallel execution, which has no analogue in a network forwarding packets independently.

**Lower Effort deserves attention.** RFC 8622 standardises a below-best-effort behaviour and **nothing compensates traffic for marking it.** Senders use it because during congestion unmarked traffic competes and loses while Lower Effort traffic passes in the gaps. If that incentive transfers, a supply side exists with no transfer of value, and the compensation machinery a two-sided crossing needs is unnecessary for this class. Whether it transfers is empirical and is the cheapest thing in this note to test.

Per the DiffServ guidance, a deployment should start with three or four and add as need appears. Which three or four is empirical and belongs to RN-34 and RN-35.

### 5.4 Mapping profiles to classes

Non-normative. A profile qualifies by its declared characteristics, never by the name of the application that produced it.

| Stream characterisation | Exclusion | Delay | Jitter | Position | Class |
|---|---|---|---|---|---|
| very high rate, near-constant, hot state, members individually disposable | high | very low | low | very high | Expedited or Assured |
| bursty, shock-correlated, inelastic, short-lived | very low | very low | n/a | very high | Expedited |
| constant cadence, inelastic, widely-read state | low | medium | **very low** | high | Cadenced |
| low rate, hard cutoff, indifferent to placement before it | very low | high until the bound | high | very low | Deferrable |
| high count, largely disjoint state, elastic, wide window | low | high | high | very low | Deferrable or Lower Effort |
| low rate, no deadline in horizon, elastic | medium | very high | very high | very low | Lower Effort |
| undeclared | Default |

Workload examples, illustrative only: order-book quote and cancel, and liquidation or arbitrage, for the first two rows; oracle and funding updates for the third; settlement and expiry-driven work for the fourth; payment transfers for the fifth; indexing and maintenance for the sixth.

The characterisation separates what a priority scalar cannot. The first two rows agree on position exposure and disagree on exclusion tolerance, since a cancelled quote can be resent and a missed liquidation cannot. The third and fifth may share a delay budget and differ by an order of magnitude in jitter tolerance. The fourth and sixth both accept long delay and differ on whether the delay has a bound.

---

## 6. The transaction mark is derived, not declared

This is the structural result taken from the model, and it changes what the programme has assumed.

Within Assured Forwarding the part that varies per packet is the drop precedence, and RFC 2697 and RFC 2698 specify how it is set: a token-bucket meter measures the flow against its committed rate and marks each packet green, yellow or red by conformance. **The sender does not choose the colour.** It chooses the class and accepts a rate contract; the colour follows from whether the stream keeps to it.

```text
declared    TSP   = class + rate contract + tolerance vector
observed          = realised arrivals, gas, state footprint
derived     TEP_i = f( TSP , conformance of the stream at i )
```

Three consequences.

**The manipulation surface shrinks.** A sender who cannot set the per-transaction mark cannot inflate it per transaction. What remains misreportable is the stream contract, one declaration covering many transactions, checkable against many observations.

**The binding becomes natural.** RN-02 requires that a declaration rest on realised behaviour plus a cost binding. That is hard for one transaction, whose realised behaviour is a single data point, and straightforward over a stream.

**TEP keeps a narrower role.** For a transaction belonging to no stream it remains an independent declaration, which is RN-01's case and what RN-15 is built on. For a stream member it is derived. RN-26 argues that at short block times the stream becomes the primary demand object because a transaction's profile is thin; this gives that argument its mechanism. The transaction-level object is thin because it is derived.

---

## 7. The second price

### 7.1 It attaches to the share

RN-26 states the gap: a priority fee prices vertical position and cannot express how much of the substrate a class holds or who may enter it.

**The second price buys a share.** It prices reserved capacity within a class over an interval, not being earlier. The priority fee continues to price position, now inside the class rather than across the block.

Two prices, two axes, no overlap. That is the cleanest reason to keep both rather than folding the temporal payment into the existing fee, and it is a different answer from RN-15's, where the temporal authorization and the priority fee both bear on position and had to be separated by argument.

### 7.2 The meter makes it bind

Without a cost binding every transaction claims the best class and the classes collapse. That is DiffServ's marking problem and RN-02's central diagnosis, reached independently.

On the Internet the binding is administrative: an edge router distrusts the endpoint's marking and re-marks by policy. A chain has no such point, because the sender signs and nobody can re-mark.

The substitute is the conformance meter of sec. 6. A stream declares a rate contract with its class; the protocol measures it deterministically from the declared terms and observed history; **members beyond contract are degraded to a lower class rather than refused.**

Three properties follow. A sender cannot inflate a single transaction, because its mark is computed. Degrading rather than refusing keeps the failure graceful, since a stream exceeding its contract loses its class rather than its service, a penalty proportional to the breach. And the meter is recomputable by anyone, where DiffServ's re-marking is an act of a trusted middlebox. That is stronger than the model, and it costs protocol state per active stream, which sec. 13 lists as the open cost.

### 7.3 A price is not a cap

RFC 3246 requires Expedited Forwarding to be policed and rate-limited, because unpoliced EF starves every other class. **A price bounds willingness to pay and does not bound quantity.** The highest class needs an explicit capacity cap in addition to whatever it charges, and the cap matters exactly under congestion, when a price alone admits whoever values it most.

---

## 8. The default, and the vertical axis

**Default must exist**, must require no declaration, and must be no worse than current treatment. RN-15 gives the reason: a sender declaring nothing should receive what it receives today, or participation is not voluntary in the ordinary sense.

Two constructions protect it and they are not equivalent. A **floor share** reserves a minimum no other class may take, which is simple and costs the other classes that share whether Default needs it or not. **Residual-only classes** take capacity Default leaves, which cannot degrade Default by construction and makes the differentiated classes worth much less under congestion, which is when they are wanted. The choice is a real trade and this note does not make it.

What is fixed is the constraint: **neutrality is a constraint on the mechanism, not a metric to trade against.** A design improving aggregate service while degrading undeclared traffic has failed whatever its other numbers.

**The vertical axis survives inside a class.** The horizontal axis allocates a share; the priority fee orders members within it. This is Assured Forwarding's structure, where the class determines allocation and the drop precedence resolves contention inside it, kept orthogonal in one field rather than collapsed into a scalar. The mechanism is therefore additive: it does not replace the priority fee, it adds the dimension the priority fee cannot express.

---

## 9. What settles at consensus

Monad decouples agreement from execution, and execution lags by three blocks. A settlement depending on realised gas resolves three blocks after the position was delivered; a settlement depending only on the committed order resolves immediately.

**Class assignment is a fact about the committed order.** Which class a transaction was admitted to, and where it was placed within its class, are both decidable when consensus completes.

So a horizontal mechanism settles in the block and carries no state across the lag. That is the sharpest practical advantage over an RN-15 analogue here, and it follows from the architecture rather than from a choice.

One qualification: the conformance meter needs the stream's history, which is protocol state persisting by design rather than state stranded by the lag. Those are different objects, and only the second is what RN-15 was built to avoid.

---

## 10. Placement freedom as a scheduling input

This is the claim most worth testing, and the one that would matter to an execution engineer rather than an economist.

A class carrying a window gives the scheduler a choice it does not have. If a transaction has declared that any of the next several blocks is acceptable, the scheduler may place it where it conflicts least rather than where it arrived. Under optimistic parallel execution, fewer conflicts means fewer aborts and less re-execution, which is additional completed work from the same hardware.

**On Ethereum's serial execution the same declaration buys no throughput at all**, because placement does not change total work. There a Deferrable class is purely an allocation instrument. Here it is both. Declared temporal slack is an input to parallel scheduling: a chain discovering conflicts optimistically is doing so against an arrival order it did not choose, and flexibility declarations let it choose.

Two limits. The scheduler must know where to place a deferrable member, and Monad cannot see conflict structure in advance, since access lists are optional in the inherited transaction model. The slack is usable only with a predictor: historical conflict rates per contract or account, a learned model, or optional declared access sets. **This is the strongest argument in the programme for optional access lists**, because the two proposals close each other: declared slack gives the scheduler freedom and declared access sets tell it how to use the freedom. And a class permitting the scheduler to move a member must still honour the declared bound, or it collapses into best effort and senders stop selecting it.

---

## 11. The link to the base fee

RN-26 finds that Monad's base-fee controller already carries a variance term, estimating the variance of demand around target from realised gas and stepping cautiously when demand is noisy.

A class system supplies the same quantity forward. A Cadenced stream states its interval and jitter bound; an Assured stream states its committed rate. Those are variance parameters, declared before arrival rather than estimated after. **The classes are therefore two instruments in one**: they allocate capacity, and they describe the demand well enough to inform the controller that prices it.

One constraint is fixed here and it is stronger than elsewhere. Letting declarations reach the controller makes the base fee depend on what senders choose, and RN-15 identifies making the base fee strategic as the regression to avoid. **A declaration may inform the controller only once it binds**, which is what sec. 7.2's meter is for, and even then a shadow comparison should precede any live coupling.

---

## 12. Where the model breaks

**End-to-end versus single domain.** DiffServ never delivered end-to-end service across the public Internet, because codepoints are re-marked or cleared at administrative boundaries and inter-domain treatment rests on bilateral agreements. It succeeded inside single administrative domains. A chain is one domain, so the failure that limited DiffServ does not apply here. It returns in full across chains.

**Nobody profits from permuting packets.** Section 4.2's fourth axis exists because this assumption fails.

**Packets within a class are fungible; transactions are not.** Two packets in one Assured Forwarding class are interchangeable to the scheduler. Two transactions in one execution class may conflict on state, and under parallel execution that determines the work performed. Class membership does not imply substitutability, which is sec. 5.2 stated from the other direction.

**The Internet does not settle.** DiffServ allocates without charging, and class choice is governed administratively rather than economically. Any execution analogue must price, which reintroduces every strategic question DiffServ could delegate to a service-level agreement.

---

## 13. What this leaves open

1. **Which three or four classes**, and what their parameters are. Empirical, and it needs RN-26's simulator.
2. **Floor share or residual-only** for protecting Default.
3. **What the rate contract commits**: transactions per interval, gas per interval, or a vector including write footprint. Section 5.2 argues a scalar understates what a share delivers.
4. **What per-stream metering state costs**, against the per-transaction declaration it replaces.
5. **How a stream is identified** without building an identity system, and what stops a sender splitting one stream into several to escape a contract it is breaching.
6. **Whether the conflict predictor of sec. 10 can be built** from history alone, or whether optional access sets are required.
7. **Whether the derived mark survives an adversarial sender** who shapes arrivals to stay in contract while timing the members that matter.
8. **Whether any of this generalises** beyond Monad. Horizontal classes are motivated here by short blocks, parallel execution and a singleton state. Which of the three is doing the work is not established, and the answer decides whether this is a Monad mechanism or a programme-level one.

---

## 14. What RN-34 and RN-35 must add

RN-34 takes the transaction level: the encoding, the window and role semantics, and the admission binding made concrete. RN-35 takes the stream level: cadence, rate envelopes, recurring service and the reliability classes a continuous producer needs, which sec. 6 argues is where the declaration properly lives.

Both must support their conclusions by simulation on RN-26's framework, including its conflict model. A design claim about a parallel-execution chain that has not been run against a conflict-aware simulator is not evidence.

The benchmark is RN-26's, and this note's own claims should be reported against it: sec. 10's throughput claim against effective parallelism, sec. 7's binding against strategic declaration, sec. 8's protection against the neutral-class row.

---

## References

- TLM Research Program. **RN-01: Temporal Execution Profile.** **RN-02: Protocol-Visible Temporal Abstraction.** **RN-04: Temporal Execution Services: A Multi-Class Execution Architecture for Ethereum.** **RN-06: Monad Through the Temporal-Liquidity Lens.**
- TLM Research Program. **RN-12: The Temporal Liquidity Market: A Conceptual Mechanism Design.** **RN-13 Part II: Capacity and Welfare in Blockchain Execution Systems.** **RN-15: A Temporal Liquidity Authorization for EIP-1559.** **RN-26: A TLM Framework and Roadmap for Monad.**

Internet standards documents, with IETF status. The per-hop behaviours are standards track; the architecture, the markers and the workload mapping are informational.

- **RFC 2474** (standards track), Nichols, K., Blake, S., Baker, F. & Black, D. *Definition of the Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers.* December 1998.
- **RFC 2475** (informational), Blake, S. et al. *An Architecture for Differentiated Services.* December 1998.
- **RFC 2597** (standards track), Heinanen, J., Baker, F., Weiss, W. & Wroclawski, J. *Assured Forwarding PHB Group.* June 1999.
- **RFC 2697** (informational), Heinanen, J. & Guerin, R. *A Single Rate Three Color Marker.* September 1999.
- **RFC 2698** (informational), Heinanen, J. & Guerin, R. *A Two Rate Three Color Marker.* September 1999.
- **RFC 3246** (standards track), Davie, B. et al. *An Expedited Forwarding PHB.* March 2002.
- **RFC 4594** (informational), Babiarz, J., Chan, K. & Baker, F. *Configuration Guidelines for DiffServ Service Classes.* August 2006. https://www.rfc-editor.org/rfc/rfc4594.html
- **RFC 8622** (standards track), Bless, R. *A Lower-Effort Per-Hop Behavior (LE PHB) for Differentiated Services.* June 2019.

Monad architecture:

- Milionis, J. & Heimbach, L., Category Labs. **Redesigning a Base Fee for Monad.** October 2025. https://www.category.xyz/blogs/redesigning-a-base-fee-for-monad
- Monad Developer Documentation. **Asynchronous Execution.** https://docs.monad.xyz/monad-arch/consensus/asynchronous-execution
- Monad Developer Documentation. **Parallel Execution.** https://docs.monad.xyz/monad-arch/execution/parallel-execution
