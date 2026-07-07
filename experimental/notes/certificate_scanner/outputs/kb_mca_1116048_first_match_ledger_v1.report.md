# KB-MCA 1116048 first-match ledger v1 report

Status: `CONDITIONAL`.

This report records exact arithmetic for the KoalaBear MCA adjacent candidate `A=1116048`
partial first-match ledger and discharges the generated-field collision image-cell bucket
plus terminal raw-paid quotient/planted rungs.
It does not prove `U(1116048) <= B*`, the first-safe agreement, or primitive Q-fin flatness.

## Deployed constants

- `p = 2130706433`.
- `q_gen = 2130706433`.
- `q_line = p^6 = 93571093019388561295270373781649880353786165192103559169`.
- `q_chal = None`.
- `q_list = None`.
- `B* = floor((q_line - 1)/2^128) = 274980728111395087`.
- `(n,k,A,j,t,w) = (2097152, 1048576, 1116048, 981104, 67472, 67471)`.
- `log2(avg) = 35.735246414552`.
- `raw margin = 22.196861710144` bits.
- `K_raw = 4807520`.

## Generated-field collision bucket

- `B_gen <= t*p = 143763024447376`.
- `B_rem_after_gen = B* - B_gen = 274836965086947711`.
- `K_after_gen = 4805007`.

This is an image-cell cost over base generated slopes.  It is not a raw support bound.

## Q0 quotient/planted rung audit

Status: `PROVED_DESCENT_WITH_TERMINAL_RAW_PAID_ROWS_AND_EXPLICIT_LOWER_RUNG_OBLIGATIONS`.

The dyadic quotient/planted descent theorem injects each covered top fiber
into a lower prefix fiber when `r_c <= w`.  The terminal covered rungs
`c=65536` and `c=131072` are paid by raw lower quotient count.

- `B_quot_terminal = 471447040`.
- `B_rem_after_gen_and_terminal_quotient = 274836964615500671`.
- `K_after_gen_and_terminal_quotient = 4805007`.
- exact quotient-descent rungs needing lower bounds: `[2, 4, 8, 16]`.
- planted-descent rungs needing lower bounds: `[32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]`.
- open planted-tail rungs: `[262144, 524288, 1048576, 2097152]`.

| c | n_c | A_c | j_c | r_c | w_c | status | K_c |
| -: | -: | -: | -: | -: | -: | --- | -: |
| 1 | 2097152 | 1116048 | 981104 | 0 | 67471 | `TOP_PRIMITIVE_TARGET` | 4805007 |
| 2 | 1048576 | 558024 | 490552 | 0 | 33735 | `PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 749194961 |
| 4 | 524288 | 279012 | 245276 | 0 | 16867 | `PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 7866613560 |
| 8 | 262144 | 139506 | 122638 | 0 | 8433 | `PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 21435171266 |
| 16 | 131072 | 69753 | 61319 | 0 | 4216 | `PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 29753587796 |
| 32 | 65536 | 34877 | 30659 | 16 | 2108 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 1451233453254335 |
| 64 | 32768 | 17439 | 15329 | 48 | 1054 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 269518971028625790 |
| 128 | 16384 | 8720 | 7664 | 112 | 527 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 3088723598520252665 |
| 256 | 8192 | 4360 | 3832 | 112 | 263 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 178584294092863 |
| 512 | 4096 | 2180 | 1916 | 112 | 131 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 1141899454925 |
| 1024 | 2048 | 1090 | 958 | 112 | 65 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 76786108785 |
| 2048 | 1024 | 545 | 479 | 112 | 32 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 16745284864 |
| 4096 | 512 | 273 | 239 | 2160 | 16 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 324102591630340 |
| 8192 | 256 | 137 | 119 | 6256 | 8 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 38033798950172476 |
| 16384 | 128 | 69 | 59 | 14448 | 4 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 348610218401621578 |
| 32768 | 64 | 35 | 29 | 30832 | 2 | `PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND` | 898414905870876045 |
| 65536 | 32 | 18 | 14 | 63600 | 1 | `PROVED_DESCENT_AND_RAW_PAID` | 1242156698671972696 |
| 131072 | 16 | 9 | 7 | 63600 | 0 | `PROVED_DESCENT_AND_RAW_PAID` | 24024210193662 |
| 262144 | 8 | 5 | 3 | 194672 | 0 | `OPEN_PLANTED_TAIL_R_GREATER_THAN_W` | 4907802939562511 |
| 524288 | 4 | 3 | 1 | 456816 | 0 | `OPEN_PLANTED_TAIL_R_GREATER_THAN_W` | 68709241153875167 |
| 1048576 | 2 | 2 | 0 | 981104 | 0 | `OPEN_PLANTED_TAIL_R_GREATER_THAN_W` | 274836964615500671 |
| 2097152 | 1 | 1 | 0 | 981104 | 0 | `OPEN_PLANTED_TAIL_R_GREATER_THAN_W` | 274836964615500671 |

