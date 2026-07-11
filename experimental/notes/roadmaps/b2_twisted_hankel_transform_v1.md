# B2 twisted full-rank Hankel transform and zero-fiber divisor normal forms

## Status

```text
ZERO-FIBER DIVISOR NORMAL FORMS: PROVED.
UNIFORM SUBSET-FOURIER IDENTITY: PROVED.
TWISTED NONSINGULAR HANKEL TRANSFORM: PROVED.
ABSTRACT ENDPOINT-POLAR DIVISOR DESCENT: PROVED.
FULL-RANK CHG NORMALIZATION BRIDGE: PROVED.
FULL-RANK DEPLOYED ZERO-FIBER ENDPOINT IDENTIFICATION: PROVED.
FULL CHG RANK-STRATUM ESTIMATE / LS / N(0) <= n^3: OPEN.
```

This note supplies an exact transform requested by
`b2_hankel_gauss_reduction.md`: the determinant-character and
inverse-quadratic twist on the nonsingular ordinary Hankel stratum can be
Fourier transformed into a signed square-plus-form divisor count.  It also
records exact zero-fiber divisor identities and an abstract endpoint-polar
descent.

The packet does **not** prove

```text
N(0) <= n^3,
max_v N(v) <= n^3,
the CHG rank-stratum conjecture,
the lower-rank pseudodeterminant transform,
(LS), or (SV*).
```

The companion note `b2_full_rank_chg_normalization_bridge_v1.md` now derives
the exact complementary-Hankel normalization and proves that every surviving
full-rank zero-fiber twist is a nonzero multiple of `e_0`.  The signed aggregate
estimate and all lower-rank strata remain open.

## 1. Deployed notation

Let

```text
n = 2097152,
w = 67471,
c = w+1 = 67472,
h = n/2 = 1048576,
m = 981104 = h-c.
```

Then

```text
n-m = h+c,
n = 2m+2c,
r_* = n-2w-2 = n-2c = 2m.
```

Let `p` be the deployed odd prime, let `H=mu_n subset F_p^times`, and
write

```text
P_j(S) = sum_{a in S} a^j.
```

For an `m`-subset `S subset H`, define

```text
Q_S(X) = product_{a in S}(X-a),
R_S(X) = (X^n-1)/Q_S(X).
```

## 2. Exact zero-fiber divisor theorem

### Proposition 2.1 - complementary coefficient gaps

For `|S|=m`, the following are equivalent:

```text
P_j(S)=0 for 1 <= j <= w,                         (Z1)
Q_S(X)=X^m+A(X), deg A <= m-c.                    (Z2)
```

When these conditions hold,

```text
R_S(X)=X^(n-m)+B(X), deg B <= n-m-c=h.            (Z3)
```

#### Proof

Write

```text
Q_S=X^m-e_1X^(m-1)+e_2X^(m-2)-... .
```

For `1<=k<=w<p`, Newton's identity is

```text
k e_k = sum_{j=1}^k (-1)^(j-1) e_(k-j) P_j(S).
```

It gives recursively

```text
P_1(S)=...=P_w(S)=0 iff e_1=...=e_w=0,
```

which is `(Z2)`.  Also `P_j(H)=0` for `1<=j<n`, so the complement
`H\S` has the same first `w` vanishing power sums.  Applying the same
argument to its locator proves `(Z3)`.

Consequently,

```text
N(0) = #{Q | X^n-1 :
           deg Q=m,
           Q=X^m+O(X^(m-c)),
           (X^n-1)/Q=X^(n-m)+O(X^(n-m-c))}.       (Z4)
```

This is a bijective divisor description, because `X^n-1` is squarefree and
its roots are exactly `H`.

### Proposition 2.2 - Bezout and Boolean interpolation certificate

Suppose

```text
Q=X^m+A, R=X^(n-m)+B, QR=X^n-1
```

with the gaps above.  Define

```text
D_Q = XQ'-mQ = XA'-mA,
D_R = XR'-(n-m)R = XB'-(n-m)B.
```

Then

