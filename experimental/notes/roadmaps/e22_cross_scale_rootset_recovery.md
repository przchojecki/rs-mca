# E22 Cross-Scale Root-Set Recovery

- **DAG node:** `e22_cross_scale_rootset_recovery`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_cross_scale_rootset_recovery/`
- **Depends on:** `e22_fixed_scale_staircase_injectivity`
- **Verifier:** `python3 experimental/scripts/verify_e22_cross_scale_rootset_recovery.py`

## Statement

If two E22 staircase locators at possibly different quotient moduli are equal,
then they have the same support root set.  Applying fixed-scale recovery at
each modulus recovers the corresponding tail and selected quotient fibers at
that scale.  Thus any hidden multiplicity is exactly a cross-scale equality
of recovered root-set data.

## Proof

Suppose

```text
L_B(X) G(X^M) = L_{B'}(X) G'(X^{M'}).
```

Both sides are monic squarefree locators over distinct domain points.  A
monic squarefree locator is determined by its root set, so equality of the
polynomials implies equality of the underlying support set `R`.

Now fix one participating modulus, say `M`.  The proved fixed-scale
injectivity node recovers from `R` the selected quotient fibers

```text
H_M(R) = {z : pi_M^{-1}(z) subset R}
```

and then the tail

```text
B_M(R) = R \ union_{z in H_M(R)} pi_M^{-1}(z).
```

The same argument applies at `M'`.  Hence no additional algebraic
multiplicity is hidden in the cross-scale equality: the locator gives the
common support, and each scale's parameters are the fixed-scale recovery of
that same support.

## Role In The Program

This is the cross-scale deduplication handoff for the `(Q)` quotient-ledger
route.  It reduces a possible equality of quotient-staircase parameterizations
at different moduli to a canonical support-level question, which is the object
priced by the subsequent E22 minimal-scale and overlap ledgers.

