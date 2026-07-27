---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: A normalized-label class large enough to violate the Q=147595 closing cap must have z=0, full label multiplicity c=sigma=282544, affine rank six, and at least 2157929 zero-excess proper-G members. Seven affinely independent members from that proper-G portion form an actual source basis. Exact cofactor intersections then force one pair with deg gcd(G_i,G_j)>=228652, deg gcd(H_i,H_j)>=282544, q_i+q_j<=131300, and a sign-consistent reduced determinant factorization. A faithful GF(31) source family disproves a one-slice aggregation bound and every universal aggregate multiplier strictly below the exact ratio 60166/5505 under the listed structural gates.
architecture: M31_RANK7_PROPER_G_ZERO_EXCESS_INCIDENCE_ROUTE_CUT_V1
atom_or_cell: Source-bound rank-seven dangerous-class reduction and varying-proper-G incidence terminal; no v4 atom value and no signed Xi_46 payment.
quantifier: Every counted normalized-label class in the unique k=4981 residual whose size is at least 9806394, and every seven-member affinely independent subset of its zero-excess proper-G portion.
projection_and_unit: Distinct LIST codewords per received word. Positive-excess, full-P, and proper-G portions are disjoint before their caps are added.
claimed_bound: A violating class has at least 2157929 zero-excess proper-G members. Every proper fixed-G slice has at most 119177 members, so at least 19 proper locators are occupied. Some actual proper-G basis pair has master-locator overlap at least 228652. The missing aggregate upper bound is exactly 2157928.
status: PROVED LOCAL DANGEROUS-CLASS REDUCTION / PROPER-G ZERO-EXCESS ROUTE CUT / Q=147595 OPEN / ROW OPEN
impact: SHARPENED SOURCE-SPECIFIC PRIMITIVE TERMINAL / ONE-SLICE AND FACTOR-BELOW-60166/5505 AGGREGATION ROUTES FALSIFIED / NO LEDGER MOVEMENT
falsifier: A class of size 9806394 with z>0, c<sigma, or affine rank at most five; an incorrect excess-one recurrence value; a zero/full/proper partition overlap; a proper fixed-G slice exceeding the exact q-dependent cap; failure of C_ij to divide a_i-a_j; a seven-basis complement-pair intersection above 4980; a forced overlap below 228652; a sign-inconsistent determinant; failure of the GF(31) full-gcd/common-V census; or any claim that the toy fixture is an M31 counterexample.
replay: Standard-library Python normal and optimized checks, phase-specific hostile mutations, an independent exact-integer replay, Sage exhaustive GF(31) source census, bounded strict JSON, a top-level envelope schema with verifier-closed nested semantics, trusted source identities before candidate-selected I/O, capped streaming regular-file source hashes, and sealed predecessor payload pins.
---

# M31 rank-seven proper-\(G\) zero-excess incidence route cut

## 1. Result and scope

The source-basis predecessor leaves one local residual at

\[
Q=147\,595,\qquad
\sigma=282\,544,\qquad
k=d-\sigma=4\,981.
\tag{1.1}
\]

One normalized-label class is currently bounded by

\[
9\,806\,438,
\tag{1.2}
\]

while the refined outer compiler closes when that bound is at most

\[
9\,806\,393.
\tag{1.3}
\]

This packet proves that any actual class \(M\) violating (1.3) must
terminate in the following source-compatible component:

```text
PROPER_G_ZERO_EXCESS_CROSS_COFACTOR_INTERLACED_INCIDENCE
```

More precisely, such a class has at least \(2\,157\,929\) zero-excess
members with \(G<P\).  Seven affinely independent members of that portion
form an actual basis of the rank-seven master span.  For some pair in this
basis,

\[
\boxed{
\deg\gcd(G_i,G_j)\ge228\,652,\qquad
\deg\gcd(H_i,H_j)\ge282\,544,\qquad
q_i+q_j\le131\,300.
}
\tag{1.4}
\]

The exact cross-cofactor equations are printed in Section 5.

No current owner sums the varying proper-\(G\) slices.  An exhaustive
small-field source family in Section 7 disproves both a one-slice
aggregation bound and every universal aggregate multiplier strictly below
the exact ratio \(60\,166/5\,505\) under the listed structural gates.  It
does not rule out a stronger field-uniform theorem.  Therefore this is a
strict route cut, not payment of \(Q=147\,595\), a v4 atom, or the M31
LIST row.