```text
deg D_Q <= m-c,
deg D_R <= n-m-c,
D_Q R + Q D_R = n.                                (Z5)
```

Indeed, differentiate `QR=X^n-1`, multiply by `X`, and subtract `nQR`.

Let `f_S` be the unique polynomial of degree `<n` whose values on `H` are
the indicator of `S`.  Equation `(Z5)` gives

```text
f_S   = D_Q R/n,
1-f_S = Q D_R/n.                                  (Z6)
```

Both right sides have degree `<n`; evaluation at roots of `Q` and `R`
proves the identities.  Therefore

```text
f_S(1-f_S) = D_Q D_R (X^n-1)/n^2.                 (Z7)
```

For `g_S=2f_S-1`, equivalently,

```text
g_S+1 =  2D_QR/n,
g_S-1 = -2QD_R/n.                                 (Z8)
```

This is an exact polynomial Pell-type factorization.  Its current degree
ranges do not by themselves give a polynomial count.

### Proposition 2.3 - first dyadic divisor split

Write

```text
Q=X^m-u, deg u<=m-c, s=X^c u.
```

Since `n=2m+2c`, reduction modulo `Q` gives

```text
X^n = X^(2c)(X^m)^2 = s^2 mod Q.
```

Hence

```text
Q | s^2-1=(s-1)(s+1),                             (Z9)
X^cQ=X^h-s.                                       (Z10)
```

Because `p` is odd and `Q` is squarefree, there is a unique split

```text
Q=Q_+Q_-,
Q_+=gcd(Q,s-1),
Q_-=gcd(Q,s+1).                                   (Z11)
```

At a root `a` of `Q`,

```text
s(a)=a^(m+c)=a^h in {1,-1}.
```

This is exactly the first quadratic-conductor split.  No recursive count is
claimed: neither factor is known to inherit the long coefficient gap.

The classical Redei theorem for fully split polynomials `X^p+g(X)` has the
wrong leading degree for `(Z4)`.  This note does not invoke a
Kopparty--Wang coefficient-gap theorem; any future use of such a result must
print its exact source and hypotheses.

## 3. Exact uniform subset-Fourier identity

Let `psi(t)=exp(2*pi*i*t/p)`.  Additive orthogonality for weight and the first
`w` moments gives, for `v=(v_1,...,v_w)`,

```text
N(v) = p^(-c) sum_{u_0,...,u_w in F_p}
         psi(-m u_0-sum_{j=1}^w u_j v_j)
         product_{a in H}
           (1+psi(u_0+sum_{j=1}^w u_j a^j)).       (F1)
```

The line `u_1=...=u_w=0` is

```text
p^(-c) sum_{u_0} psi(-m u_0)(1+psi(u_0))^n
  = binom(n,m)/p^w
  =: mu.                                           (F2)
```

Here `0<=m<=n<p`, so the root-of-unity filter selects only the term of
weight `m`.  Thus

```text
N(v)-mu = p^(-c)
  sum_{u:(u_1,...,u_w)!=0}
    psi(-m u_0-<u',v>)
    product_{a in H}(1+psi(P_u(a))).               (F3)
```

At deployment,

```text
log2(mu) approximately 35.7352,
log2(n^3)=63.
```

The excess budget is therefore about `27.26` bits, while `(F3)` has
`p^c` signed terms.  Replacing the sum by absolute values is not a viable
route.  Also, the zero fiber lacks the syndrome twist `psi(-<u',v>)`; a
zero-fiber estimate is not automatically uniform in `v`.

## 4. Twisted nonsingular Hankel transform

This section fixes all normalizations.

Let

```text
V_j = {polynomials over F_p of degree <= j}.
```

As in Elkies, `P(V_j)` is the projective space of homogeneous binary forms of
degree exactly `j`, written after dehomogenization as coefficient vectors of
length `j+1`.  A vector whose top coefficients vanish still carries its fixed
homogeneous degree.  Thus `Q in P(V_j)` divides a form `Y` of homogeneous
degree `D` only when the dehomogenized quotient has degree at most `D-j`.

For `Y in V_(2c-2)`, define

