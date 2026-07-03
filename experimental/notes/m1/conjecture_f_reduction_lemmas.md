# Conjecture F Reduction Lemmas

- **Status:** PROVED / EXPERIMENTAL verifier.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap links:** `experimental/notes/roadmaps/proof_sketch/s3b_iii_1_divisor_pencil_incidence.md`,
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md`.
- **Verifier:** `experimental/scripts/verify_conjecture_f_reductions.py`.
- **Artifact:** `experimental/data/certificates/conjecture-f-reductions/conjecture_f_reductions_toy.json`.

This note records eighteen elementary reductions around the fiber-rigidity
statement called Conjecture F in the proof sketch.  They do not prove the
primitive core.  Their role is to remove two paid structures from the statement
to settle the dimension-one base case, and to restate the remaining primitive
core as a hyperplane-arrangement incidence problem.

## Setup

Let `K` be a field and let `H` be a finite subset of `K`.  Write

```text
P_H(X) = prod_{h in H} (X-h).
```

For `j <= |H|`, let

```text
D_j(H) = { monic squarefree degree-j divisors of P_H }.
```

Equivalently, `D_j(H)` is the set of locators

```text
L_S(X) = prod_{h in S} (X-h),       S subset H, |S| = j.
```

The Conjecture F core asks for polynomial bounds on intersections of `D_j(H)`
with linear projective spaces in locator-coefficient space, after tangent
common-divisor and quotient-pullback structures have been removed.

## Lemma 1: Common-GCD Reduction

Let `P` be a projective linear space of polynomials of degree at most `j`.
Let

```text
E = P cap D_j(H)
```

and suppose all locators in `E` are divisible by a fixed monic divisor `G` of
`P_H`, with `w = deg G`.  Let `H_G` be the roots of `G`, and put
`H' = H \ H_G`.

Then division by `G` gives an injection

```text
E  ->  D_{j-w}(H')
L  ->  L/G.
```

Moreover the image is contained in the intersection of `D_{j-w}(H')` with a
linear projective space of dimension at most `dim P`, namely the projectivized
image of

```text
P cap G K[X]_{<= j-w}
```

under the linear division map `GQ -> Q`.

**Proof.**  Every `L in E` is a squarefree divisor of `P_H` and is divisible by
`G`, so `L/G` is a monic squarefree divisor of `P_H/G`, of degree `j-w`.  The
map is injective because multiplication by `G` recovers `L`.  The set of
polynomials in `P` divisible by `G` is a linear subspace: divisibility by a
fixed polynomial is the kernel of the remainder map modulo `G`.  Division by
`G` is linear on this subspace, so its projective image has dimension at most
`dim P`.

This proves that a deep common divisor is not a separate Conjecture F case: it
reduces to a smaller divisor set, and the removed roots are precisely the
tangent/common-error structure in the proof sketch.

## Lemma 2: Quotient-Pullback Scale Recursion

Assume now that `H = mu_n` is the group of `n`-th roots of unity in `K`, with
`char(K)` not dividing `n`.  Let `M | gcd(n,j)` and write `H_M = mu_{n/M}`.
The pullback map

```text
iota_M : K[Y]_{<= j/M} -> K[X]_{<= j}
iota_M(g)(X) = g(X^M)
```

is linear and maps `D_{j/M}(H_M)` bijectively onto the `M`-periodic stratum of
`D_j(H)`, meaning the locators whose root sets are unions of fibers of

```text
mu_n -> mu_{n/M},       x -> x^M.
```

Consequently, for any projective linear space `P` in degree-`j` locator space,

```text
P cap iota_M(D_{j/M}(H_M))
```

is linearly isomorphic to

```text
iota_M^{-1}(P) cap D_{j/M}(H_M),
```

where `iota_M^{-1}(P)` is a projective linear space of dimension at most
`dim P` in the smaller locator space.

**Proof.**  Because `char(K)` does not divide `n`, the map `x -> x^M` from
`mu_n` to `mu_{n/M}` has fibers of size `M`.  If
`g(Y)=prod_{y in T}(Y-y)`, then

```text
g(X^M) = prod_{y in T} (X^M-y)
```

