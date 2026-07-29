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
claimed_bound: necessary finite or overdetermined low-variable endpoints; no zero-packet claim
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
       the generic core has an exact seven-shape affine-color equation;
3+2+1: an exact common-quadratic factor model with four retained variables
       and one degree-42 symbolic role polynomial.
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

The role polynomial itself has a small rational factorization. Put

```text
A=lambda^2-lambda+1,
B=(lambda+1)(2lambda-1)(lambda-2).
```

Then `Lambda_321` is a nonzero rational scalar multiple of

```text
(B^2+50A^3)
(B^4-224B^2A^3-578A^6)
(B^4-4B^2A^3+54A^6)
(125B^4-2404B^2A^3+13448A^6).                     (28a)
```

The factor degrees are `6,12,12,12`. This is the homogenization of the
seven affine-shape polynomial (32) under `T=B^2/A^3`; identity
`4A^3-B^2=27lambda^2(lambda-1)^2` prevents an extra `A=B=0` root. Thus the
common-quadratic core has four rational role packets preserving all 42
ordered roles with multiplicity.

The role variable can be removed before elimination. In (27), put

```text
R=a(3y^2+2g_1y+g_2),  S=B,
A_0=S^2+RS+R^2,
B_0=(2S+R)(S+2R)(R-S).                             (28b)
```

Since `R*S!=0`, equation (27) is equivalent to `lambda=1+R/S`, and

```text
A(lambda)=A_0/S^2,  B(lambda)=B_0/S^3.             (28c)
```

Thus the four welded role equations are

```text
B_0^2+50A_0^3=0,
B_0^4-224B_0^2A_0^3-578A_0^6=0,
B_0^4-4B_0^2A_0^3+54A_0^6=0,
125B_0^4-2404B_0^2A_0^3+13448A_0^6=0.             (28d)
```

After (24)--(25), each line of (28d) gives one explicit system in
`(g_1,y,r,d)`: equations (26), the conic, and that role equation. Clearing
`S^6` or `S^12` is reversible on the inherited `B!=0` saturation.

The role polynomial has a second exact rational factorization that lowers
the degree of each branch. Let `zeta` be a primitive eighth root. The Galois
group `{1,3,5,7}` acts on ordered exponent pairs by
`(a,b)->(ka,kb) mod 8`, and the normalized role is

```text
lambda_(a,b)=(zeta^b-1)/(zeta^a-1),
1<=a,b<=7, a!=b.                                  (28e)
```

The 42 ordered pairs split into three orbits of size two and nine of size
four, represented by

```text
(2,6),(2,4),(4,2),
(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,1),(2,3),(4,1).
```

Their orbit polynomials, in that order, are

```text
X^2+1,
X^2-2X+2,
2X^2-2X+1,
X^4-4X^3+6X^2-4X+2,
X^4-4X^3+8X^2-4X+1,
X^4-4X^3+12X^2-16X+8,
X^4+6X^2+1,
X^4+2X^2-4X+2,
X^4+1,
2X^4-4X^3+6X^2-4X+1,
2X^4-4X^3+2X^2+1,
8X^4-16X^3+12X^2-4X+1.                          (28f)
```

Their degrees total `3*2+9*4=42`, and their product is a nonzero rational
scalar multiple of both `Lambda_321` and (28a). For a degree-`e_j` packet
`P_j`, put

```text
widehat P_j(R,S)=S^e_j P_j(1+R/S).                (28g)
```

On `R*S!=0`, the union of the four systems (28d) is equivalently the
**disjunction** of the twelve systems

```text
widehat P_j(R,S)=0,  1<=j<=12.                    (28h)
```

Each branch consists of (26), the conic, and one degree-at-most-four role
equation. The equations in (28h) are alternatives, never twelve
simultaneous constraints. Irreducibility of the displayed packets is not
needed or claimed.

On the four official characteristics, every role equation can be made
quadratic over the base field. Indeed `p=7 mod 8`, so fix `s in F_p` with
`s^2=2`. In the shifted variable `T=lambda-1`, the three rational
quadratics are

```text
T^2+2T+2,       T^2+1,       2T^2+2T+1.            (28i)
```

The nine quartics in (28f) split into the following conjugate pairs:

```text
T^2+sT+1,                       T^2-sT+1,
T^2+sT+2-s,                     T^2-sT+2+s,
T^2+3+2s,                       T^2+3-2s,
T^2+2T+4+2s,                    T^2+2T+4-2s,
T^2+(2+s)T+3+2s,                T^2+(2-s)T+3-2s,
T^2+(2+s)T+2+s,                 T^2+(2-s)T+2-s,
2T^2+2T+2+s,                    2T^2+2T+2-s,
2T^2+(2+2s)T+2+s,               2T^2+(2-2s)T+2-s,
4T^2+(4+2s)T+2+s,               4T^2+(4-2s)T+2-s.   (28j)
```

For the first six lines, each pair product equals `P_j(1+T)`; for the last
three it equals `2P_j(1+T)`. The scalar two is a unit. Thus the complete
role layer is also the disjunction of 21 systems obtained by homogenizing
(28i)--(28j) at `T=R/S`.

These quadratics are irreducible over every official `F_p`. For a normalized
role `lambda=(gamma-1)/(beta-1)`, Frobenius inversion gives

```text
lambda^p=(beta/gamma)lambda.                         (28k)
```

Since the role is nonzero and `beta!=gamma`, it cannot lie in `F_p`.
Consequently the 21 factors are exactly the Frobenius-pair packets. Changing
`s` to `-s` merely swaps the two factors on each line.

The official quadratic systems admit a compact dimensionless form. Put

```text
x=dg_1, Y=dy, q=dr, A=6-2x, U=x+Y,
L_2=15+q/2,
L_3=20+q(d+8)/3,
L_4=15+q(d^2+7d+23)/4+q^2/8,
K_6=1+q(10d^4+62d^3+163d^2+237d+213)/60
       +q^2(13d^2+55d+76)/72+q^3/48.              (28l)
```

The scaled triangular variables are

```text
G_2=(L_2-x^2-A(2x+Y))/2,
V=G_2+xY+Y^2,
S=L_3+2YV-2xG_2-A(V+xU+G_2),
R=A(3Y^2+2xY+G_2),
D=YV.                                                (28m)
```

Here `S=d^3B` and `R` is `d^3` times the role numerator in (28b). On the
inherited `d(q-d)K_6!=0` saturation, equations (26) are equivalent to

```text
E_6=D((Y-A)V-S)-K_6=0,
E_4=D(G_2^2+AU G_2-Y(A+x)V-L_4)-xK_6=0,
E_5=(q-d)(Y^2V^2(G_2+AU)+G_2K_6)-6dK_6D=0.         (28n)
```

The first line forces `D=YV!=0`. Define

```text
R_D=DR,        S_D=Y(Y-A)V^2-K_6.                  (28o)
```

Then `E_6=0` gives `(R_D,S_D)=D(R,S)`. Hence each of the 21 official role
branches is exactly the conic, (28n), and one homogeneous quadratic
`Phi(R_D,S_D)=0`, all in `(x,Y,q,d)`. This is the preferred printed input
for a future proof-producing elimination; it does not restore `lambda`,
`B`, or a color-field extension variable.

The two middle equations have a further exact determinant router. Define

```text
H=G_2+AU,
W=Y(A+x)V+L_4,
J=(q-d)G_2-6dD,
Delta=G_2J+x(q-d)D.                                 (28p)
```

Then `E_4=E_5=0` is the linear system

```text
D G_2H-xK_6=DW,
(q-d)D^2H+JK_6=0,                                  (28q)
```

with determinant `D Delta`. On `Delta!=0`, it is equivalent to

```text
Delta H-WJ=0,
Delta K_6+(q-d)D^2W=0.                             (28r)
```

On `Delta=0`, consistency gives `WJ=0`. The complete singular split is

```text
J=0:   x=H=W=0;
J!=0:  W=0 and (q-d)D^2H+JK_6=0.                  (28s)
```

No determinant component is saturated away. On the `x=0` chart, the fourth
equation is the cubic

```text
96Y^3-144Y^2+(720+24q)Y
 +q^2+4q(d^2+7d+8)-660=0.                          (28t)
```

In the singular `J=0` subbranch, `H=W=0` reduces the coefficient matrix to

