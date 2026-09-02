---
title: "RN-06 - Monad Through the Temporal-Liquidity Lens: Motivation, Novelty, and Limits"
status: "Canonical single version - public research note, offered in good faith for comment."
version: "0.4"
date: August 12, 2026
spirit: >
  Offered in good faith and in admiration of Monad's engineering. The assessment in sec. 4 is
  candid, and some of it is deliberately controversial - but it concerns limitations
  *relative to the temporal-demand problem this program studies*, not Monad's own execution
  goals, which it achieves impressively. Disagreement and correction are actively welcome.
sourcing: >
  Facts verified July 2026 against Monad's documentation (primary) and reputable secondary
  sources; where a claim rests on secondary sources it is flagged. Primary-source pointers
  and corrections welcome.
---

# RN-06 - Monad Through the Temporal-Liquidity Lens

## 0. Thesis, in one line

Monad is a serious attempt to remove Ethereum's execution ceiling *without* changing Ethereum's semantics. It is a supply-side achievement: the same ordered stream, executed far faster. Read through the Temporal Liquidity lens, that is also its boundary - **Monad optimizes how fast the single ordered stream executes, and leaves untouched what users can express about *when, in what order, and how predictably* they execute.** The demand-side market is the same on Monad as on Ethereum. And Monad's very success - 400ms blocks, sub-second finality - *sharpens* the temporal problem TLM studies, because the finer time gets, the more decisive timing becomes.

So the relationship is **complementary layers, not competition**: one concrete thing TLM can offer Monad (workload shaping, sec. 3), one large thing Monad does not attempt (enriching temporal demand, sec. 4), and a turn (sec. 5) in which that omission looks less like a limit than an *opportunity* - a demand-side layer, and ultimately a fee-mechanism framework, that could expand Monad's ecosystem and Ethereum's at large.

---

## 1. What motivates Monad

**The diagnosis.** Ethereum's throughput ceiling is not primarily consensus - it is the *execution and state layer*: single-threaded EVM execution, sequential Merkle-Patricia-Trie state access on a general-purpose key-value store (heavy random I/O), and the monolithic coupling of consensus and execution so that ordering waits on execution. Each is an engineering bottleneck, not an economic law.

**The bet.** Deliver ~10,000 TPS on a decentralized L1 while preserving **100% EVM equivalence** - identical bytecode semantics, identical developer and user experience - by re-architecting the layers *beneath* the transaction market rather than changing the market itself. Keep Ethereum's ecosystem (apps, tooling, wallets, mental model); remove the performance ceiling underneath it.

**The competitive frame.** Monad aims to win the "high-performance L1" category on both flanks: Solana-class throughput *with* EVM compatibility (speed without the non-EVM developer tax), and better latency and cost than Ethereum L1/rollups without asking anyone to leave the EVM. EVM-equivalence is a strength and a constraint at once: it is why adoption is cheap, and - as sec. 4 discusses - why the demand-side market is held fixed.

The through-line for this note: **Monad's motivation is throughput and compatibility, not market expressiveness.** It does not ask whether the single ordered stream is the right economic object; it takes the stream as given and makes it fast.

---

## 2. What is new in Monad

Four re-architected layers, plus a pipelining discipline that ties them together. (Figures verified July 2026; see References.)

**Asynchronous / deferred execution.** Consensus (ordering) is decoupled from execution. Validators agree on and vote on a block's *ordering*; execution happens afterward, in a separate pipeline. Nodes commit to a schedule first and execute second, so execution no longer sits on the consensus critical path. A consequence worth holding onto: the executed **state root lags the ordered block**, rather than being agreed in-band as on Ethereum.

**Optimistic parallel execution.** Independent transactions run concurrently across cores; conflicting ones are detected and re-executed / re-ordered so the final result is bit-identical to strict serial EVM semantics. Parallelism is *discovered after ordering* - optimistic, then validated - not declared in advance.

**MonadBFT.** A HotStuff-family pipelined BFT protocol with **tail-forking resistance**: leaders re-propose supported blocks so honest blocks are not abandoned under network delay, enabling fast (~1s) single-slot finality across a large validator set.

