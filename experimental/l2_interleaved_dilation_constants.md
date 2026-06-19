# L2 Interleaved Lists: Dilation Symmetry and the Sharp-Constant Target

- **Status:** PROVED (dilation symmetry) / EXPERIMENTAL (constants scan) / AUDIT.
- **Agent/model:** Claude Opus 4.8.
- **Date:** 2026-06-19.
- **Scope:** L2 (sharp interleaved-list constants near capacity), `agents.md`;
  `tex/slackMCA_v3.tex` interleaved-list ledger and `tex/snarks_v4.tex` Paper C
  budget. Builds on `experimental/l2_interleaved_support_bridge.md` and
  `experimental/l1_l2_random_support_fiber_baseline.md`. This note does not edit
  Papers A--D and is list/locator side only; it does not touch the M1 work. It
  transfers the dilation-symmetry method developed for L1
  (`l1_prefix_divisor_count.md` §6, §9) to the interleaved setting.

## Goal

The bridge note reduces the interleaved (column-distance) list to the
common-intersection profile of full agreement supports, and shows the trivial
`mu`-th power exponent is not intrinsic. What is still missing (SUMMARY.md) is a
*worst-case sharp constant* for concrete arity `mu` and radius `1-a/n` near
capacity. This note adds the symmetry that cuts the worst case and frames the
target precisely, with a verifier.

## 1. Dilation symmetry of the interleaved list

`H = mu_n` acts on received words by dilation. For `h in H` and a `mu`-row word
`U = (U_1,...,U_mu)`, define the *diagonal* action
```text
(h . U)_i(x) = U_i(h^{-1} x),       i = 1,...,mu.
```

**Theorem (dilation invariance of the interleaved list).** For every `h in H`,
`a >= k`, and interleaved word `U`,
```text
|Lambda(Int(C,mu), 1 - a/n, h . U)| = |Lambda(Int(C,mu), 1 - a/n, U)|.
```
Hence the worst-case interleaved list
`Lst(Int(C,mu),1-a/n) = max_U |Lambda(...,U)|` is attained on a set of
dilation-orbit representatives of `(F_q^H)^mu`, cutting the worst-case search by
up to a factor `n`.

*Proof.* Per row, `P |-> P^h`, `P^h(x) = P(h^{-1}x)`, is a degree-preserving
bijection of `C` with agreement set `A_{P^h}(U_i^h) = h \cdot A_{P_i}(U_i)`
(`l1_prefix_divisor_count.md` §9). For an interleaved codeword
`c = (c_1,...,c_mu)`, the common agreement support of `c^h = (c_1^h,...,c_mu^h)`
with `h.U` is
```text
A_{c_1^h}(U_1^h) cap ... cap A_{c_mu^h}(U_mu^h)
   = h \cdot ( A_{c_1}(U_1) cap ... cap A_{c_mu}(U_mu) ),
```
which has the same size. So `c` is listed against `U` iff `c^h` is listed against
`h.U`, and `c |-> c^h` is a bijection of the two lists. ∎

This is the L2 analogue of the L1 dilation equivariance, and it composes with the
bridge note's quotient-core diagonalization: the dilation-*fixed* interleaved
words (those with `U_i = U_i(h^{-1}X)` for a nontrivial `K_d <= H`, i.e. periodic
rows) are exactly the structured packets whose interleaved count is diagonal, not
Cartesian.

## 2. The sharp-constant target

The random baseline (bridge note; `l1_l2_random_support_fiber_baseline.md`) is
```text
E |Lambda(Int(C,mu), 1 - a/n, U)|  <=  binom(n, a) q^{-mu (a-k)},
```
saving the factor `binom(n,a)^{mu-1}` against the product-of-row-lists baseline
`binom(n,a)^mu q^{-mu(a-k)}`. The **L2 sharp-constant conjecture** (target form):
for generated-field smooth domains, above the corrected reserve,
```text
Lst(Int(C,mu), 1 - a/n)  <=  binom(n,a) q^{-mu(a-k)} + Quot_mu + n^B,
```
where `Quot_mu` is the *aligned* quotient-core packet count
`L_mu(a,tau)` of the bridge note (diagonal, **not** raised to the `mu`-th power),
and the `n^B` is the aperiodic interleaved remainder. By §1 it suffices to bound
this on dilation-orbit representatives, and by the bridge formula it reduces to
the common-intersection profile of full agreement supports --- the same
quotient/aperiodic split as L1, now for `mu`-fold intersections.

## 3. Numerical confirmation (`F_17, n=16, mu=2`)

`verify_l2_interleaved_constants.py` builds full agreement-support families for
several row words and computes the exact 2-row interleaved list and simultaneous
fiber. At `k=6, a=8`:

| rows | interleaved | fiber | cartesian (`|Supp|^2`) | ratio |
|---|---:|---:|---:|---:|
| rand0 x rand1 | 33 | 73 | 1089 | **0.030** |
| periodic x rand | 33 | 73 | 33 | 1.0 |
| monomial x periodic | 54 | 54 | 54 | 1.0 |

It verifies: the bridge `interleaved <= fiber <= min_i |Fib_Ui(a)|`; the
sub-Cartesian bound `interleaved <= prod |Supp|` (ratio `0.03` for the generic
random pair --- the saving in action); repeated-row diagonalization
`Lambda(Int,(V,V)) = Lambda(C,V)`; and the §1 dilation symmetry (invariance of
the interleaved list under `h.U` for sampled `h`).

## Ledger impact

- **Interleaved list (improves):** the worst-case interleaved list is a
  dilation-orbit invariant, so a worst-case L2 certificate may restrict to orbit
  representatives.
- **Quotient (clarified):** the structured interleaved packets are the
  dilation-fixed (periodic) words, whose count is diagonal (bridge note), not
  Cartesian.

## Status / what to do next

- PROVED: dilation invariance of the interleaved list; worst-case reduction.
- TARGET: the sharp-constant conjecture above. Next: (a) bound the aperiodic
  `mu`-fold intersection remainder on orbit representatives (the L2 analogue of
  the L1 aperiodic step); (b) compute `Quot_mu` exactly at prize parameters and
  compare to the product baseline; (c) extend the scanner to `mu=3` and to the
  extension-coordinate presentation `|Lambda(C_F,delta)| = |Lambda(Int(C_B,e))|`.

## Reproducibility

```bash
python3 experimental/verify_l2_interleaved_constants.py
python3 experimental/verify_l2_interleaved_constants.py --a 9 --format json
```
