# Mask-aware band restriction audit v1

```text
Status: AUDIT / PROVED SPARSE-PATTERN AND TOP-ORDER REDUCTIONS / OPEN ROOTED DENSE-BAND BCI
Theorem status: no A4 payment, primitive-Q theorem, or exceptional compiler is proved
```

## Purpose and claim boundary

The proposed signed exceptional-spectrum lemma cannot be obtained from the
available moment bounds for

\[
 \tau(\gamma)=\sum_{t\in T}\gamma(v_t)
\]

alone.  Those moments depend only on the profile columns.  The signed Fourier
coefficients depend on the exact first-match residual mask, and an arbitrary
mask can concentrate on one heavy fiber without changing any \(\tau\)-moment.

This note records four distinct results:

1. exact zero-character peeling into lower centered moments;
2. two deterministic tuple-tail certificates from the printed \(\tau\)-moments;
3. a diagonal and planted-pair regression showing that these results do not
   imply a mask-blind signed-bulk estimate; and
4. an unconditional mask-aware payment for every pattern satisfying the
   sparse band-density criterion;
5. a top-order restriction compiler, endpoint guardrails, and an exact dual
   witness for every remaining `(MBR)` failure.

All five reductions are proved.  The dense low-\(|\tau|\) top-order restriction
estimate, or equivalently its source-specific rooted band-to-cell inverse
theorem `(BCI)`, remains open.  These results are not the full A4 theorem: exceptional
band patterns still need an inverse theorem and a semantic
frequency-to-witness compiler.

This packet is a follow-up to PR #674.  That PR separates formal
ledger-admissibility, which already includes `(A4)`, from the unpaid pre-A4
primitive residual and gives the planted-pair Q regression.  The present note
does not duplicate its PRE/Q/Sidon boundary.  It asks what additional
mask-aware estimate would pay only the signed bulk.

## 1. Fourier conventions

Fix a finite abelian image group \(G\), write \(H=|G|\), and let

\[
 f(s)=|\Omega^\circ\cap\Phi^{-1}(s)|,
 \qquad W=\widehat f(0)=\sum_s f(s)=|\Omega^\circ|.
\]

The full profile slice supplies

\[
 M=|\Omega^0|,
 \qquad L=|\Phi(\Omega^0)|,
 \qquad \bar N=M/L,
\]

with \(W\le M\).  Use the unnormalized transform

\[
 \widehat f(\gamma)=\sum_{s\in G}f(s)\overline{\gamma(s)},
 \qquad
 f(s)=H^{-1}\sum_{\gamma\in\widehat G}
 \widehat f(\gamma)\gamma(s).
\]

All \(\ell^r(G)\) norms below use counting measure.

For logarithmic order \(q\), the normalized moment is

\[
 \Gamma_q
 =\frac1L\sum_s\left(\frac{f(s)}{\bar N}\right)^q
 =\frac{L^{q-1}}{M^q}\sum_s f(s)^q.
\tag{1}
\]

The target signed-bulk estimate is a bound of size \(\exp(o(Nq))\) after
this normalization.  The group size \(H\) is not substituted for the realized
image size \(L\).

## 2. Exact zero-character peeling

For \(j\ge2\), define

\[
 U_j^*=
 \sum_{\substack{\gamma_1+\cdots+\gamma_j=0\\
                   \gamma_i\ne0}}
 \prod_{i=1}^j\widehat f(\gamma_i),
 \qquad U_1^*=0.
\]

### Proposition 2.1

For every integer \(q\ge2\),

\[
 \boxed{
 H^{q-1}\sum_s f(s)^q
 =W^q+\sum_{j=2}^q\binom qjW^{q-j}U_j^*.
 }
\tag{2}
\]

### Proof

Fourier inversion and character orthogonality give

\[
 H^{q-1}\sum_s f(s)^q
 =\sum_{\gamma_1+\cdots+\gamma_q=0}
   \prod_{i=1}^q\widehat f(\gamma_i).
\]

Partition the tuple according to the \(j\) nonzero coordinates.  The all-zero
tuple contributes \(W^q\), no tuple has exactly one nonzero coordinate, and a
chosen set of \(j\ge2\) nonzero coordinates contributes \(W^{q-j}U_j^*\).
Summing the choices proves (2).  \(\square\)

There is also an exact physical-space form.  If

\[
 g(s)=f(s)-W/H,
\]

then \(\widehat g(0)=0\) and \(\widehat g(\gamma)=\widehat f(\gamma)\) for
\(\gamma\ne0\), so

\[
 \boxed{U_j^*=H^{j-1}\sum_s g(s)^j.}
\tag{3}
\]

Define

