```yaml
workboard_item: L
row: "(F_q,D,k=2^40,n=2^41,rho=1/2), 2^41 | (q-1), D a multiplicative coset of size 2^41; declared q_0=6597069766657"
object: LIST
target_epsilon: "not applicable; exact finite-family list bracket"
agreement: 1116691496959
B_star: "n/a"
direct_statement: "For every received word, the ordinary RS list at agreement at least a is at most floor(C(n,k)/C(a,k)); at q_0 one received word has at least the c=2 quotient-rotation closed form printed below."
architecture: DIRECT
partition_digest: "n/a (DIRECT)"
atom_or_cell: DIRECT
quantifier: "uniform upper bound over every received word; existential lower construction for every declared multiplicative coset over q_0"
projection_and_unit: "distinct ordinary Reed--Solomon codewords in one Hamming ball"
claimed_bound: "ceil(C(2^40-1,2^39+2^33-1)/(2^40*q_0^(2^33-2))) <= L_max <= floor(C(2^41,2^40)/C(2^40+2^34-1,2^40))"
status: PROVED
impact: LOCAL_ONLY
falsifier: "A failed c=2 source specialization; two distinct degree-<k polynomials agreeing on the same k evaluation points; a failure of the 65-block subset injection; or a failed exact arithmetic gate."
replay: "cd experimental/lean/l_list_truth_s1 && lake build LListTruthS1.Arithmetic LListTruthS1 && lake build"
```

# Rate-half ordinary-list truth: a champion lower specialization and a deterministic global cap

## Exact Lane L print block

```text
row:                 (F_q, D, k = 2^40, n = 2^41, rho = 1/2), 2^41 | (q-1),
                     D a multiplicative coset of size 2^41; declared q_0 = 6597069766657
object:              ordinary LIST, not MCA
radius/agreement:    delta = 1082331758593/2199023255552;
                     integer agreement a = 1116691496959
Johnson comparison:  exact finite-field Johnson agreement a_J = sqrt(2^41*(2^40-1));
                     the agreement is strictly beyond Johnson, with exact squared gap
                     n(k-1) - a^2 = 1170851739846527019909119
bound:               ceil( C(2^40-1, 2^39+2^33-1) / (2^40 * q_0^(2^33-2)) )
                       <= L_max(a) <=
                     floor( C(2^41, 2^40) / C(2^40+2^34-1, 2^40) ),
                     with certified sizes
                     721554505735 <= bits(L_rot) <= 738734374956 and
                     bits(U_pack) <= 2095944040454
route:               DIRECT_LIST
CA_or_MCA_input:     none; no CA-to-list or MCA-to-list conversion is used,
                     so no radius shift and no intrinsic-radius condition apply
code_shift:          C = RS[F_q, D, 2^40]; no C^+ = RS(k+1) shift
status:              PROVED
```

## 1. Frozen row and exact Johnson comparison

Let

```text
C = RS[F_q,D,k],
q_0 = 6597069766657 = 3*2^41+1,
n = |D| = 2^41 = 2199023255552,
k = 2^40 = 1099511627776,
a = 2^40+2^34-1 = 1116691496959.
```

The object is ordinary `LIST`: distinct codewords in one Hamming ball around one
received word.  No support, CA, MCA, pair, ray, or slope count is used.

The closed-ball radius is

```text
delta = (n-a)/n
      = 1082331758593/2199023255552.
```

It is reduced.  The exact finite-field Johnson agreement and radius are

```text
a_J = sqrt(n(k-1)) = sqrt(2^41*(2^40-1)),
delta_J = 1-sqrt((k-1)/n).
```

The row is strictly post-Johnson because

```text
a^2 < n(k-1),
n(k-1)-a^2 = 1170851739846527019909119.
```

The exact positive radius gap is

```text
delta-delta_J
= (a_J-a)/n
= 1170851739846527019909119
  /
  (2199023255552*(sqrt(2^41*(2^40-1))+1116691496959)).
```

Every claim below concerns `C=RS(k)`.  There is no `C^+=RS(k+1)` shift, no
radius shift, no CA/MCA input, and no intrinsic-radius condition.

