---
id: RN-11
title: "The Temporal Liquidity Market: A Formal Foundation"
subtitle: "The execution-capital allocation problem and the term structure of block-fee-rates"
version: v0.2 (adds the term-structure analysis; RN-12 folded in)
status: "Public draft. The formal center of the TLM program; stated, not solved."
program: "Temporal Liquidity Market (TLM)"
date: August 4, 2026
---

# RN-11 — The Temporal Liquidity Market: A Formal Foundation

*The execution-capital allocation problem and the term structure of block-fee-rates.*

## Abstract

RN-10 argues at the level of economic structure: a blockchain allocates execution capital across time, execution capacity has a time value expressible as a term structure, and temporal liquidity is a two-sided market between work that tolerates drift between wall-clock relevance and block-time execution and work that does not.

This note gives that argument its formal center, in two parts. **Part I** states the allocation as an optimization problem: demand is a tuple - an arrival process, a target, a value scale, and a decay function - the protocol allocates capacity across quanta to maximize value-weighted execution subject to capacity, neutrality, reducibility, and incentive compatibility, and the shadow prices on per-quantum capacity are the **efficient term structure** - the block-fee-rate curve a planner meeting that objective would set. **Part II** treats the term structure as a *market* object: the curve that a two-sided auction of demand and supply actually prints, constructed by **bootstrapping** from the observed prices of temporal instruments - spot inclusion, a future-slot fee, and a fee swap - under no-arbitrage. The efficient curve of Part I is the benchmark; the bootstrapped curve of Part II is the observation; their difference measures inefficiency. The mapping from the bond market to the fee market (sec. 4) is itself a contribution: it shows that today's fee market prices only the front of the curve, and it gives a rigorous guide - a checklist of instruments and their no-arbitrage relations - for designing the future-slot fees that would complete it.

Writing it this way makes several of RN-10's arguments - fee-as-filter, the two camps, the flexibility grades, deployed versus undeployed capacity - consequences of one problem, and turns the program's open questions into well-posed ones. The problem is stated, not solved.

## 0. Relationship to the other notes

RN-10 is the economics and is self-contained; this note is its formal counterpart and assumes it. The lattice of quanta is RN-05; the demand representation is RN-01/02; the reducibility constraint is RN-07; verification of declared characteristics is RN-02. Mechanism design - registration, clearing rules, exercise ordering, enforcement - is the subject of separate notes and is not attempted here. Questions this note opens are tracked in **RN-10 Follow-up Research Questions**.

Section references of the form "RN-10 sec. N" point to the economics note; internal references are to this note's own sections.

---

# Part I — The allocation problem and the efficient term structure

## 1. The execution-capital demand function, formally

Let blockchain time be indexed by quanta t = 0, 1, 2, ... (the lattice of RN-05; RN-10 sec. 6.9). A project i has four components of demand:

- an **arrival process** A_i, where A_i(s) is the quantity of execution work that becomes submittable at quantum s;
- a **target** tau_i(s), the quantum at which work arriving at s is *relevant* in wall-clock terms - the lattice image of T_wall;
- a **value scale** V_i(s) >= 0, the value of executing a unit of that work at its target;
- a **decay function** phi_i mapping integers to [0,1], with phi_i(0) = 1 and phi_i non-increasing in |d|.

The value to project i of executing, at quantum t, a unit of work that arrived at s <= t is

```text
v_i(s, t) = V_i(s) * phi_i( t - tau_i(s) )
```

**Arrival and target are separate.** Measuring decay from arrival would assume that work becomes relevant when it becomes submittable, and that assumption fails for the class RN-10 sec. 7 is built around: a mint opening at a published block, a scheduled expiry, a funding settlement can all be submitted long before they are relevant, so tau is known far in advance while the work remains immovable. Decay against tau lets the model hold *foreseeable* and *tightly bound* at once; a single-index form cannot.

