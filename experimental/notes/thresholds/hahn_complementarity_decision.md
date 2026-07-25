```yaml
workboard_item: L
row: Mersenne-31 list at 2^-100, fixed-G ordinary boundary adjacent symmetric pair (d,m) = (5413,72860) and (840822,908269)
object: LIST
target_epsilon: 2^-100
agreement: 72860 and 908269
B_star: 16777215
direct_statement: "At either adjacent ordinary-RS row, every valid exact-size selected-support realization satisfies the exact complementarity identity H = L + E_Hahn + S_shell, where E_Hahn = c1*G_1 + c2*G_2 + c3*G_3 >= 0 and S_shell = (alpha/L) sum_{i != j} (e_ij-67448)(e_ij-70799)(e_ij-70800) >= 0 with alpha = 118055716980403503/1924657059987219425146540, equivalently S_shell = (alpha/L) sum_{i != j} (5412-t_ij)(2061-t_ij)(2060-t_ij) in selected-intersection coordinates. At L = 16777215 this is the conservation law Delta_open = E_Hahn + S_shell with Delta_open = H - 16777215 = 4592053304955603301034903445/1159431963847722545269, so a support choice transfers a fixed total between low-Hahn spectral energy and three-shell distance slack and cannot change it. Two routes close exactly. The predecessor's named hypothesis RS_HAHN123_SELECTION_GAP requests H - E_Hahn < L, which the identity turns into S_shell < 0 and is therefore impossible for any existing oversized list, so that hypothesis is logically equivalent to the adjacent cap L <= 16777214 rather than a weaker independent bridge, and one oversized list is already a complete falsifier of it. Optimizing the frozen dual over support choices is dead as a standalone payment route because min_selection (H - E_Hahn) = L + min_selection S_shell >= L. The predecessor conditional theorem stands unchanged; what changes is that its hypothesis is now known to be target-equivalent."
architecture: DIRECT
partition_digest: "n/a (DIRECT)"
atom_or_cell: DIRECT fixed-G ordinary boundary adjacent-pair Hahn complementarity identity and selected-support route cut
quantifier: "Every 981129-point boundary subset E0, every received word over F_p, every family of distinct degree-less-than-d polynomials at agreement at least m for either adjacent row, and every valid exact-size selected-support realization of such a family."
projection_and_unit: "Ordinary Reed--Solomon codewords in one Hamming ball, and their selected exact-size agreement supports as constant-weight blocks. No CA numerator, MCA numerator, ray, or slope is used."
claimed_bound: "No unconditional adjacent payment. Certified consequences: every target-sized valid selected family has G_3 <= 81858218311343544899896663534139630625/389001796223311531724035804630343856388, strengthened to G_3 <= 7745382636890381786544822902247859893375/36807150535206474929475326013497088586156 by the integral first-moment floor G_1 >= 200351922/1233618913144709; a target-sized low-row list has total incidence at most 1222536914966 and total agreement surplus at most 149030066, a target-sized high-row list at most 15238236246526 and 11955691 with at least 4821524 codewords at exactly 908269 agreements; and every valid selection from an unsafe target-sized list keeps at least 8827886148613943/10^16 of its ordered distinct pairs within distance 99 of the three root intersections 2060, 2061, 5412."
status: PROVED
impact: ROUTE_CUT
falsifier: "For the identity: one exact valid realization on which the two sides of H = L + E_Hahn + S_shell differ, or an allowed integer exchange distance at which the frozen cubic is negative. For the conservation law: a target-sized valid selected family whose E_Hahn + S_shell is not 4592053304955603301034903445/1159431963847722545269. For the equivalence: one adjacent row on which RS_HAHN123_SELECTION_GAP and the cap L <= 16777214 have different truth values while the identity holds. For the surplus census: a target-sized list respecting the degree root bound but exceeding 1222536914966 or 15238236246526. For the integrality floor: a family of exactly 16777215 subsets of size 72860 whose first Hahn moment is below 200351922/1233618913144709, or exact divisibility of 16777215*72860 by 981129."
replay: "cd experimental/lean/l_hahn_complementarity_s1 && lake build LHahnComplementarityS1.Complementarity LHahnComplementarityS1.Decision LHahnComplementarityS1 && lake build"
```

