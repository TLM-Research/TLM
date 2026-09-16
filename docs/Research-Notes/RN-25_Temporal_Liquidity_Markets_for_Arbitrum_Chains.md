---
id: RN-25
title: "Temporal Liquidity Markets for Arbitrum Chains"
subtitle: "In-place TLA ordering as an optional alternative to latency competition"
version: "1.1"
status: "External review draft - L2 research and deployment agenda"
program: "Temporal Liquidity Market (TLM)"
date: "2026-09-15"
license: "CC-BY-4.0"
---

# RN-25 v1.1: Temporal Liquidity Markets for Arbitrum Chains

## In-place TLA ordering as an optional alternative to latency competition

**Temporal Liquidity Market (TLM) Research Program**  
**Research Note RN-25**  
**Version:** 1.1  
**Status:** External review draft, L2 research and deployment agenda  
**Date:** 15 September 2026

---

## Abstract

The Temporal Liquidity Market framework was developed first for L1 execution systems. RN-01 and RN-02 define transaction-level temporal profiles and the case for making temporal demand legible to the execution system. RN-06 studies Monad. RN-12 gives the general two-sided mechanism. RN-15 applies a block-local Temporal Liquidity Authorization (TLA) to Ethereum's EIP-1559 setting, and RN-16 extends the model across slots through separate Funding and Supply Legs. RN-25 carries that research program to Ethereum L2s, beginning with Arbitrum.

The motivation remains on an L2 and is independently important there. Much of the Ethereum ecosystem's application growth, transaction activity, and experimentation now occurs on L2s. These systems host trading, payments, games, tokenized assets, oracles, settlement services, and application-specific chains with different temporal demands. Arbitrum is widely used, supports financially significant applications, and offers dedicated chains with configurable sequencing. TLM for Arbitrum is therefore a separate research and deployment lane, not merely a trial run for eventual L1 adoption.

The adoption distinction is explicit. An **out-of-protocol** version changes sequencer policy and settlement services but leaves Nitro transaction validity, ArbOS state transition, and L1 contracts unchanged. An **in-protocol** version would make TLA fields or settlement consequences part of chain validity or state. The out-of-protocol path is a useful Arbitrum deployment form in its own right because sequencing is already an L2 service boundary. It also permits faster iteration. The in-protocol path remains relevant where stronger enforcement, common transaction semantics, or neutral settlement justify integration. In parallel, the Ethereum work continues to study TLA as an extension to EIP-1559, where review should be deliberate because the consequences are system-wide.

Here, “protocol” refers to the Arbitrum chain being modified. A sequencer policy may be outside Arbitrum's validity rules even though its resulting transactions and blocks ultimately settle through Ethereum.

The initial Arbitrum mechanism is block-local. Transactions may opt into TLA. Positions assigned to opt-outs remain under baseline treatment; participants are permuted only across participant positions, in descending TLA order. Positive TLA authorizes payment for realized advancement across eligible negative-TLA participants. Negative TLA supplies later participant rank and may receive compensation only when it is actually displaced. The sequencer commits to the baseline candidate order before applying TLA sorting. The finalized block then permits two tests: the realized participant order must follow the signed TLA rule, and crossing-based settlement must follow the committed baseline. This commitment verifies the sequencer's stated baseline; it does not prove truthful receipt times or candidate-set completeness.

---

## 1. The L2 claim

### 1.1 FCFS does not provide ex ante order assurance

An FCFS sequencer orders by arrival at its own observation boundary. A sender normally does not know the other transactions, their network paths, the sequencer's internal queue, or the final candidate set. It therefore does not know its relative block position before execution. FCFS is a policy for resolving observed arrivals, not a service guarantee to each sender.

That uncertainty creates a latency arms race. Traders may buy private connectivity, co-locate near sequencer infrastructure, submit redundantly, or repeatedly replace transactions to improve their chance of arriving first. On a public chain, this is a poor allocation rule. Relative order depends on private infrastructure and network location rather than a rule available on equal terms to all users. Marginal latency spending can duplicate infrastructure, increase message load, and concentrate advantage around actors with privileged access, while still giving senders no firm ordering assurance. TLA does not eliminate competition, but it moves participant-to-participant ordering into a disclosed rule whose authorizations and realized results can be measured.

### 1.2 TLM changes the ordering variable

For participating transactions, TLM replaces arrival rank as the determinant of relative order with a signed TLA value. Let `P_k` be the included participants governed by one clearing rule in L2 block `k`. The required ordering relation is

```text
a_i > a_j  =>  pos_k(i) < pos_k(j),  for i,j in P_k,
```

with a disclosed tie-breaker. A positive value requests earlier participant order and authorizes payment. A negative value accepts later participant order and may receive compensation. A participant that happened to arrive first may execute fifth when four other participants submitted higher TLA. That is not a failure: participation gives up any claim to participant-to-participant FCFS rank.

The service is **rule assurance**, not exact-position assurance. TLA does not promise an exact index, inclusion in a block, application success, or improvement over an unobservable counterfactual.

### 1.3 The two legs

The **Funding Leg** is the money authorized and escrowed by positive-TLA participants. The **Supply Leg** is the set of negative-TLA participants that consent to later participant rank. A block-local market works only if:

1. relative order is scarce enough that positive authorization appears;
2. negative-TLA supply is present in the same L2 block;
3. the realized participant order follows the TLA rule; and
4. consumer charges cover provider payments.

If no flexible supply appears, TLA remains a priority-ranking mechanism but the two-sided TLM claim has not been established.

**No deployed blockchain execution market pays a participant to accept a later position.** Ethereum L1, Timeboost, and the forward blockspace market of sec. 8 each sell an earlier or guaranteed position. The Supply Leg is the side none of them carries, and establishing it is what RN-25 has to do. This section owns that claim; later sections refer to it.

**A discount is not a payment.** Schemes that give flexible demand a lower price are common, and the Supply Leg is not one of them. Cloud spot instances are cheaper because they are interruptible. Off-peak tariffs are cheaper because load is shiftable. RFC 8622 Lower Effort marks traffic as yielding and compensates it with nothing. In each case the flexible party asks for less and receives less. Negative TLA instead receives a transfer, which requires that the provider held a position and gave it up. This is why sec. 9.3 pays only on realized displacement `d_j > 0`, and why sec. 5.1 commits the baseline before sorting. Without that entitlement there is nothing to compensate, and a declaration of flexibility does not create one.

**The paid form exists outside blockchains.** Demand-response programmes pay consumers to curtail load, measured against a metered customer baseline. Airlines pay denied-boarding compensation to passengers holding a confirmed reservation who accept later transport. Both clear at scale, and both settle the entitlement before paying, on a baseline the paying party does not construct. A single operator-run sequencer has no equivalent, which is what secs. 5.2 and 6.1 concede. That gap, rather than implementation cost, is what the baseline commitment is trying to narrow.

### 1.4 Initial mechanism scope

