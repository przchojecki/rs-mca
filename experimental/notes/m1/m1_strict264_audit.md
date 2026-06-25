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
   * **Support-wise noncontainment — actual rank certificate (not just `j+1≤r`):**
     for every `J`, the `r×(j+1)` Vandermonde with nodes `J∪{β}` (rows = degrees
     `0..r−1`) has full column rank `j+1` (Gaussian elimination mod `p`, 128 `J`
     tested). I.e. the `β`-column is *not* in the span of the `j` columns at `J`, so
     `g` cannot be re-explained on `D\J` and the retained codewords are genuinely
     distinct. The contrast at `r'=j<j+1` (β-column dependent) confirms `r≥j+1` is
     essential.
   * **σ=8 structural consistency:** `deg(P_J−P_J') ≤ j−σ = 240` (the top `σ−1 = 7`
     elementary-symmetric functions `e_1..e_7` common — the verifier groups by
     `(e_1..e_{σ−1}, e_j)`, the valid reading), selected degrees `{0,249,…,255}`
     (exactly `σ=8` of them), `j+1 = 249 ≤ r = 256` (noncontainment).
     **Correction:** earlier drafts (and the candidate note, lines 286–287) wrote
     `deg ≤ j−σ+1 = 241`; that is an **off-by-one** — it frees `e_{σ−1}` and breaks
     the common line (see item 6). The admissibility enumeration above already used
     the correct grouping, so the result is unaffected.
   The construction is therefore admissible at the deployed `(j,σ,r)=(248,8,256)`,
   **with the corrected degree condition `deg ≤ 240` (top `σ−1` common) + endpoint**.
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
5. **END-TO-END LD_sw realization on a genuine RS code — DONE**
   (`verify_m1_strict264_end_to_end.py`). The previous items verify the locator
   *algebra* in isolation; this item ties it to **actual retained codewords** of a
   real Reed–Solomon code, reproducing the standalone-proof transfer
   (`m1_cycle120_standalone_ldsw_proof.md`, Lemma 1):
   `LD_sw(RS[F,D,k], n−j) ≥ #{P_J(β):J}`. On `RS[F_97, D, 10]` (`n=16, k=10, j=4,
   σ=2`, redundancy `6=n−k`, `β∉D`), full enumeration of a fixed-jet class (size 4)
   verifies the entire pipeline: (a) the parity check `(Hw)_m=Σ_x xᵐw(x)/L_D'(x)` has
   `kernel = RS[F,D,k]` (rank `j+σ`, deg-`<k` evals in kernel); (b) the quotient
   `Q_m` is common across the class (one received line); (c) `Hg=B` and
   `He_J=A+z_J B` with `z_J=1/P_J(β)`; (d) `c_J=f+z_J g−e_J` is a genuine codeword
   (`Hc_J=0` **and** it is the evaluation of a deg-`<k` polynomial); (e) the line
   point `r_J=f+z_J g` agrees with `c_J` on **exactly** the `n−j=12` points of `D\J`
   (and differs on all `j` points of `J`); (f) distinct `P_J(β)` give distinct slopes
   — `LD_sw(C,12) ≥ 4` for this single line. **Convention note (honest):** Lemma 1's
   hypothesis `deg(P_J−P_J')≤j−σ` fixes the top `σ−1` elementary-symmetric functions
   `e_1..e_{σ−1}` (this realization over-fixes by grouping on `e_1..e_σ`, harmless);
   that is what makes `Q_m` common. The deployment adds the endpoint (item 3, item 6).
