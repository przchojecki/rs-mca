---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The surviving master-denominator family has exact span rank seven. Every counted normalized-label class is contained in the full affine hyperplane lambda(f)=beta, whose direction is the exact rank-six kernel of lambda. The label is nonzero and every common direction zero of this full hyperplane on the combined domain is a fixed mismatch. Factoring those zeros and padding at fresh non-common-zero field points makes the predecessor full-projective-line recurrence a uniform cap for every counted label. A sharper top-five outer compiler pays the complete cumulative effective-deficit head through Q=147594. At Q=147595 exactly one k=4981 residual survives, and lowering its recurrence cap by exactly 45 closes the compiler.
architecture: M31_RANK7_COMBINED_DOMAIN_FIXED_MISMATCH_RECURRENCE_V1
atom_or_cell: Source-bound rank-seven cumulative-deficit head and sharp recurrence route cut; no v4 atom value and no signed Xi_46 payment.
quantifier: Every surviving exact-rank-seven endpoint shallow master-denominator family, every complete nonzero E0 projective evaluation-line class, and every counted normalized-label class in that line; rank-at-most-six whole families are paid by the imported rank-six closure.
projection_and_unit: Distinct LIST codewords per received word. The outer compiler counts agreement pairs and divides once by g-Q.
claimed_bound: N_(delta<=147594)<=15775917<=15775932. At Q=147595 the certified compiler gives 15775993, and a 45-unit reduction of the unique k=4981 class cap closes that next head. No global row upper bound.
status: PROVED LOCAL Q=147594 HEAD / Q=147595 FORTY-FIVE-UNIT ROUTE CUT / GLOBAL ROW OPEN
impact: RANK_SEVEN_FRONTIER_ADVANCE / SHARP_ROUTE_CUT / NO_LEDGER_MOVEMENT
falsifier: Failure of the imported rank-at-most-six closure, failure of exact rank seven in the surviving branch, a counted zero normalized label, an incomplete projective line, failure of exact-lcm no-common-zero normalization on Z(P), a common direction zero of the full hyperplane that is an agreement, inability to choose the padding points, an independent recurrence or refined-outer mismatch, an endpoint above the shallow target, or promotion to a v4 atom or global row theorem.
replay: Standard-library Python normal and optimized checks, hostile mutations, an independently structured Python heap replay, Sage exact-integer and finite-field replay, strict JSON/schema/source hashes, and sealed predecessor payload pins.
---

# M31 rank-seven combined-domain fixed-mismatch recurrence

## 1. Result and scope

Use the endpoint parameters

\[
\begin{aligned}
p&=2^{31}-1,& n&=2^{21},&K&=2^{20},\\
a&=1\,116\,023,&R&=981\,129,&w&=67\,447,\\
g&=354\,972,&d&=287\,525,&L&=15\,775\,932.
\end{aligned}                                                     \tag{1.1}
\]

The combined-domain predecessor proved the cumulative rank-seven head
through \(Q=29\,554\).  A full-hyperplane source embedding and a refined
top-five outer compiler advance the complete cumulative head to

\[
\boxed{
N_{\delta\le147\,594}\le15\,775\,917=L-15.}                      \tag{1.2}
\]

The adjacent compiler value is

\[
N_{\delta\le147\,595}\le15\,775\,993=L+61.                       \tag{1.3}
\]

Exactly one residual line size survives (1.3), with combined-domain
dimension \(k=4\,981\).  Its certified cap is \(9\,806\,438\); replacing
that one value by \(9\,806\,393\) closes the head, while \(9\,806\,394\)
does not.

Equations (1.2)--(1.3) are local rank-seven statements.  They do not assign
a v4 first-match atom, pay signed \(\Xi_{46}\), treat rank at least eight,
or close the M31 LIST row.

## 2. Imported source normalization and rank dichotomy

Use the predecessor notation

\[
P=\operatorname{lcm}_iG_i,\qquad
Q_i=P/G_i,\qquad f_i=Q_ib_i,                                    \tag{2.1}
\]

\[
u=P/V\quad\hbox{on }E_0,\qquad
E_0\cap Z(P)=\varnothing.                                       \tag{2.2}
\]

The table \(u\) is nowhere zero on \(E_0\), and exact lcm normalization
gives

\[
\bigcap_{f\in\mathcal W}Z(f)\cap Z(P)=\varnothing,
\qquad
\mathcal W=\operatorname{span}\{f_i\}.                           \tag{2.3}
\]

Master normalization preserves the original codeword rank.  The imported
rank-six closure gives a whole-chart cap \(908\,116\), while a forbidden
family would contain \(15\,775\,933\) shallow members.  Thus the
rank-at-most-six branch is already paid, and the surviving branch has

\[
\dim\mathcal W=7.                                                \tag{2.4}
\]