The initial mechanism changes neither Nitro transaction validity nor physical gas accounting. Every transaction must independently satisfy ordinary Nitro fee and validity rules. Temporal payment is separate from execution and parent-data charges. The first deployment is block-local; cross-block reserves, TSP commitments, and L1 batch-posting markets remain later parts of the L2 research program.

### 1.5 Research lineage and adoption path

RN-25 is an application of the existing TLM framework, not a separate L2 theory:

| TLM note | Contribution used here |
|---|---|
| RN-01, *Temporal Execution Profile* | temporal requirements belong to a transaction's execution demand |
| RN-02, *Protocol-Visible Temporal Abstraction* | an execution system cannot allocate on temporal information it never receives |
| RN-06, *Monad: A Temporal-Liquidity Analysis* | the framework applies beyond Ethereum's specific fee mechanism |
| RN-12, *Temporal Liquidity Market Mechanism Design* | urgent demand and flexible supply form distinct market legs |
| RN-13 Part II, *Capacity and Welfare in Blockchain Execution Systems* | evaluation requires more than transaction count or nominal throughput |
| RN-15, *A Temporal Liquidity Authorization for EIP-1559* | signed TLA and block-local ordering and funding |
| RN-16, *A Two-Leg Temporal Liquidity Reserve for EIP-1559* | Funding and Supply Legs remain separate across time |
| RN-33, *Horizontal Temporal Service Classes for Monad* | an EVM-compatible L1 can expose temporal scheduling without copying Ethereum's exact mechanism |

Ethereum remains the principal L1 research target. RN-15 asks whether EIP-1559 can be extended with a second temporal signal, and RN-16 asks whether that signal can improve inter-slot congestion control. Those proposals require careful review because Ethereum is mature, widely integrated, and economically consequential. A long adoption process is appropriate.

The L2 route is not conditional on an L1 protocol change. A sequencer-side service can expose demand, supply, settlement, manipulation, and welfare effects while leaving chain validity unchanged. A dedicated Arbitrum chain lowers deployment and coordination costs without lowering the standard of evidence. Successful external operation would be a valid L2 outcome. It may also inform later in-protocol work on Arbitrum and parallel work on Ethereum, but neither is required to justify the L2 mechanism.

This sequencing of the research path also reflects feedback from a discussion with the PBS Foundation: a mechanism seeking adoption should identify what can operate outside a base protocol before asking a mature production chain to change consensus-facing rules. RN-25 applies that practical constraint without treating L2 deployment as subordinate to L1 adoption. The reference records the source of the implementation strategy, not an endorsement of the mechanism or of the claims in this note.

---

## 2. Why Arbitrum Orbit is a useful target

Arbitrum provides Nitro-based technology for launching dedicated chains. The current documentation describes configurable execution, throughput, gas tokens, data availability, governance, and validation. Ordering can use FCFS, Timeboost, or custom rules. Arbitrum One's sustained use, capital, and application activity make this a study of a production L2 architecture rather than a toy scheduling environment.

This creates three possible targets:

| Target | Degree of change | Research use |
|---|---:|---|
| out-of-protocol ordering service | low | test signed TLA, in-place ordering, funding, and settlement without changing chain validity |
| dedicated Arbitrum test chain | moderate | control traffic, sequencing policy, fee parameters, and telemetry |
| in-protocol chain extension | high | make TLA interpretation or settlement part of transaction validity or chain state after evidence exists |

The out-of-protocol service on a dedicated chain is the starting point. It permits controlled changes while retaining an EVM environment and Ethereum settlement. Moving TLA into transaction validity is a later step justified only by measured demand, clear security semantics, and evidence that external enforcement is insufficient.

### 2.1 Terminology

**ARB** is the governance token of the Arbitrum ecosystem. It is not the software stack. This note uses **Arbitrum Orbit** in the established sense of a customizable Arbitrum chain and notes that current Arbitrum materials increasingly use **Arbitrum Dedicated Blockchains** or **Arbitrum Platform**.

### 2.2 Settlement and data availability

An Orbit chain may use rollup data availability on Ethereum, an AnyTrust data-availability committee, or another supported arrangement. This choice affects transaction cost and security, but it does not remove temporal contention inside the sequencer.

TLM accounting must keep the following components separate:

```text
total user payment = L2 execution cost + parent-data cost + temporal charge + other ordering charge.
```

Subsidizing temporal service should not silently transfer parent-chain data costs unless the design states that intention.

### 2.3 Rollup-as-a-service as a deployment path

The dedicated-chain path in the target table above is now a product. Rollup-as-a-service providers deploy application-specific chains without building chain infrastructure from source. Caldera deploys such chains on Arbitrum Orbit, the OP Stack, Polygon CDK, the ZK Stack, and Eclipse SVM, with configurable data availability, gas token, and sequencing. Its Metalayer connects deployed rollups for cross-rollup messaging under shared security.

Published block-time figures for these chains are vendor-stated, undated, and inconsistent between sources, ranging from about ten milliseconds to about 250 milliseconds. This note uses them only to establish that sub-second sequencing is available on the dedicated-chain path, not as a parameter. Any implementation must measure the block time of the chain it runs on.

Three consequences for this agenda:

1. **It lowers the implementation cost named in sec. 1.** A TLM deployment can configure sequencing and fee parameters on a dedicated chain rather than standing up Nitro from source.
2. **Sub-second block production separates ordering from fee feedback.** Nitro's backlog drains once per second (sec. 4), while a rollup-as-a-service chain may sequence more frequently. RN-25 nevertheless clears the initial mechanism per L2 block and treats TLA rank as logical order, not as a millisecond service class.
3. **A rollup network gives the cross-layer horizon of sec. 1 a concrete substrate.** Temporal contention across interconnected rollups, and the settlement waits in sec. 1's layers 2 and 3, become observable rather than only argued. This connects to RN-09's chain-virtualization treatment.

A rollup-as-a-service chain still runs an operator-controlled sequencer. It lowers implementation cost but retains the baseline chain's trust assumptions about candidate formation and arrival order (secs. 5.2 and 6.1).

### 2.4 What transfers to other stacks

The note is written against Nitro because Nitro's fee controller and Timeboost are concrete. Two parts of the argument transfer to the OP Stack, Polygon CDK, and the ZK Stack; one does not.

Transfers: the sequencer is a single ordering authority with direct control over position, so the TLA interface (sec. 5), in-place sorting (sec. 6), the block-local mechanism (sec. 9), and the implementation sequence (sec. 13) apply as written; and the baseline problem of secs. 5.2 and 6.1 is a property of single-sequencer operation rather than of Nitro.

Does not transfer: sec. 4's backlog controller. The OP Stack uses an EIP-1559-style per-block update rather than a continuously draining backlog, so the fee dynamics in sec. 12.2 have to be re-derived per stack. Quantitative results in this note are Nitro results until they are repeated elsewhere.

---

## 3. L2 block, L1 block, and logical order

An Arbitrum L2 block is an ordered L2 execution object created by the sequencer. It is not a subdivision of an Ethereum block. Many L2 blocks may be produced while one 12-second Ethereum slot passes, and data associated with several L2 blocks may later be compressed and posted to Ethereum in a batch transaction. There is no one-to-one mapping between L2 blocks and L1 blocks.

