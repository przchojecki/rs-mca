# Full-lift interpolation common-factor router

## Scope

This packet treats the first Mersenne full-lift residual support `e=130237`.
It pays the coprime interpolation branch and routes every unsafe survivor to
a positive-degree common interpolation factor.  It does not classify that
factor or close the support.

## Forced polynomial-pair cores

Retain cutoff `b=65521` and the complementary actual-core cap `64796`.
Every selected affine explanation line belongs to an exact layer
`h>=65522` and has at least two members.  Exact-layer incidence therefore
gives inside common core at least

```text
2*65522-130237=807.
```

The lower bound is conservative because it is nondecreasing in both the
actual layer and the actual line size.  Write the selected line as
`c_gamma=a+gamma*b`; its inside core is exactly where the received pair is
`(r_0,r_1)=(a,b)`.

After 2,704 removed lines, the capped convex envelope has

```text
core budget=18416037,
full caps=253,
remainder=44692,
charge=132203,
target=16645012.
```

With `base=13961576` and `groups=1933560`, the next strict pigeonhole
threshold is still two.  Thus unsafety forces a 2,705th distinct
polynomial-pair core.

## Interpolation kernel

On the gauged `e`-coordinate support, give `(X,Y,Z)` weights `(1,5,5)` and
let `I_264` be the polynomials of weighted degree at most 264 that vanish at
all received points `(x,r_0(x),r_1(x))`.  The ambient monomial count is

```text
sum_(s=0)^52 (s+1)(264-5s+1)=131175,
dim I_264>=131175-130237=938.
```

For every selected pair `(a,b)` and every `Q in I_264`, the polynomial
`Q(X,a(X),b(X))` has degree at most 264 and vanishes on at least 807 distinct
core coordinates.  It is therefore identically zero, so all selected pairs
are common `F(X)`-rational zeros of the interpolation kernel.

## Coprime branch

Over the algebraic closure of `F(X)`, suppose the kernel has no common factor
of positive `(Y,Z)` degree.  Two generic kernel members are then coprime.
Each has total `(Y,Z)` degree at most `floor(264/5)=52`, so affine Bezout
permits at most

```text
52^2=2704
```

common zeros, counted with multiplicity.  This contradicts the 2,705
distinct pairs forced by the bank.

Hence every unsafe survivor has a common factor of positive `(Y,Z)` degree
in `I_264` over the algebraic closure of `F(X)`.  A factor depending only on
`X` is a unit over `F(X)` and does not qualify.

This is the exact algebraic residual.  A further theorem must classify its
ruled components or charge their line/core mass.  In particular, this packet
does not assert that every common factor is automatically a split pencil.

## Replay

```bash
python3 experimental/verify_mca_full_lift_interpolation_common_factor_router_v1.py
python3 experimental/audit_mca_full_lift_interpolation_common_factor_router_v1.py
```
