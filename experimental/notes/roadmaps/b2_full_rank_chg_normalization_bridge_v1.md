# B2 full-rank CHG normalization bridge

## Status

```text
FULL-RANK CHG NORMALIZATION BRIDGE: PROVED.
FULL-RANK DEPLOYED ZERO-FIBER ENDPOINT IDENTIFICATION: PROVED.
SIGNED HANKEL--SALIE ESTIMATE: OPEN.
LOWER-RANK PSEUDODETERMINANT STRATA: OPEN.
N(0) <= n^3 / MAX-FIBER / LS: OPEN.
```

This note fixes the scalar, determinant, centering, and Fourier conventions in
the full-rank target of `b2_hankel_gauss_reduction.md`.  It connects the
centered full-rank CHG sum to the nonsingular twisted Hankel transform proved
in `b2_twisted_hankel_transform_v1.md`.

The bridge is exact.  It does not estimate the resulting signed
Hankel--Salie aggregate.

## 1. Ledger convention and quadratic setup

Use

```text
N(v)-mu = p^(-n) sum_(r=r_*...d) T_r(v),
T_r(v)  = sum_(rank A_lambda=r) (G_v(lambda)-barG_m(lambda)),
barG_m(lambda)=p^(-w) sum_(eta in F_p^w) G_eta(lambda),
d=n-w-1,
c=w+1=n-d.                                        (B1)
```

The repository's full-rank target is

```text
|T_d(v)| <= p^(n+2-c/2).                           (B2)
```

Let `k=F_p`, `psi=e_p`, `chi` be the quadratic character, and

```text
g=sum_(x in k) psi(x^2),
g^2=chi(-1)p.                                      (B3)
```

On `H=mu_n`, define

```text
r_v(X)=n^(-1)(m+sum_(j=1...w) v_j X^(-j)),
h_v(X)=2r_v(X)-1,
g_u(X)=sum_(i=1...d)u_iX^i,
f_(u,v)=r_v+g_u.                                  (B4)
```

Then

```text
G_v(lambda)=sum_(u in k^d)
  psi(sum_(a in H) lambda_a(f_(u,v)(a)^2-f_(u,v)(a))). (B5)
```

Put `T=supp(lambda)`, `D_lambda=diag(lambda_a)_(a in T)`, and

```text
E_T=(a^i)_(a in T,1<=i<=d),
A_lambda=E_T^T D_lambda E_T.                       (B6)
```

For `h=(h_v(a))_(a in T)`, set

```text
ell=E_T^T D_lambda h,
gamma=(h^T D_lambda h-sum_(a in T)lambda_a)/4.     (B7)
```

Thus

```text
G_v(lambda)=sum_u psi(u^T A_lambda u+ell^T u+gamma). (B8)
```

When `A_lambda` is nonsingular, completion of the square gives

```text
G_v(lambda)=g^d chi(det A_lambda)
  psi(gamma-ell^T A_lambda^(-1)ell/4).             (B9)
```

## 2. Complementary Hankel matrix

Suppose

```text
t=|T|>=d,
q=t-d,
Z=H\T,
s=|Z|=c-q.                                        (B10)
```

Let

```text
L_T(X)=product_(a in T)(X-a),
L_Z(X)=product_(z in Z)(X-z).
```

Since `L_TL_Z=X^n-1`, for `a in T`,

```text
L_T'(a)L_Z(a)=na^(-1).                             (B11)
```

Define the `t x q` matrix `W=W_T` by

```text
W_(a,r)=a^(r-1)/L_T'(a)=(L_Z(a)/n)a^r,
0<=r<q.                                           (B12)
```

The Lagrange identity

```text
sum_(a in T) a^j/L_T'(a)=0, 0<=j<=t-2,
```

gives

```text
E_T^T W=0,
im W=ker E_T^T.                                   (B13)
```

Define

```text
B^0_(Z,lambda)=W^T D_lambda^(-1)W.                (B14)
```

It is an ordinary `q x q` Hankel matrix:

```text
(B^0_(Z,lambda))_(r,u)
 =sum_(a in T) L_Z(a)^2 a^(r+u)/(n^2 lambda_a).   (B15)
```

## 3. Rank duality and determinant reciprocity

If `x in ker A_lambda`, then `D_lambda E_Tx` lies in `im W`, so there is a
unique `y` with

```text
D_lambda E_Tx=Wy.
```