\[
 \mathcal C_j=
 \frac{L^{j-1}}{M^jH^{j-1}}U_j^*,
 \qquad
 \vartheta=\frac{LW}{MH}\le1.
\]

Equations (1)--(2) become

\[
 \boxed{
 \Gamma_q=
 \left(\frac LH\right)^{q-1}\left(\frac WM\right)^q
 +\sum_{j=2}^q\binom qj\vartheta^{q-j}\mathcal C_j.
 }
\tag{4}
\]

Thus zero-character sectors reduce exactly to lower-order centered sectors.
If the nonzero-character payments are uniform for \(2\le j\le q\), the factors
\(\vartheta^{q-j}\), \(2^q\), and a subexponential profile census do not create
an exponential loss on the \(Nq\) scale.

## 3. Exact tuple-tail certificates

For a nonzero zero-sum \(q\)-tuple put

\[
 S(\boldsymbol\gamma)
 =\left(\prod_{i=1}^q|\tau(\gamma_i)|\right)^{1/q}
\]

and define

\[
 \mathcal E_q(\Theta)
 =\{\boldsymbol\gamma:\gamma_i\ne0,
      \ \sum_i\gamma_i=0,\ S(\boldsymbol\gamma)\ge\Theta\}.
\]

Assume the printed moment certificate

\[
 \sum_{\gamma\in\widehat G}|\tau(\gamma)|^{2h}
 \le Hh!N^h
\tag{5}
\]

for the stated range of \(h\).

### Proposition 3.1: one-coordinate tail

For every admissible \(h\ge1\) and \(\Theta>0\),

\[
 \boxed{
 \frac{|\mathcal E_q(\Theta)|}{H^{q-1}}
 \le qh!\frac{N^h}{\Theta^{2h}}.
 }
\tag{6}
\]

If the geometric mean is at least \(\Theta\), one coordinate has magnitude at
least \(\Theta\).  Markov applied to (5) bounds the number of such characters
by \(Hh!N^h/\Theta^{2h}\).  After that coordinate and its position are fixed,
at most \(H^{q-2}\) zero-sum tuples remain.  This proves (6).

### Proposition 3.2: tensor-Hölder tail

If the moment certificate is available through order \(2hq\), then

\[
 \boxed{
 \frac{|\mathcal E_q(\Theta)|}{H^{q-1}}
 \le (hq)!\frac{N^{hq}}{\Theta^{2hq}}.
 }
\tag{7}
\]

Indeed, on \(\mathcal E_q(\Theta)\),

\[
 1\le\Theta^{-2hq}\prod_i|\tau(\gamma_i)|^{2h}.
\]

Parametrize a zero-sum tuple by its first \(q-1\) coordinates.  Hölder on
\(G^{q-1}\) gives

\[
 \sum_{\sum\gamma_i=0}\prod_i|\tau(\gamma_i)|^{2h}
 \le H^{q-2}\sum_\gamma|\tau(\gamma)|^{2hq},
\]

and (5) at order \(hq\) proves (7).

These propositions certify that a chosen tuple sector is sparse.  They do not
bound its Fourier mass, and they do not control the complementary signed sum.

## 4. Why the mask-blind bulk lemma fails

### 4.1 Vacuous thresholds

An assertion of the form "there exists \(\Theta\) such that the bulk is
small" is vacuous if \(\Theta=0\) is allowed: every tuple is exceptional and
the bulk sum is empty.  A useful threshold must have a printed tail guarantee,
or the decomposition must be stated directly as a finite union of complete
band patterns.

### 4.2 Diagonal point-mass obstruction

Let the residual be supported on one image point:

\[
 f(s)=r\mathbf1_{s=s_0}.
\]

Then

\[
 \widehat f(\gamma)=r\overline{\gamma(s_0)}.
\]

For every zero-sum tuple,

\[
 \prod_i\widehat f(\gamma_i)=r^q.
\]

Hence for any tuple set \(\mathcal B\),

\[
 \boxed{
 \frac{L^{q-1}}{M^qH^{q-1}}
 \sum_{\boldsymbol\gamma\in\mathcal B}
 \prod_i\widehat f(\gamma_i)
 =\frac{|\mathcal B|}{H^{q-1}}
  \frac1L\left(\frac r{\bar N}\right)^q.
 }
\tag{8}
\]

If \(r\ge e^{\eta N}\bar N\) and the bulk has density
\(e^{-o(Nq)}\), (8) has positive exponential \(Nq\)-rate.  There is no sign
cancellation to recover: every summand has the same phase.

This obstruction is independent of the \(\tau\)-moments because those moments
do not see which supports survive the residual mask.

### 4.3 Planted weighted-Vandermonde regression