## 2. Fixed deployed parameters

Throughout,

\[
\begin{aligned}
p&=2^{31}-1,& n&=2^{21},& K&=2^{20},\\
a&=1\,116\,023,& R&=981\,129,& w&=67\,447,\\
g&=354\,972,& d&=g-w=287\,525,\\
\sigma&=282\,544,& k&=d-\sigma=4\,981.
\end{aligned}
\tag{2.1}
\]

Use the sealed source normalization

\[
P=\operatorname{lcm}_fG_f,\qquad
Q_f=P/G_f,\qquad
f=Q_fb_f,
\tag{2.2}
\]

where \(P,G_f\) are split and squarefree,
\(\gcd(b_f,G_f)=1\), and \(\deg P=g\).  On
\(E_0=Z(L_0)\), the received table \(u=P/V\) is nowhere zero and

\[
H_f=\gcd(L_0,Y-f),\qquad
\deg H_f=\deg G_f+s_f.
\tag{2.3}
\]

Fix a complete projective evaluation-line class \(S\subset E_0\) of size
\(\sigma\), a counted normalized label \(\beta\ne0\), and its actual class.
Every member has

\[
f=f_*+L_Sa_f,\qquad \deg a_f<k.
\tag{2.4}
\]

Let \(c\) be the multiplicity of \(\beta\) on \(S\).  Each class member
agrees with \(u\) at exactly \(c\) points of \(S\).

## 3. What a violating class forces

Assume

\[
M\ge9\,806\,394.
\tag{3.1}
\]

### 3.1 Zero common-direction zeros and actual affine rank six

The predecessor proves that a positive common-direction zero gives cap

\[
444\,522.
\tag{3.2}
\]

Hence (3.1) forces \(z=0\).  The unconditional affine-span cap for
direction rank at most five is

\[
A_5(w)=
\left\lfloor
\frac{\binom{K+5}{5}}{\binom{w+5}{5}}
\right\rfloor
=908\,021.
\tag{3.3}
\]

Thus the actual class has affine direction rank exactly six.

### 3.2 Full normalized-label multiplicity

On the combined domain, a member has agreement excess

\[
(\sigma-c)+s_f.
\tag{3.4}
\]

If \(c<\sigma\), every member has at least one extra agreement.  At excess
\(w+1=67\,448\), the exact no-common-zero recurrence has rank-five child

\[
C_5(4\,980;67\,448)=444\,522
\tag{3.5}
\]

and rank-six numerator

\[
1\,053\,557\cdot444\,522
=468\,329\,264\,754
=6\,466\,046\cdot72\,429+19\,020.
\tag{3.6}
\]

The rank-at-most-five fallback is only

\[
A_5(w+1)=907\,953.
\tag{3.7}
\]

Consequently every excess-one affine subfamily of direction rank at most
six has size at most

\[
6\,466\,046.
\tag{3.8}
\]

Equation (3.1) therefore forces

\[
\boxed{c=\sigma.}
\tag{3.9}
\]

In particular every member agrees on all points of \(S\), so

\[
S\subset Z(H_f)
\tag{3.10}
\]

for every member of the class.

### 3.3 Disjoint mass partition

Split the actual class into:

1. members with \(s_f\ge1\);
2. members with \(s_f=0\) and \(G_f=P\);
3. members with \(s_f=0\) and \(G_f<P\).

These portions are disjoint.  By (3.8), the first has size at most

\[
6\,466\,046.
\tag{3.11}
\]

For the full-\(P\), zero-excess portion, intersecting the nonzero label
gives affine direction rank at most six.  The fixed-\(P\) affine-span
theorem gives

\[
\begin{aligned}
B^{\mathrm{full}}_6
&=
\left\lfloor
\frac{\binom{R-g+w+6}{6}}{\binom{w+6}{6}}
\right\rfloor\\
&=
\left\lfloor
\frac{\binom{693\,610}{6}}{\binom{67\,453}{6}}
\right\rfloor
=1\,182\,419.
\end{aligned}
\tag{3.12}
\]

The exact division remainder is

\[
86\,919\,124\,762\,661\,448\,764\,444\,630.
\tag{3.13}
\]

