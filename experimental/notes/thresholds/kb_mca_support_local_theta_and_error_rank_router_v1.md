---
workboard_item: K3-K4
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
status: PROVED_SUPPORT_LOCAL_REFINEMENT_AND_ROUTE_CUT
impact: POST_1165_LOCAL_MARGIN_AND_DIRECT_NUMERATOR_REDUCTION
direct_statement: "Beyond #1165's global direction-distance repair, the exact selected-support margin theta gives a sharper compiler. Combined with a reversible codeword gauge, it pays every post-deletion KoalaBear family through affine error rank nine and routes ranks ten through twelve to exact direction-exception terminals."
claimed_bound: "110390969172308040 through post-deletion affine error rank nine whenever the deleted stratum has size at most 2w, with signed slack 164589758939087047"
global_ledger_movement: 0
KoalaBear_closed: false
---

# Support-local affine-span refinement and error-rank router

## 1. Verdict and scope

PR #1165 refutes the former affine-span MCA compiler, installs the safe
global proper-subspace replacement with final factor
`L=max(1,e-(n-m))`, where `e` is the full-code distance of the line
direction, and now includes a full-explanation lifted-rank gauge dichotomy
and a sparse-direction punctured-Johnson profile with a centered-Gram
continuation.  This successor does not
duplicate those results.  It proves the sharper record-local factor

```text
theta=min(w+1,min_(gamma,b in C') |{x in S_gamma:r1(x)!=b(x)}|),
```

for supplied exact same-support-noncontained records, relates `theta` to
`L`, and composes it with a reversible error-rank gauge.

This packet does four things.

1. It independently replays the failure on a smooth `GF(257)` domain; this
   is a regression complementary to #1165's `GF(1009)` fixture.
2. It proves the support-local `theta` refinement and the exact comparison
   `theta>=L`.
3. It extends #1165's full-explanation gauge existence to every selected
   error rank, lowering explanation rank from `a` to `a-1`.
4. Conditional on any disjoint deleted stratum of size at most `2w`—as
   supplied by PR #1160 when that dependency is present—it obtains the
   strongest direct KoalaBear route cut justified by these inputs.

The result is not a KoalaBear closure.  It makes no S/A/E first-match
identification, uses no 31-slope exception reserve, and moves no deployed v4
atom.  It is a direct theorem about distinct affine bad slopes on one actual
received line.

## 2. Independent smooth-domain regression for #1165

Work over the smooth multiplicative domain

\[
 C=\operatorname{RS}[\mathbb F_{257},\mathbb F_{257}^{\times},1],
 \qquad (n,K,m,w,s)=(256,1,86,85,1).
\]

The code consists of constant words.  In the two-dimensional parameter
plane with coordinates `(gamma,lambda)`, take

\[
 p_i=(i,0)\quad(0\le i\le85),
 \qquad p_\star=(86,1).
\]

A coordinate of the received line is an affine parameter-line

\[
 \lambda=a+\gamma b,
 \qquad r_0(x)=a,\quad r_1(x)=b.
\]

Use exactly 256 coordinates:

- 85 copies of `lambda=0`;
- the 86 connectors from `p_i` to `p_star`, with
  \[
  b_i=(86-i)^{-1},\qquad a_i=-i(86-i)^{-1};
  \]
- 85 lines avoiding every selected parameter point, with nonzero direction
  coefficients distinct from the connector coefficients.

For each `p_i`, the exact agreement support consists of the 85 copies of
`lambda=0` plus its connector.  For `p_star`, it consists of all 86
connectors.  Assign constant explanation zero at the first 86 points and
constant explanation one at `p_star`.  Thus there are 87 distinct slopes,
each with an exact 86-point explanation, and the explanations have affine
rank one.

Every support is pair-noncontained.  For a dimension-one RS code,
simultaneous containment would require both `r_0` and `r_1` to be constant
on the identical support.  The ordinary supports contain the common normal
`(0,-1)` and a connector normal with nonzero first coordinate; the star
support contains 86 distinct connector directions.  Every incident-normal
matrix therefore has rank two.

The original global separation hypothesis also holds:

\[
 \max_{b\in C}\operatorname{agr}(r_1,b)=85<86=m.
\]

