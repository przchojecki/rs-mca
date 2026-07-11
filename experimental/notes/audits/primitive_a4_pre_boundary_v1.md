# Primitive A4/PRE boundary audit v1

```text
Status: AUDIT / PROVED LOGICAL EQUIVALENCE / COUNTEREXAMPLE GUARDRAIL
Theorem status: no new primitive-Q or Sidon payment is proved
```

## Purpose

The asymptotic frontiers manuscript uses two different objects that should not
be conflated:

1. a **ledger-admissible** profile, which satisfies condition `(A4)` by
   definition; and
2. an **unpaid primitive residual**, obtained after the named algebraic cells
   are removed but before any Fourier/Sidon payment is proved.

For the first object, the manuscript already proves `(A4) => primitive Q` in
`thm:primitive-q` and the conditional profile-envelope compiler. This note
audits that implication in elementary max-moment form. It does not promote it
to an unconditional theorem.

For the second object, this note gives an exact planted-pair regression. It
shows that fixed density, image normalization, genuine weighted Vandermonde
columns, and exponentially small normalized additive energy do not imply Q by
themselves. The example is deliberately planted. Any theorem whose admissible
class includes this weighted-Vandermonde family must either exclude it through
a source-derivation hypothesis or route it through a semantic planted
certificate. The current source-derived atlas need not contain arbitrary
weight families.

Finally, the note records the coding-language form of the unpaid theorem,
called **primitive fixed-composition rectangle evasiveness** (`PRE`). PRE is a
restatement of primitive Q for the same residual and image normalization, not
a new downstream lemma.

## 1. Exact max-moment sandwich

Fix one primitive profile and write

\[
 F_s=\Omega^\circ\cap\Phi^{-1}(s),\qquad
 f_s=|F_s|,\qquad
 M=|\Omega^0|,\qquad
 L=|\Phi(\Omega^0)|,\qquad
 \bar N=M/L.
\]

For targets in the realized full-slice image, put

\[
 R_s=f_s/\bar N,\qquad
 R_*=\max_s R_s,\qquad
 \Gamma_q=L^{-1}\sum_s R_s^q.
\]

Since \(\Omega^\circ\subseteq\Omega^0\),

\[
 L^{-1}\sum_sR_s=|\Omega^\circ|/M\le1.
\tag{1}
\]

Therefore, for every \(q\ge1\),

\[
 \boxed{L^{-1}R_*^q\le\Gamma_q\le R_*^{q-1}.}
\tag{2}
\]

The upper inequality follows from \(R_s^q\le R_*^{q-1}R_s\); the lower
inequality retains the largest summand. Consequently, if

\[
 q_N\to\infty,\qquad \log L_N/q_N=o(N),
\tag{3}
\]

then

\[
 R_*\le e^{o(N)}
 \quad\Longleftrightarrow\quad
 \Gamma_{q_N}\le e^{o(Nq_N)}.
\tag{4}
\]

Condition (3) is essential for the reverse implication. This is the
moment-accessibility condition printed in `(A3)` and `thm:primitive-q`.

## 2. Sidon payment and Boolean high energy

For a nonempty fiber define

\[
 \Delta_s=E(F_s)/f_s^3.
\]

For fixed \(\sigma>0\), its Sidon-heavy normalized submoment is

\[
 \Gamma^{\rm sid}_{q,\sigma}
 =L^{-1}\sum_{\Delta_s\le e^{-\sigma N}}R_s^q.
\tag{5}
\]

Assume uniformly that

\[
 \Gamma^{\rm sid}_{q_N,\sigma}\le e^{o(Nq_N)}
 \quad\hbox{for every fixed }\sigma>0,
\tag{SPay}
\]

and use the manuscript's proved Boolean high-energy theorem:

\[
 E(F)\ge |F|^3/K\quad\Longrightarrow\quad |F|\le K^C
\tag{6}
\]

