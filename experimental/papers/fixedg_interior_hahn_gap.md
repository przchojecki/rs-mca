# Fixed-`G` ordinary boundary interiors: an exact low-Hahn conjecture and a literal all-depth scalar stop

## Request worked from

Can the `835410` unpaid integer agreements in the Mersenne-31 fixed-`G` ordinary boundary Johnson-negative interval be paid, refuted by an explicit list, reduced to a precise attackable hypothesis, or blocked for a named argument class?

## Abstract

This paper does not pay an interior agreement unconditionally. It sharpens the
request's adjacent-row conditional to the exact integer-target interface
consumed by the frozen degree-three Hahn dual, and it closes the full
repeated-shortening scalar route. At the adjacent symmetric rows
`(k,m)=(5413,72860)` and `(840822,908269)`, the exact all-degree ordinary Hahn
relaxation has objective

```text
H = 24044092640301071703360149280
    / 1159431963847722545269.
```

Writing `ell=16777214` and `B*=ell+1=16777215`, the single named conjecture
`RS_HAHN123_SELECTION_GAP` asks that every hypothetical adjacent list of size at
least `B*` admit one valid choice of one exact-size agreement support per
codeword whose fixed-dual objective is strictly below that list's own
cardinality. It contradicts the dual and implies `L<=ell`. A uniform stronger
one-mode proxy only needs the sharp open condition

```text
G_3 > 81858218311343544899896663534139630625
      / 389001796223311531724035804630343856388
    = 0.21043146614251562...,
```

strictly weaker than `G_3>=1/4`. A convenient non-strict proxy is the slightly
stronger closed threshold `0.2104315192736428...`, which lands exactly at
`ell`. Against both, the matching fractional Hahn optimum has its first three
moments exactly zero, so ordinary pairwise positivity cannot prove the
conjecture.

Unconditionally, every route that retains only nested common-coordinate
incidence counts and then applies the named Plotkin/singleton terminal cap has
exact global minimum `30682446`, attained after two shortenings. It misses
`ell` by `13905232`. The next useful input must therefore preserve
Reed--Solomon structure discarded by the pairwise distance distribution and
scalar section sizes.

## 1. Rows and exact target

The target error probability is `2^-100`. The boundary family has

```text
p = 2147483647 = 2^31 - 1,
N = 981129,
w = 67447,
D = w+1 = 67448,
B* = 16777215,
ell = B*-1 = 16777214.
```

The Johnson-negative interval is the inclusive agreement interval

```text
72859 <= m <= 908270.
```

It contains `835412` integer agreements. The two endpoints are already paid
unconditionally by `L <= 2310492 <= 16777214`; the `835410` strict interior
agreements were open at the start of this round.
This paper decides the adjacent symmetric pair only conditionally and proves a
route cut there.

The exact row print blocks are:

```text
row:                 (F_p, E0 subset D, k=5413, n=981129, rho=5413/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=908269/981129; integer agreement 72860=k+67447
Johnson radius:      908260/981129
post-Johnson gap:    9/981129
unconditional bound: L <= 20737821
conditional bound:   L <= 16777214 under RS_HAHN123_SELECTION_GAP
C versus C+:         C=RS_Fp(E0,5413), C+=RS_Fp(E0,5414)
C+ shift:            none
CA/MCA conversion:   none
radius shift:        none
intrinsic condition: not applicable
```

```text
row:                 (F_p, E0 subset D, k=840822, n=981129, rho=840822/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=72860/981129; integer agreement 908269=k+67447
Johnson radius:      72859/981129
post-Johnson gap:    1/981129
unconditional bound: L <= 20737821
conditional bound:   L <= 16777214 under RS_HAHN123_SELECTION_GAP
C versus C+:         C=RS_Fp(E0,840822), C+=RS_Fp(E0,840823)
C+ shift:            none
CA/MCA conversion:   none
radius shift:        none
intrinsic condition: not applicable
```

Under the existing fixed-`G` equivalence, the conditional ordinary cap gains
one canonical zero anchor and becomes a fixed-`G` boundary size at most
`16777215`. This is an anchor add-back, not an MCA/CA-to-list conversion.

## 2. Selected supports and the common Johnson object

For each listed degree-less-than-`k` polynomial, select one `m`-point subset of
its agreement set. The selected-support map is injective: if two distinct
polynomials received the same selected set, their difference would have at
least `m >= k` roots despite degree less than `k`.

After complementing the high-agreement row, both adjacent rows reduce to a
constant-weight family in

```text
J(981129,72860)
```

