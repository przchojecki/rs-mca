---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: one determinant-coordinate gcd simultaneously recovers common defect roots and common background-agreement roots; all other background roots are affine coordinate equations; every fixed joint owner has an exact packing payment and a dual-domain bounded-tail split-pencil coordinate; the complete unguarded owner chart has the exact MDS support census; anchor elimination gives an owner-free weighted Cauchy divisor formulation retaining splitness and guards, whose coefficient space is a full-row-rank rational Pade-Hankel kernel; fixing the required background zeros gives exactly ell-1 Hankel rows and monic codimension ell-1; every primitive split locator is exactly a weight-d vector in one GRS syndrome coset; summing fixed-background singleton or Johnson bounds pays bounded background polarity; Haboeck plus the proved deep-point conversion bounds the adjacent-dimension shifted-Johnson shell with the exact background factor; exact constant-weight shortening bounds every fixed GRS shell, and canonical first-layout domination compiles both selected cells and complete official source prefixes
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled arbitrary-t monic pair slice with one exact anchor
quantifier: every field and every source partition satisfying the companion primitive remainder theorem
projection_and_unit: determinant coordinates with their split locators, reconstructed numerators, and source-background roots
claimed_bound: exact joint-owner identity, exact owner-containment dimension, binomial-ratio fixed-owner packing, a two-generator coefficient parameterization of every fixed owner chamber, the exact ambient owner-stratum enumerator, an exact owner-free weighted Cauchy divisor formulation, its full-rank rational Pade-Hankel kernel, exact fixed-background codimension/incidence normalization, an exact GRS syndrome-shell bijection, a per-chart singleton criterion, a binomial-times-Johnson bounded-polarity payment, an exact shifted-Johnson list cap, an exact constant-weight support-shortening cap, and a canonical first-layout/touched-set compiler paying two complete official source prefixes; no complete middle-polarity guarded aggregate, deployed-row endpoint, or Prize close
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a common anchor defect or background root missed by the gcd, an extraneous gcd root, a non-anchor background root not represented by the printed affine equation, a fixed-owner family exceeding the binomial ratio, a candidate violating the owner-cancelled determinant or two-generator coordinate, an ambient exact-owner stratum differing from the printed MDS count, a CRT pair violating the printed moment, primitive, or background Cauchy identities, a Cauchy moment block violating the printed Hankel rank, generating function, or recurrence, a nonempty fixed-background cell violating the ell-1 codimension or incidence identity, a shifted shell exceeding the printed deep-point ceiling, a constant-weight shell exceeding the shortening cap, or a canonical aggregate exceeding its exact touched/background/source charge
replay: python3 experimental/scripts/verify_list_fpc5_shifted_johnson_v1.py for the adjacent-dimension arithmetic; python3 experimental/scripts/verify_list_fpc5_constant_weight_shortening_v1.py for the support-shortening prefixes; analytic proofs for the structural theorems
---

# General t-petal joint anchor owner

## 1. Setup

Use the primitive remainder chart of
`list_tpetal_anchor_pade_chart_v1.md`. Let `(F,W)` be the squarefree split
anchor, let `Bkg` be the source background, and put

```text
R_0={y in Bkg: W(y)=0},       P_0=F L_(R_0).          (1.1)
```

For a coordinate `H`, write `(G_H,B_H)` for its reconstructed pair and

```text
R_H={y in Bkg: B_H(y)=0}.
```

The core, background, and petals are disjoint.

## 2. Joint owner theorem

### Theorem 2.1

One coordinate gcd recovers both anchor-relative owners:

```text
gcd(H,L_(R_0))=gcd(B_H,L_(R_0)),                     (2.1)
gcd(H,P_0)=gcd(G_H,F) gcd(B_H,L_(R_0)).              (2.2)
```

Equivalently, the roots of `(2.2)` are exactly

```text
(Z(G_H) intersect Z(F)) disjoint_union (R_H intersect R_0). (2.3)
```

Every distinct candidate consequently obeys

```text
|Z(G_H) intersect Z(F)|+|R_H intersect R_0|<=e-1.    (2.4)
```

#### Proof

At `y in R_0`, the determinant identity becomes

