---
id: RN-14-FQ
title: "Follow-up Research to RN-14: Open Questions Raised by the Workload Split"
version: v0.1
status: "Companion to RN-14. Working document, updated as questions are answered or reassigned."
program: "Temporal Liquidity Market (TLM)"
date: August 30, 2026
---

# RN-14 Follow-up Research Questions

## Purpose

RN-14 is an observational note. It documents a durable split in workload across four Layer-1 chains, argues that Ethereum's network effect compounded on capital but not on users, and asks whether temporal requirements are part of what separates the categories. It does not establish that they are.

A note of that kind generates more questions than it can carry. RN-14 keeps the three that could change its own reading and routes the rest here, grouped by where they would be answered rather than by where they arose. Three of the questions below are also empirical prerequisites for anything the mechanism notes propose, and are marked as such.

---

## 1. Whether the split is real as measured

The note's argument rests on cross-chain metrics that are known to be imperfect. These questions test the observation itself.

- **1.1 Is the address gap economically real?** *(Retained in RN-14 sec. 13. Status: strong prior that it is; measurement outstanding.)*

  Active-address counts include wash trading, airdrop farming and automated flow in proportions that differ by chain, and removing them on a consistent basis remains the measurement most likely to change the conclusion. It has not been done. The circumstantial case has firmed considerably, and is recorded here so the question is not restated as though nothing were known.

  *The contaminants are chain-specific, and their motives are largely absent on Tron.* Airdrop farming requires an expected token distribution, and Tron has no meaningful programme. Wash trading requires a venue metric worth inflating, and Tron's DEX volume is $0.061bn per 24 hours (RN-14 sec. 3.2), effectively nil. What Tron does carry is near-zero fees, which make spam cheap, and exchange-internal transfers, which inflate counts without being users. Ethereum and Solana carry the first two heavily. **A consistent cleaning would therefore reduce Ethereum's and Solana's counts by more than Tron's, which means the reported gap is more likely understated than overstated.**

  *Velocity discriminates.* Tron's stablecoin supply turns over at roughly 0.2 to 0.3 times daily, so the average dollar moves once every three to five days. That is consistent with settlement and transfer utility and inconsistent with the churn wash trading produces.

  *The composition is what the payments reading predicts.* Around 51 percent of all USDT sits on Tron, and Tron leads globally in USDT transfers under $1,000. Small-value transfers are the payments signature and the hardest category to fabricate profitably.

  *What would still settle it:* address-level clustering separating exchange-operational flow from end-user flow, applied identically across the four chains, over the one-year window of the trend question below.
- **1.2 Is the split explained by cost and incentive spending alone?** Regressing workload share on relative fee level and on incentive programs tests the cheapest rival explanation. *(Retained in RN-14 sec. 13.)*
- **1.3 Does the pattern hold as a trend rather than a snapshot?** Section 3.2 is one day's reading. The one-year daily series for TVL, DEX volume and 7-day moving-average DEX volume would let the derived ratios in section 3.3 be shown as trends. Endpoints and API paths are in RN-14 section 12.
- **1.4 What does stablecoin transfer volume by chain show?** This is the missing fourth figure and the one series that tests the payments reading of Tron directly rather than inferring it from the absence of DEX volume.
- **1.5 How much of the cross-provider discrepancy matters?** Artemis and DeFiLlama differ on the same quantities by roughly ten percent for Tron and four percent for Ethereum. Small enough not to move the pattern, large enough to need a stated reconciliation before the numbers are used elsewhere.

## 2. The temporal hypothesis

RN-14 infers temporal characteristics from what applications do. Nothing in aggregate data records a deadline, a delay tolerance, or a sensitivity to ordering.

