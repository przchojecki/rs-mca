# F1 Monic-Anchor Base-Core Reduction

## Claim

Let `B = F_p`, let `F/B` be a quadratic extension with Frobenius involution
`tau`, and let `D subset B` have size `n`. Fix integers

```text
k >= 1,        sigma >= 1,        a = k + sigma <= n.
```

Let `E in F[X]` be monic of degree `sigma` and nonzero on `D`. Let
`W in B[X]` be monic of degree `a`, and let `A,N in F[X]` have degree
`< sigma`, with `[N]_E != 0` in `F[X]/(E)`. Consider the extension-valued
line

```text
u_z(x) = (W(x) - A(x) - z N(x)) / E(x),        z in F.
```

For an `a`-subset `S subset D`, write

```text
L_S(X) = product_{s in S} (X - s).
```

Put

```text
hatE = lcm(E, E^tau).
```

Then `hatE in B[X]`, `deg hatE <= 2 sigma`, and the natural map

```text
iota: B[X]/(hatE) -> F[X]/(E),        [H]_{hatE} |-> [H]_E
```

is injective.

Define the locator readout and affine slope target

```text
I_hat = { [L_S]_{hatE} : S subset D, |S| = a },

P_{A,N}
  = { y in B[X]/(hatE) :
        [W - A]_E - iota(y) lies in F * [N]_E }.
```

The support-wise MCA-bad slopes of the line `u_z` at radius

```text
delta = 1 - a/n
```

are in bijection with the finite incidence set

```text
I_hat cap P_{A,N}.
```

More explicitly, an `a`-subset `S` supports the slope `z` if and only if

```text
[W - L_S - A]_E = z [N]_E.
```

Whenever this holds, the slope is support-wise noncontained. Moreover, if
`S,S'` both support slopes, then

```text
z_S = z_S'
```

if and only if

```text
[L_S]_{hatE} = [L_{S'}]_{hatE}.
```

Thus the monic-anchor balanced F1 problem reduces exactly to a base-field
locator-readout incidence problem modulo `hatE`, with effective prefix degree
at most `2 sigma`.

## Status

PROVED for the monic-anchor balanced stratum above.

This is not a full solution of F1. The residue-line normal form in
`tex/slackMCA_v3.tex` allows arbitrary anchors `w:D->F`. The proof below uses
the monic polynomial identity `W - L_S`, so the arbitrary-anchor balanced gap
remains open.

## Parameters

```text
q_gen  = |B| = p
q_line = |F| = p^2
t      = deg E = sigma
a      = k + sigma
delta  = 1 - a/n
eta    = sigma/n
```

The result is finite-length and does not assume an asymptotic reserve. Its
ledger role is structural: it identifies the exact base-field readout that a
repaired above-reserve F1 theorem must bound in this monic-anchor stratum.

## Existing Paper Dependency

This is a specialization of the residue-line framework around
`tex/slackMCA_v3.tex` `def:residue` and `thm:normalform`.

It also corrects the over-strong conjugate-pairing heuristic recorded in the
F1 audit bundle: `E notin B[X]` need not imply `gcd(E,E^tau)=1`; mixed
base-times-extension denominators exist and are handled by `hatE`.

## Proof

First, `hatE` is fixed by `tau` because it is the monic least common multiple
of `E` and `E^tau`. Hence `hatE in B[X]`, and
`deg hatE <= deg E + deg E^tau = 2 sigma`.

We next prove injectivity of `iota`. Suppose `H in B[X]` maps to zero in
`F[X]/(E)`. Then `E` divides `H` in `F[X]`. Applying `tau` to the divisibility
relation gives `E^tau | H`. Hence `hatE | H`, so `[H]_{hatE}=0`.

Now fix `z in F` and suppose `u_z` agrees on a set `T subset D` with a
degree-`<k` polynomial `P`. Then

```text
M(X) = W(X) - A(X) - z N(X) - E(X)P(X)
```

