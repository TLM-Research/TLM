---
id: RN-13
title: "Capacity Theory for Execution Systems: A Survey under a Temporal Liquidity Lens"
subtitle: "What each result assumes about demand, what transfers to blockchain execution, and what the open agenda is"
version: "1.0"
status: "Public draft - survey note, offered in good faith for comment"
replaces: "RN-13, withdrawn 1 September 2026"
program: "Temporal Liquidity Market (TLM)"
date: "September 3, 2026"
---

# RN-13 v1.0

# Capacity Theory for Execution Systems

## A Survey under a Temporal Liquidity Lens

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-13, survey**  
**Version:** 1.0  
**Status:** Public draft - survey note, offered in good faith for comment  
**Replaces:** the note withdrawn 1 September 2026  
**Date:** 3 September 2026

---

## What this note is, and is not

**This is a survey.** It collects results established by others across information theory,
wireless capacity, real-time scheduling, network calculus, mechanism design and blockchain
systems work, and reads each for one thing: the assumption it makes about demand.

**It is not a set of new capacity results.** One short original result appears, in sec. 0,
because the survey's organising claim depends on it. Everything else belongs to the authors
cited.

**The research it serves is in progress and is not reported here.** The TLM programme is
working toward capacity statements for demand classes other than the degenerate one, and none
of that work is mature enough to state. Section 15 sets out that agenda explicitly, so a
reader can see what is being attempted and judge the survey as preparation for it.

### Why survey at all

A shared blockchain executes work for users whose demands differ in time. Some transactions
are worthless a second late; others can wait an hour. Asking what such a system can
fundamentally deliver, rather than what an implementation happens to deliver, is a capacity
question, and several fields have answered versions of it.

The organising question here is not "what did each field prove" but **"what did each field
assume about demand in order to prove it."** No capacity result is ever just "capacity is at
most \(X\)". Each carries an *if*: **if** demand is periodic with known periods, capacity is
at most this; **if** demand is elastic and always backlogged, at most that. Liu and Layland's
utilization bound means nothing without "for periodic tasks with implicit deadlines" attached
to it. That *if* is usually stated once and then left behind, and recovering it is what decides
whether a result transfers.

### How to read it

**Section 0** proves why the *if* cannot be dropped. It is the one original result, and it is
short.

**Sections 1 to 9** read the theory this way, one lineage at a time, each with the demand class
it assumed and where the transposition to execution breaks.

**Sections 10 to 13** read four existing chains the same way, for the demand class each design
implicitly assumes. These are interpretations of protocol behaviour, not protocol facts, and
are labelled as such.

**Section 14** collects what transfers, what breaks, and what none of these lineages supplies,
with an epistemic status against every row.

**Section 15** states the open agenda: what the programme is trying to establish, and what
would have to be true for it to succeed.

---

# 0. Why a capacity bound must name a demand class

## 0.1 The degenerate case

Let \(\delta\) be a scheduling quantum, \(q = 0,\ldots,Q-1\) over horizon \(T\), and let an
allocation place request \(i\) under variant \(j\) at quantum \(q\), written
\(x_{ijq} \in \{0,1\}\), subject to one placement per request and per-quantum capacity
\(K_q\), with \(K_{\mathrm{tot}} = \sum_q K_q\). Write \(g_{ij}\) for the resource
requirement and \(v_{ij}(q)\) for the value of placing the request at \(q\), and let
\(F_{ij}\) be its admissible set of quanta. The pair \((F_{ij}, v_{ij}(\cdot))\) is the
**Temporal Execution Profile** of RN-01, projected to what a capacity statement needs.

Call a demand population **temporally degenerate** if for every \(i,j\)

- **(D1)** \(F_{ij} = \{0,\ldots,Q-1\}\): no request is restricted to a subset of quanta;
- **(D2)** \(v_{ij}(q) = v_{ij}\) for all \(q\): value does not depend on placement.

Every profile flat and unrestricted. Nothing in the population cares *when* it runs.

**Proposition.** *Under (D1) and (D2), in the divisible relaxation at fixed per-horizon
capacity: (a) the optimum is independent of \(\delta\); (b) no information structure refining
\((g_{ij}, v_{ij})\) raises it; and (c) the achievable region is
\(\{\boldsymbol{\lambda} : \sum_i \lambda_i \bar g_i \le K_{\mathrm{tot}}/T\}\), one
scalar.*

**Proof.** Under (D2) the objective \(\sum_{i,j,q} v_{ij}(q)x_{ijq}\) becomes
\(\sum_{i,j} v_{ij}\sum_q x_{ijq}\). Write \(y_{ij} = \sum_q x_{ijq}\). Under (D1) nothing
ties \(y_{ij}\) to particular quanta, so the per-quantum constraints aggregate to
\(\sum_{i,j} g_{ij}y_{ij} \le K_{\mathrm{tot}}\), and in the divisible relaxation any such
\(y\) is realisable by spreading \(x_{ijq}\) in proportion to \(K_q\). The program becomes a
fractional multiple-choice knapsack in which \(q\) does not appear: resolution entered only
through \(Q\), which has been summed out, giving (a). The reduced data is
\((g_{ij}, v_{ij})\), so temporal refinements leave the optimum unchanged, giving (b). Under
(D1) there are no deadlines to violate, so the supportable set is fixed by
\(K_{\mathrm{tot}}\); dividing horizon counts by \(T\) gives (c). \(\square\)

**Scope.** Divisible relaxation, fixed per-horizon capacity. Under indivisibility with
resolution-dependent capacity the first part can fail, but it fails toward *finer resolution
hurting*, since a job fitting a coarse quantum may fit no fine one.

**So a scalar resource rate is the exact capacity of this population**, and transactions per
second is the further special case of homogeneous transaction size. Throughput is not a crude
proxy for capacity; it is capacity, for one specific demand distribution.