It follows from (3.1), (3.11), and (3.12) that the zero-excess proper-\(G\)
portion has size at least

\[
9\,806\,394-6\,466\,046-1\,182\,419
=\boxed{2\,157\,929}.
\tag{3.14}
\]

Conversely, the exact missing theorem

\[
\boxed{
\#\{f:s_f=0,\ G_f<P\}\le2\,157\,928
}
\tag{3.15}
\]

would close the class because

\[
6\,466\,046+1\,182\,419+2\,157\,928
=9\,806\,393.
\tag{3.16}
\]

## 4. One proper fixed-\(G\) slice

Put

\[
q=\deg(P/G).
\tag{4.1}
\]

The proper-slice rank-loss theorem gives linear rank at most six before
the label is fixed.  Since the slice meets the nonzero hyperplane
\(\lambda=\beta\), its affine direction rank is at most five.

If \(q\ge k\), two members in the same normalized-label slice would have a
nonzero difference divisible by the coprime product

\[
L_S(P/G),
\tag{4.2}
\]

whose degree is at least \(\sigma+k=d\).  This contradicts
\(\deg(f_i-f_j)<d\).  Hence the slice has at most one member.

For \(1\le q\le k-1=4\,980\), the ordinary fixed-\(G\) affine-span theorem
on \(E_0\) gives

\[
B_5(q)=
\left\lfloor
\frac{\binom{R-g+q+w+5}{5}}{\binom{w+5}{5}}
\right\rfloor.
\tag{4.3}
\]

This is increasing in \(q\), and

\[
B_5(4\,980)
=
\left\lfloor
\frac{\binom{698\,589}{5}}{\binom{67\,452}{5}}
\right\rfloor
=119\,177
\tag{4.4}
\]

with remainder

\[
892\,372\,184\,216\,353\,689\,387.
\tag{4.5}
\]

Thus every proper fixed-\(G\) slice in (3.14) has at most \(119\,177\)
members.  A violating class occupies at least

\[
\left\lceil\frac{2\,157\,929}{119\,177}\right\rceil
=19
\tag{4.6}
\]

distinct proper locators.  This does not pay the aggregate: nineteen
independent uses of the legal scalar cap permit

\[
19\cdot119\,177=2\,264\,363>2\,157\,928.
\tag{4.7}
\]

The missing input is a cross-\(G\) incidence theorem, not a sharper
single-slice calculation.

Because \(2\,157\,929>A_5(w)\), the proper-\(G\), zero-excess portion
itself has affine rank six.  Choose seven affinely independent actual
members from it.  Since their common label is nonzero, affine independence
implies linear independence: applying \(\lambda\) to a linear relation
shows that the sum of its coefficients is zero, after which affine
independence applies.  The seven members therefore form an actual basis of
the rank-seven master span \(\mathcal W\).

## 5. Exact seven-basis incidence theorem

For the chosen basis, the root sets satisfy

\[
Z(G_i)=Z(P)\setminus Z(Q_i),
\tag{5.0}
\]

and put

\[
C_{ij}=\frac{P}{\operatorname{lcm}(G_i,G_j)}.
\tag{5.1}
\]

Thus \(Z(C_{ij})=Z(Q_i)\cap Z(Q_j)\).

From (2.4),

\[
f_i-f_j=L_S(a_i-a_j).
\tag{5.2}
\]

If

\[
J_{ij}=\gcd(G_i,G_j),\qquad
G_i=J_{ij}A_i,\qquad G_j=J_{ij}A_j,
\tag{5.3}
\]

then \(\gcd(A_i,A_j)=1\) and

\[
Q_i=C_{ij}A_j,\qquad Q_j=C_{ij}A_i.
\tag{5.4}
\]

Equations (5.2)--(5.4), together with
\(\gcd(C_{ij},L_S)=1\), imply

\[
C_{ij}\mid a_i-a_j.
\tag{5.5}
\]

The difference is nonzero and has degree below \(k\), so

\[
\boxed{\deg C_{ij}\le k-1=4\,980}
\tag{5.6}
\]

for every pair.

For \(\alpha\in Z(P)\), let \(q_\alpha\) be the number of basis locators
missing \(\alpha\).  Exact-lcm coverage gives \(0\le q_\alpha\le6\).
Set

\[
\mathcal C
=\sum_{\alpha\in Z(P)}\binom{q_\alpha}{2}
=\sum_{i<j}\deg C_{ij}.
\tag{5.7}
\]