```text
F(y)B_H(y)=Lambda(y)H(y).
```

Both displayed factors are nonzero on the source background, so
`B_H(y)=0` exactly when `H(y)=0`. Squarefreeness proves `(2.1)`. The
companion anchor-coordinate theorem gives

```text
gcd(H,F)=gcd(G_H,F).
```

Since `F` and `L_(R_0)` are coprime, multiplying the identities proves
`(2.2)--(2.3)`. Finally `H!=0` and `deg H<=e-1` prove `(2.4)`. QED.

## 3. Exact owner strata

Let `Q|P_0` be monic of degree `q<=e-1`. The coordinates whose joint owner
contains `Q` are exactly

```text
H=QK,       deg K<=e-1-q.                             (3.1)
```

This is a linear coordinate space of dimension `e-q`. The exact-owner
stratum is obtained by imposing

```text
gcd(K,P_0/Q)=1.                                       (3.2)
```

Thus defect and background owners are not independent pencils or ledgers;
they are one divisor stratum in the same low-degree coordinate body.

## 4. Remaining background equations

With

```text
Remainder_H=rem_F(-Lambda H W^(-1)),
T_H=(Remainder_H W+Lambda H)/F,                       (4.1)
```

the exact inverse reads `B_H=W+T_H`, and `T_H` is linear in `H`. Hence for
every `y in Bkg\R_0`,

```text
B_H(y)=0 iff T_H(y)=-W(y),                            (4.2)
```

one affine linear equation on the coordinate body.

## 5. Fixed joint-owner packing

For one surviving full-petal cell, write

```text
N=|C|,       b=|Bkg|,       r=2d-t ell=e-1,
u=d-(t-1)ell,       v=max(0,u).                       (5.1)
```

Fix an exact owner `Q=gcd(H,P_0)` of degree `q`. Let `F_Q` be the distinct
exact candidates with this owner. Then

```text
|F_Q| <= floor(
  binom(N+b-q,r-q+1) / binom(d+v-q,r-q+1)
).                                                    (5.2)
```

Indeed, each candidate's combined defect/background marked set has size at
least `d+v`. Two such marked sets meet in at most `r` points by the joint
determinant degree budget. After removing the common `q` owner roots, the
sets have size at least `d+v-q` in an `N+b-q` point universe and meet in at
most `r-q` points. No `(r-q+1)`-subset can occur twice, so double counting
proves `(5.2)`.

The denominator is always defined. If `u>=0`, then `d+v-r=ell`. If `u<0`,
then `d+v-r=t ell-d>=ell-b>=1` by the list threshold. In particular, for
`q=r-c`,

```text
|F_Q|<=n^(c+1).                                       (5.3)
```

Every bounded co-deficiency chamber is therefore polynomial per fixed
joint owner.

## 6. Dual-domain bounded-tail split-pencil reduction

Fix one distinct exact candidate and abbreviate `(G_H,B_H)` to `(G,B)`. Put

```text
D=gcd(F,G),       E=gcd(B,L_(R_0)),
Q=gcd(H,P_0)=D E,       q=deg Q,       c=r-q.         (6.1)
```

The factors `D,E` have roots in the disjoint core and background. Since
`D|F,G` and `E|W,B`, define

```text
A=F/D,       C=G/D,       U=W/E,       V=B/E,
K=H/(D E).                                             (6.2)
```

### Theorem 6.1

The reduced rows satisfy

```text
A V-C U=Lambda K,       K!=0,       deg K<=c,         (6.3)
gcd(A,C)=gcd(A,U)=gcd(C,V)=1.                         (6.4)
```

The locator entries `A,C` are monic squarefree and split on the core. For
every touched petal,

```text
E U == c_i D A (mod L_i),
E V == c_i D C (mod L_i),                             (6.5)
```

or, equivalently, after inverting the core/background factors modulo the
petal locator,

```text
U == c_i D E^(-1) A (mod L_i),
V == c_i D E^(-1) C (mod L_i).                        (6.6)
```

#### Proof

The joint-owner identity gives `Q=DE` and hence `H=DEK`. Substitution in
`F B-G W=Lambda H` gives

```text
D E(A V-C U)=D E Lambda K.
```