The argument of phi is then the drift RN-10 sec. 7 names: **`t - tau` is `T_block - T_wall` measured on the lattice**, and phi is the tolerance for it. The partition RN-10 draws is not an assumption laid on this model; it is the model's primitive read directly.

Two details of the definition. phi is defined on all integers, not just the non-negatives, because for target-bound work executing *early* destroys value as surely as executing late - an oracle update before the event it reports is worthless. And setting tau_i(s) = s recovers the one-sided case, which covers ordinary work that is relevant as soon as it exists.

The tuple **ECDF_i = (A_i, tau_i, V_i, phi_i)** is the project's execution-capital demand function. This recovers the umbrella dimensions (Vision; RN-01) as properties of phi, tau and A rather than as an enumerated list:

| Temporal characteristic | Formal counterpart |
|---|---|
| delay tolerance | how slowly phi_i decays away from 0 |
| deadline | the smallest d > 0 with phi_i(d) = 0 (possibly infinite) |
| decay rate | the shape of phi_i, distinct from the deadline |
| binding tightness | the width of phi_i (below) |
| duration / continuity | the support and persistence of A_i |
| intensity | the magnitude of A_i |
| predictability | the forecastability (e.g. conditional variance) of A_i and tau_i |

Two remarks. Delay tolerance is *two* parameters - a deadline and a decay shape - which is why a single urgency scalar cannot represent it (RN-01). And phi is a **declared** object while A is largely **observed**, which is the declared-versus-verified distinction the program insists on (RN-02): phi must be made credible, A can be measured. The target tau sits between the two: for scheduled work it is publicly verifiable, for triggered work it is revealed only when the trigger fires.

**Binding tightness, formally.** Fix a tolerance level alpha in (0,1) - the fraction of value a project is willing to see lost. Define

```text
W_i(alpha) = | { d in Z : phi_i(d) >= alpha } |        tolerance width, in quanta
T_i        = sum_{d in Z} phi_i(d)                     effective tolerance (area under phi)
```

W_i(alpha) is the number of quanta over which the work retains at least alpha of its value; T_i is the same idea integrated over all levels, and for the rectangular case phi = 1 on a window of D quanta and 0 outside, both reduce to D. The partition of RN-10 sec. 7 is then a threshold on this width: fix a tightness bound kappa, and

```text
tight-binding (taker)      W_i(alpha) <= kappa
loose-binding (supplier)   W_i(alpha) >  kappa
```

Three things follow.

- **The two axes are formally independent.** Tightness is a property of phi; predictability is a property of the joint law of (A_i, tau_i). Nothing in the definition of W ties it to how well tau is forecast, which is why all four cells of the RN-10 sec. 7.3 table are non-empty. A scheduled mint has tau known months ahead and W = 1.
- **The partition applies to executions, not participants.** W is defined per unit of work, through the phi attached to it. One project may emit work with W = 1 on its liquidation path and W = 10^4 on its batch-posting path, and the model assigns those to opposite camps without contradiction.
- **kappa is not arbitrary.** The natural scale is the horizon over which the shadow price varies: work is tight-binding when it cannot outlast a congestion episode. Taking kappa comparable to the autocorrelation length of p(t) makes the threshold endogenous to the chain rather than a free parameter; because that couples the partition to the price it produces, the two are best read as a joint fixed point rather than one fixed independently of the other.

**Which side a participant actually trades on** is then the intrinsic tightness evaluated against the curve. Loosely bound work holding a claim on quantum t supplies temporal liquidity when the price it is offered to move exceeds the value it loses by moving:

```text
supply at t  iff   p(t) - p(t+k)  >=  V_i * ( phi_i(t - tau_i) - phi_i(t + k - tau_i) )
```

