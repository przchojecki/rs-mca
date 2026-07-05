# E22 Fixed-Scale Staircase Injectivity

- **DAG node:** `e22_fixed_scale_staircase_injectivity`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_fixed_scale_staircase_injectivity/`
- **Verifier:** `python3 experimental/scripts/verify_e22_fixed_scale_staircase_injectivity.py`

## Statement

Fix a quotient modulus `M`.  A staircase support at this scale has the form

```text
R = B union (full selected M-fibers),    |B| < M,
```

and its locator can be written as

```text
L_R(X) = L_B(X) G(X^M),
```

where `G` records the selected quotient-fiber values.  For fixed `M`, this
locator determines both the selected fibers and the tail `B` uniquely.
Equivalently, there are no hidden multiplicities inside one fixed staircase
scale.

## Proof

A monic squarefree locator over distinct domain points determines its root
set uniquely.  Thus equality of two fixed-scale staircase locators implies
equality of their support root sets.

Given the root set `R`, recover the selected fibers by the intrinsic rule

```text
H_M(R) = {z : pi_M^{-1}(z) subset R}.
```

Every selected full fiber is contained in `R`, so it is recovered by this
rule.  Conversely, the tail has size `< M`, so it cannot contain a complete
additional `M`-fiber.  Therefore the recovered full fibers are exactly the
selected fibers.

After removing those full fibers, the remaining roots are exactly the tail:

```text
B = R \ union_{z in H_M(R)} pi_M^{-1}(z).
```

So the fixed-scale parameters `(B, H_M)` are uniquely determined by the
locator.

## Role In The Program

This fixes the first deduplication layer for the `(Q)` quotient-ledger route:
when the modulus is fixed, a quotient staircase column can be priced by
support root sets without paying for spurious tail/fiber parameter
multiplicity.

