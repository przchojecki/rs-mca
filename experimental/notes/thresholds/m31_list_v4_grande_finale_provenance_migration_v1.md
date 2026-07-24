---
workboard_item: M0/M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The current Grande Finale v4 source is an exact status-only successor of the source sealed by nineteen M31 LIST manifests. Six declared inverse edits reconstruct the prior bytes and SHA-256 exactly, while the five-atom LIST formula and labels remain unchanged. Every affected manifest has a valid payload seal and every other bound source is fresh.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: PROVENANCE_MIGRATION_ONLY
quantifier: Uniform source-compatibility statement over the nineteen sealed manifests; no received-word theorem is added.
projection_and_unit: The preserved LIST contract counts distinct codewords per received word.
claimed_bound: No new numerical bound; ledger movement zero.
status: PROVED PROVENANCE MIGRATION / ROW OPEN
impact: ARCHITECTURE_BRIDGE
falsifier: A mismatch in either whole-file hash, any inverse fragment, the reconstructed prior hash, the LIST formula or labels, a manifest payload seal, a non-Grande-Finale source binding, or an allow-listed compatibility binding identity.
replay: python3 experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --check
---

# M31 LIST v4 Grande Finale provenance migration v1

## Statement and scope

Nineteen sealed M31 LIST manifests bind
`experimental/grande_finale.tex` at

```text
34618918de8fc1c1aac5642393f49019c60ff7041a9efeacbf0b8ea01eb3d8cd.
```

The current source has hash

```text
336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d.
```

The difference is the status correction introduced by `b13de8113`: five
inserted clarification blocks and one replacement of the audited-status
sentence.  The verifier removes or reverses those six exact fragments,
requires each current fragment to occur exactly once, and recovers the prior
`328284` bytes and prior SHA-256 exactly.  The current source has `330361`
bytes, so the net insertion is `2077` bytes.

This is stronger than treating a mutable source hash as informational.
Compatibility is granted only to the exact prior hash, at the canonical path,
and only for the one declared binding identity in each audited manifest.
Every other source binding must match the current repository bytes.

## Preserved LIST contract

Both the current and reconstructed sources contain exactly once:

\[
 U_{\rm list}
 =U_{\rm paid}+U_Q+U_{\rm list-int}+U_{\rm ext}+U_{\rm new}.
\]

The following labels also occur exactly once in each:

```text
sec:list-final-certificate
eq:list-final-ledger
prob:list-completion
thm:exact-completion-certificate
```

The one new paragraph inside `prob:list-completion` explicitly says that the
problem is the final v4 successor to the old arbitrary-word list-interior
clause and includes the prefix and extension terms.  It clarifies rather than
changes the five-atom obligation.

The frozen contract remains:

```text
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition:    816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom order:   U_paid, U_Q, U_list_int, U_ext, U_new
owner order:  LOW_EXACT_WEIGHT_PACKING,
              HIGH_BOUNDARY_EXACT_CODEWORD,
              HIGH_INTERIOR_EXACT_CODEWORD
unit:         DISTINCT_CODEWORDS_PER_RECEIVED_WORD
quantifier:   UNIFORM_OVER_ALL_RECEIVED_WORDS
```

## Manifest audit

The packet discovers the affected manifests rather than trusting a hand
count, then requires the discovered sorted set to equal an explicit
allow-list.  For all nineteen manifests it verifies:

1. canonical strict JSON;
2. the internal `payload_sha256`;
3. every one of the `284` source bindings;
4. all `40` embedded payload/certificate pins;
5. exactly one compatible Grande Finale binding;
6. freshness of the other `265` bindings; and
7. the exact binding ID, role, and scope eligible for compatibility.

The affected set includes the v4 source adapter and global compiler, the
post-adapter `c=2048` chain, rank six, and the four base-field rank-seven
packets.  The weighted-head rank-seven packet does not itself pin the old
Grande Finale hash; its cumulative predecessor chain reaches the affected
manifests.

## Consequence

The sealed mathematical packets may be consumed by a successor compiler
through this explicit compatibility certificate.  The original standalone
verifiers still compare whole-file hashes and therefore remain stale when
run directly on current `main`; this packet does not silently weaken them.

No atom changes:

```text
ledger movement          = 0
official endpoint movement = 0
row closed               = false
```

In particular, this packet does not turn a rank-seven, fixed-template,
support, column, or route-cut result into a codeword payment.

## Proof audit

Statement audited:

Whether the `b13de8113` Grande Finale status correction changes the M31 LIST
five-atom chronology or invalidates the source content sealed by the nineteen
affected manifests.

Files/sections read:

The current and reconstructed `experimental/grande_finale.tex` bytes; the
final LIST ledger and labels; all affected manifests; all of their source
bindings and internal payload pins; and the packet schema/verifier.

Dependencies:

- PROVEN: exact current hash, inverse-fragment multiplicities, reconstructed
  prior hash, LIST formula/label equality, manifest payload seals, and source
  freshness subject only to the declared exact ancestor compatibility.
- UNCHANGED/OPEN: all row-level null atoms and residual terminals.

Parameter dependence:

Finite exact source and row metadata only.  No asymptotic constants occur.

Layer-cake / dyadic summability:

Not applicable.

Moment / Markov / Chebyshev:

Not applicable.  `Grande Finale` and `Chebyshev` source names do not introduce
a probabilistic argument here.

Edge cases / notation:

The exception is keyed by canonical repository path, exact prior/current
hashes, manifest path, binding ID, role, and scope.  It cannot authorize a
different path or a later source edit.

Numerical evidence:

All hashes, byte counts, payload seals, and source counts are exact.

Verdict:

GREEN - the provenance migration obligation is satisfied; the mathematical
M31 LIST row remains open.

Remaining risks:

A successor global compiler must explicitly bind this migration packet.
Direct execution of predecessor verifiers remains stale by design.

Minimal next action:

Consume this migration in the v4 rank-seven/global source registry while
preserving zero route-cut movement and the current null atoms.

## Replay

```text
python3 experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --check
python3 -O experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --check
python3 experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_list_v4_grande_finale_provenance_migration_v1.py --tamper-selftest
```
