# Clique-Cap Packet

- **Status:** PROVED / combinatorial cap.
- **DAG node:** `clique_cap`.
- **Certificate:** `experimental/data/certificates/clique-cap/clique_cap.json`.
- **Verifier:** `python3 experimental/scripts/verify_clique_cap_packet.py --check experimental/data/certificates/clique-cap/clique_cap.json`.

This packet names the `K_{m,m}` clique-amplification cap used by the list-side
`m_sweep` and `m_handling` nodes.

## Claim

In the two-sided over-agreement design, let `T` be the common `k`-set and let
each of the `m^2` cross cells require at least `a-k` non-`T` points. The cells
are disjoint outside `T`, so any such `K_{m,m}` clique requires

```text
n >= k + m^2 (a-k).
```

Equivalently, this construction can only amplify to `m^2` when

```text
m^2 <= (n-k)/(a-k).
```

## Evidence

The existing upstream verifier
`experimental/scripts/verify_x1_clique_cap.py` constructs abstract grid
designs for `m = 2,3,4`, checks all cross overlaps and support sizes, and
cross-checks the `m = 2` case against a field-realized witness.

The packet certificate records the formula and the sample design arithmetic:

```text
(m,a,k) = (2,8,4) -> n = 20, edges = 4
(m,a,k) = (3,8,4) -> n = 40, edges = 9
(m,a,k) = (4,8,4) -> n = 68, edges = 16
```

## DAG Consequence

This is the parent cap for `m_sweep`. It is not itself a list-size theorem; it
only bounds the known clique-amplification geometry.

## Non-Claims

- This packet does not prove `list_safe`.
- This packet does not prove an L1 image-fiber bound.
- This packet does not rule out all possible interleaved-list amplification
  mechanisms, only the `K_{m,m}` clique family named here.
