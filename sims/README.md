# TLM simulation code

Simulations supporting quantitative claims in the TLM research notes.

Each current script backs the tables and figures in a research note and is cited from that note. Historical scripts remain temporarily for comparison and are identified below.

| Script | Supports | Claims backed |
|---|---|---|
| `rn15_tla.py` | Current RN-15, *A Temporal Liquidity Authorization for EIP-1559* | clearing, ordering, reserve-and-settle, exact settlement |
| `rn15_prorata.py` | Current RN-15 | exact pro-rata allocation of realised provider shortfalls to consumers |
| `rn15_tla_balance.py` | Current RN-15 | randomized budget-balance and validity invariants |
| `rn15_report.py` | Current RN-15 | worked examples and randomized invariant counts |
| `rn22_basefee.py` | RN-22, *A Temporal Liquidity Fee Market Design for Ethereum* | secs. 5.1, 5.2 |

The withdrawn gas-weighted temporal-liquidity-fee model is no longer part of the active simulation directory. Current scripts use `TLA`: positive values are lump-sum consumer authorizations, while negative values are provider opt-in and later-band commitments. Under provider Scheme B, the full signed `max_priority_fee` enters the shortfall; builders select the included set but do not choose a lower effective provider priority fee.

## Running

No dependencies. Python 3.8 or later, standard library only, which is deliberate: a reviewer should be able to check the arithmetic without installing anything.

```bash
python3 rn15_report.py
python3 rn15_tla_balance.py
python3 rn22_basefee.py
```

## Tests

The tests assert the exact numbers the notes publish, not merely that the code runs. If a note's table is edited without the model changing, or the model changes without the table being updated, a test fails.

```bash
python3 tests/test_rn15_tla.py
python3 tests/test_rn15_prorata.py
python3 tests/test_rn15_tla_balance.py
python3 tests/test_rn22_basefee.py
```

They are also standard `pytest` files, so `pytest tests/` works if pytest is installed. It is not required.

## Results

`results/` holds captured output from a dated run, so a reader can check a table in a note against a recorded result without executing anything. Regenerate with:

```bash
python3 rn15_report.py      > results/rn15_report.txt
python3 rn15_prorata.py     > results/rn15_prorata.txt
python3 rn15_tla_balance.py > results/rn15_tla_balance.txt
python3 rn22_basefee.py     > results/rn22_basefee.txt
```

Results are committed. They are small, they are the artifact a reviewer actually wants, and a diff on them is the quickest way to see that a model change moved a published number.

## Keeping notes and code in step

The tests assert published numbers, so the invariant only holds if it is maintained:

**A change to a number published in a note, and the test asserting it, go in the same commit.** If a model change moves a figure, the note's table and the test both change with it. If they cannot both change, the change is not ready.

**Regenerate `results/` whenever the model changes.** CI checks that the committed results match a fresh run and fails if they have drifted.

**A number belongs to one note.** Tabulating the same figure in two notes puts them out of step the first time one is revised. Paraphrasing a result in prose elsewhere is fine; a second table is not.

Continuous integration is staged in `ci-workflow.yml`. GitHub only runs workflows from the repository root, so activate it with:

```bash
mkdir -p .github/workflows
git mv sims/ci-workflow.yml .github/workflows/sims.yml
```

## Licence

MIT, see `LICENSE`. The research notes in `docs/` are CC BY 4.0. See `docs/LICENSING.md`.

## What these simulations are and are not

They are stylized. `rn22_basefee.py` uses a single sinusoidal demand path with no elasticity, no backlog dynamics and no heterogeneity in willingness to pay; it establishes the sign of an effect and the location of a crossover, not magnitudes for real traffic. `rn15_tla.py` is an exact reference model of current TLA accounting and ordering. It is not calibrated to transaction arrival, builder behaviour or mainnet demand. `rn15_report.py` includes constructed examples and randomized property checks; these establish accounting properties, not an equilibrium.

Neither is calibrated to mainnet data. Where a note needs a magnitude rather than a direction, it says so and marks the measurement as open.
