# Toward a Mathematical Theory of Execution Capacity

## Multi-User Demand, Temporal Resolution, Information, and Fundamental Limits

**Draft v0.5 — August 2026**  
**Research Note:** RN-13  
**Status:** Working Draft

---

## Abstract

Execution systems appear throughout computer science. Operating systems schedule processes, communication networks allocate bandwidth, cloud platforms assign compute resources, GPU runtimes schedule kernels, and blockchains order and execute transactions. Although these systems differ substantially in implementation, they share a common purpose: they transform potential demand into realized execution under constraints.

This paper proposes that execution systems should be studied not only as resource-allocation systems, but also as **information-processing, capacity-limited, and market-coordination systems**. The central question is no longer only how a scheduler allocates a fixed set of requests. It is also what execution is fundamentally achievable, what information is needed to approach that limit, and how protocol-defined temporal resolution affects the capacity that can actually be exposed to heterogeneous demand.

Claude Shannon's information theory supplies the methodological starting point: define a constrained system, characterize a fundamental achievable limit, and evaluate particular mechanisms relative to that limit. Wireless communication theory extends this perspective to time-varying and multi-user environments. Goldsmith and Varaiya show that channel-state information and adaptation can change the capacity of fading channels. Tse and Hanly characterize multi-user throughput and delay-limited capacity regions under dynamic resource allocation. Statistical multiplexing and effective-bandwidth theory further show how heterogeneous stochastic streams can be supported by exploiting variation over time rather than provisioning every source independently.

These ideas motivate an analogous execution-capacity problem. On the **supply side**, an execution system exposes a set of feasible execution opportunities across time. For blockchain, this paper proposes an **execution lattice** that discretizes those opportunities at temporal resolution \(\delta\). On the **demand side**, multiple users or streams possess heterogeneous temporal requirements, including intensity, duration, deadlines, persistence, predictability, and execution flexibility. The scheduler must match these two sides using only the information made visible through the protocol.

We therefore propose a candidate family of capacity objects

\[
\mathcal{C}(\delta, I, \epsilon),
\]

where \(\delta\) is supply-side temporal resolution, \(I\) represents execution-relevant demand information available to the scheduler, and \(\epsilon\) represents allowed service or deadline violation. The ideal capacity frontier is defined independently of any particular mechanism. Existing spot fee markets, richer temporal-information interfaces, and programmable execution schedulers may then be compared by how closely they approach that frontier.

The paper retains an information-market perspective but changes its center of gravity. Shannon-style **capacity** becomes the primary organizing principle. Yao's communication complexity becomes a secondary tool for asking how much information must be communicated to approach a desired fraction of the capacity frontier. Kelly's network utility framework remains important for connecting capacity constraints, prices, user utility, and decentralized feedback.

The objective is not to claim that blockchain execution is mathematically identical to a communication channel. It is to develop a research program for the **fundamental limits of shared execution under heterogeneous temporal demand**.

---

## 1. Introduction

Execution systems are ubiquitous.

Examples include:

- operating systems;
- packet and flow schedulers;
- software-defined networks;
- wireless multiple-access systems;
- cloud and cluster schedulers;
- distributed databases;
- GPU runtimes;
- manufacturing and transportation systems;
- blockchain execution engines.

Each system receives requests over time and allocates finite resources. Traditional research examines algorithms, queueing, computational complexity, scheduling policy, control, resource allocation, and mechanism design. These perspectives are indispensable, but they often begin after the system architecture and the observable request format have already been fixed.

This paper asks a more foundational question:

> **What is fundamentally achievable by an execution system under its physical resource constraints, temporal resolution, information interface, and heterogeneous demand?**

This question has a direct precedent in communication theory. Shannon did not begin by asking whether one specific coding scheme was best. He defined a channel and asked for the maximum reliable communication rate achievable by any admissible coding strategy. Later wireless theory extended this methodology to fading channels, multiple users, dynamic allocation, side information, delay constraints, and outage.

The analogous execution-system program is:

```text
Physical and Computational Resource Limits
                    ↓
       Feasible Execution Opportunities
                    ↓
      Fundamental Capacity Region
                    ↓
      Information Available to Scheduler
                    ↓
      Protocol / Market / Scheduler
                    ↓
          Realized Execution
```

A particular mechanism should therefore be evaluated against a capacity benchmark that does not presuppose that mechanism.

This is especially relevant to blockchain systems. Public discussion often compares systems by transactions per second, block time, gas per second, or benchmark throughput. These are useful engineering metrics, but they do not answer a deeper question:

> **How much heterogeneous, time-sensitive execution demand can a shared blockchain execution substrate support, and how much capacity is lost because demand and supply are represented too coarsely?**

This paper develops a conceptual framework for asking that question.

---

## 2. Execution Systems

We define an **execution system** as:

> A system that transforms potential demand into realized execution under informational, economic, computational, temporal, and resource constraints.

An execution system contains at least:

- participants generating demand;
- finite execution resources;
- a temporal structure of resource availability;
- an information interface;
- participation and admission rules;
- a price or priority mechanism;
- a scheduling policy;
- an execution engine;
- observable outcomes and feedback.

A simple representation is:

```text
Demand
  ↓
Execution Architecture
  ↓
Execution Outcome
```

But this hides two important facts.

First, supply is not necessarily an undifferentiated scalar. Execution opportunities occur at particular times, on particular resources, and under particular dependency and consistency constraints.

Second, demand is not fixed. Protocol rules, prices, delay, uncertainty, and available execution choices influence whether and when potential demand becomes effective demand.

A more complete architecture is:

```text
Potential Demand
       ↓
Information / Participation Interface
       ↓
Submitted Demand
       ↓
Admission and Market Rules
       ↓
Scheduler
       ↕
Execution Opportunity Set
       ↓
Realized Execution
       ↓
Price, Delay, Utilization, Failure, Feedback
       ↓
Participant and Protocol Adaptation
       ↺
```

This is simultaneously a resource-allocation system, an information system, a market institution, and a feedback-control system.

---

## 3. Demand Is Endogenous

### 3.1 Potential and effective demand

We distinguish:

- **Potential demand**: work participants would generate under some feasible price and service conditions;
- **Submitted demand**: work actually communicated to the system;
- **Admitted demand**: submitted work accepted for allocation;
- **Scheduled demand**: admitted work assigned execution opportunities;
- **Executed demand**: scheduled work that completes under the execution rules.

Symbolically,

\[
D^{P}
\rightarrow
D^{S}
\rightarrow
D^{A}
\rightarrow
D^{Q}
\rightarrow
D^{E}.
\]

These transformations depend on the architecture.

A service may never appear as submitted demand because:

- execution price exceeds its unit economics;
- expected delay destroys its value;
- service variance is too high;
- the protocol cannot express its execution requirements;
- it migrates to another execution platform;
- it builds a specialized execution environment instead.

Observed blockchain demand is therefore not the full demand that could potentially use the infrastructure.

### 3.2 Price exclusion and latency exclusion

Two conceptually distinct forms of exclusion are especially important.

A request may be **price excluded** if

\[
V_i < P_i,
\]

where \(V_i\) is the economic value of execution and \(P_i\) is the required execution cost.

A request may be **latency excluded** if

\[
D_i^{\max} < D_i^{\text{achievable}},
\]

where \(D_i^{\max}\) is the maximum acceptable delay.

A system may therefore have substantial nominal throughput while failing to support important application classes.

This motivates a capacity concept richer than transactions per second.

---

## 4. Three Levels of Uncertainty

We distinguish three levels of uncertainty.

### 4.1 Demand uncertainty

**Demand uncertainty** concerns the latent workload itself:

- arrival uncertainty;
- quantity uncertainty;
- temporal-preference uncertainty;
- persistence uncertainty;
- value uncertainty;
- strategic-response uncertainty.

### 4.2 Scheduler uncertainty

**Scheduler uncertainty** concerns what the execution architecture does not know at allocation time.

It depends on:

- protocol-visible information;
- participant disclosure;
- prediction quality;
- observability;
- reporting delay;
- strategic misreporting;
- scheduling horizon.

Two systems facing similar latent demand may have very different scheduler uncertainty.

### 4.3 Execution uncertainty

**Execution uncertainty** concerns realized service:

- waiting time;
- completion time;
- jitter;
- deadline violation;
- rejection;
- queue growth;
- utilization;
- execution failure.

These quantities must remain distinct. Richer demand information may reduce scheduler uncertainty without changing demand uncertainty. Better scheduling may reduce execution uncertainty without increasing physical resources.

---

# Methodological Spine — Capacity Before Mechanism

The central commitment of this paper is to define **execution capability before execution mechanism**.

The inspiration from Shannon is methodological rather than literal. An execution system is not assumed to be a communication channel, and Shannon's communication-capacity formula is not transplanted into blockchain. Instead, we adopt the architecture of inquiry that made communication theory foundational:

```text
Primitive physical system
        ↓
Feasible execution trajectories
        ↓
Heterogeneous multi-user service requirements
        ↓
Fundamental execution-capacity region
        ↓
Restrictions from temporal representation and information
        ↓
Scheduling / pricing / market mechanisms
        ↓
Realized capacity and distance from the frontier
```

The first question is therefore not which fee mechanism or scheduler should be used. It is:

> **Given a shared execution substrate and stated physical constraints, what set of heterogeneous execution services is fundamentally supportable?**

Only after that limit is defined should particular mechanisms be introduced.

## A. Primitive physical capability

The substrate is characterized by constraints that mechanism design cannot simply wish away:

- finite computation;
- memory and state-access capability;
- dependency and conflict structure;
- communication bandwidth and propagation;
- synchronization and commitment requirements;
- consensus and security constraints where applicable;
- realizable parallelism;
- physical time.

These constraints define the underlying physical capability.

## B. Feasible execution trajectories

From the primitive substrate we define the set of execution histories that are physically and logically realizable over a horizon. The temporal execution lattice is one representation of these opportunities.

Its quantum \(\delta\) is not assumed to equal block or consensus slot time. The relationship among physical execution time, lattice quantum, commitment time, and consensus time is itself part of the theory.

## C. Heterogeneous multi-user demand

Users and services are not modeled as identical transactions. Persistent streams may differ in:

- duration and persistence;
- execution intensity;
- required inter-execution cadence;
- deadline;
- cadence and delay jitter;
- temporal flexibility;
- reliability requirement;
- economic value.

