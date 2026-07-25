# Rate-half ordinary-list truth at the declared post-Johnson agreement

## Request worked from

Determine how large the ordinary Reed--Solomon list can actually be at agreement `a = 2^40 + 2^34 - 1` on the declared rate-half multiplicative-coset family, replacing loose quotient-rotation pigeonholes where possible and supplying a deterministic upper cap.

## Executive result

The exact maximum list size is not obtained.  Two unconditional statements now bracket it, and a third statement settles the competition among all legal single-slice quotient-rotation specializations.

Let

```text
q_0 = 6597069766657 = 3*2^41+1,
n   = 2^41 = 2199023255552,
k   = 2^40 = 1099511627776,
a   = 2^40+2^34-1 = 1116691496959.
```

For `C = RS[F_{q_0},D,k]`, where `D` is any multiplicative coset of size `n`, define

```text
L_max(a) = max_u #{f in F_{q_0}[X] : deg(f)<k and f agrees with u on at least a points of D}.
```

Then

```text
L_rot <= L_max(a) <= U_pack,
```

where

```text
L_rot
=
ceil(
  C(2^40-1, 2^39+2^33-1)
  /
  (2^40*q_0^(2^33-2))
)
```

and

```text
U_pack
=
floor(
  C(2^41,2^40)
  /
  C(2^40+2^34-1,2^40)
).
```

These closed forms have certified integer-only size bounds

```text
721554505735 <= bits(L_rot) <= 738734374956,
U_pack < 2^2095944040454,
bits(U_pack) <= 2095944040454.
```

Here `bits(z)` is the unique positive integer `b` such that
`2^(b-1) <= z < 2^b`.

The lower form is the largest proved list size at the declared field in the source family.  It comes from the previously unused legal specialization `c=2`.  There are exactly `33` legal dyadic specializations at this agreement, and the guaranteed `c=2` fiber is larger than the entire candidate-subset universe of every other legal single slice.  Thus no exact `d>1` prefix count at another scale can displace this single-slice champion.

The upper form is a deterministic theorem for every received word and every Reed--Solomon evaluation set of distinct points.  It is independent of quotient-rotation and remains valid strictly beyond Johnson.

## Frozen row and radius ledger

The row is

```text
(F_{q_0}, D, k=2^40, n=2^41, rho=1/2),
2^41 | (q_0-1),
D a multiplicative coset of size 2^41.
```

The object is ordinary `LIST`, meaning distinct degree-`<k` Reed--Solomon codewords in one Hamming ball.  No CA or MCA numerator, support count, collision-pair count, ray count, or slope count is quoted as a list bound.

The exact closed-ball radius is

```text
delta = (n-a)/n
      = 1082331758593/2199023255552.
```

The fraction is reduced.  The exact finite-field Johnson agreement and radius are

```text
a_J     = sqrt(n(k-1)) = sqrt(2^41*(2^40-1)),
delta_J = 1-sqrt((k-1)/n).
```

The frozen agreement is strictly below the Johnson agreement:

```text
a^2 < n(k-1),
n(k-1)-a^2 = 1170851739846527019909119.
```

Equivalently, the decoding radius is strictly beyond Johnson by the exact positive quantity

```text
delta-delta_J
=
1170851739846527019909119
/
(2199023255552*(sqrt(2^41*(2^40-1))+1116691496959)).
```

Every statement below concerns `C=RS(k)`.  There is no shift to
`C^+=RS(k+1)`, no agreement or radius shift, no CA/MCA-to-list conversion, and therefore no intrinsic-radius condition.

## Statement A: declared-field lower construction

### Claim card

```text
row:        (F_{q_0},D,k=2^40,n=2^41,rho=1/2), D a size-2^41 multiplicative coset
object:     ordinary LIST
agreement:  a=1116691496959
radius:     delta=1082331758593/2199023255552
Johnson:    a_J=sqrt(2^41*(2^40-1)); squared agreement gap=1170851739846527019909119
bound:      L_max(a) >= L_rot, with L_rot in the closed form below
size form:  721554505735 <= bits(L_rot) <= 738734374956
code rung:  C=RS(k); no C^+ shift
conversion: direct list construction; no CA/MCA conversion or radius shift
```