This sends `ker A_lambda` to `ker B^0_(Z,lambda)`.  Conversely, if
`B^0_(Z,lambda)y=0`, then `D_lambda^(-1)Wy` lies in `ker W^T=im E_T`, which
reverses the construction.  Therefore

```text
nullity A_lambda=nullity B^0_(Z,lambda),
rank A_lambda=d iff det B^0_(Z,lambda)!=0.         (B16)
```

In the full-rank case,

```text
U=[E_T,D_lambda^(-1)W]
```

is invertible and

```text
U^T D_lambda U=diag(A_lambda,B^0_(Z,lambda)).      (B17)
```

Hence

```text
det A_lambda det B^0_(Z,lambda)
  =(det U)^2 product_(a in T)lambda_a,             (B18)
```

and

```text
chi(det A_lambda)chi(det B^0_(Z,lambda))
  =product_(a in T)chi(lambda_a).                  (B19)
```

## 4. Canonical -4 inverse normalization

For `a in T`, put

```text
kappa_(Z,a)=(L_Z(a)/n)^2,
xi_a=-4 kappa_(Z,a)/lambda_a.                     (B20)
```

This is a coordinatewise bijection on `(k^times)^T`.  Define

```text
B_Z(xi)=-4B^0_(Z,lambda).                         (B21)
```

Then

```text
B_Z(xi)_(r,u)=sum_(a in T)xi_a a^(r+u).           (B22)
```

The determinant character becomes

```text
chi(det A_lambda)
 =chi((-1)^d)(product_(a in T)chi(xi_a))chi(det B_Z(xi)). (B23)
```

There is no residual `q`-dependent sign.  Indeed,

```text
chi(lambda_a)=chi(-1)chi(xi_a),
chi(det B^0)=chi((-1)^q)chi(det B_Z),
t=d+q.
```

## 5. Complementary phase and explicit twist

The complementary projector identity is

```text
D_lambda-D_lambda E_T A_lambda^(-1) E_T^T D_lambda
  =W(B^0_(Z,lambda))^(-1)W^T.                     (B24)
```

It follows by applying both sides to the basis
`[E_T,D_lambda^(-1)W]`.

Set

```text
z_Z(v)=W^T h.                                     (B25)
```

Using `(B24)` and `B_Z=-4B^0`,

```text
gamma-ell^T A_lambda^(-1)ell/4
 =sum_(a in T) kappa_(Z,a)/xi_a
  -z_Z(v)^T B_Z(xi)^(-1)z_Z(v).                  (B26)
```

Write

```text
L_Z(X)=sum_(k=0...s)ell_(Z,k)X^k,
beta_0=m-n/2,
beta_j=v_j, 1<=j<=w.                              (B27)
```

Multiplicative orthogonality on `H` gives, for `0<=r<q`,

```text
z_(Z,r)(v)=(2/n) sum_(k=0...s) ell_(Z,k) beta_(k+r). (B28)
```

There is no wraparound because `0<=k+r<=c-1=w<n`.

For `Z=empty`,

```text
z_empty(v)=((2m-n)/n,2v_1/n,...,2v_w/n).          (B29)
```

### Corollary - zero-fiber endpoint identification

For `v=0`, only `beta_0=m-n/2` is nonzero.  Equation `(B28)` therefore gives

```text
z_Z(0)=(2 beta_0 ell_(Z,0)/n)e_0.                 (B30)
```

This scalar can vanish on a balanced row with `m=n/2`; the `(7,6,1,3)` toy is
such an example.  For every full-rank stratum with `q>=1`, it is nonzero at
deployment:

```text
beta_0=-c!=0 mod p,
ell_(Z,0)=(-1)^s product_(z in Z)z!=0,
n!=0 mod p.
```

Thus:

```text
DEPLOYED ZERO-FIBER ENDPOINT IDENTIFICATION: PROVED
for every surviving full-rank support stratum q>=1. (B31)
```

The `q=0` support layer cancels after centering, as shown below.

## 6. Exact termwise bridge

For a `q x q` Hankel matrix, define

```text
F_z^(q)(B)=chi(det B)psi(-z^T B^(-1)z), det B!=0,
F_z^(q)(B)=0,                         det B=0.      (B32)
```

Combining `(B9)`, `(B23)`, and `(B26)` gives, whenever `rank A_lambda=d`,

