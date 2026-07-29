---
workboard_item: T
row: four Mersenne rows n=8(p+1), p in {8191,131071,524287,2147483647}
object: OTHER
target_epsilon: N/A
agreement: N/A
B_star: N/A
direct_statement: the order-one h=7 HNF stratum with a cubic color interpolant of multiplicity profile 3+3 is empty
architecture: DIRECT_LOCAL_HNF
partition_digest: N/A
atom_or_cell: L1 next-to-maximal order-one cubic 3+3 color stratum
quantifier: every saturated HNF packet on each of the four declared rows
projection_and_unit: split-pencil HNF passports
claimed_bound: zero packets in the declared stratum
status: PROVED
impact: LOCAL_ONLY
falsifier: a saturated packet satisfying the printed conic, HNF coefficients, norm-color equation, and cubic 3+3 factorization
replay: python3 experimental/scripts/verify_l1_m8_h7_order_one_cubic_33_exclusion.py
---

# L1 m=8, h=7 order-one cubic 3+3 exclusion

## Result

On each row

```text
(p,n)=(8191,65536),
      (131071,1048576),
      (524287,4194304),
      (2147483647,17179869184),
```

consider a saturated next-to-maximal order-one HNF packet with parameters

```text
d=c-1,       r=rho*c,       d*r*(r-1)!=0,
```

and monic reduced sextic

```text
L(W)=W^6+l_1W^5+...+l_6.
```

Assume its six roots have an exact cubic color interpolant and use two
colors three times each. Then no such packet exists.

This closes one exact local HNF stratum. It does not prove the bridge from
the current upstream first-match residual to this HNF chart, close another
color profile, pay an MCA/list atom, or move an adjacent safe row.

## HNF input

The h=7 residual conic is

```text
35d^2r^2+14d(11d^2+27d+27)r
 +120(d^4+4d^3+7d^2+6d+3)=0.                       (1)
```

Let `g` be the degree-seven hypergeometric polynomial before the affine
shift. Its value at one is

```text
g(1)=1+r S_1+r^2 S_2+r^3d^3/48,

S_1=(10d^5+62d^4+163d^3+237d^2+213d)/60,
S_2=d^2(13d^2+55d+76)/72.                           (2)
```

The reduced-sextic coefficients needed below are

```text
l_1=6/d,
l_2=(15+rd/2)/d^2,
l_3=(20+rd(d+8)/3)/d^3,
l_4=(15+rd(d^2+7d+23)/4+r^2d^2/8)/d^4,
l_5=-6g(1)/(d^5(r-1)).                              (3)
```

Every packet also has

```text
d^(p+1) in mu_8.                                    (4)
```

Equations (1)--(4) are the complete imported HNF interface used by this
note. The reduction from a full split pencil to that interface is not
re-proved here.

## Two full cubic fibers

Write the cubic interpolant as

```text
E(W)=e_3(W^3+uW^2+vW+w),       e_3!=0.
```

If the two colors are `alpha,beta`, each cubic `E-alpha` and `E-beta` has
exactly its corresponding three roots of `L`. Monicity and squarefreeness
give

```text
L=e_3^(-2)(E-alpha)(E-beta)=e^2-se+t,                (5)
```

where `e=E/e_3`. Comparing coefficients in (5) gives

```text
l_1=2u,
l_2=u^2+2v,
l_3=2w+2uv-s,
l_4=v^2+u(2w-s),
l_5=v(2w-s).                                        (6)
```

The `l_5` relation in (6), together with (2)--(3), expands after denominator
clearing to

```text
q_2r^2+q_1r+q_0=0,                                  (7)

q_2=5d^2(5d+7),
q_1=130d^4+540d^3+845d^2+480d,
q_0=120d^5+744d^4+1956d^3+2724d^2+2076d+720.
```

The unused `l_4` relation is stronger. Substituting (3) and the first three
relations in (6) gives

```text
rd(4(d^2+3d+3)+rd)=0.
```

Saturation therefore yields

```text
r=-4(d^2+3d+3)/d.                                   (8)
```

## Elimination and norm obstruction

Put

```text
s=d^2+3d+3,       S=2d^2+9d+9.
```

Substitution of (8) into (1) and (7) gives respectively

```text
32sS=0,
-8d(d+2)S=0.                                        (9)
```

If `S` were nonzero, (9) would force `s=0` and `d=-2`, while `s(-2)=1`.
Hence

```text
S=(2d+3)(d+3)=0.                                    (10)
```

Thus `d` is the base-field value `-3/2` or `-3`, with norm `9/4` or `9`.
Every declared prime is `7 mod 8`, so

```text
F_p intersect mu_8={1,-1}.
```

The value `9` can equal `1` or `-1` only in characteristic `2` or `5`; the
value `9/4` can do so only in characteristic `5` or `13`. None is a declared
characteristic. This contradicts (4) and proves the exclusion.

## Verification

The deterministic exact-rational verifier is

```text
experimental/scripts/verify_l1_m8_h7_order_one_cubic_33_exclusion.py
sha256: 8d49e0b87da9b842d4b827b7feae6718e3c0e9628e9a94d33cfc8b49e901c66f
```

It reconstructs the cleared second quadratic from the truncated logarithmic
coefficients, checks both substitution identities, checks all four row and
norm obstructions, and includes two mutation controls. Expected success
marker:

```text
L1_M8_H7_ORDER_ONE_CUBIC_33_EXCLUSION_PASS rows=4 identities=7 mutations=2
```

## Boundary

The exact conclusion is local to the printed HNF interface and the cubic
profile `3+3`. In particular, this note does not claim:

- exhaustiveness for the active KoalaBear or Mersenne first-match residual;
- a bound on distinct bad slopes or list codewords;
- emptiness of cubic profiles `3+2+1`, `2+2+2`, or profiles using more
  colors;
- emptiness of quadratic or degree-four-and-higher color strata;
- a cyclotomic converse or an inner split-pencil lift;
- movement of any deployed safe/unsafe endpoint.

The remaining upstream bridge is to place this HNF cell inside an exhaustive
source-bound owner partition before treating it as a bankable route cut.
