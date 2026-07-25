# Two strict ordinary-list lower improvements on the declared rate-half coset family

**Request worked from, in one line.** Decide the ordinary list size of the declared rate-half multiplicative-coset Reed--Solomon family at agreement `a=2^40+2^34-1`, with a strict lower construction, deterministic upper cap, precise conjecture, or rigorous route cut accepted as a round close.

## Abstract

For the ordinary Reed--Solomon code

```text
C = RS[F_q,D,2^40],
|D| = 2^41,
2^41 | (q-1),
```

at agreement

```text
a = 1116691496959
```

this paper raises the integrated cyclic quotient-rotation list floor in two independent ways.  First, on every field and coset in the declared family, an exact character calculation identifies each odd subset-product class in the original quotient slice and gives a received word with at least

```text
11092230961998080258863221315535829014445503027953220397756221760927612835
```

distinct codewords agreeing in exactly `a` positions.  Second, on the fully declared field `q_0=6597069766657`, a different valid quotient specialization gives at least

```text
10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998
```

such codewords at the same exact agreement.  Either value is strictly larger than the previously integrated floor, so the round closes on its LOWER side.  The exact maximum list size and every nontrivial deterministic upper cap remain open.

## Bankability block

```yaml
workboard_item: L
row: "(F_q,D,k=2^40,n=2^41,rho=1/2), 2^41 | (q-1), D a multiplicative coset of size 2^41"
object: LIST
target_epsilon: "not applicable; exact finite-family list lower bound"
agreement: 1116691496959
B_star: "n/a"
direct_statement: "For every declared field and coset there is one received word with at least 11092230961998080258863221315535829014445503027953220397756221760927612835 distinct codewords of C=RS[F_q,D,2^40] agreeing in exactly 1116691496959 positions. For the declared field q=6597069766657 there is, independently, one received word with at least 10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998 such codewords at the same exact agreement."
architecture: DIRECT
partition_digest: "n/a (DIRECT)"
atom_or_cell: DIRECT
quantifier: "The first lower bound is uniform over every finite field F_q with 2^41 | (q-1) and every multiplicative coset D of size 2^41. The second lower bound is for q=6597069766657 and every such D. Both are existential over one received word and count distinct ordinary Reed--Solomon codewords."
projection_and_unit: "ordinary Reed--Solomon codewords in one Hamming ball; no support count, CA numerator, MCA numerator, ray, or slope"
claimed_bound: "Uniform lower 11092230961998080258863221315535829014445503027953220397756221760927612835; declared-q lower 10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998; both at agreement exactly 1116691496959 and hence also at agreement at least that integer."
status: PROVED
impact: LOCAL_ONLY
falsifier: "A failure of the integrated cyclic quotient-rotation theorem under either printed specialization; an odd normalized product class whose 129-subset count differs from (C(255,129)+C(127,64))/256; a collision of two construction subsets after projection to codewords; a locator with a zero set other than the prescribed mc+s points; or any failed exact integer certificate in the Lean package."
replay: "cd experimental/lean/l_ratehalf_bracket_s1 && lake build LRatehalfBracketS1.Arithmetic LRatehalfBracketS1.ProductFiber LRatehalfBracketS1 && lake build"
```

## 1. Frozen family and exact radius

The code is ordinary `LIST`, not MCA or CA.  Throughout,

```text
n = 2^41 = 2199023255552,
k = 2^40 = 1099511627776,
rho = k/n = 1/2,
a = 2^40 + 2^34 - 1 = 1116691496959.
```

The closed-ball radius is

```text
delta = (n-a)/n = 1082331758593/2199023255552.
```

The fraction is reduced.  The agreement is strictly beyond the exact finite-field Johnson agreement because

```text
a^2 < n(k-1),
n(k-1)-a^2 = 1170851739846527019909119 > 0.
```

No conversion is used: the code is `C=RS[F_q,D,2^40]`, not `C^+=RS[F_q,D,2^40+1)`, and there is no radius shift or intrinsic-radius hypothesis.

## 2. Current best statements

### Theorem A — uniform odd-product construction

For every finite field `F_q` satisfying `2^41 | (q-1)` and every multiplicative coset `D` of size `2^41`, there is one received word for which at least

```text
L_odd
= (C(255,129)+C(127,64))/256
= 11092230961998080258863221315535829014445503027953220397756221760927612835
```

distinct codewords of `C` agree in **exactly** `a` positions.  Therefore the list size at agreement **at least** `a` is also at least `L_odd`.

The integrated floor was

