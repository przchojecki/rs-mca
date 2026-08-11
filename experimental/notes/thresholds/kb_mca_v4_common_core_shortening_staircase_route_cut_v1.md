# KoalaBear v4 common-core shortening staircase route cut

**Status:** candidate proved local theorem and maximal route cut; no global
ledger movement.  Independent review is required before this packet may be
banked.

## 1. Exact scope and units

This note is pinned to commit
`c5f4ea7a0c78828c901ae5f3428894a8b2e2806b` (PR #1160 head) and to the
active KoalaBear MCA row

\[
(n,k,m,d,R,t)=(2097152,1048576,1116048,67472,1048576,981104),
\]

with target

\[
B_*=274980728111395087.
\]

Every count below is in **distinct finite affine bad slopes on one actual
received line**.  A support, explanation, local 32-tuple, common core,
locator, endpoint label, or shortening set is not a slope.

The source-bound inputs are:

- `tex/cs25_cap_v13_2.tex`, lines 215--226, for the deployed
  support-wise MCA predicate;
- `experimental/grande_finale.tex`, lines 132--149, 1395--1426,
  4724--4735, 5744--5781, 6040--6048, 6050--6135, 6622--6651,
  7082--7110, and 7585--7617;
- `experimental/notes/thresholds/common_core_cover_obstruction.md`,
  Theorem 2.1;
- `experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md`,
  which supplies the sharp local `2d=134944` near-rational bound but no
  S/A/E ledger allocation.
- `RS_MCA_Paving_v9.2.tex`, lines 2255--2309 and 2365--2397, reproducing
  Jo's slope-preserving shortening transfer and the telescoping-cost fence.

The three different source notions called “common support” must not be
identified:

1. one support simultaneously explaining the received pair in exact
   sparsification;
2. the intersection of the maximal agreement supports of one selected
   explanation family;
3. a common GCD in a locator pencil.

This packet concerns only (2).

## 2. Exact cancellation theorem

Let

\[
C_{\rm RS}=\operatorname{RS}[\mathbb F,D,k],\qquad |D|=n,
\qquad r_\gamma=r_0+\gamma r_1.
\]

Fix distinct slopes `gamma_i`, degree-`<k` explaining polynomials `h_i`,
and their maximal agreement supports

\[
\widehat S_i=\{x\in D:h_i(x)=r_0(x)+\gamma_i r_1(x)\}.
\]

Assume each slope has an actual size-`m` support-wise noncontained witness
inside its maximal support.  Put

\[
C=\bigcap_i\widehat S_i,\qquad c=|C|,
\qquad G_C(X)=\prod_{x\in C}(X-x).
\]

### Theorem 2.1 (same-record common-core cancellation)

If the explanations are not globally affine, then `c<k`.  Let `a_0,a_1`
be the unique degree-`<c` interpolants of `r_0,r_1` on `C` (zero when
`c=0`).  On `D'=D\setminus C` define

\[
r'_j(x)=\frac{r_j(x)-a_j(x)}{G_C(x)},\qquad
h'_i(X)=\frac{h_i(X)-a_0(X)-\gamma_i a_1(X)}{G_C(X)}. \tag{2.1}
\]

Then:

1. `deg h'_i<k-c`, and its maximal agreement support is exactly
   `widehat S_i\setminus C`.
2. There is an actual size-`m` noncontained witness `T_i` with
   `C subset T_i subset widehat S_i`; hence `T_i\setminus C` is an actual
   size-`m-c` noncontained witness in the shortened row.
3. Simultaneous explanation on the identical support is equivalent in both
   directions under

   \[
   (p_0,p_1)=(a_0+G_Cp'_0,a_1+G_Cp'_1). \tag{2.2}
   \]

4. This is a typed reversible adapter from the original record on `D` to a
   shortened record on `D\setminus C`.  It preserves the finite affine slope,
   field of definition, and the declared correspondences between explaining
   data, maximal supports, and same-support noncontainment.  It does **not**
   preserve literal identity of the received line, carrier, explanation, or
   support across the two rows; the displayed inverse reconstructs those
   original objects.
5. The shortened row is

   \[
   (n',k',m')=(n-c,k-c,m-c)=(R+s,s,d+s),\qquad s=k-c, \tag{2.3}
   \]

   so `m'-k'=d`, `n'-k'=R`, and `n'-m'=t`.
6. Global-affine certificates and the **algebraic identities** in
   scalar-locator certificates transport in both directions.  Original-to-
   shortened transport preserves denominator nonvanishing.  The reverse
   direction requires the additional guard `Q(x) != 0` on every deleted
   point `x in C`; nonvanishing only on `D\setminus C` is insufficient.
   Exact-support two-cover complexity satisfies

   \[
   \chi(\mathcal T)=\chi(\mathcal T')+2c,
   \qquad
   3m-k+3=(3m'-k'+3)+2c. \tag{2.4}
   \]

#### Proof

The source's maximal-support slope-degree theorem proves `c<k` in the
non-affine case.  Each numerator in (2.1) vanishes on all roots of the
squarefree locator `G_C`, so the quotients are polynomials of the declared
degrees.  Off `C`, division by the nonzero value `G_C(x)` preserves equality
pointwise; this proves the maximal-support statement and the inverse.

For the same-witness clause, suppose every size-`m` subset of
`widehat S_i` containing `C` were pair-contained.  These subsets form a
connected exchange graph.  Adjacent subsets overlap in `m-1>=k`
coordinates, so RS injectivity makes their explaining codeword pairs
identical.  One fixed pair would then explain their union, namely all of
`widehat S_i`, contradicting the assumed actual noncontained witness in
that maximal support.  Thus a noncontained `T_i` containing `C` exists, and
(2.2) preserves noncontainment in both directions.

The parameter identities are immediate from (2.3).  If

\[
Qh'_i+(c_0+c_1\gamma_i)\Lambda'_i=A'+\gamma_iB',
\]

then `Lambda_i=G_C Lambda'_i` and multiplication by `G_C`, followed by
adding `Qa_0+gamma_i Qa_1`, gives the original certificate.  Conversely,
evaluating an original certificate on `C` at two distinct slopes shows
that `A-Qa_0` and `B-Qa_1` are divisible by `G_C`.  Finally, every common
point contributes two to the two-cover sum, proving (2.4).  This completes
the proof.

### Converse hardness embedding

The compiler is not a one-way simplification.  Given a shortened record on
`(D',s,d+s)` over a field containing `c=k-s` additional distinct evaluation
points, adjoin those fresh coordinates as `C`, choose `a_0,a_1`, and use the
inverse in (2.2).  It produces an original common-core record with exactly
the same slopes and same-support badness.  (The deployed KoalaBear field has
ample compatible points.)  Therefore uniform common-core routing contains
the complete compatible staircase of shortened RS--MCA problems; “divide
the core and declare it paid” is false.

## 3. Exact KoalaBear staircase

For 32 explanations, the post-cancellation slope-degree floor is

\[
r_{\min}(c)=\left\lceil\frac{32(m-c)}{n-c}\right\rceil.
\]

The deployed degree-18 interface survives precisely when

\[
32(m-c)>17(n-c)\iff 61952>15c,
\]

so the exact last core size is `c=4130`; at `c=4131` the floor is 17.
At `c=k-1` the floor is 3.  The deployed constants in
`thm:partial-relative` therefore cannot be reused uniformly after
cancellation.

For one fixed maximal core, the source-bound support/secant compiler gives

\[
B_{\rm cell}(s)=
\min\left\{\binom{R+s}{d+s},\binom{R+s}{s+1}\right\}.
\]

It fits through `s=2` and first fails at `s=3`:

| `s` | `B_cell(s)` | `B_* - B_cell(s)` |
|---:|---:|---:|
| 1 | 549756338176 | 274980178355056911 |
| 2 | 192154133857304576 | 82826594254090511 |
| 3 | 50372197381489643749376 | -50371922400761532354289 |

If the shortened direction is list-separated, the affine-span MCA compiler
applied to the full `s`-dimensional shortened code gives

\[
J_s=\left\lfloor\prod_{i=0}^{s}\frac{R+i}{d+i}\right\rfloor.
\]

The exact boundary is

\[
J_{13}=47876303026096432<B_*,\qquad
J_{14}=743896698428332665>B_*.
\]

Thus a **fixed-family** common-core terminal is paid if it is globally
affine; if `s<=2`; or, under direction separation, if `3<=s<=13`.
The first honest residual labels are

- `DIRECTION_LIST_SHORTENED_s` for `3<=s<=13` when separation fails;
- `COMMON_CORE_SHORTENED_s_GE_14` for `s>=14`.

These labels are residuals, not owners.

## 4. Why existing shortening does not close the route

Jo's agreement-set shortening transfer preserves slopes but pays the
double-counting factor

\[
\frac{\binom nc}{\binom mc}.
\]

At the first degree-drop core `c=4131`, exact integer arithmetic gives

\[
\binom n{4131}>B_*\binom m{4131}.
\]

The ceiling of that multiplier already has 3765 bits (1134 decimal
digits), even before multiplying by any positive shortened numerator.
Therefore the published transfer theorem cannot pay the first uncovered
core in the frozen KoalaBear units.  Splitting the shortening into stages
does not help because the binomial ratios telescope.

This is a budget obstruction to that theorem, not a proof that every
possible common-core compiler must fail.

## 5. Global chronology route cut

The active source applies `thm:partial-relative` only after the local
common-core branch is removed, but it does not supply a line-level selector
that partitions varying local 32-tuple cores into disjoint slope terminals.
Summing `B_cell(s)` or `J_s` over core choices is invalid: it changes the
maximum-type v4 endgame into an enormous additive support census.  The
converse embedding above also rules out zero-cost deletion.

The first missing bridge for **this staircase-payment route** is therefore:

> For every actual first-match non-affine common-core 32-record, construct a
> total chronology-correct selector that either assigns its identical slope
> to a named earlier owner, or places it in one disjoint fixed-core family
> to which the staircase payment applies, or emits one of the two explicit
> residual labels above.  The projection fibers and add-back multiplicities
> must be derived in distinct-slope units.

Until that theorem is proved, neither the `2d` near-rational theorem nor the
fixed-family payments move `U_S`, `U_A`, `U_E`, or the global KoalaBear
ledger.  The exact output of this packet is

\[
U_{\rm ledger\ movement}=0,
\]

with a sharp first local numerical wall at `s=14` and a sharp deployed
degree-interface wall at `c=4131`.

An alternative same-owner maximum-type theorem could bypass the fixed-core
forest entirely.  This packet proves that the displayed staircase route
needs the bridge above; it does not claim that this selector is the unique
possible global repair.

## 6. Controls and nonclaims

- The #1160 67,472-slope construction is not deleted.  It is globally
  affine and separately near-rational owned.
- The exact GF(17) degree-two atom cancels from `(8,4,6)` by the core
  `{1,15}` to `(6,2,4)` while preserving all five slopes and identical-
  support noncontainment.  Puncturing without lowering `k` destroys this
  control.
- The exact GF(7) near-rational census attains `2d`; cancellation preserves
  `(d,R,t)`, so it supplies no uniform improvement to that payment.
- No layer cake, dyadic summation, moment, Markov, Chebyshev, asymptotic
  estimate, random-domain inference, K3 elimination, or witness-to-slope
  conversion is used.
- This packet does not prove S, A, E, KoalaBear closure, or the universal
  four-rate prize statement.

## 7. Required next attack

Build the source-bound common-core forest compiler on actual explanation
states.  Its hostile controls are the #1160 line and the inverse-lifted
GF(17) atom.  Every selected slope must terminate exactly once in an earlier
owner, a paid fixed-core family, `DIRECTION_LIST_SHORTENED_s`, or
`COMMON_CORE_SHORTENED_s_GE_14`.  The smallest actual selector collision is
the preferred falsifier if the compiler is false.