```text
G_v(lambda(xi))
 =chi((-1)^d)g^d
  (product_(a in T)chi(xi_a))
  psi(sum_(a in T)kappa_(Z,a)/xi_a)
  F_(z_Z(v))^(q)(B_Z(xi)).                        (B33)
```

By `(B16)` and the zero extension in `(B32)`, the right side may be summed
over every `xi in (k^times)^T` without a separate nonsingularity predicate.

## 7. Exact centering

For `q=0`, one has `|T|=d`.  The affine evaluation map on `T` is bijective,
and the one-coordinate identity

```text
sum_(y in k) sum_(lambda!=0) psi(lambda(y^2-y))=p
```

gives

```text
sum_(supp lambda=T)G_v(lambda)=p^d.               (B34)
```

This is independent of `v`; the complete fixed-`T` support layer, not each
individual term, vanishes after centering.

For `q>=1`, define

```text
C_(Z,m)^(q)(B)=p^(-w)sum_(eta in k^w)F_(z_Z(eta))^(q)(B). (B35)
```

Then

```text
T_d(v)=chi((-1)^d)g^d
 sum_(q=1...c) sum_(Z subset H,|Z|=c-q)
 sum_(xi in (k^times)^(H\Z))
   (product_(a notin Z)chi(xi_a))
   psi(sum_(a notin Z)kappa_(Z,a)/xi_a)
   [F_(z_Z(v))^(q)(B_Z(xi))-C_(Z,m)^(q)(B_Z(xi))]. (B36)
```

### The non-full-support center

If `Z!=empty`, then `q<=w`.  The map `eta -> z_Z(eta)` is surjective onto
`k^q`: the variables `eta_s,...,eta_(s+q-1)` give a triangular coefficient
matrix with diagonal `ell_(Z,s)=1`.

Gaussian linearization and averaging over `z in k^q` therefore give

```text
C_(Z,m)^(q)(B)=g^(-q)1_(det B!=0), Z!=empty.      (B37)
```

### The full-support center

For `Z=empty`, put

```text
a_m=(2m-n)/n,
z_empty(v)=(a_m,2v_1/n,...,2v_w/n).
```

Averaging over `v` forces all Gaussian coordinates except `r_0` to vanish.
If `b_0=B_(0,0)`,

```text
C_(empty,m)^(c)(B)
 =1_(det B!=0)g^(-c)sum_(t in k)psi(b_0t^2+2a_mt). (B38)
```

At deployment `a_m!=0`, so

```text
C_(empty,m)^(c)(B)
 =g^(-w)chi(b_0)psi(-a_m^2/b_0), det B!=0,b_0!=0,
 =0,                                  otherwise.  (B39)
```

Thus full-support centering removes a scalar one-dimensional `F` slice, not
the constant mode removed by `(B37)`.

## 8. Coefficient Fourier pairing and Salie pushforward

Let `W_q=k^(2q-1)` parameterize `q x q` Hankel matrices by

```text
H_q(b)_(r,u)=b_(r+u).
```

For `P(X)=sum_jP_jX^j`, use

```text
<P,b>=sum_jP_jb_j.                                (B40)
```

This is not the matrix trace pairing.  If

```text
b_j(xi)=sum_(a in T)xi_a a^j,
```

then

```text
<P,b(xi)>=sum_(a in T)xi_aP(a).                   (B41)
```

Use the plus-sign transform and inversion

```text
hat f(P)=sum_b f(b)psi(<P,b>),
f(b)=p^(-(2q-1))sum_P hat f(P)psi(-<P,b>).        (B42)
```

Define the weighted pushforward

```text
rho_Z(b)=sum_(xi mapping to b)
  (product_(a in T)chi(xi_a))
  psi(sum_(a in T)kappa_(Z,a)/xi_a).              (B43)
```

Then

```text
hat rho_Z(P)=product_(a in T) S(kappa_(Z,a),P(a)), (B44)
S(kappa,t)=sum_(xi!=0)chi(xi)psi(kappa/xi+t xi).  (B45)
```

`S` is the quadratically twisted Kloosterman, or Salie, kernel.

Put

```text
F_(Z,v)^circle=F_(z_Z(v))^(q)-C_(Z,m)^(q).
```

Fourier inversion yields the bilinear pairing

```text
T_d(v)=chi((-1)^d)g^d
 sum_(q,Z) p^(-(2q-1))sum_P
   hat(F_(Z,v)^circle)(-P)
   product_(a notin Z)S(kappa_(Z,a),P(a)).        (B46)
```