The fundamental capacity problem is therefore multi-user and temporal.

## D. Fundamental execution-capacity region

The primary object is the set of workload vectors for which **some admissible execution strategy exists** satisfying all stated service requirements under the primitive physical constraints.

This capacity region is defined before:

- EIP-1559;
- PBS;
- TLM;
- EDF or other schedulers;
- auctions;
- queues;
- priority policies;
- application-specific execution mechanisms.

These mechanisms are constructions that may approach, or fail to approach, the fundamental region.

## E. Restricted capability

Practical systems expose only a subset of fundamental capability because of:

- coarse temporal resolution;
- incomplete demand information;
- online rather than clairvoyant allocation;
- strategic behavior;
- verification constraints;
- computationally bounded scheduling;
- protocol overhead;
- decentralization requirements.

This motivates restricted regions such as

\[
\mathcal{C}(\delta,I,\epsilon),
\]

but these are downstream of the more primitive physical execution-capacity region.

## F. Three capability layers

For blockchain applications we distinguish:

\[
\boxed{\text{Physical capability}}
\]

\[
\downarrow
\]

\[
\boxed{\text{Execution-service capability}}
\]

\[
\downarrow
\]

\[
\boxed{\text{Market/protocol capability}}.
\]

**Physical capability** is imposed by computation, state, communication, synchronization, and consensus.

**Execution-service capability** asks which heterogeneous temporal services can be realized on that substrate.

**Market/protocol capability** asks which portion of that service region a concrete information, pricing, and scheduling architecture actually exposes.

The first two form the standalone mathematical theory. TLM belongs primarily to the third layer.

## G. Criterion for a useful theory

The capacity bound must be independent enough to reject as well as support a proposed mechanism.

A TLM scheduler, an Ethereum fee market, a Hyperliquid-like architecture, or another design may:

- approach the frontier;
- recover only a small fraction of the available gap;
- help only particular service classes;
- incur overhead greater than its scheduling gain;
- or provide no capacity gain.

A first-principles theory must permit all of these outcomes.

---

# Physical Geography, Speed-of-Light Bounds, and Decoupled Time Scales

A globally decentralized execution system ultimately operates on a finite planet under finite signal propagation speed. This places a hard lower bound on how quickly geographically separated participants can exchange causally relevant information.

Let

\[
c
\]

denote the speed of light and let

\[
d_{ij}
\]

denote physical distance between participating nodes \(i\) and \(j\). Even before router, fiber-path, queueing, serialization, processing, cryptographic, and protocol overheads, one-way propagation obeys the physical lower bound

\[
T_{ij}^{\mathrm{prop}}
\ge
\frac{d_{ij}}{c}.
\]

For a globally distributed validator set, Earth's finite diameter therefore enters the primitive physical model indirectly through the maximum and distribution of inter-node distances.

A more realistic network propagation term is

\[
T_{ij}^{\mathrm{net}}
=
T_{ij}^{\mathrm{prop}}
+
T_{ij}^{\mathrm{serialization}}
+
T_{ij}^{\mathrm{queue}}
+
T_{ij}^{\mathrm{processing}}
+
T_{ij}^{\mathrm{protocol}}.
\]

The speed-of-light term cannot be removed by software optimization. The other terms can potentially be reduced.

This distinction should be preserved in any physical execution model.

## Global consensus time

Consensus requires enough information to move among a sufficiently large and appropriately distributed set of participants to establish agreement, finality, or another protocol-defined notion of commitment.

Therefore, the minimum achievable consensus time is constrained by:

- physical node geography;
- speed of signal propagation;
- network bandwidth;
- topology;
- cryptographic verification;
- quorum structure;
- adversarial and security assumptions;
- protocol rounds.

A global consensus interval cannot be treated as an arbitrary engineering constant.

In an idealized model, one may write

\[
\Delta_{\mathrm{consensus}}
\ge
F_{\mathrm{consensus}}
\left(
\{d_{ij}\},
c,
C_N,
Q,
R,
S
\right),
\]

where \(C_N\) denotes communication capacity, \(Q\) quorum structure, \(R\) protocol round structure, and \(S\) the security assumptions.

The exact function is protocol-specific. The important theoretical point is that a globally decentralized consensus cadence is lower-bounded by physical communication constraints.

## Execution state can face the same physical limits

Execution is often treated as local computation, but distributed execution state can also become communication-limited.

If a state transition must be globally observed before another dependent transition can proceed, then state propagation itself introduces a physical lower bound.

For state transition \(k\),

\[
S_k
\rightarrow
S_{k+1},
\]

the minimum interval between globally dependent state transitions may include:

\[
T_{\mathrm{state}}
\ge
T_{\mathrm{execute}}
+
T_{\mathrm{state\ dissemination}}
+
T_{\mathrm{verification}}.
\]

Thus, even if CPU execution is extremely fast, globally visible serial state transitions can remain bounded by communication and propagation.

This is especially important for high-frequency shared-state services such as order books, auctions, and tightly coupled financial applications.

## Decoupling consensus, ordering, and execution

The physical bound does not imply that every useful execution event must wait for global consensus.

A central architectural question is whether three time scales can be separated:

\[
\boxed{
\text{Consensus Time}
}
\]

\[
\boxed{
\text{Execution-Ordering Time}
}
\]

\[
\boxed{
\text{Actual Execution Time}
}
\]

These need not be identical.

### 1. Consensus time

Consensus determines agreement over some global object: a block, commitment, ordering checkpoint, state root, or other protocol-level artifact.

### 2. Execution-ordering time

Execution ordering determines the logical order among operations.

An ordering decision may potentially be produced at a finer time scale than final global consensus if the architecture permits provisional or locally verifiable ordering that is later committed.

### 3. Actual execution time

Once dependencies and ordering constraints are known sufficiently for a particular operation, physical computation may occur at an even finer time scale.

This suggests the possibility of:

\[
\delta_{\mathrm{exec}}
\le
\delta_{\mathrm{order}}
\le
\Delta_{\mathrm{consensus}},
\]

where:

- \(\delta_{\mathrm{exec}}\) is the finest useful actual execution cadence;
- \(\delta_{\mathrm{order}}\) is the finest useful logical ordering cadence;
- \(\Delta_{\mathrm{consensus}}\) is the global consensus or commitment cadence.

The inequalities need not always be strict, but the theory should not assume equality.

## Why the decoupling matters for capacity

If every execution event requires independent global consensus, then global propagation delay directly limits service cadence.

If execution ordering can be determined more frequently than consensus, and actual execution can proceed more frequently still, then a shared execution system may expose substantially more temporal service capacity without shortening the global consensus interval.

This creates a new research question:

> **What execution capacity can be gained by decoupling the cadence of consensus, logical ordering, and actual execution, while preserving a globally verifiable commitment structure?**

This question belongs to the physical-capability layer rather than to any one market mechanism.

It also provides a sharper interpretation of the execution lattice:

- the lattice quantum need not equal the consensus slot;
- the lattice quantum may instead reflect the finest economically meaningful and physically realizable execution or ordering opportunity;
- consensus may periodically commit a sequence of finer-grained lattice events.

## A candidate hierarchy of time scales

A future formal model should distinguish at least:

\[
\delta_{\mathrm{CPU}}
\]

local compute instruction or execution-engine time scale;

\[
\delta_{\mathrm{exec}}
\]

useful application-visible execution-state transition time scale;

\[
\delta_{\mathrm{order}}
\]

logical ordering time scale;

\[
\Delta_{\mathrm{commit}}
\]

state commitment or checkpoint time scale;

\[
\Delta_{\mathrm{consensus}}
\]

global consensus or finality time scale.

A conventional blockchain may collapse several of these into one block interval.

A more expressive architecture may separate them.

The capacity theory should therefore ask not only

\[
C(\delta),
\]

but eventually

\[
\mathcal{C}
\left(
\delta_{\mathrm{exec}},
\delta_{\mathrm{order}},
\Delta_{\mathrm{commit}},
\Delta_{\mathrm{consensus}},
I,
\epsilon
\right).
\]

This is not yet proposed as the final capacity formula. It is a reminder that the system may possess multiple distinct temporal bottlenecks.

## Physical-law interpretation

The primitive physical model should distinguish:

1. **Irreducible physical bounds**, such as signal propagation limited by geography and the speed of light.
2. **Hardware/resource bounds**, such as compute, memory bandwidth, state access, and communication bandwidth.
3. **Protocol-induced bounds**, such as consensus rounds, block intervals, ordering rules, and commitment frequency.
4. **Architecture-induced coupling**, where several independent physical processes are unnecessarily forced to operate at the same cadence.

One of the most important tasks of execution-capacity theory may be to identify which observed blockchain limits belong to each category.

Only the first category is fundamentally irreducible.

The others may be improved through engineering, protocol design, or architectural decoupling.

---

# Part I — Fundamental Capacity

## 5. Shannon's Methodological Lesson

Claude Shannon's *A Mathematical Theory of Communication* established a theory of reliable communication under constrained channels. The importance of Shannon's work for this paper is not that an execution system is literally a noisy communication channel.

The important methodological lesson is:

> **Separate the fundamental achievable limit from the engineering mechanism used to approach it.**

In communication theory, one first defines the channel and its constraints. Capacity is then an upper bound over all admissible strategies. Particular coding, modulation, access, and scheduling schemes can be compared against that bound.

For execution systems, the analogous program is:

1. define physical and logical execution constraints;
2. define the set of feasible execution schedules;
3. define heterogeneous demand and service requirements;
4. characterize an achievable execution-capacity region;
5. impose information restrictions;
6. compare particular protocol and scheduling mechanisms against the resulting frontier.

This changes the research question from

> "Does mechanism \(M\) improve throughput?"

to

> **"How much of the fundamentally achievable execution region does mechanism \(M\) expose?"**

That distinction is central.

---

## 6. Capacity Is Not TPS

Transactions per second is an implementation-dependent metric. Transaction sizes differ. Computation differs. State access differs. Dependencies differ. Temporal requirements differ.

A more fundamental object is the set of workloads that can be supported while satisfying specified service constraints.

Suppose there are \(n\) execution streams with offered load vector

\[
\boldsymbol{\lambda}
=
(\lambda_1,\lambda_2,\ldots,\lambda_n).
\]

Define a capacity region

