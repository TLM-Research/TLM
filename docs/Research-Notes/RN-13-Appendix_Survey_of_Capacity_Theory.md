---
id: RN-13-Appendix
title: "RN-13 Appendix: A Survey of Capacity Theory under a Temporal Liquidity Lens"
subtitle: "What each result assumes about demand, and what transfers to blockchain execution"
status: "Working draft, revised as the research proceeds"
program: "Temporal Liquidity Market (TLM)"
version: "0.2"
date: "September 2, 2026"
---

# RN-13 Appendix

# A Survey of Capacity Theory under a Temporal Liquidity Lens

## What each result assumes about demand, and what transfers to blockchain execution

**Temporal Liquidity Market (TLM) Research Program**  
**Appendix to Research Note RN-13**, published with it  
**Version:** 0.2  
**Status:** Working draft, revised as the research proceeds  
**Date:** 2 September 2026

---

## What this document is

A shared blockchain executes work for users whose demands differ in time. Some transactions
are worthless a second late; others can wait an hour. Asking what such a system can
fundamentally deliver, rather than what an implementation happens to deliver, is a capacity
question, and several fields have answered versions of it.

This appendix surveys results established by others and organises them for use in RN-13,
which draws its citations from here. It is referenced from RN-13 sec. 11 and kept separate so
that the note can state its own results without also setting out the prior work they rest on.

The organising question is not "what did each field prove" but **"what did each field assume
about demand in order to prove it."** No capacity result is ever just "capacity is at most
\(X\)". Each carries an *if*: **if** demand is periodic with known periods, capacity is at
most this; **if** demand is elastic and always backlogged, at most that. Liu and Layland's
utilization bound means nothing without "for periodic tasks with implicit deadlines" attached
to it.

That *if* is usually stated once and then left behind. Recovering it is what decides whether
a result transfers to execution systems, and where it breaks if it does.

Sections 1 to 9 read the theory this way. Sections 10 to 13 read four existing chains the
same way, for the demand class each design assumes. Section 14 collects what transfers, what
breaks, and what none of these lineages supplies.

**Why the *if* cannot be dropped.** RN-13 shows that a bound holding for *every* demand
distribution must in particular hold for the temporally degenerate one, where capacity is
total resource and no temporal structure helps. A bound with no *if* is therefore the
resource bound, and says only that you cannot spend more gas than exists.

So what follows records which demand class each lineage assumed, what it proved for that
class, and what the assumption cost it elsewhere.

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

**This is the formal basis for a claim RN-13 makes on its own account.** RN-13 sec. 3.3 argues
that homogeneous demand makes temporal declarations worthless: if every request declares the
same profile, the scheduler learns nothing by being told, even when every request is urgent.
That is \(H = 0\) for a certain distribution, restated in a scheduling setting. **The
dispersion of demand types is the entropy of the type distribution.**

So a temporal field that every transaction sets to the same value carries nothing, however
many bits wide it is. Expressiveness is not information.

### 1.2 What a temporal declaration conveys

The object RN-13 needs is not \(H\) alone but the pair of quantities Shannon built from it,
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
  \(H(D)\) buys nothing. This is why RN-13 asks for the *cheapest sufficient* interface
  rather than the most expressive one.
- **A ceiling from the declaration.** \(I(D;X) \le H(X)\). A coarse field, say RN-15's few
  signed ticks, caps what can be learned regardless of how heterogeneous demand is. Choosing
  the field width is choosing how much of \(H(D)\) is reachable.

**The honest limit, which should not be skipped.** Entropy counts distinguishability, not
worth. Two demand populations can have identical \(H(D)\) while offering very different
capacity gains, because the distinctions in one may be economically trivial. Information
theory bounds what *can* be learned; it says nothing about what is worth learning. RN-13's
dispersion of \(\ell\) is the value-weighted quantity, and it is not an entropy.

### 1.3 Two halves make a capacity claim

Shannon's channel capacity \(C = \max_{p(x)} I(X;Y)\) is the same mutual information, now
between a channel's input and output, and he established the pattern every capacity result in
this survey follows. A claim has two halves. **Achievability** exhibits a construction that
reaches the limit. **Converse** proves nothing can beat it. One half alone is not a capacity
claim: a construction without a converse might be beaten tomorrow, and a bound without a
construction might be unreachable.

