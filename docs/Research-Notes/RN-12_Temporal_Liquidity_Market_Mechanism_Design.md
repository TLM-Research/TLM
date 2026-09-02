---
id: RN-12
title: "The Temporal Liquidity Market: A Conceptual Mechanism Design"
subtitle: "Trading temporal position against a neutral baseline"
version: "2.2"
status: "Public draft. A candidate mechanism for the problem RN-11 states; proposed, not adopted."
program: "Temporal Liquidity Market (TLM)"
date: "August 31, 2026"
---

# RN-12 -- The Temporal Liquidity Market: A Conceptual Mechanism Design

## Abstract

RN-11 states the allocation problem and builds no mechanism. This note proposes one, at two horizons.

**Within a slot.** Patient demand sells execution position to urgent demand. Both clear at a uniform price against a FIFO baseline, taken from the protocol's commitment order rather than physical arrival. Two results make this work. The quantum is a unit of logical time, so inter-quantum position is sellable while transactions inside a quantum are concurrent and their order is not. And advancement is conserved: none moves earlier except against a willing supplier who moves later, which separates priced priority from front-running.

**Across slots.** The same market prices a term, as an interest-rate swap. A user pays a fixed rate and receives the floating clearing price for a stated number of slots, so its cost is known whatever the market does, and the fixed rates across maturities are the term structure. No capacity changes hands, only price risk.

Separating the roles the builder now holds sends the value to whoever supplies the flexibility.

One limit binds all of it. Temporal liquidity trades only at the resolution at which consensus records commitments. Finer than that, the baseline invents the order it claims to enforce.

## 0. What this note assumes

This note proposes a conceptual mechanism, guided by RN-11. It takes the quantum lattice, the reducibility constraint that makes an allocation checkable, and the demand representation as given.

Proposing a mechanism means taking positions RN-11 was careful not to take. Read its rules as candidates to be tested (RN-11 sec. 9, the simulation stack), not as settled protocol.

## 0.1 The market this note describes

**Temporal liquidity is what one side of the market has and the other needs.** A transaction whose value survives being executed a little later carries flexibility about when it runs. A transaction whose value decays quickly, or which must land before a price moves, does not, and needs someone else's. Section 9 makes the quantity precise: a transaction's tradable window is the set of quanta its execution may be reassigned to, bounded below by when it became eligible and above by its deadline. A wide window is temporal liquidity to supply. A window one quantum wide is none, and that transaction can only buy.

**No chain has a temporal liquidity market in it, for the reasons below.**

- **Neither side can say what it has.** The fee says how much a sender will pay. It does not say when the sender needs to run, or how much later the sender could run without minding.
- **There is nowhere for the two sides to meet.** No chain has a place where a transaction that needs to be early and a transaction that would take a later position can trade with each other.
- **The trade happens anyway, without them.** Someone has to put transactions in an order, so positions are reallocated in every block. Whoever assembles the block does it, prices it privately, and keeps the proceeds. The transaction that ends up later is not asked and is not paid.

This is not a defect of one chain. Every chain that orders transactions has it, because ordering is valuable and someone has to do it.

**A market needs four things, and the rest of this note builds them.**

- Two sides that can state their positions (sec. 5).
- A baseline they trade against, so displacement is measurable (sec. 7).
- A crossing where they meet at one price (sec. 8).
- A conservation rule, so advancement is always someone else's deferral (sec. 9).

The price the crossing produces is what RN-11 derives as the dual of the allocation problem, and the rates across terms (sec. 4) are its curve.

**It is conceptual, and nothing here could be written as a specification.** It names roles, instruments and rules; it does not fix parameters, encodings, transaction formats, or activation paths. Where a specification would state a number, this note states which property the number has to have.

## 0.2 The chains it applies to

**Ethereum** is the primary target: one sequential execution lane, twelve-second slots, and proposer-builder separation, which is the most documented case of a single party both deciding order and capturing its value. Section 1 argues against that arrangement, and cites enshrined PBS as evidence that protocol-level builder commitments are constructible rather than hopeful.