Cancellation proves `(6.3)`, including `deg K<=r-q`; `K` is nonzero because
the candidate differs from the anchor. Exactness of `D=gcd(F,G)` gives
`gcd(A,C)=1`. Original primitivity gives the other two gcd identities.
Substitution in the anchor and candidate petal congruences proves
`(6.5)`. Core, background, and petals are disjoint, so `D,E` are units
modulo every `L_i`, proving `(6.6)`. QED.

### Theorem 6.2

Fix one exact owner chamber `Q`, and within it fix one reference member
`(C_0,V_0,K_0)`. Every other member has a unique polynomial `T` satisfying

```text
K_0 C-K C_0=A T,       K_0 V-K V_0=U T,
deg K<=c,               deg T<=c.                    (6.7)
```

Thus the chamber injects into bounded-degree coefficient pairs `(K,T)` in
one two-generator rational pencil. At top ownership `q=r`, all coefficients
in `(6.7)` are scalars and monicity gives

```text
(C,V)=lambda(C_0,V_0)+(1-lambda)(A,U),                (6.8)
```

where `lambda=K/K_0` is nonzero and differs from `1` for a member other than
the reference. The top chamber is therefore an ordinary affine pencil of
primitive core-split locators, coupled through `(6.3)` to a nonzero scalar
determinantal representation of the touched-petal locator.

#### Proof

For fixed `Q`, the factors `D,E` and hence the anchor row `(A,U)` are fixed.
Multiply `(6.3)` by `K_0`, subtract `K` times the reference equation, and
obtain

```text
A(K_0 V-K V_0)=U(K_0 C-K C_0).                       (6.9)
```

Since `gcd(A,U)=1`, a unique `T` gives `(6.7)`. If
`a=deg A=deg C=deg C_0`, then the numerator in the first equation has degree
at most `a+c`, proving `deg T<=c`. When `c=0`, comparison of leading
coefficients gives `T/K_0=1-K/K_0`, which is `(6.8)`. QED.

### Relation to the active split-pencil problem

The algebra in `(6.3)` and `(6.7)` is the same primitive two-generator
algebra isolated by `prop:capfr1-detrep` and targeted by
`prob:capfr1-split-pencil`. The domains are not the same: here the natural
determinant parent is the touched-petal locator `Lambda`, while the varying
locators `C` split on the disjoint core. In the active upstream problem the
varying locator divides the same evaluation-domain locator represented by
the determinant. Consequently Theorems 6.1--6.2 are a dual-domain analogue,
not a proof or direct specialization of the base-field-normalized interior
census.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`8d0d19b8860143ad1a33aeee467a18f07e37baf4`, node
`l1_fpc5_tpetal_joint_owner_split_pencil`.

## 7. Exact ambient MDS owner census

Put

```text
p=deg P_0=d+|R_0|,       Q_f=|mathbb F|,
r=2d-deg Lambda=e-1.                                  (7.1)
```

The saturated-cell inequality `deg Lambda>d` gives `r<d<=p`.

### Theorem 7.1

On the `p` roots of `P_0`, the combined anchor defect/background failure
vector is a nonzero diagonal rescaling of the evaluation vector of `H`.
Therefore the complete monic chart has exactly the support strata of the
length-`p`, dimension-`r+1` generalized Reed--Solomon code.

For any fixed monic divisor `Q|P_0` of degree `q<=r`, put

```text
s=r-q,       m=p-q.
```

The number of nonzero unguarded chart points with exact owner `Q` is

```text
N_Q(m,s)
 =sum_(j=0)^s (-1)^j binom(m,j)(Q_f^(s+1-j)-1).       (7.2)
```

There are `binom(p,q)` possible degree-`q` owners. At top ownership `q=r`,
every degree-`r` divisor occurs with exactly `Q_f-1` chart points, so the
complete top-owner ambient chart has

```text
binom(p,r)(Q_f-1)                                      (7.3)
```

non-anchor points.

#### Proof

At a root `x` of `F`, the determinant identity gives

```text
G_H(x)=-Lambda(x)H(x)/W(x).
```

At `y in R_0`, it gives

```text
B_H(y)=Lambda(y)H(y)/F(y).
```