```text
omega_j(Y) = #{[Q] in P(V_j): Q divides Y},
omega_(-1)(Y)=0.                                  (H1)
```

Divisors are homogeneous and projective: nonzero scalar multiples of `Q` are
counted once.
Every nonzero polynomial divides the zero polynomial, so

```text
omega_j(0)=|P(V_j)|=(p^(j+1)-1)/(p-1).
```

For `b=(b_0,...,b_(2c-2))`, let

```text
B(b)_(ij)=b_(i+j), 0<=i,j<c.                      (H2)
```

For `x=(x_0,...,x_(c-1))`, identify

```text
X_x(T)=sum_i x_i T^i
```

and let `x^2 in V_(2c-2)` be the coefficient vector of `X_x(T)^2`.  Use the
coefficient pairing

```text
<P,b>=sum_{r=0}^{2c-2} P_r b_r,
```

so that

```text
x^T B(b) x = <x^2,b>.                             (H3)
```

For `z in F_p^c`, set

```text
F_z(B) = chi(det B) psi(-z^T B^(-1)z), det B!=0,
F_z(B) = 0,                         det B=0.       (H4)
```

The unnormalized plus-sign Fourier transform is

```text
hat(F_z)(P)=sum_{b in F_p^(2c-1)} F_z(B(b))psi(<P,b>). (H5)
```

Finally put

```text
G_p=sum_{t in F_p}psi(t^2), |G_p|=sqrt(p).
```

### Theorem 4.1 - twisted Elkies formula, nonsingular stratum

For odd `p`,

```text
hat(F_z)(P) = G_p^(-c) sum_{x in F_p^c} psi(2z^T x) [
    p^(2c-1) 1_{P+x^2=0}
  - p^(c-1)(omega_(c-1)(P+x^2)-omega_(c-2)(P+x^2))
].                                                (H6)
```

#### Proof

For nonsingular symmetric `B`, completion of the square gives

```text
sum_x psi(x^T Bx+2z^T x)
  = G_p^c chi(det B) psi(-z^T B^(-1)z).           (H7)
```

Insert `(H7)` into `(H5)` and interchange the `x` and `b` sums.  By `(H3)`,
the inner sum is

```text
sum_{det B(b)!=0} psi(<P+x^2,b>).                 (H8)
```

The sum over all Hankel matrices is

```text
p^(2c-1) 1_{P+x^2=0}.                             (H9)
```

Elkies's exact unnormalized transform of the singular `c x c` Hankel locus
is

```text
p^(c-1)(omega_(c-1)(Y)-omega_(c-2)(Y)).           (H10)
```

Subtract `(H10)` from `(H9)` and substitute `Y=P+x^2`.  This proves `(H6)`.

The theorem is an exact algebraic transform, not an estimate.  It linearizes
the determinant and inverse-quadratic twists into a signed count of
factorizations of `P+X_x^2`.  It covers the nonsingular/full-rank ordinary
Hankel stratum only.

Primary sources:

```text
N. D. Elkies, On finite sequences satisfying linear recursions,
New York J. Math. 8 (2002), 85-97,
https://arxiv.org/abs/math/0105007

S. Dwivedi and D. Grinberg, Counting Hankel matrices of a given rank,
https://arxiv.org/abs/2109.05415
```

The second source supplies exact rank counts, not the additive
inverse-quadratic twist `(H4)`.

### Elkies Theorem 1 specialization

Elkies works with the vector space `V_D` of homogeneous binary forms of degree
`D` and its dual sequence space `W_D`.  His `H_m subset W_D` is the locus whose
`(m+1) x (D-m+1)` Hankel matrix has rank at most `m`.  His Fourier convention
is the same unnormalized plus-sign convention as `(H5)`:

```text
hat f(P)=sum_{b in W_D} f(b) psi(<P,b>).
```

Theorem 1 of Elkies states

```text
hat(1_(H_m))(P)=p^m(omega_m(P)-omega_(m-1)(P)).    (E1)
```

Set

```text
D=2c-2,
m=c-1.
```

