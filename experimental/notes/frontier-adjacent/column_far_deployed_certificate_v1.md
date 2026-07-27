# Column-far deployed certificate for the agreement-weighted transverse-secant bound

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128; p=2130706433, extension degree 6, n=2097152, k=1048576
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
architecture: DEPLOYED_CERTIFICATE_FOR_A_MERGED_THEOREM
result: every column-far fixed-union chart with nu <= 10 is paid at the deployed
        KoalaBear row; nu = 11 is the first chart beyond the full-row budget
status: PROVED (corollary; the bound is DannyExperiments', not ours)
impact: ROUTE_CUT (finite deployed certificate only)
replay: python3 experimental/scripts/verify_column_far_deployed_certificate_v1.py
        python3 experimental/scripts/verify_column_far_deployed_certificate_v1_independent.py
```

## What this packet is, and what it is not

The inequality used here is **not ours**. It is Theorem (1)-(2) of
`experimental/notes/thresholds/agreement_weighted_transverse_secant.md`
(DannyExperiments, merged at `ea4eb078`): for a weighted Reed-Solomon parity
restriction on `|U| = R + kappa`, retained finite slopes `Z` with selected error
vectors `e_gamma` of weight `<= t < R` satisfying
`{y_0,y_1} not subset V_supp(e_gamma)`,

```text
sum_{gamma in Z} binom(|A_gamma|-1, kappa) <= binom(R+kappa, kappa+1),
|Z| <= floor( binom(R+kappa,kappa+1) / binom(R+kappa-t-1,kappa) ).      (D)
```

That note closes by stating it proves "no full A2, A4, A6, A7, **finite deployed
certificate**, or prize closure". **This packet supplies exactly the missing
finite deployed certificate for the column-far branch, and nothing else.**

Our own contribution is therefore two things only:

1. **the deployed evaluation** of `(D)` at the active KoalaBear row, in exact
   integers, with the crossing located; and
2. **the column-far binding** (Lemma CF below): the global column-far
   hypothesis of `thm:exact-sparsification` *implies* the per-witness
   transversality `(D)` needs, so `(D)` applies to **every retained column-far
   chart** without any further hypothesis.

## Lemma CF (column-farness implies the transversality hypothesis)

Let `H_U : F^U -> F^R` be an MDS parity-check restriction, `|U| = R + nu`, and
fix a syndrome line `y_0 + gamma y_1`. Say the line is **column-far at radius
`r`** if

```text
there is no E subset U, |E| <= r, with y_0, y_1 both in span(H_E).      (CF1)
```

If every `gamma in Z` has a selected error vector `e_gamma` supported on at most
`r` coordinates, then for each such `gamma`, `|supp(e_gamma)| <= r`, so `(CF1)`
applied to `E = supp(e_gamma)` gives `{y_0,y_1} not subset V_supp(e_gamma)` —
precisely the hypothesis of `(D)`. Hence `(D)` holds for the whole line.

**Binding.** For the actual RS parity check, `(CF1)` at `r = n - a` is exactly
the column-far branch of `thm:exact-sparsification`: if both syndromes lay in
`span(H_E)` with `|E| <= n - a`, the received pair would differ from a codeword
pair only on `E` and hence carry common agreement at least `a`. So every chart
retained on the column-far side satisfies the hypothesis of `(D)` automatically.
The non-column-far side remains owned by the sparse normalized term; this packet
does not pay it.

## Exact deployed evaluation

At the active row `R = n - k = 1048576`, `r = n - a = 981104`, so
`R + nu - t - 1 = 67471 + nu`:

| `nu` | `(D)` at the deployed row | `<= B*` |
|---:|---:|:--:|
| 0 | 1048576 | yes |
| 1 | 8147918 | yes |
| 2 | 84416263 | yes |
| 3 | 983902549 | yes |
| 4 | 12232092309 | yes |
| 5 | 158406193634 | yes |
| 6 | 2109949210211 | yes |
| 7 | 28689347099870 | yes |
| 8 | 396280526311830 | yes |
| 9 | 5542092977392141 | yes |
| **10** | **78289526705722101** | **yes** |
| 11 | 1115145741750273207 | no |

`B* = 274980728111395087`. **Every column-far fixed-union chart with
`nu <= 10` is paid; `nu = 11` is the first that is not.**

For comparison, the printed unconditional fixed-union table
(`eq:active-fixed-union-mca`) pays `0 < nu <= 2` at this row via
`thm:fixed-union-ray`, and the larger ranges there require direction
rank-regularity. `(D)` needs no rank-regularity hypothesis, so the certified
column-far range extends from `nu <= 2` to `nu <= 10`.

## Scope and nonclaims

- The inequality is DannyExperiments'; this packet claims only its deployed
  evaluation and Lemma CF.
- **One fixed union is paid.** Summing over unions still requires the
  witness-exhaustive atlas or subexponential shadow cover that the source note
  names as its exact remaining wall. Nothing here supplies it.
- This is not `U_BC`, `U_Q`, `U_paid`, or a row certificate; no KoalaBear
  endpoint moves.
- For the Mersenne-31 MCA row the same evaluation does not extend the already
  paid nullity range.
- Residual after this cut: non-column-far/sparse pairs; column-far charts with
  `nu >= 11`; and aggregation across retained unions.

## Provenance and replay

Source pin: `main@b13de811`. Read-only source hashes are recorded in the
certificate. Both replays are stdlib-only exact integer arithmetic; the primary
verifier additionally re-derives `(D)` from the source note's stated form,
exhausts two toy MDS syndrome-line rows, checks Lemma CF constructively on
those toys, and confirms that dropping column-farness produces an all-slope
counterexample. Estimated combined CPU time: under two seconds on one core.
