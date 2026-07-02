# L1 Petal Fixed-Excess Certificate

This directory contains the replayable arithmetic certificate for
`experimental/notes/l1/l1_petal_fixed_excess_compiler.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_fixed_excess_compiler.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_fixed_excess_compiler.py \
  --check experimental/data/certificates/l1-petal-fixed-excess/l1_petal_fixed_excess_compiler.json
```

The certificate compiles Lemma 16 of the L1 full-list quotient proof program
into exact fixed-excess layer bounds. It is not a brute-force list decoder and
does not close mixed-petal amplification.