- **2.1 Do the application mixes differ in temporal characteristics at the transaction level, or only in value and frequency?** This is the note's central claim and the one it does not establish. *(Retained in RN-14 sec. 13.)*
- **2.2 Do applications on fast chains show shorter value decay, or only shorter observed inter-transaction intervals?** The two differ and only the first is a property of demand. Short intervals may reflect what the chain permits rather than what the application needs, which makes this a question about identification rather than measurement.
- **2.3 Does the capital-per-address gap reflect a difference in temporal requirements, or a difference in wealth and custody patterns?** Ethereum holds 63 times more capital per active address than Tron. That is consistent with a settlement pattern and equally consistent with a custody pattern, and the note does not separate them.
- **2.4 Does the retail and institutional split in payments appear as a difference in revealed delay tolerance, or only as a difference in value?** RN-14 section 8.3 treats these as distinct temporal populations. The claim is testable on transfer size against observed confirmation urgency.

## 3. The network-effect asymmetry

Section 6 argues capital and users are two mechanisms with opposite cost sensitivity. That is the note's most distinctive claim and its least tested.

- **3.1 Why did the capital network effect compound while the user network effect did not?** The alternative reading is one mechanism interrupted by something else, and the two imply different remedies.
- **3.2 Does habit formation depend on a frequency band that fee levels exclude?** Section 8.3 argues tolerance for friction falls as frequency rises, so a cost structure can exclude daily use while permitting occasional use. Testable as a distribution of per-address transaction frequency against per-transaction cost, across chains.
- **3.3 Are payment habits recoverable at any execution quality?** Section 8.3 argues they are held in place by counterparties rather than by preference, which would make them stickier than trading flow and harder to win back. If correct, the ordering of remedies changes.

## 4. What the protocol would have to expose

These are design questions RN-14 raises and does not attempt.

- **4.1 What temporal information would have to be protocol-visible to serve the demand that currently goes elsewhere?** Answered in RN-01 and RN-02 at the level of the interface, and in RN-12 at the level of mechanism.
- **4.2 Can differentiated temporal service coexist with a global public mempool?** Section 7.2 argues the mempool is a design commitment rather than an accident, which makes this a constraint rather than an implementation detail.
- **4.3 Does raising L1 capacity change which temporal profiles are servable, or only the price of the single profile on offer?** Section 11 finds the base fee controller returns usage to its target regardless, so capacity and interface are separate levers.
- **4.4 Does real Ethereum congestion vary slowly enough for peak reduction to lower average fees rather than only redistribute them?** RN-14 section 11 puts the crossover near ten minutes, close to the response time of the base fee controller. The simulation is in `sims/rn22_basefee.py`; the empirical half is unanswered.

## 5. Recovery, and how it would be measured

- **5.1 Which departed workloads are addressable by execution design at all, and which are held elsewhere by distribution, geography or regulation?** Section 8.4 separates the three cases but does not size them.
- **5.2 Does importing an execution model without its ecosystem recover volume?** Eclipse is the natural test case, running the SVM with Ethereum settlement since November 2024. Its volume relative to Solana's is the measurement.
- **5.3 How would one evaluate whether a temporal interface recovered anything?** Without a stated counterfactual this cannot be answered after the fact, which argues for fixing the measure before any change ships rather than after.

---

## Questions now answered elsewhere

Two questions that appeared in earlier versions of RN-14 section 13 have proper homes and are removed from the note.

| Question | Where it now lives |
|---|---|
| Given EIP-4844 established a second fee market for a second resource, what is the equivalent construction for a temporal dimension? | A forthcoming note on inter-slot temporal liquidity, as the model for an independently floating deferred fee |
| Does patient flow spread across blocks or concentrate into whichever blocks price it? | Working note of 30 August 2026 on the crossing frame, open item 2 |

---

## Where each question is answered

| Group | Answered in | Kind of work |
|---|---|---|
| 1. Whether the split is real | RN-14 itself, revised | Data collection and cleaning |
| 2. The temporal hypothesis | A new empirical note | Transaction-level measurement |
| 3. The network-effect asymmetry | RN-10, extended | Economics |
| 4. What the protocol would expose | RN-01, RN-02, RN-12, RN-15 | Interface and mechanism design |
| 5. Recovery and its measurement | RN-06, RN-09, and a deployment note | Empirical and design |

The three prerequisites for the mechanism work are questions 1.1, 1.2 and 2.1. Until the address gap survives cleaning, the cost-only explanation is tested, and temporal characteristics are observed rather than inferred, the demand-side case in RN-14 remains an argument for measurement rather than a finding.
