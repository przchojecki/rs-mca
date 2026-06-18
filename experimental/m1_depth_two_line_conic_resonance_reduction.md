# M1 Depth-Two Line-Conic Resonance Reduction

**Status:** PROVED / AUDIT.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
B(v)=v^2+v+1.
```

Extend multiplicative characters by zero at zero.  In the line-conic
resonant two-coordinate core with `mu eta=1`, write `mu=eta^(-1)` and define

```text
C_{eta,nu} =
  sum_{u,v in F_p} eta^(-1)(u) nu(v) eta(A(u,v)).
```

Then

```text
C_{eta,nu} =
  sum_{y in F_p} eta(-y) G_nu(y),

G_nu(y) =
  sum_{v in F_p} nu(v)
    chi_2(y^2 - 2(v+1)y - 3v^2 - 2v - 3).
```

Thus the line-conic-resonant slice is not a generic two-variable Kummer
problem.  It is a Mellin transform of a one-dimensional quadratic-fiber trace
family.

## Proof

For fixed `v`, the summand is zero unless `u` and `A(u,v)` are nonzero.  For
`u != 0`,

```text
eta^(-1)(u) eta(A(u,v))
  = eta(A(u,v)/u)
  = eta(-(u+v+1+B(v)/u)).
```

Use the degree-two map

```text
x = u + B(v)/u.
```

If `B(v) != 0`, the number of nonzero `u` mapping to `x` is
`1+chi_2(x^2-4B(v))`.  The contribution of the `1` term is

```text
sum_x eta(-(x+v+1)) = 0
```

because `eta` is nonprincipal.  Hence

```text
sum_u eta^(-1)(u) eta(A(u,v))
  = sum_x chi_2(x^2-4B(v)) eta(-(x+v+1)).
```

The same identity holds when `B(v)=0`: both sides are
`-eta(-(v+1))`.  Replacing `y=x+v+1` gives

```text
x^2-4B(v)
  = y^2 - 2(v+1)y - 3v^2 - 2v - 3,
```

and interchanging the `v` and `y` sums proves the claim.

## Singular-Value Checklist

For fixed `y`, the quadratic in `v` is

```text
Q_y(v) = -3v^2 - 2(y+1)v + y^2 - 2y - 3.
```

Its discriminant is

```text
disc_v(Q_y) = 16(y-2)(y+1).
```

The root collision values are therefore `y=-1` and `y=2`.  The collision of
a quadratic root with the coordinate line `v=0` is controlled by

```text
Q_y(0) = y^2 - 2y - 3 = (y-3)(y+1),
```

so it adds `y=3` and repeats `y=-1`.  The outer Mellin character adds
`y=0`, and infinity is the remaining projective point.  For `p>3`, the
candidate singular support is contained in

```text
y=0,        y=-1,        y=2,        y=3,        infinity.
```

This is the finite conductor target for the line-conic-resonant asymmetric
mass `C_2^lc`.  The active M1 certificate remains conservative: this note
does not prove the required conductor bound, but it replaces the residual
two-variable resonant slice by an explicit one-dimensional trace-family
problem.

## Finite Singular-Fiber Values

The finite singular values above do not hide a `p`-sized exceptional
contribution.  Write

```text
G_nu(y) = sum_v nu(v) chi_2(Q_y(v)).
```

For every nonprincipal `nu`,

```text
G_nu(-1) = 0,
G_nu(2)  = -chi_2(-3) nu(-1),
```

and

```text
G_nu(3)
  = chi_2(3) nu(-8/3) J(nu chi_2, chi_2),
