---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The common six-pole divisor and forced source-cover branch pair are incompatible with every degree-six dihedral coordinate, so the residual n=6 profile is empty.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE6_COMMON_POLE_EXCLUSION
quantifier: every actual full-V4 residual n=6 profile
projection_and_unit: exact projective binary-sextic fibers and quadratic source-cover branch matching; not a carrier, slope, or payment count
claimed_bound: n=6 is empty and n=3 is the sole residual full-V4 dihedral factor degree
status: PROVED_M2_R2_DIHEDRAL_DEGREE6_COMMON_POLE_EXCLUSION
impact: DELETES_ONE_OF_TWO_RESIDUAL_FULL_V4_DIHEDRAL_PROFILES
falsifier: a missing common-pole projective class, a vanishing KoalaBear exceptional resultant, or a surviving source-cover twist
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree6_common_pole_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear degree-six common-pole exclusion

## 0. Verdict

In the `n=6` profile all six poles of the common degree-30 function are one
unramified fiber of each degree-six dihedral quotient. The complete
projective atlas of two such fiber structures is finite. None is compatible
with the already-forced source-cover branch pair. Therefore `n=6` is empty,
and only `n=3` remains in the full-V4 dihedral frontier.

## 1. Common pole sextic

Normalize

```text
D_6(x)=x^6-6x^4+9x^2-2,
P_c(x)=x^6-6x^4+9x^2-c,       c notin {0,4}.
```

The internal involution `i(x)=-x` is fixed-point-free on the six roots of
`P_c`. If `ell` is the relative second quotient coordinate, then
`j=ell*i*ell^(-1)` is a second fixed-point-free involution on the same six
poles. Their two perfect matchings either coincide, share one edge and
generate `V4`, or share no edge and generate `S3`.

### Coincident matchings

The normalizer of `x -> -x` consists of `s*x` and `s/x`. Comparing the four
even coefficients of two Dickson-six fibers gives

```text
ell=s*x: s^2=1 and c'=c;
ell=s/x: s^2=9/4 and c=c'=27/8.
```

Thus `ell` is `+/-x`, with `+/-3/(2x)` as the only reciprocal exception.

### Distinct commuting matchings

A distinct commuting involution is `j(x)=k/x`. Fiber invariance forces
`k^2=9/4,c=27/8`. The sign `k=3/2` fixes two pole roots and is not an
unramified second fiber. For `k=-3/2`, conjugating `j` to sign pulls the
sextic back, up to scalar, to

```text
5z^6+11z^4+11z^2+5.
```

A scaled Dickson-six fiber satisfies `B^2=4AC` in its four even
coefficients, or `C^2=4BD` after inversion. Here both comparisons are
`121!=220`, so no second Dickson-six structure exists.

### Order-three matchings

Put `g=ij`. The relation `igi=g^(-1)` and scalar matrix freedom give

```text
g_t(x)=t(x+t)/(t-3x).
```

Writing `s=t^2`, the three odd transformed coefficients are

```text
3c+s^3+2s^2-15s,
135c+5s^3-6s^2-27s,
243c+s^3-30s^2+81s.
```

They force `(s-3)(5s+27)=0`. The first root is the ramified fiber `c=0`.
The unramified case is

```text
t^2=-27/5,       c=756/125,
ell in {+/-g_t,+/-g_t^2}.
```

Direct substitution replays the complete sextic identity.

## 2. Source-cover contradiction

For `n=6`, the source-cover classifier has `a=1,d^2=3` and requires

```text
ell^(-1)({2,b})=roots(z^2-b*d*z+b^2-1).             (1)
```

For `ell=+/-z`, coefficient comparison gives both
`b^2-2b-1=0` and `b^2-2b-2=0`.

For `ell=+/-3/(2z)`, equation `(1)` gives

```text
8b(b^2-1)-9=0,
16b^4-3(b+2)^2=0,
```

whose resultant is `22371648`, nonzero in KoalaBear characteristic.

For `ell=g_t`, eliminate `d` from the middle coefficient of `(1)` using
`d^2=3`. After `5t^2+27=0`, this gives

```text
H(b)=(-900t-2295)b^4+(3240-1530t)b^3
     +(1260t-459)b^2+(2088t-2592)b
     +1296t-2268/5.
```

The constant coefficient gives

```text
E(b)=(25t+150)b^3+(50t-45)b^2
     +(-70t-60)b-140t-198.
```

Their resultant reduces to

```text
76527504000(1472792180t+1585334079).
```

The primitive factor has norm

```text
71132574457861006005
  =1274367339 mod 2130706433 != 0.
```

The other three order-three coordinates are obtained by `t -> -t` and/or
`d -> -d`. Hence all four fail.

## 3. Scope

This packet deletes `n=6` only. It does not construct or delete `n=3`,
close the full-V4 type or K3, construct an owner, move a payment, close the
KoalaBear row, or resolve either Prize problem.
