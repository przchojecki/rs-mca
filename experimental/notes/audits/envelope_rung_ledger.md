# envelope-rung-ledger: the complete lower-side floor ledger at the four moved deployed pairs

**Named demand.** `prob:capfr1-rung-audit`
(`experimental/cap25_cap_v13_raw.tex`, "Immediate" work-queue tier):
*"For each of the four deployed adjacent values `a0+1`, run the exact
integer scanner over every divisor/rung and every slack profile used by
the quotient ledger. ... The audit must print per-rung bit losses; if any
rung is tight or inverted, the one-step finite conjecture is threatened
from the periodic side [...]"*

**Acknowledged gap being filled** (`m31_mca_conjq_rung_audit_v1.json`,
verbatim): *"only a single-rung spot check exists
(v13_raw_moved_pair.tight_rung_at_a1p: profile Gceil, c=2048, margin
-0.3938 bits, TIGHT, non-firing) -- not a full ledger at
(1116023,1116024)."* This packet is that full ledger.

**Base:** `36de5bfcc7d6e0ca44806112acec2f4a1b4a7532` (origin/main).
**No `.tex`/`.pdf` edited.**

**Status: EXPERIMENTAL / AUDIT.** Ledger verdict **NO ISSUE** — an
*outcome*, not a precondition: the generator emits
`COUNTEREXAMPLE_NEW_FLOOR` with a realization-witness section if any
frontier-covering rung fires, and its `--check` exits nonzero on a firing
rung so the outcome cannot be silently absorbed.

## Claim

For each of the four deployed rows at the current
(`prop:capg-moved-frontier` / `cor:capg-adjacent-pairs`) adjacent pairs —

| row | pair `(a0, a0+1)` | `eps*` | `B*` | pair status vs v13 |
|---|---|---|---|---|
| kb_mca | (1,116,047, 1,116,048) | `2^-128` | 274,980,728,111,395,087 | MOVED |
| kb_list | (1,116,046, 1,116,047) | `2^-128` | same | unchanged |
| m31_mca | (1,116,023, 1,116,024) | `2^-100` | 16,777,215 | MOVED |
| m31_list | (1,116,022, 1,116,023) | `2^-100` | same | unchanged |

