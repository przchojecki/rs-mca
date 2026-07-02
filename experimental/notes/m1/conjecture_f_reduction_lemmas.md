# Conjecture F Reduction Lemmas

- **Status:** PROVED / EXPERIMENTAL verifier.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap links:** `experimental/notes/roadmaps/proof_sketch/s3b_iii_1_divisor_pencil_incidence.md`,
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md`.
- **Verifier:** `experimental/scripts/verify_conjecture_f_reductions.py`.
- **Artifact:** `experimental/data/certificates/conjecture-f-reductions/conjecture_f_reductions_toy.json`.

This note records three elementary reductions around the fiber-rigidity
statement called Conjecture F in the proof sketch.  They do not prove the
primitive core.  Their role is to remove two paid structures from the statement
and to settle the dimension-one base case.

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

## Verification

The verifier checks these lemmas over `F_97` with `H = mu_16`:

```bash
python3 experimental/scripts/verify_conjecture_f_reductions.py
python3 experimental/scripts/verify_conjecture_f_reductions.py --emit
```

It exhaustively checks the common-GCD and quotient-pullback identities in the
toy parameters used by the script, and tests the voting bound on deterministic
random gcd-trivial pencils.  The verifier is supporting evidence only; the
proofs above are the mathematical content.