**Monad** shows that faster execution does not supply the market. RN-06 finds that Monad rebuilds every layer below the market and leaves the demand side as it was, with a control plane that computes an order and a scalar fee and nothing else. Four-hundred-millisecond blocks make timing more decisive, so the market matters more rather than less. And optimistic parallel execution discovers conflicts only after ordering, so it cannot remove the conflicts of an undifferentiated stream. That makes temporal classification a scaling lever and not only an economic one.

**Aptos** is the same gap under a different executor, with Block-STM and Move's typed state making conflict structure more legible on the supply side and changing nothing about what a transaction can say.

**HyperEVM** matters most, because it already runs protocol-native temporal differentiation: small blocks roughly every second at about 2M gas and large blocks roughly every minute at about 30M gas, from separate mempools with separate base fees over one shared state (RN-03 sec. 6.2). It proves a general-purpose chain can price temporal classes separately. It is also what this note is not proposing: two predefined classes rather than a declared window, chosen per account rather than per transaction, with latency coupled to atomic capacity, and priced by two separate fee markets rather than by the classes clearing against each other. The gap between that and a market is short, and it is this note's subject.

**Instantiating it, on any chain.** The architecture does not have to be adopted whole, and three levels of compatibility present themselves anywhere it is tried: a declaration inside the transaction format as it stands, one new piece of protocol state, or the fuller separation of roles once forward commitments and builder attestation exist. Backward compatibility binds hardest at the first and less at each level after. Where a chain can start depends on how fixed its fee market and tooling already are, so a chain carrying less deployed history may begin higher than Ethereum can, and HyperEVM has arguably begun already. Separate notes work out the Ethereum case; a reader elsewhere should decide which level their own chain is at.

## 1. Today's builder is not a neutral seller

Under proposer-builder separation, a builder constructs an execution payload and bids for the right to have a proposer include it; the proposer takes the most valuable bid. Builders also receive private order flow that others cannot see. So a single party is at once the block assembler, the buyer of the proposal opportunity, the reseller of execution access, a dealer trading on private order flow, and the MEV optimizer. That is not a neutral market operator; it is a vertically integrated dealer with an information advantage -- the microstructure arrangement that regulated venues separate by rule, because a matching engine that also trades on its own account against its customers' flow will.

The trend in Ethereum's own roadmap is toward constraining this. Enshrined proposer-builder separation (EIP-7732) replaces the proposer's execution payload with a signed builder commitment to reveal a payload later, and adds a payload-timeliness committee of validators that attests whether the builder revealed the committed payload on time [3]. That shows protocol-level builder commitments and their verification are workable design objects. This note takes the separation further, to the ordering itself.

## 2. Separating three roles

The mechanism rests on splitting the builder's bundle into three:

```text
Protocol                 issues and defines execution rights; sets the feasible region and the reserve
Temporal-liquidity       matches buyers and sellers of timing flexibility; clears at a public price
  exchange
Builder                  constructs a schedule compliant with the cleared assignment; may optimize
                         only inside the protocol-defined feasible set
```

The builder does not disappear and does not stop optimizing. It loses one thing: discretion over inter-quantum placement and the private surplus that discretion earns. What was an opaque reordering becomes a public clearing, and the payment that today the builder internalizes is redirected to the participants who actually provide the flexibility (sec. 8). The rest of the note specifies the exchange and the residual builder role.

## 3. Tradable future execution rights

Across slots, the instrument that makes RN-11's term structure real is a transferable claim on future execution. Define a right

```text
R = ( t1, t2, C, Gamma )
```

with [t1, t2] an execution window, C a capacity entitlement, and Gamma the service conditions: priority class, state-access restrictions, exercise rules. The holder may consume it, transfer it, subdivide it, resell it before expiry, let it expire, or post it as collateral. This is the zero-coupon instrument of RN-11 sec. 2 given an owner and a secondary market, and it is close to the execution-ticket and preconfirmation proposals already in the literature [2].

**Transferability is not automatically fair.** Execution tickets concentrate among holders with the highest MEV-extraction ability and the lowest cost of capital, so a capital-advantaged party that is not even a builder can come to dominate [4]. But the finding cuts both ways: a secondary market can *reduce* concentration by letting specialists buy just-in-time rather than pre-committing capital [5]. Resale is a design surface with a Goldilocks zone [4], not a free good. It should be facilitated, with concentration bounded by explicit means such as caps, forfeiture or decay.

