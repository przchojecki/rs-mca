# M1 equal-line split-fiber containment

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note proves the finite split-fiber containment step behind the equal-line
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

For ordinary split fibers, the verifier records

```text
prod_{z' : y(z')=y} K_x(z') = R(x,y)/(y-3)^2.      (SF)
```

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

Let `p>3`, and let `z in F_p` satisfy:

```text
z != 1,
1+3z^2 != 0,
y=(1+3z^2)/(1-z)^2 is not in the singular fiber set.
```

If a center residue `x` satisfies the finite leaf-containment equation

```text
K_x(z)=0,
```

then

```text
R(x,y)=0.
```

Thus every ordinary finite split-fiber leaf containing `x` is covered by the
quadratic projective resultant gate in the `y` parameter.

## Proof

The hypotheses exclude the pole of `y(z)`, the pole of `lambda(z)`, and the
charged singular fibers.

If `y != 3`, then `y` is a finite ordinary split value.  The finite split-fiber
identity `(SF)` applies.  Since one factor in the product is `K_x(z)=0`, the
product is zero.  As `(y-3)^2` is nonzero, `R(x,y)=0`.

The remaining ordinary finite fiber is `y=3`.  In this fiber the finite point
is `z=1/3`; the second projective point lies at infinity.  Directly,

```text
K_x(1/3) = (12x-1)/9,
```

so `K_x(1/3)=0` gives `x=1/12`, and substituting gives

```text
R(1/12,3)=0.
```

Thus the finite `y=3` leaf is also contained in the resultant gate; no extra
exceptional `y`-fiber is needed.

The excluded `y`-fibers are exactly those charged in the generic equal-line
budget, so the containment lemma feeds the cap

```text
U_eq <= 8mu
```

from `m1_equal_line_generic_popularity_budget.md`.

## Verification

The companion verifier checks the finite split-fiber identity, the singular
support exclusions, and the implication `K_x(z)=0 => R(x,y)=0` over expanded
prime rows:

```sh
python3 experimental/scripts/verify_m1_equal_line_split_fiber_containment.py
```
