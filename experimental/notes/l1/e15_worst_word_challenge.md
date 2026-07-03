# E15 Worst-Word Sunflower Challenge

## Status

EXPERIMENTAL / AUDIT.

- **Roadmap task:** E15, `worst-word challenge / QL.2`.
- **Verifier:** `experimental/scripts/verify_e15_worst_word_challenge.py`.
- **Artifact:**
  `experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json`.

This packet stress-tests the list-side heuristic that the planted sunflower
word is the worst small model, or at least that common structured challengers
do not beat it at matched radius.  The expanded exact small-parameter sweep
finds a real low-slack exception: the naive planted-worst statement is false
at `sigma=1` in several `n=16` cells.

It does not prove the L1 safe-side theorem.

## Tested Cells

All cells use the subgroup domain in `F_193`.

The exact cells are a toy official-rate sweep:

```text
n = 16,
k in {1,2,4,8},
selected 1 <= sigma <= 4,
two deterministic layouts,
two scalar schedules.
```

For each exact cell the verifier enumerates all `binom(16,k+sigma)` agreement
sets, interpolates the unique candidate polynomial, and deduplicates
degree-`<k` codewords.  It checks `328504` exact agreement sets in total.

Outcome:

```text
sigma = 1:
    12 exact cells beat the planted count.
    all non-planted extras are mixed-petal except five full-petal extras
    in two k=8 shuffled/geometric cells.

sigma >= 2:
    no exact n=16 cell beats the planted count.
    no non-planted codewords occur.
```

The structured larger cells are:

```text
n = 32, k = 16, sigma = 3:
    bounded-excess full-petal scan, d - ell <= 2,
    330330 candidates checked across 6 cells.

n = 64, k = 32, sigma = 3:
    minimal-defect two-petal locator-pencil scan,
    5286120 candidates checked across 6 cells.
```

No non-planted structured challenger appears in the `n=32` or `n=64` cells.

## Interpretation

The replayed outcome is:

```text
STRUCTURED_NONPLANTED_CHALLENGER_FOUND
```

The interpretation is a split result.

First, it refutes the literal small-model `worst_word_planted` heuristic in
the low-slack `sigma=1` layer.  The counterexamples are not mysterious: they
are mixed-petal sunflower extras, exactly the class already isolated in the L1
proof program as the remaining amplification frontier.

Second, it supports the repaired form that should matter near the lower-cutoff
proof program: after leaving the very low-slack layer, the tested exact cells
and the bounded structured larger cells do not find a challenger.  The scan
attacks the specific alternatives named in E15:

```text
multi-layout planted sunflowers,
bounded-excess full-petal challengers,
minimal-defect two-petal folded/cyclic layouts.
```

Thus the next useful statement should not be "planted is always worst."
Instead it should be a conditional or stratified version:

```text
low-slack sigma=1 mixed-petal extras are a named exception;
for sigma >= 2 in these exact cells, planted remains worst;
bounded-excess full-petal and minimal-defect two-petal challengers stay clean.
```

Future counterexample searches should therefore push beyond the controlled
families, toward growing-excess full-petal CRT kernels and diffuse mixed-petal
amplification.

## Non-Claims

This packet is not an exhaustive list decoder for `n=32` or `n=64`.

This packet does not rule out growing-excess full-petal CRT kernels or diffuse
mixed-petal patterns.

This packet refutes the naive `worst_word_planted` formulation at `sigma=1`.
It does not prove the repaired or stratified version suggested above.

## Reproduce

Regenerate:

```bash
python3 experimental/scripts/verify_e15_worst_word_challenge.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e15_worst_word_challenge.py \
  --check experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json
```

The default replay checks `72` cells and currently takes about four minutes in
this environment.
