# Rank-One Split-Scroll Counting Target

## 1. Purpose and status

This is the remaining proof target after the KoalaBear equality-wall
fixed-domain, kernel-sheaf, Kronecker, and source-normalization reductions.

The target concerns the first open KoalaBear MCA equality-wall slack

```text
sigma_wall = 134,943.
```

It is open. No active owner or charge is currently obtained from it.

The source-fiber refinement in

```text
rank_one_split_scroll_source_fiber_reduction.md
```

now proves that the primitive source scalar has simple roots exactly at the
source-map values and bounds the persistent carrier core. It first excludes
the lower `q=1` range `delta<c`; on the surviving low-excess range
`c<=delta<e`, exact pushforward degree `q=2` excludes splitting degrees 2
through 11. Together these arguments close the interval

```text
3,912 <= delta < 118,077.
```

The three-source-fiber branch is empty. The only surviving low-excess
splitting degrees are `12,13,14,15,16`.

The proved supporting notes are:

```text
experimental/notes/frontier-adjacent/
  kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md
  kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md
  kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.md
```

The newest packet proves the kernel-sheaf normal form, exceptional-divisor
bound, source-zero descent, exact locator Kronecker decomposition, and the
low-excess monicity/source identity. It does not prove the count below.

## 2. Fixed constants

```text
p       = 2,130,706,433
M       =            69
s       =       202,416
e       =       134,944
c       =        67,472
|V|     =     1,894,736
J       =       981,105
dim W   <=             9
```

The normalized excess satisfies

```text
3,912 <= delta <= 846,159 < 7e.
```

Put

```text
u = 1,048,577 + delta,
d = 67,472 + delta,
N = 202,416 + delta.
```

## 3. Original normalized records

There are 69 distinct finite parameters `t_i`, one coprime degree-`e`
pencil

```text
A_t = U+tV,
gcd(U,V)=1,
max(deg U,deg V)=e,
```

and monic squarefree locators

```text
p_i = Lambda_(D_i),
D_i subseteq U0,
|D_i|=d,
```

such that

```text
|D_i intersect D_j| <= delta,
intersection_i D_i = empty.
```

The graph polynomials

```text
F_i=A_(t_i)p_i
```

belong to one space

```text
W subseteq H^0(P1,O(N)),
dim W<=9,
```

and have identical nonzero restriction `f0` on the `s` source points.

The fixed-domain locator coefficient rank is at most 16. If `C` is the
locator coefficient-row space and

```text
T=diag(t_1,...,t_69),
```

then

```text
dim C<=16,
dim(C+CT)<=17.
```

## 4. Proved kernel-sheaf reduction

Let

```text
Phi: W tensor O -> f_*O(N)
```

be fiber evaluation for `f=[-U:V]`. A hypothetical 69-record packet has a
positive generic kernel

```text
K=ker Phi
  = direct-sum_j O(-a_j).
```

Write

```text
r=rank K,
A=sum_j a_j,
m=dim W,
q=floor(N/e)<=7.
```

The set of parameters where the actual fiber kernel is larger than `K(t)`
has size at most

```text
D_exc <= q(m-r)-A <= 7(m-r)-A.
```

All other selected records lie in the actual fibers of the generic kernel.

Source restriction gives a source-zero subkernel `K0` with

```text
rank(K/K0)<=1.
```

Every source-zero kernel section factors as

```text
Lambda_Sigma A_t Q,
deg_X Q <= delta-e.
```

Thus source-zero components descend by exactly `e`, and the descent depth is
at most six.

## 5. Clean low-excess target

Assume first

```text
delta<e.
```

The exact `q=1` source/incidence reduction excludes `delta<c`. Hence only

```text
c<=delta<e
```

remains. In this range

```text
q=floor((s+delta)/e)=2.
```

Then `K0=0`, `rank K=1`, and

```text
K=O(-a),       2<=a<=16.
```

At most

```text
16-a
```

selected parameters are exceptional. Therefore at least

```text
R_reg >= 53+a
```

regular selected records lie on one primitive scroll

```text
G(t,X)=A_t(X)P(t,X),
deg_t G<=a,
deg_t P<=a-1,
deg_X P=d.
```

There is one nonzero source scalar `lambda(t)` such that

```text
G(t,sigma)=lambda(t)f0(sigma)
```

