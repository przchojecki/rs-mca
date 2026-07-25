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

# Rate-half ordinary-list lower bracket: two strict improvements

## 1. Result and scope

Let

```text
C = RS[F_q,D,2^40],
n = |D| = 2^41,
a = 2^40 + 2^34 - 1 = 1116691496959,
delta = (n-a)/n = 1082331758593/2199023255552,
```

where `2^41 | (q-1)` and `D` is a multiplicative coset of size `2^41`.
This note concerns the ordinary list size: the number of distinct codewords of
`C` in one Hamming ball.  It never counts CA witnesses, MCA slopes, supports,
pairs, or rays, and it never changes the code to `C^+ = RS(k+1)`.

The source theorem is the cyclic quotient-rotation list floor in
`experimental/experiments.tex`, Section
`sec:rate-half-cyclic-quotient-rotation-floor`, theorem
`thm:rate-half-cyclic-quotient-rotation-floor`, with count and exact-agreement
formulas `eq:rate-half-list-floor` and
`eq:rate-half-exact-agreement`.

### Theorem 1.1 — uniform explicit odd-product lower

For every declared `q` and every declared coset `D`, there is a received word
having at least

```text
L_odd
= (C(255,129) + C(127,64))/256
= 11092230961998080258863221315535829014445503027953220397756221760927612835
```

distinct codewords of `C` agreeing with it in **exactly** `a` positions.
Consequently the list size at agreement **at least** `a` is at least `L_odd`.

The previously integrated floor was

```text
L_old
= ceil(C(255,129)/256)
= 11092230961998080258863221315535829014398723445840079610908300691051869570.
```

Thus the uniform construction improves the integrated floor by the exact
positive integer

```text
L_odd - L_old
= 46779582113140786847921069875743265.
```

The exact reduced ratio is

```text
L_odd / L_old
=
2218446192399616051772644263107165802889100605590644079551244352185522567
/
2218446192399616051772644263107165802879744689168015922181660138210373914.
```

### Theorem 1.2 — stronger declared-field specialization

For the fully declared field

```text
q_0 = 6597069766657 = 3*2^41 + 1,
```

and every multiplicative coset `D` of size `2^41`, there is a received word
having at least

```text
L_alt
= ceil(C(511,259)/(512*q_0^2))
= 10117903140720209347161374303886548269936958556723901042315597656335386755181744190072527742895613796941873719315303119609998
```

distinct codewords agreeing with it in **exactly** `a` positions.  Hence this
is also a lower bound at agreement **at least** `a`.

Its exact improvement over `L_old` is

```text
L_alt - L_old
= 10117903140720209347161374303886548269936958556723889950084635658255127891960428654243513344172167956862262811014612067740428.
```

Its exact reduced ratio to the integrated floor is

```text
L_alt / L_old
=
722707367194300667654383878849039162138354182623135788736828404023956196798696013576609124492543842638705265665378794257857
/
792302211571291447061658665395416358171337388988577115064878620789419255,
```

and this ratio is strictly greater than `2^169`.

Theorems 1.1 and 1.2 are lower constructions.  They do not determine the exact
maximum list size and do not supply a uniform upper cap.  Under the round
contract, either strict improvement is a full lower-side close; Theorem 1.1 is
uniform over the whole declared family, while Theorem 1.2 is much larger on the
one fully declared base field.

## 2. Exact Lane L print block

```text
row:                 (F_q,D,k=2^40,n=2^41,rho=1/2), 2^41 | (q-1), |D|=2^41
object:              ordinary LIST, not MCA
radius/agreement:    delta=1082331758593/2199023255552; agreement exactly a=1116691496959
Johnson comparison:  a^2 < 2^41*(2^40-1), with exact positive gap 1170851739846527019909119
bound:               uniform lower L_odd printed in Theorem 1.1; q_0-specific lower L_alt printed in Theorem 1.2
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS[F_q,D,2^40]; no C^+ shift
status:              PROVED
```

## 3. Mechanism for the uniform odd-product fiber

Use the integrated specialization

```text
c=2^33, N=256, d=1, m=129, s=c-1.
```

Write the quotient coset as `Q=b_0 K`, where `K` is cyclic of order `256`, and
choose a generator `zeta` of `K`.  Every `129`-subset
`A subset Q\{b_0}` corresponds to a `129`-subset
`S subset Z/256Z\{0}`.  Its normalized product is

```text
product(A) / b_0^129 = zeta^(sum S).
```

Let

```text
F(r) = #{S subset {1,...,255}: |S|=129 and sum(S)=r mod 256}.
```