```text
d(q^2+132q+2916)+144q=0,
q^3+126q^2+(5364-504d-72d^2)q+87480=0,             (28u)
```

together with the h=7 conic. This is a small bivariate endpoint, not an
emptiness claim: `E_6`, one role equation, and every arithmetic lift filter
remain mandatory.

The first equation in (28u) is linear in `d` after putting

```text
A(q)=q^2+132q+2916,       T(q)=-144q.               (28v)
```

On the inherited `q!=0` saturation it forces `A(q)!=0` and
`d=T(q)/A(q)`. Define

```text
B(q)=q^3+126q^2+5364q+87480,

P_W(q)=A(q)^2B(q)+72576q^2A(q)-1492992q^3,

P_C(q)=35q^2A(q)^4
 +14q(11T(q)^2A(q)^2+27T(q)A(q)^3+27A(q)^4)
 +120(T(q)^4+4T(q)^3A(q)+7T(q)^2A(q)^2
       +6T(q)A(q)^3+3A(q)^4).                      (28w)
```

Then `P_W` is monic of degree seven, `P_C` has degree ten and leader 35,
and the coefficient endpoint `(conic,F_J,F_W)` is exactly

```text
P_W(q)=P_C(q)=0,       d=-144q/A(q).                (28x)
```

Thus a unit `gcd_Fp(P_W,P_C)` excludes this singular coefficient chamber.
The source-pinned certificate packet is

```text
experimental/scripts/l1_m8_h7_cubic_321_singular_j0_gcd_modal.py
sha256: 39ccbf6493dc3a421935dbbd0b1e31e761c4e13b2c3f48eaa3c6b87d44a987e0

experimental/scripts/check_l1_m8_h7_cubic_321_singular_j0_gcd_certificate.py
sha256: a653511eb927b1627258d7c2e25e6b46439827140d1fabab743a2404e771469c
```

The one-container worker is capped at 0.125 CPU, 128 MB, and 30 seconds and
emits extended-Euclidean coefficients for all four rows. It was not run:
the configured Modal workspace is spend-blocked. The checker accepts exact
HIT packets but requires `--require-all-unit` for an exclusion certificate.

The other determinant-singular chamber also admits an exact reduction before
any elimination. Retain the notation in (28q)--(28t), take `Delta=0` and
`J!=0`, and put

```text
N=G_2^2+xD,
Z=N+6DG_2,
P=3x(6G_2+AxU-20-D)-8qx-3G_2H.                    (28y)
```

The singular equations force `H!=0` and

```text
x=0  if and only if  G_2=0.                         (28z)
```

On the `x=0` chart one has

```text
Y=(q+30)/12,       V=Y^2,       D=Y^3,

P_W^+=q^3+126q^2+(4356+504d+72d^2)q+31320=0,

(q^3+90q^2+3132q+57240)d
 =8q^3+864q^2+30528q+250560,

K_6+Y^6+L_3Y^3=0.                                  (28aa)
```

These three equations, the conic, and one role equation are equivalent to
the complete coefficient core on this chart. If the coefficient of `d` in
(28aa) vanishes, the right side must vanish as well; that exceptional chart
is not divided away.

On `x!=0`, also `G_2NZ!=0`. The identities

```text
(Y-A)V-S=6G_2+AxU-L_3-D,
Delta=qN-dZ
```

turn the sixth coefficient and determinant equations into

```text
d=P/(qx),       q^2xN-PZ=0.                         (28ab)
```

After this substitution, clear `(qx)^2` from `W`, `(qx)^4` from
`DG_2H-xK_6` and the conic, and `(qx)^8` from the quadratic role equation.
Together with the last equation of (28ab), these are five equations in only
`(x,Y,q)`. Saturate by `qxG_2NZP(q^2x-P)` and all inherited factors. This is
an exact three-variable primitive shift-pair coefficient ledger, not a unit
verdict.

Although each official role packet is irreducible over `F_p`, the variables
`q,d,x,Y` are not forced into `F_p`; they live in the ambient quadratic
field. Thus role irreducibility alone does not delete either chart. The
unrun singular-`J=0` gcd packet remains logically independent.

The generic `Delta!=0` branch has a second exact hand eliminant. Define

