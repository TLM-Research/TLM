# TLM simulation code

Simulations supporting quantitative claims in the TLM research notes.

**One script per note.** Each script backs the tables and figures in a single note, is named for that note, and is cited from that note's reference list. A claim in a note that carries a number should be traceable to a script here, and a number here that no note uses should be removed.

| Script | Supports | Claims backed |
|---|---|---|
| `rn15_tlf_balance.py` | RN-15, *A Temporal Liquidity Fee for EIP-1559* | secs. 2.1, 2.3, 3, 10 |
| `rn22_basefee.py` | RN-22, *A Temporal Liquidity Fee Market Design for Ethereum* | secs. 5.1, 5.2 |

## Running

No dependencies. Python 3.8 or later, standard library only, which is deliberate: a reviewer should be able to check the arithmetic without installing anything.

```bash
python3 rn15_tlf_balance.py
python3 rn22_basefee.py
```

## Tests

The tests assert the exact numbers the notes publish, not merely that the code runs. If a note's table is edited without the model changing, or the model changes without the table being updated, a test fails.

```bash
python3 tests/test_rn15_tlf_balance.py
python3 tests/test_rn22_basefee.py
```

They are also standard `pytest` files, so `pytest tests/` works if pytest is installed. It is not required.

## Results

`results/` holds captured output from a dated run, so a reader can check a table in a note against a recorded result without executing anything. Regenerate with:

```bash
python3 rn15_tlf_balance.py > results/rn15_tlf_balance.txt
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

They are stylized. `rn22_basefee.py` uses a single sinusoidal demand path with no elasticity, no backlog dynamics and no heterogeneity in willingness to pay; it establishes the sign of an effect and the location of a crossover, not magnitudes for real traffic. `rn15_tlf_balance.py` is exact arithmetic on constructed blocks rather than a behavioural model, and its worst case is built by hand rather than sampled, because random blocks essentially never produce the adversarial composition.

Neither is calibrated to mainnet data. Where a note needs a magnitude rather than a direction, it says so and marks the measurement as open.
