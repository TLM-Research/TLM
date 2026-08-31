---
id: RN-12
title: "The Temporal Liquidity Market: Protocol and Mechanism Design"
subtitle: "Trading temporal position against a neutral baseline"
version: v0.1 (first standalone draft, split out of RN-11: the temporal-liquidity exchange, the logical-time quantum and temporal entitlement time, the bounded tradable window, and the drift/variance discriminator)
status: "Public draft. A candidate mechanism for the problem RN-11 states; proposed, not adopted."
program: "Temporal Liquidity Market (TLM)"
date: August 5, 2026
---

# RN-12 -- The Temporal Liquidity Market: Protocol and Mechanism Design

## Abstract

RN-11 states the execution-capital allocation problem and reads its two objects -- the allocation's dual as a welfare benchmark on the value of capacity, and the bootstrapped market term structure -- without identifying them, but it deliberately builds no mechanism. This note proposes one. Within a slot, transactions trade *temporal position*: patient demand supplies temporal liquidity by accepting a later quantum, urgent demand buys it by moving to an earlier one, and the two clear at a uniform price against a first-in-first-out (FIFO) baseline. The quantum is read as a unit of logical time in Lamport's sense: inter-quantum order is the execution order consensus can agree on, while the transactions within a quantum are concurrent and carry no intrinsic order -- which is what makes inter-quantum position sellable and intra-quantum position not. The instant a transaction first acquires the right to compete -- its *temporal entitlement time* -- is protocol-defined, not a wall-clock arrival, and sits in a three-layer picture: physical time belongs to the network, protocol time to consensus, and economic time to TLM. Across slots, the future execution rights that make the term structure tradable are defined as transferable assets, with the concentration risks that transferability carries stated rather than assumed away. The organizing move is to separate three roles that today's builder holds at once -- the protocol as issuer of execution rights, an exchange that matches buyers and sellers of timing, and a builder that only constructs a compliant schedule -- so that the value of flexibility flows to the parties that supply it rather than to whoever controls block construction. The mechanism is stated as a candidate with its failure modes: the pricing of temporal liquidity, the causality rule that keeps advancement honest, the market-maker options, and the verification a validator must perform. Where RN-11 says the problem is stated but not solved, this note offers one way it might be solved, and marks what remains open.

## 0. What this note assumes

RN-11 states the allocation problem; this note proposes one mechanism for it and assumes that statement. It takes the quantum lattice, the reducibility constraint that makes an allocation checkable, and the demand representation as given.

This note proposes a mechanism, so it takes positions RN-11 was careful not to take. Read its rules as candidates to be tested (RN-11 sec. 9, the simulation stack), not as settled protocol.

## 0.1 Scope: this note is not about Ethereum

The mechanism here is stated for a chain in general. It assumes only that the system produces blocks in sequence, that some party assembles them, that execution position within and across those blocks has value, and that a native token exists to denominate payments. It does not assume an account model, a virtual machine, smart-contract expressiveness, proposer-builder separation, or any particular fee rule.

**The problem is not Ethereum's.** Every chain that orders transactions sells position without pricing it, and every chain conflates the party that constructs a block with the party that captures the value of ordering it. Section 1 uses Ethereum's proposer-builder separation as the illustration because it is the most documented instance, not because it is the only one. The same conflation exists wherever a single actor both decides order and profits from it.

**Chains with different designs may find this easier to adopt, not harder.** A chain with parallel execution, a shorter block interval, or a fee market not yet frozen by a decade of tooling has fewer constraints on what it can change. Monad, Aptos and HyperEVM each treat execution scheduling as a live design question rather than a settled one. Bitcoin, whose script is deliberately limited and whose block interval is coarse, is the hardest case for the instruments of sections 3 and 4 and the cleanest case for the ordering rule of section 14. A reader should test the mechanism against their own chain rather than translating from Ethereum.

**Ethereum is treated separately, and under its own constraints.** Two companion notes develop an Ethereum-specific instantiation, and their design goal is different from this one's:

- **RN-15** proposes a single-slot temporal liquidity fee that fits inside EIP-1559 with one signed transaction field, no new roles, and no change to the builder's position. It is the minimal version, chosen for backward compatibility rather than for completeness.
- **RN-21** sets out what an Ethereum design would need in order to work across slots rather than within one, and where the base fee controller constrains any such design.

**Backward compatibility is a design goal there and not here.** Ethereum has a decade of deployed tooling, a fee market users have learned, and a change process that rewards proposals which alter as little as possible. That is a real constraint and RN-15 accepts it. This note does not: it separates roles that Ethereum currently combines, which is a larger ask than any single EIP would carry. Readers who want the smallest change that could ship should start with RN-15. Readers who want to know what the market would look like if it were designed rather than retrofitted should stay here.

Neither direction supersedes the other. The general mechanism states what the market is; the Ethereum notes state what one chain could adopt without rebuilding itself.

---

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

with [t1, t2] an execution window, C a capacity entitlement (units of gas or reserved capacity), and Gamma the service conditions -- priority class, state-access restrictions, and exercise rules. The holder may consume it, transfer it, subdivide it, combine it with other rights, resell it before expiry, let it expire, or -- subject to design -- post it as collateral. This is the zero-coupon and coupon instrument of RN-11 sec. 2 given an owner and a secondary market, and it is close to the execution-ticket and preconfirmation proposals already in the literature, which examine expiry, refundability, resalability, and secondary markets directly [2].

**Transferability is not automatically fair.** Economic analysis of execution tickets finds that the rights concentrate among holders with the highest MEV-extraction ability and the lowest cost of capital, so that a large, capital-advantaged party that is not even a builder can come to dominate the market [4]. A holder who acquires a future proposal right and then runs a just-in-time resale auction can gain a structural edge. The finding cuts both ways: an agent-based study reports that a secondary market can *reduce* concentration by letting specialized holders buy just-in-time rather than pre-committing capital, and that non-expiring tickets change the picture again [5]. The conclusion is not that resale is unsafe but that it is a design surface with a Goldilocks zone [4], not a free good: resale should be facilitated, and concentration bounded by explicit means (caps, forfeiture, decay), not left to chance.

