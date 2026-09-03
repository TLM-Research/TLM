---
id: RN-13
title: "Blockchain Execution Capacity Through a Temporal Liquidity Lens"
subtitle: "Bounds by Demand Class, and What They Say About Upgrading a Chain"
version: "0.7"
status: "Working draft, revised as the research proceeds"
replaces: "RN-13, withdrawn 1 September 2026"
program: "Temporal Liquidity Market (TLM)"
date: "September 2, 2026"
---

# RN-13 v0.7

# Blockchain Execution Capacity Through a Temporal Liquidity Lens

## Bounds by Demand Class, and What They Say About Upgrading a Chain

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-13**  
**Version:** 0.7  
**Status:** Working draft, revised as the research proceeds  
**Replaces:** the note withdrawn 1 September 2026  
**Date:** 2 September 2026

---

## Abstract

Transactions per second is not a poor measure of blockchain capacity. It is an exactly
correct measure for one demand distribution, and the error it makes on any other is what
this note is about.

We show that when every transaction is indifferent to *when* it executes, the capacity
region collapses to a simplex described by total resource, and neither finer scheduling
resolution nor richer demand information has any value. TPS is that case, stated exactly.
The converse is the useful direction: any capacity gain from resolution or information
**requires** temporal heterogeneity in demand. This gives the programme a null hypothesis it
lacked.

It also shows why a capacity bound with no demand assumption attached says nothing. Such a
bound must hold for the degenerate case too, so it can be no better than the resource bound.
Capacity statements have to name the demand class they hold for, and we use the Temporal
Execution Profile for single-slot structure and the Temporal Stream Profile across slots.
Four classes then admit two-sided bounds, three of them transposed from real-time
scheduling and network calculus and one exact. The periodic-service class yields a
utilization bound linear in the reciprocal of the lattice quantum, which makes the value of
temporal resolution a number rather than a direction.

The mixed-class region, where deadline jobs, periodic services, bursty flows and elastic
flows contend for the same quanta, is open. Every real chain serves such a mixture and none
of them models it.

**Appendix:** *A Survey of Capacity Theory under a Temporal Liquidity Lens*, published with
this note, which carries the imported results and the demand model each one assumes.

---

# 1. The question, and what is established here

Ethereum's fee interface carries `maxFeePerGas` and `maxPriorityFeePerGas`. A liquidation
worthless after two seconds and a treasury settlement due before market close bid into the
same auction with the same two numbers.

Whether that costs anything is empirical and not obviously yes. Serving them differently
requires the protocol to know more, and knowing more is not free: disclosure invites
extraction, verification costs, richer interfaces resist incentive compatibility. So the
question is not whether temporal information should be first class. It is what capacity
depends on, and how much of it the current interface forgoes.

**Established here.**

1. **The degenerate case (sec. 3).** When demand carries no temporal structure, capacity is
   total resource, TPS is exact, and both resolution and information have zero value.
2. **A bound with no demand assumption says nothing (sec. 3.4).** It must cover the
   degenerate case, so it reduces to the resource bound.
3. **Two-sided bounds, one demand class at a time (sec. 7).** Four classes, each with an
   upper bound, an achieving scheduler, and tightness stated. Three are transposed and
   attributed; the periodic-class result is derived here.
4. **Resolution has a class-dependent value (sec. 7.6).** \(\delta\) is irrelevant to the
   elastic class, discretizes the demand-bound function for deadlines, scales the periodic
   region linearly in \(1/\delta\), and sets burst absorption for bursty flows.
5. **An upgrade reading for Ethereum (sec. 9).** Which losses each candidate change
   recovers, and for which application classes.

**Not established.** No claim that the mixed-class region is characterised, that
\(I_{\min}\) is small, or that any fee mechanism is incentive compatible. RN-11 carries the
allocation program, RN-12 and RN-15 the mechanism design, RN-14 the demand evidence.

---

# 2. Capacity, and the two demand objects

## 2.1 The region

TPS is implementation-dependent: transaction sizes differ, computation differs, state access
differs. The more fundamental object is the set of workloads supportable under stated
service constraints. For \(n\) streams with offered load \(\boldsymbol{\lambda}\),

\[
\mathcal{C} = \{\boldsymbol{\lambda} : \text{some feasible scheduling policy satisfies the service constraints}\}.
\]

A system may support high aggregate throughput with a small region for low-latency
workloads, or lower peak throughput while multiplexing delay-tolerant streams well. One
scalar cannot separate these.

## 2.2 TEP and TSP as the input parameters

Two demand objects, at two time scales, and the note's central variables.

**Temporal Execution Profile (TEP)**, single-slot, per request. For request \(i\) under
variant \(j\),

\[
\mathrm{TEP}_{ij} = \bigl(F_{ij},\; v_{ij}(\cdot)\bigr),
\]

the admissible set of quanta and the value as a function of placement. Everything the
protocol could learn about *when within a slot* a transaction wants to run is in that pair.
RN-01 defines the object; RN-15 uses its smallest useful form, a signed scalar.

**Temporal Stream Profile (TSP)**, multi-slot, per source. For stream \(i\),

\[
\mathrm{TSP}_i = \bigl(T_i,\; \lambda_i,\; \tau_i^{\mathrm{req}},\; J_i,\; \sigma_i,\; \rho_i,\; V_i\bigr),
\]

duration, intensity, required inter-execution cadence, tolerated cadence jitter, burst size
and sustained rate, and value over time. RN-02 defines it.

**The capacity object this note studies takes both as arguments:**

\[
\mathcal{C}\bigl(\delta,\; I,\; \epsilon \;;\; P(\mathrm{TEP}), P(\mathrm{TSP})\bigr),
\]

the achievable region at lattice resolution \(\delta\), information structure \(I\), and
permitted service-violation probabilities \(\epsilon\), **taking the demand distributions as
parameters** rather than holding them fixed in the background. Section 3 shows why they
cannot be dropped from the argument list.

## 2.3 Temporal liquidity, read off the profile