on every source point. Monicity proves exactly

```text
lambda(t) = coeff_(X^d) P(t,X),
p_i(X) = P(t_i,X)/lambda(t_i)
```

at every regular selected parameter.

The refined source-scalar theorem proves

```text
a=|f(Sigma)|.
```

### Low-excess rank-one split-scroll lemma

Prove that the number of selected parameters, including the exceptional
parameters, is at most 68.

An equivalent sufficient bound in this exact-`q` range is:

```text
number of regular U0-split specializations <= 52+a,
```

because

```text
(16-a)+(52+a)=68.
```

The regular locators must remain monic, squarefree, and split over the same
fixed `u`-point set, with pairwise gcd degree at most `delta`.

### Proved exact-q source-fiber refinement

Let

```text
a = |f(Sigma)|
```

be the kernel splitting degree, which is now proved to equal the number of
distinct source-map values. If `g` is the persistent carrier-root degree and

```text
h = delta-g,
```

then every hypothetical regular packet satisfies

```text
h >= e-floor((s-(a-1))/a)
54(c+h) <= (a-1)J.
```

They are incompatible for every `2<=a<=11`. In particular, the actual
`a=3` branch has at least 56 regular records and fails carrier incidence
with exact margin

```text
5,324,766.
```

The exact surviving windows are

```text
a   R_reg floor   h_min     h_max
12       65       118,077   132,382
13       66       119,375   134,943
14       67       120,487   134,943
15       68       121,451   134,943
16       69       122,294   134,943
```

The low-excess target is now to exclude `53+a` regular fixed-domain split
specializations in each of these five windows, or emit an existing
same-record owner.

## 6. General-excess target

For `delta>=e`, a regular selected locator has the exact form

```text
p_i
  = P_0(t_i)/lambda_0(t_i)
    + Lambda_Sigma Q_i,
```

where the first term belongs to the unique non-source-zero quotient line and
`Q_i` belongs to a descended universal divisibility kernel of degree at most
`delta-e`.

Repeat the kernel-sheaf decomposition on the descended space. After at most
six levels, every record has:

1. one non-source-zero rank-one scroll component;
2. a finite flag of lower-degree source-zero corrections;
3. a printed exceptional-divisor budget at every level.

### Recursive rank-one split-scroll lemma

Prove, by induction on `floor(delta/e)`, that the union of:

```text
regular split specializations at the current level,
exceptional parameters at the current level,
parameters passed to lower-degree correction levels
```

has cardinality at most 68.

The induction must preserve:

```text
monicity,
fixed-domain splitting,
pairwise gcd degree <= delta,
total gcd 1,
distinct original parameters,
the source scalar divisor,
and every exceptional-divisor charge.
```

## 7. Exact locator Kronecker information

The locator small-expansion pencil has the proved decomposition

```text
C
 = F^S
   direct-sum
   direct-sum_(alpha=1)^h
     span(v_alpha,Tv_alpha,...,T^(epsilon_alpha-1)v_alpha),
```

where

```text
h=dim(C+CT)-dim C,
dim C=|S|+sum_alpha epsilon_alpha.
```

The coordinate part consists of actual diagonal eigenlines. Each nontrivial
part is a left Kronecker block. Different Krylov generators may have
overlapping coordinate supports.

If `h=1`, at least 53 selected coordinates lie on one weighted polynomial
block. Monicity gives

```text
p_i(X)=P(t_i,X)/ell(t_i),
deg_t P<epsilon,
```

and source restriction gives the polynomial identity

```text
A_t(sigma)P(t,sigma)=ell(t)f0(sigma).
```

Hence

```text
|f(Sigma)|<=epsilon.
```

This one-block identity is available as an independent route into the
rank-one count. For `h>1`, the exact mixed-block expression must be retained;
replacing it by one GRS block is invalid.

## 8. Promising proof approaches

### 8.1 Fixed-domain divisibility

Put

```text
R_U0(X)=product_(x in U0)(X-x).
```

At every regular selected parameter,

```text
P(t_i,X)/lambda(t_i) divides R_U0(X).
```

Use the low `t`-degree, source-scalar divisor, squarefreeness, and pair-gcd
cap to bound the number of such divisibility specializations. A naive
resultant degree is too large; the proof must exploit common fixed roots.

### 8.2 Root-incidence polynomials

