---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The nowhere-zero master-denominator received table refunds one affine-span dimension after one agreement pivot. Every cumulative effective-deficit head delta=q-s=g-deg(H) obeys the nested-floor H_Q bound. This pays every pure full-G zero-anchored rank-at-most-seven family for 217543<=g<=354972 and leaves exactly 72860<=g<=217542 in that fixed-G lane. At the endpoint, however, the sharp H_Q histogram still has an exact feasible scalar and harmonic marginal primal, so global rank seven requires a cross-cofactor interlaced H-locator and deep-fiber incidence theorem.
architecture: M31_BASE_FIELD_BOUNDARY_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT_V1
atom_or_cell: Rank-seven local closure and joint-incidence route cut; no v4 atom value and no signed-Xi payment.
quantifier: Every base-field boundary-anchor rank-at-most-seven shallow family supplied by the exact master-denominator predecessor, for every residual union size 72428<=g<=354972.
claimed_bound: N_delta(<=Q)<=floor(R/(g-Q)*floor(binomial(R-g+w+6,6)/binomial(w-Q+6,6))).
status: PROVED LOCAL THEOREM AND PURE FIXED-G RANK-SEVEN CLOSURE / GLOBAL ROW OPEN
impact: ONE-PIVOT HEAD COMPILER / FIXED-G HIGH INTERVAL PAID / CROSS-COFACTOR INTERLACED LOCATOR TERMINAL FROZEN
falsifier: A nowhere-zero linear RS flat violating the nested-floor lemma; an all-g frontier cell differing from the sealed scan; a pure full-G rank-at-most-seven forbidden family at g>=217543; failure of the fixed-H fiber dichotomy; or an endpoint scalar resource excluding the sealed integer histogram and transport.
replay: Exact Python big-integer exhaustion, optimized-mode parity, proof-critical mutations, independent Sage all-g replay and fixed-H control, sealed predecessor replay, and fresh independent proof review.
---

# M31 rank-seven effective-deficit one-pivot route cut

## Status and exact scope

This packet proves three local statements.

1. A nowhere-zero received table gives a one-pivot refinement of the
   recursive affine-span Reed--Solomon compiler.
2. In the M31 master normalization, the refinement applies to
   \[
   \delta_i:=q_i-s_i=g-\deg H_i.
   \]
   It pays the entire pure full-\(G\), zero-anchored rank-at-most-seven
   branch for
   \[
   217\,543\le g\le354\,972.
   \]
3. For a fixed locator \(H\), the divisibility fiber is an empty-or-singleton
   fiber when \(\delta\le w\), and has dimension at most
   \(\min(7,\delta-w)\) when \(\delta>w\).

The packet does **not** close the mixed-\(G\) rank-seven family.  At
\(g=354\,972\), an exact adversarial \(\delta\)-histogram obeys the new
cumulative caps, the predecessor cumulative caps, all five displayed scalar
resources, and the predecessor harmonic marginal resources.  The associated
integer transport is a marginal relaxation, not a common-support or
full-gcd source family.

No v4 ledger atom moves.  Rank at least eight and the complete M31 LIST row
remain open.

## 1. Source normalization and effective deficit

The sealed parent supplies

\[
\begin{aligned}
p&=2^{31}-1,& n&=2\,097\,152,& K&=1\,048\,576,\\
a&=1\,116\,023,& R&=981\,129,& w&=67\,447,
\end{aligned}
\tag{1.1}
\]

and a forbidden shallow family would contain

\[
L=15\,775\,933
\tag{1.2}
\]

nonanchors.

For the exact master denominator

\[
P=\operatorname{lcm}_iG_i,\qquad
g=\deg P,\qquad
f_i=(P/G_i)b_i,\qquad
d=g-w,
\tag{1.3}
\]

the normalized messages lie in one linear space

\[
\mathcal W\subseteq\mathbb F_p[X]_{<d},
\qquad
\dim\mathcal W\le7.
\tag{1.4}
\]

On the fixed \(R\)-point set \(E_0=Z(L_0)\), the received table is

\[
u=P H_0=P/V.
\tag{1.5}
\]

Because \(P\) and \(V\) are units modulo \(L_0\),

