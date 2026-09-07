---
id: RN-13-Part-II
title: "Capacity and Welfare in Blockchain Execution Systems"
subtitle: "A TLM Theory of Heterogeneous Temporal Demand and Mechanism Evaluation"
version: "0.1"
status: "Working draft - research note, offered in good faith for comment"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-06"
license: "CC-BY-4.0"
companion: "RN-13 Part I, Capacity Theory for Execution Systems: A Survey under a Temporal Liquidity Lens"
---

# RN-13 Part II v0.1

# Capacity and Welfare in Blockchain Execution Systems

## A TLM Theory of Heterogeneous Temporal Demand and Mechanism Evaluation

**Temporal Liquidity Market (TLM) Research Program**  
**Status:** Working draft  
**Companion:** *RN-13 Part I — Capacity Theory for Execution Systems: A Survey under a Temporal Liquidity Lens*  
**Date:** 6 September 2026

---

## Abstract

Blockchain execution is commonly evaluated by transactions per second, gas throughput, fees, or validator revenue. Each is useful and none is a sufficient benchmark. A system can process more transactions while missing deadlines, admit low-gas work while excluding greater value, increase burn without increasing builder revenue, or improve aggregate surplus while concentrating access among users able to bid through private channels.

This note develops the TLM research framework in two layers. The first is a demand-conditioned capacity region: the workloads an execution system can serve under stated resource, temporal, information, state, and verification constraints. When demand is temporally indifferent and placement is unrestricted, the region collapses to an aggregate resource constraint. Gas throughput is the degenerate case. Temporal resolution and temporal information can matter only when complete demand profiles permit reallocations that the scalar interface cannot identify or implement.

The second layer is a mechanism benchmark. Capacity asks what can be served; it does not decide which feasible outcome is better. The benchmark therefore reports admitted and displaced demand, allocative welfare, temporal service, real resource costs, payments and burn, builder and proposer revenue, fairness, predictability, strategic robustness, decentralization pressure, and dynamic stability. These dimensions should ordinarily be presented as a scorecard and Pareto frontier rather than collapsed into one unexplained number.

The framework applies directly to the Temporal Liquidity Market. RN-12 proposes a conceptual exchange in temporal flexibility. RN-15 gives a block-local mechanism in which positive Temporal Liquidity Authorizations fund below-base-fee transactions that accept later execution bands. RN-16 adds an inter-slot reserve. These mechanisms cannot be judged by admission count or burn alone. A funded provider may use idle capacity, displace an ordinary transaction, or merely change order. Each case has a different capacity and welfare interpretation.

This note supplies a model, several restricted propositions, a loss decomposition, a benchmark protocol, and falsification criteria. The companion Part I owns the survey of Shannon, Tse, Kelly, real-time scheduling, network calculus, communication complexity, and related blockchain systems. Imported results are attributed there and used here only under stated assumptions.

---

# 1. Two questions, not one

The theoretical foundation has to answer two questions.

> **Capacity:** What demand can the execution system feasibly serve under stated service constraints?

> **Evaluation:** Which feasible allocation should a mechanism produce, and how should competing outcomes be compared?

The first question is positive. It concerns resources, timing, information, state conflicts, and scheduling. The second is partly normative. It concerns value, incidence, access, incentives, and the horizon over which the system is evaluated.

Confusing them produces several common errors:

- treating gas consumed as economic output;
- treating transaction count as capacity without controlling for transaction size;
- treating a larger feasible region as proof that a mechanism reaches it;
- treating more admitted demand as welfare without recording displacement;
- treating burn as builder revenue;
- treating private willingness to pay as social value;
- treating average utilization as evidence that every block has no slack;
- treating a fairer outcome as efficient without naming the fairness rule.

The TLM claim is not that temporal differentiation creates physical resources. It is that heterogeneous temporal demand can make a scalar fee-and-ordering interface leave feasible and valuable reallocations unused. Whether recovering them is worthwhile depends on the second question.

## 1.1 What is original here

This note distinguishes five kinds of statement.

1. **Imported result:** an established theorem used under its original assumptions.
2. **Transposition:** an established result expressed in blockchain notation, with the assumptions that fail on-chain stated separately.
3. **TLM proposition:** a result derived in the model below.
4. **Benchmark definition:** a stated evaluation choice, not a theorem.
5. **Hypothesis:** a claim requiring measurement, equilibrium analysis, or both.

Part I owns the first category. Part II uses imported results to construct the model but does not claim them as TLM discoveries.

## 1.2 What is established

Under the restrictions stated later:

- temporally indifferent divisible demand reduces to an aggregate resource region;
- subdivision and temporal information have no value in that degenerate case;
- any strict gain from temporal information or resolution requires profile structure that enables a different feasible allocation;
- capacity depends on the demand class and service constraint, not resources alone;
- a capacity improvement does not imply a welfare improvement;
- fee-market comparison requires separate capacity, welfare, incidence, and distributional accounts.