All scaling factors are nonzero. Evaluation of degree-at-most-`r`
polynomials on these `p>r` points is therefore an injective generalized
Reed--Solomon code, and the anchor-coordinate theorem identifies it with the
complete monic chart.

For fixed `Q`, exact ownership is equivalent to

```text
H=QK,       deg K<=s,
K(z)!=0 for every root z of P_0/Q.                    (7.4)
```

Inclusion-exclusion over the `m` evaluation hyperplanes `K(z)=0` gives
`(7.2)`: a fixed `j<=s` set leaves `Q_f^(s+1-j)` polynomials, while every
intersection of more than `s` hyperplanes contains only zero. The binomial
identity for the complete alternating sum absorbs that zero-polynomial
tail. Finally `P_0` has `binom(p,q)` degree-`q` divisors, and for `q=r` the
residual `K` is any nonzero scalar. QED.

### Route verdict

This upgrades the small-cell owner-coalescence warning to an exact ambient
no-go. Owner dimension, MDS support counting, or other unguarded linear
arguments realize every top divisor rather than suppressing them. Any
successful aggregate theorem must retain simultaneous splitting of the
reconstructed locator together with the primitive, background, and
first-owner guards.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`058febd07e71302be851d2f13e62cc55a8e689ba`, node
`l1_fpc5_tpetal_joint_owner_ambient_mds_census`.

## 8. Owner-free weighted Cauchy divisor formulation

Let `chi` be the unique polynomial of degree below `h=deg Lambda`
satisfying

```text
chi==c_i (mod L_i).
```

For every locator polynomial `G` of degree at most `d`, put

```text
B_G=rem_Lambda(chi G).                                (8.1)
```

### Theorem 8.1

The pair `(G,B)` belongs to the complete `t`-petal slice if and only if
`B=B_G` and `deg B_G<=d`. If the petals split into the point set `T`, write
`c(z)=c_i` for `z in T_i` and

```text
M_j(P)=sum_(z in T) c(z) z^j P(z)/Lambda'(z).         (8.2)
```

Then

```text
deg B_G<=d
iff M_j(G)=0 for 0<=j<=h-d-2.                        (8.3)
```

For a monic squarefree core-split locator `G` and every `x in Z(G)`,

```text
B_G(x)=-Lambda(x)M_0(G/(X-x)).                        (8.4)
```

Hence primitivity is exactly the nonvanishing of all punctured moments in
`(8.4)`. At every background point `y`,

```text
B_G(y)=Lambda(y) sum_(z in T)
  c(z)G(z)/((y-z)Lambda'(z)),                         (8.5)
```

so required and forbidden background agreements are explicit Cauchy
vanishing and nonvanishing tests. Finally, if `L_Core` is the source-core
locator and `A=L_Core/G`, the moment system becomes

```text
sum_(z in T)
  c(z) z^j L_Core(z)/(A(z)Lambda'(z))=0,
0<=j<=h-d-2.                                         (8.6)
```

Thus the guarded cell is one owner-free weighted reciprocal-divisor census
over `A|L_Core`; no joint owners are independently summed.

#### Proof

CRT proves `(8.1)` and the pair-slice equivalence. Lagrange interpolation
gives

```text
B_G(X)/Lambda(X)
 =sum_(z in T)c(z)G(z)/(Lambda'(z)(X-z)).             (8.7)
```

Its expansion at infinity has coefficient `M_j(G)` at `X^(-j-1)`, proving
`(8.3)`. Substituting `G=(X-x)G_x` into `(8.7)` at `X=x` proves `(8.4)`,
and evaluation at a background point proves `(8.5)`. Since core and petals
are disjoint, `A(z)` is nonzero and `G(z)=L_Core(z)/A(z)`, proving `(8.6)`.
QED.

This is a dual-domain weighted Cauchy formulation, not an identification
with ordinary prefix flatness or a proof of the base-field-normalized
split-pencil census.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`a530e44835630165f92e01d91aa0b8e57f0ae0d7`, node
`l1_fpc5_tpetal_owner_free_cauchy_divisor_chart`.

## 9. Full-rank rational Pade-Hankel kernel

Define the weighted moment sequence

