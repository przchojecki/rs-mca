---
workboard_item: T
row: four Mersenne rows n=8(p+1), p in {8191,131071,524287,2147483647}
object: OTHER
target_epsilon: N/A
agreement: N/A
B_star: N/A
direct_statement: exact p-free reductions for the order-one h=7 cubic 2+2+2 and 3+2+1 color profiles
architecture: DIRECT_LOCAL_HNF
partition_digest: N/A
atom_or_cell: L1 next-to-maximal order-one cubic 2+2+2 and 3+2+1 strata
quantifier: every saturated HNF packet in either declared multiplicity profile
projection_and_unit: split-pencil HNF passports
claimed_bound: necessary finite or four-variable endpoints; no zero-packet claim
status: PROVED
impact: LOCAL_ONLY
falsifier: a packet in either profile violating one of the printed factor or coefficient identities
replay: python3 experimental/scripts/verify_l1_m8_h7_order_one_cubic_profile_reductions.py
---

# L1 m=8, h=7 order-one cubic profile reductions

## Scope

This note sharpens two cubic-color strata in the same local HNF chart as the
companion `3+3` exclusion. It proves algebraic reductions, not emptiness:

```text
2+2+2: one quadratic and two linear remainders in one variable;
       both exceptional slopes reduce to fixed norm polynomials;
3+2+1: an exact common-quadratic factor model with four retained variables.
```

The upstream first-match-to-HNF owner bridge remains outside the note. None
of these reductions pays a deployed row atom or moves an endpoint.

## Shared HNF interface

Put `d=c-1`, `r=rho*c`, and `q=dr`. The inherited saturation includes

```text
d*q*(q-d)*g(1)!=0.
```

The scaled reduced-sextic coefficients are

```text
L_j=d^j l_j,
L_1=6,
L_2=15+q/2,
L_3=20+q(d+8)/3,
L_4=15+q(d^2+7d+23)/4+q^2/8,
L_5=-6dG/(q-d),
L_6=G,                                               (1)

G=1+q(10d^4+62d^3+163d^2+237d+213)/60
    +q^2(13d^2+55d+76)/72+q^3/48.                  (2)
```

The residual conic is `C_0=0`, where

```text
35q^2+14q(11d^2+27d+27)
 +120(d^4+4d^3+7d^2+6d+3)=0.                       (3)
```

Every packet also has `d^(p+1) in mu_8`.

## The 2+2+2 factor model

Let the monic cubic color interpolant be `e=W^3+UW^2+VW+w`. If its three
colors each occur twice, the corresponding quadratic fibers are

```text
F_i=W^2+u_iW+u_i^2-Uu_i+V,
L=F_1F_2F_3.                                        (4)
```

Let `s_2` be the second elementary symmetric function of the `u_i`, and use
the dimensionless variables

```text
a=dU,       b=d^2s_2,       x=a-3.                 (5)
```

After the first three coefficient equations eliminate the other symmetric
functions, define

```text
H=x^2-8-q/6,
K=48-12x^2+q(-d^2-3d+5)/4-q^2/24,
D_b=b^2+3Hb+3K,                                    (6)

B_5=12x^3+6
    +q(d^2+5d+11+(1-d^2-3d)x-(d+2)x^2)/2
    +q^2(d+5-x)/12,
A_5=-x(x^2+q/6).                                   (7)
```

The fourth and fifth coefficient equations are exactly

```text
D_b=0,
M_5=(q-d)(A_5b+B_5)+6dG=0.                         (8)
```

For the sixth coefficient put

```text
k=6x-3+q/2,
t_0=12x-16-q(d+2)/6,
t_1=2-x,
P_0=-x^3+3x^2+30+(x-1)q/2,
m=x^2-9,
N=18-6x,

C_3=4/27,
C_2=(4x^2-2x-15)/3,
C_1=-2xt_0+t_1P_0+km/3+(2kN-k^2)/9,
C_0=t_0^2+t_0P_0+k^2N/9+k^3/27,

A_6=C_1+4H^2/3-4K/9-3HC_2,
B_6=C_0+4HK/3-3KC_2-G.                             (9)
```

Reduction by `D_b` turns the sixth equation into

```text
M_6=A_6b+B_6=0.                                    (10)
```

Thus the p-free core is the conic, one quadratic in `b`, and two equations
linear in `b`. Since `q-d` is saturated, the fifth-equation slope vanishes
only on

```text
x=0                  or                  q=-6x^2.   (11)
```

Off (11), `M_5` determines `b` and leaves a three-variable elimination.

## First exceptional slope: x=0

At `x=0`, put

```text
A=11d^2+27d+27,
B=d^4+4d^3+7d^2+6d+3,
C=13d^2+34d+33,
D=5d^4+21d^3+37d^2+32d+15,
P=5d^3+16d^2+18d+10.                               (12)
```

Then

```text
M_5=q(d+2)J/120,
J=25q^2+10Cq+24D,                                  (13)

25C_0-35J=-10(2d+3)(35(d+2)q+12P).                (14)
```

The isolated values `d=-2,-3/2,-3` have base-field norms `4,9/4,9` and
violate the eighth-root norm condition on all four rows. Every other
survivor has

```text
q=-12P/(35(d+2)),
P_5(d)=60d^5+407d^4+1147d^3+1659d^2+1218d+360=0.  (15)
```

Hence unit gcds of `P_5` against all official norm fibers close the complete
`x=0` branch.

## Second exceptional slope: q=-6x^2

Put `y=x^2` and

```text
s=d^2+3d+3,       u=d^2+2d+2.
```

The conic and fifth equation reduce to

```text
C_y=105y^2-7Ay+10B=0,
(d+6y)(5x(s-y)+2(d+2)u)=0.                         (16)
```

