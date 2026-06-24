# M2 LD_sw Versus ABF/GG Line-Decoding Separation

**Status:** PROVED structural lemmas; COUNTEREXAMPLE / FINITE instance.

This note records a finite Reed-Solomon example showing that the support-wise
line-decoding numerator `LD_sw` does not imply the stronger ABF/GG
`(delta,a,b)` line-decodability predicate.  The received line is nonconstant,
with nonzero codeword direction, so the separation does not depend on allowing
degenerate constant lines.  Thus the M2 bridge can import an external
line-decoding theorem in the forward direction, but a small `LD_sw` bound
should not be read as proving the ABF/GG assignment-collinearity conclusion.

## Claim

There is a Reed-Solomon code `C=RS[F_13,{0,...,7},3]`, an agreement threshold
`a=5`, and a nonconstant received line with support-wise `LD_sw` contribution
`0`, while a close-codeword assignment on that same line violates the ABF/GG
collinearity conclusion with `b=n+1=9`.

Equivalently, bounded support-wise MCA numerator is not a converse to ABF/GG
line-decodability.

## Structural Mechanism

The finite example is an instance of a general code-direction invisibility
lemma.

Let `C <= F^D` be any linear code, let `r in F^D`, and let `v in C`.  For any
agreement threshold `a`, the received line

```text
ell_gamma = r + gamma v
```

has no support-wise noncontained slopes.  Indeed, if `ell_gamma|S` is explained
by a codeword on a support `S`, then

```text
r|S = ell_gamma|S - gamma v|S
```

is also explained on `S`, and `v|S` is explained because `v in C`.  Thus every
explaining support is already contained in the support-wise MCA sense.  If
`r notin C` and `v != 0`, the received line may be nonconstant and not
contained in `C`, but its contribution to `LD_sw(C,a)` is still `0`.

More generally, `LD_sw` is invariant under adding a codeword to the received
line direction.  For any line `f+gamma g` and any `v in C`, the support-wise
noncontained slopes for

```text
f + gamma(g+v)
```

are exactly the support-wise noncontained slopes for `f+gamma g`.  On each
support, subtract the codeword `gamma v` from an explaining codeword for the
line point; this gives the equivalence of line-point explainability.  The
contained-support condition is also unchanged, because `g|S` is explained by a
codeword if and only if `(g+v)|S` is explained by a codeword.  Thus the
support-wise numerator sees the direction only modulo `C`.  The code-direction
invisibility lemma is the special case where the direction is zero in this
quotient.

This invisibility is specific to the support-wise numerator.  For a code-line
candidate `u0+gamma u1` and an assigned close codeword `U(gamma)`, put

```text
c_gamma = U(gamma) - gamma v.
```

Then `U(gamma)` is close to `r+gamma v` exactly when `c_gamma` is close to
`r`, and

```text
u0 + gamma u1 = U(gamma)
```

holds exactly when

```text
u0 + gamma(u1-v) = c_gamma.
```

Thus, on a code-direction received line, the ABF/GG collinearity conclusion is
equivalent to finding a large affine graph inside the shifted assignment
`gamma -> c_gamma` into the ordinary close list of `r`.  The support-wise
numerator has already vanished before this assignment-collinearity question
appears.

Write

```text
L_a(r) = {c in C : c agrees with r on at least a coordinates}.
```

This gives an exact code-direction reduction.  For a set `L subset C`, define
`G_b(L)` to be the largest size of a partial assignment

```text
phi:T -> L,        T subset F,
```

whose graph contains no `b` points of any affine code-space line

```text
gamma -> c + gamma w,        c,w in C.
```

Assume `b >= 3` and `|C| > binom(|F|,2)`, so the greedy extension lemma below
applies.  Then ABF/GG line-decodability on all code-direction lines
`r+gamma v`, `v in C`, with trigger numerator `A`, is equivalent to

```text
G_b(L_a(r)) < A
```

for every base word `r`.  The forward direction is just the shifted-assignment
reduction: any violating decoded assignment restricts on its close slopes to a
graph-free partial assignment into `L_a(r)`.  Conversely, any graph-free
partial assignment into `L_a(r)` of size `A` extends to a full graph-free
decoded assignment, giving a violating code-direction line.  Thus the exact
positive input needed beyond `LD_sw` is a finite-geometric statement about
affine graphs inside ordinary close lists.

