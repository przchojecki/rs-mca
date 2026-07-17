# Uniform dense-shell transfer shape

## Status

```text
PROVED: the transfer envelopes TS1 and TS2 and the child-share floor TS3
hold at every depth.  The proof combines a finite Arb certificate with an
exact positive two-state induction.  Consequently the INV-TAIL hypothesis
in dense_shell_class_charges.md is discharged and its |K| <= 1 master and
class-sign conclusions are unconditional at every depth.

NOT CLAIMED: decorated-subtree positivity for general K, pointwise sign
purity, product-profile admission, hard input 2, or any lower-reserve
payment.
```

The verifier is
`experimental/scripts/verify_dense_shell_transfer_shape_arb.py`.  It uses
448-bit Arb balls through the tested dependency `python-flint == 0.9.0`,
degree-320 Chebyshev-Lobatto interpolation, explicit analytic remainders,
inherited error propagation, continuum cells, a direct-tree model
cross-check, and semantic tamper tests.  The deterministic certificate is
`experimental/data/certificates/dense-shell-transfer-shape/`.

## 1. The theorem

Use the flipped shifted-Chebyshev convention of
`dense_shell_class_charges.md`.  Put

\[
B_n(t)=\widetilde G_n(t),\qquad
a(t)=\sin^2(\pi t),\qquad
d(t)=a(t)-\frac12=-\frac12\cos(2\pi t).
\]

Let the Jacobi operator `K` act on finitely supported vectors by

\[
(Kb)_0=\frac14b_1,
\]
\[
(Kb)_1=\frac12b_0+\frac14b_2,
\]
\[
(Kb)_i=\frac14(b_{i-1}+b_{i+1})\quad(i\ge2),
\]

where absent coordinates are zero, and put `N_t=K+d(t)I`.  The exact
cascade recurrence is

\[
B_n(t)=N_{t_+}B_{n-1}(t_+)+N_{t_-}B_{n-1}(t_-),
\qquad t_\pm=\frac{1\pm t}{3},                 \tag{1}
\]

with `B_0=e_0`.

For

\[
\begin{aligned}
t_{\rm in}&=\frac14-\frac\varepsilon3,&
r&=\frac14+\frac\varepsilon9,\\
s&=\frac7{36}-\frac\varepsilon9,&
r_2&=\frac5{12}-\frac\varepsilon9,\\
s_2&=\frac{17}{36}+\frac\varepsilon9,&
g&=\frac1{18}+\frac{2\varepsilon}{9},
\end{aligned}
\]

every `j >= 6` and `0 <= epsilon <= 1/4` satisfy, componentwise,

\[
e^{-1.086g}B_{j-1}(r)\preceq B_{j-1}(s)
\preceq e^{1.086g}B_{j-1}(r),                 \tag{TS1}
\]

\[
e^{-1.663g}B_{j-1}(r_2)\preceq B_{j-1}(s_2)
\preceq e^{1.663g}B_{j-1}(r_2),               \tag{TS2}
\]

and, on all coordinates of `B_{j-1}`,

\[
B_j(t_{\rm in})\succeq\frac76B_{j-1}(r).      \tag{TS3}
\]

## 2. The invariant cone

Set

\[
\lambda=\frac{241}{500},\qquad
C=\frac{1289}{500},\qquad
\mu=\sqrt C,
\]

and define

\[
E_n(t)=-B_n'(t),\qquad F_n(t)=-B_n''(t).
\]

The all-depth invariant is

\[
\boxed{
B_n(t)\succ0,\qquad
KB_n(t)\succeq\lambda B_n(t),\qquad
0\preceq E_n(t),\qquad
0\preceq F_n(t)\preceq CB_n(t)
}                                                   \tag{2}
\]

for `0 <= t <= 1/2`.

One harmless endpoint convention is worth printing explicitly.  For
`n >= 1`, the degree-`n` coordinate is

\[
(B_n)_n=2^{1-n},\qquad (E_n)_n=(F_n)_n=0.       \tag{3}
\]