Q0 lower-rung obligations:

| c | n_c | j_c | w_c | required K_c |
| -: | -: | -: | -: | -: |
| 2 | 1048576 | 490552 | 33735 | 749194961 |
| 4 | 524288 | 245276 | 16867 | 7866613560 |
| 8 | 262144 | 122638 | 8433 | 21435171266 |
| 16 | 131072 | 61319 | 4216 | 29753587796 |
| 32 | 65536 | 30659 | 2108 | 1451233453254335 |
| 64 | 32768 | 15329 | 1054 | 269518971028625790 |
| 128 | 16384 | 7664 | 527 | 3088723598520252665 |
| 256 | 8192 | 3832 | 263 | 178584294092863 |
| 512 | 4096 | 1916 | 131 | 1141899454925 |
| 1024 | 2048 | 958 | 65 | 76786108785 |
| 2048 | 1024 | 479 | 32 | 16745284864 |
| 4096 | 512 | 239 | 16 | 324102591630340 |
| 8192 | 256 | 119 | 8 | 38033798950172476 |
| 16384 | 128 | 59 | 4 | 348610218401621578 |
| 32768 | 64 | 29 | 2 | 898414905870876045 |

## Q1 exact split-prefix collision ledger

Status: `PROVED_EXACT_PAIR_DECOMPOSITION_AND_TOY_REPLAY`.

sum_z N_w(z)^2 = binom(n,j) + sum_{e=w+1}^{min(j,n-j)} C_e, where C_e counts ordered distinct support pairs with one-sided difference e and equal first w locator-prefix coefficients.

C_e = sum_{I subset D, |I|=j-e} P_w(D\I,e), where P_w(E,e) counts ordered disjoint e-subsets A,B of E with deg(Lambda_A - Lambda_B) <= e-w-1.

For e=w+1, the condition becomes Lambda_A - Lambda_B is constant; these are the constant-shift split-pair packets.

- deployed minimum nontrivial one-sided difference: `67472`.
- deployed forbidden one-sided differences: `1..67471`.
- `gcd(n,w+1) = 16`.
- `w+1` divides `n`: `False`.

Toy replay cases:

| field | n | j | w | supports | fibers | max fiber | second moment | min e>0 |
| --- | -: | -: | -: | -: | -: | -: | -: | -: |
| F_17 | 8 | 3 | 1 | 56 | 16 | 4 | 200 | 2 |
| F_17 | 16 | 5 | 2 | 4368 | 289 | 17 | 66672 | 3 |
| F_17 | 16 | 8 | 3 | 12870 | 4881 | 7 | 38356 | 4 |
| F_97 | 16 | 8 | 2 | 12870 | 6225 | 8 | 36724 | 3 |

Q1 proves the exact collision decomposition and the low-distance gap.
It does not evaluate all deployed `C_e` summands and does not prove
the finite worst-case max-fiber bound.