has as its roots exactly the union of the `M`-element fibers above `T`.  This
is a squarefree divisor of `X^n-1` of degree `M|T|=j`.  Conversely any
locator whose root set is a union of these fibers descends uniquely to the
locator of the corresponding subset of `mu_{n/M}`.  Linearity of `iota_M` is
coefficientwise, and the preimage of a projective linear space under a linear
map is linear.

Thus quotient-periodic points also reduce to a smaller instance; the hard
statement can be phrased on the primitive, non-pullback stratum.

## Lemma 3: Dimension-One Voting Bound

Let `P = P(span(L_0,L_1))` be a projective line of polynomials of degree at
most `j`.  Assume `P` is gcd-trivial on `H`, i.e. for every `h in H` the
evaluation vector

```text
(L_0(h), L_1(h))
```

is nonzero.  Then

```text
#(P cap D_j(H)) <= floor(|H|/j).
```

For an affine parametrization `L_0 + z L_1`, the same bound holds after adding
the possible point at infinity separately:

```text
#({L_0+zL_1 : z in K} cap D_j(H)) <= floor(|H|/j) + 1.
```

**Proof.**  Each `h in H` votes for the unique projective parameter
`[a:b] in P^1` for which

```text
a L_0(h) + b L_1(h) = 0.
```

Uniqueness is exactly the gcd-trivial assumption.  There are `|H|` votes in
total.  Every member of `P cap D_j(H)` has exactly `j` distinct roots in `H`,
so it receives exactly `j` votes.  Hence the number of such members is at most
`floor(|H|/j)`.

This proves the dimension-one primitive Conjecture F case with a linear bound.
The first genuinely open primitive case is therefore dimension at least two.

## Lemma 4: Hyperplane-Concurrency Reformulation

Let `W <= K[X]_{<= j}` be a nonzero vector space and let `P(W)` be its
projectivization.  For each `h in H`, define the evaluation subspace

```text
E_h = { [L] in P(W) : L(h)=0 }.
```

If no `h in H` is a common root of all members of `W`, then every `E_h` is a
proper hyperplane in `P(W)`.  In this gcd-trivial case,

```text
P(W) cap D_j(H)
```

is exactly the set of projective points of `P(W)` lying on at least `j` of the
hyperplanes `E_h`.

Equivalently, after Lemmas 1 and 2 remove common-divisor and quotient-pullback
structure, the primitive Conjecture F problem is a `j`-fold concurrency problem
for the arrangement of evaluation hyperplanes on `P(W)`.

**Proof.**  Since no `h` is a common root, the evaluation functional
`L -> L(h)` is not identically zero on `W`, so `E_h` is a proper hyperplane.
For any nonzero `L in W`, the number of hyperplanes containing `[L]` is
exactly

```text
#{h in H : L(h)=0}.
```

If `[L]` lies in `P(W) cap D_j(H)`, then `L` is a scalar multiple of a
degree-`j` squarefree divisor of `P_H`, so it has exactly `j` roots in `H` and
lies on exactly `j` of the `E_h`.  Conversely, if `[L]` lies on at least `j`
of the `E_h`, then `L` has at least `j` distinct roots in `H`.  But
`deg L <= j` and `L` is nonzero, so it has exactly `j` roots and is a scalar
multiple of their locator.  Thus `[L]` lies in `D_j(H)`.

## Lemma 5: Vanishing-Flat Dimension Bound

Let `W <= K[X]_{<= j}` be a vector space and let `T subset H` have size `m`.
Define

```text
W(-T) = { L in W : L(t)=0 for every t in T }.
```

Then

```text
dim_K W(-T) <= j+1-m.
```

Equivalently, if `P(W(-T))` is nonempty, its projective dimension is at most
`j-m`.

**Proof.**  Let

```text
L_T(X)=prod_{t in T}(X-t).
```

Every polynomial in `W(-T)` is divisible by `L_T`, because the points of `T`
are distinct.  Division by `L_T` injects `W(-T)` into `K[X]_{<= j-m}`, whose
dimension is `j+1-m`.

This bound is sharp for the full space `W=K[X]_{<=j}`.  It is the local
dimension obstruction behind the repeated-line step in Lemma 6: if `m` domain
points induce the same evaluation hyperplane on a projective plane, then the
line underlying that hyperplane is contained in `W(-T)`, so `2 <= j+1-m` and
therefore `m <= j-1`.