with minimum exchange distance `67448`, or maximum pairwise intersection
`5412`.

For ordered inner distribution `A_e` with `A_0=1`, let

```text
G_j = 1 + sum_{e>0} A_e H_j(e)
```

be the normalized `j`th Hahn moment. The ordinary Johnson scheme gives
`G_j >= 0`.

## 3. Current best conditional statement

### Conjecture: `RS_HAHN123_SELECTION_GAP`

Every selected-support list object arising from either adjacent ordinary
Reed--Solomon row, and having cardinality `L` at least

```text
B*=16777215,
```

admits at least one valid selection of one `m`-point agreement support per
codeword such that

```text
H-(c1 G_1+c2 G_2+c3 G_3) < L,                       (3.1)
```

where

```text
c1 = 979061542845605776592576657442
     / 21065719351149270924992461,

c2 = 2127197006408557278777618631055673
     / 1137547685530096782227047625,

c3 = 389001796223311531724035804630343856388
     / 20668103898396328436283228298625,
```

and

```text
H = 24044092640301071703360149280
    / 1159431963847722545269.
```

Equivalently, that selection has weighted low-Hahn energy strictly larger than
`H-L`. The oversized-list guard and the existential support choice are both
sharp for this fixed compiler: lists already of size at most `ell` need no
condition, and only one paying valid selection is needed. The direct falsifier
is one genuine adjacent list with at least `B*` codewords for which every
size-correct valid selection leaves the objective at least `L`.

The stdlib Lean definition is
`LInteriorPayS1.RSHahn123SelectionGap`; the direct falsifier is
`LInteriorPayS1.RSHahn123SelectionGapFalsifier`. Neither is asserted as a
theorem. The logical implication from the conjecture plus the frozen dual
inequality to the integer cap is kernel-checked as
`selection_gap_compiles_integer_cap`; the incompatibility of the printed
falsifier with the conjecture is `selection_gap_falsifier_refutes`.

### Conditional theorem

The request-frozen degree-three dual is

```text
F(e) = 1 + c1 H_1(e) + c2 H_2(e) + c3 H_3(e).
```

It is nonpositive on every allowed nonzero distance and has objective `H`, so
every selected realization satisfies

```text
L + c1 G_1 + c2 G_2 + c3 G_3 <= H,                 (3.2)
```

or `L <= H-(c1 G_1+c2 G_2+c3 G_3)`. Under (3.1) this gives the contradiction
`L<L`. Therefore no list of size at least `B*` exists, and

```text
L <= B*-1 = ell = 16777214.                         (3.3)
```

Thus `RS_HAHN123_SELECTION_GAP` pays both adjacent ordinary-list rows and, after
one anchor add-back, reaches the fixed-`G` budget `B*`.

For a uniform list-size-independent proxy, the worst hypothetical oversized
cardinality is `B*`. Define

```text
Delta_open = H-B*
           = 4592053304955603301034903445
             / 1159431963847722545269.
```

Any selected family with weighted energy strictly larger than `Delta_open` has
objective below `B*` and hence below every oversized `L`.

### Sharp open and convenient closed one-mode proxies

Because every oversized list has `L>=B*` and `G_1,G_2>=0`, a uniform
sufficient selected-family condition is

```text
G_3 > theta_open := Delta_open/c3
    = 81858218311343544899896663534139630625
      / 389001796223311531724035804630343856388
    = 0.21043146614251562....                        (3.4)
```

Lean checks the exact boundary identity

```text
H-c3*theta_open = B*=16777215
```

as `exact_h3_integer_boundary_objective`, and checks
`theta_open<1/4` as `integer_open_threshold_below_quarter`. The inequality in
(3.4) is strict because equality leaves the first forbidden integer available.

A convenient closed proxy is

```text
G_3 >= theta_closed
    := (H-ell)/c3
     = 40929119489723721648112549908683964625
       / 194500898111655765862017902315171928194
     = 0.2104315192736428....                         (3.5)
```

It lands exactly at

```text
H-c3*theta_closed = ell=16777214.
```

Lean checks this as `exact_h3_threshold_objective`, and checks
`theta_open<theta_closed<1/4` through
`integer_open_threshold_below_closed` and
`h3_threshold_strictly_below_quarter`. The request's quarter assumption gives
floor `16032481`, with integer margin `744733`; both new thresholds are weaker.

## 4. Mechanism

The conditional mechanism has three layers.

1. **Injective support selection.** One exact-size agreement support represents
   each codeword without losing list cardinality.