The TEP is not only a descriptor. It is where temporal liquidity comes from, and reading it
that way is what connects a capacity statement to a market.

Define the **temporal liquidity** of request \(i\) as the value it retains when moved:

\[
\ell_i \;=\; \frac{1}{|F_{ij}|}\sum_{q \in F_{ij}} \frac{v_{ij}(q)}{\max_{q'} v_{ij}(q')} ,
\]

one when the request is indifferent across a wide admissible set, near zero when it is
pinned to a single quantum or its value collapses off the peak. Two things determine it,
and they are the two components of the TEP: **how wide \(F_{ij}\) is**, and **how flat
\(v_{ij}\) is across it**.

This gives the market's two sides a definition in the capacity model rather than by
assertion. A request with high \(\ell_i\) can be moved cheaply and is a **supplier** of
temporal liquidity; one with low \(\ell_i\) cannot and is a **consumer**. RN-15's signed
fee is the sign of \(\ell_i\) relative to the block's average, collapsed to one number, and
its two sides are these two.

**What follows for capacity.** The scheduler's gain comes from moving high-\(\ell\) work
away from quanta that low-\(\ell\) work cannot leave. So the achievable gain is not a
functional of any individual profile but of the **dispersion of \(\ell\) across the
population**. A block of uniformly patient transactions offers no gain, and neither does a
block of uniformly urgent ones. Both have suppliers or consumers but not both.

Stated as an identity the rest of the note works toward: the capacity gap
\(W^{*} - W_{\text{current}}\) **is the maximum gains from trade in temporal liquidity**, and
a market mechanism is measured by the fraction of it that gets realized. Section 8.2's
mechanism loss is exactly the unrealized fraction. The TSP carries the same reading one
level up, where \(\tau_i^{\mathrm{req}}\) and \((\sigma_i,\rho_i)\) say how far a *stream*
can be moved rather than a single request.

## 2.4 The demand that never arrives

Work passes through \(D^{P} \rightarrow D^{S} \rightarrow D^{A} \rightarrow D^{Q} \rightarrow D^{E}\),
potential to submitted, admitted, scheduled, executed. Each arrow is a filter the
architecture imposes, so measuring a chain by what it processes measures the survivors.

Three exclusion mechanisms, the third established in sec. 7.3:

- **Price exclusion**, \(V_i < P_i\). Feasible but uneconomic.
- **Latency exclusion**, \(D_i^{\max} < D_i^{\text{achievable}}\). Cannot meet its deadline.
- **Cadence exclusion**, \(\delta > \tau_i^{\mathrm{req}}\). The architecture cannot expose
  successive execution opportunities often enough, **whatever the throughput**.

## 2.5 What it takes for the scheduler to know something

Section 8 writes \(I\) for the information available to the scheduler and treats it as a
partition of the demand space. That abstraction is convenient for stating bounds and it
hides four separate conditions, each of which can fail on its own.

For a declaration to enter the allocation at all, it must be:

1. **Declared.** The sender states it, or the system infers it from observed behaviour. A
   profile nobody supplies and nothing estimates is not information.
2. **Delivered.** It reaches the point where ordering is decided, rather than being stripped
   at a relay or lost between mempool and builder.
3. **Readable there.** Whoever chooses the order can see it. A field encrypted until after
   sequencing is deliberately not readable at ordering time, which is sometimes the point.
4. **Binding.** Something makes the ordering follow it: a consensus validity rule, or an
   incentive that makes deviation unprofitable. Absent this, the declaration is advisory.

**Section 8's \(I\) assumes all four hold.** Every bound below is stated for information that
is declared, delivered, readable and binding, and a real interface satisfying only the first
three supports a strictly smaller region than the bound suggests.

**Today's priority fee is the instructive case.** It is declared, delivered, readable, and
**not binding**: builders order by it as a matter of practice and revenue, not because any
rule requires it. Under this note's model it is a perfectly good \(I\). Under RN-15 sec. 4.1
it is not enough, because a mechanism whose ordering rule cannot be enforced is inert.

Two of the four conditions are also in tension with each other, and the tension is not
resolved here. Making a profile readable at ordering time (3) exposes trading intent to
whoever reads it, so a design that hardens (4) by publishing declarations early can widen the
extraction channel. RN-01 sec. 6.1 states the same point from the demand side: **protocol-visible
is not the same as publicly revealed**, and *when* a field becomes visible is a design lever
distinct from whether it exists.

Which of the four a given upgrade satisfies is the practical question of sec. 9, and the
choice of \(I\) along these axes is an open dimension rather than a settled definition.

---

# 3. TPS is the degenerate case

## 3.1 Definition

A demand population is **temporally degenerate** if for every \(i,j\)

- **(D1)** \(F_{ij} = \{0,\ldots,Q-1\}\): no request restricted to a subset of quanta;
- **(D2)** \(v_{ij}(q) = v_{ij}\) for all \(q\): value independent of placement.

Every TEP flat and unrestricted. No deadlines, no windows, no value decay, no cadence.

## 3.2 Proposition

*Under (D1) and (D2), in the divisible relaxation at fixed per-horizon capacity
\(K_{\mathrm{tot}} = \sum_q K_q\):*

*(a)* \(W^{*}(\delta)\) *is independent of* \(\delta\), *so* \(G_{\delta} = 0\).

*(b)* \(V_I = 0\) *for every information structure refining* \((g_{ij}, v_{ij})\).

*(c)* \(\mathcal{C}\) *reduces to* \(\{\boldsymbol{\lambda} : \sum_i \lambda_i \bar{g}_i \le K_{\mathrm{tot}}\}\), *a simplex described by one scalar.*

**Proof.** Under (D2) the objective \(\sum_{i,j,q} v_{ij}(q)x_{ijq}\) becomes
\(\sum_{i,j} v_{ij}\sum_q x_{ijq}\). Write \(y_{ij} = \sum_q x_{ijq}\). Under (D1) nothing
ties \(y_{ij}\) to particular quanta, so the per-quantum constraints
\(\sum_{i,j} g_{ij}x_{ijq} \le K_q\) aggregate to
\(\sum_{i,j} g_{ij}y_{ij} \le K_{\mathrm{tot}}\); in the divisible relaxation any such \(y\)
is realisable by spreading \(x_{ijq}\) in proportion to \(K_q\). The program becomes

