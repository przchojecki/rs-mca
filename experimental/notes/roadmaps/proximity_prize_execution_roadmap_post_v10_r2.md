# RS-MCA to Proximity Prize: Execution Roadmap Post-v10 (r2)

- **Status:** AUDIT / proposed working roadmap, revision 2. Top-down planning
  artifact: this document is the root of a refinement tree, not a results claim.
- **Provenance:** r1 was drafted by Codex (normalized from a Claude/Fable
  discussion). This r2 is authored by Claude (Fable 5) acting for
  AllenGrahamHart; it is self-contained and does not require r1 to read.
- **Baseline:** `main @ 495ee489` ("Sync guides and site to Paper D v12",
  2026-07-01), plus open PRs #170, #171, #172.
- **Non-supersession:** `towards-prize.md` remains the maintainer's source of
  truth. This note is an execution scaffold under it.

## 0.0 What r2 changes relative to r1

1. **New structural section §1.2:** the open prize band is *entirely
   underdetermined* for every official rate (exact arithmetic, not opinion).
   Consequence: a dedicated underdetermined work package (WP-2.6, running as
   PR #172) joins the critical path, and the r1 assumption that regular-window
   machinery "transfers" to prize-scale rows is downgraded to a named risk.
2. **Integration is maintainer-gated.** r1's "integrate PR #170/#171" becomes
   WP-0.3 "integration-readiness audits": agents prepare replays and spot
   verifications; only the maintainer integrates.
3. **Fronts alpha/beta are gated on independent replay** of their defining
   objects (they currently live in unreviewed mega-PRs), not just on the PRs'
   own verifiers.
4. **WP-0.1 is seeded, not started fresh:** the step-1 sampler reconciliation
   (`audit_step1_sampler_reconciliation.md`) and the M0 freeze (PR #171)
   already cover most axes; the reconciliation note extends them.
5. **WP-4.3 status corrected:** the BETA_2 wall freeze + consumer theorem
   essentially exist (`m1_beta2_conditional_close.md`); the remaining work is
   scans / density routes / expert handoff, not the freeze.
6. **WP-1.1 exit is recorded as nearly satisfied:** two independent replays of
   the 506/507 numerators already exist on main (#147 package, #148 checker).
7. **Every work package now prints assets** (existing repo files) **and an
   executability tag** (`AGENT` / `MAINT` / `EXPERT`).
8. **Two standing orders added:** print the delta-regime of every safe-side
   lemma (below-regular / regular / in-band / near-cap), and replay-before-build.
9. **Refinement protocol added (§0.1):** this roadmap is the root of a
   top-down decomposition; leaves are refined in per-WP detail notes until they
   meet an explicit DONE-definition.

## 0.1 Refinement protocol (how this plan gets finer)

Working split: the bottom-up lane (Codex) proves one lemma at a time toward
the result; this lane works top-down, decomposing the prize into successively
finer, well-posed pieces until each leaf can be handed to a prover or a
scriptable verifier. The two lanes meet in the middle.

Levels:

```text
L0  the prize equation and decided/undecided regions        (this file, SS1)
L1  programs P0..P7                                          (this file, SS3)
L2  work packages with goal/assets/exit/tag                  (this file, SS4)
L3  per-WP detail notes: pinned statements, lemma DAG,
    proof-or-computation route, acceptance tests,
    failure branches                                         (wp_detail/*.md)
```

**A leaf is DONE (as a plan item) when it has:**

```text
(a) pinned notation and an exact mathematical statement;
(b) a proof-or-computation route with named prerequisites;
(c) an acceptance test a verifier script can run;
(d) a failure branch (what the plan does if the statement is false);
(e) an executability tag: AGENT / MAINT / EXPERT.
```

Detail notes live in `experimental/notes/roadmaps/wp_detail/`.
**REFINEMENT COMPLETE (2026-07-02):** every work package below has an L3
detail note meeting the DONE-definition, and the mathematical spine lives
in `proof_sketch/` (12 files: the heuristic path-chart, prediction ledger,
and minimal win set). The full map:

```text
WP    -> detail note (wp_detail/)                | math content (proof_sketch/)
0.1   -> wp_consolidation_sketch_extracts.md     | s5_s0 §4 (normative ledger)
0.2   -> wp0_2_wp4_4_rules_freeze_and_dither.md  | (live-fetch grounded)
0.3   -> wp0_3_wp0_4_replay_and_harness.md       | —
0.4   -> wp0_3_wp0_4_replay_and_harness.md       | s8_s9 §1 (refusal rule)
1.1   -> wp1_1_wp1_2_submission_and_lean.md      | s2 (two-regime picture)
1.2   -> wp1_1_wp1_2_submission_and_lean.md      | (addition certificates)
2.1   -> wp_consolidation_sketch_extracts.md     | s3a §3 (P1a/b/c)
2.2   -> wp_consolidation_sketch_extracts.md     | s3a §4 (codim argument)
2.3   -> wp2_3_stratification_case_tree.md       | s3b_ii (strip)
2.4   -> wp_consolidation_sketch_extracts.md     | s2 §5 (Paid spec)
2.5   -> wp2_5_wp4_1_window_charts_and_displacement.md | s3a (aperiodic-0)
2.6   -> wp2_6_underdetermined_program.md        | s3b_iii_1 (SPI dim 1)
3.1   -> wp3_1_wp3_3_rows_and_second_pin.md      | s2/s6 (slate numbers)
3.2   -> wp3_2_symbolic_scaling.md               | s4 (parametric formulas)
3.3   -> wp3_1_wp3_3_rows_and_second_pin.md      | s8_s9 §3 (win set)
4.1   -> wp2_5_wp4_1_window_charts_and_displacement.md | s3b_iii_2 (V^T D V)
4.2   -> (r2 WP-4.2 + s3b_iii walls)             | s3b_iii_1/2 + Graver note
4.3   -> (r2 WP-4.3, freeze exists on main)      | BETA_2 conditional close
4.4   -> wp0_2_wp4_4_rules_freeze_and_dither.md  | s5_s0 (hypothesis table)
5.1   -> wp_consolidation_sketch_extracts.md     | s7 §4 (petal battle)
5.2   -> wp5_2_wp6_2_wp6_3_bridges.md            | s7 §3 (per-m budgets)
6.1   -> (r2 WP-6.1)                             | s6 (classification)
6.2   -> wp5_2_wp6_2_wp6_3_bridges.md            | s4 (dictionary)
6.3   -> wp5_2_wp6_2_wp6_3_bridges.md            | (ledger spec)
7.1   -> wp_consolidation_sketch_extracts.md     | s8_s9 §1 (contract)
7.2   -> wp7_2_wp7_3_wp7_4_promotion_gates_dossier.md | —
7.3   -> wp7_2_wp7_3_wp7_4_promotion_gates_dossier.md | (G1-G5)
7.4   -> wp7_2_wp7_3_wp7_4_promotion_gates_dossier.md | s8_s9 §3 (ladder)
(4.2/4.3/6.1 carry their L3 content in the r2 body + sketch walls: the
freezes exist — m1_beta2_conditional_close on main, the Graver dichotomy
note on main, s6's classification — no separate file needed.)
```

**The unbroken chain, start to prize:** rules freeze + object audit
(0.2/0.1) -> replay + harness (0.3/0.4) -> ship v-PARTIAL (1.1/1.2) ->
proving-ground campaign (2.1-2.5, predicted aperiodic-0) + deficiency
ladder (2.6, tests SPI at dim 1) -> slate rows + Row-C measurement
(3.1-3.3, the first zone-(b) data) + symbolic scaling (3.2) -> the walls
(4.1-4.3) and the minimal win set {R2, zone-(b), S0} -> list side
(5.1/5.2, a-regularity priced) -> bridges (6.1-6.3) -> compiler +
promotion + dossier (7.1-7.4, v-INTERIM then v-FULL). Negative branches
land in named postures throughout (s8_s9 §4); the one non-determination
scenario is exactly the unresolved minimal win set.

## 1. Ground Truth

The Proximity Prize asks for thresholds for smooth-domain Reed-Solomon rows

```text
C = RS[F, D, k],  rho in {1/2, 1/4, 1/8, 1/16},  k <= 2^40,
|F| < 2^256,      epsilon* = 2^-128.
```

Repo-internal threshold form (adjacent-pin):

```text
B_C(a0)     >  B*(q_line) = floor(q_line / 2^128)     unsafe
B_C(a0 + 1) <= B*(q_line)                              safe
```

with the master safe-side decomposition

```text
B_C(a) <= B_tan(a) + B_quot(a) + B_ap(a) + B_ext(a)
```

each term deduplicated and divided by the printed denominator. Every note
prints: object, sampler (finite affine vs projective), `q_gen / q_line /
q_chal`, agreement/radius endpoints, closed-grid vs supremum.

Pinned row constants (verified on main):

```text
C = RS[F_17^32, H, 256], |H| = 512 (the full 2-Sylow), n = 512, k = 256
B* = floor(17^32 / 2^128) = floor((17^32 + 1) / 2^128) = 6
LD_sw(C,506) = 7 unsafe ; LD_sw(C,507) = 6 safe   (row already pinned)
regular overdetermined branch:  2A >= n+k+1 = 769  <=>  A >= 385
tangent exactness: A >= 427 ; M3 window: 385 <= A <= 426
minor size j+1 runs 128 down to 87 ; degree-only window sum = 4515 >> 6
first underdetermined agreement: A = 384 (t = j = 128, deficiency 1)
```

Two framing facts. (i) The unsafe half is largely done (Papers A/B floors,
Paper D caps); the missing half is safe-side machinery below the caps,
especially `B_ap`. (ii) The repo object and the official ABF object are not
yet certified to coincide; the M0 freeze deliberately leaves external sampler
reconciliation open. **Object reconciliation is a gate, not packaging.**

By monotonicity the 506/507 transition already pins the `F_17^32` row, so all
n=512 window work (M3 and below) is methodology development on a controlled
proving ground — valuable exactly insofar as it transfers.

## 1.2 Where the prize band lives (new in r2)

The regular/overdetermined branch exists iff `t >= j+1`, i.e.
`delta = r/n <= (1-rho)/2` (up to the 1/2n grid term). The open prize band
sits between the Johnson radius `J = 1 - sqrt(rho)` and the Paper D cap
`~ 1 - rho - 2^-9` (`2^-10` at rho=1/16). The gap is exact and universal:

```text
J - (1-rho)/2 = (1 - sqrt(rho))^2 / 2  >  0        for every rho != 1.
```

Per official rate:

```text
rate    regular ends   Johnson J   cap (approx)   t/(j+1) at J
1/2     0.25000        0.29289     0.49805        0.707
1/4     0.37500        0.50000     0.74805        0.500
1/8     0.43750        0.64645     0.87305        0.354
1/16    0.46875        0.75000     0.93652        0.250
```

So: **the regular branch never reaches the band, for any rate.** At the
Johnson radius the Hankel system is already underdetermined with
`t/(j+1) ~ sqrt(rho)`; at the cap, `t` collapses to `~ n * 2^-9`. For a
prize-scale row (`q_line` near `2^256`, `B* ~ 2^128`) the tangent numerator
`n-a+1 <= 2^41` never bites, and no current safe-side theorem reaches ANY
delta beyond the tangent regime; every candidate transition location lies in
or near the band — underdetermined territory. This row's own in-band exemplar
is `A = 265` (`delta ~ 0.482`, `t = 9`, deficiency 239) — the known hard-core
instance.

Consequences for sequencing:

```text
1. P2 (regular window) is a proving ground for stratification style,
   chart bookkeeping, and packet format — not the machinery that will
   decide any prize-scale transition.
2. The machinery that faces the band is the underdetermined chart program:
   WP-2.6, starting at deficiency 1 (A=384) and descending the deficiency
   ladder, feeding P3 (symbolic scaling) and P4 (uniform theorem).
3. "P2 transfers to P3" is therefore a RISK to manage (see SS6), not an
   assumption to rely on.
```

## 2. State Snapshot

**Main at baseline.** Paper D v12: universal + first-grid caps; quotient
support/image/dual-cosupport ledgers; extension-pole floor; canonical
regular-Hankel gcd/lcm ledgers; aperiodic chart atlas.
`towards-prize.md` milestones: M0 freeze supplied by PR #171 with external
reconciliation open; M1 schema checker done; M2 smoke row done; M3 window in
progress; M4 table not complete; M5 narrowed, not complete; M6 not started.

**Open PR #170** (synthetic low-rank / spectral lane): ranks 2..12 closed for
the checked family (affine gcd 0 roots; endpoint `[0:1]` quotient-image paid;
paid-residual ledger closes); spectral reduction
`det(H_X + Z H_Y) = det(V_X)^2 prod(x)^h det(I + Z K_h)` with explicit
Lagrange/Cauchy kernel, Toeplitz-Cauchy displacement rank 1; explicit open
target `gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1` for `87 <= m <= 128`,
`2 <= r <= ceil((m-1)/2)`; frontier probe A=426 ranks 13..20 gcd degree 0.

**Open PR #171** (M3/M4 chart-atlas + lemma kit + M0 freeze): subgroup
syndrome-section theorem; canonical/contiguous gcd formula theorems;
one-spike and uniform families; M4 budget split; direction-rank degree cap;
**rank-6 ambient sharpness** (six finite roots + one projective endpoint can
coexist in the ambient pencil class); affine-pivot compression and
gcd-equivalence; M5 kernel charts; **null-polynomial split-locator gate**
(ambient root tables are safe upper bounds; true witnesses must pass
`L | X^512 - 1` and the noncontainment gate).

**Open PR #172** (this lane, M5/WP-2.6): A=384 bucket identified — `t = j =
128`, matrix `128 x 129`, deficiency 1, regular certificate structurally
vacuous (kernel nontrivial at every slope); exhaustive F_13 toy dichotomy;
Cramer/divisibility chart program declared (detail: wp_detail/wp2_6).

**Live fronts.**

```text
alpha  spectral disjointness  gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1   (PR #170)
beta   rank-6 endpoint-sensitive boundary closure                  (PR #171)
gamma  underdetermined deficiency ladder, rung 1 = A=384           (PR #172)
```

## 3. Critical Path

```text
P0  governance gates [AGENT prep, MAINT execute]:
      WP-0.1 object reconciliation ; WP-0.2 rules freeze ;
      WP-0.3 integration-readiness audits ; WP-0.4 verification harness
P1  finite-row partial package [AGENT]: WP-1.1 submission note ; WP-1.2 Lean gates
P2  regular-window proving ground [AGENT]:
      WP-2.1 alpha ; WP-2.2 beta ; WP-2.3 stratification ;
      WP-2.4 M4 table ; WP-2.5 window residual charts
P2.5 underdetermined program [AGENT, running]: WP-2.6 deficiency ladder
P3  prize-scale rows [AGENT]: WP-3.1 row selection ; WP-3.2 symbolic scaling ;
      WP-3.3 second pin or named wall
P4  walls + uniform theorem: WP-4.1 displacement uniformization [AGENT] ;
      WP-4.2 Graver wall [AGENT freeze] ; WP-4.3 BETA_2 wall [EXPERT + AGENT scans] ;
      WP-4.4 hypothesis/dither table [AGENT]
P5  list lane [AGENT]: WP-5.1 L1 ImgFib bound ; WP-5.2 L2 constants
P6  bridges [AGENT]: WP-6.1 F1 classification ; WP-6.2 M2 statements ; WP-6.3 X1 ledger
P7  assembly: WP-7.1 compiler [AGENT] ; WP-7.2 promotion [MAINT] ;
      WP-7.3 formal gates [AGENT] ; WP-7.4 dossier [AGENT draft, MAINT sign-off]
```

Sequencing rules:

```text
P0 gates all prize-facing packaging (not all mathematics).
P1 runs now; it consumes settled material.
P2 and P2.5 run in parallel; P2.5 is the piece that faces the band,
P2 is the cheapest place to develop shared stratification style.
P3 consumes BOTH P2 and P2.5; P4 consumes P3; P5/P6 run parallel to P2-P4.
P7 last, gated by P0.
```

## 4. Work Packages

Format: goal / assets already in repo / exit test / tag. Detail notes under
`wp_detail/` refine to L3 (statements, lemma DAG, acceptance tests, failure
branches). Only WP-2.6 is refined so far; the queue is in §0.1.

### WP-0.1 Object Reconciliation [AGENT]
Goal: prove, or bridge with printed losses, repo support-wise `B_C(a)` vs
official ABF `epsilon_mca`. Axes: batching shape; `ell > 2` batching;
quantifier order; same-support noncontainment predicate; finite vs projective
sampler; `q_gen/q_line/q_chal`; closed-grid vs supremum.
Assets: `audit_step1_sampler_reconciliation.md` (4-PASS verifier; unambiguous
rows verified, two residual axes named), M0 freeze note (PR #171), #147 anchor
imports (SHA-256 + line numbers).
Exit: every axis `EQUAL` / `BRIDGED(loss printed)` / `OPEN`; zero `OPEN`
before any prize-facing claim; any inequivalent axis becomes a ledger column.
Deliverable: `experimental/notes/audits/object_reconciliation_abf.md`.

### WP-0.2 Official Rules Freeze [AGENT]
Goal: freeze operative constraints from proximityprize.org + ePrint 2026/680:
field-range wording, fixed vs dithered `k`, per-row partial credit, submission
mechanics, "preliminary" status recheck cadence.
Deliverable: `experimental/notes/audits/prize_rules_freeze.md`.

### WP-0.3 Integration-Readiness Audits for #170/#171 [AGENT prep, MAINT executes]
Goal: independent replay of every verifier/certificate in both PRs;
re-derivation of the `Phi_{m,r,h}` definitions and the rank-6 sharpness
example from scratch; checker run against pre-existing packets; timestamped
agents-log merge plan. Integration itself is the maintainer's call.
Exit: replay note per PR with any divergence flagged; alpha/beta unblocked.

### WP-0.4 Verification Harness [AGENT]
Goal: `run_all_verifiers` entry point: discover deterministic verifiers,
check certificate hashes, run the packet checker, emit one PASS/FAIL table.
Checker hardening: removed-ledger refs resolve; declared numerators
recomputed; residual labels from the allowed set; object/sampler/denominator
blocks present; cross-packet paid-root dedup enforced as checker logic.
Assets: `scripts/check_aperiodic_eliminant_packet.py`, the `verify_*.py`
corpus, #148 independent GF(17^32) tower.

### WP-1.1 Pinned Finite-Row Submission Note [AGENT, post-WP-0.1]
Goal: package the 506/507 pin in repo and official language, with non-claims.
Assets: #147 threshold package, #148 independent checker (the two replays the
exit test asks for already exist), M2 smoke packet, step-5 envelope map.
Exit: two independent numerator replays agree (met); WP-0.1 axes referenced.
Deliverable: `experimental/notes/submission/f17_32_partial_note.md`.

### WP-1.2 Formalize Counting Core [AGENT]
Goal: Lean statements for the pinned-row finite certificates and 506/507
numerators. Constraint: repo Lean is stdlib-only (no Mathlib, deliberate);
scope to finite-certificate arithmetic, not tangent theory.
Assets: `experimental/lean/rs_mca_formalization/` (builds green; BetaTwo and
F1 ledgers exist).

### WP-2.1 Front Alpha: Spectral Disjointness [AGENT, gated on WP-0.3 replay]
Targets: alpha-strong `gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1` on the window grid;
alpha-weak all-contiguous gcd. Attack ladder: counterexample-first full-grid
scan (on replayed definitions); generalized-spectrum reformulation; resultant
route; moment-run rigidity; char-17 hygiene.
Failure branch: paid collision -> refine to paid-root gcd statement; unpaid
collision -> `candidate_new_obstruction` with minimal reproduction.

### WP-2.2 Front Beta: Rank-6 Endpoint Boundary [AGENT, gated on WP-0.3 replay]
Goal: for direction-rank-6 nonsingular buckets prove one of: compressed 6x6
root table within budget; all roots/endpoints paid; or a Hankel-realized
sharpness example, counted. First move: Hankel-realizability search for the
ambient sharpness example; if unrealizable, isolate and prove the Hankel
obstruction.

### WP-2.3 Syndrome-Space Stratification [AGENT]
Goal: partition syndrome pairs `(u,v)` per agreement into strata ending in
allowed labels (tangent-paid / quotient-paid / regular-closed / pivot-chart /
residual(named)). Axes: direction rank; zero-u/zero-v/proportional; tangent
overlap; quotient periodicity; lower-rank containment; kernel-containment;
split-locator gate. Exit: adversarial syndrome fuzz routes to leaves whose
predicted contribution is confirmed by direct computation on small instances.

### WP-2.4 M4 Deduped Assembly Table [AGENT]
Goal: script-generated table per exact agreement `A`: `B_tan`,
`B_quot_support`, `B_quot_image`, `B_ext`, `B_ap_regular`, `B_ap_pivot`,
deduped total vs `B* = 6`, lower bound, gap — with conditional cells while
alpha/beta are open. Dedup arithmetic checked, not trusted.

### WP-2.5 M5 Window Residual Charts [AGENT]
Goal: close every residual leaf in the pinned M3 window by affine pivots,
projective infinity, curve pivots, dimension-degree diagnostics, or named
residual. Exit: zero `unknown` leaves in the window.

### WP-2.6 Underdetermined Boundary Program [AGENT, RUNNING — PR #172]
Goal: safe-side machinery where `t < j+1`, i.e. where the band lives.
Rungs: (1) A=384 deficiency 1: Cramer-kernel parametrization, bivariate
candidate locator, divisibility filter `L_Z(X) | X^512 - 1`, chart eliminant
or identically-valid-pencil dichotomy, rank-drop and low-degree side charts;
(2) deficiency d small: pencil charts and elimination-degree growth law;
(3) symbolic form over abstract `2^s` subgroups (feeds WP-3.2); name the wall
where elimination stops being effective.
Assets: PR #172 turn 1 (bucket identification, toy dichotomy);
`m5_underdetermined_a384_pivot_packet.md`.
**Detail: `wp_detail/wp2_6_underdetermined_program.md` (L3, done).**

### Phase P2/P2.5 Exit Criterion
alpha and beta resolved either way; stratification note merged; M4 table
complete; every window residual named; deficiency-1 machinery delivered
(eliminant or certified obstruction) with the deficiency-growth law stated;
`experimental/notes/m1/f17_32_window_theorem.md` exists.

### WP-3.1 Prize-Scale Row Selection [AGENT]
Pick: one Prime192-class scanner row; one near the top of the field range;
one quotient-hostile stress row. For each, localize the transition window
using floors/caps/tangent — and print its `t/(j+1)` profile (per §1.2 it will
be underdetermined; this is the transfer test for P2.5 machinery).

### WP-3.2 Symbolic Scaling [AGENT]
Upgrade pinned-row lemmas to symbolic row descriptors: abstract order-`2^s`
subgroup hypotheses; characteristic exclusions; symbolic stratum descriptors;
non-enumerative root-counting; complexity bounds.

### WP-3.3 Pin a Second Row or Name the Wall [AGENT]
Second prize-scale pinned row, or a wall note with minimal toy reproduction
and explicit consumer theorem.

### WP-4.1 Uniformize Displacement Structure [AGENT]
State/prove the #170 displacement and spectral identities over any field with
an order-`2^s` root of unity, with characteristic exclusions.

### WP-4.2 Projection-to-Graver Wall [AGENT freeze]
Freeze the exact missing projection inequality
(saturation-vs-vertex-boundary-defect dichotomy); prove it, reduce it to
moment-run rigidity, or adopt a dithered retreat with printed costs.
Assets: `m1_full_overlap_low_tail_completion_projection_wall.md` (dichotomy
already recorded).

### WP-4.3 BETA_2 Wall [EXPERT handoff + AGENT scans]
Status correction vs r1: the freeze exists — `m1_beta2_conditional_close.md`
reduces `(BETA_2)` to `G_geom(F) >= SL_8` for an explicit rank-8 sheaf, with a
fully citable consumer chain and a proof that local/finite methods cannot
close it. Remaining: standalone conjecture note for an l-adic monodromy
expert; corroborating scans (moments at more primes, deck-trace `m+ - m-`
indirect routes); density-theorem literature pass.

### WP-4.4 Hypothesis Management and Dithering [AGENT]
Hypothesis-coverage table for every official rate and relevant `n`, dither
costs, official-rules status (consumes WP-0.2).

### WP-5.1 L1 Image-Fiber Local Limit [AGENT; hard math]
Use `ImgFib_U`, never raw `Fib_U`. Concrete open sub-battle already isolated
on main: the full-petal sunflower branch (`t >= 3` petals, cofactor excess
`d - ell -> infinity`) is populated (witnesses at `d-ell = 2, 5`) and the
exact-rank shortcut is route-cut; needed: a growth bound on full-petal extras
or the mixed-petal amplification theorem. `q_gen` printed in every
denominator; consumable by L2.

### WP-5.2 L2 Interleaved Constants [AGENT]
Consume L1 through the codegree reduction (Theorems A/B/C, proved, L1-free).
The reduction must never claim its own base-list input.

### WP-6.1 F1 Safe-Side Classification [AGENT]
Every genuinely F-valued bad line above the corrected reserve is covered by
extension/aperiodic ledgers, or bucket tables where it is not. Assets: v10
extension-pole floor; Lean F1 ledger; sigma=1 counterexample audit.

### WP-6.2 M2 Line-Decoding Statements [AGENT]
Convert pinned MCA thresholds to line-decoding language without denominator
drift. Assets: `m2_line_decoding_mca_bridge.md`.

### WP-6.3 X1 Bridge Ledger [AGENT]
One table per bridge in the submission chain
(`list <-> CA <-> MCA <-> LD <-> curve`): radius loss, field loss, sqrt loss,
support convention, sampler.

### WP-7.1 Assembly Compiler [AGENT]
Certificate compiler: row inputs + packet refs in; `a_safe/a_unsafe`,
per-ledger status, comparison vs `floor(q_line/2^128)` out. Refuses a verdict
if any needed ledger is conjectural, unless run in labeled conditional mode.

### WP-7.2 Paper Promotion [MAINT]
Stable packets promote from `experimental/` to Papers B/C/D only after
maintainer review.

### WP-7.3 Formal Gates [AGENT]
Priority: definitions and finite certificates; M4 dedup arithmetic;
highest-risk counting lemmas. Stdlib-only constraint per WP-1.2.

### WP-7.4 Submission Dossier [AGENT draft, MAINT sign-off]
Versioned: partial (pinned row) -> interim (+ window theorem + second row or
named wall) -> full (uniform theorem + list + bridges).

## 5. Standing Orders

1. Every safe-side claim is a v12 packet.
2. Counterexample-first scans before long proof attempts, when feasible.
3. Paid-root dedup is checker logic, not prose.
4. State new lemmas over abstract order-`2^s` subgroups when possible.
5. Do not optimize the pinned row threshold; it is already pinned.
6. One theorem-cluster per PR; no mega-PRs.
7. Every note prints object, sampler, denominators, endpoint convention.
8. Walls get frozen statements, consumer theorems, toy instances, and scans.
9. Never let a reduction claim its own input.
10. Log agent work in `experimental/agents-log.md`.
11. **Print the delta-regime of every safe-side lemma:** below-regular
    (`delta <= (1-rho)/2`), in-band (`J < delta < cap`), or near-cap — so
    proving-ground results are never mistaken for band results.
12. **Replay before build:** no front or WP may consume a definition or
    example that exists only in an unintegrated PR without an independent
    replay note.

## 6. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---:|---:|---|
| Repo object differs from official `epsilon_mca` | medium | fatal if late | WP-0.1 gates prize-facing packaging |
| Regular-window machinery does not transfer to the (underdetermined) band | the *absence of the regular branch in-band* is certain (§1.2); transfer of chart style is open | high | WP-2.6 ladder is on the critical path; WP-3.1 prints `t/(j+1)` profiles as the transfer test |
| Fronts alpha/beta defined only in unreviewed mega-PRs | medium | medium | standing order 12; WP-0.3 replay gates them |
| Front alpha false | medium | medium | counterexample-first; paid-collision fallback |
| Front beta sharpness Hankel-realizable | medium | medium | count it; a polynomial-size named stratum may be fine |
| Uniform theorem false as stated | open | high | negative-resolution path first-class |
| Elimination degree blows up along the deficiency ladder | medium-high | high | WP-2.6 rung 2 measures the growth law early; wall gets frozen + consumer theorem |
| Prize rules diverge from working regime | low-medium | high | WP-0.2 freeze + periodic recheck |
| Weak checker lets bad packets pass | medium | high | WP-0.4 hardening, corrupted-packet tests |
| Queue thrash from mega-PRs | high | medium | standing order 6; timestamped logs |
| Characteristic arithmetic bugs | medium | high | char-hygiene audits in alpha/WP-4.1 |

## 7. Immediate Queue (executability-tagged)

1. [AGENT] WP-0.3 replay audits for #170/#171 (unblocks alpha/beta honestly).
2. [AGENT] WP-0.1 object-reconciliation note, seeded from step-1 + M0 freeze.
3. [AGENT] WP-0.2 rules freeze note.
4. [AGENT] WP-0.4 `run_all_verifiers` + checker hardening.
5. [AGENT] Front alpha counterexample-first scan (on replayed definitions).
6. [AGENT] Front beta Hankel-realizability search (on replayed definitions).
7. [AGENT, running] WP-2.6 rung 1: Cramer lemma -> divisibility chart ->
   eliminant-or-obstruction -> packet (PR #172 turns).
8. [AGENT] WP-2.3 stratification case-tree v1 from the #171 lemma kit (post-replay).
9. [AGENT] WP-2.4 M4 table generator with conditional cells.
10. [AGENT] WP-1.1 finite-row submission note (post WP-0.1).
11. [MAINT] Integration decisions on #170/#171/#172 (agents supply the audits).
12. [EXPERT] WP-4.3 standalone SL_8 conjecture note handoff (agents draft).

## 8. Success Criteria

Delta over `towards-prize.md`:

```text
object-reconciliation note with zero OPEN axes
checker recomputes every numerator
window theorem with abstract-subgroup lemma index
underdetermined program: deficiency-1 packet delivered and the
  deficiency-growth law stated (the band-facing deliverable)
one prize-scale row pinned or one wall frozen as conjecture + consumer
dossier versioning with non-claims intact
```

Shortest current path:

```text
object reconciliation
  + replay audits for #170/#171
  + resolve alpha and beta
  + stratify the M3 window            (proving ground)
  + climb the deficiency ladder        (band-facing machinery)
  + window theorem + transfer test on a Prime192-class row
  + uniformize displacement identities + wall packages
  + L1/L2 and bridge lanes
  + assembly compiler, formal gates, dossier
```

Negative resolutions stay first-class: determining that the true threshold is
lower than hoped is still a resolution if floors, caps, and safe side meet
with certified adjacent agreement levels.
