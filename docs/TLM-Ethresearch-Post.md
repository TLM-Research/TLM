# Temporal Liquidity: heterogeneous demand and Ethereum's single execution lane

First post from the Temporal Liquidity Market (TLM) research program.

---

## A structural mismatch

A transaction can execute in this slot or a later slot, and its economic value may vary for each temporal choice. Even within the same block, it may be executed in the earlier part or the later part, with a different economic outcome. The economic value of a transaction depends on the temporal choice of its execution.

A liquidation's value falls sharply within a slot or two. A treasury settlement holds steady for hours, then drops to zero at a cutoff. An oracle update depends on how long it has been since the last one.

Transaction types differ in the shape of value against execution time. Ethereum's protocol represents none of it. Execution is one homogeneous lane, one stream per 12-second slot, and the only signal a transaction can send about time is a scalar fee.

So the question:

> How can a network with no protocol-level mechanism for temporal differentiation, one lane per slot priced by fee alone, deliver appropriate service to transactions whose temporal requirements differ this much?

We don't think it can, and the shortfall is usually read as a capacity problem instead.

Ethereum offers one service: inclusion as soon as your fee allows. A transaction that could wait has no slower, cheaper option with a deadline attached. It either bids as though it were urgent, or bids low and accepts an open-ended wait. Urgent transactions then have to outbid patient ones that are bidding like urgent ones. Nothing in the fee tells the protocol which is which.

Two things follow, and neither is a shortage of blockspace.

Some demand is excluded rather than delayed. A transaction whose value decays slowly could be worth executing later at a lower price, but with no way to say so it must pay the current price or not transact at all. It drops out. That is suppressed demand, and it never registers in the fee market as demand, because demand that cannot be expressed is invisible to the mechanism meant to price it.

And the fee market's only control is the base fee, adjusted after each block according to how full the last one was. That adjustment rule reacts to congestion which has already happened, with no forward information about what is coming. Under bursty demand it can oscillate and converge slowly.

## Two transactions the protocol cannot tell apart

Two transactions arrive in the same slot with identical `maxFeePerGas` and `maxPriorityFeePerGas`.

- **A** is a liquidation. High value now, roughly half by the next slot, near zero within a minute. Sensitive to position within the slot.
- **B** is a treasury settlement. Flat for several hundred slots, then zero at a cutoff. Indifferent to intra-slot position.

These two messages are indistinguishable. The builder sees the same bid and treats them the same way. Any outcome that serves one serves the other by accident. Include both immediately and B has paid for urgency it does not need, consuming capacity A was competing for. Delay both and A is destroyed while B is unaffected.

Neither can send a message to fix this. The protocol has no vocabulary for the statement, and no differentiated service that such a statement would select.

## Supply side: exposing temporal structure

Ethereum exposes one temporal object to a transaction: the next slot. Inclusion is in or out, and the fee market prices that binary. Serving differentiated temporal demand needs more structure than that. Three things are missing: a finer coordinate inside the slot, future slots beyond the next one, and a pricing relationship among slots.

**Within a slot.** Position within a slot carries value, as MEV makes plain, but the protocol does not expose it. Subdividing a slot into finer quanta would make position addressable rather than a matter of builder discretion. Resolution can go well below block time. Commitment and verification cost, clock uncertainty, and observability each set a floor. This is explored in a TLM research note ([RN-05](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-05_Supply-side_Heterogeneity_and_Temporal_Granularity.md)).

