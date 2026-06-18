# M1 Depth-Two Two-Coordinate Projective Euler Target

**Status:** CONDITIONAL / AUDIT.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and homogenize

```text
Q(U,V,Z)=U^2+V^2+UV+UZ+VZ+Z^2.
```

For the two-coordinate core sum

```text
C = sum_{u,v in F_p} mu(u) nu(v) eta(A(u,v)),
```

the compactified Kummer sheaf has finite boundary components

```text
L_1=0,        L_2=0,        Q=0,
```

where `L_1,L_2` are the two active coordinate lines among
`U=0`, `V=0`, and `U+V+Z=0`. Its local monodromy at the line at infinity is

```text
(mu nu eta^2)^{-1}.
```

Thus the projective Euler-characteristic target splits into two cases:

```text
mu nu eta^2 nonprincipal:      chi = 4,
mu nu eta^2 principal:         chi = 2.
```

Consequently, a clean tame normal-crossing Kummer cohomology theorem for
this arrangement should give a `4p` top-dimensional target for the
generic two-coordinate core, and a `2p` top-dimensional target for the
infinity-unramified subfamily `mu nu eta^2=1`. The removed principal
coordinate line remains the separate genus-zero correction bounded by
`3 sqrt(p)` in
`experimental/m1_depth_two_two_coordinate_fiber_reduction.md`.

This note does not replace the current `9p` imported ledger. It identifies
the exact projective Euler calculation that a future conductor proof must
turn into a uniform trace bound.

## Monodromy at Infinity

On `P^2`, the affine core summand is represented by the rational function

```text
L_1^alpha L_2^beta Q^delta / Z^(alpha+beta+2delta).
```

Here `alpha`, `beta`, and `delta` denote the active coordinate and conic
character exponents after passing to a common character order. Therefore the
line at infinity has exponent

```text
-(alpha + beta + 2 delta).
```

Equivalently, its local monodromy is `(mu nu eta^2)^{-1}`. If this character
is principal, the sheaf is unramified at infinity and the infinity line should
not contribute to the ramified boundary coefficient for the core.

## Euler Counts

Over the algebraic closure, the conic `Q=0` is smooth for `p>3`. Each of the
four lines

```text
U=0,        V=0,        U+V+Z=0,        Z=0
```

meets `Q=0` transversely in two geometric points, because the restricted
binary quadratic has discriminant `-3`. The line-line intersections are
distinct and do not lie on the conic.

If infinity is unramified, the ramified boundary relevant to the
top-dimensional Kummer coefficient is two lines and the conic. Its Euler
characteristic is

```text
chi(D) = (2+2+2) - (1+2+2) = 1,
chi(P^2 - D) = 3 - 1 = 2.
```

If infinity is ramified, the boundary is three lines and the conic. Its
Euler characteristic is

```text
chi(D) = (2+2+2+2) - (3+2+2+2) = -1,
chi(P^2 - D) = 3 - (-1) = 4.
```

These two numbers are the expected top-dimensional Betti coefficients in a
clean middle-extension calculation.

## Relation to Existing Slices

The reciprocal quadratic subcase in
`experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md` lies in the
unramified-infinity class: `nu=mu^{-1}` and `eta^2=1`, so
`mu nu eta^2=1`. Its proved core bound `2p+2 sqrt(p)` matches the
Euler target up to the lower-order genus-zero term.

The whole infinity-unramified class is now isolated in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`. It
proves the same `2p+2 sqrt(p)` core bound whenever `mu nu eta^2=1`, using a
ratio substitution and a reciprocal-variable quadratic sum.

For nonquadratic reciprocal slices, infinity is usually ramified and the
same ratio-variable note proves the generic `4p` core bound directly. More
projectively, if any two of the three line monodromies
`mu`, `nu`, `(mu nu eta^2)^(-1)` are reciprocal, an affine chart reduces the
core to that reciprocal lemma. Hence the remaining `chi=4` problem is the
case where all three line monodromies are nonprincipal and no pair is
reciprocal.

After the projective equal-pair ledger is also removed, the asymmetric wall
has pairwise distinct line monodromies as well.  Its next normal-crossing
dense-edge obstruction is line-conic resonance: one of

```text
mu eta = 1,        nu eta = 1,
lambda eta = 1,        lambda=(mu nu eta^2)^(-1).
```

The depth-two lift-window ledger now counts this submass exactly.  Removing
it leaves the `C_2^anr` subwall, where every dense edge of the line/conic
normal-crossing divisor has nontrivial local monodromy.  This is the clean
form of the remaining `chi=4` conductor target; the line-conic-resonant
asymmetric terms are a smaller residual slice.  That slice is now reduced in
`experimental/m1_depth_two_line_conic_resonance_reduction.md`: a
line-conic-resonant core is exactly a Mellin transform of a one-dimensional
quadratic-fiber trace family, with candidate singular support contained in
`{0,-1,2,3,infinity}`.

The finite verifier

```bash
python3 experimental/verify_m1_kummer_divisor_geometry.py
```

checks the projective line/conic incidence and the two-coordinate Euler
targets on representative primes.
