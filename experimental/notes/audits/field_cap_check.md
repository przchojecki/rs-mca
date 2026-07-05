# Field Cap Check

- **Status:** PROVED / citation check.
- **DAG node:** `field_cap_check`.
- **Certificate:** `experimental/data/certificates/field-cap-check/field_cap_check.json`.
- **Verifier:** `python3 experimental/scripts/verify_field_cap_check.py --check experimental/data/certificates/field-cap-check/field_cap_check.json`.

This packet pins the field and dimension caps used by the prize budget ledger.
The ABF grand-challenge statement works in the smooth Reed-Solomon family with
the official rates, target error, dimension cap, and field-size cap below.

## Statement

For the official smooth multiplicative prize box:

```text
rates:          rho in {1/2, 1/4, 1/8, 1/16}
target error:   eps* = 2^-128
dimension cap:  k <= 2^40
field cap:      |F| < 2^256
```

These constants are not heuristic ledger choices.  They are part of the
challenge instance and therefore control the exact budget
`B* = floor(eps* Q)` and the admissibility of large ambient fields.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 5, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
rho(C) is one of 1/2, 1/4, 1/8, 1/16
eps* = 2^-128
k <= 2^40
|F| < 2^256
```

## Consequence

Packets that use a row budget, field cap, or tower/admissibility argument
should state which of these constants they consume.  In particular, the
`|F| < 2^256` cap is a field-size cap on the ambient `F`, not a generated-field
entropy reserve that can be silently merged with another ledger.

## Non-Claims

- This packet does not compute any row threshold.
- This packet does not decide whether a specific field is a good exhibit.
- This packet does not merge generated, line, challenge, or ambient field
  ledgers.