— the complete lower-side floor ledger at `a0+1`: 21 dyadic rungs
(`c = 2^j`, `j = 0..20`) x 4 slack profiles (`Gfloor`/`Gceil`/`Rem`/
`Plant`, the quotient ledger's profiles), every verdict an exact integer
comparison of the deep-point-converted integer mass `M` against `B*`
(the committed `v13_raw_moved_pair.route`:
`L = ceil(mass) -> M = ceil(L(q-n)/(q-n+k(L-1)))` for MCA rows, `M = L`
for list rows; `fires := M > B*`, `TIGHT := B*/2 < M < 2B*`).

**Result (per-row frontier-covering margins at `a0+1`):**

| row | cells | min margin (bits) | max margin (bits) | fires | tight |
|---|---:|---:|---:|---|---|
| kb_mca | 51 | −57.9321 | **−22.1969** (`c=1`) | none | none |
| kb_list | 47 | −57.9321 | **−22.0109** (`c=1`) | none | none |
| m31_mca | 50 | −24.0000 | **−0.3938** (`Gceil c=2048`) | none | **one** |
| m31_list | 47 | −24.0000 | **−3.0730** (`c=1`) | none | none |

**Headline: no rung fires.** The adjacent pairs survive the complete
folding sector. The single sub-bit rung is the known watch-item, now
pinned inside a full ledger instead of a spot check: `m31_mca`, `Gceil`,
`c = 2048`, `m = 545`, covered agreement `1,116,160 >= a0+1`, `w = 32`,
`M = L = 12,769,758` vs `B* = 16,777,215`, margin **−0.3938 bits**
(headroom `4,007,457`; it fires only at `>= B*+1`, i.e. `4,007,458` more
codewords at agreement `1,116,160`).

## Division of labor: Lean sector vs finite sector

- **Asymptotic sector (Lean, integrated, zero-sorry at the
  exponent-algebra level).** Both deployed image alphabets are *prime*
  fields — certified by explicit integer checks in the certificate
  (deterministic Miller-Rabin primality of `p_kb = 2^31-2^24+1` and
  `p_m31 = 2^31-1`; dyadic tower existence `v2(p_kb - 1) = 24`,
  `v2(p_m31 + 1) = 31`; and the alphabet-is-`p` reproduction check below).
  Hence every realizable complete-fiber folding has field ratio
  `lambda = 1`, and
  `profileIdentityDominant_of_all_fieldRatio_eq_one`
  (`GrandeFinale/ProfileEnvelopeWindow.lean`) makes the finite row
  `{(c=2^j, lambda=1) : j=1..20}` identity-dominant at *every* rational
  crossing; by `profileIdentityDominant_iff_avoidsFailureBandUnion` the
  asymptotic failure-band union is **empty** (each `lambda = 1` band is
  the empty open interval `(h, h)`). The `CompleteFiberFolding`
  structure carries `(degree, fieldRatio)` as one indivisible pair — the
  `(2,1/5)+(3,1/10)` mix-and-match regression is excluded by
  construction. The "prime forces `lambda = 1`" step is a Lean
  *nonclaim*, so the certificate carries it as the explicit integer
  checks above, not as a Lean import.
- **Finite rounding sector (this ledger).** What the Lean sector cannot
  see: per-rung rounding multipliers `|B|^{(w mod c)/c}` range up to ~31
  bits while the M31 identity fail margins are only 3.3/3.1 bits —
  genuinely undecided rung by rung, decided here by exact integers
  (Legendre + product-tree binomials at up to 2M bits).

### The M31 circle caution — decided, not assumed away

Question: does the circle construction place the effective alphabet in a
degree-2 extension (making `lambda = 1/2` drops realizable)?
**Decision: NO on the deployed rows**, on three grounds recorded in the
certificate: (i) `def:circle-twin-domain` — the deployed domain is the
*projected* Chebyshev twin-coset x-domain
`D(g,H) = chi(D(g,H)) ⊆ F_p` of cardinality `|H|`; the norm-one torus
upstairs (in `F_{p^2}`) is not the evaluation alphabet; (ii) the
`prop:capg-moved-frontier` proof, verbatim: *"the floor and the witness
classification run verbatim on the twin-coset x-domain (D ⊆ B = F_{p'}
is all that is used)"*; (iii) an integer check: all eight frozen
identity floors of `profile-envelope-numerics` reproduce with
denominator base `p` (`p^w`), not `p^{2w}` — a degree-2 effective
alphabet would fail every m31 reproduction. Counterfactual honesty: if a
future presentation realized `lambda = 1/2` at some scale,
`CompleteFiberFolding.zeroTarget_mem_inFailureBand` shows the band would
be *nonempty* and the asymptotic sector would have to be recomputed.

## Conventions (carried verbatim-with-citation)

From `experimental/data/certificates/frontier-adjacent/`
`{kb_mca,m31_mca}_v1.packet.json` `rung_margin_audit.conventions`:

```text
Gfloor : prop:graded-prefix-floor, m=floor(a/c); covers agreement mc<=a (A1 convention)
Gceil  : graded floor with m=ceil(a/c); covers agreement mc>=a (>=frontier)
Rem    : lem:quotient-remainder-prefix, s=a-mc; covers agreement EXACTLY a
Plant  : thm:v13-planted, M=c; P=C(n/c-1,k/c) at agreement k+sigma, 1<=sigma<c
```

- **Gceil monotonicity convention (carried exactly):** a floor bears on
  the safety of `a0+1` only if it covers an agreement `>= a0+1`
  (unsafety propagates downward, `def:v13-staircase`); `Gceil` is the
  frontier-bearing pure-scale floor at *every* `c`, `Gfloor` only when
  `c | a0+1`. Sub-frontier cells are reported but excluded from the
  verdict (they certify only already-unsafe agreements `<= a0`; e.g. the
  m31 rows' sub-frontier `Plant` cells fire hugely at agreements near
  `k`, exactly as the old-pair ledgers recorded).
- **Chebyshev endpoint multiplier (carried exactly):**
  `rem:qr-chebyshev` — on circle twin-coset domains the fixed/ramified
  endpoints form an exceptional set of cardinality `b`, crude total
  multiplier at most `2^b`, with **`b <= 2`** for involution-fixed
  endpoints. For the *deployed* m31 rows `b = 0`: a twin coset contains
  no self-inverse element and `T_c` has complete fibers of size `c` at
  every dyadic scale (`lem:torus-fibers`, `lem:cheb-fibers`,
  `rem:standard-position`), so no endpoint multiplier is charged.
  **Sensitivity (load-bearing):** the −0.3938 watch-item rung would fire
  under any multiplier `>= 2^0.3938` — even the crude `b = 1` factor
  flips it (`2 x 12,769,758 > 16,777,215`, gated as an integer check).
  `b = 0` is a *proved* property of the deployed standard-position
  domains, not an assumption.
- **Threshold update vs the old-pair ledger:** the old-pair
  `rung_margin_audit` compared raw rational masses against
  `Theta_mca = (q+k)/k` / `Theta_list = q/2^lam`; post-move the deployed
  comparison is integer `M` vs `B*` via the lossless `L -> M`
  conversion. Verdicts are equivalent (`ceil(F) > B*` iff `F > B*` for
  integer `B*`); *reported* margins differ for deep-suppressed cells
  (masses `< 1` floor at the trivial `L = 1` here, reading `-log2(B*)`
  instead of the old `~-10^6` raw values). Both stated so the two
  ledgers are never read as contradicting each other.

**Not conflated:** the upper-side conj:Q max-fiber rung audits
(`{kb,m31}_mca_conjq_rung_audit_v1.json`) are, per their own
reconciliation blocks, *"DISTINCT objects and must not be conflated"* —
they charge quotient-pulled-back **upper** fibers to their rungs
(`K_raw` consumption; kb GREEN, m31 NOT GREEN on its pessimistic
ladder); this packet is the complementary **lower**-side floor ledger
(does any periodic floor *exceed* the budget). Their content is cited,
not duplicated.

## Replay-vs-ledger consistency (all gated in the certificate)

1. **Maintainer partial scan** `experimental/scripts/towards v13/`
   `cap25_v13_raw_moved_frontier_checks.py` (committed provenance:
   `2b5b7ce`; in-tree at this base) — re-run this session, exit 0,
   printed margins `8.978 / 22.197` (kb_mca) and `27.927 / 3.259`
   (m31_mca) byte-matching the addendum sec 1.4 record; every one of its
   exact assertions (pass/fail comparisons, both admissibilities,
   strictness, `N1` bounds, zero-collision) is re-derived inside the
   generator from its own binomials, and the identity margins agree
   within 0.1 bit.
2. **Committed `v13_raw_moved_pair` blocks** (kb_mca, m31_mca packets):
   `L`/`M` integers at both moved points equal, margins within `5e-4`,
   deficit-to-cross equal, and the m31 `tight_rung_at_a1p` block
   (`c=2048, L=M=12769758, margin -0.3938`) equal field-by-field to this
   ledger's recomputed cell.
3. **Frozen `profile-envelope-numerics` floors:** all 8 identity floors
   reproduced exactly (this is also the alphabet-is-`p` circle check).
4. **Addendum sec 3.2 Gceil tables:** all 42 printed 2dp margins (both
   MCA rows, all 21 scales) reproduced exactly at 2dp.
5. **Unchanged-pair list packets:** graded `fires` verdicts at `a0+1`
   match the old ledger cell-by-cell, and the old ledger's single
   sub-bit cell (m31_list `Gfloor c=2048`, sub-frontier, covered
   1,114,112, −0.21) reproduces.
6. **In-tree gate suite:** `verify_frontier_adjacent_v13_rows.py` re-run
   at this base — 7/7 PASS including G7.

## Use Rule

When citing this packet:

```text
object   = lower-side periodic/quotient floor ledger at the deployed a0+1
scope    = dyadic complete-fiber rungs c=2^j (j=0..20) x {Gfloor,Gceil,Rem,Plant}
verdict  = NO ISSUE (no frontier-covering floor exceeds B*; outcome, not premise)
watch    = m31_mca Gceil c=2048: M=12,769,758 vs B*=16,777,215 (-0.3938 b, TIGHT)
NOT      = a safety certificate for a0+1 (aperiodic/L1/sparse cells untouched;
           prob:capff1-frontier stays CONJECTURAL_WITH_FALSIFIER)
```

Safety-side statements sourced from this packet MUST carry the
conditionality "within the scanned folding family"; failure-side
statements (had a rung fired) MUST carry a realization witness for the
firing folding before any printed frontier moves.

## Self-Red-Team

- *Is the verdict baked in?* No. The verdict string is computed from the
  firing set; the `--check` path exits `2` on a firing rung (distinct
  from gate failure `1`), and the independent checker re-derives the
  verdict from its own recomputed cells. Flipping any single `M` above
  `B*` in the JSON fails both scripts.
- *Could the ceiled-mass convention hide an inversion the raw-rational
  convention would catch?* No: `ceil(F) > B*` iff `F > B*` for integer
  `B*` — firing verdicts are convention-independent. The convention only
  changes *reported* margins of deeply suppressed cells (documented).
- *Could the deep-point conversion manufacture safety?* The conversion
  is applied in the direction the committed route defines (`L -> M`,
  never inflating: `M <= L` always), and the ledger additionally records
  `M == L` (lossless) at every frontier-covering MCA cell — gated.
- *Sub-frontier `Plant` cells fire; is that a contradiction?* No — they
  certify unsafety at agreements `<= a0`, which are already certified
  unsafe; the frontier verdict correctly excludes them (same exclusion
  the old-pair ledger and the addendum use). They are reported, not
  hidden.
- *Is the M31 circle row really on alphabet `F_p`?* Decided on
  manuscript grounds plus an integer check that would fail loudly if
  wrong (all eight frozen floors reproduce with `p^w` denominators; a
  degree-2 alphabet would need `p^{2w}`).
- *Endpoint multipliers:* the one place a hidden `2^b` factor could flip
  a verdict is the watch-item itself — recorded as an explicit
  sensitivity block with integer checks, with `b = 0` cited to
  `lem:cheb-fibers`/`rem:standard-position` rather than assumed.
- *Float use:* margins are informational 4dp (top-900/1100-bit mantissa,
  disjoint widths across the two scripts, lgamma cross-estimates at
  0.5-bit tolerance); no float ever decides fires/TIGHT.

## NON-CLAIMS

Mirroring the Lean module's nonclaims (`ProfileEnvelopeWindow.lean`
header: exponent algebra only; *"it does not establish the ledger
hypotheses A2/A4 or the asymptotic bridge from exponent dominance to an
envelope estimate"*):

1. **No safety theorem.** `U(a0+1) <= B*` is NOT established for any
   row. The aperiodic (`prob:band`), L1 (`prob:v13-l1-residuals`,
   `prob:v13-primitive-image-fiber`), and sparse
   (`prob:mutual`/`prob:sparse-mutual`) cells are untouched; `a0+1`
   safety remains `CONJECTURAL_WITH_FALSIFIER` (`prob:capff1-frontier`).
2. **No A2/A4, no realization, no exhaustiveness, no deployed
   finite-row bound in Lean.** The Lean citation covers only the
   asymptotic exponent algebra; everything finite in this packet is paid
   by exact integers, not by the Lean module.
3. **No claim of profile exhaustiveness.** The four profiles are the
   quotient ledger's own (the named demand's scope); "no rung fires" is
   conditional on that family.
4. **No upper-side content.** The conj:Q max-fiber audits are distinct
   objects (see above); nothing here bears on their open `L_1..L_3`
   reductions.
5. **The atlas caveat stands.** This ledger discharges the
   profile-envelope-vs-target packet's printed *deployed* nonclaim —
   *"Deployed extra_profile_barNs empty: complete lower reduces to
   universal+identity image L; not a proved full atlas"* — by committing
   the per-`(profile, c)` folding floor terms at the deployed rows for
   the complete dyadic family; it does NOT prove a witness-exhaustive
   atlas (a full atlas could only add terms, which would only raise the
   envelope).

## Reproducibility

```text
python3 experimental/scripts/verify_envelope_rung_ledger.py --emit-defaults
python3 experimental/scripts/verify_envelope_rung_ledger.py --check
python3 experimental/scripts/verify_envelope_rung_ledger_check.py --check
```

stdlib only, deterministic, byte-stable regeneration, no timing or
machine paths in any frozen output. Certificate:
`experimental/data/certificates/envelope-rung-ledger/envelope_rung_ledger.json`
(91 internal checks; generator route Legendre+product-tree, checker
route Kummer+heap with no generator import).