The right-hand side is the cost of delay (RN-10 sec. 7.1); the left is what the curve pays for it. Tight binding makes the right-hand side large for even small k, so tightly bound work is on the paying side at essentially any price - which is what "cannot be moved" means once it is written down. This is the ordinary participation condition of a liquidity supplier [1], and it does not make the camps price-dependent: tightness is intrinsic, and the price determines only whether a supplier finds the premium worth taking today.

## 2. The allocation problem

Let C(t) be the execution capacity available at quantum t. The protocol, or the market it hosts, chooses an allocation x_i(s, t) >= 0: the amount of project i's work arriving at s that is executed at quantum t. The **execution-capital allocation problem** is

```text
maximize    sum_i sum_s sum_{t >= s}  v_i(s, t) * x_i(s, t)              (TET)

subject to  sum_i sum_s x_i(s, t)   <=  C(t)        for all t            (capacity)
            sum_{t >= s} x_i(s, t)  <=  A_i(s)      for all i, s         (conservation)
            x_i(s, t) = 0                           for t < s            (causality)
            + neutrality, reducibility, incentive-compatibility           (below)
```

The objective is **temporal economic throughput** (TET), defined in RN-08 and adopted as the allocator's target in RN-10 sec. 12: value-weighted execution, where the weight already encodes deadline success and delay cost through phi. Maximizing transaction count is the degenerate case v_i identically 1. The formulation is a divisible flow: x is continuous, so the program is a linear (transportation-type) problem. Real transactions are atomic and lumpy, which turns it into an integer program where the shadow-price reading below holds only approximately - a caveat carried into sec. 4.

Three constraints distinguish this from a textbook scheduling problem, and each is a live research question:

- **Neutrality.** x may depend on declared temporal characteristics (phi, and verified properties of A) but not on the identity of i: two projects submitting identical characteristics receive identical treatment. Formally this is an anonymity property of the declaration-to-allocation map, not a constraint on a single instance.
- **Reducibility (RN-07).** The chosen x must be implementable as per-slot local parameters a builder applies deterministically, without global coordination inside the slot. A globally optimal x that cannot be so compiled is not admissible.
- **Incentive compatibility.** phi is declared. The mechanism must make truthful declaration optimal, or make over-claiming self-penalising through cost, bonding, or verification against realized behavior (RN-02). Without this the problem is solved on fiction.

These three are mechanism-level: imposing them turns the linear program into a mechanism-design problem whose optimum generally differs from the first-best. The consequence for the prices is the subject of the next section.

## 3. The dual gives the efficient term structure

Attach a multiplier p(t) >= 0 to each capacity constraint. At an optimum, complementary slackness gives p(t) > 0 only where capacity binds, and a unit of work arriving at s is executed at the quantum t maximizing v_i(s, t) - p(t) (when that maximum is non-negative; otherwise it is not executed).

> **The shadow prices {p(t)} on per-quantum capacity are the *efficient* block-fee-rate curve** (RN-10 sec. 6): the term structure a planner maximizing TET, given demand and capacity, would set.

This is a first-best object, and the qualifier matters. Because neutrality, reducibility, and incentive compatibility are mechanism-level (sec. 2), the curve an implementable mechanism prints generally departs from {p(t)}; the departure is not noise but the price of implementability, and closing it is part of the agenda (sec. 8). The *observed* market curve is a different construction, developed in Part II. With that distinction kept, several of RN-10's claims are consequences of the efficient dual:

- **Deployed versus undeployed capacity** (RN-10 sec. 4) is the distinction between binding and slack capacity constraints: p(t) = 0 exactly where capacity is not scarce. This is the note's contact with the bond intuition of sec. 4 below - capacity that is not deployed earns nothing, as idle money earns no interest.
- **A term rate below spot for committed demand** (RN-10 sec. 6.2) follows because a project with wide phi can be served wherever p(t) is low: its effective price is an average over cheap quanta, not the peak. (An equilibrium claim: it assumes the flexible demand stays marginal and does not itself lift the off-peak prices.)
- **The event-driven segment** (RN-10 sec. 7.1, sec. 9) is the case of **correlated targets with small W**: one external event sets tau_i to the same quantum for many projects at once, each with a narrow phi, so that capacity constraint binds hard and p(t) spikes. Correlation enters through tau, tightness through phi - the two features of a surge, kept separate.
- **The three flexibility grades** (RN-10 sec. 9.5) are bands of W: quantum-indifference is flexibility within a slot, delayability across slots, callability the sale of an option on one's own allocation.
- **The two camps** (RN-10 sec. 7) are the sign of W_i(alpha) - kappa, and the market of RN-10 sec. 8 is the trade between them at the price differential p(t) - p(t+k).
- **Fee-as-filter** (RN-10 sec. 5) is the sharpest consequence. A scalar spot fee is the degenerate mechanism that observes one number per transaction instead of phi. It therefore cannot separate projects differing *only* in phi; and since what it does observe is willingness to pay at the moment of arrival, it systematically serves demand with narrow phi and high V while excluding demand whose value lies in flexibility, predictability, or continuity. The filtering effect is not an implementation accident - it is what happens when a mechanism's message space is too small to express the arguments of the objective.

---

# Part II — The market term structure

## 4. The block-fee-rate is a rate: mapping the bond market to the fee market

The efficient curve of Part I is a planner's construct. The *observed* term structure is a market price, and the cleanest way to read it is by analogy to the interest-rate term structure.

The block-fee-rate at quantum t is the **yield on execution capital deployed at t**. Capacity that is supplied and used earns that rate; capacity left idle earns nothing, as money not lent earns no interest - which is the deployed-versus-undeployed distinction of RN-10 sec. 4 and the p(t) = 0-on-slack condition of sec. 3, seen from the supply side. The term structure is then the schedule of these rates across future quanta: what execution delivered at t costs today.

The analogy is not only methodological; it holds at the level of the underlying asset, and this corrects a tempting error. Execution is not a perishable good. Because time is endogenous - the protocol produces a next slot, and the network's capacity regenerates identically - execution capacity is **durable capital**. A slot is one period's *service flow* of that capital: the flow is used-or-lost within the slot, as a machine's output is, but the capital that produces it persists. Idle capacity forgoes that period's yield without being destroyed, as capital not lent forgoes interest without being consumed. This is the standard capital/rental structure - a durable asset whose per-period service is priced by a rental rate - and it is what makes the bond apparatus fit: the block-fee-rate is the rental rate (the yield on execution capital deployed in a slot), the term structure is the schedule of forward rental rates, and **principal is present** - the capital value of a durable claim on capacity, equal to the present value of the rates it will earn. RN-10's name for the object, execution *capital*, is the accurate one.

The mapping is worth setting out on its own, because the empty rows are the finding.

| Rates market | Fee-market counterpart | In today's fee market |
|---|---|---|
| Overnight / spot rate | Spot inclusion: base fee + priority tip | Exists (EIP-1559) |
| Zero-coupon bond (one future date) | Future-slot fee: a ticket for execution at quantum t | Missing; early forms in preconfirmations and execution tickets [7] |
| Yield curve / term structure | Block-fee-rate curve across future quanta | Missing - only the spot point is priced |
| Forward rate | Forward block-fee-rate f(0,t) | Missing - no future-dated prices to imply it |
| Coupon bond + principal | Durable capacity claim: periodic yield + capital (resale) value | Missing; nascent in validator rights, reserved leases |
| Fixed-for-floating swap | Fee swap over N quanta, marked to market | Missing |
| Options / swaptions | Callable allocation; express-lane ordering right | Partial (Timeboost [8]) |
| Idle cash earns 0 | Undeployed capacity earns 0 | Inherent (durable capital) |

What the mapping reveals is structural, not incremental: today's fee market prices only the front of the curve. It has an overnight rate and no curve. Every future-dated instrument - the zero, the forward, the term structure, the swap - is absent, so participants cannot see, price, or hedge the cost of execution at a future quantum. A project that needs a slot next week has no way to buy or price it today; it can only bid at the spot when the moment arrives.