By (5.6),

\[
\mathcal C\le\binom72\,4\,980=104\,580.
\tag{5.8}
\]

For \(0\le q\le6\),

\[
q\le1+\binom q2.
\tag{5.9}
\]

Therefore the total number of missing incidences

\[
\mathcal Q:=\sum_\alpha q_\alpha=\sum_iq_i
\tag{5.10}
\]

satisfies

\[
\mathcal Q\le g+\mathcal C.
\tag{5.11}
\]

The sum of the 21 pairwise complement-union sizes is

\[
\sum_{i<j}\deg\operatorname{lcm}(Q_i,Q_j)
=6\mathcal Q-\mathcal C
\le6g+5\mathcal C
\le2\,652\,732.
\tag{5.12}
\]

Hence one pair has complement union at most

\[
\left\lfloor\frac{2\,652\,732}{21}\right\rfloor
=126\,320.
\tag{5.13}
\]

Taking complements inside \(Z(P)\) proves

\[
\boxed{
\deg J_{ij}
=\deg\gcd(G_i,G_j)
\ge354\,972-126\,320
=228\,652.
}
\tag{5.14}
\]

Equivalently,

\[
\sum_{i<j}\deg\gcd(G_i,G_j)
\ge4\,801\,680,
\tag{5.15}
\]

whose average is \(228\,651+\frac9{21}\).

## 6. Reduced determinant and common-\(H\) consequence

For the pair in (5.14), choose the sign convention

\[
a_i-a_j=-C_{ij}T_{ij}.
\tag{6.1}
\]

Then (5.2)--(5.4) give the sign-consistent identity

\[
\boxed{
A_ib_j-A_jb_i=L_ST_{ij},
\qquad
\deg T_{ij}\le4\,980-\deg C_{ij}.
}
\tag{6.2}
\]

The determinant in (6.2) is nonzero.  If it vanished, coprimality of
\(A_i,A_j\) would force \(A_i\mid b_i\) and \(A_j\mid b_j\).  The canonical
conditions \(\gcd(b_i,G_i)=\gcd(b_j,G_j)=1\) would then give
\(A_i=A_j=1\), and the two basis members would coincide.

Put

\[
K_{ij}=\gcd(H_i,H_j).
\tag{6.3}
\]

By (3.10),

\[
\deg K_{ij}\ge\sigma=282\,544.
\tag{6.4}
\]

At every root of \(K_{ij}\), the common-\(V\) equations imply

\[
A_ib_j-A_jb_i=0.
\tag{6.5}
\]

Since \(K_{ij}\) is split on \(E_0\), it divides the reduced determinant.
Writing \(m_i=\deg G_i\), its degree is at most

\[
m_i+m_j-\deg J_{ij}-w-1.
\tag{6.6}
\]

Thus

\[
m_i+m_j
\ge228\,652+282\,544+67\,448
=578\,644,
\tag{6.7}
\]

and therefore

\[
\boxed{q_i+q_j=2g-(m_i+m_j)\le131\,300.}
\tag{6.8}
\]

Equations (5.6), (5.14), (6.2), (6.4), and (6.8) are the complete proved
local terminal.  They do not bound the number or total mass of the other
occupied proper locators.

## 7. Sharpness and a source-compatible finite-field control

### 7.1 The support bound is sharp

At the level of seven root sets, take \(4\,980\) roots missing each of the
21 locator pairs.  This uses \(104\,580\) roots with \(q_\alpha=2\).
Let the remaining

\[
354\,972-104\,580=250\,392
\tag{7.1}
\]

roots miss one locator each, in counts

\[
35\,771,\ 35\,771,\ 35\,770,\ 35\,770,\ 35\,770,\ 35\,770,\ 35\,770.
\tag{7.2}
\]

Every complement-pair intersection is exactly \(4\,980\), while the
largest locator-pair overlap is exactly \(228\,652\).  Thus (5.14) cannot
be improved from the seven-set constraints alone.

This is an abstract support extremizer, not a polynomial source family.

### 7.2 Exact \(GF(31)\) source family

The Sage replay constructs a separate faithful small-field family.  Over
\(\mathbb F_{31}\), put