**RaptorCast.** Block propagation via **Raptor erasure codes** over a two-level broadcast tree, each validator rebroadcasting chunks pro-rata to stake weight - so a proposer need not ship the whole block to everyone, cutting propagation latency and its variance.

**MonadDB.** A purpose-built state store holding Merkle-Patricia-Trie nodes **natively** (not embedded in a generic KV database), using **io_uring** for asynchronous disk I/O, and versioning trie nodes for efficient state sync - attacking the random-I/O tax that dominates EVM state access.

**Compiled/optimized EVM + gas details.** An optimized (compiled) EVM path; the EIP-1559 fee market kept intact; and one notable divergence - **fees are charged on the transaction's declared `gas_limit`, not `gas_used`** - a deliberate DoS / parallel-scheduling safeguard that also mildly penalizes over-provisioned limits.

**Headline numbers (verified):** mainnet live **Nov 24, 2025**; ~**10,000 TPS**, **400 ms** block time, **~800 ms** finality (~1s single-slot).

What is genuinely new is *not any single idea* (parallel EVMs, HotStuff, erasure coding, custom state DBs all pre-exist) but the **full-stack co-design**: every layer below the market rebuilt and pipelined together while holding EVM semantics fixed. That is the achievement - and the self-imposed ceiling.

### 2.1 The guiding analogy - a special-purpose distributed OS for a singleton ledger

Monad's achievement, and where it earns its respect, is **systems engineering**. The node is treated as a purpose-built distributed operating system tuned to one workload: a **singleton global ledger** - a single, shared, deterministically-replicated world state. Every classical OS subsystem is rebuilt for that one job:

- **Storage / filesystem + embedded DB:** MonadDB is a special-purpose store for one data structure (the Merkle-Patricia Trie), laid out in user space over NVMe with io_uring async I/O - a networking-grade file system / DB rather than a generic key-value store.
- **Scheduler:** optimistic parallel execution is a concurrency-control scheduler over the singleton state.
- **Network stack:** RaptorCast is a purpose-built, erasure-coded broadcast transport.
- **Kernel discipline:** deferred execution decouples ordering from execution the way a control plane decouples from a data plane.

This "node = specialized distributed OS + networking file system + embedded DB on SSD" analogy has clearly been a guiding force, and it yielded real results - because it correctly identifies the bottleneck as I/O and concurrency against one shared state, and attacks it with the right tools. This is disciplined, excellent systems work.

The precise conclusion: **Monad is an optimized *implementation* of the EVM, not a new computational or economic model.** Same instruction set, same semantics, same singleton ledger - forwarded faster.

Read this as praise with a boundary. In these terms Monad is an operating-system project - the node reimagined as a special-purpose distributed OS, and done very well. That is also where the ceiling sits: the next level is not more OS. It is **networking** - the subject of sec. 2.2.

### 2.2 The stronger analogy: control/data-plane decoupling - and the control plane Monad has left thin

sec. 2.1 credited Monad's operating-system-paradigm achievement. The step to the next level is a change of paradigm - from OS to **networking** - and it turns on the defining architectural idea of the last two decades of networking: **the decoupling of the control plane (policy - *what* should happen) from the data plane (forwarding - making it happen fast).** This is the analogy that carries Monad forward, and TLM is the lens for it.

The lineage is instructive because each step added intelligence to the *control* plane, not speed to the data plane:

- **The classic router** - an implicit split: routing protocols (BGP/OSPF) compute the forwarding table; ASICs forward at line rate.
- **GMPLS** - a *generalized* control plane spanning heterogeneous data planes (packet, TDM, wavelength, fiber): one control logic provisioning paths across multiple switching granularities.
- **SDN** - the split made *explicit and programmable*: a centralized, programmable control plane over dumb, fast forwarding elements. The value was never the separation itself; it was that the control plane became *software you could program* for traffic engineering, QoS, and admission control.
- **Its recent descendants** - **P4** (programmable data planes that enforce QoS at line rate), **SRv6 / segment routing** (policy encoded as coarse, stateless instructions carried *in the packet header*, source-routed end-to-end), and **5G network slicing** (multiple SLA-differentiated virtual networks over one physical substrate) [8].