PR #674 gives an exact family realizing this logic.  For even \(B\), take
\(N=2B\), \(m=B\), and paired rank-one weighted-Vandermonde columns

\[
 \rho_{i,+}=a_i,\qquad \rho_{i,-}=C-a_i,
 \qquad a_i=Q^i,
\]

with \(Q\ge5\), \(C>4\sum_i a_i\), and characteristic large enough to avoid
wraparound.  On the middle slice the image determines the vector
\(\delta_i=x_{i,+}-x_{i,-}\), and

\[
 L=(3^B+1)/2,\qquad M=\binom{2B}{B},\qquad
 r_B=\binom B{B/2}.
\]

Therefore

\[
 \log(r_B/\bar N)=B\log(3/2)+O(\log B).
\tag{9}
\]

For \(q=\lceil\log N\rceil\) and \(\Theta=N^{3/4}\), the second-moment
certificate gives

\[
 |\mathcal E_q(\Theta)|/H^{q-1}\le q/\sqrt N=o(1),
\]

yet choosing the exact residual mask to be the heavy fiber makes the
complementary bulk in (8) grow at rate

\[
 \frac1{Nq}\log(\text{normalized bulk})
 \longrightarrow \frac12\log(3/2)>0.
\tag{10}
\]

The family is deliberately planted and is not a falsifier for a source class
whose semantic atlas certifies and pays the relation
\(\rho_{i,+}+\rho_{i,-}=C\).  It proves that the certification theorem is
indispensable.  Column moments plus an unattached structural name do not pay
the residual mask.

## 5. Correct finite band grammar

The earlier raw dyadic formulation needs two repairs.

First, nonzero \(|\tau(\gamma)|\) has no uniform positive lower bound, so bands
indexed over all negative integers are not a finite \(O(\log N)\) partition.
Use instead

\[
 A_{<1}=\{\gamma\ne0:|\tau(\gamma)|<1\}
\]

and

\[
 A_k=\{\gamma\ne0:2^k\le|\tau(\gamma)|<2^{k+1}\},
 \qquad 0\le k\le\lceil\log_2N\rceil.
\tag{11}
\]

These symmetric sets partition the nonzero dual because \(|\tau|\le N\).

Second, a numerical score cutoff can split one band pattern.  The Fourier
projection identity below applies only to a complete pattern.  Therefore the
compiler must classify complete patterns as bulk or exceptional; any pattern
straddling the intended threshold cannot be cut tuple by tuple.

There is one further low-band guardrail.  A pattern containing `A_<1` has
no positive lower score, so enlarging it into the exceptional sector is not
controlled by a constant threshold shift.  Such patterns are assigned wholly
to the bulk and must be paid by `(MBR)`.  For patterns using only `A_k` with
`k >= 0`, upper and lower geometric scores differ by at most a factor of two.
Assigning a straddling pattern to the exceptional side is then controlled by
the tuple-tail certificate at threshold `Theta/2`.

In short, every bulk sector used below is a union of **complete band patterns**.

For a band \(A_k\), define the exact residual projection

\[
 P_kf(s)=H^{-1}\sum_{\gamma\in A_k}
 \widehat f(\gamma)\gamma(s).
\tag{12}
\]

For a pattern \(\mathbf k=(k_1,\ldots,k_j)\), let

\[
 \mathcal T_{\mathbf k}
 =\{(\gamma_1,\ldots,\gamma_j):
      \gamma_i\in A_{k_i},\ \sum_i\gamma_i=0\}.
\]

### Proposition 5.1: complete-pattern identity

\[
 \boxed{
 \sum_{\boldsymbol\gamma\in\mathcal T_{\mathbf k}}
 \prod_{i=1}^j\widehat f(\gamma_i)
 =H^{j-1}\sum_{s\in G}\prod_{i=1}^jP_{k_i}f(s).
 }
\tag{13}
\]

This follows by expanding the right side and applying character orthogonality.
Symmetry of the bands and reality of \(f\) make each \(P_kf\), and hence the
right side, real.  It need not be nonnegative.

## 6. Proved restriction range and exact remaining target

### 6.1 Quantitative bulk density

Merely requiring a nonempty bulk is too weak.  For a collection
\(\mathscr K_j^{\rm bulk}\) of complete patterns, define its normalized tuple
density by

\[
 \beta_j=H^{1-j}
 \sum_{\mathbf k\in\mathscr K_j^{\rm bulk}}
 |\mathcal T_{\mathbf k}|.
\tag{14}
\]

A useful decomposition must print a lower bound for \(\beta_j\), an upper
bound for the exceptional tuple density, or a direct bound for the exceptional
contribution.  A single bulk tuple has density only \(H^{1-j}\).

For later normalization, define

