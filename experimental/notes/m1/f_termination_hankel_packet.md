# Hankel Termination Assembly Packet

- **Status:** PROVED / assembly over green predicates.
- **DAG node:** `f_termination_hankel`.
- **Certificate:** `experimental/data/certificates/f-termination-hankel/f_termination_hankel.json`.
- **Verifier:** `python3 experimental/scripts/verify_f_termination_hankel_packet.py --check experimental/data/certificates/f-termination-hankel/f_termination_hankel.json`.

This packet packages the refined Hankel-family termination claim from the
current `prize` DAG. The statement is deliberately the saturated
root-closure version, not the older raw sparse-lattice count.

## Claim

For rate-`1/2` Hankel-kernel instances over `mu_n`, after root-closure
saturation and after paid tangent, common-divisor, quotient, pullback, and
dihedral structures are routed to their ledgers, the number of reachable
unpaid primitive saturated states is

```text
n^{O(W^2)}
```

for fixed sparse cutoff `W`. Terminal unpaid primitive leaves then satisfy the
pinned moment/member-count bound.

## Proof Inputs

The assembly uses two required predicates.

```text
hankel_rank_profile_entropy:
  bounds reachable unpaid primitive saturated states by n^{O(W^2)}
  for fixed W.

hankel_moment_clean_leaves:
  gives the terminal pinned affine moment/member-count bound.
```

The support-lattice and rational-defect packets are consumed one level below
inside `hankel_rank_profile_entropy`.

## Boundary

This packet corrects earlier false starts. Raw sparse-support lattices can be
too large: the object being counted here is the saturated root-closure state,
with memoization by generated closed support sets and budget drops along
edges. The terminal member count is also pinned-affine, not unpinned
direction-dual cleanliness.

## DAG Use

`f_termination_hankel` is the Hankel-kernel branch of the broader safe-side
descent program. It supplies the Hankel-family termination piece needed by
the F/descent lane while leaving row-specific M3/M4 certificate tables to the
separate v10 Hankel packet work.

## Non-Claims

- This packet does not bound raw sparse-support branch counts.
- This packet does not remove the fixed-`W` hypothesis.
- This packet does not produce the F17^32 M3/M4 root tables.
- This packet does not edit Papers A-D.
