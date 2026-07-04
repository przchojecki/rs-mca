# Corridor Unconditional Safe Edges: Two Proof-Audited MCA Imports

- **Status:** AUDIT / PROVED (imports proof-audited externally; row
  arithmetic exact-integer, verifier-replayed).
- **Date:** 2026-07-04.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Certificate:** `experimental/data/certificates/corridor-unconditional-safe-edges/`
  (README + JSON), verifier
  `experimental/scripts/verify_corridor_unconditional_safe_edges.py`
  (`--write` deterministic, `--check` exact-integer battery, < 1 s).
- **Sources (upstream, by ref):** `tex/cs25_cap_v12.tex` (`def:mca` ~139,
  `lem:mca-monotone`, `cor:conditional-half` ~5054); `tex/towards-prize.tex`
  (`thm:sparsify` ~661, `thm:transfer` ~780, `prop:p2-half-sharp` ~522);
  `open-proximity.tex` (~676–689, GKL24/BGKS20 theorem block; bibliography);
  `experimental/notes/roadmaps/xr_budget_audit.md` (row constants, `B*`);
  `experimental/notes/audits/m0_prize_mca_definition_freeze.md` (Use Rule);
  `experimental/data/certificates/sigma-c-sparse-census/` and
  `experimental/notes/m1/sigma_c_sparse_census.md` (sparse-mutual lane);
  `experimental/notes/audits/audit_bchks25_thm46_conditional_johnson_import.md`
  (the #272 conditional packet).
- **External audit trail:** `github.com/latifkasuli/mca` @ `3fea63a`:
  `docs/gkl24-proof-audit.md` (GKL24 line-by-line proof audit),
  `docs/bchks25-thm46-import-audit.md`, section "Hab25 proof audit"
  (Hab25 line-by-line proof audit), `docs/gkl24-corridor-import-audit.md`
  (pre-paper row reconnaissance, superseded in part by this note — see
  "Recompute" below).

## Summary

The six clean-rate corridor rows currently carry `(1-rho)/2` safe edges from
the published BCIKS20 import. Two newer results, **both now independently
proof-audited line-by-line**, move the certified safe edge unconditionally:

1. **Hab25** (ePrint 2025/2110, Thm 2; audited 2026-07-04): the `def:mca`
   event at `M = 1`, verbatim, up to the Johnson radius with quadratic error
   `(l^7/3)(rho_B n)^2`, `l = (m+1/2)/sqrt(rho_B)`, `rho_B = (k-1)/n`. The
   mechanism (per-factor-class collapse to a unique affine-in-z proximate +
   the AHIV17 petal count) is rigorous; three bookkeeping gaps (G1–G3) were
   closed in the audit; every deferral was verified against BCIKS20 ECCC
   TR20-083.
2. **GKL24** (ePrint 2024/1810 v3, Thm 3; audited 2026-07-04): mutual
   correlated agreement for **every linear code over every finite field** at
   the 1.5-Johnson radius `delta <= 1 - (1 - Delta_C + eta)^(1/3)` (`eta`
   inside the radical, endpoint open) with the **linear-in-n** count bound
   `(n+6)/eta + 2/(eta((1-Delta_C+eta)^(1/3) - (1-Delta_C+eta)^(1/2)))`.
   Every lemma is proved in-paper (zero external proof dependencies); 12
   recoverable errata were closed in the audit; the Definition-8 <=> `def:mca`
   bridge is proved in the audit (upper-bound direction unconditional,
   equivalence on `delta < Delta_C`, which the theorem radius guarantees).

**Headline:** on all six corridor rows the Hab25 quadratic bound dominates —
these are exactly the `q >~ 2^220` rows where an `n^2`-scale numerator is
budget-free at `2^-128` — and lands at (or one cell / a 0.21–0.31%-of-n
sliver under) the Johnson grid edge:

| row | current | GKL24-1.5J | Hab25-J-quad | Johnson grid edge |
|---|---|---|---|---|
| Row C 1/4 | 384 | 379 (no gain) | **512** | 513 |
| Row C 1/8 | 448 | 513 | **663** | 663 |
| Row C 1/16 | 480 | 619 | **769** | 770 |
| prize 1/4 | 824633720832 | 813725411113 (no gain) | **1092724518963** | 1099511627777 |
| prize 1/8 | 962072674304 | 1099511627777 | **1415997755216** | 1421551127559 |
| prize 1/16 | 1030792151040 | 1326340298262 | **1644686143216** | 1649267441666 |

GKL24's residual value on these rows is *not* the frontier: (a) it is a
**second, independent mechanism** (set-intersection games / sunflower-petal
counting vs Guruswami–Sudan factor algebra) certifying a weaker band — cheap
redundancy for the dossier, in a strictly better provenance class than
anything else near Johnson (fully proved in-paper, linear-in-n); (b) it covers
**general linear codes** — the only proved mutual statement available if
non-RS rows (circle/Chebyshev-tower objects) ever need MCA form; (c) at its
own radius it needs only `q >~ 2^150` (Row C shape) vs Hab25's `~2^164` at the
same radius — relevant to hypothetical mid-size-q rows, none in the current
slate.

## Recompute: exact GKL24 ladder vs the pre-paper reconnaissance

The pre-paper recon (`docs/gkl24-corridor-import-audit.md`, written before
the primary text was audited) instantiated the *survey's* rendering under a
"worst of three parses" convention. The proof audit settled the true constant
and radius (`eta` inside the radical; prefactor `(n+6)/eta`, NOT the survey's
`n + 6/eta`). Recomputed exactly:

- **All six integer radius edges are unchanged** (379/513/619 and
  813725411113 / 1099511627777 / 1326340298262): the recon already used the
  exact gate `(n-r)^3 > (k-1)n^2`, which the audit confirmed.
- **Every numerator/margin cell shifts** — all three recon parses inherited
  the survey's misprinted prefactor, which understates the bound by ~`1/eta`
  on the `n` term. At the pinned `eta = eta*` (full grid slack):
  Row C numerators `~2^15.8–2^16.3 -> 2^20.17 / 2^22.02 / 2^21.53` (margins
  now 99.98–101.83 bits, was "≥ 105.7"); prize numerators
  `~2^46.0–2^47.3 -> 2^82.30 / 2^84.00 / 2^83.66` (margins now
  **43.90–45.60 bits**, was "≥ 80.6"); minimum `q_line` to clear `2^-128`
  moves from `~2^144 / ~2^175` to `~2^148–2^150 / ~2^210.3–2^212.0`.
- **No verdict moves** (everything still clears by ≥ 43.9 bits), but the
  recon's margin figures should not be quoted going forward; the certificate
  JSON is the authority.

## The sigma_C consequence (sparse-mutual lane)

Via `thm:sparsify` (`eps_mca = max(eps_ca, sigma_C(delta)/q)`), any per-pair
MCA numerator bound pins the sparse mutual layer. On the corridor rows this
packet therefore certifies, unconditionally:

- `sigma_C(delta) <= B_GKL(delta) = O(n/eta)` — **linear in n** — on
  `((1-rho)/2, 1.5J]` for the rate-1/8 and 1/16 rows, and
- `sigma_C(delta) <= B_Hab25(delta) = O_m(n^2)` on the full band up to the
  Hab25 edges of the table,

discharging the `poly sigma_C` hypothesis of `thm:transfer` on those bands
for these rows. This complements the finite-row lanes: the upstream
`sigma-c-sparse-census` packets (exact small-field values) and the #273
gap-structure census (`mca-ca-sparse-layer-census`) probe the same object
from below at census scale; `prop:p2-half-sharp`'s `O(1)` mutual-only slopes
per pair sit comfortably inside both bounds — consistency checked in both
external audits against the F_17/F_97 killer rows (both theorems are safely
vacuous at census scale, as any true bound must be, since they are
non-vacuous only for `q >> poly(n)/eta`).

## Relation to #272 (KoalaBear conditional import): complementary regimes

The #272 packet
(`audit_bchks25_thm46_conditional_johnson_import.md`) imports BCHKS25
Thm 4.6's *linear-in-n* Johnson bound **conditionally** (gap G4: the printed
constant is sketch-level) to move the deployed KoalaBear `rho = 1/2`,
`q ~ 2^185.9` row to `r = 604,085`. The q-threshold picture separates the two
packets cleanly:

- **Hab25's proved quadratic bound needs `q >~ 2^220`** to certify
  Johnson-adjacent radii at `2^-128` (at the KoalaBear Thm 4.6 edge band
  `m = 146`, `B_note ~ 2^92.3` vs budget `2^57.9`); on KoalaBear it certifies
  only `delta <= 428878/2^21 ~ 0.2045 < 1/4` — below the existing edge. The
  KoalaBear band `(1/4, 0.288]` therefore **remains conditional** there.
- The corridor rows (`q_line >= 2^250`) sit above the `2^220` threshold, so
  the same proved theorem is budget-free here: **corridor = unconditional
  (this packet); KoalaBear = conditional (#272)**. The conditional Thm 4.6
  constant would add only 0–1 grid cells at Row C and ~0.3% of n at prize
  scale over this packet's edges — on these rows the condition is worth
  almost nothing, the opposite of the KoalaBear situation.

## Erratum: the survey's GKL24 row (`open-proximity.tex` ~676–689)

The printed theorem block misrenders GKL24 in three places (all confirmed
against the audited primary; flagged for the survey author):

1. **Radius:** printed `\delta\le 1-\sqrt[3]{1-\distmin(C)}+\eta` — the
   `+eta` outside *overstates* the radius past 1.5-Johnson. Correct:
   `\delta\le 1-\sqrt[3]{1-\distmin(C)+\eta}` (eta inside the radical;
   endpoint open).
2. **Prefactor:** printed `n+\frac6\eta` — *understates* the bound by
   ~`1/eta` on the `n` term. Correct: `\frac{n+6}\eta`.
3. **Denominator radicals:** printed
   `\sqrt[3]{1-\distmin(C)}+\eta-\sqrt{1-\distmin(C)}+\eta` — eta must sit
   inside both radicals. Correct:
   `\sqrt[3]{1-\distmin(C)+\eta}-\sqrt{1-\distmin(C)+\eta}`.

Corrected display (the audited Thm 3, `l = 1`):

```latex
\epsmca(C,\delta)\le
\left(\frac{n+6}{\eta}+
\frac{2}{\eta\bigl(\sqrt[3]{1-\distmin(C)+\eta}-\sqrt{1-\distmin(C)+\eta}\bigr)}\right)
\frac1{\abs{\F}},
\qquad \delta\le 1-\sqrt[3]{1-\distmin(C)+\eta}.
```

The `O(n/(\eta\abs{\F}))` summary line is fine as printed. Note the literal
printed parse is refutable inside the survey itself: with `+eta` extending
the radius, a large `eta` would put `eps_mca <~ n/q` at radii where the
survey's own CS25 limitation row forces `eps_ca = 1` (and
`eps_ca <= eps_mca`). Separately, the GKL24 *paper* carries 12 recoverable
errata (typo-level; the two nontrivial ones closed with complete arguments)
— list in `docs/gkl24-proof-audit.md`, errata E1–E12, worth forwarding to
the authors.

## Second-source note (Zei24)

Hab25's footnote 1 records: "In a later version, [Zei24] upgraded to the 1.5
Johnson bound as well" (Zei24 = ePrint 2024/1843, Khatam; originally
double-Johnson). If the live 2024/1843 confirms this, it is a *candidate
second independent unconditional source* at the same radius as GKL24 — same
set-intersection mechanism family — useful redundancy if GKL24's provenance
caveat (v3 after a v1 critical mistake, not peer-reviewed) ever needs
hedging. Unaudited; do not cite for certificates without a proof audit at
the same bar.

## What to do next

1. Maintainer review of the two import statements (certificate JSON,
   `imports` block) against the live ePrints; pin versions at merge.
2. Optionally promote the three-column table into `open-proximity.tex`'s
   positive-results section alongside the erratum fix above (three
   character-level edits).
3. When Row C's literal ~2^250 prime is pinned (flag C1(b)), re-run the
   verifier with the literal `q_line` — one-constant swap; margins make the
   verdicts immovable.
4. If a mid-size-q row (`log2 q in (~150, ~164)`) ever enters the slate,
   GKL24 becomes the frontier import there; revisit.
