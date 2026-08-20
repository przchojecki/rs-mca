# Full-lift core-dichotomy capped charge

## Scope

This packet adds an exhaustive actual-core split to the Mersenne recursive
line bank.  It pays `130222<=e<=130225`; it does not certify the adjacent row
unsafe or close the full Mersenne row.

## High-core branch

Fix `b_abs=65450`.  A selected affine explanation line with actual total
core `g` has at least `g-c` core coordinates inside the gauged direction
support.  Two line anchors synchronize every explanation of inside deficit

```text
h>=e-g+c+K=e-g+11
```

onto the same line.  Thus, when `g>=e+10-b_abs`, the exact weighted prefix
through `b_abs` pays the low explanations and one absolute line cap pays the
rest.  Across the five endpoint rows needed for payment and wall audit,

```text
P_e(65450)+(N-m+1) <= 5161307 < 16777215.
```

## Capped complementary branch

If no selected line enters the high branch, every actual core obeys

```text
g_i<=G_e:=e+9-b_abs.
```

Retain the forced lower bounds and greedily spend the common core budget

```text
S_r=min(rG_e,e+C(r+1,2)c)
```

up to the individual ceiling `G_e`.  The same convex exchange as in the
lower-aware theorem proves that this maximizes the total removed-line charge.

At `e=130222,130223`, fourteen threshold-18 lines give

```text
14*9736-C(14,2)*5 = 135849 > e.
```

At `e=130224,130225`, seventy threshold-16 lines give

```text
70*2041-C(70,2)*5 = 130795 > e.
```

## Adjacent wall

At `e=130226`, the first threshold is 14 and its forced total core is zero.
All later thresholds are no larger.  After 14,763 zero-lower-bound peels,

```text
S_r=545032556=8412*64785+61136,
charge=3199542,
target=13577673,
base=13317279,
next threshold=1.
```

The bank no longer forces an actual line.  This is a method wall, not an
unsafe certificate.  The residual is

```text
130226<=e<=1044241.
```

## Replay

```bash
python3 experimental/verify_mca_full_lift_core_dichotomy_capped_charge_v1.py
python3 experimental/audit_mca_full_lift_core_dichotomy_capped_charge_v1.py
```