# Adjacent fixed-`G` Hahn complementarity: the selected-support gap is target-equivalent

## Exact Lane L print blocks

Low row.

```text
row:                 (F_p, E0 subset D, k=5413, n=981129, rho=5413/981129), p=2^31-1, |E0|=981129
object:              ordinary LIST, not MCA
radius/agreement:    delta=908269/981129; integer agreement 72860=k+67447
Johnson comparison:  three error coordinates beyond the exact finite-p target-list
                     Johnson grid; complete pairwise Hahn integer cap 20737821 exceeds
                     the target 16777214 by 3960607
bound:               no unconditional payment; conditional cap L <= 16777214 stands
                     unchanged from the predecessor, and its hypothesis is now proved
                     equivalent to that cap
route:               DIRECT_LIST
CA_or_MCA_input:     none; no CA-to-list or MCA-to-list conversion is used, so no radius
                     shift and no intrinsic-radius condition apply
code_shift:          C=RS_Fp(E0,5413); C+=RS_Fp(E0,5414); no shift used
status:              PROVED
```

High row.

```text
row:                 (F_p, E0 subset D, k=840822, n=981129, rho=840822/981129), p=2^31-1
object:              ordinary LIST, not MCA
radius/agreement:    delta=72860/981129; integer agreement 908269=k+67447
Johnson comparison:  one error coordinate beyond the exact finite-p target-list Johnson
                     grid; same complete pairwise Hahn cap and excess as the low row
bound:               no unconditional payment; conditional cap L <= 16777214 stands
                     unchanged, hypothesis now proved equivalent to it
route:               DIRECT_LIST
CA_or_MCA_input:     none; no conversion, no radius shift, no intrinsic-radius condition
code_shift:          C=RS_Fp(E0,840822); C+=RS_Fp(E0,840823); no shift used
status:              PROVED
```

## 1. Frozen rows and the selected-support object

```text
p  = 2147483647 = 2^31-1,
N  = 981129,
w  = 67447,
D  = w+1 = 67448,
s0 = 72860,
B* = 16777215,
ell = B*-1 = 16777214,
adjacent rows (d,m) = (5413,72860) and (840822,908269).
```

The two agreements are complementary, `72860 + 908269 = 981129 = N`, and the high
row's selected-support shift is `N - 2*908269 = -835409`.  In both cases one
obtains an injective family of `72860`-subsets with minimum exchange distance
`67448`, equivalently pairwise selected intersection at most `5412`.

## 2. Exact complementarity and the conservation law

With `E_Hahn = c1 G_1 + c2 G_2 + c3 G_3` and `S_shell` the nonnegative slack of
the frozen cubic dual away from its three integer root shells,

```text
H = L + E_Hahn + S_shell,
S_shell = (alpha/L) sum_{i != j} (e_ij-67448)(e_ij-70799)(e_ij-70800) >= 0,
        = (alpha/L) sum_{i != j} (5412-t_ij)(2061-t_ij)(2060-t_ij),
alpha   = 118055716980403503 / 1924657059987219425146540.
```

The two printed forms are the same polynomial under `e = s0 - t`; that
substitution is mechanized as `distance_intersection_identity`, and the three
root shells correspond exactly, `72860-67448 = 5412`, `72860-70799 = 2061`,
`72860-70800 = 2060`, with the spacing `3351` preserved in both coordinates.
Because `70799` and `70800` are adjacent integers, the cubic is nonnegative at
every allowed distance; over the whole allowed range `67448 <= e <= 72860` this
is enumerated in `shell_sign_and_zeros_on_allowed`, whose certified zero set is
exactly `{67448, 70799, 70800}`.

At the first forbidden cardinality `L = B*`,

```text
Delta_open = E_Hahn + S_shell,
Delta_open = H - B* = 4592053304955603301034903445 / 1159431963847722545269.
```

Support choice therefore transfers a fixed total between spectral energy and
shell slack, and cannot change it.

## 3. The named hypothesis is target-equivalent

`RS_HAHN123_SELECTION_GAP` asks, for every list with `L >= B*`, for one valid
selection with `H - E_Hahn < L`.  The identity rewrites that request as
`S_shell < 0`, which no valid selected family satisfies.  Hence

```text
RS_HAHN123_SELECTION_GAP  <->  every adjacent list has L <= 16777214.
```

