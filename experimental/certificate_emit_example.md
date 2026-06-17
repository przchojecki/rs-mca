# Certificate Emitter Example

- **Status:** PROVED
- **Theorem/problem:** agents.md script output standard
- **Source:** experimental/certificate_emit_example.json

## Input Parameters

| Key | Value |
| --- | --- |
| `a` | 2 |
| `domain_order` | 12 |
| `k` | 6 |
| `prime` | 13 |
| `quotient_order` | 6 |
| `rho` | 1/2 |

## Mathematical Object

| Key | Value |
| --- | --- |
| `code` | RS[F_13,D,6] |
| `line` | u_z(x) = x^8 + z*x^6 |
| `radius` | 1 - k/n - 1/Nq = 1/3 |

## Result

| Key | Value |
| --- | --- |
| `locator_slope_count` | 13 |
| `locator_subset_of_mca` | true |
| `mca_bad_slope_count` | 13 |
| `mca_density` | 1 |

## Proof Certificate

| Key | Value |
| --- | --- |
| `method` | deterministic tiny example for certificate_emit.py |
| `script` | experimental/certificate_emit.py |
| `seed` | none |
