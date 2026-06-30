# A0 — Consolidated adversarial audit of Paper D v7 `thm:A` (deep-point list-to-CA conversion)

## Claim

The self-contained deep-point list-to-correlated-agreement conversion `thm:A` of
`tex/cs25_cap_v7.tex` (lines 148–268) — the only conversion load-bearing for the
universal MCA cap `thm:main` — is **correct as stated and proved**, and the
`v5 → v7` revision (adding `q > n`; relaxing the radius from strict
`f_δ < n-k-1` to non-strict `f_δ ≤ n-k-1`; closing the `thm:main` interval to
`[δ_N, 1-ρ-1/n]`) is **sound and necessary**, not cosmetic. The main cap no
longer depends on any external import. One honest residual remains on the
*fallback* route only (`prop:slacked` → ABF Thm 5.2).

## Status

**AUDIT.** Verdict in A0 template form: **the import matches exactly / `thm:A`
is correct and self-contained** for the main cap. One source-unverified item is
isolated below; it does not touch the main `thm:A → thm:main → cor:grand/deployed`
route.

This note **supersedes the scattered v4-era A0 import notes for the main cap**
(see "Prior-note reconciliation"): it is the first adversarial verification of
the *in-house* `thm:A` proof rather than of the obsolete CS25-import framing.

## Parameters / object

`C = RS[F,D,k]` (deg `< k`), `C⁺ = RS[F,D,k+1]`, `q = |F|`, `n = |D|`,
`D ⊆ B^× ⊆ F^×` a smooth multiplicative coset, `δ_N = 1-ρ-2/N`. Field ledgers
kept distinct: `q = |F|` is the **challenge** field (slopes `γ ← F`), `|B|` is
the **subfield of definition** used only in the `lem:fiber` pigeonhole. No
`q_gen`/`q_line` conflation; `thm:A` counts bad slopes over `F`, `lem:fiber`
pigeonholes locator slopes `z_A = -e₁(A) ∈ B` over `B`.

## Existing paper dependency

`tex/cs25_cap_v7.tex`: `thm:A` (148–268), `thm:main` (575–618), `lem:fiber`
(slack-two), `fact:chain` (`ε_ca ≤ ε_mca`), `lem:mca-monotone`, `rem:import`
(287). Imports: ABF (ePrint 2026/680) Defs 4.1/4.3 + challenge envelope; CS25
(2025/2046) Thm 2 (historical, demoted to `rem:import`); BCHKS (2025/2055)
Thm 1.9 via ABF Thm 5.2 (`thm:B`, used by `prop:slacked` fallback only).

## Experiment — adversarial verification (7/7 CONFIRMED, 0 REFUTED)

Seven independent skeptics each tried to **refute** one load-bearing step with
explicit finite counterexamples (pure-stdlib GF(p)/GF(2^m), thousands–millions
of instances). All survived:

| step | claim | result |
|---|---|---|
| S1 near / degree-drop | `f_α + P_i(α)g_α = (P_i(x)-P_i(α))/(x-α)`, deg `≤ k-1`, lands in `C`, rel-dist `≤ f/n ≤ δ` | CONFIRMED (6268 inst., incl. boundary, deg-k/const `P`, GF(2)⊂GF(8)) |
| S2 far / MCA obstruction | `(X-α)G(X)+1` (deg `≤k`, value 1 at α) caps any deg-`<k` match to `g_α` at `≤k` pts ⇒ `dist_2 > δ` | CONFIRMED (true max-common-agreement brute force) |
| S3 relaxation boundary | `a = n-f > k ⇔ a ≥ k+1 ⇔ f ≤ n-k-1` is **exactly tight**; `a=k` breaks far | CONFIRMED (83,731 boundary configs; tight) |
| S4 averaging + Cauchy–Schwarz | min≤mean over `\|Ω\|=q-n` + `Σm_r²=L+2ΣC(m_r,2)` ⇒ `M ≥ L(q-n)/(q-n+kL)` | CONFIRMED (~29.5M partitions) |
| S5 solve-for-L, η | inversion monotone & **tight**: applicability `kL≤q-n` ⇔ bound holds, no off-by-one | CONFIRMED (exact-Fraction sweep) |
| S6 `q>n` necessity | `q>n` is exactly what averaging (`\|Ω\|≥1`) + division (denom `>0`, `η<1`) need; **no hidden `q≥2n`** | CONFIRMED (tested `\|Ω\|=1`) |
| S7 `thm:main` composition | `C`/`C⁺` degree-drop deliberate; `a\|k` (not `a\|k+1`) via slack-two; radius cutoff exactly tight; η=1/2 constants exact | CONFIRMED (5500+ inst. + grand regime to ~2^256) |

