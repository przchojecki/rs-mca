# Rules Freeze Citation Packet

- **Status:** PROVED / citation check.
- **DAG node:** `rules_freeze`.
- **Certificate:** `experimental/data/certificates/rules-freeze/rules_freeze.json`.
- **Verifier:** `python3 experimental/scripts/verify_rules_freeze.py --check experimental/data/certificates/rules-freeze/rules_freeze.json`.

This packet records the prize-box conventions used by the downstream S0,
rate-axis, and list-side packets. It is a citation closure rather than a new
mathematical proof: the relevant challenge text is pinned to ABF26 / IACR
ePrint 2026/680, page 5, with a PDF hash.

## Claim

The operative smooth Reed-Solomon prize box uses:

```text
smooth domain: multiplicative subgroup of F of power-of-two size
target range:  k <= 2^40 and |F| < 2^256
rates:         rho in {1/2, 1/4, 1/8, 1/16}
list arity:    determinations are per declared constant m
gate:          eps* = 2^-128, with list budget eps* |F|
```

The subgroup wording is narrower than the campaign's common coset-form working
language. Coset-form arguments should therefore be treated as conservative
supersets unless a later packet explicitly needs subgroup-only normalization.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 5, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
multiplicative subgroup of F whose size is a power of two
rho(C) := k/|L|
one of 1/2, 1/4, 1/8, 1/16
k <= 2^40
|F| < 2^256
and a constant m
for a code C, an m, and an eps*
2^-128
```

These fragments assemble the rules layer consumed by `axis9_dither`,
`s0_zero_open`, and `m_handling`.

## DAG Consequence

The packet preserves the stricter reading needed by downstream ledgers:

```text
axis9_dither: no implicit dimension dither for official rows
s0_zero_open: rules layer has no remaining open convention axis
m_handling: fixed constant-m determinations are valid per-instance packets
```

`field_cap_check` and `rules_m_reading` remain the named component nodes for
the field/rate target range and the constant-`m` list quantifier respectively.

## Non-Claims

- This packet does not prove any safe or unsafe threshold.
- This packet does not promote v13 experimental rows into Paper D.
- This packet does not edit Papers A-D.
- This packet does not decide whether an external prize page has drifted after
  the pinned ABF26 PDF; it gives a reproducible citation baseline.
