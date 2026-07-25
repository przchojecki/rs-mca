# M31 fixed-`G` interior payment: exact selected-support gap and scalar route stop

```yaml
workboard_item: L
row: Mersenne-31 list at 2^-100, fixed-G ordinary boundary adjacent symmetric pair (d,m) = (5413,72860) and (840822,908269)
object: LIST
target_epsilon: 2^-100
agreement: 72860 and 908269
B_star: 16777215
direct_statement: "At both adjacent ordinary-RS rows, the inherited degree-three Hahn dual gives L <= 16777214 under the single named hypothesis RS_HAHN123_SELECTION_GAP: every hypothetical list larger than 16777214 admits one valid exact-size support selection whose dual objective is strictly below that list's own cardinality. A stronger one-mode sufficient proxy is G_3 > 81858218311343544899896663534139630625 / 389001796223311531724035804630343856388. Unconditionally, every route retaining only nested common-coordinate incidence counts and then the named Plotkin/singleton terminal cap stops above target; its exact minimum is 30682446 after two shortenings."
architecture: DIRECT
partition_digest: n/a (DIRECT)
atom_or_cell: DIRECT fixed-G ordinary boundary adjacent-pair low-Hahn compiler and scalar-route cut
quantifier: "Every 981129-point boundary subset E0, every received word over F_p, and every family of distinct degree-less-than-d polynomials at agreement at least m, for either adjacent row."
projection_and_unit: "Ordinary Reed-Solomon codewords in one Hamming ball; exact-size selected agreement supports are injective. No MCA or CA numerator is used."
claimed_bound: "Conditional L <= 16777214 at both adjacent rows; unconditional scalar-route obstruction 30682446 - 16777214 = 13905232."
status: PROVED
impact: ROUTE_CUT
falsifier: "For RS_HAHN123_SELECTION_GAP: one genuine adjacent list of at least 16777215 codewords for which every valid size-correct selected-support realization leaves the inherited objective at least that list's cardinality. For the route cut: one valid shortening depth whose exact named-route pullback cap is at most 16777214."
replay: "cd experimental/lean/l_interior_pay_s1 && lake build LInteriorPayS1 && lake build"
```

## 1. Verdict

No interior agreement is paid unconditionally. Two exact interfaces are decided.

First, the request's quarter-gap condition is sharpened to the weakest guarded
selected-support statement consumed by the frozen degree-three Hahn dual. Under
that one named hypothesis, both adjacent ordinary-list rows satisfy

```text
L <= 16777214.
```

Second, repeated common-coordinate shortening cannot repair the unconditional
gap if every section is summarized only by its size and the terminal section is
bounded by ordinary constant-weight Plotkin while applicable and the exact
singleton cap afterward. Across every shortening depth, the exact best pulled-
back cap is

```text
30682446,
```

attained after two shortenings and exceeding the target by `13905232`.

## 2. Frozen reduction

```text
p = 2147483647 = 2^31-1,
N = 981129,
w = 67447,
D = w+1 = 67448,
B* = 16777215,
ell = B*-1 = 16777214.
```

For either adjacent row, choose one exact `m`-point subset of each codeword's
agreement set. The support choice is injective because two distinct degree-
less-than-`d` polynomials cannot agree on `m >= d` points. After complementing
the high-agreement row, both sides become a constant-weight family in

```text
J(981129,72860)
```

with minimum exchange distance `67448` and maximum intersection `5412`.

For ordered inner distribution `A_e`, normalized so `A_0=1`, define

```text
G_j = 1 + sum_e A_e H_j(e).
```

Ordinary Johnson-scheme positivity gives `G_j >= 0`.

## 3. Exact low-Hahn compiler

The request-frozen dual is

```text
F(e)=1+c1 H_1(e)+c2 H_2(e)+c3 H_3(e),
```

where

```text
c1 = 979061542845605776592576657442
     / 21065719351149270924992461,

c2 = 2127197006408557278777618631055673
     / 1137547685530096782227047625,

c3 = 389001796223311531724035804630343856388
     / 20668103898396328436283228298625.
```

Its exact objective is

```text
H = 24044092640301071703360149280
    / 1159431963847722545269
  = 20737821.096899...,
```

and `F(e) <= 0` at every allowed nonzero integer distance. Hence every selected
realization obeys

```text
L + c1 G_1 + c2 G_2 + c3 G_3 <= H.                  (3.1)
```

