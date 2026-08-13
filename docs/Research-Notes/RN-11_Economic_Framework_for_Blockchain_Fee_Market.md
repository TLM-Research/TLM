---
id: RN-11
title: "An Economic Framework for a Blockchain Fee Market with Temporal Liquidity"
subtitle: "The block-fee-rate term structure and the execution-capital allocation problem"
version: v0.4 (reframes Part I around the coin-denominated term structure: a positioning section anticipating the commodity view, a numeraire/own-rate section defining the discount factor B, a section reading the fee as an abstraction over base-fee/tips/MEV, and the curve construction with temporal liquidity as the storability dial. Part II carries surgical fixes only -- the full primal-dual with both multiplier families (sec. 6), flow rather than scalar conservation (sec. 7), softened width/kappa claims and tau's epistemic status (sec. 5) -- and the reference list is normalized.)
status: "Public draft. The formal center of the TLM program; stated, not solved."
program: "Temporal Liquidity Market (TLM)"
date: August 12, 2026
---

# RN-11 -- An Economic Framework for a Blockchain Fee Market with Temporal Liquidity

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

## Positioning: blockspace between commodity and money

A natural first reaction treats blockspace as a perishable commodity. Each slot's capacity is used-or-lost, like electricity from a generator or an idle CPU cycle, so the intuition runs that its forward market must be a commodity-forward -- prices set by expected future scarcity, with no bond-like term structure and no link between spot and forward beyond expectation. If that were the whole story, the fixed-income reading of Part I would be a category error.

It is not the whole story, and the commodity reading is the wrong default, for two reasons. First, the object priced is the fee, denominated in the chain's own coin, and the coin is a storable, reinvestable numeraire with its own rate of return (sec. 0.5). Second, a non-storable service can still be linked across time by substitution on the demand side: work that tolerates the drift between wall-clock relevance and block execution can move across slots, and that movement is an intertemporal arbitrage a pure commodity lacks. Temporal liquidity is the name for that substitution, and providing it frictionlessly is the mechanism's purpose.

So blockspace sits between two limits. With no substitution mechanism it is a commodity -- a free-floating forward curve. In the limit of abundant, frictionless substitution it is money -- a fully arbitrage-linked term structure, money being the perfectly shiftable good whose curve is bond-like for that reason. Real blockspace lies between, and where it lies is not a fixed fact but an outcome of market design. **The purpose of the temporal liquidity market is to move it toward the money limit.**

This is the economic foundation the note builds, and it has two levels, as economics does. At the **macro** level -- the multi-slot economy -- the objects are the block-fee term structure, aggregate execution-capital demand read at the level of projects, the capital value of the network and its own-rate, and temporal liquidity as the intertemporal link (Part I). At the **micro** level -- the per-quantum market -- the objects are congestion prices, the two-sided clearing of temporal position, incentives, and microstructure (Part II). Part I is the macro term structure; Part II is the micro allocation whose dual values capacity; the mechanism connecting them is RN-12, and the capacity limits within which both operate are RN-13. Read this way, the note is the price-and-allocation foundation of a blockchain economy, and the reframed Part I below is its macro half.

## 0.5 Numeraire, own-rate, and the discount factor B

Everything is denominated in the native coin -- ETH on Ethereum, APT on Aptos. Fees, MEV, issuance, and staking rewards are all in-coin; a dollar view is derived, through the coin/USD forward, and carries exchange-rate risk. The term structure of Part I is therefore a term structure in the coin, and its discount factor is the coin's own discount factor, not a dollar rate.

Two quantities must be separated, because the fixed-income analogy tends to collapse them. The **rental rate** is the fee per unit of deployed capacity per period -- the block-fee-rate, the price of the service. The **discount rate** B is the price of the coin across time -- what compounds. The fee is the rental rate; B is a separate object, and compounding lives in B, not in the fee.

At the theoretic, mechanism-independent level B is the coin's **own-rate**: the yield the aggregate fee stream throws off on the capital that produces it. In steady state, with aggregate real fee income R on a capital value P and growth g,

```text
B  =  R / P  +  g ,
```

so B is a fixed point -- endogenous to the very fee stream it discounts. This is the formal content of "blockspace is capital and the fee is its yield." B is the aggregate rental *yield* (fee income relative to capital value), a rate, not the per-unit fee.

B is not the staking yield, and the difference matters. Observed staking yield mixes three things: the real fee-and-MEV income (B's numerator), protocol issuance (a monetary transfer among holders, not real income), and the specifics of the staking mechanism. Strip issuance and the mechanism and the remaining fee-derived yield is the theoretic B; staking yield is its observable, issuance-inflated proxy, and carries slashing and liquid-staking risk besides. For the theoretic term structure this note analyzes -- the fee the protocol pays out for blockspace -- B is the fee-yield, and staking is one institutional way it is realized, still in the native coin.

Two consequences. First, over a single slot B is approximately 1: a few-percent annual rate over twelve seconds is negligible, so intra-slot the discount is inert and the rental/congestion price is the whole story -- the own-rate matters only across the multi-slot horizon this part prices. Second, the principal-bearing instrument is the claim on the aggregate fee stream: staked coin, plus the deflation the base-fee burn confers on all holders, is the equity-like claim on the network's blockspace income, and its capital value P is where "principal" lives (sec. 2.3). The real income has two channels worth keeping straight -- base-fee burn accrues to all holders as scarcity, tips and MEV accrue to stakers -- and B's numerator is their sum.

The own-rate of a good measured in units of itself is Keynes's own-rate of interest [23]; the non-storability treatment (sec. 3, App. B) draws on the theory of storage and convenience yield [24] and on forward-curve models for non-storable commodities [25].

## 0.6 What "the fee" means: an abstraction over base fee, tips, and MEV

The "fee" this note prices is not the current Ethereum fee. Today the price of execution is fragmented and partly hidden: a base fee that is burned and prices congestion, a priority tip that goes to the proposer and prices inclusion within a block, and MEV captured off-protocol by builders and searchers that prices ordering and extraction -- plus payments through private order flow that never surface as a fee. A term structure needs a single, protocol-visible price of execution across time; today's composite is not that.

So the fee here is an abstraction, and the note is written for a future protocol in which that price is made clean and visible. Each of today's fragments must be re-examined and enhanced under the temporal-liquidity design, and each maps to a piece of the object:

- the **base fee** generalizes to the per-quantum congestion price -- the near end of the curve, priced across quanta rather than as one block-level number;
- the **priority tip** is replaced: the private tip-to-builder for intra-block position becomes the cleared advancement payment that flows to the flexible supplier who yields position, not to the builder (RN-12);
- **MEV** is split: inter-quantum ordering value is surfaced as a public, cleared temporal price -- part of the fee curve -- while intra-quantum extraction is suppressed or randomized (RN-12).

Cleaning the fee into one price is not a side matter; it is a precondition for a well-behaved curve, and it is part of the same friction-reduction as demand-side substitution (positioning, sec. 0.5). A fragmented, partly-hidden price is a commodity-market friction; a unified, protocol-visible price is one of the things that moves the curve toward the money limit. The instruments of Part I are defined on this cleaned fee, and where they say "fee rate" they mean this unified temporal price, not the current base-fee-plus-tip.

---

# Part I -- The block-fee-rate term structure

Part I is the macro half of the foundation: the fee curve along time, in the native coin, read as a term structure. The construction is standard fixed income (App. B); what is new is the mapping to a fee market, the observation that today only the front is priced, and the reading of the curve as a bond-like object whose link across maturities is enforced by demand-side substitution rather than storage. The bond mathematics is the backbone; non-storability enters as one bounded caveat (sec. 3), not as a reason to abandon the reading.

## 1. The block-fee-rate is a rental rate

The block-fee-rate at quantum t is the **rental rate on execution capital**: the fee earned for one period of deployed capacity. The capital is the network itself -- a durable, productive asset that throws off execution capacity each slot the way a machine throws off output, and that persists because time is endogenous (the protocol produces the next slot). A slot's capacity is one period's service flow of that capital: used-or-lost within the slot, but the network that produces it endures. Capacity deployed earns the rental; capacity idle earns nothing, as an unrented machine earns nothing -- the deployed-versus-undeployed distinction of RN-10 sec. 4, and the p(t) = 0-on-slack condition of the allocation dual (sec. 6), seen from the supply side.

Two rates, kept apart (sec. 0.5). The **rental rate** is the fee -- the price of the service each period. The **discount rate** B is the coin's own-rate -- what compounds. The bond analogy transfers to the discounting (B is a genuine interest rate on the storable coin) but not to the rental: the service is not stored and rolled, so the fee does not compound. **Principal is present** all the same -- the capital value of the network's fee stream, the present value at B of the rentals it will earn, and the object a transferable claim on capacity (sec. 2.3) carries. Calling the object execution *capital* is accurate; the fee is its rental, B its discount, and the network is what holds the principal.

The mapping is worth setting out, because the empty rows are the finding.

| Rates market | Fee-market counterpart | In today's fee market |
|---|---|---|
| Overnight / spot rate | Spot inclusion: the cleaned unit fee now (sec. 0.6) | Exists (as base fee + tip) |
| Zero / one-date claim | Future-slot fee: delivery of execution at one quantum t | Missing; early forms in preconfirmations and execution tickets [7] |
| Yield curve / term structure | Block-fee-rate curve across future quanta | Missing -- only the front is priced |
| Forward rate | Forward block-fee-rate f(0,t) | Missing |
| Coupon claim + principal | Durable capacity claim: periodic rental + capital value | Missing; nascent in validator rights, reserved leases |
| Fixed-for-floating swap | Fee swap over N quanta, cash-settled in coin | Missing |
| Swaption | Option to enter a fee swap | Missing |
| Money discount factor | B(0,t): the coin's own-rate discount (sec. 0.5) | Implicit (staking as its proxy) |
| Idle cash earns 0 | Undeployed capacity earns 0 | Inherent (durable capital) |

One row needs care, and it is the reviewer's fair point turned into a definition. A future-slot claim (row 2) is the **forward delivery price of a dated service**, F_g(0,t) -- what you pay today for execution at t -- not a zero-coupon *bond*, which would pay one unit of the coin at t. The two coincide only if the service is conflated with the numeraire. Keep three objects distinct: the money discount B(0,t) (sec. 0.5), the spot service price S_g(t), and the forward service price F_g(0,t). The bootstrap (sec. 3) uses B to discount coin cash flows and the traded forwards to fix the service curve; it does not derive F_g from B, and it does not treat a delivery price as a discount factor.

The mapping's contribution is unchanged: today's fee market has a front and no curve, and the empty rows are the design agenda -- the future-slot ticket first (it anchors the curve), then the swap (the long end and hedging), then the swaption (convexity), each with a mature analog whose economics and failure modes are known (App. B).

## 2. The instrument space

The curve is bootstrapped from traded instruments, all defined on the cleaned fee (sec. 0.6).

### 2.1 Spot service price S_g(t)

The price of execution now -- the cleaned unit fee for immediate inclusion. It is the front of the curve and the one point observable today.

### 2.2 The future-slot fee -- the forward delivery price

A claim bought at 0 that delivers one unit of execution at a single future quantum t. Its price is F_g(0,t), the **forward service price** to t -- not a zero-coupon bond price (sec. 1). The curve t -> F_g(0,t) is the term structure in its purest form, and the primitive that makes it trade is a future-slot auction or transaction ticket (in the family of execution tickets and preconfirmations [7]). This is the primary instrument to specify, most likely as an EIP, because the forward curve is what everything else bootstraps against.

### 2.3 The durable capacity claim -- where principal lives

A transferable, ownership-bearing claim on execution capacity: each period the capacity it entitles is deployed and earns the rental, and the claim carries a capital value equal to the present value at B of those rentals (sec. 1). This is the principal-bearing instrument -- a validator's block-production right, a long-lived reserved-capacity lease, staked coin as the aggregate case (sec. 0.5). A complete definition must state who owes performance, the exercise rule, and the priority against ordinary demand; these are required and open (sec. 8). For constructing the curve it is redundant -- its price is implied by the forwards and the swap -- so the bootstrap needs only those.

### 2.4 The fee swap -- cash-settled, two-sided, and the basis it carries

Over N quanta, a fixed-for-floating swap on a capacity notional Q exchanges a fixed per-quantum rate F for the realized floating rate p(t): only the difference (p(t) - F)*Q is settled each quantum, in coin, marked to market; no notional is delivered. The **fixed-rate payer** buys cost certainty (a rollup, oracle, or market maker hedging its execution cost); the **floating-rate payer** warehouses fee-rate risk for the fixed premium (a validator, searcher, or capacity provider). These are two sides of the second temporal axis: where the spot temporal-liquidity trade (sec. 7) moves *position* between a patient and an urgent party, the swap moves *rate risk* between a predictability-seeking and a risk-bearing party.

One qualification the reviewer's reading supplies, and it is worth keeping. The swap is a **cash-settled financial** claim on the fee index; the physical temporal-liquidity trade is a claim on an actual execution position. They are linked but not identical, and the wedge between them -- the **basis** between paying the fee index and securing execution -- is itself a temporal-liquidity risk premium, not a nuisance to assume away. A project that hedges its fee cost with a swap has not thereby secured its execution: it has hedged the price and kept the quantity risk. The two camps meet in the swap on the price axis and in the spot trade on the position axis, and the basis connects them.

The par fee-swap rate F*(N) is the fixed rate giving the swap zero value at inception,

```text
F*(N) = ( sum_{t=1..N} B(0,t) * f(0,t) )  /  ( sum_{t=1..N} B(0,t) )
```

with f(0,t) the forward block-fee-rate to t and B(0,t) the coin discount factor (sec. 0.5). Observing F*(N) across horizons pins the long end, as swap rates do in the fixed-income swap curve [1] (App. B).

### 2.5 The swaption -- the option to enter a swap

The right, not the obligation, to enter a fee swap at a preset rate over a future window. It prices the volatility of the curve rather than its level: a project with contingent demand buys the right to lock its cost later instead of committing now. It is the convexity instrument, extending the framework to a volatility surface. Its realization as a protocol mechanism is left to RN-12.

## 3. Constructing the curve, and the storability dial

Given the instrument prices, the forward curve f(0,t) is built by the chaining fixed income uses -- and the chaining is definitional, holding for any dated good, storable or not. Writing Total(0,0,t) for the accumulation to t,

```text
Total(0, 0, T+1)  =  Total(0, 0, T)  *  Forward(0, T, T+1) ,
```

so the forward is the ratio the observed curve implies, and the bootstrap is: the spot fixes the front; each future-slot price F_g(0,t) fixes the delivery price at t; par fee-swap rates F*(N) pin the long end and fill illiquid maturities (the bill-then-swap bootstrap [1]); interpolation completes untraded quanta; swaption prices calibrate the volatility (App. B). B(0,t) discounts the coin legs throughout.

What differs from the bond market is not the chaining but what enforces the link between the curve and today's spot. For a storable asset, supply-side storage enforces it by arbitrage. Execution is not storable slot to slot, so that channel is absent -- the reviewer's point, correct as far as it goes. But a second channel is present that a pure commodity lacks: **demand-side substitution**. Work that tolerates drift moves across slots, and that movement bounds how far adjacent forwards can separate, by the switching cost of flexible demand. Temporal liquidity is that channel, and it makes the spot-forward link real though bounded.

So the strength of the link is a dial, not a fact:

```text
flexible demand -> 0      free-floating commodity curve (expected scarcity only)
flexible demand -> large  money-like curve (fully arbitrage-linked)
in between                bond-like in denomination and chaining, with bounded
                          expected-scarcity structure (event spikes, humps) that
                          flexible demand shaves but does not erase
```

Money is the frictionless limit of this dial, not a different kind of object; blockspace priced in its own coin, with a substitution mechanism, moves toward it. This is the sense in which the term structure is bond-like: the coin numeraire and the chaining give the backbone, and temporal liquidity supplies the enforcement that storage supplies for money. Non-storability is not a wall; it is the friction the mechanism (RN-12) exists to reduce, and the degree of bondness the curve reaches is a measurable outcome of how complete that market is.

Two honesties the construction must carry. The curve is identified only on the **marketed subspace** -- the maturities and classes that actually trade; untraded maturities are interpolated, a modeling choice, not a no-arbitrage consequence, as in a thin money market. And different quanta or service classes are not perfectly substitutable (state access, finality, priority differ), so the market is incomplete and the curve unique only up to that incompleteness. Closing the gap -- making enough instruments trade, and making flexible demand deep enough to link maturities -- is what the mechanism is for. The curve so built is what the two-sided market prints, made consistent by no-arbitrage on the marketed subspace; Part II asks what that curve prices, and whether the price is efficient.

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

**Arrival and target are separate.** Measuring decay from arrival would assume work becomes relevant when it becomes submittable, and that fails for the class RN-10 sec. 7 is built around: a mint opening at a published block, a scheduled expiry, a funding settlement can all be submitted long before they are relevant, so tau is known far in advance while the work stays immovable. Decay against tau holds *foreseeable* and *tightly bound* at once; a single-index form cannot. The argument of phi is the drift RN-10 sec. 7 names: **`t - tau` is `T_block - T_wall` on the lattice**, and phi is the tolerance for it. phi is defined on all integers, because for target-bound work executing *early* destroys value as surely as late -- an oracle update before its event is worthless; setting tau_i(s) = s recovers ordinary work relevant as soon as it exists. tau is a demand type, not a quantity the protocol observes: for scheduled work (a published mint, an expiry) it is protocol-verifiable, but for triggered work (a liquidation, an arbitrage) it is private and revealed only when the trigger fires, so the mechanism elicits behavior against tau rather than reading tau directly, and the equality `t - tau = T_block - T_wall` holds in the model, not as a value the allocator can measure.

**Decay shapes are not one family.** phi is declared per unit of work and takes many shapes, each a different demand: a step (a hard deadline), an exponential (a constant hazard of irrelevance), a linear ramp, a plateau-then-cliff; periodic or multi-window value (an oracle updating on a schedule, or work with several acceptable windows), where phi has several peaks and is not monotone, so a quantum farther from the main peak can be worth more than a nearer one; two-sided shapes for target-bound work; and event-driven (option-like) value that is near zero until a state omega occurs and then large and short-lived -- the liquidation case. The shape, not just a single deadline, is what the mechanism must cope with, and it is *declared* while A is largely *observed* (RN-02). **This is why a scalar fee cannot represent demand: it sees one number, and phi is a function.**

**For some projects value is not separable across transactions.** A continuous exchange, a rollup posting, or an oracle stream values the *shape of service over time*, not each transaction alone. Its value is V_s(x_s) over the whole schedule, and a workable form penalizes instability and jitter:

```text
V_s(x_s) = sum_t u_s( X_{s,t} )  -  lambda_s * Var_t( X_{s,t} )  -  mu_s * sum_t | X_{s,t} - X_{s,t-1} |
```

where X_{s,t} is the project's executed volume in slot t: per-period utility, less a variance penalty, less a jitter penalty. This is where TLM departs from an independent-transaction knapsack -- continuity and predictability are properties of the *joint* allocation -- so proportional fairness over totals does not by itself deliver smooth service.

A consequence for trading: because the value is joint, the cost of reassigning one held quantum of a stream is the *marginal* effect on V_s(x_s), not a local phi difference -- moving a single execution can raise the stream's variance or jitter even where that execution's own phi is flat. So the supply condition generalizes: a stream lends out a held quantum when the price paid exceeds the marginal loss in V_s(x_s), and supplies only the flexibility that keeps its whole schedule within tolerance. Its quanta cannot be reassigned one at a time in isolation.

The tuple **ECDF_i = (A_i, tau_i, V_i, phi_i)** recovers the umbrella dimensions (Vision; RN-01) as properties of phi, tau, and A: delay tolerance is how slowly phi decays; the deadline is the smallest d with phi_i(d) = 0; the decay rate is phi's shape; binding tightness is phi's width; duration and intensity are the support and magnitude of A; predictability is the forecastability of A and tau.

**Binding tightness, formally.** Fix a tolerance alpha in (0,1). The tolerance width W_i(alpha) = |{ d : phi_i(d) >= alpha }| counts the quanta over which the work keeps at least alpha of its value -- a single interval when phi_i is single-peaked, a union of intervals when it is not, but always the full set of quanta to which the work may be reassigned without dropping below alpha, so the statistic needs no monotonicity assumption. The two camps of RN-10 sec. 7 are a threshold on width: fixing kappa, work is tight-binding (a taker) when W_i(alpha) <= kappa and loose-binding (a supplier) when W_i(alpha) > kappa. Tightness is a property of phi, predictability a property of the joint law of (A_i, tau_i); the two axes are independent, which is why all four cells of RN-10 sec. 7.3 are non-empty, and the partition applies to executions, not participants -- one project may emit W = 1 liquidation work and W = 10^4 batch work. A caveat on the width statistic and on kappa. W(alpha) is a coarse, first-order summary of temporal flexibility -- the *duration* of demand, in the sense bond duration summarizes rate sensitivity -- and like duration it discards the location, asymmetry, and value scale of the admissible set, which the full phi carries. The partition by kappa is therefore a first-order cut, not a sufficient statistic: two jobs of equal width but disjoint or asymmetric windows are not interchangeable, and where the cut is close the mechanism should fall back to phi. A natural conjecture -- not established here -- sets kappa's scale to the autocorrelation length of the price p(t), so work is tight-binding when it cannot outlast a congestion episode, which would make the partition and the price a joint fixed point; whether that fixed point exists is open. Loosely bound work supplies liquidity at t when the price to move it, p(t) - p(t+k), exceeds the value it loses, V_i·(phi_i(t - tau_i) - phi_i(t + k - tau_i)); tight binding makes that loss large for even small k, so tightly bound work pays a premium up to the value at stake V_i -- large, but bounded by V_i, not unbounded.

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

**The dual.** The primal has two constraint families -- capacity at each quantum and work-supply at each arrival -- so the dual carries two multiplier families: a capacity price p(t) >= 0 on each capacity constraint, and an opportunity value u_i(s) >= 0 on each work-supply constraint. The dual is

```text
minimize    sum_t C(t) p(t)  +  sum_{i,s} A_i(s) u_i(s)
subject to  u_i(s) + p(t)  >=  v_i(s, t)      for all i, s and t >= s
            p(t) >= 0,   u_i(s) >= 0
```

so u_i(s) is the shadow value of another unit of project i's work at s -- its willingness to pay, the demand side -- and p(t) is the price of capacity at t, the scarcity side. Complementary slackness reads off the placement: p(t) > 0 only where capacity binds; a unit arriving at s executes at the quantum t maximizing the **surplus** v_i(s, t) - p(t), and only where that surplus is non-negative, and at the optimum u_i(s) equals that maximized surplus. A congested quantum (high p(t)) takes only work whose value there beats the price; flexible work drifts to the cheap quanta. Two faces of one problem -- pricing capacity and placing work -- made one optimum by strong duality. The prices need not be unique: under degeneracy the dual has a face of optima (a non-unique benchmark, sec. 11), and intertemporal or reserve constraints can give slack capacity a positive option value, so p(t) = 0 on slack holds for a chosen complementary solution, not unconditionally.

> **The shadow prices {p(t)} on per-quantum capacity are the marginal value of execution capacity at each quantum** -- what a unit of capacity at t is worth to a planner maximizing TET, given demand (A, tau, V, phi) and capacity C.

These are a *welfare benchmark*, not a market price. **This note does not identify {p(t)} with the block-fee-rate term structure of Part I.** The term structure is a market construction -- a no-arbitrage curve bootstrapped from traded instruments (sec. 3); the shadow prices say what capacity *is worth* if allocated to maximize throughput. Whether a decentralized fee market's curve reproduces these shadow prices is an open question (secs. 10-11), not an identity asserted here.

What the shadow prices do give is a reading of RN-10's claims as consequences of one allocation. Deployed-versus-undeployed capacity (RN-10 sec. 4) is binding-versus-slack: p(t) = 0 where capacity is not scarce. A term rate below spot for committed demand (RN-10 sec. 6.2) is wide-phi work served wherever p(t) is low, averaging over cheap quanta. The event-driven segment (RN-10 sec. 7.1) is correlated targets with small W: one event sets tau for many projects, capacity binds, p(t) spikes. The two camps (RN-10 sec. 7) are the sign of W_i(alpha) - kappa. And **fee-as-filter** (RN-10 sec. 5) is the sharpest consequence: a scalar spot fee observes one number instead of phi, so it cannot separate projects differing only in phi, and it serves narrow-phi high-V demand while excluding demand whose value lies in flexibility, predictability, or continuity -- not an accident, but what happens when a message space is too small to express the objective's arguments. Because neutrality, reducibility, and incentive compatibility (sec. 8) are mechanism-level, the prices an implementable mechanism supports depart from the first-best {p(t)}; that departure is the price of implementability, and closing it is part of the agenda (sec. 11).

## 7. Temporal liquidity: a two-sided, conserved commodity

RN-10 sec. 8 calls temporal liquidity a two-sided market; the supply side has stayed implicit, and this section names it.

There are three roles, and today's builder holds all of them. Under proposer-builder separation a builder assembles the block, buys the proposal opportunity, resells execution access, deals on private order flow, and optimizes MEV -- a vertically integrated dealer with an information advantage, not a neutral operator. The two-sided reading separates the roles: the **protocol** issues execution rights and sets the feasible region; an **exchange** matches buyers and sellers of timing at a public price; the **builder** only constructs a schedule compliant with the cleared assignment, optimizing inside the protocol-defined set rather than choosing the order and keeping the surplus.

On the supply side, the instrument that makes Part I's term structure tradable is a transferable claim on future execution -- the zero and coupon of sec. 2 given an owner and a secondary market: R = (t1, t2, C, Gamma), a window, a capacity entitlement, and service conditions, which the holder may consume, transfer, subdivide, resell before expiry, or hold as collateral. A secondary market sharpens price discovery on the curve, but transferability is not automatically fair: execution rights concentrate among holders with the highest MEV-extraction ability and lowest capital cost, so a capital-advantaged non-builder can dominate [21], though a secondary market can also cut concentration by letting specialists buy just-in-time [22]. A perpetual *share* of capacity is the sharpest form of the risk -- permanent rent extraction, a barrier to entry -- so the safer instrument is a renewable long-duration lease the protocol can reprice, not an irrevocable perpetual right.

The two sides trade one conserved quantity -- and the conservation is a **flow** identity, per quantum, not a single scalar stock. Patient work supplies **deferral liquidity** by accepting a later quantum; urgent work demands **advancement liquidity** by moving earlier; advancement at a quantum exists only because deferral into it, or released reserve, makes the room, so per-quantum capacity is conserved under any reassignment except where the protocol releases reserve. Feasible reallocations are therefore flows and cycles over the per-quantum capacity constraints, not movements of one scalar inventory; "commodity" names the traded flexibility loosely, and what is conserved is capacity at each quantum, a vector. This is what makes it an exchange rather than a fee market: the urgent party's payment does not vanish into the builder, it compensates the flexible party that gave up its position. The two camps of sec. 5 are the two sides of this book -- and, on the risk axis, the two sides of the fee swap (sec. 2.4). Turning this into a running market -- how bids and asks clear, the causality rule that keeps advancement from preceding commitment, the uniform crossing price, the market-maker options -- is a mechanism, developed as a candidate in **RN-12**.

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

### Appendix B -- Term-structure construction for a coin-denominated, demand-linked service

In fixed income a forward/zero curve is built from traded instrument prices under no-arbitrage: the spot fixes the front, zero prices fix intermediate maturities, par swap rates pin the long end (the bill-then-swap bootstrap), interpolation completes untraded maturities, swaption prices calibrate the volatility; no-arbitrage is equivalent to a positive linear pricing functional (the fundamental theorem of asset pricing), and forward-rate dynamics follow a Heath-Jarrow-Morton model. Two adaptations are needed here, both standard once named. First, discounting is in the native coin, so the discount factor is the coin's own-rate B (sec. 0.5), not a dollar rate; the money leg compounds at B, the service leg does not. Second, the underlying is a non-storable dated service, so the spot-forward link is enforced not by storage (cash-and-carry) but by demand-side substitution -- the convenience-yield and commodity-forward literature is the analog, with temporal liquidity playing the role storage plays for a storable commodity and limited-storage/demand-response plays in electricity markets. In the limit of abundant substitution the construction reduces to the ordinary bond bootstrap; with bounded substitution the curve retains expected-scarcity structure. Sources: Hull [1]; Harrison-Kreps and Harrison-Pliska [4]; Heath-Jarrow-Morton [3]; Keynes ch. 17 own-rates [23]; Kaldor and Working on the theory of storage and convenience yield [24]; Geman on forward curves for non-storable commodities [25]. Equilibrium term-structure models (Vasicek; Cox-Ingersoll-Ross [5]) are a related, distinct construction.

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

[23] Keynes, J. M. *The General Theory of Employment, Interest and Money.* Macmillan, 1936, ch. 17 ("The Essential Properties of Interest and Money"; own-rates of interest). (sec. 0.5, App. B.)

[24] Kaldor, N. "Speculation and Economic Stability." *Review of Economic Studies* 7(1), 1939, 1-27. Working, H. "The Theory of Price of Storage." *American Economic Review* 39(6), 1949, 1254-1262. (The theory of storage and convenience yield; sec. 3, App. B.)

[25] Geman, H. *Commodities and Commodity Derivatives: Modeling and Pricing for Agriculturals, Metals and Energy.* Wiley, 2005. (Forward-curve construction for non-storable commodities; sec. 3, App. B.)

---

*Changes from v0.2.* The note is reorganized and extended, and the mechanism is split out. **Part I** sets out the market term structure as the continuation of RN-10: the bond-to-fee mapping, the instrument space -- now including the two-sided fee swap (the fixed-rate payer buys cost certainty, the floating-rate payer supplies it, so the two camps meet as counterparties, sec. 2.4) and the swaption (sec. 2.5) -- and the no-arbitrage bootstrap. **Part II** is the new contribution: the execution-capital demand function with decay measured against a target (sec. 5), the two-camps partition by binding tightness, and the allocation and its dual (sec. 6); the borrowed machinery -- knapsack, optimal execution, order-fairness impossibility, cryptographic hiding -- is credited to short appendices (A-F) rather than re-derived. The central correction from v0.2: the allocation dual is a welfare benchmark on the value of capacity and is **not** identified with the market term structure -- whether the two coincide is left open (secs. 10-11). The concrete clearing mechanism, formerly folded in, is now the separate note **RN-12**.
