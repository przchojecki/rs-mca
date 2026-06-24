# M1 Cycle116 External Packet Source Hash Audit

Status: AUDIT / EXTERNAL-CYCLE116-SOURCE-HASHES-VERIFIED.

Date: 2026-06-24.

This note verifies the source objects behind the compact Cycle116 external
packet contract:

```text
experimental/data/witnesses/m1-cycle116/external_packet_contract.json
```

The contract records four files from PR #96, branch `cycle58-5p5-audit`, commit
`fdb3cacece5a7f71399f12c697bd5193806f82ef`. The source-hash verifier checks
those paths against the actual Git objects at that commit.

## Source Files

The checked source files are:

```text
fixed_jet_certificate.json
cycle84_anchor.json
STANDALONE_CERTIFICATE_SECTION.md
verify_transfer.py
```

The verifier checks, for each file:

```text
Git blob id,
file mode,
byte size,
SHA256 digest,
path at the recorded PR #96 head commit.
```

It also checks that the two JSON inputs are copied exactly into the compact
contract:

```text
fixed_jet_certificate.json == contract["fixed_jet_certificate"],
cycle84_anchor.json == contract["cycle84_anchor"].
```

For the standalone proof text and transfer verifier, the audit keeps exact hash
binding as the authoritative check and additionally verifies a short set of
landmark fragments for the native `LD_sw`, smooth `LD_sw`, field-ledger, and
verifier-success clauses.

## Reproducibility

Fetch the PR #96 Git object once:

```sh
git fetch origin pull/96/head:refs/remotes/origin/pr-96
```

Then run:

```sh
python3 experimental/scripts/verify_m1_cycle116_external_packet_sources.py
python3 experimental/scripts/verify_m1_cycle116_external_packet_sources.py --json
```

The verifier is nonmutating. It reads the recorded source files with
`git show <commit>:<path>` and fails closed if the commit is not present in the
local Git object database.

## Effect

The previous external-packet comparison reduced the boundary to reviewer
acceptance that the compact contract faithfully records the hash-pinned PR #96
files. This source-hash audit makes that comparison executable for the actual
Git objects. The remaining review question is no longer whether the local
contract points at the intended files; it is whether reviewers accept the
external proof text and verifier content themselves.

This still does not discharge the official ABF PDF/source gate, and it does not
promote the Cycle120 chain beyond its stated audit/conditional status.
