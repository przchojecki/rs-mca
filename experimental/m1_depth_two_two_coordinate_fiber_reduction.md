# M1 Depth-Two Two-Coordinate Fiber Reduction

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard genus-zero multiplicative Weil bound on `P^1`. Let
`p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero. Let `mu`, `nu`,
and `eta` be nonprincipal multiplicative characters. The two-coordinate
mixed term with active coordinates `u,v` and principal coordinate `w` is

```text
S_open = sum_{u,v} mu(u) nu(v) 1_{w!=0} eta(A(u,v)).
```

It decomposes as

```text
S_open = sum_u mu(u) F_{nu,eta}(u) - L_{mu,nu,eta},

F_{nu,eta}(u) = sum_v nu(v) eta(A(u,v)),
L_{mu,nu,eta} = sum_u mu(u) nu(-1-u) eta(-(u^2+u+1)).
```

The line correction satisfies

```text
|L_{mu,nu,eta}| <= 3 sqrt(p).
```

The cases with active coordinate pairs `(u,w)` and `(v,w)` follow by the
symmetry of `A=uv+uw+vw-1` on the plane `u+v+w=-1`.

## Fiber Geometry

For fixed `u`, the fiber trace is a one-variable Kummer sum

```text
F_{nu,eta}(u)=sum_v nu(v) eta(A(u,v)).
```

On `P^1_v`, the zero-pole support is contained in

```text
v=0,        A(u,v)=0,        infinity.
```

The quadratic polynomial `A(u,v)` has discriminant

```text
Delta(u)=-3u^2-2u-3.
```

Thus a generic fiber has at most four support points. The degenerate fibers
with `Delta(u)=0`, and the collision fibers where `A(u,0)=0`, only reduce
the support or merge coefficients; they do not make the summand a character
power because `nu` and `eta` are both nonprincipal. Hence every fixed fiber
has the genus-zero bound

```text
|F_{nu,eta}(u)| <= 2 sqrt(p).
```

This bound alone gives only `O(p^(3/2))` after summing over `u`. The missing
degree-four estimate is exactly cancellation in the outer sum

```text
sum_u mu(u) F_{nu,eta}(u).
```

## Outer Bad-Parameter Set

The fiber support can change only when two support points collide. Besides
the outer Kummer twist at `u=0` and the point at infinity on `P^1_u`, the
finite bad parameters are exactly contained in

```text
B(u)=u^2+u+1=0,          Delta(u)=-3u^2-2u-3=0.
```

Here `B(u)=0` is the collision `v=0` with an `A(u,v)=0` root, and
`Delta(u)=0` is the collision of the two `A(u,v)=0` roots. For `p>3`, both
quadratics are separable. They are disjoint: if `B(u)=Delta(u)=0`, then

```text
Delta(u)+3B(u)=u
```

forces `u=0`, but `B(0)=1`. Also `Delta(0)=-3`, so the outer Kummer point
`u=0` is separate from the discriminant roots.

Thus the sheaf-theoretic proof target for the core sum has bad-parameter
support contained in at most six geometric points:

```text
u=0,        B(u)=0,        Delta(u)=0,        infinity.
```

This is the exact conductor inventory that a proof of the current `9p`
constant, or of a sharper `4p` target, should exploit.

## Line Correction

The principal-coordinate exclusion is the line `w=0`, i.e. `v=-1-u`. On this
line,

```text
A(u,-1-u)=-(u^2+u+1).
```

Therefore the line correction is a genus-zero Kummer sum on `P^1_u` with
support contained in

```text
u=0,        u=-1,        u^2+u+1=0,        infinity.
```

The two roots of `u^2+u+1` are distinct over the algebraic closure for
`p>3`, and neither root is `0` or `-1`. Since `mu` is nonprincipal, the
rational function is not a character-order power. The support size is at
most `5`, so the standard genus-zero bound gives `(5-2)sqrt(p)`.

## Remaining Target

This reduction replaces the two-coordinate part of the two-variable Kummer
import by a sharper one-dimensional trace-family target:

```text
|sum_u mu(u) F_{nu,eta}(u)| <= 9p - 3 sqrt(p)
```

would imply the ledger's current `9p` two-coordinate bound. Any smaller
uniform conductor bound for this trace family would directly sharpen the M1
depth-two saturation constants. In particular, the finite `4p` target audit
in `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md` becomes
the question of proving a correspondingly sharper conductor bound for this
same one-dimensional trace family.
The updated audit records a targeted tuple with ratio `3.9771715522`, so a
uniform `4p` theorem would be nearly sharp in this normalization.

The reciprocal slice `nu=mu^{-1}` is already one-dimensional in a stronger
sense: the substitution `v=tu` collapses the core sum to a genus-zero Kummer
sum in the ratio variable `t`. This subcase is isolated in
`experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`; the remaining
trace-family target is the genuinely nonreciprocal case.

The projective Euler-characteristic target for the core sum is isolated in
`experimental/m1_depth_two_two_coordinate_projective_euler_target.md`. It
explains the `4p` target as the ramified-infinity case of the compactified
line/conic arrangement, and predicts a `2p` top-dimensional coefficient when
`mu nu eta^2` is principal.
That infinity-unramified subfamily is proved by the ratio reduction in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`; the
remaining trace-family target is the infinity-ramified case.
The reciprocal lemma also removes the projective line-pair reciprocal slices
`mu nu=1`, `nu eta^2=1`, and `mu eta^2=1`, leaving only the ramified case
with no reciprocal pair among the three projective line monodromies.

The finite verifier

```bash
python3 experimental/verify_m1_depth_two_two_coordinate_fiber_reduction.py
```

checks the exact decomposition for every two-coordinate tuple in the
representative Kummer-audit samples, verifies the genus-zero line-correction
bound numerically, and reports the largest observed two-coordinate ratios.
