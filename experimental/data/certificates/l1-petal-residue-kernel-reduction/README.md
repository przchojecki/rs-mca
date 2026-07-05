# L1 Petal Residue-Kernel Reduction Certificate

This directory contains the replayable dependency certificate for
`experimental/notes/l1/l1_petal_residue_kernel_reduction.md`.

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_reduction.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_reduction.py \
  --check experimental/data/certificates/l1-petal-residue-kernel-reduction/l1_petal_residue_kernel_reduction.json
```

The certificate is a logic packet. It checks the implication DAG and records
that the only live assumption is the actual squarefree classification ledger.
It is not an algebraic search and does not close the L1 mixed/growing residual.