for an absolute constant \(C\). The latter follows from quantitative BSG and
the Boolean quasicube inequality \(|U-U|\ge|U|^{3/2}\).

### Proposition 2.1

Under (3), `(SPay)`, and (6), primitive Q holds uniformly:

\[
 \max_s f_s\le e^{o(N)}\bar N.
\tag{7}
\]

### Proof

If uniform Q failed, a worst-profile subsequence would contain a fixed
\(\eta>0\) and targets with \(R_s\ge e^{\eta N}\). By (2),

\[
 \Gamma_q\ge e^{\eta Nq-\log L}=e^{(\eta-o(1))Nq}.
\]

Fix \(\sigma>0\). After subtracting `(SPay)`, the high-energy submoment is at
least \(e^{\eta Nq/2}\) for large \(N\). Hence one high-energy fiber has
\(R_s\ge e^{\eta N/2}\). Since \(\bar N=M/L\ge1\), it also has
\(f_s\ge e^{\eta N/2}\), while (6) with \(K=e^{\sigma N}\) gives
\(f_s\le e^{C\sigma N}\). Choosing \(0<\sigma<\eta/(4C)\) is a
contradiction. \(\square\)

Primitive Q implies `(SPay)` directly from the upper half of (2). Thus, with
the printed accessibility and Boolean high-energy hypotheses,

\[
 \boxed{\text{primitive Q}\iff\text{ordinary logarithmic-moment Q}
 \iff\text{Sidon-heavy payment}.}
\tag{8}
\]

This equivalence is already the logic of `thm:primitive-q`; the contribution
here is an explicit audit boundary, not a new payment.

## 3. What ledger-admissibility assumes

Condition `(A4)` in `def:admissible-sequence` requires every primitive leaf to
carry either:

- the certified effective `(MI)` and `(MA)` payments; or
- a separately proved image-normalized Sidon/Fourier moment payment of the
  strength in `def:sidon-paid-cell`.

Therefore the literal statement

```text
ledger-admissible profile => primitive Q
```

is proved by the manuscript. It is conditional because ledger-admissibility
contains the analytic payment. It cannot be read backwards as

```text
named algebraic cells removed => A4
```

without a separate theorem. The manuscript explicitly says that primitivity
does not assume Fourier, Sidon, max-fiber, or ray estimates.

## 4. Planted-pair low-energy regression

Let \(B\) be even and set \(N=2B\), \(m=B\). Partition the coordinates into
pairs \((i,+),(i,-)\), \(1\le i\le B\). Let

\[
 a_i=Q^i\quad(Q\ge5),\qquad
 C>4\sum_{i=1}^B a_i,
\]

and choose a prime \(p\) larger than twice every integer subset sum occurring
below, so reduction modulo \(p\) is injective. Define distinct nonzero weights

\[
 \rho_{i,+}=a_i,\qquad \rho_{i,-}=C-a_i.
\]

Choose arbitrary distinct evaluation points \(t_{i,\pm}\in\mathbb F_p\).
For \(R=1\), the columns \(\rho_{i,\pm}(1)\) are genuine weighted
Vandermonde columns. The boundary map is

\[
 \Phi(x)=\sum_i\bigl(a_ix_{i,+}+(C-a_i)x_{i,-}\bigr).
\tag{9}
\]

Put

\[
 r(x)=\sum_ix_{i,-},\qquad
 \delta_i(x)=x_{i,+}-x_{i,-}\in\{-1,0,1\}.
\]

Then

\[
 \Phi(x)=Cr(x)+\sum_i\delta_i(x)a_i.
\tag{10}
\]

The image value determines \((r,\delta)\). Indeed, the choice of \(C\)
first forces equality of \(r\), and base-\(Q\) uniqueness with digits in
\(\{-2,-1,0,1,2\}\) then forces equality of every \(\delta_i\).

Let \(s=|\{i:\delta_i\ne0\}|\). On the fixed-weight slice \(|x|=B\), a
vector \(\delta\) occurs exactly when \(s\equiv B\pmod2\), and its fiber has