## 0.2 The consequence for how bounds are stated

A bound on the **gain available from temporal allocation** that holds for every demand
distribution must hold for the degenerate one, where by (a) and (b) that gain is zero.
**No such bound can improve on the resource bound**, which says only that you cannot spend
more resource than exists.

This is narrower than "demand-independent bounds say nothing", and the distinction matters:
bounds on communication, propagation and consensus are demand-independent and far from
vacuous, and Prism [10] is one. The claim is only about statements of the form *temporal
allocation can achieve at most \(X\)*, which must cover the class where it achieves nothing.

## 0.3 The converse, and what it does not say

Contrapositive: **if scheduling resolution or temporal information has any value, then (D1) or
(D2) fails.** Temporal structure in demand is *necessary* for either gain. That makes the
degenerate case a null hypothesis, since claims of the form "finer resolution enlarges what a
chain can serve" predict exactly zero under it.

Three things this does not say. It does not say temporal structure is *sufficient*:
heterogeneous profiles yield nothing if capacity never binds or if admissible sets do not
overlap. It does not say all information is worthless under degeneracy, since (b) is
conditional on \((g_{ij}, v_{ij})\) being known and only *additional temporal* disclosure is
covered. And it says nothing about how large the gain is for real demand.

**This is why the survey below is organised as it is.** Every result in it is a result about
some demand class, and the sections that follow recover which.

---

# Part I. The theory

## 1. Shannon: information is reduction of uncertainty

### 1.1 Entropy

Shannon's [1] measure of information is

\[
H(X) = -\sum_x p(x)\log p(x),
\]

and its defining feature is what it does **not** depend on. It does not depend on what the
symbols mean, only on how predictable they are. A message the receiver could have guessed
carries nothing however important its content, and \(H(X) = 0\) exactly when \(X\) is
certain.

**This is the information-theoretic form of sec. 0.3(b), and it needs the same conditioning
set.** Write \(Z\) for the non-temporal attributes a scheduler needs anyway, resource
requirement and value level, and \(D^{\mathrm{temp}}\) for the temporal profile given \(Z\). If
every request has the same temporal profile, a temporal declaration tells the scheduler
nothing further: \(H(D^{\mathrm{temp}} \mid Z) = 0\), so \(I(D^{\mathrm{temp}}; X \mid Z) = 0\).

**It does not follow that nothing can be learned.** Requests with identical temporal profiles
may still differ in gas, value, variant, state conflicts and dependencies, all of which a
scheduler can use. Only *additional temporal disclosure* is worthless, and every entropy
statement here carries \(Z\) with it.

**Entropy is not a synonym for dispersion.** \(H\) measures uncertainty about *which* type is
drawn. It says nothing about the economic distance between types, whether one can substitute
for another, or what distinguishing them is worth. Heterogeneity of discrete demand types can
be *measured* by the entropy of their type distribution; that is a different statement from
saying entropy is heterogeneity.

So a temporal field that every transaction sets to the same value carries nothing, however
many bits wide it is. Expressiveness is not information.

### 1.2 What a temporal declaration conveys

The object needed here is not \(H\) alone but the pair of quantities Shannon built from it,
and they map onto the TEP interface directly.

Let \(D\) be a transaction's true temporal demand and \(X = f(D)\) the profile it declares.
After seeing \(X\), the scheduler's remaining uncertainty about \(D\) is the **conditional
entropy** \(H(D \mid X)\), and what the declaration told it is the **mutual information**

\[
I(D;X) = H(D) - H(D \mid X).
\]

\(I(D;X)\) *is* the temporal information the interface carries. It is zero when the
declaration is independent of the truth, and maximal when the declaration determines it.

Two bounds follow immediately, and both matter for the minimum-information question.

- **A ceiling from demand, not from design.** \(I(D;X) \le H(D)\). No interface can convey
  more temporal information than demand heterogeneity contains, so widening the field past
  \(H(D)\) buys nothing, so the object worth asking for is the *cheapest sufficient*
  interface rather than the most expressive one.
- **A ceiling from the declaration.** \(I(D;X) \le H(X)\). A coarse field, say RN-15's few
  signed ticks, caps what can be learned regardless of how heterogeneous demand is. Choosing
  the field width is choosing how much of \(H(D)\) is reachable.

**The honest limit, which should not be skipped.** Entropy counts distinguishability, not
worth. Two demand populations can have identical \(H(D)\) while offering very different
capacity gains, because the distinctions in one may be economically trivial. Information
theory bounds what *can* be learned; it says nothing about what is worth learning.

Three objects should be kept apart:

- the **entropy or mutual information** of the demand-type distribution, in bits, which
  bounds what a declaration can convey;
- an individual request's **temporal flexibility**, coarsely a width statistic such as
  RN-11's \(W_i(\alpha)\), measured in quanta and omitting location and asymmetry; and
- the **allocative value** of that information, in units of welfare, which depends on
  congestion, on whether admissible sets overlap, and on whether a reassignment is feasible.

**These are three different units and the first does not bound the second.** A width statistic
has no entropy until it is treated as a random variable across requests; when \(W(\alpha)\) is
a deterministic function of the type, \(H(W(\alpha)) \le H(D)\), which is a statement about
the *declaration* of the width and not about the width itself. Nothing here determines the
third.

### 1.3 Two halves make a capacity claim

Shannon's channel capacity \(C = \max_{p(x)} I(X;Y)\) is the same mutual information, now
between a channel's input and output, and he established the pattern every capacity result in
this survey follows. A claim has two halves. **Achievability** exhibits a construction that
reaches the limit. **Converse** proves nothing can beat it. One half alone is not a capacity
claim: a construction without a converse might be beaten tomorrow, and a bound without a
construction might be unreachable.