2. **Fixed dual.** The inherited degree-three polynomial converts selected
   pairwise distance data into (3.2).
3. **RS-specific energy.** The adaptive conjecture asks for exactly enough
   objective mass to put the dual upper bound below the hypothetical list's own
   cardinality, and no condition on lists already of size at most `ell`.

The selection quantifier is essential. A universal statement about all choices
would be stronger than the compiler needs; a statement about one arbitrarily
chosen support per word would depend on an unspecified choice. Existential
payment is the sharp list-level interface for this fixed dual.

In Johnson-scheme spectral language, `G_1,G_2,G_3` are the first three
nontrivial harmonic energies. The fractional optimum imitates a three-design by
killing all three. The structural prediction is that actual fixed-syndrome
Reed--Solomon selected supports cannot be simultaneously that balanced. A
proof should choose a canonical exact-size support, express the low Hahn
energies as squared norms of centered one-, two-, and three-coordinate
incidence tensors, and use fixed-syndrome/Padé identities to force a nonzero
low-degree functional with weighted norm exceeding `H-L`. The uniform target
for the smallest oversized list is `Delta_open`.

## 5. Evidence for and against

### Evidence for

A singleton selected-support family has

```text
G_1=G_2=G_3=1
```

and pays both weighted proxy gaps. This is checked by
`singleton_satisfies_weighted_gap`. The guarded existential interface has a
nonvacuous oversized abstract instance in `oversized_selection_gap_evidence`,
with exact objective check
`open_paying_data_is_strictly_below_forbidden_integer`.

A two-support stress family at exchange distance `72860` has

```text
G_3 = 62407467461571137 / 62439698060243047
    = 0.9994838123... > theta_closed > theta_open.
```

The exact evaluation and comparison are
`endpoint_pair_g3_exact`, `endpoint_pair_clears_h3_threshold`, and
`integer_open_threshold_below_closed`.

### Evidence against a pairwise-only proof

The exact fractional primal attaining the complete Hahn optimum satisfies

```text
G_1=G_2=G_3=0.
```

This is recomputed by `fractional_primal_zero_first_three`. The fractional point
is not an actual Reed--Solomon list, so it is not an unsafe construction. It is,
however, a decisive obstruction to proving (3.1) from ordinary Johnson-scheme
positivity alone.

### Explicit falsifier format

A machine-checkable falsifier must print an actual adjacent ordinary-RS list and
certify that every size-correct valid exact-size support selection has

```text
H-(c1 G_1+c2 G_2+c3 G_3) >= L,
```

where `L` is the printed list cardinality.

A single selection with `G_3<=theta_open` only falsifies the strict one-mode
proxy for that selection; it does not by itself falsify the weighted or
existential statement if another selection pays or `G_1,G_2` compensate.

## 6. Literal all-depth scalar route cut

Consider arguments that repeatedly shorten on a common selected coordinate,
retain only the scalar incidence lower bound on section size, and then use the
named Plotkin/singleton terminal cap supplied by pairwise intersection data.

Let `s=72860`. After `t` deletions,

```text
n_t=N-t,
k_t=s-t,
n_t-k_t=N-s=908269.
```

The ordinary Plotkin denominator is

```text
P_t=D(N-t)-(s-t)(N-s)=840821*t-1290548.              (6.1)
```

At `t=0,1`, it equals `-1290548,-449727`, so Plotkin gives no finite cap. For
`2<=t<=5412=s-D`, define

```text
Q_t=floor(D(N-t)/P_t).
```

For `5413<=t<=72860=s`, the residual weight is less than `D`, so the terminal
section has at most one member. The piecewise best terminal cap is therefore

```text
T_t=Q_t  for 2<=t<=5412,
T_t=1    for 5413<=t<=72860.                          (6.2)
```

Reverse each shortening exactly: from a current cap `x` at level `j+1`, the
largest cap allowed at level `j` is

```text
floor(x*(N-j)/(s-j)).                                 (6.3)
```

The exact small cases are:

| `t` | `P_t` | `Q_t` | pulled-back cap |
|---:|---:|---:|---:|
| 2 | 391094 | 169204 | 30682446 |
| 3 | 1231915 | 53717 | 131171251 |
| 4 | 2072736 | 31926 | 1049844832 |
| 5 | 2913557 | 22712 | 10057615672 |
| 6 | 3754378 | 17626 | 105113028810 |

For every `0<=j<=72859`,

```text
N-j >= 13(s-j),
```