This exact criterion is strictly stronger than forbidding affine caps inside
the close list.  If `L_a(r)` contains a full nonconstant affine code-line

```text
{c0 + tau w : tau in F},        w != 0,
```

then `G_b(L_a(r))=|F|` for every `3 <= b <= |F|`.  Indeed, the assignment

```text
gamma -> c0 + gamma^(b-1) w
```

has no `b` points on an affine graph: after subtracting any affine graph
`c+gamma u`, apply any linear functional on the code space that sends `w` to
`1`.  The resulting scalar polynomial has leading term `gamma^(b-1)`, so it is
nonzero of degree `b-1` and has at most `b-1` roots.  Since no partial
assignment has more than `|F|` slopes, this is exact.  Therefore a positive M2
line-decodability theorem must control graph-free parametrizations of close
lists, not only large affine caps inside those lists.

This reduction has an exact pigeonhole half.  Let

```text
L = L_a(r).
```

If an assignment is close on a set `T subset F` of slopes, then the shifted
values `c_gamma` for `gamma in T` lie in `L`.  Hence some `c in L`
appears at least

```text
ceil(|T|/|L|)
```

times.  The affine code-line `c + gamma v` agrees with the original assignment
on all those slopes.  Consequently, for any trigger size `A`, code-direction
lines automatically satisfy the ABF/GG `b`-collinearity conclusion whenever

```text
|L| <= floor((A-1)/(b-1)).
```

In the full-field case `A=|F|`, this automatic range is
`|L| < ceil(|F|/(b-1))`.

As a direct obstruction, suppose `m` distinct codewords
`c_1,...,c_m in C` all agree with `r` on at least `a` coordinates, and split
the field into nonempty buckets

```text
F = A_1 disjoint union ... disjoint union A_m.
```

Define

```text
U(gamma) = c_i + gamma v,        gamma in A_i.
```

Every assigned codeword is `a`-close to the corresponding line point
`r+gamma v`.  However, any code-line `u0+gamma u1` agrees with this assignment
on at most

```text
max( max_i |A_i|, m )
```

slopes.  To see this, subtract `gamma v` from the target assignment.  If
`u1=v`, the shifted code-line is constant and can match only one bucket.  If
`u1 != v`, then the shifted code-line can hit each fixed codeword `c_i` for at
most one slope.  Therefore any collinearity threshold
`b > max(max_i |A_i|,m)` fails, even though the support-wise numerator of the
same received line is zero.

With a balanced partition this becomes the bound

```text
max(ceil(|F|/m), m).
```

The same argument has a sharper large-field form.  For a subset
`S subset L_a(r)`, define its affine-line intersection number inside the code
space by

```text
lambda(S) =
  max_{c in C, w in C \ {0}} |S cap {c+gamma w : gamma in F}|.
```

If `S` can be assigned to slope buckets of size at most `b-1` and
`lambda(S) <= b-1`, then the same code-direction line violates the
`b`-slope collinearity conclusion.  Constant shifted code-lines hit only one
bucket, and nonconstant shifted code-lines hit at most `lambda(S)` values of
`S`.  Thus ABF/GG line-decodability on code-direction lines forces the
`b`-affine-cap number

```text
alpha_b(L_a(r)) =
  max{|S| : S subset L_a(r) and lambda(S) <= b-1}
```

to be smaller than the first size that admits such a bucket partition.

For an actual `b`-affine cap `L`, this obstruction is exact in the `G_b`
criterion:

```text
G_b(L) = min(|F|, (b-1)|L|).
```

The upper bound is pigeonhole: any assignment on more than `(b-1)|L|` slopes
uses some value of `L` at least `b` times, giving a constant affine graph.  For
the lower bound, assign `min(|F|,(b-1)|L|)` slopes to values of `L`, with no
value used more than `b-1` times.  Constant affine graphs hit at most `b-1`
assigned slopes, while nonconstant affine graphs hit at most `lambda(L) <= b-1`
assigned slopes.  Thus the assignment is graph-free.