The transfer to execution is the separation itself. **A throughput figure reports what an
implementation achieves; capacity states what the system permits**, and treating the first as
the second is the confusion Shannon removed from communication.

Section 0 supplies both halves for one class, the degenerate one, where the bound and the
attaining policy coincide. No other demand class treated below has both, which is the honest
measure of what remains open.

### 1.4 Separation, and a warning that transfers with it

Shannon also proved that source coding and channel coding can be done **separately** without
loss: compress to the source entropy, then encode for the channel, and the two-stage design
is optimal. This is the deepest architectural result in the theory, because it says the
interfaces can be drawn cleanly and each side designed on its own.

**The theorem is narrower than it is usually quoted.** It holds for one source over one
point-to-point channel. Cover, El Gamal and Salehi [21] showed that for **correlated sources
sharing a multiple-access channel** the separate design is strictly suboptimal: joint
source-channel coding can transmit source pairs that no two-stage design can, because the
correlation between the sources is itself usable at the channel and compressing each source
first destroys it.

**Both halves are architectural analogies, and neither is evidence about TLM.** Source and
channel coding under asymptotic probabilistic conditions is not the same problem as demand
description followed by market allocation, and the theorem does not show that RN-01 and RN-02
can define an interface independently of RN-12 and RN-15 without loss. **That separability is
a TLM research hypothesis**, not a corollary of Shannon.

The multiple-access result is the more useful half, as a warning rather than a proof.
Execution is a multiple-access setting, and demand sources are correlated in the way that
matters: several classes respond to the same external price event, so their profiles carry
mutual information that a per-transaction description discards. Whether a scheduler could use
that correlation is open, and it is the sharpest available reason to suspect a per-request
interface may be the wrong object.

### 1.5 What does not transfer

**Demand model assumed:** a source with a known statistical description. The apparatus
presumes you can characterise what arrives, and does not contemplate a source that chooses
its description strategically.

There is no literal channel, no noise model, and no execution analogue of a bit. The
transfer is the method and the entropy argument of sec. 1.2, not the formula.

## 2. Goldsmith and Varaiya: capacity moves with information

### 2.1 The result

A fading channel has a gain \(h\) that varies over time. Goldsmith and Varaiya [2] ask what
capacity it has under two information conditions: the receiver knows \(h\), or both the
transmitter and receiver know it.

With knowledge at both ends and an average power constraint \(\bar{P}\), capacity is

\[
C = \max_{P(h)\,:\,\mathbb{E}[P(h)] \le \bar{P}} \; \mathbb{E}\left[\log\left(1 + \frac{P(h)\,h}{N}\right)\right],
\]

and the optimal power allocation is **water-filling in time**: spend more when the channel
is good, less when it is poor, and nothing at all when \(h\) falls below a threshold.

\[
P^{*}(h) = \left(\frac{1}{\lambda} - \frac{N}{h}\right)^{+}
\]

The physical channel is identical in both cases. **What changes is that the allocator can
condition its action on a state it now observes**, and capacity rises accordingly.

### 2.2 The insight that transfers, and it is quantitative

The size of the gain is not constant. Adaptation is worth a great deal when power is scarce
relative to noise and very little when it is plentiful: as \(\bar{P}\) grows, the water-filling
solution flattens and the gain from knowing \(h\) vanishes. **Information about state is worth
most exactly when the resource is tight.**

That has an execution reading, and its force has to be stated carefully. The theorem
supports a **planner benchmark**: a decision-maker given costless, verifiable state it may
ignore has a weakly larger feasible set. It does not support the different claim that a
protocol's realised welfare rises after disclosure, because disclosure here costs
verification, invites extraction, and invites misreporting.

Within the benchmark, the useful part is the shape rather than the level. Temporal demand
information should be worth little in an uncongested block, where everything fits and
placement is unconstrained, and most when blocks are full and placement is contested. A
mechanism priced on temporal declarations should therefore show a gain that **scales with
congestion**, and a measurement finding constant gain across congestion levels would suggest
something is wrong with the measurement.

The threshold structure transfers too. Water-filling says some channel states get *nothing*:
below the cutoff, transmitting is not worth the power. The execution analogue is that under
scarcity some demand should receive no service at all in this period rather than a degraded
share of it, which is an admission decision rather than a scheduling one, and it is a
different discipline from a fee market that admits whatever pays.

### 2.3 The transposition inverts

**Demand model assumed:** continuously backlogged communication demand under an average
power constraint. The model does impose traffic, coding and power assumptions; what it does
not impose is *arrival timing*, because the source always has something to send. The varying
state is on the **supply** side: the channel changes and the scheduler learns about it.

In an execution system the interesting variation is on the **demand** side: users know their
deadlines, value decay, cadence, burst structure and flexibility, and the scheduler does not.
The object becomes latent state \(D\), a protocol representation \(X = f(D)\), and a
scheduler seeing \(X\).

**What breaks:** channel state is *measured*; demand state is *declared*. Water-filling never
has to ask whether \(h\) is lying. Every incentive-compatibility question enters at this
point and has no counterpart in the source literature, which is why no amount of borrowing
from it disposes of the incentive problem.

## 3. Tse and Hanly: the region, and three results inside it

Tse and Hanly [3, 4] study a channel shared by several users whose gains vary independently.
Three results matter here, and they say different things.

### 3.1 The capacity region has structure, not just shape

The throughput capacity region

\[
\mathcal{C} = \{(R_1,\ldots,R_n) : \text{jointly achievable in the long run}\}
\]

is a **polymatroid**: for every subset \(S\) of users the sum rate is bounded by a function
\(f(S)\) that is submodular, and the region's corner points are attained by successive
decoding in a fixed order. Submodularity is the formal statement of diminishing returns to
adding users to a set.

