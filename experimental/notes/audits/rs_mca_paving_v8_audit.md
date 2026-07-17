# rs-mca-paving-v8-audit: independent pre-submission replay + provenance audit of `RS_MCA_Paving_v8`

**Status: AUDIT** (base `06b2a6fb8c49a5ec0e23b9103af7c92a328fcabf`; audited
object `experimental/RS_MCA_Paving_v8.tex`, sha256
`dd936a52e3cac8f96d35c9e1b0c506654053cf64e1ea302acd83a971110be60a`, the
digest pinned in `RS_MCA_Paving_v8_source/REPRODUCIBILITY_v8.md`; blob
identical at `7f27816`, the tip the audit ran against)

**Auditor:** Claude (Fable 5). **Type:** pre-submission "final independent
read" for the ePrint upload gate: full arithmetic replay by independent
routes, import-provenance resolution against the pinned source, and proof
spot-audits. Three independent auditor lanes (arithmetic, imports,
proofs), consolidated here.

| item | value |
| --- | --- |
| arithmetic replay | **CLEAN** — 176/176 independent checks, all routes different from the bundled scripts; both bundled scripts pass; all 5 release SHA-256 digests match |
| script-coverage gap closed | the two DP1 deployed-prefix certificates (tex L2549-2588) are checked by **neither** bundled script; confirmed here three ways (Section 1) |
| the one pre-upload item | BCHKS Thm 4.6 at `M=1` is **sketch-status in its source** but presented as proved prior theory at tex L313-315, L751-760, L382 (Section 2); fix is textual, or an import swap — both cheap, all results survive |
| normalization of the import | **EXACT** — eq (1.13) matches the source verbatim at `M=1`; no constant-mismatch defect |
| tightness observation | the M31 `a0` ceiling collapse `M = L` has only ~10% headroom (Section 3) — re-verify on any radius re-tuning |
| proof spot-audits | paving mechanism, exact sparsification, official saturation, 128-bit circle certificate: all survive adversarial replay (Section 4) |
| replay script | `experimental/scripts/verify_rs_mca_paving_v8_audit.py` (stdlib, deterministic, exit 0 = all pass) |

This audits the maintainer's submission paper and in detail:
every printed number in the 53-page manuscript reproduces exactly under
independent recomputation, the release's own verification discipline is
unusually strong, and the one finding is a provenance sentence, not a
mathematical error. Nothing below touches the correctness of any finite
certificate.

## 1. Clean replay — 176/176 independent checks

All checks were recomputed by routes deliberately different from the two
bundled release scripts: Legendre prime-factorization exponents +
product-tree binomials (not `math.comb` on the large cells), hand-rolled
Miller-Rabin/Proth/Lucas-Lehmer primality alongside a second route,
binary-search **and** isqrt quadratic boundaries, 300-bit-shift exact-integer
logarithms, and exact `Fraction` arithmetic in the conditional appendix.
Everything matches:

- **Four Proth prize rows** (tex table at L2244-2250; appendix
  L5065-5139): Proth decompositions, witness congruences, primality (two
  routes), bit lengths 167/169/170/171, `n | p-1`, all four budgets
  `floor(p/2^128)` with exact remainders, and the quadratic staircase
  boundary `F(B-1) >= 0 > F(B)` with the printed values — plus the boundary
  re-derived two additional ways.
- **256-bit special row** (cor:intro-four-saturated-rows, L509-541):
  `p = (2^128-255)*2^128+1` Proth-certified, budget `2^128-255`, subgroup
  divisibilities, all four saturation binomials `C(128,k+1)` exact and
  under budget.
- **Four length-512 paving numerators** ((2.6) and the circle rows'
  CP2): all four floor-divided binomial ratios exact, min against
  `C(512,a)` never binding, beyond-Johnson `kn > a^2` in all four.
- **Circle certificate rows** (prop:paving-circle-certificate,
  L3543-3585): Lucas-Lehmer for `2^127-1` replayed, budget
  `floor(q/2^128) = 2^126-1` exact, both numerators exact, proved bits
  128.068311 / 128.483942 reproduced to all six printed decimals.
- **RF1-RF7 conditional integers** (cor:retained-koalabear, L4825-4891):
  every printed integer (interpolation margins, RF2 top margins, rank
  margins, all four retained numerators, budget), security bits and
  tangent gaps to all printed decimals. Arithmetic only — the paper
  itself says these are conditional on `ass:retained-factor-lift`, and
  correctly so.
- **Mersenne-circle bonus rows** (cor:mersenne-circle-rows, L3710-3719):
  budget `floor((2^31-1)^5/2^128) = 2^27-1` and both quadratic margins
  (SC4 `162129591417176068`, SC5 `18014401193836548`) exact, endpoint
  identities included. With these, a sweep shows every printed integer of
  >= 11 digits in the 5290-line tex is covered by some check.