**Where these rights live: consensus state, not the mempool.** A right is a durable, transferable, ownership-bearing claim, and the commitment order that anchors the market must be forge-proof (sec. 7), so forward positions cannot sit in the mempool -- which is transient, node-local, and untrusted, and is cleared as transactions are included. They belong in **consensus-tracked state**: an enshrined reservation registry, the layer where token and NFT balances live, in which each held quantum, ticket, or lease is an entry with an owner, and a cleared temporal-liquidity trade is a state transition that reassigns it. The mempool carries only the transient traffic -- pending transactions and the bids and asks waiting for the next clear -- and once a trade clears, the reassignment settles into the registry, which is the durable state the term structure (RN-11 Part I) prices against. Two consequences. First, this is real state overhead: every outstanding reservation is protocol state, so rights should carry expiry (sec. 4's non-expiring ticket is the worst case here), and the registry must be sized and priced against that cost. Second, the alternative is to hold positions off-chain as bonded commitments -- the preconfirmation style, backed by restaking and slashing, settled on-chain only in dispute [2] -- which is lighter on state but reintroduces the semi-trusted sequencer or relay whose concentration this section warns about. On-chain registry versus bonded off-chain commitment is a neutrality-versus-overhead tradeoff, and where a design lands on it decides how much of the market is actually enshrined.

## 4. Perpetual-like instruments

A literal perpetual right to a *named* slot is impossible -- each slot is unique and consumed once. Three perpetual-*like* instruments are possible, in increasing order of risk:

- **Non-expiring execution ticket.** A ticket valid until exercised, naming no specific slot -- a floating claim on future execution supply. Its danger is inventory overhang, not permanent privilege.
- **Rolling capacity lease.** A project receives c units per slot or epoch until cancellation, R_i = { c_i(t) : t >= t0 } -- a revolving facility or subscription. It gives a project stable financing without naming slots.
- **Perpetual share of a channel.** A holder owns a fixed fraction alpha_i of a designated capacity pool, alpha_i · C_t, in every eligible period. This is the dangerous one: a permanent, tradable claim on a scarce public resource, which creates durable rent extraction and a barrier to entry -- the "who checks builder power" problem (RN-11 sec. 8) migrated into capacity ownership, with the rentier dynamics of a perpetual spectrum licence.

The recommendation is **renewable long-duration leases, not irrevocable perpetual property rights.** A lease gives a project the financing stability a perpetual would, but the protocol retains the ability to reprice, re-auction, or let the claim decay, so capacity is never permanently privatised. If a perpetual share is offered at all, it should be a share of *capacity* (so it auto-scales with the chain rather than concentrating a fixed quantity) and periodically repriced.

---

## 5. The two camps as bid and ask

RN-10's two camps become the two sides of an order book in temporal position.

**Suppliers of temporal liquidity** are transactions or streams that can move later. Each declares a maximum delay, an acceptable quantum range, a deadline, an interruption right, and a required compensation, and submits an ask

```text
a_i( dt ) = minimum compensation to accept a delay of dt quanta.
```

**Buyers of temporal liquidity** are transactions that want to move earlier than their default FIFO position. Each declares a desired advancement, a deadline, a maximum temporal premium, an acceptable quantum, and execution conditions, and submits a bid

```text
b_j( dt ) = maximum payment for an advancement of dt quanta.
```

A trade is feasible when a buyer's bid covers a supplier's ask for the same displacement,

```text
b_j( dt )  >=  a_i( dt ),
```

and it moves buyer j earlier and supplier i later while total per-quantum capacity is preserved. The point that distinguishes this from a tip auction: the buyer's payment is not captured by the builder. It finances the compensation to the supplier who provides the flexibility, with any protocol-defined portion burned or retained as a scarcity charge (sec. 8). This is the ask a and bid b of a real exchange, not a one-sided fee, with the supplier in the liquidity-provider role priced by a spread [14]. It generalizes a single auctioned priority lane such as Timeboost [7] into a compensated, FIFO-anchored, two-sided clear.

**What makes the market, and who takes which side.** Participants differ in how tightly their value binds to a target execution time, and that difference -- not the slope of value against delay, dV/dt -- is what creates the market. Value is measured against a target tau (RN-11 sec. 5), and for the target-bound work TLM cares about it is two-sided: executing early is as costly as late, so a monotone value-versus-delay curve and its slope are the wrong object. What discriminates the two sides is the tolerance a transaction's value has for the drift between wall-clock relevance and block execution, T_wall - T_block -- in both its size (the binding tightness, RN-11's W(alpha)) and its variance (predictability). Those are the two independent axes RN-11 sec. 5 already names, and the drift, unlike a private value-slope, is what the mechanism can observe and price.

- A **buyer** of temporal liquidity requires the drift small with small variance -- a tight, low-jitter landing near its target. A liquidation must land in a narrow window around a price event; an oracle update near the event it reports; ADL is safety-critical. None tolerates a wide or jittery drift, so each buys a guarantee of position.
- A **supplier** tolerates a large drift, a large variance, or both -- a batch posting, an overnight payment, background computation, governance, whose value is nearly flat across a wide window and barely moves if execution is reassigned, even unpredictably, within it. It sells that tolerance.

The slope of value re-enters only for the *size* of the order, not the side: how much a buyer pays or a supplier demands scales with the value at stake once the drift leaves the tolerable band. The trade is a Pareto improvement -- the buyer's guarantee is worth more than the tolerance the supplier gives up -- provided capacity is conserved so no third party is pushed into scarcity; what is traded is priority over the execution-capital surface, capacity reassigned, not created (sec. 10). And the side is set by the shape of the drift tolerance, transaction by transaction, not by identity: the same project supplies from its jitter-tolerant order-book updates and buys for its liquidations, and the protocol sees only the declared, verifiable tolerance. This gives a chain-independent definition: **the temporal liquidity of an execution request is the range of drift T_wall - T_block its value tolerates -- the width of the reassignment window and the variance admissible within it -- before utility falls below the declared threshold**, which is RN-11's binding-tightness width W(alpha) together with its predictability dimension.