**What transfers:** the object, and the argument against TPS. Capacity is a region, not a
number. **What is worth testing rather than assuming:** whether an execution capacity region
has comparable structure. If the achievable region over demand classes were submodular in the
set of classes admitted, a great deal of machinery would follow, including greedy optimality
for admission. Nothing here claims it, and establishing it either way would be a substantial
result in its own right.

### 3.2 Multiuser diversity: the gain grows with the number of streams

Tse and Viswanath [5] show that serving whichever user currently has the best channel yields
a throughput growing like \(\log\log n\) in the number of users. The gain is real, it comes
from *heterogeneity across users* rather than from any improvement to the channel, and it
grows slowly.

**This is a candidate analogy for multiplexing heterogeneous workloads, and not more.** The
opportunistic gain exists because users differ and their peaks do not coincide, which suggests
why a shared substrate serving many classes might do better than a dedicated one serving few.
It does not establish it.

The \(\log\log n\) result does not transfer. Wireless diversity comes from independently
varying *measured* channel states under an opportunistic scheduler; blockchain classes are
correlated when several react to the same price event, are strategic rather than measured,
conflict in state, and are not freely preemptible. A blockchain gain of this kind needs its own
model of correlation, conflicts and temporal substitution, and the rate would be that model's
result, not this one's.

### 3.3 Delay-limited capacity can be zero

Part II [4] is the one people skip, and it carries the sharpest warning. If every user must
be guaranteed a fixed rate in *every* fading state rather than on average, the achievable
region can collapse, and for some fading distributions **delay-limited capacity is exactly
zero**. A channel with positive throughput capacity may support no hard guarantee at all.

**The execution reading, stated as motivation rather than implication.** The result concerns
fading channels and does not by itself imply anything about blockchain hard-deadline capacity.
What it does is motivate keeping average, probabilistic and hard guarantees as three separate
objects, since in at least one well-studied setting the third collapses while the first stays
large. That is why this note works with \(\Pr(D_i > d_i) \le \epsilon_i\). Whether a blockchain
strict-guarantee region can be empty requires an execution-specific reduction that nobody has
supplied.

### 3.4 What the assumption costs

**Demand model assumed:** infinitely backlogged users with elastic demand. Everyone always
has something to send and nobody has a deadline.

Mapped to execution, an always-backlogged source with no deadline has an unrestricted
admissible set and value independent of placement, which is the degenerate case of sec. 0. The
mapping has to be stated, since infinite backlog is a modelling device for removing arrival
timing rather than an observed demand class. Under it the *execution* region is a simplex and
a scalar suffices. The wireless region is non-trivial only because
**supply-side** variation supplies the structure that demand does not. Execution systems have
no equivalent supply-side fading, so the non-triviality has to come from the demand side, and
that is the whole difference between the two settings.

## 4. Which capacity: three service constraints

Wireless theory separates capacity concepts by service constraint, and execution theory
needs the same discipline.

- **Throughput capacity**: supportable in a long-run average sense.
- **Delay-limited capacity**: supportable under strict delay requirements.
- **Probabilistic service capacity**: for class \(i\) with delay \(D_i\) and deadline
  \(d_i\), impose \(\Pr(D_i > d_i) \le \epsilon_i\).

The third is one practical class among several, and it is where heterogeneous
\(\epsilon_i\) across classes becomes expressible: a liquidation service and a background
settlement stream can share a substrate while requiring very different violation
probabilities. This note works with it for a stated reason rather than a general one, that
sec. 3.3 below shows hard guarantees can collapse an achievable region in at least one
well-studied setting.
Which criterion is correct, hard constraint, expected delay, tail probability or a conditional
risk measure, is the application's to choose, and the taxonomy exists to expose that choice
rather than to settle it.

## 5. Real-time scheduling: the closest precedent

This is the nearest template for what a capacity bound stated for a named demand class looks
like, and the programme has cited it more often than it has used it.

**Liu and Layland [17].** For \(n\) periodic tasks with implicit deadlines, rate-monotonic
scheduling is feasible if utilization satisfies

\[
U = \sum_i \frac{C_i}{T_i} \le n\left(2^{1/n}-1\right) \;\longrightarrow\; \ln 2 \approx 0.693,
\]

while **EDF is feasible whenever \(U \le 1\)**. Two bounds, same demand class, differing
only by the scheduling rule.

**This does not extend to fee ordering, and the point is worth stating flatly because the
inference is tempting.** Rate-monotonic assigns fixed priority by inverse task period. Fee
priority, value priority and arbitrary fixed-priority rules bear no relation to period and
**inherit no part of this utilization guarantee**. Nothing licenses reading the \(\ln 2\)
factor as the cost of ordering a blockchain by fee.

**Baruah's processor-demand criterion [18].** For a **sporadic task system on one preemptive
processor, with independent tasks, known worst-case execution times and constrained deadlines**
(\(D_i \le T_i\)), the EDF test is *exact*, necessary and sufficient: schedulable if and only
if for all \(t > 0\),

\[
h(t) = \sum_i C_i \max\left\{0, \left\lfloor \frac{t - D_i}{T_i}\right\rfloor + 1\right\} \le t .
\]

**Demand model assumed:** periodic or sporadic tasks with a minimum inter-arrival separation,
known worst-case execution time, deadlines no later than the period, independent jobs, one
preemptive processor, and a trusted scheduler.

**The test is exact in continuous time.** Evaluating it on a lattice is a further step that
needs a rounding map for releases, deadlines, periods and execution requirements, and a proof
that the discretisation is conservative. Neither is supplied here, so the transposition to a
quantised execution substrate remains a conditional analogy rather than an exact test.

**What transfers:** the *shape of the result*. A named demand class yields a utilization
bound, and an achieving scheduler is exhibited. That is the form a capacity claim needs, and
the periodic class maps onto a persistent on-chain service with a required update cadence.