Then `H_(c-1)` is exactly the singular locus of the `c x c` Hankel matrix
`B(b)`, and `(E1)` becomes `(H10)` without a sign or normalization change:

```text
sum_{det B(b)=0} psi(<Y,b>)
  = p^(c-1)(omega_(c-1)(Y)-omega_(c-2)(Y)).       (E2)
```

Reference: N. D. Elkies, *On Finite Sequences Satisfying Linear Recursions*,
New York J. Math. 8 (2002), Theorem 1, equation (35),
`https://nyjm.albany.edu/j/2002/8-5.pdf`.

## 5. Polar-orbit cancellation

Put `k=c-1` and define

```text
D_z(P)=sum_{x in V_k} psi(2z dot x)
  (omega_k(P+x^2)-omega_(k-1)(P+x^2)).            (P1)
```

### Proposition 5.1 - exact polar filtering

For `[Q] in P(V_k)`, the condition `Q|(P+x^2)` is invariant under

```text
x -> x+tQ, t in F_p.
```

The orbit character sum vanishes unless

```text
z dot Q=0.                                        (P2)
```

For `[Q] in P(V_(k-1))`, the condition is invariant under

```text
x -> x+LQ, L in V_1.
```

That orbit sum vanishes unless

```text
z is perpendicular to QV_1.                      (P3)
```

Therefore

```text
D_z(P)
 = sum_[Q] in P(V_k), z dot Q=0
       sum_x:Q|(P+x^2) psi(2z dot x)
   - sum_[Q] in P(V_(k-1)), z perpendicular QV_1
       sum_x:Q|(P+x^2) psi(2z dot x).             (P4)
```

The actions are free, and their complete additive-character sums prove the
claim.

### Proposition 5.2 - abstract endpoint descent

Assume

```text
z=beta e_0, beta!=0.                              (P5)
```

Then `(P2)` and `(P3)` both say that the constant coefficient of `Q`
vanishes, equivalently `T|Q`.  A divisor `Q=TQ'` of `P+x^2` can occur only
when

```text
P(0)+x_0^2=0.
```

Removing the common endpoint factor gives

```text
D_(beta e_0)(P)
 = sum_{x in V_k: P(0)+x_0^2=0} psi(2 beta x_0) [
     omega_(k-1)((P+x^2)/T)
   - omega_(k-2)((P+x^2)/T)
   ].                                             (P6)
```

There are at most two possible values of `x_0`.  This removes one field
dimension and forces every surviving middle divisor through a fixed endpoint.

### Full-rank bridge supplied by the companion note

The companion normalization note proves, for a full-rank support stratum with
zero set `Z`, that the induced complementary vector has coordinates

```text
z_(Z,r)(v)=(2/n)sum_k ell_(Z,k) beta_(k+r),
beta_0=m-n/2,
beta_j=v_j.                                       (P7)
```

For `v=0`, only `beta_0` is nonzero, so

```text
z_Z(0)=(2 beta_0 ell_(Z,0)/n)e_0.
```

At deployment `beta_0=-c!=0`, and `ell_(Z,0)` is a nonzero product of roots
from `H`.  Thus `(P6)` applies to every `q>=1` deployed full-rank zero-fiber
stratum.  Balanced rows with `m=n/2` instead have the zero twist; the `q=0`
support layer cancels after centering.

For general `v`, the conditions remain the syndrome-dependent polar
hyperplanes `(P2)-(P3)`.  Endpoint descent is therefore not a uniform
max-atom argument.

## 6. CHG-linked toy cancellation census

The companion script

```text
experiment_b2_twisted_hankel_cancellation_v1.py
```

adds two finite diagnostics.

First, it evaluates the ordinary-Hankel target `(H4)-(H6)` at the same field
and order `c=w+1` as the integrated CHG toys `(7,6,1,3)` and `(11,5,1,2)`.
It compares the termwise absolute transformed bound with the exact signed
transform, checks the cyclotomic identity at every sampled point, and records
polar-incidence reduction.  The `(p,c)=(7,2)` target space is exhaustive;
`(11,2)` uses a deterministic sample.