For `n=1` this follows directly from the exceptional `K_{1,0}=1/2`
entry.  Thereafter each of the two branches contributes one quarter of the
previous top coordinate.  Thus the top curvature coordinate is exact and is
not a numerical certificate obligation.

The finite certificate proves the two-state shape base at level 25, the
differential cone at level 26, and TS1--TS3 directly for levels `5 <= n <=
26`.  The rest of the proof is symbolic.

## 3. Positive two-state shape induction

Put

\[
A=K-\lambda I,
\]

and split the interval into

\[
\mathcal I=[0,1/4],\qquad \mathcal O=[1/4,1/2].
\]

Use the states

\[
I_n(q)=B_n(q)\quad(q\in\mathcal I),
\qquad O_n(t)=N_tB_n(t)\quad(t\in\mathcal O).
\]

If `q` is inner, both children are outer, so

\[
I_n(q)=O_{n-1}(q_+)+O_{n-1}(q_-).              \tag{4}
\]

If `t` is outer, set `p=t_+` and `m=t_-`.  Then

\[
O_n(t)=N_tO_{n-1}(p)+C_tI_{n-1}(m),
\qquad C_t=N_tN_m.                              \tag{5}
\]

Write

\[
t=\frac14+3\delta,\qquad m=\frac14-\delta,
\qquad 0\le\delta\le\frac1{12}.
\]

Then

\[
d(t)=P=\frac12\sin(6\pi\delta),\qquad
d(m)=-Q=-\frac12\sin(2\pi\delta).
\]

On this interval `P >= Q >= 0`, because

\[
\sin(6x)-\sin(2x)=2\cos(4x)\sin(2x)\ge0
\quad(0\le x\le\pi/12).
\]

Also `PQ <= 1/8`.  Hence

\[
C_t=(K+PI)(K-QI)=K^2+(P-Q)K-PQI.               \tag{6}
\]

All off-diagonal entries are nonnegative, while the smallest diagonal entry
of `K^2` is `1/8`.  Therefore

\[
C_t\succeq0.                                    \tag{7}
\]

The certificate establishes

\[
A^qI_{25}(t)\succeq0\quad(t\in\mathcal I),
\qquad
A^qO_{25}(t)\succeq0\quad(t\in\mathcal O),
\qquad q=0,1,2.                                 \tag{8}
\]

The operators in (4)--(5) are nonnegative polynomials in `K`, so they
commute with `A`.  Applying `A^q` proves (8) at every later level.

For an inner `t`, (8) directly gives `B_n >= 0` and `AB_n >= 0`.  For an
outer `t`,

\[
B_n(t)=O_{n-1}(p)+N_mI_{n-1}(m).
\]

Since `m in [1/6,1/4]`,

\[
c_m=\lambda+d(m)\ge\lambda-\frac14>0,
\qquad N_m=A+c_mI.
\]

Thus

\[
B_n(t)=O_{n-1}(p)+AI_{n-1}(m)+c_mI_{n-1}(m)\succeq0,       \tag{9}
\]

and

\[
AB_n(t)=AO_{n-1}(p)+A^2I_{n-1}(m)+c_mAI_{n-1}(m)\succeq0. \tag{10}
\]

The strict finite base and the positive `c_m I` term, together with the
connected Jacobi operator at the new top coordinate, give strict positivity.
Since `AB_n >= 0` is equivalent to `KB_n >= lambda B_n`, this proves the
shape part of (2) at every depth.

## 4. Derivatives and monotonicity

Differentiating (1) gives, with `p=t_+` and `m=t_-`,

\[
3E_n=N_pE_p-N_mE_m-a'(p)B_p+a'(m)B_m.          \tag{11}
\]

A second differentiation gives

\[
\begin{aligned}
9F_n={}&N_pF_p+N_mF_m
+2a'(p)E_p+2a'(m)E_m\\
&-a''(p)B_p-a''(m)B_m.                         \tag{12}
\end{aligned}
\]

The exact trace cancellation is

\[
a'(p)-a'(m)=-a'(t/3).                           \tag{13}
\]

Using it before taking signs rewrites (11) as

\[
\begin{aligned}
3E_n={}&N_p(E_p-E_m)+(d(p)-d(m))E_m\\
&+a'(p)(B_m-B_p)+a'(t/3)B_m.                   \tag{14}
\end{aligned}
\]