## Q2 heavy-fiber twist-stabilizer descent

Status: `PROVED_STABILIZER_FORCING_CONDITIONAL_ON_HEAVY_COUNT_BOUND`.

The mu_n twist action sends a prefix target (z_1,...,z_w) to (eta z_1, eta^2 z_2, ..., eta^w z_w) and preserves fiber size. If a heavy-target set has size at most M, every heavy target has twist orbit size at most M.  Hence if M<=n/h, its stabilizer has size at least h and its nonzero prefix coordinates occur only at indices divisible by h.

Deployed stabilizer thresholds:

| forced stabilizer >= h | sufficient heavy-target count <= | quotient depth floor(w/h) |
| -: | -: | -: |
| 2 | 1048576 | 33735 |
| 4 | 524288 | 16867 |
| 8 | 262144 | 8433 |
| 16 | 131072 | 4216 |
| 32 | 65536 | 2108 |
| 64 | 32768 | 1054 |
| 128 | 16384 | 527 |
| 256 | 8192 | 263 |

Toy replay cases:

| field | n | j | w | max fiber | heavy targets | heavy < n? | stabilizers |
| --- | -: | -: | -: | -: | -: | --- | --- |
| F_17 | 8 | 3 | 1 | 4 | 8 | False | `{'1': 8}` |
| F_17 | 16 | 8 | 3 | 7 | 8 | True | `{'2': 8}` |
| F_97 | 16 | 8 | 2 | 8 | 16 | False | `{'1': 16}` |

Q2 proves the symmetry/stabilizer forcing step.  It still needs an
evaluated heavy-target bound from Q1/higher moments before it can
activate the folding theorem below.

## Q2 stabilized-fiber folding rigidity

Status: `PROVED_EXACT_LIFT_FINITE_CONDITIONAL_ON_GENERATED_PREFIX_BUCKET`.

If an exact lifted prefix target is h-stabilized and h/2<=w, then every support in that exact lifted fiber is a union of h-cosets.

Finite KoalaBear use is conditional on the generated first-match
bucket including prefix-coordinate lift collisions.  Under that
wrapper, generated-prefix cells use at most:

- `w*p = 143760893740943`.
- budgeted `t*p = 143763024447376`.
- slack `2130706433`.

Quotient-descended stabilizers: `[2, 4, 8, 16]`.
Empty exact-lift stabilizers: `[32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]`.
Not applicable because `h/2>w`: `[262144, 524288, 1048576, 2097152]`.

| h | h/2 | n/h | j/h or rem | floor(w/h) | exact-lift outcome |
| -: | -: | -: | ---: | -: | --- |
| 2 | 1 | 1048576 | 490552 | 33735 | `QUOTIENT_DESCENT` |
| 4 | 2 | 524288 | 245276 | 16867 | `QUOTIENT_DESCENT` |
| 8 | 4 | 262144 | 122638 | 8433 | `QUOTIENT_DESCENT` |
| 16 | 8 | 131072 | 61319 | 4216 | `QUOTIENT_DESCENT` |
| 32 | 16 | 65536 | rem 16 | 2108 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 64 | 32 | 32768 | rem 48 | 1054 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 128 | 64 | 16384 | rem 112 | 527 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 256 | 128 | 8192 | rem 112 | 263 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 512 | 256 | 4096 | rem 112 | 131 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 1024 | 512 | 2048 | rem 112 | 65 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 2048 | 1024 | 1024 | rem 112 | 32 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 4096 | 2048 | 512 | rem 2160 | 16 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 8192 | 4096 | 256 | rem 6256 | 8 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 16384 | 8192 | 128 | rem 14448 | 4 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 32768 | 16384 | 64 | rem 30832 | 2 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 65536 | 32768 | 32 | rem 63600 | 1 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 131072 | 65536 | 16 | rem 63600 | 0 | `EMPTY_AFTER_GENERATED_PREFIX_REMOVAL` |
| 262144 | 131072 | 8 | rem 194672 | 0 | `NOT_APPLICABLE_H_OVER_2_GREATER_THAN_W` |
| 524288 | 262144 | 4 | rem 456816 | 0 | `NOT_APPLICABLE_H_OVER_2_GREATER_THAN_W` |
| 1048576 | 524288 | 2 | rem 981104 | 0 | `NOT_APPLICABLE_H_OVER_2_GREATER_THAN_W` |
| 2097152 | 1048576 | 1 | rem 981104 | 0 | `NOT_APPLICABLE_H_OVER_2_GREATER_THAN_W` |