Second, it reconstructs the original-coordinate Gaussian twist

```text
z_A(lambda,v)=l(lambda,v)/2
```

for every full-rank `A_lambda` in both integrated toys.  This is the completion
vector before complementary-Hankel rank duality.  It does not identify
`z_A(lambda,v)` with the complementary-Hankel vector `z(v)` in `(H4)`.  The
census therefore tests conventions and quantifies twist diversity without
substituting one coordinate system for the other.  The companion bridge note
now supplies their exact relationship.

The generated JSON packet prints the exact observed counts.  Its intended
review questions are:

```text
- can termwise absolute divisor mass exceed the toy n^3 scale while the signed
  transform remains below it?
- how much projective-divisor incidence survives polar filtering?
- is the original-coordinate zero-syndrome completion vector concentrated on
  one coordinate axis, or does complementary duality have real work to do?
```

These are finite experiments, not asymptotic evidence for CHG.

### Observed finite results

The deterministic packet reports:

```text
(p,c)=(7,2):
  all 7^5=16807 target pairs checked exactly;
  7056 signed transforms vanish;
  no termwise-bound versus n^3 separation occurs in this toy.

(p,c)=(11,2):
  500 deterministic target pairs checked exactly;
  242 signed transforms vanish;
  z=(1,7), P=(10,3,6) gives
      termwise absolute transformed bound = 374,
      signed transform magnitude          = 31.3093...,
      toy n^3                             = 125.
```

Thus the termwise absolute transformed bound is inconclusive on an explicit
toy where the signed value is comfortably below the target.  This is a finite
demonstration of the cancellation that the live estimate must preserve; it is
not a scaling theorem.

For 40 deterministic `(p,k)=(3,2)` polar samples, the exact filtered and
unfiltered sums agree, while the mean retained projective-divisor incidence is
approximately `0.17759` of the raw incidence.

The original-coordinate full-rank twist census gives:

```text
(p,n,w,m)=(7,6,1,3):
  99372 full-rank lambda;
  at v=0, z_A=0 for every lambda.

(p,n,w,m)=(11,5,1,2):
  146410 full-rank lambda;
  at v=0, all 11^3=1331 original-coordinate twists occur;
  110 lambda give z_A=0 and 1100 give a nonzero first-axis twist.
```

The first row is balanced: `2m/n-1=0`, so the original linear term vanishes at
zero syndrome.  The second row is not balanced and exhibits the full twist
space.  These facts concern `A_lambda` coordinates only; the proved
complementary-Hankel endpoint statement follows instead from `(P7)`.

## 7. Orthogonal-array route cut

Let `d=n-c`.  The affine interpolation space with the `c` fixed coefficients
has `p^d` elements.  MDS interpolation implies that every prescription on
`t<=d` coordinates has exactly `p^(d-t)` extensions.

Choose `r` prescribed ones and `s` prescribed zeros, with `r+s=t<=d`.
Double counting gives

```text
N(v) binom(m,r) binom(n-m,s)
  <= p^(d-t) binom(n,t) binom(t,r).                (OA1)
```

Equivalently,

```text
N(v) <= p^(d-t) binom(n,t) binom(t,r)
          / (binom(m,r) binom(n-m,s)).             (OA2)
```

Optimization remains exponential at the deployed parameters.  Thus
Vandermonde independence and positive factorial moments do not reach `n^3`.

## 8. Remaining theorem

After `(H6)`, the full-rank transform is no longer undefined.  The missing
estimate is a signed aggregate bound for the square-plus-form divisor counts
after composition with the subgroup moment map.  The zero endpoint case, if
the bridge `(P7)` is proved, asks for an endpoint-polar divisor estimate.
Uniform max-atom control asks for the corresponding estimate in every induced
polar space.

Taking absolute values introduces exponentially many middle divisors.  After
subgroup parametrization one also encounters products of Kloosterman-type
factors; termwise Weil bounds again lose the cancellation required by `(LS)`.

The correct next targets are therefore:

```text
1. estimate the normalized signed Hankel--Salie/polar divisor aggregate;
2. extend the transform or find another payment for lower-rank strata;
3. combine those estimates with the centered rank window.
```