The transfer to execution is the separation itself. **TPS reports what an implementation
achieves; capacity states what the system permits**, and treating the first as the second is
the confusion Shannon removed from communication.

RN-13 sec. 7 follows this shape deliberately. Each demand class is given an upper bound no
scheduler can exceed and a named scheduler attaining or approaching it, with the gap stated.
Where the two halves meet, the class is solved; where they do not, the gap is the honest
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

**This bears on the TLM architecture, and it cuts both ways.** The programme assumes demand
*description* (the TEP and TSP) separates cleanly from *allocation* (the mechanism), so that
RN-01 and RN-02 define an interface while RN-12 and RN-15 design a market against it. The
point-to-point separation theorem is why that architecture is plausible at all.

The multiple-access result is why it is an assumption rather than a consequence. Execution is
a multiple-access setting, and the demand sources are correlated in exactly the way that
matters: several classes respond to the same external price event, so their profiles carry
mutual information that a per-transaction description discards. Whether that lost correlation
is worth anything to a scheduler is open, and it is the sharpest available argument that a
per-request interface may be the wrong object.

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

That has a direct execution reading, and it is one of the more useful things this survey
carries into RN-13. Temporal demand information should be worth little in an uncongested
block, where everything fits and placement is unconstrained, and worth most when blocks are
full and placement is contested. A mechanism priced on temporal declarations should therefore
show a gain that **scales with congestion**, and a measurement finding constant gain across
congestion levels would be evidence something is wrong with the measurement.

The threshold structure transfers too. Water-filling says some channel states get *nothing*:
below the cutoff, transmitting is not worth the power. The execution analogue is that under
scarcity some demand should receive no service at all in this period rather than a degraded
share of it, which is an admission decision rather than a scheduling one, and it is a
different discipline from a fee market that admits whatever pays.

### 2.3 The transposition inverts

**Demand model assumed:** none, and this is the point. The varying state is on the **supply**
side. The channel changes and the scheduler learns about it.

In an execution system the interesting variation is on the **demand** side: users know their
deadlines, value decay, cadence, burst structure and flexibility, and the scheduler does not.
The object becomes latent state \(D\), a protocol representation \(X = f(D)\), and a
scheduler seeing \(X\).

**What breaks:** channel state is *measured*; demand state is *declared*. Water-filling never
has to ask whether \(h\) is lying. Every incentive-compatibility question enters at this
point and has no counterpart in the source literature, which is why the fifth loss in RN-13's
decomposition cannot be imported away.

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
for admission. RN-13 does not claim it, and establishing it either way would be a substantial
result in its own right.

### 3.2 Multiuser diversity: the gain grows with the number of streams

Tse and Viswanath [5] show that serving whichever user currently has the best channel yields
a throughput growing like \(\log\log n\) in the number of users. The gain is real, it comes
from *heterogeneity across users* rather than from any improvement to the channel, and it
grows slowly.

**This is the closest thing in the literature to an argument for a general-purpose chain over
an app chain.** The opportunistic gain exists only because users differ and their peaks do
not coincide. One class of demand on a dedicated substrate has no such gain to collect; many
heterogeneous classes on a shared substrate do.

Two cautions before the analogy is leaned on. The \(\log\log n\) rate is slow, so this is not
an argument that more classes are dramatically better. And wireless diversity comes from
*independent* variation, whereas blockchain demand peaks are frequently correlated because
several classes respond to the same price event, which is the case where the gain is
smallest.

### 3.3 Delay-limited capacity can be zero

Part II [4] is the one people skip, and it carries the sharpest warning. If every user must
be guaranteed a fixed rate in *every* fading state rather than on average, the achievable
region can collapse, and for some fading distributions **delay-limited capacity is exactly
zero**. A channel with positive throughput capacity may support no hard guarantee at all.

**The execution reading:** a system that guarantees a hard deadline to every request may have
a much smaller achievable region than one guaranteeing it to some, and under adverse demand
the strict-guarantee region can be empty while the average-service region is large. This is
the formal reason RN-13 works with probabilistic service constraints
\(\Pr(D_i > d_i) \le \epsilon_i\) rather than hard deadlines, and it is an argument against
any proposal to give every transaction a guarantee.