The mixed blockchain region—with indivisible execution, state conflicts, uncertain gas, strategic declarations, and dynamic sharing—is not characterized here.

---

# 2. Model

## 2.1 Environment and horizon

Fix a horizon (T), divided into (Q=T/\delta) logical execution or ordering quanta of width (\delta). Quantum (q) has protocol resource capacity (K_q). The aggregate resource budget is

\[
K_{\mathrm{tot}}=\sum_{q=0}^{Q-1}K_q.
\]

The quantum need not equal a consensus slot. It can describe an ordering band, mini-block, execution round, or other protocol-visible opportunity. Where execution, ordering, commitment, and consensus have different cadences, the fuller object is

\[
\delta_{\mathrm{exec}}
\leq \delta_{\mathrm{order}}
\leq \Delta_{\mathrm{commit}}
\leq \Delta_{\mathrm{consensus}}.
\]

Using one (\delta) assumes that one temporal bottleneck binds. This simplification must be named whenever a result is applied to a real chain.

The environment (E) also specifies:

- gas target and hard limit;
- execution and state-cost schedule;
- data and propagation constraints;
- consensus and finality rules;
- proposer-builder arrangement;
- mempool and inclusion policy;
- state-conflict and bundle constraints;
- adversarial capabilities.

## 2.2 Transaction-level demand: TEP

Request (j) from class or stream (i) has a Temporal Execution Profile:

```text
F_ij         feasible execution positions or window
v_ij(q,x)    value if executed in quantum q with outcome x
L_ij         gas limit or ex ante protocol resource bound
g_ij(x,s)    realized protocol gas under outcome x and state s
b_ij         signed fee and temporal authorizations
```

The full profile may include a release time, deadline, decay function, adjacency requirement, state dependencies, and failure value. A scalar width does not identify the profile. Two requests with equal window width can have different locations, asymmetries, values, gas limits, and conflicts and need not be substitutes.

This note therefore does not use dispersion in one liquidity scalar as a market-existence condition. Scalar summaries may be descriptive. Feasible exchange depends on complete profiles and the constraints coupling them.

## 2.3 Stream-level demand: TSP

A Temporal Stream Profile describes persistent demand across requests or slots. It can include:

- arrival rate or arrival curve;
- burst parameter;
- required cadence;
- deadline distribution;
- correlation with external events;
- state and resource distribution;
- value and temporal-value distribution.

TEP and TSP answer different questions. TEP states where one request can execute and what its placement is worth. TSP states how such requests arrive over time. A capacity theorem may require either or both.

## 2.4 Allocation and feasibility

Let (x_{ijq}\in\{0,1\}) indicate placement of request (ij) in quantum (q). A basic allocation satisfies:

\[
\sum_q x_{ijq}\leq 1,
\qquad
x_{ijq}=0\ \text{if}\ q\notin F_{ij},
\]

and

\[
\sum_{i,j}g_{ij}x_{ijq}\leq K_q
\quad\text{for every }q.
\]

Real systems add nonce, state-conflict, bundle, data, and verification constraints. Let (\Omega(E,D,I,\delta)) denote the resulting feasible allocation set under demand (D) and information structure (I).

Let (\lambda_i) denote the number or expected number of class-(i) requests offered over the stated horizon; a rate formulation divides both demand and capacity by (T). Define the demand-conditioned capacity region

\[
\mathcal C(E,I,\delta\mid P(\mathrm{TEP}),P(\mathrm{TSP}))
=
\{\boldsymbol\lambda:
\text{some policy satisfies the stated service constraints}\}.
\]

There is no useful capacity region without the conditioning terms. Changing a deadline, cadence, failure probability, or temporal profile can change feasibility without changing aggregate gas.

## 2.5 Information

The protocol observes (X=f(D)), not necessarily full demand. An information structure (I) specifies what the scheduler learns and when. More detail is not free: it can increase message size, verification cost, strategic surface, and extraction.

Information structures are only partially ordered. (I_1\succeq I_0) in the Blackwell sense when decisions available under (I_0) remain available under (I_1). Weak improvement under a richer structure is then definitional if the scheduler may ignore information. The research question is whether the gain is strict and large enough to exceed disclosure, verification, and strategic costs.

## 2.6 Welfare oracle

Under true demand, no strategic reporting, unrestricted computation, and all protocol constraints enforced, define

\[
W^*(E,D,\delta)=\max_{S\in\Omega(E,D,I_{\mathrm{full}},\delta)}W(D,S).
\]

This is an oracle, not an implementable mechanism. Private values are unavailable, generalized assignment is hard, and state-dependent execution can make even the feasible set costly to compute. Practical mechanisms produce (W_M\leq W^*) only under a common welfare definition and common demand trace.