In the `d=1` quotient-rotation construction, the common degree-`>=k` part of
the locator depends only on this product and on the fixed monic coefficient.
Thus every fixed residue `r` produces one explicit received-word prefix, and
its construction list contains exactly `F(r)` codewords before any possible
off-slice additions.

### 3.1 Character formula

Let `B=C(255,129)`.  Character orthogonality on the cyclic group gives

```text
256 F(r) = B + sum_{j=1}^8 A_(2^j) c_(2^j)(r),
```

where `c_d(r)` is the Ramanujan sum over the characters of exact order `d` and

```text
A_d
= [z^129] (1-z^d)^(256/d)/(1+z)
= -(-1)^floor(129/d) C(256/d-1,floor(129/d)).
```

For `d=2,4,8,16,32,64,128,256`, the coefficients are

```text
-C(127,64), -C(63,32), -C(31,16), -6435, -35, -3, 1, -1.
```

If `r` is odd, `c_2(r)=-1` and every `c_(2^j)(r)` with `j>=2` is zero.  Hence

```text
F(r) = (C(255,129)+C(127,64))/256 = L_odd
```

for every one of the `128` odd residues.  Choosing, for example, `r=1` fixes a
concrete normalized product and therefore a concrete received-word prefix.
The exact-agreement and distinct-codeword conclusions then follow from the
source theorem: distinct subsets have distinct root sets and distinct
locators, and each locator vanishes on exactly

```text
129*2^33 + (2^33-1) = 2^40 + 2^34 - 1 = a
```

points of `D`.

### 3.2 Full product-fiber spectrum

The same character formula gives the complete residue spectrum.  Here `v_2(r)`
is printed only for nonzero residues.

| residue class | multiplicity | exact fiber count | derivation |
|---|---:|---:|---|
| `v_2(r)=0` | 128 | 11092230961998080258863221315535829014445503027953220397756221760927612835 | character formula |
| `v_2(r)=1` | 64 | 11092230961998080258863221315535829014351943863726938824067538309226683299 | character formula |
| `v_2(r)=2` | 32 | 11092230961998080258863221315535829014351943863726938824053220933130265251 | character formula |
| `v_2(r)=3` | 16 | 11092230961998080258863221315535829014351943863726938824053220933120873571 | character formula |
| `v_2(r)=4` | 8 | 11092230961998080258863221315535829014351943863726938824053220933120873171 | character formula |
| `v_2(r)=5` | 4 | 11092230961998080258863221315535829014351943863726938824053220933120873167 | character formula |
| `v_2(r)=6` | 2 | 11092230961998080258863221315535829014351943863726938824053220933120873166 | character formula |
| `v_2(r)=7` | 1 | 11092230961998080258863221315535829014351943863726938824053220933120873167 | character formula |
| `r=0` | 1 | 11092230961998080258863221315535829014351943863726938824053220933120873166 | character formula |

The odd fibers are therefore the exact maxima of this construction slice.  The
multiplicity-weighted sum of the nine rows is exactly `C(255,129)`; this mass
identity and every printed count are checked by the Lean package.

## 4. Mechanism for the stronger declared-field specialization

The integrated theorem is not tied to `c=2^33`.  At the same row and exact
agreement, choose instead

```text
c=2^32,
N=n/c=512,
d=3,
m=N/2+d=259,
s=c-1.
```

All theorem hypotheses hold:

```text
c | n/2,
1 <= d <= N/2-1,
0 < s < c,
n/2 + d*c + s = 2^40 + 2^34 - 1 = a.
```

The general prefix count is `N*q^(d-1)=512*q^2`.  At `q=q_0`, pigeonhole
therefore gives

```text
ceil(C(511,259)/(512*q_0^2)) = L_alt.
```

The source theorem again proves distinctness and exact agreement.  This second
construction uses a different quotient size and a different received word; it
is not an upper bound on, or an exact enumeration of, the `N=256` slice.

## 5. Exact bankability block

The bankability block for this note is the block it begins with; it is not
repeated here.

Bridge to the row numerator: this raises the recorded floor of the declared
rate-half coset family. The upper side of the family is open, and no deployed
row is affected.

## 6. Routes killed

1. **The integrated ceiling-average is the exact `N=256` construction floor.**
   Killed by the order-two character contribution.  Every odd product class has
   `L_odd` members, exactly
   `46779582113140786847921069875743265` more than the integrated ceiling.

