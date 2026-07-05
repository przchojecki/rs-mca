# L1 Petal Realizable-Kernel Injection Certificate

This directory contains the replayable certificate for
`experimental/notes/l1/l1_petal_realizable_kernel_injection.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_realizable_kernel_injection.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_realizable_kernel_injection.py \
  --check experimental/data/certificates/l1-petal-realizable-kernel-injection/l1_petal_realizable_kernel_injection.json
```

The verifier checks that the residue bridge and Lemma 8 anchors are present.
It does not count squarefree locator points.
