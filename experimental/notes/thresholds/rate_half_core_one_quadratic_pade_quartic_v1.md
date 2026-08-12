---
workboard_item: T
row: symbolic rate-half half-distance core-one quadratic floor profile
object: LINE
target_epsilon: 2^-128 context; target-free structural theorem
agreement: a=N-t=3N/4
B_star: floor(q/2^128); no payment claimed
direct_statement: every extremal split-biform fiber has its complete padding factor; the residual projective intersection cycle has degree four; its parameter eliminant is exactly the regular Kronecker correction quartic; ordinary supported rank loss is first-jet transverse; every squarefree double-root correction reduces to a cubic Hankel recurrence whose heavy row is one exact barycentric remainder test; the heavy row is nonzero, has exact correction orders, and has overlap degree exactly d_A; the squarefree shared third jet vanishes by symmetric corank-one control; an unshared nonreduced correction is exactly a two-Hasse-jet gate, normalization forces every nonzero jet onto an exact double locator-root collision, and the Pade contact algebra reduces that collision to two coefficients selecting Smith type [4], [1,3], or [2,2]; automatic separation of the compressed recurrence from the original source is explicitly refuted; every irreducible paired-biform factor splits in both proved directions, the biform has constant content, and its factor degrees obey one of three exact profiles with no domain-degree slack; bare Layer-A row surplus plus saturation does not force rank
architecture: DIRECT
partition_digest: N/A
atom_or_cell: symmetric-Hankel core-one scalar-quadratic u=4 extremal boundary
quantifier: every odd-characteristic field and profile satisfying the exact pair-floor interface and retained core-one quadratic packet
projection_and_unit: projective parameter fibers and local intersection multiplicity
claimed_bound: after one copy of every actual-support and padded common point, exactly four projective intersection units remain; their parameter divisor is S_B^2 in the double-root arm and S_1S_2 in the two-simple arm; outside at most four correction slopes the supported derivative pairing is perfect; on every squarefree double-root locus the heavy-row gate is H|R_lambda, equivalently B_H lambda=0, every passing remainder is nonzero and correction-coprime, and j=d_A in {0,1}; at a squarefree shared root the third jet vanishes and the local Smith type is [3]; an unshared nonreduced root either closes with Smith [4] or is an exact double locator-root collision of regular corank at most two, where a(0) and [z]a for P_F=b+ay modulo the local quadratic select [4], [1,3], or [2,2]; every paired-biform factor Q_j obeys n_j=ceil((3p-3+d_A)m_j/(3e)), with exactly one of three odd/huge-even profiles and constant content; a separate exact m=2 fixture has Layer-A rank 20 rather than 24 despite 26 saturated incidence rows
status: PROVED
impact: ROUTE_CUT
falsifier: a missing positive-excess padding factor, residual intersection degree other than four, wrong Pade leading-coefficient exponent, a residual parameter root outside the correction quartic, a nonzero jet on the separated regular-corank-one nonreduced locus, a collision profile outside [4]/[1,3]/[2,2], nonconstant biform content, factor-degree slack, or a feasible factor profile outside the printed trichotomy
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
`AllenGrahamHart/rs-mca-prize-dag@57c64d1ce26d50f604d9c26bcafe2ab9911a60ac`.
The verifier records fifty-eight statement/proof SHA-256 values and can check
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

## 8. Supported first jets and coefficient-plane rank

Let `gamma` be a supported slope with residual rank loss `c_gamma>0`.
Away from `S_B` in the double-root arm or `S_1S_2` in the two-simple arm,
the exact regular factor gives

```text
ord_gamma(D_1)=c_gamma.                            (25)
```

The specialized symmetric Hankel kernel is

```text
ker M_gamma=Q_min F[X]_(<=c_gamma).                (26)
```

All positive local Smith exponents are therefore one. The derivative
moment form

```text
B_gamma(A,B)=dot Phi(Q_min^2AB)                    (27)
```

has rank `c_gamma` and radical exactly `span{R_gamma}`. There are at most
two exceptional projective slopes in the double-root arm and at most four
in the two-simple arm.

