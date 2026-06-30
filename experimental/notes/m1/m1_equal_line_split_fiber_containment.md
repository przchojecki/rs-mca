# M1 equal-line projective split-fiber containment

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note proves the projective split-fiber containment step behind the equal-line
popularity budget, in the local coordinates of
`m1_depth_two_equal_line_diagonal_reduction.md`.

It still does not prove that every global M1 high-overlap leaf reaches this
equal-line split-fiber model.  It proves that once a leaf is in this model, the
center-residue containment equation forces the quadratic resultant gate outside
the already charged singular fibers.

## Local coordinates

Use the equal-line variables from the verifier:

```text
y = (1+3z^2)/(1-z)^2,
lambda(z) = z^2/(1+3z^2),
K_x(z) = x + (3x-1)z^2.
```

The equal-line kernel identity is

```text
chi_2(x-lambda(z)) = chi_2(y) chi_2(K_x(z)).
```

The split `y`-fiber resultant is

```text
R(x,y) =
  16x^2y^2 - 8xy^2 + 4xy + y^2 - 2y + 1.
```

The projective form uses `z=[Z:T]`, `x=[X:V]`, and `y=[Y:W]`:

```text
y(z) = [T^2+3Z^2 : (T-Z)^2],
K_x^h(z) = X(T^2+3Z^2) - VZ^2,
R_h(X,V;Y,W)
 = 16X^2Y^2 - 8XVY^2 + 4XVYW
   + V^2Y^2 - 2V^2YW + V^2W^2.
```

For ordinary split fibers, the verifier records

```text
prod_{z' : y(z')=y} K_x(z') = R(x,y)/(y-3)^2.      (SF)
```

The projective identity behind this affine product is the homogeneous
resultant formula

```text
Res_{[Z:T]}(
  Y(T-Z)^2 - W(T^2+3Z^2),
  X(T^2+3Z^2) - VZ^2
) = R_h(X,V;Y,W).                                  (PR)
```

Thus `R_h` is not merely an affine chart artifact: it is exactly the norm of
the homogeneous kernel form along the projective `y`-fiber.

The projective `y`-fiber equation is

```text
(Y-3W)Z^2 - 2YZT + (Y-W)T^2 = 0,
```

with discriminant

```text
Delta_y = 4W(4Y-3W).                               (D)
```

Hence, for finite `y`, the fiber splits over the base field exactly when
`4y-3` is a square.  The ramified finite fiber is `y=3/4`, and the projective
pole `y=infinity` is the double fiber `z=1`.  Both are already charged in the
singular ledger.

Consequently the gate is exact over the base field on ordinary projective
fibers:

```text
R_h(x,y)=0
  <=> exists z in P^1 with y(z)=y and K_x^h(z)=0,              (EX)
```

provided `x,y` are base-field projective points and `y` is outside the
charged singular support.  In particular, nonsplit ordinary `y`-fibers produce
no base-field zeros of the gate.

## Singular fibers

Charge the projective `y`-values

```text
y = 0,
y = 1,
9y^2 + 2y + 1 = 0,
y = 3/4,
y = infinity.
```

This is the same six-point exceptional budget used in
`m1_equal_line_generic_popularity_budget.md`.

## Containment lemma

Let `p>3`, and let `z=[Z:T] in P^1(F_p)` have `y(z)` outside the singular
fiber set.  Equivalently, after charged fibers are removed, `z` is an
ordinary projective split-fiber leaf.

If a projective center residue `x=[X:V]` satisfies the homogeneous
leaf-containment equation

```text
K_x^h(z)=0,
```

then

```text
R_h(x,y(z))=0.
```

Thus every ordinary projective split-fiber leaf containing `x` is covered by
the quadratic projective resultant gate in the `y` parameter.

Conversely, if the ordinary `y`-fiber is split over the field and
`R_h(x,y)=0`, then the same resultant identity gives a common projective root
of the fiber equation and `K_x^h`.  Since the fiber has already split, that
common root is one of its two projective leaf parameters.  Thus the resultant
gate is exact on this local split-fiber model.

