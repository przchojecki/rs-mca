# Owner-Rooted Positive-Support Localization and Rank Guardrail

```text
Status: ZERO-LOSS ROOTED LOCALIZATION + TRADE BRANCH PROVED
Guardrail: the literal per-witness rank precursor is automatic
Nonclaim: no baseline-free collective rank cell or `(CAT)` payment
```

## Status

There are two different mathematical statements hidden in the proposed target.

1. **Literal high-load precursor extraction, with the actual complete-band restriction failure retained as part of the
   owner-rooted proof object, is proved below with zero loss.**  It always emits the
   permitted rank precursor.
2. **That rank precursor is witness-tautological.**  It is present for every
   decoding witness, independently of high load, and therefore cannot supply
   the intended semantic classification or payment. After excluding
   this baseline rank loss, the current hypotheses prove exact rooted
   localization and a quantitative planted-trade branch, but do not exhaust
   the remaining flat branch.

The distinction is essential.  The first item proves the theorem exactly as
its rank alternative is presently worded.  The second identifies the repair
needed for a useful theorem.

For integration, the automatic block-diagonal rank construction is recorded
only as a specification regression.  It must not be consumed as a semantic
rank cell: the generic comparison for a useful rank precursor must already
impose every individual witness interpolation equation.

## 1. The input must retain the actual complete-band restriction failure

Write

\[
 \mathcal R_A=\frac{L^{1-1/q}}M\|P_Af\|_q,
 \qquad
 \mathcal Y_A=e_Ax_A^{q-2}.
\]

the finite owner-rooting and projected-energy reductions prove only

\[
 \mathcal R_A^q\le \mathcal Y_A.
\]

Thus an actual failure \(\mathcal R_A\ge e^{\eta N}\) implies
\(\mathcal Y_A\ge e^{\eta Nq}\), but high \(\mathcal Y_A\) does not imply
high \(\mathcal R_A\).  Therefore the phrase “retains exponential normalized
excess” is theorem-grade only if the owner-rooted object continues to carry

\[
 \boxed{\mathcal R_A\ge e^{\eta N}.}
 \tag{1.1}
\]

The high-load inequality is a derived tag, not a replacement for (1.1).

## 2. Exact positive-support localization