```text
mu_s=sum_(z in T)c(z)z^s/Lambda'(z),       s>=0,
c=h-d-1.
```

### Theorem 9.1

If `G=sum_(a=0)^d g_a X^a`, the complete low-numerator system `(8.3)` is

```text
H_mu g=0,
H_mu=(mu_(j+a))_(0<=j<c,0<=a<=d).                    (9.1)
```

If the pair slice contains its saturated primitive monic anchor, then

```text
rank H_mu=c,       dim ker H_mu=2d+2-h.              (9.2)
```

The moment sequence is generated canonically at infinity by

```text
chi(X)/Lambda(X)=sum_(s>=0)mu_s X^(-s-1).             (9.3)
```

Writing

```text
Lambda=X^h+lambda_(h-1)X^(h-1)+...+lambda_0,
```

it obeys

```text
mu_(s+h)+lambda_(h-1)mu_(s+h-1)+...+lambda_0 mu_s=0
for every s>=0.                                      (9.4)
```

Thus the split candidates are exactly the monic degree-`d` divisors of
`L_Core` in one full-rank rational Pade-Hankel kernel. For a selected root
`x`, writing `G/(X-x)=sum q_aX^a`, the primitive guard is the punctured
first-row pairing

```text
sum_a mu_a q_a!=0.                                   (9.5)
```

The background Cauchy tests remain unchanged.

#### Proof

Linearity gives

```text
M_j(G)=sum_a g_a mu_(j+a),
```

which is `(9.1)`. The incoming slice-dimension theorem gives kernel
dimension `2d+2-h`, and rank-nullity proves `(9.2)`. Lagrange interpolation
of `chi/Lambda` proves `(9.3)`; multiplying by `Lambda` and comparing every
negative-power coefficient proves `(9.4)`. The divisor statement and
`(9.5)` are `(8.3)--(8.4)` in coefficient form. QED.

This identifies the structured kernel class but proves no split-divisor
flatness or base-field-normalized census.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`a9ffb4521cd52953bb901296fe5bb8a766a4116e`, node
`l1_fpc5_tpetal_cauchy_hankel_kernel`.

## 10. Fixed-background codimension normalization

Assume

```text
u=d-(t-1)ell>=0
```

and fix a required `u`-set `R` of background zeros. Put

```text
P_R=Lambda L_R,       h_R=t ell+u,
```

and let `chi_R` equal `c_i` modulo `L_i` and zero modulo `L_R`.

### Theorem 10.1

The pairs satisfying the touched-petal congruences, `B|_R=0`, and
`deg B<=d` reconstruct uniquely as

```text
B_(G,R)=rem_(P_R)(chi_R G).                           (10.1)
```

Their coefficient vectors lie in the rational Pade-Hankel kernel generated
by `chi_R/P_R`, with exactly

```text
h_R-d-1=ell-1                                         (10.2)
```

rows. If the fixed-`R` cell contains a primitive monic member, this block
has full row rank `ell-1`; its locator vector space has dimension
`d-ell+2`, and its monic chart has affine codimension `ell-1`, independently
of `t` and `u`.

For any contributor family, if `R_G` is the complete background zero set
and `F_R={G:R subset R_G}`, then

```text
sum_(R subset Bkg, |R|=u)|F_R|
 =sum_G binom(|R_G|,u).                               (10.3)
```

A first-`R` rule partitions contributors disjointly, although those
first-`R` pieces need not be complete linear charts.

#### Proof

Adjoin `L_R` as a zero-label CRT block and apply Theorems 8.1 and 9.1.
Equation `(10.2)` is

```text
t ell+u-((t-1)ell+u)-1=ell-1.
```

The slice-dimension theorem gives vector dimension
`2d+2-h_R=d-ell+2`; rank-nullity gives full row rank. Double-counting the
incidences `(G,R)` proves `(10.3)`. QED.

This normalization pays neither one fixed split-divisor cell nor the sum
over background sets.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit
`6b45e49c7c1f07e6dfacd1e43a3abe260c7b33a4`, node
`l1_fpc5_tpetal_fixed_background_hankel_codimension`.

## 11. Exact GRS syndrome-shell specialization

Let one of the rational Hankel charts above have locator degree `d` and `c`
recurrence rows, and put