## 2. Current bracket

For a received word `u`, let `L_u(a)` be the number of degree-`<k` codewords
agreeing with `u` on at least `a` positions, and put

```text
L_max(a) = max_u L_u(a).
```

### Theorem 2.1 — declared-field lower construction

For `q=q_0` and every multiplicative coset `D` of size `2^41`, some received
word has at least

```text
L_rot
=
ceil(
  C(2^40-1, 2^39+2^33-1)
  /
  (2^40*q_0^(2^33-2))
)
```

distinct codewords agreeing in exactly `a` positions.  Equivalently, using the
complementary binomial index,

```text
L_rot
=
ceil(
  C(2^40-1, 63*2^33)
  /
  (2^40*q_0^(2^33-2))
).
```

This integer is deliberately given in closed form.  Its rigorously certified
bit-length interval is

```text
721554505735 <= bits(L_rot) <= 738734374956.
```

In particular,

```text
L_rot > 2^721554505734.
```

### Theorem 2.2 — deterministic interpolation packing cap

For every finite field, every set `D` of `n` distinct evaluation points, every
received word, and every Reed--Solomon code `RS[F,D,k]` with agreement threshold
`a>=k`,

```text
L_u(a) <= floor(C(n,k)/C(a,k)).
```

At the frozen row this gives the closed-form cap

```text
U_pack
=
floor(
  C(2^41,2^40)
  /
  C(2^40+2^34-1,2^40)
),

L_max(a) <= U_pack.
```

The cap satisfies the rigorous integer size certificate

```text
U_pack < 2^2095944040454,
bits(U_pack) <= 2095944040454.
```

Combining the two theorems gives

```text
L_rot <= L_max(a) <= U_pack,

721554505735 <= bits(L_max(a)) <= 2095944040454.
```

The exact maximum is not determined.  The upper endpoint is nevertheless a
uniform deterministic list theorem, not the trivial full-code count `q^k` and
not a construction-slice census.

### Uniform lower inherited from the exact character slice

For every field in the declared family, not only `q_0`, the predecessor's exact
`d=1` character count still gives

```text
L_max(a) >=
(C(255,129)+C(127,64))/256
=
11092230961998080258863221315535829014445503027953220397756221760927612835.
```

The new `c=2` lower is a stronger declared-field specialization; it does not
replace the uniform-in-`q` statement.

## 3. Proof of the lower theorem

The integrated source is `experimental/experiments.tex`, Section
`sec:rate-half-cyclic-quotient-rotation-floor`, theorem
`thm:rate-half-cyclic-quotient-rotation-floor`, with count and exact-agreement
formulas `eq:rate-half-list-floor` and `eq:rate-half-exact-agreement`.

The theorem permits

```text
c | n/2,
N=n/c,
1<=d<=N/2-1,
m=N/2+d,
0<s<c,
```

and produces at least

```text
ceil(C(N-1,m)/(N*q^(d-1)))
```

codewords at exact agreement `n/2+d*c+s`.

### 3.1 The smallest legal block

Choose

```text
c = 2,
N = 2^40,
d = 2^33-1 = 8589934591,
m = 2^39+2^33-1 = 558345748479,
s = 1.
```

Then `c|n/2`, `1<=d<=N/2-1`, `0<s<c`, and

```text
n/2+d*c+s
= 2^40+2*(2^33-1)+1
= 2^40+2^34-1
= a.
```

Substitution into the integrated theorem is exactly Theorem 2.1.

### 3.2 Certified bit length of `L_rot`

Put

```text
t = 2^33,
M = N-1 = 128*t-1,
r = M-m = 63*t,
h = 64*t-1.
```

By symmetry, `C(M,m)=C(M,r)`.  The central coefficient `C(M,h)` is maximal.
Since the `M+1=2^40` binomial coefficients sum to `2^M`,

```text
C(M,h) >= 2^M/(M+1) = 2^(M-40).
```

Moving from `h` down to `r` takes `t-1` steps.  At a step with
`r+1<=u<=h`,

```text
C(M,u-1)/C(M,u) = u/(M-u+1) >= 1/2,
```