- **All five SHA-256 digests** in `REPRODUCIBILITY_v8.md` match the
  in-tree release files; both tex copies are byte-identical; the pinned
  proof-development commit `02728b2` exists.

**The DP1 coverage gap, closed.** The paper's most deployment-relevant
claim, prop:deployed-prefix-attacks (tex L2549-2588), is covered by
**neither** bundled script: the tex's own script-coverage list
(L4909-4914) routes the paving/saturation/circle/primality/budget checks
to `verify_paving_mca_v8.py` and the retained-lift arithmetic to
`verify_retained_bchks_v8.py`, and the DP1 values are described only as
"direct evaluations" (L4921-4922). This replay confirms both rows three
ways — (i) Legendre + product-tree binomials with an exact 24-step
ratio-stepping cross-tie between the two rows' binomials, (ii) the
`math.comb` route (KB `a0` binomial, 2,090,874 bits, bit-length tied in
the script), (iii) the in-tree frozen floors of
`experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json`
(all eight integers identical; margin pairs +8.9777/-22.1969 and
+27.9270/-3.2589 reproduced):

| row | `B*` | `M(L_{a0})` | `M(L_{a0+1})` | margin |
| --- | --- | --- | --- | --- |
| KB `p^6`, `2^-128` | 274980728111395087 | 138634741058327852652 | 57198030366 | +8.9777 bits |
| M31 `(2^31-1)^4`, `2^-100` | 16777215 | 4281388998575706 | 1752700 | +27.9270 bits |

A cheap upstream improvement: the four `M(L_a)` evaluations (~15 lines;
the binomials cost seconds via Legendre + product tree, in-tree pattern in
`experimental/scripts/verify_pf_deployed_rows.py`) would close the only
printed-integer gap in the release's self-verification if added to
`verify_paving_mca_v8.py`. Our `verify_rs_mca_paving_v8_audit.py` has
them as named checks and can be cribbed directly.

## 2. The provenance finding (CONFIRMED; the one pre-upload item)

**Summary.** The paper's only imported input — BCHKS ePrint 2025/2055
Theorem 4.6, specialized to `M=1` — carries a one-paragraph proof sketch
in its source, at every `M` including `M=1`; three unconditional-section
passages of v8 present it as settled proved prior theory. The
transcription and normalization of the import are exact (no mathematical
defect), the blast radius is correctly scoped by the paper's own remark,
and either of two cheap fixes resolves it with all results surviving.

**Source facts** (pinned ingest of ePrint 2025/2055, sha256
`4added3e55b8...`, Section 4.3, pp. 28-29; quotes verified against the
ingest):

- The only proof text for Theorem 4.6 is the paragraph beginning "The
  proof of Theorem 4.6 generalizes Section 3.2 as follows. Instead
  focusing on a single 'useful' factor of [Q(X,Y,Z) = C(X,Z) prod_i
  R_i(X,Y,Z)] (for simplicity we restrict to the separable case) ..." and
  ending "... the remaining non-useful factors cover few proximates by
  definition." That paragraph is the entire proof, for every `M`
  including `M=1`; there is no displayed/sketched divide with `M=1` on a
  proved side.
- The section's own preamble defers: "For Reed-Solomon codes it has been
  conjectured to hold up to the Johnson bound [ACFY25, Conjecture 4.12];
  a proof of it, which generalizes the decoder analysis from [BCI+20] is
  discussed in [Hab25]." The same preamble records that proof-complete
  list-CA stops at the double-Johnson bound (Zei24) and one-and-a-half
  Johnson (GKL24).
- The source's organization paragraph books Sections 2-3 as proving
  Theorems 1.3/1.5, while Section 4 (home of Thm 4.6) "discuss[es]" the
  translations.

**Paper passages, exact lines** (verified against the tex blob
`dd936a52...`):

- **L313-315** (unconditional intro): "the proved positive theory has a
  linear bad-slope numerator on every compact subinterval below the
  Johnson radius". The linear below-Johnson *mutual* numerator is not
  proved in any public text we could locate (the proved substrate is the
  quadratic mutual event; see the swap option below). This is the
  sentence a referee checking 2025/2055 will quote.
- **L751-760** (rem:bchks-theorem46-provenance): "Its source gives the
  displayed theorem and then sketches the list-correlated-agreement
  generalization." Read together with L318-320 ("we use only its
  displayed `M=1` specialization"), this places the `M=1` case on the
  proved side of a displayed/sketched divide; in the source, the sketch
  *is* the proof of the displayed theorem at every `M`.