\[
\mathcal{C}
=
\left\{
\boldsymbol{\lambda} :
\text{there exists a feasible scheduling policy satisfying the service constraints}
\right\}.
\]

A system may support high aggregate throughput but possess a small capacity region for low-latency workloads. Another may support lower peak throughput but efficiently multiplex heterogeneous delay-tolerant streams.

Thus, a single scalar capacity is often insufficient.

---

## 7. Supply-Side Execution Lattice

### 7.1 Why a lattice

To define a supply-side capacity bound, execution opportunities need a representation independent of the scheduler.

We propose an **execution lattice**. This is the supply-side quantum lattice of **RN-05**, imported here as the capacity substrate; RN-05 develops the finest-resolution argument (the quantum bounded by commitment and verification cost rather than consensus latency) that this note takes as given.

Let \(\delta\) denote the temporal quantum. Over horizon \(T\),

\[
q = 0,1,\ldots,Q-1,
\qquad
Q = T/\delta.
\]

At each quantum \(q\), the system exposes some feasible execution resource set \(K_q\). A simple scalar version might use

\[
K_q = \text{execution units available in quantum } q.
\]

A richer lattice may include:

- temporal position;
- computational capacity;
- state-access constraints;
- parallel execution lanes;
- dependency constraints;
- service classes;
- reserved or precommitted capacity.

The lattice is a **supply-side model**. It should not encode a particular fee mechanism or scheduler.

### 7.2 Feasible schedules

Let

\[
\Omega(T,\delta)
\]

denote all physically and logically feasible execution schedules over horizon \(T\) at temporal resolution \(\delta\).

The set \(\Omega\) incorporates constraints such as:

- total computation;
- state conflicts;
- precedence;
- validator processing limits;
- propagation and synchronization requirements;
- consensus-imposed timing;
- execution-engine parallelism.

The scheduler selects

\[
S \in \Omega(T,\delta).
\]

The existence of this schedule space allows a mechanism-independent upper-bound problem to be stated.

### 7.3 A schedule-richness diagnostic (not a capacity)

A purely supply-side quantity might examine the growth in distinguishable feasible schedules:

\[
C_L(\delta)
=
\limsup_{T\to\infty}
\frac{1}{T}
\log_2 |\Omega(T,\delta)|.
\]

This quantity is **not** a capacity and should not be read as one. It has no demand or welfare content; it grows without bound as \(\delta\to 0\) unless the resolution-dependent capacity \(K(\delta)\) of \S8.4 constrains \(|\Omega|\); and its value depends on how schedules are individuated. It is at most a *diagnostic of the substrate's expressive richness* — the analogue of a zero-error counting capacity for a channel that has not yet been given a notion of message. The economically meaningful objects are the oracle welfare \(W^{*}\) (\S31) and the service region \(\mathcal{C}(\delta,I,\epsilon)\) (\S34), which carry demand and value; \(C_L\) is retained only to make explicit that lattice richness alone is not capacity.

The main value of the lattice is therefore not the expression above. It is that it gives the supply side an explicit state space against which heterogeneous demand can be matched.

---

## 8. Slot Granularity and Temporal Resolution

### 8.1 Slot-only execution as coarse quantization

Many blockchains expose execution at block or slot granularity. If a slot of duration \(\Delta\) is treated as the indivisible scheduling unit, then

\[
\delta = \Delta.
\]

Execution opportunities inside the interval are collapsed into a single temporal coordinate.

This may produce **temporal discretization loss**. Demand that differs meaningfully at sub-slot time scales cannot be separately matched to supply if the protocol's scheduling abstraction cannot represent those differences.

### 8.2 Quantum subdivision

Suppose each slot is divided into \(m\) temporal quanta:

\[
\delta = \frac{\Delta}{m}.
\]

If subdivision does not reduce physical execution capability, the feasible scheduling set should weakly expand as temporal resolution becomes finer:

\[
\mathcal{C}(\Delta)
\subseteq
\mathcal{C}(\Delta/2)
\subseteq
\mathcal{C}(\Delta/4)
\subseteq \cdots.
\]

This motivates the idealized limit

\[
\mathcal{C}^{*}
=
\lim_{\delta\rightarrow 0}
\mathcal{C}(\delta),
\]

subject to the underlying physical and consistency constraints.

**Scope of the inclusion.** This monotonicity is a *relaxation* argument and holds cleanly only for the **divisible** capacity program (the program of \S31 relaxed to \(x_{ijq}\in[0,1]\)) at **fixed per-horizon physical capacity**: there, any coarse-feasible allocation maps to a fine-feasible one of equal value, and finer placement can only help. It is **not** automatic for the indivisible program of \S31 once per-quantum capacity depends on resolution, \(K=K(\delta)\) (\S8.4): a job whose requirement \(g_{ij}\) fits a coarse quantum may fit no single finer quantum, so it can leave the feasible set and the inclusion can reverse. The indivisible claim therefore requires either (i) jobs that may occupy a contiguous run of fine quanta (multi-quantum execution), or (ii) restriction to the fixed-\(K\) divisible relaxation. Hypothesis H2 and \S33 are stated under this scope.

### 8.3 Resolution loss and recovered capacity

Let \(M(\mathcal{C})\) be an appropriate scalar functional of a capacity region: volume, weighted welfare, supported workload, or another measure.

Then define temporal discretization loss as

\[
L_{\mathrm{resolution}}(\delta)
=
M(\mathcal{C}^{*}) - M(\mathcal{C}(\delta)).
\]

For a slot-level system,

\[
L_{\mathrm{slot}}
=
M(\mathcal{C}^{*}) - M(\mathcal{C}(\Delta)).
\]

Capacity recovered by introducing \(m\) quanta per slot is

\[
G(m)
=
M(\mathcal{C}(\Delta/m))
-
M(\mathcal{C}(\Delta)).
\]

This gives temporal quantum size a theoretical role. The question is no longer merely whether smaller scheduling intervals feel "faster." It becomes:

> **How much execution capacity is recovered as temporal resolution becomes finer?**

### 8.4 Finer quanta are not free

A real implementation may incur overhead as \(\delta\) decreases:

- more scheduling decisions;
- more state synchronization;
- larger metadata or commitment load;
- greater coordination pressure;
- increased validator complexity;
- higher communication overhead.

Hence physical effective capacity may itself depend on temporal resolution:

\[
K = K(\delta).
\]

The practically optimal resolution may therefore satisfy

\[
\delta^{*}
=
\arg\max_{\delta}
M\bigl(\mathcal{C}(\delta;K(\delta))\bigr).
\]

The theory should therefore search for an **economically and physically meaningful scheduling scale**, not assume arbitrarily small quanta are optimal.

---

# Part II — Lessons from Wireless Capacity Theory

## 9. From Shannon to Time-Varying Wireless Channels

Wireless channels vary over time. Their quality depends on fading, interference, mobility, and other physical conditions.

This forced communication theory to move beyond a static single-user capacity number.

Two developments are particularly relevant to execution systems:

1. **channel side information and adaptation**;
2. **multi-user capacity and opportunistic scheduling**.

The execution-system analogue is not exact. Wireless variation often occurs on the supply side because channel quality changes. Temporal execution markets may instead obtain much of their gain from variation and flexibility on the demand side. But both systems confront the same abstract problem:

> A shared resource changes in usefulness across time, and scheduling quality depends on what state information is available when allocation decisions are made.

---

## 10. Goldsmith and Varaiya: Capacity with Side Information

Goldsmith and Varaiya study the capacity of fading channels when channel-state information is available at the receiver alone or at both transmitter and receiver.

The important lesson for execution theory is:

> **The physical channel can remain unchanged while achievable capacity changes because the allocator has more useful state information and can adapt its actions over time.**

In their model, power and rate can be adapted to channel conditions. The optimal allocation exploits favorable temporal states rather than treating every state identically.

For execution systems, the analogous research question is:

> **Can a fixed physical execution substrate support more economically useful demand when the scheduler observes richer temporal state information?**

This suggests separating:

\[
\text{physical execution resources}
\]

from

\[
\text{information-conditioned achievable capacity}.
\]

The same hardware may expose different effective capacity depending on the scheduler's information set.

### 10.1 Demand-side rather than channel-side information

For blockchain, a natural state variable is not only the condition of the execution engine. It is the hidden temporal state of demand.

Users may know:

- whether execution must be immediate;
- whether it can move across future intervals;
- expected continuation of a stream;
- expected intensity;
- deadlines;
- acceptable jitter;
- value decay;
- burst limits;
- predictability.

We therefore introduce the generic term **execution-relevant demand information**.

Let \(D\) denote the true latent temporal state of demand and let

\[
X = f(D)
\]

be the representation communicated through the protocol.

The scheduler observes \(X\), not \(D\) directly.

This creates an execution analogue of capacity with side information.

---

## 11. Tse and Hanly: Multi-User Capacity Regions

Tse and Hanly study multiaccess fading channels in which multiple users share a time-varying communication resource. They define a **throughput capacity region** containing simultaneously achievable long-run user rates and analyze optimal dynamic resource allocation.

This is more relevant to execution systems than a single-user Shannon formula.

A blockchain or shared execution platform serves many heterogeneous users and streams simultaneously. A candidate execution capacity object is therefore

\[
\mathcal{C}
=
\left\{
(\lambda_1,\ldots,\lambda_n)
:
\text{jointly supportable under service constraints}
\right\}.
\]

The important analogy is not "transaction = wireless packet." The deeper analogy is:

```text
Wireless multi-user system        Shared execution system
--------------------------        -----------------------
multiple users                    multiple demand streams
time-varying channel states       time-varying execution opportunities
channel-state information         execution/demand state information
dynamic rate/power allocation     dynamic execution allocation
capacity region                   execution capacity region
delay-sensitive traffic           deadline/latency-sensitive execution
```

This encourages a capacity-region approach rather than a TPS benchmark.

---

## 12. Opportunistic Scheduling and Temporal Liquidity

Wireless multi-user systems can obtain **multiuser diversity** by serving users when their channels are favorable.

Execution systems may possess a dual opportunity.

A transaction stream may have multiple acceptable execution times. If the scheduler knows those feasible times, it can place flexible demand where supply is less scarce and preserve scarce near-term capacity for delay-intolerant demand.

Suppose request \(i\) has feasible execution set

\[
F_i
\subseteq
\{q_1,\ldots,q_Q\}.
\]

A delay-intolerant request might have

\[
|F_i| = 1,
\]