This cap obstruction also applies to a partial ABF/GG trigger, not only to the
full-field trigger, once the decoded assignment can be extended away from the
close slopes.  Suppose `b >= 3`, the code space has

```text
|C| > binom(|F|,2),
```

and a partial shifted assignment `phi:T -> C` has no `b` points on an affine
graph.  Then `phi` extends to a full assignment `F -> C` with the same property:
add slopes one at a time, and avoid values that would complete an affine graph
already hit on `b-1` old slopes.  Each such graph is determined by a pair of
old slope-value points, so at most `binom(|F|,2)` values are forbidden.

Consequently, if an ABF/GG trigger uses `A` close slopes and `L_a(r)` contains
a subset `S` with

```text
|S| >= ceil(A/(b-1)),        lambda(S) <= b-1,
```

then code-direction line-decodability fails under the same size condition on
`C`: choose `A` slopes, bucket them over `S` with bucket sizes at most `b-1`,
and extend the shifted assignment greedily.  In this trigger-level form,
line-decodability forces

```text
alpha_b(L_a(r)) < ceil(A/(b-1)).
```

This is the protocol-facing obstruction: the numerator `A=a_LD`, rather than
`|F|`, controls how large an affine cap in an ordinary close list is already
fatal.

Thus, for code-direction received lines, ABF/GG line-decodability with
threshold `b` requires an additional assignment-collinearity theorem for the
ordinary close list of the base word `r`.  In particular, if some base word has
`m` close codewords with

```text
max(ceil(|F|/m), m) < b,
```

then the code fails the ABF/GG collinearity conclusion on a line whose
support-wise `LD_sw` contribution is zero.

Equivalently, for any nonvacuous ABF/GG threshold `2 <= b <= |F|`, put

```text
s_b = ceil(|F|/(b-1)).
```

For every `b`, ABF/GG `(delta,a_LD,b)` line-decodability with
`a_LD <= |F|` forces

```text
alpha_b(L_a(r)) < s_b
```

for every base word `r`.  Otherwise choose a `b`-affine cap
`S subset L_a(r)` of size `s_b`, partition the full field into `s_b` nonempty
buckets of size at most `b-1`, and use the code-direction assignment above.

In the smaller-field regime `s_b <= b-1`, this cap condition collapses to an
ordinary close-list size condition.  Then ABF/GG `(delta,a_LD,b)`
line-decodability with
`a_LD <= |F|` forces every base word `r` to have fewer than `s_b` ordinary
close codewords at the same agreement threshold.  Otherwise, choose `s_b` of
them, use a balanced `s_b`-bucket assignment, and every affine code-line hits
at most

```text
max(ceil(|F|/s_b), s_b) <= b-1
```

slopes.  This violates the required `b`-slope collinearity conclusion while
the code-direction received line still contributes nothing to `LD_sw`.
The pigeonhole half above shows this threshold is exact for code-direction
lines: below `s_b`, every full-field assignment is forced to contain a
`b`-point affine graph.

Thus, in the regime `s_b <= b-1`, code-direction lines have the following exact
full-field criterion:

```text
Every full-field close-codeword assignment on every line r+gamma v, v in C,
has a b-slope affine-code-line agreement
```

if and only if

```text
|L_a(r)| < s_b
```

for every base word `r`.  The forward implication is the balanced-bucket
obstruction applied to any `s_b` close codewords of a violating base word.  The
reverse implication is the pigeonhole argument applied to the shifted
assignment `gamma -> U(gamma)-gamma v`.

## Construction

Let `D={0,...,7}` in `F_13`, let `C=RS[F_13,D,3]`, and put

```text
p0(x) = 0,             p1(x) = x(x-1).
```

The codewords `p0` and `p1` agree at `x=0,1`.  Define a received word `r` by

```text
r = p0 on {0,1,2,3,4},
r = p1 on {0,1,5,6,7}.
```

This is well-defined, and both `p0` and `p1` agree with `r` on exactly five
domain points.  Let `v(x)=x`, a nonzero codeword in `C`, and consider the
received line

```text
ell_gamma = r + gamma v.
```

