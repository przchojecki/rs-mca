# Cross-lane observation: the M1 reserve frontier meets L1's reserve at σ ~ n/log n

- **Status:** AUDIT / VERIFIED ARITHMETIC + flagged HEURISTIC. Cross-lane note.
- **Agent/model:** Claude Opus 4.8 (independent audit, branch `allen/l1-audit`).
- **Date:** 2026-06-26.
- **Verifier:** `experimental/scripts/verify_l1_m1_reserve_connection.py`.

## Verified arithmetic

For the M1 row `RS[F_17^32,H,256]` (`n=512`, `k=256`, `q=17^32`), the frontier
targets sit at slack `σ = a−k`, and `n/log₂(n) = 512/9 = 56.9`:

| target | a | σ | σ / (n/log₂ n) | σ·log₂q | log₂ C(n,s) |
|---|---|---|---|---|---|
| strict264 | 264 | 8 | 0.14 | 1046 | 507 |
| reserve272 | 272 | 16 | 0.28 | 2093 | 506 |
| reserve288 | 288 | 32 | 0.56 | 4186 | 501 |
| **reserve313** | 313 | **57** | **1.00** | 7455 | 489 |

L1 Conjecture 1 (`l1_full_list_quotient_proof_program.md`) holds **above the reserve**
`σ ≥ C·n/log n` and `σ·log₂q ≥ (1+ε)·log₂ C(n,s)`. So:
- **`reserve313` (σ=57) sits exactly at the L1 `n/log n` lower cutoff** — the frontier
  even names it the "n/log n scale" target. The other three targets are below it.
- The entropy reserve `σ·log₂q ≥ (1+ε)log₂C(n,s)` clears with huge margin at every
  target because `q=17^32` is enormous; the **binding** reserve is the `n/log n` cutoff.

So the four M1 frontier targets deliberately sweep `σ` from deep below the reserve
(`strict264`) up to the L1 reserve boundary (`reserve313`).

## Heuristic interpretation (flagged — an observation, not a claim)

The M1 obstruction is a **line**-decoding (`LD_sw`) phenomenon while L1 is single-word
list decoding, so this is a structural coincidence at the threshold, not a rigorous
implication. But it is suggestive: **if** L1's aperiodic bound `Q_1^list ≤ n^B` holds
above the reserve, then at/above `σ ~ n/log n` the retained high-agreement mass must be
**quotient-periodic** (charged to `Σ_{d>1} Q_d`), not aperiodic — consistent with the
**Cycle84 slot model** being an inherently periodic/coset structure (`badSlopes = 2187 =
3^7` is slot combinatorics). The M1 reserve frontier and L1's quotient/aperiodic split
thus appear to **meet at the same `n/log n` threshold**.

This unifies two lanes' reserve notions and suggests why `reserve313` is placed exactly
there. It is a direction to pursue (does the retained-slope structure provably transition
to quotient-periodic at `σ ~ n/log n`?), not a proven statement.

## Small-model evidence (supports the heuristic)

`verify_m1_cosupport_periodicity.py` tests the transition directly on a smooth domain
(`D` = order-16 subgroup of `F_97`, `β∉D`, `j=8`; small-model cutoff `m/log₂m = 4`). For
the two-ended fixed-jet construction it classifies each retained co-support `J` (slope
`z_J=-1/P_J(β)`, agreement set `D\J`) by its multiplicative stabilizer
`Stab(J)={h∈D:hJ=J}` — aperiodic (`|Stab|=1`, the L1 `Q_1` analogue) vs quotient-periodic
(`|Stab|>1`, the `Q_{d>1}` analogue):

| σ | ≥ cutoff(4)? | retained | aperiodic `Q_1` | periodic `Q_{d>1}` |
|---|---|---|---|---|
| 1 | no | 96 | **96** | 0 |
| 2 | no | 16 | 16 | 0 |
| 3 | no | 3 | 3 | 0 |
| 4 | **yes** | 2 | **0** | 2 (frac 1.0) |
| 5–8 | yes | 1 | 1 | 0 |

The transition matches the heuristic: **below** the `n/log n` cutoff the aperiodic
retained count is large (`96` at `σ=1`, the regime where the M1 `LD_sw` counterexample
lives); **at** the cutoff (`σ=4`) the retained mass is *entirely quotient-periodic*; and
**above** it the aperiodic count collapses to `≤1`. So `max aperiodic` drops `96 → 1`
across the cutoff. This is **supporting evidence**, not a proof — the model is small
(`m=16`, crude cutoff), and the M1 (`LD_sw`, line) vs L1 (single-word) object mismatch
still means this is a structural coincidence at the threshold, suggestive of a real
mechanism worth a proper proof.

## Reproducibility
```bash
python3 experimental/scripts/verify_l1_m1_reserve_connection.py
python3 experimental/scripts/verify_m1_cosupport_periodicity.py
```
