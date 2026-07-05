# L1 Petal Residue-Kernel Linear Bound

Status: PROVED.

Source DAG node: `petal_residue_kernel_linear_bound`.

## Statement

In the full-petal coset-chart residue bridge, let

```text
K_{I,d} = ker(pi_{>d} R_{I,d})
```

be the residue-line kernel attached to a touched petal set `I` and defect
`d`.  If `ell` is the petal size and

```text
c = d - ell,
```

then

```text
dim K_{I,d} <= c + 1.
```

## Proof

The coset-chart residue bridge identifies the full-petal growing-defect
configurations with the top-coefficient residue-line map

```text
pi_{>d} R_{I,d}.
```

Lemma 13 of `l1_full_list_quotient_proof_program.md` is stated in exactly this
full-petal notation.  It proves

```text
dim K_{I,d} <= d - ell + 1.
```

Since `c = d - ell`, this is precisely

```text
dim K_{I,d} <= c + 1.
```

This proves the linear ceiling on the residue-line kernel.

## Non-Claims

This is an ambient-kernel dimension bound.  It does not prove that the kernel
dimension is uniformly bounded in `c`, and it does not by itself bound the
number of squarefree realizable locator points in the kernel.  Those are the
separate realizability/classification tasks in the growing-defect L1 branch.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_linear_bound.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_linear_bound.py \
  --check experimental/data/certificates/l1-petal-residue-kernel-linear-bound/l1_petal_residue_kernel_linear_bound.json
```

The verifier checks that the upstream proof-program anchors for Lemma 13 and
the residue bridge are present, then emits the dependency certificate.
