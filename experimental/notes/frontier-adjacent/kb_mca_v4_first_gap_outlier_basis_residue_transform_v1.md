---
status: PROVED OUTLIER-BASIS/RESIDUE TRANSFORM / DETERMINANT MASS REINDEXED / WEIGHTED INCIDENCE OPEN / ZERO LEDGER MOVEMENT
architecture_id: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1
direct_statement: At the first open KoalaBear full-outside slack, every independent eight-row outlier basis canonically reconstructs its graph line and complement locator by 9-by-9 minors, and the determinant-weighted rich-line excess is exactly the sum of the basis-indexed rich-slope excesses.
---

# KoalaBear first-gap outlier-basis/residue transform

## Status

This packet proves an exact reindexing of the remaining first-gap
determinant payment. It combines:

1. the rank-nine rich-pencil atlas;
2. the eight independent outlier rows;
3. the first-gap complement-locator residue line.

The determinant weight is no longer an external scalar attached to a graph
line. Each independent eight-row basis reconstructs the line, its common-zero
set, its complement locator, and its moving-root map. Consequently,

\[
 \sum_L\beta_L(J_L-20)_+
\]

is exactly an unweighted sum over basis records.

This is a proved reduction. It does not bound that sum and does not move the
KoalaBear ledger.

## 1. Same-selector rank-nine data

Fix one complete selector rebuilt after the active six-owner deletion. On its
carrier \(V\), the selected errors have the proved form

\[
 e_\eta=u+\eta v+w_\eta,\qquad
 w_\eta\in K_0,\qquad \dim K_0=8.
\tag{1.1}
\]

Choose a basis of \(K_0\). Let \(g_x\in F^8\) be its row at \(x\in V\), and
write

\[
 w_\eta(x)=g_xz_\eta,\qquad z_\eta\in F^8.
\tag{1.2}
\]

For an eight-subset \(B\subseteq V\), let \(G_B\) be the \(8\times8\)
matrix with rows \(g_x\), in the canonical carrier order. Call \(B\)
independent when

\[
 \Delta_B:=\det G_B\ne0.
\tag{1.3}
\]

All objects below use this one selector. No row, source, carrier, slope, or
basis record may be imported from another selector.

## 2. A basis canonically reconstructs one graph line

Fix an independent \(B\). There are unique vectors
\(\alpha_B,\beta_B\in F^8\) satisfying

\[
 G_B\alpha_B=-u|_B,\qquad
 G_B\beta_B=-v|_B.
\tag{2.1}
\]

Define

\[
 a_B(x)=u(x)+g_x\alpha_B,\qquad
 b_B(x)=v(x)+g_x\beta_B,
\tag{2.2}
\]

and the graph line

\[
 L_B=\{(\eta,\alpha_B+\eta\beta_B):\eta\in F\}.
\tag{2.3}
\]

Let

\[
 \Gamma_B
 =\{\eta\in\Gamma_D:B\subseteq T_\eta\},
\qquad J_B=|\Gamma_B|.
\tag{2.4}
\]

### Theorem 2.1

For every selected slope \(\eta\),

\[
 \boxed{
 B\subseteq T_\eta
 \iff
 z_\eta=\alpha_B+\eta\beta_B.}
\tag{2.5}
\]

Thus \(\Gamma_B\) is exactly the selected-slope set of \(L_B\).

#### Proof

Restrict (1.1) to \(B\). Since \(G_B\) is invertible,

\[
 e_\eta|_B=0
 \iff
 G_Bz_\eta=-u|_B-\eta v|_B
 \iff
 z_\eta=\alpha_B+\eta\beta_B.
\]

This proves (2.5). \(\square\)

In particular, a rich basis does not choose among several graph lines. It
determines one graph line before any line-level counting is performed.

## 3. Exact minor formulas

For \(x\in V\), define the two bordered determinants

\[
 A_B(x)=
 \det
 \begin{pmatrix}
  G_B & u|_B\\
  g_x & u(x)
 \end{pmatrix},
\qquad
 B_B(x)=
 \det
 \begin{pmatrix}
  G_B & v|_B\\
  g_x & v(x)
 \end{pmatrix}.
\tag{3.1}
\]