\[
\begin{aligned}
Z(P)&=\{0,\ldots,7\},&
Z(L)&=\{8,\ldots,30\},\\
S&=\{8\},&
w&=1,& d&=7,& k&=6,\\
Y&=P,& V&=1.
\end{aligned}
\tag{7.3}
\]

For every pair of root sets \(Z(G)\subset Z(P)\) and
\(S\subset Z(H)\subset Z(L)\) of the same size \(m\), subject to

\[
\sum_{\alpha\in Z(G)}\alpha
=
\sum_{\alpha\in Z(H)}\alpha
\pmod {31},
\tag{7.4}
\]

define

\[
b=G-H,\qquad Q=P/G,\qquad f=Qb=P-QH.
\tag{7.5}
\]

The coefficient condition (7.4) is exactly

\[
\deg b<m-w.
\tag{7.6}
\]

Direct polynomial gcd checks give

\[
\gcd(P,f)=Q,\qquad
\gcd(L,Y-f)=H,\qquad
\gcd(PL,Y-f)=QH,
\tag{7.7}
\]

as well as

\[
\gcd(G,b)=\gcd(b,H)=1.
\tag{7.8}
\]

Every member has \(s=0\), all agree with \(Y\) on \(S\), and the family
has exact linear rank seven and normalized-label affine direction rank
six.  In fact the span is all of \(\mathbb F_{31}[X]_{<7}\), while division
of the label kernel by \(X-8\) gives all of
\(\mathbb F_{31}[X]_{<6}\).  Thus \(z=0\), and \(S=\{8\}\) is a complete
singleton projective evaluation line.  Exhaustion gives

\[
\begin{array}{c|r}
\text{all members}&65\,671\\
\text{proper-}G\text{ members}&60\,166\\
\text{full-}P\text{ members}&5\,505\\
\text{occupied }G\text{ slices}&235\\
\text{largest fixed-}G\text{ slice}&5\,505.
\end{array}
\tag{7.9}
\]

The master lcm is restored, the common unit is literally \(V=1\), and
every pair of residual supports has intersection at most

\[
k-1=5.
\tag{7.10}
\]

In particular, varying proper-\(G\) mass is exactly \(60\,166\), whereas
the largest single fixed-\(G\) slice has size \(5\,505\).  The fixture
therefore disproves a one-slice aggregate bound and any universal
multiplicative aggregate factor strictly below
\[
\frac{60\,166}{5\,505}.
\tag{7.11}
\]

This is a rigorous finite-field obstruction at that exact factor, not a
proof that every parameter-free aggregation theorem fails.  It is not an
M31 counterexample and says nothing by itself about the numerical truth
of (3.15).  A deployed closure may use the M31 depth \(w=67\,447\), its
degree ratios, a stronger field-uniform consequence of the existing
gates, or a new global consequence of the reduced determinant incidence.

## 8. Exact remaining theorem and owner audit

The unresolved deployed statement is

\[
\sum_{\substack{G<P\\s=0}}|\mathcal I_G|
\le2\,157\,928.
\tag{8.1}
\]

A sufficient slice-aware form is

\[
119\,177\,N_{1\le q\le4\,980}
+N_{q\ge4\,981}
\le2\,157\,928,
\tag{8.2}
\]

where the second term counts members, because every fixed-\(G\) slice in
that range is a singleton.  Current hypotheses do not bound either the
number of occupied low-\(q\) slices or the total high-\(q\) occupancy.

No integrated owner supplies (8.1):

- fixed-\(G\) payment is not summable over varying locators;
- common-zero payment is excluded by \(z=0\);
- periodicity and invariant quotient descent require a declared uniform
  folding absent here;
- Johnson and the affine-span recurrence already supply the caps used
  above;
- pairwise CRT exactness yields (6.2) but no global occupancy bound.

TheoremSearch and an outside primary-source search were run only after
(8.1) was frozen.  Work on subspace designs, proximity gaps for folded or
random Reed--Solomon codes, and simultaneous Padé/minimal-approximant
bases does not directly cover this deterministic ordinary-RS,
source-factorized aggregate.  No literature theorem is used as a proof
dependency.

The next valid closure attack must use the **whole occupied-locator
incidence**, not another selected-pair relaxation.  It must either prove
(8.1), extract at least 45 recurrence units from the complete family,
route every component to chronology-valid owners with disjoint add-back,
or produce a deployed-parameter source family violating (8.1).