The self-selection here does useful work on the hardest open problem in RN-11 (sec. 11, incentive compatibility): the mechanism never asks a transaction to declare its full decay function phi. It asks only whether the transaction will pay to advance or accept payment to defer, and a and b reveal exactly which side of the tight/loose partition the transaction is on. Willingness to pay substitutes for declaration, which is where transaction-fee mechanisms are on firmer ground against the elicitation impossibilities [15].

## 6. The quantum is logical time; causality is commitment time

The mechanism prices *when* a transaction executes, so it needs a notion of "when" a decentralized system can agree on. Physical wall-clock time is not it. Nodes are geo-distributed, their clocks skew, and message delays are asymmetric and manipulable, so there is no global physical clock and no agreed physical order of arrivals. What a distributed system can establish is not physical time but *logical* time -- Lamport's happens-before order [16].

**Happens-before is a partial order, and most pending transactions are concurrent.** Lamport's relation a -> b holds when a causally precedes b: the same participant in sequence, a message from a received at b, or transitively. Two events with no such chain are *concurrent* -- neither precedes the other. Pending transactions send no messages to each other, so almost none are causally related: the mempool is very nearly one large *antichain* of concurrent events. Physically there is no ground-truth total order among them to discover, and any total order a builder imposes on concurrent transactions is a convention, not a fact -- which is why a builder's fine-grained reordering can extract value that corresponds to nothing real.

**The quantum is a logical-time tick, and this is what the lattice buys.** Read RN-05's quantum as one level of a logical clock. Inter-quantum order (q < q') is a *total order in logical time*: it is the order consensus can agree on, and it is the order that appears in the ledger and governs execution. Intra-quantum is the opposite -- the transactions in one quantum are an equivalence class of *concurrent* events, an antichain with no intrinsic order. So the lattice draws exactly the line this section is about:

> **Inter-quantum order establishes a real, consensus-agreed execution order in logical time. Intra-quantum there is no order to establish -- the transactions are concurrent.**

*Commitment time is a logical timestamp -- the transaction's temporal entitlement time.* The binding commitment time t^c is not a wall-clock reading; it is the transaction's position in the logical (commitment) order consensus records -- the instant at which it first acquires the right to compete for execution. Call that instant the transaction's **temporal entitlement time**: a protocol-defined point, fixed by a consensus-recognized commitment so that no single party -- least of all a builder timestamping its own receipts -- can set it. The entitlement it confers is what the rest of the note trades: it can be retained (FIFO), sold (supply of temporal liquidity), bought (advancement), reserved, or exchanged. The causality rule is then a happens-before statement -- commitment happens-before execution -- so t^e must not precede t^c. Distinguishing three events,

```text
t^c   binding commitment   (the transaction's logical timestamp; consensus holds a commitment)
t^r   revelation           (the payload is publicly revealed)
t^e   execution
```

the constraint is t^e >= t^c, with t^c <= t^r <= t^e in the normal case. It is admissible and useful to have t^e < t^r -- execution ordered while the payload is still encrypted, revealed only just before execution -- which is what stops advancement from leaking forward information; it is never admissible to have t^e < t^c, because that places a transaction in the order before consensus holds any commitment to it. Commit-reveal, threshold encryption [11], and timed commitments [12] are what let a transaction hold its logical (commitment) position while its contents stay hidden, so the exchange prices *when* without exposing *what* -- a component, since pre-trade privacy shifts rather than abolishes rents [13], and preconfirmation work notes that a forward commitment handled naively leaks block information [2].