Fix a complete projective evaluation-line class \(S\subset E_0\).  Thus
there is a nonzero \(\lambda\in\mathcal W^*\) and nonzero scalars \(t_x\)
such that

\[
\operatorname{ev}_x|_{\mathcal W}=t_x\lambda
\quad(x\in S),                                                   \tag{2.5}
\]

and every point of \(E_0\) whose nonzero evaluation is proportional to
\(\lambda\) lies in \(S\).

For a normalized-label class counted by the agreement-pair compiler, the
common label is

\[
\beta=\frac{u(x)}{t_x}\ne0.                                     \tag{2.6}
\]

The inequality is load-bearing.  A label with no coordinate has zero
agreement-pair weight and is not counted.

Choose an actual source member \(f_*\) in the class.  With

\[
L_S(X)=\prod_{x\in S}(X-x),\qquad k=d-|S|,
\]

every actual member has the unique form

\[
f=f_*+L_Sa_f,\qquad \deg a_f<k.                                 \tag{2.7}
\]

On the disjoint combined domain

\[
\Omega=(E_0\setminus S)\mathbin{\dot\cup} Z(P),                  \tag{2.8}
\]

the predecessor received table is

\[
y(x)=
\begin{cases}
(u(x)-f_*(x))/L_S(x),&x\in E_0\setminus S,\\
-f_*(x)/L_S(x),&x\in Z(P).
\end{cases}                                                       \tag{2.9}
\]

For every actual source member it proved

\[
|\Omega|=K+k,\qquad
\operatorname{agr}_{\Omega}(a_f,y)\ge k+w.                       \tag{2.10}
\]

## 3. Full-hyperplane fixed-mismatch lemma

### Lemma 3.1

For a counted label \(\beta\), let

\[
\mathcal H_{\lambda,\beta}
=\{f\in\mathcal W:\lambda(f)=\beta\}
=f_*+\ker\lambda.                                                \tag{3.1}
\]

After division by \(L_S\), the full hyperplane (3.1) is an affine family
of exact direction rank six and degree below \(k\).  It contains every
actual source member in the label class, and every common direction zero
on \(\Omega\) is a fixed mismatch with \(y\).

### Proof

Equation (2.4) and \(\lambda\ne0\) give
\(\dim\ker\lambda=6\).  Every \(f\in\mathcal H_{\lambda,\beta}\) agrees
with \(f_*\) on all of \(S\), so \(f-f_*\) is divisible by \(L_S\).
Division maps (3.1) injectively to a degree-\(<k\) affine family with
exact direction \(\ker\lambda/L_S\).  The actual source class is a subset
of its ordinary combined-domain list by (2.10).  Extra hyperplane members
need no \(G_i,Q_i\), or source factorization.

Let \(x\in E_0\setminus S\) annihilate \(\ker\lambda\).  Linear algebra
says that \(\operatorname{ev}_x|_{\mathcal W}\) is either zero or
proportional to \(\lambda\).  Completeness of \(S\) excludes the latter.
In the former case \(f_*(x)=0\), so the divided full hyperplane has common
value zero at \(x\), while

\[
y(x)=u(x)/L_S(x)\ne0.                                           \tag{3.2}
\]

Thus \(x\) is a fixed mismatch.

Now let \(\alpha\in Z(P)\) annihilate \(\ker\lambda\).  Equation (2.3)
makes \(\operatorname{ev}_\alpha|_{\mathcal W}\) nonzero, hence

\[
\operatorname{ev}_\alpha|_{\mathcal W}=t_\alpha\lambda,
\qquad t_\alpha\ne0.                                            \tag{3.3}
\]

Every member of the full hyperplane has

\[
f(\alpha)=t_\alpha\beta\ne0.                                    \tag{3.4}
\]

Its divided common value is zero, whereas agreement with (2.9) is
equivalent to \(f(\alpha)=0\).  Hence \(\alpha\) is also a fixed mismatch.
\(\square\)

Passing to the full hyperplane is essential.  Applying the argument only
to the affine hull of the finite listed class would not identify its
direction with \(\ker\lambda\) when that hull has lower rank.

## 4. Reduction to the predecessor recurrence

Let \(Z\subset\Omega\) be the common-zero set of the divided full-hyperplane
direction and put \(z=|Z|\).  In the divided coordinates the affine base
is zero.  By Lemma 3.1, removing \(Z\) loses no agreements.  Every
direction polynomial is divisible by \(L_Z\); division preserves
distinctness and exact rank six, gives degree below \(k-z\), and leaves no
common direction zero on \(\Omega\setminus Z\).  Every actual listed
member still has at least \(k+w\) agreements.

Choose \(z\) fresh field points outside \(\Omega\) and outside the common
zero set of the divided direction.  There are enough because