```text
D=d+c.
```

Thus `D=h-1` in the unaugmented chart, while a fixed-background chart has
`c=ell-1` and `D=d+ell-1`. Let `C` be the `N`-point core, put

```text
v_x=1/L_C'(x),
H_D=(v_x x^a)_(0<=a<D, x in C),
```

and retain the moment segment `mu=(mu_0,...,mu_(D-1))`.

### Theorem 11.1

Primitive core-split locators in the chart are canonically bijective with

```text
{e in F^C: wt(e)=d and H_D e=mu}.                    (11.1)
```

If `D<N`, then

```text
ker H_D=RS[F,C,N-D],                                 (11.2)
```

so `(11.1)` is exactly the radius-`d` exact shell of that GRS code around
any word with syndrome `mu`. If `D>=N`, the fixed chart contains at most one
primitive split locator. In the noninjective range, two distinct locator
supports satisfy

```text
|S intersect T|<=d-c-1.                              (11.3)
```

For the fixed-background chart this is `d-ell`.

#### Proof

For support `S`, let `w_x` be the Cramer amplitudes from the first `d`
moments. The locator recurrence extends those moment equalities through
indices `0,...,D-1`. Setting `e_x=w_x/v_x` on `S` and zero elsewhere gives
`H_De=mu`; the primitive guard is exactly `wt(e)=d`. Conversely, a
weight-`d` vector in that syndrome fiber gives its support locator, all `c`
recurrences, and nonzero Cramer amplitudes. Vandermonde recovery makes both
maps inverse.

For `D<N`, the Lagrange leading-coefficient identity puts
`RS[F,C,N-D]` in `ker H_D`, and dimensions give equality. For `D>=N`, the
first `N` weighted Vandermonde rows are invertible. Finally, the difference
of two shell vectors is a nonzero word of the `[N,N-D,D+1]` GRS code, while
its support lies in `S union T`; this proves `(11.3)`. QED.

This is the FPC5 specialization of the integrated
`l1_syndrome_catalecticant_shells.md` theorem. The parameter dictionary and
injective-range consequence are pinned to
`AllenGrahamHart/rs-mca-prize-dag` commit
`52e7b7344`, node `l1_fpc5_tpetal_hankel_grs_syndrome_shell`.

## 12. Fixed-background GRS boundary payment

Retain `0<=u<=b` and define

```text
J_fix=d^2-N(d-ell).
```

### Theorem 12.1

For the complete contributor family `F` in one fixed
source/touched/degree cell,

```text
|F|<=binom(b,u)                                      (12.1)
```

when `d+ell-1>=N`, while

```text
|F|<=binom(b,u) N ell/J_fix                          (12.2)
```

when `d+ell-1<N` and `J_fix>0`. Hence, for every fixed absolute `C`, either
branch is polynomial when `min(u,b-u)<=C`.

Moreover, if `J_bg` is the joint-background Johnson denominator, then

```text
J_bg=b J_fix-Nu(b-u).                                (12.3)
```

#### Proof

For each required `u`-set `R`, Theorem 11.1 gives at most one support in the
injective branch. In the other branch, distinct `d`-supports intersect in at
most `d-ell`; the ordinary Johnson double count gives at most
`Nell/J_fix` supports when `J_fix>0`. The fixed-background incidence identity
gives `|F|<=sum_R|F_R|`, and there are `binom(b,u)` choices. Finally,
`binom(b,u)<=b^C` under the bounded-polarity hypothesis. Substituting
`r-u=d-ell` into `J_bg=b d^2+Nu^2-Nbr` proves `(12.3)`. QED.

This payment is pinned to `AllenGrahamHart/rs-mca-prize-dag` commit
`2af7246eb`, node `l1_fpc5_fixed_background_grs_shell_payment`.

## 13. Adjacent-dimension shifted-Johnson shell cap

Fix one source/touched/degree cell and retain

```text
N=k-1,       h=t ell,       u=d-(t-1)ell,       a=N-d.
```

Define the effective syndrome endpoint `H`, chart count `W`, and adjacent
base-code dimension `K` by