The Schur-complement formula and (2.1) give

\[
 \boxed{
 A_B(x)=\Delta_Ba_B(x),\qquad
 B_B(x)=\Delta_Bb_B(x).}
\tag{3.2}
\]

Hence the common-zero set and its complement are determined directly by
the eight outlier rows:

\[
 Z_B=\{x\in V:A_B(x)=B_B(x)=0\},
\tag{3.3}
\]

\[
 Y_B=V\setminus Z_B
 =\{x\in V:(A_B(x),B_B(x))\ne(0,0)\}.
\tag{3.4}
\]

Every point of \(B\) gives a repeated row in both bordered determinants, so

\[
 \boxed{B\subseteq Z_B.}
\tag{3.5}
\]

On \(Y_B\), the projective minor map

\[
 \Psi_B(x)=[-A_B(x):B_B(x)]\in\mathbf P^1(F)
\tag{3.6}
\]

is well-defined. Its finite fibre at \(\eta\) is

\[
 F_{\eta,B}
 =\{x\in Y_B:A_B(x)+\eta B_B(x)=0\}.
\tag{3.7}
\]

For \(\eta\in\Gamma_B\), this is the usual moving-zero fibre of the graph
line \(L_B\). The fibres are pairwise disjoint. On the first-gap
\(x_B=1\), zero-deficit extremal branch, every selected fibre is a
singleton.

Equations (3.1)--(3.7) are the missing direct coupling between the eight
outlier determinant rows and the complement locator. The locator is not an
independent line parameter:

\[
 \boxed{
 L_{Y_B}(X)=
 \prod_{\substack{x\in V\\
 (A_B(x),B_B(x))\ne(0,0)}}(X-x).}
\tag{3.8}
\]

## 4. Determinant mass becomes a basis sum

Let \(\mathcal B(K_0)\) be the independent eight-subsets of \(V\). For a
graph line \(L\), recall

\[
 \beta_L
 =
 \#\{B\in\mathcal B(K_0):B\subseteq Z_L\}.
\tag{4.1}
\]

### Theorem 4.1: outlier-basis transform

\[
 \boxed{
 \sum_{L:J_L\ge21}\beta_L(J_L-20)
 =
 \sum_{B\in\mathcal B(K_0)}(J_B-20)_+.}
\tag{4.2}
\]

#### Proof

If \(B\subseteq Z_L\), then \(a_L|_B=b_L|_B=0\). Invertibility of \(G_B\)
forces the coefficients of \(a_L,b_L\) to be precisely
\(\alpha_B,\beta_B\). Therefore \(L=L_B\), and Theorem 2.1 gives
\(J_L=J_B\).

Conversely, if \(J_B\ge21\), the selected graph points in (2.5) lie on the
unique line \(L_B\), and \(B\subseteq Z_B\). Thus the pairs

\[
 (L,B),\qquad J_L\ge21,\quad
 B\in\mathcal B(K_0),\quad B\subseteq Z_L,
\]

are in bijection with the bases \(B\) satisfying \(J_B\ge21\). Reindexing
the finite sum proves (4.2). \(\square\)

Equivalently, by expanding (4.1) first,

\[
 \sum_L\beta_L(J_L-20)_+
 =
 \sum_{B\in\mathcal B(K_0)}
 \sum_{\substack{L:B\cap Y_L=\varnothing}}
 (J_L-20)_+,
\tag{4.3}
\]

and the inner sum contains at most one rich line: \(L_B\).

This explains exactly what the determinant weight counts. It is the
multiplicity with which different independent outlier bases reconstruct the
same source-admissible complement locator.

## 5. Eight-shortened complement-locator form

At the first open full-outside slack,

\[
 |V|=2j,\qquad |Z_B|=j-1,\qquad |Y_B|=j+1.
\tag{5.1}
\]

For \(B\subseteq Z_B\), put

\[
 V_B=V\setminus B,\qquad
 \overline Z_B=Z_B\setminus B.
\tag{5.2}
\]

Then

