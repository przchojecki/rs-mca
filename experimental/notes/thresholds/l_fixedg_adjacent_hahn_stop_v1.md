# M31 fixed-G adjacent-interior Hahn stop

```yaml
workboard_item: L
row: Mersenne-31 list at 2^-100, fixed-G ordinary boundary adjacent symmetric pair (d,m) = (5413,72860) and (840822,908269)
object: LIST
target_epsilon: 2^-100
agreement: 72860 and 908269
B_star: 16777215
direct_statement: The complete ordinary Johnson-scheme Hahn/Delsarte relaxation for the adjacent fixed-G boundary pair has exact optimum 24044092640301071703360149280/1159431963847722545269 = 20737821.0968..., certified by matching primal and dual solutions. Hence L <= 20737821 unconditionally at both adjacent rows, improving the prior two-shortening cap 30682446 by 9944625, and no argument using only the ordinary pairwise intersection distribution can reach the required 16777214, which the optimum exceeds by 3960607. Under the single named hypothesis RS_H3_QUARTER_GAP the same dual gives L <= 16032481 <= 16777214.
architecture: DIRECT
partition_digest: n/a (DIRECT)
atom_or_cell: DIRECT fixed-G ordinary boundary adjacent-pair Hahn route cut
quantifier: every 981129-point boundary subset E0, every received word over F_p, and every family of distinct polynomials of degree less than d at agreement at least m, for either adjacent row; the conditional clause additionally assumes RS_H3_QUARTER_GAP uniformly on the selected-support family
projection_and_unit: ordinary Reed-Solomon codewords in one Hamming ball; selected agreement supports are injective; no MCA numerator, ray, or slope count
claimed_bound: unconditional all-degree Hahn relaxation floor 20737821, exceeding 16777214 by 3960607; conditional ordinary list cap 16032481 with margin 744733
status: PROVED
impact: ROUTE_CUT
falsifier: for the route cut, a feasible all-degree Hahn value away from the exact rational optimum, a negative certified primal moment, or a positive dual value at an allowed integer intersection; for the conditional clause, an adjacent-row selected-support family whose normalized third Hahn moment is below 1/4
replay: cd experimental/lean/l_fixedg_adjacent_hahn_stop && lake clean && lake build   (stdlib-only, no dependencies, clean build under 2 s; native_decide disclosed)
```

- **Date:** 2026-07-24.
- **Author:** Holm Buar.
- **Base:** `b13de81`.

## 1. Frozen problem and result

Over the base field `F_p`, `p = 2^31 - 1 = 2147483647`, on every allowed
`N`-point boundary subset `E0` of the deployed domain, with

```text
N = 981129,   w = 67447,   D = w + 1 = 67448,   B* = 16777215,
ell = B* - 1 = 16777214.
```

For each `1 <= d <= N - w` and `m = d + w`, the ordinary list question is a
received-word-uniform upper bound on

```text
#{ f in F_p[X] : deg f < d,  agr_{E0}(f, r) >= m }.
```

The integrated endpoint packet proves `L <= 2310492` at the two endpoints
`(d,m) = (5412,72859)` and `(840823,908270)` of the Johnson-negative interval.
The **first undecided symmetric pair immediately inside it** is

```text
(d,m) = (5413,72860)   and   (840822,908269).
```

At that pair the integrated packet leaves only the unstructured two-incidence
shortening cap `L <= 30682446`.

**Theorem 1 (unconditional, complete Hahn-LP route stop).** After selecting one
`m`-point agreement set per ordinary Reed-Solomon codeword and complementing on
the high-agreement side, both adjacent rows reduce to a constant-weight code in
`J(981129, 72860)` with minimum exchange distance `67448`. The complete
Johnson-scheme Delsarte linear program, with every Hahn degree `0,...,72860`,
has exact optimum

```text
H = 24044092640301071703360149280 / 1159431963847722545269
  = 20737821.096899...
```

Consequently

```text
L <= floor(H) = 20737821
```

at both adjacent rows. This improves the prior two-shortening cap by

```text
30682446 - 20737821 = 9944625,
```

but exceeds the required ordinary-list target by

```text
20737821 - 16777214 = 3960607.
```

**No interior agreement is paid.** Because the value is the *optimum* and not
merely a feasible upper certificate, no argument using only the ordinary
pairwise intersection distribution and Johnson-scheme positivity — at any Hahn
degree — can extend the endpoint theorem to this pair. That is the route cut.

**Theorem 2 (conditional, one named hypothesis).** For a selected-support
family, let `G_3 = 1 + sum_e A_e H_3(e)` be its normalized third Hahn moment,
`A_e` the ordered inner distribution divided by family size. Assume

```text
RS_H3_QUARTER_GAP:
For every selected-support family arising from either adjacent ordinary-RS
row, G_3 >= 1/4.
```

Then every ordinary list at either adjacent row satisfies

