# Audit: the Cycle120/Cycle119 prize gate is UNCONDITIONAL via the tangent floor

- **Status:** AUDIT / VERIFIED. Independent audit of the M1 prize-gate dependency.
- **Agent/model:** Claude Opus 4.8 (1M context), branch `allen/prize-gate-unconditional`.
- **Date:** 2026-06-26.
- **Verifier:** `experimental/scripts/verify_m1_tangent_floor_gate_ladder.py` (PASS).
- **Scope:** independent audit only. Does not edit the M1 audit notes
  (`audit_pr100_cycle120_gate.md`, `audit_pr105_cycle120_standalone.md`) or Papers A–D;
  proposes a board nonclaims refinement for `cycle116`/`cycle119` and flags the M1 owners.

## Finding

The prize-facing negative counterexample for `C = RS[F_17^32, H, 256]` —

```
emca(C, 125/256) > 2^-128   (a=262, Cycle120),   and the strict
delta*_C <= 249/512          (a=263, Cycle119)
```

— is recorded **conditional** on the unreproduced **Cycle84 census**
`N = 52,747,567,092` (see `audit_pr100_cycle120_gate.md`: "arithmetic VERIFIED, result
CONDITIONAL on finite imports"). That conditionality is **not needed for the threshold**.

The proved **moving-root tangent floor** (`experimental/data/tangent/tangent_staircase_section.tex`,
Thm "moving-root tangent floor" — an elementary MDS argument, no smoothness, no Cycle84,
no slot model) states

```
LD_sw(C, a) >= n - a + 1   for every  k+1 <= a <= n.
```

With the M2 bridge `emca(C, delta) = LD_sw(C, ceil((1-delta)n))/q` and the gate
`emca > 2^-128  <=>  LD_sw >= 7` (since `floor(17^32/2^128) = 6`):

| claim | a | tangent floor `LD_sw >=` | gate |
|---|---|---|---|
| Cycle120 `emca(C,125/256) > 2^-128` | 262 | **251** | clears (251 ≥ 7) |
| Cycle119 `delta*_C <= 249/512` | 263 | **250** | clears (250 ≥ 7) |

So both **thresholds are unconditional**. The Cycle84 census `N` is required only for the
**exact density** (`~2^-95.18`) and the exact slope count — *not* for clearing `2^-128`.

## Why this is sound (I read the proof)

The tangent floor fixes a locator `B_A` for `a-1` points of `D` and moves one root
`t in D\A`: each `t` gives a slope explained on `A∪{t}` (size `a`), and the explanation is
support-wise **noncontained** because `g` already equals `(B_A)_{<k}` on `A`, and forcing
it at `t` would make `B_A(t)=0`, impossible for `t∉A`. The `n-a+1` slopes are distinct.
This is exactly the finite-slope support-wise object the Cycle120/Cycle119 gate uses, on
the same row. The gate arithmetic (`6·2^128 < 17^32 < 7·2^128`) is checked exactly in the
verifier.

## What this does NOT establish (stays open / Cycle84-dependent)

- The exact count `N = 52,747,567,092` and the resulting **exact density `~2^-95.18`**.
- The exact threshold `delta*_C` (the tangent floor gives only `<=`; the matching
  upper side at the high-agreement end is the separate tangent-star barrier).
- These remain as recorded in the M1 audit notes.

## Recommended actions

- **Board (`site/data/frontier.json`, this PR):** refine the `cycle116` / `cycle119`
  `nonclaims`/`proof` to record that the `> 2^-128` gate is unconditional via the tangent
  floor, with the Cycle84 import scoped to the exact density. (Done in this PR.)
- **M1 audit notes (Codex/Danny — NOT edited here):** their headers may be downgraded from
  "result CONDITIONAL" to "gate PROVED unconditionally (tangent floor); exact density
  conditional on `N`." Flagged for the owners.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_tangent_floor_gate_ladder.py
python3 experimental/data/tangent/verify_tangent_staircase.py
```
