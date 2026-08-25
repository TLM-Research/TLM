---
id: RN-05
title: "Supply-side Heterogeneity and Temporal Granularity: A Quantum Lattice for Blockspace"
version: "0.4"
status: "Public draft - research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: "August 24, 2026"
---

# RN-05 v0.4

# Supply-side Heterogeneity and Temporal Granularity

## A Quantum Lattice for Blockspace

**Temporal Liquidity Market (TLM) Research Program**
**Research Note RN-05**
**Version:** 0.4
**Status:** Public draft - research note, offered in good faith for comment
**Date:** August 24, 2026

---

## Abstract

The TLM notes to date are demand-side. Temporal Liquidity names the temporal characteristics of demand; the Temporal Execution Profile (RN-01) and Temporal Demand Profile (RN-02) represent them. Supply appears only briefly - RN-01 sec. 5.2 observes that execution providers possess heterogeneous capabilities - and is not developed.

This note takes up that gap. If demand is temporally heterogeneous, the question is whether *supply* should be too: whether a single undifferentiated execution service is the right architecture, or whether a family of differentiated services, distinguished by temporal granularity, better matches heterogeneous demand.

The note introduces **temporal granularity** as a supply-side property and proposes a **quantum lattice**: a sub-slot ordering coordinate system in which ordering is constrained *across* quanta and unconstrained *within* one, and which different participants read at different depths. Slot-level validators resolve slots. A latency-sensitive sub-channel resolves quanta. Both read the same lattice; coarse readers simply do not resolve the fine structure.

Seen as a **multiplexing structure**, the lattice organizes demand along three axes - time (quantum), temporal-liquidity class, and state-access domain - each buying a distinct gain: bounded extraction, service differentiation, and parallelism respectively. This multiplexing lens (sec. 4.5) is where the architecture's value becomes legible, and it is unusual in one specific way: the resource multiplexed is *ordering*, not bandwidth, at a resolution each participant chooses. A companion result (sec. 4.6) shows that because a distributed system has no global clock, the quantum boundary is an interval of width ε, not a point - giving a resolution-confidence tradeoff and a *fine / hard-bounded / consensus-free* trilemma.

Three disciplines are imposed throughout. First, this note proposes **no mechanism**. Second, it deliberately **does not fix a quantum size**, for reasons developed in sec. 4.3. Third, its market-structure claim - that granularity differentiation could support a viable multi-class validator population - is stated as an **open question against which current evidence runs**, not as a thesis (sec. 8).

---

## 1. Motivation: The Supply Side Is Undeveloped

The Foundation Statement asks how decentralized execution markets should represent and coordinate heterogeneous temporal characteristics of demand. The implicit counterpart - what supply must look like for such coordination to be possible - has not been examined.

RN-01 sec. 5.2 states the observation without pursuing it: execution providers possess heterogeneous capabilities, while current fee markets primarily optimize immediate inclusion using scalar bids, so today's market effectively offers one dominant service - *execute as soon as possible*.

A single service is coherent only if demand is temporally homogeneous. These notes argue at length that it is not. RN-03 identifies at least two independent axes and shows demand occupying multiple cells of their cross-product. If demand is multidimensional and supply offers one service, the mismatch is structural.

---

## 2. Empirical Setting

### 2.1 The slot-time debate

EIP-7782, proposed by Barnabé Monnot and targeted at Glamsterdam, would reduce Ethereum's slot from 12 seconds to 6, compressing internal phases from roughly four seconds each to block proposal at 3s, attestation at 1.5s, and aggregation at 1.5s.

This is not the endpoint. The Ethereum Foundation's published strawmap contemplates slot times falling **as low as 2 seconds**, with finality between 6 and 16 seconds via a one-round BFT algorithm (Minimmit), reduced incrementally - on a roughly sqrt(2)-at-a-time schedule - and only when proven safe. Notably, the roadmap **decouples finality from slot time** so each may be optimized independently.

Two observations follow. The trajectory toward shorter slots is established, not speculative; this note does not claim to stop it. And the decoupling principle is itself an instance of the move this note argues for: separating temporal concerns previously conflated. The strawmap decouples finality from slot time. This note asks whether *ordering resolution* should likewise be decoupled from slot time.

### 2.2 Three facts about slot structure

**The slot is already internally subdivided.** Ethereum's slot is a phase sequence - proposal, attestation, aggregation - with distinct deadlines that EIP-7782 re-parameterises. Sub-slot temporal structure carrying real timing semantics *without separate consensus status* is already the existing architecture. This note does not introduce sub-slot time; it asks whether an existing subdivision should become economically visible.

**The validator-burden concern is contested, and the sides measure different constraints.** Critics hold that shorter slots require higher-performance hardware and better connections, raising the barrier to entry, with concern that not all validators could meet the demands, producing a less inclusive network. EIP-7782's own rationale argues the opposite: doubling the slot rate distributes bandwidth more evenly without increasing peak block size, so nodes with modest capacity remain supported.

Both may hold, because they constrain different resources. Bandwidth *throughput* is smoothed by more frequent, smaller blocks; latency *deadlines* are tightened by shorter phases. An operator may be comfortable on the former and squeezed on the latter. Arguments in this area that do not separate the two are imprecise.

**Most of the slot budget is not propagation physics.** The Robust Incentives Group's timing analysis finds blocks generally arrive close to the attestation deadline - 95th percentile 3.3s - while pure block propagation measured from relay publication is under one second, with a 95th percentile near 800ms for blocks from major relays.

The gap between ~800ms of propagation and 3.3s of arrival is not network limitation but builder-side latency optimisation - value captured by consuming available time. **Shortening the slot compresses a budget whose consumption is largely strategic rather than physical.** Reducing the budget does not remove the incentive to consume it; it raises the cost of competing for the same margin.

### 2.3 The sub-100ms frontier is real, and uniformly imposed

