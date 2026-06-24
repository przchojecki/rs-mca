# M1 Cycle116 External Transfer Replay Audit

Status: AUDIT / EXTERNAL-CYCLE116-TRANSFER-REPLAYED.

Date: 2026-06-24.

This note records a replay of the hash-pinned external Cycle116 verifier from
PR #96. The verifier is:

```text
verify_transfer.py
```

from PR #96, branch `cycle58-5p5-audit`, commit
`fdb3cacece5a7f71399f12c697bd5193806f82ef`.

The local wrapper materializes the external packet in a temporary directory
from Git objects and runs the external fail-closed verifier on its recorded
inputs:

```text
inputs/fixed_jet_certificate.json
inputs/cycle84_anchor.json
imports/cycle84_master_proof_certificate.json
imports/slot_logs.json
imports/light_verification.out
imports/STANDALONE_FINITE_CERTIFICATE.md
```

All imported files are checked against the SHA256 digests recorded in
`cycle84_anchor.json` before the external verifier is executed.

## Verified Output

The external verifier returns:

```text
decision = CYCLE116_TRANSFER_CERTIFICATE_VERIFIED,
native LD_sw(RS[F_17^16,<eta>,137],143) >= 52,747,567,092,
smooth LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092,
q_gen = q_code = q_line = 17^32,
q_chal = None,
52,747,567,092 / 17^32 > 2^-128.
```

It also emits a concrete affine-line receipt for a reference tuple, including
hashes of the lifted `f` and `g` words, the bad slope `z0`, and the support and
co-support.

The wrapper compares these outputs to the current local end-to-end M1 chain, so
the replay is not only an external exit-code check. It verifies agreement with
the local native row, smooth row, field ledger, density gate, and scope
nonclaims.

## Reproducibility

Fetch the PR #96 Git object once:

```sh
git fetch origin pull/96/head:refs/remotes/origin/pr-96
```

Then run:

```sh
python3 experimental/scripts/verify_m1_cycle116_external_transfer_replay.py
python3 experimental/scripts/verify_m1_cycle116_external_transfer_replay.py --json
```

The wrapper is nonmutating. It writes only to a temporary directory and removes
that directory after the external verifier exits.

## Scope

This audit makes the external transfer executable from hash-pinned source
objects and checks that its theorem ledger matches the local Cycle120 chain. It
does not discharge the official ABF PDF/source gate. The generic fixed-jet
proof logic used by the external verifier is now recorded locally in
`experimental/notes/m1/m1_fixed_jet_ldsw_transfer_theorem.md`; this replay
remains a provenance and executable-output check for the PR #96 packet.