\[
 |V_B|=2j-8,\qquad
 |\overline Z_B|=j-9,
\tag{5.3}
\]

and

\[
 \overline Z_B\sqcup Y_B=V_B.
\tag{5.4}
\]

In the source algebra \(A_\Sigma=F[X]/(L_\Sigma)\), all these locators are
units and

\[
 \boxed{
 L_{\overline Z_B}^{-1}
 =L_{Y_B}L_{V_B}^{-1}.}
\tag{5.5}
\]

The original quotient normalization is unchanged:

\[
 L_{Z_B}^{-1}
 =L_{Y_B}L_V^{-1}.
\tag{5.6}
\]

Let \(W_\Sigma\) be the proved two-dimensional source residue line. The
first-gap source admission test is exactly

\[
 \boxed{[L_{Y_B}]\in W_\Sigma.}
\tag{5.7}
\]

Thus a dangerous determinant contribution is a basis \(B\) for which:

1. \(B\) is an independent outlier basis;
2. the bordered-minor support (3.4) has size \(j+1\);
3. its split locator satisfies (5.7);
4. the multiplier-rank, degree-defect, and common-divisor routes do not
   emit an earlier owner;
5. \(J_B\ge21\).

The determinant has disappeared from the final incidence predicate because
it has become the index of the shortened source record.

## 6. Exact remaining theorem

The active excess allowance can be printed exactly. The imported MDS
row-flat theorem gives every retained first-gap slope at least

\[
 C_0=\binom{e+8}{8}
 =\binom{67{,}480}{8}
 =10{,}658{,}592{,}438{,}443{,}717{,}273{,}371{,}372{,}062{,}592{,}575
\tag{6.1}
\]

independent basis incidences. Let

\[
 N_V=|V|=1{,}962{,}208,
\qquad
 B_{\rm rem}=274{,}961{,}102{,}171{,}022{,}152.
\tag{6.2}
\]

The exact largest sufficient active allowance is

\[
\begin{aligned}
 E_{\max}^{\rm active}
 &=(B_{\rm rem}+1)C_0
   -20\binom{N_V}{8}-1\\
 &=2{,}930{,}589{,}315{,}151{,}076{,}074{,}409{,}054{,}963{,}728{,}781{,}743{,}707{,}264{,}369{,}983{,}654.
\end{aligned}
\tag{6.3}
\]

Indeed, if \(H\) is the number of retained first-gap slopes, the fixed-basis
double count and (4.2) give

\[
 HC_0
 \le
 \sum_{B\in\binom V8}J_B
 \le
 20\binom{N_V}{8}
 +\sum_B(J_B-20)_+.
\tag{6.4}
\]

Thus

\[
 \sum_B(J_B-20)_+\le E_{\max}^{\rm active}
 \Longrightarrow
 HC_0<(B_{\rm rem}+1)C_0
 \Longrightarrow
 \boxed{H\le B_{\rm rem}.}
\tag{6.5}
\]

The minus one in (6.3) is exact: increasing the allowance by one reaches
the integer threshold \((B_{\rm rem}+1)C_0\).

This active allowance is deliberately not the legacy M1 value. It uses the
current six-owner reserve and the rebuilt first-gap carrier. Numerically it
allows an average excess of

\[
 \left\lfloor
 \frac{E_{\max}^{\rm active}}{\binom{N_V}{8}}
 \right\rfloor
 =537{,}676
\tag{6.6}
\]

per ambient eight-subset. Consequently a pointwise cap \(J_B\le20\) is far
stronger than the bridge requires.

There is also an exact tail formulation. For

\[
 N_q^{\rm adm}
 =
 \#\{B\in\mathcal B_{\rm adm}:J_B\ge q\},
\tag{6.7}
\]

the elementary layer-cake identity gives

\[
 \boxed{
 \sum_{B\in\mathcal B_{\rm adm}}(J_B-20)_+
 =
 \sum_{q=21}^{j+1}N_q^{\rm adm}.}
\tag{6.8}
\]

This turns the weighted theorem into a family of ordinary basis-counting
problems.

Two exact sufficient specializations are useful. Since \(J_B\le j+1\), it
is enough to prove

