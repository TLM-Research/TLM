# Review of RN-16 — *A Temporal Liquidity Reserve for EIP-1559*

**Reviewed version:** 0.1, dated 1 September 2026  
**Recommendation:** Major revision before simulation

## Overall assessment

RN-16 identifies the correct trade made by moving from RN-15’s contemporaneous mean to a posted price: individual charges become independent of the current included set, while exact per-block balance becomes intertemporal solvency. The distinction between a token reserve here and RN-12’s capacity reserve is important and should be adopted across the notes.

The proposed reserve is not yet well-defined enough to simulate. It inherits RN-15’s unit and payment-cap problems, has no neutral declaration when (P_t\ne0), and lacks a boundary rule at (R=0). The two-slope controller is described with market-making language, but its claimed spread revenue and stability properties do not follow without matched quantities and a behavioral demand model.

## Required revisions

### 1. Critical — fix the inherited units before defining reserve flows

**Location:** Sections 2 and 5.

`TLF_i` is a tick count in RN-15, while (P_t), (d_i), and fee payments are treated as wei per gas. The reserve update (R_{t+1}=R_t+\sum g_i d_i) has the correct token unit only if (d_i) is first converted to wei per gas.

**Recommendation:** separate integer declarations from monetary prices and define all conversions. Re-derive (s r<1/2) with the tick, flooring, and strict-bound cases included.

### 2. Critical — define a neutral default under a nonzero posted price

**Location:** Sections 2, 5, and 6.

Under (d_i=TLF_i-P_t), `TLF = 0` is charged or credited whenever (P_t\ne0). The closing-auction section says a failed conditional order can fall back to `TLF = 0`, but that fallback is not neutral. This also breaks backward compatibility for legacy transactions unless they are explicitly excluded.

**Recommendation:** define a participation flag and a neutral settlement point. A participating neutral order would normally declare the posted mid (P_t), but ordering, rounding, cap range, price updates, and transaction lifetime then need rules. Specify what happens when a transaction signed under (P_t) is included after the price changes.

### 3. Critical — make the reserve an explicit balance sheet

**Location:** Sections 2–5.

The update equation records net flow but does not specify custody, ownership, liabilities, minimum balance, capitalization, or who receives surplus. When (d_i<0), the reserve must fund the difference between sender payment, proposer compensation, and burn. A negative reserve would amount to unsecured protocol issuance or debt.

**Recommendation:** define assets, permitted liabilities, initial capitalization, proposer payment, burn funding, withdrawal rights, and an invariant such as (R_t\ge0). State whether reserve income is burned, retained, or rebated.

### 4. Critical — no finite reserve guarantees the promised credit under unrestricted flow

**Location:** Sections 3–5 and 9.

A sequence of provider-heavy blocks can drain any finite reserve. The cap bounds loss per unit of gas, not cumulative loss. Until a boundary rule is chosen, the posted credit is not a credible promise.

**Recommendation:** choose a solvency mechanism before controller tuning: pre-funded liability limits, dynamic credit haircuts, hard suspension, participant claims, or external recapitalization. Then state the service guarantee in normal and boundary states.

### 5. Critical — `c > s` does not create a spread on every crossed unit

**Location:** Section 5.

The mechanism does not match equal consumer and provider quantities. Consumer-heavy or provider-heavy blocks settle independently against the reserve. Different slopes can create expected positive reserve flow under a particular distribution, but (c>s) does not guarantee structural accumulation “on every crossed unit.” There may be no crossed unit at all.

**Recommendation:** derive expected reserve drift from gas-weighted declaration distributions and participation responses. Use bid–ask-spread language only for matched trades or define the reserve as dealer counterparty to each side and account for its inventory exposure.

### 6. High — specify the controller rather than describing its direction

**Location:** Section 5.

No update equations are given for (P_t), (c_t), or (s_t). “Fast level and slow slopes” is a design intuition, not a controller. Stability cannot be evaluated without delays, saturation, price bounds, observation windows, and a model of demand response.

**Recommendation:** write explicit discrete-time update rules and linearize or stress-test them against a stated demand model. Include empty blocks, regime shifts, adversarial declarations, cap saturation, and the interaction with EIP-1559.

### 7. High — the two controllers do not necessarily act on one signal, but they do interact through demand

**Location:** Sections 4, 5, and 8–10.

The base-fee controller observes gas utilization; the reserve controller observes reserve flow or declarations. These are not literally one signal. They can still interact because both prices affect inclusion and composition. Calling it the standard two-controllers/one-signal case is therefore imprecise.

**Recommendation:** model a coupled system with at least gas demand, temporal declarations, base fee, posted temporal price, and reserve balance. Identify direct and cross elasticities rather than relying on the analogy.

### 8. High — posted-price independence is conditional

**Location:** Section 3.

A current block cannot directly alter a predetermined (P_t), but builders and users can manipulate the observations used to set future prices. If (P_t) tracks recent declarations, filler flow and builder selection return as lagged attacks.

**Recommendation:** replace “the threats stop applying” with “same-block influence is removed.” Analyze lagged manipulation, censorship, wash participation, transaction splitting, and anticipatory trading around updates.

### 9. High — conditional declarations need expiry and price-version semantics

**Location:** Section 6.

A sender can know the posted price at signing only if the transaction names a valid price version or inclusion interval. Otherwise the price may change before inclusion. Falling back after a condition fails also changes ordering and may create optionality against the reserve.

**Recommendation:** include price epoch, expiry, limit condition, fallback behavior, and replay/replacement rules in the signed transaction. Analyze the free-option problem created by conditional participation.

### 10. Medium — separate the two reserves in names and notation now

**Location:** Section 11 and cross-note terminology.

RN-12’s reserve is execution capacity by quantum; RN-16’s reserve is a native-token settlement balance. Calling both (R) obscures which conservation law is being relaxed.

**Recommendation:** use names such as (R^{cap}_q) for capacity reserve and (B^{TL}_t) for the temporal settlement fund. Update RN-12, RN-15, RN-16, and RN-22 consistently.

## Strong material to preserve

- The allocation remains intra-slot while settlement crosses slots.
- The note states that solvency replaces exact balance.
- Same-block composition and own-gas effects are separated from posted-price effects.
- The reserve/base-fee interaction is treated as an open question.
- The distinction between capacity reserve and monetary reserve is recognized.
- The required simulation outputs are listed rather than implied to exist.

## Recommended revision order

1. Import corrected RN-15 units and payment authorization.
2. Define participation, price epochs, and a neutral default.
3. Specify the reserve balance sheet and zero-bound rule.
4. Write explicit controller equations.
5. Derive drift and solvency under behavioral and adversarial demand.
6. Only then run the proposed coupled-controller simulations.