\[
p-K-2d+1=2\,145\,860\,022>0.                                    \tag{4.1}
\]

Add arbitrary received values at those points; the recurrence permits
zero or nonzero labels.  The padded family has the predecessor parameters

\[
(N_{\rm dom},K_{\rm msg},m)=(K+k,k,k+w).                         \tag{4.2}
\]

Theorem 2.2 and Corollary 2.3 of the weighted-head predecessor therefore
give the uniform label cap

\[
\boxed{B_{\rm src}(k)=C^{\rm ncz}_6(k).}                         \tag{4.3}
\]

No rank-five fallback is needed inside the exact-rank-seven branch:
every finite label class was enlarged to the same full exact-rank-six
hyperplane.  The separate rank-at-most-six whole-family branch was paid
before (2.4).

## 5. Exact recurrence and refined endpoint

Replay the predecessor recurrence with ambient gap \(K\), excess \(w\),
dimensions \(1\le k\le d\), and ranks through six.  At the former
six-dimensional obstruction it gives

\[
\begin{array}{c|r}
k&C^{\rm ncz}_6(k)\\ \hline
4\,981&9\,806\,438\\
4\,982&9\,806\,312\\
4\,983&9\,806\,186\\
4\,984&9\,806\,060\\
4\,985&9\,805\,934\\
4\,986&9\,805\,807.
\end{array}                                                       \tag{5.1}
\]

At \(k=4\,981\), the binding rank-six recurrence division is

\[
\left\lfloor
\frac{710\,260\,719\,335}{72\,428}
\right\rfloor
=9\,806\,438,
\quad\hbox{remainder }27\,871.                                  \tag{5.2}
\]

The predecessor coarse top-six outer compiler has maximum

\[
\begin{aligned}
M_{\rm coarse}
={}&282\,544(9\,806\,438)\\
&+4\,980(718\,621)+693\,605(716\,918)\\
={}&3\,271\,586\,860\,242.                                      \tag{5.3}
\end{aligned}
\]

It pays \(Q=147\,593\).  At \(Q=147\,594\), its only violating
largest-line size is \(s_1=282\,544\); the runner-up \(s_1=282\,543\)
already gives head \(15\,775\,743\).  The unique survivor admits a sharper
top-five compiler.

Put

\[
B=d-1-s_1=4\,980,\qquad
F(s)=C^{\rm ncz}_6(d-s),\qquad
M(x)=\max_{1\le t\le x}F(t).                                    \tag{5.4}
\]

Let \(a=s_6\) be the sixth largest projective-line size.  Then

\[
1\le a\le\lfloor B/5\rfloor=996,\qquad
s_2\le B-4a,                                                     \tag{5.5}
\]

and every tail line has size at most \(a\).  Charge every nonlargest
coordinate at \(M(a)\), then upgrade at most \(B\) top-five coordinates
to \(M(B-4a)\).  This gives

\[
U(a)
=(R-s_1)M(a)+B\bigl(M(B-4a)-M(a)\bigr).                          \tag{5.6}
\]

The exact 996-value per-coordinate envelope has a unique maximum

\[
\max_aU(a)=U(996)
=698\,585\cdot716\,918
=500\,828\,161\,030.                                             \tag{5.7}
\]

The runner-up is \(500\,826\,095\,155\), attained at \(a=990,991\).
At \(a=996\), the five top parts are forced to equal \(996\), and the tail
mass is \(693\,605\).  Retain exact tail divisibility.  For
\(F(s)=C^{\rm ncz}_6(d-s)\), put

\[
\ell(s)=s\bigl(F(996)-F(s)\bigr).
\]

An exact shortest-path computation on \(\mathbb Z/996\mathbb Z\), with
edge \(+s\) of weight \(\ell(s)\), gives minimum loss \(87\,136\) in the
target residue \(693\,605\bmod996=389\).  The optimum is the single
part \(389\), where \(F(389)=716\,694\), padded by \(696\) zero-loss
parts of size \(996\):

\[
693\,605=696\cdot996+389.                                       \tag{5.8}
\]

Thus the exact tail and nonlargest contributions are

\[
\begin{aligned}
T_{\rm tail}&=497\,257\,822\,254,\\
U_{\rm exact}&=500\,828\,073\,894.
\end{aligned}                                                    \tag{5.9}
\]

The \(87\,136\) correction is much smaller than the \(1\,978\,739\) gap
to the next \(a\)-envelope, so \(a=996\) remains the global maximum.
The refined numerator is

\[
M_{\rm ref}
=282\,544(9\,806\,438)+500\,828\,073\,894
=3\,271\,578\,292\,166.                                         \tag{5.10}
\]

At the last paid cutoff,

