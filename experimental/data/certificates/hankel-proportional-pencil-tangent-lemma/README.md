# Hankel Proportional-Window Root-Compression Lemma

This certificate records the reusable v9 reduction for proportional syndrome
windows:

```text
u_m = c v_m for m<t+j  =>  H(u)+Z H(v) = (c+Z)H(v)
on the exact-A Hankel bucket.
```

Consequences:

```text
nonzero regular minor: root union {-c}
affine pivot with B_T != 0: slope {-c}
B_T = 0: contained, since A_T = c B_T = 0
```

After the tangent/common-code-line ledger removes `Z=-c`, a proportional branch
has no aperiodic residual.  If proportionality holds only on the visible window,
the bucket is still compressed to one slope, but a tail check is needed before
charging that slope to the tangent ledger.  This is a reusable classification
lemma; it is not an actual M3 row root table.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json
```

The verifier checks prime-field regular and singular toy cases, affine pivot
ratios, a local-window-only proportional example with a nonzero tail, and the
pinned `F_17^32`, `A=426`, `c=5` proportional packet/subtraction artifacts.