---

# 3. Gas throughput as the degenerate case

## 3.1 Definition

A demand population is **temporally degenerate** over the horizon when every request:

1. can be placed in any quantum; and
2. has value independent of its placement.

There are no deadlines, windows, cadence requirements, or value decay. Resource requirements may still differ.

## 3.2 Proposition: aggregate resource suffices

**TLM Proposition 1.** Under temporal degeneracy, divisible requests, fixed (K_{\mathrm{tot}}), and no additional per-quantum coupling, feasibility reduces to

\[
\sum_i \lambda_i\bar g_i\leq K_{\mathrm{tot}}.
\]

The capacity region is a simplex described by aggregate protocol resource. Temporal subdivision and temporal refinements of the information structure add no value.

**Proof sketch.** Because placement does not affect feasibility or value, per-quantum variables can be aggregated into admitted quantities. Under divisibility, any aggregate allocation within (K_{\mathrm{tot}}) can be spread across quanta in proportion to (K_q). Quantum labels disappear from the program. A temporal message cannot improve an allocation whose objective and constraints are invariant to position. \(\square\)

This is **gas throughput**, not transaction-count TPS unless requests have equal gas or an explicit average-size normalization. Gas-weighted capacity is the degenerate case closest to how Ethereum meters blocks.

## 3.3 Converse and limits

The contrapositive is useful but narrow: a strict gain from temporal resolution or temporal information implies that temporal degeneracy fails. It does not say that every heterogeneous population produces a gain.

Strict gain additionally requires:

- a feasible reallocation across complete profiles;
- sufficient resource and state compatibility;
- information that distinguishes the relevant alternatives;
- an allocation rule that uses it;
- benefits exceeding mechanism and verification costs.

Profile heterogeneity is necessary in many cases and never sufficient by itself. Equal scalar width does not imply homogeneity; unequal scalar width does not guarantee trade.

Under indivisibility, changing (\delta) can also hurt. A job that fits one coarse quantum may fit no finer quantum if per-quantum capacity falls with subdivision. Resolution must therefore be evaluated jointly with (K(\delta)).

---

# 4. Four limits and one loss decomposition

## 4.1 Four kinds of limit

1. **Physical:** propagation, bandwidth, computation, memory, storage, and verification.
2. **Protocol-induced:** block intervals, gas limits, consensus rounds, validity, and ordering rules.
3. **Architecture-induced coupling:** independent processes forced onto one cadence or serial order.
4. **Information and mechanism:** flexibility exists but is not observable, credible, or used.

Physical and protocol capacity are not interchangeable. A faster machine may leave an ordering restriction unchanged. A richer scheduler may improve service without increasing physical execution.

## 4.2 Loss decomposition

Relative to the full-information oracle, define five conceptual losses:

```text
physical loss          outside the substrate's feasible capability
resolution loss        feasible at finer temporal granularity but not on the lattice
information loss       useful flexibility exists but is not exposed
mechanism loss         exposed information is not converted into allocation
strategic loss         manipulation, verification, and private-channel response
```

These losses need not be additively separable in data. A richer interface can change strategy, and finer resolution can raise verification cost. The decomposition is an attribution framework, not an accounting identity.

---

# 5. Demand-class bounds

Part I reviews the source theories. This section records how their constraint forms enter the TLM model.

## 5.1 Elastic class

For unrestricted, placement-indifferent divisible demand, Proposition 1 applies. Aggregate resource is the binding description. No temporal mechanism improves capacity in this class.

## 5.2 Deadline class

For independent periodic or sporadic jobs with known execution requirement (C_i), period (T_i), and relative deadline (D_i), the demand-bound function is

\[
h(t)=\sum_i C_i
\max\left\{0,
\left\lfloor\frac{t-D_i}{T_i}\right\rfloor+1
\right\}.
\]

Under the imported preemptive uniprocessor assumptions reviewed in Part I, EDF feasibility is characterized by (h(t)\leq t) for the relevant intervals.

The blockchain transposition replaces processor time with protocol resource over temporal intervals. It is exact only in the corresponding divisible, independent, known-cost model. Transactions are generally indivisible, gas may be known only after execution, and state conflicts create additional coupling. The transposition supplies a benchmark or relaxation, not a direct Ethereum schedulability theorem.

## 5.3 Periodic-service class

Suppose service (i) requires cadence (\tau_i^{\mathrm{req}}). Over horizon (T), let at most (M) meaningful transitions be exposed per quantum. A necessary cadence constraint is

\[
\sum_i\frac{\delta}{\tau_i^{\mathrm{req}}}\leq M,
\]

alongside the resource-rate constraint