\[
 f(\delta)=\binom{B-s}{(B-s)/2}
\tag{11}
\]

members. For even \(B\),

\[
 L=\frac{3^B+1}{2},\qquad
 M=\binom{2B}{B},\qquad
 f_{\max}=\binom B{B/2}.
\tag{12}
\]

Stirling's formula gives

\[
 \frac{f_{\max}}{M/L}
 =\exp\left(B\log\frac32+o(B)\right)
 =\exp\left(\frac{\log(3/2)}2N+o(N)\right).
\tag{13}
\]

Thus image-normalized Q fails at positive exponential rate.

### Exact energy

The heavy fiber \(\delta=0\) is an additive copy of the middle slice

\[
 \mathcal A=\binom{[B]}{B/2}.
\]

Writing \(B=2k\), its exact additive energy is

\[
 E(\mathcal A)=\binom{2k}{k}
 \sum_{r=0}^k\binom kr^2\binom{2(k-r)}{k-r}.
\tag{14}
\]

The exponential rate of the summand at \(r=xk\) is
\(2h(x)+2(1-x)\log2\), maximized at \(x=1/3\) with value \(2\log3\).
Consequently,

\[
 \log E(\mathcal A)=B\log6+o(B),
\]

and since \(\log|\mathcal A|=B\log2+o(B)\),

\[
 \boxed{
 \frac{E(\mathcal A)}{|\mathcal A|^3}
 =\exp\left(-B\log\frac43+o(B)\right)
 =\exp\left(-\frac{\log(4/3)}2N+o(N)\right).}
\tag{15}
\]

The fiber is therefore both exponentially heavy relative to its image average
and exponentially low-energy. Its explanation is the planted relation

\[
 \rho_{i,+}+\rho_{i,-}=C.
\]

The exact scope is:

| Hypothesis or guard | Status for the family |
|---|---|
| fixed density \(m/N=1/2\) | satisfied |
| full-image normalization | satisfied and counted exactly |
| genuine finite-field weighted Vandermonde columns | satisfied with \(R=1\), distinct points, and nonzero weights |
| exponentially low normalized energy | satisfied |
| source derivation from an intended smooth/circle row `(A1)` | not established |
| survival of a witness-exhaustive semantic atlas `(A2)` | not established |
| analytic payment `(A4)` | deliberately absent |
| deployed positive-depth ratio | not satisfied; \(R/N\to0\) |

Thus the example is not a valid counterexample to a source-derived semantic
atlas that excludes the row or routes its planted relation. It is a regression
against deriving `(A4)` from the four satisfied properties alone. In
particular, the absence of a planted label is not itself an inequality, but the
current atlas is not required to admit every arbitrary planted weight family.

## 5. Coding-language interface: PRE

Let \(H_\lambda\) be the \(R\times N\) weighted Vandermonde matrix with
columns

\[
 v_i=\rho_i(1,t_i,\ldots,t_i^{R-1})^{\mathsf T}.
\]

Every \(R\) columns are independent. Hence
\(C_\lambda=\ker H_\lambda\) is an \([N,N-R,R+1]\) MDS code, equivalently
a coordinate-scaled GRS code.

For \(x^0\in\{0,1\}_m^N\) with \(H_\lambda x^0=s\), the full Boolean fiber
is

\[
 (x^0+C_\lambda)\cap\{0,1\}_m^N.
\tag{16}
\]

After translation it consists of codewords \(c\in C_\lambda\) with

\[
 c_i\in\{-x_i^0,1-x_i^0\},\qquad \sum_i c_i=0.
\tag{17}
\]

Let \(\mathcal P_\lambda\) be the first-match union of already paid
witnesses. The unpaid profile statement can therefore be written as:

> **Primitive fixed-composition rectangle evasiveness (PRE).** Uniformly for
> every source-derived primitive profile and every realized coset,
> \[
> \left|(x^0+C_\lambda)\cap\{0,1\}_m^N
>       \setminus\mathcal P_\lambda\right|
> \le e^{o(N)}
> \frac{\binom Nm}{|\Phi_\lambda(\{0,1\}_m^N)|}.
> \tag{PRE}
> \]

For the exact same residual and normalization, PRE is primitive Q written in
coding language.

### Proposition 5.1 (qualified PRE/Q/Sidon equivalence)

Fix the same residual and full-image normalization throughout. Assume there is
an order \(q_N\to\infty\) with

\[
 \log L_N/q_N=o(N),
\]

and assume the Boolean high-energy implication (6). Then the following are
equivalent, uniformly over the profile sequence:

1. PRE;
2. primitive Q;
3. `(SPay)` at order \(q_N\) for every fixed \(\sigma>0\).

### Proof

PRE and primitive Q are the same inequality after rewriting a fiber as the
fixed-composition rectangle (16)--(17). Primitive Q implies `(SPay)` by the
upper max-moment inequality in (2), because the Sidon-heavy moment is a
submoment of \(\Gamma_q\). Conversely, `(SPay)` implies primitive Q by
Proposition 2.1, which uses precisely the displayed accessibility condition
and the Boolean high-energy implication. \(\square\)

Without those two printed hypotheses, this note claims only the definitional
equivalence `PRE <=> primitive Q`; it does not claim `PRE <=> (SPay)`.
PRE is not an additional compiler theorem and does not make the problem easier
by itself.

Random-RS capacity theorems do not directly supply PRE for every fixed smooth
evaluation subgroup: their random evaluation-set hypothesis is a different
input.

## 6. Relation to live routes

- **Moment-curve subgroup large sieve.** A sign-sensitive estimate retaining
  the fixed-weight coefficient would prove `(SPay)`. The integrated B2 ledger
  records this as an open crux.
- **One-sided secant variance `(SV*)`.** High moments control the exceptional
  spectrum, but the required coupling to the signs of the fixed-weight
  coefficient remains open.
- **Hankel--Salie aggregate.** The full-rank normalization bridge is exact;
  its signed aggregate estimate and lower-rank strata remain open.
- **Inverse Littlewood--Offord.** Quadratic-Bohr trapping is proved, while the
  exponential-scale Bohr-to-GAP or equivalent semantic-certificate step is
  still open.

All four are alternative formulations or sufficient routes to the same
unpaid rectangle-evasiveness/Sidon payment. None is closed by this audit.

## 7. Final status

```text
PROVED / ALREADY UPSTREAM:
  A4 + moment accessibility + Boolean high-energy theorem => primitive Q.

PROVED IN THIS AUDIT:
  exact max-moment sandwich;
  exact planted-pair image/fiber census;
  exact middle-slice energy formula and exponential rate;
  weighted-Vandermonde/MDS coding reformulation.

NOT PROVED:
  A4 from algebraic first-match removal;
  PRE for the source-derived primitive residual;
  any signed large-sieve, SV*, Hankel--Salie, or Bohr-to-GAP estimate;
  an unconditional asymptotic profile-envelope theorem.
```

The noncircular remaining target is still `(SPay)`, equivalently PRE/Q under
the printed accessibility and Boolean high-energy hypotheses.

## Sources

1. `experimental/asymptotic_rs_mca_frontiers.tex`, especially
   `def:admissible-sequence`, `prop:high-energy-impossible`, and
   `thm:primitive-q`.
2. `experimental/notes/roadmaps/b2_l1_reduction_ledger.md`.
3. PR #662, full-rank Hankel--Salie normalization bridge.
4. PRs #661 and #663, quadratic-Bohr trapping and Bohr-to-GAP route audit.
5. Brakensiek, Gopi, and Makam, *Random Reed--Solomon Codes Achieve
   List-Decoding Capacity With Linear-Sized Alphabets*, arXiv:2304.09445.
