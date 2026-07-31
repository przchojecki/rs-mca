---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The surviving inner-degree-4 outer A6/S6 type has exactly four geometric genus-zero passports: three three-point covers and one four-point cover.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_A6S6_GENUS_ZERO_PASSPORT_REDUCTION
quantifier: every geometric degree-15 rational outer map in the imported A6/S6 two-subset survivor with the prescribed 5^3 pole cycle
projection_and_unit: exact geometric passport classification; not a field-descent, source-star, owner, or slope payment
claimed_bound: nine index-compatible class budgets reduce to four generating passports
status: PROVED_M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS_FIELD_AND_SOURCE_INCIDENCE_OPEN
impact: NARROWS_SOLE_M4_TYPE_TO_THREE_RIGID_COVERS_AND_ONE_HURWITZ_FAMILY
falsifier: another parity-compatible residual index-16 budget, a deleted budget generating A6/S6, or a retained tuple failing to generate the printed group
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.py --check --tamper-selftest
---

# KoalaBear inner-degree-4 genus-zero passport reduction

## 0. Verdict

The sole inner-degree-four outer `A6/S6` type from the parent route cut is
not an arbitrary degree-15 map. Its complete geometric passport frontier is

```text
A6:  5.1, 2.2.1.1, 4.2
S6:  5.1, 2.1.1.1.1, 2.2.1.1, 2.2.2
S6:  5.1, 2.1.1.1.1, 6
S6:  5.1, 2.2.2, 3.2.1
```

The first, third, and fourth rows are three-point covers. The second is a
four-point cover.

## 1. Complete class and tuple census

Riemann--Hurwitz gives total branch index `28`. The mandatory `5^3` pole
cycle costs `12`, leaving `16`. Reconstructing all 11 conjugacy classes of
`S6` and their action on the 15 two-subsets leaves nine parity-compatible
class multisets at residual index 16.

Fixing the pole cycle, enumerate every prefix in each class multiset and
derive the last cycle from product one. The largest row has only
`15^3=3375` prefixes. Five budgets generate only proper groups of order 60
or 120. The four rows above generate `A6` or `S6`; both split `A6` 5-cycle
classes give the same verdict.

## 2. Scope

Riemann existence converts the four generating tuples into the exact
geometric genus-zero frontier. This does not provide a model over the
challenge field, split the three pole points or a 15-point unramified zero
fiber, impose the quartic source-star correspondence, delete the remaining
`m=4` type, or pay any owner or ledger quantity.

The next finite target is the three rigid three-point covers. The four-point
Hurwitz family should be attacked only after those field and source-incidence
tests are compiled.