Several Layer-1 chains now operate at or below ~100ms block times. Aptos reports ~65ms block times with 400ms finality, and a December 2025 milestone of sub-50ms mainnet block times; its current stack claims cross-namespace transactions at <50ms with sub-second latency and near-instant <10ms block times within a single namespace. Solana's Alpenglow targets 150ms finality. Sui reaches under 400ms for owned-object transactions, which bypass full consensus entirely since only the owner can mutate them.

**Figure 1** (Chainspect, circulated July 2026) ranks Layer-1 block times: Aptos 38ms, Fogo 40ms, Sui 76ms, Somnia 101ms, Solana 397ms, TON 410ms, Sei 417ms, through TRON at 3s.

*Two cautions on this figure.* It is a competitive-positioning artifact rather than a neutral benchmark, and the measured quantity is not labelled. Aptos Labs themselves warn that end-to-end latency - submission to irrevocable settlement - is distinct from internal measurements like block time, which can be misleading. The figure should be read as illustrating a design frontier, not as a measurement basis.

The frontier nonetheless establishes what this note needs: **sub-100ms ordering is an engineering reality, not a speculation.**

It also establishes the contrast that motivates the lattice. Every chain on that figure achieved fine resolution by making *block time itself* small, imposing that resolution uniformly on every validator. Ethereum's strawmap pursues the same path toward 2s. None of these architectures offers *differentiated* granularity. That is the gap this note occupies.

### 2.4 A necessary taxonomy

Four distinct quantities are routinely conflated in this literature. The note uses them as follows.

| Quantity | Definition | Set by |
|---|---|---|
| **Block time** | Interval between block productions | Protocol parameter |
| **Finality** | Time until settlement is irrevocable | Consensus algorithm |
| **End-to-end latency** | User submission to acknowledged settlement | Full pipeline |
| **Ordering-commitment resolution** | Finest granularity at which a position commitment can be expressed and honoured | Commitment and verification cost |

The quantum is an instance of the fourth. It is not a block time, not a finality target, and not an end-to-end latency. sec. 4.3 shows why this distinction determines what sizes are attainable.

**One implication should be stated before it is assumed.** Fine *ordering-commitment resolution* does not imply fine execution, fine finality, or fine global visibility. A 100 ms commitment coordinate sits on top of a slot that still executes, finalises, and propagates on its own schedule. What a fine quantum buys is a finer unit in which a *position commitment* can be expressed and later checked - not faster settlement, and not a guarantee that every participant observes the fine structure as it happens. Claims about what granularity delivers should be read against this row of the table and no other.

---

## 3. Temporal Granularity as a Supply-side Property

> **Temporal granularity is the finest temporal resolution at which an execution provider can reliably make and honour ordering commitments.**

Granularity is a *capability*, not a preference - bounded by connectivity, hardware, geography, and software, and in principle observable through realised behaviour rather than declaration. In RN-02's terms it is an **observed property**, subject to the verification requirement of RN-02 sec. 6.

Granularity is not speed. A coarse-granularity operator is not necessarily slow in aggregate; it is imprecise about *position*. It may deliver reliable inclusion within a slot while being unable to commit to a position inside it.

Granularity is what a uniform block time compresses away. Under a single slot boundary, an operator capable of fine positional precision and one capable only of whole-slot precision provide the *same* protocol-visible service. The finer capability exists but has no representation - the supply-side analogue of the demand-side information loss RN-01 sec. 5.1 describes.

---

## 4. The Quantum Lattice

### 4.1 Definition

> **Definition - Quantum (provisional).**
> A quantum is the indivisible unit of ordering-commitment resolution: a sub-slot interval across which ordering is constrained and within which ordering is unconstrained.

Indivisibility is the substantive property. A commitment cannot be expressed finer than one quantum; the interior is free *because* it lies below the resolution limit of the commitment system. Interior freedom is not a concession but the operational meaning of indivisibility.

**"Free" means priority is not sold, not that order is absent.** A deterministic state machine must still serialize transactions that conflict on shared state, and causally concurrent transactions can conflict. So the interior of a quantum is not an unordered set at execution time; it is a set over which *no ordering commitment has been sold*. Some rule still decides the realised sequence, and an instantiation must say which - a commutative batch where conflicts are excluded by construction, a verifiable-random serialization, or a deterministic conflict-resolution procedure. The distinction matters because "the interior is free" invites the reading that intra-quantum position carries no value, when what the note claims is that intra-quantum position is not *purchasable*. RN-12 sec. 10 and RN-07 make the same point from the mechanism and control-plane sides; sec. 4.4 below carries the cost consequence.

A quantum is therefore not a miniature slot. It fixes a *partial* order: a transaction in quantum *k* precedes all in *k+1* and follows all in *k-1*, while its position among its own quantum's members remains free.

### 4.2 The lattice and its sub-channels

The quanta of a slot form a **lattice** - a shared coordinate system, not a set of separate objects. The term is meant literally, and it is worth saying which lattice: the partitions of a slot, ordered by refinement, form a lattice under the usual meet and join. One partition refines another when every cell of the finer sits inside a cell of the coarser; the join of two partitions is their coarsest common refinement, and the meet their finest common coarsening. A reader resolving whole slots and a reader resolving individual quanta occupy different points in that lattice, and the coarse reading is a genuine coarsening of the fine one rather than a different object. That is what supports the claim below that there is one coordinate system rather than several - and it is why refinement, not subdivision alone, is the operative relation.

Participants read the lattice at different depths. Slot-level validators resolve slots and are unaffected by finer structure. A latency-sensitive **sub-channel** resolves individual quanta. Intermediate participants may resolve at intermediate depth.

This is what makes differentiation possible without fragmentation. There is one coordinate system, not several; coarse readers are not trusting an opaque object but reading the same structure at lower resolution. Fine-grained capability is available to those who need it without being imposed on those who do not - the property that distinguishes the lattice from uniform block-time reduction (sec. 2.3).

