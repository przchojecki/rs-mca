# M1 Depth-Two Reciprocal Two-Coordinate Lemma

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard genus-zero multiplicative Weil bound on `P^1`. Let
`p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero. Let `mu` and
`eta` be nonprincipal multiplicative characters. Consider the two-coordinate
core sum with reciprocal active coordinate characters

```text
C_{mu,eta} = sum_{u,v in F_p} mu(u) mu^{-1}(v) eta(A(u,v)).
```

If `eta` is nonquadratic, then

```text
|C_{mu,eta}| <= 4p.
```

If `eta` is quadratic, then

```text
|C_{mu,eta}| <= 2p + 2 sqrt(p).
```

Restoring the principal-coordinate exclusion `w!=0` subtracts the line
correction

```text
L_{mu,eta}
  = sum_u mu(u) mu^{-1}(-1-u) eta(-(u^2+u+1)),
```

which satisfies

```text
|L_{mu,eta}| <= 3 sqrt(p).
```

The same bounds hold for the active coordinate pairs `(u,w)` and `(v,w)` by
the symmetry of `A=uv+uw+vw-1` on the plane `u+v+w=-1`.

## Ratio Reduction

Because `mu` is extended by zero, only `u,v != 0` contribute to the core.
Set `v=tu`. Then

```text
mu(u) mu^{-1}(tu) = mu^{-1}(t).
```

The missing `u=0` term in the inner sum is independent of `t`, so it cancels
after summing against the nonprincipal character `mu^{-1}(t)`. Hence

```text
C_{mu,eta} = sum_t mu^{-1}(t) H_eta(t),

H_eta(t) = sum_u eta(-(a(t)u^2+b(t)u+1)),
```

where

```text
a(t)=t^2+t+1,        b(t)=t+1,
Delta(t)=b(t)^2-4a(t)=-3t^2-2t-3.
```

## Nonquadratic Conic Character

For nonquadratic `eta`, the fixed-`t` conic sum is the standard quadratic
fiber identity

```text
H_eta(t)
  = eta(1/4) J(eta,chi_2)
    eta(Delta(t)) eta^{-1}(a(t)) chi_2(Delta(t)).
```

This formula is also correct at `a(t)=0` and `Delta(t)=0`, with both sides
zero. Therefore

```text
C_{mu,eta}
  = eta(1/4) J(eta,chi_2)
    sum_t mu^{-1}(t) eta(Delta(t)) eta^{-1}(a(t)) chi_2(Delta(t)).
```

The remaining sum is a genus-zero Kummer sum in `t`. Its zero-pole support is
contained in

```text
t=0,        a(t)=0,        Delta(t)=0,        infinity.
```

This is at most six geometric points. The local monodromy at `t=0` is
`mu^{-1}`, so the sheaf is nontrivial. The genus-zero bound gives
`4 sqrt(p)` for the ratio sum, while `|J(eta,chi_2)|=sqrt(p)`. Thus
`|C_{mu,eta}| <= 4p`.

## Quadratic Conic Character

For `eta=chi_2`, the fixed-`t` fiber identity is

```text
H_{chi_2}(t)
  = -chi_2(-a(t))
    + p chi_2(-a(t)) 1_{Delta(t)=0}.
```

The smooth part

```text
sum_t mu^{-1}(t) chi_2(-a(t))
```

has support contained in `t=0`, `a(t)=0`, and infinity, so it is at most
`2 sqrt(p)`. The exceptional discriminant term has at most two summands and
contributes at most `2p`. This gives

```text
|C_{mu,chi_2}| <= 2p + 2 sqrt(p).
```

## Line Correction

The removed line is `w=0`, i.e. `v=-1-u`. On this line,

```text
A(u,-1-u)=-(u^2+u+1).
```

The line correction is therefore a genus-zero Kummer sum on `P^1_u` with
support contained in

```text
u=0,        u=-1,        u^2+u+1=0,        infinity.
```

This support has at most five geometric points, and the local monodromy at
`u=0` is `mu`, so the standard genus-zero bound gives `3 sqrt(p)`.

## Contribution to the M1 Trace-Family Target

The general two-coordinate wall is the trace-family sum

```text
sum_u mu(u) F_{nu,eta}(u).
```

This note proves that the diagonal reciprocal subfamily `nu=mu^{-1}` does
not require the unresolved two-variable import: after the ratio substitution
`v=tu`, it becomes a one-dimensional genus-zero Kummer sum. The remaining
open two-coordinate target is therefore the genuinely nonreciprocal family.

## Projective Reciprocal Line Pairs

The reciprocal reduction is projective, not tied to the original affine
choice of active coordinates. The compactified two-coordinate core has line
monodromies

```text
mu,        nu,        lambda=(mu nu eta^2)^(-1)
```

on the two active coordinate lines and the line at infinity. If any two of
these three line monodromies are reciprocal, choose those two lines as the
affine coordinate axes. The conic remains projectively equivalent to the same
line/conic arrangement, so the core is one of the reciprocal sums handled
above.

Besides the original `mu nu=1` slice, this proves the ramified-infinity
slices

```text
nu eta^2 = 1,        mu eta^2 = 1.
```

In these two slices `eta` is necessarily nonquadratic for a true
two-coordinate term, and the core bound is `4p`; the removed principal line
still costs at most `3 sqrt(p)`. Thus the unresolved two-coordinate wall can
be restricted further to the case where all three projective line monodromies
are nonprincipal and no pair among them is reciprocal.

## Projective Equal Line Pairs

The same projective chart bookkeeping applies to equal, rather than
reciprocal, projective line monodromies.  If `mu=lambda` or `nu=lambda`, then
choose the equal pair as the affine coordinate axes.  The open sum is carried
exactly to a coordinate-diagonal open sum with the same conic character:

```text
S_{mu,nu,eta}^{open} = S_{theta,theta,eta}^{open}
```

for the common projective line character `theta`.  The case `mu=nu` is the
original coordinate-diagonal chart.  Therefore the diagonal conductor audit in
`experimental/m1_depth_two_equal_line_diagonal_reduction.md` applies to the
whole projective equal-pair slice.

For one active chart, the equal-pair union has the inclusion-exclusion count

```text
#{some equal projective line pair}
  = 3 #{mu=nu} - 2 #{mu=nu=lambda}.
```

This is the `C_2^peq = 3C_2^diag - 2C_2^eq` mass reported by the saturation
verifier.

The finite verifier

```bash
python3 experimental/verify_m1_depth_two_reciprocal_two_coordinate_lemma.py
```

checks the exact ratio identities, the projective reciprocal chart changes,
the projective equal-pair chart changes, the line decomposition, and the
claimed finite bounds on representative Kummer-audit samples.