\[
\sum_i\frac{g_i}{\tau_i^{\mathrm{req}}}
\leq
\frac{K_{\mathrm{tot}}}{T}.
\]

**TLM Proposition 2.** Under divisible independent periodic service, fixed (M), and a fixed aggregate resource rate, halving (\delta) doubles the admissible cadence bound until the resource constraint or another coupling constraint binds.

This is not a claim that the entire capacity region scales without limit. Resolution stops helping when gas, execution, data, state, verification, or consensus becomes binding.

The Liu–Layland and EDF utilization results reviewed in Part I illustrate that scheduling policy can leave part of a deadline or cadence region unused. They do not imply that fee ordering is rate-monotonic scheduling or that Ethereum loses a fixed percentage of capacity.

## 5.4 Bursty class

For a stream with arrival envelope

\[
\alpha_i(t)=\sigma_i+\rho_i t,
\]

network-calculus service curves can bound backlog and delay when aggregate service dominates aggregate arrival. The blockchain use is a transposition. External price events create correlated bursts, state conflicts make service non-fungible, and strategic senders can shape arrivals. Finer quanta do not necessarily improve burst absorption because per-quantum capacity may fall as (\delta) shrinks.

## 5.5 Statistical class

Effective-bandwidth theory can characterize stochastic multiplexing gains under stationarity and tail assumptions. The corresponding TLM quantity is the difference between peak provisioning and service under multiplexed temporal profiles.

Blockchain sources are strategic and often correlated. Statistical multiplexing is therefore a hypothesis to measure, not an assumption to import silently.

## 5.6 Mixed class

Real chains serve elastic transactions, deadlines, periodic services, and correlated bursts together. Under this paper's blockchain-specific model—indivisible execution, state conflicts, uncertain gas, strategic declarations, and dynamic sharing—the mixed region is not characterized here.

It is not generally the intersection of separate class regions unless resources are partitioned in advance. Dynamic sharing may outperform fixed partitions, but the gain and the appropriate objective remain open.

---

# 6. Capacity is not the benchmark

A capacity region says what some scheduler could serve. It does not say:

- which requests a mechanism admits;
- whether admitted requests have greater value than displaced ones;
- whether deadlines are met;
- who pays and who receives;
- whether builders will implement the allocation;
- whether access is concentrated;
- whether the mechanism remains solvent over time.

Two mechanisms can operate inside the same region and produce different outcomes. Conversely, a mechanism can enlarge one service region while reducing welfare because richer rules increase execution, disclosure, state, or strategic costs.

The benchmark object is therefore a vector:

\[
B(M;D,E)=
(A,W,W_T,C,P,F,Q,R,Z),
\]

where:

```text
A   admitted and displaced demand
W   allocative welfare
W_T temporal service and delay loss
C   real resource and mechanism costs
P   payments, burn, revenue, refunds, and incidence
F   fairness and access
Q   predictability and service quality
R   strategic robustness and decentralization pressure
Z   dynamic stability
```

This vector is a benchmark definition. It is not a theorem that these dimensions are complete or commensurable.

---

# 7. Hard constraints before comparison

## 7.1 Resource feasibility

Included work must satisfy gas, data, execution, state, propagation, and verification limits. Protocol gas should be reported separately from measured physical cost because equal gas can conceal different state access, locality, parallelism, and wall-clock execution.

## 7.2 Financial solvency

Burn, tips, subsidies, refunds, and reserve liabilities must be funded for every valid execution. Expected balance is insufficient unless the mechanism specifies who absorbs a deficit.

## 7.3 Verifiability

Validators must recompute validity, allocation, ordering, and settlement from consensus-visible information. A builder-selected value affecting settlement must be published.

## 7.4 Causality

Pre-execution decisions may use only information available at that time. Realized gas can settle a payment after execution but cannot fund an unreserved obligation before execution.

## 7.5 Individual authorization

No sender may be charged beyond its signed ceilings. If fee and temporal authorizations are separate, balance reservation and realized liability must state both.

Mechanisms failing a hard constraint do not enter the performance ranking under that environment.

---

# 8. The benchmark dimensions

## 8.1 Admitted demand

Report at least:

```text
N_admit       number of admitted requests
G_admit       gas consumed
V_admit       estimated gross execution value
N_deadline    requests completed within service windows
N_added       requests absent under the baseline and admitted under the candidate
N_displaced   baseline requests removed by the candidate
```

Transaction count favors small requests. Gas favors gas-intensive work and inherits the protocol schedule. Gross value is difficult to observe. Deadline success ignores how early execution occurred inside the window. The measures remain separate.

Admission should also be reported by application, temporal class, sender class, and market role. “More providers were funded” is incomplete unless the study says whether they used idle capacity or displaced ordinary transactions.

## 8.2 Allocative welfare

A general welfare account is

