# Clean-Rate Corridor Pipeline

- **Campaign task:** C-2.
- **DAG node:** Q3R.3.
- **Status:** SKELETON / REPLAYED CERTIFICATE PACKET.
- **Verifier:** `experimental/scripts/verify_clean_rate_corridor_pipeline.py`.
- **Artifact:** `experimental/data/certificates/clean-rate-corridor-pipeline/clean_rate_corridor_pipeline_skeleton.json`.

This packet packages the clean prize-rate corridor rows for rates `1/4`, `1/8`,
and `1/16`.  It is intentionally lightweight: it replays committed arithmetic
certificates and emits per-row skeletons for the Row-C class and pinned
high-agreement class.  It does not run new Row-C sampling and does not claim a
new lower-agreement theorem.

## Sources

The verifier consumes:

```text
experimental/scripts/verify_roadmap_r2_numbers.py
experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json
experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json
experimental/data/certificates/row-c-e1-sampling/e1_sharp_norm_height_constants.json
```

It also calls the high-agreement compiler's exact adjacent boundary routine for
the pinned-class probes.

## Corridor Rows

| rate | quotient crossing | tau* crossing | cap crossing | width in cap cells |
|---|---:|---:|---:|---:|
| `1/4` | `0.744141` | `0.746811` | `0.748047` | `2.00` |
| `1/8` | `0.870854` | `0.872853` | `0.873047` | `1.12` |
| `1/16` | `0.934888` | `0.936162` | `0.936523` | `1.67` |

Each row checks the ordering

```text
list_lower < quotient < tau* < cap
```

and verifies that the upper list-window endpoint tracks `tau*` at the recorded
r2 tolerance.

## Per-Row Skeletons

| rate | integrality crossings `(relaxed, dyadic, planted)` | min margin bits | pinned power2 bits | first lower-agreement bit | Row-C even frontier at 256 bits |
|---|---:|---:|---:|---:|---:|
| `1/4` | `(176, 256, 256)` | `803035429458.8638` | `128..168` | `169` | `N' <= 100` |
| `1/8` | `(248, 256, 256)` | `3919267045601.578` | `128..169` | `170` | `N' <= 120` |
| `1/16` | `(384, 512, 512)` | `2729001948841.092` | `128..170` | `171` | `N' <= 112` |

For the pinned class, the adjacent power-of-two probes are part of the
certificate:

```text
1/4:  2^168 pinned, 2^169 requires lower-agreement theory
1/8:  2^169 pinned, 2^170 requires lower-agreement theory
1/16: 2^170 pinned, 2^171 requires lower-agreement theory
```

For the Row-C class, this packet records only the e1 norm-height frontiers and
the integrality margins.  The value-set sampler remains out of scope for this
lightweight PR.

## Replay

```bash
python3 experimental/scripts/verify_clean_rate_corridor_pipeline.py --write
python3 experimental/scripts/verify_clean_rate_corridor_pipeline.py --check
python3 experimental/scripts/verify_roadmap_r2_numbers.py
python3 experimental/scripts/verify_integrality_margin_tables.py --check experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json
python3 experimental/scripts/certify_high_agreement_threshold_package.py --check experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json
python3 experimental/scripts/verify_e1_sharp_norm_height_constants.py --check experimental/data/certificates/row-c-e1-sampling/e1_sharp_norm_height_constants.json
python3 -m py_compile experimental/scripts/verify_clean_rate_corridor_pipeline.py
```

## Nonclaims

This packet does not run `verify_row_c_e1_value_set_sampler.py`, does not launch
any large scan, does not prove lower-agreement theory beyond the pinned class,
does not prove the list-side safe theorem, and does not promote a leaderboard
row.  It only provides concrete per-rate certificate skeletons with replayed
arithmetic and margins.