### `RS_HAHN123_SELECTION_GAP`

Every hypothetical adjacent ordinary-RS list of cardinality `L >= B*` admits
at least one valid choice of one exact-size agreement support per codeword such
that

```text
H-(c1 G_1+c2 G_2+c3 G_3) < L.                       (3.2)
```

Combining (3.1) and (3.2) gives `L<L`, so no oversized list exists and
`L<=ell`. The direct falsifier is one genuine adjacent list of size at least
`B*` for which every size-correct valid selection leaves the objective at least
`L`.

The Lean definitions are `RSHahn123SelectionGap` and
`RSHahn123SelectionGapFalsifier`. The compiler is
`selection_gap_compiles_integer_cap`; the falsifier incompatibility theorem is
`selection_gap_falsifier_refutes`.

### One-mode thresholds

The sharp open integer-target energy is

```text
Delta_open = H-B*
           = 4592053304955603301034903445
             / 1159431963847722545269.
```

Since `G_1,G_2>=0`, a stronger one-mode sufficient condition is

```text
G_3 > theta_open
    = 81858218311343544899896663534139630625
      / 389001796223311531724035804630343856388
    = 0.21043146614251562....
```

Lean checks `H-c3*theta_open=B*` and `theta_open<1/4`. A convenient non-strict
closed condition is

```text
G_3 >= theta_closed
    = 40929119489723721648112549908683964625
      / 194500898111655765862017902315171928194
    = 0.2104315192736428....
```

which lands exactly at `ell`. The inherited quarter proxy gives floor
`16032481`, with integer margin `744733` below `ell`.

## 4. Evidence and obstruction

Positive evidence is kernel-checked at three levels.

- `singleton_satisfies_weighted_gap`: a singleton has `G_1=G_2=G_3=1`.
- `endpoint_pair_g3_exact` and `endpoint_pair_clears_h3_threshold`: a direct
  two-support stress instance has
  `G_3=62407467461571137/62439698060243047`.
- `oversized_selection_gap_evidence`: a finite abstract oversized-list model
  checks the guarded existential interface and exact threshold wiring. It is
  explicitly not claimed to arise from Reed--Solomon polynomials.

The exact negative evidence is `fractional_primal_zero_first_three`: the
matching fractional optimum of the complete Hahn LP has

```text
G_1=G_2=G_3=0.
```

Thus ordinary pairwise Johnson positivity alone cannot prove the named gap.
The fractional point is not an actual list or lower construction.

## 5. Literal all-depth scalar route cut

After `t` common-coordinate shortenings, the residual constant-weight
parameters are

```text
N_t=N-t,  s_t=72860-t,  N_t-s_t=908269.
```

The Plotkin denominator is

```text
P_t=D(N-t)-(72860-t)908269
   =840821*t-1290548.
```

It is negative at `t=0,1` and positive from `t=2`. For `2<=t<=5412`, use

```text
Q_t=floor(D(N-t)/P_t).
```

For `5413<=t<=72860`, residual weight is below `D`, so the exact terminal cap
is one. Reverse incidence pullback uses

```text
x -> floor(x*(N-j)/(72860-j)).
```

The exact first cases are

| `t` | terminal Plotkin cap | pulled-back cap |
|---:|---:|---:|
| 2 | 169204 | 30682446 |
| 3 | 53717 | 131171251 |
| 4 | 31926 | 1049844832 |
| 5 | 22712 | 10057615672 |
| 6 | 17626 | 105113028810 |

For every `0<=j<=72859`,

```text
N-j >= 13(72860-j),
```

so any positive terminal cap at depth `t` pulls back to at least `13^t`. For
`t>=7`, this is at least `13^7=62748517`. Hence two shortenings are globally
optimal in the named scalar route, including the exact singleton terminal
range:

```text
min cap = 30682446 > 16777214.
```

The key Lean names are `pullback_ge_pow_thirteen_all_depth`,
`residual_below_distance_subsingleton`,
`two_shortening_is_best_terminal_route_minimum`, and
`best_terminal_incidence_route_cannot_pay`.

## 6. Exact Lane-L print blocks

