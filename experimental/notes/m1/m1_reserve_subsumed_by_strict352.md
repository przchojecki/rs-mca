# M1 frontier-board reserve targets are subsumed by strict352

- **Status:** RESOLVED / VERIFIED (arithmetic subsumption). The three board reserve
  targets `reserve272`, `reserve288`, `reserve313` are **closed** by Codex's strict352
  quotient-core floor. Their only open piece (exact "≥7 achievability") is now proved,
  in-repo, by a different route than the one I was auditing.
- **Agent/model:** Claude Opus 4.8 (independent M1 audit, branch `allen/m1-reserve-subsumption`).
- **Date:** 2026-06-26.
- **Verifier:** `experimental/scripts/verify_m1_reserve_subsumed_by_strict352.py` (PASS, 17/17).
- **Supersedes the open question in:** `experimental/notes/m1/m1_reserve_scale_audit.md`.

## What the reserve targets asked for

`site/data/frontier.json` posts three reserve-scale **targets** (status `"target"`),
all on the single smooth rate-1/2 row `C = RS[F_17^32, H, 256]` (`n=512, k=256,
|H|=512, q=17^32`), each asking for **≥ 7 retained support-wise bad slopes** deeper
below capacity:

| id | a | σ=a−k | board radius δ | needed slopes |
|----|---|---|---|---|
| reserve272 | 272 | 16 | 15/32 | 7 |
| reserve288 | 288 | 32 | 7/16 | 7 |
| reserve313 | 313 | 57 | 199/512 | 7 |

My earlier audit (`m1_reserve_scale_audit.md`) certified the bridge gate, the slack-σ
two-ended setup, and free-dimension non-degeneracy, but explicitly **left the exact
"≥7 achievability" open** ("Cycle84-slot-model-dependent, not in-repo").

## Why strict352 closes them

Codex's strict352 result (`experimental/data/strict352/strict352_quotient_core_summary.md`,
canonical counts in `strict352_quotient_core_output.txt`) proves, by an **in-repo dyadic
quotient-core construction** (`x → x^c`, `c ∈ {4,8,16,32}`; quotient-prefix pigeonholing;
deep-point conversion) — **no Cycle84 slot model required** — on the **same row**, under
the **same** finite-slope support-wise MCA convention:

```
LD_sw(C, a) >= 7   for every  264 <= a <= 352,    and    LD_sw(C, 352) >= 16,
```

producing **distinct support-wise MCA-bad slopes** — exactly the object the reserve rows
count. The three reserve agreements are interior to `[264, 352]`, and the proved
per-agreement floor `M(a)` clears the requirement with enormous margin:

| id | a | proved floor `M(a)` | ≥ 7? | gate `M(a)·2^128 > 17^32`? | δ = (n−a)/n matches board? |
|----|---|---|---|---|---|
| reserve272 | 272 | 19,399,767,849,168 | ✓ | ✓ | ✓ (15/32) |
| reserve288 | 288 | 1,631,266 | ✓ | ✓ | ✓ (7/16) |
| reserve313 | 313 | 295 | ✓ | ✓ | ✓ (199/512) |

The **bridge gate** is identical on both sides: `⌊17^32 / 2^128⌋ = 6`, so `≥7` is the
exact bar (`6·2^128 < 17^32 < 7·2^128`), and `emca(C,δ) = LD_sw/q > 2^-128`. The minimum
proved floor over the whole range `[264, 352]` is `M = 11` (the `c=32` rows
`a = 321..351`), so every agreement in range — not just the three named targets — clears
`≥7`.

**Non-vacuity.** The live frontier `a = 353` is **not** covered (`M(353) = 3 < 7`), so
the three reserve targets sit strictly inside the proved range, just below the wall. The
subsumption is not an artifact of an over-wide claim.

## Scope / honest caveats

- This is an **arithmetic subsumption** of the three **board rows**: it confirms the
  strict352 *theorem* (taken as proved upstream; its own proof + verifier live in
  `experimental/data/strict352/`) covers exactly what the reserve *targets* requested.
  It does **not** re-prove the quotient-core construction.
- "Reserve" is **overloaded** in the repo. The three subsumed objects are the **M1
  frontier-board search targets**. They are **not** the Paper-C *field-separated
  proximity reserve certificate* (`experimental/data/schemas/reserve_certificate_schema.json`,
  `tex/snarks_v4.tex` `def:cert`/`rule:reserve`), which is a much richer multi-budget
  object (separated `q_arith/q_gen/q_line`, entropy + quotient-profile + list + MCA
  budgets, extension status). That Paper-C lane is **untouched** by this finding.

## Recommended board update (proposal only — not applied)

`site/data/frontier.json` still lists `reserve272/288/313` as `status:"target"`. On the
strength of strict352 they should move to `status:"proved"` (or be folded into the
strict352 record, which already spans `264 ≤ a ≤ 352`). This edits Przemek's board data,
so it is left as a **proposal** for the maintainer, not applied here.

## Consequence for my plan

The M1 reserve lane is **retired** (closed, not abandoned). The live M1 frontier is
`a = 353 / slack 97 / δ = 159/512`, where the coarse dyadic method yields only 3 slopes.
Next audit moves target that wall (residual-depth frontier partition: quotient-periodic
/ tangent / aperiodic branches) rather than the now-closed reserve targets.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_reserve_subsumed_by_strict352.py
# upstream proof of the strict352 floor it relies on:
python3 experimental/data/strict352/verify_strict352_quotient_core.py
```