A **sub-channel** here means a set of transactions committed at a stated granularity, together with the providers serving them. Whether sub-channels are best defined over transactions, providers, or service tiers is an open question (sec. 9).

**A composition rule is a prerequisite, not an open extra.** The refinement argument above establishes that coarse and fine *readings* are consistent when they describe one partition. It does not establish that commitments issued by *different* providers, at different granularities, without consensus deciding between them, compose into one canonical execution outcome. Post-hoc verification can check that a provider kept a signed promise; it cannot make two providers' promises globally consistent with each other when both touch the same state. Assignment integrity (sec. 4.3) is the narrower problem of one provider labelling honestly; this is the wider one.

Any instantiation therefore has to fix four things: **who issues** a granularity commitment (proposer, builder, or a registered provider), **what certificate** carries it, **what conflict rule** applies when commitments disagree, and **over what scope** a commitment binds - per proposer, per transaction, per state-access domain, or per service class. Where providers touch disjoint state the question is mild, since commuting transactions impose no serialization requirement (sec. 4.5). Where they touch shared state it is the same serialization problem RN-09's triangle and RN-12 confront, and it should be treated as a precondition on the architecture rather than an item deferred to sec. 10.

### 4.3 On not specifying a quantum size

This note deliberately **does not fix a quantum size**, for two reasons.

The first is consistency: RN-01 sec. 4.1 establishes representation-neutrality as a house principle - the abstraction is the object, the representation an implementation choice. Quantum size is a question of the same kind, and fixing a number would invite argument about the number rather than the architecture.

The second is structural, and is the note's central technical result:

> **The quantum's lower bound is set by commitment and verification cost, not by consensus latency.**

Consensus over a geo-distributed validator set is floor-limited by message propagation: Aptos observes that such a set requires average 100+ms latency to send messages across it, making fast finality a challenge. Ethereum's own propagation is measured near 800ms at p95 from relay publication.

A quantum outside consensus is not subject to that floor. It is a *local* ordering coordinate honoured by a provider before propagation and verified against realised behaviour afterward. Nothing must be agreed across the validator set within one quantum - only *committed to* by the provider and *checked* subsequently.

The quantum can therefore be **much finer than block time - plausibly far below any feasible one - but it is not arbitrarily fine.** Three bounds hold below it. Commitment and verification cost, the note's own result. Clock uncertainty ε, which sec. 4.6 develops and which governs how sharp a boundary can be. And a third that is easy to miss: a commitment must **propagate, be observed, and remain available** for the quantum to function as a *neutral* coordinate at all. A 100-200 ms label visible only to colocated actors is not a global coordinate; it is a private advantage, and fineness bought that way is a colocation subsidy rather than a service. How fine the quantum can usefully be is therefore an empirical question about commitment cost, clock error, and observability jointly - not a physics question, but not an unbounded one either. What survives is the separability claim: granularity and block time are distinct concerns, and the floor on the former is not the consensus floor on the latter.

**One distinction the argument must not blur.** "Verification cost" splits into two problems of very different difficulty, and only one is cheap:

- *Verifying the cross-quantum order* is cheap. The published block reveals the sequence; checking that quantum-*k* transactions precede quantum-*(k+1)* transactions against their labels is trivial.
- *Verifying quantum **assignment** is not.* Which quantum a transaction "arrived in" is attested by the provider. A strategic provider can preserve the partial order perfectly while assigning labels adversarially - placing a victim's transaction in *k+1* and its own flow in *k*. This is invisible in the final ordering and cannot be caught by post-hoc verification of realised behaviour without an **independent arrival witness** (an attester sub-committee, arrival attestations, or cryptographic sequencing).

The fineness result therefore rests only on the cheap half (ordering-commitment verification). *Assignment integrity* is a separate, unsolved problem - the same arrival-witness problem that any sub-slot ordering scheme faces (it is RN-04's sub-slot-lane Problem P1 in this note's vocabulary) - and it is carried explicitly in the threat model (sec. 9).

### 4.4 Consequences

**It is a coarsening, not a refinement, of ordering commitment.** Relative to a fully specified intra-block order, quantum-level commitment says *less*. This aligns with Foundation Part II sec. 5.4's preference for coarse, protocol-simple abstractions, and is why the quantum is a plausible TLM object rather than a complexity increase.

**It provides a tunable parameter.** Quantum size trades commitment strength against construction flexibility. Large quanta approach whole-slot semantics; quanta approaching a single transaction approach full ordering specification. The useful region lies between and is empirically open.

**It bounds, without eliminating, reordering surface.** Free intra-quantum reshuffling confines extraction opportunities within a quantum rather than across the block. Whether this reduces extraction or merely relocates it is open, and should not be asserted without simulation.

**It gives execution priority a coordinate.** RN-01 sec. 3.2 collapses protocol and execution time into a single Blockchain Time, noting the finer split matters when intra-slot ordering is at issue. Execution priority - the intra-slot dimension of Temporal Liquidity - has had no unit in which to be expressed. The quantum is a candidate unit, and this is the note's clearest connection to the umbrella concept.

**Interior structure is not free - it re-imports verification cost.** The fineness result of sec. 4.3 holds for *free-interior* quanta, because nothing inside a quantum must be verified. A service that chooses to *constrain* a quantum's interior - imposing, say, FIFO within it (this is exactly what RN-04's sub-slot Continuous State lane does) - buys stronger semantics at a price: its quantum is now bounded below not by consensus latency but by *its own interior-verification cost*, the assignment-integrity problem of sec. 4.3. Interior freedom and fineness are thus two faces of one property, and a class purchases departures from it. This yields a clean design dial across RN-04's portfolio: a class buys as much interior order as it is willing to pay to verify - the Protected Window class takes interior freedom seriously (batch-per-window semantics, where intra-batch ordering games die because the interior is unordered), while the Continuous State class pays for interior order.

---

## 4.5 The Lattice as a Multiplexing Structure

