"""RN-15 TLA balance checks under the current two-branch mechanism."""

import random

from rn15_tla import clear, check


def randomized_balance(blocks=20_000, seed=17):
    rng = random.Random(seed)
    violations = {}
    for _ in range(blocks):
        base_fee = rng.choice([1, 7, 30, 120, 1_000])
        txs = []
        for txid in range(rng.randint(0, 25)):
            limit = rng.choice([21_000, 60_000, 200_000, 1_000_000])
            used = rng.randint(0, limit)
            if base_fee and rng.random() < 0.4:
                max_fee = rng.randrange(base_fee)
                max_priority = rng.randint(0, min(5, max_fee))
                tla = -rng.randint(1, 500_000_000)
            else:
                max_fee = base_fee + rng.randint(0, 60)
                max_priority = rng.randint(0, min(20, max_fee))
                tla = rng.choice([0, rng.randint(1, 500_000_000)])
            txs.append((txid, limit, used, max_fee, max_priority, tla))
        rows, meta = clear(txs, base_fee)
        for failure in check(rows, meta):
            violations[failure] = violations.get(failure, 0) + 1
    return violations


if __name__ == "__main__":
    failures = randomized_balance()
    print("RN-15 TLA randomized balance checks")
    print("blocks 20000")
    print("violations", failures or "none")