while a highly flexible request may have

\[
|F_i| \gg 1.
\]

This gives a concrete interpretation of temporal flexibility:

> **Temporal flexibility expands the set of supply-side lattice positions to which a unit of demand may be feasibly mapped.**

This is a central matching insight.

Wireless opportunism primarily exploits favorable **supply states**. Temporal execution scheduling may primarily exploit flexible **demand states**. The optimization structures may nevertheless be closely related.

---

## 13. Scheduling Scale and a Demand Coherence Time

Wireless adaptation is valuable only if the system reacts on a time scale appropriate to the variation of the channel. If adaptation is much slower than channel variation, useful state is averaged away. If it is much faster than relevant variation, additional adaptation may add complexity with little benefit.

This suggests an execution analogue.

Let

\[
\tau_D
\]

denote a characteristic time scale over which the economically relevant temporal state of a demand stream changes materially. In operational form, \(\tau_D\) is a specified statistic of the demand profile \(\theta_i\): for a stream, the autocorrelation time of its arrival/intensity process \(a_i\); for value-decaying work, the half-life of \(v_i(t)\); for a cadence-bound service, its required inter-execution interval \(\tau_i^{\mathrm{req}}\). These need not coincide, and which one governs the relevant regime is itself an empirical question; the ratio below should be computed against whichever statistic the workload's binding constraint selects.

Let

\[
\delta
\]

be the execution-lattice quantum.

Define the dimensionless ratio

\[
\rho
=
\frac{\delta}{\tau_D}.
\]

Candidate regimes are:

### Coarse regime

\[
\rho \gg 1.
\]

The lattice is too coarse to resolve meaningful temporal demand variation. Capacity may be stranded because distinct temporal opportunities are collapsed.

### Matched regime

\[
\rho \approx 1.
\]

Scheduling resolution is of the same order as economically meaningful demand variation.

### Oversampled regime

\[
\rho \ll 1.
\]

Further resolution may provide diminishing capacity gain while increasing implementation overhead.

This is only a proposed analogy. It should be tested rather than assumed. But it offers a principled research path for selecting blockchain scheduling quantum size.

---

## 14. Throughput, Delay-Limited, and Outage-Like Capacity

Wireless theory distinguishes different capacity concepts depending on service constraints.

Execution theory may need the same discipline.

### 14.1 Throughput capacity

\[
\mathcal{C}_{\mathrm{throughput}}
\]

contains workloads supportable in a long-run average sense.

### 14.2 Delay-limited capacity

\[
\mathcal{C}_{\mathrm{delay}}
\]

contains workloads supportable while satisfying deterministic or strict delay requirements.

### 14.3 Probabilistic service capacity

For demand class \(i\), let \(D_i\) be execution delay and \(d_i\) its service deadline. Impose

\[
\Pr(D_i > d_i) \leq \epsilon_i.
\]

Then

\[
\mathcal{C}_{\epsilon}
\]

is the capacity region under permitted service-violation probabilities.

This is potentially more realistic than requiring either perfect guarantees or pure best effort.

A high-frequency liquidation service and a background settlement stream may occupy the same execution substrate while requiring very different \(\epsilon_i\), delay, and value profiles.

---

## 15. Statistical Multiplexing and Multiple Time Scales

Wireless capacity theory is not the only relevant communication-network lineage.

Tse, Gallager, and Tsitsiklis studied **statistical multiplexing of multiple time-scale Markov streams**. Effective-bandwidth theory and later network-calculus approaches similarly ask how stochastic traffic sources with heterogeneous temporal structure can share finite capacity while satisfying service constraints.

This literature matters because execution demand is often stream-like rather than transaction-like.

A persistent execution stream may have:

- long duration;
- stable mean intensity;
- bursts at shorter time scales;
- predictable periodic structure;
- low or high deadline tolerance;
- correlated arrivals.

The scheduler can potentially exploit statistical multiplexing across streams rather than provisioning each stream for its peak demand.

This is directly related to the broader Temporal Liquidity idea:

> Demand has temporal structure. Capacity can be gained when the execution architecture is able to observe and exploit that structure.

The correct mathematical starting point may therefore combine:

\[
\text{multi-user capacity}
+
\text{statistical multiplexing}
+
\text{deadline-constrained scheduling}.
\]

---

# Part III — Demand-Side Temporal Information

## 16. Temporal Demand Profiles

For stream \(i\), represent temporal demand abstractly by

\[
\theta_i
=
\left(
v_i(t),
q_i(t),
d_i,
j_i,
p_i,
h_i,
a_i
\right),
\]

where, provisionally:

- \(v_i(t)\): economic value as a function of execution time or delay;
- \(q_i(t)\): expected execution intensity;
- \(d_i\): deadline or delay tolerance;
- \(j_i\): tolerated timing variability;
- \(p_i\): persistence or continuation behavior;
- \(h_i\): planning horizon or duration;
- \(a_i\): arrival-process characteristics.

This representation is illustrative rather than canonical.


### 16.1 Stream execution cadence

For persistent services, transaction latency alone is insufficient. A service also has a required **execution cadence**: the maximum temporal separation it can tolerate between consecutive economically meaningful executions or state transitions.

Let successive execution times of service \(i\) be \(t_{i,1},t_{i,2},\ldots\). Define

\[
\tau_{i,k}=t_{i,k+1}-t_{i,k}.
\]

A service may require

\[
\tau_{i,k}\leq \tau_i^{\mathrm{req}},
\]

or equivalently require execution frequency

\[
f_i^{\mathrm{req}}=\frac{1}{\tau_i^{\mathrm{req}}}.
\]

This differs from individual transaction delay,

\[
D_{i,k}=t_{i,k}^{\mathrm{exec}}-t_{i,k}^{\mathrm{arrival}}.
\]

The first describes the temporal cadence of a **service stream**; the second describes the waiting time of an individual request.

A provisional stream profile is therefore

\[
\theta_i=(T_i,\lambda_i,\tau_i^{\mathrm{req}},J_i,F_i,V_i,\ldots),
\]

where \(T_i\) is duration or persistence, \(\lambda_i\) execution intensity, \(\tau_i^{\mathrm{req}}\) required inter-execution cadence, \(J_i\) tolerated cadence jitter, \(F_i\) temporal flexibility around individual executions, and \(V_i\) economic value or temporal utility.

This distinction is especially important for continuously operating services such as an on-chain two-sided order book. Such a service may fit within aggregate compute capacity while remaining unusable if successive economically meaningful state transitions cannot occur frequently enough.

### 16.2 Block time is not necessarily application execution cadence

Current blockchain architectures often make block or slot time appear to be the minimum separation between meaningful service updates. This is an architectural property, not necessarily a fundamental limit.

Let slot duration be \(\Delta\), and let an execution lattice expose \(m\) quanta per slot:

\[
\delta=\frac{\Delta}{m}.
\]

If only block boundaries expose independently meaningful execution states, a persistent service may effectively be limited to cadence on the order of \(\Delta\). If the architecture instead permits independently meaningful execution opportunities at the quantum scale, then in the simplest model service cadence may approach \(\delta\).

Thus,

\[
\boxed{\text{block/slot time}\neq\text{fundamental minimum application execution interval}.}
\]

Whether sub-slot execution states can safely and usefully be exposed depends on execution, state-consistency, commitment, and consensus architecture. Quantum subdivision is therefore not assumed to be free.

### 16.3 Temporal-resolution or cadence exclusion

In a simple one-meaningful-transition-per-quantum model, service \(i\) is cadence-feasible only if

\[
\delta\leq\tau_i^{\mathrm{req}}.
\]

If \(\delta>\tau_i^{\mathrm{req}}\), the service lies outside the architecture's temporal-resolution capacity even if total computation over the slot is sufficient.

This creates a third exclusion mechanism:

- **price exclusion** — execution is feasible but uneconomic;
- **latency exclusion** — an individual operation cannot meet its arrival-to-execution deadline;
- **cadence exclusion** — the architecture cannot expose successive meaningful execution opportunities frequently enough for a persistent service.

A throughput measure can therefore be misleading. A chain may process a large number of operations over a slot while failing to provide the state-transition frequency required by an application.

### 16.4 Two gains from finer quantum resolution

Reducing \(\delta\) can create two different capacity gains.

**Multiplexing gain** occurs when finer resolution lets already-feasible heterogeneous demand be packed more efficiently across execution opportunities.

**Service-enablement gain** occurs when finer resolution makes feasible an application class whose required execution cadence could not be supported at slot granularity.

The demand-side capacity study should therefore estimate the distribution

\[
P(\tau^{\mathrm{req}})
\]

across persistent services, together with intensity, duration, jitter, flexibility, and economic value.


For TLM, a **Temporal Liquidity Profile** can be understood more generally as a protocol-visible representation of the temporal structure and flexibility of execution demand.

The theory should not assume that every component above must be disclosed. One objective is to determine the minimum useful representation.

---

## 17. Supply-Demand Duality

The emerging theory has two distinct objects.

### Supply side

\[
L(\delta)
\]

is the execution lattice at temporal resolution \(\delta\).

### Demand side

\[
\Theta = \{\theta_i\}_{i=1}^{n}
\]

is the set of heterogeneous temporal demand profiles.

The scheduler solves a matching problem:

\[
\Theta
\overset{\mathcal{A}}{\longrightarrow}
L(\delta).
\]

This provides a more precise interpretation of execution scheduling:

> **Execution scheduling is the matching of temporally structured demand to temporally structured supply under resource, information, and incentive constraints.**

A spot market is one particular information and allocation architecture for performing this matching. It is not the definition of the problem.

---

## 18. The Fundamental Oracle Benchmark

To define an upper bound, introduce an idealized oracle scheduler.

Assume:

- physical execution resources are fixed;
- the execution lattice is fixed;
- true temporal demand is known;
- strategic misreporting is absent;
- scheduling computation is unconstrained;
- all physical, consistency, and security constraints remain enforced.

Let

\[
W(D,S)
\]

be a welfare or service objective for demand \(D\) under schedule \(S\).

Define

\[
W^{*}(\delta)
=
\max_{S\in\Omega(T,\delta)}
W(D,S).
\]

This is not an implementable mechanism. It is a benchmark.

A practical mechanism \(M\) produces

\[
W_M(\delta,I)
\leq
W^{*}(\delta).
\]

The difference can be decomposed conceptually into several losses.