### Theorem A

For the declared prime field `F_{q_0}` and every multiplicative coset `D` of size `2^41`, some received word has at least

```text
L_rot
=
ceil(
  C(2^40-1,2^39+2^33-1)
  /
  (2^40*q_0^(2^33-2))
)
```

distinct degree-`<2^40` codewords agreeing in exactly
`2^40+2^34-1` positions.

By binomial symmetry the same integer is

```text
ceil(
  C(2^40-1,63*2^33)
  /
  (2^40*q_0^(2^33-2))
).
```

Its certified bit-length interval is

```text
721554505735 <= bits(L_rot) <= 738734374956.
```

In particular,

```text
L_rot > 2^721554505734.
```

### Hypotheses used

The source theorem requires a finite field, a multiplicative coset `D` of even size `n`, `C=RS[F,D,n/2]`, a divisor `c|n/2`, `N=n/c`, integers `1<=d<=N/2-1`, `m=N/2+d`, and `0<s<c`.  The specialization used here is

```text
c = 2,
N = 2^40,
d = 2^33-1 = 8589934591,
m = 2^39+2^33-1 = 558345748479,
s = 1.
```

It satisfies

```text
n/2+d*c+s
= 2^40+2*(2^33-1)+1
= 2^40+2^34-1
= a.
```

### Explicit falsifier

The theorem is falsified by any one of the following:

- failure of one displayed specialization hypothesis;
- a failure of the integrated cyclic quotient-rotation theorem at these parameters;
- two distinct selected subsets producing the same constructed codeword despite distinct root sets;
- a counterexample to either certified power-of-two inequality used in the bit-length proof.

The first and fourth classes are checked by the Lean instances listed below.  The locator construction and distinctness mechanism are the source theorem.

## Mechanism for Statement A

The integrated cyclic quotient-rotation theorem assigns every `m`-subset `A` of an `(N-1)`-point quotient slice a locator whose degree-`>=k` coefficient prefix is controlled by

```text
a_0(A),...,a_{d-1}(A)
```

and by one fixed monic coefficient.  The subset product `a_0(A)` takes at most `N` values, while each remaining prefix coefficient takes at most `q` values.  Hence the `C(N-1,m)` subsets occupy at most `N*q^(d-1)` prefixes.  One prefix fiber has size at least the displayed ceiling.  Fixing that prefix turns the lower locator tails into distinct degree-`<k` codewords near one received word.

The new point is parameter selection, not a new locator identity.  The frozen excess

```text
e = a-n/2 = 2^34-1
```

allows the smallest nontrivial divisor `c=2`, giving an enormous quotient size `N=2^40`.  The field-prefix penalty is large, but the subset entropy is larger.

## Certified size of the lower closed form

Put

```text
t = 2^33,
M = 2^40-1 = 128*t-1,
r = 63*t,
h = 64*t-1.
```

By symmetry the numerator is `C(M,r)`.  The central coefficient `C(M,h)` is maximal.  Since all `M+1=2^40` binomial coefficients sum to `2^M`,

```text
C(M,h) >= 2^M/(M+1) = 2^(M-40).
```

Moving from `h` down to `r` takes `t-1` steps.  At every step `r+1<=u<=h`,

```text
C(M,u-1)/C(M,u)
= u/(M-u+1)
>= 1/2,
```

because `3u>=M+1`.  Therefore

```text
C(M,r) >= 2^(M-40-(t-1)) = 2^(127*t-40).
```

The exact field bracket

```text
2^42 < q_0 < 2^43
```

gives

```text
2^40*q_0^(t-2) < 2^(43*t-46),
```

and hence

