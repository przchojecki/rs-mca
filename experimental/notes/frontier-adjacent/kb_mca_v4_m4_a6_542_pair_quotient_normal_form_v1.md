---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The rigid inner-degree-4 passport A6:5.1,2.2.1.1,4.2 has an explicit degree-15 unordered-pair quotient over Q(nu), and its three order-five points split over the KoalaBear challenge field.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_A6_542_RIGID_PAIR_QUOTIENT
quantifier: the retained rigid A6 [5,4,2] passport up to source and target projectivity
projection_and_unit: outer-cover normal form and pole-field descent; not active-fiber, source-star, owner, or MCA-slope payment
claimed_bound: the third of three rigid m4 passports is explicit over Q(nu) and has a completely split three-point pole divisor over F_(2130706433^6)
status: PROVED_M4_A6_542_PAIR_QUOTIENT_AND_POLE_DESCENT_ACTIVE_FIBER_AND_SOURCE_STAR_OPEN
impact: LOCAL_ONLY
falsifier: failure of the source pair-remainder identity, branch factorization, or either-embedding field descent
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_a6_542_pair_quotient_normal_form_v1.py --check --tamper-selftest
---

# KoalaBear rigid A6 [5,4,2] pair quotient

## 0. Verdict

Work over `E=Q(nu)`, `nu^2-nu+4=0`. Put

```text
L =26828299u-7525603+3231308nu,
A2=63975032888671u^2+(-824138157082+7855063570280nu)u
   +245313368811+2125523128760nu.
```

The retained rigid passport `A6:5.1,2.2.1.1,4.2` has exact model

```text
T(u)=c L(u)^5 A2(u)^5/(P1(u)P2(u)Q2(u)^2Q4(u)^2),
```

where the nonzero scalar and four denominator factors are printed in the
certificate. Exact subtraction factors, up to a nonzero scalar, as

```text
R1 R2^2 S1^4 S2^4
```

with factor degrees `1,1,1,2`. Thus the fibers over `0,1,infinity` are

```text
(5,5,5), (4,4,4,2,1), (2,2,2,2,2,2,1,1,1).
```

## 1. Construction

The source is BelyiDB's companion
`6T15-[5,4,2]-51-42-2211-g0` over `Q(nu)`. Its unordered-pair remainder
determinant is an irreducible quintic. A rank-eight cubic-adjoint system,
including two infinitely-near tangent conditions, has one moving factor
linear in each pair coordinate. Solving the two moving factors gives a
degree-five rational parameter.

The verifier is import-free and does not trust the displayed outer map. It
implements exact arithmetic in `Q(nu)`, reconstructs the compact pair
parameter, reduces the pinned degree-six numerator and denominator modulo
`X^2-yX+z`, and proves that both remainder ratios equal the displayed `T`.
It then checks the `T-1` identity, squarefreeness, coprimality, and
Riemann--Hurwitz.

## 2. Pole descent

For `p=2130706433`, both roots of `nu^2-nu+4` lie in `F_p`. Under both
embeddings, the quadratic factor `A2` is separable and does not meet `L`.
Its roots lie in `F_(p^2)`, hence in `F_(p^6)`. After the target transform
`1/T`, these are the required three pole points.

## 3. Source custody and scope

```text
BelyiDB commit: 7d5b899b0741ebd505363f7f811e5737e906abee
path: belyi_db/6/6T15-[5,4,2]-51-42-2211-g0.m
blob: 55e23bc1ef1d939329a5a6b377d03c07f0ac9f2d
```

This completes construction and pole descent for all three rigid `m=4`
passports. It does not identify a split unramified active fiber, impose the
quartic source-star incidence, delete the `m=4` type, or pay an owner,
ledger, endpoint, or KoalaBear row.
