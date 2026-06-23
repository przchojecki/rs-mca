# M1 Cycle84 Exact Occupancy Chain

Status: AUDIT / FINITE-MODEL-EXACT-OCCUPANCY-CHAIN / CONDITIONAL.

Date: 2026-06-24.

This note records the end-to-end finite-model chain that turns the Cycle84
projected replay into the exact product occupancy used by the Cycle116 and
Cycle120 M1 audit.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py
```

## Inputs

The chain consumes four local finite checks:

```text
verify_m1_cycle84_color_collision_witnesses.py
verify_m1_cycle84_projected_log_certificate.py
verify_m1_cycle84_projected_full_replay_receipt.py
verify_m1_cycle84_kernel_lift_candidates.py
```

The full replay receipt says that the projected tau-folded census over the
current `slot_logs.json` covered all `16,384` shards and found:

```text
oriented half-domain entries = 26,373,783,552,
projected duplicate bins    = 30,
folded projected energy     = 60,
max projected multiplicity  = 2.
```

The color-shell verifier gives:

```text
color shell size = 52,747,567,104.
```

The kernel-lift verifier checks the `30` projected duplicate bins against the
current normalized slot table and finds:

```text
projected bins checked        = 30,
normalized witnesses checked  = 60,
true tau collision orbits     = 6,
true double fibers after tau  = 12,
true ordered energy after tau = 24.
```

## Consequence

Every true product collision has equal full log, hence equal projected log.
Therefore it lies in one of the fully replayed projected duplicate bins. Since
the full projected replay has max projected multiplicity `2`, every true product
fiber has size at most `2`.

The kernel-lift verifier checks all projected duplicate bins and identifies
exactly six true collision orbits in the oriented half-domain. Applying tau gives
twelve true double fibers on the full color shell. Hence the exact ordered
off-diagonal product energy is

```text
D = 12 * 2 = 24.
```

Since all nontrivial fibers are double fibers, the number of distinct products is

```text
52,747,567,104 - 12 = 52,747,567,092.
```

Thus the exact Cycle84 finite-model conclusion is:

```text
#{Phi(T)} = 52,747,567,092,
m_max(beta) = 2,
D = 24,
no fibers of size >= 3.
```

The remaining finite-audit boundary is human review that the generated C++
replay source follows the algorithm audited in
`m1_cycle84_projected_replay_algorithm_audit.md`. The ABF source-gate question is
outside this finite-model note.