\[
\left\lfloor\frac{M_{\rm ref}}{g-147\,594}\right\rfloor
=
\left\lfloor\frac{3\,271\,578\,292\,166}{207\,378}\right\rfloor
=15\,775\,917,                                                   \tag{5.11}
\]

with remainder \(176\,540\) and margin \(15\).  At the adjacent cutoff,

\[
\left\lfloor\frac{M_{\rm ref}}{207\,377}\right\rfloor
=15\,775\,993,                                                   \tag{5.12}
\]

with remainder \(191\,805\) and excess \(61\).  Both the coarse and refined
scans leave exactly

\[
|S|=282\,544,\qquad k=d-|S|=4\,981.                              \tag{5.13}
\]

Changing only the cap at \(k=4\,981\) gives the sharp threshold

\[
\begin{array}{c|c}
\text{replacement cap}&\text{compiled }Q=147\,595\text{ head}\\ \hline
9\,806\,394&15\,775\,933,\\
9\,806\,393&15\,775\,932.
\end{array}                                                       \tag{5.14}
\]

Thus the next proof obligation is a 45-unit improvement on one
source-compatible exact-rank-six recurrence state, or a proof that the
current hypotheses permit its coarse extremizer.

### Audit history

The first conservative draft applied Lemma 3.1 only when the listed class
itself had affine rank six and retained a rank-five fallback.  That safe
but weaker compiler stopped at \(Q=139\,131\).  Fresh review identified
the full-hyperplane enlargement (3.1), which removes the fallback without
assuming the finite class spans the kernel.  The superseded
\(Q=139\,131\) calculation is recorded here rather than silently
discarded.

## 6. Relation to current upstream work

This lemma assumes no \(T_{16}\), \(T_{32}\), dyadic, quotient-support, or
other alignment.  Ragged collision examples therefore do not falsify it.
It also does not rely on an ordinary pairwise Hahn/Delsarte improvement;
the source-specific fixed-mismatch gate is information absent from that
relaxation.  The current upstream pencil-census and provenance packets are
file-disjoint and prove different statements.

## 7. Ledger effect and nonclaims

The exact local frontier moves from

\[
Q=29\,554\quad\hbox{to}\quad Q=147\,594.                         \tag{7.1}
\]

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

No rank-at-least-eight result, v4 ownership assignment, signed atom, or
global row bound is claimed.

## 8. Proof audit

Statement audited:

The implication from a counted normalized-label class to the full
exact-rank-six hyperplane, then to a no-common-zero recurrence instance,
and from the refined top-five compiler to the cumulative outer head.

Dependencies:

- PROVEN by predecessors: exclusion of whole-family rank at most six,
  exact rank seven in the surviving branch, master-denominator
  normalization, \(u=P/V\) nowhere zero on \(E_0\), exact-lcm
  no-common-zero normalization on \(Z(P)\), complete projective-line
  slicing, the combined-domain table and agreement count, the full-line
  recurrence, and the top-six outer compiler.  The sealed exact-provenance
  migration certifies that the rank-six parent's canonical
  `experimental/grande_finale.tex` ancestor differs from the current source
  only by the audited status-text operations; all other bindings and every
  payload seal remain fresh.
- PROVEN here: full-hyperplane containment, nonzero counted labels, the
  exact-rank-six kernel identity, fixed-mismatch classification on both
  pieces of \(\Omega\), padding availability, and (4.3).
- EXACT CERTIFIED COMPUTATION: recurrence arrays, coarse and refined outer
  optimizers, exact tail-residue shortest path, adjacent survivor, and
  45-unit threshold.
- OPEN: the 45-unit \(k=4\,981\) improvement, all later heads, ranks at
  least eight, v4 ownership, and the global row.

Parameter dependence:

Finite exact M31 integers only.  There are no asymptotic constants.

Layer-cake / dyadic summability:

Not applicable.

Moment / Markov / Chebyshev:

Not applicable.

Edge cases / notation:

Only nonempty normalized-label classes receive agreement-pair weight.
Only the surviving exact-rank-seven branch enters the line compiler;
rank-at-most-six whole families are paid separately.  The full hyperplane,
not the finite class affine hull, supplies exact direction rank six.
Padding points avoid the divided direction's common polynomial zero set.
The recurrence cap is an upper bound and is not asserted to be attained by
a source family.  Cutoffs above \(w\) are legal because the combined
\(k+w\) agreement bound is independent of \(Q\), while the outer compiler
only requires \(Q<g\).

Numerical evidence:

All endpoint values are exact integer computations.  They certify the
finite compiler arithmetic, not existence of an extremal list.

Verdict:

GREEN for the local theorem after independent proof and arithmetic review.
Do not authorize a global proof.

Remaining risks:

The full-hyperplane enlargement, padding reduction, refined top-five
compiler, and tail-residue calculation are load-bearing.  The final
45-unit residual may require
information beyond the existing projective-line recurrence.
