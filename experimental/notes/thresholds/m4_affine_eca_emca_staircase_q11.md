# m=4 affine-shear eca/emca staircase audit for F_11,n=10,k=6

Date: 2026-07-04. Status: EXPERIMENTAL / AUDIT.

## Claim

For the toy row `F_11,n=10,k=6`, the affine-shear quotient verifier computes the
exact worst-case finite-slope numerators

```text
eca_C(r)  = max over pairs of # CA-bad finite slopes
emca_C(r) = max over pairs of # MCA-bad finite slopes
```

for every sub-capacity radius `r=0,1,2,3`.

## Endpoint Conventions

```text
m = n-k = 4
agreement a = n-r
radius r = floor(delta*n), with 0 <= r <= m-1
slopes are finite gamma in F_11 only
denominator q_line = 11
CA uses the same radius r for point closeness and pair-far distance
MCA witness: exists S with |S| >= n-r, point restricted to S in C|S,
and eps2|S not in C|S
```

This is a toy finite-slope row over the base field. It is not a deployed-row
certificate, not a leaderboard entry, and not a protocol `q_chal` claim.

## Method

The verifier uses translation invariance by codeword pairs and then quotients
syndrome-class representatives by the finite-slope-preserving affine-shear
subgroup

```text
(f1,f2) -> (u*f1 + s*f2, t*f2),  u,t in F_q^*, s in F_q.
```

This is deliberately not a full `GL_2` quotient. Full `GL_2` can move finite
slopes to or from the point at infinity, so it does not preserve the finite
bad-slope numerator. The affine-shear action instead induces

```text
gamma -> (u*gamma+s)/t
```

on finite slopes, a bijection of `F_q` that fixes the point at infinity outside
the counted set.

The quotient is checked against full syndrome-class enumeration on the smaller
rows `F_5,n=4,k=2` and `F_7,n=6,k=3` before the `m=4` row is trusted. The
repo-side `--check` mode validates the emitted certificate invariants and
payload hash; it does not recompute the expensive `F_11,n=10,k=6` row.

## Result

| q | n | k | m=n-k | radii | eca_num | emca_num | sigma_num |
|---:|---:|---:|---:|---|---|---|---|
| 11 | 10 | 6 | 4 | r=0,1,2,3 | 1,2,9,11 | 1,2,9,11 | 0,1,2,11 |

The row saturates at `r=3`: all eleven finite slopes are MCA-bad for an
extremal pair. The `r=2` row is already nontrivial but not saturated:
`emca_C(2)=9`.

The certificate records the argmax pairs, bad-slope lists, affine-shear
representative count, raw syndrome-pair count, `sparsify_holds` flags, and a
stable payload hash.

## Reproducibility

```powershell
python experimental/scripts/verify_exact_worstcase_eca_emca_affine_quotient.py --check experimental/data/certificates/exact-worstcase-eca-emca-staircase/exact_worstcase_eca_emca_staircase_m4_q11_rows.json
python experimental/scripts/verify_exact_worstcase_eca_emca_affine_quotient.py --row 5,4,2 --compare-full
python experimental/scripts/verify_exact_worstcase_eca_emca_affine_quotient.py --row 7,6,3 --compare-full
python experimental/scripts/script_reproducibility_audit.py --format json
git diff --check
```

## Scope And Omitted Rows

- The natural m=4 row set for this lane also includes `F_13,n=12,k=8` and
  `F_17,n=16,k=12`. Those rows are not run here and remain open for a
  follow-up.
- No GPU-dependent row is claimed here.
- The committed verifier's `--check` path is an offline-certificate invariant
  check. The expensive row generation is disclosed as `offline_provenance:
  true` in the certificate.

## Non-Claims

- No `q=13` or `q=17` `m=4` staircase is certified here.
- No deployed-size row is certified.
- No protocol soundness, challenge-field, or asymptotic theorem is claimed.
- The affine-shear law is used only as an exact finite quotient for these
  toy-row computations; it is not promoted to a general theorem in the papers.