Assume (2) at level `n-1`.  Then `B'=-E <= 0` and `E'=F >= 0`.
Since `m <= p`, `B_m >= B_p` and `E_p >= E_m`.  Every term in (14) is
nonnegative, because `N_p` is an outer positive operator.  Hence

\[
E_n\succeq0.                                    \tag{15}
\]

## 5. Riccati envelope and curvature

For one positive coordinate `b(t)` of `B_{n-1}(t)`, put

\[
h(t)=\frac{E(t)}{B(t)}=-\frac{b'(t)}{b(t)}.
\]

Evenness gives `h(0)=0`, and `F <= CB` gives

\[
h'=\frac FB+h^2\le C+h^2.
\]

Comparison with `y'=C+y^2`, `y(0)=0`, yields

\[
0\le h(t)\le H(t)=\mu\tan(\mu t),
\qquad 0\le t\le\frac12.                       \tag{16}
\]

Consequently

\[
1\le\frac{b(u)}{b(v)}
\le\frac{\cos(\mu u)}{\cos(\mu v)}
\quad(0\le u<v\le1/2).                         \tag{17}
\]

### Lower curvature bound

For `t <= 1/4`, both child operators are nonnegative and both child second
derivatives `a''` are nonpositive, so every term in (12) is nonnegative.

For `t >= 1/4`, `d(m) <= 0` and `a''(m) >= 0`.  Since `K` is positive and
`F_m <= C B_m`,

\[
N_mF_m=KF_m+d(m)F_m\succeq C d(m)B_m.          \tag{18}
\]

Discarding the remaining nonnegative terms gives

\[
9F_n\succeq-a''(p)B_p+(Cd(m)-a''(m))B_m.       \tag{19}
\]

The second scalar coefficient is nonpositive.  By (17),

\[
B_m\preceq R(t)B_p,
\qquad R(t)=\frac{\cos(\mu m)}{\cos(\mu p)}.
\]

The scalar Arb gate proves on `[1/4,1/2]`

\[
-a''(p)+(Cd(m)-a''(m))R(t)>5.14.               \tag{20}
\]

Thus `F_n >= 0`.

### Upper curvature bound

Put

\[
V_p=N_pB_p,\qquad V_m=N_mB_m,
\qquad c_p=\lambda+d(p),\qquad c_m=\lambda+d(m).
\]

The shape inequality gives

\[
V_p\succeq c_pB_p,\qquad V_m\succeq c_mB_m.    \tag{21}
\]

The outer branch satisfies `N_pF_p <= C V_p`.  For the other branch set

\[
\chi(t)=
\begin{cases}
1,&t\le1/4,\\
\lambda/c_m,&t\ge1/4.
\end{cases}
\]

If `m` is inner, positivity and `F_m <= CB_m` give

\[
N_mF_m\preceq KF_m
\preceq CKB_m
\preceq C\frac\lambda{c_m}V_m.                 \tag{22}
\]

Thus `N_mF_m <= C chi V_m` in both cases.  By (16), define

\[
P_s=2a'(p)H(p)-a''(p),
\qquad M_s=2a'(m)H(m)-a''(m).
\]

Subtracting the upper bound for (12) from `9CB_n` gives

\[
9CB_n-9F_n\succeq D_pB_p+D_mB_m,               \tag{23}
\]

where

\[
D_p=8Cc_p-P_s,
\qquad D_m=(9C-C\chi)c_m-M_s.
\]

The scalar gate proves

\[
D_m>0.0224,
\qquad D_p+D_m>0.0282.                          \tag{24}
\]

If `D_p >= 0`, (23) is immediate.  If `D_p < 0`, use `B_m >= B_p` and
`D_m > 0`.  Hence `F_n <= C B_n`.

The certificate proves the curvature base at level 26.  Evenness gives
`E_26(0)=0`, and `E_26'=F_26 >= 0`, so the full cone propagates for every
`n >= 26`.

## 6. Deducing the targets

The scalar gate proves

\[
H(5/18)<1.086,
\qquad H(1/2)<1.663.                            \tag{25}
\]

Monotonicity and integration of (16) now give TS1 and TS2.

For TS3, the children of `t_in` are `r` and `r_2`, so

\[
B_{n+1}(t_{\rm in})=N_rB_n(r)+N_{r_2}B_n(r_2). \tag{26}
\]

The shape inequality and (17) give

\[
B_n(r_2)\succeq\rho(\varepsilon)B_n(r),
\qquad
\rho(\varepsilon)=\frac{\cos(\mu r_2)}{\cos(\mu r)}.
\]

The scalar gate proves

\[
\lambda+d(r)+\rho(\varepsilon)(\lambda+d(r_2))
>\frac76+0.095.                                 \tag{27}
\]

This proves TS3 with substantial slack.  The finite gate covers `5 <= n <=
26`; the invariant covers every later level.

## 7. Continuum certificate

Map `[0,1/2]` to `[-1,1]` by `t=(1+x)/4` and use the Bernstein ellipse
`E_2`.  Its imaginary semiaxis in the `t` plane is `3/16`.  The two child
maps send `E_2` into itself: the plus map is a convex combination of a point
inside `E_2` and the input, and the minus map is a contracted reflection.

On the child images,

\[
\|K\|_{\ell^1\to\ell^1}=\frac12,
\qquad
|d(t_\pm)|\le\frac12\cosh(2\pi/16).
\]

The verifier propagates explicit complex-domain bounds for `B`, `E`, `F`,
and `F'`.  If an analytic scalar function is bounded by `M` on `E_rho`, its
Chebyshev coefficients satisfy `|a_k| <= 2M rho^{-k}`.  Lobatto
interpolation aliases each omitted Chebyshev mode to a mode of real sup norm
at most one.  The exact tail plus its alias therefore has norm at most

\[
\frac{4M\rho^{-K}}{\rho-1}.
\]

The verifier uses the more conservative bound

\[
16M\rho^{-K}/(\rho-1).                          \tag{28}
\]

For nodal errors bounded by `delta`, the DCT-I formula gives

\[
\|I_K e\|_\infty\le2K\delta.                   \tag{29}
\]

Every inherited error is propagated with this explicit operator bound.
Midpoint balls plus rigorous derivative radii cover every continuum cell.
The top identities (3) cover the exact curvature coordinates omitted from
the finite numerical loop.

The certificate uses 448-bit Arb arithmetic, degree 320, `rho=2`, 512 cells
for the scalar and base gates, and 256 epsilon cells for the finite targets.
It records every certified margin with its worst continuum cell and
coordinate.  It pins the proof, verifier, replay wrapper, upstream base,
consumer script, exact rational consumer contract, and consumed dense-shell
note.

The same base and scalar gates are also evaluated with interval-valued
parameters and prove the cone uniformly on the rational box

\[
0.48199\le\lambda\le0.48201,
\qquad
2.57799\le C\le2.57801.                       \tag{30}
\]

Thus the proof is not a single-point numerical coincidence at
`lambda=241/500`, `C=1289/500`.  The finite TS1--TS3 gate is independent of
these auxiliary cone parameters.

## 8. Master consequence and boundary

The existing four-grandchild master reduction consumes exactly TS1, TS2,
and TS3.  The scalar gate certifies

\[
\left(e^{-1.663g}-\operatorname{need}(\varepsilon)\right)
\frac76 e^{-1.086g}
-\sin(4\pi/9)\sin(\pi g)>0.00574               \tag{31}
\]

on the full epsilon interval.  Therefore `INV-TAIL` is discharged, the
master theorem is unconditional at every depth, and the `|K| <= 1`
dense-shell class-sign theorem holds for every `B`.

The next independent obligation is the general decorated charge

\[
T_\pi(K)>0\qquad(|K|\ge2).
\]

The producer and class-charge consumer both read
`experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json`,
which fixes TS1, TS2, TS3, and the master-margin floor as exact rationals.

This note does not claim it and does not alter the remaining product-profile
admission, non-product-band, large-moment Sidon, atlas-totality, or distinct-
ray obligations.
