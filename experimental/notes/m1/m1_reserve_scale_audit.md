# M1 reserve-scale frontier audit: deeper slack targets (σ = 16, 32, 57)

- **Status:** AUDIT / IN PROGRESS. The bridge gates and the corrected slack-σ
  two-ended setup are VERIFIED for all three reserve targets; the "≥7 retained
  slopes" achievability is the open audit question (slot-model-dependent, with an
  added slope-richness tension that makes deeper targets progressively harder).
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

## The open question (slot-model-dependent + a real tension)

The exact **≥7 achievability** at each reserve scale is governed by the **Cycle84
seven-slot color-filtered model**, whose spec is NOT in-repo (rejected archive `#96`)
— the same boundary as strict264 and the Cycle120 numerator `N`.

**Reserve-scale tension (new, and the reason these are nontrivial):** the per-line
slope-richness *collapses* as slack `σ` rises (verified small-model trend,
`verify_m1_strict264_admissibility.py` slope-richness table and
`verify_m1_strict264_mechanism.py` `10→2→1→1`). So the deeper targets are
progressively **harder**: whether `≥7` distinct retained slopes survive at `σ=16`,
`32`, `57` is exactly what this audit isolates. This audit does **not** assert
achievability; it certifies the gate + setup and flags the count.

## Next audit steps

- Characterize the small-model slope-richness scaling at **fixed redundancy** `r`
  (so `j=r−σ`), as `σ` grows toward `r/2` and beyond, to give a plausibility read on
  whether `≥7` can survive at each reserve `σ` (subject to field/domain size). The
  real row has a huge field `17^32`, so the binding constraint is the slot structure,
  not the field — flag accordingly.
- Keep the exact `≥7` count flagged as Cycle84-slot-model-dependent.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_reserve_scale_bridge.py
# shared strict264 stack (the construction is identical at larger sigma):
python3 experimental/scripts/verify_m1_strict264_two_ended_transfer.py
python3 experimental/scripts/verify_m1_strict264_end_to_end.py
```