```text
T=G_2+6D,
Q_0=6G_2+AxU-20-8q/3-D,
W_0=Y(A+x)V+15+23q/4+q^2/8,
R_0=G_2H-xQ_0-W_0.                                  (28ac)
```

Then `Q_6=(Y-A)V-S=Q_0-qd/3`, `W=W_0+q(d^2+7d)/4`, and
`J=qG_2-dT`. On `E_6=0`, the fourth and fifth coefficients are equivalent
to the two quadratics

```text
P_4=-3qd^2+q(4x-21)d+12R_0=0,

P_5=qTd^2-(3DH+q^2G_2+3TQ_0)d
       +3q(DH+G_2Q_0)=0.                            (28ad)
```

Their leading terms cancel exactly:

```text
3P_5+TP_4=C_1d+C_0,                                 (28ae)

C_1=qT(4x-21)-9DH-3q^2G_2-9TQ_0,
C_0=9q(DH+G_2Q_0)+12TR_0.
```

Consequently the `C_1!=0` chart has `d=-C_0/C_1`; after clearing powers of
`C_1`, it consists of `P_4`, `E_6`, the conic, and one role equation in only
`(x,Y,q)`. Saturate the reconstructed forms of `d,q-d,Delta,W` and every
inherited factor. The `C_1=0` chart is not discarded: it retains

```text
C_1=C_0=P_4=E_6=Conic=Phi=0                         (28af)
```

in `(x,Y,q,d)`, with `Delta*W!=0`. Thus the former generic four-variable
request is now an overdetermined four-equation three-variable chart plus an
exceptional locus carrying two equations independent of `d`. This remains a
reduction, not a dimension or unit verdict.

The conic and sixth coefficient supply a second independent linear
eliminant. Put

```text
kappa=12q+366-176x,
B_1=-q(120D+1062+86q)-528R_0,
B_0=360DQ_0-360-1098q-191q^2+10q^3,
M_1=3B_1+q kappa(4x-21),
M_0=3B_0+12 kappa R_0.                              (28ag)
```

Cancellation of the common `d^4` term, followed by one reduction modulo
`P_4`, gives the exact identity

```text
2(M_1d+M_0)
 =2160E_6+3q Conic+2(kappa-132d)P_4.                (28ah)
```

Thus, with the conic and `P_4` retained, `E_6=0` is equivalent to
`M_1d+M_0=0`. The complete generic coefficient core now has two linear
equations in `d`:

```text
C_1d+C_0=0,       M_1d+M_0=0,
Omega=C_1M_0-M_1C_0=0.                             (28ai)
```

There are three exact charts. If `C_1!=0`, reconstruct `d=-C_0/C_1` and
retain `Omega=0`. If `C_1=0,M_1!=0`, retain `C_0=0` and reconstruct
`d=-M_0/M_1`. Only the doubly singular chart keeps `d`, with

```text
C_1=M_1=C_0=M_0=P_4=Conic=Phi=0.                   (28aj)
```

Each rational chart also retains the denominator-cleared `P_4`, conic, and
role equation, plus the reconstructed nonzero factors. This is an exact
route reduction; `Omega=0` and the doubly singular equations are not unit
or dimension verdicts.

The doubly singular coefficient locus itself has a final quadratic-quotient
reduction. Put

```text
a_d=4x-21,       alpha=a_d/3,       beta=4R_0/q.
```

Since `q!=0`, `P_4=0` is exactly `d^2=alpha d+beta`. Reducing the conic in
this quotient gives

```text
9q^2 Conic=N_1d+N_0 mod P_4,                       (28ak)

N_1=q^2(40a_d^3+480a_d^2+(2520+462q)a_d+6480+3402q)
       +2880qR_0(a_d+6),

N_0=qR_0(480a_d^2+5760a_d+30240+5544q)
       +17280R_0^2+q^2(3240+3402q+315q^2).
```

For one official role packet write

```text
Phi(X,Y)=c_2X^2+c_1XY+c_0Y^2,
S_0=(Y-A)V-Q_0.
```

The packet is irreducible, hence `c_0!=0`. On `E_6=0`, homogeneity and
`S=S_0+qd/3` give the exact remainder