The lattice is most clearly *seen* - and its value most clearly *located* - as a multiplexing system, the vocabulary this note's supply-side lineage (networking, optical transport) makes natural. Classical multiplexing shares a physical channel. The lattice shares two logical resources at once - blockspace *capacity* and sequence *position* - organized along three axes:

| Axis | What it is | Classical analogue | The gain it buys |
|---|---|---|---|
| **Time (quantum)** | sub-slot ordering cells, read at variable depth | TDM + scalable/layered coding | ***positional* multiplexing** - within a quantum, position is unordered, so ordering contention is shared rather than fought, bounding the reordering/extraction surface |
| **Class (temporal-liquidity profile)** | service classes over the demand dimensions (RN-04) | class-based multiplexing (DiffServ) | **service differentiation + statistical-multiplexing gain** - same-class demand shares capacity because its peaks do not coincide |
| **State-access domain** | which state a transaction touches | space-division multiplexing (SDM); database concurrency control | **parallelism** - transactions on disjoint state commute, so they may occupy the same position without conflict |

Two properties make the combination distinctive; it does not reduce to any single named scheme.

1. **The multiplexed resource is *ordering*, not bandwidth.** Statistical multiplexing shares capacity; the quantum additionally shares *position in the sequence*. The gain of positional multiplexing is not throughput but reduced contention and bounded extraction - a resource classical multiplexing has no name for.
2. **Resolution is a per-reader choice.** In TDM every party reads the same slot grid; here coarse readers resolve coarse cells and fine readers resolve fine ones over one substrate - the scalable/layered-coding principle applied to time (sec. 4.2).

*A caveat that keeps the frame honest.* The three axes are not of the same kind. Time and class structure the *ordering commitment*; the state-access axis structures *which orderings matter* - it is an equivalence (commuting transactions), not a coordinate. "Cube" is a multiplexing lens for locating value, not a claim that all three axes carry ordering semantics.

**Where the value is, read off the axes.** The framework makes the value proposition legible. The **class** axis is where heterogeneous demand is matched to heterogeneous service (RN-04). The **state** axis is where parallelism and throughput are won (the workload-shaping hypothesis: classification increases available parallelism *before* scheduling - see RN-04 sec. 7, and RN-06 for the full Monad analysis). The **time** axis is where extraction is bounded (interior freedom confines reordering within a quantum). A single-service, single-ordered-stream architecture collapses all three axes to one point - the mismatch these notes argue against, now stated as a loss of multiplexing gain on three independent axes.

---

## 4.6 The Boundary Is an Interval: Physical-time Uncertainty and the Resolution-Confidence Tradeoff

sec. 4.3 treated *adversarial* assignment (a provider labelling dishonestly). There is also an *honest* limit: a distributed system has no global wall-clock, so "which quantum did a transaction arrive in?" has no observer-independent answer near a boundary. Two honest observers disagree - Lamport's point that physical simultaneity is not well-defined without agreement.

**The quantum boundary is therefore an interval, not a point,** of width ε ≈ (clock-synchronisation error + arrival jitter). A transaction whose observed arrival lies within ε of a boundary is genuinely ambiguous. This is a floor sec. 4.3 did not name, distinct from both prior floors:

- **consensus-latency floor** (~100ms) - sec. 4.3: does not bind, since quanta carry no consensus status;
- **clock-uncertainty floor (ε)** - governs how *sharp* a boundary can be; below ε a hard boundary is meaningless;
- **commitment/verification-cost floor** - sec. 4.3's answer.

The canonical treatment is Spanner's **TrueTime** (Corbett et al., 2012), which represents time as an interval `[earliest, latest]` with bounded uncertainty and either *waits out* the uncertainty (commit-wait) or accepts a probabilistic guarantee. **The borrowing needs a caveat.** TrueTime's bound is small and, more to the point, *trustworthy* because Google operates GPS receivers and atomic clocks across its own datacentres - a single administrative domain with uniform, audited timing infrastructure. Permissionless validators share none of that. ε is correspondingly larger, harder to bound, and - unlike Spanner's - not verifiable by the parties relying on it, since a validator's claimed clock quality is itself a declaration. The mechanism transfers; the tight, trusted ε does not. This is the same conditions-gap RN-02 sec. 2 identifies in DiffServ, and it is why the centralisation point below bites rather than being incidental. Applied here, two resolutions and a quantifiable tradeoff:

- **Guard band (commit-wait):** defer arrivals within ε of a boundary to the next quantum (or tie-break deterministically) - a *hard* boundary, at the cost of effective resolution bounded near ε.
- **Soft lattice:** accept that the partial order holds with a *stated confidence*; near-boundary order is probabilistic.

For arrivals roughly uniform in a quantum of width Q, the ambiguous fraction is ≈ ε/Q, so **confidence ≈ 1 - ε/Q** - near-certain when Q ≫ ε, collapsing as Q -> ε. *This is a stated modelling assumption, not a law.* Uniform arrivals and a single scalar ε stand in for what are really an arrival-time distribution and a clock-error distribution, and real traffic is bursty rather than uniform - liquidation cascades and oracle updates cluster precisely where boundary ambiguity is most costly. The relation should be read as a first-order dial whose shape a later note should replace with measured distributions. It yields a **trilemma**:

> A quantum cannot be simultaneously **fine**, **hard-bounded**, and **consensus-free**. Consensus buys fine-and-hard, but that is Option C (sec. 5.3) - a shorter slot, excluded. Otherwise: fine-and-soft (probabilistic boundary), or hard-and-coarser (guard band ≈ ε).

**Two mitigations, from the lattice's own structure, confine the damage.** Interior freedom (sec. 4.4) means boundary ambiguity never touches a quantum's interior. And the state-access axis (sec. 4.5) means most boundary ambiguities are *harmless*: transactions on disjoint state commute, so their relative quantum is irrelevant. The confidence problem therefore collapses onto exactly one small set - **conflicting transactions arriving within ε of a boundary** - which is precisely the set a guard band should catch.