**These rights live in consensus state, not the mempool.** A right is durable, transferable and ownership-bearing, and the commitment order that anchors it must be forge-proof (sec. 7), so it cannot sit in a transient, node-local, untrusted mempool. It belongs in a reservation registry, the layer where token balances live, where a cleared trade is a state transition that reassigns an entry. Two consequences follow. Every outstanding reservation is protocol state, so rights should carry expiry and the registry must be priced against that cost. And the alternative, holding positions off-chain as bonded commitments settled on-chain only in dispute [2], is lighter on state but reintroduces the semi-trusted sequencer whose concentration this section warns about. Where a design lands on that tradeoff decides how much of the market is actually enshrined.

## 4. Term instruments: fixing the price of execution over X slots

Section 3 defines a right to *capacity* at a future time. The instrument a recurring user actually wants is narrower and safer: not ownership of future capacity, but a fixed price for it.

**The swap.** A user with a per-slot execution requirement faces a floating cost: whatever temporal liquidity clears at, slot by slot, for the next X slots. A term instrument replaces that with a single rate `f_X` agreed now:

```text
each slot t in [t0, t0 + X):
    floating leg   p*_t          the cleared price of temporal liquidity in slot t
    fixed leg      f_X           agreed at t0, constant over the term
    net to payer of fixed        p*_t - f_X
```

The user pays fixed and receives floating, so its realised cost is `f_X` per slot whatever `p*` does. This is an interest-rate swap with the cleared temporal-liquidity price as the floating leg. There is no principal and no capacity is delivered: the two parties exchange payments on a notional, and what the user has bought is certainty about cost rather than a claim on execution.

**Why a swap rather than a forward purchase of capacity.** Nothing is reserved: capacity is still allocated by the clear of sec. 8 in every slot, and the swap holder competes in it like anyone else, where a lease takes capacity out of the market before the market runs. Nothing is privatised either, since what changes hands is price risk rather than the resource, so the concentration argument of sec. 3 barely applies: acquiring every swap on the market would leave the holder with a large exposure to the price of time and no ability to execute earlier than anyone else. It is also cheaper in state, being one contract with a rate, a term and two parties rather than a set of reserved quanta. And the two sides are already in the room. A consumer pays the floating clearing price every slot and would rather pay a known rate, so it pays fixed and receives floating. A supplier receives that floating price every slot and would rather receive a known rate, so it receives fixed and pays floating. The exposures are opposite, either side may quote first, and the two camps of sec. 5 are the two legs of the swap, so no dealer has to stand between them.

**The set of fixed rates is the term structure.** A one-slot rate, a ten-slot rate and a thousand-slot rate are different numbers, and the curve they trace is exactly the object RN-11 sec. 2 derives as the dual of the allocation problem. This matters because it gives the curve a construction rather than only a definition: real interest-rate curves are bootstrapped from traded swap rates, and the same procedure applies here. RN-11's curve is what the mechanism should reproduce; the swap rates are how it would be observed.

**The perpetual is the no-maturity limit, not a separate idea.** A swap with no fixed end, settled periodically against the floating rate and closed when either side chooses, is the natural form for a stream whose horizon is not known in advance. It is a perpetual in the sense the derivatives market uses the word, a continuously settled position, and not in the sense of a permanent entitlement.

**Why not sell capacity forward instead.** The obvious designs all transfer the resource rather than the price, and each is worse for the same reason. A non-expiring ticket never clears off the registry, which is the worst case for the state cost of sec. 3. A rolling lease removes capacity from the market in every slot it covers. A perpetual share of a capacity pool is a permanent tradable claim on a scarce public resource, with the rentier dynamics of a spectrum licence and the concentration problem of RN-11 sec. 8 migrated into ownership. If capacity is sold forward at all, it should be by renewable lease rather than irrevocable right, so the protocol keeps the ability to reprice or let a claim decay.

## 5. The two camps as bid and ask

RN-10's two camps become the two sides of an order book in temporal position.

**Suppliers of temporal liquidity** are transactions or streams that can move later. Each declares a maximum delay, an acceptable quantum range, a deadline, an interruption right, and a required compensation, and submits an ask

```text
a_i( dt ) = minimum compensation to accept a delay of dt quanta.
```