Two consequences and two caveats run through the rest of the note. The **FIFO baseline is FIFO in logical time** (sec. 7), never physical arrival, because physical arrival cannot be totally ordered; advancement means moving to an earlier quantum -- ahead of logically-earlier commitments -- a consensus-checkable act bounded below by t^c. **Intra-quantum position is not for sale** (secs. 9, 13): within a quantum there is no "before," so selling within-quantum order would be selling an arbitrary tiebreak as if it were priority -- unfair, and extractable [10]. The caveats: causal dependencies do exist and must be respected -- if j reads state i writes, then i -> j, they are not concurrent, cannot share a quantum as an unordered pair, and the dependency forces i earlier (the precedence and conflict constraints of RN-11 sec. 4); and the quantum's granularity acquires a meaning -- it should be no finer than the resolution at which consensus can establish a genuine logical order, since finer than that the protocol would be pricing distinctions among events it cannot really order. That bounds quantum size from below by the system's logical-time resolution, the lever RN-05 left open (sec. 15).

**Three layers of time.** The picture separates into three, and they are worth naming separately. *Physical time* belongs to the network -- the wall-clock instants at which a transaction reaches a node in Tokyo, a builder in Frankfurt, a relay in Virginia, a validator in Singapore, all different and none authoritative. *Protocol time* belongs to consensus -- the logical order the chain agrees on, in which the temporal entitlement time is fixed. *Economic time* belongs to TLM -- the layer at which the entitlement to a quantum is priced, traded, and reserved. The layers nest by mapping and bound: economic time is mapped onto protocol (logical) time, which is bounded in turn by physical time, so the market may reassign execution only within what consensus can order and what the network can deliver -- the tradable window of sec. 9, never wider. A financial exchange collapses the first two into one gateway that stamps orders as they arrive and makes its own sequence authoritative; a blockchain has no single gateway, so consensus must be it -- harder, because the order must be Byzantine-agreed, but cleaner, because no one party owns it. The consequence for fairness is that FIFO on physical arrival was never well defined -- earlier according to whom? -- so FIFO here is FIFO on temporal entitlement time (sec. 7), and the mechanism stops trying to reconstruct a physical order that does not exist. That is the note's position on a real design fork: a blockchain should not attempt to recover physical arrival order, it should define a protocol-native temporal entitlement and let the economic layer trade it. This is what it means to make time a first-class economic variable rather than a contested timestamp.

## 7. FIFO as the neutral baseline

Advancement has to be advancement *relative to something*, and the neutral reference is FIFO on the temporal entitlement time -- FIFO in the logical (commitment) order of sec. 6, since physical arrival cannot be totally ordered. FIFO on physical arrival was only ever an approximation of an order that does not exist; FIFO on entitlement time is exact, because that order is what consensus records. Because strong order-fairness is impossible [8], this baseline is stated as an achievable neutrality property, not derived from a stronger one. Let q_i^0 be the earliest quantum available to transaction i under protocol-observed FIFO:

```text
q_i^0 = min { q : q >= q_i^commit,  C_q^remaining >= g_i }
```

where q_i^commit is the quantum of i's commitment time and g_i its gas. Absent any temporal-liquidity trade, i sits at or after its FIFO position, q_i >= q_i^0, and may be pushed later only within its deadline d_i:

```text
q_i^0  <=  q_i  <=  d_i          (no trade, or voluntary/ compensated deferral)
```

To execute *earlier* than its FIFO position -- but never before its commitment eligibility -- a transaction must buy temporal liquidity at or above the protocol minimum spread and clear against supplied flexibility:

```text
q_i < q_i^0   requires   p_i^TL  >=  p_min   and a cleared match against a supplier or reserve.
```

The neutrality principle is then sharp:

> FIFO establishes the initial temporal entitlement. Any advancement must be purchased from parties whose entitlement is displaced, or from explicitly reserved protocol capacity.

This is fairer than the status quo in a specific, checkable way: no one is advanced except by a trade that compensates whoever they passed, and the builder cannot reorder and keep the surplus. It also resolves the tension flagged in RN-11 sec. 4 and sec. 8 -- advancement is bought only against *willing* suppliers (or reserve), never against a non-consenting FIFO transaction, so priced priority does not become sanctioned front-running.

