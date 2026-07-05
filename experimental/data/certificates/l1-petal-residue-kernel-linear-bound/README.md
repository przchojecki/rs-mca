# L1 Petal Residue-Kernel Linear-Bound Certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_petal_residue_kernel_linear_bound.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_linear_bound.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_linear_bound.py \
  --check experimental/data/certificates/l1-petal-residue-kernel-linear-bound/l1_petal_residue_kernel_linear_bound.json
```

The verifier checks that the residue bridge and Lemma 13 anchors are present.
It does not count realizable squarefree kernel points.
