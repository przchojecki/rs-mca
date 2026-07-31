---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The sole residual n=3 profile has an explicit genus-zero model realizing the common function, six poles, coefficient quartic, and complete source locators, so geometry alone cannot delete it.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE3_GEOMETRIC_REALIZATION_FENCE
quantifier: one explicit Zariski-open geometric family in the sole residual factor degree
projection_and_unit: exact rational maps and divisor pullbacks; not a deployed endpoint, carrier, slope, or payment count
claimed_bound: abstract common-function and complete-source geometry cannot universally exclude n=3
status: PROVED_M2_R2_DIHEDRAL_DEGREE3_GEOMETRIC_REALIZATION_FENCE
impact: MOVES_THE_RESIDUAL_GATE_TO_FIXED_ACTIVE_PENCIL_OR_OWNER_SEMANTICS
falsifier: failure of the printed pullback, coefficient, genus, or complete-source identities
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree3_geometric_realization_fence_v1.py --check --tamper-selftest
---

# KoalaBear degree-three geometric realization fence

## 0. Verdict

The last full-V4 dihedral profile survives every abstract geometric gate
simultaneously. This does not construct a deployed endpoint record. It proves
that the next obstruction must use the fixed active pencil or a
chronology-valid recurrent owner/payment.

## 1. Explicit source model

At `a=b=-1,d=-1,ell=1`, put

```text
D3(y)=y^3-3y,
h(t)=(t^2+2)/(1-t^2),
psi(x)=2/(x^2+1),
U=x^2+1,
H(t,x)=2U*t^2-2x(x^2+3)t+U^2.
```

The coefficient root sum and product are

```text
S=x(x^2+3)/(x^2+1),       P=(x^2+1)/2,
```

and satisfy

```text
Q_(-1,-1)(S,P)=9(S^2P^2-2P^3-3P^2+1)=0.
```

The discriminant of `H` in `t` is

```text
-4(x^2-1)^2(x^2+2),
```

so the normalization is rational. Direct substitution gives

```text
(h(t)^2+h(t)h(psi(x))+h(psi(x))^2-3)
 =9H(t,x)H(t,-x)
  /((t^2-1)^2(x^2-1)^2(x^2+3)^2).
```

Thus `H` and its source-deck conjugate pull back the non-diagonal factor in

```text
D3(y)-D3(z)=(y-z)(y^2+yz+z^2-3).
```

## 2. Common function and complete source

For any degree-ten `G` with two distinct generic order-five poles,
`F=G composed D3` has degree 30 and six distinct order-five poles. The
degree-six source function is

```text
phi(t)=D3(h(t))
      =(t^2+2)(2t^4-10t^2-1)/(t^2-1)^3,
phi'(t)=54t(2t^2+1)/(t^2-1)^4.
```

Its branch values, and the extra values introduced by `psi`, are only
`+/-2`. Choose the two poles away from them. If `R(v)` is their quadratic
locator, the twelve source labels are the roots of the numerator of
`R(phi(t))`, while the degree-24 complete source form is the numerator of
`R(phi(psi(x)))`.

For every source label `alpha`, the common-D3 identity gives

```text
H(alpha,x) divides B(x).
```

The twelve quartics and twice the degree-24 source form both have degree 48.
The local quadratic bound therefore upgrades divisibility to

```text
sum_alpha div(H(alpha,x))=2 div(B).
```

This realizes the exact two-`K_(2,2,2)` source-star graph as well.

## 3. Scope

This is a geometric route fence. It does not instantiate the fixed
KoalaBear active numerator or denominator, construct an endpoint record or
owner, move a payment, close the full-V4 type or K3, close KoalaBear, or
resolve either Prize problem.