- **L382** (novelty table): "Linear MCA bound below Johnson & prior" —
  contrast the same table's honest "conditional" cell for the retained
  appendix at L393-395.

**The asymmetry against the paper's own standard.** Appendix A holds
itself to: "Because that combined statement is not printed verbatim in
either source, we isolate it as an assumption instead of silently
promoting the synthesis to a theorem" (L4764-4768). Theorem 4.6 receives
softer treatment than that standard on the same kind of question.

**Blast radius — correctly scoped by the paper itself.** Only eq (1.13)
(L714-723), the below-Johnson branch of thm:intro-exponential-frontier,
and the below-Johnson limit of cor:intro-security-exponents depend on the
import; the remark at L751-760 already says exactly this. **No finite
certificate, prize row, paving/circle result, or Appendix-A row depends
on it** (verified: the prize rows use the quadratic `F_{n,k}`; the paving
script's Johnson comparisons are geometric `kn > a^2` checks with no
Thm 4.6 numerics).

**The normalization itself is exact.** Eq (1.13) matches the source
statement verbatim at `M=1`: bound, `t = m + 1/2`,
`m = max(ceil(sqrt(rho)/(1-sqrt(rho)-gamma)), 3)`, the degree-parameter
to dimension reindexing `rho_n^- = (k_n-1)/n`, and it correctly uses
Thm 4.6's `m` (not Thm 1.5's factor-2-smaller one). There is no
constant-mismatch defect of the err*-factor-3 class here.

**Two fixes, either sufficient, both cheap:**

1. **Textual reword** (no restructuring): L313-315 "proved positive
   theory" -> "stated positive theory" (or "linear bad-slope numerator
   stated in BCHKS, with proof sketched in the source"); add to
   rem:bchks-theorem46-provenance that the source's proof of Theorem 4.6
   is a sketch even at `M=1`; table cell L382 "prior" -> "prior statement
   (proof sketched in source)". Optionally qualify the abstract's
   Johnson-range phrase the same way, or move the below-Johnson branch to
   the Appendix-A conditional tier.
2. **Import swap**: replace the load-bearing citation with the proved
   quadratic mutual event (Haboeck, ePrint 2025/2110; also BCGM25,
   published). The two affected asymptotic results need only a `poly(n)`
   mutual numerator below Johnson (zero base-two exponent), which the
   quadratic bound supplies — both survive verbatim, and Theorem 4.6 can
   remain cited as the sharper stated route.

Consistent with this repo lineage's earlier import audit of the same
theorem (`notes/audits/audit_bchks25_thm46_conditional_johnson_import.md`
and our banked gap-G4 audit): same conclusion, now load-bearing because
the submission books it in unconditional prose.

## 3. Tightness observation: the M31 ceiling collapse (not a defect)

The printed DP1 values `M(L_a)` equal `L_a` because the ceiling of
eq (4.2) collapses; the exact collapse condition is `k(L-1)^2 < q - n`
(from `(L-1)(q-n+k(L-1)) < L(q-n)`). At the KB `a0` cell this is
comfortable (`2.0153e46` vs `9.3571e55`). At the **M31 `a0` cell it is
tight**: `k(L-1)^2 = 1.9221e37` vs `q - n = 2.1268e37`, ratio 0.9038 —
about 10% headroom. The inequality is verified exactly (named check
`M31-A0-CEILING-COLLAPSE-INEQUALITY` in the replay script). A modestly
deeper re-tuned radius would make `M < L` and invalidate the
printed-equals-`L` shortcut; any future re-tuning of the M31 row should
re-verify this inequality rather than assume `M = L`.

## 4. Minor items and proof spot-audit summary

**F2 (one-sentence definitional fix).** thm:intro-paving (L437) is stated
for "a linear `[n,k]` MDS code" and thm:exact-sparsification (L923) for
"every linear code", but the operative definitions are RS-specific:
def:explanation (L816-828) defines explanation via `ev_S(f)`,
`f in F[X]_{<k}`, under the Section-2 preamble `C = RS_F(D,k)`
(L810-811); def:mca-bad (L834) and def:ca-sparse-numerators (L900)
inherit this, while the proofs use the general reading
`u|_S in C|_S` (e.g. L1214). No mathematical gap — the two notions
coincide for RS and every proof step is representation-free — but
`B^MCA` is formally undefined for a non-RS MDS code as written. Fix:
state explanation as `u|_S in C|_S` for general linear `C`, with the RS
evaluation form as the special case.

**REPRODUCIBILITY nits (LOW, documentation only).**

- Line 9 of `REPRODUCIBILITY_v8.md` says `verify_paving_mca_v8.py` checks
  "... field-budget, and retained BCHKS comparisons"; the paving script
  contains no retained-appendix checks (those live only in
  `verify_retained_bchks_v8.py`). The tex's own description (L4909-4914)
  has the split right. One-word fix.
