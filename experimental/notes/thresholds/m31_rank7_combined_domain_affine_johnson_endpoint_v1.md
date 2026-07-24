---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every normalized-label subclass obtained by deleting one complete E0 projective line in the rank-seven endpoint family is one rank-at-most-six ordinary Reed-Solomon list on the disjoint union (E0 minus S) union Z(P). Its length is K+k, dimension is k, and every member has at least k+w agreements. Intersecting the unconditional rank-six affine-span cap with ordinary Johnson and the predecessor E0 cap pays the complete cumulative deficit head through Q=29554. The exact head is 15775891, forty-one below the shallow target. At Q=29555 the same compiler gives 15776139, and the residual is localized to k=4981 through 4986; a uniform combined-domain cap 14115290, only 238 below the generic affine-span cap, would close that next head.
architecture: M31_RANK7_COMBINED_DOMAIN_AFFINE_JOHNSON_ENDPOINT_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: Source-bound rank-seven cumulative deficit head; no v4 atom value and no signed Xi_46 payment.
quantifier: Every rank-at-most-seven shallow master-denominator family at the endpoint g=354972, every complete E0 projective-line class, and every normalized-label subclass in that class.
projection_and_unit: Distinct LIST codewords per received word. The outer compiler counts agreement pairs and divides once by g-Q; it does not sum support, locator, or denominator labels as codewords.
claimed_bound: N_(delta<=29554)<=15775891<=15775932. The first unclosed head Q=29555 has cap 15776139. No global row upper bound.
status: PROVED LOCAL Q=29554 HEAD / Q=29555 ROUTE CUT / GLOBAL ROW OPEN
impact: RANK_SEVEN_FRONTIER_ADVANCE / ROUTE_CUT / NO_LEDGER_MOVEMENT
falsifier: Failure of the combined-domain embedding, overlap between E0 and Z(P), a subclass direction rank above six, fewer than k+w combined agreements, an exact endpoint arithmetic mismatch, a Q=29554 head above 15775932, or promotion to a v4 atom or global row theorem.
replay: Standard-library Python normal and optimized checks, hostile mutations, independent Python recomputation, Sage exact-integer replay, strict JSON/schema/source hashes, predecessor payload pins, and the exact Grande Finale provenance migration.
---

# M31 rank-seven combined-domain affine/Johnson endpoint

## 1. Result and scope

Use the endpoint normalization

\[
\begin{aligned}
p&=2^{31}-1,& n&=2^{21},& K&=2^{20},\\
a&=1\,116\,023,& R&=981\,129,& w&=67\,447,\\
g&=354\,972,&d&=g-w=287\,525.
\end{aligned}                                                     \tag{1.1}
\]

The predecessor rank-seven packet pays every cumulative effective-deficit
head through \(Q=26\,193\), but its two-domain split stops at the
\(Q=26\,194\), \(k=3\,145\) line subclass.  The missing observation is that
the two tables in that split can be joined before applying a list theorem.

The joined table gives one ordinary Reed--Solomon list.  Its unconditional
rank-six affine-span and Johnson bounds pay not only \(Q=26\,194\), but the
entire cumulative head

\[
\boxed{
N_{\delta\le29\,554}\le15\,775\,891
=15\,775\,932-41.}                                                \tag{1.2}
\]

Because this is a cumulative head, (1.2) also pays every smaller cutoff.
The first failure of this compiler is exact:

\[
N_{\delta\le29\,555}\le15\,776\,139
=15\,775\,932+207.                                                \tag{1.3}
\]

Equation (1.2) is a local rank-seven payment.  It is not a v4
first-match atom, a signed-\(\Xi_{46}\) payment, a rank-at-least-eight
theorem, or a proof of the M31 LIST row.

## 2. The combined-domain lemma

Use the predecessor notation

\[
P=\operatorname{lcm}_iG_i,\qquad
Q_i=P/G_i,\qquad f_i=Q_i b_i,                                    \tag{2.1}
\]