---

## 19. A Capacity-Loss Decomposition

Observed execution performance may fall below the ideal frontier for different reasons.

### 19.1 Physical loss

Demand lies outside the true physical capability of the system.

Examples include:

- minimum achievable latency;
- insufficient computation;
- state bottlenecks;
- propagation constraints;
- consensus requirements.

No fee or information mechanism can recover this loss without changing the substrate.

### 19.2 Temporal-resolution loss

Supply opportunities exist physically but are not separately schedulable because the execution model is temporally too coarse.

This is the gap between an ideal fine-resolution lattice and the protocol-visible scheduling lattice.

### 19.3 Information loss

The scheduler cannot exploit feasible flexibility because demand does not reveal enough of its temporal structure.

### 19.4 Mechanism loss

The information exists, but the scheduling, pricing, or admission mechanism does not exploit it efficiently.

### 19.5 Strategic and verification loss

A richer interface may create manipulation, verification, privacy, or commitment problems that reduce realizable gains.

Thus the observed capacity frontier is not only a property of raw hardware.

Conceptually,

```text
Fundamental Physical Opportunity
            ↓
Temporal Representation
            ↓
Information Interface
            ↓
Market / Scheduling Mechanism
            ↓
Strategic and Implementation Constraints
            ↓
Realized Service Capacity
```

This decomposition is central to the proposed theory.

---

# Part IV — Capacity as a Function of Information

## 20. Information-Conditioned Capacity

Let \(D\) denote latent execution-relevant demand state.

The protocol exposes message

\[
X = f(D).
\]

The scheduler chooses an allocation based on

\[
(X,L(\delta)).
\]

Let \(I\) summarize the execution-relevant information available to the scheduler.

**The type of \(I\).** Throughout, \(I\) denotes an **information structure** — the map \(X=f(D)\) together with the partition of the latent demand space it induces — ordered in the **Blackwell** sense: \(I_1 \succeq I_0\) means \(I_1\) is a sufficient refinement of \(I_0\), so any allocation realizable under \(I_0\) is realizable under \(I_1\). The monotonicity of capacity in information (\S21) is stated with respect to this partial order, not a scalar. Scalar summaries — a bit-rate for the message \(X\), or the mutual information \(\mathrm{I}(D;X)\) — are used only as *proxies* when a total order is needed (for instance the minimal-information quantity \(I_{\min}(\eta)\) of \S22), and whether such a proxy is monotonically linked to scheduling gain is itself an open question (\S48). Two Blackwell-incomparable information structures may not be ranked by capacity at all.

With that fixed, we propose the candidate capacity family

\[
\boxed{
\mathcal{C}(\delta,I,\epsilon)
}
\]

with:

- \(\delta\): supply-side temporal resolution;
- \(I\): demand-side information available for allocation;
- \(\epsilon\): allowed service violation or reliability requirement.

This expression is a research object, not a completed theorem.

The ideal structure suggests:

\[
\mathcal{C}(\Delta,I_0)
\subseteq
\mathcal{C}(\delta,I_1)
\subseteq
\mathcal{C}^{*},
\]

when \(\delta < \Delta\) and \(I_1\) is strictly more useful than \(I_0\), subject to overhead and strategic effects.

The theory should determine when these inclusions are strict and when richer information or finer resolution produces no meaningful gain.

---

## 21. The Value of Temporal Information

The strongest TLM hypothesis can now be stated without assuming any particular fee mechanism:

> **Holding physical execution resources fixed, credible information about heterogeneous temporal demand can enlarge the achievable service region by allowing the scheduler to match flexible demand to otherwise stranded execution opportunities.**

Let \(M\) be a scalar measure of a capacity region. Then the value of additional information may be written as

\[
V_I
=
M(\mathcal{C}(\delta,I_1,\epsilon))
-
M(\mathcal{C}(\delta,I_0,\epsilon)).
\]

This is distinct from adding physical resources.

A positive \(V_I\) would demonstrate **information-enhanced capacity**.

---

## 22. Shannon Versus Yao in This Framework

Shannon and Yao play different roles in this framework, not parallel ones: capacity is the primary object, and communication complexity is a secondary tool.

### 22.1 Shannon's role

Shannon motivates the primary question:

> **What is fundamentally achievable under a constrained resource model?**

The main execution-theory object is therefore a capacity frontier or capacity region.

### 22.2 Yao's role

Yao's communication complexity motivates a secondary but important question:

> **How much information must participants communicate for the scheduler to approach a desired point on the capacity frontier?**

Define, provisionally,

\[
I_{\min}(\eta)
=
\min
\left\{
I:
M(\mathcal{C}(\delta,I,\epsilon))
\geq
\eta
M(\mathcal{C}^{*}(\delta,\epsilon))
\right\}.
\]

For example:

- how much temporal information is needed to reach 90% of the oracle benchmark?
- how much additional disclosure is required to move from 90% to 99%?
- is a small categorical profile nearly as effective as a high-dimensional demand description?

This is where communication-complexity ideas may become useful.

Yao therefore remains in the framework, but **capacity precedes communication complexity**.

---

## 23. Efficient Information, Not Maximum Information

A scheduler with perfect demand knowledge may define a useful upper bound, but it is not necessarily a desirable protocol design.

Richer disclosure can create costs:

- communication overhead;
- verification cost;
- privacy loss;
- strategic manipulation;
- complexity;
- state growth;
- centralization pressure;
- stale or inaccurate forecasts.

The practical objective is therefore not full information.

It is:

> **the smallest robust information interface that captures most of the available capacity gain.**

This connects information theory, communication complexity, mechanism design, and protocol architecture.

A TLM profile should therefore be evaluated not by how expressive it is, but by its position on a frontier such as

\[
\text{Capacity Gain}
\quad\text{versus}\quad
\text{Information / Verification Cost}.
\]

---

# Part V — Markets, Prices, and Feedback

## 24. Kelly: Capacity as an Economic Allocation Problem

Frank Kelly's work shows that communication networks can be studied simultaneously as:

- constrained physical systems;
- optimization problems;
- price-mediated markets;
- feedback-control systems.

Users possess utility for allocated rate. Network capacity constraints create shadow prices. Distributed rate-control mechanisms can converge toward efficient or proportionally fair operating points.

This remains fundamental for execution systems.

However, the execution problem considered here extends beyond elastic rate allocation. It includes:

- discrete jobs;
- deadlines;
- time-varying value;
- stream persistence;
- future execution opportunities;
- jitter;
- indivisible state transitions;
- strategic temporal disclosure.

The natural extension is:

\[
\text{rate market}
\rightarrow
\text{temporally differentiated execution market}.
\]

---

## 25. Fees as Information and Demand Filters

A fee mechanism performs several functions:

1. signals scarcity;
2. determines participation;
3. suppresses lower-valued demand;
4. changes submission timing;
5. prioritizes competing requests;
6. may fund resource supply;
7. produces feedback about imbalance.

But a price signal may be informationally incomplete.

If two users have different temporal flexibility but can express only willingness to pay for near-term execution, the market may force both into the same spot competition even when a temporally differentiated allocation would serve both.

This motivates a distinction between:

\[
\text{price information}
\]

and

\[
\text{temporal service information}.
\]

A capacity theory provides a benchmark for determining whether richer temporal information actually increases the feasible or welfare-achievable region.

---

## 26. Closed-Loop Execution Markets

An execution market is dynamic.

```text
Demand declarations and temporal profiles
                  ↓
             Admission
                  ↓
        Scheduling and pricing
                  ↓
     Delay, price, utilization, failure
                  ↓
        Participant adaptation
                  ↓
       Updated future demand
                  ↺
```

The protocol contains coupled loops:

### Economic loop

Prices and expected service alter participation.

### Informational loop

Realized behavior reveals forecast quality and demand structure.

### Control loop

Protocol parameters and schedulers respond to congestion and service outcomes.

Capacity analysis should eventually incorporate this endogeneity. The first theory, however, may begin with an exogenous demand model in order to establish clean bounds.

---

# Part VI — Blockchain as a Motivating Application

## 27. Existing Blockchain Capacity Work

The phrase "blockchain capacity" already has important prior art.

Bagaria, Kannan, Tse, Fanti, and Viswanath's Prism work explicitly studies blockchain performance relative to underlying physical communication limits. Their framework treats communication capacity and propagation delay as fundamental limits for consensus throughput and confirmation latency.

This paper does not replace that approach.

Instead, it proposes a different layer of capacity analysis:

```text
Network / Consensus Capacity
          ↓
Physical Execution Substrate
          ↓
Execution-Service Capacity
          ↓
Market and Scheduling Mechanism
```

Prism asks how a consensus protocol can approach underlying network limits.

The present paper asks:

> **Given a shared execution substrate, what heterogeneous execution demand can be supported, and how do temporal resolution and demand information affect the service-capacity frontier?**

These are complementary questions.

---

## 28. Ethereum as a Coarse Temporal Execution Market

Ethereum provides a useful motivating example.

At a high level, execution capacity is allocated block by block. EIP-1559 supplies a congestion-responsive base fee, and priority fees help express willingness to pay for inclusion. PBS separates block construction from block proposal and introduces specialized builders.

These mechanisms substantially improve price discovery, allocation, and block construction.

Yet the transaction interface reveals relatively limited information about long-horizon temporal demand.

A user may know:

- this transaction is urgent;
- this batch can wait twenty minutes;
- this service will submit a predictable stream;
- this workload is persistent;
- this request may execute in any of several future windows;
- this application needs low latency but has stable aggregate demand.

Much of this structure is absent from ordinary spot transaction bidding.

The capacity question is not whether every transaction needs such metadata.

It is:

> **How much capacity is lost when heterogeneous temporal demand is compressed into a coarse spot execution interface?**

---

## 29. Why Applications Leave Shared Chains

A high-frequency execution project may leave a general-purpose chain for several different reasons.

### Physical impossibility

Its latency requirement lies below the chain's physical or consensus-imposed floor.

### Price exclusion

Its per-operation value cannot support the prevailing spot fee.

### Service uncertainty

Its business model cannot tolerate variance in execution delay or cost.

### Missing temporal contract

The system cannot express persistent or predictable demand in a way that permits capacity planning.

These should not be conflated.

TLM is not a solution to physical impossibility. Its plausible gain lies in the latter categories: **recovering capacity stranded by coarse scheduling, incomplete temporal information, and spot-only allocation.**