- The doc pins Python 3.12; both scripts also pass under 3.9.6 (stdlib
  only). No issue — informational.

**Proof spot-audits (adversarial replay; all survive).**

- thm:intro-paving: the augmented-matroid paving property, the
  parity-functional double count, and the CA <= MCA subclass step are
  airtight, including lem:paving-bases' induction and the per-slope
  charging uniqueness.
- thm:exact-sparsification: the identity holds in both directions with
  the boundary cases (`a = n`, `a <= k`) consistent under the stated
  conventions; the adjacent exact-half-distance theorem also replays.
- thm:official-saturation + the four saturated rows: endpoint bookkeeping,
  the `a = k+1` numerator, and the exact budget equivalence all confirm.
- prop:paving-circle-certificate: confirmed end-to-end at the paper's
  parameters — twin-coset hypotheses (`g^2 not in H`,
  `ord(g) = 2^127` not dividing `2^10`, the all-scale condition), the
  2:1 projection, both rows' numerators, budgets, and bits.
- thm:intro-exponential-frontier: structure sound (regime boundaries,
  envelope, Stirling exponent) modulo the Section-2 import, and it
  survives with the proved quadratic import.

## Self-Red-Team

- *Could the sketch-status assessment itself be stale?* The audit is
  against the pinned 2025/2055 ingest (sha256 `4added3e55b8...`). If a
  revised ePrint version has since added a full Section-4 proof, the
  finding downgrades to citation hygiene (cite the revision); the
  pre-upload recommendation is unchanged (re-pin and cite whichever
  version carries the proof relied on).
- *Is the paper hiding the sketch?* No — L318-320 and the remark disclose
  a sketch exists. The finding is narrower: the specific words "proved
  positive theory" (L313), the table cell "prior" (L382), and the
  displayed-vs-sketched framing (L751-760) go beyond that disclosure,
  because the sketch covers the displayed theorem itself at `M=1`.
- *Could the "not proved anywhere" claim be too strong?* We verified the
  source's own deferral (Conjecture 4.12 / Hab25) and our prior deep
  audit of Hab25 = ePrint 2025/2110 (proves the quadratic `M=1` mutual
  event, defers the linear one). We do not claim a literature-exhaustive
  search; the Use Rule below is phrased accordingly.
- *Collapse condition form.* The audit lane originally printed the
  denominator `q-n+k(L-1)` next to `k(L-1)^2`; the exact iff-condition
  for `M = L` is `k(L-1)^2 < q-n` (derivation in Section 3). At these
  magnitudes the two readings agree (the `k(L-1)` term is ~1e21 against
  ~1e37); the script checks the exact form *and* recomputes `M` by
  direct ceiling, so the verdict does not depend on the algebra note.
- *Check-count drift.* The audit lane's independent recomputation was
  176 checks; the committed port prints 186 (it adds the named collapse
  checks, the frozen-floor cross-ties, SC4/SC5, and the digest section,
  and folds primality to one deterministic stdlib route (dropping the audit lane's sympy second route)). Same coverage,
  strictly larger; exit 0 requires all of them.

## NON-CLAIMS

- No claim about the paper's novelty, the Proximity Prize criteria, or
  the committee's standards — only replay and provenance.
- No claim that BCHKS Theorem 4.6 is false, nor that its sketch cannot be
  completed: we verify its **proof status in the pinned source**, not its
  mathematical truth.
- Section (D) of the replay verifies conditional arithmetic only; it does
  not discharge `ass:retained-factor-lift` (neither does the paper claim
  it does).
- No paper `.tex` was edited; the two fix options in Section 2 are
  recommendations for the maintainer, verbatim-ready but not applied.
- The proof spot-audits are targeted adversarial replays of the load-bearing
  mechanisms, not a line-by-line formalization of the 53 pages.

**Use Rule.** Until the Section-2 reword or import swap lands in the tex:
downstream material must not cite eq (1.13), the below-Johnson branch of
thm:intro-exponential-frontier, or the below-Johnson limit of
cor:intro-security-exponents as resting on *proved* prior theory — cite
them as resting on the *stated* BCHKS Theorem 4.6 (proof sketched in
source), or route through the proved quadratic mutual event (Hab25
2025/2110 / BCGM25). Everything else in the paper — every finite
certificate, prize row, paving/circle/saturation result, and the DP1
deployed rows — may be cited as independently replay-confirmed at tex
`dd936a52...` per this note, subject to the M31 collapse-inequality
re-check on any radius re-tuning.

**Verification:** `python3 experimental/scripts/verify_rs_mca_paving_v8_audit.py`
(exit 0, 186 checks). Both bundled release scripts also pass as shipped.