**The baseline needs a commitment order at the resolution it prices.** FIFO on commitment time presupposes that consensus establishes an order among commitments at the granularity the market trades. If consensus resolves only to the slot -- if all of a slot's commitments are concurrent at consensus (the antichain of sec. 6) -- then there is no intra-slot FIFO to anchor, and the builder, holding the whole slot at build time, assigns intra-slot position freely. For the baseline to be neutral and enforceable at quantum resolution, the protocol must supply that finer order itself: an enshrined preconfirmation or commitment log, or a sequencer whose timestamps the builder cannot forge. Absent such a source, intra-slot order is not FIFO-able and must be left concurrent -- randomized or unsold (sec. 13) -- and only slot-level advancement can be priced. So the resolution at which temporal liquidity can trade is bounded by the resolution at which consensus records commitments (sec. 6, sec. 15): price finer than that and the baseline is inventing the order it claims to enforce.

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

## 10. Deferral and advancement liquidity

The two camps are two views of one conserved quantity. **Deferral liquidity** is the ability to move execution later, q -> q + Delta, supplied by patient transactions. **Advancement liquidity** is the ability to move it earlier, q -> q - Delta, demanded by urgent ones. They are not separate commodities: advancement exists only because deferral (or reserve release) creates it. Hence

> Temporal liquidity is conserved through the reallocation of capacity positions, except where the protocol releases previously reserved capacity.

That conservation is what makes this an exchange rather than a fee market. A fee market prints a price and lets the builder keep the proceeds; an exchange moves a position from one party to another and pays the party that gave it up.

Often the position moved is not fresh arriving work but a *pre-existing held allocation* -- a multi-slot stream's reserved quantum in a future slot. A trade then swaps standing positions (the seller vacates a held quantum and takes a later one, the buyer takes the vacated one), conserving per-quantum capacity, and the same quantum may be re-traded before its slot is built. For a stream whose value is joint (RN-11 sec. 5), its ask is the marginal effect on its whole schedule, not a per-unit loss, so held positions are reassigned only while the stream stays within tolerance.

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

The hybrid is the strongest: the protocol is not speculating on the price of time, it is enforcing a transparent reserve policy, and the reserve backstop caps how bad thin-market episodes can get without displacing participant price discovery. The design of R -- its size, its release rule, its price -- becomes a first-class protocol parameter (sec. 15).

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

The mechanism does not remove MEV; it changes which form is legitimate. **Legitimate temporal value** is a user openly paying for an earlier quantum at a market-cleared, protocol-visible price. **Illegitimate ordering extraction** is a builder silently reordering on private information and keeping the surplus. The design permits the first and, by moving inter-quantum placement to a public clear, aims to make the second impossible at the inter-quantum level.

It does not settle order *within* a quantum -- and by the logical-time reading (sec. 6) there is nothing to settle, because the transactions are concurrent. That is a feature, not a gap: since no "before" exists inside a quantum, a deterministic tiebreak would price a priority that does not exist, and it has been shown to introduce large, exploitable ordering bias (sorting equal-priority items by validator index, say), with an unpredictable tiebreak the remedy [10]. The principled treatments are order-independent execution (a commutative batch) or verifiable randomness -- never a deterministic tiebreak. And the revenue cost of strict fair ordering is real and has been measured [9]. The architecture this note recommends takes both findings seriously: **price movement between quanta, and suppress or randomise discretionary ordering within a quantum**, so the priced market and the residual MEV surface are kept apart (RN-11 sec. 4).

## 14. The Neutral Temporal Ordering Rule

The mechanism collects into seven statements:

