# Verifier steering-source pin repair

**Status:** AUDIT / REPAIR.

**Replay:**

```text
python3 experimental/scripts/verify_steering_source_pin_demotion.py --check
python3 experimental/scripts/verify_steering_source_pin_demotion.py --tamper-selftest
```

Full packet replay (six verifiers, both modes, ~234s total) is listed in §4.

## 1. Defect

Five of six integrated verifiers did not replay at `71f6434`.  Two independent
causes, both packaging; no mathematical claim was affected and no recorded
integer changed.

**Cause A -- steering-source pin rot (four packets).**  The verifiers gate
`agents.md` by git blob hash inside their source-pin sets.  `agents.md` is the
repository's governance file: it is rewritten whenever the maintainer re-steers.
Commit `fb6d955` ("Prioritize post-Johnson RS list bounds") replaced blob
`30d8b9f1b4caa3c7504fe3d24fc7ce8da84de434` with
`b85f2d23fdca64ac3b36b815c85b9bc366970c35`, so every packet frozen against the
former blob began failing `--check` *before* it was integrated, through no fault
of the integration.  The failure mode is structural rather than incidental: any
packet that hard-gates a steering file has a lifetime bounded by the next
steering edit.

**Cause B -- transport-file dependency (one packet).**  Root `PR_BODY.md` and
standalone `experimental/agents-log-entry-*.md` fragments are PR transport; the
integration policy states they are deliberately not imported.  One verifier still
required them to be present, so it hard-failed in-repo on files that are never
supposed to exist there.

Observed state before repair:

```text
packet                                        --check  --tamper-selftest  cause
m31_quotient_prefix_flatness_t64_witness      FAIL     FAIL               A
kb_mca_v4_tangent_source_adapter_v1           FAIL     (unsupported)      A
kb_uq_boundary_prefix_tangent_rooted_shell_v1 FAIL     FAIL               A
m31_quotient_t16_mixing_floor                 FAIL     PASS               B
m31_quotient_band_swap_census_t16_mixing      FAIL     FAIL               A
m31_postjohnson_conversion_contract           PASS     PASS               --
```

The one passing verifier passes by timing accident: its packet was frozen after
`fb6d955`, so it pins the current blob and would rot at the next steering edit.

## 2. Repair

**Steering demotion.**  Each affected verifier declares

```python
STEERING_SOURCES = frozenset({"agents.md"})
```

and, at its source-pin comparison, reports drift instead of failing:

```text
NOTE steering source drifted: agents.md recorded <frozen>, observed <current>
```

The *recorded* blob is retained in the emitted payload, so packet digests remain
byte-reproducible under drift.  Provenance is preserved; only the gate is
removed.  The demotion is confined to `agents.md`: every other pinned source
stays a hard gate.

**Transport tolerance.**  The transport-file requirement is replaced by the
recorded-hash table already used by the band-swap census packet
(`LEGACY_PACKET_FILE_SHA256`).  The recorded hash of each transport file is
cross-checked against the certificate, so a tampered certificate entry is still
rejected; only *absence* is tolerated.

**Artifact-integrity restoration.**  The tangent-rooted shell packet had its
artifact-hash gate disabled wholesale during integration, leaving it with no
integrity check at all.  The gate is restored over retained files only: every
artifact present is hashed, and the set of absent artifacts must equal the
declared transport-only set.  The original inventory-equality test cannot apply
in-repo, since the packet root is the repository rather than a standalone bundle.

**Mode parity.**  The tangent source adapter already ran six semantic mutations
inside `check()` but exposed no `--tamper-selftest`.  The flag is now accepted,
so every packet verifier answers both modes.

## 3. Adversarial checks

```text
tamper a non-steering pinned source (grande_finale.tex)  -> rejected by all four
steering drift on agents.md                              -> tolerated, reported
tamper a recorded transport hash in the certificate      -> rejected
tamper a retained artifact (tangent-rooted shell)        -> rejected
un-declare a steering demotion                           -> rejected by the gate
```

The first line is the load-bearing one: the demotion must not become a general
weakening of source pinning.  It does not.

## 4. End state

All six verifiers pass both modes at repaired main:

```text
python3 experimental/scripts/verify_m31_quotient_prefix_flatness_t64_witness.py       --check | --tamper-selftest
python3 experimental/scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py            --check | --tamper-selftest
python3 experimental/scripts/verify_kb_uq_boundary_prefix_tangent_rooted_shell_v1.py  --check | --tamper-selftest
python3 experimental/scripts/verify_m31_quotient_t16_mixing_floor.py                  --check | --tamper-selftest
python3 experimental/scripts/verify_m31_quotient_band_swap_census_t16_mixing.py       --check | --tamper-selftest
python3 experimental/scripts/verify_m31_postjohnson_conversion_contract.py            --check | --tamper-selftest
```

Three certificates carry a one-line re-pin of the edited verifier's own recorded
`sha256`; no other recorded value changes anywhere in this packet.

## 5. Nonclaims

This packet proves nothing mathematical.  It moves no ledger term, bounds no
residual, kills no terminal, and changes no statement, status, or recorded
integer of any packet it touches.  It does not re-import transport files, and it
does not assert that the steering file's *content* is irrelevant to the packets
-- only that its blob hash is the wrong instrument for gating a replay.

The Lean-only deployed-owner-profiles packet has no Python verifier and is
therefore outside this repair; its authority is the `m31_q_rooted_shell` lake
build, unaffected by either cause.