**One caveat, connecting to sec. 8.** Reducing ε to allow finer quanta requires better clocks (GPS / PTP / White Rabbit versus NTP), which favours well-resourced operators. Boundary sharpness is thus itself a centralisation vector - the same failure mode as verification-cost-as-a-barrier (sec. 9). Fine quanta cost not only commitment verification but clock precision, and neither is neutral.

---

## 5. Consensus Status: Three Options

The project's operating constraint is to build on Ethereum rather than rebuild it.

### 5.1 Option A - Ordering coordinate with no consensus status

Quanta are a representational convention. Builders and proposers use them to express and honour commitments; consensus is unchanged and unaware.

*Assessment.* Minimal change, no new consensus cost, strictly compatible. Its weakness is credibility: a convention with no protocol status is only as strong as the incentives sustaining it.

### 5.2 Option B - Commitment with post-hoc verification

Quanta remain outside consensus, but commitments are explicit, backed by cost or stake, and verified against realised behaviour.

*Assessment.* Most consistent with the other notes. RN-02 sec. 6 already argues self-declared temporal information is insufficient because a costless declaration is trivially gamed, and that credibility should rest on realised behaviour plus a cost or stake binding making over-claiming self-penalising. Applying this to granularity is a direct extension. It obtains differentiation without paying for sub-slot consensus.

*This note treats Option B as the leading candidate*, noting it inherits RN-02 sec. 6's open questions and lands in territory occupied by preconfirmation research (sec. 7).

### 5.3 Option C - Full consensus on quanta: excluded on structural grounds

Option C is not rejected on a cost judgment. It is excluded because it is **incompatible with the property that makes the quantum useful**.

If quanta carried consensus status, their size would be bounded below by validator-set message latency - the 100+ms floor for geo-distributed consensus, and in Ethereum's case a propagation profile measured near 800ms at p95. **Consensus scale sets a floor; commitment scale does not.** A quantum with consensus status could not be fine, and a quantum that cannot be fine has no advantage over simply shortening the slot.

The reduction is exact: anything validators must agree on, vote over, and resolve disagreement about is *functionally a slot*. A slot containing *n* consensus-bearing quanta is a shorter slot with extra structure, inheriting every objection to shorter slots - tighter deadlines, higher operator requirements, centralisation pressure - and adding new ones.

This matters because a motivating intuition for this note was that granularity might relieve pressure to shorten block time. Option C does the opposite. The quantum is a coarsening device, not a hidden slot-time reduction.

**A committee or pipelined variant sits between A and C, and is not dismissed here.** The three options above are stated as a clean frontier, but intermediate designs exist: a rotating attester sub-committee witnessing arrivals without full validator-set agreement, or a pipelined scheme in which commitment and verification overlap successive quanta. These weaken Option C's latency floor without reaching Option B's pure post-hoc posture, and one of them may well be where an arrival witness (sec. 4.3) comes from. This note does not evaluate them - doing so requires the mechanism analysis it excludes - but the A/B/C partition should be read as three reference points on a frontier, not an exhaustive enumeration.

**The partitioned-state variant** - quantum-level consensus over a subset of state, opaque to slot-level validators - fails for related reasons. State partitioning, not timing, is the binding constraint: a subset stays opaque only while genuinely isolated, and composability makes clean isolation rare. A commitment attested to without evaluation is a trust assumption, creating a smaller committee with authority over valuable state - the concentration risk of sec. 8 in its sharpest form. And slot-level validators are not unaffected: they still bear data propagation and reorg exposure, the constraints that bind small operators.

---

## 6. Competitive Positioning: Equipping Ethereum for Latency-sensitive Applications

A second motivation is competitive rather than defensive.

Applications with acute temporal requirements have increasingly built their own chains. RN-03 documents Hyperliquid: a fully on-chain order book with sustained continuity, partial predictability, acute execution-priority sensitivity, and bursty delay-intolerant events. The chains in sec. 2.3 - Aptos, Sui, Solana, and others - compete explicitly for such workloads on timing characteristics.

Ethereum's available responses have so far been uniform: reduce slot time for everyone, or accept that such applications leave. The strawmap pursues the former toward 2s. Both responses impose one resolution on the entire validator set.

The lattice offers a third: applications obtain fine ordering resolution through a sub-channel *without* requiring every validator to operate at that resolution. Fine granularity becomes available where demanded rather than mandatory everywhere. If viable, this would let Ethereum serve latency-sensitive demand without the decentralisation cost of forcing uniform capability upgrades.

**This argument must not be overstated,** and RN-03 sec. 6 supplies the discipline. Hyperliquid built its own L1, VM, and deterministic sequencing - it took control of the whole execution path, not merely the ability to *describe* its demand. Sovereignty, integrated margin and liquidation logic, and product strategy are confounds. Aptos's sub-10ms intra-namespace figures depend on namespace isolation, an architectural choice unavailable to Ethereum.

The defensible claim is therefore narrow: **the lattice removes one reason to leave, not all of them.** Whether that reason is material relative to the others is an empirical question this note does not resolve.

---

## 7. Relationship to Preconfirmation Research

Preconfirmation research has independently developed sub-slot temporal coordinates. This note therefore **situates itself relative to** that work - acknowledging its priority on sub-slot coordinates, and identifying what a demand-side, supply-architecture framing adds - rather than opposing it.

**Layer and motivation.** Preconfirmations and Primev are **L1-anchored primitives**: commitments about *Ethereum L1* inclusion, ordering, and execution, with **based rollups (L2) a major driving use case** (a based rollup borrows L1 proposers, so without preconfirmations it inherits ~12s latency; preconfirmations are much of what makes it competitive). They are **mechanism-first** - their aim is a *credible guarantee to a user*: fast inclusion, an ordering commitment, MEV monetisation. TLM is **model-first and demand-side** - its aim is to represent the temporal characteristics of demand as an economic object and match them to differentiated supply. The quantum is a provider *capability/coordinate*, not a *guarantee to a user* (sec. 7.1). Where the two converge - sub-slot coordinates, and pricing delay *within* a slot - the convergence is *evidence the demand-side object is real*, not a priority contest.