1. Every transaction acquires an initial temporal entitlement at its temporal entitlement time -- its consensus-recognised commitment instant t^c -- and a FIFO baseline position from it.
2. A transaction may be deferred to a later quantum or slot only within its declared temporal profile and deadline, either voluntarily or in return for temporal-liquidity compensation.
3. A transaction may be advanced relative to its FIFO entitlement only by purchasing temporal liquidity at or above the protocol minimum spread and the market-clearing price.
4. No transaction may execute before its binding commitment time.
5. Advancement capacity must come from matched voluntary deferral or from explicitly contracted protocol reserve.
6. Builders must honour the cleared inter-quantum assignment; they do not privately sell temporal priority.
7. Intra-quantum transactions are concurrent (sec. 6): their order is semantically unordered or broken only by verifiable randomness, never by a deterministic tiebreak, which would price a priority that does not exist.

The rule is coherent, enforceable in principle, and economically meaningful: it makes the flexibility that patient demand holds into an asset that patient demand can sell, and it makes the value of that asset flow to its holder rather than to the party that happens to build the block.

## 15. What is unsolved

Stating the mechanism makes its open parts precise.

1. **Incentive compatibility of a and b.** Willingness to pay reveals the side of the partition (sec. 5), but the ask and bid schedules are themselves declarations; the mechanism must make truthful a_i, b_j optimal or approximately so under the transaction-fee-mechanism impossibilities [15]. Over-stating flexibility to collect deferral compensation is the specific deviation to defend against.
2. **Thin markets.** Per-quantum temporal-liquidity markets may be thin and fragmented; the reserve backstop (sec. 11) bounds the damage but its size, price, and release rule (the design of R) are open, and a mis-set reserve is itself industrial policy.
3. **Concentration of rights.** Transferable and perpetual-like rights concentrate under capital and MEV advantages [4]; caps, forfeiture, decay, and lease-not-perpetuity (secs. 3-4) are candidate bounds, and which combination keeps the market in the Goldilocks zone [4][5] is unresolved.
4. **The within-quantum rule.** Random, batch, or disclosed-auction ordering inside a quantum each have different bias and MEV properties [10]; the choice interacts with state-conflict resolution and is not settled here.
5. **The reserve as monetary policy.** A protocol reserve that releases advancement capacity is close to a central bank operating in a market for time; its rule set has distributional consequences that deserve their own treatment.
6. **Interaction with the term structure.** The intra-slot exchange of this note and the cross-slot term structure of RN-11 are the same market at two horizons; how the clearing price p* relates to the bootstrapped forward curve, and whether the two can be made mutually consistent under no-arbitrage, is the natural next question.
7. **Quantum granularity.** The logical-time reading (sec. 6) bounds the quantum from below by the resolution at which consensus can establish a genuine order, but not from above; the tradeoff -- finer quanta give more sellable temporal positions and a more precise market, coarser quanta enlarge the concurrent class and shrink the MEV surface -- is a design choice RN-05 leaves open and this mechanism makes economically consequential.
8. **The storage and settlement layer** (sec. 3). Forward positions must live in consensus-tracked state (a reservation registry), not the mempool, which means every outstanding reservation is state; how to bound that overhead (expiry, aggregation, pricing state), whether to enshrine the registry on-chain or hold positions as bonded off-chain commitments, and what the off-chain route costs in neutrality, are open. The choice sets how much of the market is actually enshrined versus delegated to a semi-trusted sequencer.

The contribution is the shift the mechanism embodies: from a one-sided market in which transactions bid to consume blockspace, to a two-sided market in which urgent demand buys temporal position from flexible demand, and the parties that supply flexibility -- not the builder -- receive its value. That RN-11 could be given such a mechanism at all is the claim; whether this is the right one is what the open questions and the simulation stack (RN-11 sec. 9) are for.

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

[15] Roughgarden, T. *Transaction Fee Mechanism Design.* arXiv:2106.01340; *JACM* 2024. (The impossibilities bounding truthful elicitation; sec. 5 and sec. 15, Q1.)

[16] Lamport, L. "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM* 21(7), 1978, 558-565. (The happens-before partial order and logical clocks; the absence of a global physical time in a distributed system. The quantum read as logical time, inter-quantum as a total logical order and intra-quantum as concurrent -- sec. 6.)