This is the note's practical contribution. The bond market's completed instrument set is a checklist of what a temporally complete fee market would need, and the empty rows are the design agenda - candidate protocol primitives, most naturally EIPs, introduced in the order the bootstrap needs them: the future-slot ticket first (the zeros anchor the curve), then the swap (hedging and the long end). Because each proposed primitive has a mature analog whose economics, no-arbitrage constraints, and failure modes are known, a future-slot fee proposal can be evaluated against an established theory rather than designed ad hoc. That is the sense in which this mapping is a theoretical foundation for future-slot fee design, not only an analogy.

## 5. The instrument space

The observed curve is bootstrapped from the prices of traded instruments. Their fee-market counterparts:

### 5.1 Spot inclusion - the overnight rate

The price of execution now: base fee plus priority tip for next-block inclusion. It is the front of the curve and already observable on-chain.

### 5.2 The future-slot fee - the zero-coupon claim

A claim bought at time 0 that delivers one unit of execution (one unit of gas, or of reserved capacity) at a single future quantum t. Its price P(0, t) is the **zero-coupon block-fee-rate** to maturity t - the price today of execution delivered at t - and the curve t -> P(0, t) is the term structure in its purest form. The protocol primitive that makes it trade is a **future-slot auction / transaction ticket** (in the family of execution tickets and preconfirmations [7]); its clearing price is P(0, t). This is the primary instrument to specify, most likely as an EIP, because the zero-coupon curve is what everything else bootstraps against.

### 5.3 The coupon bond - the durable capacity claim

A coupon bond pays periodic coupons plus principal. Its counterpart is a **durable, transferable claim on execution capacity** that yields periodic execution (the coupons) and carries a capital value (the principal). Because time is endogenous (sec. 4), such a claim persists, and its capital value is the present value of the block-fee-rates it will earn. This is where principal lives - the durable side of the market, whose nascent forms are a validator's block-production right and a long-lived, transferable reserved-capacity lease. Transferability is what turns a single-use ticket into a principal-bearing claim, so whether tickets are transferable decides whether the market has a capital side at all. For *constructing the curve*, though, this instrument is redundant: its price is implied by the zeros and the swap, so the bootstrap (sec. 6) needs only those.

### 5.4 The fee swap - the workhorse

The instrument a real project would demand. Over a horizon of N quanta (e.g. 10 slots, or a week of slots), a fixed-for-floating swap on a capacity notional Q per quantum:

- **Floating leg:** each quantum t, the realized execution price p(t).
- **Fixed leg:** a fixed per-quantum rate F.
- **No principal exchanged.** Only the difference is settled; the notional is a scale, never delivered - as in an interest-rate swap.
- **Marked to market each quantum:** at t, settle (p(t) - F) * Q; the position is re-valued against the current forward curve.

A rollup, market maker, or oracle with continuous demand uses it to fix its per-quantum execution cost over a week without holding capacity it cannot store. The counterparty taking the floating side - a validator, searcher, or capacity provider - is the supply side of RN-10's two-sided market. The **par fee-swap rate** F*(N) is the fixed rate giving the swap zero value at inception,

```text
F*(N) = ( sum_{t=1..N} D(0,t) * f(0,t) )  /  ( sum_{t=1..N} D(0,t) )
```

with f(0,t) the forward block-fee-rate to t and D(0,t) a discount factor. Observing F*(N) across horizons pins the curve at the long end, as swap rates do in the fixed-income swap curve [1].

### 5.5 Options - convexity, not the base curve

Callable allocations (RN-10 grade-3 flexibility) and ordering rights such as Timeboost's express lane [8] are options on the rate - caps, floors, the right to execute or reorder. Their prices carry volatility information and would extend the framework to a volatility surface; they are not needed for the base curve and are placed here only for completeness.

