# Sigma_C k=2 Boundary Map

**Status:** AUDIT / EXPERIMENTAL. The finite rows in the certificate are
PROVED finite enumerations; the family-level interpretation is experimental.

This note maps prime-field `k=2` rows in the sub-capacity band for the sparse
mutual layer from `towards-prize.tex`.

Endpoint conventions:

- `m = n-k`.
- `r = floor(delta*n)`.
- sub-capacity band means `2r > m` and `r <= m-1`.
- only finite slopes `gamma in F_q` are counted; there is no projective
  infinity slope.
- toy rows use `q_gen = q_line = q`; `q_chal` is unused.
- the evaluation domain is a multiplicative subgroup (`n | q-1`); `sigma_C`
  was checked to be invariant to this choice on the CPU-feasible rows
  (multiplicative-subgroup versus arbitrary distinct points give the same
  `sigma_C`), so the subgroup-domain rows are representative of the general
  prime-field `k=2` behaviour.

The replay packet is:

```text
experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_k2_boundary_map.json
```

It is checked by:

```text
python experimental/scripts/verify_sigma_c_sparse_census.py --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_k2_boundary_map.json
```

The full scans were executed offline on a CUDA GPU accelerator; the device,
CuPy version, integer-arithmetic mode, per-row elapsed times, and kernel source
SHA-256 are recorded in the certificate's `gpu_run` block. The committed
verifier is CPU/stdlib and replays the packet invariants and recorded
witnesses; no GPU is needed to check this contribution.

## Completed Rows

| q | n | k | m | r | pairs scanned | sigma_C | classification |
|---:|---:|---:|---:|---:|---:|---:|---|
| 7 | 6 | 2 | 4 | 3 | 2,246,689 | 7 | saturated |
| 11 | 5 | 2 | 3 | 2 | 144,601 | 5 | intermediate; CPU consistency anchor, not duplicated in the packet |
| 13 | 6 | 2 | 4 | 3 | 95,257,009 | 13 | saturated |
| 17 | 8 | 2 | 6 | 4 | 482,919,545,089 | 9 | intermediate |
| 19 | 6 | 2 | 4 | 3 | 935,066,161 | 13 | intermediate |

The new row is `(19,6,2,r=3)`, and it gives `sigma_C = 13`.
It is an intermediate row because `3 < 13 < 19`.

## Pattern Test

Earlier `k=2` intermediate rows suggested the possible pattern
`sigma_C = 2r+1`:

```text
(11,5,2,r=2): sigma_C = 5 = 2r+1
(17,8,2,r=4): sigma_C = 9 = 2r+1
```

The new row refutes that pattern:

```text
(19,6,2,r=3): sigma_C = 13, while 2r+1 = 7
```

Thus the current finite evidence is:

- the original `k>=2` immediate-saturation refinement is false;
- the narrower `k=2` intermediate-count rule `sigma_C = 2r+1` is also false;
- both saturation and intermediate behavior occur among small prime-field
  `k=2` rows.

This is evidence for a more structured boundary, not an asymptotic law.

## Planning Envelope

Rows were considered for primes `q in {3,5,7,11,13,17,19,23}`, `k=2`,
`4 <= n <= min(12,q)`, multiplicative-subgroup domains `n | q-1`, and every
sub-capacity radius.

Rows outside the kept envelope:

| q | n | r | pairs total | reason |
|---:|---:|---:|---:|---|
| 11 | 10 | 5 | 6,314,320,009,201 | long row; left open |
| 11 | 10 | 6 | 633,370,960,009,201 | beyond run envelope |
| 11 | 10 | 7 | 43,631,540,560,009,201 | beyond run envelope |
| 13 | 12 | 6 | 20,880,747,391,466,593 | beyond run envelope |
| 13 | 12 | 7 | 3,012,388,644,652,170,337 | beyond run envelope |
| 13 | 12 | 8 | 317,120,717,857,026,063,457 | beyond run envelope |
| 13 | 12 | 9 | 23,770,542,632,380,943,416,417 | beyond run envelope |
| 17 | 8 | 5 | 111,438,836,234,497 | beyond run envelope |
| 19 | 9 | 4 | 2,120,239,932,841 | beyond run envelope |
| 19 | 9 | 5 | 763,994,057,532,841 | beyond run envelope |
| 19 | 9 | 6 | 183,613,710,281,532,841 | beyond run envelope |
| 23 | 11 | 5 | 18,984,504,513,027,505 | beyond run envelope |
| 23 | 11 | 6 | 10,029,248,032,236,395,953 | beyond run envelope |
| 23 | 11 | 7 | 3,785,328,635,630,763,924,913 | beyond run envelope |
| 23 | 11 | 8 | 1,000,464,366,961,642,031,570,353 | beyond run envelope |

## Validation

The rows `(11,5,2,r=2)` and `(7,6,2,r=3)` were also scanned by the independent
CPU path because their pair counts are below `5e7`; both matched the GPU
values. The `(11,5,2,r=2)` row is kept as a consistency anchor and is not
duplicated in the packet.

## Non-Claims

This is not an asymptotic theorem, not a deployed-row claim, not a
`q_chal` soundness statement, and not extension-field evidence.