\[
W=
\sum_i v_i(x_i,t_i)
-C_{\mathrm{exec}}
-C_{\mathrm{state}}
-C_{\mathrm{data}}
-C_{\mathrm{verification}}
-C_{\mathrm{latency}}
-C_{\mathrm{mechanism}}
-C_{\mathrm{strategic}}.
\]

Each term must be defined for the study. An arbitrary constant should not be introduced merely to complete the equation.

Payments among users, builders, proposers, and validators are usually transfers within a system-wide boundary. They affect incentives and incidence but should not be subtracted twice. MEV should be decomposed into builder revenue, user loss, transfers among traders, and any real allocative harm before netting.

## 8.3 Temporal service

Report:

- deadline success;
- average and tail lateness;
- realized value loss from delay;
- delivery of authorized bands or windows;
- service by urgency class;
- unserved demand by complete temporal profile.

One loss measure is

\[
L_T=\sum_i\left[v_i(t_i^{\mathrm{best}})-v_i(t_i)\right],
\]

where (t_i^{\mathrm{best}}) is the best feasible point under the comparison. This does not assume that users reveal (v_i) truthfully; empirical work may require bounds or application-specific proxies.

## 8.4 Resource cost and utilization

Report gas relative to target and hard limit, execution and verification time, data load, state reads and writes, persistent state growth, failed execution, and mechanism-computation cost.

For reserve-and-settle mechanisms, reservation efficiency is

\[
\eta_R=\frac{\sum_i S_i}{\sum_i R_i}.
\]

A low ratio indicates conservative admission and unused matching capacity, not insolvency.

## 8.5 Economic incidence

Report separately:

- user execution payments;
- temporal payments;
- priority fees;
- proposer and builder revenue;
- base-fee burn;
- provider discounts or subsidies;
- refunds;
- reserve accumulation and drawdown;
- observable out-of-band payments.

These answer different questions. Higher burn is not builder revenue. Higher builder revenue is not necessarily higher welfare. Lower average fees are not necessarily fair.

## 8.6 Fairness and access

State the fairness rule. Candidate measures include:

- equal treatment of equivalent requests;
- inclusion and deadline success by demand class;
- payment dispersion for equivalent service;
- concentration of early positions and gains;
- sensitivity to wealth, sophistication, and private-order-flow access;
- maximum burden imposed on one class;
- envy or justified-envy tests under declared service.

No one statistic establishes fairness. Distribution should be published alongside aggregate results.

## 8.7 Predictability

Measure fee variance, inclusion-probability calibration, deadline reliability, temporal-band delivery, and sensitivity to other block arrivals. Predictability can have value even when expected inclusion and payment are unchanged.

## 8.8 Strategic robustness and decentralization

Test bid shading, false temporal declarations, transaction splitting, gas-limit inflation, pool manipulation, builder subset choice, censorship, bundle workarounds, and private position sales. Also measure the advantage of low latency, proprietary simulation, private order flow, and large balance sheets.

## 8.9 Dynamic stability

Report base-fee paths, oscillation, backlog, recovery after shocks, and—where value crosses slots—reserve balance and deficit risk. A one-block allocation gain can destabilize a multi-block controller.

---

# 9. Burn, holder value, and blockchain output

Burn requires an explicit accounting boundary.

When additional execution raises base-fee burn, circulating ETH is lower than it otherwise would be. Existing holders may benefit through reduced dilution or a price response if ETH demand is unchanged. That is an economic-incidence claim, not a direct transfer to holders and not automatically new social output.

Report:

\[
\Delta\mathrm{Burn},
\quad
\Delta\mathrm{NetIssuance},
\quad
\Delta\mathrm{UserPayment},
\quad
\widehat{\Delta H}_{\mathrm{holders}}.
\]

Do not assume

\[
\widehat{\Delta H}_{\mathrm{holders}}
=
\Delta\mathrm{Burn}.
\]

The market-value effect depends on expectations, ETH demand, issuance policy, and supply elasticity. Counting both the full user payment and an equal holder gain as new welfare double-counts part of the same incidence.

For a broad economic boundary, blockchain output is better represented by realized service value net of real costs. For a token-holder objective, burn and issuance receive additional weight. For protocol-security analysis, proposer and validator revenue may be central. Results should be shown under each relevant boundary rather than changing boundaries inside one argument.

## 9.1 Is excluded activity a loss?

For demand class (c), define the counterfactual access value

\[
L_c
=
W^*(\text{all classes})
-
W^*(\text{class }c\text{ excluded}),
\]

allowing capacity to be reallocated in both cases.

If class (c) would use otherwise idle capacity and creates value above real cost, exclusion is a loss. If it would displace greater-value execution, exclusion may be efficient in a static model. Dynamic network effects, composability, resilience, and future option value can change the answer and must be stated separately.