## 6. Bootstrapping the observed curve

Given the instrument prices, construct the forward block-fee-rate curve f(0,t) under no-arbitrage (the Fundamental Theorem of Asset Pricing: absence of arbitrage is equivalent to a positive linear pricing functional [4]):

1. **Front:** the spot (sec. 5.1) fixes f(0,0).
2. **Zeros:** each future-slot price P(0,t) (sec. 5.2) fixes the delivery price at t; with a discounting convention this yields D(0,t) and the forward f(0,t) at each traded maturity.
3. **Long end / gaps:** par fee-swap rates F*(N) (sec. 5.4) constrain discount-weighted averages of the forwards over [1,N], filling maturities where zeros are illiquid - the standard bill-then-swap bootstrap [1].
4. **Interpolation** across untraded quanta completes the curve; its dynamics are a forward-rate model in the sense of Heath-Jarrow-Morton [3], the stochastic object RN-10 sec. 6.8 asks for.

The curve so built is whatever the two-sided auction of demand and supply prints, made mutually consistent by no-arbitrage - not the output of a chosen objective.

## 7. Observed versus efficient

Part I and Part II give two curves. The dual {p(t)} is the **efficient** curve - what a TET-maximizing planner would set given (A, tau, V, phi) and C. The bootstrapped f(0,t) is the **observed** curve - what the market prints. Their difference is the object of interest: the gap between the market's price of time and the efficient one, which measures illiquidity, market power, extraction, and incentive loss. Part I supplies the benchmark; Part II supplies the observation; RN-10's economics is the account of why the two differ and what would narrow the gap.

## 8. The research programme this opens

Writing the problem down makes its open parts precise. From Part I:

1. **Existence and structure of the dual.** For the finite divisible program, shadow prices exist by strong duality; what is open is *uniqueness* (degeneracy admits a non-unique curve) and existence in the stochastic and continuum limits.
2. **Incentive compatibility.** Can declaration of phi be made truthful, or approximately so, under the impossibilities that bound transaction-fee mechanisms [2]? This is where the program expects the hardest obstruction. The width statistic W(alpha) narrows it: a mechanism need not elicit all of phi, only enough of its width to place work on one side of kappa; understating width is self-penalising, overstating is what must be defended against. Value V is declared too and, in a fee mechanism, revealed through willingness to pay.
3. **Reducibility.** Which optimal or near-optimal allocations compile to per-slot local parameters (RN-07), and what is the welfare price of restricting to those that do?
4. **Stochastic formulation.** A is uncertain, so Part I is the certainty-equivalent case; the proper object is a stochastic control problem whose dual is the *forward* curve (sec. 6, step 4).
5. **Tractability and atomicity.** Even the deterministic problem is a large assignment problem, and real work is indivisible; a practical engine needs approximation with provable loss bounds, and the shadow-price reading needs its integer-programming caveat made precise.

From Part II:

6. **The minimal spanning set.** Which instruments must trade for the curve to be identified - is spot plus future-slot tickets plus a swap enough, and at which maturities?
7. **The future-slot auction (EIP).** How to auction a transaction/execution ticket for quantum t neutrally and extraction-resistantly; the auction is the price source, so its manipulation-resistance bounds the curve's reliability.
8. **Transferability and the principal residual** (sec. 5.3): should tickets be resellable, and what does a secondary market do to neutrality and to the front of the curve?
9. **Swap settlement on-chain:** notional convention, per-quantum or per-epoch mark-to-market, collateral, and the reference index for the floating leg.
10. **Liquidity.** The bootstrap assumes tradeable prices; thin or intermittent instrument markets make the curve noisy or unidentified. Which maturities can realistically be liquid?

The claim is that the apparently disparate parts of RN-10 - projects, capacity across time, fee-as-filter, the term structure, the two camps, and the reserve - are facets of one problem and its two curves. That unification is the contribution; the questions above are the work it makes possible, tracked with the rest of the agenda in **RN-10 Follow-up Research Questions**.

