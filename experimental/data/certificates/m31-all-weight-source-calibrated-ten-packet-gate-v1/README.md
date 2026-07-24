# M31 all-weight source-calibrated ten-packet gate v1

This packet certifies one exact route cut for the Mersenne-31 ordinary-list
row at agreement `1116023`.

It proves that an additive shallow-census closure with a structured cap `C`
and a uniform primitive exchange-degree cap `c` must satisfy

```text
C + 913682*c <= 15775932.
```

Any structured owner declared to absorb the certified fixed-remainder C1
source must allow at least `6796404` nonanchor companions. Consequently
`c >= 10` cannot close this architecture. The first viable integer is `c=9`,
which requires `C <= 7552794`.

The fixed-remainder source itself occupies at most `447` MDS-admissible
positive exchange degrees relative to an anchor (`33 <= e <= 479`), so one
degree contains at least `15205`
companions. Thus the cap nine must be imposed only after a source-bound
structured first-match removal.

The packet moves no v4 atom and does not close the row.

Replay:

```bash
python3 experimental/scripts/verify_m31_all_weight_source_calibrated_ten_packet_gate_v1.py --check
python3 -O experimental/scripts/verify_m31_all_weight_source_calibrated_ten_packet_gate_v1.py --check
python3 experimental/scripts/verify_m31_all_weight_source_calibrated_ten_packet_gate_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_all_weight_source_calibrated_ten_packet_gate_v1_independent.py
```

The main verifier checks strict JSON, source hashes, predecessor payload pins,
the exact Grande Finale provenance migration, the exact arithmetic, and
hostile mutations. The independent verifier derives
the load-bearing integers from the raw row and source parameters without
importing the main verifier.