## 9. Ledger effect and nonclaims

The active v4 ledger remains

```text
U_paid    = 3730
U_Q       = null
U_list_int= null
U_ext     = null
U_new     = null
Xi_46     remains open
row       remains open
```

No official endpoint, v4 atom, signed charge, rank-at-least-eight branch,
or stable paper is changed.

## 10. Proof audit

### Statement audited

The implication from a hypothetical violating \(Q=147\,595\) label class
to the disjoint positive/full/proper mass partition, the exact
\(2\,157\,928\) missing cap, the seven-proper-member incidence theorem,
and the source-compatible small-field aggregation route cut.

### Files and sections read

- `m31_rank7_source_basis_private_root_overlap_dichotomy_v1.md`,
  Sections 2--7.
- `m31_rank7_combined_domain_fixed_mismatch_recurrence_v1.md`,
  Sections 2--5.
- `m31_rank7_combined_domain_affine_johnson_endpoint_v1.md`,
  Sections 2--4.
- `m31_rank7_shallow_master_denominator_cut_v1.md`, Theorems 2.1 and
  3.1.
- `m31_varying_g_affine_span_shortening_route_cut_v1.md`, Theorem 2.1.
- Current project instructions and workboard.

### Dependencies

- **PROVEN by sealed predecessors:** exact rank seven, split squarefree
  master normalization, no common zero on \(Z(P)\), nonzero complete-line
  labels, combined-domain agreement, exact rank-six full hyperplane,
  positive-common-zero payment, excess recurrence, fixed-\(G\) rank loss,
  and the \(Q=147\,595\) closing threshold.
- **PROVED here:** \(c=\sigma\) in a violating class; the disjoint
  positive/full/proper decomposition; exact proper mass threshold;
  sharpened proper fixed-slice cap \(119\,177\); nineteen-slice minimum;
  existence of an actual proper zero-excess basis; complement-intersection
  theorem; overlap \(228\,652\); common-\(H\), cofactor-sum, and reduced
  determinant consequences.
- **EXACT CERTIFIED COMPUTATION:** recurrence arrays, binomial divisions,
  incidence floors, abstract support extremizer, and exhaustive
  \(GF(31)\) polynomial/gcd census.
- **UNPROVEN:** (8.1), any owner for the terminal, \(Q=147\,595\), later
  heads, ranks at least eight, v4 ownership, and the global row.

### Parameter dependence

Sections 2--6 and 8 are finite exact statements at the deployed M31
parameters.  Section 7.1 is an abstract seven-set sharpness construction.
Section 7.2 is an exact toy-scale \(GF(31)\) counterfixture only.  There
are no asymptotic constants or hidden dependence on
\(T,Y,\mathcal L,\mathcal L_{\bar I},\lambda,I\); the displayed
\(\lambda\) dependence is the fixed normalized-label functional.

### Layer-cake / dyadic summability

Not applicable.

### Moment / Markov / Chebyshev

Not applicable.

### Edge cases / notation

The label \(\beta\ne0\) is essential for converting seven affinely
independent class members into a linear basis.  The \(q\ge k\) singleton
case must be separated before maximizing the fixed-\(G\) cap.  The
positive-excess, full-\(P\), and proper-\(G\) pieces are disjoint.
\(C_{ij}\) is coprime to \(L_S\) because \(Z(P)\cap E_0=\varnothing\).
Equation (6.1) fixes the determinant sign.  The \(GF(31)\) family is not
extrapolated to M31.

### Numerical evidence

All deployed endpoint values are exact integer computations supporting
proved finite implications.  The \(GF(31)\) census exactly falsifies a
one-slice bound and universal aggregate factors strictly below
\(60\,166/5\,505\); it is not evidence for or against the deployed
numerical cap without additional argument.

### Verdict

**GREEN** for the local dangerous-class reduction, \(228\,652\) incidence
theorem, and the exact one-slice/factor-below-\(60\,166/5\,505\) route cut.
**YELLOW / OPEN GAP** for (8.1).  Do not authorize global payment.

### Remaining risks

The recurrence import, disjoint mass partition, label-hyperplane rank
loss, and common-\(V\) reduced determinant are load-bearing.  The remaining
aggregate may depend essentially on the deployed prefix depth and cannot
be inferred from the toy family.
