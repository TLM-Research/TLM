---
id: RN-11
title: "The Temporal Liquidity Market: A Formal Foundation"
subtitle: "The block-fee-rate term structure and the execution-capital allocation problem"
version: v0.3
status: "Public draft. The formal center of the TLM program; stated, not solved."
program: "Temporal Liquidity Market (TLM)"
date: August 5, 2026
---

# RN-11 -- The Temporal Liquidity Market: A Formal Foundation

## Abstract

RN-10 argues at the level of economic structure: a blockchain allocates execution capital across time, execution capacity has a time value expressible as a term structure, and temporal liquidity is a two-sided market between execution demand that can absorb the drift between wall-clock relevance and block-time execution, and demand that cannot. This note gives that argument its formal center, in two parts.

**Part I** continues RN-10's term-structure reading. The block-fee-rate is a rate -- a yield on execution capital deployed in a slot -- and the curve is the schedule of those rates across future quanta, a no-arbitrage fee curve constructed by bootstrapping from traded temporal instruments in the manner of the interest-rate term structure. Read this way, today's fee market prices only the front of the curve: it has a current fee rate -- the price of inclusion in the very next slot -- and nothing further out. The note maps the instruments a temporally complete fee market would need -- a future-slot *zero* (a zero-coupon claim: paid for today, it delivers execution at one future quantum and nothing else), a fee swap (a contract that exchanges the floating, uncertain future fee rates over a time period for a fixed rate agreed today, so a project can lock its execution cost over a time period), and a swaption (the right to enter such a fee swap) -- and gives the bootstrap that would build the curve from their prices. The fee swap is two-sided by construction, which is where the two camps of temporal liquidity meet as counterparties.

**Part II** asks what that curve prices, and represents demand with a *shape in time*: an arrival process, a relevance target, a value scale, and a decay function, so a project's delay tolerance, deadline, decay rate, and binding tightness are read off one representation. In this multi-slot, multi-quantum setting the value-weighted allocation has a dual -- shadow prices on capacity that say what execution at each quantum is worth to a planner. These are a welfare benchmark, not a market price, and the note does not identify them with the Part I term structure; whether a decentralized fee market reproduces them is left open.

The mathematics both parts use -- knapsack, LP duality, no-arbitrage bootstrapping, optimal execution -- is standard and credited to appendices; what is new is the setting and the variables: demand's time-shape, temporal liquidity as a two-sided conserved commodity, and the allocation whose dual values capacity over time. The problem is stated, not solved; a candidate mechanism is RN-12.

## 0. Relationship to the other notes

RN-10 is the economics and is self-contained; this note is its formal counterpart and assumes it. The lattice of quanta is RN-05; the demand representation is RN-01/02; the reducibility constraint is RN-07; verification of declared characteristics is RN-02. The concrete clearing mechanism is RN-12. Questions this note opens are tracked in **RN-10 Follow-up Research Questions**.

References of the form "RN-10 sec. N" point to the economics note; internal references are to this note's own sections. Results borrowed from other literatures are stated where used and detailed in the appendices, one per source, so the note stays self-contained without re-deriving standard material.

## What is new, and what is not

The tools in this note are standard; the contribution is the formulation that combines them. Stated plainly, so the credit is clear:

**Not new -- borrowed, and credited where used.** The term-structure construction -- zeros, forwards, swaps, the no-arbitrage bootstrap -- is standard fixed income (App. B). Block-building as a knapsack (App. A). The optimal-execution parallel and the Markov-decision-process reading of scheduling (App. C). Order-fairness impossibility and the revenue-versus-fair-ordering tradeoff (App. D). The transaction-fee-mechanism impossibilities (App. E). Cryptographic hiding -- commit-reveal, threshold encryption, timed commitments (App. F). Execution tickets, preconfirmations, and the concentration risk of transferable rights (sec. 7). Two-sided markets and liquidity provision as economics. None of this is claimed as original.

**New -- the setting and the variables.**

1. *Demand as a shape in time* (sec. 5). The execution-capital demand function: arrival separated from a relevance target, decay phi measured against the target so its argument is the drift `T_block - T_wall`, phi a function -- not a scalar urgency -- with two-sided shapes and a binding-tightness width `W(alpha)`. Fee-as-filter, that a scalar fee cannot separate projects differing only in phi, is the consequence.
2. *Temporal liquidity as a two-sided, conserved commodity* (sec. 7). Time-flexibility itself as a supplied asset; advancement exists only as deferral plus released reserve; the two camps are partitioned by tightness, and they meet as the two sides of a fee swap (sec. 2.4).
3. *The allocation and its dual* (sec. 6). The multi-slot, multi-quantum problem whose objective is temporal economic throughput, and whose shadow prices value capacity over time -- a benchmark distinct from, and not identified with, the market term structure of Part I.

One caveat kept in view throughout: the relation between the shadow-price benchmark and the market curve is asserted nowhere as an identity; it is an open question (secs. 10-11). The contribution is a formulation, not a theorem.

---

# Part I -- The block-fee-rate term structure

Part I continues RN-10's reading of execution capacity as a term structure. It is the market object: a fee curve along time, constructed the way an interest-rate curve is. The construction is standard fixed income (App. B); what is new is the mapping to the fee market, the observation that today only the front is priced, and the reading of the fee swap and swaption as the instruments through which the two camps of temporal liquidity would trade.

## 1. The block-fee-rate is a rate: mapping the bond market to the fee market

The block-fee-rate at quantum t is the **yield on execution capital deployed at t**. Capacity that is supplied and used earns that rate; capacity left idle earns nothing, as money not lent earns no interest -- the deployed-versus-undeployed distinction of RN-10 sec. 4, and the p(t) = 0-on-slack condition of the allocation dual (sec. 6), seen from the supply side. The term structure is the schedule of these rates across future quanta: what execution delivered at t costs today.

