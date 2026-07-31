---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every allowed residual one-parameter quartic Q_(a,b), with a in {-1,1} and b outside {-2,2}, is geometrically irreducible and rational; it has three nodes for b!=a or one node and one tacnode for b=a.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_RESIDUAL_QUARTIC_SINGULARITY_ATLAS
quantifier: every geometric parameter b allowed by the residual n=3 or n=6 normal form
projection_and_unit: exact plane-curve singularity and function-field classification; not a carrier, slope, or payment count
claimed_bound: coefficient factorization and genus delete no allowed residual parameter
status: PROVED_M2_R2_DIHEDRAL_RESIDUAL_QUARTIC_SINGULARITY_ATLAS
impact: CLOSES_THE_COEFFICIENT_GEOMETRY_ATTACK_AND_FORCES_THE_FRONTIER_TO_ACTUAL_POLE_SOURCE_REALIZATION
falsifier: a reducible allowed Q_(a,b), an extra singularity, a degenerate printed tangent cone, or normalization genus different from zero
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_residual_quartic_singularity_atlas_v1.py --check --tamper-selftest
---

# KoalaBear residual quartic singularity atlas

## 0. Verdict

For `a=-1` (`n=3`) or `a=1` (`n=6`) and every `b notin {-2,2}`, the
one-parameter quartic `Q_(a,b)` is geometrically irreducible and rational.
Coefficient factorization and genus delete no allowed parameter.

## 1. Square-class form

Put `X=S^2`. The quartic is

```text
R(X,P)=C X^2+(B P^2-4C P+E)X+M(P),
```

with

```text
M=(a-2)(P+1)^2 N(P),
N=(a-b^2+2)P^2+2(a-2b+2)P+(a-2),
disc(N)=4(a+2)(b-2)^2,
disc_X(R)=P^2(alpha P^2+beta),
alpha=(a-2)(a+2)(b-2)^3(b+2),
beta=-4(a+2)(a-b)(b-2)^3.
```

For `b!=a`, `R` is a nonsplit quadratic extension and the norm square
class of `X` is the nonsquare quadratic `N`. Thus replacing `X` by `S^2`
remains geometrically irreducible. For `b=a`, the equation becomes
quadratic in `S`; after removing square factors its radicand is still `N`,
so it remains irreducible.

## 2. Singularities

When `b!=a`, the complete singularity set is

```text
(S,P)=(0,-1),
P=0, S^2=(a-2)/(a-b).
```

The Hessian determinants are respectively

```text
-4(a-2)(a+2)(b-2)^4,
16(a-2)(a+2)(b-2)^3,
```

so all three are nodes. When `b=a`, the first node remains and the other
two coalesce at `[1:0:0]`; the local form has nonzero `P^2` and `U^4`
terms, giving a tacnode of delta two. Total delta is three in either case,
equal to the arithmetic genus of a plane quartic.

## 3. Scope

This packet proves geometric viability, not actual source realization. It
does not construct or delete `n=3` or `n=6`, delete the full-V4 type,
construct an owner, or close K3, an endpoint row, the KoalaBear row, or
either Prize problem. The next gate is the six order-five pole fibers and
complete source locators in the printed `Q_(a,b)` families.
