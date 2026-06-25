# M1 strict264 audit: pushing the Cycle120 obstruction to agreement 264

- **Status:** AUDIT / IN PROGRESS. The M2-bridge arithmetic and the slack-8
  two-ended setup are VERIFIED; the "≥7 retained slopes" count is the open audit
  target (and depends on the Cycle84 slot model, not in-repo).
- **Agent/model:** Claude Opus 4.8 (M1-frontier audit, branch `allen/m1-strict264-audit`).
- **Date:** 2026-06-25.
- **Target (Przemek's frontier site, `site/data/frontier.json` id `strict264-min`):**
  for the row `C = RS[F_17^32, H, 256]` (`n=512`, `k=256`, `ρ=1/2`), *"find or
  audit at least seven retained bad slopes at agreement 264."* Independent audit;
  does not edit Papers A–D or any other branch.

## Why agreement 264, and why "seven"

By the integrated **M2 bridge** (`m2_line_decoding_mca_bridge.md`),
`emca(C,δ) = LD_sw(C, ⌈(1−δ)n⌉)/|F|`. At agreement `264 = ⌈(1−δ)·512⌉` the radius
is `δ = 1 − 264/512 = 31/64 = 0.484375`. The denominator gate:
```
⌊17^32 / 2^128⌋ = 6,     so   LD_sw(C,264) ≥ 7  ⟹  emca(C,31/64) = 7/17^32 > 2^-128.
```
Hence **seven** retained bad slopes at agreement 264 already certify
`emca(C,31/64) > 2^-128`, i.e.
```
δ*_C ≤ 31/64 = 248/512  <  249/512   (the Cycle119 endpoint).
```
So strict264 is a *strict strengthening* of the Cycle119 (agreement-263) endpoint.
(All arithmetic verified: `verify_m1_strict264_bridge.py`.)

## The construction this extends

Cycle119 (agreement 263) uses the **two-ended fixed-jet locator** with
`n=512, j=249, σ=7, r=j+σ=256=n−k`, agreement `= n−j = 263`, and `≥ N =
52,747,567,092` bad slopes. Strict264 is the **same construction one rung
deeper**:
```
agreement 264  ⟹  j = n − 264 = 248,   σ = n − k − j = 8,   r = j+σ = 256.
```
So strict264 = the two-ended fixed-jet locator at **slack σ = 8** (one more fixed
top coefficient than Cycle119). More slack ⟹ more prefix constraints ⟹ a smaller
surviving co-support family ⟹ fewer bad slopes: the count drops from `N ~ 5·10^10`
at `σ=7` toward the **`O(1)` retained set** at `σ=8`. The `strict264-2187`
candidate (`badSlopes = 2187 = 3^7`) suggests a ternary choice over the 7
Cycle84 slots; the `≥7` minimal target is the conservative survivor count.

## Audit plan (what is checkable here vs what needs the slot model)

1. **M2-bridge + slack-8 setup arithmetic — DONE** (`verify_m1_strict264_bridge.py`):
   `δ=31/64`, `⌊17^32/2^128⌋=6`, `7/17^32 > 2^-128`, `δ*≤31/64<249/512`;
   `(j,σ,r) = (248,8,256)`, agreement `= n−j = 264`, `r = n−k`.
2. **The retained-slope MECHANISM (small-model, L1-free) — DONE**
   (`verify_m1_strict264_mechanism.py`). Full enumeration on a smooth domain
   (`F_17`, order-8 `D`, `j=4`, `β` a non-`D` point) confirms the two-ended
   fixed-jet count `#{distinct P_J(β)}` (over `j`-subsets `J` with top `σ-1`
   coefficients + endpoint `P_J(0)` fixed) is **non-increasing in `σ`** and
   reaches `1` when the locator is fully constrained:
   ```
   σ:                1    2    3    4(=j)
   retained slopes: 10    2    1    1
   ```
   This is exactly why agreement `264` (`σ=8`) retains only a *few* slopes where
   agreement `262/263` (`σ=6/7`) retains the full `N`: each extra slack rung adds
   a fixed coefficient and shrinks the admissible co-support family. The
   construction's algebra (`z_J = -1/P_J(β)`, `β∉D ⟹ P_J(β)≠0`, distinct
   `P_J(β) ↔` distinct slope) is checked. The *exact* survivor count at `σ=8`
   for the real row is governed by how the 8 constraints meet the 7-slot Cycle84
   combinatorics — see item 3.