\[
 \mathcal C_{j,\mathbf k}
 =\frac{L^{j-1}}{M^j}
 \sum_s\prod_{i=1}^jP_{k_i}f(s).
\tag{15}
\]

Equation (13) and the zero-character peeling give the exact pattern form

\[
 \boxed{
 \Gamma_q=
 \left(\frac LH\right)^{q-1}\left(\frac WM\right)^q
 +\sum_{j=2}^q\binom qj
  \left(\frac{LW}{MH}\right)^{q-j}
  \sum_{\mathbf k\in\mathscr I^j}\mathcal C_{j,\mathbf k}.
 }
\tag{16}
\]

Since \(L\le H\) and \(W\le M\), the multiplier \(LW/(MH)\) lies in
\([0,1]\).  Lower-order pattern estimates therefore need only fit the final
\(\exp(o(Nq))\) scale; they do not intrinsically need a separate
\(\exp(o(Nj))\) theorem at every order.

### 6.2 Universal sparse-pattern payment

The following result is unconditional and retains the exact residual mask.

### Theorem 6.1: band-density restriction

For \(A\subseteq\widehat G\), put

\[
 P_Af(s)=H^{-1}\sum_{\gamma\in A}\widehat f(\gamma)\gamma(s),
 \qquad \delta_A=|A|/H.
\]

For every \(r\ge2\),

\[
 \boxed{
 \|P_Af\|_{\ell^r(G)}\le W\delta_A^{1-1/r}.
 }
\tag{17}
\]

Consequently, if \(\delta_k=|A_k|/H\) and

\[
 D_{\mathbf k}=\left(\prod_{i=1}^j\delta_{k_i}\right)^{1/j},
\]

then

\[
 \boxed{
 \left|\sum_s\prod_{i=1}^jP_{k_i}f(s)\right|
 \le W^jD_{\mathbf k}^{j-1}.
 }
\tag{18}
\]

Writing \(\rho=W/M\le1\), the image-normalized form is

\[
 \boxed{
 |\mathcal C_{j,\mathbf k}|
 \le \rho\bigl(L\rho D_{\mathbf k}\bigr)^{j-1}.
 }
\tag{19}
\]

### Proof

Positivity gives \(|\widehat f(\gamma)|\le W\), so

\[
 \|P_Af\|_\infty\le W\delta_A.
\]

Parseval gives

\[
 \|P_Af\|_2^2
 =H^{-1}\sum_{\gamma\in A}|\widehat f(\gamma)|^2
 \le W^2\delta_A.
\]

Therefore

\[
 \|P_Af\|_r^r
 \le\|P_Af\|_\infty^{r-2}\|P_Af\|_2^2
 \le W^r\delta_A^{r-1},
\]

which proves (17).  Hölder proves (18), and substituting \(W=\rho M\)
proves (19).  \(\square\)

For \(k\ge0\), the printed \(\tau\)-moment estimate implies

\[
 \boxed{
 \delta_k\le
 \min_{1\le h\le R}\frac{h!N^h}{2^{2hk}}.
 }
\tag{20}
\]

Different coordinates of a pattern may use different values of \(h\).  Thus
every pattern satisfying

\[
 \boxed{L\rho D_{\mathbf k}\le\exp(o(N))}
\tag{21}
\]

is paid absolutely, hence signed, at the required scale.  Equivalently, the
criterion is \(\log^+(L\rho D_{\mathbf k})=o(N)\).  This positive-part form is
important: an exponentially smaller value is easier to pay and must not be
excluded by writing the stronger equality \(\log(L\rho D)=o(N)\).

The result does not generally pay dense low-\(|\tau|\) bands.  In particular,
the moment estimate may give only \(\delta_{<1}\le1\).

### 6.3 Open dense-band MBR and a top-order compiler

The remaining mask-aware multilinear band restriction payment is

\[
 \boxed{
 \sum_s\prod_{i=1}^jP_{k_i}f(s)
 \le \exp(\varepsilon_NNj)\frac{M^j}{L^{j-1}},
 \qquad \varepsilon_N\to0,
 }
\tag{MBR}
\]

for every source-derived semantically saturated bulk pattern.  That phrase is
only shorthand here for the received-line/profile, whole-slope residual,
effective-group, incidence, and owner data listed in Section 6.6; it is not a
standalone Fourier-mask predicate.  The estimate is signed; an absolute-value
estimate is sufficient but stronger.

It is unnecessary to prove a separate strong linear estimate at every order.

### Theorem 6.2: top-order restriction compiler

Let \(q\ge3\).  Suppose every band used in the certified bulk satisfies

