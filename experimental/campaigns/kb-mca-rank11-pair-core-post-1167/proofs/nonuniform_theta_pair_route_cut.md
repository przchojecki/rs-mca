# Nonuniform-theta and fixed-pair route cut

Status: candidate local theorem.  This proves a stronger structural terminal
for post-near error rank eleven, but it does not pay that rank or move an
active-v4 atom.

## 1. Pointwise resource inequality

Retain the notation of the support-transverse affine-span MCA compiler.  For
each selected slope define its own margin

\[
 \theta_\gamma=\min\left\{w+1,
 \min_{b\in C'}|\{x\in S_\gamma:r_1(x)\ne b(x)\}|\right\}.
\]

Then

\[
 \sum_{\gamma\in Z}\theta_\gamma\le C_s,
 \qquad
 C_s=\left\lfloor\max\left\{
 \frac{n^{\underline{s+1}}}{m(w+1)^{\overline{s-1}}},
 \frac{(n-K+s)^{\underline{s+1}}}{(w+1)^{\overline s}}
 \right\}\right\rfloor. \tag{1}
\]

This is not obtained by summing the printed minimum-margin theorem.  It is a
pointwise strengthening of its ordered-basis proof.  With the proof's global
zero-normal parameters `z` and `g`, each individual parameter point owns at
least

\[
 (m-g)\theta_\gamma(w+1)^{\overline{s-1}}
\]

ordered full-rank coordinate tuples.  A tuple determines at most one
parameter point.  Summing before taking a minimum gives

\[
 \sum_\gamma\theta_\gamma\le
 \left\lfloor
 \frac{(n-z)^{\underline{s+1}}}
 {(m-g)(w+1)^{\overline{s-1}}}
 \right\rfloor.
\]

For fixed `z` the right side is largest at `g=z`; the same successive-ratio
calculation as in the source proof puts its maximum over
`0<=z<=K-s` at `z=0` or `z=K-s`.  These are exactly the two terms in (1).
No uniformity of the extension count is assumed.

## 2. Low-pair weighted incidence

Fix `tau` with `1<=tau<=w-1`.  For every record with
`theta_gamma<=tau`, choose a minimizing `b_gamma` and set

\[
 a_\gamma=h_\gamma-\gamma b_\gamma,
 \qquad \lambda_\gamma=\tau+1-\theta_\gamma.
\]

Every `(a_gamma,b_gamma)` agrees with the received pair on at least
`m-tau` coordinates.  If

\[
 Q_s(\tau)=\left\lfloor
 \frac{\binom{n-K+s}{s}}{\binom{w-\tau+s}{s}}
 \right\rfloor,
 \qquad Q_s(\tau)^2<|\mathbb F|,
\]

the ordinary affine-span theorem and sub-square interleaving collapse imply
that at most `Q_s(tau)` distinct ordered pairs occur.

Put `E=B_*-2w+1`.  If the original line has more than `B_*` bad slopes,
then its post-near family has at least `E` slopes.  By (1), the total weight
of the low records satisfies

\[
 W_\tau=\sum_{\theta_\gamma\le\tau}
 (\tau+1-\theta_\gamma)
 \ge (\tau+1)E-C_s. \tag{2}
\]

Indeed, add the nonnegative quantities
`tau+1-theta_gamma` for the low records and use
`sum theta_gamma<=C_s`; discarding the high-record cardinality only weakens
the result.  Pigeonholing (2) over the at most `Q_s(tau)` **ordered pairs**
gives one fixed pair with weight at least, whenever the numerator is
positive,

\[
 L_s(\tau)=\left\lceil
 \frac{\max\{0,(\tau+1)E-C_s\}}{Q_s(\tau)}
 \right\rceil. \tag{3}
\]

There is no factor two in (3).  Representing pairs as a bipartite graph has
at most `2Q_s` vertices but total endpoint degree `2W_tau`; equivalently,
the direct edge pigeonhole already gives (3).

## 3. Exact fixed-pair core terminal

For the fixed pair `(a,b)`, put

\[
 H=\{x:r_0(x)=a(x),\ r_1(x)=b(x)\},
 \qquad \delta=\max\{1,m-|H|\}.
\]

For every record assigned to this pair, its minimizing margin satisfies

\[
 \theta_\gamma=|S_\gamma\setminus H|\ge \delta.
\]

The sets `S_gamma\setminus H` are pairwise disjoint: outside `H`, the
equation

\[
 r_0(x)-a(x)+\gamma(r_1(x)-b(x))=0
\]

has at most one finite solution.  Hence one such pair has at most

\[
 \left\lfloor\frac{n-|H|}{\delta}\right\rfloor
 \leq\left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor
\]

records and total weight at most

\[
 P_\tau(\delta)=
 \left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor
 (\tau+1-\delta).
 \tag{4}
\]

Here the equality uses the fixed chosen minimizer: on the support,
`r_1-b` vanishes exactly at the points of `H`.  Notice that `H` need not be
contained in every support; only `S_gamma intersect H` is used.

For KoalaBear explanation dimension `s=10`, exact optimization of (3) gives

\[
 \tau=6486,qquad L_{10}(6486)=743449148.
\]

Comparison with (4) forces `delta<=8`, and the pair owns at least

\[
 \left\lceil\frac{743449148}{6486}\right\rceil=114624
\]

distinct slopes.  A second optimization maximizes the forced record count:

\[
 \tau=1795,qquad L_{10}(1795)=360132809,qquad
 \left\lceil\frac{L_{10}(1795)}{1795}\right\rceil=200632,
\]

and (4) then forces `delta<=4`.

Thus every over-budget error-rank-eleven line produces, separately for each
optimized cutoff, an actual fixed minimizing pair in the corresponding
certified terminal above.  The two supplied pairs need not coincide.  This is a
genuine common-core/global-code-line concentration, not distinct-neighbor
expansion.  It remains unpaid: the sharp parallel-star control permits
parallel records, and the direct bound
`floor((n-m+j)/j)` is still compatible with both terminals.

## 4. Complete coupled resource/core ceiling

The same pointwise resource inequality can be coupled to every cumulative
pair-list cap, instead of using only one cutoff.  For a distinct selected
low pair `e=(a,b)`, let

\[
 H_e=\{x:r_0(x)=a(x),\ r_1(x)=b(x)\},\qquad
 \delta_e=\max\{1,m-|H_e|\}.
\]

The identity in Section 3 gives `theta_gamma>=delta_e` for every record
owned by `e`.  Its disjoint exception sets give the multiplicity

\[
 c_\delta=\left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor. \tag{5}
\]

Fix one minimizing direction, and hence one pair type, for every selected
record once and before scanning `t` or `J`.  If `G(t)` is the number of
distinct selected pair types with
`delta_e<=t`, then each such pair agrees with the received pair on at least
`m-t` coordinates.  Consequently the same sub-square interleaving theorem
gives

\[
 G(t)\le Q_s(t). \tag{6}
\]

For a cutoff `J` satisfying `Q_s(J)^2<|F|`, monotonicity makes the field
guard valid at every `t<=J`.  Since `c_delta` decreases, Abel summation (or
the greedy integral LP) gives the uncoupled low ceiling

\[
 Q_s(1)c_1+\sum_{\delta=2}^J
 \bigl(Q_s(\delta)-Q_s(\delta-1)\bigr)c_\delta. \tag{7}
\]

There is a small but rigorous improvement over adding an independent high
cap to (7).  A low record of type `delta` consumes at least `delta` units of
the global resource (1), while a high record consumes at least `J+1`.
Thus the exact integral relaxation first fills the available record slots in
increasing `delta`; every low record is strictly more resource-efficient than
a high record.  If `R_J` and `L_J` are the resource and record totals from
that greedy fill, its exact ceiling is

\[
 U(J)=2w+L_J+
 \left\lfloor\frac{C_s-R_J}{J+1}\right\rfloor. \tag{8}
\]

The exchange proof is immediate: replacing a selected lower-cost record by
a high record cannot increase cardinality, and all cumulative pair-type
constraints are prefixes, so selecting the cheapest available types first
is integral-optimal.  Partial use of the final pair-type layer is allowed;
all statements are upper bounds on records, not existence assertions.

The exact KoalaBear scan of every legal cutoff has minimum

\[
\begin{aligned}
 J&=26033,\\
 Q_{10}(J)&=107486241601454,\\
 L_J&=811957734614064312,\\
 R_J&=106597778100457375003,\\
 \left\lfloor\frac{C_{10}-R_J}{J+1}\right\rfloor
   &=798572504373,\\
 U(J)&=811958533186703629.
\end{aligned}
\]

This remains above the target by

\[
 811958533186703629-274980728111395087
 =536977805075308542.
\]

Therefore even the **coupled** use of the nonuniform theta resource, every
cumulative interleaved pair-list cap, complete core deficiency, and the
sharp per-pair exception packing fails by a factor greater than `2.95`.
This is a certificate-class route cut, not a construction of a Reed--Solomon
extremizer.

## 5. Boundary and next theorem

The weakest useful next statement is now source-specific:

> Route every actual fixed minimizing pair with either `(delta<=8, weighted
> load>=743449148)` or `(delta<=4, record load>=200632)` to an existing
> chronology owner, or prove an additional collision bound across its
> disjoint exception sets.

The GF(11) constant-code star remains a mandatory negative control.  It
shows that (4), pair parallelism, and the absence of distinct-neighbor
expansion are real.  The next useful theorem must therefore couple
**different fixed pairs** (for example, by a chronology-correct owner for
overlapping dense cores) rather than re-price the same marginal resources.
No rank-eleven payment, active-v4 movement, KoalaBear closure, layer-cake
summability, or asymptotic inference is claimed.