It is not one statement short of the cap; it is the cap.  One actual adjacent
list of at least `B*` codewords is already a complete falsifier, and no separate
certification over all of its selections is needed, because the identity holds
for every selection.  This is mechanized as `selection_gap_iff_safe` and
`unsafe_iff_falsifier`, with the dual floor `L <= H - E_Hahn` entering as the
model hypothesis it is.

## 4. Optimizing the frozen dual over support choices is dead

For a fixed actual list,

```text
min_selection (H - E_Hahn) = L + min_selection S_shell >= L.
```

Support optimization can tighten the frozen dual certificate down toward the
actual list size but never below it, so it cannot pay the row on its own.

## 5. Integrality refinement

The continuous fractional optimum has `G_1 = 0`; a target-sized integral family
of `72860`-subsets cannot.  Exact division gives `B* s0 mod N = 244929`, and
minimal integer coordinate-degree variance gives

```text
G_1 >= 200351922 / 1233618913144709,
```

which is exactly `rho (N-rho) / (B* s0 (N-s0))` at that remainder, mechanized as
`first_moment_floor_exact`.  Feeding it through the conservation law sharpens the
target-sized third-moment ceiling from

```text
theta_open  = 81858218311343544899896663534139630625
              / 389001796223311531724035804630343856388
```

to

```text
7745382636890381786544822902247859893375
  / 36807150535206474929475326013497088586156,
```

an improvement strictly between `4.0*10^-10` and `4.1*10^-10`.  This is exact and
far too small to pay the row; its significance is that the continuous boundary
`G_1 = G_2 = G_3 = S_shell = 0` is not realizable by a target-sized integral
family.  The predecessor's larger non-strict proxy `theta_closed` is excluded a
fortiori, since `theta_open < theta_closed` is certified.

## 6. Surplus census and forced concentration

Solving the exact integer incidence quadratic at `L = B*` gives the printed
maxima; each is certified as an exact boundary, in that the maximum satisfies the
quadratic and the next integer does not.

```text
low row:   T <= 1222536914966,  surplus <= 149030066,
high row:  T <= 15238236246526, surplus <= 11955691,
```

so a target-sized high-row counterexample has at least `4821524` codewords whose
full agreement set has exactly `908269` points, and therefore no support-choice
freedom at all.  With

```text
Q_star = Delta_open/(alpha(B*-1)) = 181495440148245273326617612350
                                    / 47158238754849128004301,
```

and the enumerated minimum `32835100` of the shell cubic over allowed
intersections at distance at least `100` from all three roots — attained exactly
at `t = 2161`, certified in `radius100_shell_minimum` — every valid selection
from an unsafe target-sized list keeps at least `8827886148613943/10^16` of its
ordered distinct pairs within distance `99` of `{2060, 2061, 5412}`.

One display note, so the note and the paper cannot be read as disagreeing: the
complementary outside-band figure `1172113851386057/10^16` printed in the paper
is a strict upper bound on the exact quotient `Q_star/32835100`, whose exact
expansion begins `0.117211385138605630...`; both printed figures are therefore
valid in the direction each is used, and `band_fractions_bound` certifies them in
exactly that bound form.

## 7. Relationship to the predecessor packet

The predecessor theorem stands unchanged and is not amended, retracted or
reopened.  Under `RS_HAHN123_SELECTION_GAP` its conditional cap `L <= 16777214`
remains true.  What this packet changes is what that conditional buys: the
hypothesis is now known to be equivalent to its own conclusion, so it is not an
independent bridge that anyone should attempt to discharge separately.  That is a
structural correction to the interface, not a defect in the theorem.

## 8. Formalization, axioms, and replay

The Lean package `experimental/lean/l_hahn_complementarity_s1` is stdlib-only,
with no Mathlib and no external dependency.  It certifies the frozen rows and the
complementary agreements, the root-shell correspondence and preserved spacing,
the distance/intersection substitution identity, the sign and exact zero set of
the shell cubic over the whole allowed range in both coordinates, the exact
rational ledger (`H`, `Delta_open`, both one-mode thresholds and their order, the
first-moment floor as an exact variance quotient, the integral third-moment
ceiling with two-sided bounds on its improvement, `Q_star`, and the negligibility
of the first-moment contribution), both integer incidence maxima as exact
boundaries, the enumerated radius-`100` shell minimum with its unique attaining
intersection, the two band fractions in bound form, the inherited route-stop
excesses, and the two logical theorems of Section 3.