Preconf transaction designs carry a **target slot** - the latest slot in which a transaction may be included, giving time-bound validity - together with a **target round**, the specific round *within* the target slot by which it must be included. MR-MEV-Boost segments slots into multiple preconfirmation rounds. Primev describes a slot split into a beacon round and an execution round supporting hybrid preconfirmation ratios for fulfillers and deliverers, with beacon-round commitments made by proposers or outsourced and execution-round commitments made by builders.

**Timescales, and a striking convergence.** These systems span a range. MR-MEV-Boost issues preconfirmations in coarse batches, seconds apart. But Primev's **mev-commit** runs a dedicated commitment chain at a **200ms block time - 60 blocks per Ethereum slot** - advertising ~100ms preconfirmed settlement, and Chainbound's **Bolt** offers sub-second proposer commitments. That 200ms / 60-per-slot cadence is *exactly* the granularity RN-04's sub-slot lane contemplates and the fine end of this note's lattice - independent corroboration that sub-100-200ms sub-slot structure is real and useful. One architectural difference matters: mev-commit obtains its 200ms resolution by running a **separate fast chain** (its own consensus) - effectively Option C (sec. 5.3) relocated to a coprocessor - whereas the lattice pursues comparable resolution *without* a separate consensus (Option B: commitment plus post-hoc verification, sec. 5.2). The cadence converges; the substrate does not.

The economics are already temporal. Primev observes that without a time-related mechanism actors can wait until a slot's end and issue a just-in-time preconfirmation to game the system, and proposes rewarding commitments experiencing the least **information decay**, with information decay tracking economic decay to price a commitment. That is a value-versus-delay relationship priced inside a slot.

### 7.1 Where quantum and round differ

| | Preconf **round** | Quantum |
|---|---|---|
| **Form** | Deadline - a round *by which* inclusion must occur | Partition - a lattice inducing partial order over all transactions |
| **Scope** | Per-transaction opt-in; non-preconf transactions unaffected | Structural property of the slot |
| **Nature** | Guarantee made to a user (mechanism-side) | Capability of a provider (supply-side) |
| **Interior** | Unspecified - position within a round has no representation | Explicitly free - interior freedom is definitional |
| **Who sets it** | Mechanism-defined, uniform | Advertised per provider; read at varying depth |

*Terminology note.* This note retains **quantum** rather than adopting *round*. "Round" is overloaded across at least four meanings in adjacent literature - preconf segment, phase-role, BFT consensus step (Minimmit is described as one-round-finality), and cryptographic iteration - which would make sentences such as "round-level consensus" ambiguous precisely where precision is needed. *Quantum* additionally carries the indivisibility connotation sec. 4.1 requires. The choice is not fully settled: "quantum lattice" is defended here against *round*, but not against the quantum-computing misread, and the title remains provisional.

### 7.2 The missing elements

Two elements of the lattice have no counterpart in the round designs surveyed.

**Intra-unit ordering freedom.** Target round is a deadline; it says nothing about position within a round because it does not need to. Deliberate *withholding* of ordering precision as a design feature - coarsening to bound extraction surface and preserve construction flexibility - is absent from the surveyed designs.

**Provider-advertised granularity.** Rounds are uniform and mechanism-defined. Nothing in these designs allows a provider to advertise the resolution it can support, nor participants to read the structure at differing depths. That is the supply-side gap.

### 7.3 What TLM contributes

1. Preconfirmation research arrived at these coordinates **mechanism-first**, to solve inclusion guarantees. TLM asks what demand-side *characteristic* those mechanisms implicitly price, and whether it warrants representation independent of any one mechanism.
2. The information-decay problem is, in the canonical concept note's vocabulary, a **deadline** problem treated as a **decay** problem. Those are two independent parameters, and any representation assuming a single flexibility scalar will misfit deadline-with-cliff demand. Just-in-time gaming is deadline behaviour. Whether separating the parameters sharpens the mechanism is concrete and testable.
3. Preconfirmation work prices delay **within** a slot; EIP-1559 empirical work prices delay **across** slots. No current work unifies them under a single demand-side object. The TEP is a candidate.

Consistent with RN-02 sec. 10's treatment of intents and order-flow auctions, preconfirmation research is **partially competing, not purely complementary**.

---

## 8. The Multi-class Validator Question - and the Evidence Against It

The motivating intuition was that granularity differentiation might let operators of differing capability serve differing demand classes, giving smaller operators a viable role rather than forcing uniform upgrades.

Current evidence runs against this.

**Commitment infrastructure.** The systematisation of ePBS research reports that, with the additions required to maximise a validator's viability in terms of commitment opportunity, home operators may face pressure to join a blockspace negotiation team, while commercial validators may face vendor lock-in with prohibitive migration costs. Commit-Boost exists partly to address fragmentation and excessive client additions arising from commitment infrastructure. The observed effect of commitment-based differentiation to date is *increased* burden on small operators.

**Production time-priority markets.** The Vision Statement records that Arbitrum's Timeboost express lane has been independently analysed as driving spam and centralisation. Foundation Part II sec. 5.5 states the corresponding principle: exposed information must not systematically advantage actors best positioned to forecast or exploit temporal demand.

**Validator-set design.** Ethereum research notes that a capped validator set could simplify faster slot times but might raise the entry threshold for small stakers, while rotating-committee designs allow large-scale participation at the cost of consensus complexity.

**Revenue is not margin.** Tiering may formalise stratification rather than relieve it. If patient, coarse-granularity demand is intrinsically low-margin, a granularity tier is a low-margin tier and small operators are locked into it rather than liberated by it. The claim that differentiation "gives small validators a living" is unsupported unless patient demand can be aggregated into predictable, schedulable volume whose *margin* is competitive.

