# Selected-owner unit layers: exact charge, source-free obstruction, and the remaining source inverse

## Status

```text
Status: PROVED exact slope-faithful layer charge identity (already compatible
        with the integrated charge theorem) + PROVED sparse-band unit payment
        (the integrated chart-free bound) + PROVED positive-rooted source-free
        dense-band obstruction + PROVED generic exact-witness line decoration
        with an explicit semantic-survival nonclaim + PROVED uniform
        SFULP <=> SULSI quantifier equivalence.

OPEN: selected-owner unit-layer source inverse (SULSI): a positive-rate unit-
      layer excess on an actual source chart must emit an earlier cell at one
      of the records actually selected by that layer.

LANE: image-scale MI/MA or direct Sidon payment.
```

This packet does not promote a theorem into the frontiers manuscript.  It
audits the exact boundary between the integrated pruned signed bound and the
remaining dense-band source inverse.

The current repository already proves two ingredients used below:

* `general_pruned_signed_bound.md` proves the universal unit-mask estimate
  \[
  \mathcal R_A(u)\le {L\over M}(L\delta_A)^{1/2-1/q};
  \]
* `charge_preserving_split_decomposition.md` proves that natural charges of
  every positive-rooted partition piece are exact pairings with the original
  norming dual and are bounded by the corresponding projected norm.

The new content is the source-free positive-rooting obstruction, the selected-
owner guardrail, and the precise source theorem still required in the dense
range.

Machine checks:

```text
experimental/scripts/verify_selected_owner_unit_layer_boundary.py
experimental/data/certificates/selected-owner-unit-layer-boundary/
  selected_owner_unit_layer_boundary.json
```

The larger source-line census is replayed separately by
`experimental/scripts/census_slope_faithful_multiplicity_layers.py`.
Its compact certificate stores aggregate and per-regime extrema plus
quantized SHA-256 commitments to every omitted line, analysis, and arbitrary-
mask control row.  The `--check` mode recomputes all 9,800 lines before
comparing those commitments.

---

## 1. Exact unit layers and their natural charge

Let `G` be a finite abelian group, `H=|G|`, and let
`Phi: Omega^0 -> G` be a source chart.  Put

```text
M = |Omega^0|,
L = |Phi(Omega^0)|.
```

For a residual support family, let

```text
f(s) = #{S in Omega^circ : Phi(S)=s}.
```

For a band `A subseteq hat G \ {0}`, write `P_A` for the self-adjoint Fourier
projection and

```text
R_A(h) = (L^(1-1/q)/M) ||P_A h||_q.
```

Fix an exact `P_A f`-norming dual `g`, so

```text
||g||_(q') = 1,
Re <P_A f,g> = ||P_A f||_q.
```

Define

\[
r(s)=\operatorname{Re}\overline{(P_Ag)(s)},
\qquad
\omega(S)=[r(\Phi(S))]_+.
\]

The positive count function is therefore

\[
b(s)=f(s)\mathbf1_{\{r(s)>0\}}.
\tag{1.1}
\]

Its unit layers are

\[
u_j(s)=\mathbf1_{\{b(s)\ge j\}}
      =\mathbf1_{\{f(s)\ge j\}}\mathbf1_{\{r(s)>0\}}.
\tag{1.2}
\]

At each syndrome, order the actual residual records canonically and attach the
`j`-th record `(S_{s,j},o(S_{s,j}),h_{S_{s,j}})` to `u_j(s)=1`.  The syndrome
mask `u_j` is independent of this ordering, but the attached owner is not.

The natural charge of the layer is

\[
\begin{aligned}
c_j
&=\sum_{s:b(s)\ge j}\omega(S_{s,j})\\
&=\sum_su_j(s)r(s)\\
&=\operatorname{Re}\langle u_j,P_Ag\rangle\\
&=\operatorname{Re}\langle P_Au_j,g\rangle.
\end{aligned}
\tag{1.3}
\]

Consequently,

\[
0\le c_j\le\|P_Au_j\|_q,
\tag{1.4}
\]

and, exactly,

\[
b=\sum_{j=1}^{b_{\max}}u_j,
\qquad
\sum_jc_j=\sum_{S:\omega(S)>0}\omega(S).
\tag{1.5}
\]

This is the unit-layer specialization of the integrated natural-charge theorem.
It is recorded here because the selected-owner issue in Section 6 is invisible
if charges are detached from their actual layer records.

---

## 2. The complete source-free estimate

Let

