# Four-row exact-completion compiler certificate

This directory contains the historical open-state certificate for the four
deployed Grande Finale v3 adjacent rows. Active Grande Finale v4 supersedes
its MCA atom interface and list chronology, so this certificate is not a
current-source acceptance gate. It recomputes the exact row calibration,
binds the v3 proof artifacts, enforces one compatible first-match architecture,
and records the v3-era architecture route cut.

It does **not** certify any row safe.  The canonical terminal is
`ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET`, and all four row-sharp `U_Q`
values remain null.

Replay from the repository root:

    python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --check
    python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --check
    python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --tamper-selftest
    python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1.py --tamper-selftest
    python3 experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py --check
    python3 -O experimental/scripts/verify_four_row_exact_completion_compiler_v1_independent.py --check

The machine-consumable future-candidate contract is
`experimental/data/schemas/four_row_exact_completion_candidate_v1.schema.json`.
The runtime enforces its exact object shape and additionally parses typed,
payload-hashed partition, atom, Q-component, and architecture/owner-map
adapters.  It rejects path aliases, noncanonical or escaping source paths, unbound
digests, unused sources, incomplete owner order, and scope/value drift.
This is a necessary structural preflight only: candidate-authored adapters are
not trusted attestations.  The command always emits `closure_certified=false`,
the trusted-source registry is empty, and no atom is banked until independent
proof review is followed by an explicit compiler/registry update.  Its legacy
content detector is deliberately recorded as incomplete under arbitrary
provenance transforms; it is a fail-closed convenience check for recognized
inputs, not a trust oracle.
Any future nonempty trusted registry must additionally reject self/cyclic
adapter graphs and prove that every transitive dependency terminates at a
reviewed, registry-pinned theorem or exact certificate leaf.

Known imported-packet provenance issue: the older fixed-line extension
correction's full Python acceptance gate still names two pre-promotion source
paths.  This compiler binds the live dimension--degree theorem in
`tex/cs25_cap_v13_2.tex` directly and records the older gate as stale; the
correction's core Python census and independent Sage witness replay pass.