```text
u<0:          H=h,           W=1,
0<=u<=b:      H=d+ell,       W=binom(b,u),
K=N-H.                                                (13.1)
```

Assume `K>=2`. For `m>=3`, put

```text
Q_m=floor sqrt((2m+1)^14 N^7
               /(384^2 (K-1)^3)).                    (13.2)
```

### Theorem 13.1

If

```text
(2m a)^2 >= (2m+1)^2 N(K-1),
K Q_m<q-N,                                            (13.3)
```

then the complete fixed cell has at most

```text
W L_m(q),
L_m(q)=ceil(Q_m(q-N)/(q-N-KQ_m))                     (13.4)
```

contributors.

#### Proof

In the `u<0` chart, Theorem 11.1 has `D=h-1`, hence target code
`C^+=RS[F,Core,K+1]`. For each fixed required background set in the other
branch, `D=d+ell-1` and the same identity holds; summing those charts costs
the exact factor `W=binom(b,u)`.

Apply Haboeck's proved quadratic MCA theorem to the adjacent code
`C=RS[F,Core,K]`. Its reduced degree rate is `(K-1)/N`, and the first
inequality in `(13.3)` says that the shell agreement reaches its printed
radius. MCA monotonicity and `epsilon_ca<=epsilon_mca` give a CA bad-slope
numerator at most `Q_m` at radius `d/N`.

The integer-radius hypothesis of `thm:A` is automatic:

```text
d<=H-1=N-K-1.
```

Using `eta=KQ_m/(q-N)` in `thm:A` gives exactly `(13.4)`. QED.

This is the one-code-dimension strip

```text
N(K-1)<a^2<=NK.                                      (13.5)
```

The method has no finite `m` when `a^2<=N(K-1)`. It retains the full
background-choice factor and therefore does not mistake a per-chart bound
for a cell payment.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit `22978e3ae`,
nodes `rs_deep_point_list_to_ca_conversion` and
`l1_fpc5_shifted_johnson_grs_shell_cap`.

## 14. Canonical first-layout compiler

Let `Delta` be a set of exact shifted cells at one fixed `(M,t)`. Cell `d`
may have its own `W_d`, `K_d`, `m_d`, and `L_d(q)` from Theorem 13.1.

### Theorem 14.1

Across every admissible maximal source layout, the complete canonical
first-owner class has size at most

```text
binom(M,t) sum_(d in Delta) W_d L_d(q)+M.             (14.1)
```

#### Proof

Choose the first admissible maximal source layout after earlier global
owners. General first-layout domination carries every selected non-anchor in
this layout and charges every later-layout member to one of its `M` planted
anchors. In the first layout, touched subsets and exact defects are disjoint
reconstructed cells. There are `binom(M,t)` touched subsets, and Theorem 13.1
bounds each fixed touched/defect cell. Sum these bounds and add the anchors
once. QED.

At `n=8192`, exact integer replay gives the following sufficient global
field gates:

```text
rate   M   shifted cells (t,d,u)                    sufficient q
1/2    5   (4,2264,-193)                            2^228
1/4   13   (3,911,-33)                              2^233
1/8   29   (3,486,-8)                               2^220
1/16  61   (3,248,-2),(3,292,42)                    2^254
```

For rate `1/16`, `M=61`, each of the other six shifted/nonpositive-Johnson
defects `d=286,...,291` exceeds `floor(q/2^128)` after the exact
`binom(61,3)` multiplier even at `q=2^256-1`. Four of those six pass at
fixed-cell level, so this is a necessary outer-composition audit rather than
a restatement of Theorem 13.1.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit `b0852b67c`,
node `l1_fpc5_shifted_johnson_first_layout_payment`.

## 15. Constant-weight shortening of every GRS shell

Fix a chart from Theorem 11.1. Put

```text
H=t ell, sigma=H-d                         when u<0,
H=d+ell, sigma=ell                         for one fixed background chart,
w=min(d,N-d).                                             (15.1)
```

For `0<=j<=w`, set

```text
x=w-j,
Delta_j=x^2-(N-j)(x-sigma).                              (15.2)
```

Call `j` admissible if `x<sigma`, with `P_j=1`, or if `Delta_j>0`, with

