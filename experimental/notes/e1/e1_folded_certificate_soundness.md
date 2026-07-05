# E1 Folded Certificate Soundness

Status: PROVED.

Source DAG node: `e1_folded_certificate_soundness`.

## Statement

For 2-power `N'`, the folded short-vector certificate is sound for E1: if the
complete folded search over

```text
w in {-2,-1,0,1,2}^{N'/2}
```

finds no nonzero vector with

```text
sum_x w_x zeta^x = 0 mod p,
```

then every E1 collision is cyclotomic/antipodal and there is no non-quotient
exceptional collision at that row.

## Proof

By the kernel-lattice reframing, an E1 collision at a row with `p = 1 mod N'`
is exactly a ternary vector

```text
v in {-1,0,1}^{N'}
```

with

```text
sum_x v_x zeta^x = 0 mod p,
```

modulo the already-known cyclotomic relations.

For 2-power `N'`, `zeta^{N'/2} = -1`.  Pair opposite coordinates and define

```text
w_x = v_x - v_{x+N'/2},        0 <= x < N'/2.
```

Then

```text
sum_{x<N'/2} w_x zeta^x
  = sum_{x<N'} v_x zeta^x.
```

Each `w_x` lies in `{-2,-1,0,1,2}`.  The folded vector is zero exactly for the
antipodal/cyclotomic relation `v_x = v_{x+N'/2}` at every opposite pair.

Therefore any non-cyclotomic E1 collision produces a nonzero folded vector
`w in {-2,-1,0,1,2}^{N'/2}` with folded sum zero.  A complete folded search
that finds no such nonzero `w` excludes every non-quotient E1 collision at
that row.

## Non-Claims

This packet only proves the folded-certificate implication.  It does not run
the folded no-vector search for `N'=128` or `N'=256`.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_folded_certificate_soundness.py \
  --check experimental/data/certificates/e1-folded-certificate-soundness/e1_folded_certificate_soundness.json
```

The verifier checks note anchors and a toy `N'=16` folded-kernel example.
