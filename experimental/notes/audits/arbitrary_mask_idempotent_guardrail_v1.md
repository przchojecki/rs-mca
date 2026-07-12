# Dense-Idempotent Arbitrary-Mask Guardrail

```text
Status: ABSTRACT FOURIER/RIM COUNTEREXAMPLE PROVED
Source-semantic status: NOT A VALID `(CAT)`/PRIMITIVE-SIDON FALSIFIER
Use: regression against deriving signed payment from harmonic and rim data alone
```

## 1. Abstract theorem

For every fixed `$q>2$`, there are finite additive groups `$G_N$`, dense
symmetric character sets `$A_N\subseteq\widehat G_N\setminus\{0\}$`, full
fixed-weight slices of size `$M_N$`, rim-packed support families, arbitrary
subset-sum maps, and residual masks with

\[
 \max_s\frac{f_N(s)L_N}{M_N}=e^{o(N)}
\]

but

\[
 \boxed{
 \mathcal R_{A_N}(f_N)
 \ge
 \exp\!\left(\left(\frac12-\frac1q\right)N-o(N)\right).
 }
\]

Thus Fourier orthogonality, a dense symmetric multiplier, subset-sum form,
rim packing, and light fibers do not imply the owner-rooted signed estimate for an
arbitrary residual mask.

## 2. Dense idempotent multiplier

Let `$G=\mathbb F_p^R$`, `$L=|G|$`, and partition nonzero characters into
scalar orbits. Select half of those orbits by independent signs and let `$A$`
be their union. For `$x\ne0$`, Khintchine's inequality gives

\[
 \mathbb E\left|\sum_{\xi\in A}\chi_\xi(x)\right|\gg\sqrt L.
\]

Hence some symmetric orbit union satisfies

\[
 \Lambda(A):=\sum_x|K_A(x)|\gg\sqrt L,
 \qquad
 K_A(x)=\frac1L\sum_{\xi\in A}\chi_\xi(x).
\]

Put `$u(y)=\operatorname{sgn}K_A(-y)$` and `$r=(1+u)/2$`. Since zero is not
in `$A$`, `$P_A1=0$`, while

\[
 (P_Au)(0)=\Lambda(A).
\]

Therefore

\[
 \|P_Ar\|_q\ge\frac12\Lambda(A)\gg\sqrt L.
\]

The factor `$L^{1/2-1/q}$` is the exact obstruction when `$q>2$`.

## 3. Rim-packed subset-sum realization

Take `$t=4N$`, `$a=2N$`, and `$M={4N\choose2N}`. A greedy independent set in
the Johnson graph gives a family `$\mathcal C$` with

\[
 |\mathcal C|\ge\frac{M}{4N^2+1},
 \qquad
 |S\cap S'|\le a-2.
\]

For independent uniform columns `$v_j\in G$`, the map

\[
 \Phi(S)=\sum_{j\in S}v_j
\]

is pairwise universal on distinct supports. A second-moment argument gives a
choice with

\[
 \sum_x(F(x)-\mu)^2\le2|\mathcal C|,
 \qquad
 \mu=|\mathcal C|/L.
\]

In the regime `$\log L=N-o(N)$` and `$\log M=4(\log2)N-o(N)$`, the image is
all of `$G$`. Define the residual by the kernel-sign mask

\[
 \Omega^\circ=\{S\in\mathcal C:r(\Phi(S))=1\}.
\]

Writing `$f=\mu r+e$`, the discrepancy gives `$\|e\|_2\le\sqrt{2|\mathcal
C|}$`. Projection contraction and the idempotent lower bound yield

\[
 \mathcal R_A(f)
 \ge
 e^{(1/2-1/q)N-o(N)}.
\]

At the same time,

\[
 \max_x\frac{f(x)L}{M}
 \le O(N^{-2})+e^{-\Omega(N)}.
\]

The exact norming dual makes the full positive packet violate the proposed
signed-minor estimate by the same exponential factor.

## 4. Why this is not a source-semantic falsifier

The construction does not satisfy the current owner-rooted input contract.

1. **Column grammar.** The columns are independent uniform vectors. They are
   not proved to be genuine weighted-Vandermonde columns
   `$\rho(t)(1,t,\ldots,t^{R-1})$` on distinct source points.
2. **Band grammar.** `$A$` is a random union of scalar character orbits. A
   complete band in the current compiler is a full dyadic `$|\tau(\gamma)|$`
   band. The proof does not show that its `$A$` is one such band.
3. **Residual grammar.** The mask is chosen after seeing the Fourier kernel.
   It is not shown to be the output of the semantic first-match atlas.
4. **Received-line grammar.** Assigning a separate owner word to each support
   does not place those words on one affine received line `$U_z=u+zv$`.
5. **Profile derivation.** No validated row-to-profile certificate converts
   the random subset-sum state into an admissible smooth RS profile.

Consequently the construction proves

\[
 \boxed{
 \text{abstract harmonic + rim hypotheses}
 \not\Rightarrow
 \text{signed owner-rooted payment},
 }
\]

but it does not prove that source-derived, semantically saturated the primitive signed-payment boundary is
false.

## 5. Hereditary-mask boundary

Restricting to one actual source fiber preserves support records, owners,
explaining polynomials, and the original `$M/L$` normalization. It does not,
by itself, prove that the source-algebraic emission theorem accepts arbitrary record masks.

Thus the valid statement remains conditional:

\[
 \boxed{\text{hereditary mask-aware source-algebraic emission}\Longrightarrow\text{source-algebraic heavy-fiber inverse}.}
\]

Calling mask admissibility a lemma is a signature extension unless the atlas
proves closure under such masks.

## 6. Charge-routing boundary

The current packet already repairs the independent-charge defect. A valid
charge-preserving semantic-or-signed dichotomy decomposition must print nonnegative charges `$c_i$` satisfying

\[
 \sum_i c_i=\Omega_+,
 \qquad
 c_i\le\sum_{S\in\mathcal U_i}\omega(S),
 \qquad
 \|P_{B_i}b_{\mathcal U_i}\|_q\ge c_i.
\]

If charges are defined by signed pairings, their nonnegativity and exact sum
must be verified. A norm lower bound alone does not control the fixed-dual
pairing.

Retained q-excess gives only

\[
 \mathcal Y_{B_i}\ge\mathcal R_{B_i}^q
 \ge e^{\eta Nq-o(Nq)};
\]

it does not imply relative retention of the original `$\mathcal Y_A$`.

## 7. Correct use in the primitive signed-payment boundary

The abstract construction is a regression forcing any successful proof to use
source realizability. A valid theorem must show that a kernel-sign-like mask
cannot arise from the exact weighted-Vandermonde, one-line, semantic residual
grammar unless it emits a genuine source cell.

A suitable remaining target is a source transfer-radius inverse:

> For every source-derived no-semantic packet, either the normalized signed
> complete-band transfer operator has `$L^q$` gain `$1+o(1)$`, or the same
> charged owner data emit a genuine quotient, repeated planted template,
> proper-field descent, baseline-free collective rank loss, or saturation.

The threshold must be `$1+o(1)$`; a fixed one-step gain can tensorize to an
exponential loss.

## 8. Status

```text
Proved:
  abstract q>2 dense-idempotent arbitrary-mask obstruction;
  exact list of source guards it does not satisfy.

Still open:
  hereditary mask admissibility for the source theorem;
  source-rigidity exclusion of kernel-sign residuals;
  charge-preserving signed nonstructure payment.
```