\[
q_i=\deg Q_i,\qquad
\delta_i=q_i-s_i,\qquad
\operatorname{agr}_{E_0}(f_i,u)=g-\delta_i,                       \tag{2.2}
\]

where \(u=P/V\) is nowhere zero on \(E_0\), \(s_i\ge0\) is the shallow
excess, and

\[
E_0\cap Z(P)=\varnothing.                                        \tag{2.3}
\]

Fix one complete projective-line class \(S\subset E_0\), put
\(\sigma=|S|\), and fix one normalized-label subclass of size \(c\).
Thus \(0\le c\le\sigma\), every member of the slice agrees with \(u\)
at exactly those \(c\) coordinates of \(S\), and the slice has affine
direction rank at most six.  Choose \(f_*\) in the slice.  Every other
member has the unique form

\[
f_i=f_*+L_Sa_i,\qquad \deg a_i<k,\qquad k=d-\sigma.                \tag{2.4}
\]

Define one received table on the disjoint domain

\[
\Omega=(E_0\setminus S)\mathbin{\dot\cup} Z(P)                    \tag{2.5}
\]

by

\[
y(x)=
\begin{cases}
(u(x)-f_*(x))/L_S(x),&x\in E_0\setminus S,\\
-f_*(x)/L_S(x),&x\in Z(P).
\end{cases}                                                       \tag{2.6}
\]

Every denominator in (2.6) is nonzero: outside \(S\), the locator \(L_S\)
does not vanish, and (2.3) separates \(Z(P)\) from \(S\).

On \(E_0\setminus S\), the polynomial \(a_i\) agrees with the first table
at exactly

\[
(g-\delta_i)-c                                                   \tag{2.7}
\]

coordinates.  At every root of \(Q_i\), equation (2.1) gives \(f_i=0\),
so \(a_i\) agrees with the second table at at least \(q_i\) coordinates.
Consequently

\[
\begin{aligned}
\operatorname{agr}_\Omega(a_i,y)
&\ge(g-\delta_i-c)+q_i\\
&=g+s_i-c\\
&\ge g-\sigma\\
&=k+w.                                                           \tag{2.8}
\end{aligned}
\]

The domain length is

\[
|\Omega|=(R-\sigma)+g=(R+w)+(g-w-\sigma)=K+k.                    \tag{2.9}
\]

Thus every normalized-label subclass is an affine family of distinct
degree-\(<k\) polynomials, of direction rank at most six, in the ordinary
\([K+k,k]\) Reed--Solomon list with agreement at least \(k+w\).

This proof permits common direction zeros and common agreements.  No
no-common-zero projective recurrence is used.

## 3. Two unconditional subclass caps

The recursive affine-span theorem applied with actual affine rank
\(r\le6\) gives

\[
A_r=
\left\lfloor
\frac{\binom{K+r}{r}}{\binom{w+r}{r}}
\right\rfloor.                                                    \tag{3.1}
\]

The exact values for \(r=0,\ldots,6\) are

\[
1,\ 15,\ 241,\ 3\,757,\ 58\,410,\ 908\,021,\ 14\,115\,528,        \tag{3.2}
\]

so the at-most-six cap is

\[
A_6=14\,115\,528.                                                 \tag{3.3}
\]

Ordinary Johnson gives, whenever its denominator is positive,

\[
J(k)=
\left\lfloor
\frac{(K+k)(w+1)}
{(k+w)^2-(K+k)(k-1)}
\right\rfloor.                                                    \tag{3.4}
\]

The denominator simplifies to

\[
4\,550\,146\,385-913\,681k.                                      \tag{3.5}
\]

It is positive exactly through \(k=4\,980\):

\[
D(4\,980)=15\,005,\qquad D(4\,981)=-898\,676.                    \tag{3.6}
\]

At the predecessor obstruction,

\[
J(3\,145)=
\left\lfloor
\frac{70\,936\,478\,008}{1\,676\,619\,640}
\right\rfloor
=42.                                                             \tag{3.7}
\]