\[
 \boxed{
 \|P_kf\|_{\ell^q(G)}
 \le \exp(\varepsilon_NN)\frac{M}{L^{1-1/q}}.
 }
\tag{q-BR}
\]

Then for every \(2\le j\le q\) and every pattern built from those bands,

\[
 \boxed{
 |\mathcal C_{j,\mathbf k}|
 \le \exp(\varepsilon_NNj)L^{(q-j)/(q-2)}.
 }
\tag{22}
\]

After (16), all such bulk patterns through order \(q\) contribute only
\(\exp(o(Nq))\), assuming the printed accessibility
\(\log L=o(Nq)\).

### Proof

Orthogonal projection on \(\ell^2(G)\) gives

\[
 \|P_kf\|_2\le\|f\|_2\le\|f\|_1=W\le M.
\]

For \(2\le j\le q\), put

\[
 \theta_j=\frac{2(q-j)}{j(q-2)},
 \qquad
 \frac1j=\frac{\theta_j}{2}+\frac{1-\theta_j}{q}.
\]

Interpolation with `(q-BR)` yields

\[
 \|P_kf\|_j
 \le \exp((1-\theta_j)\varepsilon_NN)
 M L^{-(1-\theta_j)(1-1/q)}.
\]

Hölder and direct simplification give (22).  There are at most
\(K^j\) patterns at order \(j\), where \(K=O(\log N)\), and

\[
 \sum_{j=0}^q\binom qjK^j=(1+K)^q
 =\exp(o(Nq)).
\]

The largest remaining factor from (22) is \(L\), whose logarithm is
\(o(Nq)\) by accessibility.  Equation (16) completes the proof.  \(\square\)

Thus the open bulk problem is concentrated in top-order restriction on the
dense low-\(|\tau|\) bands.

### 6.4 Dense MBR already contains the max-atom endpoint

For a point-mass residual \(f(s)=r\mathbf1_{s=s_0}\), define

\[
 d_{\mathbf k}=|\mathcal T_{\mathbf k}|/H^{j-1}.
\]

Every zero-sum tuple has product \(r^j\), so exactly

\[
 \boxed{
 \mathcal C_{j,\mathbf k}
 =\frac{d_{\mathbf k}}L\left(\frac r{\bar N}\right)^j.
 }
\tag{23}
\]

If \(\beta_q\) is the total density (14) of the top-order bulk patterns and
each obeys `(MBR)`, then

\[
 \boxed{
 \log\frac r{\bar N}
 \le \varepsilon_NN+\log K
 +\frac{\log L-\log\beta_q}{q}.
 }
\tag{24}
\]

Hence accessibility and \(-\log\beta_q=o(Nq)\) force
\(r\le\exp(o(N))\bar N\).  Nonempty bulk is not enough; quantitative tuple
density is essential.

There is also a per-band point-mass guardrail.  Choose a dyadic threshold
\(T\) with

\[
 N^{3/4}/2\le T\le N^{3/4}.
\]

The second \(\tau\)-moment gives

\[
 H^{-1}|\{\gamma:|\tau(\gamma)|\ge T\}|
 \le N/T^2\le4/\sqrt N.
\]

After removing the zero character, the remaining low spectrum has density at
least \(1-H^{-1}-4/\sqrt N\) and is partitioned into
\(K=O(\log N)\) complete bands.  Hence some low band has

\[
 \delta_k\ge\frac{1-H^{-1}-4/\sqrt N}{K}.
\tag{23a}
\]

For \(f=r\mathbf1_{s=s_0}\), Fourier inversion gives exactly

\[
 P_kf(s_0)=r\delta_k,
 \qquad
 \|P_kf\|_q\ge r\delta_k.
\tag{23b}
\]

Thus `(q-BR)` on every low band already forces

\[
 \frac r{\bar N}
 \le
 \exp(\varepsilon_NN)
 \frac{K L^{1/q}}{1-H^{-1}-4/\sqrt N}
 =\exp(o(N))
\]

under accessibility.  This rules out proving the dense low-band theorem by a
mask-blind density, Hausdorff--Young, hypercontractive, or uncertainty estimate;
it is a route cut, not a source-derived counterexample.

There is a broader endpoint.  Let \(q\) be even, let \(\mathscr B\) be the
bands whose repeated pattern is certified bulk, and put

\[
 E=\bigcup_{k\notin\mathscr B}A_k,
 \qquad \delta_E=|E|/H.
\]

Repeated-pattern `(MBR)` implies

\[
 \boxed{
 f_{\max}\le
 \frac WH+W\delta_E
 +|\mathscr B|\exp(\varepsilon_NN)
  \frac{M}{L^{1-1/q}}.
 }
\tag{25}
\]