```

where

```text
J(alpha,beta) = sum_t alpha(t) beta(1-t)
```

is the usual Jacobi sum with characters extended by zero.  Hence
`|G_nu(3)| = sqrt(p)` unless `nu=chi_2`, in which case
`G_nu(3)=-chi_2(-2)`.

The `y=0` term contributes nothing to `C_{eta,nu}` because `eta(0)=0`.
Therefore the whole finite singular contribution to the Mellin transform is
bounded by

```text
|eta(-2)G_nu(2) + eta(-3)G_nu(3)| <= 1 + sqrt(p).
```

Thus any `p`-scale obstruction to the desired `|C_{eta,nu}|<=4p` target
must come from the lisse open trace over

```text
P^1_y \ {0,-1,2,3,infinity},
```

not from a bad finite fiber.

Indeed, the identities follow by direct specialization:

```text
Q_{-1}(v) = -3v^2,        Q_2(v) = -3(v+1)^2,
Q_3(v)   = -v(3v+8).
```

The first gives `chi_2(-3) sum_{v!=0} nu(v)=0`.  The second gives
`chi_2(-3) sum_{v!=-1} nu(v)=-chi_2(-3)nu(-1)`.  For the third, write
`a=8/3`; then

```text
G_nu(3) = chi_2(-3) sum_v (nu chi_2)(v) chi_2(v+a).
```

Substituting `v=-at` gives the displayed Jacobi sum and the factor
`chi_2(3)nu(-a)`.

## Open-Set Line Correction

For the actual two-coordinate open sum, the principal coordinate line
`w=0`, i.e. `v=-1-u`, must be removed.  The correction is

```text
L_{eta,nu} =
  sum_u eta^(-1)(u) nu(-1-u) eta(-(u^2+u+1)).
```

This is a genus-zero Kummer sum on `P^1_u` with support contained in

```text
u=0,        u=-1,        u^2+u+1=0,        infinity.
```

Since `eta` is nonprincipal, the local monodromy at `u=0` is nontrivial, so
the standard genus-zero bound gives `|L_{eta,nu}| <= 3 sqrt(p)`.  Thus the
remaining conductor issue for the open line-conic-resonant slice is exactly
the one-dimensional `y`-family above, plus this already understood
line correction.

## Relation to the M1 Wall

The line-conic-resonant mass was isolated in
`experimental/m1_depth_two_lift_window_theorem.md` as `C_2^lc`.  Combining
this reduction with a future conductor bound for `G_nu(y)` would remove the
last two-coordinate slice still charged at the old `9p` import after the
conditional projective-equal and nonresonant ledgers.

## Admissible Character Filter

The transformed pair `(eta,nu)` is not arbitrary in the actual asymmetric
`C_2^lc` ledger.  Fix one projective line-conic resonance and divide the
common character order by the coordinate-character lift.  Write the resonant
line exponent as `a` and the second active line exponent as `b`, with
`a,b in Z/eZ` nonzero.  The conic exponent is then `-a`, so in the notation
of this note

```text
eta = chi^{-a},        nu = chi^b.
```

The three projective line exponents are

```text
a,        b,        a-b.
```

The already removed equal-line and reciprocal-line slices are exactly the
four forbidden relations

```text
b = a,        b = -a,        b = 2a,        2b = a        mod e.
```

Thus the actual character range for the transformed `C_2^lc` conductor
target is

```text
a,b != 0,        b != a,        b != -a,
b != 2a,         2b != a        mod e.
```

In this range the other two possible line-conic resonances are also absent:
`nu eta=1` would give `b=a`, and `lambda eta=1` would give `b=0`, where
`lambda=(nu eta)^(-1)` is the infinity-line monodromy.

Inclusion-exclusion over the four forbidden relations gives the per-fixed
resonant-line count

```text
R(e) = (e-1)(e-5) + 3 1_{2|e} + 2(gcd(e,3)-1).
```

This is the character-side form of the `C_2^lc` split:

```text
C_2^lc = 9R(e).
```

The factor `9` is the product of the three active coordinate pairs and the
three possible resonant projective lines.  The finite verifier checks the
filter, its equivalence with "no equal or reciprocal projective line pair",
and the displayed count directly for character orders `2 <= e <= 40`.

## Conditional Ledger Target

The precise conductor target is now the following one-dimensional statement:

```text
|C_{eta,nu}| <= 4p
```

for every nonprincipal line-conic-resonant pair occurring in `C_2^lc`.  Since
the open two-coordinate sum differs from `C_{eta,nu}` by the genus-zero line
correction above, this would give the certificate-facing replacement

```text
|S_open| <= 4p + 3 sqrt(p)
```

on the whole `C_2^lc` slice.  This is intentionally recorded as a
`CONDITIONAL` target, not as a proved theorem: the missing input is the
middle-extension conductor bound for the rank-two quadratic-fiber
pushforward on the `y`-line.

The saturation scanner now reports this optional ledger separately.  If the
projective equal-pair import, the clean nonresonant line/conic import, and
this line-conic-resonant conductor import are all accepted, the residual
ramified nonreciprocal two-coordinate mass after the proved
`C_2^0` and `C_2^rec` reductions is charged at

```text
4(C_2^peq + C_2^anr + C_2^lc)
  = 4(C_2^peq + C_2^asym).
