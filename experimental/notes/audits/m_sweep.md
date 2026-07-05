# M-Sweep Packet

- **Status:** PROVED / DAG assembly from `clique_cap`.
- **DAG node:** `m_sweep`.
- **Certificate:** `experimental/data/certificates/m-sweep/m_sweep.json`.
- **Verifier:** `python3 experimental/scripts/verify_m_sweep.py --check experimental/data/certificates/m-sweep/m_sweep.json`.

This packet names the finite interleaving-arity sweep used by the list-side
`m_handling` node.

## Claim

The `clique_cap` node gives

```text
n >= k + m^2(a-k).
```

Writing `t = a-k`, every `K_{m,m}` clique-amplification route in a row with
domain size `n`, dimension `k`, and over-agreement slack `t` must satisfy

```text
m <= floor(sqrt((n-k)/t)).
```

The prize DAG records the relevant near-corridor sweep as approximately

```text
m <= sqrt((n-k)/t) ~ 16..31.
```

That is the affordable finite range consumed by `m_handling`; constants outside
that range remain routed through a uniform-in-`m` or large-`m` regularity input.

## Evidence Boundary

This packet is an arithmetic consequence of `clique_cap`, not an independent
list-size theorem. It uses the same list-side bookkeeping as
`experimental/notes/roadmaps/wp_detail/wp0_2_wp4_4_rules_freeze_and_dither.md`
and the clique-cap witness verifier
`experimental/scripts/verify_x1_clique_cap.py`.

## DAG Consequence

`m_sweep` supplies the finite-sweep input to `m_handling` and `list_safe`.
It does not close the L1 image-fiber or codegree predicates.

## Non-Claims

- This packet does not cover arbitrary constant `m` uniformly.
- This packet does not prove `list_safe`.
- This packet does not provide the large-`m` regularity branch.