**What does not transfer is any statement about quantum size.** Liu and Layland compare
schedulers under a **fixed processor service rate**. A cadence argument that varies quantum
duration while holding transitions per quantum fixed changes transitions per second, and is
therefore a change in service capacity rather than a gain from resolution. Any cadence gain of that kind rests on a separate
blockchain architectural assumption, namely that the per-quantum cap is architecture-induced
rather than physical. It is not imported from real-time scheduling, and RN-04 sec. 8.1 states
independently that finer quanta create no per-slot capacity.

**What breaks:** worst-case execution time is assumed known, which on-chain is a gas
estimate that is only verifiable after execution; tasks are assumed independent, which
state-conflicting transactions are not; and no task lies about its period.

## 6. Network calculus and effective bandwidth: the bursty and statistical classes

Deterministic network calculus [19] characterises a source by an arrival curve, typically the
token bucket \(\alpha(t) = \sigma + \rho t\), and a server by a service curve \(\beta\).
Backlog and delay bounds follow directly from their relationship.

Tse, Gallager and Tsitsiklis [6] studied statistical multiplexing of multiple time-scale
Markov streams; effective-bandwidth theory gives an admissible region
\(\sum_i \alpha_i(\theta) \le C\) at a space parameter \(\theta\), which is strictly larger
than peak-rate provisioning. **The difference between the two is the multiplexing gain, and
it is a quantity, not a slogan.**

**Demand model assumed:** stochastic sources with stationary, characterisable structure, and
crucially, sources that do not respond strategically to the admission rule.

**What transfers:** the burst and stream abstractions, and the fact that peak provisioning
is not capacity. **What breaks:** blockchain demand is strategic, and bursts are often
*correlated across streams* because they respond to the same external event, which is
exactly the case statistical multiplexing handles worst.

## 7. Yao: how much must be communicated

Yao [9] founded communication complexity. Once a frontier is defined, it motivates lower
bounds on how much private information must cross the protocol boundary to approach it.

Capacity is primary and communication complexity secondary. The order cannot be reversed:
there is no asking how much information reaches a frontier that has not been defined.

**What breaks:** worst-case bounds, often loose for economic settings where average-case or
distributional statements are what matter.

## 8. Nisan and Segal, Mount and Reiter: the same question in economics

Mount and Reiter [15] formalised the informational size of a message space and proved the
competitive process minimal among a broad class of mechanisms realising a given goal. They
do not ask whether a mechanism is efficient, but how much participants must say before any
mechanism can be.

Nisan and Segal [14] asked how much communication is needed to find a value-maximizing
allocation, and showed that **any protocol which finds one must also discover supporting
prices**, in general personalized and nonlinear.

The second result is the one to sit with. If prices are not an add-on to an efficient
allocation but something the communication necessarily reveals, then a capacity frontier and
a price system are not separate objects to study in sequence.

**Demand model assumed:** static, no temporal substrate, no lattice. That gap is where
this programme operates.

## 9. Kelly: and why a fee-only interface is not a mistake

### 9.1 The result

Kelly [7, 8] poses network rate allocation as

\[
\max_{x \ge 0} \; \sum_i U_i(x_i) \quad \text{s.t.} \quad Ax \le C,
\]

users \(i\) with concave utility \(U_i\) for rate \(x_i\), routing matrix \(A\), link
capacities \(C\). Dualising the capacity constraints gives a price \(p_l\) per link, and the
problem separates: each user independently solves

\[
\max_{x_i \ge 0} \; U_i(x_i) - x_i \sum_{l \in \text{route}(i)} p_l ,
\]

while each link adjusts its price in response to aggregate load. The primal-dual dynamics
converge to the social optimum, and \(U_i = \log x_i\) gives proportional fairness.

### 9.2 The part that matters most to this programme

The striking feature is what the network does **not** need to know.

> **No link ever learns any user's utility function.** Each observes only its own aggregate
> load and publishes one scalar. That is sufficient for the decentralized allocation to reach
> the social optimum.

For elastic rate demand, the minimum sufficient interface is **one number per resource**, and
the direction of information flow is from the network to the user, not the reverse.

This is the strongest available prior on the minimum-information question, and it points the
opposite way from the TLM thesis for one class of demand. **Ethereum's fee-only interface
is not an oversight.**

The correspondence has to be stated at the right level. Kelly proves that a scalar congestion
price is sufficient **within the elastic-rate model**: divisible rates, concave utilities, and
specified primal-dual dynamics. EIP-1559 resembles that architecture, a scalar adjusted from
observed load that users best-respond to without revealing utilities, but it has discrete
transactions, strategic bidders, a target block size and a different update rule, so **it does
not inherit Kelly's welfare or convergence theorem**. What survives is the architectural
resemblance, which is enough to make the point.

The TLM claim has to be stated against that, not around it. It is not that price is
insufficient in general. It is that Kelly's sufficiency is **conditional on the elastic
class**, which is the degenerate case of sec. 0, and that the classes outside it are the
ones where a scalar price cannot carry what the scheduler needs. A deadline is not expressible
as a willingness to pay, because it is a constraint rather than a preference; a required
cadence is a property of a stream and not of any transaction in it.

### 9.3 What the model does not carry

**Demand model assumed:** elastic rate demand, divisible and infinitely backlogged, with
concave utility in rate alone.

Four things absent, and each is a demand class the programme has to treat: discrete indivisible jobs; deadlines
and admissible windows; value that decays with time rather than depending only on quantity;
and stream persistence, where the object being allocated to is a source with duration and
cadence rather than a flow.

The extension is from a rate market to a temporally differentiated execution market, where
dualising time-indexed capacity constraints gives **a vector of time-indexed resource shadow
prices** rather than a single price.