Every selected received word has distance at least 170 from the constant
code, strictly outside the near-rational radius `w=85`.  Nevertheless the
two terms in the printed `s=1` bound are both

\[
 \left\lfloor\frac{256\cdot255}{86\cdot85}\right\rfloor=8,
\]

contradicting the 87 exact slopes.

## 3. The first false inference

Choose a basis `c_1,...,c_s` for the explanation direction space.  The
coordinate normal is

\[
 v_x=(r_1(x),-c_1(x),\ldots,-c_s(x))\in\mathbb F^{s+1}.
\]

After `r` independent normals have been selected, let `W` be their span.
The old proof studies `W^perp`, of dimension `s+1-r`.  When the slope
coordinate is nonzero on `W^perp`, its kernel has dimension `s-r`.  This
supplies Reed--Solomon codeword equations only while `r<s`.

At the final step `r=s`, the kernel has dimension zero.  The coordinates
whose normals lie in `W` satisfy only

\[
 r_1(x)=b(x)
\]

for one codeword `b` in the explanation direction space.  Global direction
separation bounds this fiber by `m-1`, not by `K`.  In the counterexample,
the normal line `W=span(0,-1)` has occupancy 85 although the proof claims at
most `K=1`.

Full incident rank does not repair this.  It only guarantees one final
normal outside `W`; it does not produce the missing factor `w`.

## 4. Correct support-transverse compiler

Assume `n>=m=K+w`, `w>0`, and let `A=c_0+C'` be an affine subspace of
the RS code with `1<=dim C'=s<=K`.  For each slope in a nonempty set of
distinct `gamma`, retain an exact `m`-set `S_gamma`, an
explanation `c_gamma in A`, and same-support pair noncontainment.  Define