\[
\max_y \sum_{i,j} v_{ij}y_{ij}
\quad\text{s.t.}\quad
\sum_{i,j} g_{ij}y_{ij} \le K_{\mathrm{tot}},
\quad \sum_j y_{ij} \le 1,
\]

a fractional multiple-choice knapsack in which \(q\) does not appear. Resolution entered only
through \(Q\), and \(Q\) has been summed out, giving (a). The reduced data is
\((g_{ij}, v_{ij})\), so any structure revealing it attains the optimum and temporal
refinements add nothing, giving (b). Under (D1) there are no deadlines to violate, so
\(\epsilon\) is vacuous and the supportable set is fixed by \(K_{\mathrm{tot}}\), giving
(c). \(\square\)

**Scope.** The restriction of sec. 6.3: divisible relaxation, fixed per-horizon capacity.
Under indivisibility with \(K = K(\delta)\), part (a) can fail, but it fails toward *finer
resolution hurting*, since a job fitting a coarse quantum may fit no fine one. Absent
temporal heterogeneity, subdivision is at best free and at worst harmful.

## 3.3 The converse, and two null conditions that are not the same

Contrapositive of (a) and (b): **if \(G_\delta > 0\) or \(V_I > 0\), then (D1) or (D2)
fails.** Temporal structure is *necessary* for any gain on either axis, not merely helpful.

But the two axes do not die of the same cause, and separating them matters for what a market
can do.

**Indifference kills resolution.** If profiles are flat and unrestricted, there is no
placement worth optimising, so \(G_\delta = 0\). This is (D1) and (D2).

**Homogeneity kills information.** If every profile is *identical*, whatever its shape, the
scheduler learns nothing by being told, because knowing one request tells it all of them. So
\(V_I = 0\) whenever \(\ell_i\) has zero dispersion, even when every \(\ell_i\) is low.

These come apart. Take a population in which every request is pinned to the same quantum,
\(F_{ij} = \{q^{*}\}\) for all \(i\). It is maximally urgent and not indifferent, so
resolution can still help: subdividing \(q^{*}\) lets contending requests occupy distinct
sub-positions. But information is worthless, because the requests are indistinguishable.
Uniform urgency is degenerate on one axis and not the other.

**What this says about the market.** Section 2.3 defines \(\ell_i\); the gain from a
temporal liquidity market is a functional of its **dispersion**, not its level. A block of
uniformly patient transactions has suppliers and no consumers; a block of uniformly urgent
ones has consumers and no suppliers. Neither clears, and in neither case does a declaration
carry information the scheduler did not already have.

So the existence condition for a temporal liquidity market and the existence condition for
information-driven capacity gain are the same condition: **dispersion in \(\ell\)**. That is
a stronger statement than the note previously made and it is falsifiable, since \(\ell\)
dispersion is measurable from execution traces given a declared or inferred profile.

**The null hypothesis.** H-δ predicts zero under indifference; H-I predicts zero under
homogeneity; both predict zero under degeneracy, which implies both. A measurement showing
no gain on a near-degenerate workload confirms the theory rather than refuting it.

## 3.4 A bound with no demand assumption says nothing

A capacity bound holding for *every* demand distribution must hold for the degenerate one.
There capacity is exactly \(K_{\mathrm{tot}}\) by 3.2(c), and the bound is tight. **So the
execution-capacity bound that names no demand class is the resource bound**, and it says only
that you cannot spend more gas than exists.

Any capacity statement with content names the demand class it holds for. That is what
Liu and Layland do for periodic tasks, what Baruah does for sporadic ones, and what
effective-bandwidth theory does for stationary sources. Section 7 does it for TEP and TSP
classes.

## 3.5 The spectrum

| Demand | TEP / TSP structure | Is TPS right? |
|---|---|---|
| Uniform arrivals, no deadlines | degenerate | **Exactly correct** |
| Payments, transfers, retail flow | wide windows, slow decay | Good approximation |
| Recurring settlement, batches | cadence constraint, flat within it | Right on volume, wrong on feasibility |
| Oracle updates, periodic services | required cadence \(\tau^{\mathrm{req}}\) | Wrong: feasibility is \(\delta \le \tau^{\mathrm{req}}\) |
| Trading, liquidation, arbitrage | sharp decay, event-driven bursts | Wrong: measures **peak provisioning** |

The last row is worth separating. For event-driven demand the throughput a chain must supply
is set by the arrival **peak** while the capacity consumed is set by the **mean**.
Provisioning to peak leaves the system idle between events, and quoting peak as capacity
both overstates what can be sustained and understates what could be served if peaks of
different streams were interleaved. That interleaving is the multiplexing gain of sec. 7.5,
and no scalar can see it.

---

# 4. Four kinds of limit

A capacity theory exists to say which observed limits are fundamental and which are
artifacts. Four categories.

1. **Irreducible physical.** Signal propagation limited by geography and light speed.
2. **Hardware and resource.** Compute, memory bandwidth, state access, communication.
3. **Protocol-induced.** Consensus rounds, block intervals, ordering rules, commitment
   frequency.
4. **Architecture-induced coupling.** Independent physical processes forced to one cadence.

Categories 1 and 2 bound what the substrate can do; 3 and 4 bound what it is allowed to
express. Section 8.2's loss decomposition partitions the observed gap along the same seam,
and the correspondence covers those first two losses only.

The fourth category is the one worth naming, because nothing physical requires it and it is
the category most likely to be mistaken for a physical limit.

## 4.1 The physical floor

