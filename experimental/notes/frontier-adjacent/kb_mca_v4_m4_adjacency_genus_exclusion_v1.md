---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The sole inner-degree-4 transverse type is empty. Its r=8 outer component is the connected ordered-adjacency orbital on 120 pairs of two-subsets. Across the four exhaustive A6/S6 passports that orbital has genus 3,6,4,13, while the actual source has genus at most 3 and maps to it separably with degree 2.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_ADJACENCY_GENUS_EXCLUSION
quantifier: every actual inner-degree-4 transverse terminal in the imported four-passport A6/S6 frontier
projection_and_unit: exact outer-orbital genus contradiction; not a carrier, received-data, explaining-polynomial, or affine-slope owner
claimed_bound: all four m4 passports have no actual producer; the independent transverse frontier falls from 9 to 8 types in inner degrees 2 and 3
status: PROVED_M4_TRANSVERSE_ROW_EMPTY_EIGHT_LOWER_TYPES_OPEN
impact: CLOSES_INNER_DEGREE_4_AND_REMOVES_THE_FOUR_POINT_HURWITZ_FAMILY_WITHOUT_CONSTRUCTION
falsifier: a disconnected ordered-adjacency action, an incorrect induced branch index, source genus above three, component-to-image degree other than two, or inseparability
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_adjacency_genus_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-4 adjacency-genus exclusion

## 0. Verdict

The complete inner-degree-four transverse row is empty. The independent
frontier now consists of eight types:

```text
m=2: r=2,4,8
m=3: r=2,3,4,6,12.
```

No source-star coefficient incidence or construction of the four-point
Hurwitz family is needed for this deletion.

## 1. Imported geometry

The pinned source route starts with an actual outgoing component `H_0` of
bidegree `(u,2u)`. In the residual branch it maps birationally to the
bidegree-`(2u,2u)` endpoint self-correspondence component `Gamma`. At `u=2`,
the normalization therefore satisfies

```text
g(Gamma)=g(H_0)<=p_a(H_0)=(2-1)(4-1)=3.             (1.1)
```

The transverse compiler proves `delta*r=4m`. The outer route and passport
packets leave only `(m,r,delta)=(4,8,2)`, with outer monodromy `A6` or `S6`
on the 15 two-subsets of six letters, and exactly four branch passports.

## 2. Ordered adjacency orbital

The point stabilizer has subdegrees `1,6,8`. The size-eight relation pairs a
two-subset `A` with each `B` meeting it in one letter. Thus the outer
component `C` is the connected orbital cover on

```text
Omega={(A,B): |A|=|B|=2 and |A intersect B|=1},
```

which has `15*8=120` ordered states. The coordinates of the
self-correspondence are ordered; swapping them is an involution of `C`, not
an identification of its points.

Exact action of each letter class on `Omega` gives

```text
letter type       cycles on Omega       index
6                       20                100
5.1                     24                 96
4.2                     30                 90
3.2.1                   26                 94
2.1.1.1.1               72                 48
2.2.1.1                 60                 60
2.2.2                   60                 60.
```

The verifier reconstructs each row both by direct cycle traversal and by
Burnside averaging the fixed points of all powers.

## 3. Genus contradiction

Summing those indices over the exhaustive passports and applying
Riemann--Hurwitz to the connected degree-120 orbital cover gives

```text
passport                                      total index   genus(C)
S6: 5.1,2.1.1.1.1,6                              244           3
S6: 5.1,2.2.2,3.2.1                              250           6
A6: 5.1,2.2.1.1,4.2                              246           4
S6: 5.1,2.1.1.1.1,2.2.1.1,2.2.2                 264          13.
```

The challenge characteristic is `2130706433`, so the degree-two map
`Gamma -> C` is separable. Its Riemann--Hurwitz inequality is

```text
g(Gamma)>=2*g(C)-1.
```

The four required source genera are at least `5,11,7,25`, each contradicting
`(1.1)`. Hence every passport has no actual producer.

## 4. Scope

The three rigid normal forms remain exact constructions and descent
certificates, but they are not dependencies of this deletion. This packet
does not delete any inner-degree-two or inner-degree-three type, construct a
same-record carrier/data/slope owner, close `u=2`, K3, or the KoalaBear row,
or move any ledger quantity.