**The honest formulation:**

> **Under what conditions, if any, does temporal differentiation of execution supply raise the participation floor rather than cap it?**

Candidate conditions worth investigating: whether commitment overhead can be made granularity-proportional, so coarse participation carries correspondingly low operational cost; whether verification of realised behaviour can be made cheap enough not to require specialised infrastructure; and whether aggregated patient demand exhibits competitive margin characteristics. Spire Labs' preconfirmation registry, which explicitly includes solo-stakers alongside large operators in posting collateral, is a relevant data point.

---

## 9. Threat Model

**Misclassification across tiers.** If differentiated classes carry differentiated fees, a provider profiting by misclassifying transactions across tiers breaks the scheme. Under Roughgarden's criteria this is a myopic-miner-incentive-compatibility question; Foundation Part II sec. 8 notes that enlarging the message space can make such guarantees harder to hold jointly.

**Granularity as an extraction signal.** A transaction's declared quantum reveals urgency. Foundation Part II sec. 10 notes that in an adversarial mempool, revealing a temporal characteristic early is what exposes it to extraction.

**Verification cost as a barrier.** If verifying granularity claims requires infrastructure only large operators can run, verification becomes the centralising force - the failure mode RN-02 sec. 2 identifies in DiffServ's dependence on edge policing.

**Quantum-assignment manipulation.** Distinct from - and more dangerous than - over-claiming capability: a provider preserves the published cross-quantum order perfectly while assigning *labels* adversarially, placing a victim's transaction in a later quantum and its own flow in an earlier one. Because it is invisible in the final ordering, post-hoc verification of realised behaviour cannot detect it without an independent arrival witness (sec. 4.3). This is the integrity assumption on which the whole lattice rests, and closing it is the same problem as RN-04's sub-slot-lane sequencing (P1).

**Strategic granularity claims.** Over-claiming fine granularity to capture premium flow, absent a cost binding, is the analogue of DiffServ's mark-bleaching problem.

**Sub-channel capture.** If a fine-granularity sub-channel becomes the venue for most valuable flow, participation in it may concentrate regardless of the lattice's formal openness.

---

## 10. Open Questions

- Is temporal granularity measurable from realised behaviour without self-declaration?
- What determines the quantum's practical lower bound - what are the actual commitment and verification costs?
- Should sub-channels be defined over transactions, providers, or service tiers?
- Does intra-quantum reordering freedom reduce extraction, or relocate it?
- Can a demand-side object unify within-slot and across-slot delay pricing?
- Does separating deadline from decay improve on information-decay pricing in preconfirmation mechanisms?
- Under what conditions does supply differentiation raise rather than cap the participation floor (sec. 8)?
- Is the propagation-versus-arrival gap (sec. 2.2) attributable to strategic timing, and would granularity commitments narrow it?
- How does the lattice interact with proposer lookahead, inclusion lists, and ePBS commitment slots?
- Would a lattice materially affect application chain-choice decisions, given the confounds of sec. 6?

---

## 11. Relationship to TLM

- Foundation Statement - the framework and principles.
- `Temporal-Liquidity` - the umbrella concept and its dimensions.
- RN-01 - transaction-level demand representation (TEP).
- RN-02 - why temporal characteristics should be protocol-visible, and through what representations.
- RN-03 - empirical motivation for multidimensional temporal demand.
- RN-04 - the **service classes** (execution semantics) built *on* the lattice; its sub-slot lane is a sub-channel of this note's lattice (see below).
- RN-05 (this note) - the **supply-side substrate**: temporal granularity, the quantum lattice, and the market-structure question they raise.
- Future mechanism notes - pricing, tier structure, and settlement remain out of scope.

### Services on the substrate: relationship to RN-04

RN-04 and RN-05 are different layers of the supply side, not competing notes. **RN-05 supplies the coordinate substrate** - the lattice on which ordering commitments are expressed (partial order across quanta; readers at varying depth). **RN-04 supplies the execution semantics** - a small portfolio of service classes (Continuous State, Protected Window, Scheduled, Best-Effort) defined over the demand dimensions and layered on that substrate.

```
Temporal Liquidity (demand umbrella)
   -> TEP / TDP           demand representations       (RN-01 / RN-02)
   -> Quantum lattice     supply coordinate system     (RN-05 - this note)
   -> Service classes     execution semantics          (RN-04)
   -> Execution engines   Monad-class, per service
   -> Shared settlement
```

Three consequences make the layers fit precisely:

- **RN-04's sub-slot lane is a sub-channel of this lattice**, read at an (illustrative) 200ms depth, with FIFO purchased as interior semantics. RN-05 supplies the vocabulary that lane's ad-hoc "snapshot" lacked; RN-04 supplies a worked sub-channel with demand mapping and a deployment path. RN-04's fixed 200ms should be read as an *illustration* - chosen to match the Hyperliquid cadence it imports - not a design constant; sec. 4.3 is the reason the number is empirical.
- **Interior freedom is the shared design dial** (sec. 4.4): a class buys as much interior order as it will pay to verify. Protected Window keeps interiors free (batching); Continuous State pays for FIFO order.
- **Option B here (commitment + post-hoc verification, sec. 5.2) is RN-04's deployment-path step 1** (a bonded commitment-market pilot) - the two notes arrived at the same first mechanism independently, which is corroborating.

---

## Summary

If demand is temporally heterogeneous, undifferentiated supply is a mismatch. This note names the supply-side property (temporal granularity), proposes a coordinate system for expressing it (the quantum lattice, with ordering constrained across quanta and priority unsold within), and shows that resolution much finer than block time follows from the lattice's lack of consensus status - bounded below by commitment and verification cost, by clock uncertainty, and by the observability a neutral coordinate requires.

