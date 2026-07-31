---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: For inner degree 4, outer subdegrees 1,2,4 force the degree-15 outer map to decompose and route the endpoint to impossible inner degree 12 or 20. Only (r,delta)=(8,2) survives, with primitive outer monodromy A6 or S6 on the 15 two-subsets of six points.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_OUTER_A6S6_ROUTE_CUT
quantifier: every actual inner-degree-4 transverse terminal satisfying the imported source-pencil compiler
projection_and_unit: exact outer-monodromy route cut; not a carrier owner, received-line theorem, or slope payment
claimed_bound: three of four inner-degree-4 transverse types have no producer; the global independent frontier falls from 12 to 9 types
status: PROVED_M4_ONLY_R8_DELTA2_A6S6_OUTER_SURVIVES_OTHER_K3_ROWS_OPEN
impact: CUTS_M4_TO_ONE_A6S6_TWO_SUBSET_OUTER_TYPE
falsifier: a primitive degree-15 group with subdegree 1,2,4; another proper factor degree; or a valid inner-degree-12 or inner-degree-20 source profile
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_outer_a6s6_route_cut_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-4 outer route cut

## 0. Verdict

The four incoming types are

```text
(r,delta)=(1,16),(2,8),(4,4),(8,2).
```

The first three have no producer. Only `(8,2)` survives, and its outer
degree-15 monodromy is `A6` or `S6` on two-subsets. The independent
frontier is nine types: three at `m=2`, five at `m=3`, and this one at
`m=4`.

## 1. Primitive outer catalogue

Write `f=F composed h`, with `deg(h)=4` and `deg(F)=15`. The actual
component maps to an outer correspondence of bidegree `(r,r)`. If `F` is
indecomposable, that correspondence is a point-stabilizer suborbit in a
primitive degree-15 group. The complete catalogue is

```text
group                 nontrivial subdegrees
A7                    14
A6 on two-subsets     6,8
S6 on two-subsets     6,8
PSL(4,2)              14
A15                   14
S15                   14
```

No primitive row contains `1,2,4`. Those types force `F` to decompose.

## 2. Proper-factor route

A proper right factor of a degree-15 map has degree 3 or 5. Composing it
with `h` gives the endpoint an inner decomposition of degree 12 or 20.
Inner degree 12 is proved empty. Inner degree 20 violates the exhaustive
source/Riemann-Hurwitz profile: three exceptional four-point source fibers
would contribute `3*4*(5-1)=48`, above `2*20-2=38`.

Thus `r=1,2,4` are empty. For `r=8`, only the `A6,S6` two-subset actions
remain. Their point-stabilizer orbits have sizes `1,6,8`. A five-cycle
fixing the sixth point acts on the 15 pairs as `5^3`, so the inherited pole
profile does not delete the survivor.

## 3. Custody and scope

The exact classification source is GAP PrimGrp commit
`5612e113d50ac23a7d10945383936e20440b4e14`; its 894-byte degree-15 entry
has SHA-256
`d24658310cb386c9663e95ab9024eab9142d79f849131f499da36eeda82c003e`.

The replay reconstructs both two-subset actions and the `5^3` pole cycle.
The `(8,2)` survivor is not deleted or paid. No endpoint census, owner,
carrier/data bridge, `u=2`, K3, or KoalaBear-row closure is claimed.