```text
row:                 (F_p, E0 subset D, k=5413, n=981129, rho=5413/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=908269/981129; integer agreement 72860=k+67447
Johnson radius:      908260/981129
post-Johnson gap:    9/981129
unconditional bound: L <= 20737821
conditional bound:   L <= 16777214 under RS_HAHN123_SELECTION_GAP
C versus C+:         C=RS_Fp(E0,5413); C+=RS_Fp(E0,5414); no shift used
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
C versus C+:         C=RS_Fp(E0,840822); C+=RS_Fp(E0,840823); no shift used
CA/MCA conversion:   none
radius shift:        none
intrinsic condition: not applicable
```

The existing fixed-`G` equivalence adds one canonical zero anchor, giving at
most `16777215` fixed-`G` codewords conditionally. This is an anchor add-back,
not a CA/MCA-to-list conversion.

## 7. Routes killed

1. **Complete ordinary pairwise Hahn/Delsarte.** Exact optimum floor
   `20737821`; exact target excess `3960607`; matching fractional first-three
   moments `0,0,0`.
2. **Repeated incidence shortening with Plotkin/singleton terminal facts.**
   Exact global minimum `30682446`; target excess `13905232`.
3. **The quarter as a sharp fixed-dual threshold.** Exact replacement:
   `theta_open=0.21043146614251562...`; convenient closed replacement
   `theta_closed=0.2104315192736428...`; the guarded weighted selection
   statement is sharper still.

## 8. Formalization, axioms, and replay

Package path:

```text
experimental/lean/l_interior_pay_s1
```

Principal modules:

```text
LInteriorPayS1/CriticalGap.lean
LInteriorPayS1/SelectionGap.lean
LInteriorPayS1/AllDepthStop.lean
LInteriorPayS1/BestTerminalStop.lean
```

Every theorem has a `#print axioms` census. Closed rational and large-integer
statements disclose `native_decide`; quantified incidence and pullback lemmas
are direct stdlib proofs. There is no Mathlib dependency, `sorry`, custom axiom,
or committed `.lake/` directory.

```text
cd experimental/lean/l_interior_pay_s1
lake build LInteriorPayS1
lake build
```

## 9. Derivation-direction ledger

| quantity | exact value | direction |
|---|---:|---|
| interval size | `835412` | derived inclusively from frozen endpoints |
| initially unpaid interior | `835410` | derived by removing two endpoints |
| ordinary target | `16777214` | derived as `B*-1` |
| adjacent objective `H` | exact rational in §3 | inherited from matching certificates |
| adjacent unconditional floor | `20737821` | derived as `floor(H)` |
| adjacent excess | `3960607` | derived by subtraction |
| `Delta_open` | exact rational in §3 | derived as `H-B*` |
| `theta_open` | exact rational in §3 | derived as `Delta_open/c3` |
| `theta_closed` | exact rational in §3 | derived as `(H-ell)/c3` |
| quarter floor | `16032481` | derived by exact rational division |
| quarter margin | `744733` | derived by subtraction |
| shortening caps at `t=2,...,6` | table in §5 | enumerated by exact division and pullback |
| per-step pullback factor | at least `13` | bounded from the exact ratio inequality |
| coarse tail floor | `62748517` | derived as `13^7` |
| scalar-route minimum | `30682446` | derived from exact small cases and tail bound |
| scalar-route excess | `13905232` | derived by subtraction |
| unconditional interior payment | not obtained / open | open |
| proof of `RS_HAHN123_SELECTION_GAP` | not obtained / open | open |
| explicit adjacent unsafe list | not obtained / open | open |

## 10. Nonclaims and next step

The named gap and all stronger moment proxies are conjectural. The route-cut
cap is not a list construction or lower bound. No MCA or CA numerator is quoted
as ordinary-list safety. No agreement other than the adjacent symmetric pair is
decided.

The natural successor is an RS-specific invariant retaining information lost by
ordinary distances and scalar section sizes: either a fixed-syndrome/Padé
identity that forces the selected low-Hahn energy, or a first low-order
Terwilliger semidefinite constraint tested against `Delta_open`. Either route
has a direct falsifier.

## 11. References

- `experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md`,
  Theorem 2.1 and §§3, 4, 6.
- `experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md`,
  Theorem 4.1 and Corollaries 5.1--5.2.
- Request-frozen adjacent Hahn optimum, matching primal/dual certificates, and
  `RS_H3_QUARTER_GAP` conditional compiler.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/CriticalGap.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/SelectionGap.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/AllDepthStop.lean`.
- `experimental/lean/l_interior_pay_s1/LInteriorPayS1/BestTerminalStop.lean`.
