# Exact-\(q\) Five-Degree Split-Scroll Target

## 1. Purpose

This is the remaining low-excess theorem after the source-fiber reduction
and exact-\(q\) carrier-incidence closure.

The only surviving kernel splitting degrees are

\[
\boxed{a\in\{12,13,14,15,16\}.}
\]

A proof of this target closes the low-excess universal-kernel branch. The
general-excess source-zero descent for \(\delta\ge e\) would still remain.

## 2. Fixed data

\[
\begin{aligned}
s&=202{,}416,\\
e&=134{,}944,\\
c&=67{,}472,\\
J&=981{,}105,\\
M&=69.
\end{aligned}
\]

Assume

\[
c\le\delta<e,
\qquad
N=s+\delta.
\]

Then

\[
\boxed{q=\lfloor N/e\rfloor=2.}
\]

Let

\[
\mathcal K\simeq\mathcal O(-a),
\qquad
m=\dim W\le9.
\]

The exact inherited bounds are

\[
a\le2(m-1)\le16,
\]

\[
D_{\rm exc}\le2(m-1)-a\le16-a,
\]

and

\[
\boxed{R_{\rm reg}\ge53+a.}
\]

## 3. Source-fiber normal form

The primitive source scalar has exactly \(a\) simple projective roots,
equal to the source-map values. Write

\[
\Sigma=\bigsqcup_{j=1}^a\Sigma_j,
\qquad
n_j=|\Sigma_j|.
\]

With \(L_j\) the parameter linear form at the \(j\)-th value,

\[
P(t,X)
=
\sum_{j=1}^a
Q_j(X)\frac{\lambda(t)}{L_j(t)}.
\]

Index the unique source value at parameter infinity by \(a\). Then

\[
Q_j
=
\Lambda_{\Sigma\setminus\Sigma_j}R_j,
\]

with

\[
\deg R_j\le\delta-e+n_j-1
\quad(j<a),
\]

and

\[
\deg R_a\le\delta-e+n_a.
\]

## 4. Persistent carrier core

Let

\[
C_0=\{x\in U_0:P(t,x)\equiv0\},
\qquad
g=|C_0|,
\qquad
h=\delta-g.
\]

Every \(R_j\) is divisible by \(\Lambda_{C_0}\). After writing

\[
R_j=\Lambda_{C_0}\widetilde R_j,
\]

the exact residual budget is

\[
\boxed{
\sum_{j=1}^a\deg\widetilde R_j
\le
s-a(e-h)-(a-1).
}
\tag{4.1}
\]

In particular,

\[
\boxed{
h\ge
e-\left\lfloor\frac{s-(a-1)}a\right\rfloor.
}
\tag{4.2}
\]

## 5. Fixed-domain split records

For each regular selected parameter \(t_i\),

\[
p_i(X)=\frac{P(t_i,X)}{\lambda(t_i)}
\]

is monic, squarefree, and split over one fixed carrier \(U_0\). After
removing \(\Lambda_{C_0}\), each locator has degree

\[
D=c+h,
\]

and the available carrier has size

\[
J+D.
\]

For distinct regular records,

\[
\deg\gcd(p_i/\Lambda_{C_0},p_j/\Lambda_{C_0})\le h.
\]

Every nonpersistent carrier coordinate occurs in at most \(a-1\) regular
locators.

## 6. Exact surviving windows

\[
\begin{array}{c|c|c|c|c}
a&D_{\rm exc}\text{ cap}&R_{\rm reg}\text{ floor}&h_{\min}&h_{\max}\\ \hline
12&4&65&118{,}077&132{,}382\\
13&3&66&119{,}375&134{,}943\\
14&2&67&120{,}487&134{,}943\\
15&1&68&121{,}451&134{,}943\\
16&0&69&122{,}294&134{,}943.
\end{array}
\]

The upper bounds come from

\[
54(c+h)\le(a-1)J
\]

and \(h<e\).

## 7. Target theorem

> **Exact-\(q\) five-degree split-scroll cap.**
> For every \(a\in\{12,\ldots,16\}\), no normalized low-excess packet
> satisfying Sections 2--6 contains \(53+a\) regular split
> specializations.

