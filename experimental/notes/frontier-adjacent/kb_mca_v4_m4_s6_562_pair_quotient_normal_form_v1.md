---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The rigid inner-degree-4 passport S6:5.1,2.2.2,3.2.1 has an explicit rational degree-15 unordered-pair quotient, and its three order-five points split over the KoalaBear challenge field.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_S6_562_RIGID_PAIR_QUOTIENT
quantifier: the retained rigid S6 [5,6,2] passport up to source and target projectivity
projection_and_unit: outer-cover normal form and pole-field descent; not active-fiber, source-star, owner, or MCA-slope payment
claimed_bound: the second of three rigid m4 passports is explicit over Q and has a completely split three-point pole divisor over F_(2130706433^6)
status: PROVED_M4_S6_562_PAIR_QUOTIENT_AND_POLE_DESCENT_ACTIVE_FIBER_AND_SOURCE_STAR_OPEN
impact: LOCAL_ONLY
falsifier: failure of the pair-remainder identity, rational parameter, branch factorization, or even-extension pole descent
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_s6_562_pair_quotient_normal_form_v1.py --check --tamper-selftest
---

# KoalaBear rigid S6 [5,6,2] pair quotient

## 0. Verdict

Put

```text
A2=25444u^2-50922u+15129,
C3=14658356u^3-31403007u^2-8441982u+33495606,
C6=915512069923328u^6+6554290056691968u^5
   -83250949083482880u^4+290661295480797960u^3
   -474965645409866205u^2+379227334439635443u
   -119893424310248247.
```

The retained rigid passport `S6:5.1,2.2.2,3.2.1` has rational model

```text
T(u)=177147(188u-287)^5 A2(u)^5/(C3(u)C6(u)^2).
```

Direct subtraction gives

```text
numerator(T)-denominator(T)
=3125(88u+123)^2(89u-123)^3(208u-369)^6
       (683u-1107)^3(980u-1599).
```

Thus the fibers over `0,1,infinity` are

```text
(5,5,5), (6,3,3,2,1), (2,2,2,2,2,2,1,1,1).
```

## 1. Construction

The source is BelyiDB's rational companion
`6T16-[5,6,2]-51-321-222-g0`. Its unordered-pair remainder determinant is an
irreducible quintic. A cubic-adjoint pencil through the singular scheme, two
rational regular points, and the required infinitely-near tangent has five
fixed resultant factors and one moving factor linear in the pair coordinate.
Solving that moving factor produces the displayed rational parameter.

The certificate verifier does not trust the formula: it substitutes the
parameter into the pair quintic, reconstructs both degree-six remainder
ratios with exact polynomial arithmetic, and checks all branch factors and
coprimality.

## 2. Pole descent

The three order-five points are

```text
287/188,
(25461+7257 sqrt(5))/25444,
(25461-7257 sqrt(5))/25444.
```

The quadratic discriminant is `1053280980=14514^2*5`. It therefore splits
over the even extension `F_(2130706433^6)`. After the target transform `1/T`,
these are the required three pole points.

## 3. Source custody and scope

```text
BelyiDB commit: 7d5b899b0741ebd505363f7f811e5737e906abee
path: belyi_db/6/6T16-[5,6,2]-51-321-222-g0.m
blob: 94cff64a36672ba6bde9e6cbc1fa251230aa8001
```

This is an exact K3 input, not a row-paying atom. It does not identify a
split unramified active fiber, impose the quartic source-star incidence,
delete the `m=4` type, or pay an owner, ledger, endpoint, or KoalaBear row.
