---
workboard_item: T
row: symbolic rate-half half-distance core-one quadratic floor profile
object: LINE
target_epsilon: 2^-128 context; target-free structural theorem
agreement: a=N-t=3N/4
B_star: floor(q/2^128); no payment claimed
direct_statement: every extremal split-biform fiber has its complete padding factor; the residual projective intersection cycle has degree four; its parameter eliminant is exactly the regular Kronecker correction quartic
architecture: DIRECT
partition_digest: N/A
atom_or_cell: symmetric-Hankel core-one scalar-quadratic u=4 extremal boundary
quantifier: every field and profile satisfying the exact pair-floor interface and retained core-one quadratic packet
projection_and_unit: projective parameter fibers and local intersection multiplicity
claimed_bound: after one copy of every actual-support and padded common point, exactly four projective intersection units remain; their parameter divisor is S_B^2 in the double-root arm and S_1S_2 in the two-simple arm
status: PROVED
impact: ROUTE_CUT
falsifier: a missing positive-excess padding factor, residual intersection degree other than four, wrong Pade leading-coefficient exponent, or a residual parameter root outside the correction quartic
replay: python3 experimental/scripts/verify_rate_half_core_one_quadratic_pade_quartic_v1.py --check
---

# Rate-half core-one quadratic Pade/quartic eliminant

## 1. Relation to the Lane-T frontier

The companion pair-floor packet reduces the extremal core-one quadratic
boundary to two coprime biforms

```text
Q(t,X),       G(t,X)
```

with bidegrees

```text
(e,3e-2),       (e-2,p-3),       2p=3e-1.          (1)
```

It previously supplied full split fibers only at zero excess and left the
regular Kronecker quartic `E_4` unrelated to the biform intersection
ledger. This note closes both structural gaps. It is a profile-level route
cut, not a `LineRay` payment or an adjacent-row theorem.

The proof source is pinned to
`AllenGrahamHart/rs-mca-prize-dag@beb25530100b14f23413c470219fdb6b8521094b`.
The verifier records the ten statement/proof SHA-256 values and can check
them against a local source checkout with `--source-root`.

## 2. Every off-line fiber, including positive excess

For an off-line supported slope `delta`, let

```text
I_delta=S_delta intersect U_0,
P_delta=S_delta\U,
A_delta=product_(x in I_delta)(X-x),
B_delta=product_(x in P_delta)(X-x).                (2)
```

Write `a_delta` for its union excess and `r_delta` for its padded-heavy
degree. The center difference is a nonzero RS word supported on a set of
size `d_min+a_delta`. Factoring its forced `k-1-a_delta` zeros leaves a
nonzero polynomial `H_delta` with `deg H_delta<=a_delta`. The exact fiber
factorizations are

```text
Q(delta,X)=chi_delta A_delta B_delta R_delta,
G(delta,X)=zeta_delta A_delta H_delta R_delta.      (3)
```

At `x in P_delta`, both endpoint centers equal the received word, while
the selected center has nonzero error. Hence `H_delta(x)!=0`, and therefore

```text
gcd(B_delta,H_delta)=1,
gcd_X(Q(delta,-),G(delta,-))=A_delta R_delta.       (4)
```

Thus all positive-excess padding is mandatory in the split-biform
intersection. At every actual-support root the first-jet difference remains

```text
G_t/Q_t-G_X/Q_X
 =(x-s_0)v_xL_U0'(x)e_delta(x)/Lambda(delta)!=0,    (5)
```

so every actual-support intersection is transverse.

## 3. Exact four-unit residual

The two curves are coprime. Their projective intersection number is

```text
I=(3e-2)(e-2)+e(3e-7)/2
  =(9e^2-23e+8)/2.                                 (6)
```

There are `3e` off-line slopes, and on slope `delta` the mandatory common
polynomial `A_delta R_delta` has degree `n-a_delta`, where
`n=(3e-7)/2`. Since `sum_delta a_delta=e`, the mandatory first copies have
total degree

```text
sum_delta(n-a_delta)=3en-e=I-4.                    (7)
```

After subtracting one copy of every such actual-support and padding point,
the residual effective projective intersection cycle `Z_4` therefore has

```text
deg Z_4=4.                                         (8)
```

This count is projective and does not lose a parameter- or domain-infinity
fiber.

## 4. Contracted Pade numerator

Let

