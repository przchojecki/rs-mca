# Atlas nonuniform `T(509,35,8)` certificate

**Author:** Manuel E. Rey-Álvarez Zafiria

This directory records an explicit nonuniform hierarchical `T(509,35,8)`
system of cardinality `762,054,269,114`.

`optimizer_output.json` contains the 305 selected six-color patterns and the
CP-SAT search metadata.  The optimizer status is `FEASIBLE`; it is used only
as a source of an explicit witness, not as an optimality certificate.

`cover.txt` is the compact frozen witness generated from that JSON file.
`primary_output.json` and `independent_output.json` record two exact audits.
Both auditors enumerate every relevant integer composition and recompute the
cardinality with integer binomial arithmetic.  They use only the Python
standard library.

From the repository root, reproduce the recorded cover and audits with:

```text
python3 experimental/scripts/verify_atlas_nonuniform_turan_cover.py \
  experimental/data/certificates/atlas-nonuniform-turan-35-to-8/optimizer_output.json \
  /tmp/atlas_cover.txt \
  /tmp/atlas_primary_output.json

python3 experimental/scripts/audit_atlas_nonuniform_turan_cover.py \
  /tmp/atlas_cover.txt \
  /tmp/atlas_independent_output.json

cmp /tmp/atlas_cover.txt \
  experimental/data/certificates/atlas-nonuniform-turan-35-to-8/cover.txt
cmp /tmp/atlas_primary_output.json \
  experimental/data/certificates/atlas-nonuniform-turan-35-to-8/primary_output.json
cmp /tmp/atlas_independent_output.json \
  experimental/data/certificates/atlas-nonuniform-turan-35-to-8/independent_output.json
```

The optional search implementation
`experimental/scripts/optimize_atlas_nonuniform_turan_cover.py` requires
OR-Tools.  Re-running the search is unnecessary for checking the finite
theorem, and a time-limited parallel search need not reproduce the same
feasible witness.

`SHA256SUMS.txt` authenticates the note, implementations, and recorded
certificate files.