[Mini-blocks](https://ethresear.ch/t/mini-blocks-ssv-backed-sub-slot-auctions-for-ethereum-pbs/24898) reaches something adjacent from the supply side: several auction rounds per slot, cleared by a distributed-validator cluster. Its motivation is that block value concentrates in the first few transactions while the rest of the block settles into a quieter regime. That observation is evidence for the same heterogeneity described here, arrived at from the extraction side rather than the demand side.

**Across slots.** The protocol prices the next slot. It offers a transaction no relationship to the slot after that, or the one a minute out. Deadlines, windows, and cadence require treating future slots as addressable. That is what would make "execute before market close" something the protocol can act on rather than a scheduling problem the application solves outside it.

**Prices that link the two.** Once future slots are addressable, the question is what they cost, and how today's fee relates to a fee at a future slot. That is a term structure, and it is what makes forward commitments and reservations coherent rather than ad hoc. This is explored in a TLM research note ([RN-11](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-11_Term_Structure_and_Allocation_of_Execution_Capital_in_TLM.md)).

Ethereum research already reaches into future slots, for a different purpose. [Execution tickets](https://ethresear.ch/t/execution-tickets/17944) and [execution auctions](https://ethresear.ch/t/execution-auctions-as-an-alternative-to-execution-tickets/19894) allocate the right to *propose* a future slot, ahead of time, among proposers and builders. [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732), the ePBS headliner for Glamsterdam, adds structure inside the slot through its payload-timeliness committee and dual deadlines. Preconfirmation designs commit to inclusion within a slot.

So the machinery for addressing slots other than the immediate next one is being built. What none of it provides is a way for a *transaction* to state a temporal requirement, or a service to buy against that statement. These proposals organize the supply side among its own participants.

The supply side has to expose temporal structure before the demand side has anything to select.

## Evidence: three forms of the same gap

The cost of the missing mechanism is being paid today, three different ways.

### Paid in place: the liquidation gas race

Aave liquidations run on Ethereum mainnet and are time-critical. Liquidators monitor positions continuously, react to oracle price movements, and submit with high priority to be first. There is no way to state *this must execute before the position deteriorates*, so the only instrument available is a larger bid. Liquidators bid gas against one another, and Aave's own documentation notes that under congestion a bot can overpay to the point where the liquidation is no longer profitable.

What is being bought there is not capacity but position. That is a temporal service, sold through the only channel the protocol offers, priced by an auction that cannot distinguish urgency from willingness to spend. The demand is real, it is on Ethereum today, and the cost of expressing it badly is paid per transaction by everyone in the race.

### Paid by leaving: dYdX

dYdX moved off Ethereum to its own chain, and the reason it gave was temporal. A decentralized order book needs order placement and cancellation at a latency that, in its assessment, neither Ethereum L1 nor Ethereum L2s could provide. The L2 rejection matters here: the constraint was not fees or throughput alone, and more blockspace would not have answered it.

Other factors were present, including sovereignty, product control, and token economics. But the stated reason is one Ethereum's execution interface cannot address. Not "we need more capacity" but "we need a different relationship to time."

An exit costs more than the application. Liquidity that leaves stops being composable with what remains: assets are bridged rather than held, order flow splits across venues, and the same capital backs less activity. Ethereum loses the fee revenue and the depth, and the destination gains both. Fragmentation is the cost of serving temporal demand one chain at a time.

### Built elsewhere: HyperEVM

A production general-purpose EVM Layer-1 has already exposed temporal structure at protocol level, in a limited form. [RN-03](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-03_Hyperliquid_A_Case_Study_in_Temporal_Liquidity.md) treats the case in full, with sources.

HyperEVM maintains one EVM state but schedules two kinds of block. **Small blocks** are produced roughly every second at a low gas limit (about 2M gas as documented), serving latency-sensitive traffic. **Large blocks** are produced roughly once a minute at a high gas limit (about 30M gas), serving contract deployment, migrations, and heavy or large-atomic work. The two draw from separate mempools and expose separate base fees, two independent congestion signals, yet interleave into one increasing block sequence over shared state under one consensus. One chain, not two. (Cadences and limits are documented values, subject to change.)

> HyperEVM introduces protocol-native temporal differentiation by allowing transactions to select between execution lanes with different latency and atomic-capacity profiles.

Three things make this relevant to Ethereum.

It is **chain-level, not application-level**. HyperEVM is a general-purpose chain competing for ordinary smart-contract activity, so it compares directly to Ethereum's single execution lane rather than to an exchange's internal matching rule. (Hyperliquid's HyperCore order book also prioritizes by price and time, but that is an application's internal rule, not the chain's.)

**Temporal classes are priced separately.** Two base fees over shared physical capacity is a market structure, not a scheduling convenience. Temporal service is priced as its own thing rather than folded into one number.

**A live chain found it worth operating.** Demand for differentiated temporal service was sufficient to justify building and running the mechanism.

HyperEVM's version is limited in two ways. It is **coarse**: two predefined classes rather than a stated preference, so a transaction cannot say "within 2s at price X, within 60s at price Y," nor give an arbitrary deadline. And the dimensions are **coupled**: the fast lane bundles low latency with low atomic capacity, the slow lane the reverse, so choosing a lane chooses both. Distinct temporal characteristics collapse back into one knob.

Protocol-level temporal differentiation works on a general-purpose EVM chain. Whether it can be done finely, neutrally, and without the coupling is what we think is worth working on.

Which is where the goal of this work sits. We want to widen the set of applications Ethereum can host on its own base layer, so that time-sensitive work has a reason to stay rather than leaving for a sovereign chain, and so that liquidity is not split across chains as a side effect of an interface limitation. Every exit costs the applications that remain, through thinner liquidity and lost composability, and costs the departing application Ethereum's security and settlement. A temporal market is one route to making that trade unnecessary.

## Demand side: identifying a transaction's temporal type

Given exposed structure, a transaction needs a way to say which part of it applies. That is where **temporal liquidity** comes in.

We use the term for the economically meaningful temporal characteristics execution demand carries, and the flexibility they define. The dimensions:

- **execution priority**, sensitivity to ordering within a slot
- **delay tolerance**, how value varies with waiting
- **execution windows and deadlines**, when execution stops being valuable
- **predictability**, forecastability of demand
- **continuity**, whether demand is sustained or one-off

These are independent. A transaction can be priority-sensitive but deadline-loose, or deadline-bound and indifferent to intra-slot position. A stream can be predictable in aggregate while each transaction in it is urgent. That last independence is one reason a single scalar cannot stand in for the set.

Two representations, at different granularities.

**Temporal Execution Profile (TEP)** ([RN-01](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-01_Temporal_Execution_Profile.md)), transaction-level, chiefly declared preference. Returning to A and B: A would identify as priority-sensitive with steep decay over a short window, B as position-indifferent with a hard deadline several hundred slots out. Under today's interface both send the same message. As an illustration, not a proposal, a TEP might carry:

```text
eligibility / commitment certificate   when the transaction becomes admissible
resource-demand vector                 what it consumes
admissible execution set or deadline   where in block time it may land
value over a small set of outcomes     what each landing is worth to it
expiry, cancellation, fallback         what happens if none is available
```

**Temporal Stream Profile (TSP)** ([RN-02](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-02_Protocol_Visible_Temporal_Abstraction.md)), stream-level, chiefly observed property. Some demand is a flow rather than a single transaction: an oracle updating on a cadence, a rollup posting batches. What describes such demand is the statistics of the stream, its average rate and cadence, the jitter around that cadence, its burstiness, how persistent it is, and how well it can be forecast. These are properties of the sequence, not of the transactions in it. A single transaction has no rate or cadence, so no TEP can express them however it is designed. That is why the stream level needs a representation of its own.

At this stage both are conceptual. Their fields and encoding would be defined along with the mechanism that consumes them, rather than fixed in advance.

Two kinds of time are in play here. Applications state what they need in **physical time**: market closes, reporting cycles, the moment a price goes stale. The chain executes in **blockchain time**: an ordered sequence of slots and positions within them. A temporal profile has to carry the mapping between the two, since a requirement expressed in one must be served in the other.

## Two design points

**Protocol-visible is not publicly revealed.** A deadline or urgency field exposes trading intent, and a profile visible in a public mempool before ordering can be priced against or front-run. When a field becomes visible is a design choice that governs extraction: committed and hidden, builder-visible, consensus-certified, or revealed only after sequencing. Information reaching the scheduler and information reaching strategic observers are different things, and they can be separated.

**Pricing, not policing, makes a declaration credible.** The reflex is that declared preferences invite false urgency and therefore need verification. We think that overreaches. If each temporal class is charged at its prevailing market-clearing rate, selecting the urgent class means paying the urgent rate, so false urgency is self-limiting rather than a manipulation to detect. Private value is not verifiable in any case: a missed deadline is observable, the counterfactual value of a different execution time is not. It also means the classes stay open without a reputation or identity system, so a new participant is not disadvantaged for lacking a history.

## What comes next

Mechanism design comes later. These are the questions the program starts with.

**Throughput and execution.** One thing this is not: a way to raise sustained throughput. The base fee is a controller targeting a fixed gas usage, so any lasting increase is choked back to the target. What a temporal interface changes is which transactions occupy that target and what the peak costs, not how much gets through. Beyond the fee level, temporal structure is scheduling information. Knowing which transactions can be deferred, which must stay adjacent, and which are independent is much of what an execution engine needs in order to run work in parallel, and Monad, Aptos and HyperCore each show what becomes available when a chain treats execution scheduling as a design problem rather than a given. Whether temporal profiles can feed that kind of engine, and what that does to throughput, is a direction we want to pursue ([RN-06](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-06_Monad_A_Temporal-Liquidity_Analysis.md)).

**Which applications it brings back.** Some that left did so for temporal reasons and could return if Ethereum offered the service they needed. Others left for sovereignty, product control, or token economics. Separating the two tells us how much is actually recoverable.

**How it fits the existing fee market.** EIP-1559, ePBS, execution tickets, and slot auctions improve allocation, and this builds on them rather than replacing them. Temporal classes would interact with the base fee and with proposer and builder incentives, so part of the work is understanding those interactions and what they imply for the mechanisms already in place.

**The mechanism itself.** The supply-side structure and the demand-side profile fields are both still to be designed. Every class added costs disclosure, extraction surface, and protocol complexity, so the question is what the smallest useful set is rather than how much differentiation is possible.

The measurements that would settle these: deadline-success rates, waiting-time distributions, fee spend, utilization, effects on non-participants, extraction, and computational cost.

## Conclusion

Ethereum's execution interface says almost nothing about time beyond a price for the next slot. The cost of that shows up on the chain as gas races, and off it as applications that build somewhere else. The aim of this work is to close that gap, so that the base layer can host the timing-sensitive part of the ecosystem rather than exporting it.

Making temporal structure protocol-visible touches the fee market, block building, extraction, and the roadmap work already under way. It opens more questions than one program can work through, and many of them will be better answered by people closer to those areas.

The work so far is a set of research notes, a Vision Statement, and a Foundation Statement, all in the repository below. They set out the problem as we currently frame it and mark what is still open. The notes referenced above are [RN-01](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-01_Temporal_Execution_Profile.md) (temporal execution profiles), [RN-02](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-02_Protocol_Visible_Temporal_Abstraction.md) (protocol-visible temporal abstraction), [RN-03](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-03_Hyperliquid_A_Case_Study_in_Temporal_Liquidity.md) (the Hyperliquid and HyperEVM case), [RN-05](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-05_Supply-side_Heterogeneity_and_Temporal_Granularity.md) (supply-side granularity), [RN-06](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-06_Monad_A_Temporal-Liquidity_Analysis.md) (Monad and parallel execution), and [RN-11](https://github.com/TLM-Research/TLM/blob/main/docs/Research-Notes/RN-11_Term_Structure_and_Allocation_of_Execution_Capital_in_TLM.md) (term structure and allocation).

**https://github.com/TLM-Research/TLM**

We are looking for comments and for collaborators on the program.