Equivalently, prove

\[
\#\{\text{regular specializations}\}\le52+a.
\]

Then

\[
(16-a)+(52+a)=68
\]

bounds the total selected parameters, including exceptional fibers.

A valid alternative is a canonical already-paid semantic cell rooted at one
of the same regular selected records.

## 8. Useful structure

The five cases are close to maximal regularity:

* \(a=16\) has no exceptional parameters;
* \(a=15\) has at most one;
* \(a=14\) has at most two;
* the parameter degree is only \(a-1\le15\);
* the source-fiber residual budget is exact and monicity-refined;
* the locator coefficient space still has dimension at most 16 and
  one-step \(T\)-expansion at most 17; and
* all records split on the same deployed KoalaBear carrier.

These constraints should be used together. First and pair-incidence moments
alone admit all five windows.

The regular coordinates are now classified more precisely in
`regular_grs_mds_deficit_reduction.md`. The locator coefficient-row space is
exactly a weighted \(\operatorname{GRS}_a\) code, and its one-step
parameter expansion has dimension exactly \(a+1\). If

\[
D=c+h,\qquad n=J+D,
\]

and \(R\) regular records are retained, the carrier-row MDS deficits satisfy

\[
\boxed{
\sum_x\bigl((a-1)-m_x\bigr)
=(a-1)J-(R-a+1)D.
}
\]

For \(a=12\), this forces at least \(394{,}145\) minimum-weight rows already
at \(R=65\), and at least \(1{,}136{,}341\) at \(R=69\). The \(R=69\)
branch is restricted further to

\[
118{,}077\le h\le118{,}599.
\]

In that all-regular branch, the total post-core source-fiber multiplier
degree is at most \(6{,}265\); at the first surviving endpoint it is at most
one. At that endpoint, eleven residual source-fiber multipliers are
constant and only one can be linear.

This exact GRS stability is useful structure, but it is not a contradiction
without the source-fiber divisor and fixed-domain splitting constraints.

## 9. Promising routes

1. **Small-expansion classification.** Combine the exact locator Kronecker
   decomposition with \(a\le16\) and the source-fiber divisor. The \(a=16\)
   case is particularly rigid because every selected coordinate is regular.
2. **Fixed-domain Schur product.** The weighted GRS block is now proved on
   all regular coordinates. Use its Schur products together with the
   fixed-domain split columns and source-fiber coefficient divisors to force
   an excessive common factor or an existing semantic owner.
3. **Monicity/Wronskian minors.** Use the one lost leading coefficient at
   each finite source value to build a nonzero minor of parameter degree
   below the number of regular specializations.
4. **Near-MDS row support.** Use the exact MDS-deficit identity and its
   forced minimum-weight rows. The first concrete subtarget is the
   selected fixed-domain GRS-vertex lemma in
   `regular_grs_mds_deficit_reduction.md`.
5. **Complement-locator descent.** Interpolate the fixed-carrier
   complementary locators. The proved identity in
   `complement_locator_interpolation_descent.md` factors the divisibility
   error as
   \[
   H_T(t)\Lambda_\Sigma(X)S(t,X),
   \qquad
   \deg_tS\le a-2.
   \]
   On every minimum-weight carrier row, this is the exact
   degree-\((a-2)\) complementary defect after all selected nonincidences
   are removed. The associated descended companion \(C\) has an exact
   resultant budget
   \[
   \deg_X\operatorname{Res}_t(\overline P,C)-RD
   \le
   \Delta_R+\mathcal B_a(h).
   \]
   The stronger theorem in `homogeneous_resultant_factorization.md`
   computes this resultant exactly as
   \[
   \zeta R_{\mathcal U}^{a-1}\prod_j\widetilde R_j.
   \]
   It is nonzero and contains no roots beyond the carrier and actual
   residual source multipliers. Hence the resultant route is closed. The
   focused subtarget is to classify the degree-\((a-2)\) factors
   \(S(t,x)\) before taking the resultant.