```text
L(X)=L_U0(X),       d=3e-2,       a(t)=lc_X Q(t,X),
Phi_t(h)=sum_(x in U_0)omega_x(t)h(x).              (9)
```

Define the canonical second-kind numerator and its companion polynomial by

```text
B(t,X)=sum_x omega_x(t)L(X)/(X-x),
P_F(t,X)=sum_x omega_x(t)[Q(t,X)-Q(t,x)]/(X-x).    (10)
```

Lagrange interpolation of `G` gives the exact Pade syzygy

```text
QB-Lambda G=LP_F.                                  (11)
```

If the regular Kronecker determinant is normalized by

```text
adj M_1=D_1qq^T,       deg D_1=e-2,                (12)
```

then the formal fixed-degree resultant is

```text
Res_X^(d,d-1)(Q,P_F)=c a^(2d+1)D_1.                (13)
```

For a generic separable fiber, represent the first `d` moments on the roots
`r_i` of `Q` with weights `theta_i`. Then

```text
P_F(r_i)=theta_iQ_X(r_i),
Vand(r_1,...,r_d)^2 product_i theta_i=D_1a^2,       (14)
```

and the root-product definition of the resultant proves `(13)`. Polynomial
continuation covers inseparable fibers and degree drops.

The exponent `2d+1` is essential. It is the complete domain-infinity
contact of the core-stripped Forney numerator. Removing it identifies

```text
div(D_1)=pi_*div(s_F).                              (15)
```

The raw resultant degree is `2de-e+d`; subtracting `e(2d+1)` leaves
`d-2e=e-2`, exactly the degrees on both sides of `(15)`.

## 5. The regular quartic is the correction quartic

The proved contact divisors are

```text
double root: div(s_F)=R_*+2B,
two simple:  div(s_F)=R_1+R_2+P_1+P_2,             (16)
```

where `deg B=2`, `deg P_1=1`, and `deg P_2=3`. Let `S_B,S_1,S_2` cut out
their parameter pushforwards. Comparing `(15)` with the supported
rank-loss factorization of `D_1` gives

```text
double root: D_1=c g_*S_B^2,       E_4=c' S_B^2,

two simple:  D_1=c G_1G_2S_1S_2,  E_4=c' S_1S_2.  (17)
```

Cancellation in `(17)` is polynomial cancellation and does not require
the correction and supported factors to be disjoint.

## 6. Exact parameter eliminant

Take the `X`-resultant of `(11)`. The formal leading-coefficient exponent is

```text
|U_0|+d-1-(p-3)=2d+1,                              (18)
```

so `(13)` cancels it completely and yields

```text
Lambda^d Res_X(Q,G)=c D_1 Res_X(Q,L).              (19)
```

The row roots of `Q` and the exact supported rank-loss factors of `D_1`
cancel every center-line factor. At an off-line slope they combine as

```text
(n-a_delta-r_delta)+r_delta=n-a_delta.             (20)
```

Therefore

```text
Res_X(Q,G)
 =c E_4 product_(delta off line)
          ell_delta^(n-a_delta),                   (21)

pi_*Z_4=div(E_4).                                  (22)
```

Equations `(17),(22)` locate the four units exactly in parameter space:

```text
double root: pi_*Z_4=2div(S_B),
two simple:  pi_*Z_4=div(S_1)+div(S_2).             (23)
```

No additional unsupported or infinity parameter fiber remains.

## 7. Marked orders and the remaining wall

The rank-one marked determinant identities sharpen to

```text
double root: g_*^3S_B^8,
two simple:  G_1^5G_2S_1^7S_2,
             G_1G_2^5S_1S_2^7.                    (24)
```

Orders eight and seven are not abstract symmetric-pencil contradictions.
A standard symmetric singular Kronecker block with kernel coordinate `z^3`,
direct-summed with `[[0,z],[z,1]]` or `[z]`, realizes exactly those marked
orders. Hence the next exclusion must use a genuinely prize-specific input:
the Hankel anti-diagonal equations, the three-class contracted source,
simultaneous split fibers, or the received-word/Forney identities.

## Nonclaims

This packet does not exclude either quadratic root arm, prove a live
`LineRay` census, pay a v4 atom, move an adjacent endpoint, or change a
leaderboard score. It identifies the remaining degree-four geometry and
rules out determinant multiplicity as a standalone closure argument.
