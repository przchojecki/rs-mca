---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Equality of the coefficient quotient and actual endpoint quadratic covers forces the relative second-endpoint branch preimages to be the roots of z^2-b*d*z+b^2+d^2-4, and classifies source genus zero by b^2=a+2.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_RESIDUAL_SOURCE_COVER_TWIST_CLASSIFIER
quantifier: every actual residual n=3 or n=6 one-parameter quartic with its second endpoint twist
projection_and_unit: exact quadratic function-field square class and V4 branch passport; not a carrier, slope, or payment count
claimed_bound: g(source)=0 iff b^2=a+2 and g(source)=1 otherwise
status: PROVED_M2_R2_DIHEDRAL_RESIDUAL_SOURCE_COVER_TWIST_CLASSIFIER
impact: REMOVES_THE_UNTRACKED_SECOND_ENDPOINT_BRANCH_REGIME
falsifier: failure of the square-class identity, a different endpoint branch-preimage pair, or source genus outside the printed classifier
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_residual_source_cover_twist_classifier_v1.py --check --tamper-selftest
---

# KoalaBear residual source-cover twist classifier

## 0. Verdict

Retain the relative projective twist `Z=ell(Z_0)` between the standard and
actual second endpoint coordinates. Equality of the two quadratic source
subextensions forces

```text
ell^(-1)({2,b})=roots(z^2-b*d*z+b^2+d^2-4),
d^2=a+2.
```

Consequently the source genus is zero exactly when `b^2=a+2`, and one
otherwise. Neither regime is deleted.

## 1. Square-class identity

Use

```text
u(r)=1/r, v(r)=lambda/r, mu^2=lambda,
Y=r+1/r, Z_0=r/mu+mu/r,
a=lambda+lambda^(-1), d=mu+mu^(-1).
```

Then `d^2=a+2`. With `m(x)=(x-2)/(x-b)`, direct reduction gives

```text
m(Y(r))m(Y(vr))=(Z_0-d)^2/Q_b(Z_0),
Q_b(z)=z^2-b*d*z+b^2+d^2-4.
```

The left side defines the coefficient-quotient quadratic cover. The actual
endpoint lift is `W^2=m(ell(Z_0))`. Writing this last radicand as a ratio of
the two linear forms above `2,b`, equality of square classes forces those
linear forms to be the two factors of the squarefree `Q_b`.

## 2. Source genus

The standard `Z_0` branch values are `2,-2`, and

```text
Q_b(2)=(b-d)^2, Q_b(-2)=(b+d)^2.
```

The genus-zero V4 passport has exactly one endpoint branch value aligned
with this pair, so `b=+/-d`. The genus-one passport has none aligned. Since
`d^2=a+2`, this proves the classifier.

## 3. Scope

This packet does not assert existence in either genus regime, impose the
common degree-30 function or its six poles, construct complete source
locators, delete either profile, or close K3, KoalaBear, an endpoint row,
or either Prize problem.