The minus sign is forced by inversion.  There is no complex conjugation.

## 9. Inserting the twisted Elkies transform

Let

```text
E_q(Y)=p^(2q-1)1_(Y=0)
 -p^(q-1)(omega_(q-1)(Y)-omega_(q-2)(Y)).         (B47)
```

By Elkies Theorem 1, this is exactly the Fourier transform of the nonsingular
`q x q` Hankel locus under `(B42)`.

For `r=(r_0,...,r_(q-1))`, let `R(X)=sum_jr_jX^j`.  The transform theorem in
`b2_twisted_hankel_transform_v1.md` gives

```text
hat(F_z^(q))(-P)=g^(-q)sum_(r in k^q)
  psi(2z^Tr)E_q(R^2-P).                           (B48)
```

For `Z!=empty`, centering removes exactly the `r=0` term:

```text
hat(F_(Z,v)^circle)(-P)=g^(-q)sum_(r!=0)
  psi(2z_Z(v)^Tr)E_q(R^2-P).                      (B49)
```

For `Z=empty`, centering removes the full line
`r=(t,0,...,0)`:

```text
hat(F_(empty,v)^circle)(-P)=g^(-c)sum_r [
  psi(2z_empty(v)^Tr)
  -psi(2a_mr_0)1_(r_1=...=r_w=0)
]E_c(R^2-P).                                      (B50)
```

Equations `(B46)`, `(B49)`, and `(B50)` are the fully expanded full-rank
CHG--Elkies formula.

## 10. Exact CHG normalization

Define

```text
H_d(v)=sum_(q,Z) p^(-(2q-1))sum_P
  hat(F_(Z,v)^circle)(-P)
  product_(a notin Z)S(kappa_(Z,a),P(a)).         (B51)
```

Then

```text
T_d(v)=chi((-1)^d)g^d H_d(v).                     (B52)
```

Since `|g|=p^(1/2)` and `d+c=n`,

```text
|T_d(v)| <= p^(n+2-c/2)
iff
|H_d(v)| <= p^(n/2+2).                            (B53)
```

For the deployed row,

```text
p=2130706433,
n=2097152,
c=67472,
d=2029680,
m=981104=n/2-c,
beta_0=-c,
a_m=-2c/n.
```

Here `p=1 mod 4` and `d` is even, so

```text
chi((-1)^d)g^d=p^(d/2)=p^1014840.                (B54)
```

Therefore, exactly,

```text
T_d(v)=p^1014840 H_d(v),                          (B55)
|T_d(v)|<=p^2063418 iff |H_d(v)|<=p^1048578.      (B56)
```

This proves the normalization bridge.  The bound on `H_d(v)` is the remaining
signed analytic theorem.

## 11. Proof boundary and next theorem

Proved here:

```text
- full-rank rank duality and determinant reciprocity;
- canonical -4 inverse variables;
- the complete scalar phase and explicit z_Z(v);
- deployed zero-fiber endpoint identification on every q>=1 full-rank stratum,
  with the balanced `m=n/2` zero-twist exception printed;
- q=0 centered cancellation;
- non-full and full-support centering formulas;
- coefficient Fourier pairing and Salie factorization;
- exact T_d/H_d normalization and deployed exponents.
```

Still open:

```text
- |H_d(v)|<=p^(n/2+2);
- lower-rank pseudodeterminant strata;
- the aggregate CHG conjecture, LS, and N(0)<=n^3.
```

The next load-bearing target is the sign-sensitive estimate for `(B51)` after
substituting `(B49)-(B50)`.  Termwise absolute Salie or divisor bounds do not
provide that cancellation.

## 12. Verification

Run:

```bash
python experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --check
python experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --tamper-selftest
```

The stdlib verifier checks the rank, determinant, `-4`, projector, phase,
explicit-twist, endpoint, centering, coefficient-pairing, Salie-factorization,
and deployed-exponent identities on the integrated `(7,6,1,3)` and
`(11,5,1,2)` toys.  These finite checks protect normalization; they do not
replace the proof or establish the open signed estimate.

## Sources

```text
N. D. Elkies, On finite sequences satisfying linear recursions,
New York J. Math. 8 (2002), Theorem 1,
https://nyjm.albany.edu/j/2002/8-5.pdf

Integrated reduction context:
experimental/notes/roadmaps/b2_hankel_gauss_reduction.md
```