**Buyers** want to move earlier than their default FIFO position. Each declares a desired advancement, a deadline, a maximum premium, an acceptable quantum, and execution conditions, and submits a bid

```text
b_j( dt ) = maximum payment for an advancement of dt quanta.
```

A trade is feasible when a buyer's bid covers a supplier's ask for the same displacement,

```text
b_j( dt )  >=  a_i( dt ),
```

and it moves buyer j earlier and supplier i later with per-quantum capacity preserved. The buyer's payment finances the supplier's compensation, with any protocol-defined portion burned or retained as a scarcity charge (sec. 8). That is the ask and bid of an exchange, with the supplier in the liquidity-provider role priced by a spread [14], and it generalises a single auctioned priority lane such as Timeboost [7] into a compensated, FIFO-anchored, two-sided clear.

**What sets the side is drift tolerance, not the slope of value.** Value is measured against a target tau (RN-11 sec. 5), and for target-bound work executing early is as costly as late, so a monotone value-against-delay curve is the wrong object. What discriminates is how much drift between wall-clock relevance and block execution, T_wall - T_block, a transaction's value tolerates: its size, which is RN-11's binding-tightness width W(alpha), and its variance, which is predictability. Those are two axes RN-11 already names, and unlike a private value slope the drift is something the mechanism can observe.

- A **buyer** needs small drift with small variance. A liquidation must land in a narrow window around a price event, an oracle update near the event it reports, ADL is safety-critical. None tolerates a wide or jittery landing, so each buys a guarantee of position.
- A **supplier** tolerates large drift, large variance, or both: a batch posting, an overnight payment, background computation, governance, whose value is nearly flat across a wide window. It sells that tolerance.

The slope re-enters only for the size of the order, not the side: how much either party pays scales with the value at stake once drift leaves the tolerable band. And the side is a property of the transaction rather than the sender, so one project supplies from its jitter-tolerant order-book updates and buys for its liquidations, with the protocol seeing only the declared tolerance. This gives a chain-independent definition:

> **The temporal liquidity of an execution request is the range of drift T_wall - T_block its value tolerates, the width of the reassignment window and the variance admissible within it, before utility falls below the declared threshold.**

**Self-selection does the work of elicitation.** The mechanism never asks a transaction to declare its decay function phi. It asks only whether the transaction will pay to advance or accept payment to defer, and a and b reveal which side of the partition it is on. Willingness to pay substitutes for declaration, which is where transaction-fee mechanisms stand on firmer ground against the elicitation impossibilities [15].

## 6. The quantum is logical time; causality is commitment time

The mechanism prices *when* a transaction executes, so it needs a "when" a decentralized system can agree on. Physical wall-clock time is not it: nodes are geo-distributed, clocks skew, and message delays are asymmetric and manipulable, so there is no global physical clock and no agreed physical order of arrivals. What a distributed system can establish is *logical* time, Lamport's happens-before order [16].

**Most pending transactions are concurrent.** Happens-before is a partial order: a -> b holds when a causally precedes b, and two events with no such chain are concurrent. Pending transactions send no messages to each other, so the mempool is very nearly one large antichain. There is no ground-truth total order among them to discover, and any total order a builder imposes is a convention rather than a fact, which is why fine-grained reordering can extract value corresponding to nothing real.

**The quantum is a logical-time tick.** Read RN-05's quantum as one level of a logical clock:

> **Inter-quantum order establishes a real, consensus-agreed execution order in logical time. Intra-quantum there is no order to establish, because the transactions are concurrent.**

That is what makes inter-quantum position sellable and intra-quantum position not.

**Commitment time is a logical timestamp.** The binding commitment time t^c is the transaction's position in the commitment order consensus records: the instant it first acquires the right to compete. Call it the transaction's **temporal entitlement time**, protocol-defined so that no party, least of all a builder timestamping its own receipts, can set it. That entitlement is what the rest of the note trades, whether retained (FIFO), sold, bought or reserved. Three events matter:

```text
t^c   binding commitment   (the transaction's logical timestamp; consensus holds a commitment)
t^r   revelation           (the payload is publicly revealed)
t^e   execution
```