---

## 30. Temporal Liquidity Market as a Test Architecture

Within this general theory, a Temporal Liquidity Market is one candidate execution architecture.

TLM proposes that applications may communicate protocol-visible information about the temporal structure of execution demand.

The theory developed here gives TLM a falsifiable objective:

> **Does temporal disclosure plus programmable scheduling move the realized execution region materially closer to the fundamental capacity frontier?**

TLM should not define the upper bound.

Instead:

\[
\mathcal{C}_{\mathrm{TLM}}
\subseteq
\mathcal{C}^{*}.
\]

The research task is to measure the gap.

In some demand regimes, TLM may produce substantial gains.

In others, spot allocation may already be close to optimal.

A useful theory must be capable of showing both.

---

# Part VII — Candidate Formal Model

## 31. Minimal Two-Sided Model

A first formal model should be deliberately simple.

Let time horizon \(T\) be divided into \(Q\) quanta of size \(\delta\).

Supply:

\[
K_q \geq 0,
\qquad
q=1,\ldots,Q.
\]

Demand stream \(i\) contains jobs \(j\) with:

\[
g_{ij} = \text{execution resource requirement},
\]

\[
F_{ij} \subseteq \{1,\ldots,Q\}
= \text{feasible execution quanta},
\]

and value

\[
v_{ij}(q)
\]

if executed in quantum \(q\).

Let binary allocation variable

\[
x_{ijq}\in\{0,1\}.
\]

Physical capacity requires

\[
\sum_{i,j} g_{ij}x_{ijq}
\leq
K_q
\quad
\forall q.
\]

Each job executes at most once:

\[
\sum_q x_{ijq} \leq 1.
\]

Temporal feasibility requires

\[
x_{ijq}=0
\quad\text{if }q\notin F_{ij}.
\]

An oracle welfare upper bound is

\[
W^{*}
=
\max_x
\sum_{i,j,q}
v_{ij}(q)x_{ijq}
\]

subject to the constraints above.

This is not yet a complete execution theory. But it gives us a clean benchmark against which information restrictions and online scheduling can be introduced.

**Relationship to RN-11, and tractability.** This program is the same object as the execution-capital allocation problem of **RN-11**, in different notation. RN-11 writes the allocation as \(x_i(s,t)\) with time-shaped value \(v_i(s,t)=V_i(s)\,\phi_i(t-\tau_i(s))\), where the decay function \(\phi_i\) generalizes the hard feasible set \(F_{ij}\) used here: \(F_{ij}\) is the rectangular special case \(\phi_i\in\{0,1\}\), and the value profile \(v_{ij}(q)\) above subsumes \(\phi_i\) when values are allowed to vary across quanta. RN-11 additionally reads the dual shadow prices on per-quantum capacity as a **welfare benchmark on the value of capacity**, which it deliberately does **not** identify with the market block-fee-rate term structure — whether a decentralized fee market reproduces those shadow prices is left open there. That benchmark is the pricing-side counterpart of the capacity benchmark defined here and is not re-derived in this note. To keep the corpus from carrying two drifting copies, **RN-11 is treated as the owner of the canonical allocation program** and this note references it (see \S53a). Finally, the oracle is clairvoyant *and* computationally unbounded by assumption (\S18): the program is a generalized assignment problem, NP-hard in general, so the simulation targets of \S52 should budget for exact small instances plus relaxations rather than assume \(W^{*}\) is cheap to compute at scale.

---

## 32. Information Restrictions

The oracle sees \(F_{ij}\) and \(v_{ij}(q)\).

A real protocol may see only a compressed message

\[
m_{ij}
=
\phi(F_{ij},v_{ij},\ldots).
\]

Examples:

- price only;
- price + deadline;
- price + execution window;
- categorical temporal class;
- compact Temporal Liquidity Profile;
- full curve.

For message scheme \(\phi\), define

\[
W_{\phi}
=
\max_{\pi \in \Pi(\phi)}
\mathbb{E}[W(\pi(m))].
\]

Then the information loss is

\[
L_I(\phi)
=
W^{*}-W_{\phi}.
\]

This formulation creates a path toward Yao-like lower bounds and rate-distortion-like questions without making either theory the starting point.

---

## 33. Resolution Restrictions

Now hold demand information fixed but vary quantum size.

Let

\[
W^{*}(\delta)
\]

be the oracle optimum at resolution \(\delta\).

Then:

\[
W^{*}(\Delta)
\leq
W^{*}(\Delta/2)
\leq
W^{*}(\Delta/4)
\leq \cdots
\]

under ideal subdivision assumptions — specifically, for the divisible relaxation at fixed per-horizon capacity (the scope note in \S8.2). For the indivisible program of \S31 with resolution-dependent per-quantum capacity \(K(\delta)\), this ordering can fail unless jobs may span multiple contiguous quanta.

Define

\[
G_{\delta}
=
W^{*}(\delta)
-
W^{*}(\Delta).
\]

This directly measures the value of finer supply-side temporal resolution.

The first empirical and simulation goal should be to estimate the shape of

\[
W^{*}(\delta)
\]

for realistic demand traces.

---

## 34. Joint Resolution-Information Surface

The central theoretical object of this version is therefore a two-sided surface:

\[
\boxed{
W(\delta,I)
}
\]

or, more generally,

\[
\boxed{
\mathcal{C}(\delta,I,\epsilon).
}
\]

This creates four instructive regimes:

| Supply resolution | Demand information | Interpretation |
|---|---|---|
| coarse | poor | slot-level spot market |
| fine | poor | high-resolution scheduler with little demand knowledge |
| coarse | rich | information-rich market constrained by coarse execution time |
| fine | rich | high-resolution, information-rich execution architecture |

This separation is essential.

More temporal information cannot recover a physical latency floor.

Finer time resolution cannot help if the scheduler cannot distinguish flexible from inflexible demand.

The largest gains may require **joint improvement of both sides**.

---

# Part VIII — Research Hypotheses

## 35. Capacity Hypotheses

### H1 — Capacity-Region Hypothesis

Shared execution systems are better characterized by a multi-dimensional achievable workload region than by a single throughput scalar.

### H2 — Temporal-Resolution Hypothesis

Holding physical resources fixed, finer scheduling resolution can enlarge the achievable execution region when demand contains economically meaningful sub-slot temporal heterogeneity. (Formally a relaxation result for the divisible program at fixed per-horizon capacity; see the scope note in \S8.2.)

### H3 — Diminishing-Resolution Hypothesis

Capacity gain from finer temporal resolution eventually diminishes once the quantum becomes materially smaller than the characteristic temporal variation of demand.

### H3a — Service-Cadence Hypothesis

For persistent execution services, aggregate throughput and individual transaction latency do not fully determine feasibility. A service may additionally require a maximum spacing between consecutive meaningful executions. Finer lattice resolution can enlarge the capacity region by admitting service classes whose required cadence lies below the block or slot interval.

### H3b — Block-Time Decoupling Hypothesis

The block or consensus slot interval need not be the fundamental minimum application execution interval. Architectures that safely expose multiple meaningful execution opportunities within a slot may support service cadences determined by the execution lattice quantum rather than the slot duration.


### H4 — Information-Enhanced Capacity Hypothesis

Holding physical resources and temporal resolution fixed, credible temporal demand information can enlarge the achievable service or welfare region.

### H5 — Joint Capacity Hypothesis

Execution capacity is jointly constrained by the temporal resolution of supply and the execution-relevant information exposed by demand.

### H6 — Multiuser Temporal-Multiplexing Hypothesis

Heterogeneous temporal flexibility creates multiplexing gain because flexible streams can be shifted away from scarce execution intervals while delay-intolerant streams consume near-term capacity.

### H7 — Delay-Constrained Capacity Hypothesis

A workload may lie inside a system's throughput capacity region while lying outside its delay-constrained service region.

### H8 — Information Sufficiency Hypothesis

A low-dimensional temporal profile may capture most of the capacity gain obtainable from full demand disclosure.

### H9 — Information Lower-Bound Hypothesis

For a fixed demand model, temporal resolution, and target efficiency \(\eta\), there exists a minimum amount of execution-relevant information required to achieve \(\eta\) of the oracle benchmark.

### H10 — Mechanism Gap Hypothesis

Even with identical physical resources and identical information, different market and scheduling mechanisms can realize materially different fractions of the capacity frontier.

---

# Part IX — Measurement and Experimental Program

## 36. Stage 1: Synthetic Capacity Experiments

Begin with controlled demand classes:

- immediate jobs;
- deadline jobs;
- window-flexible jobs;
- periodic streams;
- persistent low-variance streams;
- bursty unpredictable streams.

For each workload, compute or approximate:

\[
W^{*}(\delta,I_{\mathrm{full}}).
\]

Then vary \(\delta\).

Measure:

- supported workload;
- deadline satisfaction;
- utilization;
- welfare;
- stranded capacity;
- queue delay.

The objective is to determine whether a nontrivial resolution-capacity curve exists.

---

## 37. Stage 2: Information Ablation

Hold the lattice constant.

Compare information schemes:

1. resource demand only;
2. resource demand + price;
3. + deadline;
4. + execution window;
5. + stream duration and intensity;
6. + compact Temporal Liquidity Profile;
7. oracle full information.

Estimate

\[
W(\delta,I_k)
\]

for each information interface.

This directly measures the marginal value of temporal disclosure.

---

## 38. Stage 3: Multiuser Capacity Region

Instead of one aggregate workload, construct two or more demand classes.

For two classes,

\[
(\lambda_1,\lambda_2).
\]

Numerically trace the achievable frontier.

Examples:

- urgent + patient;
- continuous + bursty;
- predictable low-latency + unpredictable low-latency;
- settlement + liquidation;
- machine workload + human spot demand.

Compare how the frontier moves under:

- slot-only scheduling;
- quantum scheduling;
- price-only information;
- temporal profiles;
- oracle scheduling.

This may provide the clearest visual evidence for or against the theory.

---

## 39. Stage 4: Real Blockchain Traces

Replay identical transaction or application traces under multiple abstract schedulers.

Potential case studies include:

- Ethereum;
- Hyperliquid-style continuous trading demand;
- Monad-like faster execution substrate;
- Aptos-like parallel execution substrate.

The goal is not initially to reproduce every implementation detail.

The goal is to separate:

\[
\text{physical substrate effect}
\]

