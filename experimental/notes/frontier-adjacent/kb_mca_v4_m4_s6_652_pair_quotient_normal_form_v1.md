---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The rigid inner-degree-4 passport S6:5.1,2.1.1.1.1,6 has an explicit rational degree-15 unordered-pair quotient, and its three order-five points split over the KoalaBear challenge field.
architecture: null
partition_digest: null
atom_or_cell: K3_M4_S6_652_RIGID_PAIR_QUOTIENT
quantifier: the unique geometric rigid cover in the retained S6 [6,5,2] passport, up to source and target projectivity
projection_and_unit: outer-cover normal form and pole-field descent; not active-fiber, source-star, owner, or MCA-slope payment
claimed_bound: one of three rigid m4 passports is explicit over Q and has a completely split three-point pole divisor over F_(2130706433^6)
status: PROVED_M4_S6_652_PAIR_QUOTIENT_AND_POLE_DESCENT_ACTIVE_FIBER_AND_SOURCE_STAR_OPEN
impact: LOCAL_ONLY
falsifier: failure of the pair-remainder determinant, rational normalization, branch factorization, or even-extension pole descent
replay: python3 experimental/scripts/verify_kb_mca_v4_m4_s6_652_pair_quotient_normal_form_v1.py --check --tamper-selftest
---

# KoalaBear rigid S6 [6,5,2] pair quotient

## 0. Verdict

The retained rigid passport

```text
S6: 5.1, 2.1.1.1.1, 6
```

has an explicit rational degree-15 model. Put

```text
Q4=u^4+176u^3+14520u^2+660176u+12576619,
Q6=u^6-330u^5+22143u^4+3380740u^3
   -372423117u^2-39333485730u-870224422859.
```

Then

```text
T(u)= -9566429400000 (u+44)^6 (u+55)^3
      / ((u+143) Q4(u)^2 Q6(u)),

T(u)-1= -(u+77)^5 (u^2-44u-4961)^5
         / ((u+143) Q4(u)^2 Q6(u)).
```

The fibers over `0,1,infinity` are respectively

```text
(6,6,3), (5,5,5), (2,2,2,2,1,1,1,1,1,1,1).
```

## 1. Unordered-pair construction

The source is BelyiDB's rational degree-six companion
`6T16-[6,5,2]-6-51-21111-g0`, pinned below. For an unordered pair of roots,
write `X^2-yX+z`. Reducing the numerator and denominator of the degree-six
map modulo this quadratic and setting the two remainder vectors proportional
gives an irreducible plane quintic.

The parent packet has exactly five generating tuples after fixing the
5-cycle. Its order-five centralizer acts freely on those five tuples, so they
form one simultaneous-conjugacy class. The printed map therefore represents
the retained rigid cover, not an unclassified extra component.

Projection from its rational triple point by `z=my` leaves a quadratic in
`y` with discriminant

```text
2^20 m^2 (11m+16)^4 (3025m^2-2816m+1024).
```

The residual conic has point `(m,w)=(0,32)` and the rational parametrization

```text
m=-64(u+44)/((u-55)(u+55)).
```

Substitution and exact cancellation give the displayed degree-15 map. The
certificate verifier reconstructs this route with `Fraction` polynomial and
rational-function arithmetic rather than trusting the printed formula.

## 2. Pole descent

After the target transform `T/(T-1)`, the pole points are

```text
-77, 22+33 sqrt(5), 22-33 sqrt(5).
```

The quadratic discriminant is `21780=66^2*5`. Every base-field unit is a
square in the even extension `F_(p^6)`, and `p=2130706433` divides none of
`2,3,5,11`. Hence all three points are distinct and rational over the
KoalaBear challenge field.

## 3. Source custody and scope

```text
BelyiDB commit: 7d5b899b0741ebd505363f7f811e5737e906abee
path: belyi_db/6/6T16-[6,5,2]-6-51-21111-g0.m
blob: 454b284b8d09d855b1fde5c86dac2c28859f0f67
```

This closes coefficient construction and pole descent for one rigid
passport. It does not identify a completely split unramified active fiber,
impose the fixed quartic source-star incidence, delete the `m=4` type, or pay
an owner, ledger, endpoint, or KoalaBear row.