High fees are evidence of private willingness to pay, not proof of social value. Payments, oracle infrastructure, and public services may create benefits outside the originating transaction. Trading fees can include private transfers or extraction. Application labels cannot substitute for the counterfactual.

---

# 10. Comparing mechanisms

## 10.1 Pareto comparison

A universal weighted score

\[
Score(M)=\sum_k\omega_kz_k(M)
\]

embeds a social objective and depends on normalization. It can allow severe exclusion to be offset by enough revenue under one choice of weights.

The default procedure is:

1. screen hard constraints;
2. publish the benchmark vector;
3. identify Pareto dominance where it exists;
4. display trade-off frontiers where it does not;
5. use weighted objectives only with published weights and sensitivity analysis.

Mechanism (M_1) Pareto-dominates (M_0) over an agreed metric set when it is no worse on every metric and better on at least one. Most comparisons will produce a frontier rather than one winner.

## 10.2 Multiple reference optima

Report regret against several objectives:

- welfare-maximizing allocation;
- admitted-count-maximizing allocation;
- gas-admission-maximizing allocation;
- deadline-satisfaction-maximizing allocation;
- builder-revenue-maximizing allocation;
- fairness-constrained allocation.

The distance between them shows how much the choice of objective matters.

---

# 11. Benchmark protocol

1. **State the comparison.** Name the baseline, candidate, environment, horizon, accounting boundary, and behaviors held fixed.
2. **Define demand classes.** Include complete temporal profiles where possible. Do not infer temporal preference from fees alone.
3. **Construct scenario families.** Test underfilled, target-level, and full blocks; spikes; thin and one-sided markets; heterogeneous gas limits; bundles; state conflicts; concentrated builders; and adversarial declarations.
4. **Separate mechanical from behavioral results.** First verify validity, accounting, solvency, and deterministic allocation. Then add bidding, builder choice, proposer auctions, and induced demand.
5. **Replay a common demand trace.** Record requests added, removed, reordered, or repriced under each mechanism.
6. **Publish distributions.** Report means, tails, and class-level outcomes.
7. **Stress assumptions.** Vary demand elasticity, valuation, builder objective, gas uncertainty, state cost, private order flow, and benchmark weights.

Fixed-demand and equilibrium-demand comparisons should remain separate. The first asks what the rule changes for the same requests. The second asks which requests arrive after participants adapt.

---

# 12. Application to RN-15

RN-15 adds a signed Temporal Liquidity Authorization to a block-local EIP-1559 construction. Positive authorizations fund the pool and seek earlier bands. Negative declarations opt below-base-fee providers into funding and commit them to later bands. Providers reserve against gas limits and settle against realized gas.

RN-15 does not increase Ethereum's long-run protocol capacity. Its effects divide into four cases.

## 12.1 Idle-capacity admission

The provider uses gas that the block would otherwise leave unused. Admitted execution and utilization rise without direct displacement. Welfare rises only if execution value exceeds real resource, state, verification, and mechanism costs. The next base fee depends on total gas relative to target.

## 12.2 Displacement

The block would otherwise be full. A funded provider replaces an ordinary transaction. This is reallocation, not capacity expansion. Compare the provider's value, temporal service, and incidence with the displaced transaction's value, tip, deadline, and costs.

## 12.3 Ordering-only change

The included set and gas remain fixed while urgent transactions move earlier and flexible transactions later. The primary output is temporal welfare. Burn and the next-base-fee signal may be unchanged.

## 12.4 Induced demand

Below-base-fee conditional inclusion or priced temporal bands may attract applications that previously avoided the chain. This is an equilibrium effect and should not be inferred from fixed-block accounting.

## 12.5 RN-15 scorecard

| Dimension | Minimum output |
|---|---|
| Admission | added, displaced, and reordered requests by class |
| Welfare | temporal and execution value minus real costs |
| Temporal service | band delivery, deadline success, delay loss |
| Resources | gas, execution, state growth, reservation slack |
| Incidence | consumer charges, provider discounts, tips, burn, refunds |
| Fairness | inclusion and payment distributions |
| Robustness | builder tip and subset choice, private ordering, strategic TLA |
| Dynamics | next-base-fee path |

Budget balance and simulation invariants establish feasibility properties. They do not establish welfare or equilibrium performance.

---

# 13. Application to RN-16

RN-16 considers carrying unmatched authorization across slots in a Temporal Liquidity Reserve rather than refunding it at each block boundary. This relaxes the requirement that funding and provider need meet in one slot. It also changes the benchmark horizon.

Additional hard constraints and metrics include:

- ownership of reserve balances;
- withdrawal rights and timing;
- intertemporal solvency;
- reserve accumulation and depletion;
- treatment of deficits;
- incidence across cohorts and slots;
- response to sustained one-sided demand;
- interaction with the base-fee controller;
- recovery after shocks;
- governance and capture of retained value.