vanishes on `T`. The polynomial `M` has degree exactly `a` and is monic:
`W` is monic of degree `a`, while all other terms have degree `< a`.
Therefore `|T| <= a`. If `|T| = a`, then `M = L_T`, because both are monic
degree-`a` polynomials with the same `a` roots. Rearranging gives

```text
W - L_T - A = z N + E P,
```

and therefore

```text
[W - L_T - A]_E = z [N]_E.
```

Conversely, if this residue identity holds for an `a`-subset `S`, then
`W-L_S-A-zN` is divisible by `E`. The quotient has degree `< k`, since the
numerator has degree `< a = k+sigma` after the leading terms of `W` and `L_S`
cancel. Thus `u_z` is code-explained on `S`.

The slope `z` is unique for a fixed support `S`: if

```text
z [N]_E = z' [N]_E,
```

then `(z-z')[N]_E=0`, and `[N]_E` is a nonzero vector over the field `F`.

It remains to prove noncontainment. Suppose the direction

```text
g(x) = -N(x)/E(x)
```

agrees on an `a`-subset `S` with a degree-`<k` polynomial `G`. Then

```text
E(X)G(X) + N(X)
```

has degree `< a` and vanishes on the `a` points of `S`, so it is identically
zero. This would imply that `E` divides `N`, contradicting `[N]_E != 0` and
`deg N < deg E`. Hence the direction is not explained on `S`; no common
degree-`<k` explanation of the anchor and direction exists on that support.
Every supported slope above is therefore support-wise MCA-bad.

The incidence description now follows. For an `a`-subset `S`, the condition

```text
[W - L_S - A]_E = z [N]_E
```

is equivalent to

```text
[L_S]_{hatE} in P_{A,N},
```

by the definition of `P_{A,N}` and the map `iota`. The previous uniqueness
argument assigns exactly one slope to each such locator readout.

Finally, let `S,S'` be two supporting `a`-subsets. They give the same slope
if and only if

```text
[W - L_S - A]_E = [W - L_{S'} - A]_E,
```

which is equivalent to `E | (L_S - L_{S'})`. Since `L_S-L_{S'} in B[X]`,
applying `tau` gives `E^tau | (L_S-L_{S'})`. Thus
`hatE | (L_S-L_{S'})`, i.e.

```text
[L_S]_{hatE} = [L_{S'}]_{hatE}.
```

The converse is immediate because `E | hatE`. This proves the stated
bijection between bad slopes and `I_hat cap P_{A,N}`.

## Frobenius-Core Corollary

Assume now that `E` is squarefree. Let

```text
G = gcd(E, E^tau),        E_1 = E/G.
```

Then `G in B[X]`, `gcd(E_1,E_1^tau)=1`, and

```text
hatE = G E_1 E_1^tau,
deg hatE = deg G + 2 deg E_1 <= 2 sigma.
```

In particular, the fully Frobenius-stable case is exactly `E=G in B[X]`.
A genuinely extension-valued denominator may still have a nontrivial base
core `G`; the conjugate-free part `E_1` is the part that doubles the effective
base readout dimension.

If additionally `E,A,N,W in B[X]`, then all bad slopes lie in `B`. Indeed,
`[W-L_S-A]_E` and `[N]_E` have representatives in `B[X]` of degree `< sigma`.
If `[W-L_S-A]_E = z[N]_E`, then equality of representatives gives
`z N in B[X]`; since `N` has a nonzero coefficient in `B`, this forces
`z in B`. Thus base-valued balanced lines are subfield-confined and cannot be
charged against the larger denominator `|F|` without an explicit transfer
theorem.

## Arbitrary Finite-Extension Frobenius Closure

The same monic-anchor reduction is not specific to quadratic extensions.  Let
`F/B` be any finite extension of degree `e`, and let `tau(x)=x^|B|` be the
Frobenius generator of `Gal(F/B)`.  For a monic denominator

```text
E in F[X],        deg E = sigma,
```

define its Frobenius closure

```text
hatE = lcm(E, E^tau, E^{tau^2}, ..., E^{tau^{e-1}}).
```

