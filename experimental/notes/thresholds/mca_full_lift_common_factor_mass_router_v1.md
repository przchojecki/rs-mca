# Full-lift common-factor mass router

## Scope

This packet strengthens the Mersenne `e=130237` interpolation residual.  It
forces near-total received-point concentration on the common factor; it does
not classify the factor or close the support.

## Full line supply

At cutoff `65521`, every selected low-core line has inside core at least 807
and actual total core at most 64796.  After 7,582 removals the capped charge
is

```text
charge=881897, target=15895318, next threshold=2.
```

Thus an unsafe family forces a 7,583rd distinct polynomial pair.  After that
line the threshold drops to one; no later line is used.

## Factor capture

Over the algebraic closure of `F(X)`, let `P` be the full gcd of the nonzero
members of the weight-264 interpolation kernel and put
`d=deg_(Y,Z)P`.  The common-factor router gives `1<=d<=52`.

After division by `P`, the cofactor family has gcd one and `(Y,Z)` degree at
most `52-d`.  Two generic cofactors are coprime, so affine Bezout permits at
most `(52-d)^2` selected pairs outside `P=0`.  Therefore

```text
on-factor pairs >= 7583-(52-d)^2 >= 4982.
```

## Received-point concentration

Each captured pair has an inside core of size at least 807, contained in

```text
S_P={x:P(x,r_0(x),r_1(x))=0}.
```

Distinct pair cores intersect in at most five coordinates.  If `t` pairs
are captured, incidence Cauchy gives

```text
|S_P| >= ceil(t*807^2/(807+5(t-1))).
```

This expression is increasing in `t`; at the uniform minimum `t=4982`,

```text
|S_P|>=126188,
130237-|S_P|<=4049.
```

Hence every unsafe survivor has a degree-at-most-52 factor relation holding
on at least 96.89% of the inside support and carrying at least 4,982
degree-five polynomial sections.

This is not a common core shared by all sections, and the packet does not
assert that `P` is irreducible, rational, or a split pencil.

## Replay

```bash
python3 experimental/verify_mca_full_lift_common_factor_mass_router_v1.py
python3 experimental/audit_mca_full_lift_common_factor_mass_router_v1.py
```