because `3u>=M+1`.  Therefore

```text
C(M,r) >= 2^(M-40-(t-1)) = 2^(127*t-40).
```

The declared field obeys the exact power bracket

```text
2^42 < q_0 < 2^43.
```

Hence the denominator obeys

```text
2^40*q_0^(t-2) < 2^(43*t-46),
```

and therefore

```text
L_rot > 2^((127*t-40)-(43*t-46))
      = 2^(84*t+6)
      = 2^721554505734.
```

For the other direction,

```text
C(M,r) < 2^M,
2^40*q_0^(t-2) > 2^(42*t-44),
```

so the real quotient is below `2^(86*t+43)`.  Its ceiling is at most that
power, yielding

```text
bits(L_rot) <= 86*t+44 = 738734374956.
```

No floating-point logarithm is used in either direction.

## 4. All legal quotient scales and the extremal scale

Let the agreement excess over `n/2` be

```text
e = a-n/2 = 2^34-1.
```

Every divisor of `n/2=2^40` is `c=2^j`.  The conditions

```text
d*c+s=e,
1<=d,
0<s<c
```

hold exactly for

```text
1 <= j <= 33,

d = 2^(34-j)-1,
s = 2^j-1,
N = 2^(41-j),
m = 2^(40-j)+2^(34-j)-1.
```

Thus there are exactly `33` legal quotient-rotation specializations at the
frozen agreement.  The choices `j=33` and `j=32` are the predecessor's
`(c,d,N)=(2^33,1,256)` and `(2^32,3,512)` cases.  The new choice is `j=1`.

### Theorem 4.1 — `c=2` dominates every other single-slice specialization at `q_0`

For every other legal scale, `c>=4`, so `N<=2^39`.  Even before any prefix
pigeonhole, one fixed auxiliary slice in the integrated theorem has fewer than

```text
2^(N-1) <= 2^(2^39-1)
```

candidate subsets.  By contrast, the `c=2` guaranteed prefix fiber is larger
than `2^721554505734`, and

```text
721554505734 - 2^39 = 171798691846 > 0.
```

Therefore the `c=2` pigeonhole lower bound exceeds the entire candidate
universe of every other legal single slice.  This proves that its printed lower
bound is strongest among the `33` legal specializations of the integrated
formula, even if an exact `d>1` prefix count were later found at another scale.
It does not rule out a separate theorem gluing several auxiliary slices into one
received word, and it is not a proof that quotient-rotation is extremal among
all Reed--Solomon received words.

## 5. Proof of the global upper cap

Fix a received word `u`.  For every listed polynomial `f` of degree `<k`, let

```text
A_f = {x in D : f(x)=u(x)}.
```

Then `|A_f|>=a`.  If `f` and `g` are distinct, the nonzero polynomial `f-g`
has degree `<k`, so it has at most `k-1` roots.  Consequently

```text
|A_f intersect A_g| <= k-1.
```

Count pairs `(f,T)` where `f` is listed and `T` is a `k`-subset of `A_f`.
Every listed `f` contributes at least `C(a,k)` pairs.  A fixed `k`-subset `T`
of `D` occurs for at most one `f`: two such polynomials would both equal `u`
on `T`, hence would agree on `k` distinct points and be identical.  There are
only `C(n,k)` possible `T`.  Thus

```text
L_u(a)*C(a,k) <= C(n,k),
```

which proves Theorem 2.2 after integer flooring.

### 5.1 Certified bit length of `U_pack`

Put `T=2^34` and `r=T-1`.  Then

```text
n=128*T,
k=64*T,
a=65*T-1,
C(a,k)=C(a,r).
```

Moreover,

```text
a = 65*r+64 >= 65*r.
```

Inside any `a`-set, take `r` disjoint blocks of `65` points.  Choosing one
point from each block gives `65^r` distinct `r`-subsets.  Therefore

```text
C(a,r) >= 65^r > 64^r = 2^(6*r).
```

Also `C(n,k)<=2^n`, since it is one term of the binomial sum.  Hence