## Lemma 6: Projective-Plane Pair-Counting Bound

Keep the hypotheses of Lemma 4 and assume additionally that `dim P(W)=2`.
Then

```text
#(P(W) cap D_j(H)) <= binom(|H|,2) / (j-1).
```

If the evaluation lines `E_h` are pairwise distinct, the sharper simple-line
bound holds:

```text
#(P(W) cap D_j(H)) <= binom(|H|,2) / binom(j,2).
```

**Proof.**  For a point `p in P(W)`, let `m(p)` be the number of evaluation
lines passing through it, counted with multiplicity in `H`.

First note that no projective line `E` can occur with multiplicity at least
`j`.  If `m` distinct points of `H` have the same evaluation line, then the
vector subspace underlying `E` lies in `W(-T)` for a set `T` of size `m`.
Since that vector subspace has dimension `2`, Lemma 5 gives `2 <= j+1-m`, so
`m <= j-1`.

Group the evaluation lines by equality, with multiplicities `a_i`.  For any
point lying on groups whose total multiplicity is at least `j`, the number of
unordered pairs of roots drawn from two distinct line-groups through that point
is

```text
sum_{r<s} a_r a_s.
```

Because each `a_i <= j-1`, this cross-pair count is at least `j-1`: the
minimum occurs by placing `j-1` roots in one line-group and `1` in another.
Each unordered pair of roots from distinct line-groups determines exactly one
intersection point of the two corresponding projective lines, so these
cross-pair charges are disjoint over high-incidence points.  The total number
of unordered root-pairs is at most `binom(|H|,2)`, giving

```text
# {p : m(p) >= j} <= binom(|H|,2)/(j-1).
```

Lemma 4 identifies this high-incidence set with `P(W) cap D_j(H)`.

In the pairwise-distinct case all `a_i` are `1`.  Then every high-incidence
point carries at least `binom(j,2)` line-pairs, and the sharper simple-line
bound follows from

```text
sum_p binom(m(p),2) = binom(|H|,2).
```

Thus the primitive dimension-two Conjecture F case is polynomial for arbitrary
gcd-trivial projective planes.  Higher-dimensional primitive intersections are
the first remaining incidence-theoretic core.

## Corollary 6A: Twin-Line Decomposition in Projective Planes

Keep the hypotheses of Lemma 6.  Group the domain points by equality of their
evaluation lines:

```text
h ~ h'    <=>    E_h = E_{h'} in P(W)^*.
```

Call a class of size at least two a **twin class**.  If
`C subset H` is a twin class, then every locator point
`[L] in P(W) cap D_j(H)` either contains all roots of `C` or none of them.
Consequently the `C`-containing subfamily has a common divisor

```text
G_C(X)=prod_{h in C}(X-h)
```

and, after division by `G_C`, injects into a projective line section of
`D_{j-|C|}(H\C)`.  It is therefore paid by the common-GCD reduction followed
by the dimension-one voting bound.

The residual subfamily avoiding all twin classes has the sharp simple-line
pair bound

```text
# residual <= binom(s,2) / binom(j,2),
```

where `s` is the number of singleton evaluation-line classes.

**Proof.**  If `E_h=E_{h'}`, then the two evaluation functionals on `W` are
proportional.  Hence for every `L in W`,

```text
L(h)=0    <=>    L(h')=0.
```

The same argument applies to every member of a twin class `C`: a projective
point of `P(W)` lies on the shared evaluation line if and only if it vanishes
at every root of `C`.  Thus any divisor point meeting `C` is divisible by
`G_C`, and division by `G_C` is exactly Lemma 1.  Since imposing the shared
evaluation line is one linear condition on a projective plane, the subspace of
`W` divisible by `G_C` has projective dimension at most one; Lemma 3 controls
the reduced line section, after removing any further common roots.

If a divisor point avoids every twin class, all of its `j` roots lie on
pairwise distinct singleton evaluation lines.  The point is therefore charged
by at least `binom(j,2)` unordered pairs of singleton lines.  Two distinct
projective lines in a plane meet in exactly one point, so these charges are
disjoint across residual divisor points.  There are only `binom(s,2)` singleton
line-pairs, giving the displayed bound.

