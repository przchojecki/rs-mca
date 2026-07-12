# Owner-Rooted Dense-Band Localization

```text
Status: PROVED FINITE LOCALIZATION + SPARSE/LOW-LOAD PAYMENT / OPEN PRIMITIVE SIDON PAYMENT
Theorem status: no dense complete-band estimate, A4 theorem, primitive Q, or Proximity Prize theorem is proved
```

## Purpose

This note banks the finite reductions available before the source-specific
primitive Sidon/Fourier payment:

1. a band-restriction excess has an exact norming-dual representation on the
   actual residual supports;
2. unique noncommon slope ownership roots its positive mass without loss; and
3. after strict-excess and repeated-rim removal, the residual support family is
   an exact `(a-1)`-packing;
4. sparse complete bands are paid at full-image scale;
5. every remaining excess has an exact norming dual and rooted positive mass;
6. the band is split by projected energy; and
7. the low projected-energy class is paid by interpolation.

The difficult source-specific estimate remains unchanged.  Nothing below
bounds the norming-dual mass using the moment-curve band, and nothing converts
large rooted mass into a quotient, field, rank, planted, or saturation payment.

This is a follow-up to the mask-aware reduction packet. It sharpens the
owner-rooted input required by the open source-to-cell implication. It does
not claim that the `(CAT)` first-match atlas already supplies the missing
signed estimate, `(UNIF)`, or the `(RC)` ray compiler.

The fixed-support ownership argument refines the manuscript's
`prop:exact-support-upper`, while the occupancy deletion is compatible with
`lem:saturation-principle`.  The present rim-packing conclusion is new only
after adding the explicit post-saturation and cross-slope rim-free hypotheses.

## 1. Fourier and residual conventions

Let (G) be a finite abelian group of order (H), and use

\[
 \widehat f(\gamma)=\sum_{s\in G}f(s)\overline{\gamma(s)},
 \qquad
 f(s)=H^{-1}\sum_{\gamma\in\widehat G}\widehat f(\gamma)\gamma(s).
\tag{1}
\]

All norms and inner products use counting measure:

\[
 \langle u,v\rangle=\sum_{s\in G}u(s)\overline{v(s)}.
\]

Let (Omega^circ) be the actual pre-A4 residual support set, let
(Phi:\Omega^circ\to G), and put

\[
 f(s)=|\{x\in\Omega^\circ:\Phi(x)=s\}|.
\tag{2}
\]

For normalization, let

\[
 \Omega^0\subseteq{T\choose a},
 \qquad M=|\Omega^0|,
 \qquad L=|\Phi(\Omega^0)|,
 \qquad W=|\Omega^\circ|.
\tag{2a}
\]

The manuscript's primitive prefix leaf uses the full-slice convention
`$\Omega^0={T\choose a}$`.  When a proper profile sub-slice is allowed, define
the thinning factor

\[
 \kappa=\frac{{N\choose a}}M.
\tag{2b}
\]

For a symmetric character band (A=-A\subseteq\widehat G), define

\[
 P_Af(s)=H^{-1}\sum_{\gamma\in A}\widehat f(\gamma)\gamma(s).
\tag{3}
\]

Symmetry makes (P_A) self-adjoint.  Dyadic bands defined by
(|\tau(\gamma)|) have this symmetry because
(\tau(-\gamma)=\overline{\tau(\gamma)}).

## 2. Exact norming-dual pullback