3. **The σ=8 two-ended ADMISSIBILITY (small-model, L1-free) — DONE**
   (`verify_m1_strict264_admissibility.py`). Full enumeration (`F_97`, order-16
   `D`, `β` a non-`D` point, `j=5`, `σ=3`) verifies the construction's core algebra:
   * **The common parity-check identity** `ℓ(P_J·A) = A(β)` for every `J` and every
     `A` with `deg A < σ`, where `ℓ` is the *two-ended triangular recovery*: the
     endpoint coefficient `[X^0](P_J A) = c·a_0` recovers `a_0`, and the top
     selected coefficients `[X^{j+t}](P_J A) = a_t + Σ_{i>t}(-1)^{i-t}e_{i-t}a_i`
     (`t=1..σ-1`) back-substitute `a_{σ-1},…,a_1`. Diagonal `(c,1,…,1)` ⟹ invertible
     (needs only `c≠0` — the nonzero endpoint).
   * **`ℓ` is common across a fixed-jet class:** it uses only the shared
     `(e_1..e_{σ-1}, c, β)`, so one `ℓ` serves every `J` in the class. Verified on
     all 64 multi-member classes — the *same* `ℓ` recovers `A(β)` from every member,
     and the bad slopes `z_J = -1/P_J(β)` are distinct across the class.
   * **σ=8 structural consistency:** `deg(P_J−P_J') ≤ j−σ+1 = 241`, selected degrees
     `{0,249,…,255}` (exactly `σ=8` of them), `j+1 = 249 ≤ r = 256` (noncontainment).
   The construction is therefore admissible at the deployed `(j,σ,r)=(248,8,256)`.
4. **Survivor combinatorics — PARTIAL (checkable part DONE; exact count NOT).**
   The *per-line* image of the count drop is verified
   (`verify_m1_strict264_admissibility.py`, slope-richness table): at fixed `(p,m,j)`
   the maximum number of distinct slopes one common line can carry **collapses** as
   slack `σ` rises by one — e.g. `(193,32,5)`: `σ=2 → 44` slopes, `σ=3 → 3`. This is
   the per-line shadow of the global `~5·10^10` (σ=7) `→` `O(1)` (σ=8) drop. The
   **exact count ≥7 / `2187 = 3^7`** at the deployed parameters depends on the
   **Cycle84 seven-slot color-filtered model**, whose spec is NOT in-repo (rejected
   archive `#96`). So the exact "7" (or `2187`) cannot be recomputed here from first
   principles; this audit certifies the mechanism + admissibility and flags the count
   as slot-model-dependent (same honest boundary as the Cycle120 numerator `N`).

## Honest scope
- **VERIFIED (arithmetic):** the M2-bridge gate (7 slopes ⟹ `>2^-128`, `δ*≤31/64`)
  and the slack-8 two-ended parameters `(j,σ,r)=(248,8,256)`.
- **VERIFIED (mechanism, small-model):** the retained-slope count drops with slack
  (`10→2→1→1`, `verify_m1_strict264_mechanism.py`) and its per-line image — slope
  richness collapses `σ=2 → σ=3` (`verify_m1_strict264_admissibility.py`).
- **VERIFIED (admissibility, small-model):** the σ=8 two-ended construction's algebra
  — common parity-check identity `ℓ(P_J·A)=A(β)`, invertible triangular recovery,
  one common `ℓ` per fixed-jet class with distinct slopes, and the σ=8 degree /
  endpoint / noncontainment constraints (`verify_m1_strict264_admissibility.py`).
- **OUT OF SCOPE (needs the rejected-archive slot spec):** the exact survivor count
  `≥7` / `2187` for the actual `F_17^32` row — slot-model-dependent.

## Audit verdict (interim)
The strict264 obstruction is **structurally sound and admissible**: every checkable
layer — the bridge arithmetic, the slack-8 parameters, the retained-slope drop
mechanism, and the two-ended common-`ℓ` construction at `(248,8,256)` — passes
independent verification. The single remaining gap is the *exact* survivor count
`≥7`, which is governed by the Cycle84 7-slot model not present in the repo. The
audit neither confirms nor refutes the precise "7"; it certifies everything around
it and isolates the one slot-model-dependent number.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_strict264_bridge.py
python3 experimental/scripts/verify_m1_strict264_mechanism.py
python3 experimental/scripts/verify_m1_strict264_admissibility.py
```