from

\[
\text{scheduling-resolution effect}
\]

from

\[
\text{information-interface effect}.
\]

---

# Part X — Prior Work and Intellectual Lineage

## 40. Shannon

Shannon provides the methodological foundation:

- uncertainty;
- constrained information;
- fundamental achievable limits;
- separation of capacity from coding mechanism.

This paper borrows the methodology, not a literal channel equivalence.

---

## 41. Goldsmith and Wireless Adaptation

Goldsmith and Varaiya show how side information and time-varying resource adaptation alter fading-channel capacity. Goldsmith's broader adaptive wireless work studies rate and power adaptation under changing channel conditions.

The TLM relevance is:

- state information can have capacity value;
- adaptation must occur on an appropriate temporal scale;
- physical resources and information-conditioned capacity should be distinguished.

---

## 42. Tse, Hanly, and Multiuser Capacity

Tse and Hanly provide several especially relevant ideas:

- throughput capacity region;
- delay-sensitive versus delay-tolerant capacity concepts;
- dynamic allocation across fading states;
- multiuser resource sharing.

Tse and Viswanath further develop multiuser diversity and opportunistic communication, emphasizing how scheduling can exploit temporal variation across users.

The execution analogue is a multi-stream capacity region under heterogeneous temporal demand.

---

## 43. Statistical Multiplexing and Effective Bandwidth

Work on statistical multiplexing, effective bandwidth, queueing, and network calculus studies how stochastic traffic sources can share finite service capacity while respecting delay and backlog requirements.

This literature may supply much of the mathematical machinery needed for temporal execution streams.

It is especially relevant to:

- duration;
- intensity;
- burstiness;
- multiple time scales;
- deadlines;
- statistical admission;
- service guarantees.

---

## 44. Yao and Communication Complexity

Yao's contribution remains conceptually useful but secondary.

Once an execution-capacity frontier is defined, communication complexity motivates lower-bound questions about how much private demand information must cross the protocol boundary to approach that frontier.

The key distinction is:

```text
Shannon / wireless capacity:
What is fundamentally achievable?

Yao / communication complexity:
How much information must be exchanged to achieve a target outcome?
```

In this framework, the first question is primary.

---

## 45. Kelly and Network Utility Maximization

Kelly's work connects:

- user utility;
- prices;
- capacity constraints;
- congestion feedback;
- distributed optimization;
- fairness.

This becomes essential when the execution-capacity theory moves from feasibility to economic allocation.

The long-term objective is not merely to maximize jobs served. It is to characterize an economically meaningful execution frontier under heterogeneous value and time preference.

---

## 46. Blockchain Fundamental Limits

Prism and related work by Bagaria, Kannan, Tse, Fanti, Viswanath, and collaborators provide important blockchain prior art for the fundamental-limits methodology.

Their emphasis is primarily the physical communication and consensus layer.

The present paper proposes a complementary execution-layer question:

> **What is the service-capacity frontier of a shared execution substrate under heterogeneous temporal demand?**

This distinction should be preserved carefully.

---

# Part XI — Open Questions

## 47. Formal Questions

1. What is the correct mathematical definition of execution capacity?
2. Should the primary object be a region, welfare frontier, stability region, or combination?
3. What is the correct supply-side lattice representation?
4. Which physical constraints belong inside \(\Omega(T,\delta)\)?
5. Under what assumptions is capacity monotone as \(\delta\) decreases?
6. When does finer temporal resolution produce zero gain?
7. What is the appropriate analogue of a characteristic or coherence time for temporal demand?
8. How should execution streams with multiple time scales be modeled?
9. How should state conflicts and precedence constraints alter the lattice?
10. How should stochastic future capacity be represented?

## 48. Information Questions

11. What temporal information is sufficient for near-optimal allocation?
12. How should information quantity be measured when messages are semantic rather than raw bits?
13. Can mutual information between latent demand state and protocol-visible profile predict scheduling gain?
14. Can an execution-information lower bound be derived?
15. Is there a rate-distortion-like relationship between temporal-profile precision and acceptable execution-quality loss?
16. How costly are stale or inaccurate profiles?
17. What information should remain private?

## 49. Market Questions

18. How can temporal information be elicited truthfully?
19. How should price interact with temporal flexibility?
20. When should predictable demand receive different treatment from bursty demand?
21. How should fairness be defined across heterogeneous temporal classes?
22. Can shadow prices be defined for lattice cells or future capacity?
23. How should persistent demand commitments be enforced?
24. Can temporal pricing increase participation rather than merely redistribute existing blockspace?

## 50. Blockchain Questions

25. How much capacity does slot-level temporal granularity strand in realistic blockchain workloads?
26. How does the capacity-resolution curve differ across Ethereum-like, Monad-like, Aptos-like, and specialized execution substrates?
27. Which high-frequency applications are physically impossible on a given chain and which are merely excluded by the current service interface?
28. How much low-value demand is suppressed by spot congestion pricing despite being schedulable at other times?
29. Can TLM recover materially useful capacity without increasing physical execution resources?
30. What quantum resolution is justified by real demand rather than arbitrary engineering preference?

---

# Part XII — Proposed Research Roadmap

## 51. First Theorem Target

The first theorem should be intentionally modest.

Construct a two-class model:

- class \(U\): urgent jobs with one feasible quantum;
- class \(F\): flexible jobs with a window of \(k\) feasible quanta.

Fix total physical execution capacity.

Compare:

1. slot-level scheduling;
2. fine-quantum oracle scheduling;
3. fine-quantum scheduling without flexibility information;
4. fine-quantum scheduling with flexibility information.

Seek conditions under which:

\[
\mathcal{C}_{\mathrm{slot}}
\subsetneq
\mathcal{C}_{\mathrm{quantum,no-info}}
\subseteq
\mathcal{C}_{\mathrm{quantum,info}}
\subseteq
\mathcal{C}^{*}.
\]

Even one strict-inclusion result would establish that temporal resolution and demand information are distinct sources of execution-capacity gain.

---

## 52. First Simulation Target

Build a discrete-event simulator with:

- configurable slot duration;
- configurable quantum \(\delta\);
- fixed physical capacity per horizon;
- heterogeneous temporal demand streams;
- price-only and profile-aware schedulers;
- oracle benchmark.

Plot:

\[
\text{capacity or welfare}
\quad\text{versus}\quad
\delta.
\]

Then plot:

\[
\text{capacity or welfare}
\quad\text{versus}\quad
\text{information interface}.
\]

Finally estimate the joint surface:

\[
W(\delta,I).
\]

This would turn the theory from narrative into measurable research.

---

## 53. First Empirical Target

Identify demand traces where temporal structure is economically meaningful.

Examples:

- continuous order-book updates;
- liquidation bursts;
- rollup batch submission;
- oracle updates;
- recurring settlement;
- automated machine-to-machine activity.

Estimate:

- characteristic time scales;
- burstiness;
- deadline distributions;
- persistence;
- feasible execution windows.

Then ask whether a slot-only scheduler destroys economically useful temporal distinctions.

---

## 53a. Reconciliation with RN-05 and RN-11

This note deliberately overlaps two existing TLM notes and should reference, not restate, them.

- **RN-05 — the supply substrate.** The execution lattice (\S7–\S8) and the quantum \(\delta\) are RN-05's quantum lattice. RN-05 argues the finest-resolution bound — that a sub-slot ordering quantum is limited by commitment and verification cost rather than by consensus latency — which this note imports as its physical-capability premise. The time-scale hierarchy \(\delta_{\mathrm{exec}}\le\delta_{\mathrm{order}}\le\Delta_{\mathrm{commit}}\le\Delta_{\mathrm{consensus}}\) is the multi-clock reading of the same substrate.
- **RN-11 — the allocation program.** The benchmark program of \S31 is RN-11's execution-capital allocation problem. RN-11 is the more developed statement (time-shaped value \(v_i(s,t)=V_i(s)\phi_i(t-\tau_i(s))\); neutrality, reducibility, and incentive-compatibility constraints; and the dual shadow prices read as a welfare benchmark on capacity, which RN-11 explicitly does **not** identify with the market term structure). **RN-11 owns the canonical program;** this note uses it only as a capacity benchmark and does not introduce a competing formalization.

Notation should be unified across the three notes in a single pass: the hard feasible set \(F_{ij}\) here is the rectangular special case of RN-11's decay function \(\phi_i\); this note's \(K_q\) is RN-11's per-quantum capacity \(C(t)\); this note's welfare \(W^{*}\) is RN-11's TET objective. Until that pass, cross-references above mark the correspondences.

---

# Standalone Scope and Future Use

The theory developed in this paper is intentionally independent of TLM and of any particular blockchain.

A valid execution-capacity definition should remain meaningful if TLM does not exist. It should apply across different consensus protocols, fee mechanisms, scheduling algorithms, execution engines, and application domains.

TLM, Ethereum, Hyperliquid-like trading systems, and future programmable execution architectures are therefore **applications of the theory**, not assumptions used to define its bound.

The intended role of this paper in future work is:

\[
\text{What is fundamentally possible?}
\rightarrow
\text{What information is necessary?}
\rightarrow
\text{What mechanism approaches it?}
\rightarrow
\text{How close does a real system get?}
\]

Future lattice research, TLM mechanisms, fee designs, and application case studies should be able to cite the same capability model rather than redefining capacity for each architecture.

# Positioning Against Existing Blockchain Architecture Work

The architectural ingredients of this theory are not individually new, and the paper should say so explicitly.

Several lines of blockchain research have already established important pieces:

- **Prism and related work** study blockchain performance relative to physical communication limits such as bandwidth and propagation delay.
- **Narwhal/Tusk and related DAG-mempool architectures** decouple reliable transaction dissemination from ordering.
- **Flow and related modular architectures** separate ordering/consensus roles from execution/computation roles.
- **Parallel execution systems** such as Block-STM and related work study how dependency structure, conflicts, and concurrency constrain realized execution throughput.
- **Real-time blockchain scheduling work** studies deadlines and multi-block schedulability.
- **Queueing and fee-market work** studies stability, congestion, waiting time, and price-mediated admission.

These works strongly support the premise that blockchain operation is composed of distinct subsystems with different constraints and time scales.

The contribution of the present theory is therefore **not the observation that consensus, ordering, dissemination, commitment, and execution can be decoupled**.

The proposed contribution is to treat that decoupling as the starting point of a **first-principles temporal capability model**.