```text
L_old
= ceil(C(255,129)/256)
= 11092230961998080258863221315535829014398723445840079610908300691051869570.
```

The strict improvement is

```text
L_odd-L_old = 46779582113140786847921069875743265.
```

The exact reduced ratio is

```text
L_odd/L_old
=
2218446192399616051772644263107165802889100605590644079551244352185522567
/
2218446192399616051772644263107165802879744689168015922181660138210373914.
```

### Theorem B — stronger specialization on the declared field

Take the fully declared field

```text
q_0 = 6597069766657 = 3*2^41+1.
```

For every multiplicative coset `D` of size `2^41` in this field, there is one received word for which at least

```text
L_alt
= ceil(C(511,259)/(512*q_0^2))
= 10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998
```

distinct codewords agree in **exactly** `a` positions.  Hence the same integer is a lower bound at agreement **at least** `a`.

The exact difference from the integrated floor is

```text
L_alt-L_old
= 10117903140720209347161374303886548269936958556723889950084635658255127891960428654243513344172167956862262811014612067740428.
```

The exact reduced ratio is

```text
L_alt/L_old
=
722707367194300667654383878849039162138354182623135788736828404023956196798696013576609124492543842638705265665378794257857
/
792302211571291447061658665395416358171337388988577115064878620789419255,
```

and it is strictly greater than `2^169`.

### Certified stop on exactness

No upper theorem is obtained.  The exact family list size is open because the quotient-rotation theorem injects its construction subsets into nearby codewords but does not prove that all nearby codewords arise from that slice.  Thus the current bracket has the lower endpoint `L_odd` uniformly and the stronger endpoint `L_alt` at `q_0`; its upper endpoint remains the trivial full-codeword count.

## 3. Mechanism

### 3.1 Integrated source theorem

The source is `experimental/experiments.tex`, Section `sec:rate-half-cyclic-quotient-rotation-floor`, theorem `thm:rate-half-cyclic-quotient-rotation-floor`.  For parameters

```text
c | n/2,
N = n/c,
1 <= d <= N/2-1,
m = N/2+d,
0 < s < c,
```

it constructs a received word with at least

```text
ceil(C(N-1,m)/(N*q^(d-1)))
```

distinct codewords agreeing in exactly

```text
n/2+d*c+s
```

positions.  The exact count and exact-agreement formulas are labelled `eq:rate-half-list-floor` and `eq:rate-half-exact-agreement` in that source.

### 3.2 Exact product fibers in the original quotient slice

Use

```text
c=2^33, N=256, d=1, m=129, s=2^33-1.
```

Write the quotient coset as `Q=b_0 K`, with `K` cyclic of order `256`, and fix a generator `zeta`.  A `129`-subset `A` of `Q\{b_0}` corresponds to a `129`-subset `S` of the nonzero residues modulo `256`, and

```text
product(A)/b_0^129 = zeta^(sum S).
```

Define

```text
F(r) = #{S subset {1,...,255}: |S|=129, sum(S)=r mod 256}.
```

For `d=1`, the source locator's degree-`>=k` part is fixed by the subset product and the fixed monic coefficient.  Therefore one fixed residue `r` gives one fixed received-word prefix and exactly `F(r)` construction codewords before any off-slice additions.

Character orthogonality gives

```text
256 F(r) = C(255,129) + sum_{j=1}^8 A_(2^j)c_(2^j)(r),
```

where `c_d(r)` is a Ramanujan sum and

```text
A_d
= [z^129](1-z^d)^(256/d)/(1+z)
= -(-1)^floor(129/d) C(256/d-1,floor(129/d)).
```

For the orders `2,4,8,16,32,64,128,256`, the coefficient vector is

```text
[-C(127,64), -C(63,32), -C(31,16), -6435, -35, -3, 1, -1].
```

If `r` is odd, `c_2(r)=-1` and the other seven Ramanujan sums vanish.  Thus every odd residue has

```text
F(r)=(C(255,129)+C(127,64))/256=L_odd.
```

Choosing `r=1` fixes a concrete normalized product and hence a concrete received-word prefix.  Distinct subsets give distinct root sets, locators, and codewords by the integrated theorem.  Every locator has exactly

```text
129*2^33+(2^33-1)=a
```

zeros on `D`, proving exact agreement.  The full character formula also shows that the `128` odd residues are the maxima of the complete `256`-residue spectrum.

### 3.3 A different quotient at the same agreement

On `q_0`, choose instead

```text
c=2^32,
N=512,
d=3,
m=259,
s=2^32-1.
```

The source hypotheses hold, and

