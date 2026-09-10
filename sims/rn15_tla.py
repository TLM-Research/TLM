"""RN-15 reference model using current TLA semantics.

Input: ``(L, g, max_fee, max_priority_fee, TLA)`` or the same prefixed by
``tx_id``. Gas, fee rates, TLA and settlement amounts are integers.

Positive TLA is a consumer's maximum lump-sum authorization. Negative TLA opts
a below-base-fee transaction into provider treatment and determines its later
execution band; its magnitude is not a subsidy cap.

Provider Scheme B is consensus-deterministic here.  A funded provider pays its
signed ``max_fee`` from its own balance; the pool pays
``base_fee + max_priority_fee - max_fee`` per realised gas; and the builder
receives the full signed ``max_priority_fee``.  The builder chooses the
included set, but not an arbitrary lower effective priority fee.
"""


def signed_band(tla, tla_tick):
    if not isinstance(tla_tick, int) or tla_tick <= 0:
        raise ValueError("tla_tick must be a positive integer")
    return tla // tla_tick


def _normalise(txs):
    out, seen = [], set()
    for pos, tx in enumerate(txs):
        if len(tx) == 5:
            txid, fields = pos, tx
        elif len(tx) == 6:
            txid, fields = tx[0], tx[1:]
        else:
            raise ValueError("transaction must have five fields, or tx_id plus five fields")
        if txid in seen:
            raise ValueError("transaction ids must be unique")
        seen.add(txid)
        L, g, mf, mp, tla = fields
        if not all(isinstance(v, int) and not isinstance(v, bool)
                   for v in (L, g, mf, mp, tla)):
            raise TypeError("gas, fee fields and TLA must be integers")
        if L <= 0 or not 0 <= g <= L:
            raise ValueError("require L > 0 and 0 <= g <= L")
        if mf < 0 or mp < 0:
            raise ValueError("fee fields must be nonnegative")
        if mf < mp:
            raise ValueError("max_fee must be at least max_priority_fee")
        out.append(dict(txid=txid, input_pos=pos, L=L, g=g, mf=mf, mp=mp, tla=tla))
    return out


def _apportion(total, consumers):
    """Exact pro-rata integer apportionment: largest remainder, then tx_id."""
    if not consumers:
        if total:
            raise ValueError("nonzero settlement without consumers")
        return {}
    pool = sum(x["commit"] for x in consumers)
    if not 0 <= total <= pool:
        raise ValueError("settlement exceeds consumer pool")
    shares, remainders, assigned = {}, [], 0
    for x in consumers:
        q, rem = divmod(x["commit"] * total, pool)
        shares[x["txid"]] = q
        assigned += q
        remainders.append((rem, str(x["txid"]), x["txid"]))
    remainders.sort(key=lambda z: (-z[0], z[1]))
    for _, _, txid in remainders[:total - assigned]:
        shares[txid] += 1
    return shares