```text
L_rot > 2^((127*t-40)-(43*t-46))
      = 2^(84*t+6)
      = 2^721554505734.
```

Conversely,

```text
C(M,r) < 2^M,
2^40*q_0^(t-2) > 2^(42*t-44),
```

so the real quotient is below `2^(86*t+43)`.  Taking the ceiling yields

```text
bits(L_rot) <= 86*t+44 = 738734374956.
```

No floating-point estimate is used.

## Statement B: deterministic interpolation-packing upper cap

### Claim card

```text
row:        every RS[F,D,k] with distinct |D|=n; frozen row n=2^41,k=2^40
object:     ordinary LIST
agreement:  any a>=k; frozen a=1116691496959
radius:     frozen delta=1082331758593/2199023255552
Johnson:    frozen row is post-Johnson by squared gap 1170851739846527019909119
bound:      L_u(a) <= floor(C(n,k)/C(a,k)) for every received word u
size form:  frozen cap U_pack < 2^2095944040454
code rung:  C=RS(k); no C^+ shift
conversion: direct list upper bound; no CA/MCA conversion or radius shift
```

### Theorem B

Let `F` be any finite field, let `D` be any set of `n` distinct evaluation points, let `C=RS[F,D,k]`, and let `a>=k`.  For every received word `u`,

```text
L_u(a) <= floor(C(n,k)/C(a,k)).
```

At the frozen row,

```text
L_max(a)
<=
U_pack
=
floor(
  C(2^41,2^40)
  /
  C(2^40+2^34-1,2^40)
),
```

and

```text
U_pack < 2^2095944040454,
bits(U_pack) <= 2095944040454.
```

### Proof

For every listed polynomial `f`, define its full agreement set

```text
A_f = {x in D : f(x)=u(x)}.
```

Then `|A_f|>=a`.  If `f` and `g` are distinct degree-`<k` polynomials, `f-g` is nonzero of degree `<k` and therefore has at most `k-1` roots.  Hence

```text
|A_f intersect A_g| <= k-1.
```

Count pairs `(f,T)` in which `f` is listed and `T` is a `k`-subset of `A_f`.  Every listed polynomial contributes at least `C(a,k)` pairs.  A fixed `k`-subset `T` of `D` belongs to at most one listed polynomial: two polynomials that both equal `u` on all points of `T` agree at `k` distinct points and are identical.  Since there are `C(n,k)` possible `T`,

```text
L_u(a)*C(a,k) <= C(n,k).
```

Integer flooring proves the theorem.

### Certified size of the cap

Let

```text
T = 2^34,
r = T-1.
```

Then

```text
n = 128*T,
k = 64*T,
a = 65*T-1 = 65*r+64,
C(a,k)=C(a,r).
```

Inside an `a`-point set, choose `r` disjoint blocks of `65` points.  Selecting one point from each block injects `65^r` choices into the `r`-subsets.  Therefore

```text
C(a,r) >= 65^r > 64^r = 2^(6*r).
```

Also `C(n,k)<=2^n`, because it is one term in the binomial sum.  Thus

```text
U_pack
< 2^(n-6*r)
= 2^(122*T+6)
= 2^2095944040454.
```

This certificate is entirely integral.

### Explicit falsifier

The generic theorem is falsified by a finite field, a distinct evaluation set, a received word, and more than `floor(C(n,k)/C(a,k))` distinct degree-`<k` polynomials with agreement at least `a`.  Equivalently, such a witness must force either one `k`-subset to determine two distinct degree-`<k` polynomials or invalidate the pair count above.

The frozen size certificate is falsified by a failure of the exact decomposition `a=65*(2^34-1)+64`, the `65`-block injection, the binomial-sum bound, or the printed exponent identity.

## Statement C: exact legal-scale census and single-slice extremality

### Claim card