Thus a stabilized target is not remaining top-rung primitive mass after
generated-prefix lift collisions are removed: it either descends to
one of the Q0 quotient rungs `h=2,4,8,16`, or is empty in the exact
lift for `h=32,...,131072`.

## Q2 heavy-fiber closure theorem

Status: `CONDITIONAL_ON_PRIMITIVE_HEAVY_ORBIT_EXCLUSION`.

If primitive-heavy-orbit exclusion holds, every threatening target has nontrivial dyadic stabilizer.  After generated-prefix lift-collision removal, Q2 folding sends each such target to quotient descent when h divides j, or to an empty exact-lift branch when h does not divide j.

The remaining open input is the primitive-heavy-orbit exclusion certificate:

```text
For every trivial-stabilizer prefix-target orbit O, N_pre(O) * p^w <= 4805007 * binom(n,j).
```

The stronger global count bound

```text
|{z : |R_pre(z)| > threshold}| <= 1048576
```

would imply this, but is not necessary.

Generated-prefix lift collisions on certified heavy targets are covered by:

- cell model: `heavy-target-local prefix lift collision cells (z,d)`.
- separate worst-case cells at `h=2`: `70748471296`.
- existing generated allowance `t*p`: `143763024447376`.
- `K` if deducted separately: `4805006`.

Do not claim no new cost unless these generated-prefix cells are explicitly
coalesced into the generated first-match bucket.

Lower-rung exact-lift certificates for quotient-descended heavy targets:

| h | N | J | W | K_h | exact-lift max fiber | status |
| -: | -: | -: | -: | -: | -: | --- |
| 2 | 1048576 | 490552 | 33735 | 749194961 | 11440 | `PROVED_EXACT_LIFT_FINITE_USE_REQUIRES_GENERATED_PREFIX_BUCKET` |
| 4 | 524288 | 245276 | 16867 | 7866613560 | 11440 | `PROVED_EXACT_LIFT_FINITE_USE_REQUIRES_GENERATED_PREFIX_BUCKET` |
| 8 | 262144 | 122638 | 8433 | 21435171266 | 11440 | `PROVED_EXACT_LIFT_FINITE_USE_REQUIRES_GENERATED_PREFIX_BUCKET` |
| 16 | 131072 | 61319 | 4216 | 29753587796 | 11440 | `PROVED_EXACT_LIFT_FINITE_USE_REQUIRES_GENERATED_PREFIX_BUCKET` |

These four exact-lift bounds do not prove finite lower-rung flatness by
themselves; finite use still requires generated-prefix lift collision
handling.  They do show that once lifted, the descended rows are far below
their printed `K_h * average` targets.

Conditional pointwise route:

If for every finite prefix target z the first-match ledger may retain one exact lifted prefix class and charge all other exact lift classes over z as generated-prefix collisions, then every residual finite fiber is contained in one exact lifted fiber and has size <=11440.  This would imply no target is heavy.

The assignment depends on the finite target z and its retained exact lift class.  A row-indexed w*p image-cell count does not by itself bound the number of removed exact lift classes or raw supports.  The packet records this as a conditional route and adds a small finite replay showing that the naive image-cell to support-payment inference is false.

The exact remaining support-level certificate is:

```text
(|G_gen_prefix(z)| + 11440) * p^67471 <= 4805007 * binom(2097152,981104) for every primitive target z.
```

A convenient stronger bound would be:

```text
|G_gen_prefix(z)| <= t*p = 143763024447376
```

Since each retained exact-lift class is already <=11440, bounding the non-retained generated-prefix support mass is equivalent, up to 11440, to the finite primitive prefix-fiber bound for that target.

## Generated-prefix support-payment counterexample

Status: `COUNTEREXAMPLE_TO_NAIVE_SUPPORT_PAYMENT_FROM_IMAGE_CELLS`.

This small replay shows why a generated-prefix image-cell label is not
a support/fiber payment.

| field | n | j | w | primitive target | finite fiber | exact lift classes | largest lift class | non-retained supports | w*p |
| --- | -: | -: | -: | -: | -: | -: | -: | -: | -: |
| F_17 | 16 | 8 | 1 | 1 | 757 | 193 | 20 | 737 | 17 |

Every non-retained lift class is a genuine generated-prefix collision label, but the support multiplicity is much larger than the row-indexed image-cell count.  A separate support/fiber multiplicity theorem is required for finite Q2 use.

## Q2 failed-route evidence

Status: `EVIDENCE_RECORDED_NO_Q2_CLOSURE`.

The attempted Route A/B/C/D packets are recorded as evidence and
interfaces for future certificates.  They do not close Q2.

The common remaining target is:

```text
For every primitive finite prefix target z, prove |G_gen(z)| <= t*p, or at least (|G_gen(z)|+11440)*p^67471 <= 4805007*binom(2097152,981104).
```

Conditional arithmetic:

- retained exact-lift bound: `11440`.
- `t*p`: `143763024447376`.
- `t*p + retained`: `143763024458816`.
- threshold floor: `274836936291722953`.
- slack bits: `10.900668`.

| route | status | key diagnostic |
| --- | --- | --- |
| A / Delsarte-distance | `OPEN_MISSING_ROUTE_A_DUAL_EXCESS_CERTIFICATE` | Gilbert lower-bound gap vs `t*p`: `1368895.464109` bits |
| B / split-pair rank | `PROVED_LOCAL_FULL_ROW_RANK_ONLY_INSUFFICIENT` | local rank `67471`, nullity `1`, naive gap `354469.455279` bits |
| C / primitive excess | `OPEN_REQUIRED_PRIMITIVE_EXCESS_CERTIFICATE` | q=3 tuple threshold log2 `173.794061` |
| D / folding defect | `OPEN_MISSING_ROUTE_D_FOLDING_DEFECT_SUPPORT_CERTIFICATE` | first nonzero signed defect `33737`, gap `215091.380413` bits |

Route D is the most useful next structure, but it still needs:

```text
Large signed folding-defect transfer: every large signed defect satisfying the odd prefix equations must be quotient-descended, sparse/Pade-Hankel, M1/half-turn/window-shadow, rank-drop with printed pivot cost, generated-field support-paid, or bounded in a primitive full-rank defect stratum by <=t*p.
```

## Q1 distance-only insufficiency

Status: `PROVED_DISTANCE_ONLY_INSUFFICIENT`.

The Q1 one-sided distance lower bound e>=w+1 is far too weak by itself to imply primitive-heavy-orbit exclusion or #heavy<=n/2.

- `log2 Johnson ball radius e-1 = 721930.784998`.
- `log2 binom(n,j) = 2090873.279793`.
- `log2 greedy distance-code lower bound = 1368942.494795`.
- `log2(n*T) = 78.931354`.

A generic constant-weight packing with the Q1 distance constraint can be astronomically larger than the heavy-target scale.  The missing theorem must use moment-curve algebra and first-match branch structure, not distance alone.

## Split-prefix collision distance

Status: `PROVED_SUPPORT_LEVEL_PREFIX_COLLISION_RIGIDITY`.

If two distinct split supports have the same first `w` locator-prefix
coefficients, then their common-prefix collision has large support distance.