This line is nonconstant and is not contained in `C`, since `r` is not a
codeword: any degree-`<3` polynomial agreeing with `r` on `{0,1,2,3,4}` would
be `p0`, but `r(5)=p1(5) != 0`.  Every large support on which a line point is
code-explained also explains the base `r`: subtract the already code-explained
direction `gamma v`.  The same support explains the direction `v` because
`v in C`.  Hence this line has no support-wise noncontained slopes at agreement
`5`; its contribution to `LD_sw(C,5)` is `0`.

Now define an adversarial close-codeword assignment on the slopes:

```text
U(gamma) = p0 + gamma v for gamma in {0,1,2,3,4,5},
U(gamma) = p1 + gamma v for gamma in {6,7,8,9,10,11,12}.
```

Every assigned codeword is `delta=3/8` close to the corresponding line point
`r + gamma v`.  Thus the ABF/GG line-decoding premise is triggered for any
numerator `a_LD <= 13`.

However, no code-line `u0 + gamma u1` agrees with this assignment on nine
slopes.  This is the `m=2` bucket obstruction above with bucket sizes `6` and
`7`; the exact maximum is `max(ceil(13/2),2)=7 < 9`.  The list-size corollary
also applies directly: for `b=9`, one has `s_b=ceil(13/8)=2`, and the base
word `r` has exactly the two close codewords `p0,p1`.  This two-point set is a
`9`-affine cap in the code space, so it also saturates the affine-cap
obstruction threshold.  If the close list had size `1` instead, every
full-field assignment on a code-direction line would have a constant shifted
value on all `13` slopes, hence would satisfy the `9`-slope collinearity
conclusion by pigeonhole.

The trigger-level obstruction is already visible at `A=9`, not only at the
full-field trigger `A=13`.  Assign four of nine close slopes to `p0` and five
to `p1`; this partial shifted assignment has no nine-point affine graph.  Since
`|C|=13^3 > binom(13,2)`, the greedy extension lemma fills the remaining four
slopes with codewords while preserving the absence of nine collinear graph
points.  Thus the same example also refutes the ABF/GG implication with
trigger numerator `a_LD=9`.

## Consequence for M2

The parameter-match note proves the useful forward implication:

```text
ABF/GG (delta,a_LD,n+1) line-decodable
  => LD_sw(C,ceil((1-delta)n)) <= a_LD
  => epsilon_mca(C,delta) <= a_LD/|F|.
```

The structural lemmas, exact shifted-assignment reduction, and finite
Reed-Solomon instance show the converse fails for a conceptual reason, not a
numerical accident.  A genuine M2 theorem therefore needs a separate
assignment-collinearity input if it aims to prove ABF/GG line-decodability;
residue-line packing or `LD_sw` alone proves the MCA numerator, not the
stronger close-codeword assignment theorem.  The `m`-bucket bound also explains
what such an input must control: affine-graph incidence inside ordinary close
lists, not only the size of the support-wise bad-slope set.  The direction-coset
invariance explains why residue-line packing naturally quotients by codeword
directions, while ABF/GG line-decodability remains sensitive to the shifted
assignment.  In the
`b=n+1` convention, the code-direction obstruction demands ordinary close-list
control at the scale `ceil(|F|/n)` whenever `ceil(|F|/n) <= n`; below that
scale, code-direction lines are controlled by pigeonhole.  In this full-field
code-direction slice, that close-list threshold is not only necessary but
sufficient.  Outside this smaller-field regime the necessary condition becomes
an affine-cap condition inside the ordinary close list: every subset large
enough to balance the field into buckets of size `< b` must itself contain
`b` points on a nonconstant affine line in the code space.  With the greedy
extension lemma, the same affine-cap condition applies at the actual
line-decoding trigger numerator `a_LD` whenever the code space has more than
`binom(|F|,2)` codewords.

This does not contradict the ABF/GG theorem.  It only rules out a possible
shortcut from support-wise MCA bounds back to line-decodability.

## Verifier

The script
`experimental/scripts/verify_m2_ldsw_line_decoding_separation.py` enumerates
the finite RS code, all supports of size at least five, and all code-lines:

```bash
python3 experimental/scripts/verify_m2_ldsw_line_decoding_separation.py
python3 experimental/scripts/verify_m2_ldsw_line_decoding_separation.py --json
```
