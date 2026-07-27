# Audit: column-far deployed certificate v1

## What is claimed, and by whom

The inequality is **DannyExperiments'**, from
`experimental/notes/thresholds/agreement_weighted_transverse_secant.md`
(merged `ea4eb078`). This packet claims only two things:

1. its **exact deployed evaluation** at the active KoalaBear MCA row, with the
   crossing located (paid through `nu = 10`; `nu = 11` first unpaid); and
2. **Lemma CF** — column-farness at radius `r` implies the per-witness
   transversality the bound requires.

The source note ends by stating it proves "no full A2, A4, A6, A7, **finite
deployed certificate**, or prize closure". This packet is precisely that missing
finite deployed certificate for the column-far branch, and claims nothing beyond
it.

## History of this packet (disclosure)

An earlier version of this branch proposed an independent per-fixed-union bound
`|Z| * C(nu+h,nu) <= C(R+nu,nu) * R` under a *global* column-far hypothesis. On
review that bound was found to be **strictly dominated** by the already-merged
`(D)`: the symbolic ratio is `(nu+h)/(h(nu+1)) ~ 1/(nu+1)`, and at this row `(D)`
pays `nu = 10` where the earlier bound fails (78289526705722101 against
861057176799343503, with `B* = 274980728111395087`). The earlier bound also
assumed *more* — global column-farness rather than per-witness transversality.
It has been withdrawn in favour of this corollary; nothing from it is claimed.

## Audit points

1. **Attribution is structural, not decorative.** The bound is never restated as
   ours; the certificate records `bound_owner` explicitly, and both verifiers
   pin the source note by content hash so the packet breaks if it drifts.
2. **Lemma CF is a one-line implication, and it is checked constructively.**
   `|supp(e_gamma)| <= r`, so `(CF1)` applied to `E = supp(e_gamma)` gives the
   hypothesis. The primary verifier re-checks this on every column-far line of
   both toy rows, not just symbolically.
3. **The `h` vs `w` convention.** This row uses the actual MCA code
   (`k = 1048576`), so `t = n - a = 981104` and `R + nu - t - 1 = 67471 + nu`.
   The printed frontier table's `w = 67471` uses the `K = k+1` boundary-Q
   convention; the two differ by one by design, and the mutation control
   `bound(R, t-1, 10) != values[10]` pins that the value is sensitive to it.
4. **Comparison with the printed table is quoted, not paraphrased.** The
   verifier recomputes `C(R+2,3)/(R-t) = 2847909263951` and asserts it equals
   the printed `eq:active-fixed-union-mca` entry, so the claim "extends `nu <= 2`
   to `nu <= 10`" is checked against the source rather than asserted.
5. **Rank-regularity is not assumed.** `(D)` carries no direction rank-regularity
   hypothesis, which is what distinguishes the extended range from the printed
   larger ranges available via `cor:rank-regular-fixed-union-ray`.
6. **One fixed union only.** Summation over unions still requires the
   witness-exhaustive atlas or subexponential shadow cover named as the exact
   remaining wall in the source note. Not supplied here, and not implied.
7. **Mersenne-31 is not touched.** The same evaluation does not extend that
   row's already paid nullity range; no claim is made there.

## Replay

```text
python3 experimental/scripts/verify_column_far_deployed_certificate_v1.py
python3 experimental/scripts/verify_column_far_deployed_certificate_v1_independent.py
```

Both are stdlib-only exact integer arithmetic. The independent replay shares no
code with the primary: it builds binomials from a factorial ladder (asserting
divisibility exactness at each step), re-derives the row from
`(p, degree, n, k, a)`, and recomputes `B* = q >> 128` from `q = p^6` rather than
quoting it. Estimated combined CPU time: under two seconds on one core.