The constraint is t^e >= t^c, normally with t^c <= t^r <= t^e. Ordering execution before revelation, t^e < t^r, is admissible and useful, because it stops advancement from leaking forward information; commit-reveal, threshold encryption [11] and timed commitments [12] let a transaction hold its logical position while its contents stay hidden. Pre-trade privacy shifts rents rather than abolishing them [13], and a forward commitment handled naively leaks block information [2]. Execution before commitment, t^e < t^c, is never admissible: it places a transaction in the order before consensus holds anything to it.

**What this fixes for the rest of the note.** FIFO is FIFO in logical time (sec. 7), never physical arrival, and advancement means moving ahead of logically-earlier commitments, bounded below by t^c. Intra-quantum position is not for sale, since selling it would sell an arbitrary tiebreak as though it were priority [10]. Causal dependencies are the exception to concurrency: if j reads state i writes then i -> j, they cannot share a quantum unordered, and i is forced earlier (RN-11 sec. 4). And the quantum should be no finer than the resolution at which consensus can establish a genuine order, or the protocol prices distinctions it cannot make. That bounds quantum size from below, the lever RN-05 left open.

**Three layers of time.** *Physical time* belongs to the network and is authoritative nowhere. *Protocol time* belongs to consensus and fixes the temporal entitlement time. *Economic time* belongs to TLM, where the entitlement is priced and traded. They nest: economic time maps onto protocol time, which is bounded by physical time, so the market may reassign execution only within what consensus can order, the tradable window of sec. 9 and never wider. A financial exchange collapses the first two into one gateway that stamps arrivals and makes its own sequence authoritative; a blockchain has no gateway, so consensus must be it. That settles a real design fork: a chain should not try to recover physical arrival order, it should define a protocol-native entitlement and let the economic layer trade it.

## 7. FIFO as the neutral baseline

Advancement has to be advancement relative to something, and the neutral reference is FIFO on the temporal entitlement time: FIFO in the logical commitment order of sec. 6, which is exact because that order is what consensus records. Since strong order-fairness is impossible [8], this is stated as an achievable neutrality property rather than derived from a stronger one. Let q_i^0 be the earliest quantum available to i under protocol-observed FIFO:

```text
q_i^0 = min { q : q >= q_i^commit,  C_q^remaining >= g_i }
```

Absent a trade, i sits at or after that position and may be pushed later only within its deadline d_i:

```text
q_i^0  <=  q_i  <=  d_i
```

To execute earlier, though never before its commitment eligibility, it must buy:

```text
q_i < q_i^0   requires   p_i^TL >= p_min   and a cleared match against a supplier or reserve.
```

> **FIFO establishes the initial temporal entitlement. Any advancement must be purchased from parties whose entitlement is displaced, or from explicitly reserved protocol capacity.**

That is checkable, and it is what separates priced priority from sanctioned front-running: nobody is advanced except by a trade that compensates whoever they passed, the counterparty is willing rather than displaced without consent, and the builder cannot reorder and keep the surplus (RN-11 secs. 4 and 8).

**The baseline needs a commitment order at the resolution it prices.** If consensus resolves only to the slot, so that all of a slot's commitments are concurrent (sec. 6), there is no intra-slot FIFO to anchor and the builder assigns intra-slot position freely. Neutrality at quantum resolution therefore requires the protocol to supply the finer order itself: an enshrined preconfirmation or commitment log, or a sequencer whose timestamps the builder cannot forge. Without one, intra-slot order must be left concurrent, randomised or unsold (sec. 13), and only slot-level advancement can be priced. **The resolution at which temporal liquidity can trade is bounded by the resolution at which consensus records commitments.** Price finer than that and the baseline invents the order it claims to enforce.

## 8. The crossing-price mechanism

The exchange clears as a uniform-price call auction. Collect the buyers' bids and suppliers' asks for a given displacement and sort them,

```text
b_(1) >= b_(2) >= ...          (bids, descending)
a_(1) <= a_(2) <= ...          (asks, ascending)
```

Let k be the largest index with b_(k) >= a_(k); that is the matched quantity. A uniform crossing price is any

```text
p*  in  [ a_(k) , b_(k) ] .
```

Then temporal-liquidity buyers pay p*, suppliers receive p* less any protocol charge, the builder receives only an explicit construction fee, and the ordering change is publicly verifiable. The single most important property is the separation it enforces:

```text
payment for construction        (to the builder, explicit)
payment for temporal advancement (to suppliers, via the exchange)
```

Today a builder internalises both; here they are different payments to different parties at a public price. A uniform price rather than pay-as-bid matters for the same reason it does on any exchange: everyone clears at the same marginal price, which removes the discriminatory pricing that would otherwise re-introduce the time-unfairness of RN-11 sec. 8 (property v). A protocol-defined slice of p* can be burned or retained as a scarcity charge without changing the neutrality of the clear.

In equilibrium terms, p* is the market price of temporal position. A transaction buys when the value of securing a quantum inside its required low-variance window exceeds p*, and supplies when the value it would lose from being reassigned within its tolerance falls below p*; the clear equates the value of temporal position across the market to a single price. That is the supply inequality of RN-11 sec. 5 -- supply when p(t) - p(t+k) covers the value lost by moving -- met at a cleared price rather than read off a posted curve.

## 9. Quantum-level statement and conservation

Per transaction i, let a_i be its commitment/arrival quantum, d_i its deadline, q_i^0 its FIFO quantum, q_i its final assigned quantum, g_i its gas, and let b_i, s_i be its advancement bid and delay ask. The placement must respect eligibility and deadline,

```text
a_i  <=  q_i  <=  d_i ,
```

The interval [a_i, d_i] is the transaction's **tradable window** -- bounded below by its temporal entitlement time (causality, sec. 6) and above by its deadline. Everything inside it is tradable; everything outside is inadmissible. The width of the window is the transaction's temporal liquidity: the binding-tightness width W(alpha) of RN-11 sec. 5, read as the set of quanta to which its execution may be reassigned. That set is a single sub-interval of [a_i, d_i] for single-peaked value and, for periodic or multi-window work (RN-11 sec. 5), a union of intervals within [a_i, d_i]; the mechanism reassigns position across whichever set it is. A transaction with a wide window carries much temporal liquidity to supply; one whose window is a single quantum (a_i = d_i) carries none and can only buy.

The signed displacement Delta_i = q_i - q_i^0 classifies the transaction:

```text
Delta_i > 0    supplies temporal liquidity   (moved later)
Delta_i = 0    neutral, at its FIFO position
Delta_i < 0    consumes temporal liquidity    (moved earlier)
```

Displacement is defined only across quanta: within a quantum the transactions are concurrent (sec. 6), so there is no finer position to move to or from, and Delta_i counts logical-time ticks, not physical instants. Advancement must be matched by deferral or by released reserve. In equal-size form this is a conservation condition,

```text
sum_{i: Delta_i < 0} g_i |Delta_i|   <=   sum_{j: Delta_j > 0} g_j Delta_j   +   R ,
```

with R the protocol-contracted reserve capacity; with variable gas and many quanta the operative constraint is per quantum, sum_i g_i x_{i,q} <= C_q for all q, and the market clears subject to all of them. Advancement is not created from nothing: it is deferral, seen from the other side, plus whatever reserve the protocol chooses to release.

## 10. An exchange, not a fee market

Position is conserved whoever moves it. A builder reordering privately conserves it too, since someone is always pushed later, so conservation is not what separates the two.

**The difference is consent.** A rearrangement performed on the block produces a *displaced* transaction: one that bore a cost it did not agree to and is not told about. A trade produces a *counterparty*: one that offered to move later, at a price it named, and was paid. Conservation says the cost falls on someone. It does not say that someone chose it, and choosing is the whole of the difference.

This is why the instrument of sec. 4 is a swap and not a fee. A swap has two sides, each of which wanted its own leg, and neither is the other's victim. So does this market.

Often the position moved is not fresh arriving work but a *pre-existing held allocation*, a multi-slot stream's reserved quantum in a future slot. A trade then swaps standing positions: the seller vacates a held quantum and takes a later one, the buyer takes the vacated one, per-quantum capacity is conserved, and the same quantum may be re-traded before its slot is built. For a stream whose value is joint (RN-11 sec. 5), its ask is the marginal effect on its whole schedule rather than a per-unit loss, so held positions are reassigned only while the stream stays within tolerance.