Indeed, decompose \(f=W/H+P_Ef+\sum_{k\in\mathscr B}P_kf\), use
\(|P_Ef|\le W\delta_E\), and take the \(q\)-th root of repeated-pattern
`(MBR)`.  If

\[
 \delta_E\le\exp(o(N))/L,
\tag{26}
\]

then (25), accessibility, and \(|\mathscr B|=O(\log N)\) give primitive Q.
If the supplied accessible order is odd, replacing it by the nearest smaller
even order preserves \(q\to\infty\) and \(\log L/q=o(N)\).

This does not make `(MBR)` circular, but it identifies its true strength: a
dense-bulk theorem with image-scale exceptional-frequency control already
contains the primitive max-atom endpoint.

### 6.5 The positive band-energy subtarget

For every symmetric band,

\[
 \boxed{
 \sum_s(P_kf(s))^2
 =H^{-1}\sum_{\gamma\in A_k}|\widehat f(\gamma)|^2.
 }
\tag{27}
\]

Thus order-two `(MBR)` is the positive collision-energy estimate

\[
 H^{-1}\sum_{\gamma\in A_k}|\widehat f(\gamma)|^2
 \le \exp(2\varepsilon_NN)\frac{M^2}{L}.
\tag{28}
\]

There is no signed cancellation in (28).  The open one-sided secant statistic
`(SV*)` and the normalized CHG/Hankel--Salié aggregate are different signed
objects.  Either could prove primitive Q and then imply (28), but neither
existing reduction directly proves this band energy.

The order-two dual witness localizes exactly to the PRE/Q endpoint.  If
\(\|u\|_2=1\) and

\[
 \langle P_kf,u\rangle>A,
\]

then orthogonality, Cauchy--Schwarz, and nonnegativity give

\[
 A^2<\|P_kf\|_2^2\le\|f\|_2^2
 =\sum_s f(s)^2\le f_{\max}W.
\tag{28a}
\]

Therefore

\[
 \boxed{f_{\max}>A^2/W.}
\tag{28b}
\]

At \(A=\exp(\varepsilon_NN)M/\sqrt L\), the inequality \(W\le M\)
gives

\[
 f_{\max}>\exp(2\varepsilon_NN)M/L.
\]

Thus a \(j=2\) BCI witness emits only the same PRE/Q-heavy endpoint.  On the
unpaid residual, converting that endpoint into quotient, planted, field, rank,
saturation, or pencil structure is precisely the open semantic compiler.

### 6.6 Exact dual witness and the remaining rooted BCI theorem

If a complete pattern violates `(MBR)`, Hölder implies that at least one band
satisfies

\[
 \|P_kf\|_j>
 \exp(\varepsilon_NN)\frac{M}{L^{1-1/j}}.
\tag{29}
\]