6. **Same-record owner adapter.** Convert a forced Kronecker or source-fiber
   block into an already enabled owner without replacing the selected
   record.
7. **Minimum-window birational rigidity.** The theorem in
   `minimum_window_coefficient_curve_birationality.md` proves that the
   source-coefficient curve is birational at the lower endpoint of every
   surviving window. Low-degree-cover and rational-normal-curve
   explanations are therefore unavailable there. Use the endpoint source
   divisors directly on the resulting degree-\(D\) curve.
8. **Source-partition Cremona descent.** The exact transformation in
   `source_partition_cremona_descent.md` replaces the minimum-window
   degree-\(D\) coefficient curve by a birational curve of degree at most
   \(n_0+\mathcal B_a(h_{\min})\), while converting each selected locator
   into a degree-\((a-1)\) hypersurface with the same owner incidence.
   Prove rigidity for this lower-degree model.
9. **Reciprocal-Cauchy separation.** The transformed selected vertices
   have the exact complementary-product coordinates in
   `reciprocal_cauchy_separator_target.md`. Prove that degree
   \(R-a+2\) forms through those vertices have no additional base locus.
   This would combine with Bézout to remove
   \[
   a=12,\quad R=69,\quad
   118{,}077\le h\le118{,}316.
   \]
   Degree-\((R-a+1)\) unisolvence is false in finite generic tests, so it
   must not be used as a shortcut.
10. **KoalaBear postcritical interpolation.** The weaker target in
    `postcritical_reciprocal_cauchy_interpolation_target.md` asks for
    full interpolation in the actual KoalaBear field and packet in degree
    \(R-a+2\), one degree after the false critical unisolvence claim. It
    implies separation in degree
    \(R-a+3\). For
    \[
    a=12,\quad R=69,
    \]
    it would remove
    \[
    118{,}077\le h\le118{,}283,
    \]
    leaving \(316\) values through \(h=118{,}599\). The all-fields
    version is false: \(\mathbf F_{13}\), \((a,R)=(4,8)\) has 273
    exceptional partitions among 6,435, of ranks 54 and 55 rather than
    56. Different exact failures occur in characteristics 17, 19, and 23,
    so pure interpolation is not the preferred universal route.
    Every known failure is supported on coincident block lines and prints
    the planted identity
    \(P_B-cP_C=(1-c)A_\Sigma\). The preferred target is therefore
    same-record semantic-or-interpolation after paying that branch.
    The complete relation-space computation, rather than only the defect
    count, shows that all known kernels are generated by these line
    relations. Distinct full blocks on one line are pairwise disjoint, and
    every additional vertex is a near-full fiber consuming \(a-1\) new
    selected roots. Thus the canonical-line capacity is
    \[
    a\left\lfloor\frac Ra\right\rfloor
    +
    \mathbf1_{\{R\bmod a=a-1\}}.
    \]
    At \(a=12,R=69\), this is exactly 60 vertices, while a
    postcritical relation on a line needs at least 61. Hence the known
    block-line mechanism is impossible in the hardest all-regular branch;
    any failure there is necessarily non-block-line. The same is true for
    \(a=14,R=67,68,69\).
    The exact critical-kernel and Cremona-star hypercohomology
    reformulations are in
    `cremona_star_hypercohomology_reduction.md` and
    `reciprocal_cauchy_block_line_emission.md`.

## 10. Invalid shortcuts

The following remain insufficient:

* ordinary first or pair-incidence counting;
* the generic-kernel-free cap \(63\);
* formal-root GM--MDS independence without a fixed-domain minor;
* discarding exceptional fibers;
* treating a source-fiber coefficient as an owner;
* assuming one Kronecker block or disjoint block supports; or
* forgetting the general-excess descent after closing this theorem.

## 11. Consequence and nonclaims

This target plus the proved exact-\(q\) reductions closes the low-excess
rank-one branch. It does not by itself prove:

* the recursive \(\delta\ge e\) branch;
* the full universal-kernel cap \(68\);
* the equality-wall payment; or
* any later KoalaBear slack.