Let \(C_Q(k)\) be the predecessor at-most-rank-six cap on the
\(E_0\setminus S\) side after deleting a line with residual dimension
\(k\).  The new safe normalized-label cap is

\[
B_Q(k)=\min\{C_Q(k),A_6,J(k)\text{ when active}\}.                 \tag{3.8}
\]

The affine-span and Johnson terms are both ordinary RS list theorems on
\(\Omega\); they are not support relaxations or sums over planted-root
labels.

## 4. Exact outer compiler

For every line size \(\sigma\), the normalized-label subclasses have sizes
\(c_j\) with \(\sum_jc_j=\sigma\).  Multiplying (3.8) by the exact agreement
pair weights therefore bounds the whole line by

\[
\sum_j c_jB_Q(d-\sigma)\le \sigma B_Q(d-\sigma).                  \tag{4.1}
\]

The predecessor projective geometry says that the six largest line sizes
have total at most \(d-1\).  For a proposed largest size \(\sigma\), put

\[
B=d-1-\sigma,\qquad
u=\min(\sigma,B-4),\qquad
b=\min(\sigma,\lfloor B/5\rfloor),                               \tag{4.2}
\]

and let \(M_Q(x)=\max_{1\le t\le x}B_Q(d-t)\).  The exact agreement-pair
numerator is bounded by

\[
\sigma B_Q(d-\sigma)
+B M_Q(u)
+\bigl(R-(d-1)\bigr)M_Q(b).                                      \tag{4.3}
\]

Divide the maximum of (4.3) once by \(g-Q\).

At \(Q=26\,194\), the combined compiler already gives

\[
14\,302\,721,
\tag{4.4}
\]

which is \(1\,473\,211\) below the shallow target.  At the exact endpoint
\(Q=29\,554\), the maximizing data are

\[
\begin{array}{c|r}
\text{largest line size}&282\,544\\
\text{largest residual }k&4\,981\\
B_Q(4\,981)&14\,115\,528\\
\text{other top mass}&4\,980\\
\text{other top cap}&1\,640\,588\\
\text{tail mass}&693\,605\\
\text{tail cap}&1\,639\,739\\
\text{numerator}&5\,133\,759\,040\,567.
\end{array}                                                       \tag{4.5}
\]

Since \(g-Q=325\,418\), flooring (4.5) gives (1.2).  Before the floor,
the numerator is already

\[
13\,199\,009
\tag{4.6}
\]

below \(15\,775\,932(325\,418)\).

## 5. First residual and exact next threshold

At \(Q=29\,555\), the same exhaustive scan gives

\[
\begin{array}{c|r}
g-Q&325\,417\\
\text{maximizing line size}&282\,544\\
\text{maximizing residual }k&4\,981\\
\text{numerator}&5\,133\,824\,008\,972\\
\text{head after flooring}&15\,776\,139.
\end{array}                                                       \tag{5.1}
\]

Exactly six largest-line sizes survive the target comparison:

\[
282\,539,\ldots,282\,544,
\qquad k=4\,986,\ldots,4\,981.                                   \tag{5.2}
\]

They begin immediately after the ordinary Johnson denominator becomes
nonpositive.  Replacing the generic combined-domain affine cap (3.3) by
one uniform cap \(A\), while retaining every other proved term, gives the
sharp integer threshold

\[
\begin{array}{c|c}
A&\text{compiled head}\\ \hline
14\,115\,290&15\,775\,932\\
14\,115\,291&15\,775\,933.
\end{array}                                                       \tag{5.3}
\]

Thus a source-compatible theorem improving (3.3) by only

\[
14\,115\,528-14\,115\,290=238                                   \tag{5.4}
\]

uniformly on the six residual dimensions in (5.2) closes the next
cumulative head.

This is a route localization, not a proof that such an improvement follows
from arbitrary rank-six RS geometry.  The next theorem must exploit the
glued source table (2.6), the planted-divisor origin of its agreements, or
another chronology-valid owner.  A no-common-zero recurrence may be used
only after the common-agreement component is separately paid.

