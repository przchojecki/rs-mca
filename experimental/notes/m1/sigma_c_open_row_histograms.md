# Sigma_C Open-Row Histogram

**Status:** AUDIT / EXPERIMENTAL. The recorded finite row is a PROVED finite
enumeration; any family-level reading remains experimental.

This note records a full sparse-pair scan for the open prime-field row
`(q,n,k,r) = (13,12,6,4)`, one of the open rows listed in the companion
sparse-sigma `k=2` census contribution.

Endpoint conventions:

- `m = n-k`.
- `r = floor(delta*n)`.
- only finite slopes `gamma in F_q` are counted; there is no projective
  infinity slope.
- toy rows use `q_gen = q_line = q`; `q_chal` is unused.

The replay packet is:

```text
experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_histograms_open_rows.json
```

It is checked by:

```text
python experimental/scripts/verify_sigma_c_sparse_census.py --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_histograms_open_rows.json
```

The full scan was executed offline on a CUDA GPU accelerator; the device, CuPy
version, integer-arithmetic mode, elapsed time, and kernel source SHA-256 are
recorded in the certificate's `gpu_run` block. The committed verifier is
CPU/stdlib and replays the packet invariants and recorded witnesses; no GPU is
needed to check this contribution.

## Result

| q | n | k | m | r | pairs scanned | sigma_C | interpretation |
|---:|---:|---:|---:|---:|---:|---:|---|
| 13 | 12 | 6 | 6 | 4 | 395,359,140,961 | 13 | saturated |

This row saturates the finite-slope upper bound: `sigma_C = q_line = 13`.
Together with the earlier `k=2` boundary rows, it shows that saturation still
occurs at rate `1/2` and `m=6`, while the lower-rate `(17,8,2,r=4)` row remains
intermediate with `sigma_C = 9`.

## Histogram

```text
0: 10,654,129
1: 138,750,768
2: 1,482,624
4: 112,320
5: 1,415,232
6: 13,253,760
7: 71,839,872
8: 371,464,704
9: 2,657,640,960
10: 15,613,663,104
11: 62,457,108,480
12: 149,654,441,664
13: 164,367,313,344
```

The saturated pairs are not isolated: `164,367,313,344` sparse pairs attain
all 13 finite slopes.

## Scope

The longer row `(11,10,2,r=5)` is not claimed here. It remains the next open
histogram row in the same certificate family; a partial or unfinished scan
would not be a finite enumeration claim.

This note is not an asymptotic theorem, not a deployed-row claim, not a
`q_chal` soundness statement, and not extension-field evidence.