\[
u(x)\ne0\qquad(x\in E_0).
\tag{1.6}
\]

The exact full gcd is

\[
H_i=\gcd(L_0,Y-f_i),
\qquad Y=PH_0,
\tag{1.7}
\]

and

\[
\deg H_i=\deg G_i+s_i=g-q_i+s_i.
\tag{1.8}
\]

Define the **effective deficit**

\[
\boxed{\delta_i=q_i-s_i=g-\deg H_i.}
\tag{1.9}
\]

Then the exact number of agreements of \(f_i\) with \(u\) on \(E_0\) is

\[
\operatorname{agr}_{E_0}(f_i,u)
=\deg H_i
=g-\delta_i.
\tag{1.10}
\]

This is stronger information than the old implication
\(q_i\le Q\Rightarrow\operatorname{agr}_{E_0}\ge g-Q\):
the same implication now holds directly for the larger head
\(\delta_i\le Q\).

## 2. Nowhere-zero one-pivot compiler

### Theorem 2.1

Let \(E\) be a set of \(N\) distinct field points.  Let

\[
\mathcal W\subseteq\mathbb F[X]_{<d}
\tag{2.1}
\]

be a \(k\)-dimensional linear space, \(k\ge1\), and let

\[
u:E\longrightarrow\mathbb F^\times
\tag{2.2}
\]

be nowhere zero.  Put

\[
m=d+v,\qquad v\ge0.
\tag{2.3}
\]

Let \(Z\subseteq E\) be the common-zero set of \(\mathcal W\), with
\(z=|Z|\).  If \(m>N-z\), the list is empty.  Otherwise

\[
\boxed{
\#\{f\in\mathcal W:\operatorname{agr}_E(f,u)\ge m\}
\le
\left\lfloor
\frac{N-z}{m}
\left\lfloor
\frac{\binom{N-d+k-1}{k-1}}
     {\binom{v+z+k-1}{k-1}}
\right\rfloor
\right\rfloor.}
\tag{2.4}
\]

For \(k=0\), the linear space contains only zero, so the list is empty
when \(m>0\).

The nested floor order in (2.4) is part of the statement.

### Proof

Let \(L_Z\) be the locator of \(Z\).  Every member of \(\mathcal W\) is
divisible by \(L_Z\).  Put

\[
\mathcal W'=\{f/L_Z:f\in\mathcal W\},
\qquad
u'(x)=u(x)/L_Z(x)\quad(x\in E\setminus Z).
\tag{2.5}
\]

