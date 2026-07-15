# Selected-owner cube means: ambient leakage, commutator guard, and equitable reduction

## Status

```text
PROVED:
  exact ambient/within-image fourth-power decomposition;
  exact empty-mode/projection commutator identity;
  positive-rate Hamming ambient-leakage guardrail;
  equitable-chart reduction of within-chart SOCML4 to ambient leakage;
  unconditional maximal-band quartic unit-mask bound.

CONDITIONAL:
  equitable-chart SOCQI4, only under an explicit paid empty-mode admission
  theorem at the same selected owners.

OPEN:
  source-specific ambient leakage (AL4);
  non-equitable within-image cube localization;
  commutator or signed nonempty-mode compression;
  compiler admission and payment of general cube-spectrum cells.
```

This packet audits the proposed selected-owner cube-mean localization target.
It does not promote a stable paper theorem.  Its purpose is to separate three
obligations which a source-cube proof must not merge:

```text
ambient leakage outside the realized image;
within-image variation after cube averaging;
charge-faithful admission/payment of cube modes.
```

The band-uniform cube packet proves exact cube-spectrum identities and a sound
per-pattern floor, but leaves admission and middle-width compression open.
The cylinder packet proves exact base-3 hierarchy renormalization and flatness
on its stated hierarchy, but leaves nonhierarchical bands and admission open.
This note is compatible with those boundaries.

Machine checks:

```text
experimental/scripts/verify_selected_owner_cube_mean_boundary_v1.py --check
experimental/scripts/verify_selected_owner_cube_mean_boundary_v1.py \
  --tamper-selftest
```

Certificate:

```text
experimental/data/certificates/selected-owner-cube-mean-boundary-v1/
  selected_owner_cube_mean_boundary_v1.json
```

SHA-256:

```text
0a93c1b33f633b359013fb230ab3138def481782c3d8da91d22df4e5b454f2aa
```

## Repository interfaces consumed

This packet consumes, without reproving:

* `experimental/notes/audits/selected_owner_unit_layer_boundary_v1.md` for
  the exact selected-owner unit layers, natural charge, and source-free dense
  idempotent guardrail;
* `experimental/notes/thresholds/band_uniform_cube_reduction.md` for the exact
  cube-spectrum identity and sound per-pattern floor;
* `experimental/notes/thresholds/cylinder_renormalization.md` for the exact
  base-3 hierarchy renormalization and its stated flatness scope.

These interfaces were integrated as experimental material on base commit
`764f1c0243770baa437d4ae790b1448afa091680`.  Their open admission,
nonhierarchy, and large-order boundaries remain open here.

## 1. Setup

Let `G` be a finite abelian effective profile group, `H = |G|`, and let

```text
Phi : Omega^0 -> G,
S = Phi(Omega^0),
M = |Omega^0|,
L = |S|.
```

Let `Omega^circ subseteq Omega^0` be the actual whole-slope first-match
residual and

```text
f(s) = #{X in Omega^circ : Phi(X) = s}.
```

For a complete symmetric source band `A subseteq hat G \ {1}`, use

```text
hat h(gamma) = sum_s h(s) conjugate(gamma(s)),
P_A h(s) = H^(-1) sum_{gamma in A} hat h(gamma) gamma(s).
```

If `P_A f != 0`, fix its exact quartic norming dual `g`:

```text
||g||_(4/3) = 1,
Re <P_A f,g> = ||P_A f||_4.
```

If `P_A f = 0`, use the canonical convention `g = 0`.  In both cases
`||g||_(4/3) <= 1`; the zero convention prevents an arbitrary dual from
manufacturing positive selected layers when the projected count vanishes.

Put

```text
r(s) = Re conjugate((P_A g)(s)),
b(s) = f(s) 1_{r(s) > 0},
u_j(s) = 1_{b(s) >= j}.
```