```text
L <= 16032481 <= 16777214,
```

with exact safety margin `744733`. Adding the canonical fixed-`G` zero anchor
gives at most `16032482` codewords in the fixed-`G` ball, again `744733` below
`B*`. The hypothesis is deliberately stronger than needed and has one direct
falsifier: an actual adjacent-row selected-support family with `G_3 < 1/4`.
`RS_H3_QUARTER_GAP` is an assumption. Theorem 2 must not be quoted
unconditionally.

## 2. Exact Lane-L print blocks

```text
row:                 (F_p, E0 subset D, d=5413, n=981129, rho=5413/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=908269/981129 and integer agreement 72860=d+67447
Johnson comparison:  exact finite-p, ell=16777214 Johnson radius 908260/981129;
                     post-Johnson gap 9/981129
bound:               complete all-degree Hahn relaxation floor = 20737821
                     > 16777214 by 3960607; under RS_H3_QUARTER_GAP, L <= 16032481
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS_Fp(E0,5413); no C^+ shift
status:              PROVED ROUTE CUT / CONDITIONAL LIST BOUND
```

```text
row:                 (F_p, E0 subset D, d=840822, n=981129, rho=840822/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=72860/981129 and integer agreement 908269=d+67447
Johnson comparison:  exact finite-p, ell=16777214 Johnson radius 72859/981129;
                     post-Johnson gap 1/981129
bound:               complete all-degree Hahn relaxation floor = 20737821
                     > 16777214 by 3960607; under RS_H3_QUARTER_GAP, L <= 16032481
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS_Fp(E0,840822); no C^+ shift
status:              PROVED ROUTE CUT / CONDITIONAL LIST BOUND
```

## 3. Post-Johnson position of the pair

With the exact finite-`p` Johnson condition in the form

```text
Lhs(a) = (ell-1) (p a - N)^2
Rhs(d) = N^2 (p-1)^2 (ell-1) - N (p-1) p ell (N - (d-1)),
```

`Lhs` is strictly increasing in `a`, so `Lhs(a) >= Rhs(d)` — the regime where
Johnson already gives `L <= ell` — begins at a single threshold agreement. The
threshold is located on both sides:

```text
low row  d = 5413:    Rhs - Lhs(72868) = 5205542238636045247040359936547 > 0   (not covered)
                      Lhs(72869) - Rhs = 6070309882968202312269231869644 > 0   (covered)
high row d = 840822:  Rhs - Lhs(908269) = 99216260018857531361012790918704 > 0 (not covered)
                      Lhs(908270) - Rhs = 41331612211590842518015690016521 > 0 (covered)
```

So Johnson covers agreements from `72869` (low) and `908270` (high), i.e. error
radii `908260` and `72859`. The audited pair sits at error radii `908269` and
`72860`, which is

```text
908269 - 908260 = 9    and    72860 - 72859 = 1
```

coordinates beyond the exact finite-field Johnson radius. Both rows are
genuinely post-Johnson. The shared classical Johnson deficit of the pair is
`N (d-1) - m^2 = 1290548` in both rows; it is recorded for orientation only and
pays nothing.

## 4. Matching Hahn certificates

For `0 <= j <= 72860` the normalized Johnson zonal function is

```text
H_j(i) = sum_{t=0}^{j} (-1)^t C(j,t) C(981130-j,t) C(i,t) / ( C(72860,t) C(908269,t) ).
```

### 4.1 Dual upper certificate

With `F(i) = 1 + f_1 H_1(i) + f_2 H_2(i) + f_3 H_3(i)` and

```text
f_1 = 979061542845605776592576657442 / 21065719351149270924992461
f_2 = 2127197006408557278777618631055673 / 1137547685530096782227047625
f_3 = 389001796223311531724035804630343856388 / 20668103898396328436283228298625
```

all three coefficients are positive, and exact simplification gives the cubic

```text
F(i) = - (118055716980403503 / 1924657059987219425146540)
         (i - 67448) (i - 70799) (i - 70800).
```

The leading coefficient is negative and the roots are `67448 < 70799 < 70800`,
so the only interval where `F` could be positive lies strictly between the
consecutive integers `70799` and `70800` and contains no integer. Hence
`F(i) <= 0` at every allowed integer distance, and Delsarte duality gives
`L <= F(0) = 1 + f_1 + f_2 + f_3`.

### 4.2 Full-degree primal certificate

Fractional inner-distribution mass sits at distances `67448, 70799, 70800`
(intersections `5412, 2061, 2060`) with positive weights

```text
y_0 = 11248760258723433202306504856279750 / 542640826015902648804433187
y_1 = 5964107581872309468780632000 / 1295085503617906083065473
y_2 = 1726595658518143191722829859 / 485801992852195746467711.
```