```text
row:        declared q_0 rate-half multiplicative-coset row
object:     ordinary LIST lower constructions from the integrated quotient-rotation theorem
agreement:  a=1116691496959; delta=1082331758593/2199023255552
Johnson:    same post-Johnson squared gap 1170851739846527019909119
bound:      exactly 33 legal dyadic scales; c=2 lower beats every other single-slice candidate universe
size form:  other slices have fewer than 2^(2^39-1) candidates; c=2 gives more than 2^721554505734 codewords
code rung:  C=RS(k); no C^+ shift
conversion: direct list construction; no CA/MCA conversion or radius shift
```

### Theorem C

Every divisor of `n/2=2^40` is `c=2^j`.  The exact-agreement equation

```text
d*c+s = a-n/2 = 2^34-1
```

with `1<=d` and `0<s<c` holds precisely when

```text
1 <= j <= 33,
d = 2^(34-j)-1,
s = 2^j-1,
N = 2^(41-j),
m = 2^(40-j)+2^(34-j)-1.
```

Thus exactly `33` legal specializations exist.  The two previously printed cases are `j=33` and `j=32`; the champion is `j=1`.

For every other legal scale, `c>=4`, hence `N<=2^39`.  One fixed auxiliary slice of that specialization contains only `C(N-1,m)` candidate subsets, and

```text
C(N-1,m) < 2^(N-1) <= 2^(2^39-1).
```

The `c=2` guaranteed fiber is larger than `2^721554505734`.  The exponent margin over the largest other-slice universe is

```text
721554505734-(2^39-1) = 171798691847.
```

Therefore the `c=2` printed lower is strongest among all `33` legal single-slice specializations, even if an exact prefix-fiber count is later proved at another scale.

This theorem does not rule out a construction that glues several auxiliary slices into one received word, and it does not assert global extremality among all Reed--Solomon lists.

### Explicit falsifier

The census is falsified by a legal dyadic exponent outside `1,...,33` or an illegal exponent inside that interval.  Single-slice extremality is falsified by another legal single slice containing at least `L_rot` candidate subsets, or by failure of the certified `c=2` lower exponent.

## Uniform exact character evidence

The predecessor's `d=1`, `c=2^33`, `N=256` slice is exactly countable by character orthogonality.  Its maximum product fiber is attained on the odd residue classes and gives, uniformly over every field and coset in the declared family,

```text
L_max(a)
>=
(C(255,129)+C(127,64))/256
=
11092230961998080258863221315535829014445503027953220397756221760927612835.
```

Full claim data are the same row, object, radius, Johnson gap, code rung, and no-conversion ledger printed above; only the lower bound and field quantifier differ.  This evidence is kernel-checked in the explicitly supplied predecessor package by

```text
LRatehalfBracketS1.integrated_floor_formula_exact
LRatehalfBracketS1.odd_product_fiber_arithmetic
LRatehalfBracketS1.product_spectrum_mass_exact
LRatehalfBracketS1.odd_product_is_spectrum_max
```

It supports the source mechanism and shows that the original pigeonhole was genuinely loose.  It does not count the `c=2` high-dimensional prefix fiber.

## Evidence for the new statements

The finite-field construction is the integrated theorem in
`experimental/experiments.tex`, Section
`sec:rate-half-cyclic-quotient-rotation-floor`, with labels

```text
thm:rate-half-cyclic-quotient-rotation-floor
eq:rate-half-list-floor
eq:rate-half-exact-agreement
```

The stdlib-only replay package is

```text
experimental/lean/l_list_truth_s1/
```

and the kernel-checked arithmetic/census instances are

```text
LListTruthS1.declared_row_exact
LListTruthS1.radius_and_johnson_exact
LListTruthS1.legal_scale_census_exact
LListTruthS1.c_two_specialization_exact
LListTruthS1.field_power_bracket_exact
LListTruthS1.rotation_bit_interval_exact
LListTruthS1.quotient_scale_dominance_exact
LListTruthS1.packing_bit_cap_exact
```