The analogy holds at the level of the underlying asset, and this corrects a tempting error. Execution is not a perishable good. **The capital is the network itself** -- a durable, productive asset that throws off execution capacity each slot the way a machine throws off output, and that persists, regenerating identically because time is endogenous (the protocol produces the next slot). A slot's capacity is one period's *service flow* of that capital: used-or-lost within the slot, but the network that produces it endures. The fee is what the network earns for that service; spoken from the network owner's side -- validators, stakers, or the holder of a transferable claim on capacity -- it is the return on capital. So the block-fee-rate is the rental rate (the fee per period of deployed capacity), the term structure is the schedule of forward rental rates, and **principal is present**: the capital value of the network's fee stream, the present value of the rates it will earn. Idle capacity forgoes that period's return without destroying the capital, as capital not lent forgoes interest without being consumed. RN-10's name for the object, execution *capital*, is the accurate one -- the network is what holds it.

The mapping is worth setting out on its own, because the empty rows are the finding.

| Rates market | Fee-market counterpart | In today's fee market |
|---|---|---|
| Overnight / spot rate | Spot inclusion: base fee + priority tip | Exists (EIP-1559) |
| Zero-coupon bond (one future date) | Future-slot fee: a ticket for execution at quantum t | Missing; early forms in preconfirmations and execution tickets [7] |
| Yield curve / term structure | Block-fee-rate curve across future quanta | Missing -- only the spot point is priced |
| Forward rate | Forward block-fee-rate f(0,t) | Missing -- no future-dated prices to imply it |
| Coupon bond + principal | Durable capacity claim: periodic yield + capital (resale) value | Missing; nascent in validator rights, reserved leases |
| Fixed-for-floating swap | Fee swap over N quanta, marked to market | Missing |
| Swaption | Option to enter a fee swap at a preset rate | Missing |
| Callable / express-lane | Callable allocation; ordering right | Partial (Timeboost [8]) |
| Idle cash earns 0 | Undeployed capacity earns 0 | Inherent (durable capital) |

What the mapping reveals is structural: today's fee market prices only the front of the curve. It has an instantaneous spot rate and no curve. Every future-dated instrument -- the zero, the forward, the term structure, the swap -- is absent, so participants cannot see, price, or hedge the cost of execution at a future quantum. A project that needs a slot next week has no way to buy or price it today; it can only bid at the spot when the moment arrives.

This is the mapping's contribution: the bond market's completed instrument set is a checklist of what a temporally complete fee market would need, and the empty rows are the design agenda -- candidate protocol primitives, most naturally EIPs, introduced in the order the bootstrap needs them: the future-slot ticket first (the zeros anchor the curve), then the swap (hedging and the long end), then the swaption (convexity). Because each proposed primitive has a mature analog whose economics, no-arbitrage constraints, and failure modes are known (App. B), a future-slot fee proposal can be evaluated against an established theory rather than designed ad hoc.

## 2. The instrument space

The observed curve is bootstrapped from the prices of traded instruments. Their fee-market counterparts:

### 2.1 Spot inclusion -- the instantaneous spot rate

The price of execution now: base fee plus priority tip for next-block inclusion. It is the front of the curve and already observable on-chain.

### 2.2 The future-slot fee -- the zero-coupon claim

A claim bought at time 0 that delivers one unit of execution (one unit of gas, or of reserved capacity) at a single future quantum t. Its price P(0, t) is the **zero-coupon block-fee-rate** to maturity t -- the price today of execution delivered at t -- and the curve t -> P(0, t) is the term structure in its purest form. The protocol primitive that makes it trade is a **future-slot auction / transaction ticket** (in the family of execution tickets and preconfirmations [7]); its clearing price is P(0, t). This is the primary instrument to specify, most likely as an EIP, because the zero-coupon curve is what everything else bootstraps against.

### 2.3 The coupon bond -- the durable capacity claim

A coupon bond pays periodic coupons -- interest at a rate x% on its principal -- plus the principal at maturity. Its counterpart is a **durable, transferable claim on execution capacity**: each period the capacity it entitles is deployed and earns fees, and those fees are the coupon. The coupon rate is a fee yield -- a claim with capital value P that earns a fee f each period yields x% = f / P -- so **interest, in the bond, is fee, in the chain**: the block-fee-rate is the rate at which deployed execution capital pays, exactly as a coupon is the rate at which lent principal pays. The principal is the claim's capital value, the present value of the fees it will earn (sec. 1). This is where principal lives -- a validator's block-production right, a long-lived reserved-capacity lease. Transferability is what turns a single-use ticket into a principal-bearing claim (sec. 7). For *constructing the curve*, though, this instrument is redundant: its price is implied by the zeros and the swap, so the bootstrap (sec. 3) needs only those.

### 2.4 The fee swap -- the workhorse, and it is two-sided

The instrument a real project would demand, and the one where the two camps of temporal liquidity (sec. 7) meet as counterparties. Over a horizon of N quanta, a fixed-for-floating swap on a capacity notional Q per quantum exchanges a fixed per-quantum rate F for the realized floating rate p(t): only the difference (p(t) - F)·Q is settled each quantum, the notional is never delivered, and the position is marked to market against the current forward curve.