### 3.4 What the assumption costs

**Demand model assumed:** infinitely backlogged users with elastic demand. Everyone always
has something to send and nobody has a deadline.

That assumption is exactly RN-13's temporally degenerate case. Under it the *execution*
region is a simplex and a scalar suffices. The wireless region is non-trivial only because
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

The third is the realistic one, and it is where heterogeneous \(\epsilon_i\) across classes
becomes expressible. A liquidation service and a background settlement stream can share a
substrate while requiring very different violation probabilities.

## 5. Real-time scheduling: the closest precedent

This is the literature RN-13 previously listed and never used, and it is the nearest
template for what a capacity bound stated for a named demand class looks like.

**Liu and Layland [17].** For \(n\) periodic tasks with implicit deadlines, rate-monotonic
scheduling is feasible if utilization satisfies

\[
U = \sum_i \frac{C_i}{T_i} \le n\left(2^{1/n}-1\right) \;\longrightarrow\; \ln 2 \approx 0.693,
\]

while **EDF is feasible whenever \(U \le 1\)**. Two bounds, same demand class, differing
only by the scheduling rule.

**Baruah's processor-demand criterion [18].** For sporadic tasks the test is *exact*, necessary
and sufficient: schedulable if and only if for all \(t > 0\),

\[
h(t) = \sum_i C_i \max\left\{0, \left\lfloor \frac{t - D_i}{T_i}\right\rfloor + 1\right\} \le t .
\]

**Demand model assumed:** periodic or sporadic tasks, known worst-case execution time,
deadlines tied to periods, independence, a trusted scheduler.

**What transfers:** the *shape of the result*. A named demand class yields a utilization
bound, and an achieving scheduler is exhibited. That is precisely the form RN-13 needs, and
the periodic class maps onto a persistent on-chain service with a required update cadence.

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
RN-13 operates.

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

This is the strongest available prior on RN-13's minimum-information question, and it points
the opposite way from the TLM thesis for one class of demand. **Ethereum's fee-only interface
is not an oversight.** For elastic, deadline-free, placement-indifferent demand, Kelly proves
a price is enough, and EIP-1559's base fee is recognisably a Kelly price on a single
congested resource: a scalar, adjusted by observed load, that users best-respond to without
revealing anything.

The TLM claim has to be stated against that, not around it. It is not that price is
insufficient in general. It is that Kelly's sufficiency is **conditional on the elastic
class**, which is precisely RN-13's degenerate case, and that the classes outside it are the
ones where a scalar price cannot carry what the scheduler needs. A deadline is not expressible
as a willingness to pay, because it is a constraint rather than a preference; a required
cadence is a property of a stream and not of any transaction in it.

### 9.3 What the model does not carry

**Demand model assumed:** elastic rate demand, divisible and infinitely backlogged, with
concave utility in rate alone.

Four things absent, and each is a class in RN-13 sec. 7: discrete indivisible jobs; deadlines
and admissible windows; value that decays with time rather than depending only on quantity;
and stream persistence, where the object being allocated to is a source with duration and
cadence rather than a flow.

The extension is from a rate market to a temporally differentiated execution market, where
the dual variable is no longer one price per resource but a **price per resource per time**,
which is a term structure. RN-11 develops that object and its shadow-price reading; RN-12 and
RN-15 own the mechanism side.

---

# Part II. Existing chains, read for the demand they assume

Every chain embeds an implicit answer to "what does demand look like?" in its execution
interface. Naming that answer is what the temporal liquidity lens is for. The layer analysis behind this part
is RN-08; the per-chain analyses are RN-03 and RN-06.

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

**Consequence:** Aptos raises \(K_q\), the per-quantum capacity, and leaves \(\delta\) and
\(I\) untouched. In RN-13's terms it moves the resource constraint and not the temporal one.

## 12. Monad: pipelining, which is also not scheduling

Monad targets EVM equivalence with optimistic parallel execution, asynchronous deferred
execution, pipelined consensus and execution, and a purpose-built state database (RN-06).