Before router, queueing, serialization, cryptographic or protocol overhead, one-way
propagation between nodes at distance \(d_{ij}\) obeys
\(T_{ij}^{\mathrm{prop}} \ge d_{ij}/c\). Only that term is irreducible; the rest is
engineering. Consensus additionally needs information to reach a sufficiently large and
distributed participant set, so minimum consensus time is constrained by geography,
propagation, bandwidth, topology, verification cost, quorum structure, adversarial
assumptions and protocol rounds.

---

# 5. The time-scale hierarchy

If every execution event required independent global consensus, propagation delay would
directly limit service cadence. Ordering can be determined more often than consensus, and
execution more often still. A model should distinguish

\[
\delta_{\mathrm{CPU}} \le \delta_{\mathrm{exec}} \le \delta_{\mathrm{order}} \le \Delta_{\mathrm{commit}} \le \Delta_{\mathrm{consensus}} .
\]

A conventional chain collapses several into one block interval; that collapse is category
four, not a physical necessity. Three consequences license what follows.

- **The lattice quantum need not equal the consensus slot.** It may reflect the finest
  economically meaningful and physically realizable execution or ordering opportunity, with
  consensus periodically committing a sequence of finer events.
- **Block time is not the fundamental minimum application execution interval.**
- **This note's own object is a collapse.** Everything below uses a single \(\delta\). The
  honest object is
  \(\mathcal{C}(\delta_{\mathrm{exec}}, \delta_{\mathrm{order}}, \Delta_{\mathrm{commit}}, \Delta_{\mathrm{consensus}}, I, \epsilon \mid P(\mathrm{TEP}), P(\mathrm{TSP}))\),
  and the single-\(\delta\) form assumes one temporal bottleneck binds.

The decoupling is established prior art: Narwhal and Tusk [11] separate dissemination from
ordering, Flow [12] consensus from execution, Block-STM [13] studies realizable parallelism.
**What is proposed here is not the decoupling but a capacity abstraction over it.**

---

# 6. The lattice

## 6.1 Definition

Let \(\delta\) be the temporal quantum; over horizon \(T\), \(q = 0,\ldots,Q-1\) with
\(Q = T/\delta\), and each quantum exposes resource \(K_q\). This is RN-05's quantum lattice
[16], imported as the capacity substrate. Let \(\Omega(T,\delta)\) be the feasible schedules,
incorporating computation limits, state conflicts, precedence, validator processing,
propagation, consensus timing and engine parallelism.

**Lattice richness is not capacity.** The growth rate
\(C_L(\delta) = \limsup_T \frac{1}{T}\log_2|\Omega(T,\delta)|\) has no demand or welfare
content and grows without bound as \(\delta \to 0\) unless \(K(\delta)\) constrains it. It is
a diagnostic of expressive richness, retained only to make that explicit.

## 6.2 Subdivision

With \(\delta = \Delta/m\), if subdivision does not reduce physical capability the feasible
set weakly expands, motivating
\(\mathcal{C}^{*} = \lim_{\delta \to 0}\mathcal{C}(\delta)\).

## 6.3 Exactly what is proved

**This is a relaxation argument with narrow scope.** It holds for the **divisible** program
at **fixed per-horizon capacity**: there, any coarse-feasible allocation maps to a
fine-feasible one of equal value.

It is **not** automatic for the indivisible program once \(K = K(\delta)\). A job whose
requirement \(g_{ij}\) fits a coarse quantum may fit no single finer quantum, so it can leave
the feasible set and **the inclusion can reverse**. The indivisible claim needs either
multi-quantum jobs occupying a contiguous run, or restriction to the fixed-\(K\) divisible
relaxation. Section 3.2 and the class bounds of sec. 7 inherit this scope.

## 6.4 Finer quanta are not free

Decreasing \(\delta\) adds scheduling decisions, state synchronization, metadata, commitment
load, coordination pressure and communication overhead, so \(K = K(\delta)\) and the
practical optimum is \(\delta^{*} = \arg\max_\delta M(\mathcal{C}(\delta; K(\delta)))\).

**The existence of an interior \(\delta^{*}\) is a hypothesis, not a corollary.** Section 6.2
gives monotonicity at fixed \(K\); sec. 6.4 removes fixed \(K\); whether the product has an
interior maximum for realistic \(K(\delta)\) is what sec. 10 must measure.

---

# 7. Bounds by demand class

The core of the note. For each class: an upper bound no scheduler can exceed, a scheduler
attaining or approaching it, and a statement of tightness. Transposed results are attributed;
the periodic-class bound is derived here.

## 7.1 Elastic class: exact

\(F_{ij}\) unrestricted, \(v_{ij}\) flat. By 3.2, the region is
\(\sum_i \lambda_i \bar g_i \le K_{\mathrm{tot}}\), attained by any feasible packing.
**Upper and lower bounds coincide.** This is TPS, and it is the only class for which a scalar
is sufficient.

## 7.2 Deadline TEP class: exact, transposed

Requests with release times and deadlines, \(F_{ij}\) a contiguous window. Baruah, Mok and
Rosier [18] give a necessary and sufficient condition: schedulable if and only if for all
\(t > 0\),

\[
h(t) = \sum_i C_i \max\left\{0, \left\lfloor \frac{t - D_i}{T_i}\right\rfloor + 1\right\} \le t .
\]

**Attained by EDF** on a divisible uniprocessor. The transposition replaces processor time
with per-quantum resource and \(C_i\) with gas requirement \(g_i\); the demand-bound function
becomes a *resource*-bound function evaluated on the lattice.

**Where \(\delta\) enters.** It discretizes \(h(t)\): the test is evaluated at quantum
boundaries, so a coarse lattice can only overestimate demand in an interval and reject
feasible workloads. Resolution buys accuracy in the admission test, not capacity directly.

**What breaks.** \(C_i\) is assumed known; on-chain the gas requirement is an estimate
verifiable only after execution. Tasks are assumed independent; state-conflicting
transactions are not. And no task misreports its deadline.

## 7.3 Periodic TSP class: two half-spaces, and \(\delta\) enters linearly

Persistent services with a required update cadence \(\tau_i^{\mathrm{req}}\): oracle feeds,
funding-rate updates, liquidation monitors, periodic settlement.