```

Equivalently, relative to the conservative `9p` charge on that residual, the
leading L1 weight drops by `5(C_2^peq+C_2^asym)` and the square-root mass
adds `3(C_2^peq+C_2^asym)`.  The active `saturation_certificate` remains
unchanged.

The verifier also performs a finite counterexample-first audit for this
target.  It exhausts all nonprincipal `(eta,nu)` for `p=17,31` and checks
targeted larger cases; in the current audit it reports no `4p` violation for
the core or open sums and no `3 sqrt(p)` violation for the line correction.
The remaining-wall scanner also has a dedicated line-conic-resonant pass:
in its current report grid, the largest `C_2^lc` asymmetric ratio is
`2.7649691518p`, below the nonresonant asymmetric maximum
`3.2173609608p`.

## Full-Character Second Moment

The transformed core also has an exact orthogonality check.  Sum over all
multiplicative characters `eta,nu` of `F_p^*`, including the principal
character extended by zero.  Then

```text
sum_{eta,nu} |C_{eta,nu}|^2 = (p-1)^2 S_p,

S_p = 2p^2 - 8p + 13 - chi_2(-3)p + 9chi_2(-3) + chi_2(-2).
```

Indeed, character orthogonality gives `(p-1)^2` times the number of
collisions

```text
v=v' != 0,        A(u,v)/u = A(u',v)/u' != 0.
```

For fixed `v`, this is the collision count of

```text
u |-> -(u+v+1+B(v)/u),        u in F_p^*.
```

If `B(v) != 0`, the only collisions are

```text
u=u'        or        uu'=B(v).
```

Thus the count for that `v` is

```text
2(p-1) - (1+chi_2(B(v))) - (1+chi_2(Delta(v)))^2,
Delta(v) = -3v^2 - 2v - 3,
```

where the first subtraction removes the double-counted branch points and the
second removes the zero value `A=0`.  If `B(v)=0`, the map is linear on
`F_p^*` and the nonzero-value count is `p-2`.

Summing over `v in F_p^*` uses

```text
sum_{v in F_p^*} chi_2(B(v)) = -2,
sum_{B(v)!=0} chi_2(Delta(v)) = -1 - 3chi_2(-3),
#{v in F_p^*: B(v)!=0, Delta(v)!=0}
  = p - 3 - chi_2(-3) - chi_2(-2),
```

which gives the displayed formula for `S_p`.  In particular the full-family
root-mean-square core size is `sqrt(S_p) < sqrt(2)p`.  This does not prove
the pointwise `4p` target, but it rules out any hidden large average behind
the line-conic resonant family.

The removed line has an even simpler full-character moment:

```text
sum_{eta,nu} |L_{eta,nu}|^2
  = (p-1)^2 (p - 3 - chi_2(-3)).
```

Here orthogonality forces `-1-u=-1-u'` and then `u=u'`; the support excludes
`u=0`, `u=-1`, and the `1+chi_2(-3)` roots of `u^2+u+1`.

## Nonprincipal Second Moment

The full-character moment above still includes the principal `eta` and `nu`
rows, which are not part of the line-conic-resonant M1 target.  These rows
carry a visible part of the average.  Removing them gives an exact
nonprincipal moment.

Let

```text
S = {(u,v): u != 0, v != 0, A(u,v) != 0},
        x(u,v)=A(u,v)/u.
```

Write

```text
T_p = #S,
N_x = sum_{x in F_p^*} #{(u,v) in S: x(u,v)=x}^2,
N_v = sum_{v in F_p^*} #{u: (u,v) in S}^2.
```

Then

```text
T_p = p^2 - 3p + 3 + 3 chi_2(-3),

N_x = p^3 - 3p^2 + 5p - 19
      + (6p - 16) chi_2(-3),

N_v = p^3 - 5p^2 + 11p - 11
      + (6p - 13) chi_2(-3) - chi_2(-2).