An RN-16 comparison should show the matching gain from carrying value against the financial and strategic risk created by protocol state.

---

# 14. Ethereum and high-throughput systems

## 14.1 Ethereum

Ethereum regulates long-run gas around an EIP-1559 target below the hard block limit. Operating near target does not mean every block reaches the limit, but it means transient headroom is not free sustainable capacity.

The TLM question for Ethereum is therefore:

> Can temporal information improve the value, access, or ordering of execution under deliberately scarce L1 capacity?

It is not:

> Can a fee rule permanently raise Ethereum's gas throughput?

Ethereum may rationally specialize in high-security settlement while routine execution moves to L2. That strategy does not prove that the highest fee identifies the highest-value activity or that every absent demand class was efficiently excluded. The benchmark must distinguish efficiently excluded demand, misallocated demand, and demand strategically delegated to L2.

## 14.2 High-throughput systems

High nominal throughput alone does not create a temporal-liquidity market. If capacity is abundant and all requests receive equivalent timely service, the temporal scarcity price approaches zero.

A high-throughput system becomes relevant when it still exhibits local temporal scarcity:

- bursts after oracle or market events;
- hot-state contention;
- liquidation or auction priority;
- differentiated confirmation guarantees;
- delayed work that can be moved across intervals;
- sequencer or builder bottlenecks;
- demand classes sharing aggregate capacity but requiring different cadence.

Such a system may be a useful implementation environment because temporal classes can be designed into the execution interface rather than retrofitted into EIP-1559. The research criterion is temporal contention, not leaderboard TPS.

Scaling and TLM are complements:

> Scaling expands the feasible region. TLM attempts to allocate execution across heterogeneous temporal demand within that region.

---

# 15. Hypotheses and falsification

## H1. Temporal heterogeneity

Complete transaction and stream profiles differ enough to permit feasible exchanges of position or timing.

**Falsified or weakened by:** near-identical profiles, incompatible windows, state conflicts, or gains disappearing once complete profiles replace scalar summaries.

## H2. Information value

A protocol-visible temporal representation improves feasible service or temporal welfare relative to fee-only information.

**Falsified or weakened by:** no improvement on common demand traces, or gains smaller than disclosure and verification costs.

## H3. Mechanism realization

A practical allocation rule captures a material share of the full-information gain.

**Falsified or weakened by:** strategic reporting, builder subset choice, computation, or private markets eliminating the gain.

## H4. Distributional acceptability

Gains do not depend on burdens or exclusions inconsistent with the stated fairness rule.

**Falsified or weakened by:** concentration of early service, payment, or inclusion among a narrow class despite positive aggregate welfare.

## H5. Dynamic stability

Inter-slot mechanisms improve matching without unstable reserve or base-fee interaction.

**Falsified or weakened by:** persistent depletion, unbounded accumulation, oscillation, delayed deficits, or strategic reserve capture.

## H6. Deployment relevance

The demand affected by temporal differentiation is large enough to matter on the target chain.

**Falsified or weakened by:** providers usually displacing higher-value work, temporal benefits being small, or the relevant demand already receiving equivalent service on L2 or through existing markets.

---

# 16. Measurement program

## 16.1 Mechanical simulation

Verify accounting, reservation, refunds, authorizations, ordering, edge cases, and adverse sequences. These tests establish implementation properties, not equilibrium.

## 16.2 Trace replay

Replay historical blocks and mempool traces to estimate idle capacity, displacement, fee-cap headroom, gas-limit slack, burn, builder revenue, and next-base-fee paths. Temporal value requires application-specific proxies or bounds.

## 16.3 Workload measurement

Measure wall-clock execution, cache locality, state access, data, and parallelism separately from protocol gas. This tests whether gas remains a useful resource proxy under the candidate allocation.

## 16.4 Behavioral analysis

Model TLA shading, provider fee selection, builder tip and subset choice, proposer bidding, transaction splitting, and private-ordering substitution. Use multiple behavioral models where no equilibrium is known.

## 16.5 Deployment experiment

Test builder computation time, client and mempool burden, propagation, failed bundles, verification, and concentration. A testnet result does not establish mainnet welfare but can reject infeasible designs.

---

# 17. Open problems

1. Characterize the mixed TEP/TSP region under indivisibility, state conflicts, uncertain gas, and strategic declarations.
2. Determine when finer temporal resolution increases net capacity after (K(\delta)), verification, and propagation costs are included.
3. Find minimal sufficient temporal representations without assuming a total information order.
4. Define estimable temporal-value bounds when users do not reveal value curves truthfully.
5. Choose the welfare boundary for burn, MEV, and token-holder effects.
6. Determine which fairness requirements should be hard constraints.
7. Attribute persistent state and future verification cost to present execution.
8. Include private payments and order flow when only partial observations exist.
9. Model builder choice when the selected provider tip changes both revenue and allocation rank.
10. Determine the correct horizon for joint base-fee and reserve evaluation.
11. Compare Ethereum L1 specialization with ecosystem-wide service through L2.
12. Identify chains where temporal contention is material despite high aggregate throughput.