This interacts with the common coefficient plane
`W_q=span(q_0,...,q_e)`. Since `W_q` is totally isotropic for every endpoint
combination, its image in the nondegenerate quotient of `(27)` is totally
isotropic. Hence

```text
dim((W_q intersect ker M_gamma)/span(Q_gamma))
 <=floor(c_gamma/2).                               (28)
```

If `E_gamma=(Q_i(x))` is evaluated on the exact contracted actual support,

```text
e-floor(c_gamma/2)<=rank E_gamma<=e.               (29)
```

In particular an ordinary rank-one loss slope has exact rank `e`; the
primitive locator is the only coefficient-plane vector vanishing on its
whole actual support. Rank two has rank `e-1` or `e`.

## 9. Separated double-root correction: cubic residual

Assume in the double-root arm that `S_B` is squarefree and
`gcd(g_*,S_B)=1`. Divide the fixed heavy row:

```text
U(t,X)=[Q(t,X)-Q(t,x_*)]/(X-x_*).                  (30)
```

The first quotient moment is `P_F(t,x_*)`. Supported kernel divisibility,
the contact divisor `R_*+2B`, and the higher vertical contact `R_*+3B`
give

```text
P_F(t,x_*)=D_1(t)C_0(t),
M(t)U(t)=D_1(t)C(t),       deg_t C<=3,             (31)

C_(i+1)=x_*C_i-kappa S_Bh_i.                      (32)
```

Thus each of the two separated correction roots has one positive regular
Smith invariant of exponent two: type `[2]`, not `[1,1]`. This is a true
Hankel/Forney reduction beyond the abstract marked-order fence. It does not
exclude the resulting cubic recurrence. Nonreduced `S_B` and roots shared
with `g_*` remain outside `(30)--(32)`.

## 10. Heavy-row center overlap

Still on the separated double-root locus, put

```text
J=gcd(Lambda,g_*S_B^2),       j=deg J<=3,
Lambda=J Lambda_0,            g_*S_B^2=JH.         (33)
```

The cubic bracket in `(31),(32)` and coprimality of `Lambda_0,H` give a
form `T_j` of degree at most `j` such that

```text
a_QS_BB(t,x_*)-a_D L_U0(x_*)C_0(t)=Lambda_0T_j,
G(t,x_*)=H(t)T_j(t).                               (34)
```

Thus all but at most three roots of the fixed heavy row are prescribed.
If `J=1`, then `T_j` is a scalar, possibly zero. Writing

```text
G(t,X)=sum_(r=0)^(e-2)g_r(X)t^r,       deg_X g_r<=n,
```

shows that evaluation at `x_*` augments the existing coefficient-RS gate by
only the `j+1<=4` scalar coefficients of `T_j`. This is an exact adapter to
the split-biform boundary, not a proof that the augmented matrix has full
rank.

## 11. Layer-A saturation-count route fence

A separate exact family rules out a tempting generic-rank shortcut. Over an
odd field containing `mu_32`, let `W` be any thirteen points of `mu_16`, let
the nine slopes be `mu_8 union {eta}` with `eta notin mu_8`, and set

```text
Q(Z,X)=Z^2-X^4.                                    (35)
```

For every `x in W`, the two incident slopes are `+x^2,-x^2`. Hence the
Layer-A evaluation matrix at `m=2,rho=7,T=9,a=13` has 26 saturated
incidence rows and 24 columns. Nevertheless,

```text
ker E={A(X)(Z^2-X^4): deg A<=3},
rank E=20,       nullity E=4.                      (36)
```

Indeed, writing a kernel biform as
`a_2(X)Z^2+a_1(X)Z+a_0(X)`, evaluation at both signs on thirteen points
forces `a_1=0` and `a_0=-X^4a_2`, then `deg a_2<=3`. Thus positive row
surplus `3m^2-5m=2` plus pointwise saturation does not force full rank.
This does not realize the canonical pair-union supports, complete all nine
global blocks, or impose the endpoint Hankel/source constraints. Those extra
hypotheses remain available and must be used essentially by any positive
Layer-A theorem.