Fix (1<q<\infty), and let (q'=q/(q-1)).

### Proposition 2.1 (norming dual)

If (P_Af\ne0), there is (g:G\to\mathbb C) with

\[
 \|g\|_{q'}=1
\]

such that

\[
 \boxed{
 \|P_Af\|_q
 =\operatorname{Re}\langle P_Af,g\rangle
 =\operatorname{Re}\langle f,P_Ag\rangle
 =\sum_{x\in\Omega^\circ}w_g(x),
 }
\tag{4}
\]

where

\[
 w_g(x)=\operatorname{Re}\overline{(P_Ag)(\Phi(x))}.
\tag{5}
\]

One may take

\[
 g(s)=
 \frac{P_Af(s)|P_Af(s)|^{q-2}}
      {\|P_Af\|_q^{q-1}},
\tag{6}
\]

with the value zero when (P_Af(s)=0).

### Proof

Equation (6) gives

\[
 \|g\|_{q'}^{q'}
 =\frac{\sum_s|P_Af(s)|^q}{\|P_Af\|_q^q}=1
\]

and

\[
 \langle P_Af,g\rangle=\|P_Af\|_q.
\]

The multiplier of (P_A) is the real indicator of the symmetric set (A),
so (P_A=P_A^*).  Hence

\[
 \langle P_Af,g\rangle=\langle f,P_Ag\rangle.
\]

Finally, expand (f) using (2).  This gives (4)--(5).  (square)

### Corollary 2.2 (positive mass)

Writing (w_g^+=\max(w_g,0)),

\[
 \boxed{
 \sum_{x\in\Omega^\circ}w_g^+(x)\ge\|P_Af\|_q.
 }
\tag{7}
\]

Thus a normalized (q)-BR excess produces positive mass on the exact residual
mask.  This is an identity and a sign-preserving truncation, not a Fourier
estimate.

## 3. Exact slope rooting

Let (D\subseteq\mathbb F) be the evaluation domain and let

\[
 U_z=u+zv,
 \qquad z\in\mathbb F,
\tag{8}
\]

be a received line.  The RS code consists of evaluations of polynomials of
degree (<k).  A size-(a) witness is a triple ((z,h,S)) with

\[
 |S|=a,
 \qquad
 U_z|_S=h|_S,
 \qquad
 \deg h<k.
\tag{9}
\]

Assume (a\ge k+1).  Call (S) a common-line support when both (u|_S) and
(v|_S) are restrictions of degree-(<k) polynomials.

### Proposition 3.1 (fixed-support slope uniqueness)

If a support (S) is a witness at two distinct slopes, then (S) is a
common-line support.  Consequently every noncommon witness support has at most
one slope owner.

### Proof

Suppose

\[
 u+zv=h_z,
 \qquad
 u+z'v=h_{z'}
\]

on (S), with (z\ne z').  Subtraction gives

\[
 v|_S=\frac{h_z-h_{z'}}{z-z'}\bigg|_S,
\]

which is a degree-(<k) restriction.  Substitution then gives the same fact
for (u|_S).  (square)

After removing common-line supports, let

\[
 o:\Omega^\circ\to\mathcal Z
\]

be the unique owner map.  Define

\[
 W_z=\sum_{o(x)=z}w_g^+(x),
 \qquad
 W_+=\sum_xw_g^+(x).
\tag{10}
\]

### Proposition 3.2 (lossless rooting and heavy-owner alternative)

The positive mass partitions exactly:

\[
 \boxed{W_+=\sum_{z\in\mathcal Z}W_z.}
\tag{11}
\]

Moreover, for every (0<\eta<1), the owner set

\[
 \mathcal Z_\eta=
 \left\{z:W_z\ge\eta W_+/|\mathcal Z|\right\}
\tag{12}
\]

carries at least ((1-\eta)W_+).

### Proof

Equation (11) is the partition by the function (o).  The total mass of
owners outside (mathcal Z_\eta) is strictly less than
(|\mathcal Z|\eta W_+/|\mathcal Z|=\eta W_+).  (square)

This is the precise output of the slope-rooting lemma. It does not assert that one slope alone
must carry a constant fraction of the mass.

## 4. Exact agreement and rim packing

For a witness ((z,h,S)), let its complete agreement set be

\[
 T(z,h)=\{t\in D:U_z(t)=h(t)\}.
\tag{13}
\]

The witness is complete-agreement-exact when $|T(z,h)|=a$.  Strict-excess
removal means that every retained witness is complete-agreement-exact.

Terminology matters here.  The manuscript's "exact-$a$ support" means a
chosen support of size $a$; it may be contained in a larger complete
agreement set.  This section uses the stronger post-saturation condition
$|T(z,h)|=a$.  The two notions must not be interchanged.

### Proposition 4.1 (saturation packet equivalence)

Assume (a-1\ge k).

1. If (|T(z,h)|\ge a+1), then all (a)-subsets of any
   ((a+1))-subset of (T(z,h)) are witnesses at (z).
2. Conversely, if all (a)-subsets of an ((a+1))-set (T) are witnesses at
   the same slope, then one degree-(<k) polynomial agrees with (U_z) on all
   of (T).

### Proof

The first assertion is immediate by restriction.  For the converse, adjacent
(a)-subsets of (T) intersect in (a-1\ge k) points.  Their interpolation
polynomials therefore agree identically.  The graph of (a)-subsets of (T),
joined when they differ by one point, is connected.  Hence every subset uses
the same polynomial, which agrees on their union (T).  (square)

For a support (S), call each ((a-1))-subset (R\subset S) a rim.  Assume
the semantic compiler has removed:

* every strict-excess/saturation packet from Proposition 4.1; and
* every repeated cross-slope rim, meaning no rim lies in supports with two
  distinct owners.

### Theorem 4.2 (global rim packing)

Under these hypotheses, any two distinct residual supports satisfy

\[
 \boxed{|S\cap S'|\le a-2.}
\tag{14}
\]

Equivalently, every ((a-1))-rim belongs to at most one residual support.
Consequently,

\[
 \boxed{
 a|\Omega^\circ|
 \le {N\choose a-1},
 \qquad
 |\Omega^\circ|
 \le\frac1a{N\choose a-1}
 =\frac1{N-a+1}{N\choose a}.
 }
\tag{15}
\]

### Proof

Suppose two supports share an ((a-1))-rim.

If their owners are distinct, this contradicts the repeated cross-slope rim
removal.

If their owner is the same slope, their degree-(<k) interpolation polynomials
agree on (a-1\ge k) points and are therefore identical.  That polynomial
agrees with the received word on the union, which has (a+1) points.  This
contradicts strict-excess removal.

Thus rims are globally disjoint.  Every support contains exactly (a) rims,
while the ambient coordinate set has ({N\choose a-1}) rims.  Double counting
proves (15).  (square)

## 5. Normalization and the sparse-band corollary

Theorem 4.2 gives

\[
 \rho:=\frac WM
 \le
 \frac\kappa{N-a+1}.
\tag{16}
\]

The cleaner bound `$\rho\le1/(N-a+1)$` requires the full-slice identity
`$M={N\choose a}$`.  It must not be inferred from the weaker inclusion
`$\Omega^0\subseteq{T\choose a}$`.

For a complete character band `$A\subseteq\widehat G$`, put
`$\delta_A=|A|/|G|$`.  The universal band-density theorem in the mask-aware
packet gives

\[
 \|P_Af\|_q\le W\delta_A^{1-1/q}.
\tag{17}
\]

Therefore

\[
 \boxed{
 \frac{L^{1-1/q}}M\|P_Af\|_q
 \le
 \frac\kappa{N-a+1}(L\delta_A)^{1-1/q}.
 }
\tag{18}
\]

### Corollary 5.1 (sparse-band complete-band restriction bound)

On the full slice, every complete band satisfying

\[
 \log^+(L\delta_A)=o(N)
\]

obeys

\[
 \boxed{
 \|P_Af\|_q
 \le
 \exp(o(N))\frac M{L^{1-1/q}}.
 }
\tag{19}
\]

For a proper profile sub-slice, the explicit factor `$\kappa$` remains unless
`$\log\kappa=o(N)$`.  This is the strongest complete-band restriction bound consequence obtained directly
from rim packing and the already-proved band-density estimate.

## 6. Rim packing does not imply dense-band complete-band restriction bound

Let `$B$` be even, put `$N=2B$` and `$a=B$`, choose `$A_i=Q^i$` with `$Q\ge5$`,
and choose `$C>2\sum_iA_i$`.  On

\[
 T=\{A_i,C-A_i:1\le i\le B\},
\]

use `$\Phi(S)=\sum_{t\in S}t$` and the full slice
`$\Omega^0={T\choose B}$`.  Superincreasing uniqueness gives

\[
 L=\frac{3^B+1}{2}.
\tag{20}
\]

The fiber at `$s_0=BC/2$` is

\[
 \mathcal F_B=
 \left\{
 \bigcup_{i\in J}\{A_i,C-A_i\}:|J|=B/2
 \right\},
 \qquad
 W={B\choose B/2}.
\tag{21}
\]

For distinct members,

\[
 |S_J\cap S_{J'}|=2|J\cap J'|\le B-2=a-2,
\tag{22}
\]

so the heavy fiber is a global `(a-1)`-packing.  Nevertheless

\[
 \frac{WL}{M}
 =\exp\left(B\log\frac32+O(\log B)\right).
\tag{23}
\]

The nonzero dual has only `$O(\log N)$` complete dyadic bands.  For a densest
band `$A$`, the point-mass identity gives `$P_Af(s_0)=W\delta_A$` with
`$\delta_A=\exp(-o(N))$`.  Logarithmic-moment accessibility also gives
`$L^{-1/q}=\exp(-o(N))$`; hence

\[
 \frac{L^{1-1/q}}M\|P_Af\|_q
 \ge
 \exp\left(\frac12\log\frac32\,N-o(N)\right).
\tag{24}
\]

The complete depth-one prefix fiber is realized by one received line using
`thm:prefix-to-line-hardness` and `cor:exact-prefix-ray-realization`, with
`$k=a-2$` and a separating pole.  The realization has complete agreement
exactly `$a$`, distinct owners, and no common support.

This is not a semantic counterexample.  It has the canonical planted relation

\[
 A_i+(C-A_i)=C.
\tag{25}
\]

A correct first-match compiler must emit and pay that planted cell.  The valid
negative conclusion is only:

```text
complete agreement + unique owners + global rim packing
does not imply dense-band complete-band restriction bound.
```

## 7. Rooted theorem sufficient for complete-band restriction bound

### Assumption 7.1 (rooted exponential excess-to-cell emission, rooted excess-to-cell emission)

For every fixed `$\eta>0$`, suppose an actual whole-slope residual and unpaid
complete band satisfy

\[
 \frac{L^{1-1/q}}M\|P_Af\|_q\ge e^{\eta N}.
\tag{26}
\]

Then the exact norming dual and owner map emit:

1. a positive-weight support `$S\in\Omega^\circ$`;
2. its unique surviving owner slope `$z=o(S)$`;
3. a canonical earlier atlas cell containing that same slope `$z$`;
4. the realized cell parameters and a validated distinct-slope projection
   payment.

The rooted requirement is essential.  A certificate for another or already
removed slope yields no contradiction.

### Theorem 7.2 (rooted excess-to-cell emission implies dense-band complete-band restriction bound)

If Assumption 7.1 holds uniformly, there is `$\epsilon_N\to0$` such that

\[
 \boxed{
 \|P_Af\|_q
 \le e^{\epsilon_NN}\frac M{L^{1-1/q}}
 }
\tag{27}
\]

for every actual unpaid profile-band pair.

### Proof

If (27) failed uniformly, some fixed `$\eta>0$` would satisfy (26) along an
infinite subsequence.  rooted excess-to-cell emission would return a support in the residual whose owner
slope belongs to an earlier paid cell.  Whole-slope first-match deletion would
have removed every later witness at that slope, contradicting
`$S\in\Omega^\circ$`.  Taking the supremum of the normalized logarithmic excess
over actual unpaid profile-band pairs gives `$\epsilon_N\to0$`.  (square)

The subexponential profile census does not prove uniformity.  It only preserves
an already uniform estimate when paid profiles and complete patterns are
summed.

## 8. Projected-energy gate

Put

\[
 E_A=\|P_Af\|_2^2,
 \qquad
 e_A=\frac{LE_A}{M^2},
 \qquad
 x_A=L\rho\delta_A.
\tag{28}
\]

Since `$\|P_Af\|_\infty\le W\delta_A$`, interpolation gives

\[
 \boxed{
 \frac{L^{1-1/q}}M\|P_Af\|_q
 \le e_A^{1/q}x_A^{1-2/q}.
 }
\tag{29}
\]

Thus the exact sufficient energy target is

\[
\boxed{e_Ax_A^{q-2}\le\exp(o(Nq)).}
\tag{30}
\]

Define the normalized band excess and projected-energy load by

\[
 \mathcal R_A=
 \frac{L^{1-1/q}}M\|P_Af\|_q,
 \qquad
 \mathcal Y_A=e_Ax_A^{q-2}.
\tag{31}
\]

Raising (29) to the `$q$`-th power gives the exact gate

\[
 \boxed{\mathcal R_A^q\le\mathcal Y_A.}
\tag{32}
\]

### Theorem 8.1 (owner-rooted projected-energy compiler)

Fix an actual source-derived profile, whole-slope first-match residual, and
complete character band. Assume the ownership, complete-agreement,
and rim-packing guards.

1. If `$\log^+(L\delta_A)=o(N)$` on the full slice, Corollary 5.1 pays the
   band.
2. For any sequence `$\varepsilon_N\to0$`, every remaining band with
   `$\mathcal Y_A\le e^{\varepsilon_NNq}$` satisfies

   \[
    \mathcal R_A\le e^{\varepsilon_NN}.
   \tag{33}
   \]

3. If, for some fixed `$\eta>0$`,

   \[
    \mathcal R_A\ge e^{\eta N},
   \tag{34}
   \]

   then

   \[
    \boxed{\mathcal Y_A\ge e^{\eta Nq}.}
   \tag{35}
   \]

   Moreover Propositions 2.1, 3.1, 3.2, 4.1, and Theorem 4.2 attach to that
   same band its exact norming dual, positive support weights, unique surviving
   owner map, complete-agreement-exact support records, and global
   `(a-1)`-rim packing.

### Proof

The sparse case is Corollary 5.1.  Equation (33) is the `$q$`-th root of
`$\mathcal R_A^q\le\mathcal Y_A$`.  Equation (35) is its contrapositive lower
bound under (34).  The rooted proof object is supplied without loss by the
earlier propositions.  (square)

The theorem is a reduction, not a dense-band estimate. It proves that every
unpaid dense band has fixed positive projected-energy rate and carries the
exact owner-rooted proof object required by a source-to-cell theorem.

Ordinary MDS/Johnson packing controls unprojected collision energy only at a
subexponential scale in the deep polynomial-field regime.  A successful energy
proof must be band-projected and source-sensitive, or emit a paid cell.

## 9. Positive-support and secant localization

The companion packets prove two exact refinements of Theorem 8.1.
First, an inherited complete-band restriction bound failure must retain the actual condition
`$\mathcal R_A\ge e^{\eta N}$`; high `$\mathcal Y_A$` alone does not imply it.
The exact norming dual then localizes with zero loss to the positive-support
count function `$b$`:

\[
 \|P_Ab\|_q\ge\Omega_+\ge\|P_Af\|_q,
 \qquad
 \|P_Ab\|_2^2\ge\Omega_+^2.
\]

This emits rooted frequency and physical-pair packets. Same-syndrome
collisions give quantitative exact source trades. In the remaining flat
branch, two distinct positive syndromes generate a cyclic subgroup
`$K=\langle u\rangle$`; one symmetric packet in at most six `$K^\perp$`-cosets
retains

\[
 \mathcal R_{A'}(b)\ge\frac{\mathcal R_A(f)}{\operatorname{ord}(u)},
 \qquad
 \mathcal Y_{A'}(b)\ge
 \frac{\mathcal Y_A(b)}{\operatorname{ord}(u)^{q-1}},
 \qquad
 |A'|\ge\frac{|A|}{\operatorname{ord}(u)}.
\]

These losses are compiler-grade when
`$\log\operatorname{ord}(u)=o(N)$`; for additive profile groups over
`$\mathbb B$`, it suffices that `$\log\operatorname{char}\mathbb B=o(N)$`.

Two specification guardrails remain load-bearing. The block-diagonal rank
drop obtained from each explaining polynomial is automatic for every witness,
so it is not a semantic rank cell. Likewise, every nonzero source secant has
a cyclic annihilator, so the six-coset packet is not yet a canonical paid
quotient cell. The exact localization is proved; the source-specific atlas
conversion is not.

## 10. What remains open

The primitive signed-payment audit proves that a five-way semantic conversion is not a
routine consequence of the localized packet. A single overloaded source-fiber
mask produces a complete-band restriction failure, so a *hereditary*
source-algebraic emission theorem would imply
a source-algebraic heavy-fiber inverse theorem. For the whole residual, an
additional admissibility/transfer lemma is required before applying source-algebraic emission to
that point mask.

The corrected interface is a charge-preserving rooted semantic-or-signed
dichotomy. It must either emit a semantic source packet or pay the packet by a
one-sided signed minor estimate. The charge decomposition must be nonnegative
and exact; retained q-excess yields

\[
 \mathcal Y_B\ge\mathcal R_B^q
 \ge e^{\eta Nq-o(Nq)},
\]

but does not imply relative retention of the original `$\mathcal Y_A$`.

An abstract dense-idempotent construction shows that harmonic, subset-sum,
rim-packing, and light-fiber assumptions alone do not prove the signed branch
for `$q>2$`: an arbitrary kernel-sign mask attains normalized gain
`$L^{1/2-1/q}$`. This is not a source-semantic counterexample. Its columns are
not proved weighted Vandermonde, its orbit union is not one complete dyadic
`$|\tau|$` band, its mask is not a first-match residual, and its separately
assigned owner words are not one received affine line. The construction is a
mandatory guardrail showing exactly where source realizability must enter.

The packing estimate is support-combinatorial. It does not by itself control
the dense-band projection.  The remaining proof obligations are:

```text
Heavy-fiber interface:
  prove hereditary mask admissibility or a source-algebraic heavy-fiber inverse.
Signed nonstructure payment:
  prove the charge-preserving semantic-or-signed dichotomy.
Atlas conversion:
  emit exact quotient, planted, field, rank, or saturation data accepted by (CAT).
Same-owner payment:
  verify that the emitted paid cell contains the positive-weight owner slope.
```

The correct downstream statement is

\[
 \boxed{
 \text{finite owner-rooting + projected-energy gate + semantic source-to-cell emission}
 \Longrightarrow
 \text{dense complete-band payment}
 \Longrightarrow
 \text{the top-order compiler of the mask-aware packet}.
 }
\]

No A4 or primitive-Q status is promoted by this packet.