**The swap has two sides, and they are the two camps.** The **fixed-rate payer** buys cost certainty -- it pays F and receives p(t), so a congestion spike in the realized rate is offset; this is demand that values predictability, hedging its execution cost (a rollup, an oracle, a market maker with continuous demand). The **floating-rate payer** takes the other side -- receiving F, paying p(t) -- warehousing fee-rate risk for the fixed premium; this is supply that can bear the variability (a validator, searcher, or capacity provider). Fixed-for-floating and floating-for-fixed are the two camps in one instrument: one locks its cost, the other is paid to absorb the swing. Where the spot temporal-liquidity trade (sec. 7) moves *position* between a patient and an urgent party, the swap moves *rate risk* between a predictability-seeking and a risk-bearing party -- the same two-sided structure on the second temporal axis.

The **par fee-swap rate** F*(N) is the fixed rate giving the swap zero value at inception,

```text
F*(N) = ( sum_{t=1..N} D(0,t) * f(0,t) )  /  ( sum_{t=1..N} D(0,t) )
```

with f(0,t) the forward block-fee-rate to t and D(0,t) a discount factor. Observing F*(N) across horizons pins the curve at the long end, as swap rates do in the fixed-income swap curve [1] (App. B).

### 2.5 The swaption -- the option to enter a swap

A **swaption** is the right, not the obligation, to enter a fee swap at a preset fixed rate over a future window. It prices the *volatility* of the fee curve rather than its level: a project with contingent demand -- unsure whether it will commit, and so whether it will need to lock its cost -- buys the right to strike a swap later instead of committing now. It is the convexity instrument the mapping predicts, extending the framework to a volatility surface and letting a project hedge the *possibility* of future congestion rather than a known exposure. Callable allocations (RN-10 grade-3 flexibility) and ordering rights such as Timeboost's express lane [8] are the other options on the rate. How a swaption is realized as a protocol mechanism -- what it means to hold, price, and exercise an option on a future on-chain fee swap -- is left to RN-12; here it is noted as the instrument the term-structure reading predicts, and as one the two camps could use to trade the *option* on future flexibility, not only flexibility itself.

## 3. Bootstrapping the observed curve

Given the instrument prices, construct the forward block-fee-rate curve f(0,t) under no-arbitrage -- absence of arbitrage is equivalent to a positive linear pricing functional [4] (App. B):

1. **Front:** the spot (sec. 2.1) fixes f(0,0).
2. **Zeros:** each future-slot price P(0,t) (sec. 2.2) fixes the delivery price at t; with a discounting convention this yields D(0,t) and the forward f(0,t) at each traded maturity.
3. **Long end / gaps:** par fee-swap rates F*(N) (sec. 2.4) constrain discount-weighted averages of the forwards over [1,N], filling maturities where zeros are illiquid -- the standard bill-then-swap bootstrap [1].
4. **Interpolation** across untraded quanta completes the curve; its dynamics are a forward-rate model in the sense of Heath-Jarrow-Morton [3], and swaption prices would calibrate its volatility.

The curve so built is whatever the two-sided auction of demand and supply prints, made mutually consistent by no-arbitrage -- not the output of a chosen objective. Part II asks what that curve prices, and whether the price is efficient.

---

# Part II -- The temporal allocation problem

Part I priced capacity from the outside, as a market curve. Part II asks what the curve prices: the allocation of capacity across quanta to demand that has a shape in time. Most of the allocation machinery is standard, and this part takes those results rather than re-derive them, so the body can dwell on what is new -- the demand representation (sec. 5), the dual as a benchmark (sec. 6), and temporal liquidity as a conserved two-sided commodity (sec. 7).

## 4. The setting, and the part that is standard

Execution happens in slots, and RN-05 divides each slot into time-ordered quanta t = 0, 1, 2, ... (RN-10 sec. 6.9). What the term structure prices is the allocation of that capacity across quanta to demand that has a position in time. What makes it more than scheduling is the drift between when work is relevant in wall-clock terms and when the chain executes it (RN-10 sec. 7): `T_block - T_wall`, on the lattice.

Much of the allocation is standard, and we use those results rather than re-derive them. A single slot is a 0/1 knapsack -- maximize included fee under a gas limit -- NP-hard, with greedy value-density selection (which is what priority-fee ordering implements) near-optimal for small items [13] (App. A); its capacity multiplier is the base fee, the spot point of Part I's curve. The lattice turns packing into sequencing: once a transaction's value depends on what precedes it -- a backrun after its target, a sandwich around a victim, an arbitrage against prior state -- the objective is order-dependent and no longer separable, and whoever controls the order captures the difference. That captured value is the builder's power, and it is why the ordering rule cannot be left to the party that profits from it. Real blocks add precedence, conflicts, and all-or-nothing bundles, making the operative problem a precedence-constrained, sequence-dependent mixed-integer program (App. A), intractable at scale (sec. 9).

**One new design choice belongs here.** The lattice lets the protocol price the *quantum* a transaction lands in without pricing its *position within* that quantum. Making quantum assignment the market object, and leaving intra-quantum order protocol-randomized or unordered, keeps the temporal-liquidity market separate from the MEV ordering market: a project buys *when* it executes to the granularity of a quantum, not the right to sit immediately before a victim. This narrows what can be sold, in exchange for cutting the ordering rents that pit revenue against fair ordering [14] (App. D), and it fixes what fairness (sec. 8) must protect -- the assignment map, not a within-quantum permutation the protocol declines to sell.

## 5. The execution-capital demand function

This is the note's central new object: demand represented not by a scalar fee but by a shape in time.

A project i has four components of demand:

- an **arrival process** A_i, where A_i(s) is the quantity of execution work that becomes submittable at quantum s;
- a **target** tau_i(s), the quantum at which work arriving at s is *relevant* in wall-clock terms -- the lattice image of T_wall;
- a **value scale** V_i(s) >= 0, the value of executing a unit of that work at its target;
- a **decay function** phi_i mapping integers to [0,1], normalized so phi_i(0) = 1 at the target -- the fraction of peak value kept when execution drifts d = t - tau quanta off-target. phi_i need not be monotone or single-peaked (below).