For each `x in U0`, the scalar polynomial

```text
P_x(t)=P(t,x)
```

has degree at most `a-1`. Unless it vanishes identically, `x` can occur in
at most `a-1` regular root sets. Separate persistent roots, then use the
pair-gcd and total-gcd conditions to control them.

The source-fiber refinement and exact `q=2` make the first moment
load-bearing: they exclude every `a<=11`. Ordinary higher incidence moments
do not close the five windows `a=12,...,16`. The next goal is a
rank/source-sensitive fixed-domain theorem for those five high-regularity
families.

The regular-coordinate structure is now exact. The note

```text
regular_grs_mds_deficit_reduction.md
```

proves that the locator coefficient-row space on the regular parameters is
the weighted code

```text
GRS_a(t_1,...,t_R; 1/lambda(t_1),...,1/lambda(t_R)),
```

and that its one-step diagonal expansion has dimension exactly `a+1`.
Writing `D=c+h`, the carrier-row MDS deficits satisfy

```text
Delta_R
  = sum_x ((a-1)-m_x)
  = (a-1)J-(R-a+1)D.
```

For `a=12`, this gives:

```text
R   h_max    minimum-weight rows at h_min
65  132,382                  394,145
66  128,749                  579,694
67  125,245                  765,243
68  121,864                  950,792
69  118,599                1,136,341
```

The all-regular case is therefore confined to

```text
118,077 <= h <= 118,599.
```

Its total post-core source-fiber multiplier degree is at most `6,265`, and
at the first surviving endpoint it is at most one. At that endpoint,
eleven residual source-fiber multipliers are constant and only one can be
linear.

This still does not close by incidence alone. At `R=69` and the lower
endpoint, the average pair codegree contributed by the forced
minimum-weight rows is about `26,641`, compared with the allowed pair-gcd
cap `118,077`. The next input must constrain how the source-divisor
coefficient curve meets the minimum-weight vertices of this exact GRS
arrangement.

### 8.3 Kronecker-block plus source divisor

Use the exact locator Kronecker decomposition. In a one-block component,
monicity gives a common denominator and source restriction forces all source
values into its zero divisor. Classify the low-source-image alternative or
route it to an existing pair-global source owner.

Coordinate eigenlines and mixed Krylov blocks must be counted separately.

On the regular coordinates the new GRS theorem removes this ambiguity:
there is one exact weighted-GRS block. Mixed components can still occur in
the full locator small-expansion object through exceptional coordinates,
so they cannot be discarded from the recursive global count.

### 8.4 Remainder or Wronskian method

Compute the remainder of `R_U0` on division by the monic family `p_t`.
Every coefficient vanishes at every regular split specialization. Seek a
low-degree nonzero minor, Wronskian, or subresultant after dividing the
persistent-root part.

### 8.5 Rank-aware RS list bound

Use the equivalent fixed-domain agreement list:

```text
69 degree-<=delta polynomials,
affine span dimension <=8,
agreement c+delta with one word,
pair common agreement <=delta.
```

The ordinary Johnson bound is approximately 72.6 at `delta=3,912` and then
weakens. A successful bound must use affine dimension, split locators, or
the source pencil.

### 8.6 Degree-descent induction

Prove the low-excess rank-one count first. Then show that every
source-zero correction either:

```text
consumes a bounded exceptional-divisor budget,
descends to the already-proved lower degree,
or forces a persistent common locator factor.
```

The last case must contradict total gcd 1 or emit a valid same-record owner.

### 8.7 Complement-locator interpolation descent

The note

```text
complement_locator_interpolation_descent.md
```

proves a canonical fixed-domain identity. If `Q(t,X)` interpolates the
support-side complementary carrier locators

```text
q_i=R_U/p_i,
```

then

```text
Pbar(t,X)Q(t,X)-lambda(t)R_U(X)
  = H_T(t)Lambda_Sigma(X)S(t,X),
deg_t S <= a-2,
deg_X S <= |U|-s-1.
```

For a carrier row incident to `m_x` regular locators, the two
selected-root factors have degrees at most

```text
a-1-m_x
and
m_x-1.
```

Their product is `Lambda_Sigma(x)S(t,x)`. Thus the MDS deficit
`eta_x=a-1-m_x` is exactly the available degree on the first factor.