This is the QF.4 skeleton used by the roadmap: simple arrangements are handled
by the sharp pair count, while repeated-line violations are not new primitive
mass; they are common-divisor charts one degree lower.

The standalone packet
`experimental/notes/m1/conjecture_f_dim2_skeleton.md` records this as the DAG
node `f_dim2_skeleton` and adds an exhaustive `F_17` degree-three replay over
all projective planes.

## Corollary 6B: Sparse-Dependence Descent

Let `W <= K[X]_{<=j}` have projective dimension `d`, and let
`T subset H` have size `w`.  Suppose the evaluation functionals on `T` have a
full-support linear dependence on `W`: there are nonzero scalars
`lambda_t`, `t in T`, such that

```text
sum_{t in T} lambda_t L(t) = 0          for every L in W.
```

Then every locator point `[L] in P(W) cap D_j(H)` with at least `w-1` roots in
`T` contains all roots of `T`.  Consequently the `T`-containing branch has a
common divisor

```text
G_T(X)=prod_{t in T}(X-t)
```

and division by `G_T` injects it into

```text
P(W(-T)/G_T) cap D_{j-w}(H\T).
```

If `rho` is the rank of the `T`-evaluation map on `W`, then `rho <= w-1` and

```text
dim P(W(-T)/G_T) = d-rho
```

whenever the branch is nonempty.  Hence the quantity `j-d` drops by

```text
w-rho >= 1.
```

After removing the `T`-containing branch, every residual locator contains at
most `w-2` roots of `T`.

**Proof.**  If `L` vanishes at all roots of `T` except possibly `t0`, the
displayed dependence reduces to

```text
lambda_{t0} L(t0)=0.
```

Since `lambda_{t0}` is nonzero, `L(t0)=0`.  Thus any locator containing
`w-1` roots of `T` contains all of `T`.  The all-contained branch is then
exactly a common-GCD branch with divisor `G_T`, so Lemma 1 gives the injection
after division.

The vector space `W(-T)` is the kernel of the `T`-evaluation map on `W`, so
its vector dimension is `dim W-rho`.  Division by `G_T` is a linear injection,
and therefore the reduced projective dimension is `d-rho`.  The assumed
linear dependence gives `rho <= w-1`, which yields

```text
(j-w)-(d-rho) = (j-d) - (w-rho) <= (j-d)-1.
```

The residual assertion is the contrapositive of the closure statement.

This is the sparse descent rung used after the QF.4 twin split: a low-support
dual relation is not a new primitive source by itself.  Its near-saturated
locators are paid by common-GCD descent, and the remaining locators have a
strictly smaller overlap with that sparse support.

## Corollary 6C: Dual-Distance Moment Frame

Let `W <= K[X]_{<=j}` have vector dimension `d+1`, and let

```text
ev_H(W) = { (L(h))_{h in H} : L in W } <= K^H.
```

Write `C_W^perp` for the dual code of `ev_H(W)`, and let `w_*(W,H)` be the
minimum support size of a nonzero word of `C_W^perp`, with `w_* = infinity`
if the dual code is zero.

The low-weight dual words are exactly the degeneracies used above:

- `w_*=1` occurs precisely when some `h in H` is a common root of `W`;
- a support-two dual word on `{h,h'}` occurs precisely when the evaluation
  functionals at `h` and `h'` are proportional on `W`, i.e. when `h,h'`
  form a twin evaluation-line class;
- a support-`w` dual word with all coefficients nonzero is exactly the
  sparse-dependence input of Corollary 6B.

If `w_*(W,H)>r`, then every `T subset H` with `|T|<=r` imposes independent
conditions on `W`:

```text
dim W(-T) = dim W-|T|.
```

Consequently, for `0<=r<=min(d,j)` and

```text
E = P(W) cap D_j(H),
```

the `r`-th containment moment satisfies

```text
#E binom(j,r)
  <= binom(|H|,r) binom(|H|-r,d-r).
```

Equivalently,

```text
#E <= binom(|H|,r) binom(|H|-r,d-r) / binom(j,r).
```

In particular, if `w_*(W,H)>d`, then

```text
#E <= binom(|H|,d) / binom(j,d).
```

Thus when `j >= theta |H|`, `d <= j/2`, and `d=O(log |H|)`, a dual-distance gap
`w_*>d` gives the polynomial bound

