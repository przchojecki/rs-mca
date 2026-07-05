# Interleaved M-Handling Packet

- **Status:** PROVED / DAG assembly.
- **DAG node:** `m_handling`.
- **Certificate:** `experimental/data/certificates/m-handling/m_handling.json`.
- **Verifier:** `python3 experimental/scripts/verify_m_handling.py --check experimental/data/certificates/m-handling/m_handling.json`.

This packet records the list-side `m` convention consumed by `list_safe`.
In the refreshed prize DAG, `m_handling` is proved from three named inputs:

```text
rules_freeze
rules_m_reading
m_sweep
```

The role of this packet is to make that assembly explicit in `experimental/`
without claiming a new list-safe theorem.

## Claim

The official list challenge is read per declared constant `m`. Under that
reading, fixed-`m` packets and small-`m` batches are valid per-instance
determinations or partial determinations. The separate all-constant family
still needs uniform-in-`m` control or a large-`m` route.

Within the campaign's affordable range, `m_sweep` supplies the finite cap
coming from the existing clique-amplification bound:

```text
n >= k + m^2 (a - k)
m <= sqrt((n-k)/(a-k))
```

Near the row corridors this is the `m <= sqrt((n-k)/t) ~ 16..31` sweep recorded
in the prize DAG. Larger declared constants are not silently covered by this
packet; they remain routed through the large-`m` regularity branch.

## Evidence Boundary

- `rules_freeze` pins the ABF26 page-5 prize-box conventions.
- `rules_m_reading` pins the per-declared-constant-`m` interpretation.
- `m_sweep` uses the upstream clique-cap material:
  `experimental/scripts/verify_x1_clique_cap.py` and
  `experimental/notes/roadmaps/wp_detail/wp0_2_wp4_4_rules_freeze_and_dither.md`.

The packet is therefore a DAG assembly statement. It does not replace the L1
image-fiber or codegree inputs needed by `list_safe`.

## Consequence

List-side row packets should state their `m` scope:

```text
fixed m:        valid per-instance determination if the other row inputs close
small m batch:  creditable partial coverage over the listed constants
large m:        requires uniform-in-m or large-m regularity input
```

## Non-Claims

- This packet does not prove `list_safe`.
- This packet does not prove the L1 image-fiber theorem.
- This packet does not prove the codegree conversion.
- This packet does not cover every constant `m` by finite sweep.