The first RN-25 mechanism clears within one L2 block. Later batch posting to Ethereum is outside that mechanism.

| Object | Role in RN-25 |
|---|---|
| L2 block | clearing and realized-order boundary |
| participant position set | positions eligible for TLA permutation |
| logical TLA order | descending order of participating transactions by TLA |
| L2 batch | later data-publication object, outside the block-local mechanism |
| L1 block or slot | Ethereum inclusion object, outside the block-local mechanism |

RN-25 uses **logical order**, not “early and late bands of a quantum.” If the term *quantum* is retained for consistency with RN-15, it means a logical ordering class inside an L2 block, not a period of wall-clock time.

---

## 4. Nitro's base fee is a floor

Nitro charges a base fee for L2 execution. A transaction specifies a maximum fee, and the transaction does not execute if the current base fee exceeds that maximum. Nitro therefore has an admission floor analogous to the relevant EIP-1559 condition:

```text
m_i>= b_t.
```

Nitro also has a configured minimum base fee `F_0`. Its execution-price function is based on a **gas backlog** `B`, a running measure of accumulated work, rather than on parent-block utilization. The backlog rises when work is consumed and drains over time:

```text
B <- B + G
```

when a transaction consumes `G` NitroGas, and

```text
B <- max(B - T*S, 0)
```

after `T` seconds at sustainable speed limit `S`. The fee rises exponentially once the backlog exceeds a tolerance `B_0`:

```text
F(B) = F_0 * e^max(0, b*(B - B_0))
```

where `B_0` is the backlog tolerance and `b` a rate constant. The variables are therefore: `B` the gas backlog, `G` the NitroGas a transaction consumes, `S` the sustainable speed limit, `T` elapsed seconds, `F_0` the minimum base fee, `B_0` the tolerance, and `b` the rate constant.

**Source and dating.** The exponential form, the backlog accumulator, and the per-second drain are as described in the Arbitrum gas and fees documentation, read 15 September 2026, which gives the base fee as an exponential function of the backlog with one constant controlling the rate of escalation and one allowing a small backlog before escalation begins, and states that the speed limit is subtracted from the backlog on each one-second clock tick, floored at zero. The speed limit on Arbitrum One is documented at 7,000,000 gas per second. `F_0`, `B_0`, `b`, and `S` are chain configuration, so a dedicated chain sets its own. The equations above are this note's notation for that mechanism, not quoted source code; an implementation must be checked against the ArbOS version it runs.

Two consequences follow. Nitro represents congestion as accumulated work over time rather than as block-by-block utilization. The fee controller moves at one-second resolution while L2 blocks and transaction ordering may move faster, so ordering and congestion feedback operate on different clocks. The block-local TLA rule does not require those clocks to coincide.

### 4.1 Consequence for TLM: exclude below-base-fee funding

RN-15 studies transactions whose own fee ceiling is below the current base fee. RN-25 does not import that rule. Every transaction submitted by the ordering proxy must satisfy Nitro's ordinary fee and validity checks on its own.

The initial mechanism therefore uses temporal payments only for a separate scheduling service and provider compensation. It does not use consumer funds to cure an invalid fee authorization. This keeps L2 execution pricing, estimated parent-data charges, and temporal settlement as distinct accounting components.

### 4.2 Physical gas still counts

Provider-funded execution is not physically cheaper. Every admitted transaction must count fully toward NitroGas usage and any multidimensional resource limits. TLA may inform economic scheduling or forecasts, but it cannot discount execution in safety accounting.


### 4.3 Priority fees and the base-fee floor

Arbitrum does not have one priority-fee policy across all chains. ArbOS Elara added configurable priority-fee collection for dedicated Arbitrum chains in August 2026. Arbitrum One did not simultaneously adopt priority-fee ordering; a Priority Gas Auction remains a separate governance question. RN-25 therefore treats priority fees as chain configuration, not as a universal Arbitrum rule.

The initial mechanism keeps the Nitro base fee as an execution-admission floor. A future sponsored variant could permit a paymaster or positive-TLA pool to pay part of a sender's execution charge, but the full base fee must still be paid by someone. That extension is separate from the ordering market specified here.

---

## 5. Minimal TLA interface

The first block-local implementation does not require the full TEP or TSP schema. It needs an ordinary valid transaction and a signed TLA instruction:

```json
{
  "transaction_hash": "0x...",
  "tla_wei": "...",
  "candidate_l2_block": 12345,
  "nonce": 7,
  "expiry_l2_block": 12346,
  "signature": "0x..."
}
```

Absence of this instruction means opt-out. Presence means participation; therefore `tla_wei = 0` may be retained as a participating neutral value if an implementation needs it. The design must not use the same representation for opt-out and participating zero.

The TLA value has two functions:

- its signed scalar determines participant order; and
- when positive, it caps temporal payment, while a negative value marks supply and can encode a provider reservation magnitude.

These functions may later be separated into two fields if incentive analysis shows that one scalar is too restrictive. The initial implementation keeps the RN-15 form so that the comparison is direct.

### 5.1 Two commitments and two verification levels

Let `P_k` be the participating transactions included under one clearing rule in block `k`. Before applying TLA sorting, the sequencer commits to its baseline candidate order and participation map:

```text
H_k = H(k, ordered candidate hashes, participation flags, signed TLA instructions).
```

The commitment must be fixed before the sorted block is released. The sequencer later reveals the committed list, or publishes data sufficient to reconstruct it.

Sort participants by descending TLA across the positions assigned to participants, using baseline participant order as the tie-breaker. The realized block is ordering-compliant when:

```text
project(B_k, P_k) = sort(P_k, descending TLA, baseline tie-break).
```

This creates two verification levels:

1. **Ordering verification.** Signed TLA values and the finalized block establish whether included participants follow descending TLA.
2. **Crossing and settlement verification.** The committed baseline additionally establishes which positive participants advanced across which negative participants and whether charges, payments, and refunds follow sec. 9.

### 5.2 What the commitment does not prove

The baseline commitment binds the sequencer to the order it states it would have used. It does not prove candidate-set completeness, truthful receipt times, or the absence of pre-commitment omission. Stronger claims require timestamped receipts, independent witnesses, a trusted execution environment, or a decentralized sequencing design.

RN-25 does not require those stronger systems for the initial experiment. It makes the narrower settlement claim relative to the committed baseline and requires the deployment to preserve any stronger arrival evidence the chain already records.

---

## 6. Opt-out-protected extension of FCFS

The initial design uses **in-place participant sorting**.

1. The sequencer applies its ordinary process and assigns candidate positions.
2. Positions assigned to opt-out transactions remain governed by the baseline policy.
3. Only transactions carrying a valid TLA instruction participate.
4. Participating transactions are sorted by TLA across the positions assigned to participants.
5. Opt-outs do not authorize their positions to be traded.

Suppose the sequencer's ordinary position assignment is:

| Position | Transaction | Status | TLA |
|---:|---|---|---:|
| 1 | A | participant | 10 |
| 2 | X | opt-out | — |
| 3 | B | participant | 50 |
| 4 | Y | opt-out | — |
| 5 | C | participant | 30 |

The participant positions are `{1,3,5}`. Sorting only participants produces `(B, X, C, Y, A)`. A arrived into the first participant position but executes in the last because its TLA is lowest. X and Y retain baseline treatment.

This is not global FCFS. It is an optional extension under which consenting transactions exchange relative order while opt-outs remain outside the exchange. The mechanism is procedurally neutral when participation is voluntary, the rule is disclosed, the same rule applies to all participants, and signed values determine the realized order.

### 6.1 Baseline inheritance and the added commitment

RN-25 inherits the chain's observation boundary and does not claim to prove true network arrival. It nevertheless raises the evidence required for **paid crossing settlement**: the sequencer must commit to the baseline candidate order before sorting. Public observers can then verify the added TLA relation, realized crossings, and settlement relative to that commitment. Candidate completeness and pre-commitment behavior remain under the baseline operator and audit assumptions.

### 6.2 Robinhood constraint

Robinhood Chain states that transactions are ordered by arrival and cannot bypass one another by paying higher fees. In-place TLA protects opt-outs, but participants do bypass one another by signed authorization. It therefore still departs from literal global FCFS. RN-25 presents it as a possible optional policy for a configurable Arbitrum chain, not as a description of Robinhood's current system or an adoption claim.

---

## 7. Why TLM is not Timeboost

Timeboost and TLM both recognize that relative order has economic value. Their market structures are different.

Timeboost auctions control of one express lane for a round. When a controller exists, its transactions avoid the configured delay applied to ordinary traffic. The default documentation describes a 60-second round and a 200-millisecond delay, both configurable. This creates one privileged intermediary and one binary service distinction: controller traffic and delayed traffic.

TLM operates at transaction level. Each sender can state a signed temporal position:

- positive TLA requests earlier participant order and authorizes payment;
- negative TLA supplies later participant order and may receive payment;
- absence of TLA preserves ordinary treatment.

The contrast is structural:

| Question | Timeboost | In-place TLA |
|---|---|---|
| Who buys priority? | one express-lane controller per round | individual participating transactions |
| How is service expressed? | access to the express lane | signed scalar ordering among participants |
| What happens to ordinary traffic? | configured delay when a controller exists | opt-out positions are not traded |
| Is there a paid flexibility side? | no | yes, through negative TLA |
| Where does latency competition remain? | inside controller submission and ordinary arrival paths | admission to the candidate block and TLA ties |
| Can payment reach flexible users? | not by the Timeboost rule | yes, through the Funding and Supply Legs |

### 7.1 The central argument

Timeboost monetizes the latency race by selling an express right to one intermediary. TLM changes the ordering variable for consenting transactions and routes part of urgent demand's payment to flexible demand. That distinction matters:

1. **Direct expression.** A transaction declares its own TLA instead of depending on access to the round controller.
2. **Two-sided clearing.** Positive authorization has a corresponding negative supply side. Timeboost collects willingness to pay for speed but does not reveal willingness to accept delay.
3. **Opt-out protection.** The initial in-place rule does not trade positions assigned to nonparticipants. Timeboost's configured delay applies to non-controller traffic when a controller exists.
4. **Auditable ordering rule.** Included participants can check whether descending TLA order was delivered. This is a different assurance from gaining access to an express submission channel.
5. **Reduced return to co-location among participants.** Once transactions enter the candidate set, participant-to-participant order is determined by TLA rather than arrival latency.

### 7.2 Evidence on concentration and spam

The concern is not hypothetical. Messias and Torres study more than 11.5 million express-lane transactions and about 151,000 auctions from April through July 2025. They report that two entities won more than 90 percent of auctions and that about 22 percent of time-boosted transactions reverted. Their title states the conclusion directly: *“The Express Lane to Spam and Centralization.”* Their interpretation is that Timeboost did not meet its stated fairness, decentralization, and spam-reduction goals during the observed period.[^timeboost-messias]

Later work does not make the empirical question one-sided. Zhu develops a model in which Timeboost can reduce duplicate transaction submission and reports a post-adoption decline in measured MEV-related spam relative to comparison L2s.[^timeboost-zhu] These studies use different spam definitions, periods, and identification methods. RN-25 should therefore not claim that Timeboost always increases spam. It makes the narrower claim that auctioning one express lane can concentrate control and does not by itself create transaction-level flexibility supply. Both claims can be tested directly.

The concentration result matters independently of the spam result. A one-winner auction can internalize revenue for the DAO while still placing the effective ordering interface behind a small number of recurrent controllers or resellers. TLA instead allows each participating transaction to submit a signed temporal value and creates an explicit negative side. This does not guarantee decentralization, but it makes provider participation, payment concentration, and realized order observable at transaction level.

### 7.3 Positive-sum objective and what TLM must prove

The temporal payment itself is a transfer: what the consumer pays is received by providers, the operator, or both. A transfer alone does not increase total welfare. The positive-sum case comes from changes in behavior and allocation:

- an urgent consumer receives a more predictable relative order and may avoid an expired opportunity;
- a flexible provider receives compensation for accepting later participant rank;
- the sequencer can receive a disclosed service fee rather than relying only on opaque latency advantages;
- other users may face less redundant traffic and fewer replacement submissions; and
- the ecosystem may spend fewer resources on private latency infrastructure that only changes relative rank.

These gains can make all participating sides better off relative to their alternatives. They can also fail. TLA can replace a technology arms race with a monetary bidding race, favor well-capitalized users, produce thin negative supply, or allow the sequencer to manufacture affiliated providers. The correct claim is therefore not that TLM is automatically positive-sum. It is that TLM creates a mechanism through which mutually beneficial intertemporal exchange is possible, while Timeboost is primarily a sale of privileged access.

Evaluation must compare Timeboost-like service and TLA under the same traffic and capacity, measuring latency expenditure, spam, controller and provider concentration, ordinary-user treatment, temporal payments, provider participation, and deadline outcomes.

If negative supply does not appear and TLA merely sells priority, Timeboost is the stronger deployed benchmark. If negative supply clears and reduces wasteful latency competition without harming opt-outs, TLM supplies a market function Timeboost does not have.