**Monad has already performed the decoupling.** Deferred execution *is* a control/data-plane split: MonadBFT computes the ordering (control plane); the parallel EVM and MonadDB forward it at line rate (data plane). Architecturally, Monad is an SDN-era data plane - **but it runs a pre-SDN control plane**, one that is *thin and single-dimensional*: it computes a transaction order and a scalar EIP-1559 fee, but no demand-side policy - no classes, windows, reservations, or temporal differentiation. Ordering and a fee market are themselves policy (ordering is the MEV-relevant decision, sec. 4a); what is missing is not policy but the *demand-side* control the rest of this note describes. It is a programmable-forwarding substrate wired to a controller that computes order and price and nothing else.

That is the gap a demand-side layer fills, and TLM is the lens that names what the control plane should compute:

- **SDN -> a programmable control plane.** TLM is controller logic: classify demand, differentiate service, do admission control - the policy the ordering plane currently omits.
- **5G network slicing -> temporal service classes.** TLM's service classes (RN-04) are slices: SLA-differentiated virtual lanes over one shared ledger.
- **GMPLS -> multi-granularity control.** TLM's time × class × state-access structure (RN-05) is a generalized control plane over heterogeneous execution granularities - the blockchain analog of GMPLS unifying control across switching layers.
- **SRv6 / DiffServ -> coarse, stateless, in-band policy.** Modern networking converged on carrying policy as coarse, stateless markings *in the packet* (DiffServ codepoints, SRv6 segments). This is TLM's design constraint - coarse, neutral, stateless-friendly, declared in the transaction. **TLM's constraint is not a compromise; it is the same discipline the newest networking independently arrived at.**

So the analogy is not decorative. It says Monad built the forwarding substrate - programmable and decoupled - and left the control plane unbuilt; and it tells us, from a mature field, what that control plane looks like: QoS classes, slicing, admission control, coarse stateless in-band policy. That is the layer TLM specifies, and the direction in which Monad's architecture most naturally advances.

**As a trajectory:** Monad has done a great job as a special-purpose **OS project** - it made the singleton ledger fast. The next level is a modern special-purpose **networking project** for the blockchain: one whose control plane differentiates service, slices the substrate, and shapes traffic. The OS paradigm made execution fast; the networking paradigm - service differentiation, slicing, traffic engineering - is how that speed becomes expressible as a market. **TLM is the catalyst and the lens for that transition.**

