# Anchored rich-flat router for KoalaBear error rank eleven

## 1. Exact inherited interface

Work in the deployed KoalaBear row

```text
n = 2,097,152
K = 1,048,576
m = 1,116,048
w = m-K = 67,472
B* = 274,980,728,111,395,087
2w = 134,944.
```

After the reversible gauge from the predecessor stack, the selected post-near
explanations lie in an affine flat `c_0+C'`, where `C'` is a subspace of the
degree-`<K` Reed--Solomon code of dimension `s<=10`.  Each selected slope has
one fixed actual minimizing pair

\[
 e=(a_e,b_e)\in(c_0+C')\times C'
\]

and complete pair core

\[
 H_e=\{x:r_0(x)=a_e(x),\ r_1(x)=b_e(x)\}.
\]

For a low-margin record, the predecessor proof gives

\[
 |H_e|\ge m-\theta_\gamma.
\]

The nonuniform support resource is

\[
 \sum_\gamma\theta_\gamma
 \le C_{10}=106618568137036225644. \tag{1}
\]

No first-match owner or ledger value is imported.

## 2. Anchor one actual low record

Fix a cutoff `tau` and put

\[
 A=m-\tau,\qquad d=A-K=w-\tau,\qquad c=2A-n.
\]

Let `L` be the selected records with `theta_gamma<=tau`.  If `L` is empty,
(1) already pays the post-near family by the high-tail bound.  Otherwise choose
one actual anchor record `gamma_0`, its exact size-`m` support `S_0`, and its
selected minimizing pair `e_0`.

Set

\[
 G_0=S_0\cap H_{e_0}.
\]

Because the cutoff is below the truncation level in the definition of the
margin,

\[
 A\le |G_0|\le m. \tag{2}
\]

Every represented low pair type `e` has `|H_e|>=A`, and therefore

\[
 |H_e\cap G_0|
 \ge |H_e|+|G_0|-n
 \ge 2A-n=c. \tag{3}
\]

This is the reason for anchoring an actual record rather than using the
complete anchor pair core, which can be much larger than `m`.

## 3. Pair-difference row spaces and rich annihilator flats

Choose a basis `P_1,...,P_s` of `C'`.  Write the coefficient matrix of a pair
as `M_e in F^(2 x s)`.  For `e!=e_0`, put

\[
 X_e=M_e-M_{e_0},\qquad U_e=\operatorname{rowspan}(X_e).
\]

Its rank `r` is one or two.  For a coordinate `x`, let

\[
 v_x=(P_1(x),\ldots,P_s(x))\in\mathbb F^s.
\]

At every `x in H_e cap G_0`, the two pair types both equal the received pair,
so

\[
 X_ev_x=0.
\]

Consequently, if a row space `U` is represented by at least one pair type,
then its canonical anchor-zero set

\[
 Z_U=\{x\in G_0:v_x\in U^\perp\}
\]

satisfies

\[
 |Z_U|\ge c. \tag{4}
\]

### Definition: `h`-transverse row space

A represented row space `U` is `h`-transverse when every proper linear
subspace `F<U^perp` contains at most `h` of the labeled vectors
`{v_x:x in Z_U}`.  Labels, rather than distinct projective points, are counted.
This definition therefore detects zero columns, projective clones, and every
higher flat concentration.

## 4. Ordered-basis count

Let `r=dim U` and `t=s-r`.  If `U` is `h`-transverse, the vectors indexed by
`Z_U` span `U^perp`; otherwise their span itself would be a proper flat
containing at least `c>h` labels.

Choose an ordered basis greedily.  After `j<t` independent vectors have been
chosen, their span is a proper subspace of `U^perp` and contains at most `h`
labels of `Z_U`.  Hence there remain at least

\[
 |Z_U|-h\ge c-h
\]

choices outside the current span.  Thus `U^perp` owns at least

\[
 (c-h)^t \tag{5}
\]

ordered labeled bases.

An ordered independent `t`-tuple from `G_0` spans only one `t`-space and hence
determines only one row space `U`.  Since `|G_0|<=m`, the number of represented
`h`-transverse rank-`r` row spaces is at most

\[
 N_r(\tau,h;s)
 \le
 \left\lfloor\frac{m^{\underline{s-r}}}{(c-h)^{s-r}}\right\rfloor. \tag{6}
\]

For the deployed range, `(m-t)/(c-h)>1` for every `0<=t<=9`.  The right side
is therefore nondecreasing in `s-r`.  Uniformly over `s<=10`,

\[
 N_1(\tau,h)
 \le\left\lfloor\frac{m^{\underline9}}{(c-h)^9}\right\rfloor,
 \qquad
 N_2(\tau,h)
 \le\left\lfloor\frac{m^{\underline8}}{(c-h)^8}\right\rfloor. \tag{7}
\]

This lemma is elementary and does not import a generic-position or subspace-
design hypothesis.

## 5. Paying each transverse row-space group

The anchor pair type itself owns at most

\[
 n-A \tag{8}
\]

selected slopes.  Indeed every owning support has a nonempty exception set
outside its complete pair core, and the fixed-pair ratio map is injective.

### Rank one

For one fixed rank-one row space `U=<P>`, every pair difference has the form

\[
 M_e-M_{e_0}=u_e v^T,
\]

where `v` is the coefficient vector of `P`.  The complete group is therefore
one fixed-right-factor anticode.  PR #1171's common-core-aware affine-ray
theorem gives the uniform group cap

\[
 R_1=8147918. \tag{9}
\]

The groups are disjoint by their row space; summing (9) here does not sum an
uncontrolled collection of overlapping local certificates.

### Rank two

For one fixed two-dimensional row space `U`, all represented pairs lie in

\[
 (a_{e_0}+U)\times(b_{e_0}+U).
\]

At cutoff `tau`, the ordinary affine list cap in each projection is

\[
 M_2(\tau)=
 \left\lfloor
 \frac{\binom{n-K+2}{2}}{\binom{w-\tau+2}{2}}
 \right\rfloor. \tag{10}
\]

The actual sextic field satisfies `M_2(tau)^2<|F|` at the selected cutoff, so
the sub-square interleaving collapse bounds the number of distinct ordered
pair types in this group by `M_2(tau)`.  Each pair type owns at most `n-A`
slopes.  Hence one rank-two row-space group costs at most

\[
 R_2(\tau)=(n-A)M_2(\tau). \tag{11}
\]

## 6. The complete transverse envelope

By (1), the number of records with `theta_gamma>=tau+1` is at most

\[
 H(\tau)=\left\lfloor\frac{C_{10}}{\tau+1}\right\rfloor. \tag{12}
\]

If every represented rank-one and rank-two row space is `h`-transverse, then
(7)--(12) give

\[
\begin{aligned}
 |Z_{\rm bad}|
 \le{}&2w+H(\tau)+(n-A)\\
 &+R_1\left\lfloor\frac{m^{\underline9}}{(c-h)^9}\right\rfloor\\
 &+R_2(\tau)\left\lfloor\frac{m^{\underline8}}{(c-h)^8}\right\rfloor.
 \tag{13}
\end{aligned}
\]

At

\[
 \tau=1547,\qquad h=42452,
\]

exact arithmetic gives

```text
A                              1,114,501
c = 2A-n                         131,850
d = A-K                           65,925
n-A                              982,651
M_2                                  252
R_2                          247,628,052
N_1                        7,365,150,514
N_2                          589,969,647
rank-one groups       60,010,642,445,729,852
rank-two groups      146,093,034,425,737,644
anchor pair                     982,651
low total             206,103,676,872,450,147
high tail              68,875,044,016,173,272
near add-back                     134,944
------------------------------------------------
total                  274,978,720,888,758,363
slack                    2,007,222,636,724
```

The adjacent value `h=42453` is over budget by
`17,108,854,816,460`.  An exhaustive exact scan of every legal cutoff finds
that `42452` is the largest threshold payable by (13), attained at cutoffs
`1547,1548,1549`; the earliest cutoff is selected because it retains the
largest anchor-overlap floor.

Thus the entire `h`-transverse low-margin branch is paid.

## 7. Exact survivor terminal

If the line is over budget, some represented row space `U`, of rank
`r in {1,2}`, is not `42452`-transverse.  Hence there is a proper subspace

\[
 F<U^\perp
\]

containing at least `42453` labeled evaluation columns from `Z_U`.  Put

\[
 W=F^\perp\le C'.
\]

Then

\[
 U\subsetneq W,
 \qquad
 \dim W\ge r+1, \tag{14}
\]

and every polynomial in `W` vanishes on the same actual coordinate set
`J subset G_0`, with

\[
 |J|\ge42453. \tag{15}
\]

Because `J subset G_0`, the anchor pair equals the received pair on `J`.
Every pair type in the represented `U`-group also equals the received pair on
`J`.

Let

\[
 L_J(X)=\prod_{x\in J}(X-x).
\]

Then `L_J` divides every polynomial in `W`.  Division is injective and yields

\[
 L_J^{-1}W\le\mathbb F[X]_{<K-|J|},
 \qquad
 K-|J|\le1006123. \tag{16}
\]

The two exact possibilities are therefore:

- a represented rank-one pair-difference direction extends to a direction
  subspace of dimension at least two with a common factor of degree at least
  `42453`; or
- a represented rank-two pair-difference plane, which already has at least
  `131850` common anchor zeros, extends to a direction subspace of dimension
  at least three with a common factor of degree at least `42453`.

This is the new terminal.  It is source-level and actual-coordinate, but it is
not yet a chronology owner or a payment of rank eleven.

## 8. Nonclaims

- Rank eleven is not paid.
- KoalaBear is not closed.
- No active-v4 atom moves.
- The emitted larger subspace is not assumed to contain every remaining pair
  type.
- The per-row-space group charges are summed only after the anchor gives a
  disjoint row-space partition of the fixed selected low family.
