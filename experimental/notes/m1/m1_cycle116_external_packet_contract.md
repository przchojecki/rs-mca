# M1 Cycle116 External Packet Contract Comparison

Status: AUDIT / EXTERNAL-CYCLE116-PACKET-CONTRACT-COMPARED.

Date: 2026-06-24.

This note closes one finite source-comparison boundary in the M1 Cycle120
chain. It records a compact contract extracted from the closed external
Cycle116 packet in PR #96 and checks that the packet uses exactly the same
field model, slot blocks, co-support, native fixed-jet bridge, smooth lift, and
Cycle84 finite values as the local M1 verifiers in this PR.

The extracted contract is:

```text
experimental/data/witnesses/m1-cycle116/external_packet_contract.json
```

It is pinned to PR #96, branch `cycle58-5p5-audit`, commit
`fdb3cacece5a7f71399f12c697bd5193806f82ef`, with hashes for the external
`fixed_jet_certificate.json`, `cycle84_anchor.json`,
`STANDALONE_CERTIFICATE_SECTION.md`, and `verify_transfer.py` source files.

The corresponding Git-object source check is:

```text
experimental/notes/m1/m1_cycle116_external_packet_source_hash_audit.md
python3 experimental/scripts/verify_m1_cycle116_external_packet_sources.py
```

That verifier reads the recorded files from the PR #96 head commit with
`git show`, checks blob ids, file modes, byte sizes, and SHA256 digests, and
checks that the two JSON inputs are copied exactly into the compact contract.

The external transfer verifier itself is replayed in:

```text
experimental/notes/m1/m1_cycle116_external_transfer_replay_audit.md
python3 experimental/scripts/verify_m1_cycle116_external_transfer_replay.py
```

That wrapper materializes the PR #96 packet in a temporary directory, runs the
hash-pinned `verify_transfer.py`, and compares its native and smooth `LD_sw`
ledger to the current local Cycle120 end-to-end chain.

## Local Comparison

The verifier

```text
python3 experimental/scripts/verify_m1_cycle116_external_packet_contract.py
```

checks the extracted packet against the current local audits:

```text
the field is F_17[X]/(X^16+X^8+3);
eta=6X^9 and beta=X+2 match the local Cycle116 model;
the three base exponent sets and base locator polynomials match the local
  slot identity replay;
the packet slot indices are exactly the seven active cosets 1,...,7;
the source co-support clause is
  J_T={1} union union_{t=1}^7 eta^t lift(i_t,a_t);
the local slot assembly verifies |J_T|=1+7*16=113;
the native parameters are n=256, j=113, sigma=6, k=137, agreement=143;
the smooth lift adds R of size 137 and A of size 119, giving
  n=512, j=250, k=256, agreement=262, delta=125/256;
the imported Cycle84 values match the exact local chain:
  packet supports 52,747,567,104,
  distinct products 52,747,567,092,
  ordered off-diagonal energy 24,
  m_max=2.
```

## Effect On The M1 Chain

Before this comparison, the end-to-end Cycle120 note still had a source
boundary saying that the external Cycle116 packet had to be compared against
the locally verified `{1}` plus seven active 16-point slot-block co-support.
That comparison is now executable.

This does not prove official ABF compatibility, and it does not ask reviewers
to trust the closed PR #96 packet blindly. Together with the source-hash and
transfer-replay audits, it narrows the remaining source issue to reviewer
acceptance of the external verifier's provenance and output if that packet is
cited directly. The fixed-jet proof-logic core is now recorded locally in:

```text
experimental/notes/m1/m1_fixed_jet_ldsw_transfer_theorem.md
python3 experimental/scripts/verify_m1_fixed_jet_ldsw_theorem.py
```

## Remaining Boundaries

The remaining boundaries are:

```text
reviewer acceptance of the Cycle84 generated replay source contract;
official ABF PDF/source verification for the Cycle120 row gates, sampler,
  smoothness, same-support predicate, and closed-threshold convention.
external PR #96 provenance/output review if the packet is cited directly.
```

## Reproducibility

Run:

```sh
python3 experimental/scripts/verify_m1_cycle116_external_packet_contract.py
python3 experimental/scripts/verify_m1_cycle116_external_packet_contract.py --json
python3 experimental/scripts/verify_m1_cycle116_external_packet_sources.py
python3 experimental/scripts/verify_m1_cycle116_external_packet_sources.py --json
python3 experimental/scripts/verify_m1_cycle116_external_transfer_replay.py
python3 experimental/scripts/verify_m1_cycle116_external_transfer_replay.py --json
```

Both verifiers are nonmutating. The contract comparison imports and runs the
local Cycle84, Cycle116 slot identity, slot assembly, fixed-jet bridge, and
smooth-lift verifiers, then checks the exact cross-artifact equalities listed
above. The source-hash and transfer-replay audits require the PR #96 Git object
locally:

```sh
git fetch origin pull/96/head:refs/remotes/origin/pr-96
```