```text
#E <= (2/theta)^d.
```

**Proof.**  A vector `lambda in K^H` lies in `C_W^perp` if and only if

```text
sum_{h in H} lambda_h L(h)=0       for every L in W.
```

Restricting the support of `lambda` gives exactly a linear dependence among
the evaluation functionals on that support.  Support `1` means the corresponding
functional is zero on `W`, hence a common root.  Support `2` means two
nonzero evaluation functionals are proportional, unless one of them is already
the support-one case.  Full-support words of size `w` are precisely the input
of Corollary 6B.

If `w_*>r`, no subset of size at most `r` carries a nontrivial dependence, so
the evaluation map on every such subset has full rank.  This proves
`dim W(-T)=dim W-|T|`.

Now double-count pairs `(L,T)` with `[L] in E` and `T` an `r`-subset of the
root set of `L`.  Each locator contributes exactly `binom(j,r)` pairs.  For a
fixed `T`, the `T`-containing branch lies in `P(W(-T))`; after division by
`G_T=prod_{t in T}(X-t)`, Lemma 1 and Corollary 8 bound it by
`binom(|H|-r,d-r)`, because `P(W(-T))` has projective dimension `d-r`.
Summing over all `binom(|H|,r)` choices of `T` gives the displayed moment
bound.  Taking `r=d` gives the final exact inequality.  If `j>=theta |H|` and
`d <= j/2`, then

```text
binom(|H|,d)/binom(j,d)
  <= (|H|/(j-d+1))^d
  <= (2/theta)^d.
```

This is the QF.6 dual-distance frame: common roots, twins, and sparse
relations are the low-weight dual obstructions; once they are absent up to
rank `r`, the remaining spread regime has an explicit `r`-wise containment
moment.

## Lemma 7: Fixed-Dimension Incidence Bound

Let `W <= K[X]_{<=j}` have vector dimension `d+1`, and assume `W` is
gcd-trivial on `H`.  Then

```text
#(P(W) cap D_j(H)) <= binom(|H|,d).
```

Consequently every fixed projective dimension `d` satisfies Conjecture F with
exponent at most `d`.  The remaining primitive core is necessarily a
dimension-growing problem.

**Proof.**  Let `[L] in P(W) cap D_j(H)`, and let `R subset H` be the `j`
roots of `L`.  Since `L` spans a line in `W(-R)`, Lemma 5 gives

```text
1 <= dim W(-R) <= j+1-j = 1.
```

Thus `dim W(-R)=1`.  Since `dim W=d+1`, the evaluation equations
`M(r)=0`, `r in R`, have rank `d` on `W`.  Hence some `d`-element subset
`T subset R` already has rank `d`; equivalently, the `d` evaluation
hyperplanes for `T` intersect in the single projective point `[L]`.

Choose, for each `[L]`, the lexicographically first such independent
`d`-subset of its root set.  This choice is injective: if two locator points
chose the same independent `T`, both would lie in the one-point intersection
of the evaluation hyperplanes indexed by `T`.  Therefore the number of locator
points is at most the number of `d`-subsets of `H`.

For `d=j` and `W=K[X]_{<=j}`, the bound is sharp: every `j`-subset of `H`
gives its locator.

## Corollary 8: Fixed Dimension After Common-Root Removal

Let `W <= K[X]_{<=j}` have vector dimension `d+1`, and let

```text
C = {h in H : L(h)=0 for every L in W}
```

be the common root set of `W` on `H`, with `c=|C|`.  Then

```text
#(P(W) cap D_j(H)) <= binom(|H|-c,d).
```

**Proof.**  Let

```text
G_C(X)=prod_{h in C}(X-h),       H' = H \ C.
```

Every member of `W` is divisible by `G_C`, and division gives a vector-space
isomorphism

```text
W  ->  W' <= K[X]_{<= j-c}.
```

By maximality of `C`, the reduced space `W'` is gcd-trivial on `H'`.  Also,
division by `G_C` maps `P(W) cap D_j(H)` injectively into
`P(W') cap D_{j-c}(H')`.  Applying Lemma 7 to `W'` and `H'` gives the bound.

This packages the common-divisor/tangent branch and the fixed-dimensional
primitive branch into one reusable statement: after stripping common roots, all
fixed-dimensional fibers are polynomially bounded.

