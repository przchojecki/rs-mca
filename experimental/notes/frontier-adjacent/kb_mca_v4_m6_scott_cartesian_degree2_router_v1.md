---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every inner-degree-6 transverse terminal is impossible or routes to inner degree 2. Kernel-free degree-10 actions force an intermediate inner degree 5. Otherwise Scott-compatible columns have size 5 or 10; size 5 is excluded, while a size-10 column contains the quartic suborbit and factors to degree 2 or 5.
architecture: null
partition_digest: null
atom_or_cell: K3_M6_SCOTT_CARTESIAN_DEGREE2_ROUTER
quantifier: every actual inner-degree-6 transverse terminal satisfying the imported source-pencil compiler
projection_and_unit: exact geometric decomposition routing; not a carrier owner, received-line theorem, or slope payment
claimed_bound: all six inner-degree-6 transverse types cease to be independent producers; the global independent frontier falls from 18 to 12 types in inner degrees 2,3,4
status: PROVED_M6_ROUTED_TO_INNER_DEGREE_2_OR_EXCLUDED_M5_OTHER_K3_ROWS_OPEN
impact: REMOVES_M6_AS_A_TERMINAL_PRODUCER_BY_WREATH_INTERMEDIATE_BLOCKS_OR_SCOTT_CARTESIAN_COLUMNS
falsifier: a kernel-free degree-10 chain without an index-five intermediate subgroup, another Scott compatibility size supporting the quartic orbit, or an indecomposable degree-10 column map with subdegree four
replay: python3 experimental/scripts/verify_kb_mca_v4_m6_scott_cartesian_degree2_router_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-6 Scott-Cartesian router

## 0. Verdict

Every actual inner-degree-six transverse terminal dies or routes to inner
degree two:

```text
m=6  ->  m=2 or no producer.
```

Together with the proved `m=12` close and `m=10` router, the independent
transverse frontier is 12 types in degrees `2,3,4`. The degree-two
destination is neither deleted nor paid.

## 1. Imported terminal

Write `f=F composed h`, with `deg(h)=6` and `deg(F)=10`. The terminal inner
map is indecomposable. Its primitive monodromy catalogue is

```text
H       order   socle   subdegrees
A5         60   A5      1,5
S5        120   A5      1,5
A6        360   A6      1,5
S6        720   A6      1,5
```

and the actual quartic component gives a transverse point-stabilizer
suborbit `Delta` of size four.

## 2. Kernel-free chains

Let `N` be the kernel on the ten blocks of size six. If `N=1`, then `G` is
one of the 45 transitive degree-ten groups. For the endpoint chain
`A<G_0<G`, one has `[G:G_0]=10` and `[G_0:A]=6`. The primitive quotient of
`G_0` has order divisible by 60, so `600` divides `|G|`. The complete
catalogue leaves entries 40--45: four subgroups of `S5 wr C2`, then the
natural `A10,S10`.

The last two point stabilizers are `A9,S9`. Simplicity of `A9`, the normal
subgroups of `S9`, and `|S6|=720` exclude every transitive degree-six
quotient. In entries 40--43, the ten points split into two blocks of five
and the point stabilizer has one nonabelian composition factor: the remote
`A5`. It yields the standard degree-six `A5` or `S5` quotient, whose point
stabilizer is the normalizer `D10` or `F20` of a five-cycle.

The exact chains are

```text
G type                 |G|     |G_0|  H    |A|  |M|  [M:A]
[A5^2]2               7200       720  A5   120   600    5
parity wreath, split 14400      1440  S5   240  1200    5
parity wreath, twist 14400      1440  S5   240  1200    5
[S5^2]2              28800      2880  S5   480  2400    5
```

The subgroup `M` enlarges the local four-point stabilizer to the
corresponding five-point group while retaining the remote five-cycle
normalizer. Thus every kernel-free case forces the already excluded
inner-degree-five decomposition.

## 3. Scott-compatible columns

Suppose `N` is nontrivial. Its derived subgroup is subdirect in ten copies
of `A5` or `A6`, and Scott's lemma partitions the coordinates into diagonal
strips. Refine a strip by permutation compatibility: two coordinates are
compatible when their twist is realized by a bijection of the six-point
socle actions. These classes form a uniform invariant partition.

For `alpha` in the first block, `D_alpha` has orbits `1,5` in a compatible
coordinate. An incompatible `A6` coordinate has no fixed point and is
transitive, since `A5` has no subgroup of index two, three, or four. A
different Scott strip also contributes a transitive factor. Hence the four
points of `Delta` are synchronized fixed counterparts in one compatibility
class. Its size is at least five and divides ten, so it is five or ten.

Compatible twists can be untwisted because the two-transitive socle
centralizer is trivial. Size five gives the excluded row. At size ten, the
four points of `Delta` lie in the same degree-ten column fiber as `alpha`.
No primitive degree-ten group has subdegree four: its nontrivial subdegrees
are `3,6` or `9`. The column map therefore has a proper right factor of
degree two or five. Only degree two survives.

## 4. Frontier and custody

The routed types are

```text
(r,delta)=(1,24),(2,12),(3,8),(4,6),(6,4),(8,3).
```

The exact sources are GAP PrimGrp commit
`5612e113d50ac23a7d10945383936e20440b4e14`, GAP TransGrp commit
`165fc21ff497b24b7a5975582b331e6692ba04f1`, and Scott's lemma,
Proc. Symp. Pure Math. 37 (1980), p.328,
DOI `10.1090/pspum/037/604599`.

The replay reconstructs all four wreath groups, their primitive six-point
quotients, and their index-five intermediate chains. It performs no
endpoint search. No owner, carrier/data bridge, payment, `u=2`, K3, or
KoalaBear-row closure is claimed.