6. **Two-ended transfer — VERIFIED FINDING (off-by-one in the stated jet)**
   (`verify_m1_strict264_two_ended_transfer.py`). The LD_sw transfer needs the
   common-line part `A_J := H e_J − z_J B` (`z_J=1/P_J(β)`, `B_m=β^m`) to be common
   across the jet class — only then does a single received line `f+z g` exist
   (`Hf = A_common`). Since `A_m = −Q_m(β)` and `Q_{j+t}` depends on `e_1..e_t`, the
   **top** row `m=j+σ−1` depends on `e_{σ−1}`. Full enumeration on `RS[F_97,D,8]`
   (`j=5, σ=3`) decides three readings:
   * **`e_1..e_{σ−1}` common** (Lemma 1): `A_J` common across all 1000 classes ✓.
   * **`e_1..e_{σ−1}, e_j` common** (Lemma 1 + endpoint): `A_J` common (64 classes) ✓.
   * **`e_1..e_{σ−2}, e_j` common, `e_{σ−1}` free** (the candidate note's *literal*
     `deg ≤ j−σ+1` reading): `A_J` is **NOT common** — it varies in **exactly the top
     parity row** `m=j+σ−1`, so no single line fits. ✗
   **Conclusion:** the deployed two-ended construction is valid **iff `e_{σ−1}` is
   fixed too**, i.e. the correct jet is `deg ≤ j−σ` (top `σ−1` common) **+ endpoint**;
   the literal `deg ≤ j−σ+1` in the candidate note (and earlier drafts) is an
   off-by-one that breaks the common line. With the corrected jet, the construction
   reduces to the proven Lemma 1 transfer (item 5) on the endpoint-fixed sub-family.
   strict264's conclusion is unaffected (the admissibility enumeration already used
   the correct grouping); only the stated degree condition is corrected `241 → 240`.
   **Corroboration by the deployed record:** the `cycle119` proof record
   (`site/data/frontier.json`) states its jet as *"common top-six coefficients plus
   common nonzero constant coefficient."* For cycle119, `σ = 263−256 = 7`, so "top
   six" `= e_1..e_6 = e_1..e_{σ−1}` **+ constant (endpoint)** — exactly the **corrected**
   jet, fixing the top `σ−1 = 6`. The candidate note's *general* statement
   `deg ≤ j−σ+1` would fix only the top `σ−2 = 5`; the record fixes one more. So the
   actual deployed construction already uses the correct jet — the off-by-one is
   confined to the note's *general prose*, and the verified correction matches the
   proof record.

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
- **VERIFIED (end-to-end, genuine RS code):** the LD_sw transfer
  `LD_sw(C,n−j) ≥ #{P_J(β)}` realized as actual codewords agreeing on `D\J`, one
  common received line, noncontained (`verify_m1_strict264_end_to_end.py`).
- **VERIFIED (transfer finding, correction):** the two-ended jet must fix
  `e_1..e_{σ−1}` (top `σ−1`, `deg ≤ j−σ`) **+ endpoint**; the literal `deg ≤ j−σ+1`
  (freeing `e_{σ−1}`) breaks the common line in the top parity row
  (`verify_m1_strict264_two_ended_transfer.py`). Stated degree condition corrected
  `241 → 240`; strict264's conclusion is unaffected.
- **OUT OF SCOPE (needs the rejected-archive slot spec):** the exact survivor count
  `≥7` / `2187` for the actual `F_17^32` row — slot-model-dependent.

## Audit verdict (interim)
The strict264 obstruction is **structurally sound and admissible**: every checkable
layer — the bridge arithmetic, the slack-8 parameters, the retained-slope drop
mechanism, the two-ended common-`ℓ` construction at `(248,8,256)` (with the
**corrected jet** `deg ≤ 240` + endpoint), and the LD_sw transfer realized
end-to-end on a genuine RS code — passes independent verification. The audit also
**caught and corrected an off-by-one** in the stated jet (`241 → 240`): the literal
condition would free `e_{σ−1}` and break the common received line; the construction
is valid only with `e_{σ−1}` fixed, after which it reduces to the proven Lemma 1
transfer. The single remaining gap is the *exact* survivor count `≥7`, governed by
the Cycle84 7-slot model not present in the repo. The audit neither confirms nor
refutes the precise "7"; it certifies everything around it (now including the
corrected jet) and isolates the one slot-model-dependent number.

## Reproducibility
```bash
python3 experimental/scripts/verify_m1_strict264_bridge.py
python3 experimental/scripts/verify_m1_strict264_mechanism.py
python3 experimental/scripts/verify_m1_strict264_admissibility.py
python3 experimental/scripts/verify_m1_strict264_end_to_end.py
python3 experimental/scripts/verify_m1_strict264_two_ended_transfer.py
```
