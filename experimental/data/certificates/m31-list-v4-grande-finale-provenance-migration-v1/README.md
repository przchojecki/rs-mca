# M31 LIST v4 Grande Finale provenance migration v1

This certificate proves exact compatibility between the Grande Finale v4
bytes sealed by nineteen M31 LIST manifests and the current source after the
`b13de8113` status correction.

It reconstructs the prior source by six exact inverse edits, checks both
whole-file SHA-256 values, checks the five-atom LIST formula and labels, and
audits all affected manifest payloads, source bindings, and internal pins.
Only the canonical Grande Finale path with one allow-listed binding identity
per manifest may use the compatibility exception.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --check
python3 -O experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --tamper-selftest
```

The packet moves no atom and closes no row.  It does not alter or reseal any
predecessor manifest, and it does not make the original standalone
predecessor verifiers accept the current whole-file hash.