**The distinction that matters:** asynchronous execution decouples consensus from execution
in the *implementation* pipeline. The order is fixed and execution runs behind it. That is
not deferred user scheduling, which is a demand-side service choice.

**Implicit TEP class:** immediacy again, with a shorter slot.

**Consequence:** Monad reduces \(\Delta\) and therefore lowers the floor on \(\delta\). Under
the periodic-class bound this enlarges the cadence region proportionally, which is a real
capacity gain for cadence-bound services and is invisible in a TPS comparison. The
consensus-execution seam Monad makes explicit is also where a control engine would attach.

## 13. HyperCore: two classes, hard-coded

HyperCore is Hyperliquid's specialized execution component, on-chain order books, margin,
matching and liquidations, sharing HyperBFT consensus with HyperEVM (RN-03).

**Implicit TEP class:** two of them, and this is what makes it the interesting case. The
order-book domain assumes low jitter, consistent ordering, cancellation responsiveness and
liquidation priority. The EVM domain assumes general-purpose immediacy.

**Consequence, and the reason it matters to RN-13:** HyperCore is an existence proof that
two materially different execution environments can share one consensus, and therefore that
a chain need not assume a single TEP class. But the two classes are **co-designed,
co-governed and fixed at build time**. Serving a third class means building it. That is
precisely the difference between hard-coding a TEP partition and exposing an interface that
lets demand declare its own, which is what RN-13 argues the general case requires.

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
claimed as new.** What RN-13 proposes is the capacity abstraction built over the decomposition:
given the time scales each subsystem admits, and given a demand distribution over TEP and TSP
classes, what multiuser service region follows. The decoupling is the premise, not the
contribution.

---

# Part III

## 14. What transfers, what breaks, what nobody supplies

| Lineage | What transfers | Demand class assumed | Where it breaks |
|---|---|---|---|
| Shannon | limit-before-mechanism method | characterisable source | no literal channel or bit |
| Goldsmith, Varaiya | capacity depends on the allocator's information | supply-side variation | state is measured there, **declared** here |
| Tse, Hanly | capacity region, not scalar | elastic, infinitely backlogged | that class is RN-13's degenerate case |
| Service-constraint taxonomy | throughput / delay-limited / probabilistic | any, once \(\epsilon_i\) is stated | none serious; this transfers cleanly |
| Liu, Layland [17]; Baruah [18] | **utilization bound per demand class; exact tests** | periodic and sporadic tasks | WCET assumed known; tasks independent and honest |
| Network calculus [19] | \((\sigma,\rho)\) burst characterisation | deterministic arrival curves | blockchain bursts are event-correlated |
| Effective bandwidth | statistical multiplexing gain as a number | stationary stochastic sources | sources here are strategic |
| Yao | minimum information to reach a target | worst case | often loose economically |
| Mount, Reiter; Nisan, Segal | informational requirements; prices fall out | static allocation | no temporal substrate, no lattice |
| Kelly | prices, shadow costs, decentralized allocation | elastic rate | no deadlines, no indivisible jobs |
| Prism [10] | physical, propagation and consensus limits | consensus layer | not the execution layer |
| Block-STM [13] | realizable parallelism | any | raises \(K_q\), not temporal structure |

**Nothing above supplies the following, which is where original work is required.**

1. **A declared, strategic demand side.** Every lineage assumes demand state is measured or
   stochastic. Here it is announced by a party with an interest in the answer.
2. **A protocol-chosen temporal lattice.** Wireless has physical coherence time; real-time
   scheduling has a given task model. A blockchain **picks** its quantum, so temporal
   resolution is a design variable and not a given.
3. **Value heterogeneity across time.** Kelly has utility for rate, real-time scheduling has
   deadlines. Neither has value that decays continuously and differently per stream.
4. **A mixed-class capacity region.** Each lineage characterises one demand class well. No
   one has characterised a substrate serving deadline jobs, periodic services, bursty flows
   and elastic flows *at once*, contending for the same quanta. Every chain in Part II
   serves such a mixture and none of them models it.

The fourth is the gap RN-13 aims at.

---

## References

Numbering follows RN-13 so citations move between the two documents unchanged.

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