```text
n/2+d*c+s = 2^40+2^34-1 = a.
```

The general denominator is now

```text
N*q_0^(d-1)=512*q_0^2
=22282920707143600347625292288.
```

The exact numerator is

```text
C(511,259)
=225456433407227622163483597843439619508493793232120672594634608050001706637890080324384766467272782434839065859827588447117318678944033170766566666570205.
```

Taking the exact ceiling gives `L_alt`.  This construction uses a different quotient and generally a different received word; it does not claim that the original quotient slice contains `L_alt` codewords.

## 4. Evidence for and against

### Kernel-checked evidence

The stdlib-only package is

```text
experimental/lean/l_ratehalf_bracket_s1/
```

with public target `LRatehalfBracketS1`.  Both the explicit module targets and the package default target build successfully.

The frozen row and alternate specialization are checked by:

```text
LRatehalfBracketS1.declared_row_exact
LRatehalfBracketS1.radius_and_johnson_exact
LRatehalfBracketS1.alternate_parameters_exact
LRatehalfBracketS1.alternate_binomial_exact
LRatehalfBracketS1.alternate_lower_exact
LRatehalfBracketS1.alternate_strict_improvement
LRatehalfBracketS1.alternate_ratio_exact
```

The exact product-fiber arithmetic is checked by:

```text
LRatehalfBracketS1.integrated_floor_formula_exact
LRatehalfBracketS1.odd_product_fiber_arithmetic
LRatehalfBracketS1.character_coefficients_exact
LRatehalfBracketS1.product_spectrum_mass_exact
LRatehalfBracketS1.odd_product_is_spectrum_max
LRatehalfBracketS1.odd_product_ratio_exact
```

All `13` theorems use `native_decide` and have an adjacent `#print axioms` census.  Twelve report only their generated native-decision certificate axiom; `LRatehalfBracketS1.alternate_parameters_exact` additionally reports `propext`.  There is no ordinary `decide`, `sorry`, `admit`, custom axiom, Mathlib import, or external package dependency.

### Source comparison

Lean certifies the exact integer gates and the complete printed arithmetic shadow.  The finite-field locator construction and subset-to-codeword injection are supplied by the integrated source theorem; the character-orthogonality argument above supplies the exact product-fiber count.  Compilation is therefore evidence for the arithmetic statements, not a claim that the TeX theorem was silently re-formalized.

### Evidence against an exact settlement

The construction map is injective but not proved surjective onto the Hamming ball.  No argument here controls codewords whose agreement locators are outside either quotient-rotation slice.  Consequently an upper cap equal or near to either lower count is unsupported, and the exact list size remains open.

## 5. Routes killed

1. **Ceiling-average sharpness in the original slice.**  Killed by the exact order-two character contribution: every odd product fiber contains `L_odd`, exceeding `L_old` by `46779582113140786847921069875743265`.

2. **Uniformity of the product classes.**  Killed by the nonzero coefficient vector `[-C(127,64),-C(63,32),-C(31,16),-6435,-35,-3,1,-1]`; the product distribution is resolved by the `2`-adic valuation of the target exponent.

3. **Optimality of the frozen quotient parameters on `q_0`.**  Killed by the legal tuple `(c,N,d,m,s)=(2^32,512,3,259,2^32-1)`, which gives `L_alt/L_old>2^169` at the same exact agreement.

4. **Turning a slice census directly into a list upper bound.**  Cut by the missing surjectivity statement.  The exact obstructing quantity is the uncounted off-slice codeword population; no finite value for it is proved here.

## 6. Open questions and natural next step

The main open questions are:

- What choice of `(c,N,d,s)` maximizes the general quotient-rotation lower formula for a given `q` while keeping the same agreement?
- Can the higher-prefix vector for `d>1` be analyzed exactly, as the product coordinate was for `d=1`, rather than only by pigeonhole?
- Can every codeword near the constructed received word be classified into finitely many quotient slices, yielding the first nontrivial upper cap on this family?
- Is there a received word combining several parameter slices without collapsing codeword distinctness?

The natural next step is an exact optimization theorem for the general quotient-rotation parameter family, followed by an off-slice locator classification.  An optimization alone can raise the lower floor again; the locator classification is the missing ingredient for a genuine upper/lower bracket.

## 7. Derivation-direction ledger

Every mathematical integer printed above is classified here.