**That vector is not yet a term structure.** A financial term structure requires dated
contracts, settlement rules and spanning assumptions, and carries no-arbitrage conditions a
shadow-price vector need not satisfy. RN-11 constructs the market object and reads the duals
against it; the distinction is RN-11's to maintain, and this survey only supplies the dual.
RN-12 and RN-15 own the mechanism side.

---

# Part II. Existing chains, read for the demand they assume

Every chain embeds an implicit answer to "what does demand look like?" in its execution
interface. Naming that answer is what the temporal liquidity lens is for. The layer analysis
behind this part is RN-08; the per-chain analyses are RN-03 and RN-06.

**These are interpretations, not protocol fields.** No chain declares a TEP class. Each
heading below is a *TLM reading of the default execution interface*, and it compresses
transaction format, mempool policy, builder behaviour, execution architecture and application
convention into one label. Protocol facts and the reading of them should be kept apart, and
where a chain does something the label hides, that is said.

## 10. Ethereum: the immediacy assumption

The interface carries a fee and a tip. A higher tip buys **sooner inclusion** and expresses
nothing about later, scheduled or reserved execution. A contract can enforce a deadline, but
that only invalidates late execution rather than telling the protocol how to schedule before
it. A nonce fixes one sender's order and is not a scheduling preference.

**Implicit TEP class:** every transaction wants execution as soon as possible, and
differences among transactions are differences in willingness to pay for that.

**Implicit \(\tau_D\):** the slot, twelve seconds. Everything faster is invisible;
everything slower is unexpressed.

**Consequence:** demand that is genuinely patient has no way to say so and gains nothing by
being patient, while demand needing sub-slot cadence cannot be served at all. Both are
outside the assumed class, and both are the excluded demand RN-14 measures.

## 11. Aptos: concurrency, which is orthogonal

Block-STM executes a canonically ordered block speculatively in parallel, discovering
concurrency within a fixed order. The question it answers is: given an ordered block, how
can available concurrency be exploited safely?

**Implicit TEP class:** the same immediacy assumption as Ethereum. Parallelism changes how
much work fits in a slot, not which slot work wants.

**Worth stating precisely:** concurrency and temporal liquidity are orthogonal. A settlement
transaction may safely delay thirty blocks (high temporal liquidity) while conflicting with
many others once it runs (low parallelism); thousands of independent urgent payments are the
reverse.

**Consequence, as a TLM reading rather than a systems result:** Aptos raises \(K_q\), the
per-quantum capacity, and does not change the declaration interface. It moves the resource
constraint rather than the temporal one. The reading is conditional on the
architecture model: parallel execution can also affect latency and, through conflict rates,
the service a given transaction actually receives, neither of which \(K_q\) alone captures.

## 12. Monad: pipelining, which is also not scheduling

Monad targets EVM equivalence with optimistic parallel execution, asynchronous deferred
execution, pipelined consensus and execution, and a purpose-built state database (RN-06).

**The distinction that matters:** asynchronous execution decouples consensus from execution
in the *implementation* pipeline. The order is fixed and execution runs behind it. That is
not deferred user scheduling, which is a demand-side service choice.

**Implicit TEP class:** immediacy again, with a shorter slot.

**Consequence, conditional on the architecture model:** Monad reduces \(\Delta\) and so lowers
the floor on \(\delta\). Whether that enlarges the periodic-class region depends on how the
visible-transition cap \(M\), the physical service rate \(\mu\) and the execution lag scale
with the shorter block, and any such gain stops at the physical service rate \(\mu\). What can
be said without those assumptions is that a shorter commitment interval lowers a floor; whether
any service class crosses it is measurement. The consensus-execution seam Monad makes explicit
is also where a control engine would attach.

## 13. Hyperliquid: differentiation at two levels

RN-03 documents two distinct forms of temporal differentiation here, and they are not the
same mechanism.

**HyperCore against HyperEVM.** HyperCore is a purpose-built engine running on-chain order
books, margining, matching and liquidations, sharing HyperBFT consensus with HyperEVM. Two
materially different execution environments under one consensus.

**HyperEVM's dual block lanes**, which is the more relevant of the two for capacity classes.
One EVM state, two kinds of block: small blocks roughly every second at a low gas limit for
latency-sensitive traffic, large blocks roughly once a minute at a high gas limit for
deployments and heavy atomic work. **Separate mempools, separate base fees**, interleaved into
one block sequence over shared state. Lane selection is explicit and account-based rather than
inferred.

**Why the second matters here.** The large lane's value is not aggregate throughput, since
sixty small blocks exceed one large block in total gas. It is **single-block atomic capacity**:
a deployment too large for a small block cannot be split across several. So the lanes separate
*cadence* from *atomic block capacity*, which are two different dimensions and are conflated
by any single throughput figure. That is a production demonstration of the sec. 4 point that
capacity concepts have to be separated by service constraint.

**What generalises and what does not.** Both mechanisms show a chain need not assume one
demand class. But in each case the classes are **co-designed, co-governed and fixed at build
time**: serving a third means building it. That is the difference between hard-coding a
partition and exposing an interface that lets demand declare its own, which is what the
general case appears to require. It is a strong existence proof and not a general host.

## 13.1 The decoupling is prior art, and should not be claimed

Four of the chains above fuse consensus, ordering and execution to varying degrees, but the
research literature has already taken them apart, and any note in this area should say so
before claiming anything.

**Narwhal and Tusk** [11] separate reliable transaction dissemination from ordering, showing
the mempool can run at its own cadence independent of consensus. **Flow** [12] separates
consensus and ordering roles from execution and computation. **Block-STM** [13] shows how much
concurrency an ordered block actually admits. **Prism** [10] bounds consensus performance
against physical communication limits.

Together these establish that blockchain operation decomposes into subsystems with different
constraints and different natural time scales. **That observation is not available to be
claimed as new.** What the programme proposes is a capacity abstraction built over the
decomposition: given the time scales each subsystem admits, and given a demand distribution
over temporal profiles, what multiuser service region follows. The decoupling is the premise,
not the contribution.