```

Consequently

```text
sum_{eta != 1, nu != 1} |C_{eta,nu}|^2
  = (p-1)^2 S_p - (p-1)(N_x+N_v) + T_p^2

  = p^4 - 8p^3 + 22p^2 - 6p + 1
    + (-p^3 + 5p^2 + 4p - 2) chi_2(-3)
    + (p^2 - p) chi_2(-2).
```

Thus the true nonprincipal family has root-mean-square size
`p+O(1)`, rather than the `sqrt(2)p+O(1)` full-character RMS.  The
principal rows account for the missing average mass; the actual resonant
target has no hidden large second moment.

For the proof, nonprincipal orthogonality gives

```text
sum_{eta != 1} eta(x/x') = (p-1) 1_{x=x'} - 1,
sum_{nu != 1} nu(v/v') = (p-1) 1_{v=v'} - 1.
```

Expanding the product gives the displayed formula in terms of `S_p`, `N_x`,
`N_v`, and `T_p`.

It remains only to compute the two marginal collision sums.  For fixed
`v != 0`,

```text
#{u: (u,v) in S}
  = p - 2 - chi_2(-3v^2-2v-3) + 1_{v^2+v+1=0}.
```

Squaring and summing over `v != 0`, using the elementary quadratic sums for
`-3v^2-2v-3` and `v^2+v+1`, gives the displayed `N_v`.

For fixed `x != 0`, the equation `x=A(u,v)/u` is the affine conic

```text
u^2+v^2+uv+(x+1)u+v+1=0
```

with `u,v != 0`.  Its projective determinant is
`-(x-1)(x+2)/4`.  For `x != 1,-2`, the conic is nonsingular; it has
`p+1` projective points, `1+chi_2(-3)` points at infinity, and the removed
coordinate lines contribute `1+chi_2(-3)` points with `u=0` and
`1+chi_2((x-1)(x+3))` points with `v=0`.  Hence

```text
#{(u,v) in S: x(u,v)=x}
  = p - 2 - 2 chi_2(-3) - chi_2((x-1)(x+3)).
```

At the two degenerate values, the singular points are `(-1,0)` for `x=1`
and `(1,-1)` for `x=-2`, with tangent cone `U^2+UV+V^2`.  Therefore

```text
M_1    = (1+chi_2(-3))(p-2),
M_{-2} = 1 + (1+chi_2(-3))(p-3).
```

Summing these squared fiber sizes over `x in F_p^*` gives the displayed
`N_x`.

## Principal-Row Leakage

The principal rows excluded above have exact formulas.  They explain why the
full-character moment has RMS `sqrt(2)p+O(1)` while the actual nonprincipal
target has RMS `p+O(1)`.

If `eta=1` and `nu` is nonprincipal, then

```text
C_{1,nu}
  = -sum_v nu(v) chi_2(-3v^2-2v-3)
    + sum_{v^2+v+1=0} nu(v).
```

This is only a genus-zero-size row: the first term is a Kummer sum on
`P^1_v` with support contained in `v=0`, the two roots of
`-3v^2-2v-3`, and infinity, while the second term has at most two summands.

If `nu=1` and `eta` is nonprincipal, then

```text
C_{eta,1}
  = -sum_x eta(x) chi_2((x-1)(x+3))
    + chi_2(-3) p (eta(1)+eta(-2)).
```

Thus the `nu=1` row contains the two `p`-scale exceptional conic
degeneracies at `x=1` and `x=-2`.  These rows are not part of `C_2^lc`, but
they account for the extra full-character second-moment mass.

Finally,

```text
C_{1,1} = T_p = p^2 - 3p + 3 + 3chi_2(-3).
```

The first formula follows from fixed `v`: the number of contributing
`u != 0` is

```text
p - 2 - chi_2(-3v^2-2v-3) + 1_{v^2+v+1=0},
```

and the constant term vanishes against nonprincipal `nu`.  The second follows
from fixed `x=A/u`: the generic conic count is

```text
p - 2 - 2chi_2(-3) - chi_2((x-1)(x+3)),
```

but at the two degenerate values `x=1,-2` the actual count differs by
`chi_2(-3)p`, giving the exceptional term.

The finite verifier is

```bash
python3 experimental/verify_m1_depth_two_line_conic_resonance_reduction.py
```
