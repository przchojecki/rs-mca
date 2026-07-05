# E22 Cross-Scale Support Canonical Form

- **DAG node:** `e22_cross_scale_support_canonical_form`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_cross_scale_support_canonical_form/`
- **Depends on:** `e22_cross_scale_rootset_recovery`
- **Verifier:** `python3 experimental/scripts/verify_e22_cross_scale_support_canonical_form.py`

## Statement

For any E22 staircase support `R`, the set of quotient moduli `M > t` for
which `R` has a tail-plus-full-`M`-fibers representation is recovered
canonically from `R`.

For each divisor `M` of the domain size, define

```text
F_M(R) = union of all M-fibers fully contained in R,
B_M(R) = R \ F_M(R).
```

Then `R` has a candidate tail-plus-full-fibers representation at scale `M`
exactly when `|B_M(R)| < M`.  In that case `B_M(R)` is the recovered tail and
the full fibers in `F_M(R)` are the selected quotient fibers.  Equal-support
cross-scale representations therefore have the same canonical support-scale
data.

This canonicalization may include tail-only candidate scales; downstream
nondegeneracy and pricing multiplicity are handled by the later
`e22_cross_scale_pricing_multiplicity` node.

## Proof

Fix a support `R` in the multiplicative subgroup domain.  For a divisor `M`
of the domain size, the quotient map `x -> x^M` partitions the domain into
fibers of size `M`.

If

```text
R = B union (full selected M-fibers),    |B| < M,
```

then every selected full fiber is contained in `R`, so it appears in
`F_M(R)`.  Conversely, since `|B| < M`, the tail cannot contain any additional
complete `M`-fiber.  Hence the full fibers contained in `R` are exactly the
selected fibers, and the leftover set is exactly the tail:

```text
F_M(R) = union selected fibers,
B_M(R) = B.
```

This fixed-scale recovery can be applied simultaneously to every divisor
`M`.  Therefore the candidate scales are precisely those with
`|B_M(R)| < M`, and at each such scale the recovered tail and selected fibers
are uniquely determined by `R`.

If two staircase parameterizations have equal support, the
`e22_cross_scale_rootset_recovery` node first identifies the common support
root set.  Applying the rule above to that common support gives the same
canonical object:

```text
(R, {M : |B_M(R)| < M}, {B_M(R), selected M-fibers}_M).
```

## Role In The Program

This note is the first canonical quotient-staircase ledger object for the
`(Q)` missing-input route in `agents.md`.  It lets later exact prefix-collision
and quotient-pricing work use support-scale classes rather than raw
parameterizations, isolating the remaining work in explicit minimal-scale,
overlap, and multiplicity nodes.

