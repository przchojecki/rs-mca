# Lean Formalization Starter

This directory starts a small Lean 4 formalization for the rs-mca project.
It is deliberately stdlib-only: no `mathlib` dependency is required.

The first module, `RsMca.Basic`, formalizes:

- proof-status labels used by the agent ledger;
- words over a finite domain and agreement on a support;
- support-wise line-MCA bad-support predicates, parameterized by an abstract
  line-combination operation;
- quotient-locator parameter arithmetic, including the identity
  `supportSize = a * ell` when `k = a * rank` and `ell = rank + 1`;
- a minimal script-certificate record matching the `agents.md` output standard.

The second module, `RsMca.DeepPoint`, formalizes the quantitative cores of the
X1/L2 forward interleaved deep-point bridge
(`notes/x1/x1_deep_point_interleaved_bridge.md`):

- the deep-image membership predicate (§1-§2);
- the `K_{m,m}` clique-amplification cap arithmetic (§2.6 C):
  `cliqueGridSize m a k = k + m^2 (a-k)`, with `cliqueSupport_over_a` proving the
  support exceeds `a` for `m >= 2`, `a > k` (two-sided over-agreement), and
  `cliqueGridSize_mono`;
- the conditional-budget exponent arithmetic (§2.6 R, §2.8):
  `listExponent_areg_le_worst` (a-regular exponent `1 <= mu`) and
  `budgetClears_mono` (an L1 bound clearing the budget at `mu` clears it
  a-regularly).

All `RsMca.DeepPoint` theorems are proved (no `sorry`); the finite-field/
combinatorial proofs of the identity and the a-regular collapse remain stated
elsewhere as targets.

## Build

```sh
cd experimental/lean/rs_mca_formalization
lake build
```

This is not a formal proof of the main rs-mca theorems. It is a typed starting
point for later agents to connect finite script certificates and locator
identities to theorem statements.
