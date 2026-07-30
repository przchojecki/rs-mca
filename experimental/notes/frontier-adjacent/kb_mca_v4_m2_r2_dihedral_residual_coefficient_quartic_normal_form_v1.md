---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every surviving full-V4 n=3 or n=6 source coefficient image is the canonical quartic pullback of its symmetric sibling conic and belongs to an explicit one-parameter family Q_(a,b), with a=-1 or 1 respectively.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_RESIDUAL_COEFFICIENT_QUARTIC_NORMAL_FORM
quantifier: every actual residual (m,r,delta)=(2,2,4) component with dihedral factor degree n in {3,6}
projection_and_unit: exact geometric coefficient-image equation; not a carrier, slope, or payment count
claimed_bound: six arbitrary sibling coefficients reduce to one geometric parameter b for each of n=3 and n=6
status: PROVED_M2_R2_DIHEDRAL_RESIDUAL_ONE_PARAMETER_QUARTIC_NORMAL_FORM
impact: REDUCES_THE_RESIDUAL_REALIZATION_FRONTIER_TO_TWO_ONE_VARIABLE_FAMILIES
falsifier: a nonsymmetric sibling relation, a coefficient image outside the canonical pullback, an endpoint quadratic with zero or two branch values aligned to the Y projection, or a transformed coefficient outside the printed formulas
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_residual_coefficient_quartic_normal_form_v1.py --check --tamper-selftest
---

# KoalaBear residual coefficient-quartic normal form

## 0. Verdict

The two exact residual star graphs do not require an arbitrary plane-quartic
search. Each coefficient image is the canonical pullback of a symmetric
sibling conic, and every actual image belongs to one explicit family

```text
Q_(a,b),       a=-1 for n=3,       a=1 for n=6.
```

Only `b` remains. This does not construct or delete either profile.

## 1. Canonical quartic pin

Let `v` be the deck involution of the `Z` projection on the rational outer
component and let `Y` be the other projection. The map

```text
p -> (Y(p),Y(vp))
```

is birational onto a symmetric bidegree-`(2,2)` sibling correspondence.
Write its equation in elementary symmetric coordinates as

```text
k(sigma,pi)
 = A*pi^2+B*sigma*pi+C*(sigma^2-2*pi)+D*pi+E*sigma+F.
```

After normalizing the endpoint quadratic to `h(t)=t^2`, an unordered source
pair with `S=t+s`, `P=t*s` satisfies

```text
sigma=S^2-2P,       pi=P^2.
```

The entire source coefficient image therefore lies on

```text
Q=A P^4+B S^2P^2-2B P^3+C S^4-4C S^2P
  +(2C+D)P^2+E S^2-2E P+F.                        (1)
```

The residual source theorem makes the image an irreducible plane quartic,
so actual existence forces equality with `(1)`.

## 2. Relative dihedral normalization

Use the regular dihedral action

```text
u(r)=1/r,       v(r)=lambda/r,       a=lambda+lambda^(-1).
```

Eliminating `r` from `Y(r)` and `Y(vr)` gives the sibling conic

```text
x^2+y^2-a*x*y+(a^2-4)=0,
```

with `a=-1` for `D3` and `a=1` for `D6`.

The first quadratic pullback has exactly two branch places in both allowed
source-genus passports. Since the `Y` projection has branch values `2,-2`,
exactly one branch value of `h` lies in this pair. Normalize it to `2`, call
the other `b`, and retain the necessary fence `b notin {2,-2}`. The target
change `m(x)=(x-2)/(x-b)` then permits `m composed h(t)=t^2` without losing
the relative endpoint coordinate.

## 3. One-parameter family

Transporting the sibling conic by `m` gives

```text
A=(a-2)(a-b^2+2),
B=-(a-2)(2a-b^2-2b+4),
C=(a-b)^2,
D=4a^2-a*b^2-4a*b-4a+16b-16,
E=-2(a-2)(a-b),
F=(a-2)^2.                                         (2)
```

Substitution of `(2)` into `(1)` is the promised `Q_(a,b)`.

## 4. Scope

This packet does not prove irreducibility or actual source realization for
an arbitrary `b`, construct or delete `n=3` or `n=6`, delete the full-V4
type, construct an owner, or close K3, an endpoint row, the KoalaBear row,
or either Prize problem. The next exact task is the exceptional-parameter
factorization and the six-pole/source-locator equations in these two
one-variable families.
