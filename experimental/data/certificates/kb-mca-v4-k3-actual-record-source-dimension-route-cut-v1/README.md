# KoalaBear K3 actual-record dimension-sensitivity audit v1

This packet gives an actual deployed KoalaBear received line and a
full-extension-degree affine bad slope whose shifted-lattice minimum is
exactly `67473` under both printed dimension conventions. Relative to the
code-dimension shift `K=k`, this is the boundary numerical profile. Relative
to the finite prefix shift `K=k+1`, it is the first-interior numerical profile.

No frozen Q, BC, or `U_new` owner is inferred. The cited Q theorem concerns a
special prefix witness family, and the sources do not provide the missing
dimension/priority projection from the arbitrary actual record to the frozen
owner cells. The result is therefore an exact dimension-sensitivity audit and
an open `SEM-QBC` adapter requirement—not success condition A or B, a K3
closure, or a ledger payment.

The zero-codeword witnesses lie on the pure `A g1` census ray (`B=0`), so the
packet also does not claim primitive `r_out=4` survival or membership in any
of #1157's thirteen endpoint routes. Ledger movement is zero.

## Replay

The primary check is deliberately fail-closed: the exact public-DAG checkout
must be supplied, or source replay fails.

```bash
python3 -B experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.py \
  --check --tamper-selftest --dag-root /path/to/rs-mca-prize-dag
python3 -B -O experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.py \
  --check --tamper-selftest --dag-root /path/to/rs-mca-prize-dag
/usr/local/bin/sage \
  experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.sage
~/math_code/.venv/bin/python \
  experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1_flint.py
```

The DAG root must contain exact commit
`3edb8b31b6735a0a2302a578a21dc6e50bd64046`. The primary verifier checks all
five repository pins and all six DAG pins against their committed bytes; it
also requires the working repository sources to equal the exact #1158 pins.

The optional Wolfram replay is:

```bash
~/math_code/scripts/wm.sh -file \
  experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.wl
```

The primary checker rejects duplicate keys, floats, NaN, booleans in integer
positions, extra nested fields, hostile semantic mutations, and parser
mutations. It checks the recursively strict schema, canonical payload seal,
packet hashes, architecture and partition, row-manifest seal and chronology,
field/subgroup arithmetic, lattice root bounds, profile arithmetic, pure-ray
scope, null ledger, and the exact huge support-count fingerprint. Sage, FLINT,
and Wolfram independently replay the arithmetic without making owner claims.

#1157 and #1158 were also replayed separately at their exact heads during the
audit. This packet itself binds #1158's parent manifest and exact source bytes;
it does not pretend that hashing the parent manifest reruns every predecessor
check.
