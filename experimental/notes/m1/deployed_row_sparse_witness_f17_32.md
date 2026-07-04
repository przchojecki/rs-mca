# Deployed-row sparse witness over F_17^32

Date: 2026-07-04

Status: PROVED / EXPERIMENTAL

## Claim

For the deployed-shaped row

```text
C = RS[F_17^32, H, 256],   |H| = 512,
m = n-k = 256,             r = 129,
```

the moving-zero construction from
`experimental/notes/thresholds/cap25_v12_sparse_sigma_first_layer_audit.md`
exhibits one sparse pair with at least

```text
n-k+2 = 258
```

distinct finite MCA-bad slopes.

This proves the displayed finite witness by construction.  Its interpretation
as evidence for `prob:mutual` is EXPERIMENTAL.

## Endpoint Conventions

```text
r = floor(delta n)
finite slopes only
q_line = 17^32
q_gen = 17
q_chal = null
support union size <= r
```

At this row,

```text
2r = 258 >= m+1 = 257,
2 <= r <= m-1,
k >= 2.
```

So the moving-zero lower-bound hypotheses apply at the sparse half-distance
onset `r=129`.

## Certificate

The certificate is:

```text
experimental/data/certificates/deployed-sparse-witness-f17-32/deployed_sparse_witness_f17_32_r129.json
```

It uses the tower representation from
`experimental/scripts/verify_m1_cycle120_self_contained_certificate.py`:

```text
F16 = F_17[X] / (X^16 + X^8 + 3)
F_17^32 = F16[theta] / (theta^2 - 6X^9)
H = <theta>, |H| = 512.
```

The deterministic construction takes:

```text
Z_* = H indices 0..253,       |Z_*| = k-2 = 254
E'  = H indices 254..382,     |E'| = r = 129
X   = H indices 383..511,     |X| = m-r+2 = 129
Pi(X) = product_{z in Z_*}(X-z).
```

On `E'`,

```text
epsilon_1(j) = j Pi(j),
epsilon_2(j) = -Pi(j),
```

and both sparse words are zero outside `E'`.

The certificate records the `Pi` coefficients, the sparse pair values on
`E'`, and one record for each tangent or moving-zero slope.  For moving-zero
records it stores the exact derivation `(X-x)Pi` and a coefficient hash instead
of repeating the full 256-coefficient vector in every record; the verifier
reconstructs and checks the coefficients from first principles.

The committed JSON blob is `2,117,771` bytes.  This is larger than the usual
certificate packets in this repository because the file keeps 258
first-principles per-slope witness records at `n=512`, including the supports
and closing-codeword data needed for exact replay.  Slimming it would weaken
the certificate unless the maintainer prefers a variant with sampled records
plus a regeneration command.

## Result

```text
tangent slopes:      129
moving-zero slopes:  129
total certified:     258
support size:        384
required support:    383
```

For `x in H \ (Z_* union E')`, the close codeword is

```text
z_x(X) = (X-x)Pi(X),  deg z_x = 255 < 256,
S_x = Z_* union E' union {x}, |S_x| = 384.
```

The one-sided mutual failure follows because any degree `<256` extension of
`epsilon_2` on `S_x` would vanish on `Z_* union {x}`, so it would be
`c(X-x)Pi(X)`.  Two distinct points of `E'` force incompatible values of `c`.

For tangent slopes `gamma=j_0 in E'`, the zero codeword agrees on
`(H \ E') union {j_0}` and `epsilon_2` is not degree `<256` explainable on that
same support.

## Reproducibility

Full replay:

```powershell
py -3.13 experimental\scripts\verify_deployed_sparse_witness_f17_32.py --check experimental\data\certificates\deployed-sparse-witness-f17-32\deployed_sparse_witness_f17_32_r129.json --full
```

Observed locally on 2026-07-04:

```text
F_17^32 deployed sparse moving-zero witness
status: PROVED / EXPERIMENTAL
row: F_17^32 n=512 k=256 r=129
certified_bad_slopes: 258
checked_records: 258/258
```

## Non-Claims

- This is not an upper bound on `sigma_C`.
- This is not a leaderboard row.
- This is not a deployed soundness claim.
- This does not supersede or extend the CAP25 sparse first-layer audit.
- The raw finite-slope numerator does clear the `2^-128` gate because
  `floor(17^32 / 2^128) = 6`, but this is only a sparse-witness lower bound at
  `r=129`; it is not a deployed threshold or cap certificate.
