# Singleton-MASTER reductions certificate

This packet checks the conventions and finite regressions supporting the exact
analytic reductions in `singleton_master_reductions.md`.

The proof status is intentionally fail closed:

```text
SIM status: OPEN
unconditional SIM: false
unconditional PDSP_2: false
```

## Claim map

| Claim | Proof authority | Machine gate | Status |
| --- | --- | --- | --- |
| Insertion-position factorization | Note, Section 2 | `insertion_factorization` | Proved |
| Normalized sufficient criterion | Note, Section 3 | `normalized_criterion` | Proved reduction |
| Terminal singleton coordinate | Note, Section 4 | `terminal_coordinate` | Proved |
| Scalar upper-cap lemma | Note, Section 5 | `scalar_upper_cap_regression` | Proved |
| First-insertion positivity | Note, Section 7 plus ordinary MASTER authority | `first_insertion_positivity_regression` | Proved |
| Cap-six and shifted-Jacobi source cuts | Note, Section 6 | `source_m0_guardrails` | Proved counterexamples |
| All-position singleton MASTER (`SIM`) | None | Fail-closed status guard | Open |

Run from the repository root:

```bash
python experimental/scripts/verify_singleton_master_reductions.py --write-manifest --emit-cert
python experimental/scripts/verify_singleton_master_reductions.py --check
python experimental/scripts/verify_singleton_master_reductions.py --tamper-selftest
```

The script is a regression verifier. The proved all-depth reductions are established
by the analytic arguments in the note, not by the finite scans.

`SHA256SUMS.txt` hashes the four stable packet-owned inputs: the note, verifier,
consumer contract, and this README, after normalizing UTF-8 text to LF. The
emitted JSON certificate and the manifest itself are excluded to avoid a
self-referential digest. Shared coordination files (`experimental/agents-log.md`
and `experimental/scripts/README.md`) are intentionally excluded because
unrelated future entries must not invalidate this certificate; the outer PR
bundle manifest still covers their delivered versions. The verifier rejects
missing entries, extra entries, digest mismatches, and changes to the bound
ordinary-MASTER authority files.