## 12. The heavy row is one barycentric remainder

Let `X` be the classified row set, with `x_* notin X`, and let `P_x(t)` be
the monic row-root polynomial.  If the connected scalar weld has its unique
projective full-support kernel vector `lambda`, define

```text
L_X(Y)=product_(x in X)(Y-x),
b_x=L_X(x_*)/((x_*-x)L_X'(x)),
R_lambda(t)=sum_(x in X)b_x lambda_x P_x(t).       (37)
```

For the center-overlap factorization `(33)`, the augmented heavy-row gate is
exactly

```text
H divides R_lambda.                                (38)
```

Equivalently, in a chart whose infinity is not a root of `H`, form the
`(m-j) x |X|` matrix `B_H` whose `x`-column is the coefficient vector of
`b_x rem_H(P_x)`.  Then the staged exclusion ledger is

```text
rank W=|X|                         => excluded;
rank W=|X|-1 and Krow lambda!=0    => excluded;
Krow lambda=0 and B_H lambda!=0   => excluded;
B_H lambda=0                      => R_lambda=H T_j,
                                      deg T_j<=j.   (39)
```

Thus the formerly qualitative augmented coefficient-MDS condition is one
explicit univariate remainder.  No generic-rank assumption is used.

## 13. Every separated heavy row is nonzero

Suppose that `S_B` is squarefree and `gcd(g_*,S_B)=1`. There is no
restriction on correction-center overlap. Then

```text
G(t,x_*)!=0,
R_lambda(t)=G(t,x_*)!=0                             (40)
```

for every passing connected-weld candidate. Indeed, a zero row would make
`X-x_*` a component of `G`. At either root of `S_B`, the row polynomial
`Q(t,x_*)` has order three. If that root is not off-line supported, including
when it is a center, `(21)` gives exact resultant order two, a contradiction.
If it is off-line supported, the exact
all-excess fiber factorization puts `x_*` in its actual-support or padding
factor.  The first case contradicts first-jet transversality; the second
forces `g_*` to vanish there, contrary to `gcd(g_*,S_B)=1`.  Hence the
separated heavy row is a genuine projective row for every overlap degree
`j=0,1,2,3`.

## 14. Exact correction jets and the overlap cap

At a root `tau` of `S_B`, put `c_tau=ord_tau Lambda`, which is zero or one.
On the normalized curve, `X-x_*` has order three and the Forney section has
order two. The Pade syzygy subtracts one exactly when `tau` is a center,
while fixed-row substitution changes the value only from order three onward.
Consequently

```text
ord_tau G(t,x_*)=2-c_tau=ord_tau H,
T_j(tau)!=0,
gcd(T_j,S_B)=1.                                    (41)
```

The full three-center source identity sharpens the overlap count. Every
assigned-center error support is contained in
`supp(b_0,b_1)=U=S_alpha union S_beta`, while `x_*` lies outside `U`. Thus a
correction root at any center would make `x_*` padded there, putting that
center in both `g_*` and `S_B`, contrary to separatedness. The exact center
deficit ledger allows at most one center root of `g_*`. Hence

```text
gcd(S_B,Lambda)=1,
deg gcd(g_*,Lambda)<=1,
j=deg gcd(Lambda,g_*S_B^2)<=1.                     (42)
```

Thus the exact nonzero remainder has at most two scalar coefficients, and
none of its free factors can be a correction root.

## 15. A squarefree shared root is one third-jet gate

Allow a simple common root `tau` of `g_*` and `S_B`, and let `z` be its base
uniformizer. Then `Q(t,x_*)` has order four and `D_1` has order three. The
correction branch always gives

```text
z^2 | F_0,       kappa_tau=(F_0/z^2) mod z.         (43)
```

The supported and correction contacts may be distinct normalized branches,
so their orders are not added without this extra jet. The exact recurrence
instead gives

