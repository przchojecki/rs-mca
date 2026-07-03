# E15 Worst-Word Sunflower Challenge

## Status

EXPERIMENTAL / AUDIT.

- **Roadmap task:** E15, `worst-word challenge / QL.2`.
- **Verifier:** `experimental/scripts/verify_e15_worst_word_challenge.py`.
- **Artifact:**
  `experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json`.

This packet stress-tests the list-side heuristic that the planted sunflower
word is the worst small model, or at least that common structured challengers
do not beat it at matched radius.

It does not prove the L1 safe-side theorem.

## Tested Cells

All cells use the subgroup domain in `F_193`.

The exact cells are:

```text
n = 16, k = 8, sigma = 2, s = 10.
```

For each of four deterministic sunflower layouts and two scalar schedules, the
verifier enumerates all `binom(16,10)=8008` agreement sets, interpolates the
unique candidate polynomial, and deduplicates degree-`<k` codewords.  In every
exact cell the list size is exactly the planted count:

```text
list size = planted count = 3,
non-planted codewords = 0.
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

No non-planted structured challenger appears in these cells.

## Interpretation

The replayed outcome is:

```text
NO_STRUCTURED_CHALLENGER_FOUND_IN_BOUNDED_CELLS
```

This supports the `worst_word_planted` heuristic only in the tested finite
models.  The evidence is useful because it attacks the specific alternatives
named in E15:

```text
multi-layout planted sunflowers,
bounded-excess full-petal challengers,
minimal-defect two-petal folded/cyclic layouts.
```

The result is consistent with the proof-program reductions: exact two-petal
and fixed-excess full-petal layers should not create a larger worst word.
Any future counterexample should therefore look beyond these controlled
families, toward the remaining mixed-petal amplification frontier.

## Non-Claims

This packet is not an exhaustive list decoder for `n=32` or `n=64`.

This packet does not rule out growing-excess full-petal CRT kernels or diffuse
mixed-petal patterns.

This packet does not prove `worst_word_planted`; it only records a replayable
red-team pass for the bounded structured challengers above.

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

The default replay checks `20` cells and currently takes about four minutes in
this environment.