This is a genuine one-step parameter-degree descent. It is not yet an
active owner: `q_i` is the locator of `Y_i` inside the normalized carrier,
whereas the active packet is rooted at the original complement locator
`Lambda_(Z_i)`.

The same note proves the exact resultant ledger. For the descended companion
`C`,

```text
deg_X Res_t(Pbar,C) - R*D
  <= Delta_R + B_a(h),
B_a(h) = s-a(e-h)-(a-1).
```

Thus the naive resultant route is saturated by the already printed
weighted-GRS deficit and source-fiber multiplier budget. The useful next
theorem, proved in

```text
homogeneous_resultant_factorization.md
```

is stronger:

```text
Res_[T0:T1](Pbar,C)
  = unit * R_U^(a-1) * product_j Rtilde_j.
```

The resultant is nonzero, and its complete divisor consists only of the
carrier and the actual residual source multipliers. Therefore neither a
resultant-zero second kernel nor an excess-resultant-multiplicity argument
is available. The remaining proof must retain the rowwise factors
`A_x`, `B_x`, and `S(t,x)` before the resultant collapses their selected
owner pattern.

### 8.8 Minimum-window coefficient-curve birationality

The note

```text
minimum_window_coefficient_curve_birationality.md
```

proves that the coefficient map

```text
X -> [Qbar_1(X):...:Qbar_a(X)]
```

is birational onto its image at the lower endpoint of each of the five
surviving windows. At each endpoint, two finite zero-slack source fibers
give a coefficient ratio of degree `n0=e-h_min+1`. The covering degree
divides both `D=c+h_min` and `n0`, whose gcd is one in all five cases.

Thus no minimum-window endpoint can be reduced to a nontrivial cover of a
lower-degree rational normal curve or scroll section. The endpoint target
is a genuinely birational degree-`D` fixed-domain problem.

### 8.9 Source-partition Cremona descent

The note

```text
source_partition_cremona_descent.md
```

applies standard Cremona transformation to the source coefficient map and
proves the exact lower-degree coordinates

```text
Psi_j=Lambda_(Sigma_j)*product_(k!=j) Rtilde_k.
```

At the five minimum endpoints, `Psi` remains birational and has degree at
most

```text
16,869; 15,577; 14,463; 13,501; 12,652
```

for `a=12,...,16`. Each selected locator equation becomes a
degree-`(a-1)` hypersurface satisfying

```text
H_i(Psi)=R_*^(a-2)*pbar_i.
```

This preserves every selected incidence after the explicit common residual
divisor is removed. It is the preferred endpoint model for a geometric
rigidity proof.

### 8.10 Reciprocal-Cauchy separator target

The note

```text
reciprocal_cauchy_separator_target.md
```

identifies every Cremona-transformed selected vertex with the evaluation
vector of a complementary split polynomial:

```text
y_I ~= (M_I(alpha_1)/G(alpha_1),...,M_I(alpha_a)/G(alpha_a)).
```

The exact sufficient subtarget is that degree `R-a+2` forms through this
finite reciprocal-Cauchy configuration separate every point outside the
configuration. If proved, the descended degree and MDS-deficit count give

```text
N_min <= (R-a+2) E_Psi.
```

For `a=12`, `R=69`, this would exclude all

```text
118,077 <= h <= 118,316
```

with endpoint margin `141,070`. A stronger degree-`R-a+1`
unisolvence claim is false in generic finite tests; the corrected
separator statement remains open.

### 8.11 KoalaBear postcritical interpolation target

The weaker note

```text
postcritical_reciprocal_cauchy_interpolation_target.md
```

asks for full interpolation on the same transformed vertices, in the
actual KoalaBear field and packet, in degree `R-a+2`. It proves
separation one degree later, so the resulting
Bezout bound is

```text
N_min <= (R-a+3) E_Psi.
```

For `a=12`, `R=69`, this would exclude

```text
118,077 <= h <= 118,283
```

with endpoint margin `124,201`, leaving `316` all-regular values
`118,284,...,118,599`.

The original all-fields formulation is false. Over `F_13` at
`(a,R)=(4,8)`, 273 of the 6,435 source/selected partitions have
postcritical rank 54 or 55 instead of 56. Different exact failures occur
in characteristics 17, 19, and 23, so the corrected target must permit
semantic exceptions rather than assume a finite list of bad
characteristics.