By \(\ell^j\)-duality there is a real \(u\) with
\(\|u\|_{j'}=1\), \(j'=j/(j-1)\), such that self-adjointness of \(P_k\)
gives the exact mask-aware witness

\[
 \boxed{
 \sum_{x\in\Omega^\circ}(P_ku)(\Phi(x))
 >\exp(\varepsilon_NN)\frac{M}{L^{1-1/j}}.
 }
\tag{30}
\]

The letter \(u\) is used for the dual test to avoid collision with the column
map often denoted \(g(t)\).  Equation (30) is proved, but the remaining source
theorem must be rooted in the actual first-match consumer.

```text
Rooted band-to-cell inverse theorem (BCI).

Input:
  the received line and realized profile (r, lambda);
  the ordered atlas cut and the actual residual Omega^circ_(r,lambda)
    produced by whole-slope first-match deletion;
  Phi on the translated effective difference span, its effective group G_eff,
    H=|G_eff|, and L=|Phi(Omega^0)| for the realized full-slice image;
  the support-to-witness/slope incidence and owner map;
  a complete symmetric nonzero tau-band A_k, order j, and normalized real
    dual test u satisfying (30).

Output:
  a specified positive-weight surviving witness and distinct slope from that
    same residual incidence;
  a canonical valid certificate in a closed earlier cell, including its exact
    cell parameters and owner;
  the printed distinct-slope projection payment consumed by that cell.
```

The rootedness is load-bearing.  An unrooted named certificate may belong to a
slope already removed by first match and gives no contradiction with semantic
saturation.  Only the rooted emission theorem lets semantic saturation exclude
the output and prove `(BR)`, hence `(MBR)`.  Neither the \(\tau\)-moments, low
additive energy, the CHG normalization, nor a list of cell names proves rooted
`(BCI)`.  The phrase "source-derived semantically saturated residual" remains
shorthand until these inputs and ownership conditions are printed.

PR #668 proves a canonical-transversal VC-compression image theorem for
arbitrary subset-sum maps, but explicitly leaves post-atlas block/fiber typing,
effective-image charge, and full A4 open.  It does not supply rooted `(BCI)` for the
exact residual mask.

### 6.7 Correct status

The replacement is now partly proved:

```text
L rho D_k <= exp(o(N))
  => that complete pattern is paid absolutely: PROVED.

top-order q-BR on every remaining bulk band
  => every lower zero-character sector is paid at exp(o(Nq)): PROVED.

dense low-|tau| q-BR, or rooted BCI for every dual violation witness
  => full source-specific MBR: OPEN.
```

The preferred unresolved target is the dense-band rooted `(BCI)` theorem or a direct
top-order `(q-BR)` estimate.  A separate all-orders restriction induction is
not required.

### 6.8 Theorem dependency table

| Item | Required hypotheses | Status here | Consumer |
|---|---|---|---|
| Zero-character peeling and complete-pattern identity | finite Fourier orthogonality | PROVED | all moment orders |
| Tuple-tail certificates | printed \(\tau\)-moments | PROVED | exceptional score census |
| Universal band-density restriction | \(f\ge0\), exact band density | PROVED | sparse complete patterns |
| Moment-certified sparse payment | (20) and \(L\rho D\le\exp(o(N))\) | PROVED implication | part of bulk MBR |
| Top-order compiler | dense-band `(q-BR)` as input, accessibility | PROVED implication | every lower bulk sector |
| Dense low-\(|\tau|\) `(q-BR)` | source-derived semantic residual | OPEN | remaining bulk MBR |
| Rooted band-to-cell inverse `(BCI)` | dual witness (30), received line/profile, whole-slope residual, incidence, owner, paid output | OPEN alternative | remaining bulk MBR |
| Exceptional-pattern inverse/compiler | tail-certified exceptional patterns | OPEN | full signed compiler |
| A4 / primitive Q | complete bulk and exceptional payments | NOT CLAIMED | asymptotic envelope |

## 7. Experimental census

The accompanying script performs a complete finite Fourier census on ten
subgroup identity profiles and one deliberately planted arbitrary-weight
regression.  It computes exact fixed-weight coefficients, secant contributions,
fiber counts, threshold sweeps, character triples, sign ablations, and
conservative structural proxies.

It also checks the exact reductions independently on \(\mathbb Z/11\mathbb Z\):
orders `2` through `5` for (2), all `27` three-fold patterns in a nontrivial
three-band partition for (13), `121` point-mass zero-sum triples for (8), and a
finite one-coordinate tail instance.  The largest floating-point residuals are
`1.50e-7` for peeling, `3.56e-12` for the complete-pattern identity, and
`5.73e-14` for the diagonal identity.

The same finite block checks the new inequalities.  The largest observed ratio
to the universal band-density bound is `0.3634`, the largest sparse triple
ratio is `0.01064`, the top-order interpolation ratio is at most `1.0000`, the
repeated-pattern endpoint ratio is `0.7608`, and the dual-witness pairing error
is `4.45e-16`.  The script also checks the interpolation exponent identity
exactly in `65` rational cases with `3 <= q <= 12`.

The reviewer-requested localizations are also replayed: the order-two ratio
\(\|P_kf\|_2^2/(f_{\max}W)\) is `0.1135`, and the largest error in the
point-mass identity \(P_kf(s_0)=r|A_k|/H\) is `6.65e-16`.

### 7.1 Paid-versus-dense pattern census

For each toy the verifier partitions every nonzero character into `A_<1` or a
dyadic band, enumerates every nonempty ordered three-band pattern by exact
group convolution, and records both the exact value and the moment-certified
upper bound for \(L\rho D_{\mathbf k}\).  The finite budgets `1`, `N`, and
`N^2` are review diagnostics for \(\exp(o(N))\); they are not asymptotic
theorem labels.

The `N^2` diagnostic gives:

| source-like profile | nonempty patterns | exact-density paid fraction | moment-certified paid fraction | certified dense diagnostic residue |
|---|---:|---:|---:|---:|
| `sg17_n8_w2_m4` | 64 | 1.000 | 0.578 | 27 |
| `sg13_n12_w2_m6` | 21 | 1.000 | 0.333 | 14 |
| `sg17_n16_w2_m8` | 21 | 1.000 | 0.000 | 21 |
| `sg19_n18_w2_m9` | 21 | 1.000 | 0.000 | 21 |
| `sg41_n8_w2_m4` | 64 | 1.000 | 0.578 | 27 |
| `sg17_n8_w3_m4` | 64 | 1.000 | 0.578 | 27 |
| `sg17_n16_w3_m8` | 121 | 0.149 | 0.000 | 121 |
| `sg73_n24_w2_m12` | 125 | 0.360 | 0.000 | 125 |
| `sg97_n16_w2_m8` | 122 | 0.164 | 0.000 | 122 |
| `sg193_n24_w2_m12` | 125 | 0.000 | 0.000 | 125 |

The theorem therefore removes a visible sparse range, while the printed moment
certificates alone leave every pattern in several harder toys in the dense
diagnostic residue.  This is evidence for the revised proof architecture:
Theorem 6.1 should be applied first, and dense-band `(q-BR)`/rooted `(BCI)` should be
asked only for the surviving patterns.  It is not evidence that the finite
`N^2` cutoff is the correct asymptotic boundary.

The principal observations are:

| observation | finite result |
|---|---|
| 90th-percentile individual \(|\tau|\) cutoff | captures between `0.000` and `0.974` of positive mass on source-like toys |
| matched-density tuple-product score | beats any-large-coordinate selection in all 3 complete triple censuses |
| fixed geometric cutoff \(1.5\sqrt N\) | captures positive shares `0.223`, `0.000`, and `0.000` in those triple censuses |
| source-like rank-3 sign ablation | absolute/signed ratio `116.1` |
| planted sign ablation | absolute/signed ratio `706.4` |
| conservative proxy coverage | covers as little as `0.000` of positive exceptional mass in one source-like profile |

At \(1.5\sqrt N\), the signed bulk divided by the toy \(N^2\mu\) scale ranges
from `-0.1573` to `0.6761`; in the larger rank-two toys it is `-0.0003159` for
`sg73_n24_w2_m12` and `0.001082` for `sg193_n24_w2_m12`.

These experiments support three design choices but prove none of them
asymptotically:

1. tuple-product patterns are more faithful than a union bound over large
   individual characters;
2. signs must be retained; and
3. simple frequency proxies cannot be treated as semantic atlas certificates.

The external CHG regression from PR #662 is also recorded: one finite witness
has termwise absolute mass `374`, signed magnitude `31.3093`, and toy target
`125`.  This is another guardrail against replacing `(MBR)` by absolute
summation.

## 8. Remaining compiler

Within the signed-bulk half, Theorem 6.1 pays every pattern satisfying the
sparse band-density criterion and Theorem 6.2 reduces all remaining orders to
one dense top-order `(q-BR)` estimate.  The exact dual target for that estimate
is rooted `(BCI)` in Section 6.6.

After the bulk is paid, the exceptional side still requires two logically
separate lemmas:

1. **exceptional-pattern inverse structure:** excessive positive mass on the
   tail-certified exceptional patterns produces a canonical algebraic object;
2. **frequency-to-support witness:** that object yields a validated quotient,
   field-descent, planted, rank, saturation, or other named owner-level
   certificate with a printed payment.

Semantic first-match saturation can exclude the second conclusion only after
the certificate-existence theorem is proved.  The absence of a certificate in
a record is not an analytic inequality.

Thus the corrected program is

```text
complete finite bands
  + exact zero-character peeling
  + proved sparse-pattern payment
  + dense-band q-BR or rooted BCI
  + exceptional-pattern inverse structure
  + semantic frequency-to-witness compiler
  => signed exceptional-spectrum compiler
  => pre-A4 Sidon payment / primitive Q.
```

In this packet the complete finite band grammar, exact zero-character peeling,
sparse-pattern payment, top-order reduction, endpoint guardrails, and dual
witness are proved.  Dense-band `(q-BR)`/rooted `(BCI)` and both exceptional-side
lemmas remain open.

## 9. Reproduction

From the repository root:

```sh
python3 experimental/scripts/experiment_mask_aware_band_restriction_v1.py --check
python3 experimental/scripts/experiment_mask_aware_band_restriction_v1.py --tamper-selftest
```

Use `--write --check` to regenerate the JSON certificate.  The script requires
NumPy.  The finite census is experimental evidence and a regression suite; it
does not prove dense-band `(q-BR)`/rooted `(BCI)`, source-atlas exhaustivity, `(A4)`,
primitive Q, or the Proximity Prize theorem.

## References

- `experimental/asymptotic_rs_mca_frontiers.tex` for the primitive/A4 ledger
  boundary and image-normalized moment interface.
- `experimental/notes/roadmaps/b2_l1_reduction_ledger.md` for the signed
  conductor large-sieve and secant-variance routes.
- PR #662 for the full-rank CHG/Hankel--Salié normalization and sign-sensitive
  finite regressions.
- PR #674 for the PRE/Q/Sidon audit boundary and planted-pair regression.
- PR #668 for the canonical-transversal VC-compression image theorem and its
  explicit post-atlas/A4 nonclaims.
