# Reserve Certificate JSON Schema

- **Status:** AUDIT / EXPERIMENTAL.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note accompanies `experimental/reserve_certificate_schema.json`,
  a Draft 2020-12 JSON Schema for Paper C's field-separated proximity reserve
  certificate.

## What The Schema Mirrors

The schema follows `tex/snarks_v4.tex` `def:cert` and `rule:reserve`.
It requires:

- the certificate tuple fields:
  `q_arith`, `q_gen`, `q_line`, `domain`, `n`, `k`, `rho`, `delta`, `a`,
  `sigma`, `mu`, `nu`, `extension_degree`, `B_L`, `A_M`, `Gamma_ent`,
  `Gamma_Q`, `Gamma_M`, `C_loc`, `lambda_list`, and `lambda_mca`;
- the eight evidence blocks in `def:cert`: generated-field ledger, quotient
  profile, locator/list bound, interleaved-list bound, list-over-field budget,
  MCA or line-decoding budget, failure-ladder audit, and extension status;
- the six checks in `rule:reserve`: entropy margin, local slack, quotient
  profile budget, distance/failure gap, list-field budget, and MCA or
  line-decoding budget.

Each evidence block carries a proof status and source labels so that a generated
certificate can distinguish theorem-backed entries from assumptions,
conjectural entries, obstruction audits, and experimental script output.

## Design Choices

- Numeric fields that may naturally be exact rationals or symbolic expressions
  accept either JSON numbers or nonempty strings.
- Bit quantities use a shared object with a primary value and optional lower
  or upper bounds, so scripts can record conservative intervals.
- Extension mode is explicit.  If `q_line` or `q_chal` exceeds `q_gen`, the
  `extension_status` block has separate slots for the extension-list derivation
  and the extension-MCA or line-decoding derivation.
- The top-level `certificate_kind` separates theorem-backed certificates,
  conditional certificates, and obstruction audits.

## Validation Performed

The schema was checked as valid JSON with:

```bash
python3 -m json.tool experimental/reserve_certificate_schema.json >/dev/null
```

It was also checked with `jsonschema.Draft202012Validator.check_schema`, and a
minimal sample certificate containing all required blocks validated against it.

It is not yet wired to a certificate emitter.  The next step is to add a small
example certificate and validate it with a JSON Schema implementation, then make
future certificate emitters target this shape.