2. **The 256 product classes are uniform.**
   Killed by the nine-row `2`-adic spectrum in Section 3.2.  The obstruction is
   the exact nontrivial character-coefficient vector
   `[-C(127,64),-C(63,32),-C(31,16),-6435,-35,-3,1,-1]`.

3. **The frozen quotient choice `c=2^33`, `N=256`, `d=1` is optimal for the
   declared field.**  Killed by the valid `c=2^32`, `N=512`, `d=3`
   specialization, whose lower bound exceeds the old floor by the exact integer
   printed in Theorem 1.2 and by a ratio greater than `2^169`.

4. **An exact census of the quotient-rotation slice is automatically a list
   upper bound.**  Cut: the source theorem injects its construction subsets
   into codewords but does not prove that every nearby codeword lies in that
   slice.  The exact family list size and every uniform upper cap remain open.

## 7. Lean replay and proof boundary

The stdlib-only package is
`experimental/lean/l_ratehalf_bracket_s1/`, with public target
`LRatehalfBracketS1` and namespace `LRatehalfBracketS1`.

The arithmetic certificates are:

```text
LRatehalfBracketS1.declared_row_exact
LRatehalfBracketS1.radius_and_johnson_exact
LRatehalfBracketS1.alternate_parameters_exact
LRatehalfBracketS1.alternate_binomial_exact
LRatehalfBracketS1.alternate_lower_exact
LRatehalfBracketS1.alternate_strict_improvement
LRatehalfBracketS1.alternate_ratio_exact
LRatehalfBracketS1.integrated_floor_formula_exact
LRatehalfBracketS1.odd_product_fiber_arithmetic
LRatehalfBracketS1.character_coefficients_exact
LRatehalfBracketS1.product_spectrum_mass_exact
LRatehalfBracketS1.odd_product_is_spectrum_max
LRatehalfBracketS1.odd_product_ratio_exact
```

All thirteen theorems use `native_decide`, and every theorem is followed by
`#print axioms`.  No ordinary `decide`, `sorry`, `admit`, custom axiom, Mathlib,
or external dependency is used.  The generated native-decision certificate
axiom is therefore disclosed on every affected theorem; the build log prints
the exact census.

Lean verifies the frozen arithmetic and the complete printed product-spectrum
shadow.  The finite-field locator construction, character-orthogonality proof,
and map from construction subsets to distinct exact-agreement codewords are the
mathematical proofs in this note together with the integrated source theorem;
green compilation is not claimed to replace that source comparison.

## 8. Derivation-direction ledger

| printed value | direction | source |
|---|---|---|
| `q_0=6597069766657`, `n=2^41`, `k=2^40`, `a=1116691496959` | frozen | round contract and integrated source |
| radius numerator `1082331758593` and Johnson gap `1170851739846527019909119` | derived | exact integer subtraction; `radius_and_johnson_exact` |
| `C(255,129)` and `L_old` | enumerated then derived | `fastBinomial`; `integrated_floor_formula_exact` |
| `C(127,64)` and eight character coefficients | enumerated | `fastBinomial`; `odd_product_fiber_arithmetic`; `character_coefficients_exact` |
| nine product-fiber counts | derived | character formula and power-of-two Ramanujan sums; Lean mass/max checks |
| `L_odd` | derived | exact odd-character reduction; `odd_product_fiber_arithmetic` |
| `L_odd-L_old` and reduced ratio | derived | exact integer arithmetic; `odd_product_fiber_arithmetic`; `odd_product_ratio_exact` |
| alternate parameters `(c,N,d,m,s)=(2^32,512,3,259,2^32-1)` | derived | same-agreement specialization; `alternate_parameters_exact` |
| `C(511,259)` | enumerated | `fastBinomial`; `alternate_binomial_exact` |
| `512*q_0^2`, `L_alt`, and ceiling slack | derived | exact integer arithmetic; `alternate_lower_exact` |
| `L_alt-L_old`, reduced ratio, and ratio `>2^169` | derived | exact integer arithmetic; `alternate_strict_improvement`; `alternate_ratio_exact` |
| exact family list size / deterministic upper cap | not obtained / open | no exhaustive off-slice theorem |

## 9. Verdict and next step

**COUNTEREXAMPLE_NEW_FLOOR.**  The integrated floor is strictly improved on the
whole declared family, and the one fully declared field has a much larger
independent lower construction at the same exact post-Johnson agreement.

The natural next step is no longer to sharpen the `N=256` average.  It is to
optimize the general `(c,N,d,s)` quotient-rotation family as a function of `q`
and then prove an off-slice upper theorem, or exhibit a third construction that
raises the lower floor again.