At each active syndrome, `u_j` retains the actual canonically selected source
record `(X_{s,j},o(X_{s,j}),h_{X_{s,j}})`.  Its natural charge is

```text
c(u_j) = Re <P_A u_j,g> = sum_s u_j(s) r(s).
```

Suppress `j` and write

```text
u = u_j,
F = P_A u.
```

Let `C = {C_alpha}` be a disjoint source-derived cube chart with

```text
Q = union_alpha C_alpha subseteq S.
```

The chart is assumed to cover `supp u`; uncovered selected syndromes must be
kept as an explicit residual.  Define `E_C` to take the class mean on each
`C_alpha` and to be zero on `G \ Q`.

## 2. Exact ambient decomposition

### Proposition 2.1

For every `F : G -> C`,

\[
\begin{aligned}
\|F-E_{\mathcal C}F\|_4^4
={}&\sum_\alpha\sum_{x\in C_\alpha}
\left|F(x)-{|C_\alpha|}^{-1}\sum_{y\in C_\alpha}F(y)\right|^4\\
&+\sum_{x\in\mathcal S\setminus Q}|F(x)|^4
+\sum_{x\in G\setminus\mathcal S}|F(x)|^4.
\end{aligned}
\tag{2.1}
\]

In particular,

\[
\boxed{
\|F-E_{\mathcal C}F\|_4
\ge \|1_{G\setminus\mathcal S}F\|_4.
}
\tag{2.2}
\]

If `Q = S`, then

\[
\|F-E_{\mathcal C}F\|_4^4
=\|1_{\mathcal S}(I-E_{\mathcal C})F\|_4^4
+\|1_{G\setminus\mathcal S}F\|_4^4.
\tag{2.3}
\]

### Proof

On a chart class, subtract the printed class mean.  On `G \ Q`,
`E_C F = 0`.  The three displayed regions are disjoint, so their fourth
powers add exactly.  `square`

### Consequence: ambient leakage is a separate theorem

Any universal no-cell SOCML4 statement with `E_C` zero off the realized image
necessarily contains

\[
\boxed{
L^{-1/4}\|1_{G\setminus\mathcal S}P_Au\|_4
\le e^{o(N)}.
}
\tag{AL4}
\]

Within-image Walsh derivatives and cube averaging do not change a single
value on `G \ S`; they cannot prove `(AL4)` by themselves.

## 3. Exact empty-mode commutator guard

Let `E = E_C`.  Since `E` is a real self-adjoint idempotent, the empty Walsh
charge is

\[
c_0=\langle Eu,Er\rangle_{\mathbb R}.
\tag{3.1}
\]

### Proposition 3.1

One has the exact identity

\[
\begin{aligned}
c_0
&=\operatorname{Re}\langle Eu,P_Ag\rangle\\
&=\operatorname{Re}\langle E(P_Au),g\rangle
+\operatorname{Re}\langle(P_AE-EP_A)u,g\rangle.
\end{aligned}
\tag{3.2}
\]

Consequently,

\[
\boxed{
\left|c_0-\operatorname{Re}\langle E(P_Au),g\rangle\right|
\le \|[P_A,E]u\|_4.
}
\tag{3.3}
\]

### Proof

The first equality is the definition of `r` and real self-adjointness of
`E`.  Move the self-adjoint Fourier projection from `g` to `Eu`, add and
subtract `E(P_Au)`, and apply Holder with `||g||_(4/3) <= 1`.  `square`

### Full charge

On an admitted affine Boolean cube, write normalized Walsh coefficients as
`hat u_alpha(D)` and `hat r_alpha(D)`.  The complete charge is

\[
\boxed{
c(u)=c_0+
\sum_\alpha 2^{d_\alpha}
\sum_{\varnothing\ne D\subseteq[d_\alpha]}
\widehat u_\alpha(D)\widehat r_\alpha(D)
+c_{\rm uncovered}.
}
\tag{3.4}
\]

