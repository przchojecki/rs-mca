---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The degree-five Dickson/Chebyshev profile in the full-V4 inner-degree-2 row is impossible because its totally ramified pole forces source-star weight four, above the proved maximum three.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE5_SOURCE_STAR_EXCLUSION
quantifier: every actual residual (m,r,delta)=(2,2,4) component with dihedral factor degree n=5
projection_and_unit: exact complete-source divisor multiplicity; not a carrier, slope, or payment count
claimed_bound: n=5 is empty and the full-V4 factor list narrows to {2,3,6}
status: PROVED_M2_R2_DIHEDRAL_DEGREE5_EMPTY
impact: DELETES_ONE_OF_FOUR_FULL_V4_DIHEDRAL_FACTOR_PROFILES
falsifier: a non-singleton totally ramified reflection-quotient fiber, failure of the complete source pullback, or a source-star weight budget admitting weight four
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree5_source_star_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear m2 r2 degree-five dihedral source-star exclusion

## 0. Verdict

The `n=5` factor profile in the full-V4 `(m,r,delta)=(2,2,4)` row is empty.
The surviving factor degrees are

```text
n in {2,3,6}.
```

No one of these three profiles is deleted here.

## 1. The totally ramified outer pole

Let

```text
q_u:P1_Y->P1,       q_v:P1_Z->P1
```

be the degree-five reflection quotients from the preceding dihedral packet.
The rotation branch has one point of ramification index five in each
reflection quotient; call the two coordinate values `y_0,z_0`. The unique
admissible `n=5` pole profile puts a simple pole of `G` at their common
quotient value. Consequently `y_0,z_0` are order-five poles of `F`.

On the rational outer component `C`, both points over `Z=z_0` have
`Y=y_0`. They are distinct: inertia at the common branch value is the
order-five rotation group and contains neither reflection defining the two
degree-two projections. Thus

```text
Y^*[y_0]=Z^*[z_0]
```

as reduced degree-two fibers on `C`.

## 2. Complete source pullback

The endpoint inner map `h` is unramified above all six outer poles. Write

```text
h^(-1)(z_0)={w_+,w_-},       h^(-1)(y_0)={t_+,t_-}.
```

These are complete source labels. The source reduction supplies the
quadratic base-change map `psi(X)=W` and

```text
div(B)=psi^*(sum_i [alpha_i]).
```

For `w` in `{w_+,w_-}`, put `D_w=psi^*[w]`. Each `D_w` has degree two and
lies in `div(B)`; the two divisors are disjoint. This uses only the complete
pullback identity. It does not identify `D_w` with the coordinate quadratic
having the same index.

For every `x` in `D_w`, every root of the source quadratic `H(T,x)` lies in
`{t_+,t_-}`. Complete-source saturation gives two distinct source labels at
each root of `B`: each row contributes local order at most `ord_x(B)`, while
the total local order is `2 ord_x(B)`. Hence

```text
H(T,x) is proportional to (T-t_+)(T-t_-).
```

All of `D_(w_+)` and `D_(w_-)` therefore lands on the same matching
source-star vertex `{t_+,t_-}`. Its forced weight is

```text
deg(D_(w_+))+deg(D_(w_-))=2+2=4.
```

The proved quartic defect gate has maximum star weight three, equivalently
`sum_v binomial(w_v,2)<=3`; weight four alone costs six. Contradiction.

## 3. Scope

This packet deletes only the `n=5` factor profile inside the full-V4 type.
It does not delete `n=2,3,6`, either other `m=2` type, or the full-V4 type
itself. It constructs no carrier/data/explaining-polynomial/slope owner,
closes no `u=2`, K3, endpoint, KoalaBear, or Prize row, and moves no ledger
quantity.