| value or family of values | direction | justification |
|---|---|---|
| `n=2^41=2199023255552`, `k=2^40=1099511627776`, `rho=1/2`, `a=2^40+2^34-1=1116691496959` | frozen | request and integrated source |
| `q_0=6597069766657=3*2^41+1` | frozen | request and integrated source |
| radius numerator `1082331758593`, denominator `2199023255552`, and reducedness | derived | exact subtraction and gcd; `radius_and_johnson_exact` |
| Johnson gap `1170851739846527019909119` | derived | exact integer subtraction; `radius_and_johnson_exact` |
| original tuple `(c,N,d,m,s)=(2^33,256,1,129,2^33-1)` | frozen specialization | integrated source |
| group/residue counts `256`, `255`, `129`, `128`, and character-order count `8` | derived | quotient size, deleted identity, subset size, odd-residue count, and powers of two dividing `256` |
| `C(255,129)=2839611126271508546268984656777172227686073202135060380392524976909278609885` | enumerated | `fastBinomial`; `integrated_floor_formula_exact` |
| `L_old=11092230961998080258863221315535829014398723445840079610908300691051869570` | derived | exact ceiling of `C(255,129)/256`; `integrated_floor_formula_exact` |
| `C(127,64)=11975573020964041433067793888190275875` | enumerated | `fastBinomial`; `odd_product_fiber_arithmetic` |
| coefficient vector `[-C(127,64),-C(63,32),-C(31,16),-6435,-35,-3,1,-1]` | derived, entries enumerated | coefficient extraction formula; `character_coefficients_exact` |
| `L_odd=11092230961998080258863221315535829014445503027953220397756221760927612835` | derived | character orthogonality for an odd target; `odd_product_fiber_arithmetic` |
| `L_odd-L_old=46779582113140786847921069875743265` | derived | exact subtraction; `odd_product_fiber_arithmetic` |
| reduced ratio `L_odd/L_old` printed in Theorem A | derived | exact gcd and cross multiplication; `odd_product_ratio_exact` |
| exact-zero identity `129*2^33+(2^33-1)=a` and target `r=1` | derived / chosen | source exact-agreement formula and a fixed odd residue |
| alternate tuple `(c,N,d,m,s)=(2^32,512,3,259,2^32-1)` | derived | same-agreement parameter solution; `alternate_parameters_exact` |
| denominator `512*q_0^2=22282920707143600347625292288` | derived | exact multiplication; `alternate_lower_exact` |
| `C(511,259)=225456433407227622163483597843439619508493793232120672594634608050001706637890080324384766467272782434839065859827588447117318678944033170766566666570205` | enumerated | `fastBinomial`; `alternate_binomial_exact` |
| `L_alt=10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998` | derived | exact ceiling; `alternate_lower_exact` |
| `L_alt-L_old=10117903140720209347161374303886548269936958556723889950084635658255127891960428654243513344172167956862262811014612067740428` | derived | exact subtraction; `alternate_strict_improvement` |
| reduced ratio `L_alt/L_old` and comparison `>2^169` | derived / bounded | gcd, cross multiplication, and exact division; `alternate_ratio_exact`, `alternate_strict_improvement` |
| theorem count `13`, native-decision-only count `12`, and one additional-`propext` declaration | enumerated | declaration list and printed axiom census |
| exact maximum list size and every nontrivial deterministic upper cap | not obtained / open | no off-slice exhaustion or surjectivity theorem |

## 8. References

1. `experimental/experiments.tex`, Section `sec:rate-half-cyclic-quotient-rotation-floor`.
2. `experimental/experiments.tex`, theorem `thm:rate-half-cyclic-quotient-rotation-floor`.
3. `experimental/experiments.tex`, equations `eq:rate-half-list-floor` and `eq:rate-half-exact-agreement`.
4. `experimental/notes/thresholds/ratehalf_list_bracket.md`.
5. `experimental/lean/l_ratehalf_bracket_s1/LRatehalfBracketS1/Arithmetic.lean`.
6. `experimental/lean/l_ratehalf_bracket_s1/LRatehalfBracketS1/ProductFiber.lean`.
7. `experimental/lean/l_ratehalf_bracket_s1/LRatehalfBracketS1.lean`.

## Serendipity epilogue

The most interesting unasked observation is that the declared agreement does not determine a unique quotient scale.  The identity `d*c+s=2^34-1` leaves a family of valid factorizations, and changing from the original product-only prefix to a slightly smaller fiber with two additional free prefix coordinates makes the combinatorial numerator grow so much faster than the field-denominator penalty that the lower bound jumps by more than `2^169`.  This turns the quotient parameter `c` from bookkeeping into a genuine optimization variable and suggests that the current declared-field lower may still be far from the best construction available at the same radius.