SOCML4 controls `(I-E)P_Au`; it does not control `[P_A,E]u`, and it does not
compress the nonempty sum in (3.4).  A compiler theorem must prove one of:

```text
commutator control plus signed nonempty-mode compression;
direct selected-owner semantic classification of the exact mode charges.
```

The per-pattern floor from the band-uniform packet remains sound, but summing
it over all raw modes can cost an exponential factor.

## 4. Hamming ambient-leakage guardrail

This section gives a source-free boundary regression.  It is not a valid
post-atlas Reed-Solomon falsifier and is not in the unresolved low-depth
weighted-Vandermonde class.

Let

```text
G = F_2^n,
n = 4m,
S = {x in F_2^n : |x| = n/2},
L = C(n,n/2).
```

Use standard-basis subset-sum columns, so

```text
tau(y) = n - 2|y|.
```

Take the complete dyadic source-score band

\[
A_2=\{y:4\le|\tau(y)|<8\},
\tag{4.1}
\]

which consists of the four shells `|y| = n/2 +/- 2, n/2 +/- 3`.

### Lemma 4.1: exact middle-layer kernel

For every `s in S`,

\[
K_{A_2}(s)=
2^{1-n}(-1)^{m+1}\binom{n/2}{n/4-1}.
\tag{4.2}
\]

### Proof

For `a = n/2`, the Krawtchouk generating function is

\[
\sum_w K_w(a)z^w=(1-z)^a(1+z)^a=(1-z^2)^a.
\]

The odd shells vanish.  The two even shells give

\[
K_{a-2}(a)+K_{a+2}(a)
=2(-1)^{m+1}\binom{2m}{m-1}.
\]

Divide by `|G| = 2^n`.  `square`

Put

\[
\kappa_n=2^{1-n}\binom{n/2}{n/4-1}.
\tag{4.3}
\]

Choose distinct labels `ell_1,...,ell_n in F_2^r`, where
`r = ceil(log_2 n)`, and color the middle layer by

\[
c(X)=\sum_{i\in X}\ell_i.
\tag{4.4}
\]

If two middle-layer sets share an `(a-1)`-rim, they differ by exchanging
`i != j`, and their colors differ by `ell_i + ell_j != 0`.  Every color class
is therefore rim-free.  Some class `E` satisfies

\[
|E|\ge {L\over2^r}\ge {L\over2n}.
\tag{4.5}
\]

Let `f = 1_E`, take its exact quartic norming dual, and let

```text
u = 1_{s in E : r_A(s) > 0}
```

be its selected positive unit layer.

### Proposition 4.2: positive-rate ambient value

Every chart supported inside `S` obeys

\[
L^{-1/4}\|P_{A_2}u-E_{\mathcal C}(P_{A_2}u)\|_4
\ge {\kappa_n^3L^{7/4}\over(2n)^2},
\tag{4.6}
\]

and

\[
\log\left({\kappa_n^3L^{7/4}\over(2n)^2}\right)
={\log2\over4}n-O(\log n).
\tag{4.7}
\]

### Proof

Radiality and Lemma 4.1 give

\[
|P_{A_2}f(0)|=\kappa_n|E|.
\]

Positive rooting and projection contraction give

\[
\sqrt{|\operatorname{supp}u|}
\ge\|P_{A_2}u\|_4
\ge\|P_{A_2}f\|_4
\ge\kappa_n|E|.
\]

Thus `|supp u| >= kappa_n^2 |E|^2`.  Since the kernel has the same signed
value at every middle-layer point,

\[
|P_{A_2}u(0)|
=\kappa_n|\operatorname{supp}u|
\ge\kappa_n^3|E|^2.
\]

The origin is outside `S`, so `E_C(P_Au)(0) = 0`.  Apply (4.5), normalize by
`L^(1/4)`, and use Stirling's formula.  `square`

This regression proves that ambient leakage is a real positive-rate mechanism
for source-free middle-layer charts.  It does not prove that a semantically
saturated low-depth RS profile survives the existing atlas.