The primal Hahn constraints are tight in degrees `1, 2, 3`. Every degree
`4,...,490` has strictly positive slack; the minimum over that range occurs at
degree `5` and equals

```text
550052954011442897244763831709362374052806653649987382880740
-----------------------------------------------------------
551410447208318265674262258763948662468585127118502801971127
```

For the tail, with `v_i = C(72860,i) C(908269,i)`, `|X| = C(981129,72860)` and
`mu_j = C(981129,j) - C(981129,j-1)`, Johnson orthogonality and weighted Cauchy
give

```text
| sum_r y_r H_j(i_r) |^2  <=  ( sum_r y_r^2 / v_{i_r} ) |X| / mu_j,
```

whose exact right side is below one at `j = 491`. Moreover `mu_{j+1}/mu_j > 1`
through `j = 72859`, because the cross-product margin `(981129 - 2j)^2 - 981131`
has minimum `697910557790 > 0` on the range. Every remaining primal constraint
is therefore strictly feasible.

Finally

```text
1 + y_0 + y_1 + y_2 = 1 + f_1 + f_2 + f_3
                    = 24044092640301071703360149280 / 1159431963847722545269.
```

Primal and dual values coincide, so this rational is the exact optimum of the
complete finite Hahn/Delsarte LP, not merely a degree-three upper certificate.
This is what upgrades a bound into a route cut.

## 5. Independent derivation and replication

The result was derived twice, independently, from the same frozen contract.
Both derivations produced the identical exact optimum, the identical cubic dual
factorization, and the same primal support `{67448, 70799, 70800}`.

Every load-bearing value was then re-derived a third time from the frozen
parameters alone, in exact rational arithmetic, and — importantly —
independently of this packet's own Hahn recurrence, using the direct zonal
formula above. That pass confirmed: the dual factorization identity as an exact
polynomial identity; `F(i) <= 0` at every allowed integer distance with roots
exactly at `67448, 70799, 70800`; `F(0)` equal to the printed optimum;
`1 + f_1 + f_2 + f_3 = 1 + y_0 + y_1 + y_2`; primal tightness in degrees
`1, 2, 3`; strictly positive slack across degrees `4..490` with the minimum at
degree `5` matching the printed 60-digit rational digit-for-digit; the
degree-`491` tail bound below one; the multiplicity margin `697910557790`; and
both Johnson thresholds with their `9` and `1` coordinate gaps.

## 6. Kernel-checked evidence

`experimental/lean/l_fixedg_adjacent_hahn_stop/` (stdlib-only, no Mathlib, no
`sorry`) proves the frozen parameter identities, the row partitions and
complement symmetry, both classical and exact finite-Johnson deficits with the
`9`/`1` gaps, positivity of all primal weights and dual coefficients, the dual
cubic factorization and its nonpositivity at every allowed integer intersection,
primal tightness in degrees `1-3`, agreement of the Hahn recurrence with the
direct formula through degree `3`, strictly positive primal prefix slack through
degree `490`, the tail gate at degree `491`, and the coincidence of the primal
and dual objectives with `floor(H) = 20737821`.

`native_decide` is used and disclosed; the axiom census reports exactly one
`native_decide` axiom per theorem and no `sorryAx`. Because the Lean package
cross-checks its recurrence against the direct formula only through degree `3`,
the independent direct-formula pass of section 5 across degrees `4..490` is the
evidence that the recurrence-based slack theorem is checking the intended
quantity.

## 7. Nonclaims

- The optimum is a **relaxation value, not a construction.** The primal
  certificate is fractional; it exhibits no Reed-Solomon list of size
  `20737821`, gives no lower bound, and does not refute the target row.
- `L <= 20737821` does **not** pay any interior agreement: it is `3960607`
  above `B* - 1`.
- Theorem 2 is conditional on `RS_H3_QUARTER_GAP`, which is an assumption, not
  a theorem.
- The route cut is scoped exactly to the ordinary pairwise intersection
  distribution on the selected supports. It does not rule out routes using
  information absent from that distribution.
- No MCA numerator, ray, slope, or CA/MCA conversion appears anywhere in this
  packet. Nothing here is a payment or a bankable atom.

## 8. Named successor

Any argument that closes this pair must use information absent from the ordinary
Johnson distribution. The two most natural candidates:

1. a two-coordinate / Terwilliger semidefinite constraint, which sees triples
   the pairwise distribution cannot; or
2. an RS-specific fixed-syndrome or polynomial-fibre condition, which uses that
   the codewords are low-degree polynomials rather than arbitrary
   constant-weight words.

The open quantitative question is whether a small Terwilliger relaxation already
pushes the adjacent optimum below `16777214`, or whether the gap `3960607` is
intrinsic to all bounded-order relaxations.

## 9. Replay

```bash
cd experimental/lean/l_fixedg_adjacent_hahn_stop && lake clean && lake build
```

Stdlib-only, no dependencies, clean build under two seconds.