---

# Part III

## 14. What transfers, what breaks, and what is missing

The rows below are not at the same level. Reading a framework as a benchmark is how the main
note reached two claims it has since withdrawn, so the status is stated first.

| Status | Meaning |
|---|---|
| **Benchmark** | a quantitative bound that survives a fully stated mapping to execution |
| **Layer bound** | quantitative, but for a different layer than the execution layer studied here |
| **Conditional** | applies only under assumptions not native to blockchain execution |
| **Taxonomy** | a classification that organises the question, not a bound |
| **Implementation** | a demonstrated method, not a limit |
| **Analogy** | suggests an object or a question, supplies no bound |
| **Open** | needs a new proof or a measurement before it supplies anything |

**No row is currently a Benchmark**, and that is the honest state of the transfer.

| Lineage | Status | What transfers | Demand class assumed | Where it breaks |
|---|---|---|---|---|
| Shannon | Analogy | limit-before-mechanism method; entropy bounds a declaration | characterisable source | no literal channel or bit; source is not strategic |
| Shannon separation | Analogy | interfaces may be separable | one source, one channel | fails for correlated multiple-access sources [21] |
| Goldsmith, Varaiya | Conditional | a planner's set grows with costless state | supply-side variation | state is measured there, **declared** here |
| Tse, Hanly | Analogy | capacity region, not scalar | elastic, infinitely backlogged | that class is the degenerate case of sec. 0 |
| Multiuser diversity [5] | Analogy | heterogeneity across users can be a gain | independent measured variation | correlated, strategic, conflicting here |
| Service-constraint taxonomy | Taxonomy | throughput / delay-limited / probabilistic | any, once \(\epsilon_i\) is stated | organises the question; supplies no bound |
| Liu, Layland [17] | Conditional | scheduling rule changes the guaranteed region | periodic, implicit deadlines, **priority by rate** | **no transfer to fee priority** |
| Baruah [18] | Conditional | exact schedulability test in continuous time | sporadic, known WCET, preemptive uniprocessor, constrained deadlines | WCET known only after execution; tasks conflict in state; lattice mapping unproved |
| Network calculus [19] | Open | \((\sigma,\rho)\) burst characterisation | deterministic arrival curves | no service curve stated for a chain; bursts event-correlated |
| Effective bandwidth | Open | multiplexing gain as a quantity | stationary stochastic sources | sources are strategic; specialisation missing |
| Yao | Analogy | minimum information to reach a target | worst case | often loose economically |
| Mount, Reiter; Nisan, Segal | Analogy | informational requirements; prices fall out | static allocation | no temporal substrate, no lattice |
| Kelly | Conditional | scalar price suffices for one class | divisible elastic rate, concave utility | EIP-1559 resembles it without inheriting the theorem |
| Prism [10] | Layer bound | physical, propagation and consensus limits | consensus layer | bounds consensus, not execution |
| Block-STM [13] | Implementation | realizable parallelism | any | a method, not a limit; effects beyond \(K_q\) unmodelled |

**Nothing above supplies the following, which is where original work is required.**

1. **A declared, strategic demand side.** Every lineage assumes demand state is measured or
   stochastic. Here it is announced by a party with an interest in the answer.
2. **A protocol-chosen temporal lattice.** Wireless has physical coherence time; real-time
   scheduling has a given task model. A blockchain **picks** its quantum, so temporal
   resolution is a design variable and not a given.
3. **Value heterogeneity across time.** Kelly has utility for rate, real-time scheduling has
   deadlines. Neither has value that decays continuously and differently per stream.
4. **This particular mixed-class region.** Each lineage characterises one demand class well.
   The surveyed lineages do not supply a region for a substrate serving deadline jobs,
   periodic services, bursty flows and elastic flows *at once* under strategic declaration,
   per-quantum blockchain capacity, value decay and enforceable ordering.

**Every claim above is limited to the lineages actually reviewed here.** "Nothing supplies
this" would be broader than the survey shows, and several literatures that plausibly bear on
it have not been read: **mixed-criticality scheduling**, which handles classes with
non-commensurable failure modes and is closest to the mixed-class problem; **multiclass queueing**;
**constrained Markov decision processes**; **stochastic network optimization**; and for
point 3 specifically, **scheduling with tardiness costs**, **soft real-time utility
functions**, **restless bandits** and **deadline-dependent rewards**, all of which model value
that varies with completion time.

**Until that pass is done, the originality boundary is provisional.** It should be read as a
statement about what this survey covers, not about what exists.

The chains in Part II plausibly receive heterogeneous workloads while their base interfaces do
not expose the class structure. Establishing the presence and scale of each class in each is
empirical work that RN-14 begins and does not finish.

---

# 15. The open agenda

The survey is preparation. This section states what it is preparation *for*, so the gap
between what is established and what is being attempted is visible rather than implied.

**None of the following is claimed. All of it is in progress.**

## 15.1 What the programme is trying to establish

**A capacity statement per demand class.** Section 0 supplies one, for the degenerate class,
where the bound and the attaining policy coincide. Four other classes are open, and each needs
both halves: an upper bound no scheduler exceeds, and a scheduler attaining or approaching it.

| Class | What exists | What is missing |
|---|---|---|
| Deadline-constrained | an exact continuous-time test (sec. 5) | a rounding map to a quantised lattice, and a proof it is conservative |
| Periodic service | a necessary cadence condition, under a one-transition-per-period assumption | sufficiency; an operational definition of a meaningful transition; treatment of batching and shared updates |
| Bursty | arrival-curve characterisation (sec. 6) | a service curve stated for a chain; treatment of event-correlated bursts |
| Statistically multiplexed | effective-bandwidth region (sec. 6) | specialisation to strategic rather than stochastic sources |