## 11. Who makes the market

Three market structures are possible, with a clear preference among them.

- **Pure order book.** Buyers and sellers cross bids and asks directly. It gives genuine price discovery, no protocol balance-sheet exposure, and neutrality, but risks thin and fragmented per-quantum liquidity and uncertain execution.
- **Protocol automated market maker.** The protocol posts a temporal-liquidity curve from reserve state, p^TL = f(R_q, D_q, sigma_q). It gives continuous availability and a predictable interface, but puts the protocol on the hook for inventory/reserve risk, turns curve design into hidden industrial policy, and invites manipulation.
- **Hybrid.** Ordinary liquidity comes from participants; the protocol supplies only an emergency reserve at a deterministic, published curve.

```text
participant asks and bids
        +
protocol reserve backstop      ->     temporal-liquidity clearing
```

The hybrid is the strongest: the protocol is not speculating on the price of time, it is enforcing a transparent reserve policy, and the reserve backstop caps how bad thin-market episodes can get without displacing participant price discovery. The design of R -- its size, its release rule, its price -- becomes a first-class protocol parameter.

Participant liquidity may itself be the residual of a market one level down. A project is often an internal economy of execution demands -- a matching engine, periodic order-book updates, scheduled funding payments, urgent liquidations -- that reallocates among its own classes before any residual reaches the exchange: order-book updates supply temporal liquidity to a liquidation wave inside the project first. That gives a three-level nesting -- inside a project, then between projects at this exchange, then the protocol reserve as backstop -- developed in RN-09.

## 12. The builder's residual role and verification

The builder receives a pre-cleared assignment

```text
S = { ( i, q_i, constraints_i ) }
```

and may still optimise everything that does not move a transaction between quanta: parallel execution, packing, state-access scheduling, and intra-quantum sequencing where the protocol allows it. It may not alter the cleared inter-quantum placement. Validators check the assignment against the clear:

- no transaction appears before its commitment time (sec. 6);
- FIFO transactions were not advanced without a cleared, compensated trade (sec. 7);
- advancement payments cleared and displaced suppliers were credited (sec. 8);
- deadlines, reservations, and per-quantum capacity hold (sec. 9).

Validators verify *compliance, not optimality* (RN-11 sec. 8): proving a schedule globally optimal is intractable, so the protocol checks the cleared assignment and the service floors and lets the builder keep the residual optimisation. ePBS already has staked builders committing to payloads and a validator committee attesting to timely reveal [3]; verifying a cleared ordering is the same kind of object, one step further in.

## 13. What this does to MEV

The mechanism does not remove MEV. It changes which form is legitimate. A user openly paying for an earlier quantum at a market-cleared, protocol-visible price is buying temporal value; a builder silently reordering on private information and keeping the surplus is extracting it. Moving inter-quantum placement to a public clear permits the first and aims to foreclose the second.

Within a quantum there is nothing to settle, because the transactions are concurrent (sec. 6). That is a feature. A deterministic tiebreak would price a priority that does not exist, and has been measured to introduce large exploitable bias [10]; strict fair ordering has a real revenue cost [9]. So: **price movement between quanta, and randomise or batch within one**, which keeps the priced market and the residual MEV surface apart (RN-11 sec. 4).

## 14. The Neutral Temporal Ordering Rule

The mechanism collects into four obligations.

1. **Entitlement.** Every transaction takes its initial position from its temporal entitlement time, the consensus-recognised commitment instant `t^c`, and may not execute before it.
2. **Movement only by trade.** A transaction may be deferred within its declared profile in return for compensation, and advanced above its FIFO entitlement only by purchasing temporal liquidity at the clearing price.
3. **Advancement is funded.** It comes from matched voluntary deferral or from contracted protocol reserve, and builders honour the cleared assignment rather than selling priority privately.
4. **Concurrency is not sold.** Intra-quantum transactions are unordered or separated by verifiable randomness, never by a deterministic tiebreak, which would price a priority that does not exist.

Together these make the flexibility patient demand holds into an asset it can sell, and send the value of that asset to its holder rather than to whoever builds the block.

## 15. What this changes