\[
\delta_A={|A|\over H},
\qquad
K_A(x)={1\over H}\sum_{\gamma\in A}\gamma(x).
\]

For any unit mask `u=1_E` with `|E|<=L`, projection contraction and Parseval
give

\[
\|P_Au\|_2\le\sqrt L,
\qquad
\|K_A\|_2^2=\delta_A.
\tag{2.1}
\]

Cauchy--Schwarz gives

\[
\|P_Au\|_\infty
\le\sqrt{L\delta_A}.
\tag{2.2}
\]

Interpolating between (2.1) and (2.2),

\[
L^{-1/q}\|P_Au\|_q
\le (L\delta_A)^{1/2-1/q},
\tag{2.3}
\]

or equivalently

\[
\mathcal R_A(u)
\le {L\over M}(L\delta_A)^{1/2-1/q}.
\tag{2.4}
\]

Thus unit-layer payment is unconditional whenever

\[
\left({1\over2}-{1\over q}\right)\log^+(L\delta_A)=o(N).
\tag{2.5}
\]

This includes `q=2`, subexponential realized image, and sparse bands with
`log(L delta_A)=o(N)`.  This is exactly the range of the integrated chart-free
pruned bound.  No source algebra is needed there.

For dense bands with `delta_A=e^{-o(N)}`, `log L=Theta(N)`, and growing `q`,
the right side of (2.3) can have positive exponential rate.

---

## 3. A sufficient discrepancy theorem

Suppose a no-cell source layer satisfies

\[
\|P_Au\|_\infty
=\sup_x\left|\sum_{s\in E}K_A(x-s)\right|
\le e^{\alpha_NN},
\qquad \alpha_N\to0.
\tag{3.1}
\]

Since `||P_Au||_2<=sqrt L`, interpolation gives

\[
L^{-1/q}\|P_Au\|_q
\le\|P_Au\|_\infty^{1-2/q}
\le e^{(1-2/q)\alpha_NN}.
\tag{3.2}
\]

Therefore a selected-owner discrepancy-or-cell theorem is sufficient for the
desired unit-layer payment.  The hard step is deriving (3.1) from the coupled
weighted-Vandermonde, locator, band, and first-match equations.

---

## 4. Positive rooting does not remove the dense idempotent obstruction

### Proposition 4.1 (source-free positive-rooted obstruction)

Fix an odd prime `p` and `q>2`.  For arbitrarily large `R`, there are dense
symmetric scalar-complete bands

\[
A\subseteq\widehat{\mathbb F_p^R}\setminus\{0\}
\]

and a unit mask `f` whose exact positive packet is itself a unit mask `u`, but

\[
|G|^{-1/q}\|P_Au\|_q
\ge c|G|^{1/2-1/q}.
\tag{4.1}
\]

Hence positivity, unit multiplicity, scalar completeness, and the `l2`
projection estimate do not imply dense-band unit payment.

### Proof

Put `G=F_p^R`, `H=|G|`, and partition the nonzero dual into scalar orbits

\[
\ell=\{c\gamma:c\in\mathbb F_p^\times\}.
\]

Choose each orbit independently with probability `1/2` and let `A` be their
union.  For `x!=0`, write

\[
Z_\ell(x)=\sum_{\gamma\in\ell}\gamma(x).
\]

Then

\[
Z_\ell(x)=
\begin{cases}
p-1,&\ell\subseteq x^\perp,\\
-1,&\text{otherwise},
\end{cases}
\]

and an exact count of projective lines gives

\[
\sum_\ell Z_\ell(x)^2=H-p+1.
\tag{4.2}
\]

Writing the selectors as `(1+epsilon_l)/2`, Khintchine's inequality, with the
deterministic half-sum absorbed as a bounded shift, gives

\[
\mathbb E\left|\sum_{\gamma\in A}\gamma(x)\right|\gg\sqrt H.
\]

Consequently

\[
\mathbb E\Lambda(A)\gg\sqrt H,
\qquad
\Lambda(A)=\sum_x|K_A(x)|.
\tag{4.3}
\]

The number of scalar orbits is `(H-1)/(p-1)`, so Chernoff gives exponentially
small probability that `|A|/H` is outside a fixed neighborhood of `1/2`.
Since `Lambda(A)<=H`, the contribution of this bad-density event is
`o(sqrt H)`.  Hence some dense scalar-complete `A` satisfies

\[
\Lambda(A)\ge c\sqrt H.
\tag{4.4}
\]

The kernel is real and `sum_x K_A(x)=0`.  Thus for

\[
E_0=\{s:K_A(-s)>0\},
\]