**The mixed-class region.** A substrate serving several classes at once faces contention among
objectives that are not commensurable: a deadline miss, a cadence violation and a throughput
shortfall are different failures with no common currency. The region is not the intersection
of the individual regions, since intersection would describe a fixed partition, and a fixed
partition recreates inside one chain the assumption an application-specific chain makes.

**Whether that region is genuinely open is itself unsettled**, and sec. 14 names the
literatures that have to be read before novelty is claimed.

## 15.2 What would have to be true for it to matter

Three empirical conditions, none of which this note establishes.

1. **Real demand is far from degenerate.** Section 0 shows the whole programme has zero value
   under temporal degeneracy. How far real chains sit from it is measurement, and it should be
   done per block rather than per day, since a daily aggregate can look mixed while every
   individual block is not.
2. **The gain exceeds the cost of obtaining it.** Temporal disclosure invites extraction,
   costs verification, and complicates incentive compatibility. The relevant quantity is net
   of all three, and it can be negative.
3. **Temporal declarations can be elicited truthfully.** Every allocation result surveyed here
   assumes declarations that mean what they say. Known impossibility results in
   transaction-fee mechanism design bound what is achievable, and where this programme sits
   against them is not yet stated.

## 15.3 What would falsify it

The degenerate case of sec. 0 gives a null hypothesis, which is worth stating as a target
rather than a footnote. **Claims that finer scheduling resolution or richer temporal
declaration enlarge what a chain can serve predict exactly zero gain under temporal
degeneracy.** A measurement finding no gain on a near-degenerate workload confirms the account;
one finding gain on a genuinely degenerate workload refutes it.

Two further outcomes would count against the programme rather than for it: a demonstration
that no ordering rule constraining position can be enforced against out-of-band agreement,
which would make declaration inert; and a measurement showing the disclosure cost of a useful
interface exceeds its allocative gain.

Where this note stands in the programme is that it establishes what capacity depends on, and
nothing about how much any of it is worth.

---

## References

Numbering is stable across the programme's capacity work, so entries keep their numbers when
material moves between documents. Gaps are intentional.

[1] C. E. Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, vol. 27, pp. 379-423 and 623-656, 1948.

[2] A. J. Goldsmith and P. P. Varaiya, "Capacity of Fading Channels with Channel Side Information," *IEEE Transactions on Information Theory*, vol. 43, no. 6, pp. 1986-1992, 1997.

[3] D. N. C. Tse and S. V. Hanly, "Multiaccess Fading Channels, Part I," *IEEE Transactions on Information Theory*, vol. 44, no. 7, pp. 2796-2815, 1998.

[4] S. V. Hanly and D. N. C. Tse, "Multiaccess Fading Channels, Part II: Delay-Limited Capacities," *IEEE Transactions on Information Theory*, vol. 44, no. 7, pp. 2816-2831, 1998.

[5] D. Tse and P. Viswanath, *Fundamentals of Wireless Communication*, Cambridge University Press, 2005.

[6] D. N. C. Tse, R. G. Gallager, and J. N. Tsitsiklis, "Statistical Multiplexing of Multiple Time-Scale Markov Streams," *IEEE Journal on Selected Areas in Communications*, vol. 13, no. 6, pp. 1028-1038, 1995.

[7] F. P. Kelly, "Charging and Rate Control for Elastic Traffic," *European Transactions on Telecommunications*, vol. 8, no. 1, pp. 33-37, 1997.

[8] F. P. Kelly, A. K. Maulloo, and D. K. H. Tan, "Rate Control for Communication Networks: Shadow Prices, Proportional Fairness and Stability," *Journal of the Operational Research Society*, vol. 49, no. 3, pp. 237-252, 1998.

[9] A. C.-C. Yao, "Some Complexity Questions Related to Distributive Computing," *STOC 1979*, pp. 209-213.

[10] V. Bagaria, S. Kannan, D. Tse, G. Fanti, and P. Viswanath, "Deconstructing the Blockchain to Approach Physical Limits," *ACM CCS 2019*. arXiv:1810.08092.

[11] G. Danezis, E. Kokoris-Kogias, A. Sonnino, and A. Spiegelman, "Narwhal and Tusk," *EuroSys 2022*. arXiv:2105.11827.

[12] A. Hentschel, D. Shirley, and L. Lafrance, "Flow: Separating Consensus and Compute," 2019. arXiv:1909.05821.

[13] R. Gelashvili et al., "Block-STM: Scaling Blockchain Execution by Turning Ordering Curse to a Performance Blessing," *PPoPP 2023*. arXiv:2203.06871.

[14] N. Nisan and I. Segal, "The Communication Requirements of Efficient Allocations and Supporting Prices," *Journal of Economic Theory*, vol. 129, no. 1, pp. 192-224, 2006.

[15] K. Mount and S. Reiter, "The Informational Size of Message Spaces," *Journal of Economic Theory*, vol. 8, no. 2, pp. 161-192, 1974.

[17] C. L. Liu and J. W. Layland, "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment," *Journal of the ACM*, vol. 20, no. 1, pp. 46-61, 1973.

[18] S. K. Baruah, A. K. Mok, and L. E. Rosier, "Preemptively Scheduling Hard-Real-Time Sporadic Tasks on One Processor," *Proceedings of the 11th IEEE Real-Time Systems Symposium*, pp. 182-190, 1990.

[19] J.-Y. Le Boudec and P. Thiran, *Network Calculus: A Theory of Deterministic Queuing Systems for the Internet*, Springer LNCS 2050, 2001.

[21] T. M. Cover, A. El Gamal, and M. Salehi, "Multiple Access Channels with Arbitrarily Correlated Sources," *IEEE Transactions on Information Theory*, vol. IT-26, no. 6, pp. 648-657, 1980. DOI: 10.1109/TIT.1980.1056273.