The value to project i of executing, at quantum t, a unit of work that arrived at s <= t is

```text
v_i(s, t) = V_i(s) * phi_i( t - tau_i(s) )
```

**Arrival and target are separate.** Measuring decay from arrival would assume work becomes relevant when it becomes submittable, and that fails for the class RN-10 sec. 7 is built around: a mint opening at a published block, a scheduled expiry, a funding settlement can all be submitted long before they are relevant, so tau is known far in advance while the work stays immovable. Decay against tau holds *foreseeable* and *tightly bound* at once; a single-index form cannot. The argument of phi is the drift RN-10 sec. 7 names: **`t - tau` is `T_block - T_wall` on the lattice**, and phi is the tolerance for it. phi is defined on all integers, because for target-bound work executing *early* destroys value as surely as late -- an oracle update before its event is worthless; setting tau_i(s) = s recovers ordinary work relevant as soon as it exists.

**Decay shapes are not one family.** phi is declared per unit of work and takes many shapes, each a different demand: a step (a hard deadline), an exponential (a constant hazard of irrelevance), a linear ramp, a plateau-then-cliff; periodic or multi-window value (an oracle updating on a schedule, or work with several acceptable windows), where phi has several peaks and is not monotone, so a quantum farther from the main peak can be worth more than a nearer one; two-sided shapes for target-bound work; and event-driven (option-like) value that is near zero until a state omega occurs and then large and short-lived -- the liquidation case. The shape, not just a single deadline, is what the mechanism must cope with, and it is *declared* while A is largely *observed* (RN-02). **This is why a scalar fee cannot represent demand: it sees one number, and phi is a function.**

**For some projects value is not separable across transactions.** A continuous exchange, a rollup posting, or an oracle stream values the *shape of service over time*, not each transaction alone. Its value is V_s(x_s) over the whole schedule, and a workable form penalizes instability and jitter:

```text
V_s(x_s) = sum_t u_s( X_{s,t} )  -  lambda_s * Var_t( X_{s,t} )  -  mu_s * sum_t | X_{s,t} - X_{s,t-1} |
```

where X_{s,t} is the project's executed volume in slot t: per-period utility, less a variance penalty, less a jitter penalty. This is where TLM departs from an independent-transaction knapsack -- continuity and predictability are properties of the *joint* allocation -- so proportional fairness over totals does not by itself deliver smooth service.

A consequence for trading: because the value is joint, the cost of reassigning one held quantum of a stream is the *marginal* effect on V_s(x_s), not a local phi difference -- moving a single execution can raise the stream's variance or jitter even where that execution's own phi is flat. So the supply condition generalizes: a stream lends out a held quantum when the price paid exceeds the marginal loss in V_s(x_s), and supplies only the flexibility that keeps its whole schedule within tolerance. Its quanta cannot be reassigned one at a time in isolation.

The tuple **ECDF_i = (A_i, tau_i, V_i, phi_i)** recovers the umbrella dimensions (Vision; RN-01) as properties of phi, tau, and A: delay tolerance is how slowly phi decays; the deadline is the smallest d with phi_i(d) = 0; the decay rate is phi's shape; binding tightness is phi's width; duration and intensity are the support and magnitude of A; predictability is the forecastability of A and tau.

**Binding tightness, formally.** Fix a tolerance alpha in (0,1). The tolerance width W_i(alpha) = |{ d : phi_i(d) >= alpha }| counts the quanta over which the work keeps at least alpha of its value -- a single interval when phi_i is single-peaked, a union of intervals when it is not, but always the full set of quanta to which the work may be reassigned without dropping below alpha, so the statistic needs no monotonicity assumption. The two camps of RN-10 sec. 7 are a threshold on width: fixing kappa, work is tight-binding (a taker) when W_i(alpha) <= kappa and loose-binding (a supplier) when W_i(alpha) > kappa. Tightness is a property of phi, predictability a property of the joint law of (A_i, tau_i); the two axes are independent, which is why all four cells of RN-10 sec. 7.3 are non-empty, and the partition applies to executions, not participants -- one project may emit W = 1 liquidation work and W = 10^4 batch work. kappa is not free: its natural scale is the autocorrelation length of the price p(t), so work is tight-binding when it cannot outlast a congestion episode, which makes the partition and the price a joint fixed point. Loosely bound work supplies liquidity at t when the price to move it, p(t) - p(t+k), exceeds the value it loses, V_i·(phi_i(t - tau_i) - phi_i(t + k - tau_i)); tight binding makes the loss large for even small k, so tightly bound work pays at essentially any price.

## 6. The allocation problem and its dual

Let C(t) be capacity at quantum t. The protocol, or the market it hosts, chooses x_i(s, t) >= 0, the amount of project i's work arriving at s executed at quantum t:

```text
maximize    sum_i sum_s sum_{t >= s}  v_i(s, t) * x_i(s, t)              (TET)

subject to  sum_i sum_s x_i(s, t)   <=  C(t)        for all t            (capacity)
            sum_{t >= s} x_i(s, t)  <=  A_i(s)      for all i, s         (conservation)
            x_i(s, t) = 0                           for t < s            (causality)
            + neutrality, reducibility, incentive compatibility          (sec. 8)
```

