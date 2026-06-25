# M1 reserve-scale frontier audit: deeper slack targets (σ = 16, 32, 57)

- **Status:** AUDIT / CHECKABLE PARTS DONE. The bridge gates, the corrected slack-σ
  two-ended setup, and the free-dimension non-degeneracy are VERIFIED for all three
  reserve targets; the exact "≥7 retained slopes" achievability remains the open
  question (Cycle84-slot-model-dependent, not in-repo). An earlier "slope-richness
  tension makes deeper targets harder" framing was **corrected**: the reserve `σ` are
  far from the degenerate `σ≈r/2` limit, so there is no structural obstruction; small
  models are simply field/domain-capped and inconclusive (see the open-question section).
- **Agent/model:** Claude Opus 4.8 (M1-frontier audit, branch `allen/m1-strict264-audit`, PR #110).
- **Date:** 2026-06-25.
- **Targets (Przemek's frontier `site/data/frontier.json`):** beyond `strict264-min`
  (σ=8), three deeper reserve-scale targets on the same row `RS[F_17^32,H,256]`
  (`n=512, k=256, ρ=1/2`), each asking for **≥7 retained bad slopes** further below
  capacity. Independent audit; does not edit Papers A–D or any other branch.

## The reserve ladder (all verified arithmetic — `verify_m1_reserve_scale_bridge.py`)

| id | agreement `a` | `σ=a−k` | `j=n−a` | `r=j+σ` | radius `δ=(n−a)/n` | corrected jet `deg ≤ j−σ` |
|----|----|----|----|----|----|----|
| strict264-min | 264 | 8 | 248 | 256 | 31/64 | 240 |
| reserve272 | 272 | 16 | 240 | 256 | 15/32 | 224 |
| reserve288 | 288 | 32 | 224 | 256 | 7/16 | 192 |
| reserve313 | 313 | 57 | 199 | 256 | 199/512 | 142 |

The redundancy is **fixed** at `r = n−k = 256` for every target (agreement `= n−j`);
deeper targets trade co-support `j` for slack `σ`.

## What is verified (arithmetic / structural, L1-free)

1. **The bridge gate is the SAME for every agreement.** `⌊17^32 / 2^128⌋ = 6`, so
   `LD_sw(C,a) ≥ 7 ⟹ emca(C,δ) = LD_sw/17^32 ≥ 7/17^32 > 2^-128 ⟹ δ*_C ≤ δ`. The gate
   does not depend on `a`, so **seven** slopes certify the bound at *any* radius. Each
   reserve target therefore yields a progressively **stronger** (smaller) `δ*` upper
   bound: `31/64 → 15/32 → 7/16 → 199/512`, all strictly decreasing and all `≤` the
   Paper-D cap `1−ρ−2^-9 = 255/512` at `ρ=1/2`.
2. **The slack-σ two-ended setup** at each scale: `σ=a−k`, `j=n−a`, `r=j+σ=n−k=256`,
   agreement `= n−j`.
3. **The corrected two-ended jet** (per `verify_m1_strict264_two_ended_transfer.py`):
   `deg(P_J−P_J') ≤ j−σ` (top `σ−1` elementary-symmetric functions `e_1..e_{σ−1}`
   common) **+ endpoint** `P_J(0)` common. NOT `deg ≤ j−σ+1` (the off-by-one that
   frees `e_{σ−1}` and breaks the common received line). The whole strict264
   certified stack (admissibility identity, noncontainment rank certificate,
   end-to-end LD_sw transfer on a genuine RS code) transfers verbatim to each reserve
   scale — it is the *same construction* at larger `σ`, with `r` fixed.

## The open question (slot-model-dependent) — and a corrected framing

The exact **≥7 achievability** at each reserve scale is governed by the **Cycle84
seven-slot color-filtered model**, whose spec is NOT in-repo (rejected archive `#96`)
— the same boundary as strict264 and the Cycle120 numerator `N`.

**Corrected framing (`verify_m1_reserve_scale_richness.py`).** An earlier draft of
this note claimed a "reserve-scale tension": that slope-richness *collapses* as `σ`
rises, making deeper targets progressively harder. A fixed-redundancy experiment
shows that framing was **overstated**:
- **Field-independent fact:** the free dimension of a fixed-jet class is
  `free_dim = j−σ = r−2σ`, which is `0` only at the degenerate limit `σ=r/2`
  (`j=σ`, the locator forced unique). The reserve targets sit at
  `free_dim = 240, 224, 192, 142` (ratios `0.94, 0.88, 0.75, 0.55`) — all far from
  `0`. So the **degenerate-uniqueness obstruction is ruled out**; the `10→2→1→1`
  collapse cited earlier was the `σ→j` degenerate limit, which the reserve `σ` do
  **not** reach.
- **Honest negative:** the small-model richness sweep is **inconclusive** for the
  real row. Distinct slopes are values in `F_p`, so the count is field-capped
  (`≤ p ≤ 257 ≪ 17^32`), and over the tiny domains used it collapses to `1` while
  `free_dim` is still `> 0` — a field/domain artifact, not a structural law. A
  `512`-point smooth domain over `F_{17^32}` is far beyond what is enumerable here.

**Net:** the reserve targets are **not** structurally degenerate (free dimension is
ample), but neither the small model nor any in-repo computation can establish or
refute the exact `≥7`; that remains **Cycle84-slot-model-dependent**. This audit
certifies the gate + setup, rules out the degenerate obstruction, and flags the
count — it does **not** assert achievability.

## Next audit steps

- The checkable parts are done (gate, setup, corrected jet, free-dimension
  non-degeneracy). The exact `≥7` count stays flagged as Cycle84-slot-model-dependent
  (not in-repo). Remaining moves: audit the `strict264-2187` candidate's `2187=3^7`
  shape if the slot spec ever lands, or pivot.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_reserve_scale_bridge.py
python3 experimental/scripts/verify_m1_reserve_scale_richness.py
# shared strict264 stack (the construction is identical at larger sigma):
python3 experimental/scripts/verify_m1_strict264_two_ended_transfer.py
python3 experimental/scripts/verify_m1_strict264_end_to_end.py
```