### The `v5 → v7` correction (the substantive finding)

- **`q > n` added** — S6 shows this is the precise necessary-and-sufficient
  field-size condition. The predecessor `q ≥ 2n` (Cho26b) is **not** needed;
  it only sharpens the constant via `1-n/q ≥ 1/2`, never validity. v7's claim
  to drop it is correct.
- **strict `f<n-k-1` → non-strict `f≤n-k-1`** — load-bearing, not cosmetic:
  `thm:main` invokes `thm:A` at the CA endpoint `δ = 1-ρ-1/n`, where
  `⌊δn⌋ = n-k-1` **exactly**. The old strict bound would have wrongly excluded
  the very endpoint `thm:main` consumes. S3 proves `f≤n-k-1 ⇔ a=k+1>k` is
  exactly tight (`a=k` breaks the far-condition — verified one notch each way).
- **`thm:main` interval closed** to `[δ_N, 1-ρ-1/n]`; `ε_mca` then reaches
  `[δ_N, 1-ρ)` via `fact:chain` + MCA-monotonicity. Seam consistent (S7).

## Prior-note reconciliation

Five prior A0 notes reconciled — `a0_cs25_import_audit.md`,
`a0_cs25_rational_constant_derivation.md`,
`a0_external_import_source_check_20260618.md`, `cs25_import_audit.md`,
`codex-f1-l1-20260617/.../20260617_A0_CRITES_STEWART_AUDIT.md`:

- **All audited Paper D v4** (one v4/v6); each treated `thm:A` as an *unverified
  external import* (CS25 Thm 2 via ABF Thm 5.3) and rated it AUDIT/CONDITIONAL.
  **None verified the self-contained v5/v7 proof** — this note is the first.
- **None contradict v7** (`notes_contradicting_v7 = 0`): every reproduced
  constant matches `thm:A` verbatim.
- **None relied on the stale strict bound**: they predate the floor formulation
  and express admissibility as `δ ∈ (0, d_min(C))`, never stating `f<n-k-1` *or*
  `f≤n-k-1`. They are silent on it, not dependent.
- **Maintainer flag (carried forward from `cs25_import_audit.md`):** the v4-era
  import-conditionality framing is obsolete for the main cap; if the
  admissibility condition is ever cited from those notes it must use v7's
  non-strict `f ≤ n-k-1`.

## External-import status

**Now self-contained (not load-bearing on any external PDF):**
- `thm:A` — proved in-house (v7 line 148); correctness rests on S1–S7.
- **ABF Defs 4.1/4.3, Fact 4.5 chain, challenge envelope
  (`ρ∈{1/2,1/4,1/8,1/16}`, `k≤2^40`, `|F|<2^256`, `ε*=2^-128`), KoalaBear-sextic
  §6.3 / Tables 2–3** — **EXACT, primary-verified** (ABF ePrint 2026/680 fetched
  via Wayback). v7's "[ABF26] up to notation" is accurate (v7 = `s=1` scalar
  specialization).
- **CS25 Thm 2** — primary PDF Cloudflare-blocked; statement from two consistent
  HackMD renderings matches `thm:A`'s intermediate bound
  `L = ⌈εq(q-n)/(q-n-kεq)⌉, ε<(q-n)/(kq)` **verbatim** (`minor_diff`). The
  "same consequence as CS25" provenance (line 53) is *secondary*-supported. The
  secondary source renders the radius as `f<n-k-1` (one unit stronger), but this
  is **non-blocking**: `thm:A` is self-contained and S3 independently proves
  `f≤n-k-1` is the exactly-tight correct boundary.