Then `hatE in B[X]`, `deg hatE <= e sigma`, and the natural map

```text
iota: B[X]/(hatE) -> F[X]/(E)
```

is injective.  With the same monic-anchor hypotheses as above, but now over
the extension `F/B`, the bad slopes are again in bijection with

```text
I_hat cap P_{A,N},
```

where

```text
I_hat = { [L_S]_{hatE} : S subset D, |S| = a },

P_{A,N}
  = { y in B[X]/(hatE) :
        [W - A]_E - iota(y) lies in F * [N]_E }.
```

Moreover, two supporting subsets give the same slope if and only if their
locator residues agree modulo `hatE`.  Thus in extension degree `e`, the
balanced monic-anchor stratum increases the base locator-readout degree by at
most a factor of `e`, not by an uncontrolled field-size term.

Proof.  The polynomial `hatE` is fixed by Frobenius because the lcm ranges over
the whole Frobenius orbit of `E`; hence `hatE` has coefficients in `B`.  The
degree bound is immediate from the lcm of `e` degree-`sigma` polynomials.

If `H in B[X]` maps to zero in `F[X]/(E)`, then `E | H` in `F[X]`.  Applying
`tau^i` for every `i` gives `E^{tau^i} | H`, so `hatE | H`; this proves
injectivity of `iota`.

The support and noncontainment proof is identical to the quadratic case:
monicity forces any agreement support of size `a` to have locator `L_S`, and
the direction `-N/E` cannot be explained on an `a`-set by a degree-`<k`
polynomial because `[N]_E != 0`.  If two supporting sets yield the same slope,
then `E | (L_S-L_T)`.  Since `L_S-L_T in B[X]`, all Frobenius conjugates of
`E` divide this difference, hence `hatE | (L_S-L_T)`.  The converse follows
from `E | hatE`.

The quadratic theorem above is the special case `e=2`, where the closure is
`lcm(E,E^tau)`.

## Orbit-Degree Budget

The bound `deg hatE <= e sigma` can be sharpened factor by factor.  Write the
factorization of `E` in `F[X]` as

```text
E = product_f f^{m_f},
```

where `f` ranges over monic irreducible polynomials in `F[X]`, with all but
finitely many multiplicities `m_f` equal to zero.  Frobenius acts by
`f -> f^tau`.  For each Frobenius orbit `O` meeting the support of `E`, put

```text
m_O = max_{f in O} m_f.
```

Then

```text
hatE = product_O product_{f in O} f^{m_O},

deg hatE = sum_O m_O sum_{f in O} deg f.
```

In particular, a squarefree factor whose coefficient field has degree `d` over
`B` contributes orbit length `d`, not the full extension degree `e`.
Base-defined factors have orbit length one.  Repeated factors are charged by
the maximum multiplicity appearing in their Frobenius orbit, as is natural for
an lcm.

Proof.  The Frobenius conjugates of `E` have factorizations

```text
E^{tau^i} = product_f (f^{tau^i})^{m_f}.
```

The lcm takes, for each irreducible factor in a Frobenius orbit, the largest
multiplicity with which any conjugate contributes that factor.  This largest
multiplicity is exactly `m_O`, and the displayed product and degree formula
follow.

## Ledger Impact

This theorem gives the repaired F1 problem a sharper local target:

- the unrestricted numerator-preserving lift is already refuted by the
  `sigma=1` counterexample;
- in the balanced monic-anchor stratum, extension denominators reduce to
  locator incidences modulo the base polynomial `hatE`;
- in extension degree `e`, the extension can increase the effective
  generated-field readout degree by at most a factor of `e`, with the exact
  payment given by the Frobenius-orbit degree budget above;
- the remaining unresolved F1 issue is the arbitrary-anchor balanced stratum
  allowed by the full residue-line normal form.

Consequently, a protocol certificate should not cite an unrestricted
extension-line lift. A defensible replacement must either prove a no-rich-line
bound for the base-core incidence set above, handle arbitrary anchors, or add a
separate balanced-extension residue-line term.