we have

\[
(P_A\mathbf1_{E_0})(0)={1\over2}\Lambda(A),
\qquad
\|P_A\mathbf1_{E_0}\|_q\ge c\sqrt H.
\tag{4.5}
\]

Now choose `E` maximizing `F(E)=||P_A 1_E||_q` over all subsets and let `g` be
an exact norming dual.  Put

\[
r(s)=\operatorname{Re}\overline{(P_Ag)(s)}.
\]

If `s in E` and `r(s)<0`, deleting `s` and testing against the same `g` would
strictly increase `F`.  If `s notin E` and `r(s)>0`, adding `s` would strictly
increase `F`.  Therefore

\[
r(s)\ge0\ (s\in E),
\qquad
r(s)\le0\ (s\notin E).
\tag{4.6}
\]

Let `E_+={s in E:r(s)>0}`.  The exact positive packet of `f=1_E` is
`u=1_{E_+}`, and

\[
\begin{aligned}
F(E)
&=\sum_{s\in E}r(s)
=\sum_{s\in E_+}r(s)\\
&=\operatorname{Re}\langle P_A\mathbf1_{E_+},g\rangle
\le\|P_A\mathbf1_{E_+}\|_q.
\end{aligned}
\]

Combining this with (4.5) proves (4.1). `square`

This proposition is not a source-profile counterexample: neither the band nor
the mask has been derived from the same weighted-Vandermonde first-match data.
It is a separation theorem for source-free proofs.

---

## 5. Generic line decoration is not source coupling

### Lemma 5.1 (generic exact-witness decoration)

Let `D` be a finite locator set and `C subseteq binom(D,a)` a finite support
family.  After a sufficiently large finite extension, there is one affine line

\[
U_z=u+zv
\]

such that every `S in C` has a distinct assigned slope `z_S` and a polynomial
`h_S` of degree `<a-1` whose exact agreement set with `U_{z_S}` is `S`.

For `S`, put