```text
(F_i/z^2) mod z=x_*^i kappa_tau,
D_1|F_i for every i       iff kappa_tau=0.          (44)
```

The nonvanishing branch is in fact impossible. At a shared supported slope,
the specialized regular symmetric Hankel block has corank one and determinant
order three. A symmetric Schur-complement lemma forces `u^TMu` to order at
least three, while its order-two coefficient is
`kappa_tau U_tau(x_*)`. The padded root is simple, so `U_tau(x_*)!=0` and

```text
kappa_tau=0,
D_1|F_i for every i,
Smith_tau(D_1)=[3].                                 (45)
```

Consequently the cubic quotient, center-overlap factorization, exact
correction orders, and barycentric remainder gate extend to every
squarefree `S_B`, whether or not it shares roots with `g_*`. A correction
center is necessarily already the unique possible padded-heavy center, so
the same cap `j<=1` holds. Every squarefree double-root survivor is therefore
one nonzero constant/linear remainder case.

## 16. Nonreduced correction is exactly two Hasse jets

Suppose instead that `S_B=c_S ell_tau^2` and `g_*(tau)!=0`. With
`z=ell_tau`, the heavy row and regular determinant have exact orders

```text
ord_tau Q(t,x_*)=6,       ord_tau D_1=4.           (46)
```

Correction contact forces `z^2|F_0`, but no addition of orders from
possibly distinct normalized branches is made. Define

```text
kappa_2=[z^2]F_0,       kappa_3=[z^3]F_0.          (47)
```

The exact moment recurrence starts its error in order six, so

```text
[z^s]F_i=x_*^i kappa_s       for s=2,3,            (48)
D_1|F_i for every i
       iff kappa_2=kappa_3=0.                       (49)
```

On the vanishing branch the cubic quotient extends and the regular Smith
type is `[4]`. This is a two-scalar decision gate, not a proof that either
jet vanishes. A nonreduced root also shared with `g_*` has a different
determinant order and is not included.

## 17. Exact deficit overlap and a macroscopic split factor

The full source partition identifies the center roots of `g_*` exactly with
the deficit indicators `r_gamma`. A correction center is already one of
those padded-heavy centers. Therefore, without a supported/correction
disjointness hypothesis,

```text
J=gcd(Lambda,g_*S_B^2)=gcd(Lambda,g_*),
j=deg J=d_A.                                        (50)
```

Thus `d_A=0` gives a nonzero scalar remainder quotient, while `d_A=1`
gives a nonzero quotient of degree at most one. The overlap degree is not an
independent branch parameter.

There is also a global factor restriction unavailable from bare Layer-A
counting. Put

```text
M=e-2,       N=p-3,       R=3p-3+d_A,       T=3e,
G=c(X) product_j Q_j,       (m_j,n_j)=bideg Q_j.    (51)
```

Every classified row has exactly `M` distinct roots among the `T` supported
slopes. Counting each factor's grid zeros in both directions closes with
equality and gives

```text
T n_j>=R m_j.                                      (52)
```

Equality in the total row ledger forces every `Q_j(-,x)` to split
completely and disjointly on every classified row. Exact degree on each of
the at least `e+6+d_A` clean parameter fibers likewise makes every
`Q_j(delta,-)` split over `U_0` there.

Finally,

```text
R/T=3/2-(9-2d_A)/(6e),       N=(3M-1)/2.           (53)
```

If all factor degrees were below `3e/(9-2d_A)`, integer rounding in `(52)`
would give `sum n_j>=N+1`. Hence one irreducible factor satisfies

```text
d_A=0: m_j>=ceil(e/3)=61083979321,
d_A=1: m_j>=ceil(3e/7)=78536544842                 (54)
```

on the official row. The Layer-A low-degree-factor mechanism is therefore
impossible here. The remaining object is a macroscopic two-directionally
split factor, not an arbitrary high-degree component.

## 18. The separated regular-corank-one profile has no free jet

Retain the unshared nonreduced correction of Section 16 and let `N(z)` be
the regular symmetric block after removing the permanent primitive kernel.
If

