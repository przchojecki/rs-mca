# Exact full affine syndrome-locator hull rigidity

Author: Manuel E. Rey-Álvarez Zafiria

## 1. Fixture and theorem

Work over `F_p`, with `p = 2^31-1`, in the active punctured M31 rank-two
fixture recorded by the accompanying input file. Let
`F_0,...,F_15` be its sixteen known monic degree-479 split syndrome
locators. Then

```text
Aff(F_0,...,F_15)
  intersect {degree-479 locators split on the 1,023-point fixture domain}
= {F_0,...,F_15}.
```

Thus the sixteen locators are exactly the split intersection of their
15-dimensional affine hull.

The assertion is proved by classifying every nonempty coefficient support.
Supports 2 and 3 are handled by the sparse locator census. Supports 4 through
8 are handled by support-specific partition sieves. Supports 9 through 16
are handled by two support-parametric exact sieves with different core
orders.

The dense half contains

```text
sum_(s=9)^16 binom(16,s) = 26,333
```

supports. The primary and independent sieves process `10,694,457,224` and
`10,694,457,231` admissible projective normals, respectively. Every local
row set has full rank, every residual split margin is positive, and the
minimum dense margin in either computation is 10.

The final synthesis covers all

```text
2^16 - 1 = 65,535
```

nonempty coefficient supports. The only split cases are the sixteen
support-one vertices.

## 2. Support-eight terminal

At support eight, both exact partition sieves classify all `12,870` strata.
There is no local seven-row rank defect. The certified core-root cap is 200,
the minimum residual split margin is 12, and every repeated normal
reconstructs to exactly eight core roots and no outside root.

## 3. Structural route cuts

Two additional exact computations rule out standard low-complexity
explanations of the observed hull.

On each of the 509 core rows, neither the fourteen principal locator values
nor their reciprocals admit a rational parameterization `P_a/Q_b` with
`a+b <= 12`.

The length-509, dimension-16 evaluation code has exact Schur-power profile

```text
(dim C, dim C^(2), dim C^(3)) = (16,136,509).
```

Its Schur square is maximal and its cube fills the ambient space. In
particular, the fixture's rigidity is not explained by a generalized
Reed-Solomon product structure or another low-product-dimension model.

## 4. Scope

This is a fixture-specific theorem inside the affine hull of the sixteen
known locators. It does not prove that every split locator in the full
syndrome section lies in this hull. It therefore does not establish complete
fixture-list equality, exclude arbitrary outsider locators, deploy a typed
first-match argument, or pay a Paper-D row.

The two C++ implementations use different core orders. The JSON bundle and
the synthesis program provide a short exact replay of their terminal
certificates; the source programs also permit complete regeneration.