\[
Q_S(X)=\prod_{t\in S}(X-t),
\qquad
\ell_S(y)=\sum_{t\in S}{y(t)\over Q_S'(t)}.
\]

The leading interpolation coefficient is `ell_S(y)`, so the unique slope is

\[
z_S=-{\ell_S(u)\over\ell_S(v)}
\]

when `ell_S(v)!=0`.  Distinct-slope failures and extra agreement at
`t notin S` are zero sets of explicit nonzero polynomials in `(u,v)`.  Their
finite product is nonzero, and over a sufficiently large extension it has a
nonvanishing evaluation. `square`

**Scope.** This lemma supplies exact decorated witness records and distinct
assigned slopes.  It does not prove that those slopes survive every unrelated
semantic first-match cell, nor does it preserve the deeper relation
`k=a-R-1` used by a nontrivial prefix boundary.  It therefore cannot falsify a
source-semantic theorem.  It only shows that the phrase "attach owners" is not
itself the missing coupling.

The required coupling is

```text
Phi <-> weighted Vandermonde equations <-> k and R
    <-> actual |tau|-bands <-> semantic first-match atlas.
```

---

## 6. Why the selected owner is load-bearing

For a fixed syndrome, permuting its residual records changes

```text
(S_{s,j}, o(S_{s,j}), h_{S_{s,j}})
```

but does not change

```text
u_j(s)=1_{b(s)>=j},
P_A u_j,
||P_A u_j||_q.
```

Therefore a proof consuming only the syndrome mask cannot decide which owner
was attached to the layer.  Whole-slope first-match deletion yields a
contradiction only if the emitted cell contains an owner actually selected by
that layer.  A certificate at another record with the same syndrome need not
remove the selected record.

The missing inverse must have the form

\[
L^{-1/q}\|P_Au_j\|_q\ge e^{\eta N}
\Longrightarrow
\operatorname{Cell}(S_{s,j},o(S_{s,j}),h_{S_{s,j}})
\tag{6.1}
\]

for some attached record in the same layer.

---

## 7. Exact remaining theorem: SULSI

> **Selected-owner unit-layer source inverse (SULSI).** For every fixed
> `eta>0`, all sufficiently large source-derived profiles have the following
> property.  If an actual owner-labelled unit layer satisfies
> \[
> L^{-1/q}\|P_Au_j\|_q\ge e^{\eta N},
> \]
> then that layer emits a validated earlier cell rooted at one of its attached
> records `(S_{s,j},o(S_{s,j}),h_{S_{s,j}})`.

Let SFULP denote the uniform minor-or-cell statement

\[
L^{-1/q}\|P_Au_j\|_q\le e^{\epsilon_NN},
\qquad \epsilon_N\to0,
\]

on every no-cell layer.

### Theorem 7.1

\[
\mathrm{SULSI}\iff\mathrm{SFULP}.
\]

For SULSI `=>` SFULP, take the supremum of the positive normalized logarithm
over no-cell layers at each `N`.  If it does not tend to zero, a fixed positive
rate survives on a subsequence and SULSI emits a forbidden cell.  The reverse
direction follows because eventually `epsilon_N<eta`.  Empty suprema are
defined to be zero. `square`

The equivalence is a quantifier audit, not an analytic proof.  It identifies
the exact uniform source theorem hidden in the desired asymptotic notation.

---

## 8. Heavy-fiber consequence

On a semantically saturated residual, SULSI rules out the cell alternative, so

\[
\mathcal R_A(u_j)\le e^{o(N)}{L\over M}.
\]

Since `b=sum_j u_j` and positive localization gives
`R_A(b)>=R_A(f)`, an excess `R_A(f)>=e^{eta N}` forces

\[
b_{\max}{L\over M}\ge e^{\eta N-o(N)}.
\tag{8.1}
\]

Because `b(s)<=f(s)`, this is an image-normalized heavy residual fiber.

This reduction does not by itself pay that heavy fiber.  The integrated heavy-
fiber admissibility transfer makes the fiber available to the semantic side;
the general five-way emission remains open.  PR #735 proves saturation,
involution-planted, and multiplicative-folding classes and reports a finite
prime-field census, but explicitly leaves the general many-syndrome analytic
residual untouched.

---

## 9. Slope-faithful census

The deterministic census tests actual affine received lines, exact agreement,
whole-slope saturation deletion, common-support removal, unique owner records,
depth-one moment images, complete dyadic `|tau|` bands, and `q in {3,4,6}`.

```text
random lines                              9800
nonempty residuals                        8322
band/order rows                         113139
maximum actual R_A                     0.650732
maximum arbitrary full-mask R_A        1.016517
maximum actual/lex R_A ratio           10.376752
maximum positive multiplicity                  4
multiplicity rows                         21386
multiplicity rows with rooted trade       21386
maximum actual unit-layer transfer      0.672550
maximum arbitrary unit-mask transfer    0.780437
```

The compact certificate commits to all 113,139 analysis rows and 113,139
arbitrary-mask control rows while retaining only aggregate and per-regime
summaries in the review diff.  Its three stream digests are:

```text
line stream       056c84fc81dd3097ee2555e5fb069e0860ff34a8186be09f9625ef4d3ab7641d
analysis stream   371696ef69d80b5713a21ca97e1731c03ae684b72cd4fd7507d569c5751baf92
control stream    6e646bd4da61ef1df121cfeaf0748f99d7da66465028f7a12641fc93971fc40b
```

The census includes consecutive locators and multiplicative subgroups over
fields `F_7` through `F_19`.  It is evidence for source-layer rigidity, not an
asymptotic theorem.  In particular, bounded `N` and bounded `q` cannot exclude
an eventual positive-rate source family.

It does prove experimentally that lexicographic one-per-syndrome deletion is a
bad semantic proxy: the normalized band load changed by a factor greater than
ten while the actual owner records remained valid.

---

## 10. Proof routes and nonclaims

The most focused sufficient theorem is selected-owner kernel discrepancy:

\[
\sup_x\left|\sum_{s:b(s)\ge j}K_A(x-s)\right|
\ge e^{\eta N}
\Longrightarrow
\text{a selected-owner cell}.
\]

Potential routes must use the source coupling explicitly:

1. signed locator rigidity for the selected exact-agreement records;
2. nontrivial zero-sum tuple expansion followed by source-cell emission;
3. exceptional-spectrum localization plus selected-owner conversion;
4. VC/compression bounds for actual source layers, not arbitrary masks;
5. Bohr concentration followed by an exact quotient, planted, field, rank, or
   saturation certificate.

This packet does **not** prove:

* dense-band SULSI or SFULP;
* the general heavy-fiber semantic inverse;
* image-scale MI/MA or direct Sidon payment;
* the asymptotic RS--MCA theorem or the Proximity Prize threshold.

Its conclusion is narrower and reusable:

```text
source-free unit-layer analysis stops at the integrated interpolation bound;
positive rooting does not improve that boundary;
the remaining theorem must consume the selected source owner and the coupled
weighted-locator / band / first-match equations.
```