```text
corank N(0)=1,       P_tau(x_*)!=0,                (55)
```

then the full specialized Hankel kernel has dimension two and its compressed
minimal recurrence `P_tau` has degree `d-1`. The explicit separation gives

```text
Q(tau,X)=c(X-x_*)P_tau(X),
U_tau(x_*)=cP_tau(x_*)!=0.                         (56)
```

For a symmetric corank-one block with determinant order four, the Schur
complement has order four. Therefore

```text
N(z)v(z) in z^2 F[[z]]^d
       implies v(z)^T N(z)v(z) in z^4 F[[z]].      (57)
```

The order-two and order-three coefficients of the latter self-pairing are
respectively

```text
kappa_2 U_tau(x_*),       kappa_3 U_tau(x_*).      (58)
```

Equations `(56)--(58)` force

```text
kappa_2=kappa_3=0.                                 (59)
```

Thus the cubic quotient extends and the regular Smith type is `[4]` on the
separated corank-one locus. A corank-one nonzero-jet survivor must instead
satisfy `P_tau(x_*)=0`. This separation does not follow from
`x_* notin U_0`: Section 21 records an exact truncated-moment counterexample.

## 19. Constant content and the exact factor-degree trichotomy

The content `c(X)` in `(51)` is constant. Indeed, a content root belongs to
`U_0` because any clean parameter fiber is squarefree and split there. But
every `y in U_0` has the nonzero dual-MDS source row

```text
G(t,y)=L_U0'(y) omega_y(t)Q(t,y)/Lambda_A(t),       (60)
```

contradicting a zero content row. Hence

```text
sum_j m_j=M,       sum_j n_j=N.                    (61)
```

Put `q=9-2d_A`. For each factor define

```text
n_j^min=ceil(Rm_j/T),       a_j=n_j-n_j^min>=0.
```

Classify an odd `m_j` as small when `qm_j<3e` and large otherwise;
classify an even `m_j` as ordinary when `qm_j<6e` and huge otherwise.
The exact rounding values are

```text
2n_j^min-3m_j = 1,-1,0,-2                         (62)
```

in those four classes. If `S,L,H` count the small-odd, large-odd, and
huge-even factors and `E=sum_j a_j`, `(53)` and `(61)` give

```text
S-L-2H+2E=-1.                                     (63)
```

Degree alone gives `L<=2`, `H<=1`, and `H=1 => L=0`. Equation `(63)`
then forces `E=0` and exactly one of

```text
(S,L,H)=(0,1,0),       (1,2,0),       (1,0,1).    (64)
```

All remaining factors are ordinary even, and every factor lies exactly on
the incidence lower envelope

```text
n_j=ceil(Rm_j/T).                                  (65)
```

On the official row, the least parity-compatible large-odd degrees are
`61083979321` for `d_A=0` and `78536544843` for `d_A=1`; the least huge-even
degrees are `122167958642` and `157073089684`. This trichotomy exhausts the
degree ledger but does not exclude any of its three profiles.

## 20. Normalization forces every nonzero jet onto collision

Retain the unshared nonreduced correction. On the normalization, write

```text
B=sum_b m_b b,       e_b=ord_b(t-tau),
s=ord_tau F_0.                                      (66)
```

The exact vertical and contact divisors are `R_*+3B` and `R_*+2B`.
Because `g_*(tau)!=0`, no point of `R_*` lies above `tau`. Substituting the
fixed value `x_*` into `P_F` changes its branch value only by a multiple of
`X-x_*`, of order `3m_b`, while `P_F` itself has exact order `2m_b`.
Therefore

```text
e_b s=2m_b.                                        (67)
```

Since `deg B=2` and `s>=2`, exactly three patterns remain:

```text
B=2b, e_b=1:                  s=4, Smith [4];
B=2b, e_b=2:                  s=2;
B=b_1+b_2, e_(b_1)=e_(b_2)=1: s=2.                (68)
```

In both `s=2` cases, `kappa_2!=0` and the specialized locator has `x_*`
as a root of exact multiplicity two. Thus a first-nonzero third jet and
every noncollision nonzero-jet profile are impossible.