If the ordinary `y`-fiber is nonsplit over the base field, then `R_h(x,y)` has
no base-field zero.  Indeed, a zero would make the irreducible quadratic fiber
divide the quadratic kernel form over the base field.  But the kernel form has
zero `ZT` coefficient, while the ordinary uncharged fiber has mixed
coefficient `-2Y`.  The only way this mixed coefficient can vanish is `Y=0`,
which is the charged fiber `y=0`.  Hence no nonsplit ordinary fiber contributes
a base-field gate zero.

The discriminant ledger `(D)` makes this field accounting explicit: ordinary
nonsplit finite fibers are exactly the finite `y` with nonsquare `4y-3`, after
the charged fibers have been removed.

The finite affine statement from the previous version is the chart `T=V=1`:
if

```text
z != 1,
1+3z^2 != 0,
y=(1+3z^2)/(1-z)^2 is not in the singular fiber set,
K_x(z)=0,
```

then `R(x,y)=0`.

## Proof

The hypotheses exclude the charged singular fibers, including `y=0`, which is
the pole of `lambda(z)`, and `y=infinity`, which is the pole of `y(z)`.

The point `z` lies in the projective `y`-fiber, so it is a common zero of

```text
Y(T-Z)^2 - W(T^2+3Z^2)
```

and `K_x^h(Z,T)`.  Therefore their binary resultant vanishes.  By `(PR)`,
this resultant is exactly `R_h(x,y)`, so `R_h(x,y)=0`.

Conversely, if `R_h(x,y)=0`, then `(PR)` says that the two binary quadratics
have a common projective zero after base change.  If the ordinary fiber is
split over the base field, the common zero is one of its base-field roots,
giving a leaf `z` with `K_x^h(z)=0`.  If the ordinary fiber is nonsplit, it is
irreducible over the base field; a common root forces the fiber quadratic to
divide `K_x^h`, contradicting the mixed-coefficient argument above.  Thus the
base-field equivalence `(EX)` holds on all ordinary uncharged fibers.

The remaining paragraphs unpack this identity in the affine chart used by the
original finite verifier.

If `z` is finite and `y != 3`, then `y` is a finite ordinary split value.  The
finite split-fiber identity `(SF)` applies.  Since one factor in the product is
`K_x(z)=0`, the product is zero.  As `(y-3)^2` is nonzero, `R(x,y)=0`.

The remaining ordinary projective fiber is `y=3`.  It has two points:
`z=1/3` and `z=infinity`.

At the finite point `z=1/3`, directly

```text
K_x(1/3) = (12x-1)/9,
```

so `K_x(1/3)=0` gives `x=1/12`, and substituting gives

```text
R(1/12,3)=0.
```

At the projective point `z=infinity=[1:0]`, the homogeneous kernel equation is

```text
K_x^h([1:0]) = 3X - V = 0.
```

Thus `x=[X:V]=[1:3]`, i.e. affine `x=1/3`, and substituting gives

```text
R(1/3,3)=0.
```

Thus the full projective `y=3` fiber is also contained in the resultant gate;
no extra exceptional `y`-fiber is needed.

The excluded `y`-fibers are exactly those charged in the generic equal-line
budget, so the containment lemma feeds the cap

```text
U_eq <= 8mu
```

from `m1_equal_line_generic_popularity_budget.md`.

## Verification

The companion verifier checks the finite split-fiber identity, the projective
degree-two fibers, the discriminant splitting ledger `(D)`, the homogeneous
resultant identity `(PR)`, the singular support exclusions, and the
implications `K_x(z)=0 => R(x,y)=0` and `K_x^h(z)=0 => R_h(x,y)=0`, plus the
exact equivalence `(EX)` and the absence of nonsplit base-field gate zeros,
over expanded prime rows:

```sh
python3 experimental/scripts/verify_m1_equal_line_split_fiber_containment.py
```