```text
U_pack
< 2^(n-6*r)
= 2^(122*T+6)
= 2^2095944040454.
```

Again, this is integer-only and contains no floating-point estimate.

## 6. Routes killed

1. **Only the two predecessor specializations are legal.**  Killed by the exact
   `33`-scale census `1<=j<=33`.

2. **The `c=2^32,d=3,N=512` pigeonhole is the strongest declared-field lower.**
   Killed by `c=2`, whose guaranteed list has more than
   `2^721554505734` codewords.

3. **An exact `d>1` prefix count at any other quotient scale could recover the
   single-slice lower champion.**  Killed by the whole-slice obstruction: every
   `c>=4` slice has fewer than `2^(2^39-1)` candidates, while the `c=2`
   guaranteed fiber is already larger by an exponent margin of at least
   `171798691847` relative to `2^(2^39-1)`.

4. **Nothing deterministic caps the list from above.**  Killed by the global
   interpolation packing cap `U_pack`.

5. **The quotient-rotation census is automatically the exact RS list.**  Still
   killed by the predecessor obstruction: the construction theorem injects its
   subsets into nearby codewords but does not exhaust all nearby codewords.

6. **The classical second-moment Johnson denominator can supply this cap.**
   Killed by the exact negative denominator condition
   `a^2<n(k-1)`, with squared gap
   `1170851739846527019909119`.  The new cap uses `k`-subset packing instead.

## 7. Lean replay and proof boundary

The stdlib-only package is

```text
experimental/lean/l_list_truth_s1/
```

with public target `LListTruthS1` and namespace `LListTruthS1`.

Kernel-checked arithmetic instances are:

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

All eight theorems use `native_decide`, and every theorem is followed by
`#print axioms`.  No ordinary `decide`, `sorry`, `admit`, custom axiom, Mathlib,
or external Lean dependency is used.  The native-decision certificate axiom is
disclosed by the printed census.

Lean certifies the frozen integers, legal-scale census, and exponent arithmetic.
The finite-field locator construction is the integrated source theorem.  The
central-binomial, block-injection, and `k`-subset double-count arguments are the
mathematical proofs in this note; green compilation is not claimed to replace
source comparison.

Replay:

```text
cd experimental/lean/l_list_truth_s1
lake build LListTruthS1.Arithmetic LListTruthS1
lake build
```

## 8. Derivation-direction ledger

| printed value | direction | source |
|---|---|---|
| `q_0`, `n`, `k`, `a` | frozen | request and integrated theorem |
| radius numerator `1082331758593` | derived | exact subtraction; `declared_row_exact` |
| Johnson squared gap `1170851739846527019909119` | derived | exact arithmetic; `radius_and_johnson_exact` |
| exact radical radius gap | derived | rationalization of `a_J-a` |
| `33` legal quotient scales | derived and enumerated | divisor classification; `legal_scale_census_exact` |
| `c=2` parameters | derived | legal-scale formula; `c_two_specialization_exact` |
| `L_rot` closed form | derived | integrated quotient-rotation theorem |
| lower exponent `721554505734` | bounded | central coefficient, step ratios, `q_0<2^43`; `rotation_bit_interval_exact` |
| `L_rot` bit interval | bounded | exact power bracket for `q_0`; `field_power_bracket_exact`, `rotation_bit_interval_exact` |
| other-scale exponent ceiling `2^39-1` | bounded | total subset universe `C(N-1,m)<2^(N-1)` |
| dominance margins `171798691846`, `171798691847` | derived | exact subtraction; `quotient_scale_dominance_exact` |
| `U_pack` closed form | derived | `k`-subset interpolation double count |
| packing exponent `2095944040454` | bounded | 65-block injection and binomial sum; `packing_bit_cap_exact` |
| exact maximum list size | not obtained / open | off-slice codewords are not classified |

## 9. Current verdict

The exact list size remains open, but the declared family now has a proved
lower/upper bracket.  At `q_0`, `c=2` gives the strongest printed lower among all
`33` legal single-slice specializations.  Uniformly over all received words and
all declared fields, interpolation packing supplies a deterministic cap at the
same row and agreement.