```text
P_j=floor((N-j)sigma/Delta_j).                           (15.3)
```

### Theorem 15.1

Every fixed chart has at most

```text
A_j=floor(binom(N,j)P_j/binom(w,j))                     (15.4)
```

members. The complete fixed source/touched/degree cell has at most `A_j`
when `u<0` and at most `binom(b,u)A_j` when `0<=u<=b`.

#### Proof

Theorem 11.1 injects chart members into weight-`d` support vectors in one
GRS syndrome coset whose kernel distance is `H`. If `S,T` are distinct
supports, the difference vector is a nonzero kernel word supported inside
`S union T`, so

```text
H<=2d-|S intersect T|,
|S triangle T|>=2(H-d)=2sigma.                          (15.5)
```

Complement the supports when `d>N/2`; distance is unchanged and their weight
is now `w`. Counting incidences with `j`-subsets shows that some common
`j`-set is contained in at least

```text
|F| binom(w,j)/binom(N,j)
```

members. Remove it. The residual family has length `N-j`, weight `x`, and
distance at least `2sigma`. It is singleton when `x<sigma`. Otherwise its
pairwise intersections are at most `x-sigma`; the ordinary incidence
second-moment argument gives

```text
m Delta_j<=(N-j)sigma.
```

This proves `(15.3)--(15.4)`. Summing the exact required-background charts
gives the final factor. QED.

Unlike Theorem 13.1, this theorem has no adjacent-dimension or field-size
hypothesis. It may still be exponential when the required shortening depth
grows.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit `12ed6c980`,
node `l1_fpc5_grs_shell_constant_weight_shortening_cap`.

## 16. Official first-scale prefix payment

Apply Theorem 15.1 to every exact `(PF6)` survivor at `n=8192`, minimize over
all admissible shortening depths, and compile through Theorem 14.1.

### Theorem 16.1

At rate `1/8`, the complete source-scale prefix `M=29,...,32` has `126`
fixed defect cells in five `(M,t)` groups and total global cap

```text
G_8=195112047344632914122867933361797765038.            (16.1)
```

It is paid for `q>=2^128 G_8`; this threshold has 256 bits and is below
`2^256`.

At rate `1/16`, the complete prefix `M=57,...,67` has `374` cells in twelve
groups, with `M=60` empty, and total cap

```text
G_16=2444555448501019158442942184801171570.             (16.2)
```

It is paid for `q>=2^128 G_16`, a 249-bit threshold.

#### Proof

For each fixed `(M,t)`, sum the exact chart factors and caps from Theorem
15.1 over the disjoint defect cells, multiply once by `binom(M,t)`, and add
the `M` planted anchors from Theorem 14.1. Sum the resulting bounds over
touched counts and source scales. Exact integer replay gives `(16.1)` and
`(16.2)`. Since the target budget is `floor(q/2^128)`, the printed field
gates are sufficient. QED.

The same compiler is above the strict budget cap at rate-half `M=5`,
rate-quarter `M=13`, rate-`1/8` `M=33`, and rate-`1/16` `M=68`. These are
upper-bound route fences, not lower bounds on any contributor family.

Source provenance: `AllenGrahamHart/rs-mca-prize-dag` commit `12ed6c980`,
node `l1_fpc5_grs_shortening_official_prefix_payment`.

## 17. Nonclaim

The theorem types the joint owner and all remaining background equations and
pays each fixed guarded owner. The dual-domain reduction neither counts its
pencils nor supplies a converse from arbitrary coefficient pairs to guarded
FPC5 candidates. The MDS formula counts the complete unguarded chart, not
the guarded contributors. The Cauchy, Hankel, fixed-background, and GRS-shell
formulations are exact. Theorems 13.1 and 14.1 add a field-dependent payment
in the adjacent-code strip. Theorems 15.1 and 16.1 extend fixed-chart control
beyond that strip and pay two finite official prefixes, but their shortening
depth can grow and the outer cap still fails at the four printed next
scales. These theorems do not supply a complete middle-polarity upper bound,
aggregate the realized guarded owners, pay lower field slices or larger
rows, deploy a Prize endpoint, or close the full large-source target. Summing
`(5.2)` over all divisors of `P_0` can still be exponential.