The objective is **temporal economic throughput** (TET), defined in RN-08 and adopted in RN-10 sec. 12: value-weighted execution, the weight already encoding deadline success and delay cost through phi. It is one choice among several -- builder revenue, welfare, fairness, MEV resistance are others, and they conflict; TLM's move is to make the objective explicit and push part of it into protocol-verifiable constraints (sec. 8) rather than leave it to builder discretion. As written with x continuous this is a linear (transportation-type) program, the divisible generalization of the sec. 4 knapsack; real transactions are atomic, making it an integer program where the shadow-price reading below holds only approximately.

A word on causality, and on why a slot and a quantum behave differently here. A block is built once per slot, at the build deadline, when the builder already holds every transaction that arrived during the slot. Causality therefore bites at the **slot** level: work committed in slot N cannot appear in a block for an earlier slot, which is what x_i(s, t) = 0 for t < s enforces when s and t index slots. **Within** a slot it need not. Because the builder builds once with the whole slot in hand, the intra-slot quanta are positions it assigns, not arrival times it must respect -- it can place work that arrived late in the slot at an early quantum. That intra-slot freedom is not a causality gap but the builder's ordering power itself, and there is no consensus-established order finer than the slot for it to violate (the concurrent antichain of RN-12 sec. 6). So intra-slot placement is governed by the mechanism -- a FIFO baseline on commitment order, priced advancement, or leaving intra-quantum order concurrent and unsold (RN-12) -- not by causality; and s should be read at whatever resolution consensus actually records the commitment, since finer than that the protocol is assigning order, not enforcing it.