**Beyond two planes - temporally layered control.** The networking lineage is itself moving *past* a single control/data split toward **multi-timescale control**: a slow, global control plane (O-RAN's Non-RT RIC, ≥1s) computing policy and optimization; a fast, local control layer (Near-RT RIC, 10ms-1s) doing bounded closed-loop adaptation; and a real-time, deterministic data plane (per-TTI scheduling) kept deliberately out of the slow loops. The blockchain analog is direct: multi-slot global coordination (capacity allocation, forward curve, a temporal-liquidity reserve) belongs in a *slow* control plane; per-slot admission and class assignment in a *fast* one; slot-level ordering stays simple and deterministic. The governing invariant - *a global, multi-slot decision is admissible only if it reduces to a per-slot parameter the data plane applies locally and deterministically* - is what keeps execution simple while coordinating demand across many slots. This layered-control architecture is TLM's structural foundation, developed in **RN-07 (in preparation)**.

An honest caveat, for the systems reader: unlike a stateless forwarding element, Monad's data plane *produces* state (the state root) that gates validity - so this is control/data separation *with a deferred feedback path*, not pure stateless forwarding.

### 2.3 Why the framing matters: the singleton concentrates contention

The singleton ledger is why OS optimization has a ceiling that a demand-side layer can lift. All demand contends on **one** shared state, so throughput is bounded not only by implementation speed but by the **conflict structure of the workload**. Optimistic parallel execution discovers conflicts *after* ordering; it cannot remove conflicts inherent in an undifferentiated stream. Partitioning demand into temporal service classes (own state domain, own cadence) reduces contention *by construction* - a **workload** change no amount of data-plane / OS optimization can substitute for. This gives the sec. 3.1 workload-shaping hypothesis a sharper cause: on a singleton state, temporal classification is a **first-class scaling lever, not merely an economic one**.

---

## 3. Where Monad sits relative to TLM

Monad improves nearly every layer *below* the transaction market while deliberately preserving Ethereum's semantics: one linearly ordered transaction stream, executed faster, committed in the original order.

- **Monad asks:** *how do we compute the ordered result faster?*
- **TLM asks:** *should every transaction receive the same execution service at all?*

```
Application
   |
Temporal demand  ->  service selection      <- TLM (above the market)
   |
Transaction ordering
   |
Execution engine                            <- Monad (below the market)
   |
Storage / Consensus
```

Different layers; complementary, not competing. A Continuous State service (RN-04) could *use* a Monad-class engine inside it: TLM selects the service; an engine like Monad accelerates execution within it. Service-to-engine need not be one-to-one.

### 3.1 The workload-shaping hypothesis

Monad discovers parallelism *after* ordering - optimistic execution against one ordered stream, validating dependencies afterward. A demand-side layer can act *before* ordering:

> **Classifying demand into temporal services before scheduling increases the parallelism available to any execution engine and reduces contention - regardless of which engine runs inside each service.**

In database terms: Monad improves the **concurrency-control algorithm**; temporal classification changes the **workload presented to it**. Separating a high-rate, conflict-heavy continuous stream into its **own state domain** (and own cadence) removes cross-class conflicts *by construction* - because the state is then disjoint, not because the work is labeled 'temporal.' The reduction comes from state-domain separation; temporal classification helps only where a class's timing tracks its state access, and where classes share hot state (a popular AMM pool, an oracle) there is no by-construction gain. The claim is therefore that classification *into separate state domains* changes the workload the executor sees. This is a systems-performance argument for classification that is **independent of the economic argument** - and it is quantifiable:

> **Proposed experiment.** Replay a historical or synthetic transaction mix through (a) one ordered stream, (b) conflict-aware scheduling, (c) temporal classification, and (d) joint temporal-and-conflict scheduling; measure state-access conflict rates and achievable parallel speedup under an optimistic-execution model, and account for classification, isolation, and re-execution overhead. Comparing (c) against (b) and (d) isolates the temporal contribution from the state-partitioning one. A material difference supports the hypothesis; none refutes it.

This is offered as a contribution, not a critique: a concrete, falsifiable systems claim that anyone is welcome to run or rebut.

### 3.2 The application roster - homogeneous by self-selection

**Verified snapshot (mid-2026).** The on-paper directory is diverse - 300+ projects across DeFi, DEX, perps, lending, liquid staking, stablecoins, NFT, gaming, social, prediction markets, AI, and infrastructure. But **activity, TVL, and volume concentrate heavily in DeFi and trading.** TVL (~$220M-$410M across the period) sits almost entirely in lending + DEX + perps + liquid-staking + stablecoins; a single order-book perpetuals venue runs ~$1.2B/month; the large early TVL landed in ported Uniswap/Curve/Morpho. Gaming, NFT, and social exist but are largely prototyping. Monad brands itself a "DeFi-first chain" and "the home of high-frequency finance." **The roster is homogeneous where it counts - concentrated in latency- and throughput-sensitive trading.**

**Why homogeneous - a self-selection mechanism.** Monad's principal differentiator versus Ethereum and its L2s is *speed* (identical EVM, identical semantics). So the applications with the strongest reason to prefer Monad are those **bottlenecked by speed**: high-frequency DeFi, on-chain CLOBs, perps, arbitrage, liquidation engines, high-rate market making. Applications that don't need speed gain little by leaving Ethereum's liquidity and network effects. The ecosystem therefore self-selects toward the speed-sensitive tail - **speed is a magnet with a narrow pull.**

**Why this matters here.**
- The applications Monad attracts are **those with the most differentiated temporal demand** - continuous order flow, hard deadlines (liquidations), ordering sensitivity, predictability and continuity needs. They are the demand-side dual of Monad's supply-side pitch.
- Monad has thus assembled the users whose temporal demands are most acute - high-frequency trading and on-chain order books, which turn on ordering, continuity, and protected execution, not price alone. A **scalar-fee, single-queue market** (Ethereum and its variants) collapses these into one scalar, willingness to pay for priority; and even a single-axis **urgency-vs-price tiering** (Kiayias) adds only one temporal dimension. Neither expresses the multi-dimensional temporal structure these users need - which is what RN-03 (the evidence) and RN-04 (the service classes) set out.

The orientation matters. Kiayias's tiering [7] is the clean theoretical treatment of one axis - well-suited to a mechanism-design proof. TLM's focus is the engineering counterpart: a multi-dimensional service architecture ported from networking QoS and the traffic-management practice of the internet's builders, not a new fee-mechanism theorem. The contribution we care about is systems engineering carried over from Web-scale networking, with the mechanism theory as a constraint rather than the goal.
- It bears on sec. 2.3 and sec. 4(c): homogeneity toward HFT/DeFi means **high contention on shared pools** (AMMs, books, oracles), where optimistic parallelism degrades and workload-shaping helps most.

**Honesty check.** "Homogeneous" means concentration of *activity and value*, not of the raw directory (diverse on paper). And launch-era DeFi concentration is partly a maturity artifact - DeFi ports fastest - so the mix may broaden over time. But the structural claim is durable: *speed self-selects speed-sensitive, temporally-rich demand.*

### 3.3 The Exit Argument - application sovereignty as revealed preference

*This section addresses the Ethereum-ecosystem reader (protocol researchers and the incentive-design community). It frames TLM less as a proposed mechanism than as a diagnosis of value the current market is already losing.*

**The observation - a pattern, not an anecdote.** The entire on-chain-perp / order-book class chose sovereign app-chains over Ethereum's general-purpose market: **dYdX v4** rebuilt on a Cosmos app-chain, **Hyperliquid** launched its own L1, **Aevo** runs off-chain matching with on-chain settlement. Different designs, same defection.

**The revealed preference.** These teams paid a steep price to leave - Ethereum's security, deepest liquidity, composability, and EVM tooling. Rational actors pay that price only when the general-purpose market fails to provide something first-order. Their stated reasons cluster into two drivers:
1. **Throughput** - a live order book needs constant place/cancel/modify flow Ethereum could not carry;
2. **Ordering / extraction control** - deterministic sequencing, front-running resistance, control over MEV and fee structure - i.e. *temporal and extraction control*.

**The decomposition that clarifies TLM's role.**
- **Monad neutralizes driver (1).** A fast, EVM-equivalent L1 removes the *throughput* reason to leave. If throughput were the only driver, a scaled Ethereum-equivalent would retain these applications.
- **Driver (2) survives Monad untouched.** Even a maximally fast general chain gives applications no protocol-native ordering protection and no way to express temporal service. That residual - temporal and extraction control - is what still justifies sovereignty. It is the space TLM studies.
- **In short:** *scaling removes the throughput reason to exit; a temporal layer removes the extraction reason. Neither alone closes the exit; together they do.*

**The cost to Ethereum.** Each exit is ecosystem fragmentation - Ethereum loses its highest-value, most latency-sensitive flow (the same HFT/DeFi segment sec. 3.2 shows Monad courting) to sovereign chains, along with security surface, liquidity, and composability. The fee market's **incompleteness along the temporal axis** is one driver of exit.

**A retention lever.** The Continuous State lane (RN-04 sec. 8) is designed to keep that flow *"inside the tent rather than on a sovereign chain"* - a demand-side service class delivering temporal / extraction control **without** leaving Ethereum's neutrality and shared security. Completing the temporal dimension of the market is a way to retain flow the general market is currently losing.

**An honest caveat.** Exit is multi-causal - app-chains also want their own token economics, sequencing-fee capture, and full-stack customization. Temporal and extraction control is a first-order but not the sole driver. What makes it the relevant one here is that it is the single exit driver Ethereum could address *without surrendering neutrality*. The argument deliberately concedes throughput to scaling and claims only the temporal/extraction driver.

---

## 4. Limits of Monad (relative to the temporal-demand problem)

A candid assessment, offered in good faith - and, in places, deliberately provocative. These are limits **relative to the problem TLM studies (the temporal structure of demand)**, not relative to Monad's own goal of fast, compatible execution, which it achieves impressively (sec. 4.1 makes this explicit). Ordered from most-central to most-general.

**(a) It optimizes supply and holds demand fixed - the core gap.** Monad keeps the scalar EIP-1559 fee market and the single global ordered stream exactly as Ethereum has them. Users still express only *price*; the temporal structure of demand (priority, delay tolerance, deadlines, predictability, continuity) stays implicit and un-priced. Monad makes the same price-only market run faster. This is progress in execution, not in market expressiveness - and by design, because EVM-equivalence forecloses demand-side redesign.

**(b) Faster blocks change the temporal race Monad does not mediate.** Compressing block time to 400ms makes some timing distinctions *more* decisive - latency, ordering position, and sub-slot placement matter more when slots are short - and Monad adds no protocol-level extraction resistance (no encrypted ordering, no protected windows, no temporal classes), so front-running and sandwiching persist. Whether the race *intensifies* or eases is not settled, though: shorter blocks also cut waiting time and the value of marginal priority, so the sign depends on the ratio of propagation delay to block interval, the auction cadence, and finality. Stated as a hypothesis, not a fact: **Monad made time finer, which makes the market for time more consequential - a market a temporal layer, not Monad, would mediate.**

**(c) Optimism degrades under exactly the workloads that matter.** Optimistic parallel execution excels when transactions are independent, but degrades toward serial (re-execution overhead) on hot, contended state - popular AMM pools, oracle updates, liquidation cascades - which is where value and MEV concentrate. Realized speedup is workload-dependent, and the high-contention case is the weak case. This is the opening for sec. 3.1: classifying before ordering attacks contention structurally rather than discovering it optimistically.

**(d) Deferred execution moves a cost rather than removing it.** Decoupling execution from consensus buys throughput, but the executed state root lags the ordered block. That complicates anything needing *executed-state* certainty at ordering time - instant cross-system confirmations, some light-client and bridging patterns, latency-sensitive composability. It is a sensible trade, but a trade, and it interacts with use cases that care about *when state is known* - itself a temporal property.

**(e) `gas_limit`-based charging is a real (if minor) pricing distortion.** Charging on declared rather than consumed gas protects the parallel scheduler but taxes users who cannot tightly predict consumption and nudges wallets toward conservative limits. A modest efficiency cost inherited from the parallelism design.

**(f) Performance raises the centralization floor.** 10k TPS with MonadDB (io_uring, fast NVMe), RaptorCast bandwidth, and state-growth pressure lifts validator hardware and networking requirements. The standard high-performance-L1 tension applies: throughput bought partly with steeper node requirements, with the usual long-run questions about validator-set breadth and geographic decentralization. Not unique to Monad, but not escaped by it.

**(g) EVM-equivalence is a strategic ceiling, not only a feature.** The advantage (cheap adoption) is also the cap: by binding itself to exact Ethereum semantics, Monad cannot itself introduce the multidimensional, temporally-aware market TLM describes. It is committed to being *fast Ethereum* - which leaves the demand-side frontier to a layer above it.

### 4.1 The fair counter-argument
Monad would reasonably say: *market redesign is not our job - we are the execution substrate, and neutrality and compatibility are the point.* That is correct, and it is why the framing throughout is "complementary layers," not "Monad is wrong." The limits above are limits **relative to the temporal-demand problem**, not relative to Monad's own stated goal - fast, compatible execution - which it largely achieves.

---

## 5. Does Monad *need* a demand-side layer? The first-adopter argument

The analysis so far treats Monad as substrate and TLM as a layer above it. There is a stronger reading: **Monad may be the natural first adopter of such a layer - because the very ecosystem it wants to grow is capped by the one layer it has not built.**

1. **Monad finished the hard supply-side work.** It has a fast, EVM-equivalent *forwarding plane* (data plane). What it has *not* built is the demand-side *control plane* - admission control and traffic management deciding which flows get which execution service.
2. **Throughput is commoditizing; demand-side service is the durable advantage.** Raw speed is becoming table stakes (several fast chains now exist). What lasts is serving demand *better* - and Monad's own target market (on-chain CLOBs, HFT DeFi; sec. 3.2) is the set whose value comes from temporal structure.
3. **Speed alone does not retain the defectors (sec. 3.3).** The applications Monad courts still have a reason to prefer sovereign chains: ordering and extraction control. A demand-side traffic manager - temporal service classes - is what closes that gap in-protocol.
4. **The upside is ecosystem *expansion*, not just retention.** With temporal service classes, application types become viable that neither Ethereum nor plain-fast-Monad can host: protected continuous markets, deadline-guaranteed execution, predictable streams. The addressable space grows along a dimension speed cannot reach.

**Networking restatement.** Monad built a fast router and left it running a single best-effort queue. Its highest-value users (trading) are the ones that most need QoS classes. Adding an admission-control / traffic-management layer is what lets a fast router offer differentiated service - and how the ecosystem expands beyond what forwarding speed alone can capture.

### 5.1 Honest objections (and why they are surmountable)
- **"It breaks EVM-equivalence / neutrality."** It need not for *default* traffic. The service classes are **opt-in and coarse** - a protocol-recognized virtual lane (RN-04 sec. 8) that leaves base EVM semantics and default traffic untouched. One distinction to keep: for transactions that *do* opt in, a different ordering, window, or state domain can change observable outcomes - gas, reverts, composability - even with identical bytecode. So what is preserved is **bytecode compatibility for all, and behavioral equivalence for default traffic** - not behavioral equivalence for opted-in traffic. This is the DiffServ lesson (add differentiated classes without touching the core forwarding path), with the honest rider that opting in is a behavioral choice, not a free marking.
- **"Admission control centralizes / picks winners."** The classes are defined by *temporal characteristics of demand*, not by identity or application - neutral by construction (any transaction declaring the characteristic qualifies). Extraction-resistance and neutrality are explicit design constraints.
- **"Not our layer - we do execution."** True today; but the boundary is a *choice*, and the ecosystem payoff sits just above where execution stops. Whether such a layer is built, enshrined, or merely hosted as a protocol-recognized lane is open.

### 5.2 In what spirit this is offered
The first-adopter reading is a **hypothesis offered for consideration, not a prescription.** Whether Monad - or Ethereum, or anyone - builds such a layer, hosts it as a recognized lane, or declines it entirely is their call; the contribution here is the analysis, not a demand on any team. It is offered in admiration of Monad's engineering, and in the belief that the most interesting next step for a chain that has largely solved execution is to serve demand *better*. It is meant to invite scrutiny - including the objection that this layer is unnecessary.

### 5.3 The wider point: TLM is a *framework*, and it carries a supply-side agenda

The first-adopter argument is still too small if it stops at admission control. The deeper value is that **TLM is a framework** - a lens, vocabulary, and methodology for seeing the temporal structure of demand - and once one adopts the lens, the gaps appear in the *fee mechanism itself*, not only in the service layer above it.

- **Demand side (Phase 1 - the model).** Classify and measure temporal characteristics of demand; the admission-control / traffic-manager layer (sec. 5).
- **Supply side (Phase 2 - the mechanisms, largely still to be designed).** The framework exposes concrete gaps in EIP-1559's scalar fee market and points toward *new protocol mechanisms* that price and coordinate temporal demand: a generalization of tiered fees (Kiayias et al. [7]) beyond urgency, temporal / windowed auctions, and a dynamic temporal-liquidity reserve (an open research direction). These are **protocol-level (EIP-scale) questions**, not application features.

Two things make this an agenda rather than a wish:
1. **The users are already identified.** The gap is not hypothetical - its constituency is the defector set (sec. 3.3) and Monad's own HFT/DeFi roster (sec. 3.2). A fee-mechanism enhancement that prices temporal demand ships with a ready user base and a measurable retention/expansion case, not a search for one.
2. **It advances both ecosystems at once.** For Monad, it is the mechanism layer that turns "fast Ethereum" into a strong home for temporally-rich finance. For Ethereum, it is a supply-side fee-mechanism research agenda - what EIP-1559 left on the table along the temporal axis. And a fast general-purpose chain, less bound by Ethereum's governance timelines and already serving these users, is a natural place to **prototype** a mechanism Ethereum could later adopt.

**A necessary caveat.** These supply-side mechanisms are a research *agenda*, not finished results - some sketched, most open. The honest framing: *TLM is the framework that identifies what is missing and the users who need it; the mechanisms that fill the gap remain open problems, to be built with collaborators.* This note does not claim them solved.

> **Net:** TLM is not merely a demand-side layer to bolt on. It is a framework that (a) names the missing temporal dimension of the fee mechanism, (b) comes with an identified user base, and (c) opens a supply-side, EIP-level mechanism agenda - a way to advance a fast chain's ecosystem *and* Ethereum's at large.

---

## 6. Takeaways

1. **Monad and TLM are complementary layers, not competitors** - Monad the execution substrate, a temporal layer the demand-side policy above it.
2. **Workload shaping is a concrete, testable systems claim (sec. 3.1)** - classifying demand before ordering may raise achievable parallelism; the proposed experiment is offered for anyone to run or refute.
3. **The temporal race sharpens as blocks get faster (sec. 4b)** - Monad made time finer, so the market for time matters more.
4. **App-chain exit is evidence, not anecdote (sec. 3.3)** - and the temporal/extraction driver is the one Ethereum could address without ceding neutrality.
5. **The opportunity (sec. 5)** - a fast chain that has solved execution can expand its ecosystem by adding a demand-side layer; offered as a hypothesis, not a prescription.
6. **Next step** - run the sec. 3.1 experiment; it converts the note's central systems claim into evidence. Contributions and rebuttals are welcome.

---

## References

[1] Monad Documentation. https://docs.monad.xyz/ - architecture, async/deferred execution, opcode/gas model. *(Primary.)*

[2] Monad architecture overviews - MonadBFT (HotStuff-family, tail-forking resistance), RaptorCast (Raptor erasure codes, stake-weighted broadcast tree), MonadDB (native MPT, io_uring, versioned nodes), optimistic parallel execution.

[3] Monad mainnet - public mainnet live **Nov 24, 2025**; ~10,000 TPS, 400ms blocks, ~800ms finality. *(Secondary: Backpack Learn, Messari, CoinGecko, Blockworks Research.)*

[4] Monad gas model - EIP-1559 base+priority fee retained; EVM-equivalent opcode pricing; fees charged on declared `gas_limit` not `gas_used`. *(Monad docs, "Opcode Pricing"; category.xyz gas-limit note.)*

[5] Monad ecosystem / roster (mid-2026) - DeFi-first concentration; ~$220M-$410M TVL; order-book perp venue ~$1.2B/month; 300+ directory projects; "home of high-frequency finance." *(Secondary: Backpack Learn "Monad Ecosystem"; blog.monad.xyz; Messari.)*

[6] App-chain exit pattern - dYdX v4 migration from Ethereum/StarkEx to a Cosmos app-chain citing throughput and sovereignty over ordering, fees, and MEV (dydx.xyz "Announcing dYdX Chain"); Hyperliquid own-L1 perp DEX; Aevo off-chain matching + on-chain settlement.

[7] Kiayias, A., Koutsoupias, E., Lazos, P. & Panagiotakos, G. *Tiered Mechanisms for Blockchain Transaction Fees.* arXiv:2304.06014, 2023.

[8] Control/data-plane decoupling lineage - GMPLS (generalized MPLS control plane over heterogeneous switching); SDN (ONF, control/forwarding-plane separation); P4 (programmable data planes enforcing QoS at line rate); SRv6 / segment routing (stateless, in-header, source-routed policy); 5G network slicing over SDN/NFV. *(Surveys: "5G network slicing using SDN and NFV," Computer Networks / arXiv:1912.02802; P4 network-slicing and SRv6 literature.)*

*Sourcing note: primary Monad documentation is cited where available; claims resting on secondary sources are marked. Corrections and primary-source pointers are welcome.*