## Corollary 9: Fixed Dimension on Quotient-Pullback Strata

Assume `H=mu_n`, `char(K)` does not divide `n`, and `M | gcd(n,j)`.  Write
`H_M=mu_{n/M}` and `iota_M(g)(X)=g(X^M)`.  Let `W <= K[X]_{<=j}` have
projective dimension `d`, and define the descended quotient space

```text
W_M = iota_M^{-1}(W) <= K[Y]_{<= j/M}.
```

If `W_M` is gcd-trivial on `H_M`, then

```text
#(P(W) cap iota_M(D_{j/M}(H_M))) <= binom(n/M,d).
```

More generally, if `C_M` is the common root set of `W_M` on `H_M`, with
`c=|C_M|`, then

```text
#(P(W) cap iota_M(D_{j/M}(H_M))) <= binom(n/M-c,d).
```

**Proof.**  Lemma 2 identifies the left-hand side with

```text
P(W_M) cap D_{j/M}(H_M).
```

The linear map `iota_M` is injective on `K[Y]_{<=j/M}`, so `dim P(W_M) <= d`.
If `W_M` is gcd-trivial, Lemma 7 gives the first bound.  If `W_M` has common
root set `C_M`, Corollary 8 applied on the quotient domain gives the second
bound.

Thus the quotient-periodic paid branch inherits the same fixed-dimensional
polynomial control after descent.  Conjecture F's genuinely new content is not
in fixed-dimensional tangent or quotient strata; it is in primitive
dimension-growing intersections.

## Corollary 10: Proper Quotient-Union Bound

Keep the hypotheses of Corollary 9, and define the proper quotient-periodic
part of `D_j(mu_n)` by

```text
D_j^{quot}(mu_n) =
  union_{M | gcd(n,j), M>1} iota_M(D_{j/M}(mu_{n/M})).
```

For each such `M`, set

```text
W_M = iota_M^{-1}(W),       d_M = dim P(W_M),
```

and let `c_M` be the number of common roots of `W_M` on `mu_{n/M}`.  Empty
`W_M` contributes zero.  Then

```text
#(P(W) cap D_j^{quot}(mu_n))
  <= sum_{M | gcd(n,j), M>1} binom(n/M-c_M,d_M).
```

In particular, if `dim P(W) <= d`, then the coarser uniform estimate

```text
#(P(W) cap D_j^{quot}(mu_n))
  <= sum_{M | gcd(n,j), M>1} sum_{r=0}^d binom(n/M,r)
```

holds.  For fixed `d`, this is polynomial in `n` with an explicit divisor-sum
constant depending only on the active quotient scales.

**Proof.**  Decompose the proper quotient-periodic locus as the displayed
finite union over `M`.  Corollary 9 bounds the `M`-summand by
`binom(n/M-c_M,d_M)`.  Summing over `M` gives the first estimate; overlaps can
only make the union smaller.  Since `d_M <= d`, the second estimate follows by
bounding each `binom(n/M-c_M,d_M)` by

```text
sum_{r=0}^d binom(n/M,r).
```

This turns the entire fixed-dimensional quotient-paid part into bookkeeping.
After common-root and quotient-union removal, a fixed-dimensional section has
only the primitive incidence problem left; any super-polynomial obstruction to
Conjecture F must therefore come from dimensions growing with the row.

## Corollary 11: Affine Slope-Table Consumer

Let

```text
A = L_0 + V  subset K[X]_{<=j}
```

be an affine family of locator candidates, with `dim V=r`, and put

```text
W = span(L_0,V),       d = dim P(W).
```

Then the number of monic valid locators in the affine table satisfies

```text
#{L in A cap D_j(H)} <= binom(|H|-c,d),
```

where `c` is the number of common roots of `W` on `H`.  In the subgroup case
`H=mu_n`, the proper quotient-periodic part of the affine table additionally
satisfies

```text
#{L in A cap D_j^{quot}(mu_n)}
  <= sum_{M | gcd(n,j), M>1} sum_{s=0}^d binom(n/M,s).
```

**Proof.**  The affine family `A` is contained in the vector space `W`.
Because `D_j(H)` consists of monic locators, each affine hit is a single
projective point of `P(W)`; two different affine parameters cannot represent
the same monic polynomial.  Corollary 8 therefore bounds `A cap D_j(H)` by
the common-root reduced projective bound for `P(W)`.