## 6. Interaction with alignment counterexamples

No dyadic, \(T_{16}\), \(T_{32}\), or quotient-support alignment is assumed
anywhere in Sections 2--5.  Ragged support collisions therefore do not
falsify this packet.  Conversely, this packet does not classify or pay such
collisions; it operates after source normalization, at the codeword and
agreement-pair level.

## 7. Ledger effect and nonclaims

The exact local frontier moves from

\[
Q=26\,193\quad\hbox{to}\quad Q=29\,554.                           \tag{7.1}
\]

The active v4 ledger does not move:

```text
U_paid    = 3730
U_Q       = null
U_list_int= null
U_ext     = null
U_new     = null
Xi_46     remains open
row       remains open
```

No theorem is claimed for rank at least eight.  No fixed-\(G\) or
normalized-label cap is summed as a global codeword atom.  The \(Q=29\,555\)
number is a route cut for this exact compiler, not a lower construction or
an impossibility theorem for stronger source incidence.

## 8. Proof audit

Statement audited:

The implication from one normalized-label projective-line slice to one
ordinary combined-domain RS list, and from the resulting two unconditional
subclass caps to the complete rank-seven cumulative head.

Files/sections read:

The active recursive affine-span and fixed-union Johnson theorems in
`experimental/grande_finale.tex`; the rank-seven normalization,
full-projective-line recurrence, planted-root table, and \(Q=26\,194\)
route cut in the predecessor weighted-head packet; the v4 source adapter;
and the exact Grande Finale provenance migration.

Dependencies:

- PROVEN by predecessors: master-denominator normalization, disjointness
  \(E_0\cap Z(P)=\varnothing\), exact deficit identity
  \(\delta_i=q_i-s_i\), projective-line normalized-label slicing, rank loss
  to at most six, top-six prefix constraint, recursive affine-span theorem,
  and ordinary Johnson theorem.
- PROVEN here: the glued table (2.6), agreement lower bound (2.8), exact
  \([K+k,k]\) parameters, cap intersection (3.8), outer endpoint (1.2), and
  first-residual threshold (5.3).
- OPEN: a source-compatible improvement on the six dimensions (5.2),
  all later rank-seven heads, ranks at least eight, v4 chronology payment,
  and the global row.

Parameter dependence:

Finite exact M31 integers only.  There are no asymptotic constants.

Layer-cake / dyadic summability:

Not applicable.  No level-set error is integrated.

Moment / Markov / Chebyshev:

Not applicable.  No moment inequality is used.

Edge cases / notation:

The normalized-label size \(c\) may be zero only for an empty slice and is
otherwise at most \(\sigma\).  Common direction zeros and common agreements
are permitted by the affine-span theorem.  Johnson is included only when
its exact denominator is positive.  At-most-six affine rank is handled by
checking every rank \(0,\ldots,6\), not by assuming exact rank six.

Numerical evidence:

The endpoint scan, binomial ratios, Johnson activation boundary, optimizer,
floor/remainder arithmetic, and cap threshold are exact big-integer
computations.  They are proofs of the finite compiler arithmetic, not
evidence for the missing source-incidence theorem.

Verdict:

GREEN - the local \(Q=29\,554\) cumulative head and the exact
\(Q=29\,555\) route localization satisfy the stated proof obligation.
Global rank seven and the M31 LIST row remain open outside this packet's
statement.

Remaining risks:

The new local head is not chronology-valid v4 ledger mass.  The first
unresolved six dimensions may contain source configurations attaining the
generic affine cap; no direct construction or exclusion is claimed.

Maximal next action:

Classify the common-agreement component of the glued table on
\(k=4\,981,\ldots,4\,986\) and prove either a uniform cap at most
\(14\,115\,290\), a paid owner, or an explicit source-realizable primitive
route cut.  Do not return to aligned-only support censuses.

## 9. Replay

```text
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --check
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1_independent.py
/usr/local/bin/sage experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.sage
```
