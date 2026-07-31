---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the full-V4 inner-degree-2 row, the outer bidegree-(2,2) component is rational and forces a Dickson/Chebyshev right factor of the outer degree-30 map of degree 2, 3, 5, or 6.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_OUTER_FACTOR_REDUCTION
quantifier: every actual residual (m,r,delta)=(2,2,4) component after the line/conic coefficient-image exclusions
projection_and_unit: exact geometric component, source-cover, and pole-divisor reduction; not a slope count or payment
claimed_bound: the arbitrary outer component is reduced to factor degrees n in {2,3,5,6}
status: PROVED_M2_R2_DIHEDRAL_FACTOR_DEGREES_2_3_5_6
impact: NARROWS_THE_FULL_V4_M2_ROW_TO_FOUR_DIHEDRAL_FACTORS
falsifier: a positive-genus outer quotient, a non-dihedral pair of degree-two projections fixing the common function, or a pole profile outside the four printed degrees
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_outer_factor_reduction_v1.py --check --tamper-selftest
---

# KoalaBear m2 r2 dihedral outer-factor reduction

## 0. Verdict

The full-V4 `(m,r,delta)=(2,2,4)` row has a rational outer component. Its
two degree-two projections force

```text
F=G composed q_n,        n in {2,3,5,6},
```

where `q_n` is a geometric Dickson/Chebyshev quotient. No listed degree is
deleted here.

## 1. The outer component is rational

Let `Gamma` be the source normalization and let `S=<a,c>` be its full
endpoint V4 stabilizer. The outer normalization is `C=Gamma/S`.

For source genus zero, `C` is rational. For source genus one, the preceding
genus theorem gives `#Fix(a)=0`, so `a` is translation by nonzero
two-torsion. The conjugation identity

```text
c eta c^(-1)=eta*a
```

excludes `c` from the translation subgroup: every two-torsion translation
commutes with an elliptic reflection. Thus `c` and `a*c` are reflections
with four fixed points each. Riemann--Hurwitz gives

```text
0=4(2g(C)-2)+0+4+4,
```

so `g(C)=0` in this case as well.

The same calculation gives the branch inertia passports for
`Gamma->C`:

```text
source genus 0: a,c,a*c,
source genus 1: c,c,a*c,a*c.
```

## 2. Dihedral factor

Write the two degree-two projections as

```text
Y,Z:C=P1 -> P1.
```

Their deck involutions `u,v` are distinct; otherwise the two quotient
subfields coincide and the outer component is a `(1,1)` graph. The common
degree-60 function `F(Y)=F(Z)` is invariant under both. Its deck group is
finite, so `<u,v>=D_n` is finite dihedral. The quotient tower

```text
C -> C/<u>=P1_Y -> C/D_n=P1
```

has degrees `2,n`. Therefore `F=G composed q_n`, where `q_n` is the
degree-`n` reflection-to-dihedral quotient. Since `deg(F)=30`, `n` divides
`30`.

## 3. Six-pole sieve

The tame quotient `q_n` has local indices only `1,2,n`, including one
totally ramified point of index `n`. Every pole of `F` is one of six
distinct points of order five. If `y` is a pole of `G` and `x` lies above
it, then

```text
ord_x(F)=e_x(q_n) ord_y(G)=5.
```

Except when `n=5`, every selected pole is unramified and each pole fiber
has `n` points. Hence `n` divides six as well as thirty, giving `n=2,3,6`.
For `n=5`, one generic order-five pole of `G` gives five poles of `F`, and
one simple pole at the totally ramified value gives the sixth. The outer
pole degree is `5+1=6`. Degrees `10,15,30` have no local index five and an
unramified fiber is already too large. This proves the four-degree list.

## 4. Scope

This packet does not delete any of `n=2,3,5,6`, solve source-star
incidence, construct a carrier/data/explaining-polynomial/slope owner,
close `m=2`, `u=2`, K3, or the KoalaBear row, or move any ledger quantity.
