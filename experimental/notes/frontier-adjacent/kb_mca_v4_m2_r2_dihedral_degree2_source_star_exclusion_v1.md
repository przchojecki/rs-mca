---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The degree-two Dickson/Chebyshev profile in the full-V4 inner-degree-2 row is impossible because one generic D2 quotient pole forces eight source-star units onto four vertices, of minimum defect four above the proved budget three.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE2_SOURCE_STAR_EXCLUSION
quantifier: every actual residual (m,r,delta)=(2,2,4) component with dihedral factor degree n=2
projection_and_unit: exact normalized source-star multiplicity; not a carrier, slope, or payment count
claimed_bound: n=2 is empty and the full-V4 factor list narrows to {3,6}
status: PROVED_M2_R2_DIHEDRAL_DEGREE2_EMPTY
impact: DELETES_A_SECOND_FULL_V4_DIHEDRAL_FACTOR_PROFILE
falsifier: failure of regular D2 coset K2,2 incidence, failure of the normalized source cross-edge lemma, or an eight-unit/four-vertex defect below four
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree2_source_star_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear m2 r2 degree-two dihedral source-star exclusion

## 0. Verdict

The `n=2` factor profile in the full-V4 `(m,r,delta)=(2,2,4)` row is empty.
Together with the degree-five exclusion, the surviving factor degrees are

```text
n in {3,6}.
```

Neither remaining profile is deleted here.

## 1. Regular D2 incidence

Fix one of the three generic order-five poles `p` of `G`. Write

```text
q_u^(-1)(p)={y_0,y_1},       q_v^(-1)(p)={z_0,z_1}.
```

All four values are unramified. The two distinct reflection subgroups of
`D_2=V4` have trivial intersection. On the four-point regular orbit, the
map to the product of their two coset sets is therefore bijective. Thus the
outer incidence between the two `Y` and two `Z` values is `K_(2,2)`: both
`Z` values see the same pair `{y_0,y_1}`.

## 2. Source cross-edge lemma

Fix `z` in `{z_0,z_1}` and one endpoint source label
`w in h^(-1)(z)`. The endpoint map `h` is unramified above every source
pole. Full endpoint V4 stability puts both points of `h^(-1)(y_i)` above the
fixed `W=w` on the source normalization, for each `i=0,1`. The normalized
`W=w` fiber therefore consists of four distinct points, two over each
`y_i`.

The normalized source component is isomorphic to this endpoint component,
with `W=psi(X)`. Hence `D_w=psi^*[w]` is reduced of degree two here. Write
its points as `x,bx`. The preserving lift

```text
(T,X)->(tau(T),b(X))
```

shows that the two source sheets have the same number of roots over each
`y_i`. Combined, they have exactly two roots over each `y_i`; each sheet
therefore has one. Every star over `D_w` is one of the four cross edges

```text
h^(-1)(y_0) times h^(-1)(y_1).
```

## 3. Exact defect contradiction

For each `z`, there are two endpoint labels `w`, each with two source units.
The two `Z` values therefore contribute

```text
2 Z-values * 2 endpoint lifts * 2 source units = 8 units
```

on at most four cross vertices. If their weights are `w_1,...,w_4`, then
Cauchy--Schwarz gives

```text
sum_i binomial(w_i,2)
 = (sum_i w_i^2-8)/2
 >= ((8^2/4)-8)/2
 = 4.
```

The complete-source quartic defect budget is three. This contradiction
deletes `n=2`.

## 4. Scope

This packet does not delete `n=3,6`, either other `m=2` type, or the
full-V4 type itself. It constructs no carrier/data/explaining-polynomial/
slope owner, closes no `u=2`, K3, endpoint, KoalaBear, or Prize row, and
moves no ledger quantity.
