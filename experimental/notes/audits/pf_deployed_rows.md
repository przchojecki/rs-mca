# pf-deployed-rows: finite failure map for the degree-uniform (PF) certificate at the printed deployed rows

**Lane.** Hard input **(b)** of `agents.md` — *"image-scale MI + MA, or a
direct Sidon payment"* — in the assigned adversarial failure mode
*"mismatch between asymptotic proof and finite deployed rows."*

**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (base
`4e3c4ee`, unchanged at this packet's base `486c8fb`). **No `.tex`/`.pdf`
edited.**

**Status: EXPERIMENTAL / AUDIT.** Verdict **NO ISSUE** (the draft asserts
no deployed-row (PF) instance; this packet quantifies the open cell).

## Claim

`rem:pf-numerical` reads the pointwise minor-arc range
(`def:prefix-flat-range`, tag (PF)) for finite certificates as the exact
minor-character check `|B|^R C(Lambda+m-1, m) <= e^{o(N)} C(N, m)`. This
packet performs that check zero-slack at all eight charts of the four
printed v13 deployed rows (identity-prefix chart: `|T| = n = 2^21`,
`m = a`, `R = w`, `|B| = p`), at the **most favorable** admissible
parameters (`C0 = 1`, `Delta_pole = 0`, `|P| = 0`, `sqrt` floored; circle
factor 2 for the M31 rows per the definition's twin-coset clause):

| row | chart | a | surplus (bits) | flip `Lambda*` |
|---|---|---|---|---|
| kb_mca | a0 / a1 | 1,116,047 / 1,116,048 | +280,001.52 / +280,032.75 | 4 / 2 |
| kb_list | a0 / a1 | 1,116,046 / 1,116,047 | +280,001.27 / +280,032.51 | 4 / 2 |
| m31_mca | a0 / a1 | 1,116,023 / 1,116,024 | +471,766.09 / +471,797.39 | 3 / 2 |
| m31_list | a0 / a1 | 1,116,022 / 1,116,023 | +471,765.79 / +471,797.09 | 3 / 2 |

**The degree-uniform (PF) route to (MI) cannot be instantiated at any
printed deployed row**: the largest `Lambda` for which PF-exact holds is
`Lambda* in {2, 3, 4}`, versus the Weil-forced
`Lambda >= isqrt(p) = 46,159` (kb) / `2*isqrt(p) = 92,680` (m31 circle) —
four orders of magnitude apart; the surplus is monotone increasing in
`C0`, `Delta_pole`, `|P|` (exact sweep for `Delta_pole in {0,1,2}` in the
certificate), so no admissible assignment flips any chart. Halving the
Weil constant to `C0 = 1/2` (sub-admissible; `Lambda` floored) still
leaves a +162,699.33-bit surplus at kb_mca a0 — gated in the
certificate's `surplus_sweep_exact_bits["C0=1/2"]` entry per chart.

## Relation to the draft (why NO ISSUE, and what is new)

- `prop:pf-deep-prefix-barrier` proves the asymptotic failure of the
  degree-uniform certificate in the deep regime `Lambda_N >= cN`. The
  deployed rows sit at `Lambda ~ 2.2%-4.4% of N` — a regime that
  proposition does not cover. This packet is its finite effective
  complement at the printed rows, with exact constants.
- The flip thresholds calibrate the repaired pointwise certificate
  `thm:prefix-flatness-power-sum` (PF'): at deployed scale it needs
  `|P_j(alpha)| <= Lambda*` with `Lambda* in {2, 3, 4}` — i.e. essentially
  perfect power-sum cancellation, far beyond the degree-uniform Weil
  majorant (cf. `prop:frontier-weil-separation`, whose `Lambda = o(N)`
  sufficiency direction is not contradicted: it feeds (PF'), not (PF)).
- Scaling honesty both directions: along a fixed-field family the surplus
  is `Theta(sqrt(p) log n) = o(n)` — the asymptotic (PF) hypothesis is
  consistent with these rows; conversely at this `n` the surplus is
  0.1335 (kb) / 0.2250 (m31) bits **per coordinate**, order-`n`-scale.
- Score-convention reconciliation: `fourier-sidon-payment`'s toy menu
  scores the same quantity with a toy cutoff `score/|T| < 0.5`; under that
  convention the deployed rows would read as toy-passes. Both readings are
  consistent — the `o(|T|)` slack is exactly the open question — and the
  certificate records both numbers side by side to prevent the family
  from appearing self-contradictory. (Parameter deltas: the toys use
  `C0 = 2` and round `sqrt` up; this packet uses `C0 = 1` and `isqrt`.)

The remaining pinned labels (`def:major-arc-aggregate`,
`def:aggregate-minor-payment`, `prop:pf-ma-square-dichotomy`,
`prop:weighted-weil-minor-arcs`,
`cor:sidon-payment-from-prefix-flatness`) anchor the (MA)/(MI)/Sidon
statements referenced in the nonclaims.

## Mathematical assumptions of the verifier

1. Chart identification `|T| = n`, `m = a`, `R = w`, `|B| = p` — the
   identity-prefix chart the deployed floors already use. Validated
   internally: `ceil(C(n,a)/p^w)` reproduces all eight frozen floor
   integers of `profile-envelope-numerics` exactly, and both printed
   margin pairs per row.
2. The zero-slack reading of (PF) per `rem:pf-numerical` ("For finite
   certificates this is the minor-character check").
3. The cycle-index leg `||e_m|| <= C(Lambda+m-1, m)` is the one
   machine-checked upstream (`powersum_rigidity/PrefixFlatness.lean`,
   `esymm_norm_le`); its note already states the Weil range boundary
   qualitatively ("the deployed rows sit far past it") — this packet
   quantifies it.

## Dual routes

Generator: Legendre floor-sum exponents + product-tree exact binomials;
all comparisons exact integers; flip thresholds by exact ratio recursion;
~10 s. Checker (`_check.py`, no generator import): Kummer carry-count
exponents + smallest-first heap merging for the big binomials, `math.comb`
for the cycle-index binomials, top-1100-bit mantissa log2 (vs the
generator's 900), lgamma cross-estimates at 0.5-bit tolerance, fresh pin
re-scan, and an independent re-key of the frozen numerics oracle; ~4.5 min
(the `math.comb` route dominates — that is the point of route disjointness).

## Credit / differentiation

- `prop:pf-deep-prefix-barrier` (maintainer, `4e3c4ee`): the asymptotic
  degree-uniform barrier; this packet is its finite complement at the
  printed rows (different regime, exact constants, flip thresholds).
- `deployed-template-replay` (integrated #497): replays the B*/L/U chain
  and leaves `A4_PF_MA_or_Sidon: "OPEN"` at both its rows; this packet
  quantifies that cell at all four rows including the list rows.
- `fourier-sidon-payment` (integrated #500): pins the (PF)/(MA)/Sidon
  statements and evaluates toy menus; its `does_not_assert` excludes
  deployed-row PF certificates — supplied here.
- `sidon-residual-input` (integrated #527): separates the SFM1 shallow
  hypothesis ratio at deployed-like triples — a different inequality
  (hypothesis regime of `thm:unconditional-shallow-mi-ma`), no (PF)
  surpluses or flip thresholds.
- `profile-envelope-vs-target` / `lower-reserve-unsafe` (integrated):
  hard inputs (d)/(e) at the same rows — floor/margin brackets, no (PF).
- `powersum_rigidity/PrefixFlatness.lean` (integrated): zero-sorry proof
  of the cycle-index leg this packet instantiates.

## Boundaries respected

No `.tex`/`.pdf` edits; no claim against the asymptotic (PF), the
effective-span variant (`log A_N` — not evaluable while hard input (a) is
open; ambient failure does not imply effective failure), (MA), or (PF');
floor/margin reproductions are oracle checks, not new results; the
finite-prize/deployed-threshold lane (parked per `agents.md`) is not
entered — this packet is hard-input-(b) route arithmetic.

## Reproducibility

```
python3 experimental/scripts/verify_pf_deployed_rows.py --emit-defaults   # ~10 s
python3 experimental/scripts/verify_pf_deployed_rows.py --check           # ~10 s
python3 experimental/scripts/verify_pf_deployed_rows_check.py --check     # ~4.5 min
```

stdlib only, deterministic, byte-stable regeneration, no timing in any
frozen output. Certificate:
`experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json`
(gated on 57 internal checks + the frozen-oracle equalities;
`RESULT: PASS (57 checks)`).
