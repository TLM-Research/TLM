---
id: RN-10
title: "The Economics of the Temporal Liquidity Market: How TLM Expands the Blockchain Economy"
version: v0.6 (recasts sec. 3 as the commodity/capital/money storability thesis - blockspace's fee, quoted in the native coin, is storable and the coin is a claim on the capital that produces blockspace - and adds the numeraire/own-rate and fee-as-abstraction subsections as the canonical exposition RN-11 can reference and simplify against; bridges sec. 6 to it; corrects the abstract and sec. 13 to the dual/market-curve non-identity. Supersedes v0.5: retitled around the causal claim; sec. 12 rewritten as the synthesis that claim needs, including retention and the exit evidence; **project type** introduced in sec. 1 as the class-level unit above **project**; abstract reordered to close on the argument. Supersedes v0.4, which added the two-sided-market keystone, the partition by binding tightness, and the prior-art positioning of sec. 8.8, and moved the formal statement to RN-11 and the open questions to a companion note.)
status: "Concept note - the economics of the TLM program. Public draft, circulated for external review and comment."
program: "Temporal Liquidity Market (TLM)"
date: August 12, 2026
---

# RN-10 - The Economics of the Temporal Liquidity Market

## Abstract

Blockchain fee markets are usually modelled as spot markets: isolated transactions bidding for inclusion in the next block. This note argues that a market in **temporal liquidity** - in the flexibility to execute sooner or later - is what turns such a fee market into an economy, and that it **expands** that economy beyond what a spot price can support at all.

The argument begins with a different object. A blockchain continuously re-produces execution capacity, slot after slot; the infrastructure that produces it is durable capital; and the economically meaningful unit of demand is not the transaction but the **project** - a long-lived source of demand with a characteristic temporal profile. Read this way, a blockchain is a market that allocates **execution capital across time** among competing projects, and its purpose is to finance a diverse ecosystem rather than to clear a queue.

Three claims follow. First, blockspace is a **two-dimensional** resource (capacity by time), and only under this view does temporal structure become an endogenous, protocol-visible, first-order variable rather than an exogenous index. Second, **a fee mechanism is never neutral with respect to project type**: a single scalar spot price implicitly selects which project types can exist on-chain, and so functions as industrial policy hidden inside a pricing rule. Third, the inter-temporal dimension of demand admits a **term structure of block-fee-rates** - a **block-fee yield curve**, the execution-market counterpart of the yield curve of interest rates - in which a committed, predictable project rationally pays a low, smooth rate while volatile demand pays spot, and which must be **arbitrage-free** as a hard design constraint. The curve's *shape* is itself informative: inverted during congestion, upward-sloping ahead of a known event, humped around a scheduled one - a readout of the demand mix, as in finance. Its practical form is a **swap curve**, exchanging a fixed rate for the floating spot fee; and because the floating index is published by the protocol every block, such a contract needs no oracle and is marked to market continuously, making it a natural on-chain construction.

These are unified by a formal statement of the problem, given in the formal companion note **RN-11**: the protocol allocates capacity across quanta so as to maximize value-weighted execution subject to capacity, neutrality, reducibility, and incentive compatibility, and its dual is a vector of shadow prices on per-quantum capacity - a *welfare benchmark* that RN-11 states alongside the market term structure **without identifying the two**, leaving open whether a decentralized fee market reproduces it. Read as a benchmark, the dual turns several of the arguments below, including fee-as-filter, into consequences of one allocation. This note stays at the level of economic structure and does not develop it.

The keystone claim (sec. 8) is that a market in flexibility needs both a supplier and a taker, and that making temporal characteristics protocol-visible is what brings both into existence. A scalar spot fee builds only the taker side - the priority fee is a bid for temporal liquidity with no way for anyone to offer it - and, by pricing patient demand off the chain, erodes the very population that could supply it. It is also a delayed feedback controller, adjusting next block's price after this block's congestion, with the overshoot and slow convergence that delayed control implies. A two-sided temporal market instead contracts flexibility in advance and calls it within the quantum, damping a surge as it happens rather than signalling it to the block after.

Demand divides on a single question (sec. 7): **how much drift between wall-clock relevance and block-time execution can this work absorb?** Work that tolerates drift can step aside and is the natural **supplier** of temporal liquidity; work that cannot is the natural **taker**. This is deliberately *not* a division by predictability - a mint at a known block or a scheduled expiry is entirely foreseeable and entirely immovable, and congests exactly like an unforeseen liquidation. Predictability is an independent axis, and it governs something else: whether a shortfall can be cleared by a scheduled call auction or must rely on capacity contracted in advance. Tightly bound work cannot be served by reserving a future slot at all; it needs a paid *right to execute if the moment arrives*, closer to insurance than to a reservation. The note also identifies what a term structure does *not* price - the axes it does not reach: intra-quantum ordering, state contention, extraction-resistance, and truthful revelation - and argues that reserve capacity must be *contracted flexibility*, not residual slack, since slack is anti-correlated with need.

These converge on one claim (sec. 12). Pricing horizons makes long-lived projects financeable; making flexibility visible builds the supply side a spot market never had; and a two-sided market serves an event-driven economy that a tip auction can only ration. A fourth route is already on the record: the on-chain perpetuals and order-book **project type** - dYdX v4, Hyperliquid, Aevo - did not stay and overpay but **left to build sovereign chains**, and it left as a whole type, not as scattered firms. **A chain holds a project type only if its market can express what that type needs**; where it cannot, the type exits and takes its liquidity and composability with it. So **a temporal liquidity market expands the set of project types a chain can carry** - not because capacity grew, but because demand that was unpriceable became priceable, and a project type that had no reason to stay acquired one. Concrete mechanisms are out of scope and are developed elsewhere. Prior art is drawn from capacity and peak-load pricing, market microstructure, fixed-income theory, market design, and monetary economics; an exploratory section on the circulation of execution capital is posed as questions.

## 1. From transactions to projects

The fundamental economic object is not the transaction; it is the **project**. A project is a long-lived source of execution demand with a characteristic temporal-liquidity profile - a perpetual exchange such as Hyperliquid, a payment network, an oracle network, a rollup, an AI-agent platform, a game world, a secondary market, or a virtual app-chain (RN-09). Transactions are simply the realizations of a project's ongoing demand.

```text
Execution capital  ->  projects  ->  execution streams  ->  transactions
```

This mirrors how a financial market treats firms and projects, not individual trades, as the unit that capital is allocated to. A perpetual exchange is not a stream of unrelated transactions competing for the next block; it is one project with a distinct, continuous, low-latency, bursty-under-volatility demand for execution capital over time. Seeing the project - not the transaction - as the object is what lets the protocol reason about financing an ecosystem rather than clearing a queue.

**Two levels, and the note needs both.** A **project** is an individual going concern: Hyperliquid, one payment network, one oracle service. A **project type** is the set of projects that do the same kind of thing and therefore share a temporal structure, so that they stand or fall together on the same market design: on-chain perpetuals and order books, payment rails, oracle networks, rollup settlement, agent platforms.

The distinction carries the argument, because a market's failure is visible across a project type and invisible at a single project - one venue leaving is a business decision, a whole type leaving is a statement about the market (sec. 5, sec. 12).

Two neighboring terms mean something else. The **service classes** of RN-04 (immediate, protected-window, scheduled, patient) describe *how* work is served, not who demands it; one project type uses several of them (sec. 6.7). And this note calls the two demand *modes* the continuous economy and the event-driven **economy** (sec. 9); those cut *across* project types rather than partitioning them, since a perpetuals venue has continuous quoting and event-driven liquidations and lives in both.

## 2. Execution-capital demand functions

Each project carries its own **execution-capital demand function (ECDF)** - its demand for execution capital as it evolves over time, described by duration, intensity, flexibility, deadline, persistence, and predictability (the RN-01 temporal profile, read at project scale). For example: a perpetual exchange has continuous, low-latency demand with a predictable baseline and volatility-driven bursts; a payment network has steady, recurring, mildly delay-tolerant demand; an AI-agent platform has continuous background execution with elastic, variable urgency. A virtual chain (RN-09) is naturally a project with its own ECDF, not merely an isolated execution environment.

This description is informal. **RN-11** gives it a formal definition and places it inside the allocation problem it belongs to.

**A note on the level of analysis.** This note works at the level of *economic structure*: what kinds of demand exist, what markets could exist between them, and what a protocol would need to make visible for those markets to form. It does not propose a fee mechanism and does not compare itself to one.

That distinction matters most wherever EIP-1559 appears below. EIP-1559 is a carefully engineered and, in its own terms, elegant design: an algorithmic base fee that responds to utilization and is burned, paired with a priority fee that auctions the margin. It solves the problem it was built for - pricing inclusion in the next block, with predictable user-facing fees and a credible burn - and solves it well. Where this note observes that something is absent, the observation is about the **scope of the market that exists today**, not a defect in the mechanism: a mechanism cannot be faulted for lacking what it was never asked to provide. The intended use of this framework is the opposite of a critique - to identify structure that a chain like Ethereum, or any other, could add on top of what already works.

Projects and their demand functions are the *demand* side. What they are demanding is execution capacity - and how that capacity should be understood is the subject of the next section.

## 3. Three views of blockspace: commodity, capital, and money

Blockspace can be viewed three ways. They are not rivals but levels, and the note's claim is that the conventional account stops at the first when the economically decisive facts are at the third.

**View 1 - blockspace as a commodity (the conventional view).** Take a single slot in isolation. Its capacity is a perishable service flow: whatever is not used in slot *t* is gone - like a megawatt-hour not drawn at noon, an unsold seat on a departed flight, an idle CPU cycle. Priced this way, blockspace is a non-storable commodity, its market a spot market for the next block (EIP-1559) with, at most, a commodity-forward curve driven by expected scarcity. On this view a blockchain is an electricity grid for computation, and it is the analogy most people reach for first.

**View 2 - the network as durable capital (the stock-flow correction).** View 1 is true of a slot alone but mistakes the flow for the whole. The network is a durable, productive asset that re-produces execution capacity slot after slot; a slot's capacity is one period's *service flow* of that capital. The stock persists, the flow is perishable - the standard structure of any durable asset that yields a non-storable service (a generator, an aircraft, a telecom network). This corrects one over-reach: unused slot capacity is not stored throughput carried forward (each slot is a fresh allocation, sec. 4), but the capital that produces it endures, and what carries across time is a *commitment* on future flow, not saved-up flow. View 2 is not an alternative to View 1; it is the level at which "who gets this block" becomes "how is this capital's output allocated across time."

**Execution capital, defined.** The term names this stock, not the flow. *Execution capital is blockspace viewed as capital - the network's durable, capacity-producing capability.* Its per-slot service flow is **blockspace** (execution capacity), the object a market prices and allocates; its **capital value**, the principal, is the present value of the fees that flow will earn (sec. 3.1). The three stay distinct throughout: the capital is the stock, blockspace is its flow, and the capital value is what the stock is worth. Where later sections speak of *allocating execution capital across time*, they mean allocating that flow - deploying the capital's output - as one speaks of allocating human capital by deploying labor, not of dividing up the stock itself.

So far this is the electricity story: durable grid, perishable power. If it stopped here, blockspace would be a commodity with a commodity-forward curve and nothing more, and a reviewer who read it that way would be right. The third view is where blockspace departs from electricity, and it is the foundation of the note.

**View 3 - the fee is money, and the money is the capital (why blockspace is not electricity).** Electricity is priced in a numeraire *external* to the grid: dollars, which the grid does not issue and whose value does not derive from electricity. Blockspace is priced in the *native coin* of the chain that produces it, and that single fact changes the economics. The coin is **storable** - you can hold it across slots - and **yield-bearing**: its own rate of return, realized through staking, is paid out of the very fee stream blockspace generates. The coin is therefore not external money but a **claim on the capital that produces blockspace**: holding it (staked, plus the deflation the base-fee burn confers on every holder) is holding equity in the blockspace business. The fee, quoted in that coin, is **storable in the way the dated service is not** - not because slot-*t* execution can be warehoused to slot *t+1*, but because the *value* dimension of the market lives in a storable, endogenous, yield-bearing numeraire rather than in external cash.

This puts blockspace on a spectrum whose two ends are familiar:

- at one end, a pure **commodity** priced in external money (electricity): the service is non-storable and the numeraire is decoupled, so the forward curve is scarcity-driven and carries no bond structure;
- at the other end, **money** itself: perfectly storable and shiftable, so its term structure is fully arbitrage-linked - money is simply the frictionless limit of a temporal market, not a different kind of object.

Blockspace sits between: its service flow is non-storable (the commodity end), but its numeraire is the storable, endogenous capital of the system (the money end). Where it lands is not fixed - it is an outcome of market design, and the lever is temporal liquidity. Demand that tolerates drift can move across slots, and that substitution is the intertemporal arbitrage a pure commodity lacks; the more of it a market mobilizes, the more the blockspace curve behaves like a money curve than an electricity one. **The purpose of a temporal liquidity market is to move blockspace toward the money end of that spectrum** - to give a non-storable service the term structure of a storable one, by supplying the substitution that storage supplies for a commodity and that issuance-and-lending supplies for money.

| | Commodity (View 1) | Capital (View 2) | Money (View 3) |
|---|---|---|---|
| Object | a single slot's service flow | the durable network producing it | the fee, quoted in the native coin |
| Storable? | no - perishable flow | stock persists, flow expires | the value dimension is storable and yield-bearing |
| Numeraire | external (dollars) | -- | the chain's own coin, a claim on the capital |
| Forward curve | scarcity-driven, no bond structure | -- | bond-like in denomination and chaining, linked by demand substitution |
| Analogy | electricity | a generator | an economy priced in its own currency |
| Conventional stop | EIP-1559 spot | -- | TLM |

The rest of the note prices execution on View 3: a term structure in the native coin (sec. 6), whose level and discounting live in the coin's own-rate (sec. 3.1), whose shape is set by the demand mix, and whose spot-forward linkage is enforced by temporal liquidity. The honest caveat travels with it: the dated service is non-storable, so the linkage is bounded by the mass of flexible demand, and the curve keeps commodity features - event spikes, humps - to the extent substitution is thin. That caveat is a dial, not a wall, and turning it is what the program is for.

### 3.1 The numeraire and its own-rate

Two rates must be kept apart, because pricing execution in the coin invites collapsing them. The **fee** is a *rental rate* - the price of one period of deployed capacity, in coin. The **discount rate** B is the price of the coin across time - what compounds. The fee is not an interest rate; B is, and B is the coin's **own-rate**: the yield the aggregate fee stream throws off on the capital that produces it. In steady state, with aggregate real fee income R on a capital value P and growth g, B = R/P + g - a fixed point, endogenous to the fee stream it discounts. That endogeneity is the formal content of "the money is the capital."

B is not the staking yield. Staking yield mixes the real fee-and-MEV income (B's numerator), protocol issuance (a monetary transfer among holders, not real income), and the mechanics of staking; strip the last two and the fee-derived remainder is B. Staking is one institutional way B is realized, still in the coin. Two consequences carry into sec. 6. Over a single slot B is approximately 1 - a few percent a year over twelve seconds is negligible - so intra-slot the discount is inert and the congestion price is the whole story; B matters only across the multi-slot horizon. And principal lives in the aggregate claim on the fee stream - staked coin plus burn-accretion - whose capital value is what a durable capacity claim (sec. 6) is worth. An individual patient transaction that supplies flexibility holds no such claim; its compensation is a transfer among users (sec. 6.1), not a yield on capital. The two are different objects, and the incidence should be read off explicitly: base-fee burn accrues to all holders as scarcity, tips and MEV to stakers, and B's numerator is their sum.

### 3.2 The fee is an abstraction

One clarification the rest of the note depends on: the "fee" priced here is not today's Ethereum fee. Today the price of execution is fragmented and partly hidden - a base fee that is burned and prices congestion, a priority tip to the proposer that prices intra-block position, and MEV captured off-protocol that prices ordering. A term structure needs one clean, protocol-visible price of execution across time. So the fee here is the unified price a future TLM-enabled protocol would expose, into which those fragments are re-examined and folded: the base fee generalizes to the per-quantum congestion price, the tip becomes a cleared advancement payment to the flexible supplier (RN-12), and inter-quantum ordering value is surfaced as a public temporal price while intra-quantum extraction is suppressed. Cleaning the fee into one object is itself part of moving blockspace toward the money end of the spectrum: a fragmented, hidden price is a commodity-market friction; a unified, visible one is a precondition for a well-behaved curve.

## 4. Deployed and undeployed capital, and leases

At any slot, execution capital = deployed + undeployed. Undeployed capacity is **reserve capital that was not lent out that period** - like a bank's reserves - not waste. It can serve as reserve capacity, optionality, a congestion buffer, insurance against demand spikes, and headroom for future commitments. One caution keeps the accounting honest: undeployed capacity is a *per-slot* reserve, not an accumulating balance - each slot offers a fresh allocation, and what carries across time is a *commitment* (a lease on future capacity), not stored-up throughput. The goal of protocol design is therefore not zero idle capacity but an **optimal deployment policy** across the capacity-by-time grid.

That policy naturally admits **execution-capital leases**: forward or long-term reservations of future capacity, coexisting with a spot market for immediate execution. This is the oldest pattern in capacity pricing - reserved versus on-demand cloud instances, electricity capacity markets and peak-load pricing, airline revenue management, and network QoS reservation (IntServ/RSVP) [2-5]. The lease *concept* - forward versus spot - is public and belongs here; the specific pricing of a temporal-liquidity reserve is a separate, in-progress mechanism and is not developed in this note.

## 5. The supply side: the fee mechanism as filter and enabler

This is the note's central supply-side claim. **A fee mechanism is never neutral with respect to project type.** A single scalar spot price - EIP-1559's base-plus-priority fee [6] - implicitly selects which project types are viable on-chain and which are not.

A scalar spot market serves one kind of demand well: work that is one-shot, latency-tolerant, and willing to compete on price after arrival. It serves poorly, or excludes, project types whose value is **temporal** - continuous low-latency streams, reserved and predictable baselines, deadline-bounded work, high-frequency order flow. Projects of those types either overpay during congestion, fragment their activity off-chain, or leave to build a sovereign chain. The third option is the consequential one and it is already observed: the departure of the on-chain perpetuals and order-book project type (RN-03, RN-06 sec. 3.3) is this filtering in action, taken up as the retention argument in sec. 12. The general market could not price that type's temporal demand, so it filtered it out - and filtering, at the scale of a whole project type, means departure.

Read this way, the fee mechanism is an **implicit industrial policy hidden inside a pricing rule**. By rewarding one temporal profile and penalizing others, it decides which project types an ecosystem can support - not by design, but as a side effect of using a single scalar price for a multidimensional demand. A market-design literature makes the same point about continuous trading: Budish, Cramton and Shim show that the continuous limit order book mechanically manufactures a socially wasteful speed race, curable by moving to frequent batch auctions - a change in the *mechanism*, not the participants [7, 8]. The lesson transfers: the shape of the fee/allocation mechanism, not merely its price level, determines which demand is served.

The design objective follows directly: **neutrality, fairness, and openness across temporal profiles** (sec. 11). A well-designed execution-capital market does the opposite of the scalar filter - it *unearths and enables* a diverse ecosystem of projects (exchanges, secondary markets, payment rails, oracle networks, app-chains) that a spot-only market suppresses. The supply-side question TLM asks is therefore not "how do we price the next block?" but "what allocation mechanism finances the widest set of valuable projects under neutral rules?"

## 6. The time value of execution: a term structure of block-fee-rates

*This chapter draws on the term structure of interest rates - the time-value-of-money concept at the center of fixed-income finance. It develops the instrument, not the mechanism: how execution should be priced across horizons, not how a protocol should be built to do it.*

The conventional fee view - "urgent demand pays more" - is a single, volatile *spot* price. In finance that is only the shortest point on a whole **term structure**. The time value of money is not one number but a curve of rates across horizons, and blockspace has a direct and useful analog. That analog is priced on View 3 of sec. 3 - a term structure in the native coin, discounted at the coin's own-rate (sec. 3.1), whose spot-forward linkage is enforced by temporal liquidity rather than by storage. The arbitrage-free "one curve" developed below (secs. 6.6-6.7) is the base-model idealization: it holds on the marketed subspace, it is what the mechanism works to complete, and the storability dial of sec. 3 is its standing caveat.

### 6.1 A unit rate: the block-fee-rate

Define the **block-fee-rate** as the fee to obtain one unit of execution capacity for one unit of blockchain time - the execution-market counterpart of the interest rate (the price of money per unit time).

The unit of blockchain time matters, and it is **not the slot**. A slot is too coarse to be the atom of a temporal market: at twelve seconds it cannot express the sub-second structure that latency-sensitive demand cares about. Following RN-05, a slot is subdivided into an ordered series of **quanta**, and the curve is defined on that finer grid:

- **Across quanta, time is ordered.** A transaction in quantum k precedes every transaction in quantum k+1. This ordering is what the curve prices: a rate is attached to each quantum.
- **Within a quantum, time is not ordered.** Transactions in the same quantum execute in parallel, or in an arbitrary order; no wall-clock sequence is guaranteed. There is therefore no finer position for the curve to price, and none is offered.

So the block-fee-rate is a function on the **quantum lattice** - potentially far finer than a slot - not a per-slot number. This is developed in sec. 6.11, where the quantum is identified as the time step of the pricing model. Today's fee market prices one point on this axis. On Ethereum the immediate-block price has two parts that do different jobs: an algorithmic **base fee** that responds to utilization and is burned - a congestion controller and a monetary sink rather than a bid - and a **priority fee** that auctions the margin among transactions competing for the same block. Together they answer the question "what does it cost to execute now." What is absent is not precision at that point but the rest of the axis: there is one horizon, and so one rate, where a curve would have many.

**Rate, yield, and the curve.** Two words are worth fixing, because they are not synonyms and it matters here who is on each side. A **rate** is the price of capacity per unit time - the direct counterpart of an interest rate - and it is what a project pays to execute. A **yield** is what the provider of the resource earns. In this market the provider of capacity is the **network itself**: it produces execution capacity every quantum and earns fee revenue on it, so the schedule of rates across horizons is the network's yield on the capital stock of sec. 3. Users are takers of that capacity; the network is the counterparty on the other side, exactly as a rate is a cost to a borrower and a yield to a lender.

This also fixes what a flexibility payment is. When a project steps aside during congestion (sec. 8) and is compensated, it is **not** earning an investment return on capital it owns: it holds no capacity to lend. The payment offsets the fees it pays the network - a rebate on its own cost of execution, funded by a project that needs the capacity more. Flexibility payments are transfers among users within the network's fee take, not a second yield.

Following ordinary market usage, this note therefore calls the plotted schedule of rates across horizons the **block-fee yield curve**, and reserves *block-fee-rate* for the quantity at a single point on it.

### 6.2 A term structure of block-fee-rates

One way to see what is missing today: **the protocol prices the next block and nothing beyond it.** A block-fee yield curve is the rest of the term structure - the horizons past the immediate one, which no chain currently prices at all.

Forward pricing of blockspace is not untried. Markets for proposer commitments and preconfirmations let validators sell inclusion rights ahead of time - ETHGas as far as 64 slots out - and gas costs have been modelled as a stochastic process to value forwards and options over them [18]. Those efforts establish that a forward price for execution can be quoted and traded. What they produce is a set of prices at particular horizons, sold by the parties who hold the capacity. The proposal here is different in object: a **curve**, with a no-arbitrage condition tying every horizon to every other (sec. 6.6), and defined over the quantum lattice rather than the slot (sec. 6.9). A curve is what makes the horizons a single market rather than a collection of separate ones, and it is what lets a rate at one tenor discipline the rate at another.

Interest rates form a term structure - a set of rates by horizon - with standard objects, each of which has a blockspace counterpart:

| Interest-rate object | What it is | Block-fee-rate counterpart |
|---|---|---|
| short / overnight rate | instantaneous rate, reset continuously | the rate at the next quantum; today's immediate-block price (base fee plus priority fee) is the one point that exists |
| spot (zero) rate to maturity T | single rate from now to T | rate to reserve capacity from now through quantum T |
| forward rate f(t; T1, T2) | rate agreed now for a future interval | rate agreed now for capacity in a future window |
| long-term / term rate | average rate over a long horizon | rate for a committed horizon of steady demand, spanning many quanta |
| swap rate | fixed rate exchanged for floating over a tenor | fixed block-fee-rate a project pays to receive volatile spot - a lease converting spot exposure into a fixed rate |

The key point - and the correction to the naive "urgency = pay more" view - is that a project with **committed, steady demand over a long horizon can rationally pay a low, smooth rate**, exactly as a borrower who commits to a term gets a term rate rather than the volatile overnight rate. Volatility lives at the short end: the spot base fee spikes with congestion and, on a 12-second slot, can oscillate. The value of a **forward** or **swap** rate is that it lets a project lock a predictable rate and hand the spot volatility back to the market. A perpetual exchange with continuous, predictable demand (RN-03) is the canonical borrower who wants a fixed one-year rate, not to be re-priced every block. Concretely, a **one-year execution swap** would exchange the floating spot base fee for a fixed one-year block-fee-rate - the tenor-average of expected future short rates, in swap terms - giving the project a stable cost and the protocol a committed demand it can plan around.

### 6.3 The shape of the yield curve reads the demand mix

The two kinds of demand described in sec. 7 are not served by different markets; they occupy **different regions of the same curve**.

- **The short end** - the current slot, resolved at quantum granularity - is where demand that cannot wait must transact. This is spot: the rate at the next quantum and the few after it.
- **The long end** - horizons beyond the current slot, out to whatever tenor the market supports - is where demand that can commit in advance transacts.

Because both are priced on one curve, the curve's **shape** carries information. It is a readout of the demand mix, and it is heterogeneous for exactly the reason yield curves are heterogeneous in finance: different populations with different horizons are bidding at once.

| Shape | What it means on-chain | Finance counterpart |
|---|---|---|
| **Inverted** (short above long) | the surge state: event-driven demand is bidding for immediate execution while capacity further out stays cheap | inversion signalling tight current conditions |
| **Upward-sloping** (long above short) | anticipated scarcity: a known future event - a large mint, an airdrop, a scheduled upgrade - makes forward capacity dear relative to a quiet present | term premium; expected tightening |
| **Humped** | a scheduled event at a particular horizon lifts rates at that tenor, leaving both the immediate and the distant regions lower | a maturity-specific supply or demand concentration |
| **Flat** | a balanced mix with no strong expectation either way | equilibrium |

Note that **inversion is the normal congestion state for a blockchain**, not an anomaly: a surge raises the near quanta far above the forward horizon. A scalar spot fee reports one number and can express none of these states; a curve reports the distribution of demand across time, and its shape becomes a public signal that participants - and the protocol's own control logic - can read and act on.

### 6.4 The swap curve: fixed versus floating

In practice the most useful representation of a term structure is often not a set of zero rates but the **swap curve** - the schedule of fixed rates that exchange for floating at each tenor [14]. The same holds here, and for a reason specific to blockchains.

A **block-fee swap** exchanges two legs over a horizon:

- the **floating leg**: the realized spot block-fee-rate, quantum by quantum;
- the **fixed leg**: a single rate agreed at inception for the whole horizon.

A project with steady demand pays fixed and receives floating: its execution cost becomes a budgeted line item, and the volatility of the spot fee passes to a counterparty willing to hold it. This is what the term rate of sec. 6.2 looks like once it is actually traded rather than merely quoted.

Two properties make this unusually well suited to on-chain implementation.

**The floating index is native.** The hardest part of building an interest-rate swap in traditional markets is agreeing on the floating reference; the long history of LIBOR and its replacement is largely a history of that problem - a rate submitted by a panel, administered by an institution, and vulnerable to manipulation. Here the reference already exists. The protocol publishes the base fee every block, canonically, as part of consensus. No oracle, no panel, no administrator: the index is a first-class protocol observable, produced by the same system that settles the contract.

**It is mark-to-market by construction.** The value of the swap at any moment is the difference between the fixed leg and the expected remaining floating leg, and because the index updates every block, that mark is continuously and objectively computable on-chain. Continuous marking is what makes margining, collateral calls, and default handling tractable - and settlement can stream per quantum rather than in periodic lumps (sec. 4).

Together these make a block-fee swap a natural decentralized-finance construction: a contract with a native canonical index, a continuously computable mark, and settlement in the same system that produces the index. The curve such a market reveals - the **block-fee swap curve** - would then be the practical benchmark, bootstrapped from traded contracts rather than administered by anyone. That matters for neutrality (sec. 11): a curve discovered by trading needs no committee to set it.

### 6.5 A risk-free curve and a commitment spread

Interest-rate term structures come in layers: a near-risk-free curve (Treasury / OIS, no default risk), and, for less creditworthy borrowers, a **spread** over it reflecting the credibility of the commitment. The blockspace analog is direct:

- The **base block-fee-rate curve** is the protocol's neutral price of capacity across horizons - the "risk-free" curve.
- A reservation or lease is only as good as the **commitment behind it**. A bonded, verified commitment - a project that posts a deposit and has a track record (RN-02 verification; RN-08 reservation deposits) - earns the base rate. A weakly-committed or unbonded reservation, one that may go unused, pays a **spread** over the base curve, or must post more collateral. The spread is the price of *commitment credibility*, just as a credit spread prices default risk.

This keeps the structure neutral: the spread is a function of *verified commitment*, not identity - a committed, verified one-year demand earns the low rate whoever holds it.

### 6.6 The fundamental law: arbitrage-free pricing

The law that makes a term structure coherent is **no-arbitrage** - the fundamental theorem of asset pricing: no set of trades should produce a riskless profit from nothing [15]. Under it, the pieces of a curve are not free to choose. Forward rates are *pinned* by spot rates - a two-year commitment must equal one year rolled into the no-arbitrage one-year-forward, or someone arbitrages the gap - and instruments with identical cash flows must have identical prices (the law of one price). Arbitrage-free pricing is what makes spot, forward, and swap rates one consistent object rather than three unrelated numbers.

The same law must govern block-fee-rates. If a one-year committed rate could be replicated more cheaply by rolling forward reservations, or capacity bought in one form could be risklessly re-sold in another, the schedule is broken. Any multi-horizon execution-pricing scheme must therefore be arbitrage-free - a hard constraint on mechanism design, and the economic sibling of Roughgarden's off-chain-agreement-proofness (OCA-proofness): a well-designed schedule leaves no riskless off-protocol or cross-instrument trade [8].

### 6.7 One curve, not many: the term structure itself differentiates temporal liquidity

A first instinct is to give each service class (RN-04) its own curve, as different credit qualities each have a yield curve. That is probably the wrong lesson, for two reasons.

First, in fixed income one does *not* keep a separate curve for three-month money and five-year money: a **single** term structure prices every horizon, and different needs are just different points or patterns on it. The temporal service classes - immediate, protected-window, scheduled, patient - are likewise different *shapes of demand across the time axis*, not different credit qualities. A single term structure of block-fee-rates already differentiates them: a deadline-bound task prices near the volatile short end; a committed, predictable stream prices off the smooth term/forward part; a reservation is a forward point. The curve is the differentiator.

Second, **multiple curves invite arbitrage between them.** If continuous, protected-window, and scheduled capacity each carried an independent curve, one could often replicate a dearer class from cheaper points on another and profit risklessly. Collapsing to one arbitrage-free term structure removes that cross-class arbitrage by construction: there is a single price of capacity at each point on the time axis, and every service is a portfolio of positions on it.

So the stronger hypothesis this chapter prefers is: **one arbitrage-free term structure of block-fee-rates is the ultimate object that differentiates inter-temporal liquidity.** Duration, delay tolerance, windows, deadlines, predictability, and continuity all map to positions on the single curve, and "service classes" are named regions of it rather than separate markets.

Two dimensions sit outside a pure horizon curve and are worth naming, so the claim is not overstated:

- **Commitment credibility** (sec. 6.5) enters as a *spread* on the curve - the credit-risk analog. A weakly-bonded reservation pays the base rate plus a spread, or posts more collateral. This is a spread function on one curve (or a bonding rule), not a separate market.
- **Ordering inside a quantum, and state access** (RN-01, RN-05) are *orthogonal* axes. Recall the granularity (sec. 6.1): the curve lives on the quantum lattice, so it prices *which quantum* a unit of work occupies - a position in an ordered sequence that can be far finer than a slot. What it does not price is anything *inside* a quantum, because inside a quantum there is no ordering to price: execution there is parallel or arbitrary by construction. Should a service class choose to impose an interior order (say, first-come-first-served within a quantum), that is a *different good*, bought at a verification cost, not a point on the horizon curve (RN-04, RN-05). The same holds for **state access** - which state a transaction touches, and whether it collides with others - which is a contention property, not an inter-temporal one. Both remain separate variables in RN-05's multiplexing structure, not additional curves.

With those two caveats, the term structure is the single, unifying instrument for the time dimension of temporal liquidity.

### 6.8 HJM: a framework, not a single model

Because these curves move stochastically (demand and congestion shocks), pricing forwards, leases, and swaps needs a model of how the *whole curve* evolves. The **Heath-Jarrow-Morton (HJM)** approach is the right reference because it is a **framework, not one model** [12]. HJM takes the entire initial forward-rate curve as given, lets the modeller specify the *volatility* of forward rates, and then the **no-arbitrage condition determines the drift** (the HJM drift condition) - arbitrage-freeness, not the modeller, fixes it. Specific models are instances within the family: Ho-Lee and Hull-White, and the mean-reverting short-rate models of Vasicek and Cox-Ingersoll-Ross [13]. HJM has also been **extended to defaultable term structures** (credit spreads [15]) - which is what the commitment-credibility spread of sec. 6.5 needs. But the primary object to model is the *single* forward block-fee-rate curve (sec. 6.7), with the commitment spread layered on it. HJM is therefore the natural framework to adapt: model the forward block-fee-rate curve, and its commitment spread, under a no-arbitrage drift condition. This is a substantial research program in its own right, flagged as a direction, not a result.

### 6.9 The quantum lattice as the time discretization of the model

The term structure needs a time grid, and RN-05's **quantum lattice** supplies it. The correspondence is closer than an analogy: it is the same construction.

In continuous-time interest-rate modelling one writes the dynamics over an interval Delta_t and takes Delta_t small; numerical implementations then work on a **lattice** (binomial or trinomial tree) whose steps discretize the driving Brownian motion. RN-05 divides the slot into **quanta**: a partial order is fixed *across* quanta, while *within* a quantum ordering is free - parallel semantics, no guaranteed wall-time order by default. That gives an execution-side time grid with the property a pricing grid needs:

> **The quantum is the Delta_t of the model.** It is the atom of pricing time: because nothing inside a quantum is ordered by default, nothing inside it is distinguishable to price. Rates are defined per quantum, and the curve is a function on the lattice.

Three consequences follow.

**High-frequency representation.** Because quanta can be far finer than a slot (RN-05's result that quantum size is bounded by commitment and verification cost, not consensus latency), the lattice can represent demand at high-frequency-finance resolution while the chain still settles at slot cadence. A block-fee-rate curve defined on quanta can therefore express short-horizon structure - the sub-slot region where market making and latency-sensitive strategies live - that a slot-level rate cannot see.

**A natural refinement limit.** In finance Delta_t may be taken arbitrarily small toward the continuous limit. Here refinement stops where the lattice stops: the quantum floor set by commitment/verification cost, and the clock-uncertainty interval epsilon of RN-05 sec. 4.6 (a boundary is an interval, not a point). So the model has a *physically meaningful* smallest step rather than an idealized one - and the confidence relation of RN-05 (roughly 1 - epsilon/Q) becomes a statement about how sharply a rate at a given resolution can be defined at all.

**Volatility and stochastic dynamics.** With a grid in hand, the usual machinery applies: model the forward block-fee-rate as a stochastic process on the lattice, with a Brownian (or jump-augmented) driver for congestion shocks, and let no-arbitrage fix the drift (sec. 6.8). Congestion is bursty, so a pure diffusion is likely insufficient - a jump component is the natural extension, and the HJM family accommodates it. Interior freedom matters here too: because intra-quantum order is unconstrained, the process is defined on quantum-indexed states, not on individual transaction positions - which keeps the state space tractable.

This is the concrete bridge between the two halves of the program: **RN-05 supplies the coordinate substrate (the lattice); this chapter prices on it.** The open modelling question is which driving process fits observed congestion, and whether rates estimated at one quantum resolution remain consistent when the lattice is coarsened or refined.

### 6.10 What the term structure covers, and what it does not

This is the point at which the temporal-liquidity umbrella becomes a *priceable object* rather than a list of properties, so its scope should be stated.

**Covered - the inter-temporal family.** Delay tolerance and value decay (short versus term rates); execution windows and deadlines (points and segments on the curve); duration and continuity (the horizon of a commitment); predictability (why a committed, forecastable profile earns a smooth term rate rather than volatile spot); and commitment credibility (as a spread, sec. 6.5). These collapse into one arbitrage-free curve (sec. 6.7).

**Not covered.** Four gaps are genuine, and none is closed by a term structure. Each is a *different axis*, not a longer horizon on the same one:

1. **Ordering within a quantum.** The curve prices *which quantum* on the lattice (sec. 6.1, sec. 6.9) - a grid that can be far finer than a slot - but not *position inside* one, because intra-quantum order is free by construction. Interior order is a rank, not a horizon: a separate good purchased at a verification cost, developed in RN-04/RN-05, and where most extraction occurs.
2. **State access and contention.** Two commitments occupying the same quantum may collide on hot state. A rate says nothing about *which* state a transaction touches, so the curve cannot price contention externalities on particular contracts (the state axis of RN-05).
3. **Extraction-resistance.** The curve prices time but does not protect it. Worse, a forward reservation *reveals future demand*, creating a new disclosure surface that the term structure itself cannot defend. Any such market must be evaluated for off-chain-agreement-proofness and front-running exposure (sec. 6.6; RN-04).
4. **Truthful revelation and verification.** Pricing presumes an observable profile. Nothing in a curve makes a declaration honest; verification, bonding, and realized-behavior checks sit outside it (RN-02).

**The long end is not among them.** It is worth being explicit, because the objection is a natural one: no party today controls capacity at a far-future slot, so how can a long horizon be priced? The answer is the one fixed-income markets settled long ago, and it is already in the construction. A swap has no deliverable underlying. It exchanges a fixed leg against a realized floating index and settles in cash, and the block-fee swap of sec. 6.4 does exactly this against an index the protocol itself publishes every block. A project locking a one-year rate is not buying a far-future slot from anyone; it is exchanging its exposure to the realized path. Because the index is native and the mark is continuously computable, the contract is collateralizable and defaultable-against without any party controlling future capacity. Physical reservation is one way to serve a long horizon, and the harder one; cash settlement against the native index is the other, and it is available immediately. How far out such a market extends in practice is a question of how it is built out over time, not a limit of the framework.

**Summary.** The term structure is a complete instrument for the **time axis** and an incomplete one for temporal liquidity as a whole: it prices *which quantum*, but not *where inside a quantum*, not *on what state*, and not *safely against whom*. Those remain the open problems of the wider program.

### 6.11 Why this matters

The term-structure view replaces "urgency = pay more" with a theory of the **time value of execution capacity**. It explains why a committed, predictable project should pay *less*, not more, than volatile spot demand; why forward and swap instruments are the natural way to give projects stable costs; and why the credibility of a commitment - not the identity of the committer - should set the spread. It also supplies a discipline and a simplification: a *single* schedule of rates across horizons (plus a commitment spread) must be **arbitrage-free**, which unifies the service classes into one curve, rules out hand-set per-class fees, and ties the design to a well-understood body of theory. It is the economic content behind the forward-versus-spot leases of sec. 3.

---

## 7. Two camps of demand

Every on-chain execution has an external referent: some wall-clock moment at which the economic need arises - a price crosses a threshold, a contract expires, a batch fills, a user acts. Execution then happens at some block time. The economically decisive question is how tightly the second must track the first:

> **How much drift between wall-clock relevance and block-time execution can this work absorb before its value is destroyed?**

Write the gap as `T_block - T_wall`. What matters is not its realized value but the **tolerance** for it - how wide a dispersion the work can accept. That tolerance sorts demand into two camps, and it is the question the framework turns on.

- **Tight binding.** The gap must be near zero and near-deterministic. Value collapses almost immediately as execution drifts from the moment of relevance.
- **Loose binding.** The gap may be wide and variable. Value survives substantial drift.

**This is not the same as predictability, and conflating the two is the error to avoid.** Knowing *when* work will arrive says nothing about whether it can be *moved*. A scheduled token mint at a known block, an expiry settlement at an appointed time, a funding-rate payment at a fixed hour - all are perfectly foreseeable and completely immovable. They are scheduled *and* tightly bound, and they will contribute to a surge exactly like an unforeseen liquidation. Predictability and flexibility are independent properties, a point this program established earlier (RN-03) and which the formal treatment keeps separate. The distinction that does the work is between when work *arrives* and when it is *relevant*: relevance is what execution drifts away from, and tolerance for that drift is a separate property from knowing when the moment will come. RN-11 makes both precise - tolerance as the width of a decay function measured against the relevance target, predictability as a property of how arrivals and targets are distributed - and they are defined over different objects, which is why the table in sec. 7.3 has no empty cells.

### 7.1 The tight-binding camp: takers of temporal liquidity

Work whose value is destroyed by drift must execute at the contested moment, and therefore *takes* temporal liquidity from whoever will yield it. Its members look unalike and arrive by different routes:

- **Triggered and unforeseen.** A liquidation once a position crosses its threshold; an arbitrage before the gap closes; an oracle update before a stale price is exploited; a response to a depeg. The trigger's timing is not knowable in advance.
- **Triggered and foreseen.** A mint opening at a published block; an auction close; a scheduled expiry or index rebalance; a funding settlement. Fully anticipated - and no more movable for it.

Both are tightly bound, and both are **correlated**: one external event summons many actors at once, so the arrival is systemic rather than idiosyncratic. That correlation is what turns tight binding into congestion.

Tolerance is a *measurable* property, not a self-declared preference, because delay has a quantifiable cost: the value lost to drift is the cost of delay, and the mechanism by which it is lost - price moving against the order while it waits, and information leaking to whoever can act sooner - is the subject of a long line of work in market microstructure [9]. A tightly bound execution is one whose cost of delay rises steeply within a few quanta.

The instruments of sec. 6 do not serve this camp, for a structural reason: a curve prices *horizons*, and tightly bound work has no horizon to be moved along. Nor can the problem be solved by defensive reservation - if every potential taker held a standing claim against an event that fires rarely, nearly all of that capacity would sit idle in nearly every quantum. What fits instead is a **right rather than a reservation**: a premium paid now for the right, not the obligation, to execute if the moment arrives. That is the structure insurance and interruptible-supply contracts use for exactly this rare-correlated-urgent shape, and it matches the reserve framing of sec. 4: standing ready is the cost, and the premium is what pays for it.

This camp is developed in its own right in **sec. 9**.

### 7.2 The loose-binding camp: suppliers of temporal liquidity

Work that tolerates drift can be moved, and is therefore able to *supply* temporal liquidity - to step aside when the contested moment is worth more to someone else. Its members also look unalike, and differ only in the width and shape of the tolerance they can state:

- **Continuous streams with a movable baseline.** Market making, payment rails, routine order flow: constant demand, much of which is individually shiftable by a few quanta even though the stream as a whole is not.
- **Periodic work with a window.** Payroll, subscriptions, rollup batch posting, distributions: due within an interval rather than at an instant.
- **Patient and batch.** Rebalancing, archival, proof generation, analytics: tolerance measured in minutes or hours. The natural buyer of undeployed capacity (sec. 4), and the demand most plainly suppressed by a spot-only fee today.
- **Interactive.** Consumer applications wanting *bounded* latency for user experience: a guarantee of a band, not a position in a queue - and able to sit anywhere within that band.

Because each can state a tolerance in advance, all are served by the same instruments: the yield curve, forwards, leases, and swaps of sec. 6. One curve, several positions on it (sec. 6.7).

A caution follows directly from sec. 7's opening. Membership is a property of *the work*, not of the project. A single application typically issues both kinds: an exchange's routine quoting is loosely bound while its liquidation path is tightly bound; a rollup's batch posting is loose while its forced-inclusion path is tight. The camps partition **executions**, not applications - which is why the temporal characteristic must be declared per execution object rather than inferred from who submitted it.

### 7.3 Predictability is the second, independent axis

Tolerance decides *which side of the market* a piece of work is on. Predictability decides something else entirely: *which clearing mechanism can be used*. The two axes are orthogonal, and keeping them apart resolves what would otherwise be a contradiction.

| | **Foreseeable timing** | **Unforeseeable timing** |
|---|---|---|
| **Tight binding** (taker) | mint at a known block; scheduled expiry; index rebalance | liquidation; arbitrage; depeg response |
| **Loose binding** (supplier) | periodic batch posting; payroll | opportunistic rebalancing; background compute |

The practical consequence is a clean division of mechanism. **Foreseeable** congestion can be cleared by a scheduled call auction with a published imbalance, because there is time to broadcast the shortfall and invite offers (sec. 8.4). **Unforeseeable** congestion cannot; it needs supply contracted in advance and callable without a solicitation round (sec. 9.5). Tolerance tells you who trades; predictability tells you how the trade is arranged.

### 7.4 Why the division matters

The two camps need structurally different instruments: **commitments** for loosely bound work, **rights** for tightly bound work. A spot-only fee offers neither. It offers one instrument - a bid for the next block - to both at once, which is the filtering effect of sec. 5 in its plainest form: it serves whatever fits a spot auction and excludes the rest.

The division also locates each camp in the market for flexibility (sec. 8). Loosely bound work, able to declare a wide tolerance, is the natural **supplier** of temporal liquidity. Tightly bound work is the natural **taker**. That the two are complements rather than competitors is what makes a two-sided market possible - and it is why a chain that prices loosely bound work off-chain leaves the tightly bound with no one to trade with.

## 8. Temporal liquidity as a two-sided market

The preceding sections describe an economic object and a pricing instrument. This section states the claim that binds them, and it is the keystone of the framework: **a market in flexibility needs both a supplier and a taker, and making temporal characteristics protocol-visible is what brings both into existence.** Without it, event-driven demand cannot be served at all - not served badly, but not served.

The two camps of sec. 7 are the two sides of that market: work that tolerates drift between wall-clock relevance and block-time execution can step aside, and work that does not cannot.

### 8.1 Where temporal liquidity is supplied from

Temporal liquidity is not an ambient property of a system. It is *supplied*, by particular demand. When a surge arrives, the only capacity that can be released without destroying value is capacity held by work that does not need to run now. That work is the supplier.

This is the standard structure of liquidity, imported rather than invented. In market microstructure, liquidity is *immediacy*: Demsetz showed that immediacy is costly to supply, so only a subset of participants supplies it and is compensated by the demanders of immediacy; Grossman and Miller modelled market liquidity as the equilibrium of the supply of and demand for immediacy; Foucault, Kadan and Kandel showed that in a limit-order market the sorting is done by *patience* - patient traders post limit orders and supply liquidity, impatient traders take it with market orders [17]. The taker/supplier partition of sec. 7 is that same sorting applied to a different scarce good. What changes is the good: the supplier does not provide inventory in an asset but a **claim on a position in time**, and the concession it earns is paid in execution priority rather than in price. The consequence is that liquidity provision here is not the province of a specialized intermediary class; ordinary demand supplies it, by being patient.

But it can supply only if the protocol can *see* that it is flexible. In a scalar fee market, a transaction content to run after the surge is indistinguishable from one that must run immediately: both are bids. The flexibility exists in the world and is invisible to the mechanism, so it cannot be mobilized. Nothing prices it, nothing calls it, nothing compensates it.

This is why the model-first approach is not a methodological preference but a precondition. Modelling a project's temporal characteristics (RN-01/02; formally, RN-11) is what makes flexibility **addressable**: the protocol can identify which demand has a wide decay profile, invite it to stand aside, pay it, and verify afterwards that it did.

**Naming the supplier type.** Among the flexibility grades of sec. 9.5 is demand that sells the right to be displaced during congestion. "Interruptible" names what is done to it; a better name says when it returns: **surge-deferrable** - work that yields while a surge is running and executes once the surge has passed. The distinction is economically real, because the supplier is not giving up execution, only its position in time; and the price it charges depends on how quickly it is made whole (sec. 9.5, retry semantics).

### 8.2 Where the demand for temporal liquidity comes from

The taker is the mirror image: work that must execute now and cannot be moved - a liquidation before a position turns insolvent, an oracle update before a stale price is exploited, an arbitrage before the opportunity closes. Its value collapses within a few quanta of the moment it is needed: a narrow decay profile (RN-11).

The event-driven economy (sec. 7.1, sec. 9) is the taker side, and its defining feature is correlation: takers arrive together, which is what makes a surge a surge.

### 8.3 The market: matching rather than rationing

Once both sides are protocol-visible, they can be matched. Suppliers hold capacity they will release at a price; takers need capacity and will pay for it. The protocol brings them together and clears (sec. 9.5). That is a **market for temporal liquidity**, in which flexibility itself is the traded good.

The economic content is a change of kind. Under a tip auction a surge is a zero-sum race: everyone bids higher, surplus is dissipated into fees and latency investment, and patient demand is simply outbid and pushed out. Under a matched market the patient demand is *paid* to step aside, the urgent demand is served, and the value moves between the two parties instead of being burned.

There is also a capacity consequence worth stating plainly. Matching makes effective capacity **elastic at the moment of need**. A chain whose per-quantum capacity is fixed can nevertheless serve more urgent work during a surge than that capacity would suggest, by displacing flexible work into later quanta - without breaking prior commitments, and without adding hardware.

### 8.4 A working precedent: the equity closing auction

This design is not hypothetical. Equity markets run it every day, at the moment of their most concentrated demand, and the correspondence is close enough to be worth setting out in full.

At the close of a US trading session two kinds of order arrive. **Market-on-close (MOC)** orders must execute at the closing price: price-insensitive but absolutely time-bound, submitted by index funds, ETFs, and anyone whose mandate is tied to the official close. **Limit-on-close (LOC)** orders participate only if the clearing price is acceptable. These populations are correlated in exactly the way the takers of sec. 9.2 are - index rebalances, expirations, and month-ends summon them all at once.

The two sides rarely match. The residual is the **imbalance**, and what the exchange does with it is the instructive part.

- **The imbalance is published in advance.** NYSE disseminates a regulatory closing imbalance from 3:50 p.m., updated every second until the close, for any symbol whose imbalance exceeds a threshold (500 round lots, about 50,000 shares); Nasdaq publishes analogous indicative information [16]. The exchange broadcasts, ten minutes ahead: *here is the excess demand, and here is roughly where it will clear.*
- **Supply is then invited.** Participants may submit offsetting orders up to the close, including **imbalance-only orders** - an order type that exists solely to take the other side of a published imbalance. This is liquidity called forth by the signal.
- **Everything clears at one price.** The auction is a uniform-price call, so position within the event carries no value.
- **The urgent pay the flexible.** The imbalance side accepts a price concession; those supplying the offsetting liquidity earn it. The transfer runs directly between the two populations.

The outcome is the part worth dwelling on. The moment of greatest concentrated demand has become **the most liquid moment of the trading day**. US closing auctions matched roughly $50-55 billion per day in 2024, close to 9% of total notional volume - up from about 3% in 2010 - and roughly 20% on index-rebalance and expiration days [16]. The mechanism did not merely survive a concentration of urgent demand; it turned that concentration into the day's deepest pool of liquidity.

Every element has a counterpart here. MOC orders are event-driven demand bound to a specific window (sec. 9.2). The published imbalance is the **advance adequacy signal** of sec. 9.5 - and its use in a live market is evidence that publishing scarcity ahead of time calls forth supply rather than merely inviting predation. Imbalance-only orders are **flexibility offered on call** (sec. 8.1). Uniform-price clearing is the batch mechanism that removes any value in ordering within the event. And the price concession is the premium flowing from takers to suppliers.

Two differences sharpen the parallel.

**The close is scheduled; most chain surges are not.** Everyone knows the close is at 4 p.m., which is what makes a ten-minute imbalance broadcast and a submission window workable. That is the predictability axis of sec. 7.3 doing its work: **foreseeable** congestion - a known mint, a planned rebalance, a scheduled expiry - could use this design almost directly, with a published imbalance and a call auction at the appointed quantum, even though the demand causing it is tightly bound and entirely immovable. **Unforeseeable** surges cannot, and need supply contracted in advance that can be called without a solicitation round (sec. 9.5). Foreseeability determines the clearing arrangement; tolerance determines who is on which side of it.

**An equity imbalance is directional; a capacity shortfall is not.** In equities the two sides are buyers and sellers of the same asset, and the imbalance is net direction. On a chain there is no "sell side" of transactions: the shortfall is excess demand against bounded capacity, and the offsetting side supplies not the opposite trade but **deferral** - releasing a claim on the contested quantum. The market is two-sided in the same structural sense, but what the supplier provides is time rather than inventory.

**What the auction clears, and why two camps make it possible.** The analogy applies at a precise place on the lattice. A closing auction clears one moment - the close - and the counterpart here is not the whole curve but a single contested region: **the top quanta of the current slot**, which is exactly where event-driven demand sits (sec. 9.2). Everything further out is priced by the curve of sec. 6; this auction resolves the one region where the curve cannot help, because there is no later horizon to move to within it.

That such an auction is *possible* at all follows from the two-camp structure of sec. 7. A call auction needs two populations willing to clear against each other at one price. In a spot-only market there is only one population, all bidding the same direction, and an auction among them is a pure race. Once loosely bound work is visible and can offer deferral, the contested region has two sides - tightly bound demand seeking the top quanta, and loosely bound work holding claims there that it is willing to release - and a uniform-price call over that region becomes a well-posed clearing problem rather than a queue. **The camps are what make the auction work; the auction is what makes the camps trade.**

### 8.5 Today's market has only one side

Today's fee market already recognizes that urgency should be priceable: a priority fee is a bid for temporal liquidity, and the demand side of this market therefore exists and functions. What has never been built - because no fee mechanism was ever asked to build it - is the **supply side**. There is no way for a participant to *offer* flexibility, to be recognized as an offerer, or to be compensated for exercising it. The market has takers and no makers, and a market with one side is an auction.

One qualification sharpens the claim. There *is* an emerging supply side of a different kind: preconfirmation and proposer-commitment markets, in which validators sell rights to blockspace they are already entitled to produce [18]. That is the **producer** selling capacity forward - the analogue of a generator contracting output. It is a real market and it prices a real thing. But it does not create the side described here, because a validator cannot manufacture capacity during a surge; selling it forward redistributes claims on a fixed quantity, and at the contested moment the quantity is unchanged. The only source of additional capacity at the moment of need is **demand that agrees to move**, and that side has no channel at all. Producer-side forward sales and demand-side flexibility are complements, not substitutes: the first makes execution predictable, the second makes capacity elastic.

This is a statement about market structure, not about the quality of any mechanism (sec. 2). Two consequences follow, and the second is the more consequential.

**Price rises without mobilizing supply.** When demand surges, the immediate-block price climbs. Higher prices ration effectively - that is what they are for - but they cannot call forth flexibility, because flexibility has no channel through which to enter. Price is one instrument, and the other side of the trade has no way to respond.

**And a rising spot price displaces the very population that could supply flexibility.** The demand best placed to stand aside is patient, deferrable, price-sensitive, and low in value per transaction - exactly the demand that a high immediate price excludes first. Raising the spot price does not merely fail to recruit these participants; it moves them to cheaper venues or off-chain. So a spot-only market **erodes its own potential liquidity supply**: the harder it rations one surge, the less flexible demand remains on the chain to absorb the next. The filtering argument of sec. 5 returns here in its sharpest form, because what is filtered out is the population a temporal market would depend on.

### 8.6 Delayed feedback versus contemporaneous response

There is a second structural point, and it will be familiar to anyone who has worked on congestion control.

An algorithmic base fee of the EIP-1559 kind is a **feedback controller**: it observes the previous block's utilization and adjusts the next block's price toward a target. It does that job well, and the design is deliberately damped to keep user-facing fees predictable. But every feedback loop carries the delay of one block time in its path, and that is a property of the loop rather than of any particular tuning. Tuned aggressively, such a controller **overshoots** - the price peaks after the surge has already passed, falling on whoever arrives next. Tuned conservatively, it **converges slowly** - remaining below the clearing level while congestion persists. Fee oscillation around a surge is not an implementation defect; it is what delayed feedback control does, and no choice of parameters removes it.

The deeper point is one of scope rather than tuning: a controller of this kind is designed to steer average utilization toward a target over many blocks, not to allocate capacity within the moment a surge arrives. Those are different problems.

A temporal-liquidity market answers a surge differently, because it does not act through price adjustment at all. Supply is **contracted in advance** and **called at the moment of need**, within the same quantum, by matching. The response is contemporaneous with the surge rather than lagging it by a block, and it works by *moving demand* rather than by *repricing everyone*. Congestion is damped at its onset instead of being signalled to the block after it.

The networking parallel is exact. A price-or-window feedback loop can only react after a round-trip delay, whereas admission control over pre-contracted interruptible capacity acts immediately at the point of congestion. The two are complementary - but only the second operates inside the interval in which the surge actually happens.

### 8.7 What protocol-level differentiation creates

Putting these together, making temporal characteristics protocol-visible does four things a scalar fee cannot:

1. **It makes flexibility identifiable.** A supplier can be distinguished from a taker - the precondition for any market in flexibility.
2. **It makes flexibility compensable.** A declared and verified profile can be paid, through a lower standing rate or an exercise premium (sec. 9.5), which is what causes supply to appear.
3. **It makes flexibility callable.** Pre-registration lets the protocol act within the quantum rather than in the next block.
4. **It retains the supply side.** By offering patient demand a cheaper place on the curve instead of pricing it off the chain, the mechanism keeps the population that supplies temporal liquidity.

> **This is the keystone role of the temporal liquidity market: it turns a one-sided rationing device into a two-sided market in flexibility - and in doing so serves an entire economy, the event-driven one, that a scalar spot fee cannot serve at all.**

### 8.8 What this construction inherits, and what it adds

The pieces of this argument have identifiable parents, and saying which is which is the fastest way to see where the contribution lies.

**Inherited.** That liquidity is immediacy, that immediacy is supplied by the patient and demanded by the impatient, and that the supplier is paid a concession for it, is settled market microstructure [17]. That heterogeneous urgency exists on chains and that a fee mechanism can price-discriminate on it is established: tiered mechanisms allocate block space into tiers with increasing delay and decreasing price [8], models of quasi-patient users show how the fraction of demand willing to wait changes fee dynamics [19], and measurement confirms both that a diurnal fee cycle exists and that firms already shift work into cheap windows to exploit it [19]. That execution can be priced forward is demonstrated by proposer-commitment markets and by derivative valuation over gas processes [18]. That contracted flexibility clears scarcity better than rationing is standard practice in electricity markets, and that a two-sided call auction turns concentrated urgent demand into the deepest liquidity of the day is demonstrated daily by equity closing auctions [16].

**Added here.** Four things do not follow from that inheritance.

1. **Patient demand as the liquidity supplier, and the resulting two-sided market.** The blockchain literature treats patient users as a *demand segment* to be priced more cheaply, or as a parameter in fee dynamics. Here they are the **counterparty**: the party from whom capacity is bought at the moment of need, paid a premium for a claim they release. Tiered pricing gives the patient a discount for accepting a worse queue; this gives them a payment for supplying something scarce. The difference is not one of degree - one is price discrimination over a single-sided market, the other is a market with two sides.
2. **Binding tightness as the partition criterion.** The dividing variable is the tolerance for drift between wall-clock relevance and block-time execution, `T_block - T_wall` (sec. 7). It is not urgency, not value, not schedulability, and not predictability, and it cuts across all four. Its practical consequence is that the partition applies to **executions, not participants**: the same application supplies liquidity on one path and takes it on another.
3. **Protocol visibility as the precondition, not an optimization.** Flexibility that the mechanism cannot see cannot be priced, called, or paid, so it does not exist as supply. This is why the demand representation (RN-01/02) comes before the mechanism rather than after it, and it is what makes the market constructible at all.
4. **A curve rather than a set of prices.** Forward blockspace prices exist; a no-arbitrage term structure over a quantum lattice, in which the rate at every horizon disciplines the rate at every other, does not (sec. 6).

The nearest adjacent work is worth distinguishing, because the word is the same and the object is not. Two-sided transaction-fee mechanisms in the recent literature mean *users versus executing nodes* - heterogeneous valuations on one side, heterogeneous costs on the other [20]. That is a producer/consumer market. The two-sidedness here is **within demand**: both sides are users, and what crosses between them is position in time.

## 9. The event-driven spot economy

Section 6 developed the instrument for the continuous economy - a term structure across horizons. This chapter is its counterpart at the other extreme: the economy that lives entirely at the **spot** point, is genuinely urgency-driven, and cares about position *inside* the slot.

### 9.1 Where it sits on the lattice

On the two-dimensional lattice of RN-05 - capacity by time, with the slot divided into quanta - this demand occupies a narrow, identifiable region:

```text
                 quantum position within slot
                 earliest ------------------> latest
   current slot  [  EVENT-DRIVEN REGION  ]  |          |
   slot + 1      |          |               |          |
   slot + 2      |          |    <- term / continuous demand spreads here
   ...           |          |               |          |
```

Three coordinates define it: **current slot only** (the event is now; a future slot is worthless), **earliest quanta** (top of the slot), and **priority within the quantum**. That is the whole good. It is the true spot economy - the shortest point on the curve - and it is the one place where *position inside a quantum*, which a horizon curve cannot price (sec. 6.10), is the entire object of value.

### 9.2 Surge, herding, and rationing

Event triggers are **correlated**: a liquidation threshold, an oracle update, a depeg, a mint opening calls many actors at the same instant. Demand therefore arrives as a synchronized surge, not as independent draws. Because per-slot capacity is bounded, the surge cannot all be served, and something must ration it.

Today rationing is purely by price - a tip auction - which produces the familiar gas and latency race, and concentrates extraction at exactly the moment when the most value is at stake.

### 9.3 The tension: committed capacity versus surge revenue

Here fairness and neutrality come under real pressure. Suppose continuous and scheduled projects hold prior commitments on this slot's capacity (leases, sec. 4 and 6). A surge arrives with very high willingness to pay. The block builder faces a choice:

- **Maximize immediate fee:** reallocate capacity away from prior commitments to surge bidders. Revenue-maximizing in the moment.
- **Honor commitments:** serve the surge only from remaining capacity, and ration the rest.

The first option is the dangerous one, and the reason is structural: **a commitment that can be broken whenever spot exceeds the term rate is not a commitment.** It fails precisely in the states of the world where it was bought. If that is possible, no rational project will pay for forward capacity, and the entire term structure of sec. 6 collapses. Commitment integrity under surge is therefore a *precondition* for the continuous economy, not an operational detail - the same lesson insurance and reinsurance learned: a promise is worth what it is worth under stress.

### 9.4 Reserve is contracted flexibility, not leftover space

A third path exists between breaking commitments and hard-rationing: hold a **reserve** and release it under surge. But the word needs care, and an important distinction was glossed over in sec. 3.

**Residual slack** - blockspace that happens to go unsold in a slot - is not a reserve. It has a disqualifying property: it is *anti-correlated with need*. During a surge there is no slack, because that is what a surge means. A reserve built on leftover space is empty exactly when it is wanted.

A real reserve must be **created**, by someone forgoing use of capacity they actually hold. This is how electricity systems work: operating reserve is not idle capacity the operator owns but **contracted, paid-for headroom** - generators bid into ancillary-services markets and are paid to run below maximum or stay ready to start, and interruptible loads are paid to be curtailable. Reserve exists because participants are compensated for standing ready.

The blockchain counterpart is the same: reserve is the **aggregate of pre-contracted temporal flexibility**. Which means the reserve and the demand-response mechanism of sec. 9.5 are not two ideas but one - the reserve *is* the contracted flexibility, and a "draw" is simply calling it.

### 9.5 Two-sided elasticity: graded flexibility and a matching engine

Rationing need not be one-sided. If participants declare their temporal flexibility in advance - the profiles of RN-01/02 - a surge can be cleared on **both** sides, with patient demand paid and urgent demand served.

The flexibility is naturally **graded**, and the grades map onto the two axes of the lattice:

- **Delayable** - executable up to *x* slots later. Inter-slot flexibility: the time axis of sec. 6.
- **Quantum-indifferent** - content to be placed at a later quantum within the same slot. Intra-slot flexibility - and precisely the axis a horizon curve cannot price (sec. 6.10). This is also exactly what event-driven demand wants, since that demand needs the earliest quanta of *this* slot.
- **Callable** - demand already scheduled for this slot that has sold the right to be interrupted. If not called, it executes normally; if called, it yields and retries.

Two properties follow. First, these are **called in merit order** - cheapest flexibility first: quantum shift, then delay, then interruption - which is ordinary economic dispatch and minimizes the cost of meeting a given reserve level. Second, the grades are compensated through **two different channels**: delayable and quantum-indifferent demand is paid *ex ante through the rate* (declared flexibility earns a lower standing rate, sec. 6), while callable demand is paid *at exercise* as a premium. Flexibility is always paid for - in the rate or in the premium - which is what makes declaring it rational.

The economically interesting part is what the protocol does and does not do. Both sides **pre-register**: buyers who will pay to preserve execution during congestion, and sellers who will yield at a stated premium. The protocol then acts as a **matching engine** between them, not as an insurer. It holds no fund, takes no position, and sets no administrative price. That matters for neutrality: an administered scarcity curve requires someone to choose the value of failed execution, which is a political act; a matched market discovers the price between consenting, pre-committed parties.

This is **demand response**, the mechanism electricity markets use for the same problem - contract interruptible capacity ex ante, call it when the system is tight - and the blockchain setting suits it unusually well. Declarations are **machine-readable**, so they can be expressed and honored programmatically; compliance is **verifiable after the fact** against realized behavior (RN-02); and the exchange converts a zero-sum congestion race into a positive-sum trade, with less value burned in the race itself. For the builder, the input to scheduling changes: instead of a single fee ranking, a **programmable set of elasticities** to solve against - a scheduling problem, not an auction.

Three economic consequences follow.

**Reserve adequacy becomes observable in advance.** Because flexibility is pre-registered per slot, the protocol can publish how much exists for each upcoming slot - a capacity-adequacy signal that no chain offers today, letting participants see a thinly covered slot before the surge arrives.

**The premium carries wrong-way risk.** A seller of interruptibility is called precisely when execution is most valuable, including to them. Rational sellers price that correlation in, so contracted flexibility will cost more than a naive "cost of waiting" estimate suggests. Cheap reserve should not be expected.

**Retry semantics determine supply depth.** Whether a called participant is guaranteed placement in the next slot, or rejoins the queue and takes its chances, changes what it is giving up - and therefore how much flexibility is offered and at what price.

*The concrete mechanism - registration, the clearing rule, exercise ordering, and enforcement - is a mechanism-design question and is developed separately, not in this note.*

## 10. An exploratory lens: execution capital and the circulation of value

*This section is deliberately exploratory and interdisciplinary. It proposes questions, not results, and flags its own limits.*

If a project's activity is financed by execution capital, then the rate at which that capital **circulates** - how often capacity is turned over into productive economic activity - is itself an economic variable. This invites a loose parallel to monetary economics. The quantity theory writes MV = PY: a money stock M circulating at velocity V supports nominal activity PY [10]. Monetary aggregates layer money by liquidity - M1 (currency and demand deposits), M2 (M1 plus savings and small time deposits), and formerly M3 (M2 plus large time deposits and institutional balances), which the Federal Reserve discontinued in 2006 as conveying nothing beyond M2 [11]. Deployed versus undeployed execution capital (sec. 4) loosely echoes money in circulation versus reserves.

The open macro question is then: **does higher-frequency execution - faster circulation of on-chain capital through exchanges, secondary markets, and high-frequency strategies - raise the efficiency and growth of the on-chain economy, or does it, past some point, generate socially wasteful competition?** The empirical and theoretical record on high-frequency trading in traditional markets is genuinely two-sided, and honesty requires stating both: some microstructure work finds HFT narrows spreads and speeds price discovery, improving liquidity; other work, including Budish et al. and follow-on arms-race quantification, finds that continuous-market *design* turns speed into rent-seeking that a batch or temporal design would dampen [7, 8, 9]. Whether adding high-frequency finance to an economy improves aggregate productivity, and how it interacts with the velocity and composition of circulating value, is not settled even off-chain - and on-chain it is essentially unstudied.

Two cautions bound the analogy. Execution capacity is not money: it is neither a unit of account nor a general store of value, and "velocity" here means the turnover of execution capacity into productive activity, not the spending of a medium of exchange. The undeployed-reserve parallel (sec. 4) is suggestive - reserves not lent out - but it is a parallel, not an identity, so M1/M2 do not literally apply. What survives the analogy, and is worth pursuing, is a single reframing: the useful target of protocol design may be the **productive circulation of execution capital** - financing more diverse and valuable projects per unit of capacity - rather than raw throughput or raw speed. TET (sec. 12) is the first attempt at a metric in that spirit.

## 11. Neutrality, fairness, and openness

The safeguards against "industrial policy by fee rule" are three:

- **Neutrality.** Equivalent *verified* temporal profiles receive equivalent treatment. The protocol differentiates only by measurable temporal characteristics, never by application identity.
- **Fairness.** Ordinary demand keeps a guaranteed minimum service; no project type is structurally excluded, and differentiation does not become exclusion.
- **Openness.** New kinds of projects can be admitted and priced without special permission - a low barrier to entry for demand types the designers did not anticipate.

These are the conditions under which differentiation *enables* diversity rather than picking winners.

## 12. What a temporal liquidity market adds up to

The pieces of this note are one argument. Stated end to end:

A scalar spot price is a filter (sec. 5). It serves demand that is one-shot, latency-tolerant, and willing to compete on price after arrival, and it excludes or drives off-chain the demand whose value is temporal - continuous low-latency streams, reserved baselines, deadline-bounded work. The exclusion is not a defect in any mechanism; it is what happens when a single number is asked to represent a multidimensional demand.

Making temporal characteristics visible removes that filter in three distinct ways, and they are additive.

- **It prices horizons** (sec. 6). A committed, predictable project pays a smooth term rate instead of volatile spot, which is what makes a long-lived project financeable at all. Nothing in a spot market lets a project buy predictability.
- **It creates a supply side** (sec. 8). Flexibility that is invisible cannot be priced, called, or paid, so it does not exist as supply and only one side of the market is built. Once it is visible, patient demand becomes a counterparty rather than a casualty - and effective capacity becomes elastic at the moment of need, without adding hardware.
- **It serves an economy that spot cannot serve** (sec. 9). Event-driven demand arrives correlated, at the earliest quanta, against bounded capacity. A tip auction rations it by burning value in a race. A two-sided market clears it by moving flexible work aside and paying for the move.

A fourth route is different in kind from the first three, and it is the only one already on the record. **It retains project types that would otherwise leave.** The three routes above concern demand that might enter; this one concerns demand that has already gone. The on-chain perpetuals and order-book project type did not stay and overpay - it left, and it left as a whole type, not as scattered firms. dYdX v4 rebuilt on a Cosmos app-chain, Hyperliquid launched its own L1, Aevo moved matching off-chain: different teams, different designs, one departure. Each paid a steep price to go - Ethereum's security, its deepest liquidity, its composability, its tooling. Rational teams pay that price only when the general market cannot provide something first-order, and what they went to get was throughput and control over ordering and timing (RN-03, RN-06 sec. 3.3). That the whole type went, and not one firm in it, is what makes this evidence about market design rather than about any company.

That generalizes into a constraint on market design, and it is the practical form of the fee-as-filter argument. **A chain holds a project type only if its market can express what that type needs.** Where the market cannot, the type does not merely pay more - it exits, and takes its liquidity, state, and composability with it. Incompleteness along the temporal axis is therefore not only a pricing inefficiency; it bounds which project types the chain's economy can contain. Each departure also fragments the ecosystem, duplicating consensus and security across sovereign silos that bridges connect but do not unify (RN-08 sec. 1).

Two honest qualifications. Exit is **multi-causal**: app-chains also want their own token economics, sequencing-fee capture, and full-stack customization, and a reasonable position holds that sovereignty is good for innovation and guards against single-point governance capture. And nothing here says consolidation is desirable in itself. The narrower claim is the defensible one: temporal and extraction control is one driver of exit, and it is the one a general chain could address **without surrendering neutrality** - which is what makes it the driver worth studying.

Each of these routes admits or holds project types the others do not. Together they are the claim in the title: **a temporal liquidity market expands the set of project types a chain can carry** - not because capacity grew, but because demand that was unpriceable became priceable, demand that was unserved became servable, and demand that had no reason to stay acquired one.

The protocol's job, read this way, is capital allocation: preserve neutrality, allocate execution capital efficiently across time, admit a diverse set of project types, and raise long-run economic productivity. Raw transaction throughput is the wrong metric for that job. **Temporal economic throughput (TET)** - value-weighted by deadline success, delay, predictability, and correct timing (RN-08) - is the right target, because it measures what the allocation is for.

This is a hypothesis and it is falsifiable in the program's usual way. If temporally-structured, project-type-scale demand proves negligible, unidentifiable, or unpriceable under neutral rules, the framing should be revised or dropped.

## 13. Follow-up research

This note sets out an economic framework. A framework of this kind generates work at other levels - a formal statement of the allocation problem, mechanism design for clearing and enforcement, empirical estimation of demand functions, and the architecture that carries it - and that work is under way in the rest of the program. The questions the formulation opens, and where each is taken up, are collected in the companion note **RN-10 Follow-up Research Questions**.

Two continuations are immediate. The **formal statement** in RN-11 sets the market block-fee-rate curve beside the dual of the allocation problem - a welfare benchmark it does *not* identify with the market curve - and asks under what conditions the two coincide; turning that into results is the program's central mathematical task. **Virtual chains** (RN-09) are the architectural counterpart of the demand-side argument made here: they are how "financing a diverse ecosystem of projects" becomes something a host chain can actually do.

## Central thesis

> A blockchain should not be viewed primarily as a transaction-processing engine. It should be viewed as an **execution-capital market** whose purpose is to **finance a diverse ecosystem of economic projects**, each with its own temporal-liquidity profile, through neutral and programmable allocation of execution capacity across blockchain time.
>
> **A market in temporal liquidity is what makes that possible.** Without it, flexibility cannot be seen, priced, called, or paid, so only one side of the market exists and the chain rations by price - which selects for a narrow band of project types and drives the rest off-chain. With it, the set of project types a chain can carry expands.
>
> **And the converse is the design constraint.** A chain holds a project type only if its market can express what that type needs. Where it cannot, the type does not pay more - it leaves and builds its own chain, as on-chain perpetuals already have. Market design therefore decides not only what a chain charges, but which project types it gets to contain.

---

## Note to reviewers

This note is circulated for comment. Feedback is welcome on anything, but these are the points where it would be most useful:

1. **Is the capital framing sound, or does it break?** Section 2 argues blockspace is better read as durable capacity-producing capital than as a perishable per-slot good. Economists may find the stock/flow treatment loose; the note would benefit from being told exactly where.
2. **Does the term structure survive contact with fixed-income theory?** Section 6 claims a *single* arbitrage-free curve differentiates inter-temporal demand, with commitment credibility as a spread, and proposes adapting HJM. Practitioners will know immediately whether the analogy holds or where it is naive - particularly sec. 6.7 (one curve, not many) and sec. 6.9 (the quantum lattice as the model's time grid).
3. **Is the fee-as-filter claim (sec. 5) too strong?** It asserts that a scalar spot fee selects which project types can exist on-chain. Counter-examples welcome - a project type that thrives on a scalar fee despite strongly temporal demand would be the useful one.
4. **Are the segments the right partition (sec. 7)?** The dividing variable is tolerance for drift between wall-clock relevance and block-time execution, made precise in RN-11 as the width of a decay function measured against a relevance target. Is that the right statistic, is a single threshold the right way to cut it, and is any important class of demand missing from the partition?
5. **The monetary lens (sec. 10)** is offered as an interdisciplinary probe rather than a result. Is the velocity-of-execution-capital question worth pursuing, and who else is working on it?
6. **Is the formal statement (RN-11) the right abstraction?** It claims the parts of this note are facets of a single allocation problem whose dual is a welfare benchmark on the value of capacity over time, set beside the market block-fee-rate curve rather than identified with it. Is that formulation correct and well-posed; is the duality argument sound; and is this the right central problem for the program, or is there a better one?
7. **What is missing?** The note tries to state its own limits (sec. 6.10), but gaps it has not noticed are the most valuable thing a reader can supply.

**Division of labour.** This note is the *why*: the economic case for execution-capital markets. The formal problem they solve is **RN-11**. The *how* - registration, clearing rules, exercise ordering, and enforcement - is the subject of companion mechanism notes, and is out of scope here by design. The questions this formulation opens at every level, and where each is taken up, are collected in **RN-10 Follow-up Research Questions**.

## References (prior art)

**TLM program**

[1] TLM Research Notes RN-01 through RN-09, and the Vision Statement.

**Capacity, reservation, and time-differentiated pricing**

[2] Boiteux, M. "Peak-Load Pricing." *Journal of Business*, 1960; Steiner, P. O. "Peak Loads and Efficient Pricing." *QJE*, 1957.

[3] Cloud reserved vs on-demand/spot instances (e.g. AWS EC2 spot markets) - industry practice in time-differentiated compute pricing.

[4] Airline revenue / yield management: Littlewood (1972); Belobaba (1987) - selling the same capacity at differentiated terms by demand type.

[5] Braden, Clark & Shenker. *Integrated Services in the Internet Architecture (IntServ).* RFC 1633, 1994 - reservation of network capacity (QoS).

**Fee-market and market design**

[6] Buterin et al. *EIP-1559: Fee Market Change for ETH 1.0 Chain,* 2019.

[7] Budish, E., Cramton, P. & Shim, J. "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response." *Quarterly Journal of Economics* 130(4), 2015, 1547-1621.

[8] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM*, 2024. Kiayias, Koutsoupias, Lazos & Panagiotakos, *Tiered Mechanisms for Blockchain Transaction Fees,* 2023. Capponi & Zhu, *Auctioning Time to Mitigate Latency Races,* 2026.

**Microstructure, liquidity, and the cost of time**

[9] Kyle, A. S. "Continuous Auctions and Insider Trading." *Econometrica*, 1985. Zhao, Y. *The Cost of Delay,* SSRN 4436697.

**Monetary economics (for the exploratory lens in sec. 10)**

[10] Fisher, I. *The Purchasing Power of Money,* 1911 (quantity theory, MV = PT); Friedman, M. on velocity and monetary aggregates.

[11] Federal Reserve, monetary aggregates M1/M2; *Discontinuance of M3* (H.6 release, March 23, 2006).

**Time value / term structure of interest rates (for sec. 6)**

[12] Heath, D., Jarrow, R. & Morton, A. "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." *Econometrica* 60(1), 1992, 77-105. (HJM: no-arbitrage dynamics of the whole forward-rate curve.)

[13] Vasicek, O. "An Equilibrium Characterization of the Term Structure." *Journal of Financial Economics* 5, 1977, 177-188; Cox, J., Ingersoll, J. & Ross, S. "A Theory of the Term Structure of Interest Rates." *Econometrica* 53, 1985, 385-407. (Mean-reverting short-rate models.)

[14] Standard fixed-income references on the term structure, forward and swap rates, and credit spreads (e.g. Hull, *Options, Futures, and Other Derivatives*).

[15] No-arbitrage foundations: Harrison, J. M. & Kreps, D. "Martingales and Arbitrage in Multiperiod Securities Markets." *Journal of Economic Theory* 20, 1979; Harrison, J. M. & Pliska, S. R. (1981). (Fundamental theorem of asset pricing: no arbitrage iff an equivalent martingale measure exists.) Defaultable / multi-class term structure: Jarrow, R. & Turnbull, S. (1995); Duffie, D. & Singleton, K. (1999).

[16] Equity closing auctions: NYSE, *Opening and Closing Auctions* fact sheet and Closing Auction data insights (regulatory closing imbalance published from 3:50 p.m., updated every second; offsetting MOC/LOC and Closing IO orders); Nasdaq closing cross. Volume figures: US closing auctions ~$50-55bn/day and ~9% of notional in 2024, up from ~3% in 2010, ~20% on rebalance and expiration days.

**Liquidity as immediacy: the parent construction (sec. 8.1, sec. 8.8)**

[17] Demsetz, H. "The Cost of Transacting." *Quarterly Journal of Economics* 82(1), 1968, 33-53. (Immediacy is costly to supply; suppliers are compensated by demanders of immediacy.) Grossman, S. J. & Miller, M. H. "Liquidity and Market Structure." *Journal of Finance* 43(3), 1988, 617-633. (Liquidity as the equilibrium of supply of and demand for immediacy.) Foucault, T., Kadan, O. & Kandel, E. "Limit Order Book as a Market for Liquidity." *Review of Financial Studies* 18(4), 2005, 1171-1217. (Patient traders post limit orders and supply liquidity; impatient traders take it - sorting by patience.)

**Forward pricing of execution (sec. 6.2, sec. 8.5)**

[18] Proposer-commitment and preconfirmation markets, in which validators sell rights to blockspace they are entitled to produce (e.g. ETHGas, which quotes commitments up to 64 slots ahead; Commit-Boost and BOLT as validator-side infrastructure). Meister, B. K. & Price, H. C. W. *Gas Fees on the Ethereum Blockchain: From Foundations to Derivatives Valuations,* arXiv:2406.06524, 2024 (gas price as a fractional Ornstein-Uhlenbeck process; valuation of forwards and options over it).

**Patient and deferrable demand on chains (sec. 8.8)**

[19] Penna, P. & Schneider, M. *Serial Monopoly on Blockchains with Quasi-patient Users,* arXiv:2405.17334, 2024 / *Financial Cryptography* 2025 (a fraction delta of pending transactions persists to the next round; impatient and patient users as the limiting cases). Aldridge, I., Annaeva, G., Beriker, L. & Cai, Z. *On-chain Peak Shaving,* arXiv:2604.19956, 2026 (transaction-level evidence, N = 62,142, that firms shift work toward low-congestion windows; a measured peak-hour premium). Zhang, L. & Zhang, F. *Understand Waiting Time in Transaction Fee Mechanism: An Interdisciplinary Perspective,* arXiv:2305.02552, 2023.

**The other sense of "two-sided" (sec. 8.8)**

[20] Bahrani, M. & Durvasula, N. *Resonance: Transaction Fees for Heterogeneous Computation,* arXiv:2411.11789, 2024 - a two-sided transaction-fee mechanism in the *users versus executing nodes* sense, with heterogeneous user valuations and heterogeneous node costs. Distinguished in sec. 8.8 from the within-demand two-sidedness developed here.

*Note: sec. 10 (monetary / high-frequency-finance lens) is exploratory and interdisciplinary; its claims are posed as open questions, and its analogy is bounded by the disanalogies stated in the text.*

---