The theory asks:

\[
\boxed{
\text{What are the irreducible and architecture-induced time scales of each subsystem?}
}
\]

and then:

\[
\boxed{
\text{What multi-user execution-service capacity follows from those time scales?}
}
\]

This is a different objective from pipelining components for better benchmark throughput.

## Distinct temporal capability layers, restated

The time-scale hierarchy this positioning relies on — \(\delta_{\mathrm{exec}}\le\delta_{\mathrm{order}}\le\Delta_{\mathrm{commit}}\le\Delta_{\mathrm{consensus}}\), the four-way split of causes (irreducible-physical / security / protocol-induced / architecture-induced coupling), and the question *how much application execution capacity can exist below the cadence of global consensus?* — is developed once in the front section **Physical Geography, Speed-of-Light Bounds, and Decoupled Time Scales** and is not repeated here. The narrower point of this section is that **each of those layers is already the subject of an established research line**, so the contribution claimed below is the capacity abstraction over them, not the layering itself.

## Synthesis rather than isolated novelty

The research contribution should therefore be positioned conservatively but clearly:

> Existing work has independently established physical network limits, modular consensus architectures, dissemination-ordering separation, ordering-execution separation, parallel execution limits, real-time scheduling, and queueing behavior. This paper seeks to unify these results into a mathematical theory of execution capacity in which multiple temporal layers are primitive system variables and heterogeneous application demand is evaluated against a fundamental service-capacity frontier.

This positioning is deliberately different from claiming that any individual architectural decoupling is new.

The novelty, if established, would lie in the **capacity abstraction and unification**.

## A Shannon-style research posture

As in \S5 and \S40, the analogy to Shannon is methodological, not literal: he did not invent noise, bandwidth, or coding but defined the right constrained system and asked for a limit above any particular implementation. Likewise this note does not claim to invent consensus/execution separation, parallelism, or multi-block scheduling; it asks whether those components can be organized into one first-principles question — *given physical constraints and heterogeneous temporal demand, what execution-service region is fundamentally achievable?* — which then serves as the benchmark for concrete architectures.

---

# Related Work as Components, Not the Spine

Existing theories should be acknowledged and used according to the component they contribute.

| Research lineage | Component useful to execution-capacity theory |
|---|---|
| Shannon information theory | Fundamental-limit methodology; capacity before construction |
| Goldsmith / fading-channel theory | State information; temporal adaptation; capacity under changing conditions |
| Tse / Hanly multi-user theory | Capacity regions; multi-user allocation; delay-limited capacity |
| Statistical multiplexing / effective bandwidth | Stochastic streams; multiple time scales; admission under QoS |
| Real-time scheduling | Period/cadence; deadline; jitter; schedulability tools |
| Queueing theory | Stability; waiting time; congestion dynamics |
| Yao / communication complexity | Minimum information needed to approach a target outcome |
| Kelly / network utility | Prices; shadow costs; decentralized allocation |
| Blockchain fundamental-limits work | Communication, propagation, consensus, and security constraints |
| Parallel execution research | Compute/state conflict structure and realizable parallelism |

The research program should use these results where they solve subproblems. A real-time scheduling theorem may characterize one admissible scheduler. An effective-bandwidth result may characterize one stochastic traffic class. A blockchain consensus bound may constrain the physical substrate. None of these components, by itself, defines the full execution-capacity problem.

The standalone object remains:

> **the fundamental capability of a shared temporal execution system serving heterogeneous multi-user demand.**

---

# 54. Relationship to TLM

This paper is broader than TLM.

Its general claim is that execution systems should be studied through a joint theory of:

\[
\boxed{
\text{physical capacity}
+
\text{temporal resolution}
+
\text{demand information}
+
\text{multiuser allocation}
}
\]

TLM is a concrete research framework that motivates the demand-side component.

Within TLM:

- **Temporal Liquidity** characterizes the economic structure and flexibility of execution demand;
- **Temporal Liquidity Profiles** are candidate information interfaces;
- the **execution lattice** represents supply-side execution opportunities;
- **programmable execution scheduling** performs the matching;
- fee and market mechanisms coordinate strategic participants.

The capacity theory therefore gives TLM a benchmark independent of its own mechanisms.

That is important scientifically.

If TLM cannot move the realized execution frontier closer to the fundamental bound, its mechanisms are not justified by capacity arguments.

If it can, the theory provides a principled way to measure the gain.

---

# 55. Conclusion

Execution systems can be studied as information-processing and market-coordination systems.

This paper adds a more fundamental layer:

> **Execution systems should also be studied through their achievable capacity frontiers.**

Shannon's lasting methodological contribution is the separation of fundamental limits from engineering mechanisms. Wireless communication theory shows how that methodology extends to time-varying resources, side information, multiple users, adaptive scheduling, delay constraints, and statistical multiplexing.

These ideas suggest a new execution-theory program.

On the supply side, an execution lattice describes feasible execution opportunities at temporal resolution \(\delta\).

On the demand side, heterogeneous users and streams possess temporal structure and flexibility that may be only partially visible to the scheduler.

The scheduler matches these two sides.

The resulting achievable region depends not only on physical resources, but also on temporal resolution, available demand information, service guarantees, strategic behavior, and allocation mechanisms.

A candidate organizing object is

\[
\boxed{
\mathcal{C}(\delta,I,\epsilon).
}
\]

This formulation leads to concrete questions:

- How much capacity is lost when a slot is the indivisible temporal scheduling unit?
- How much capacity can be recovered by finer execution quanta?
- What temporal information from users is necessary to realize that gain?
- How do multiple streams with different deadlines, persistence, and flexibility share the execution substrate?
- What fraction of the fundamental frontier can a spot fee market achieve?
- What fraction can a richer temporal market achieve?
- What is the minimum information interface needed to approach the frontier?

These questions place TLM inside a broader research program rather than making TLM the assumption of the theory.

The long-term objective is a theory in which protocol mechanisms can be evaluated the same way communication technologies are evaluated against capacity bounds:

> **not by whether they appear faster or more expressive, but by how much of the fundamentally achievable execution opportunity they recover.**

---

# References

[1] C. E. Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal*, vol. 27, pp. 379–423 and 623–656, 1948.

[2] A. J. Goldsmith and P. P. Varaiya, “Capacity of Fading Channels with Channel Side Information,” *IEEE Transactions on Information Theory*, vol. 43, no. 6, pp. 1986–1992, 1997. DOI: 10.1109/18.641562.

[3] D. N. C. Tse and S. V. Hanly, “Multiaccess Fading Channels—Part I: Polymatroid Structure, Optimal Resource Allocation and Throughput Capacities,” *IEEE Transactions on Information Theory*, vol. 44, no. 7, pp. 2796–2815, 1998.

[4] S. V. Hanly and D. N. C. Tse, “Multiaccess Fading Channels—Part II: Delay-Limited Capacities,” *IEEE Transactions on Information Theory*, vol. 44, no. 7, 1998.

[5] D. Tse and P. Viswanath, *Fundamentals of Wireless Communication*, Cambridge University Press, 2005.

[6] D. N. C. Tse, R. G. Gallager, and J. N. Tsitsiklis, “Statistical Multiplexing of Multiple Time-Scale Markov Streams,” *IEEE Journal on Selected Areas in Communications*, 1995.

[7] F. P. Kelly, “Charging and Rate Control for Elastic Traffic,” *European Transactions on Telecommunications*, vol. 8, no. 1, pp. 33–37, 1997. DOI: 10.1002/ett.4460080106.

[8] F. P. Kelly, A. K. Maulloo, and D. K. H. Tan, “Rate Control for Communication Networks: Shadow Prices, Proportional Fairness and Stability,” *Journal of the Operational Research Society*, vol. 49, no. 3, pp. 237–252, 1998. DOI: 10.1057/palgrave.jors.2600523.

[9] A. C.-C. Yao, “Some Complexity Questions Related to Distributive Computing (Preliminary Report),” in *Proceedings of the 11th Annual ACM Symposium on Theory of Computing*, pp. 209–213, 1979. DOI: 10.1145/800135.804414.

[10] V. Bagaria, S. Kannan, D. Tse, G. Fanti, and P. Viswanath, “Deconstructing the Blockchain to Approach Physical Limits,” arXiv:1810.08092, 2018.

[11] G. Danezis, E. Kokoris-Kogias, A. Sonnino, and A. Spiegelman, “Narwhal and Tusk: A DAG-based Mempool and Efficient BFT Consensus,” *EuroSys 2022*. arXiv:2105.11827.

[12] A. Hentschel et al. (Dapper Labs), “Flow: Separating Consensus and Compute — Block Formation and Execution,” 2019. arXiv:1909.05821.

[13] R. Gelashvili, A. Spiegelman, Z. Xiang, G. Danezis, Z. Li, D. Malkhi, Y. Xia, and R. Zhou, “Block-STM: Scaling Blockchain Execution by Turning Ordering Curse to a Performance Blessing,” *PPoPP 2023*. arXiv:2203.06871.

[14] Real-time blockchain scheduling — deadline and multi-block schedulability literature (representative; primary citation to be fixed).

[15] TLM Research Notes: **RN-05** (*Supply-side Heterogeneity and Temporal Granularity* — the quantum lattice, imported here as the supply substrate); **RN-11** (*The Term Structure and Allocation of Execution Capital in a Temporal Liquidity Market* — the canonical allocation program and its dual, and the block-fee-rate term structure).

---

## Status of This Draft

This is a research-framework draft, not a completed mathematical theory.

In particular:

- \(\mathcal{C}(\delta,I,\epsilon)\) is a proposed organizing object rather than an established capacity formula;
- the execution lattice requires a formal definition;
- monotonicity with finer temporal resolution depends on assumptions about subdivision overhead and physical constraints;
- information quantity \(I\) is fixed as a Blackwell information structure (\S20); a scalar surrogate for total-order questions remains to be chosen;
- no theorem yet establishes that richer temporal disclosure strictly increases capacity;
- no incentive-compatible reporting mechanism is assumed;
- blockchain physical limits, consensus limits, and execution-service limits must remain carefully separated;
- the analogies to fading channels, coherence time, multiuser diversity, rate-distortion theory, and communication complexity are research guides rather than claims of mathematical equivalence.

The next stage should therefore prioritize a minimal model, a small theorem, and simulation before further expansion of terminology.