```text
27Phi(R,S_0+qd/3)+c_0qP_4=U_1d+U_0,                (28al)

U_1=9q(c_1R+2c_0S_0)+c_0q^2a_d,
U_0=27(c_2R^2+c_1RS_0+c_0S_0^2)+12c_0qR_0.
```

Thus the doubly singular core has two further linear equations in `d` and
the packet-specific parameter determinant

```text
Xi=N_1U_0-U_1N_0=0.                                (28am)
```

If `N_1!=0`, reconstruct `d=-N_0/N_1`; if `N_1=0,U_1!=0`, retain `N_0=0`
and reconstruct `d=-U_0/U_1`. Only

```text
N_1=U_1=N_0=U_0=0                                  (28an)
```

still retains `d`. The 21 choices of `(c_2,c_1,c_0)` are alternatives, not
simultaneous equations. The fully proportional quotient locus remains an
open packet, not a discarded denominator component.

The fully proportional coefficients can themselves be solved explicitly.
Put

```text
b=a_d+6=4x-15,
P=40b(b^2-6b+27)+42q(11b+15),
Q=480b^2+12960+5544q,
T_c=3240+3402q+315q^2.                              (28ao)
```

The equations `N_1=N_0=0` imply `b!=0`: at `b=0`, one has
`N_1=630q^3!=0`. They are exactly

```text
R_0=-qP/(2880b),
F_N:=6P^2-bPQ+2880b^2T_c=0.                        (28ap)
```

For the selected role packet define

```text
delta_Phi=c_1^2-4c_2c_0.
```

The equations `U_1=U_0=0` are exactly

```text
S_0=-c_1R/(2c_0)-qa_d/18,

c_0^2(q^2a_d^2+144qR_0)=81delta_Phi R^2.           (28aq)
```

The expression in parentheses is the discriminant of `P_4` as a quadratic
in `d`. Thus the last proportional residue consists of the four earlier
coefficient-zero equations, the reconstructions (28ap)--(28aq), `F_N=0`,
and `P_4=0`. This is a role-discriminant weld, not a prime-field nonsquare
contradiction: the coefficient variables live in the ambient quadratic
field. Every arithmetic lift remains mandatory.

The bivariate endpoint in (28ap) factors further. Put `z=b^2`. Then

```text
F_N=24F_b(z,q),

F_b(z,q)=63(1575-247z)q^2
          +9240z(9-z)q
          +400z(9-z)(z+27).                        (28ar)
```

The inherited `bq!=0` saturation gives `z!=0`; also `z=9` would leave
`-63*648q^2=0`, so `z!=9`. Away from `1575-247z=0`, the discriminant in
`q` is

```text
302400z(9-z)(-200z^2+4239z-14175).                 (28as)
```

The vanishing-leading-coefficient chart is retained and solved exactly:

```text
z=1575/247,       q=-10(z+27)/231.                 (28at)
```

This is an ambient-field quadratic endpoint, not a square-condition
verdict. The four coefficient-zero equations, role-discriminant weld,
`P_4`, and all arithmetic filters remain.

The four coefficient-zero equations also admit an exact parameter router.
Put

```text
a=b-6,                 kappa=12q-44b-294,
ell=(b^2+6b+105+8q)/16,

D_*=3q(40b^2-253b+1155)-20b(11b^2+81b+414),
Q_*=720b(360+1098q+191q^2-10q^3)+kappa qP,
K_*=240bqa-P.                                         (28au)
```

Then `M_1=M_0=0` is exactly

```text
D_*=3600bD !=0,       Q_*=72D_*Q_0.                (28av)
```

The original scaled definitions independently give

```text
H+G_2=ell,             A=-(b+3)/2 !=0.             (28aw)
```

Define

```text
E_G=K_*-720bq^2,             F_G=6D(K_*-2160bQ_0),
J_G=2160b(Q_0-D)-P,          L_G=2160b ell-6P.     (28ax)
```

After (28av)--(28aw), `C_1=C_0=0` is exactly

```text
E_GG_2+F_G=0,          J_GG_2+D L_G=0.             (28ay)
```

Thus on `E_G!=0`, reconstruct `G_2=-F_G/E_G` and retain the bivariate
compatibility equation

```text
Theta_G:=E_GD L_G-J_GF_G=0.                        (28az)
```