Over horizon \(T\) there are \(Q = T/\delta\) quanta, and let at most \(M\) meaningful state
transitions be exposed per quantum. Service \(i\) needs \(T/\tau_i^{\mathrm{req}}\)
transitions, so feasibility requires \(\sum_i T/\tau_i^{\mathrm{req}} \le M\,T/\delta\), that
is

\[
\boxed{\;\sum_i \frac{\delta}{\tau_i^{\mathrm{req}}} \;\le\; M \;}
\qquad\text{(cadence utilization)}
\]

alongside the ordinary resource-rate constraint

\[
\sum_i \frac{g_i}{\tau_i^{\mathrm{req}}} \;\le\; \frac{K_{\mathrm{tot}}}{T}
\qquad\text{(resource utilization)}.
\]

**The capacity region for this class is the intersection of two half-spaces.** Three
consequences.

**(i) TPS sees only the second.** The cadence constraint is invisible to any throughput
measure, and it is exactly cadence exclusion of sec. 2.4, now stated as *which constraint
binds*. A chain can be far inside its resource constraint and outside its cadence
constraint, processing a large volume while failing every service that needs frequent
updates.

**(ii) The region scales linearly in \(1/\delta\).** Halving the quantum doubles admissible
cadence utilization. **This makes the value of temporal resolution a number for this class**,
rather than a direction, and it is the sharpest form of H-δ available.

**(iii) The scheduling rule costs a constant.** By the transposition of Liu and Layland [17],
a fixed-priority rule assigned by rate attains only \(U \le n(2^{1/n}-1) \to \ln 2 \approx 0.693\)
of the bound, while EDF attains \(U \le 1\). **A chain scheduling by fee rather than by
urgency is in the first case**, and the gap is roughly thirty per cent of the cadence region,
lost to the priority rule alone.

**Scope.** Implicit deadlines (\(D_i = \tau_i^{\mathrm{req}}\)), independence, and the
divisible relaxation of sec. 6.3. Under indivisibility the constant degrades.

## 7.4 Bursty TSP class: transposed, deterministic

Streams characterised by a token-bucket arrival curve \(\alpha_i(t) = \sigma_i + \rho_i t\)
against a service curve \(\beta\). Network calculus [19] gives backlog and delay bounds
directly from their relationship, and the admissible region is the set of \((\sigma,\rho)\)
vectors the service curve dominates.

**Where \(\delta\) enters.** It sets burst absorption. A quantum of size \(\delta\) with
capacity \(K_q\) can absorb a burst of at most \(K_q\); finer quanta with proportionally
smaller \(K_q\) absorb less per quantum but offer more of them, so the effect on \(\sigma\)
tolerance is not monotone and depends on \(K(\delta)\).

**What breaks.** Blockchain bursts are frequently **correlated across streams**, because
several react to the same external price event. Network calculus handles adversarial bursts
but the correlated case is where its bounds are loosest, and it is the common case here.

## 7.5 Statistical TSP class: transposed, asymptotic

Stochastic sources with stationary structure. Effective-bandwidth theory gives an admissible
region \(\sum_i \alpha_i(\theta) \le C\) at a space parameter \(\theta\), strictly larger
than peak-rate provisioning. Tse, Gallager and Tsitsiklis [6] treat multiple time scales.

**The difference between this region and peak provisioning is the multiplexing gain**, and
it is a computable quantity. For the trading and liquidation row of sec. 3.5 it is the
difference between what a chain must build and what it must serve.

**What breaks.** Sources here are strategic, not stochastic, and a source that knows the
admission rule can shape its declared profile against it.

## 7.6 What the classes say jointly about \(\delta\)

| Class | Role of \(\delta\) |
|---|---|
| Elastic | irrelevant; capacity is \(K_{\mathrm{tot}}\) whatever \(\delta\) |
| Deadline TEP | discretizes the demand-bound test; buys admission accuracy |
| Periodic TSP | **scales the cadence region linearly in \(1/\delta\)** |
| Bursty TSP | sets burst absorption, non-monotone through \(K(\delta)\) |

**The value of temporal resolution is class-dependent**, which is a stronger and more useful
claim than "finer resolution enlarges the region". It also means a chain choosing \(\delta\)
is implicitly choosing which class it serves well.

## 7.7 The mixed region is open

Each class above has a characterisation. **Their mixture does not.** A substrate serving
deadline jobs, periodic services, bursty flows and elastic flows at once faces contention
for the same quanta among objectives that are not commensurable: a deadline miss, a cadence
violation and a throughput shortfall are different failures.

The region is not the intersection of the individual regions. Intersection would be correct
if each class were allocated a fixed share, but a fixed partition is exactly what a general
chain should avoid, since it recreates the app-chain assumption inside one chain. The
interesting region is the one attainable under *dynamic* sharing, and it is generally larger
than any fixed partition and smaller than the sum.

**This is the open problem, and it is the reason the note exists.** Every chain in the
appendix serves such a mixture, and none of them models it.

---

# 8. The benchmark, and what can be computed

## 8.1 The oracle

Assume physical resources and lattice fixed, true demand known, no misreporting,
unconstrained scheduling computation, all consistency and security constraints enforced.
Then \(W^{*}(\delta) = \max_{S \in \Omega(T,\delta)} W(D,S)\), and any practical mechanism
gives \(W_M(\delta,I) \le W^{*}(\delta)\).

The concrete program: decisions \(x_{ijq} \in \{0,1\}\), one placement per request, \(x_{ijq}=0\)
if \(q \notin F_{ij}\), per-quantum capacity respected, and
\(W^{*} = \max_x \sum_{i,j,q} v_{ij}(q)x_{ijq}\). This is RN-11's execution-capital allocation
problem in different notation; \(F_{ij}\) is the rectangular case of RN-11's decay function
\(\phi_i\). RN-11 owns the dual and its shadow-price reading.

## 8.2 Where the gap goes

