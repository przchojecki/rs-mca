# M1 Cycle84 Witness Fixtures

Status: AUDIT / FINITE-MODEL-WITNESS.

This directory contains compact witness data for the Cycle84 finite model used
by `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`.

`slot_logs.json` gives one discrete log certificate for each of the 336
normalized slot values. It is checked by:

```sh
python3 experimental/scripts/verify_m1_cycle84_projected_log_certificate.py
```

The verifier checks that every log exponentiates to the current normalized slot
value, verifies colors and residue vectors, and checks the tau-pair projected
log structure. It does not rerun the projected duplicate-bin census.

`projected_census_receipt.json` records the compact JSON output of the archived
heavy tau-folded projected duplicate-bin scan. It is checked by:

```sh
python3 experimental/scripts/verify_m1_cycle84_projected_census_receipt.py
```

The receipt verifier checks that the recorded half-domain count, duplicate-bin
keys, multiplicities, and energy arithmetic are consistent with the current
projected-log certificate, color-shell verifier, and kernel-lift candidates. It
does not rerun the heavy scan that produced the receipt.

Selected shards of the projected census can be regenerated from the current log
certificate by:

```sh
python3 experimental/scripts/verify_m1_cycle84_projected_census_shard_replay.py
```

By default this recompiles a temporary C++ replay and scans the 30 shards that
contain the receipt's duplicate bins. Use `--all-shards` for the complete
16,384-shard replay, and `--threads N` to set the OpenMP shard-scanning worker
count.