because `N-13s=33949` and the margin grows by `12` at each step. Any positive
terminal cap at depth `t` therefore pulls back to at least `13^t`. For `t>=7`,
this is at least

```text
13^7=62748517.
```

Consequently

```text
min_{2<=t<=72860} pulled_back(T_t)=30682446,          (6.4)
```

attained at `t=2`, and

```text
30682446-16777214=13905232.                           (6.5)
```

The abstract singleton justification is
`residual_below_distance_subsingleton`; the all-depth ratio theorem is
`pullback_ge_pow_thirteen_all_depth`; and the exact piecewise
Plotkin/singleton conclusion is
`two_shortening_is_best_terminal_route_minimum` and
`best_terminal_incidence_route_cannot_pay`.

This is a theorem about the named inference system, not a list lower bound and
not a construction of `30682446` codewords. Its direct falsifier is one valid
shortening depth `2<=t<=72860` whose exact piecewise Plotkin/singleton terminal
cap, after exact reverse incidence pullback, is at most `16777214`, or a failure
of one of the printed terminal or pullback inequalities.

## 7. Routes killed

### 7.1 Ordinary pairwise Hahn/Delsarte, all degrees

The request-frozen complete relaxation has exact objective `H`, floor
`20737821`, and target excess

```text
20737821-16777214=3960607.
```

Its matching fractional primal has zero first-three Hahn moments. Therefore no
argument retaining only the ordinary pairwise intersection distribution can
prove the required low-Hahn gap.

### 7.2 Repeated incidence shortening plus the named Plotkin/singleton terminal cap

Every possible shortening depth `2<=t<=72860` is covered by (6.4). The exact
obstruction is the route minimum `30682446`, with target excess `13905232`.
Deeper shortening is not a hidden escape: after `t=5412`, the terminal cap is
already the exact singleton cap.

### 7.3 The quarter as the sharp fixed-dual threshold

The sharp integer-target one-mode condition is the open threshold
`G_3>theta_open=0.21043146614251562...`, not `1/4`. The convenient closed
threshold is `theta_closed=0.2104315192736428...`. More sharply, the guarded
weighted existential selection condition (3.1) is the actual fixed-dual list
interface, because positive `G_1` or `G_2` can compensate for smaller `G_3` and
lists already below `B*` require no condition.

## 8. Formalization and validation

The stdlib-only package is

```text
experimental/lean/l_interior_pay_s1
```

with namespace `LInteriorPayS1`. The principal modules are:

```text
LInteriorPayS1/CriticalGap.lean
LInteriorPayS1/SelectionGap.lean
LInteriorPayS1/AllDepthStop.lean
LInteriorPayS1/BestTerminalStop.lean
```

The exact replay is

```text
cd experimental/lean/l_interior_pay_s1
lake build LInteriorPayS1
lake build
```

Both the explicit library target and the package default target pass. Every
theorem has a `#print axioms` census. Closed rational and large integer checks,
and the finite oversized-list evidence instance, disclose `native_decide`;
ordinary `decide` is used only for tiny closed positivity side conditions in the
power-monotonicity steps; the quantified pullback proofs are direct stdlib
arguments. The package has no
Mathlib dependency, `sorry`, custom axiom, or committed `.lake/` tree.

## 9. Derivation-direction ledger