It does not formalize the Johnson scheme, the Hahn functions, Reed--Solomon
codes, the cubic dual factorization, the integer variance minimization, or the
random-transversal sample space.  In particular the dual floor `L <= H - E_Hahn`
is a hypothesis of the Lean model, supplied by the paper's Theorem 3.1, not
re-derived in Lean.

Twenty theorems are stated and each is followed by `#print axioms`.  The census
splits into exactly three disclosed classes:

```text
native-decision certificate only, 8 theorems:
  declared_rows_exact, root_shells_exact, allowed_ranges_exact,
  shell_sign_and_zeros_on_allowed, intersection_sign_and_zeros_on_allowed,
  incidence_maxima_exact, radius100_shell_minimum,
  inherited_route_stops_exact

native-decision certificate with propext, Classical.choice, Quot.sound,
8 theorems (the exact rational statements, whose decidable instances on Rat
are classical):
  dual_constants_positive, delta_open_exact, thresholds_exact,
  first_moment_floor_exact, integral_ceiling_exact,
  first_moment_contribution_small, qstar_exact, band_fractions_bound

propext and Quot.sound only, no native certificate, 4 theorems:
  distance_intersection_identity, selection_gap_iff_safe,
  unsafe_iff_falsifier, no_selection_beats_the_floor
```

No `sorry`, `admit`, custom axiom, or committed `.lake/` tree is used, and no
theorem is closed by the ordinary `decide` tactic.  The `decide` function occurs
only inside the finite band predicate as a Bool-valued evaluation.

Replay:

```text
cd experimental/lean/l_hahn_complementarity_s1
lake build LHahnComplementarityS1.Complementarity LHahnComplementarityS1.Decision LHahnComplementarityS1
lake build
```

## 9. Status of each printed quantity

| Quantity | Direction | Status |
| --- | --- | --- |
| frozen rows, complementary agreements, high-row shift `-835409` | frozen / derived | exact, mechanized |
| root shells `67448,70799,70800` and `5412,2061,2060`, spacing `3351` | derived | exact, mechanized |
| distance/intersection substitution identity | derived | proved in Lean for all integers |
| shell cubic sign and zero set on the allowed range | derived | exact, enumerated in Lean |
| complementarity identity `H = L + E_Hahn + S_shell` | derived | proved in the paper |
| conservation law `Delta_open = E_Hahn + S_shell` | derived | `Delta_open` exact and mechanized |
| target-equivalence of `RS_HAHN123_SELECTION_GAP` | derived | proved in Lean from the dual floor |
| dual-optimization route kill | derived | proved in the paper |
| `theta_open`, `theta_closed`, and their order | derived | exact, mechanized |
| first-moment floor `200351922/1233618913144709` | bounded | variance argument in the paper, quotient mechanized |
| integral third-moment ceiling and its improvement | bounded | exact, mechanized two-sided |
| incidence maxima `1222536914966`, `15238236246526` | derived | exact boundaries, mechanized |
| surpluses `149030066`, `11955691`, count `4821524` | derived | exact, mechanized |
| `Q_star`, minimum `32835100`, band fractions | derived | exact, mechanized in bound form |
| inherited excesses `3960607`, `13905232` | inherited | exact, mechanized |
| unconditional adjacent payment | not obtained / open | open |
| nonvacuous RS reserve lower bound | not obtained / open | open |
| explicit adjacent unsafe list | not obtained / open | open |

## 10. What remains open

No adjacent interior row is paid, unconditionally or otherwise, and the
`835410` interior agreements of the middle interval remain unpaid.  The exact
obstruction is no longer an unnamed selected-support hypothesis: it is the
absence of an RS-specific theorem forcing the coupled deletion/addition system on
full agreement sets to contribute more than the conserved reserve, together with
the absence of an actual target-sized counterexample.  The paper's random
transversal identity reduces a usable certificate to the first three
falling-factorial moments of pairwise full-agreement intersections; no attached
source supplies the inequality that would make it cross `Delta_open`.

The full argument, its falsifiers and its derivation-direction ledger are in
`experimental/papers/hahn_complementarity_decision.md`.