---

## References

[1] Demsetz, H. "The Cost of Transacting." *Quarterly Journal of Economics* 82(1), 1968, 33-53. Grossman, S. J. & Miller, M. H. "Liquidity and Market Structure." *Journal of Finance* 43(3), 1988, 617-633. Foucault, T., Kadan, O. & Kandel, E. "Limit Order Book as a Market for Liquidity." *Review of Financial Studies* 18(4), 2005, 1171-1217. (Liquidity as immediacy; sorting by patience. RN-10 sec. 8.1 and sec. 8.8.) Hull, J. C. *Options, Futures, and Other Derivatives* (bootstrapping the zero curve; swaps and the par-swap-rate construction, sec. 5-6).

[2] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM*, 2024. (The impossibility results that bound sec. 8, question 2.)

[3] Heath, D., Jarrow, R. & Morton, A. "Bond Pricing and the Term Structure of Interest Rates." *Econometrica* 60(1), 1992, 77-105. (Forward-rate dynamics; the stochastic formulation of sec. 8, question 4, and sec. 6.)

[4] Harrison, J. M. & Kreps, D. "Martingales and Arbitrage in Multiperiod Securities Markets." *Journal of Economic Theory* 20, 1979; Harrison, J. M. & Pliska, S. R. (1981). (No-arbitrage iff a positive linear pricing functional exists; the foundation of the bootstrap in sec. 6.)

[5] Vasicek, O. "An Equilibrium Characterization of the Term Structure." *Journal of Financial Economics* 5(2), 1977; Cox, J., Ingersoll, J. & Ross, S. "A Theory of the Term Structure of Interest Rates." *Econometrica* 53(2), 1985. (Equilibrium / stochastic-discount-factor term-structure models, calibrated to an observed curve - the optimization foundation for the curve, distinct from the allocation dual of Part I.)

[6] Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014, 2023. (Pricing one temporal dimension - urgency - which sec. 3's fee-as-filter generalizes.)

[7] Future-slot claims on execution (the nascent forms cited in sec. 4 and sec. 5.2): Neuder, M. & Drake, J. *Execution Tickets.* Ethereum Research (ethresear.ch), 2024 - an auctioned, protocol-issued right to construct the execution payload for a future slot. Drake, J. *Based Preconfirmations.* Ethereum Research (ethresear.ch), 2024 - a credible commitment to include a transaction at a coming slot; see also *Towards an Implementation of Based Preconfirmations Leveraging Restaking,* Ethereum Research, 2024, https://ethresear.ch/t/towards-an-implementation-of-based-preconfirmations-leveraging-restaking/19211. These are research-stage proposals, not finalized EIPs.

[8] Arbitrum Timeboost (auctioned express-lane ordering right). Offchain Labs documentation.

[9] TLM Research Notes: RN-10 (the economics), RN-01/02 (demand representation and verification), RN-05 (the quantum lattice), RN-07 (the reducibility invariant), and RN-10 Follow-up Research Questions (the full agenda).

---

*Changes from v0.1.* The term-structure analysis (formerly drafted as RN-12) is folded in as Part II: the block-fee-rate read as a yield with the bond analogy (sec. 4), the instrument space (sec. 5), the no-arbitrage bootstrap (sec. 6), and the observed-versus-efficient reconciliation (sec. 7). Part I's central identification is corrected: the allocation dual is the *efficient* term structure (a first-best benchmark), not the observed curve, resolving the conflation between the welfare dual and the market curve. Divisibility/atomicity and the mechanism-level status of the three constraints are now stated. The perishability framing is replaced with the durable-capital reading (execution capacity persists because time is endogenous), so principal is present as the capital value of a durable capacity claim. Reference [7] now cites the execution-ticket and based-preconfirmation proposals.