## 5. Equitable full-group reduction

Let `Pi = {B_beta}` be a source-derived partition of all of `G`, and let
`E_Pi` be conditional expectation onto functions constant on its parts.
Assume every admitted source cube is a part of `Pi`, and retain
`Q = union C_alpha`.

The analytic assumptions are:

```text
(EQ1) E_Pi f = f.

(EQ2) P_A Ran(E_Pi) subseteq Ran(E_Pi).

(EQ3) L^(-1/4) ||1_{G\Q} P_Au||_4 <= exp(epsilon_N N),
      with epsilon_N -> 0.
```

Because `P_A` is self-adjoint, `(EQ2)` is equivalent to

\[
[P_A,E_\Pi]=0.
\tag{5.1}
\]

Equivalently, for every two partition cells `B_beta,B_beta'`,

\[
\sum_{y\in B_{\beta'}}K_A(x-y)
\]

is independent of `x in B_beta`.

### Theorem 5.1: equitable-chart SOCML4 reduction

Under `(EQ1)-(EQ3)`,

\[
\boxed{
L^{-1/4}\|P_Au-E_{\mathcal C}(P_Au)\|_4
\le e^{\epsilon_NN}.
}
\tag{5.2}
\]

### Proof

By `(EQ1)-(EQ2)`, `h = P_Af` is `Pi`-measurable.  If `h = 0`, the canonical
dual and all selected layers vanish, so the conclusion is immediate.
Otherwise its exact norming dual

\[
g(x)={|h(x)|^2h(x)\over\|h\|_4^3}
\]

is a pointwise function of `h`, so it is `Pi`-measurable.  Another use of
`(EQ2)` makes `P_Ag` and `r` measurable.  Hence `b`, every threshold layer
`u`, and finally `F = P_Au` are `Pi`-measurable.

Thus `F` is constant on each admitted cube and `E_C F = F` on `Q`.  Therefore

\[
F-E_CF=1_{G\setminus Q}F,
\]

and `(EQ3)` proves (5.2).  `square`

This is a reduction criterion, not a universal proof: `(EQ3)` is the ambient
and uncovered-part estimate remaining after equitability kills within-cube
variation.

## 6. Paid empty-mode admission

Equitability also makes `u` and `r` constant on each admitted source cube, so

\[
\widehat u_\alpha(D)=\widehat r_\alpha(D)=0
\qquad(D\ne\varnothing).
\tag{6.1}
\]

If the chart covers `supp u`, the exact natural charge becomes

\[
c(u)=\sum_\alpha |C_\alpha|u_\alpha r_\alpha.
\tag{6.2}
\]

Equation (6.2) eliminates nonempty-mode compression.  It does not by itself
prove an atlas payment.  For that conclusion one must add:

```text
(EQ4) Paid empty-mode admission.

Each active source-cube type is an enabled earlier atlas cell.  The packet
prints a verifier-checkable source derivation, the exact selected owners in
that cell, a validated owner-level projection/payment theorem, whole-slope
first-match semantics, and an exp(o(N)) aggregate type/multiplicity census.
```

### Theorem 6.1: conditional equitable SOCQI4

Under `(EQ1)-(EQ4)`, every active equitable selected layer is contained in a
paid empty-mode cell at the same selected owners.  Together with Theorem 5.1,
this gives the equitable-chart SOCML4 and CSAP4 conclusions and the resulting
SOCQI4 inverse implication.

### Proof

Theorem 5.1 gives the analytic localization.  Equation (6.1) leaves only the
empty mode, while `(EQ4)` supplies the independently validated admission and
payment at the owners actually attached to the selected layer.  Whole-slope
first match removes those owners before the later residual.  `square`

Theorem 6.1 is intentionally conditional.  Omitting the payment theorem from
`(EQ4)` would rename the open admission problem rather than solve it.

## 7. Unconditional maximal-band theorem

Let

\[
A_*=\widehat G\setminus\{1\}.
\]

Then

\[
P_{A_*}h=h-H^{-1}\sum_{x\in G}h(x).
\tag{7.1}
\]

### Theorem 7.1

For every unit mask `u = 1_E` with `m = |E| <= L`,

\[
\boxed{
L^{-1/4}\|P_{A_*}u\|_4\le2^{1/4}.
}
\tag{7.2}
\]

Hence the maximal band cannot produce a positive-rate selected-layer quartic
violation, without any cube or semantic assumption.

### Proof

The projection takes value `1-m/H` on `E` and `-m/H` off `E`.  Therefore

\[
\begin{aligned}
\|P_{A_*}u\|_4^4
&=m(1-m/H)^4+(H-m)(m/H)^4\\
&\le m+m^4/H^3\\
&\le2m\le2L.
\end{aligned}
\]

Take fourth roots.  `square`

### Corollary 7.2: maximal-band ambient residual

If source cubes cover `S` and `u` is constant on them, then

\[
L^{-1/4}\|P_{A_*}u-E_{\mathcal C}(P_{A_*}u)\|_4
= {m\over H}\left({H-L\over L}\right)^{1/4}
\le\left({L\over H}\right)^{3/4}
 \left(1-{L\over H}\right)^{1/4}
\le1.
\tag{7.3}
\]

Indeed, the difference is `-m/H` on `G \ S`, zero on `S`, and `m <= L`.

## 8. Correct universal target

After this audit, a general selected-owner cube theorem must prove three
separate uniform inputs:

\[
L^{-1/4}\|1_{G\setminus\mathcal S}P_Au\|_4=e^{o(N)},
\tag{8.1}
\]

\[
L^{-1/4}\|1_{\mathcal S}(I-E_{\mathcal C})P_Au\|_4=e^{o(N)},
\tag{8.2}
\]

and either

\[
L^{-1/4}\|[P_A,E_{\mathcal C}]u\|_4=e^{o(N)}
\tag{8.3}
\]

plus signed nonempty-mode compression, or a direct selected-owner semantic
classifier paying the exact terms in (3.4).

The tested cube-capture census reports an image `L4` fraction close to one on
its largest source-model row (`0.999268` at `B = 12`, `q = 4.199`).  That is
finite evidence for (8.1) on those rows, not a uniform theorem.  The Hamming
guardrail shows why the ambient term must still be printed as a separate
obligation.

## 9. Ledger impact

This packet changes the proof plan in four ways.

1. A source-cube localization theorem must print an ambient leakage input or
   use a controlled partition of all `G`.
2. Empty-mode charge cannot be identified with the projected cube mean unless
   the commutator is controlled or equitability is proved.
3. Exact base-3 hierarchy flatness becomes compiler-useful only after its
   operator-level equitability and paid-admission interfaces are checked.
4. The maximal band is removed from the quartic selected-layer residual
   unconditionally by Theorem 7.1.

No finite deployed row, row-sharp Q theorem, general SULSI theorem, or
asymptotic RS-MCA theorem is closed.

## 10. Reproducibility and nonclaims

The verifier checks:

```text
exact Krawtchouk shell identity for n = 4m;
exact rim-free color-class census;
the positive-rate lower-bound formula and asymptotic exponent ledger;
finite commutator identities and a nonzero commutator guardrail;
equitable-partition invariance and selected-layer measurability;
the maximal-band quartic and ambient formulas;
certificate replay and semantic tamper rejection.
```

The Hamming family is a source-free ambient guardrail, not a valid
source-derived post-atlas falsifier.  Finite checks do not prove any asymptotic
source estimate.  The equitable theorem assumes `(EQ3)`, and the SOCQI4
conclusion separately assumes the paid admission theorem `(EQ4)`.

No `.tex`, `.pdf`, or stable paper source is modified.