**The dual.** Attach a multiplier p(t) >= 0 to each capacity constraint. At an optimum, complementary slackness gives p(t) > 0 only where capacity binds, and a unit of work arriving at s executes at the quantum t maximizing v_i(s, t) - p(t). Read v_i(s, t) - p(t) as a **surplus** -- the value of executing the unit at t minus the price of the capacity it uses there -- so each unit goes to its highest-surplus quantum and executes only if that surplus is non-negative: a congested quantum (high p(t)) takes only work whose value there beats the price, while flexible work drifts to the cheap ones. (Two faces of one problem: finding the prices p(t) is a minimization -- the dual, pricing capacity as low as possible while still covering every unit's value -- while placing the work given those prices is the maximization here; strong duality makes them one optimum.)

> **The shadow prices {p(t)} on per-quantum capacity are the marginal value of execution capacity at each quantum** -- what a unit of capacity at t is worth to a planner maximizing TET, given demand (A, tau, V, phi) and capacity C.

These are a *welfare benchmark*, not a market price. **This note does not identify {p(t)} with the block-fee-rate term structure of Part I.** The term structure is a market construction -- a no-arbitrage curve bootstrapped from traded instruments (sec. 3); the shadow prices say what capacity *is worth* if allocated to maximize throughput. Whether a decentralized fee market's curve reproduces these shadow prices is an open question (secs. 10-11), not an identity asserted here.

What the shadow prices do give is a reading of RN-10's claims as consequences of one allocation. Deployed-versus-undeployed capacity (RN-10 sec. 4) is binding-versus-slack: p(t) = 0 where capacity is not scarce. A term rate below spot for committed demand (RN-10 sec. 6.2) is wide-phi work served wherever p(t) is low, averaging over cheap quanta. The event-driven segment (RN-10 sec. 7.1) is correlated targets with small W: one event sets tau for many projects, capacity binds, p(t) spikes. The two camps (RN-10 sec. 7) are the sign of W_i(alpha) - kappa. And **fee-as-filter** (RN-10 sec. 5) is the sharpest consequence: a scalar spot fee observes one number instead of phi, so it cannot separate projects differing only in phi, and it serves narrow-phi high-V demand while excluding demand whose value lies in flexibility, predictability, or continuity -- not an accident, but what happens when a message space is too small to express the objective's arguments. Because neutrality, reducibility, and incentive compatibility (sec. 8) are mechanism-level, the prices an implementable mechanism supports depart from the first-best {p(t)}; that departure is the price of implementability, and closing it is part of the agenda (sec. 11).

## 7. Temporal liquidity: a two-sided, conserved commodity

RN-10 sec. 8 calls temporal liquidity a two-sided market; the supply side has stayed implicit, and this section names it.

There are three roles, and today's builder holds all of them. Under proposer-builder separation a builder assembles the block, buys the proposal opportunity, resells execution access, deals on private order flow, and optimizes MEV -- a vertically integrated dealer with an information advantage, not a neutral operator. The two-sided reading separates the roles: the **protocol** issues execution rights and sets the feasible region; an **exchange** matches buyers and sellers of timing at a public price; the **builder** only constructs a schedule compliant with the cleared assignment, optimizing inside the protocol-defined set rather than choosing the order and keeping the surplus.

On the supply side, the instrument that makes Part I's term structure tradable is a transferable claim on future execution -- the zero and coupon of sec. 2 given an owner and a secondary market: R = (t1, t2, C, Gamma), a window, a capacity entitlement, and service conditions, which the holder may consume, transfer, subdivide, resell before expiry, or hold as collateral. A secondary market sharpens price discovery on the curve, but transferability is not automatically fair: execution rights concentrate among holders with the highest MEV-extraction ability and lowest capital cost, so a capital-advantaged non-builder can dominate [21], though a secondary market can also cut concentration by letting specialists buy just-in-time [22]. A perpetual *share* of capacity is the sharpest form of the risk -- permanent rent extraction, a barrier to entry -- so the safer instrument is a renewable long-duration lease the protocol can reprice, not an irrevocable perpetual right.

The two sides trade one conserved quantity. Patient work supplies **deferral liquidity** by accepting a later quantum; urgent work demands **advancement liquidity** by moving earlier; advancement exists only because deferral, or released reserve, creates it, so temporal liquidity is conserved except where the protocol releases reserve. This is what makes it an exchange rather than a fee market: the urgent party's payment does not vanish into the builder, it compensates the flexible party that gave up its position. The two camps of sec. 5 are the two sides of this book -- and, on the risk axis, the two sides of the fee swap (sec. 2.4). Turning this into a running market -- how bids and asks clear, the causality rule that keeps advancement from preceding commitment, the uniform crossing price, the market-maker options -- is a mechanism, developed as a candidate in **RN-12**.

## 8. The constraints the mechanism must meet

Three constraints separate this from a scheduling problem; each is a research question, and each rests on results the note takes from elsewhere.

**Fairness.** "Fair" has several inequivalent, partly incompatible meanings -- identity neutrality, receive-order fairness, no-starvation, minimum-service floors, time fairness [15] -- and they cannot all hold: strong receive-order fairness is impossible (Condorcet cycles; only a gamma-batch weakening survives) [10] (App. D). So fairness cannot be assumed as a primitive; the note takes *neutrality* -- the allocation depends on declared characteristics, not identity -- as the constraint on the map, adds no-starvation and minimum-service as liveness and floor constraints, and applies order-fairness only at quantum granularity (sec. 4 leaves intra-quantum order unsold). The new framing is the role separation it forces: the builder is the residual claimant on ordering value, so it cannot be the party that sets or enforces fairness. The protocol defines the feasible region, the builder optimizes inside it, and validators verify **compliance, not optimality** -- a checkable lower-bound service standard (floors, neutrality, reservations), with the residual optimization left to the builder and made auditable by reducibility (RN-07).

**Information.** The allocator may use only what is public: its policy must be adapted to a filtration {F_t}, F_t-measurable and non-anticipating. This gives a clean reading of MEV as a *measurability* violation -- the builder allocates on its private filtration G_t (finer than F_t) and captures the difference, which is the informed-trader edge of the Kyle model [11]. Coarsening the decision's filtration to the public one is what commit-reveal, threshold encryption, and timed commitments do (App. F); identity-blindness is only partial, since type leaks through contract address, gas, and timing, so the achievable goal is economic indistinguishability with respect to protocol treatment, not anonymity.

**Incentive compatibility.** phi is declared, so the mechanism must make truthful declaration optimal, under the impossibilities that bound transaction-fee mechanisms [2] (App. E). The width statistic W(alpha) narrows the task: a mechanism need not elicit all of phi, only enough of its width to place work on one side of kappa; understating width is self-penalizing, overstating is what must be defended against.

## 9. Solving it, and why simulation

The exact program is a mixed-integer, then stochastic, then -- dynamically -- a Markov decision process, for which the standard operational method is receding-horizon (model-predictive) control; recent work casts Ethereum's dynamic scheduling and pricing exactly as such an MDP [20] (App. C). Framed statically it is the multi-period optimal-execution problem of quantitative trading [12] (App. C), with one difference worth stating: the "impact" here is a protocol-set capacity price, the horizon is endogenous, and the schedule must additionally satisfy the neutrality, reducibility, and information constraints (sec. 8) a single trader never carries -- which is where the fee-market version stops being a relabeled known problem.

The dynamic view matters because allocations are held forward and revised, not assigned once. A multi-slot stream reserves a schedule of quanta across future slots (a lease, or forward tickets, RN-12), and those held positions are themselves the traded objects: taking or selling temporal liquidity reassigns an *already-allocated* quantum -- the stream sells a held quantum, moving it later within its window, or buys an earlier one -- so the standing x(s, t) is a forward schedule under continuous revision as trades clear and new demand arrives. A held quantum may be reassigned several times before its slot is built; what the slot realizes is the schedule after all trades, and it is these forward positions that the term structure (Part I) prices.

Because an exact solve is out of reach -- combinatorial, stochastic, mechanism-constrained, high-dimensional, and with a possibly non-unique benchmark -- the objects the analysis defines are estimated by simulation: small exact instances for ground truth (App. A), an LP relaxation whose duals are the capacity benchmark (sec. 6), heuristics, agent-based markets, Monte-Carlo scenarios, and learned policies (kept out of the protocol unless auditable). Run this way, the market prints instrument prices to bootstrap the Part I curve, and the same realized demand yields the benchmark, so the two can be compared (sec. 10). The metric RN-10 cares about most is project survival and diversity: whether the design lets more kinds of viable project exist.

## 10. The benchmark and the market curve: two objects

Part I and Part II give two curves, and it matters that they are two, not one.

The shadow prices {p(t)} (sec. 6) are the **capacity benchmark** -- a welfare object, what a unit of capacity at t is worth to a planner maximizing temporal throughput on the realized demand. The bootstrapped f(0,t) (sec. 3) is the **market term structure** -- a price object, the no-arbitrage fee curve the two-sided market actually prints. They come from different constructions: one is the dual of an allocation, the other a no-arbitrage fit to traded instrument prices. **This note does not claim they coincide.**

Whether they coincide -- under what completeness, liquidity, and incentive conditions a decentralized fee market's no-arbitrage curve reproduces the efficient shadow prices -- is the open question this framing makes precise (sec. 11). If they diverge, the divergence is informative: it would measure illiquidity, market power, extraction, and incentive loss, and RN-10's economics is the account of why it arises. But that is a hypothesis to test against the benchmark, not an identity to assert. Part I supplies the market observation; Part II supplies the benchmark; measuring the two on the same realized demand (sec. 9) is how the gap is estimated.

## 11. The research programme this opens

Writing the problem down makes its open parts precise.

On the market curve (Part I): the **minimal spanning set** -- which instruments must trade for the curve to be identified; the **future-slot auction** as a neutral, extraction-resistant price source; **transferability and concentration** -- should tickets be resellable, and what does a secondary market do to neutrality and to the front of the curve (secs. 2.3, 7); **swap and swaption settlement on-chain** -- notional and mark-to-market conventions, and what it means to hold an option on a future fee swap (RN-12); and **liquidity** -- which maturities can realistically be liquid, since the bootstrap assumes tradeable prices.

On the allocation (Part II): **existence and uniqueness of the dual** (degeneracy admits a non-unique benchmark; the stochastic and continuum limits are open); **incentive compatibility** of phi-declaration under the transaction-fee-mechanism impossibilities [2] (App. E), narrowed by W(alpha); **fairness made specific** (sec. 8) -- which achievable property the protocol commits to, and the welfare cost of enforcing it; the **information constraint** (sec. 8) -- what public filtration is enforceable given encryption's latency and metadata leakage; **reducibility** (RN-07) -- which near-optimal allocations compile to per-slot local parameters; and **tractability and simulation design** (sec. 9).

Bridging the two: **benchmark versus market** (sec. 10) -- under what conditions the market's no-arbitrage curve reproduces the capacity benchmark, and whether the two can be made mutually consistent. This is the question the note deliberately leaves open rather than settle by assertion.

The claim is that the disparate parts of RN-10 -- projects, capacity across time, fee-as-filter, the term structure, the two camps, and the reserve -- are facets of one problem: an allocation whose dual values capacity over time, and a market that prices the same capacity along time. That formulation is the contribution; the questions above are the work it makes possible, tracked with the rest of the agenda in **RN-10 Follow-up Research Questions**.

---

## Appendices -- prior art, credited

Each appendix states a borrowed result and its source; the body uses the result and points here. The appendices are not re-derivations.

### Appendix A -- Block-building as a knapsack

Single-slot block construction is a 0/1 knapsack: maximize included fee subject to a gas limit. The problem is NP-hard, but greedy value-density selection (sort by fee per unit gas) is near-optimal when items are small relative to capacity, and it is what priority-fee ordering already implements. Real blocks add precedence, conflicts, all-or-nothing bundles, and order-dependent (MEV) value, making the operative problem precedence-constrained and sequence-dependent. For the multi-period version with deadlines and cumulative capacities, fully-polynomial approximation schemes exist. Sources: Mohan & Khezr [13]; Gao, Birge & Gupta [19].

### Appendix B -- Term-structure bootstrapping and no-arbitrage

In fixed income a forward/zero curve is constructed from traded instrument prices under no-arbitrage: the spot fixes the front, zero-coupon prices fix intermediate maturities, par swap rates pin the long end (the bill-then-swap bootstrap), interpolation completes untraded maturities, and swaption prices calibrate the volatility. No-arbitrage is equivalent to a positive linear pricing functional (the fundamental theorem of asset pricing); forward-rate dynamics follow a Heath-Jarrow-Morton model. Sources: Hull [1]; Harrison-Kreps and Harrison-Pliska [4]; Heath-Jarrow-Morton [3]. Equilibrium term-structure models (Vasicek; Cox-Ingersoll-Ross [5]) are a related, distinct construction.

### Appendix C -- Optimal execution and the scheduling MDP

Multi-period optimal execution schedules a parent order over a horizon to trade off execution cost against the risk or decay of delay; the stochastic version is a dynamic program with an HJB equation. Dynamically, transaction scheduling and pricing over a mempool is a Markov decision process with long-run discounted reward; receding-horizon (model-predictive) control is the standard operational method under uncertainty. Sources: Almgren-Chriss and Bertsimas-Lo [12]; the mempool MDP [20].

### Appendix D -- Fair ordering: impossibility and the revenue tradeoff

Strong receive-order fairness is unattainable: batch-order-fairness admits Condorcet-style cycles, so only a weakened gamma-batch version with unavoidable batching is achievable (Aequitas). Enforcing fair-ordering constraints has a measured revenue cost, large under congestion. Sources: Kelkar, Zhang, Goldfeder & Juels [10]; Pugatsov, Ileri & Decouchant [14].

### Appendix E -- Transaction-fee-mechanism impossibility

Truthful transaction-fee mechanisms face impossibility results bounding what can be simultaneously incentive-compatible for users, for the builder, and against collusion; these bound how much of phi a fee mechanism can elicit. Source: Roughgarden [2].

### Appendix F -- Cryptographic information hiding

Commit-reveal, threshold encryption, and timed commitments let a protocol fix a commitment or eligibility before revealing transaction contents, coarsening the ordering party's information toward the public set; threshold encryption can also seed verifiable randomness that limits ordering manipulation (Helix). Pre-trade privacy of this kind is conditional: private transaction pools reduce front-running only when the risk is high and otherwise shift rents. Sources: Helix [16]; Timed Commitments Revisited [17]; Capponi, Jia & Wang [18].

---

## References

[1] Demsetz, H. "The Cost of Transacting." *Quarterly Journal of Economics* 82(1), 1968, 33-53. Grossman, S. J. & Miller, M. H. "Liquidity and Market Structure." *Journal of Finance* 43(3), 1988, 617-633. Foucault, T., Kadan, O. & Kandel, E. "Limit Order Book as a Market for Liquidity." *Review of Financial Studies* 18(4), 2005, 1171-1217. (Liquidity as immediacy; sorting by patience. RN-10 sec. 8.1 and sec. 8.8.) Hull, J. C. *Options, Futures, and Other Derivatives* (bootstrapping the zero curve; swaps, swaptions, and the par-swap-rate construction -- App. B).

[2] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM*, 2024. (The impossibility results that bound sec. 11 -- App. E.)

[3] Heath, D., Jarrow, R. & Morton, A. "Bond Pricing and the Term Structure of Interest Rates." *Econometrica* 60(1), 1992, 77-105. (Forward-rate dynamics; secs. 3, 9 -- App. B, C.)

[4] Harrison, J. M. & Kreps, D. "Martingales and Arbitrage in Multiperiod Securities Markets." *Journal of Economic Theory* 20, 1979; Harrison, J. M. & Pliska, S. R. (1981). (No-arbitrage iff a positive linear pricing functional exists; the foundation of the bootstrap in sec. 3 -- App. B.)

[5] Vasicek, O. "An Equilibrium Characterization of the Term Structure." *Journal of Financial Economics* 5(2), 1977; Cox, J., Ingersoll, J. & Ross, S. "A Theory of the Term Structure of Interest Rates." *Econometrica* 53(2), 1985. (Equilibrium / stochastic-discount-factor term-structure models -- App. B.)

[6] Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014, 2023. (Pricing one temporal dimension -- urgency -- which sec. 6's fee-as-filter generalizes.)

[7] Future-slot claims on execution: Neuder, M. & Drake, J. *Execution Tickets.* Ethereum Research (ethresear.ch), 2024 -- an auctioned right to construct the execution payload for a future slot. Drake, J. *Based Preconfirmations.* Ethereum Research (ethresear.ch), 2024 -- a credible commitment to include a transaction at a coming slot. Research-stage proposals, not finalized EIPs.

[8] Arbitrum Timeboost (auctioned express-lane ordering right). Offchain Labs documentation.

[9] TLM Research Notes: RN-10 (the economics), RN-08 (temporal economic throughput), RN-05 (the quantum lattice), RN-01/02 (demand representation and verification), RN-07 (the reducibility invariant), and RN-10 Follow-up Research Questions.

[10] Kelkar, M., Zhang, F., Goldfeder, S. & Juels, A. "Order-Fairness for Byzantine Consensus" (Aequitas). *CRYPTO* 2020. (Impossibility of strong batch-order-fairness and the gamma-batch weakening -- App. D.)

[11] Kyle, A. S. "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1985, 1315-1335. (The informed trader's edge as the gap between a private and a public information set; sec. 8.)

[12] Almgren, R. & Chriss, N. "Optimal Execution of Portfolio Transactions." *Journal of Risk* 3(2), 2001, 5-39. Bertsimas, D. & Lo, A. "Optimal Control of Execution Costs." *Journal of Financial Markets* 1(1), 1998, 1-50. (Multi-period optimal execution -- App. C.)

[13] Mohan, V. & Khezr, P. "Blockchains, MEV and the Knapsack Problem: A Primer." arXiv:2403.19077, 2024. (Block building as a knapsack -- App. A.)

[14] Pugatsov, A., Ileri, C. U. & Decouchant, J. "The Blockchain Execution Dilemma: Optimizing Revenue XOR Fair Ordering." arXiv:2604.23266, 2026. (The revenue-versus-fair-ordering trade-off -- secs. 4, 6; App. D.)

[15] Lechowicz, A., Sengupta, R., Sun, B., Kamali, S. & Hajiesmaili, M. "Time Fairness in Online Knapsack Problems." *ICLR* 2024; arXiv:2305.13293. (Time fairness and its trade-off with competitiveness; sec. 8.)

[16] Asayag, A., et al. "Helix: A Scalable and Fair Consensus Algorithm Resistant to Ordering Manipulation." IACR ePrint 2018/863. (Threshold encryption to hide contents and seed verifiable randomness -- App. F.)

[17] "Timed Commitments Revisited." IACR ePrint 2023/977. (Forced revelation after a set time -- App. F.)

[18] Capponi, A., Jia, R. & Wang, Y. "Do Private Transaction Pools Mitigate Frontrunning Risk?" IACR ePrint 2023/1461. (Private pools reduce front-running only conditionally -- App. F.)

[19] Gao, Z., Birge, J. R. & Gupta, V. "Approximation Schemes for Multiperiod Binary Knapsack Problems." arXiv:2104.00034, 2021. (FPTAS for multiperiod binary knapsack -- App. A.)

[20] "Dynamic Transaction Scheduling and Pricing in the Ethereum Mempool." arXiv:2605.12794, 2026. (Dynamic scheduling/pricing as an MDP over mempool state -- App. C.)

[21] "MEV Capture and Decentralization in Execution Tickets." arXiv:2408.11255, 2024. (Transferable execution rights concentrate under MEV-extraction ability and low capital cost; sec. 7.)

[22] "Galaxy Era: Agent-based Simulation of Execution Tickets." arXiv:2501.16090, 2025. (A secondary market can reduce concentration via just-in-time purchase; sec. 7.)

---

*Changes from v0.2.* The note is reorganized and extended, and the mechanism is split out. **Part I** sets out the market term structure as the continuation of RN-10: the bond-to-fee mapping, the instrument space -- now including the two-sided fee swap (the fixed-rate payer buys cost certainty, the floating-rate payer supplies it, so the two camps meet as counterparties, sec. 2.4) and the swaption (sec. 2.5) -- and the no-arbitrage bootstrap. **Part II** is the new contribution: the execution-capital demand function with decay measured against a target (sec. 5), the two-camps partition by binding tightness, and the allocation and its dual (sec. 6); the borrowed machinery -- knapsack, optimal execution, order-fairness impossibility, cryptographic hiding -- is credited to short appendices (A-F) rather than re-derived. The central correction from v0.2: the allocation dual is a welfare benchmark on the value of capacity and is **not** identified with the market term structure -- whether the two coincide is left open (secs. 10-11). The concrete clearing mechanism, formerly folded in, is now the separate note **RN-12**.
