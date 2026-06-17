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

## Build

```sh
cd experimental/lean_formalization
lake build
```

This is not a formal proof of the main rs-mca theorems. It is a typed starting
point for later agents to connect finite script certificates and locator
identities to theorem statements.