Let \(g\) be the exact norming dual, \(\|g\|_{q'}=1\), and define

\[
 \omega(S)=\left[\operatorname{Re}
 \overline{(P_Ag)(\Phi(S))}\right]_+,
 \qquad
 \mathcal S_+=\{S\in\Omega^\circ:\omega(S)>0\}.
\]

Put

\[
 b(s)=|\mathcal S_+\cap\Phi^{-1}(s)|,
 \qquad
 \Omega_+=\sum_{S\in\mathcal S_+}\omega(S),
 \qquad
 n_+=|\mathcal S_+|.
\]

### Lemma 2.1 (zero-loss rooted localization)

One has

\[
 \boxed{
 \|P_Ab\|_q\ge \Omega_+\ge\|P_Af\|_q,
 \qquad
 \|P_Ab\|_2^2\ge\Omega_+^2,
 \qquad
 n_+\ge\Omega_+.
 }
 \tag{2.1}
\]

Consequently, under (1.1),

\[
 \boxed{
 \frac{L^{1-1/q}}M\|P_Ab\|_q
 \ge \mathcal R_A
 \ge e^{\eta N},
 }
 \tag{2.2}
\]

and, defining the packet load with \(b\) in place of \(f\),

\[
 \boxed{
 \mathcal Y_A(b)\ge \mathcal R_A(b)^q\ge e^{\eta Nq}.
 }
 \tag{2.3}
\]

Moreover

\[
 \boxed{
 n_+\ge e^{\eta N}\frac{M}{L^{1-1/q}}
       =e^{\eta N}\frac ML L^{1/q}
       \ge e^{\eta N}.
 }
 \tag{2.4}
\]

Every support in \(\mathcal S_+\) retains its actual unique surviving owner.

#### Proof

Positive truncation gives \(\Omega_+\ge\|P_Af\|_q\).  Since \(b\) counts
exactly the supports on which the pulled-back real dual summand is positive,

\[
 \Omega_+
 =\operatorname{Re}\langle b,P_Ag\rangle
 =\operatorname{Re}\langle P_Ab,g\rangle.
\]

Hölder and \(\|g\|_{q'}=1\) imply

\[
 \Omega_+\le\|P_Ab\|_q.
\]

Because \(q'\le2\), counting-norm monotonicity also gives
\(\|g\|_2\le1\), hence

\[
 \Omega_+\le\|P_Ab\|_2\le\|b\|_2\le\|b\|_1=n_+.
\]

This proves (2.1).  Equation (2.2) follows by normalization.  Applying the already-proved interpolation gate to the residual count \(b\) gives (2.3).  Since
\(L\le M\), (2.4) follows from \(n_+\ge\|P_Af\|_q\).  Rooting follows from
\(\mathcal S_+\subseteq\Omega^\circ\).  \(\square\)

## 3. Literal rooted high-load precursor extraction theorem

Assume the finite owner-rooting and projected-energy object includes the received line

\[
 U_z=u+zv
\]

over the evaluation field \(\mathbb F\), and that each retained support
\(S\) has its actual witness polynomial \(h_S\), with

\[
 U_{o(S)}|_S=h_S|_S,
 \qquad \deg h_S<k,
 \qquad a\ge k+1.
\]

### Theorem 3.1 (literal rooted high-load structure extraction)

Under (1.1), the proposed rooted high-load precursor extraction conclusion holds with no support, character,
owner, dual-mass, or projected-energy loss.  Take

\[
 A'=A,
 \qquad
 \mathcal S'=\mathcal S_+,
 \qquad
 \mathcal Z'=o(\mathcal S_+),
 \qquad
 \omega'=\omega|_{\mathcal S_+}.
 \tag{3.1}
\]

For each \(S\in\mathcal S_+\), define the explicit augmented evaluation
matrix

\[
 B_S=\left(
 \begin{array}{ccccc}
 1&t&\cdots&t^{k-1}&U_{o(S)}(t)
 \end{array}
 \right)_{t\in S}
 \in\mathbb F^{a\times(k+1)}.
 \tag{3.2}
\]

Then

\[
 \boxed{
 \operatorname{rank}_{\mathbb F}B_S=k,
 \qquad
 \operatorname{rank}_{\rm generic}B_S=k+1.
 }
 \tag{3.3}
\]

Let

\[
 B=\bigoplus_{S\in\mathcal S_+}B_S.
 \tag{3.4}
\]

It satisfies

\[
 \boxed{
 \operatorname{rank}_{\mathbb F}B=kn_+,
 \qquad
 \operatorname{rank}_{\rm generic}B=(k+1)n_+,
 \qquad
 r=n_+\ge e^{\eta N}.
 }
 \tag{3.5}
\]

Thus

\[
 \mathcal D_{\rm rank}
 =\bigl(\mathbb F,D,k,
       \{(S,o(S),h_S,B_S):S\in\mathcal S_+\},B,r\bigr)
 \tag{3.6}
\]

is a printed, verifier-checkable rank precursor rooted at every positive-weight
owner.  The packet retains the full normalized excess by (2.2).

#### Proof

The first \(k\) columns of \(B_S\) form a Vandermonde evaluation matrix on
\(k\) or more distinct points, so they have rank \(k\).  Write

\[
 h_S(X)=\sum_{j=0}^{k-1}c_{S,j}X^j.
\]

On every row \(t\in S\), the witness equation gives

\[
 U_{o(S)}(t)=h_S(t)=\sum_{j=0}^{k-1}c_{S,j}t^j.
\]

Hence the last column is in the span of the first \(k\), proving
\(\operatorname{rank}B_S=k\).  Since \(a\ge k+1\), a generic free last
column is outside that \(k\)-dimensional span, so the generic rank is
\(k+1\).  Rank and generic rank add under block direct sum, yielding (3.5).
All rooting and excess assertions follow from Lemma 2.1.  \(\square\)

### Verification interface

For every block the verifier prints:

* the field modulus or field representation;
* the ordered support coordinates;
* the owner slope;
* the coefficients of \(h_S\);
* the matrix \(B_S\);
* one nonzero \(k\times k\) Vandermonde minor;
* vanishing of every \((k+1)\times(k+1)\) minor, or modular row-reduction rank;
* the direct-sum deficiency \(r=n_+\).

This is exact finite-field arithmetic.  There is no asymptotic or numerical
step.

## 4. Why Theorem 3.1 is not the intended owner-rooted localization

The rank loss in (3.3) is the defining interpolation identity of a decoding
witness.  It exists for one witness, before any Fourier or high-load argument.
The direct sum in (3.4) merely adds one automatic deficiency per witness.
Therefore Theorem 3.1 proves the literal wording but extracts no new shared
source structure.

In particular, it does not identify:

* a common deficient minor across many supports;
* a differential-locator or tangent rank loss beyond the witness incidence;
* a common secant, Hankel, or moment matrix with an unexpected corank;
* a slope-projection bound or paid rank cell.

A useful rank alternative must compare against the generic rank **inside the
ordinary witness incidence**, not against an ambient matrix in which the
received-word column is free.

One precise repair is:

> **Baseline-free collective rank precursor.**  Print a canonical matrix
> \(C(\mathcal S',\mathcal Z')\), not a direct sum of one-witness augmented
> interpolation matrices, and a number \(r>0\) such that
> \[
>  \operatorname{rank}C
>  \le
>  \operatorname{rank}_{\rm generic\ on\ the\ witness\ locus}C-r.
> \]
> The same rows, columns, and generic witness-locus rank must be defined
> uniformly over the profile, and the deficient packet must carry the printed
> rooted mass or projected energy required for the semantic atlas conversion.

Equivalently, the target may expressly forbid a deficiency implied separately
by each relation \(U_{o(S)}|_S\in\mathbb F[X]_{<k}|_S\).

## 5. Strongest non-tautological extraction currently proved

Lemma 2.1 also gives an exact physical packet:

\[
 \|P_Ab\|_2^2
 =\sum_{S,S'\in\mathcal S_+}
 K_A(\Phi(S)-\Phi(S'))
 \ge\Omega_+^2.
 \tag{5.1}
\]

Every pair is rooted at its actual owners.  Moreover

\[
 \sum_s b(s)^2\ge\|P_Ab\|_2^2\ge\Omega_+^2.
 \tag{5.2}
\]

After removing the \(n_+\) diagonal pairs, at least

\[
 \boxed{\Omega_+^2-n_+}
 \tag{5.3}
\]

ordered pairs of distinct positive supports have equal syndrome.  Each such
pair gives the exact trade

\[
 \boxed{
 \sum_{t\in S\setminus S'}v_t
 =
 \sum_{t\in S'\setminus S}v_t.
 }
 \tag{5.4}
\]

Hence:

### Corollary 5.1 (rooted planted-trade branch)

If

\[
 \boxed{\Omega_+^2\ge2n_+,}
 \tag{5.5}
\]

then at least \(\Omega_+^2/2\) ordered nontrivial rooted trade incidences are
emitted.  A sufficient condition in the original parameters is

\[
 \boxed{
 \mathcal R_A^2
 \ge
 \frac{2L^{2-2/q}}{M(N-a+1)}.
 }
 \tag{5.6}
\]

This branch detects the mandatory paired planted regression.

The remaining non-tautological branch is

\[
 \boxed{\Omega_+^2<2n_+.}
 \tag{5.7}
\]

It is an exponentially large, comparatively flat, positive-dual support
packet with exact owners, rim packing, received-line equations, a rooted
frequency packet, and rooted positive-kernel pair energy.  No theorem in
the finite owner-rooting and projected-energy reductions converts (5.7) into a quotient, bounded-template trade, field
 descent, baseline-free collective rank loss, or saturation witness.

## 6. Correct nontrivial owner-rooted target

After banking Lemma 2.1 and Corollary 5.1, the exact new theorem is:

> **Flat rooted source inverse (flat rooted source inverse).**  Suppose an actual source-derived
> packet satisfies
> \[
>  \mathcal R_A\ge e^{\eta N},\qquad
>  |S\cap S'|\le a-2,\qquad
>  \Omega_+^2<2|\mathcal S_+|,
> \]
> together with the complete received-line and owner records.  Then it emits,
> with printed thresholds and subexponential loss, a quotient precursor,
> bounded-template planted precursor, proper-field precursor, baseline-free
> collective rank precursor, or saturation precursor rooted at one of the
> same positive-weight owners.

This is materially sharper than starting from \(\mathcal Y_A\): the packet is
already restricted to positive norming-dual supports, has zero-loss \(q\)-BR
excess, has exponential cardinality, and carries exact pair and owner data.

## 7. PR-safe conclusion

The theorem can be promoted in one of two ways:

1. **Literal promotion.**  State Theorem 3.1 and explicitly label its rank
   precursor “witness-baseline”; do not claim it enables the semantic atlas conversion or complete-band restriction bound.
2. **Intended promotion.**  Amend rooted high-load precursor extraction by retaining \(\mathcal R_A\), defining
   numerical thresholds for every precursor, and replacing “rank precursor”
   with the baseline-free collective definition above.  Then bank Lemma 2.1,
   the physical packet, owner localization, and Corollary 5.1 as proved, while
   leaving flat rooted source inverse as the next theorem.

The exact logical boundary is

\[
 \boxed{
 \text{actual dense-band excess}
 \Longrightarrow
 \text{zero-loss rooted positive-support packet}
 \Longrightarrow
 \begin{cases}
  \text{rooted planted trades},&\Omega_+^2\ge2n_+,\\
  \text{flat rooted source packet},&\Omega_+^2<2n_+.
 \end{cases}
 }
\]

The literal rank alternative closes the displayed rooted high-load precursor extraction syntax, but only flat rooted source inverse
would close its intended semantics.
