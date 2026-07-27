# KoalaBear v4 tangent-plus-deep owner Lean kernel

This stdlib-only package checks the finite first-match, frontloading, and
integer kernels used by the active tangent-plus-deep source adapter.

Replay:

```sh
lake clean
lake build
```

The pinned Lean v4.31.0 build completes in three jobs. The printed axiom
census is `[propext]` for the three `simp`-based Boolean/propositional
equivalence theorems and `[]` for `firstOwner_unique` and
`deployedConstantsExact`; see `CORRESPONDENCE.md`.

The source/cardinality correspondence and nonclaims are in
`CORRESPONDENCE.md`.
