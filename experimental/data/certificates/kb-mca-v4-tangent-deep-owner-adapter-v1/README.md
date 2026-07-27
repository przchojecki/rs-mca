# KoalaBear v4 tangent-plus-deep owner adapter certificate

This directory freezes the direct active-v4 successor partition proved in
`experimental/notes/frontier-adjacent/kb_mca_v4_tangent_deep_owner_adapter_v1.md`.

The packet banks two source-bound owner envelopes:

```text
SOURCE_COORDINATE_TANGENT_IMAGE                 981104
ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER       349526
known total                                    1330630
remaining budget                  274980728110064457
```

The deep cell is applied only after tangent. Its global `349526` envelope is
valid under that restriction. Q, balanced core, and final complement remain
null and nonbankable.

Files:

* `row_manifest.json` freezes the row, source bindings, source-owner
  hypotheses, and five-stage exact first-match partition.
* `manifest.json` freezes the four accounting atoms and open closure state.
* the schema under `experimental/data/schemas/` fixes the architecture and
  partition digest.

Replay from the repository root:

```sh
python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_owner_adapter_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_owner_adapter_v1.py --tamper-selftest
```

Regenerate intentionally with:

```sh
python3 experimental/scripts/verify_kb_mca_v4_tangent_deep_owner_adapter_v1.py --emit
```

The Python verifier is structural. The source cardinality theorems are the
bound files printed in `row_manifest.json`; the finite first-match and integer
kernels are additionally formalized in the companion stdlib-only Lean
package.

This certificate does not import the legacy M1 stack, replay conditional Q,
close the row, or move an endpoint.