For the quotient-periodic part, apply Corollary 10 to the same projective
space `P(W)` and then restrict back to the affine subset.  Restriction can
only decrease the count.

This is the form consumed by slope/root-table scripts: an affine chart does
not need a separate Conjecture F argument once the projectivized chart has
fixed dimension.  The only remaining primitive obstruction must involve
projective dimensions growing with the row.

## Corollary 12: Exponent-Budget Consumer

Let `n=|H|`.  If a projective or affine chart has projective span dimension
`d`, then the common-root reduced locator count from Corollaries 8 and 11 obeys

```text
# <= binom(n-c,d) <= n^d.
```

Thus projective dimension `d` is an explicit `n^d` ledger exponent for the
non-quotient fixed-dimensional part.

In the subgroup case, the proper quotient-union part from Corollary 10 obeys
the coarser but uniform estimate

```text
#(P(W) cap D_j^{quot}(mu_n))
  <= tau(gcd(n,j)) (d+1) n^d,
```

where `tau(g)` is the number of proper quotient scales `M>1` dividing
`g=gcd(n,j)`; empty scales may be omitted.  Equivalently, for an exact `n^B`
ledger it is enough to take

```text
B >= d + log_n(tau(gcd(n,j))(d+1)).
```

**Proof.**  The first inequality is Corollary 8 or Corollary 11, followed by
the elementary bound `binom(n-c,d) <= n^d`.  For quotient-union points,
Corollary 10 gives

```text
sum_{M | gcd(n,j), M>1} sum_{s=0}^d binom(n/M,s).
```

Every summand satisfies `binom(n/M,s) <= n^s <= n^d`, and there are at most
`tau(gcd(n,j))(d+1)` such summands.

This is the form used by final ledger comparisons: once a residual chart has
bounded projective dimension, the required polynomial exponent is explicit.
Any counterexample to an `n^B` Conjecture F consumer with `B` above this budget
must therefore come from dimension-growing primitive charts, not from
fixed-dimensional common-root, quotient, or affine-chart bookkeeping.

## Corollary 13: Johnson-Ball Common-Core Cover

Fix a locator root set `R subset H` with `|R|=j`.  For an integer
`0 <= r <= j`, let

```text
B_r(R) = { T subset H : |T|=j and j-|R cap T| <= r }
```

be the radius-`r` Johnson ball around `R`.  Then

```text
|B_r(R)|
  =
  sum_{d=0}^{min(r,j,|H|-j)}
      binom(j,d) binom(|H|-j,d).
```

Moreover `B_r(R)` is covered by common-root charts:

```text
B_r(R)
  =
  union_{C subset R, |C|=j-r}
      { T subset H : |T|=j and C subset T },
```

Hence

```text
|B_r(R)|
  <=
  binom(j,r) binom(|H|-j+r,r)
  <=
  |H|^{2r}.
```

**Proof.**  A locator at Johnson distance `d` from `R` is obtained by removing
`d` roots of `R` and adding `d` roots from `H\R`, giving the exact sum.  If
`T` has distance at most `r`, then `|R cap T| >= j-r`, so choosing any
`(j-r)`-subset `C` of `R cap T` places `T` in the common-root chart indexed by
`C`.  Conversely every locator containing such a `C` shares at least `j-r`
roots with `R`, so it lies in `B_r(R)`.  For a fixed `C`, the chart size is
`binom(|H|-(j-r),r)=binom(|H|-j+r,r)`, and there are `binom(j,r)` possible
cores.

This corollary is the bridge to the FM1 overlap ledger: FM1 covariance is
supported in a Johnson ball of radius `t-1`, and this ball is a union of
explicit common-root charts.  When `t` is fixed, the entire high-overlap
neighborhood is polynomially priced by common-root accounting; when `t` grows,
this corollary identifies exactly why the remaining problem becomes
dimension-growing rather than fixed-dimensional.

## Corollary 14: FM1 High-Overlap Common-Core Budget

In the FM1 second-moment notation, covariance between locator indicators can
occur only for ordered pairs `(R,T)` with

```text
d(R,T) = j-|R cap T| < t.
```