Until those steps are complete, no primitive/secant compiler may consume this
packet as a proof of `N(0)<=n^3` or `max_v N(v)<=n^3`.

## 9. Verification packet

Run:

```bash
python experimental/scripts/verify_b2_twisted_hankel_transform_v1.py --check
python experimental/scripts/verify_b2_twisted_hankel_transform_v1.py --tamper-selftest
python experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --check
python experimental/scripts/verify_b2_full_rank_chg_normalization_bridge_v1.py --tamper-selftest
python experimental/scripts/experiment_b2_twisted_hankel_cancellation_v1.py --artifact-check
python experimental/scripts/experiment_b2_twisted_hankel_cancellation_v1.py --check  # full regeneration, about 1 minute
python experimental/scripts/experiment_b2_twisted_hankel_cancellation_v1.py --tamper-selftest
```

The verifier checks:

```text
- exact deployed parameter identities;
- divisor-gap, Bezout, interpolation, and dyadic-split identities on toys;
- the uniform subset-Fourier identity on a complete small case;
- (H6) exhaustively for p=3,c=2 and on deterministic samples for
  p=5,c=2 and p=3,c=3;
- polar filtering and endpoint descent on deterministic small cases;
- the CHG-linked ordinary-Hankel and original-coordinate twist censuses;
- note status/nonclaim guards and certificate integrity.
```

The central Fourier, twisted-transform, polar-filter, and endpoint equalities
are checked with exact cyclotomic arithmetic.  A sum `sum_j a_j psi(j)` is
stored as its integer coefficient vector and reduced modulo

```text
Phi_p(X)=1+X+...+X^(p-1).
```

For prime `p`, two coefficient vectors of length `p` represent the same
cyclotomic integer exactly when their difference is constant in every
coordinate.  Floating-point complex values are retained only as human-readable
diagnostics; they are not the pass/fail criterion.

Finite regression is not a proof of Elkies's theorem or of the deployed CHG
estimate.  It protects the signs, homogeneous projective-divisor normalization,
coefficient pairing, exact cyclotomic identity, and claim boundary used here.

## 10. Proof-to-code correspondence

| Claim | Proof location | Verifier function / certificate field |
|---|---|---|
| `(Z1)-(Z4)` complementary gaps | Proposition 2.1 | `check_divisor_toy`; `divisor_toys` |
| `(Z5)-(Z8)` Bezout/interpolation | Proposition 2.2 | `check_divisor_toy`; `divisor_toys` |
| `(Z9)-(Z11)` dyadic split | Proposition 2.3 | `check_divisor_toy`; `divisor_toys` |
| `(F1)-(F3)` uniform Fourier identity | Section 3 | `check_uniform_fourier`; `uniform_fourier` |
| `(H1)-(H5)` conventions | Section 4 | `homogeneous_divides`, `omega`, `hankel` |
| `(E1)-(E2)` Elkies specialization | Section 4 | `omega`; note-contract guards |
| `(H6)-(H10)` twisted transform | Theorem 4.1 | `check_twisted_case`; `twisted_hankel_cases` |
| `(P1)-(P4)` polar filtering | Proposition 5.1 | `polar_original`, `polar_filtered`; `polar_endpoint` |
| `(P5)-(P6)` endpoint descent | Proposition 5.2 | `endpoint_descended`; `polar_endpoint` |
| `(P7)` and full CHG normalization | Companion bridge note | `verify_b2_full_rank_chg_normalization_bridge_v1.py` |
| CHG-linked finite diagnostics | Section 6 | `ordinary_hankel_census`, `original_gauss_twist_census` |
| `(OA1)-(OA2)` route cut | Section 7 | `check_oa_route_cut`; `oa_route_cut` |
| status and nonclaims | Status / Sections 5, 8 | `note_contract`; both JSON packets |

The scripts intentionally have no function corresponding to `(P7)`, CHG,
`(LS)`, `(SV*)`, or `N(0)<=n^3`: those are open claims, not verifier outputs.