\[
 \theta_0=
 \min_{\gamma\in Z}\min_{b\in C'}
 |\{x\in S_\gamma:r_1(x)\ne b(x)\}|,
 \qquad
 \theta=\min\{\theta_0,w+1\}.
\]

Pair noncontainment gives `theta>=1`: if `r_1=b` on `S_gamma`, then
`(c_gamma-gamma b,b)` explains the received pair on that same support.

### Theorem 4.1 (quantitative support-transverse affine-span bound)

Under these hypotheses,

\[
 |Z|\le\left\lfloor\max\left\{
 \frac{n^{\underline{s+1}}}
      {m\theta(w+1)^{\overline{s-1}}},
 \frac{(n-K+s)^{\underline{s+1}}}
      {\theta(w+1)^{\overline s}}
 \right\}\right\rfloor. \tag{4.1}
\]

The first rising product is empty when `s=1`.

Whenever a gauge changes the containing affine explanation space, `theta`
is recomputed in its translated direction space; it is not inherited from
the ungauged presentation.

### Proof

Let `z` be the number of zero normals and `g<=z` the number that are
identically incident.  The usual polynomial-space argument gives
`z<=K-s`.  Every parameter point has `m-g` incident nonzero normals.

After `r` independent incident normals have been chosen with `1<=r<s`,
the valid common-zero argument leaves at least

\[
 w+s-r
\]

incident normals outside their span.  At `r=s`, let `(delta,mu)` generate
the annihilator.

- If `delta=0`, a nonzero degree-`<K` codeword vanishes on every normal in
  the span.  Removing the zero normals leaves at least `w+1>=theta`
  incident choices outside.
- If `delta` is nonzero, put
  `b=delta^{-1} sum_i mu_i c_i in C'`.  The definition of `theta` supplies
  at least `theta` points of the actual support whose normals lie outside
  the span.

Thus each parameter point owns at least

\[
 (m-g)\theta(w+1)^{\overline{s-1}}
\]

ordered full-rank coordinate tuples.  A full-rank tuple determines at most
one parameter point, so

\[
 |Z|\le
 \frac{(n-z)^{\underline{s+1}}}
 {(m-g)\theta(w+1)^{\overline{s-1}}}. \tag{4.2}
\]

For fixed `z`, the ratio is largest at `g=z`.  Its successive ratio in `z`
changes sign at most once, from decreasing to increasing, because its sign
is the sign of

\[
 n-(s+1)m+sz.
\]

Hence the maximum is at `z=0` or `z=K-s`.  These endpoints give (4.1).

For the `GF(257)` fixture, (4.1) gives 759, so the 87-slope family is now a
positive regression rather than a contradiction.

## 5. Exact error-rank gauge

For selected explanations `h_gamma`, put

\[
 e_\gamma=r_0+\gamma r_1-h_\gamma,
 \qquad
 a=\dim\operatorname{span}\{e_\gamma-e_{\gamma_0}\}.
\]

Same-support noncontainment implies `r_1` is not a codeword.  Therefore the
map

\[
 (\delta,c)\longmapsto\delta r_1-c
\]

is injective on the span of the pairs
`(gamma-gamma_0,h_gamma-h_gamma_0)`.  That pair space has dimension `a`,
and its slope projection is nonzero.  Choose `(1,b)` in it.  The reversible
translation

\[
 r'_1=r_1-b,
 \qquad h'_\gamma=h_\gamma-\gamma b
\]

preserves every slope, error word, agreement support, and same-support
containment predicate.  The transformed explanation differences are the
kernel of the slope projection, so their affine dimension is exactly
`a-1`.

This is a proof-coordinate adapter.  It generally changes the literal
received-line representative.  The inverse adds `b` back, so a direct
maximum-over-lines count is preserved; representation-dependent v4 owner
predicates must not be recomputed after the gauge without a separate
theorem.

Write the gauge codeword as `b_0`.  If local-margin failure on the
translated line produces `b_1` in its explanation direction space, then
`r'_1=r_1-b_0` agrees with `b_1` away from the exception set.  The terminal
on the original complete record is therefore the codeword `b_0+b_1`, with
the identical support and identical exception coordinates.

At full explanation rank `K`, the lifted pair space has dimension `K` or
`K+1`; this gives the two rank outcomes already classified more sharply by
#1165, which describes all gauges.  The new use here is the arbitrary-rank
adapter needed for the direct post-near error-rank router.

## 6. Exact deployed consequences

### 6.1 Full KoalaBear code

With only `theta>=1`, the repaired bound gives:

| explanation rank `s` | cap | fits `B*` |
|---:|---:|:---:|
| 1 | 16,295,594 | yes |
| 2 | 253,241,283 | yes |
| 3 | 3,935,435,218 | yes |
| 4 | 118,319,201,475 | yes |
| 5 | 3,677,348,367,069 | yes |
| 6 | 114,289,853,114,503 | yes |
| 7 | 3,552,007,973,114,420 | yes |
| 8 | 110,390,969,172,173,096 | yes |
| 9 | 3,430,729,820,133,944,932 | no |

After the exact near-rational deletion `2w=134944`, the least local margins
that pay the former rank range are:

| `s` | least `theta` | repaired cap | cap plus `2w` | slack |
|---:|---:|---:|---:|---:|
| 8 | 1 | 110390969172173096 | 110390969172308040 | 164589758939087047 |
| 9 | 13 | 263902293856457302 | 263902293856592246 | 11078434254802841 |
| 10 | 388 | 274790124064526354 | 274790124064661298 | 190604046733789 |
| 11 | 12050 | 274970108028773601 | 274970108028908545 | 10620082486542 |

At the preceding margins, the totals are respectively

```text
s=9,  theta=12:    285894151677963688
s=10, theta=387:   275500176064828033
s=11, theta=12049: 274992929018868606
```

Combining the gauge with `s=a-1` proves the direct route:

```text
post-near affine error rank a <= 9
    -> total bad slopes <= 110390969172308040 < B*;

a = 10,11,12 and the line is over budget
    -> an actual selected support has at most 12,387,12049
       direction exceptions, respectively, for the inverse-gauge
       codeword b_0+b_1;

a >= 13
    -> no payment from this compiler.
```

The rank-zero and rank-one edge cases do not use (4.1).  Two distinct
slopes force error rank at least one.  At rank one, the gauged explanations
coincide; every noncontained support contains a noncommon coordinate, and
each such coordinate belongs to at most one slope, giving the sufficient
bound `|Z|<=n`.

### 6.2 Support-local calibration on a shortened complete code

For a fixed common core, cancellation produces the complete shortened row

\[
 (n',K',m')=(R+s,s,d+s).
\]

The former `J_13` direction-separated payment used the false final factor.
With the support-local theorem and automatic `theta>=1`, the exact shortened
caps fit through `s=9`, not `s=13`:

| `s` | repaired cap at `theta=1` | fits `B*` |
|---:|---:|:---:|
| 8 | 3,566,101,912,297,072 | yes |
| 9 | 55,413,538,236,037,195 | yes |
| 10 | 861,057,176,799,343,503 | no |

At `s=10,11,12,13`, the least paying support margins are respectively

\[
 4,\quad49,\quad757,\quad11748.
\]

Thus the sound fixed-core terminals are now:

```text
SHORTENED_SUPPORT_TRANSVERSE_PAID_s_LE_9
SHORTENED_DIRECTION_EXCEPTIONS_LE_3_AT_s10
SHORTENED_DIRECTION_EXCEPTIONS_LE_48_AT_s11
SHORTENED_DIRECTION_EXCEPTIONS_LE_756_AT_s12
SHORTENED_DIRECTION_EXCEPTIONS_LE_11747_AT_s13
COMMON_CORE_SHORTENED_s_GE_14
```

The cancellation theorem itself is unaffected.  PR #1165's newer
full-lift, punctured-Johnson, centered-Gram near-Johnson, and mean-centered
Gram routes remain separate, compatible refinements
of the top shortened cells.  The invalidated pieces are
the direction-separated payment in #1163, the corresponding imported
terminal in #1164 Theorem 4.1, public-DAG node `3a13f2d`, and downstream
numerical conclusions that use that node's old formula, including the
rank-wall part of `60db12dc` and the nonempty-core composition `fc74e16c`.
Their independent algebraic or set-theoretic sublemmas are not refuted.

### 6.3 Mersenne-31 stress-test row

After `2w=134896`, the least margins at explanation ranks one through four
are

\[
 1,\quad16,\quad237,\quad7118.
\]

Same-support noncontainment alone therefore pays only rank one on that row.
This is a stress-test consequence, not a `2^-128` Mersenne prize claim.

## 7. Chronology and ownership

The direct Koala route uses only the intrinsic partition

\[
 Z_{\rm bad}=Z_{\rm near}\sqcup
 (Z_{\rm bad}\setminus Z_{\rm near}),
 \qquad |Z_{\rm near}|\le2w.
\]

It does not add the conditional 31-slope exception reserve.  It does not
claim that a gauged representative has the same Q/BC/S/A/E owner.  The
original complete records are selected before gauging; the gauge is used
only to count the identical set of slopes and supports on a translated
received line, with an explicit inverse.

The active v4 source still lacks an executable first-match S/A/E residual at
this joint.  That underdetermination is irrelevant to the direct rank-ten
route cut but continues to block ledger insertion.

## 8. Evidence and controls

The sealed release certificate contains:

- a self-contained Python reconstruction of all 256 coordinates and 87
  records;
- an independent Sage reconstruction over `GF(257)`;
- exact endpoint optimization over 10,716 legal small parameter profiles;
- exact KoalaBear, shortened-row, and Mersenne-31 arithmetic;
- an exact Sage gauge control on the `GF(257)` regression, including the
  error identity, one-rank drop, and literal inverse;
- a FLINT rational-arithmetic replay;
- a Wolfram exact-integer and modular-incidence replay;
- hostile mutations for the old final factor, missing `theta`, adjacent
  nonpaying margins, altered support counts, and custody hashes.

During theorem discovery, separate `GF(11)`, `GF(17)`, and 90-family
adversarial controls were also run.  They are research-campaign evidence,
not part of the sealed release certificate and are not used as proof.

The Exa literature sweep covered finite-field point--hyperplane incidence,
design-matrix rank bounds, and rich-flat estimates.  It found useful general
context but no primary-source theorem that supplies the missing
support-local final transversality factor for these RS records; no external
lemma is imported.

## 9. Remaining frontier

The maximal surviving theorem is no longer a generic rank computation.  It
is the exact direction-exception forest:

> On every over-budget post-near family of selected error rank 10, 11, or
> 12, classify the actual record/codeword pair whose exact `m`-support has at
> most 12, 387, or 12,049 direction exceptions.  Prove a disjoint
> same-owner common-core/shortening payment, or emit the first actual
> primitive component.

Rank at least 13 remains a separate high-rank terminal.  Neither terminal is
forced into an existing owner by this packet.