Then `H=ell-G_2` and `Y=(ell-2G_2)/A-x`. On `E_G=0`, the first equation
in (28ay) forces `Q_0=q^2/3`, equivalently
`Q_*-24D_*q^2=0`. If `J_G!=0`, use `G_2=-D L_G/J_G`; if `J_G=0`, retain
`L_G=0` and `G_2`. This last doubly exceptional chart is not discarded.
Every chart remains coupled to (28ar), the structural equations, the role
discriminant, `P_4`, and all arithmetic lift filters. No chart is declared
empty.

For a denominator-free endpoint, define

```text
L_*=135b(b^2+6b+105+8q)-6P,
F_*=D_*K_*-30bQ_*,
J_*=150bQ_*-3D_*^2-5PD_*,
X_*=Q_*-24D_*q^2,
Theta_*=5E_GD_*^2L_*-6J_*F_*.                    (28ba)
```

The exact clearing identities are

```text
F_G=F_*/(600b),
J_G=J_*/(5D_*),
Theta_G=Theta_*/(18000bD_*).                      (28bb)
```

Thus the generic coefficient endpoint is

```text
F_b(b^2,q)=Theta_*(b,q)=0,       E_G!=0,
G_2=-F_*/(600bE_G).                               (28bc)
```

On `E_G=0,J_*!=0`, retain `F_b=E_G=X_*=0` and reconstruct
`G_2=-D_*^2L_*/(720bJ_*)`. The only coefficient chart retaining `G_2` is

```text
F_b=E_G=X_*=J_*=L_*=0.                            (28bd)
```

Here `Theta_*` has total degree at most 12 and `q`-degree at most six,
while `F_b` has `q`-degree two. These are coefficient endpoints only; all
substituted structural, role, `P_4`, and arithmetic equations remain.

## Symmetric affine-color equation for 2+2+2

The same role polynomial imposes the three-color condition on the symmetric
`2+2+2` core without restoring the individual `u_i`. Put

```text
A(lambda)=lambda^2-lambda+1,
B(lambda)=(lambda+1)(2lambda-1)(lambda-2),

K_8(P,Q)=Res_lambda(
  Lambda_321(lambda),
  27A(lambda)^3Q^2+B(lambda)^2P^3).                (29)
```

For any three values with elementary symmetric functions `E_1,E_2,E_3`,
define their depressed-cubic invariants

```text
P=E_2-E_1^2/3,
Q=E_3-E_1E_2/3+2E_1^3/27.                         (30)
```

For the normalized ordered triple `(0,1,lambda)`, these equal
`-A(lambda)/3` and `B(lambda)/27`; hence (29) vanishes. In the factor model
(11), the three values

```text
f(u_i),  f(T)=T^3-2UT^2+(U^2+V)T-UV,
```

differ from the three colors by one common scale and translation. Their
`E_i` are obtained without choosing the roots from

```text
Res_T(T^3-s_1T^2+s_2T-s_3, Z-f(T))
  =Z^3-E_1Z^2+E_2Z-E_3.                            (31)
```

Thus `K_8(P,Q)=0` is an exact necessary color equation in the existing
symmetric variables. The 56 color triples have seven oriented affine
shapes, with cyclic gap types

```text
(1,1,6),
(1,2,5), (1,5,2),
(1,3,4), (1,4,3),
(2,2,4),
(2,3,3).
```

For `T=-27Q^2/P^3`, direct substitution gives the exact color polynomial

```text
Theta_8(T)=(T+50)(T^2-224T-578)(T^2-4T+54)
           (125T^2-2404T+13448).                  (32)
```

The three isosceles values are `-50` and `112+/-81sqrt(2)`. The two
scalene reflection pairs give `2+/-5sqrt(-2)` and
`(1202+/-486sqrt(-1))/125`. Reflection conjugates, rather than identifies,
these scalene affine invariants. Thus the primitive characteristic-zero
squarefree radical of (29), as a binary form in `P^3,Q^2`, has degree seven;
its homogeneous form is `P^21 Theta_8(-27Q^2/P^3)` and includes `P=0`.