def clear(txs, base_fee, tla_tick=100_000, block_gas_limit=None):
    """Clear one RN-15 block and return ``(rows, metadata)``."""
    if not isinstance(base_fee, int) or isinstance(base_fee, bool) or base_fee < 0:
        raise ValueError("base_fee must be a nonnegative integer")
    rows = _normalise(txs)
    if block_gas_limit is not None:
        if not isinstance(block_gas_limit, int) or block_gas_limit < 0:
            raise ValueError("block_gas_limit must be a nonnegative integer")

    for x in rows:
        x.update(commit=0, p=0, s=0, R=0, S=0, funded=False,
                 pay_extra=0, payment=None, to_builder=0,
                 band=signed_band(x["tla"], tla_tick))
        if x["tla"] > 0 and x["mf"] >= base_fee:
            x["side"], x["commit"] = "C", x["tla"]
        elif x["tla"] < 0 and x["mf"] < base_fee:
            x["side"] = "P"
            x["p"] = x["mp"]
            x["s"] = base_fee + x["p"] - x["mf"]
            x["R"], x["S"] = x["L"] * x["s"], x["g"] * x["s"]
        elif x["mf"] >= base_fee:
            x["side"] = "N"
        else:
            x["side"] = "I"  # below base fee without negative-TLA opt-in

    consumers = [x for x in rows if x["side"] == "C"]
    pool = sum(x["commit"] for x in consumers)
    candidates = sorted((x for x in rows if x["side"] == "P"),
                        key=lambda x: (x["s"], str(x["txid"])))
    reserved, funding_order = 0, []
    for x in candidates:
        if reserved + x["R"] <= pool:
            reserved += x["R"]
            x["funded"] = True
            funding_order.append(x["txid"])
        else:
            x["side"] = "X"

    used = sum(x["S"] for x in rows if x["funded"])
    charges = _apportion(used, consumers)
    for x in rows:
        if x["side"] == "C":
            x["pay_extra"] = charges[x["txid"]]
            tip = min(x["mf"] - base_fee, x["mp"])
            x["payment"] = x["g"] * (base_fee + tip) + x["pay_extra"]
            x["to_builder"] = x["g"] * tip
        elif x["side"] == "N":
            tip = min(x["mf"] - base_fee, x["mp"])
            x["payment"] = x["g"] * (base_fee + tip)
            x["to_builder"] = x["g"] * tip
        elif x["side"] == "P":
            x["payment"] = x["g"] * x["mf"]
            x["to_builder"] = x["g"] * x["p"]

    live = [x for x in rows if x["side"] in ("C", "N", "P")]
    if block_gas_limit is not None and sum(x["g"] for x in live) > block_gas_limit:
        raise ValueError("included transactions exceed block gas limit")
    execution_order = [x["txid"] for x in sorted(
        live, key=lambda x: (-x["band"], x["input_pos"]))]
    return rows, dict(A=pool, reserved=reserved, used=used,
                      released=reserved - used, refunded=pool - used,
                      funded=len(funding_order), wanted=len(candidates),
                      funding_order=funding_order, execution_order=execution_order,
                      tla_tick=tla_tick, base_fee=base_fee,
                      block_gas_used=sum(x["g"] for x in live),
                      block_gas_limit=block_gas_limit)


def check(rows, meta, base_fee=None):
    """Return violations of v2.2 accounting and ordering rules."""
    bf = meta["base_fee"] if base_fee is None else base_fee
    bad = []
    live = [x for x in rows if x["side"] in ("C", "N", "P")]
    providers = [x for x in live if x["side"] == "P"]
    consumers = [x for x in live if x["side"] == "C"]
    if any(x["payment"] != x["g"] * x["mf"] for x in providers):
        bad.append("provider price not max_fee")
    if any(x["p"] != x["mp"] for x in providers):
        bad.append("provider priority fee not full signed maximum")
    if any(x["s"] != bf + x["p"] - x["mf"] or
           x["R"] != x["L"] * x["s"] or x["S"] != x["g"] * x["s"]
           for x in providers):
        bad.append("provider shortfall accounting")
    if any(not 0 <= x["pay_extra"] <= x["commit"] for x in consumers):
        bad.append("temporal charge outside TLA")
    if any(x["payment"] - x["pay_extra"] > x["g"] * x["mf"]
           for x in live if x["side"] in ("C", "N")):
        bad.append("execution fee above max_fee")
    if any(x["pay_extra"] for x in live if x["side"] == "N"):
        bad.append("neutral charged temporal amount")
    if sum(x["pay_extra"] for x in consumers) != sum(x["S"] for x in providers):
        bad.append("balance")
    if meta["reserved"] > meta["A"] or meta["used"] > meta["reserved"]:
        bad.append("pool overdrawn")
    if any(x["payment"] < 0 for x in live):
        bad.append("negative payment")
    by_id = {x["txid"]: x for x in live}
    fs = [by_id[i]["s"] for i in meta["funding_order"]]
    if fs != sorted(fs):
        bad.append("provider funding order")
    bands = [by_id[i]["band"] for i in meta["execution_order"]]
    if bands != sorted(bands, reverse=True):
        bad.append("TLA band order")
    if meta["block_gas_limit"] is not None and meta["block_gas_used"] > meta["block_gas_limit"]:
        bad.append("block gas limit")
    return bad
