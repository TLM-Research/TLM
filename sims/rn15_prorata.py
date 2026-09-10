"""RN-15 TLA pro-rata settlement example.

Positive TLA values are lump-sum consumer authorizations.  Funded providers
receive Scheme-B shortfall funding based on the full signed priority fee.  The
realised aggregate shortfall is apportioned to consumers pro rata, with exact
integer largest-remainder accounting.
"""

from rn15_tla import clear, check


def example():
    base_fee = 30
    txs = [
        ("consumer-a", 200_000, 150_000, 60, 8, 400_000),
        ("consumer-b", 200_000, 90_000, 45, 3, 200_000),
        ("neutral", 100_000, 50_000, 50, 2, 0),
        ("provider-a", 60_000, 40_000, 29, 1, -200_000),
        ("provider-b", 60_000, 30_000, 25, 1, -400_000),
    ]
    rows, meta = clear(txs, base_fee)
    print("RN-15 TLA pro-rata consumer settlement")
    print("id side TLA priority shortfall commitment/charge payment")
    for row in rows:
        amount = row["pay_extra"] if row["side"] == "C" else row["S"]
        print(row["txid"], row["side"], row["tla"], row["p"],
              row["s"], amount, row["payment"])
    print("pool", meta["A"], "used", meta["used"],
          "refunded", meta["refunded"])
    print("checks", check(rows, meta) or "all pass")


if __name__ == "__main__":
    example()
