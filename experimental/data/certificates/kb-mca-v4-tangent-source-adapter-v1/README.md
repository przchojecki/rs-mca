# KoalaBear v4 tangent source adapter certificate

This directory certifies Lane K1 gate **(B)** for the deployed KoalaBear MCA
row. It banks exactly one active Grande Finale v4 atom:

```text
U_paid = 981104 distinct bad finite slopes per received line
```

The architecture is `GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1` and the partition digest is
`4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc`. The declared owner chronology is:

1. `SOURCE_COORDINATE_TANGENT_IMAGE`;
2. `ACTIVE_V4_BOUNDARY_PREFIX_Q`;
3. `ACTIVE_V4_BALANCED_CORE`;
4. `UNPAID_V4_COMPLEMENT`.

The four cells are iterated exact set differences. Only the first has an upper
payment here. The exact known ledger is

```text
B*                           = 274980728111395087
U_paid                       =                981104
remaining numerical reserve = 274980728110413983
```

The remaining number is reserve, not an allocation. `U_Q`, `U_BC`, and `U_new`
remain open. The legacy M1 value `422354730332` is recorded only for comparison
and is not imported.

## #1132 source-pin repair

The predecessor row and manifest pinned `experimental/grande_finale.tex` at
blob `8a5d9791900ca9eed773feba146b92ad296704ce`.  The exact #1132 predecessor
contains the material `b13de8113` saturated-balanced-core status update at
blob `6b21d6ea937a8a9f85fc7ade6032d73efd4c7222`.  The row and manifest seals in
this directory were refreshed to bind the latter blob.  The packet verifier
passes after that repair.  Drift in `agents.md` remains a printed steering
diagnostic, not a proof-source gate.

## Files

- `row_manifest.json` freezes the row, architecture, partition, owner order,
  quantifier, unit, and source hashes.
- `manifest.json` records all four atom slots and the one bankable value.
- `../../schemas/kb_mca_v4_tangent_source_adapter_v1.schema.json` fixes the
  machine contract.
- `../../../notes/frontier-adjacent/kb_mca_v4_tangent_source_adapter_v1.md`
  contains the source-bound proof and scope audit.
- `../../../lean/kb_m1_source_bound_bridge/` contains the stdlib-only formal
  finite-image/partition kernel.
- `../../../scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py` is structural
  replay, not proof validation.

## Replay

```text
python3 experimental/scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py --check
python3 -O experimental/scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py --check
```

Lean is validated by a direct `lake build` of the package. Green compilation must still
be compared manually with the source theorem and the correspondence note.
