# Mixed-Radix Frontier Reframe

- **Status:** PROVED / citation reframe.
- **DAG node:** `mixed_radix_frontier`.
- **Certificate:** `experimental/data/certificates/mixed-radix-frontier/mixed_radix_frontier_reframe.json`.
- **Verifier:** `python3 experimental/scripts/verify_mixed_radix_frontier_reframe.py --check experimental/data/certificates/mixed-radix-frontier/mixed_radix_frontier_reframe.json`.

This packet records why mixed-radix smooth domains are not a prerequisite for
the official prize box.  The ABF grand-challenge statement defines the smooth
evaluation domain as a multiplicative subgroup whose size is a power of two.
Thus the deployed smooth-domain family is 2-power; mixed-radix packets remain
useful experiments and possible generalizations, but they are not a critical
frontier requirement for the official 2-power prize reading.

## Claim

The `mixed_radix_frontier` node closes by vacuity for the official prize
family:

```text
official smooth domain: multiplicative subgroup of power-of-two order
mixed-radix domains: outside this official box unless a maintainer broadens it
```

Repo notes sometimes use multiplicative cosets of 2-power subgroups.  This is
a conservative modelling convention: multiplying the evaluation domain by a
nonzero scalar is a coordinate change of the same 2-power-order structure.  It
does not introduce a mixed-radix domain.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 5, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The decisive fragments are:

```text
smooth evaluation domain
multiplicative subgroup
size is a power of two
```

These are domain-family conditions.  They leave no mixed-radix obligation in
the official smooth multiplicative prize box.

## Consequence

Mixed-radix notes should be labelled as one of:

```text
GENERALIZATION        beyond the official 2-power smooth-domain box
TOY/FALSIFIER         stress-test for proof machinery
CONSERVATIVE_AUDIT    checks whether a 2-power argument would survive broader domains
```

They should not block official-row proof packets whose statements are explicitly
restricted to the ABF 2-power smooth-domain family.

## Non-Claims

- This packet does not prove any theorem for mixed-radix domains.
- This packet does not invalidate existing mixed-radix experiments.
- This packet does not broaden the official prize family beyond 2-power smooth
  multiplicative domains.