The exact continuation is recorded in

```text
cremona_star_hypercohomology_reduction.md
```

Postcritical surjectivity is equivalent to killing the critical relation
space by simultaneous coordinate multiplication, and also to one
total-degree-one hypercohomology vanishing on the permutohedral
resolution of Cremona. The KoalaBear specialization, or a same-record
semantic owner for every rank-deficient exception, remains open.

The proved block-line branch is in

```text
reciprocal_cauchy_block_line_emission.md
```

Every selected `a`-block contributes `a` vertices on one canonical line,
and two block lines coincide exactly when

```text
P_B - c P_C = (1-c) A_source.
```

In the complete `F_13` census, the entire postcritical relation space is
generated by the coincident block-line relation spaces in every
configuration. The printed exceptions in characteristics 17, 19, and 23
and the higher-dimensional planted regressions have the same property.

Distinct full blocks on one line are pairwise disjoint, while any
additional vertex is a near-full fiber consuming `a-1` new selected
roots. Hence the exact maximum canonical-line-supported postcritical
relation dimension is

```text
max(0,
    a floor(R/a)
    + 1_(R mod a = a-1)
    - R + a - 3).
```

It is zero for `a=12,R=69` and for `a=14,R=67,68,69`. Thus the known
planted mechanism cannot create any interpolation defect in those
branches. This pays the algebraic classification of all known failures as
a bounded split-pencil precursor and removes that branch completely from
the hardest all-regular case; the same-record atlas payment where the
capacity is positive and the non-block-line relation classification
remain open.

## 9. Useful exact numerics

Pair-incidence packing already forces

```text
delta>=3,912.
```

At `delta=3,912`:

```text
minimum pair incidence = 9,177,094
available cap          = 9,177,552
remaining margin       =       458
```

The near-equality means that carrier-root multiplicities are close to the
balanced distribution. This is useful for a stability or higher-incidence
argument, but is not itself a contradiction.

The exact-q source-fiber reduction additionally gives:

```text
a=3 contradiction margin        = 5,324,766
excluded low-excess interval    = [3,912, 118,076]
excluded integer delta values   = 114,165
surviving splitting degrees     = 12,13,14,15,16
minimum surviving h             = 118,077
```

## 10. Required proof output

A successful proof should print:

1. the kernel rank and splitting degrees;
2. every exceptional-divisor budget;
3. the source-zero descent tree;
4. the primitive non-source-zero generator and source scalar;
5. the persistent-root decomposition;
6. the exact count of regular split specializations at each level;
7. the treatment of coordinate and mixed Kronecker components;
8. the final total at most 68; and
9. the resulting equality-wall line payment.

## 11. Invalid shortcuts

The following do not prove the target:

1. applying the cap 63 after the generic kernel becomes positive;
2. counting zeros of an identically zero determinant;
3. discarding source-zero corrections;
4. assuming every Kronecker decomposition has one block;
5. assuming different blocks have disjoint coordinate support;
6. using formal-root GM-MDS independence at the fixed KoalaBear domain;
7. using the ordinary Johnson cap;
8. treating an auxiliary descended quotient as an active owner;
9. forgetting exceptional fiber kernels; or
10. proving a bound only for regular parameters and omitting their add-back.

## 12. Valid falsifier

A valid falsifier must construct 69 distinct parameters satisfying the full
original normalized packet, together with the proved kernel and descent
interfaces. In the low-excess branch it must in particular supply:

```text
c<=delta<e,
12<=a<=16,
at most 16-a exceptional parameters,
at least 53+a regular parameters,
one primitive G=A_tP,
p_i=P(t_i)/lambda(t_i) monic and U0-split,
pair gcd degree <=delta,
total gcd 1,
a=|f(Sigma)|,
h in the corresponding exact surviving window.
```

An arbitrary rational scroll or an arbitrary split polynomial family is not
a falsifier.

## 13. Consequence and nonclaims

The recursive rank-one split-scroll lemma implies:

```text
universal-kernel branch <=68
+ generic-kernel-free branch <=63
=> every primitive equality-wall line <=68 source-map classes
=> sigma_wall=134,943 paid.
```

It does not pay later slacks, the conditional Q theorem, or any other
KoalaBear residual.

# OPEN EXTERNAL PROOF TARGET
