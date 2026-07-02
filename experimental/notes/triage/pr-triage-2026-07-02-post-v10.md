# PR triage: post-v10 roadmap and Hankel packets

Date: 2026-07-02

Agent/model: Codex

Scope: open PRs #170--#174 after the then-current Paper D v10 package.

## Summary

No PR in this batch moves the public leaderboard or proves a new prize-facing
threshold.  The useful material is proof infrastructure:

- #170 supplies a synthetic low-rank M3/M4 subpacket and a spectral reduction.
- #171 is a very large generated rank-witness packet; only the compact M0
  definition freeze and checker hardening are suitable for main at this stage.
- #172 supplies the first M5 underdetermined-boundary packet at `A=384`.
- #173 supplies two M1 reductions: a simple-pole projected locator wall and a
  dyadic shifted-prefix value bridge.
- #174 supplies a subordinate r2 roadmap/DAG.  Its main correction is that the
  official prize band is entirely underdetermined, so the regular M3 window is
  a proving ground rather than the direct band-facing method.

## Integration decisions

### PR #170 — synthetic low-rank M3/M4 packet

Decision: integrate, with narrow scope.

Integrated files:

```text
experimental/notes/m3/m3_low_rank_affine_spectral_reduction.md
experimental/data/certificates/hankel-f17-32-m3-endpoint-c2-capacity/
experimental/data/certificates/hankel-f17-32-m3-low-rank-spectral-frontier/
experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image/
experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-paid-residual-ledger/
experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-v10-affine-gcd/
experimental/scripts/verify_f17_32_m3_endpoint_c2_capacity.py
experimental/scripts/verify_f17_32_m3_low_rank2_12_endpoint_quotient_image.py
experimental/scripts/verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py
experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py
experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py
```

Static audit:

- The determinant-lemma reduction in
  `experimental/notes/m3/m3_low_rank_affine_spectral_reduction.md` is a
  standard matrix-determinant-lemma/Cauchy-Binet argument.
- The packet READMEs consistently say `synthetic low-rank ladder` and do not
  claim an arbitrary-row M3 theorem.
- The spectral-frontier JSON is explicitly `EXPERIMENTAL / AUDIT`.

Local replay note:

- Lightweight endpoint and paid-residual checks were run during triage.
- The affine-gcd replay is compute-heavy and was not completed locally; do not
  treat the checked-in JSON as independently replayed by this integration.

### PR #171 — rank-witness endpoint mega-packet

Decision: split/hold, with two compact extracts.

Integrated extracts:

```text
experimental/notes/audits/m0_prize_mca_definition_freeze.md
scripts/check_aperiodic_eliminant_packet.py
```

Rationale:

- The M0 freeze is a useful audit note and matches the `towards-prize.md`
  milestone structure.
- The checker update adds `regular_minor_gcd` support for v10-style packets.
- The rest of #171 adds more than 100k generated lines and many rank-6 sidecar
  claims.  Those need smaller PRs, independent replay notes, and a compressed
  synthesis before integration.

### PR #172 — M5 underdetermined A=384 boundary

Decision: integrate.

Integrated files:

```text
experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md
experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
```

Status:

- `ACTIVE / EXPERIMENTAL`.
- The note makes no threshold or safety claim.
- Its value is that it identifies the first underdetermined boundary
  `A=384`, where the regular Hankel root-containment certificate becomes
  structurally vacuous.

### PR #173 — M1 simple-pole and dyadic value reductions

Decision: integrate.

Integrated files:

```text
experimental/notes/m1/m1_simple_pole_projected_locator_wall.md
experimental/notes/m1/m1_dyadic_shifted_prefix_value_bridge.md
```

Status:

- `PROVED REDUCTION / ROUTE CUT / OPEN WALL` for the simple-pole projected
  locator wall.
- `PROVED local bridge / REPAIR / AUDIT` for the shifted-prefix value bridge.

These are useful theory reductions, not prize solves.

### PR #174 — roadmap r2 and prize DAG

Decision: integrate as subordinate planning material.

Integrated files:

```text
experimental/notes/roadmaps/proximity_prize_execution_roadmap_post_v10_r2.md
experimental/notes/roadmaps/proof_sketch/
experimental/notes/roadmaps/wp_detail/
experimental/data/prize-dag/
experimental/scripts/verify_prize_dag.py
experimental/scripts/verify_roadmap_r2_numbers.py
experimental/scripts/plot_prize_dag.py
```

Status:

- `AUDIT / proposed working roadmap`.
- `towards-prize.md` remains the maintainer source of truth.

The main adopted correction is that the official prize band lies entirely
below the regular overdetermined Hankel range, so the M5 underdetermined chart
program is on the critical path.

## Leaderboard impact

No new leaderboard entry should be added from this batch.  The PRs add
methodology and audits, not a new verified threshold, numerator, safe-side
upper bound, or public prize-facing row.