---

# 18. Claims and non-claims

## 18.1 Claims

- Capacity must be conditioned on a demand class and service requirement.
- Gas throughput is the degenerate temporally indifferent case under stated relaxations.
- Heterogeneity is not enough; strict gains require feasible profile-level reallocation and usable information.
- Capacity and welfare are separate objects.
- Admission, burn, builder revenue, welfare, and fairness should not be used interchangeably.
- Mechanisms should ordinarily be compared through a scorecard and Pareto frontier.
- RN-15 must distinguish idle-capacity admission, displacement, ordering-only effects, and induced demand.
- RN-16 requires an intertemporal benchmark because value and liabilities cross slots.

## 18.2 Non-claims

- TPS is never useful.
- Finer temporal resolution always helps.
- A scalar temporal-liquidity statistic determines market existence.
- Imported scheduling bounds apply directly to indivisible blockchain transactions.
- More admitted transactions or more burn necessarily increases welfare.
- High fees identify high social value.
- TLM increases Ethereum's long-run gas target.
- RN-12, RN-15, or RN-16 is efficient or incentive compatible.
- One fairness or welfare definition is universal.

---

# 19. Conclusion

Blockchain execution systems allocate more than computation. They allocate inclusion, time, payment burden, builder and proposer revenue, burn, state growth, and exposure to uncertainty. A theory based only on transactions or gas cannot represent all of these outcomes.

The first object is a demand-conditioned capacity region. It records what the substrate and protocol can serve under temporal, resource, information, and state constraints. In the temporally indifferent divisible case, the region reduces to aggregate resource and gas throughput is sufficient. Outside that case, capacity depends on service windows, cadence, bursts, resolution, and what the scheduler knows.

The second object is a mechanism benchmark. It records which part of the region a mechanism reaches and what the resulting allocation does to value, delay, resources, payments, access, strategy, and stability. A larger admission count is not automatically a better allocation; additional execution may use idle capacity or displace something more valuable. Burn can affect holder incidence without becoming builder revenue or new welfare dollar for dollar.

Together the two objects provide the intended foundation for TLM:

\[
\boxed{
\text{What can be served?}
\quad+\quad
\text{Which feasible outcome is better?}
}
\]

The next research step is empirical. Apply the same demand traces and accounting boundaries to the baseline, RN-15, and later reserve mechanisms; publish the full benchmark vector; and identify where each mechanism lies on the resulting frontier. TLM matters only where complete temporal profiles reveal a feasible reallocation whose benefits exceed its physical, mechanism, strategic, and distributional costs.

---

# References

## TLM research notes

- RN-01. *Temporal Execution Profiles.*
- RN-02. *Protocol-Visible Temporal Abstraction.*
- RN-11. *Term Structure and Allocation of Execution Capital in TLM.*
- RN-12. *The Temporal Liquidity Market: A Conceptual Mechanism Design.*
- RN-13 Part I. *Capacity Theory for Execution Systems: A Survey under a Temporal Liquidity Lens.*
- RN-14. *The Demand Ethereum Does Not Serve.*
- RN-15 v2.3. *A Temporal Liquidity Authorization for EIP-1559.*
- RN-16. *A Temporal Liquidity Reserve for EIP-1559.* Working draft.

## Imported theory and protocol references

The full literature treatment and transfer conditions appear in RN-13 Part I. Principal sources used by this paper include:

- Shannon, C. E. “A Mathematical Theory of Communication.” *Bell System Technical Journal*, 1948.
- Goldsmith, A. J. and Varaiya, P. P. “Capacity of Fading Channels with Channel Side Information.” *IEEE Transactions on Information Theory*, 1997.
- Tse, D. N. C. and Hanly, S. V. “Multiaccess Fading Channels.” *IEEE Transactions on Information Theory*, 1998.
- Liu, C. L. and Layland, J. W. “Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment.” *Journal of the ACM*, 1973.
- Baruah, S. K., Mok, A. K., and Rosier, L. E. “Preemptively Scheduling Hard-Real-Time Sporadic Tasks on One Processor.” *Real-Time Systems*, 1990.
- Kelly, F. P., Maulloo, A. K., and Tan, D. K. H. “Rate Control for Communication Networks.” *Journal of the Operational Research Society*, 1998.
- Buterin, V. et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain.* https://eips.ethereum.org/EIPS/eip-1559