## 21. The exact collision is two Pade coefficients

The determinant identity also has a local-module refinement. If

```text
K_Q(X,Z)=[Q(X)-Q(Z)]/(X-Z),
H=(Phi(X^(i+j)))_(0<=i,j<d),                       (69)
```

and `T_Q` is the coefficient matrix of `K_Q`, then

```text
Bez(Q,P_F)=T_Q H T_Q^T,
det T_Q=+-lc_X(Q)^d.                               (70)
```

Hence, on a finite degree-preserving chart, the regular Hankel block has
the same complete Smith invariants as the contact algebra

```text
F[[z]][X]/(Q,P_F).                                 (71)
```

In odd residue characteristic, at the exact double collision put
`y=X-x_*`, isolate the quadratic Hensel
factor, and reduce `P_F` modulo it:

```text
q=y^2+c_1y+c_0,       P_F=b+ay mod q,
ord_z(b,c_0,c_1,a)=(2,6,>=3,>=0).                 (72)
```

More precisely, if `P_F=b+ay+qR`, then

```text
F_0=P_F(t,x_*)=b+c_0R(z,0).
```

Thus `F_0` is not literally the remainder coefficient `b`; their
difference starts in order six, so `ord_z F_0=2` still gives
`ord_z b=2`.

Multiplication by `b+ay` has the two-by-two presentation

```text
[ b       -a c_0 ]
[ a        b-a c_1].                               (73)
```

Its determinant has exact order four. The regular corank is at most two,
and its complete positive Smith profile is

```text
a(0)!=0:                  corank one, [4],
a(0)=0, [z]a!=0:          corank two, [1,3],
a(0)=0, [z]a=0:           corank two, [2,2].       (74)
```

Thus the abstract corank-three and corank-four collision profiles do not
occur. The nonreduced Lane-T escape is two explicit Pade coefficients, not
an unrestricted higher-corank singularity. This local collision
classification makes no characteristic-two claim.

The unit-`a` profile cannot be discarded by original-source separation.
Over `F_101` at `(e,p,d,n_0)=(5,7,13,19)`, explicit all-nonzero weights on
`U_0={1,...,19}` have the same first 27 moments as all-nonzero weights on
disjoint compressed supports of sizes 12 and 11 containing `x_*=30`.
The corresponding Hankel matrices have regular coranks one and two, and
their degree-13 kernel polynomials have `x_*` as an exact double root. This
refutes the truncated Vandermonde inference only; it is not a global
split-biform counterexample.

## 22. The collision coefficients are global split-biform jets

The two coefficients in `(74)` have an exact global interpretation. Define

```text
U(t,X)=[Q(t,X)-Q(t,x_*)]/(X-x_*),
W(t,X)=[U(t,X)-U(t,x_*)]/(X-x_*).                 (75)
```

At an exact double collision,

```text
W_tau=Q(tau,X)/(X-x_*)^2,       W_tau(x_*)!=0.    (76)
```

Put

```text
A(t)=Phi_t(W(t,X))=P_(F,X)(t,x_*),
E_i(t)=Phi_t(X^iW(t,X)),
lambda_0=a(0),       lambda_1=[z]a.               (77)
```

From `P_F=b+ay+qR`, `ord c_1>=3`, and `ord c_0=6`,

```text
A=a mod z^3.                                      (78)
```

The identity

```text
Phi_t(X^iU)=Q_X(t,x_*)h_i+E_(i+1)-x_*E_i          (79)
```

together with the forced order two on the left and
`ord_z Q_X(t,x_*)>=3` propagates the first two coefficients:

```text
[z^s]E_i=x_*^i lambda_s       (s=0,1).            (80)
```

If `lambda_0=0`, then `W_tau` lies in the specialized Hankel kernel and
the differentiated self-pairing is

```text
[z]Phi_t(W(t,X)^2)=lambda_1W_tau(x_*).             (81)
```

Differentiate the exact Pade syzygy `(11)` in `X` and evaluate at `x_*`:

```text
Q_X B+Q B_X-Lambda G_X=L'F_0+LA.                 (82)
```

The heavy point lies outside `U_0`, and an unshared correction cannot be
one of the three assigned centers: at such a center it would be a padded
locator root and hence a root of `g_*`. Therefore
`Lambda(tau)L(x_*)!=0`. Taking the constant and first parameter
coefficients in `(82)` gives

```text
lambda_0=-Lambda(tau)G_X(tau,x_*)/L(x_*),

lambda_0=0
  => lambda_1=-Lambda(tau)[z]G_X(t,x_*)/L(x_*).   (83)
```

Consequently the complete local contact-algebra router is the following
global split-biform jet dictionary:

```text
G_X(tau,x_*)!=0:                         [4];
G_X(tau,x_*)=0, [z]G_X(t,x_*)!=0:        [1,3];
G_X(tau,x_*)=[z]G_X(t,x_*)=0:            [2,2].   (84)
```

This identifies the exact remaining targets. It does not prove that any
line of `(84)` is empty.

## 23. The split jets are explicit scalar-weld functionals

The correction parameter in Section 22 is outside the supported slope set.
Indeed, it is not an assigned center by `Lambda(tau)!=0`. If it were an
off-line supported slope, the exact vertical-fiber gcd

```text
gcd_X(Q(tau,X),G(tau,X))=A_tau(X)R_tau(X)          (85)
```

would make the common root `x_* notin U_0` padded-heavy, contrary to
`g_*(tau)!=0`. Thus every classified row-root polynomial below is nonzero
at `tau`.

Write the classified rows as

```text
G(t,x)=lambda_xP_x(t)       (x in X),              (86)
```

where `lambda` is the unique projective full-support vector allowed by the
connected scalar weld. Put

```text
L_X(Y)=product_(x in X)(Y-x),
b_x=L_X(x_*)/[(x_*-x)L_X'(x)],
d_x=b_x[L_X'(x_*)/L_X(x_*)-1/(x_*-x)].            (87)
```

Coefficientwise Lagrange interpolation and its `X`-derivative give

```text
R(t):=G(t,x_*)
     =sum_x b_x lambda_xP_x(t),

J(t):=G_X(t,x_*)
     =sum_x d_x lambda_xP_x(t).                   (88)
```

For Hasse coefficients at `tau`, define

```text
R_s=sum_x b_x lambda_xP_x^[s](tau),
J_s=sum_x d_x lambda_xP_x^[s](tau).               (89)
```

The Pade syzygy has terms of orders six and two at the heavy point, so
`ord_tau R=2`. The entire retained collision is therefore the finite gate

```text
R_0=R_1=0,       R_2!=0,

J_0!=0:                    [4];
J_0=0, J_1!=0:             [1,3];
J_0=J_1=0:                 [2,2].                 (90)
```

All summands in the zeroth equations are individually nonzero before the
forced cancellations. Equation `(90)` is an explicit test on the realized
row-root sets and weld vector; it is not yet a nonvanishing theorem.

## Nonclaims

This packet does not exclude either quadratic root arm, prove a live
`LineRay` census, pay a v4 atom, move an adjacent endpoint, or change a
leaderboard score. It identifies the remaining degree-four geometry,
rules out determinant multiplicity as a standalone closure argument, and
reduces only the separated double-root correction to the printed cubic
recurrence and exact heavy-row remainder. The nonvanishing theorem covers
all center-overlap degrees, but does not exclude a nonzero passing remainder.
The Layer-A fixture refutes only a
generic count-and-saturation implication, not the structured endpoint
configuration. Squarefree shared corrections are absorbed into the unified
constant/linear remainder gate. An unshared nonreduced correction remains
open only in the three profiles `[4]`, `[1,3]`, and `[2,2]`, selected by
the two global split-biform jets in `(83)--(84)`; none is excluded here. A
shared nonreduced correction and the two-simple correction remain open. The exact factor
trichotomy is a restriction, not an exclusion or a `LineRay` payment.