**Fallback `prop:slacked` (`thm:B` route) — internal-radius `1/n` concern RESOLVED:**
- The underlying **BCHKS Thm 1.9 is primary-verified** (Toronto mirror).
- The audit's flagged **strict-vs-non-strict `1/n` internal radius is a
  NON-ISSUE** (`verify_a0_thmB_internal_radius.py`). BCHKS uses degree `≤ k`
  (dim `k+1`; `bchks.txt` L3071, Def 1.8) while cs25 uses degree `< k` (L83), so
  the same code `C` forces BCHKS's `δ = 1-ρ+1/n`, and its conclusion
  `Δ([f,g],C²) ≥ δ-1/n` becomes **`≥ 1-ρ`**, not `1-ρ-1/n`. Equivalently
  BCHKS's own far-argument (L3116–3124) = `thm:A`'s S2: `g=-1/(x-α)` agrees with
  a deg-`<k` poly on `≤ k` points, so `Δ(g,C) ≥ 1-ρ`. Hence
  `Δ([f,g],C²) ≥ 1-ρ > 1-ρ-1/n = δ_int`: the strict `ε_ca` event holds with a
  full `1/n` margin, and **v7's internal radius `1-ρ-1/n` is correct and
  conservative** (the "maximally slacked" form, line 858). Certificate: in every
  small-field case `maxagree(g) = k` exactly (BCHKS `≥` is tight at `1-ρ`) yet
  `1-ρ > 1-ρ-1/n`.

**Residual on the FALLBACK only (source-access, not a known defect):**
- The **literal cited intermediary ABF Thm 5.2 wording is unverified**
  (ePrint 403; the fetched ABF PDF has Defs 4.1/4.3 but not the 5.2 packaging).
  What ABF 5.2 supplies is the contrapositive packaging that turns BCHKS's
  `δ`-indexed code statement into `thm:B`'s fixed-code / free-radius form via the
  `LDR` machinery — including the field-radius `+2/n` slack and the list-size
  boundary (`Lst ≥ q` vs the `LDR` "`≤ q`" convention). The internal radius is
  settled above; this remaining item is the `LDR`/field-radius packaging and is
  a *source-access* caveat, **not** a confirmed off-by-one.
  **It sits on the fallback, not the main self-contained cap.**

## Ledger impact

Field-transfer / MCA ledgers: the universal cap's conversion is **certified**
(no import debt on the main route). Removes the long-standing "CS25 import
conditional" caveat for `thm:main`/`cor:grand`/`cor:deployed`. The fallback
`prop:slacked` internal-radius `1/n` concern is **resolved** (non-issue); it
remains CONDITIONAL only on the ABF Thm 5.2 `LDR`/field-radius packaging source.

## Constants — numerical certificate (all pass, exact)

`verify_a0_thmA_v7_cap_certificate.py`: 25 envelope rows + KoalaBear-sextic row,
exact integer/Fraction compares. `eq:hyp` binding slack **52.46 bits** (`ρ=1/8`);
floor `≥ 2^-86` (true worst `~2^-85.0`); floor `≥ 2^-42` at `q≥2n` (razor-thin,
margin `~1/(2n+1)`, strictly true); deployed floor `2^-21.000 > 2^-22`. **The
published constants `2^-86 / 2^-42 / 2^-22` are everywhere `≤` the true values —
the paper conservatively understates its own margin (safe).**

## Reproducibility

```sh
python3 experimental/scripts/verify_a0_thmA_v7_cap_certificate.py   # numerical cap certificate (25 rows + deployed)
python3 experimental/scripts/verify_a0_thmA_v7_boundary_tight.py    # f<=n-k-1 boundary is exactly tight (a=k+1 ok, a=k breaks)
python3 experimental/scripts/verify_a0_thmB_internal_radius.py      # fallback thm:B internal radius 1-rho-1/n is safe (BCHKS gives >= 1-rho)
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py    # prior deep-point algebra grid (kL-q+n+k > 0)
```

Audit harness: `a0-thmA-audit` workflow (17 agents), run 2026-06-30. ABF
2026/680 fetched via Wayback; BCHKS 2025/2055 via Toronto mirror; CS25 2025/2046
via two consistent HackMD renderings (primary PDFs Cloudflare-blocked).