The contribution is the shift the mechanism embodies: from a one-sided market in which transactions bid to consume blockspace, to a two-sided market in which urgent demand buys temporal position from flexible demand, and the parties that supply flexibility -- not the builder -- receive its value. That RN-11 could be given such a mechanism at all is the claim; whether this is the right one is what the simulation stack (RN-11 sec. 9) is for.

---

## References

[1] TLM Research Notes: RN-11 (the allocation problem and the term structure), RN-10 (the economics and the two camps), RN-05 (the quantum lattice), RN-07 (the reducibility invariant), RN-01/02 (demand representation and verification).

[2] Future-slot claims on execution: Neuder, M. & Drake, J. *Execution Tickets.* Ethereum Research (ethresear.ch), 2024. Drake, J. *Based Preconfirmations.* Ethereum Research (ethresear.ch), 2024. (Expiry, refundability, resalability, and the leakage of block information from forward commitments.)

[3] *EIP-7732: Enshrined Proposer-Builder Separation (ePBS).* Ethereum Improvement Proposals, https://eips.ethereum.org/EIPS/eip-7732. (A signed builder payload commitment plus a payload-timeliness committee that attests to timely reveal; protocol-level builder commitments are verifiable.)

[4] *MEV Capture and Decentralization in Execution Tickets.* arXiv:2408.11255, 2024. (Rights concentrate among holders with the highest MEV-extraction ability and lowest capital cost; a dominant non-builder buyer can capture much of the value; a quantitative Goldilocks zone balances capture against market diversity.)

[5] *Galaxy Era: Agent-based Simulation of Execution Tickets.* arXiv:2501.16090, 2025. (Secondary markets let specialised holders enter and exit just-in-time and can reduce concentration; non-expiring tickets evaluated.)

[6] *The Future of MEV.* arXiv:2404.04262, 2024. (Context for protocol brokering of MEV through execution tickets and auctions.)

[7] Arbitrum Timeboost (auctioned express-lane ordering right). Offchain Labs documentation. (A single auctioned priority lane; the mechanism here is a compensated, FIFO-anchored generalisation.)

[8] Kelkar, M., Zhang, F., Goldfeder, S. & Juels, A. "Order-Fairness for Byzantine Consensus" (Aequitas). *CRYPTO* 2020. (The impossibility of strong batch-order-fairness; why FIFO neutrality must be stated as an achievable property.)

[9] Pugatsov, A., Ileri, C. U. & Decouchant, J. "The Blockchain Execution Dilemma: Optimizing Revenue XOR Fair Ordering." arXiv:2604.23266, 2026. (The measured revenue cost of fair-ordering constraints under congestion.)

[10] *Fair on the Surface: Transaction-Ordering Bias and MEV in the Mysticeti DAG-based BFT Protocol.* arXiv:2607.13378, 2026. (A deterministic validator-index tie-break introduces large ordering bias; an unpredictable tie-break is the remedy.)

[11] Asayag, A., Cohen, G., Grayevsky, I., Leshkowitz, M., Rottenstreich, O., Tamari, R. & Yakira, D. "Helix: A Scalable and Fair Consensus Algorithm Resistant to Ordering Manipulation." IACR ePrint 2018/863. (Threshold encryption to hide contents from ordering nodes; the sec. 6 causality/hiding requirement.)

[12] *Timed Commitments Revisited.* IACR ePrint 2023/977. (Forced revelation after a set time; commitment-time eligibility before public revelation.)

[13] Capponi, A., Jia, R. & Wang, Y. "Do Private Transaction Pools Mitigate Frontrunning Risk?" IACR ePrint 2023/1461. (The conditional effect and rent-shifting of pre-trade privacy.)

[14] Demsetz, H. "The Cost of Transacting." *Quarterly Journal of Economics* 82(1), 1968. Grossman, S. J. & Miller, M. H. "Liquidity and Market Structure." *Journal of Finance* 43(3), 1988. (The liquidity supplier / market-maker role priced by a spread; secs. 5, 11.)

[15] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM* 2024. (The impossibilities bounding truthful elicitation; sec. 5.)

[16] Lamport, L. "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM* 21(7), 1978, 558-565. (The happens-before partial order and logical clocks; the absence of a global physical time in a distributed system. The quantum read as logical time, inter-quantum as a total logical order and intra-quantum as concurrent -- sec. 6.)
