# m=4 Affine-Shear eca/emca Staircases: q=13 and q=17 Rows

**Status:** AUDIT / EXPERIMENTAL.  The finite rows are offline exact
enumeration outputs over affine-shear representatives.  The committed stdlib
checker does not rerun the global enumeration; it audits the packet integrity,
required row set, staircase invariants, and recorded argmax witnesses.

The theorem/problem ID is `towards-prize thm:sparsify; finite m=4
affine-shear eca/emca staircase`.

This note completes the `m=4` toy-row staircase pattern for:

```text
F_13, n=12, k=8
F_17, n=16, k=12
```

The endpoint convention is:

- `m = n-k = 4`.
- `r = floor(delta*n)`, with radii `0 <= r <= m-1`.
- agreement is `a = n-r`.
- only finite slopes `gamma in F_q` are counted.
- sigma rows use the tail-support convention: the union of the pair supports
  lies in the last `r` coordinates, matching the `F_11,n=10,k=6` m=4
  staircase packet.
- the representative quotient is the affine-shear action
  `(f1,f2) -> (u*f1+s*f2,t*f2)`, with `u,t` nonzero.  Full projective
  transformations are not used.

The affine-shear quotient is deliberately not a full `GL_2` quotient.  Full
`GL_2` can move finite slopes to or from the point at infinity, so it does not
preserve the finite bad-slope numerator.  The affine-shear action induces
`gamma -> (u*gamma+s)/t`, a bijection of `F_q` on the counted finite slopes.

The replay packet is:

```text
experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q13_q17_gpu_rows.json
```

It is checked by:

```text
python experimental/scripts/verify_exact_worstcase_eca_emca_affine_gpu_packet.py --check experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q13_q17_gpu_rows.json
```

The offline enumeration ran on a CUDA GPU accelerator; the device, CuPy
version, and per-row kernel source SHA-256 values are recorded in the
certificate's `gpu_runs` block. The committed checker is CPU/stdlib; no GPU is
needed to check this packet.
It recomputes the sparsify right-hand side as
`max(eca_num(r), sigma_num(r))` and checks it against both `emca_num(r)` and
the recorded `sparsify_rhs` field.

## Results

| q | n | k | raw pair classes | representatives | eca staircase | sigma staircase | emca staircase |
|---:|---:|---:|---:|---:|---|---|---|
| 13 | 12 | 8 | 815,730,721 | 440,301 | 1, 2, 12, 13 | 0, 1, 2, 13 | 1, 2, 12, 13 |
| 17 | 16 | 12 | 6,975,757,441 | 1,612,981 | 1, 2, 15, 17 | 0, 1, 2, 17 | 1, 2, 15, 17 |

For both rows, the sparsify identity holds at every radius:

```text
emca_num(r) = max(eca_num(r), sigma_num(r)).
```

The shape matches the earlier `m=4` `F_11,n=10,k=6` row: the middle radius
is driven by the CA numerator, while the largest sub-capacity radius saturates
all finite slopes.

## Non-Claims

This is not a deployed-row certificate, not a `q_chal` soundness claim, not a
standalone upper-bound verifier, and not an asymptotic theorem.  The optimized
enumeration is offline; the committed checker verifies the packet integrity,
required row set, monotonicity, sparsify equality, and all recorded argmax
slope lists exactly.
