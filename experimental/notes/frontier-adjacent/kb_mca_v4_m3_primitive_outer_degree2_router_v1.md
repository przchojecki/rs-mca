---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Every inner-degree-3 transverse producer is impossible or also gives the endpoint an inner-degree-2 decomposition. The complete primitive degree-20 catalogue is two-transitive and has no required outer subdegree; all proper-factor destinations are closed or route to degree 2.
architecture: null
partition_digest: null
atom_or_cell: K3_M3_PRIMITIVE_OUTER_DEGREE2_ROUTER
quantifier: every actual inner-degree-3 transverse terminal in the imported eight-type frontier
projection_and_unit: exact geometric decomposition router; not nonexistence of every degree-3 decomposition and not a carrier/data/slope payment
claimed_bound: all five m3 types cease to be independent producers; the independent transverse frontier falls from 8 to the three m2 types
status: PROVED_M3_NO_INDEPENDENT_PRODUCER_ROUTES_TO_M2
impact: REDUCES_THE_COMPLETE_INDEPENDENT_TRANSVERSE_FRONTIER_TO_M2
falsifier: a missing primitive degree-20 group, a primitive subdegree 2,3,4,6,12, another proper factor degree, or an unhandled degree-6,12,15,30 destination
replay: python3 experimental/scripts/verify_kb_mca_v4_m3_primitive_outer_degree2_router_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-3 primitive-outer router

## 0. Verdict

Inner degree three is not an independent producer. Every actual `m=3`
producer is impossible or also supplies an inner-degree-two decomposition of
the same endpoint. The independent transverse frontier is

```text
m=2: (r,delta)=(2,4),(4,2),(8,1).
```

This is a routing statement, not nonexistence of every degree-three
decomposition.

## 1. Primitive outer exclusion

For `m=3`, the outer map has degree `20` and the transverse compiler gives

```text
(r,delta)=(2,6),(3,4),(4,3),(6,2),(12,1).
```

If the outer map were indecomposable, its primitive geometric monodromy
would need point-stabilizer subdegree `r`. The complete degree-20 GAP
`PrimGrp` entry is

```text
group          order          subdegrees
PSL(2,19)       3420             1,19
PGL(2,19)       6840             1,19
A20             20!/2            1,19
S20             20!              1,19.
```

No row contains a required subdegree. The verifier reconstructs both
projective-line actions, their orders and subdegrees, and a compatible
`5^4` pole cycle without GAP. Completeness is pinned to PrimGrp commit
`5612e113d50ac23a7d10945383936e20440b4e14`, where the exact 342-byte
`PRIMGRP[20]` entry has SHA-256
`cbc9ca7fda9b0de36a4034a4d59e24bb6c07aff0e54458604990919583007133`.

## 2. Composite destinations

The outer map therefore has a proper right factor `q`. Since its degree is
20,

```text
deg(q)                  2       4       5       10
deg(q composed h)       6       12      15      30.
```

The exact parent terminals handle all four columns:

- `m=6` is impossible through degree five or routes to `m=2`;
- `m=12` is empty;
- `m=15` is excluded by the source/Riemann--Hurwitz profile;
- `m=30` refines to `m=6`, hence routes to `m=2` or is empty.

Thus no `m=3` row remains an independent terminal.

## 3. Scope

The certificate binds all five parent terminals by exact commit, Git blob,
and canonical payload. It does not assert that an endpoint lacks an
additional degree-three decomposition, delete or pay a degree-two row,
construct a carrier/data/explaining-polynomial/slope owner, close `u=2`,
K3, or the KoalaBear row, or move any ledger quantity.