Division embeds \(\mathcal W'\) as a \(k\)-dimensional subspace of

\[
\operatorname{RS}(E\setminus Z,d-z).
\tag{2.6}
\]

Since \(u\) is nowhere zero, every point of \(Z\) is a mismatch for every
member of the list.  Moreover \(u'\) is nowhere zero, and
\(f(x)=u(x)\) is equivalent to
\((f/L_Z)(x)=u'(x)\) off \(Z\).  Thus a listed word retains at least \(m\)
agreements on \(E\setminus Z\).

For \(x\in E\setminus Z\), evaluation at \(x\) is a nonzero functional on
\(\mathcal W'\).  Hence

\[
\mathcal W'_x=\{f'\in\mathcal W':f'(x)=u'(x)\}
\tag{2.7}
\]

is empty or is an affine flat with direction dimension \(k-1\).  The
already-proved recursive affine-span compiler, applied on the punctured
domain, bounds the listed members of \(\mathcal W'_x\) by

\[
B_{k-1}(z)=
\left\lfloor
\frac{\binom{(N-z)-(d-z)+k-1}{k-1}}
     {\binom{m-(d-z)+k-1}{k-1}}
\right\rfloor
=
\left\lfloor
\frac{\binom{N-d+k-1}{k-1}}
     {\binom{v+z+k-1}{k-1}}
\right\rfloor.
\tag{2.8}
\]

Double-count the pairs \((f,x)\) for which \(f\) is listed and
\(f(x)=u(x)\).  Every listed \(f\) contributes at least \(m\) pairs, while
there are \(N-z\) possible pivots and at most \(B_{k-1}(z)\) listed words
through each pivot.  Therefore

\[
|\mathcal L|m\le(N-z)B_{k-1}(z),
\tag{2.9}
\]

which gives (2.4).

Both \(N-z\) and \(B_{k-1}(z)\) are nonincreasing in \(z\).  After weakening
to \(z=0\), the raw inner ratio is nondecreasing in \(k\), since

\[
\frac{\operatorname{raw}_{k+1}}{\operatorname{raw}_k}
=\frac{N-d+k}{v+k}\ge1
\tag{2.10}
\]

whenever \(m=d+v\le N\).  Floors preserve this comparison.  Thus a uniform
rank-at-most-seven bound may set \(z=0\) and \(k=7\).

## 3. M31 cumulative effective-deficit bound

For an integer cutoff \(Q\), put

\[
\mathcal I_Q=\{i:\delta_i\le Q\}.
\tag{3.1}
\]

Every member of \(\mathcal I_Q\) has at least

\[
g-Q=(g-w)+(w-Q)
\tag{3.2}
\]

agreements on \(E_0\).  Apply Theorem 2.1 with

\[
N=R,\qquad d=g-w,\qquad m=g-Q,\qquad v=w-Q.
\tag{3.3}
\]

This gives

\[
\boxed{
|\mathcal I_Q|
\le
H_Q(g):=
\left\lfloor
\frac{R}{g-Q}
\left\lfloor
\frac{\binom{R-g+w+6}{6}}
     {\binom{w-Q+6}{6}}
\right\rfloor
\right\rfloor.}
\tag{3.4}
\]

The exact integer implementation is

```text
inner = binomial(R-g+w+6,6) // binomial(w-Q+6,6)
H_Q   = R * inner // (g-Q)
```

The legal nonvacuous scan range is

\[
\boxed{
\max(g-R,-366\,886)
\le Q\le
\min(w,g-w-1).}
\tag{3.5}
\]

The two lower bounds come from \(\deg H_i\le R\) and
\(\delta_i=q_i-s_i\ge-366\,886\).  The first upper bound keeps
\(w-Q\ge0\).  For the second, \(f_i\ne0\) and

\[
q_i=\deg\gcd(P,f_i)\le\deg f_i\le g-w-1,
\qquad
\delta_i\le q_i.
\tag{3.6}
\]

Negative \(Q\) is meaningful for effective-deficit heads.  It is not a
negative-\(q\) assertion.

The predecessor affine-span cap

\[
C_Q(g)=
\left\lfloor
\frac{\binom{R-g+w+7}{7}}
     {\binom{w-Q+7}{7}}
\right\rfloor
\tag{3.7}
\]

also applies verbatim to \(\delta_i\le Q\), because its proof only needs the
agreement floor (3.2).  The new \(H_Q\) family is the additional
nowhere-zero resource.

## 4. Exact all-\(g\) frontier

Let

\[
T=L-1=15\,775\,932
\tag{4.1}
\]

and define

\[
Q_\star^H(g)=
\max\{Q\text{ in (3.5)}:H_Q(g)\le T\}.
\tag{4.2}
\]

Exact big-integer exhaustion of every

\[
72\,428\le g\le354\,972
\tag{4.3}
\]

gives:

```text
g cells                         282,545
maximal Q*_H intervals           38,569
Q*_H range                 -23,382 ... 15,186
interval SHA-256
4e2e2d6ddf919ace174a1cdd3f8df78520d0608a90c87fa231a5075cb8d13b52
```

The interval-length histogram is

```text
2: 1
4: 608
5: 6,225
6: 7,068
7: 6,716
8: 6,640
9: 6,750
10: 4,475
11: 86
```

Selected exact cells are:

| \(g\) | \(Q_\star^H\) | \(H_{Q_\star^H}\) | next cap | forced tail |
|---:|---:|---:|---:|---:|
| 72,428 | -23,382 | 15,775,051 | 15,776,260 | 882 |
| 72,859 | -23,288 | 15,775,862 | 15,777,078 | 71 |
| 72,860 | -23,288 | 15,775,606 | 15,776,811 | 327 |
| 100,000 | -17,825 | 15,775,580 | 15,776,821 | 353 |
| 150,000 | -9,365 | 15,775,346 | 15,776,676 | 587 |
| 200,000 | -2,265 | 15,775,549 | 15,776,985 | 384 |
| 217,542 | -1 | 15,774,477 | 15,775,952 | 1,456 |
| 217,543 | 0 | 15,775,767 | 15,777,242 | 166 |
| 250,000 | 3,951 | 15,775,804 | 15,777,360 | 129 |
| 300,000 | 9,550 | 15,775,689 | 15,777,378 | 244 |
| 328,677 | 12,548 | 15,774,337 | 15,776,109 | 1,596 |
| 328,678 | 12,549 | 15,775,929 | 15,777,701 | 4 |
| 354,972 | 15,186 | 15,774,749 | 15,776,606 | 1,184 |

The largest weakest tail upper bound is \(1\,852\), at

\[
(g,Q_\star^H)=(354\,397,15\,129).
\tag{4.4}
\]

There are 204 cells at which the weakest tail upper is zero.  These are
exact marginal thresholds, not row payments.

## 5. Pure full-\(G\) rank-seven closure

Suppose the complete family has one fixed denominator \(G\).  Then its exact
master lcm is \(P=G\), so

\[
q_i=0,\qquad
\delta_i=-s_i\le0
\tag{5.1}
\]

for every member.  Thus the entire family belongs to the \(Q=0\) head.

Exact arithmetic gives

\[
H_0(217\,542)=15\,775\,952>L,
\tag{5.2}
\]

\[
H_0(217\,543)=15\,775\,767<L.
\tag{5.3}
\]

The expression \(H_0(g)\) is nonincreasing in \(g\): both
\(R/g\) and

\[
\binom{R-g+w+6}{6}
\tag{5.4}
\]

are nonincreasing.  Therefore:

> **Corollary 5.1 (pure full-\(G\) rank-seven payment).**
> No pure full-\(G\), zero-anchored linear-rank-at-most-seven family of
> forbidden size exists for
> \[
> 217\,543\le g\le354\,972.
> \]

The existing fixed-\(G\) ordinary-RS Johnson cap pays through
\(g=72\,858\), and
the existing endpoint peeling theorem pays \(g=72\,859\).  Hence the exact
remaining interval in this **rank-at-most-seven pure fixed-\(G\) lane** is

\[
\boxed{72\,860\le g\le217\,542,}
\tag{5.5}
\]

containing 144,683 integer values.

This is not a statement about unrestricted-rank ordinary RS lists.  Rank
eight and above are outside Corollary 5.1.

The fixed-\(G\) universal embedding predecessor shows why (5.5) is a real
terminal: on this slice the received word can be an arbitrary nonzero-valued
ordinary RS received table.  Thus another locator-variation argument cannot
close (5.5).

## 6. Fixed-\(H\) divisibility fibers

Fix a monic divisor \(H\mid L_0\), let

\[
h=\deg H=g-\delta,
\tag{6.1}
\]

and consider

\[
\mathcal X_H=
\{f\in\mathcal W:H\mid Y-f\}.
\tag{6.2}
\]

### Proposition 6.1

If \(h\ge d\), then \(\mathcal X_H\) is empty or a singleton.  When it is
nonempty,

\[
f=\operatorname{rem}_H(Y)
\tag{6.3}
\]

and the remainder has degree \(<d\).

If \(h<d\) and \(f_0\in\mathcal X_H\), then

\[
\mathcal X_H
=
f_0+
\bigl(\mathcal W\cap H\mathbb F[X]_{<d-h}\bigr).
\tag{6.4}
\]

Consequently

\[
\dim_{\rm aff}\mathcal X_H
\le\min(7,d-h)
=\min(7,\delta-w).
\tag{6.5}
\]

### Proof

For \(f,f'\in\mathcal X_H\),

\[
H\mid f-f'.
\tag{6.6}
\]

If \(h\ge d\), the nonzero polynomial \(f-f'\) cannot be both divisible by
\(H\) and have degree \(<d\).  This proves uniqueness.  Reducing
\(Y-f\) modulo \(H\) proves (6.3), with the explicit warning that the
remainder may have degree at least \(d\), in which case the fiber is empty.

If \(h<d\), every difference is \(Ha\) with \(\deg a<d-h\), and the converse
is immediate after intersecting with \(\mathcal W\).  Multiplication by
\(H\) is injective, giving (6.5).

Since \(h\ge d\) is equivalent to \(\delta\le w\), the complete moderate
effective-deficit range has fixed-\(H\) uniqueness.  The first six deep
layers

\[
\delta=w+1,\ldots,w+6
\tag{6.7}
\]

force fixed-\(H\) affine rank at most \(1,\ldots,6\); from
\(\delta\ge w+7\), rank seven can survive.

The exact source fiber also requires

\[
\gcd(L_0,Y-f)=H
\tag{6.8}
\]

and the planted-gcd, lcm, degree, and shallow gates.  It is only a subset of
(6.4); it is not asserted to be affine.  Fixed-\(H\) uniqueness is not a
global count because the number of possible \(H\) remains uncontrolled.

## 7. Exact endpoint scalar route cut

At

\[
g=354\,972,
\tag{7.1}
\]

put

\[
h_0=H_0,\qquad
h_j=H_j-H_{j-1}\ (1\le j\le15\,186),
\qquad
h_{15\,187}=L-H_{15\,186}.
\tag{7.2}
\]

Set

\[
s=0,\qquad q=\delta=j
\tag{7.3}
\]

on row \(j\).  This produces a nonnegative exact integer marginal with:

```text
rows                              15,188
H_0                            3,268,160
H_15,185                      15,772,893
H_15,186                      15,774,749
H_15,187                      15,776,606
final bucket                       1,184
closure upper                       1,183
histogram SHA-256
7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0
```

Its exact moments are

\[
\sum_j jh_j=122\,692\,619\,370,
\tag{7.4}
\]

\[
\sum_j j^2h_j=1\,411\,089\,367\,885\,678,
\tag{7.5}
\]

\[
g\sum_j jh_j-\sum_jj^2h_j
=42\,141\,355\,115\,121\,962.
\tag{7.6}
\]

Every predecessor \(C_Q\) head is respected.  The five displayed scalar
resource utilizations, in parts per billion, are:

| resource | utilization |
|---|---:|
| first pivot | 69,379,632 |
| colored \(E\) | 92,411,130 |
| colored \(S\) | 5,721,454 |
| cross block | 39,674,193 |
| affine line | 91,623,946 |

All are strictly below \(10^9\).

The predecessor harmonic construction has

\[
q_6=222\,004,\qquad
d_6=1\,270\,586,\qquad
e=65\,515,
\tag{7.7}
\]

and admits every integer

\[
10\,411\,669\le x\le10\,411\,790.
\tag{7.8}
\]

At the lower endpoint, greedy transport couples the \(q=\delta\) rows to
the two mismatch classes \(b=0,e\).  Its column totals are

\[
(10\,411\,669,\ 5\,364\,264),
\tag{7.9}
\]

its unique split row is

\[
(q,\ b=0,\ b=e)=(11\,539,\ 202,\ 946),
\tag{7.10}
\]

and its canonical hash is

```text
c3b09d3958cd5b6ebc4c78c937e3f86e5a5d95d632c3be7db3c136efbde6bb79
```

The active placement margins are 277,918 and 572,181.

This proves that the declared cumulative, scalar, and harmonic **marginal
relaxation** does not close the endpoint.  It does not construct one
rank-six hyperplane support, one received word, a source family, or exact
full gcds.

## 8. The remaining locator geometry

At the endpoint,

\[
d=g-w=287\,525=140\cdot2048+805.
\tag{8.1}
\]

The inherited effective-\(\delta\) interpretation of the predecessor
\(C_Q\) frontier forces 1,039 members with

\[
\delta\ge2\,464,\qquad
h\le352\,508=172\cdot2048+252.
\tag{8.2}
\]

The new \(H_Q\) frontier forces 1,184 members with

\[
\delta\ge15\,187,\qquad
h\le339\,785=165\cdot2048+1\,865.
\tag{8.3}
\]

Both thresholds are below \(w\), but the forced tails extend beyond \(w\).
On the moderate portions

\[
2\,464\le\delta\le w
\qquad\text{and}\qquad
15\,187\le\delta\le w,
\tag{8.4}
\]

fixed-\(H\) uniqueness applies.  Members with \(\delta>w\) instead lie in
the deep affine divisibility fibers of Proposition 6.1.  Thus the residual
splits disjointly into a moderate cross-\(H\) branch and a deep
fixed-\(H\)/mixed-\(H\) branch.

For a monic degree-\(c\) fold \(\phi\), with \(c=2048\), the integrated
free-module identity is

\[
\mathbb F[X]
=\bigoplus_{a=0}^{c-1}X^a\mathbb F[\phi].
\tag{8.5}
\]

If \(e=c\kappa+r\), \(0\le r<c\), then the degree filtration is

\[
\mathbb F[X]_{<e}
\cong
\mathbb F[T]_{\le\kappa}^{\,r}
\oplus
\mathbb F[T]_{\le\kappa-1}^{\,c-r}.
\tag{8.6}
\]

This is exact channel arithmetic; it is not a claim that the filtered
slice is an \(\mathbb F[T]\)-submodule.

For (8.2),

\[
h-d=64\,983=31\cdot2048+1\,495.
\tag{8.7}
\]

For (8.3),

\[
h-d=52\,260=25\cdot2048+1\,060.
\tag{8.8}
\]

Thus a useful successor must couple many positional channels, not merely
repeat one 16-column or fixed-remainder calculation.

## 9. Domain-alignment route cut

The master-denominator theorem is uniform over arbitrary boundary locators
\(A_0,L_0\) of degrees \(a,R\).  Boundary cardinalities alone do not force
complete folded fibers.

Partition the \(n\) evaluation points into \(65\,536\) blocks of size 32.
There is an exact boundary layout with

\[
|A_0\cap B|=
\begin{cases}
18,&1\,911\text{ blocks},\\
17,&63\,625\text{ blocks},
\end{cases}
\tag{9.1}
\]

and hence

\[
|L_0\cap B|=
\begin{cases}
14,&1\,911\text{ blocks},\\
15,&63\,625\text{ blocks}.
\end{cases}
\tag{9.2}
\]

An \(H\)-support of size 352,508 can be interlaced with occupancy 6 in
24,828 blocks and 5 in the rest.  It fits inside every \(L_0\)-block and
contains no complete block.

Likewise, partition into 1,024 blocks of size 2,048.  One may take \(A_0\)
occupancy 1,090 in 887 blocks and 1,089 in 137 blocks, so \(L_0\) has
occupancy 958 and 959 respectively.  The same \(H\)-support can have
occupancy 345 in 252 blocks and 344 in the rest.  Again it fits in \(L_0\)
and contains no complete block.

These are exact support layouts and valid squarefree boundary locators.
They show that degree and cardinality hypotheses do not imply a
complete-fiber adapter.  They are **not** claimed to satisfy the locator
prefix, common-rank, or full-gcd source equations.

The non-integrated upstream PR #1073, at checked head
`c2d901ebe405d11330d07777ec8926a733c81829`, proves the sharp local cap
3,432 only after fixing:

- the pinned \((u,v)=(0,1)\) quotient profile;
- one canonical \(T_{32}\) remainder; and
- one depth-32 locator-prefix target.

It proves no source adapter from arbitrary \(H\mid L_0\), no
cross-remainder or cross-cofactor aggregation, and no uniform control of the
arbitrary boundary profile and unit \(V\).  Therefore #1073 is neither an
owner nor a dependency of this packet.  Importing its cap without those
keys would be a quantifier error.

## 10. Frozen remaining theorem

The combined live terminal is

```text
CROSS_COFACTOR_INTERLACED_H_AND_DEEP_FIBER_INCIDENCE
```

A closing rank-seven theorem must take as input one
\(\dim\mathcal W\le7\) space, arbitrary split \(P\mid A_0\), arbitrary unit
\(V\bmod L_0\), and the exact locators

\[
H_i=\gcd(L_0,Y-f_i),
\qquad
Q_i=\gcd(P,f_i),
\tag{10.1}
\]

while respecting every cumulative \(C_Q\) and \(H_Q\) head.  It must then
do one of the following:

1. pay the combined effective-deficit tail uniformly;
2. prove a source-compatible adapter to an already-paid invariant quotient
   owner; or
3. emit an explicit source-compatible primitive family.

The theorem must retain both pieces of the disjoint split from Section 8:
moderate cross-\(H\)/cross-cofactor incidence and deep fixed-\(H\) or
mixed-\(H\) divisibility fibers.

The pure full-\(G\) subterminal is now narrower and exact:

\[
\text{rank-at-most-seven deterministic ordinary-RS list bound for }
72\,860\le g\le217\,542.
\tag{10.2}
\]

Another scalar rank calculation, Johnson moment, fixed-\(H\) uniqueness
argument, or fixed canonical remainder cannot close the remaining mixed
family.

## 11. Proof audit

### Statement audited

The implication from the exact master-denominator family to the
nowhere-zero one-pivot cap, its pure full-\(G\) corollary, and the
fixed-\(H\) divisibility-fiber dichotomy.

### Dependencies

- **PROVEN by sealed predecessors:** master-denominator equivalence,
  rank preservation, exact \(H_i\), nonvanishing of \(P/V\) on \(E_0\),
  the recursive affine-span compiler, the low fixed-\(G\) Johnson and
  endpoint payments, and the fixed-\(G\) universal RS embedding.
- **PROVED here:** Theorem 2.1, the effective-deficit specialization,
  Corollary 5.1, and Proposition 6.1.
- **VERIFIED EXACTLY:** every all-\(g\) frontier cell, endpoint histogram,
  scalar inequality, harmonic interval, transport marginal, module degree,
  and balanced support layout.
- **TOY CONTROL ONLY:** the independent Sage fixed-\(H\) fibers over
  \(\mathbb F_{31}\).
- **UNPROVEN:** the moderate cross-\(H\)/cross-cofactor and deep-fiber
  incidence theorem, mixed-\(G\) rank-seven closure, ranks at least eight,
  and the complete row.

### Parameter dependence

All numerical statements are exact at (1.1)--(1.2).  There is no
asymptotic constant and no hidden dependence on \(T,Y,L_{\bar I},\lambda\),
\(I\), or a dyadic level.

### Layer-cake / dyadic summability

Not applicable.

### Moment / Markov / Chebyshev

No probabilistic moment, Markov, or Chebyshev inequality is used.
“Chebyshev” in the surrounding project refers to a polynomial fold.

### Edge cases and notation

- The outer and inner floors in (2.4) cannot be merged.
- The empty-list case \(m>N-z\) is handled before the double count.
- The \(k=0\) case is separate.
- Negative \(Q\) is only an effective-deficit head.
- At \(\delta=w\), the fixed-\(H\) fiber is still empty or a singleton.
- At \(h>d\), \(\operatorname{rem}_H(Y)\) need not have degree \(<d\).
- The affine object in the deep branch is the divisibility fiber, not
  necessarily the exact-gcd fiber.
- “Rank” is zero-anchored linear rank.

### Verdict

**GREEN locally / YELLOW globally.**  Three fresh independent audits found
the one-pivot theorem, endpoint relaxation, and packet scope sound with the
edge cases stated above.  The local fixed-\(G\) payment is bankable.  No
global row proof or ledger movement is authorized.

### Remaining risks

- The endpoint marginal primal may fail to lift to a source family; that is
  exactly why it is a route cut rather than a counterexample.
- The remaining pure fixed-\(G\) interval contains an arbitrary
  deterministic rank-at-most-seven ordinary-RS obstruction.
- Fixed-\(H\) uniqueness does not control the number of locators.
- A folded-fiber theorem must first prove source/domain compatibility.
- Rank at least eight requires a separate planted-zero incidence theorem.

### Maximal next action

Attack one exhaustive source-bound dichotomy over the combined \(C_Q/H_Q\)
frontier:

\[
\text{many complete compatible fibers}
\quad\text{or}\quad
\text{interlaced cross-cofactor/deep-fiber incidence cap}.
\]

The first branch must route through a proved adapter to an existing quotient
owner.  The second must bound all varying \(H\), cofactors, remainders, and
targets together.  A primitive component must remain explicitly unpaid
rather than being forced into an owner.