All eight theorems use `native_decide`; no ordinary `decide` is used.  Every theorem is followed by `#print axioms`.  The census reports the generated native-decision certificate axiom for every theorem.  It additionally reports `propext` for

```text
LListTruthS1.legal_scale_census_exact
LListTruthS1.c_two_specialization_exact
```

and no additional axiom for the other six beyond their generated native-decision certificate axiom.

The explicit and package-default replay targets are

```text
cd experimental/lean/l_list_truth_s1
lake build LListTruthS1.Arithmetic LListTruthS1
lake build
```

The package has no dependency beyond Lean's standard library, contains a `.gitignore` excluding `.lake/`, and commits no `.lake/` artifact.

## Evidence against exact settlement

The source construction proves an injection from one prefix fiber into one list; it does not prove that every nearby codeword arises from that fiber or even from quotient-rotation.  For `d>1`, including the champion `d=2^33-1`, the exact joint distribution of the high-degree prefix remains unknown.  The deterministic cap treats agreement sets only as a packing of subsets and discards most Reed--Solomon algebra.  Consequently the lower and upper forms are both rigorous but are not close enough to determine `L_max(a)`.

The single-slice extremality theorem also leaves open cross-slice gluing: distinct choices of the distinguished quotient point or partial fiber might conceivably contribute to one received word under an additional identity not present in the integrated theorem.

## Routes killed

1. **Only the two printed specializations are legal.**  Killed by the exact census of `33` scales, kernel-checked by `LListTruthS1.legal_scale_census_exact`.

2. **The `c=2^32,d=3,N=512` pigeonhole is the strongest declared-field lower.**  Killed by the `c=2` lower `L_rot>2^721554505734`.

3. **An exact `d>1` count at another quotient scale could recover the single-slice champion.**  Killed by the candidate-universe ceiling `2^(2^39-1)` and the exact exponent margin `171798691847`.

4. **Nothing deterministic caps the list from above.**  Killed by

```text
L_u(a) <= floor(C(n,k)/C(a,k))
```

and, at the frozen row, `U_pack<2^2095944040454`.

5. **The classical Johnson second-moment denominator can pay this row.**  Killed by

```text
a^2<n(k-1)
```

with exact squared gap `1170851739846527019909119`.  The interpolation-packing proof does not use that denominator.

6. **The quotient-rotation census is the exact full list.**  Not proved and therefore unavailable: the precise obstruction is the absent exhaustivity map from arbitrary nearby degree-`<k` polynomials to the selected locator slice.  A falsifier of that obstruction would be a proved exhaustive parametrization.

## Open questions and natural next step

The exact maximum remains open.  Three questions are now sharply separated:

- What is the exact or sharply bounded prefix-fiber size in the champion `c=2`, `d=2^33-1` slice?
- Can several auxiliary quotient-rotation slices be made to share one received word?
- How much stronger is the list cap once one uses algebraic consistency beyond the fact that `k` evaluations determine a degree-`<k` polynomial?

The natural next step is an inverse theorem for near-extremal interpolation packings on this row: prove that a family approaching
`C(n,k)/C(a,k)` must satisfy an additional common-prefix or quotient structure, then either route that structure into a sharper upper bound or construct a larger explicit list.  This directly attacks the gap left by both ends of the present bracket.

## References

Mathematical source and exact labels:

```text
experimental/experiments.tex
  sec:rate-half-cyclic-quotient-rotation-floor
  thm:rate-half-cyclic-quotient-rotation-floor
  eq:rate-half-list-floor
  eq:rate-half-exact-agreement
```

Supplied predecessor derivations:

```text
experimental/notes/thresholds/ratehalf_list_bracket.md
experimental/papers/ratehalf_list_lower_improved.md
experimental/lean/l_ratehalf_bracket_s1/
```

This packet:

```text
experimental/notes/thresholds/ratehalf_list_truth.md
experimental/lean/l_list_truth_s1/
```

Lake replay:

```text
cd experimental/lean/l_list_truth_s1
lake build LListTruthS1.Arithmetic LListTruthS1
lake build
```

## Derivation-direction ledger

| Printed quantity | Direction | Certification or derivation |
|---|---|---|
| `q_0=6597069766657=3*2^41+1` | frozen | request and integrated source; row identity checked by `declared_row_exact` |
| `n=2^41=2199023255552` | frozen | request; checked by `declared_row_exact` |
| `k=2^40=1099511627776` | frozen | request; checked by `declared_row_exact` |
| `rho=1/2` | derived | `2k=n`; checked by `declared_row_exact` |
| `a=2^40+2^34-1=1116691496959` | frozen | request; checked by `declared_row_exact` |
| radius numerator `1082331758593` and denominator `2199023255552` | derived | `n-a` and `n`; reduction checked by `declared_row_exact` |
| Johnson agreement and radius radicals | derived | exact finite-field Johnson formula |
| squared Johnson gap `1170851739846527019909119` | derived | exact subtraction; checked by `radius_and_johnson_exact` |
| radical post-Johnson radius gap | derived | rationalization of `sqrt(n(k-1))-a` |
| excess `e=2^34-1` | derived | `a-n/2` |
| legal interval `1<=j<=33` and count `33` | derived and enumerated | dyadic divisor classification; checked by `legal_scale_census_exact` |
| `c=2`, `N=2^40`, `d=8589934591`, `m=558345748479`, `s=1` | derived | legal-scale formula; checked by `c_two_specialization_exact` |
| `L_rot` closed form | derived from proved theorem | integrated quotient-rotation theorem at the preceding specialization |
| `t=2^33`, `M=128t-1`, `r=63t`, `h=64t-1` | derived | algebraic rewriting of the binomial numerator |
| field bracket `2^42<q_0<2^43` | bounded | exact integer comparison; checked by `field_power_bracket_exact` |
| lower exponent `721554505734` | bounded | central coefficient, step ratios, and field upper bracket; checked by `rotation_bit_interval_exact` |
| upper lower-form exponent `738734374955` | bounded | binomial sum and field lower bracket; checked by `rotation_bit_interval_exact` |
| bit interval `721554505735..738734374956` | bounded | preceding strict power bounds; checked by `rotation_bit_interval_exact` |
| other-slice exponent ceiling `2^39-1` | bounded | `N<=2^39` and one binomial term is below its full binomial sum |
| dominance margins `171798691846` and `171798691847` | derived | exact exponent subtraction; checked by `quotient_scale_dominance_exact` |
| uniform character count decimal | enumerated/derived | exact character-orthogonality spectrum; checked by the cited predecessor Lean names |
| `U_pack` closed form | derived from proved theorem | `k`-subset interpolation double count |
| `T=2^34`, `r=T-1`, `a=65r+64` | derived | frozen-row rewriting; checked by `packing_bit_cap_exact` |
| packing exponent `2095944040454` | bounded | `65`-block injection and binomial sum; checked by `packing_bit_cap_exact` |
| exact `L_max(a)` | not obtained / open | arbitrary off-slice nearby codewords are not classified |
| exact champion prefix-fiber count | not obtained / open | no exact `d>1` joint-prefix distribution theorem |
| global quotient-rotation extremality | not obtained / open | no cross-slice gluing or full-list exhaustivity theorem |

## Serendipity epilogue

The most interesting unasked-for feature is that the finest possible quotient scale wins for a nonlocal reason.  Taking `c=2` makes the uncontrolled prefix dimension enormous, so at first sight the factor `q_0^(d-1)` looks fatal.  Nevertheless the quotient subset universe grows so much faster that the guaranteed heavy fiber not only beats the two previously studied scales; it exceeds the entire candidate universe of every other legal single slice.  This turns all exact-prefix programs away from `c=2` into secondary questions for the lower champion and redirects the main difficulty toward the global upper structure of arbitrary Reed--Solomon lists.
