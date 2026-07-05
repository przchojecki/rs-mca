# m=4 Affine-Shear eca/emca Rows for q19 and q23

**Status:** AUDIT / EXPERIMENTAL. The rows are finite offline enumerations
checked by exact argmax replay; family-level pattern language is experimental.

This note extends the affine-shear quotient staircase packet for `m=n-k=4`
with the rows `(q,n,k) = (19,18,14)` and `(23,22,18)`.

Endpoint conventions:

- agreement is `a=n-r`;
- radius is `r=floor(delta*n)`;
- only finite slopes are counted;
- the pair-distance and point-closeness radius is the same `r`;
- toy rows use `q_gen=q_line=q`; `q_chal` is unused.

The replay packet is:

```text
experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q19_q23_gpu_rows.json
```

It is checked by:

```text
python experimental/scripts/verify_exact_worstcase_eca_emca_affine_gpu_packet_q19_q23.py --check experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q19_q23_gpu_rows.json
```

The offline enumeration ran on a CUDA GPU accelerator; the device, CuPy
version, and per-row kernel source SHA-256 values are recorded in the
certificate's `gpu_runs` block. The committed checker is CPU/stdlib; no GPU is
needed to check this packet.  It recomputes the sparsify right-hand side as
`max(eca_num(r), sigma_num(r))` and checks it against both `emca_num(r)` and
the recorded `sparsify_rhs` field.

## Results

| q | n | k | representatives | eca staircase | sigma staircase | emca staircase |
|---:|---:|---:|---:|---|---|---|
| 19 | 18 | 14 | 2,772,921 | `1,2,18,19` | `0,1,2,19` | `1,2,18,19` |
| 23 | 22 | 18 | 7,059,601 | `1,2,21,23` | `0,1,2,23` | `1,2,21,23` |

The validation ladder also reproduced the earlier rows:

```text
(5,4,2):  eca/emca = 1,4
(7,6,3):  eca/emca = 1,2,7
(11,10,6): eca/emca = 1,2,9,11
```

## r=2 Pattern

Across the five `m=4` rows currently checked by this affine-shear engine, the
`r=2` eca/emca values are:

```text
q=11: 9
q=13: 12
q=17: 15
q=19: 18
q=23: 21
```

This is not a single linear formula in `q`. The new points support the more
modest experimental observation that the `r=2` value stays close to, but below,
the finite-slope cap before the `r=3` row saturates.

## Non-Claims

This is not a deployed-row certificate, not a `q_chal` soundness claim, and not
an asymptotic theorem. It records finite rows checked by packet invariants and
exact argmax witness replay.