| printed count or constant | exact value | direction |
|---|---:|---|
| target error probability | `2^-100` | frozen input |
| field size | `2147483647` | derived as `2^31-1` |
| boundary length | `981129` | frozen input |
| slack | `67447` | frozen input |
| exchange distance | `67448` | derived as `w+1` |
| budget | `16777215` | frozen input |
| ordinary target | `16777214` | derived as `B*-1` |
| interval endpoints | `72859,908270` | frozen input |
| interval size | `835412` | derived inclusively |
| initial unpaid interior size | `835410` | derived by deleting two endpoints |
| adjacent rows | `(5413,72860)`, `(840822,908269)` | derived by one inward step |
| constant weight | `72860` | derived by complement symmetry |
| maximum intersection | `5412` | derived as `s-D` |
| low-row errors | `908269` | derived as `N-72860` |
| high-row errors | `72860` | derived as `N-908269` |
| low Johnson errors | `908260` | inherited exact finite-field threshold |
| high Johnson errors | `72859` | inherited exact finite-field threshold |
| post-Johnson gaps | `9,1` | derived by subtraction |
| endpoint unconditional cap | `2310492` | inherited proved endpoint theorem |
| complete adjacent objective `H` | exact rational in §3 | inherited from request-frozen matching certificates |
| adjacent unconditional floor | `20737821` | derived as `floor(H)` |
| adjacent integer target excess | `3960607` | derived by integer subtraction |
| coefficients `c1,c2,c3` | exact rationals in §3 | inherited from request-frozen dual |
| adaptive per-list energy boundary | `H-L` | derived from the fixed dual objective and hypothetical list cardinality |
| sharp open energy boundary `Delta_open` | exact rational in §3 | derived as `H-B*` |
| decimal `Delta_open` | `3960606.096899...` | bounded display of exact rational |
| stronger closed energy boundary | `H-ell` | derived from the exact objective and target |
| decimal stronger closed boundary | `3960607.096899...` | bounded display of exact rational |
| inherited quarter proxy | `1/4` | frozen hypothesis from the request |
| sharp open threshold `theta_open` | exact rational in §3 | derived as `Delta_open/c3` |
| decimal `theta_open` | `0.21043146614251562...` | bounded display of exact rational |
| stronger closed threshold `theta_closed` | exact rational in §3 | derived as `(H-ell)/c3` |
| decimal `theta_closed` | `0.2104315192736428...` | bounded display of exact rational |
| quarter conditional floor | `16032481` | derived by exact rational division |
| quarter margin | `744733` | derived as `ell-16032481` |
| singleton moments | `1,1,1` | enumerated from singleton inner distribution |
| endpoint-pair `G_3` | exact rational in §5 | enumerated by direct Hahn formula |
| endpoint-pair decimal | `0.9994838123...` | bounded display of exact rational |
| fractional first-three moments | `0,0,0` | enumerated from exact primal weights |
| maximum shortening depth | `72860` | derived as initial support weight |
| Plotkin/singleton transition | `5412/5413` | derived from `s-D` |
| denominator constants | `840821,-1290548` | derived by expanding (6.1) |
| signed denominators at depths `0,1` | `-1290548,-449727` | derived from (6.1) |
| rows at depths `2,...,6` | table in §6 | enumerated by exact division/pullback |
| base ratio margin | `33949` | derived as `N-13s` |
| margin increment | `12` | derived from one deletion |
| pullback factor | at least `13` | bounded by the exact ratio inequality |
| first coarse depth | `7` | derived as first depth after exact cases `2,...,6` |
| coarse floor | `62748517` | derived as `13^7` |
| scalar-route minimum | `30682446` | derived from exact small cases plus coarse tail |
| scalar-route excess | `13905232` | derived by subtraction |
| fixed-`G` conditional size | `16777215` | derived by one-anchor add-back |
| unconditional interior payment | not obtained / open | open |
| proof of `RS_HAHN123_SELECTION_GAP` | not obtained / open | open |
| explicit adjacent unsafe list | not obtained / open | open |

## 10. Open questions and natural next step

The exact open gap `Delta_open` is small enough to be a concrete target but
large enough that aggregate pairwise positivity misses it completely. The most direct next
step is one of:

1. derive (3.1) for a canonical support selection from fixed-syndrome/Padé
   compatibility, preserving cross-coordinate information; or
2. add the first low-order Terwilliger semidefinite constraint and test whether
   it excludes the zero-moment fractional optimum by strictly more than `Delta_open`.

A negative result is equally useful if it prints an actual adjacent list or a
source-compatible relaxation point below the weighted threshold and states
exactly which RS invariant it still discards.

## 11. References

- `experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md`,
  Theorem 2.1 and §§3, 4, 6.
- `experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md`,
  Theorem 4.1 and Corollaries 5.1--5.2.
- `experimental/notes/thresholds/fixedg_interior_hahn_gap.md`, §§2--9.
- `experimental/notes/thresholds/l_fixedg_adjacent_hahn_stop_v1.md`,
  Theorems 1--2 and §§3--6: exact all-degree optimum, matching primal and dual
  certificates, and the named hypothesis `RS_H3_QUARTER_GAP` with its
  conditional compiler.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/CriticalGap.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/SelectionGap.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/AllDepthStop.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/BestTerminalStop.lean`.

## Serendipity epilogue

The most interesting unasked-for feature is that the scalar shortening route
gets rapidly worse for a structural reason independent of the Hahn optimum:
throughout the entire support depth, reversing one incidence shortening costs
at least a factor `13`. The familiar two-shortening cap was not merely the best
attempt tried so far; it is the exact optimum of the literal all-depth scalar
system, even after replacing late Plotkin estimates by the exact singleton
terminal cap. That sharp separation suggests that any successful interior
argument must couple sections rather than continue slicing them independently.