- one-sided difference lower bound: `67472`.
- symmetric-difference lower bound: `134944`.

This is useful Q1 collision rigidity, but it is not a worst-case fiber
bound; the remaining primitive max-orbit certificate is still open.

## Honest exact-lift fiber bound

Status: `PROVED_EXACT_LIFT_ONLY_NOT_DEDUCTED`.

Over the honest cyclotomic model, equality of the first `w` prefix
coordinates forces terminal `16`-coset periodicity because `w >= 2^16`.

- terminal coset size: `131072`.
- exact honest prefix-fiber bound: `11440`.

This bound is deliberately not deducted as a finite-field first-match
payment.  The missing input is a valid finite-field lift-class cost
model for prefix-vector fibers.

## First-match table

| order | branch | status | cost | deducted proved? |
| -: | --- | --- | ---: | --- |
| 1 | `contained_or_noncontained_failure` | `INTERFACE_BUCKET_NOT_A_DEDUCTED_SAFE_CELL` | 0 | no |
| 2 | `rank_drop_or_pivot_failure` | `OPEN_EXACT_MINOR_OR_PIVOT_BUCKET_REQUIRED` |  | no |
| 3 | `tangent_common_line_residue` | `OPEN_FOR_THIS_ROW` |  | no |
| 4 | `quotient_periodic_or_divisor_stabilized` | `PARTIAL_PROVED_DESCENT_WITH_TERMINAL_RAW_PAID` | 471447040 | yes |
| 5 | `planted_prefix_structured` | `OPEN_EXACT_IMAGE_COST_REQUIRED` |  | no |
| 6 | `extension_valued_slope` | `OPEN_PROPER_EXTENSION_BRANCH` |  | no |
| 7 | `base_generated_field_collision` | `PROVED_IMAGE_CELL_COVER` | 143763024447376 | yes |
| 8 | `sparse_sigma_or_sparse_support` | `OPEN_ROW_SPECIFIC_BOUND_REQUIRED` |  | no |
| 9 | `m1_half_turn_or_coefficient_shadow` | `PARTIAL_NORMAL_FORM_WITH_NAMED_RESIDUAL` | 2097153 | no |
| 10 | `primitive_qfin_residual` | `TARGET_NOT_DEDUCTED` |  | no |

## Partial paid-cell ledger

This is not a complete `U(1116048)` upper ledger.

- `B_paid_proved = 143763495894416`.
- `B_rem_proved = 274836964615500671`.
- `K_rem_proved = 4805007`.

Open branches:

- `contained_or_noncontained_failure`: `INTERFACE_BUCKET_NOT_A_DEDUCTED_SAFE_CELL`.
- `rank_drop_or_pivot_failure`: `OPEN_EXACT_MINOR_OR_PIVOT_BUCKET_REQUIRED`.
- `tangent_common_line_residue`: `OPEN_FOR_THIS_ROW`.
- `planted_prefix_structured`: `OPEN_EXACT_IMAGE_COST_REQUIRED`.
- `extension_valued_slope`: `OPEN_PROPER_EXTENSION_BRANCH`.
- `sparse_sigma_or_sparse_support`: `OPEN_ROW_SPECIFIC_BOUND_REQUIRED`.
- `m1_half_turn_or_coefficient_shadow`: `PARTIAL_NORMAL_FORM_WITH_NAMED_RESIDUAL`.
- `primitive_qfin_residual`: `TARGET_NOT_DEDUCTED`.

## Conditional closure theorem

Status: `CONDITIONAL_ON_ALL_NAMED_OPEN_BRANCH_PAYMENTS`.

This packet records only the implication shape for a future complete
safe-side certificate.  It does not prove `U(1116048) <= B*`.

Required future inputs:

- Every named open first-match branch is paid by an explicit theorem/certificate with printed cost.
- The remaining primitive Q-fin residual satisfies max_z |R(z)| <= 4805007 * binom(2097152,981104) / p^67471.
- The complete first-match paid-cell sum is <= B* under the repo endpoint and denominator conventions.

Remaining budget: `274836964615500671`.
Required multiplier: `4805007`.
Conclusion if all inputs exist: the row would close under a future complete U(1116048) upper-ledger certificate.

This packet does not prove U(1116048)<=B*.  It does not pay all named open branches and does not prove the primitive max-orbit certificate.

## Finite-field guardrail

The `{1,3}` support `[0, 1, 3, 14]` over `F_17` is a finite survivor with slope `16`, but its honest cyclotomic defect is nonzero and reduces to zero modulo `17`.

## Next target

`KB-MCA 1116048 primitive Q-fin max-orbit flatness after first-match removal`.

Target multiplier under the proved ledger: `K_rem = 4805007`.

The theorem to prove is:

```text
max primitive Q-fin fiber <= K_rem * binom(n,j) / p^w
```

## Q1 and Q2 plan

### Q1: exact split-prefix collision ledger

Status: `PROVED_IN_THIS_PACKET_AS_EXACT_PAIR_DECOMPOSITION`.

Reduce the exact second moment sum_z N_w(z)^2 to ordered split-pair collision counts stratified by one-sided distance e=|S\T|, with no nontrivial terms below e=w+1.

Deliverables:

- exact second-moment decomposition by e.
- constant-shift split-pair normal form for minimal e=w+1 collisions.
- small cyclic-domain replay of the distance gap and stratum identity.

Proof ideas:

- Use Lambda_S=G A and Lambda_T=G B; prefix equality is a high-order vanishing condition on G(A-B).
- Minimal collisions have A-B constant, matching quotient constant-shift split pairs.

### Q2: heavy-fiber symmetry descent and primitive max-orbit reduction

Status: `PROVED_STABILIZER_AND_EXACT_LIFT_FOLDING_WITH_OPEN_SUPPORT_MULTIPLICITY`.

Use orbitwise moment/excess certificates, or a support-level generated-prefix multiplicity theorem, to rule out primitive heavy target orbits.  Then apply the proved twist-stabilizer theorem and exact-lift folding rigidity to route every threatening stabilized target toward quotient descent or emptiness.

Deliverables:

- twist orbit-stabilizer theorem for prefix targets.
- stabilizer-to-quotient target normal form.
- exact-lift folding theorem for stabilized target fibers.
- finite wrapper conditional on generated-prefix support multiplicity.
- small replay showing generated-prefix image cells are not support payments.
- toy replay showing few max-heavy fibers force nontrivial stabilizer.

Proof ideas:

- The mu_n twist action sends z_i to eta^i z_i and preserves fiber sizes; few heavy fibers force stabilizer.
- An h-stabilized exact lifted target has lambda_1=...=lambda_{h/2}=0, so Newton identities force P_1,P_2,P_4,...,P_{h/2}=0.
- Iterated 2-power antipodal balancing then forces the support to be a union of h-cosets.
- Finite KoalaBear use first classifies nonzero lifted low-prefix coefficients reducing to zero as generated-prefix collisions; support payment still needs a multiplicity theorem.

Remaining ledger work:

- prove or certify extension-valued slope image cells.
- prove lower-rung quotient/planted max-fiber certificates for c=2..32768.
- prove arbitrary planted-tail bounds for c>=262144.
- prove primitive-heavy-orbit exclusion from Q1/higher collision ledgers so Q2 stabilizer forcing activates.
- prove sparse-sigma image costs or keep sparse branch in primitive residual.
- pay pair-deficient residual windows and classify arbitrary sparse Hankel row-slices beyond printed {1,r} coefficient windows.
- prove generated-prefix support multiplicity for non-retained exact lift classes, or an equivalent primitive orbitwise flatness certificate.
- prove primitive max-orbit flatness with K<=4805007, or replace it by a replayable certified recursion.
