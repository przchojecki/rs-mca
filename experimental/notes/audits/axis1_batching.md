# Axis 1 Batching Shape

- **Status:** PROVED / citation check.
- **DAG node:** `axis1_batching`.
- **Certificate:** `experimental/data/certificates/axis1-batching/axis1_batching.json`.
- **Verifier:** `python3 experimental/scripts/verify_axis1_batching.py --check experimental/data/certificates/axis1-batching/axis1_batching.json`.

This packet resolves S0 axis 1.  The official MCA sampler uses affine lines in
two received words, matching the repo convention `u + z v`.

## Statement

ABF26 defines the relevant set family as lines:

```text
{f1 + gamma f2}_{gamma in F}
```

and states that the MCA grand challenge is considered with respect to this
line family.  Therefore the official sampler is a two-word affine line, not a
nonlinear powers-of-alpha batching convention.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, pages 3 and 17, with PDF
sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
Lines
{f1 + gamma f2}_{gamma in F}
family Flines
only consider MCA with respect to the family of lines
```

## Consequence

MCA packets may use the repo's affine-line parameterization:

```text
line(z) = u + z v
```

If a protocol packet uses another sampler shape, such as powers of one
challenge, it must state that as a protocol-specific generator variant rather
than the official MCA object.

## Non-Claims

- This packet does not analyze polynomial-generator MCA.
- This packet does not prove a proximity bound for any line family.
- This packet does not decide CA/list objects; it fixes only the MCA sampler
  shape for this axis.
