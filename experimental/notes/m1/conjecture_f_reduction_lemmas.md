# Conjecture F Reduction Lemmas

- **Status:** PROVED / EXPERIMENTAL verifier.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap links:** `experimental/notes/roadmaps/proof_sketch/s3b_iii_1_divisor_pencil_incidence.md`,
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md`.
- **Verifier:** `experimental/scripts/verify_conjecture_f_reductions.py`.
- **Artifact:** `experimental/data/certificates/conjecture-f-reductions/conjecture_f_reductions_toy.json`.

This note records five elementary reductions around the fiber-rigidity
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

## Lemma 5: Projective-Plane Pair-Counting Bound

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
`j`.  If `m > j` distinct points of `H` had the same evaluation line, then
every nonzero locator point on `E` would have more than `j` roots, impossible
for degree at most `j`.  If `m = j`, then the vector subspace underlying `E`
would consist of degree-`<=j` polynomials vanishing on the same `j` points.
That full vanishing subspace is one-dimensional, spanned by the locator of
those `j` roots, contradicting that `E` is a projective line.  Hence every
repeated evaluation line has multiplicity at most `j-1`.

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

## Verification

The verifier checks these lemmas over `F_97` with `H = mu_16`:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```

It exhaustively checks the common-GCD and quotient-pullback identities in the
toy parameters used by the script, tests the voting bound on deterministic
random gcd-trivial pencils, checks the hyperplane-concurrency equivalence on
deterministic random gcd-trivial projective planes, and verifies the
projective-plane pair-counting bound, including forced repeated-line planes.
The verifier is supporting evidence only; the proofs above are the mathematical
content.