This repairs an earlier draft that incorrectly counted the five Euclidean
reflection classes as affine classes. The safe cross-characteristic equation
remains the full resultant (29); reduction can merge factors. On the generic
fifth-slope branch, eliminating `b` now leaves the conic, substituted `D_b`,
compatibility of `M_5,M_6`, and (29): four equations in `(x,q,d)`. This is a
reduction, not an emptiness verdict.

The invariants in (30) themselves have a small closed form. Put

```text
z=x^2+q/6,
p=b-12,
eta=-xp-q(d+2)/6,
ell=z-2p/3.                                        (33)
```

Then

```text
P=ell^2p+6x ell eta-(4/3)x^2p^2,

Q=-8x^3(eta^2+2p^3/27)-4x^2 ell p eta
  -(4/3)x ell^2p^2+ell^3 eta.                      (34)
```

Indeed, after centering the `u_i`, their invariants are `p,eta`, and the
value map becomes `Av^2+Lv` with `A=-2x`, `L=ell`. For any centered triple,
the image invariants are

```text
P=L^2p-3AL eta-A^2p^2/3,
Q=A^3(eta^2+2p^3/27)-A^2Lp eta
  +(2/3)AL^2p^2+L^3 eta.                           (35)
```

Substituting (34) in (32) gives four rational homogeneous color factors:

```text
50P^3-27Q^2,
729Q^4+6048P^3Q^2-578P^6,
729Q^4+108P^3Q^2+54P^6,
91125Q^4+64908P^3Q^2+13448P^6.                    (36)
```

Off the exceptional slopes, write

```text
alpha=-(q-d)xz,
beta=(q-d)B_5+6dG,
b=-beta/alpha.                                    (37)
```

Each of the four rational color packets is now an explicit system in only
`(x,q,d)`: the conic, substituted `D_b`,
`alpha B_6-A_6 beta=0`, and one factor of (36).

There is also a denominator-free quotient weld. With `p=b-12`, define

```text
C=d^2+3d+3,
a=3x^2-q/2,
h=3qC/4+q^2/8.
```

Then `D_b=0` is exactly `p^2+ap-h=0`. If
`p^n=U_np+V_n` in this quadratic quotient, the recurrence is

```text
(U_0,V_0)=(0,1), (U_1,V_1)=(1,0),
U_(n+1)=V_n-aU_n,  V_(n+1)=hU_n.                  (38)
```

It turns each factor `F_i` in (36) into a unique remainder
`c_(i,1)p+c_(i,0)`. In particular,

```text
12P=(-60x^4-8qx^2+8q(d+2)x+4qC+q^2)p
    -12xq(d+2)(x^2+q/6) mod D_b.                  (39)
```

Put

```text
delta=12alpha+(q-d)B_5+6dG,
gamma=12A_6+B_6.                                   (40)
```

On `alpha!=0`, packet `i` is equivalent to the conic and

```text
delta^2-a alpha delta-h alpha^2=0,
alpha gamma-A_6 delta=0,
alpha c_(i,0)-c_(i,1)delta=0.                      (41)
```

Indeed `M_5` gives `p=-delta/alpha`; substitution proves both directions.
The exceptional loci deleted by `alpha` are exactly the inherited `q=d`
saturation and the separately owned `x=0`, `q=-6x^2` branches.

## Verification

The exact-rational identity checker is

```text
experimental/scripts/verify_l1_m8_h7_order_one_cubic_profile_reductions.py
sha256: 58d4457c97b5ba5c2b03f8b4d3dfc4e7777a73e9befab571ff764077c0f71858
```

Its expected marker is

```text
L1_M8_H7_ORDER_ONE_CUBIC_PROFILE_REDUCTIONS_PASS linear_samples=2 x0_samples=3 q6x2_samples=3 common_quadratic=1 role_polynomial=1 role_factors=4 role_weld=1 galois_role_packets=12 frobenius_role_packets=21 scaled_quadratic_core=1 coefficient_matrix_router=1 singular_j0_univariate=1 singular_jnonzero_charts=1 generic_linear_d=1 generic_double_linear_d=1 doubly_singular_quotient=1 fully_proportional_parameters=1 fully_proportional_bivariate=1 fully_proportional_coefficients=1 fully_proportional_bivariate_compiler=1 affine_color_shapes=7 affine_formula=1 quotient_weld=1
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