The first factor is `d-q` and is saturated. Squaring the other factor gives

```text
Q_y=25y(s-y)^2-4(d+2)^2u^2=0.                     (17)
```

Define

```text
E=14(2d^2+9d+9)^2-75B,
F=5B(19d^2+63d+63)-126(d+2)^2u^2.                 (18)
```

Exact quadratic reduction gives

```text
rem_(C_y)(Q_y)=2(Ey+F)/63.                         (19)
```

Therefore every survivor is a root of

```text
R_12(d)=105F^2+7AFE+10BE^2.                        (20)
```

This polynomial has degree 12 and leading coefficient `149868`. Unit norm
gcds of `R_12` close the complete `q=-6x^2` branch. Equation (17) was obtained
by a necessary squaring, so a nonunit root must return to (16).

## Aggregate norm request

The bounded launcher

```text
experimental/scripts/l1_m8_h7_cubic_222_norm_endpoints_modal.py
```

computes, for `P_5` and `R_12` on every declared prime,

```text
gcd(P(X),X^(8(p+1))-1) over F_p.                   (21)
```

Because the product over `zeta in mu_8` of `X^(p+1)-zeta` is the second
polynomial in (21), a unit aggregate gcd is equivalent to all eight
individual norm-color gcds being unit after adjoining `mu_8`. The launcher
uses one 512 MB container, one CPU, a 60-second timeout, and prints each of
its eight rows immediately. It is a compute request, not evidence in this
PR.

## The 3+2+1 common quadratic

Let `F` be the monic cubic triple-color factor, `G=L/F`, and normalize its
values on the roots of `G` to `B,B,lambda B`, where

```text
lambda=(gamma-alpha)/(beta-alpha).
```

Exact double multiplicity gives a common monic quadratic:

```text
Q=W^2+uW+v,
G=Q(W)(W-y),
F-B=Q(W)(W-z).                                     (22)
```

Put `a=y-z`. Then `a!=0`,

```text
F=G+aQ+B,
aQ(y)=(lambda-1)B.                                 (23)
```

Write `G=W^3+g_1W^2+g_2W+g_3`. The factor equations are

```text
u=g_1+y,
v=g_2+g_1y+y^2,
g_3=-vy.                                           (24)
```

From `L=G^2+aQG+BG`, the first three coefficients solve

```text
a=l_1-2g_1,
g_2=(l_2-g_1^2-a(2g_1+y))/2,
B=l_3-2g_3-2g_1g_2-a(v+ug_1+g_2).                (25)
```

The retained equations are

```text
l_4=g_2^2+2g_1g_3+a(vg_1+ug_2+g_3)+Bg_1,
l_5=2g_2g_3+a(vg_2+ug_3)+Bg_2,
l_6=g_3^2+avg_3+Bg_3,                              (26)

a(3y^2+2g_1y+g_2)=(lambda-1)B,                    (27)
```

together with the conic. After (24)--(25), these are five equations in only
`(g_1,y,r,d)` for each fixed role value `lambda`. The seven cyclic color-set
orbits and six multiplicity-role assignments give at most 42 role packets.

## One polynomial for all 3+2+1 roles

The 42 role inputs need not be specialized separately. Put

```text
C(U)=(U^8-1)/(U-1)=U^7+...+U+1
```

and define

```text
R(lambda)=Res_U(C(U),C(1+lambda(U-1))),
Lambda_321(lambda)=R(lambda)/(lambda-1)^7.          (28)
```

The seven roots of `C` are the nontrivial eighth roots. For fixed `u`, the
seven roots in `lambda` correspond to the seven possible nontrivial colors
`v=1+lambda(u-1)`. The forbidden diagonal choice `v=u` gives one simple
root `lambda=1`; separability makes its total multiplicity exactly seven.
Thus `R` has degree 49 and `Lambda_321` has degree 42. After squarefree
reduction its roots are exactly all distinct ordered role ratios modulo
common color scaling.

Adjoin `Lambda_321(lambda)=0` to (24)--(27), perform the common-quadratic
elimination once with symbolic `lambda`, and factor retained lambda
components only afterward.

## Verification

The exact-rational identity checker is

```text
experimental/scripts/verify_l1_m8_h7_order_one_cubic_profile_reductions.py
sha256: 4124a850994b029403317f818e874616d7b3831b709e4aa7aa5f4ebfbbda9abb
```

Its expected marker is

```text
L1_M8_H7_ORDER_ONE_CUBIC_PROFILE_REDUCTIONS_PASS linear_samples=2 x0_samples=3 q6x2_samples=3 common_quadratic=1 role_polynomial=1
```

The bounded compute-request launcher has SHA-256

```text
d3b4aacf170e13fecdf36718f8566bd597beacf4965aa1584077dbe61db9f695
```

Pass `--output PATH` to bank the eight-row remote return. Validate an
all-unit certificate with

```text
python3 experimental/scripts/check_l1_m8_h7_cubic_222_norm_certificate.py PATH
sha256: 9ba5e7ee7a66d459453f5aba312fff5649c7ee37c12264b39d29304ebc8d244f
```

Neither script was executed in the exporting environment: project policy
sends computation to Modal, and the configured Modal workspace is currently
spend-blocked. The written proofs and scripts are available for independent
replay; no pending execution is counted as evidence.

## Boundary

This note does not claim:

- a unit norm gcd for `P_5` or `R_12`;
- emptiness of the generic `2+2+2` branch or any `3+2+1` role;
- coverage of four-, five-, or six-color cubic profiles;
- the upstream first-match-to-HNF owner bridge;
- an assignment-preserving Frobenius converse or inner split-pencil lift;
- payment of a LIST/MCA atom or movement of an adjacent endpoint.