\[
 \boxed{
 |\mathcal B_{\rm adm}|
 \le
 2{,}987{,}090{,}124{,}862{,}857{,}014{,}844{,}845{,}210{,}892{,}819{,}423{,}095{,}108{,}344.}
\tag{6.9}
\]

The ambient eight-subset count is

\[
 \binom{N_V}{8}
 =
 5{,}450{,}465{,}756{,}550{,}941{,}286{,}862{,}563{,}447{,}363{,}700{,}950{,}928{,}416{,}516.
\tag{6.10}
\]

Thus the cardinality-only route needs to exclude at least

\[
 2{,}463{,}375{,}631{,}688{,}084{,}272{,}017{,}718{,}236{,}470{,}881{,}527{,}833{,}308{,}172
\tag{6.11}
\]

ambient eight-subsets from the admitted basis class, about \(45.2\%\).

Alternatively, spend the full ambient count on all tail levels through
\(q=537{,}696\). The remaining exact allowance is

\[
 4{,}689{,}031{,}792{,}167{,}053{,}939{,}299{,}604{,}056{,}471{,}215{,}877{,}091{,}326{,}838.
\]

Since there are \(443{,}409\) later levels, it is enough to prove

\[
 \boxed{
 N_{537{,}697}^{\rm adm}
 \le
 10{,}574{,}958{,}542{,}039{,}187{,}159{,}709{,}442{,}200{,}025{,}745{,}704{,}510.}
\tag{6.12}
\]

This is about \(1.94\cdot10^{-6}\) of the ambient eight-subsets. The two
routes expose different plausible mechanisms:

```text
moderate source-residue exclusion across all bases
OR
very strong rarity only for extremely rich bases.
```

For the active first-gap selector, define

\[
 \mathcal B_{\mathrm{adm}}
 =
 \left\{
 B\in\mathcal B(K_0):
 \begin{array}{l}
 |Y_B|=j+1,\\
 [L_{Y_B}]\in W_\Sigma,\\
 \text{the line is coprime, exact-degree, and semantically unpaid}
 \end{array}
 \right\}.
\tag{6.1}
\]

The first-gap determinant obligation is now exactly:

> **Selected-basis source-residue packing.** Prove the active reserve bound
> \[
> \boxed{
> \sum_{B\in\mathcal B_{\mathrm{adm}}}(J_B-20)_+
> \le E_{\max}^{\mathrm{active}}.}
> \tag{6.13}
> \]
> If (6.2) fails, emit a canonical earlier or new owner containing one of
> the same selected slopes represented by the offending basis record.

This is equivalent to the line-weighted theorem, but it is a better proof
interface:

* the eight outlier rows are explicit;
* the graph line is reconstructed rather than quantified independently;
* the complement locator is the support of two exact \(9\times9\) minors;
* the source condition is membership in a fixed two-dimensional residue
  line;
* the richness statistic is the actual same-selector multiplicity \(J_B\);
* the exact allowance is the current active integer (6.3), not an imported
  legacy reserve.

## 7. Exact source-coupled finite census

The verifier includes a stronger finite control than the abstract
basis/line toy.

Work over \(F_{17}\) with

\[
 e=2,\qquad j=6,\qquad |\Sigma|=4,\qquad |V|=12.
\]

It uses the actual RS-supported subspace

\[
 K_0
 =
 L_\Sigma\langle1,X,X^2,X^3\rangle|_V,
\qquad \dim K_0=4.
\tag{7.1}
\]

Every four-subset of \(V\) is a basis, so there are

\[
 \binom{12}{4}=495
\]

basis records. For each of 36 exact source pairs, the verifier:

1. exhausts all 792 split locators;
2. applies both quotient-interpolation tests;
3. keeps only coprime exact-degree-two source lines;
4. represents every line in one common affine \(K_0\)-coset;
5. selects one witness per finite slope by the canonical lexicographic
   complement rule;
6. rebuilds every rich graph line from its basis;
7. checks the weighted atlas and layer-cake identities.

The exact maxima are:

```text
source cases                                      36
K0 bases                                         495
maximum admitted rich bases                       20
maximum admitted rich-basis fraction           20/495
maximum weighted excess                           45
maximum basis multiplicity                         7
```

The maximum admitted count occurs in `random_08`, with four primitive
source lines, 13 selected slopes, and two rich selected lines. The maximum
weighted excess occurs in `random_15`, with four primitive lines, 15
selected slopes, and three rich selected lines. The maximum multiplicity
occurs in `random_00`.

This control is finite and uses one printed selector rule. It does not prove
complete-selector existence or a deployed asymptotic density bound. It does
show that the coupled source-residue/bordered-minor predicate can be much
smaller than the ambient MDS basis set even when every carrier subset is
independent. The observed maximum admission density is about \(4.04\%\),
well below the deployed cardinality-only sufficient ratio \(54.8\%\).
Accordingly, the moderate source-residue exclusion route is currently better
supported than a strategy aimed only at the extreme tail
\(J_B\ge537{,}697\).

## 8. Plausible proof routes from the transformed target

### 8.1 Pluecker/minor elimination

Treat (3.1) as polynomial functions of the Pluecker coordinate
\(\Delta_B\) and the two bordered-minor families. Combine the split-locator
condition (5.7) with the source-pencil determinant

\[
 R_0S_1-R_1S_0=c_\Sigma L_\Sigma.
\]

A positive-rate family of admitted bases should force either a common
minor factor, multiplier-rank excess, or a lower-degree source-rational
parameter.

### 8.2 Matroid shortening

For each \(B\), work on the shortened carrier \(V_B\). The determinant
weight has become one fixed contraction, while the source locator remains
in the same two-dimensional residue line. Seek a uniform split-locator
bound on this rank-eight contraction, then sum over canonical basis types
rather than all bases.

### 8.3 Moving-root image bound

Use the projective minor map \(\Psi_B\). Every selected slope in
\(\Gamma_B\) has a nonempty finite fibre, and the fibres are disjoint.
Prove that a source-admissible locator with more than twenty selected values
forces one of:

\[
 \text{degree defect, common divisor, rank excess, field descent,
 or a bounded-census repeated minor template.}
\]

### 8.4 Canonical basis compression

The same graph line may have many bases. Choose a canonical basis from its
matroid restriction and charge every other basis by basis exchange to a
bounded set of minor signatures. A successful compression must retain the
exact multiplicity in (4.2); ordinary basis exchange without source-residue
data is known not to close.

## 9. Route cuts

This packet does not justify any of the following:

* replacing \(\mathcal B(K_0)\) by all eight-subsets;
* bounding \(J_B\) and the number of bases separately;
* importing \(Y_B\) or \(W_\Sigma\) from another selector;
* using the formally valid but non-closing
  \(\binom{2j-8}{846{,}163}\) fixed-dimensional bound;
* treating multiplier-rank excess as paid without a same-owner projection;
* claiming that (4.2) itself reduces the active integer ledger.

The exact scalar \(x=1\) extremizer survives every separated cap. A proof
must use the coupled minor-locator/residue predicate in (6.1).

## 10. Machine replay

The deterministic verifier checks:

1. basis-to-line reconstruction;
2. the two bordered-minor identities;
3. \(B\subseteq Z_B\);
4. graph-line/multiplicity equality;
5. the line-weighted and basis-weighted atlas sums;
6. the exact eight-shortened locator identities;
7. the exact richness layer cake and active sufficient thresholds;
8. the source-coupled `F_17` RS/K0/selector census;
9. fail-closed zero-ledger status.

Replay with:

```bash
python experimental/scripts/verify_kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.py --check
python experimental/scripts/verify_kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.py --tamper-selftest
```

## 11. Theorem boundary

```text
# PROVED
independent outlier basis -> unique graph line
9x9 bordered minors -> exact common-zero/complement locator
line-weighted determinant excess = basis-indexed richness excess
eight-shortened locator identity
source admission = same two-dimensional residue-line test

# OPEN
selected-basis source-residue packing bound
same-owner emission from a packing failure
complete-selector construction/coverage
active reserve payment
```