For each fixed `R`, this high-overlap set is the Johnson ball
`B_{t-1}(R)`.  Hence the number of ordered high-overlap pairs is exactly

```text
binom(n,j)
*
sum_{d=0}^{min(t-1,j,n-j)}
    binom(j,d) binom(n-j,d),
```

and it is bounded by

```text
binom(n,j) binom(j,t-1) binom(n-j+t-1,t-1)
  <=
binom(n,j) n^{2(t-1)}.
```

**Proof.**  This is Corollary 13 applied independently around every center
`R`.  The exact count is the ordered center count `binom(n,j)` times the
radius-`t-1` Johnson ball size.  The displayed upper bound is the common-core
cover from Corollary 13 with `r=t-1`.

This is a ledger statement rather than a new probabilistic inequality.  It
says that, for fixed slack `t`, the whole FM1 covariance support is already
priced by common-root charts with a per-center `n^{2(t-1)}` budget.  Therefore
fixed-slack high-overlap covariance is not part of the primitive Conjecture F
core; the core begins when the effective Johnson radius grows with the row.

## Corollary 15: Polynomial Chart-Atlas Consumer

Let `R subset D_j(H)` be covered by affine charts

```text
A_alpha = L_alpha + V_alpha        (alpha in I),
```

where `V_alpha` is a finite-dimensional vector space of polynomial directions.
Put

```text
W_alpha = span(L_alpha,V_alpha),        d_alpha = dim P(W_alpha),
```

and let `c_alpha` be the number of common roots of `W_alpha` on `H`.  Then

```text
#R <= sum_{alpha in I} binom(|H|-c_alpha,d_alpha).
```

In particular, if `|I| <= A` and `d_alpha <= d` for every chart, then

```text
#R <= A |H|^d.
```

For `H=mu_n`, the proper quotient-periodic part covered by the same atlas
satisfies the coarser ledger bound

```text
#(R cap D_j^{quot}(mu_n))
  <= A tau(gcd(n,j)) (d+1) n^d.
```

Equivalently, if `A <= n^a`, the chart atlas has non-quotient exponent budget

```text
B = a+d,
```

and quotient-union exponent budget

```text
B = a+d+log_n(tau(gcd(n,j))(d+1)).
```

**Proof.**  Apply Corollary 11 to each affine chart and take the union bound.
For the quotient-periodic part, apply the quotient-union estimate from
Corollary 12 chart by chart and again take the union bound.

This is the direct interface for M5/M6 chart decompositions.  A finite or
polynomial-size atlas of bounded projective dimension is already a polynomial
Conjecture F ledger.  Any super-polynomial residual must either require
super-polynomially many charts, growing projective dimension, or a chart family
outside the fixed-dimensional affine model.

## Verification

The verifier checks these lemmas over `F_97` with `H = mu_16`:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```

It exhaustively checks the common-GCD and quotient-pullback identities in the
toy parameters used by the script, tests the voting bound on deterministic
random gcd-trivial pencils, checks the hyperplane-concurrency equivalence on
deterministic random gcd-trivial projective planes, verifies the vanishing-flat
dimension bound, verifies the projective-plane pair-counting bound including
forced repeated-line planes, verifies the twin-line decomposition into
common-GCD line charts plus the sharp simple-line residual, verifies the
sparse-dependence closure/descent rule on forced sparse relation spaces,
verifies the dual-distance moment frame including support-one common-root,
support-two twin, and support-three sparse-dependence degeneracies, and
verifies the fixed-dimension incidence bound on random subspaces plus the
sharp full-space case.  It also verifies the
common-root corollary on forced common-root subspaces and the
fixed-dimensional quotient-pullback consumer, plus the proper quotient-union
bound at `n=16,j=8` across the scales `M in {2,4,8}`.  It also checks the
affine slope-table consumer directly on deterministic random affine charts,
prints the resulting fixed-dimension/quotient-union exponent budgets, checks
the polynomial chart-atlas consumer on deterministic affine atlases, and
checks the Johnson-ball common-core cover both by exact toy enumeration and by
formula on deployed-shape rows.  It also checks the FM1 high-overlap
ordered-pair budget by exact toy enumeration and deployed-shape formulas.  The
verifier is supporting evidence only; the proofs above are the mathematical
content.