Five losses: **physical** (outside the substrate's capability, categories 1 and 2 of sec. 4),
**temporal-resolution** (schedulable in principle, not expressible on the lattice, categories
3 and 4), **information** (flexibility exists but is not revealed), **mechanism** (revealed
but not exploited), and **strategic and verification** (a richer interface creates
manipulation and verification problems that reduce realizable gains).

The first two are what sec. 4 classifies and sec. 7 bounds. The third and fourth are sec. 8.4.
The fifth is RN-12's and RN-15's, and this note does not answer it.

## 8.3 The benchmark cannot be computed, and the class bounds are the answer

Two obstacles. The information is private and unverifiable. And \(W^{*}\) is a generalized
assignment problem, NP-hard in general.

\(W^{*}\) is not a side quantity; it is the denominator. **Every ratio this note asks for is
a ratio to something nobody can evaluate exactly.**

Three responses, in increasing order of usefulness.

**Bracket it.** The linear-programming relaxation, which is the divisible program of
sec. 6.3, gives \(W_{\mathrm{LP}} \ge W^{*}\). Any feasible schedule gives a lower bound, and
the LP-rounding algorithm of Fleischer, Goemans, Mirrokni and Sviridenko [20] guarantees
\(W_A \ge (1-1/e)W^{*}\). So \(W_A \le W^{*} \le \min(W_{\mathrm{LP}}, W_A/(1-1/e))\).

**Bracket the ratio, not the optimum.** Computing both sides with the same approximation and
dividing is wrong, since worst-case errors compound rather than cancel. The two-sided form
brackets the quantity of interest directly:

\[
\frac{W_A(I)}{W_{\mathrm{LP}}(I_{\mathrm{full}})} \;\le\; \eta \;\le\; \frac{W_{\mathrm{LP}}(I)}{W_A(I_{\mathrm{full}})} ,
\]

with width governed by the empirical integrality gap rather than the worst case.

**Use a class bound instead.** For a workload in one of the classes of sec. 7, the
class bound *is* a computable benchmark, and a tight one where the class result
is exact. This is why the class bounds matter beyond taxonomy: they replace an uncomputable
benchmark with computable ones wherever the workload is characterisable.

## 8.4 Capacity as a function of information

The protocol exposes \(X = f(D)\) and the scheduler allocates on \((X, L(\delta))\), under the
four conditions of sec. 2.5. \(I\) is an **information structure**, ordered in the **Blackwell** sense: \(I_1 \succeq I_0\) means
any allocation realizable under \(I_0\) is realizable under \(I_1\).

That definition does more work than it appears to. \(V_I \ge 0\) follows
immediately, so weak monotonicity of capacity in information is definitional and not a
finding. **All content is in strictness and magnitude**, and the testable claim is that the
gain is strictly positive and large enough to exceed disclosure, verification and extraction
cost. The order is also partial: two Blackwell-incomparable structures may not be ranked at
all, so intuitions of the form "more information helps" need this apparatus to be stated
safely.

Write \(\mathcal{C}^{\mathrm{full}}(\delta,\epsilon)\) for the full-information region **at
fixed** \(\delta\), distinct from \(\mathcal{C}^{*}\), the resolution limit of sec. 6.2.
Measuring an information result against the resolution benchmark would make an information
shortfall indistinguishable from a lattice that is too coarse.

**The minimum-information question.** Because the Blackwell order is partial, a minimum does
not generally exist. Fix a scalar cost \(c(I)\), a declared message length in bits, and
define

\[
I_{\min}(\eta) = \arg\min_{I} \bigl\{c(I) : M(\mathcal{C}(\delta,I,\epsilon)) \geq \eta\,M(\mathcal{C}^{\mathrm{full}}(\delta,\epsilon))\bigr\} .
\]

**The cheapest sufficient interface under a stated cost**, not the least informative one.
The ablation ladder of sec. 10 is a total order by construction, which is what makes this
estimable. Nisan and Segal [14] and Mount and Reiter [15] pose the same question for static
allocation; their result that any protocol finding an efficient allocation must also discover
supporting prices suggests capacity and pricing are less separable than treating them in
sequence implies. Nothing here establishes that correspondence.

---

# 9. Reading this for Ethereum

The theory's practical content is that **realized capacity can rise without physical capacity
rising**, by recovering losses two, three and four. This section says which change recovers
which loss, for which application class.

## 9.1 What Ethereum currently assumes

The interface expresses willingness to pay for **sooner inclusion** and nothing else. A
higher tip buys immediacy; a contract deadline only invalidates late execution rather than
informing the schedule; a nonce orders one sender's own transactions.

**The implicit TEP class is immediacy**, with \(\delta = \Delta\), the slot. Everything
faster is inexpressible and everything patient gains nothing by being patient. In the terms
of sec. 3.5, Ethereum has optimised for a demand distribution close to degenerate, while
serving a mixture that is not.

## 9.2 Ethereum holds the supply side of a market it does not run

The observation this section is for, and it follows from sec. 2.3 rather than from
advocacy.

Ethereum's stated purpose is neutral settlement, and it has succeeded at attracting exactly
that: treasury operations, bridge flow, batch settlement, DAO execution, periodic
rebalancing. **Those are high-\(\ell\) workloads.** They have wide admissible sets and slow
value decay, which is what makes them settlement rather than trading.

High-\(\ell\) work is temporal liquidity *supply*. So the base layer has accumulated a deep
supply side, and it currently pays that side nothing. A patient transaction posts the same
base fee as an urgent one, waits by resubmitting rather than by declaring, and receives no
compensation for flexibility it in fact has. The supply exists, is large, and is invisible
to the protocol.

Meanwhile the low-\(\ell\) side, perpetual trading, liquidation, high-frequency arbitrage,
has substantially left for chains built around it, which is what RN-14 documents. So the
composition has moved toward one side.

**This is the constraint on any two-sided mechanism at the base layer**, and it is a
sharper statement than "Ethereum should price time". RN-15's fee is budget-balanced within
a block, so it needs consumers and suppliers **in the same block**. Section 3.3 says
dispersion in \(\ell\) is what makes that possible, and sec. 9.1 says Ethereum's dispersion
has been falling. What follows is a condition and a measurement.

- The mechanism is worth most in blocks where a price event forces both sides to arrive
  together. Oracle updates read by patient rebalancers and impatient liquidators are the
  clearest case, and it is why RN-15 sec. 6 rests on it rather than on aggregate statistics.
- **Measuring \(\ell\) dispersion per block, not per day, is the empirical question that
  decides whether the mechanism has anything to clear.** An average over a day can look
  healthy while every individual block is one-sided.

The strategic reading is that Ethereum's problem is not a shortage of temporal liquidity. It
is that it has a large uncompensated supply and a departed demand side, and a mechanism that
compensates supply may be a precondition for the demand side returning rather than a
consequence of it. That ordering is a conjecture and is not established here.

## 9.3 Three changes, ordered by cost

**Intra-slot position declaration.** RN-15's temporal liquidity fee: a signed field pricing
position *within* the existing block, budget-balanced, no new protocol state, no change to
\(\Delta\). In these terms it sets \(\delta_{\mathrm{order}} < \Delta_{\mathrm{consensus}}\)
without touching consensus, recovering part of the **temporal-resolution loss** for the
deadline TEP class of sec. 7.2. It does not help the periodic class, because it changes
position within a slot rather than the number of transitions available across slots.

**Deadline and window declaration.** Letting a transaction state an admissible execution
window rather than only a price recovers **information loss** for patient demand, and turns
the admission test into sec. 7.2's demand-bound criterion. The gain is the difference between
scheduling by fee and scheduling by urgency, which sec. 7.3 quantifies for the periodic class
at roughly the \(\ln 2\) factor. This is the change with the best ratio of gain to protocol
disruption, and the one whose incentive problems are least understood.

**A sub-slot execution lattice.** Exposing \(m\) meaningful state transitions per slot moves
\(\delta\) to \(\Delta/m\) and, by sec. 7.3, scales the cadence region linearly in \(m\).
This is the only one of the three that removes cadence exclusion, and it is the largest
change, requiring the decoupling of sec. 5 to be real rather than conceptual.

## 9.4 Which applications each serves

| Change | Recovers | Serves |
|---|---|---|
| Intra-slot position (RN-15) | resolution loss, within slot | liquidation, arbitrage, anything contending for position |
| Window declaration | information loss | settlement, treasury operations, batch and bridge flow |
| Sub-slot lattice | cadence exclusion | oracle feeds, funding updates, order-book-like services |

**The ordering matters for a chain that has chosen neutral settlement as its purpose.**
Window declaration serves settlement flow, which is closest to Ethereum's stated target, and
requires no change to block cadence. The sub-slot lattice serves a class Ethereum has largely
ceded, which RN-14 documents, and is the expensive option. A chain should be explicit about
which of these it is buying.

## 9.5 What this does not claim

That any of the three is incentive compatible, that the gains exceed disclosure cost, or that
the mixture Ethereum serves is characterised. The first is RN-12 and RN-15; the second is
\(I_{\min}\); the third is sec. 7.7 and open.

**A separate argument, not established here.** A chain fixing its TEP assumptions is
optimised for today's mix and needs a protocol change when new application classes arrive,
whereas a chain carrying a demand-side interface adapts without one. That is an option-value
claim, it belongs to economics rather than capacity theory, and its support is RN-14 on
whether the mix moves and RN-01 sec. 2 on fragmentation. It does not follow from anything
above.

---

# 10. Hypotheses and measurement

**H-δ, resolution.** Finer scheduling resolution enlarges the achievable region when demand
carries meaningful sub-slot heterogeneity, with the gain class-dependent per sec. 7.6, and an
interior \(\delta^{*}\) exists for realistic \(K(\delta)\).

**H-I, information.** The gain from credible temporal demand information is strictly positive
and exceeds its disclosure, verification and extraction cost. *Weak positivity is
definitional (sec. 8.4); the content is strictness and magnitude.*

**H-min, sufficiency.** A low-dimensional profile attains most of the full-information region
at a cost far below full disclosure.

**Null hypothesis (sec. 3.3).** All three predict zero under temporal degeneracy.

**Stage 1, class bounds.** Verify each class bound of sec. 7 numerically on synthetic
workloads drawn from that class, and confirm the achieving schedulers attain them. This
validates the transpositions before anything is built on them.

**Stage 2, information ablation.** Hold the lattice fixed and climb the ladder: resource
demand only; plus price; plus deadline; plus window; plus stream duration and intensity; a
compact profile; full information. This is a total order by construction, which is what makes
\(I_{\min}\) estimable, and it is the most direct estimate available.

**Stage 3, the mixed region.** Two and then more classes contending for one lattice. Trace
the frontier under fixed partition, dynamic sharing, and oracle scheduling. **This is the
open problem of sec. 7.7 and the stage most likely to produce a result nobody has.**

**Stage 4, real traces.** Replay identical traces under multiple abstract schedulers across
Ethereum, a continuous-trading workload, a faster substrate and a parallel substrate,
separating the physical substrate effect from the resolution effect from the
information-interface effect. Report brackets per sec. 8.3, naming the approximation used.

---

# 11. Relation to other work, and open questions

The imported results and the demand model each assumes are in the appendix to this note,
*A Survey of Capacity Theory under a Temporal Liquidity Lens*, and are not repeated. In brief: Shannon [1] the method;
Goldsmith and Varaiya [2] that capacity moves with the allocator's information, transposed
here from supply side to demand side; Tse and Hanly [3, 4] the region rather than the scalar,
with Tse and Viswanath [5] on multiuser diversity, the mechanism by which heterogeneity
across users becomes a gain rather than a nuisance;
Tse, Gallager and Tsitsiklis [6] streams across time scales; Kelly [7, 8] prices from capacity
constraints, developed in RN-11; Yao [9] and, closer, Nisan and Segal [14] and Mount and
Reiter [15] the informational requirements of allocation; Liu and Layland [17] and Baruah,
Mok and Rosier [18] the per-class utilization bound, which is the template sec. 7
follows; network calculus [19] the burst characterisation; Prism [10] the consensus-layer
limits, complementary to the execution-layer question here.

**One transposition inverts rather than transfers.** In wireless the varying state is on the
supply side and is *measured*. Here it is on the demand side and is *declared*, so it can be
misreported, and every incentive question enters at that point with no counterpart in the
source literature. That is why the fifth loss of sec. 8.2 cannot be imported away.

## 11.1 Open questions

1. **The mixed-class region (sec. 7.7).** What is attainable under dynamic sharing among
   classes with non-commensurable failure modes? This is the note's central gap.
2. **Does an interior \(\delta^{*}\) exist** for realistic \(K(\delta)\), and where?
3. **How far do the transposed bounds survive** unknown execution cost, state conflicts and
   strategic declaration? Section 7.2's caveats apply to every borrowed row.
4. **What is \(I_{\min}\) empirically**, and how does it move with the class mixture?
5. **Which of sec. 2.5's four conditions can a real chain satisfy at once?** Readability at
   ordering time and resistance to extraction pull against each other, and no design here
   satisfies all four without cost.
6. **How can temporal information be elicited truthfully?** Every result here assumes
   declarations that mean what they say, and known impossibility results in transaction-fee
   mechanism design bound what is achievable.
7. **How much capacity does slot-level granularity strand in practice?** The measurement the
   theory exists to make askable, and the one that decides whether it was worth building.

---

# References

[1] C. E. Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, vol. 27, pp. 379-423 and 623-656, 1948.

[2] A. J. Goldsmith and P. P. Varaiya, "Capacity of Fading Channels with Channel Side Information," *IEEE Transactions on Information Theory*, vol. 43, no. 6, pp. 1986-1992, 1997. DOI: 10.1109/18.641562.

[3] D. N. C. Tse and S. V. Hanly, "Multiaccess Fading Channels, Part I: Polymatroid Structure, Optimal Resource Allocation and Throughput Capacities," *IEEE Transactions on Information Theory*, vol. 44, no. 7, pp. 2796-2815, 1998.

[4] S. V. Hanly and D. N. C. Tse, "Multiaccess Fading Channels, Part II: Delay-Limited Capacities," *IEEE Transactions on Information Theory*, vol. 44, no. 7, pp. 2816-2831, 1998.

[5] D. Tse and P. Viswanath, *Fundamentals of Wireless Communication*, Cambridge University Press, 2005.

[6] D. N. C. Tse, R. G. Gallager, and J. N. Tsitsiklis, "Statistical Multiplexing of Multiple Time-Scale Markov Streams," *IEEE Journal on Selected Areas in Communications*, vol. 13, no. 6, pp. 1028-1038, 1995.

[7] F. P. Kelly, "Charging and Rate Control for Elastic Traffic," *European Transactions on Telecommunications*, vol. 8, no. 1, pp. 33-37, 1997. DOI: 10.1002/ett.4460080106.

[8] F. P. Kelly, A. K. Maulloo, and D. K. H. Tan, "Rate Control for Communication Networks: Shadow Prices, Proportional Fairness and Stability," *Journal of the Operational Research Society*, vol. 49, no. 3, pp. 237-252, 1998. DOI: 10.1057/palgrave.jors.2600523.

[9] A. C.-C. Yao, "Some Complexity Questions Related to Distributive Computing," *STOC 1979*, pp. 209-213. DOI: 10.1145/800135.804414.

[10] V. Bagaria, S. Kannan, D. Tse, G. Fanti, and P. Viswanath, "Deconstructing the Blockchain to Approach Physical Limits," *ACM CCS 2019*. arXiv:1810.08092.

[11] G. Danezis, E. Kokoris-Kogias, A. Sonnino, and A. Spiegelman, "Narwhal and Tusk: A DAG-based Mempool and Efficient BFT Consensus," *EuroSys 2022*. arXiv:2105.11827.

[12] A. Hentschel, D. Shirley, and L. Lafrance, "Flow: Separating Consensus and Compute," 2019. arXiv:1909.05821.

[13] R. Gelashvili, A. Spiegelman, Z. Xiang, G. Danezis, Z. Li, D. Malkhi, Y. Xia, and R. Zhou, "Block-STM: Scaling Blockchain Execution by Turning Ordering Curse to a Performance Blessing," *PPoPP 2023*. arXiv:2203.06871.

[14] N. Nisan and I. Segal, "The Communication Requirements of Efficient Allocations and Supporting Prices," *Journal of Economic Theory*, vol. 129, no. 1, pp. 192-224, 2006. DOI: 10.1016/j.jet.2005.02.001.

[15] K. Mount and S. Reiter, "The Informational Size of Message Spaces," *Journal of Economic Theory*, vol. 8, no. 2, pp. 161-192, 1974. DOI: 10.1016/0022-0531(74)90012-X.

[16] TLM Research Notes: **RN-05** (*Supply-side Heterogeneity and Temporal Granularity*, the quantum lattice); **RN-11** (*The Term Structure and Allocation of Execution Capital*, the canonical allocation program and its dual).

[17] C. L. Liu and J. W. Layland, "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment," *Journal of the ACM*, vol. 20, no. 1, pp. 46-61, 1973. DOI: 10.1145/321738.321743.

[18] S. K. Baruah, A. K. Mok, and L. E. Rosier, "Preemptively Scheduling Hard-Real-Time Sporadic Tasks on One Processor," *Proceedings of the 11th IEEE Real-Time Systems Symposium*, pp. 182-190, 1990.

[19] J.-Y. Le Boudec and P. Thiran, *Network Calculus: A Theory of Deterministic Queuing Systems for the Internet*, Springer LNCS 2050, 2001.

[20] L. Fleischer, M. X. Goemans, V. S. Mirrokni, and M. Sviridenko, "Tight Approximation Algorithms for Maximum General Assignment Problems," *SODA 2006*, pp. 611-620.