**Scope.** This is an architecture note. It supplies vocabulary and a coordinate system; it proposes no mechanism, prices nothing, and does not attempt the capacity question - what workload is feasible at a given granularity, and how an `N x k` allocation behaves under fixed per-slot work, belong to the capacity theory and the trace-driven simulation, not here. Where this note states a bound it is structural, not measured.

Three concessions are made deliberately. Preconfirmation research reached sub-slot coordinates first; TLM's contribution is the demand-side object beneath them and the two elements their rounds lack (sec. 7.2). The competitive argument removes one reason applications leave Ethereum, not all of them. And the multi-class validator thesis that motivated the note is not supported by current evidence; it is retained as an open question with the contrary evidence stated.

> **Heterogeneous temporal demand raises the question of whether execution supply should be differentiated by temporal granularity. This note supplies the architectural vocabulary - a lattice read at differing depths - and leaves its market-structure consequences open.**

---

## References

- Monnot, B. *EIP-7782: Reduce Block Latency.* https://eips.ethereum.org/EIPS/eip-7782
- Robust Incentives Group. *An analysis of attestation timings in a 6-s slot.* https://rig.ethereum.org/post/an-analysis-of-attestation-timings-in-a-6-s-slot
- Buterin, V. Ethereum strawmap / "fast L1" trajectory and Minimmit finality. (Secondary coverage; primary source to be substituted.)
- *SoK: Current State of Ethereum's Enshrined Proposer Builder Separation.* arXiv:2506.18189
- Primev. *Preconfirmations: The Fulfillment-Delivery Paradigm.* https://mirror.xyz/preconf.eth/sgcuSbd1jgaRXj9odSJW-_OlWIg6jcDREw1hUJnXtgI
- Launchnodes. *Ethereum Pre-Confirmations and Based Rollups Explained.* (Preconf transaction structure; MR-MEV-Boost.)
- Aptos Labs. *Sub-Second Latency: Aptos Delivers Instant Transactions.* (E2E latency vs block time distinction; 100+ms geo-distributed messaging.)
- Aptos. *The New Aptos Tech Stack.* (Block time and finality figures.)
- Chainspect. Layer-1 block time comparison (Figure 1).
- Lamport, L. *Time, Clocks, and the Ordering of Events in a Distributed System.* Communications of the ACM 21(7), 1978. (No global physical time; causal/partial order.)
- Corbett, J. C. et al. *Spanner: Google's Globally-Distributed Database.* OSDI 2012. (TrueTime; time as a bounded interval with commit-wait.)
- TLM Research Program. Foundation Statement Parts I-III; `Temporal-Liquidity`; RN-01; RN-02; RN-03; RN-04 (service classes layered on this note's lattice).

*Citations to be normalised against the project `Related-Work` document.* Three are secondary and are **not to be cited as primary in any published version** until substituted: the **strawmap / Minimmit** trajectory (currently via secondary coverage - substitute Buterin's primary post and the Minimmit paper); **Chainspect's** Layer-1 block-time comparison (Figure 1 - a competitive-positioning artifact whose measured quantity is unlabelled, as sec. 2.3 already cautions; substitute per-chain primary documentation or drop the figure); and the **Hyperliquid** block-time and cadence figures (substitute the protocol documentation cited in RN-03, which carries verification dates). Where a claim in this note rests on one of the three, it should be read as illustrative of a design frontier rather than as a measurement.

---

## Revision Note

*Substantive changes only - claims added, qualified, or withdrawn, so that anyone citing an earlier version can see what has changed. Editorial, formatting, and metadata changes are in the repository history.*

**Version 0.4** (August 24, 2026)

- **Withdraws "arbitrarily fine" (sec. 4.3).** v0.3 concluded the quantum could be arbitrarily fine because it carries no consensus status. It is now stated as *much finer than block time but bounded* - below by commitment and verification cost, by clock uncertainty, and by the propagation and observability a coordinate needs in order to stay neutral rather than becoming a colocation subsidy. The separability of granularity from block time is retained; the unbounded form should not be cited.
- **Justifies "lattice" (sec. 4.2).** Previously asserted. The object is now named: the refinement lattice of partitions of a slot, with meet and join, so readers at different depths occupy points in one lattice.
- **Qualifies the free interior (sec. 4.1).** "Free" means priority is not *sold*, not that order is absent; conflicting transactions are still serialized, and an instantiation must name the intra-quantum rule.
- **Qualifies the confidence relation (sec. 4.6).** `confidence ~ 1 - epsilon/Q` is a modelling assumption under uniform arrivals, not a law, and TrueTime's bounded epsilon rests on single-domain clock infrastructure that permissionless validators do not share.
- **Promotes the composition rule from open question to prerequisite (sec. 4.2).** How commitments from different providers over shared state resolve to one outcome is a precondition on the architecture, not deferred work.

**Version 0.3** (July 23, 2026)

- **Narrows the sec. 4.3 verification result.** Cross-quantum ordering verification is cheap and the fineness argument rests only on that; *quantum-assignment* integrity is a separate unsolved arrival-witness problem. Earlier versions did not separate the two.
- **Qualifies interior freedom (sec. 4.4).** Constraining a quantum's interior re-imports verification cost, so fineness and interior freedom are two faces of one property.
- **Adds the clock-uncertainty floor (sec. 4.6).** The quantum boundary is an interval of width epsilon, not a point, giving a resolution-confidence tradeoff and the fine / hard-bounded / consensus-free trilemma.

**Version 0.2**

- **Withdraws any specified quantum size.** Replaced by the structural result that commitment scale is not floor-limited by consensus latency.
- **Re-grounds the rejection of Option C** on that structural result - consensus status is incompatible with fineness - rather than on a cost judgment.
- **Corrects the slot-time framing (sec. 2.1).** The EF strawmap contemplates 2s slots; this note does not claim to stop slot-time reduction.
- **Introduces the lattice framing** (sec. 4.2), replacing granularity-as-provider-property alone.
