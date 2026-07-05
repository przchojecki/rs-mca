# Lean package for `towards-prize.tex`

This folder contains a Mathlib-based Lean formalization track for selected
definitions and theorem statements from `tex/towards-prize.tex`, the compact
prize-facing threshold note.

The Lean entry point is:

```text
experimental/lean/towards_prize/TowardsPrize.lean
```

The package is normalized as:

```text
package: towards_prize
library: TowardsPrize
namespace: TowardsPrize
toolchain: leanprover/lean4:v4.28.0
dependency: mathlib v4.28.0
```

Build command, in an environment where Mathlib dependencies are available:

```sh
cd experimental/lean/towards_prize
lake build
```

Codex did not run `lake build` during integration.  The source was inspected for
obvious trust placeholders; no `sorry`, `admit`, or added `axiom` occurs in
`TowardsPrize.lean`.

## Scope

The package formalizes the integer-radius MCA/CA definitions and selected
results from the note, including:

- Hamming weight and distance for words over a finite evaluation type;
- linear codes as `Submodule F (ι -> F)`;
- `closeBy`, `colFar`, `CAbad`, `MCAbad`, `epsCA`, `epsMCA`, and `sigmaC`;
- the comparison theorem `epsCA_le_epsMCA`;
- the small-field threshold theorem `dstar_eq_zero_of_small`;
- deep-regime and half-distance safe-side statements;
- the sparse-layer theorem `sparsify`;
- the identity-prefix floor `prefix_floor`;
- the deep-point conversion `deep_point_conversion`.
- finite certificate anchors under `TowardsPrize.FiniteAnchors`, mapped in
  `CERTIFICATION_MAP.md`.

This is not a complete formalization of Paper D v12 or of every numerical
certificate in `towards-prize.tex`.  In particular, the cap criterion and the
binomial-entropy checks behind the deployed Theorem 1.1 rows remain outside this
Lean package unless separately added and mapped.

## Review Status

Status: `FORMALIZATION / AUDIT`.

Before promoting any claim as Lean-certified, run the package in a controlled
Mathlib-enabled Lean 4.28 environment and add a theorem-by-theorem map.  Claims
that depend on Python certificate replay, external imports, or Paper D should
remain labelled as verifier-backed or conditional unless their Lean theorem
name is explicitly listed.

## Finite Anchor Map

`CERTIFICATION_MAP.md` lists the new finite arithmetic anchors for selected
`sigma_C`, `eca_C`/`emca_C`, and identity-prefix rows. These are Lean-checked
arithmetic records, not replacements for the Python verifier-backed census
claims.