[^timeboost-messias]: Johnnatan Messias and Christof Ferreira Torres, [*The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost*](https://arxiv.org/abs/2509.22143), arXiv:2509.22143 (2025). The quoted words are the paper's title.
[^timeboost-zhu]: Brian Zhu, [*Does Timeboost Reduce MEV-Related Spam? Theory and Evidence from Layer-2 Transactions*](https://arxiv.org/abs/2512.10094), arXiv:2512.10094 (2025).

---

## 8. Relationship to forward blockspace markets

A forward market for Ethereum blockspace now operates outside consensus, and it is the closest economic neighbor to TLM outside the express-lane designs of sec. 7. On ETHGas, L2s and other buyers purchase L1 blockspace, and forward inclusion in it, from validators, with base-fee futures alongside and validator supply committed at scale, including ether.fi's reported three-year allocation. It is a market layer over the existing allocation, not a change to it.

The market supplies evidence that some users will pay for timed execution commitments. A rollup buying forward L1 inclusion for its batches would also express temporal demand at the L2-to-L1 posting layer. These facts support the broader TLM research agenda, but that cross-layer market is separate from RN-25's initial block-local ordering rule.

This market does not carry the paid flexibility side of sec. 1.3, and it is a discount-free sale of position rather than a compensation scheme. Whether that side clears against urgent demand in real traffic is a central empirical question for L2 deployment (sec. 15, question 1); sec. 14 states the same point as a hazard. If TLM only re-sells inclusion, a forward market already covers the useful part.

The layer is not the distinction. What separates the proposed L2 mechanism from a forward inclusion market is the paid flexibility side.

### 8.1 The sequencer holds both sides of the market

An L2 sequencer or batch poster can supply temporal service to L2 users and may also buy forward L1 inclusion for future batches. This places one operator on both sides of a cross-layer timing market. Forward purchase is optional rather than part of the ordinary rollup architecture, and analogous intermediary roles may also arise among L1 block owners and builders.

Three questions follow, all testable against markets that already operate.

**A committed posting slot is a deadline.** A sequencer or batch poster that has bought forward L1 inclusion has converted its own demand into deadline-shaped demand of the kind sec. 5.1 describes: work must be batched and posted by a fixed time or the purchased slot is wasted. An operator buying at spot has a decay curve instead. Whether the two behave differently when ordering their users' transactions is a direct question about temporal preference propagating down a layer.

**Knowing user deadlines should change what L1 inclusion is worth.** A sequencer that reads TEP deadlines knows how much of its pending work can wait past the next posting opportunity. That is the input to how far forward it should buy, and at what price. If declared temporal information lets an L2 buy L1 inclusion more cheaply for the same service, that is the TLM claim tested one layer up, against a priced market rather than a simulation.

**Smoothing below may not smooth above.** Sec. 14 notes that smoothing L2 execution can shift posting bursts to the parent chain. Stated as a market question: does a TLM-aware L2 reduce the variance of its own forward L1 purchases, or only relocate it? This is a cross-layer question, outside the block-local mechanism and outside the five questions of sec. 15; the forward market makes it measurable when the work reaches that stage.

---

## 9. Block-local TLA mechanism

### 9.1 Candidate and participation sets

For L2 block `k`, the sequencer forms its candidate set under ordinary practice and commits to its baseline order as specified in sec. 5. Let `P_k` contain candidates carrying valid TLA instructions and let `N_k` contain opt-outs. The sequencer freezes the positions assigned to `N_k` and permutes only `P_k` across participant positions.

The commitment makes the stated baseline binding for ordering and settlement. It does not establish that every received transaction was included in the candidate set.

### 9.2 Ordering

Participating transactions are ordered by descending TLA. Baseline participant order breaks equal TLA values. A participant gives up any claim to its prior participant rank. Positive TLA provides priority only relative to lower-TLA participants in the same clearing domain.

Nonce dependencies, atomic bundles, and other mandatory constraints must be resolved deterministically before settlement. A transaction that cannot occupy its TLA position without violating a declared constraint is either grouped into a disclosed dependency component or excluded from the clearing set. An implementation may not invoke an ad hoc exception after seeing the payment result.

### 9.3 Realized crossings

Let `r_i^0` be transaction `i`'s rank among participants in the committed baseline and `r_i` its realized participant rank. Positive participant `i` crosses negative provider `j` when:

```text
a_i > 0,
a_j < 0,
r_j^0 < r_i^0,
r_i < r_j.
```

Write `X_ij = 1` for this relation. A negative declaration alone creates no payment claim. Provider `j` is eligible only when it is successfully included and displaced later:

```text
d_j = max(r_j - r_j^0, 0) > 0.
```

A last-arriving negative participant that remains last has supplied no realized crossing and receives no provider payment. This rule ties the Supply Leg to a service visible relative to the committed baseline without claiming that the baseline proves true network arrival.

### 9.4 Funding, refunds, and invariants

For positive participant `i`, let `A_i = a_i` be its maximum temporal authorization, `q_i` its actual charge, `f_i` its refund, `x_ij` the amount it funds for provider `j`, and `phi_i` any separately disclosed operator fee. Require:

```text
0 <= q_i <= A_i,
x_ij > 0 only if X_ij = 1,
q_i = sum_j x_ij + phi_i,
f_i = A_i - q_i,
y_j = sum_i x_ij,
sum_i sum_j x_ij = sum_j y_j.
```

The mechanism therefore does not burn or silently retain unmatched authorization. If a consumer crosses no eligible negative provider, its provider-transfer charge is zero. Any operator charge must purchase a separately stated service and must not be described as provider compensation.

Every participating transaction still pays its ordinary Nitro execution and data charges. Temporal funding does not cure an invalid fee authorization in this initial mechanism.

### 9.5 Reference settlement: uniform price per matched rank unit

RN-25 uses a uniform-price crossing rule as its reference implementation. Let `z_ij` be matched rank units on eligible crossing edges. The deterministic matching procedure must satisfy:

```text
z_ij >= 0,
z_ij > 0 only if X_ij = 1,
sum_j z_ij <= max(r_i^0 - r_i, 0),
sum_i z_ij <= d_j.
```

At clearing price `pi_k`, charges and provider payments are:

```text
q_i = pi_k * sum_j z_ij + phi_i <= A_i,
y_j = pi_k * sum_i z_ij.
```

Choose the highest feasible matched quantity under a published deterministic matching and price rule, subject to consumer authorization and provider eligibility. Unmatched authorization is refunded and unmatched negative supply receives no payment. The reference implementation should initially set `phi_i = 0`; a later operator fee should be evaluated separately rather than hidden in clearing.

The exact price-selection rule, whether a posted price, a threshold price, or a uniform auction price, must be fixed before deployment. Simulation may compare these price selectors while preserving the crossing, budget-balance, and refund invariants above.

### 9.6 Alternative settlement choices

The reference rule is not claimed to be uniquely correct. Three alternatives remain within the same architecture:

1. **Pairwise pro rata:** distribute each consumer's actual charge only among the eligible providers it crossed.
2. **Pooled displacement:** pool actual charges and pay eligible providers in proportion to realized deferral; this treats temporal supply as a block-level commodity rather than a bilateral exchange.
3. **Marginal-provider settlement:** pay only the minimum provider set needed to support funded advancement under a deterministic matching rule.

All alternatives must preserve the sec. 9.4 invariants. In particular, pairing limits eligible transfers; it does not require the full authorization to be spent.

### 9.7 Verification and non-claims

Observers recompute the baseline commitment, participant positions, descending-TLA order, crossing graph, matched units, charges, provider payments, operator fees, and refunds. Settlement is valid only if these values follow the published rule.

The mechanism does not claim that the committed baseline is complete or that it records true network arrival. It claims only that the sequencer bound itself to that baseline before sorting and settled the resulting exchange consistently.

---

## 10. Value split between Ethereum L1 and L2s

Two figures, both as of 8 September 2026. DefiLlama reports about \$49.4 billion of DeFi TVL on Ethereum L1, against roughly \$9 to \$10 billion across the major L2s, led by Base, Arbitrum, and Robinhood Chain. L2BEAT and Growthepie measure value secured, which includes assets held or represented on an L2 whether or not they are in a DeFi application, and put the aggregate at roughly \$36 to \$38 billion. The two measures are not comparable, and bridge custody creates double-counting in any ecosystem-wide total, so this note does not compute a ratio from them.

Neither figure is the relevant one. TVL measures where capital sits; TLM studies execution demand over time, and L1 can retain most capital while L2s carry a large share of high-frequency execution. The measurements that would settle it are execution gas, transaction count, fee and sequencer revenue, latency, expiry and cancellation, and the temporal concentration of arrivals. Sec. 12.1 lists them as reporting requirements. Until they are collected, the size of TLM's addressable L2 demand is not established here.

---

## 11. Robinhood Chain: an Orbit chain with current economic activity

Robinhood Chain makes the Orbit discussion concrete. It is not an application deployed on Arbitrum One and it is not a separate L1. It is a dedicated Ethereum L2 built with the Arbitrum Platform, the current product and documentation name for the technology commonly associated with Arbitrum Orbit.

Its architecture can be summarized as:

```text
Robinhood applications and users
            |
            v
Robinhood Chain sequencer and Nitro execution
            |
            v
Arbitrum rollup contracts and bridge
            |
            v
Ethereum settlement and blob data availability
```

Robinhood Chain has its own chain ID, sequencer endpoints, transaction ordering, applications, and state. It uses ETH as its native gas token, posts data through Ethereum blobs, and connects to Ethereum through the canonical Arbitrum bridge. The chain therefore illustrates what an Orbit deployment provides: an operator can retain Ethereum settlement and EVM compatibility while selecting chain-specific execution and sequencing policies.

### 11.1 Why it is an important present example

Robinhood Chain is already economically material among Ethereum L2s. As of 8 September 2026, DefiLlama reports approximately:

- \$0.9 billion of application-level DeFi TVL;
- \$3.3 billion of bridged value;
- \$1.0 billion of stablecoins; and
- \$1.9 billion of DEX volume over the preceding 24 hours.

These figures are volatile and should be dated whenever reused. They nevertheless show that dedicated Arbitrum chains are no longer only development environments. Robinhood Chain combines current users, capital, trading, and tokenized-asset applications on a configurable L2.

These dashboard figures show current capital and activity, not temporal contention or willingness to supply delay. Robinhood Chain is therefore evidence that a dedicated Arbitrum chain can host economically relevant applications, but not evidence that a TLM market would clear there.

### 11.2 Workload relevance to TLM

Robinhood Chain's stated application focus includes tokenized real-world assets and financial services. That application mix can generate both urgent and flexible execution.

| Urgent demand | Flexible demand |
|---|---|
| liquidation | portfolio reconciliation |
| collateral protection | reporting and record updates |
| market execution | scheduled NAV calculation |
| arbitrage | batch settlement |
| immediate oracle use | delayed oracle summaries |

### 11.3 Ordering constraint

Robinhood Chain currently describes its sequencing policy as FCFS: ordering is determined by arrival time rather than a higher transaction fee. A paid bypass service would conflict with that stated commitment. This note therefore does not propose changing Robinhood Chain's current ordering policy without operator and community agreement.

Robinhood remains useful for a simulation of deadline-aware batching that preserves global FCFS, but such a scheduler would test information value rather than the paid two-sided mechanism.

**FCFS here is an operator commitment, not an externally complete arrival record.** The chain launched on 1 July 2026 and uses an operator-controlled sequencer. That sequencer could in principle delay, reorder, insert, or withhold. RN-25 does not require Robinhood or another Orbit chain to disclose an arrival trace it does not already disclose. An in-place TLA implementation would inherit the same baseline trust model and add only the disclosed TLA ordering relation among participants.

### 11.4 Oracle and stream example

The oracle example is relevant. One market event can produce:

- an urgent update for liquidation or trading;
- the same observation delivered later; and
- derived summaries over 1, 5, 10, or 15 minutes.

An Orbit chain serving tokenized markets could expose both transaction-level TEPs and stream-level TSPs. Transaction-level profiles are easier to prototype, but Robinhood Chain is relevant to TLM because recurring financial, oracle, reconciliation, and reporting flows can be described as streams rather than isolated transactions.

---

## 12. Evaluation framework

The L2 mechanism should be evaluated against at least three baselines:

1. FCFS with Nitro pricing;
2. Timeboost or another express-lane design; and
3. TLM with the same physical capacity and traffic.

### 12.1 Metrics

Report:

- latency by declared and realized class;
- deadline-weighted admitted value;
- transaction expiry and cancellation;
- provider participant rank and compensation;
- consumer authorization, charge, and refund;
- sequencer revenue;
- Nitro backlog and base-fee path;
- L2 execution and parent-data costs;
- physical utilization by resource;
- opt-out service quality and position preservation under available baseline records;
- ordering concentration;
- spam and replacement traffic;
- censorship and failover behavior; and
- distribution of benefits among users.

The same evaluation should record the demand measurements sec. 10 identifies as missing: execution gas and transaction count by class, fee and sequencer revenue, realized latency, expiry and cancellation rates, displaced demand, and the temporal concentration of arrivals. These measures describe TLM's addressable L2 demand more directly than TVL.

### 12.2 Traffic models

Use:

- Poisson arrivals as an accounting baseline;
- Markov-modulated arrivals for quiet and burst regimes;
- Hawkes processes for event-driven clustering;
- periodic streams for oracle and settlement workloads; and
- empirical traces where available.

The Nitro controller should be simulated directly. Reusing Ethereum's once-per-block base-fee model would produce the wrong feedback dynamics.

### 12.3 Success condition

The first output is not a frontier improvement but an existence result: whether flexible supply cleared against urgent demand at all, and in what proportion, under real or realistic traffic (open question 1). A frontier gain reported without a cleared two-sided market is measuring a priority-only mechanism and should be labelled as such.

Given clearing, the target is not maximum utilization. The mechanism should then improve a frontier among:

- deadline completion;
- admitted demand;
- ordinary-user latency;
- fee stability;
- sequencer incentives;
- physical safety; and
- fairness.

---

## 13. Implementation sequence

### Stage 1: trace-driven simulation

- reproduce Nitro backlog pricing;
- construct the ordinary candidate order using the baseline available in the trace;
- freeze opt-out treatment and sort participants in place;
- compare FCFS, Timeboost-like express service, universal TLA sorting, and opt-out-protected in-place TLA;
- compare payment rules while holding TLA order fixed;
- model escrow, refunds, invalidity, nonce constraints, and atomic groups; and
- measure how much latency advantage remains at admission and equal-TLA ties.

### Stage 2: dedicated-chain ordering service

- accept ordinary transactions and optional signed TLA instructions;
- use the chain's existing candidate formation and recordkeeping;
- escrow positive authorizations;
- apply in-place participant sorting before block construction;
- publish signed TLA values, realized participant order, charges, payments, and refunds; and
- preserve any arrival evidence the chain already records or exposes.

The ordering service must publish or reveal the committed baseline needed for crossing settlement. It need not publish exact receipt timestamps or claim that the committed list is a complete network-arrival trace. A chain that wants stronger candidate and opt-out auditing may add receipts or independent witnesses.

### Stage 3: evidence threshold for in-protocol work

An in-protocol proposal should begin only after the first two stages establish:

- recurring positive authorization and negative supply under real or trace-calibrated traffic;
- a settlement rule that balances without discretionary subsidy;
- a bounded manipulation surface;
- a measurable reduction in latency expenditure or improvement in temporal welfare;
- acceptable treatment of opt-outs; and
- a specific failure of external enforcement that chain validity would solve.

Only then should work consider a typed transaction field, ArbOS validation, chain-state settlement, or a formal Arbitrum governance proposal. This sequence is practical, not a claim that external services are sufficient in the long run.

### Other later work

- richer TEP fields and TSP reservations;
- RN-16-style persistence across L2 blocks;
- below-base-fee sponsorship;
- interaction with Timeboost controllers;
- cross-layer L1 posting markets; and
- decentralized sequencing and stronger arrival evidence.

---

## 14. Risks and limitations

### Sequencer discretion

A centralized sequencer may ignore temporal declarations, favor affiliated order flow, or misreport ordering. In-protocol enforcement could improve accountability, but it should follow evidence from the out-of-protocol deployment rather than precede it.

### False urgency and false flexibility

Users may manipulate declarations. Payment consequences can reduce but not eliminate this behavior.

### FCFS degradation

In-place sorting protects opt-out positions relative to the committed baseline. The commitment makes that preservation auditable for listed candidates but does not prove candidate completeness or truthful receipt times. TLA participation abandons baseline rank among participants by design.

### Double charging

Timeboost, priority fees, forward blockspace contracts, TLA, and TSP reservations may charge for overlapping temporal service. The mechanism must define what each payment purchases.

### Thin provider supply

Some application mixes may contain many urgent consumers but few transactions willing to wait, and a two-sided market cannot be assumed to clear. This is the bet stated in sec. 1.3: urgent demand is demonstrated, flexible supply is not. A related failure is subtler. Demand that would accept a discount for waiting may decline a compensated position, because compensation requires opting in, holding a baseline rank, and being seen to be displaced. Flexible traffic could then exist on the chain and still never enter the Supply Leg.

### Capacity confusion

Temporal-liquidity supply is not physical capacity. Delayed transactions eventually require execution and data availability.

### Cross-layer effects

Smoothing L2 execution may shift data-posting bursts to the parent chain rather than remove them. L2 and L1 costs must be measured together. Sec. 8.1 states the same effect as a market question, measurable against the forward blockspace market.

### Proxy operator conflict

The sequencer can favor affiliated participants, omit transactions from the candidate set, or manufacture provider flow. TLA ordering is auditable only over the included participants and signed values that become visible. A deployment must report operator affiliation and provider concentration.

### Governance and concentration

An operator-controlled temporal market may become another source of rent or preferential access. Operation on a dedicated chain does not by itself establish that the design is suitable for a neutral shared L2.

---

## 15. Open questions

Five questions determine the first phase:

1. **Does the market form?** Does negative-TLA supply appear in the same L2 blocks and in sufficient quantity to clear against positive authorization?
2. **Does it reduce waste?** Does in-place TLA reduce redundant submission, replacement traffic, co-location advantage, or other participant-to-participant latency expenditure?
3. **Which price selector works?** Given the crossing and refund invariants, should matched rank units use a posted price, threshold price, or uniform auction price?
4. **Can manipulation be bounded?** Can eligibility, accounting, and disclosure limit affiliated provider flow, false flexibility, and sequencer self-dealing while preserving opt-out treatment?
5. **Does it improve on Timeboost?** Under the same traffic and capacity, does TLA improve temporal welfare, participation, and concentration relative to Timeboost-like express service?

Secondary design, implementation, cross-block, and cross-layer questions are maintained in the companion note [**RN-25 Open Questions**](RN-25-Open-Questions_v1.0.md) rather than expanding the main argument.

---

## 16. Claims and non-claims

### Claims made here

- FCFS does not give a sender certain relative position before L2 execution.
- In-place TLA replaces arrival rank with signed TLA rank among consenting, included participants.
- Public TLA compliance can be checked from signed TLA values and the realized participant order.
- Relative to the committed baseline, a negative participant supplies compensable service only when an eligible positive participant crosses it and funded matching occurs.
- Opt-outs retain their positions relative to the committed baseline; crossing-based settlement adds a baseline-order commitment but does not claim to prove true arrival or candidate completeness.
- Positive TLA creates a Funding Leg, while negative TLA creates a transaction-level Supply Leg.
- No deployed blockchain execution market pays a participant to accept a later position.
- A discount for waiting and a payment for yielding are different instruments, and only the second requires a committed baseline.
- Timeboost sells an express-lane right but does not create this paid flexibility side.
- TLA can reduce the return to latency investment for relative ordering after candidate admission.
- The out-of-protocol path can test the central market claims at lower coordination cost; it does not replace the in-protocol research program for Ethereum or Arbitrum.
- TLM can support positive-sum exchange when improved urgent outcomes, provider compensation, and reduced latency waste exceed mechanism and displacement costs; the payment transfer alone is not a welfare gain.

### Claims not made here

- that TLA proves a global arrival order or candidate-set completeness;
- that advancement relative to the committed baseline proves improvement relative to true network-arrival order;
- that the committed baseline proves truthful receipt times or candidate-set completeness;
- that TLA eliminates the race to enter a candidate block;
- that monetary bidding is inherently fairer than latency competition;
- that negative supply will be deep enough to clear;
- that demand-response or denied-boarding mechanisms transfer to a chain, beyond showing that a paid flexibility side clears where the entitlement is settled first; or
- that Arbitrum, Robinhood, or Timeboost operators intend to adopt TLM.

---

## 17. Conclusion

The simplest Arbitrum counterpart to RN-15 is a block-local, opt-in ordering market. The L2 block is the clearing boundary. The sequencer retains its ordinary candidate process, leaves opt-outs under baseline treatment, and sorts participating transactions in place by signed TLA. A participant may occupy the first position in the committed baseline and execute later because higher-TLA participants rank ahead. That result is compliant: TLA sells a disclosed ordering rule and a settlement measured against the commitment, not proof about true network-arrival order.

Settlement uses a committed baseline rather than an unrecorded hypothetical counterfactual. The sequencer binds itself to that baseline before sorting; observers then verify realized crossings, charges, payments, and refunds. This does not solve the arrival-witness problem: the commitment proves consistency with the stated baseline, not completeness or truthful receipt time.

The comparison with Timeboost is substantive. Timeboost auctions a privileged lane to one controller and delays ordinary traffic when that lane is active. TLM lets individual transactions express temporal demand and supply, protects opt-outs under the in-place design, and allows urgent payments to compensate flexible participants. If that supply side clears and latency expenditure falls, TLM provides a function Timeboost does not. If it does not, the deployed express-lane model remains the stronger account of L2 demand for time.

The first research task is therefore concrete: implement in-place TLA sorting in simulation, compare it with FCFS and Timeboost-like service under the same candidate sets, and measure provider supply, payment concentration, latency-race reduction, opt-out treatment, and Nitro backlog effects.

This is also an adoption strategy. Ethereum remains the main L1 setting for the EIP-1559 extension, but a mature L1 should demand a high evidentiary standard and a deliberate review process. Arbitrum provides a shorter route to a controlled test without reducing the rigor of the mechanism or evaluation. Evidence from that test can determine whether TLA should remain an external sequencing service or advance toward chain-enforced semantics.

---

## Acknowledgment

The distinction between an early out-of-protocol deployment and a later in-protocol proposal was sharpened by feedback in a meeting with Norman Saade of the PBS Foundation. The note's mechanism, analysis, and remaining claims are the responsibility of the TLM Research Program; this acknowledgment does not imply endorsement by Norman Saade or the PBS Foundation.

---

## References

- Arbitrum. **Arbitrum documentation.** https://docs.arbitrum.io/
- Offchain Labs. **Arbitrum Nitro: A Second-Generation Optimistic Rollup.** https://docs.arbitrum.io/nitro-whitepaper.pdf
- Arbitrum. **Gas and fees** (exponential base fee in the gas backlog, per-second speed-limit drain, Arbitrum One speed limit of 7,000,000 gas per second). Read 15 September 2026. https://docs.arbitrum.io/how-arbitrum-works/deep-dives/gas-and-fees
- Arbitrum. **ArbOS Elara: Compliance Filtering, Priority Fee Support** (configurable priority-fee collection for dedicated blockchains; Arbitrum One PGA remains separate). 20 August 2026. https://blog.arbitrum.io/arbos-elara/
- Arbitrum. **Dynamic pricing for Arbitrum chains** (which pricing parameters a dedicated chain configures). Read 15 September 2026. https://docs.arbitrum.io/launch-arbitrum-chain/configure-your-chain/common/gas/dynamic-pricing-for-arbitrum-chains
- Arbitrum. **How Timeboost works** (default 60-second round, default 200 ms arrival delay outside the express lane, delay applied only when a round has a controller). Read 15 September 2026. https://docs.arbitrum.io/how-arbitrum-works/timeboost/gentle-introduction
- Arbitrum. **Timeboost for Arbitrum chains** (round and delay as chain configuration). Read 15 September 2026. https://docs.arbitrum.io/launch-arbitrum-chain/chain-config/sequencer/timeboost
- Arbitrum. **Timeboost is Now Live on Arbitrum.** https://blog.arbitrum.io/gattaca-titan-timeboost-live-on-arbitrum/
- Johnnatan Messias and Christof Ferreira Torres. **The Express Lane to Spam and Centralization: An Empirical Analysis of Arbitrum's Timeboost.** arXiv:2509.22143. https://arxiv.org/abs/2509.22143
- Brian Zhu. **Does Timeboost Reduce MEV-Related Spam? Theory and Evidence from Layer-2 Transactions.** arXiv:2512.10094. https://arxiv.org/abs/2512.10094
- Arbitrum. **L1 vs L2: Choosing the Right Chain Architecture.** https://blog.arbitrum.io/l1-vs-l2-choosing-the-right-chain-architecture-for-your-enterprise/
- Arbitrum. **Robinhood Chain mainnet is live, built with the Arbitrum Platform.** https://blog.arbitrum.io/robinhood-chain-mainnet/
- Robinhood. **Robinhood Chain documentation.** https://docs.robinhood.com/chain/
- Caldera. **Rollups-as-a-Service and the Metalayer.** Vendor material; block-time figures are undated and inconsistent between sources. https://caldera.xyz/ and https://caldera.xyz/blog/what-is-a-rollups-as-a-service-raas
- ETHGas. **Our Technology: Overview** (external blockspace market: inclusion and execution preconfirmations, micro-intervals, and announced base-fee products). https://docs.ethgas.com/
- ETHGas. **Blockspace Futures Market launch.** PRNewswire, 19 December 2025. https://www.prnewswire.com/news-releases/ethgas-debuts-ethereums-blockspace-futures-market-with-800m-of-commitments-and-12m-seed-round-led-by-polychain-capital-302646868.html
- ETHGas and ether.fi. **Institutional blockspace markets, three-year validator commitment.** The Block, April 2026. https://www.theblock.co/post/397457/etherfi-3-billion-eth-validator-liquidity-ethgas-three-years
- US Federal Energy Regulatory Commission. **Order No. 745, Demand Response Compensation in Organized Wholesale Energy Markets** (payment for measured curtailment against a customer baseline). 2011.
- US Department of Transportation. **14 CFR Part 250, Oversales** (denied-boarding compensation to a passenger holding a confirmed reservation who accepts later transport). Cited for the entitlement structure in sec. 1.3, not as a market design.
- IETF. **RFC 8622, A Lower-Effort Per-Hop Behavior (LE PHB).** 2019. (Yielding traffic marked without compensation; the discount-without-payment case in sec. 1.3.)
- DefiLlama. **Ethereum chain TVL.** https://defillama.com/chain/ethereum
- DefiLlama. **Base, Arbitrum, Robinhood Chain, OP Mainnet, Starknet, Mantle, and Linea chain TVL pages.** https://defillama.com/chains
- L2BEAT. **Ethereum L2 value secured.** https://l2beat.com/scaling/summary
- Growthepie. **Ethereum L2 value secured.** https://www.growthepie.com/chains
- TLM Research Program. **RN-01: Temporal Execution Profile.**
- TLM Research Program. **RN-02: Protocol-Visible Temporal Abstraction.**
- TLM Research Program. **RN-04: Temporal Service Architecture.**
- TLM Research Program. **RN-05: Supply-side Heterogeneity and Temporal Granularity.**
- TLM Research Program. **RN-06: Monad, A Temporal-Liquidity Analysis.**
- TLM Research Program. **RN-09: Chain Virtualization in TLM.**
- TLM Research Program. **RN-12: Temporal Liquidity Market Mechanism Design.**
- TLM Research Program. **RN-13 Part II: Capacity and Welfare in Blockchain Execution Systems.**
- TLM Research Program. **RN-14: The Demand Ethereum Does Not Serve.**
- TLM Research Program. **RN-15: A Temporal Liquidity Authorization for EIP-1559.**
- TLM Research Program. **RN-16: A Two-Leg Temporal Liquidity Reserve for EIP-1559.**
- TLM Research Program. **RN-17: Temporal Service Profiles and Future Execution Tickets.**
- TLM Research Program. **RN-33: Horizontal Temporal Service Classes for Monad.**
