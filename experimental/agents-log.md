# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, proof,
  heuristic, or computation
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-07-02 - Proof-sketch COMPLETE: final coherence pass (turn 13)

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/prize_proof_sketch_spine.md`
  (prediction ledger §7, one-paragraph summary §8, queue closed);
  `s2_paid_ledger.md` (corridor width corrected to per-rate values).
- **Status:** COHERENCE PASS — no new mathematics; the tree remains
  CONJECTURAL / SKETCH throughout, labels audited.
- **What is being added:** Terminal turn of the proof-sketch loop.
  Machine-checked: all cross-file references resolve; every node carries
  its status labels. Applied the s8_s9 fix-list: the s2 corridor width
  ("~1.5 grid steps") corrected to the verified per-rate values
  (2.17/2.00/1.12/1.67). Added to the spine: the prediction ledger
  (P1a/b/c, P-beta, P2-corrected, P3, P4, window-0 — each with its
  testing experiment and failure meaning) and the one-paragraph summary
  of the whole sketch. Tree totals: spine + 11 content files, 13 turns,
  every arithmetic claim machine-verified before commit, two
  self-corrections recorded en route (window m=1..t; P2 restated) plus
  one label-attribution correction (noanchor vs perfiber).
- **How it is useful:** The sketch is now a complete, internally
  cross-checked heuristic path-chart from the repo's proved results to a
  prize resolution, with the minimal win set isolated ({R2, zone-(b),
  S0 zero-OPEN} — one collision family plus care), falsifiable
  predictions wired to already-scheduled experiments, and every negative
  branch landing in a named posture.
- **What to do next:** Maintainer/author review of the tree; the
  experiments that test it are the WP-2.1/2.2 scans and the resumable
  PR #172 deficiency ladder; the two definitional audits (S0 axes 1/2/4)
  and two rules lookups (generating, dither) are care-not-mathematics.

### 2026-07-02 - Proof-sketch S8+S9: assembly contract and negative branches

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s8_s9_assembly_and_negative.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** consolidation + verified arithmetic; the §4 bet is labelled
  LOW-CONFIDENCE SKETCH. No result claimed.
- **What is being added:** Turn 12, the last content node. (1) The
  assembly compiler contract: gates (both, always), generating check,
  Paid(A) with interval cells, four verdict classes with the exact
  condition set H6 printed, refusal rule; the compiler IS the uniform
  theorem in executable form. (2) Unconditional coverage today, verified:
  every admissible row with q_line up to ~2^128 (n-k)/3 is already pinned
  (log2 q <= 166.4 at n = 2^41) — the remaining prize content is a ~90-bit
  band of field sizes. (3) Minimal win conditions: {R2, zone-(b),
  S0 zero-OPEN} for grand MCA (+L1 at reserve and a-regularity-or-B<=1.6
  for grand list) — at bottom ONE collision family plus care. (4) The
  consolidated negative-branch table (every fork from turns 1-11, one
  line each); the single genuinely bad scenario is zone-(b) unresolved AND
  R2 unproven, leaving delta* bracketed at verified corridor widths
  2.17/2.00/1.12/1.67 grid steps — a bracket does not win a determination
  prize. (5) Handoff fix-list for the final coherence pass (s2 corridor
  width correction, cross-ref and label audit, prediction ledger).
- **How it is useful:** Turns eleven nodes of sketch into one executable
  decision procedure with named upgrade conditions, and states exactly
  how much of the prize is already resolved (in field-size terms).
- **What to do next:** Turn 13 (terminal): the FINAL coherence pass over
  the whole tree, then flag for review.

### 2026-07-02 - Proof-sketch S5+S0: per-rate theorem shapes and object axes

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s5_s0_statements_and_object.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** consolidation of verified constants + CONJECTURE-level
  theorem shapes + audit ledger. No result claimed.
- **What is being added:** Turn 11. (1) Master per-rate table re-derived
  and consolidated with the verified ordering list_lo < quot < tau* =
  list_hi < cap at every rate (the list window's upper end coincides with
  tau*). (2) The Grand MCA per-rate theorem written as it would be
  submitted: hypothesis block H1-H6 (exact dyadic rate, generating,
  conventions, quotient profile, the unproved core) and the conclusion
  delta* = 1 - rho - c_rho/log2(q_line) with the bracket; what is
  unconditional today listed (pinned row, qcore unsafe half, cap).
  (3) Hypothesis pricing: exact rates force 2-power k, making quotient
  structure MAXIMAL (adversarially richest point); if WP-0.2 finds dither
  latitude the dyadic quotient-core mechanism dies and roughly half the
  reserve swings on a rules question (fork F2 — the sketch's single
  largest sensitivity). Projective-gate +1 edge case demonstrated
  (q = 3*2^128 - 1). (4) S0 ledger: axes 3/5/7 verified, 6 dictionary
  done, 1/2/4 open definitional audits, 8/9 new rules lookups; zero-OPEN
  remains the prize-facing gate.
- **How it is useful:** Gives the program its submission-shaped target
  statements with every hypothesis priced, and isolates the one
  non-mathematical lever (dither) that moves the answer most.
- **What to do next:** Turn 12: S8/S9 (assembly compiler contract +
  negative-branch bookkeeping), then the final coherence pass.

### 2026-07-02 - Proof-sketch S6: the extension lift imports the list threshold

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s6_extension_lift.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** PROVED-cited floor + verified arithmetic + classification
  CONJECTURE. No new theorem claimed.
- **What is being added:** Turn 10. (1) The trivial half: B-rational
  pencils only produce B-slopes (linearity), so genuinely F-valued bad
  slopes need F-valued words or the pole mechanism. (2) Verified: the v10
  extension-pole numerator N(L) ~ L below saturation (~2^216), so B_ext
  crosses the MCA gate exactly when the base list crosses 2^128 — the
  extension mechanism IMPORTS grand challenge 2's threshold window
  (S7: [H/256, H/128]) into grand challenge 1's ledger, and binds where
  live. (3) Verified: it is live only for NON-generating rows, and
  admissibility forces those tiny (q_gen = q_line^{1/m} < 2^128; base
  gate <= 1; base reserve doubled); prime-field and generating rows
  (incl. the pinned row) escape — "domain generates F" becomes the
  favorable S5 hypothesis and a WP-0.2 check on the official family.
  (4) Safe-side classification conjecture: (i) B-pencil-rational /
  (ii) pole type / (iii) subfield tower — with my audited sigma=1
  counterexample (0.298, 0.266 at the toys) as calibration at the
  predicted e=2 shape, and the Lean F1 ledger as the typecheck target.
- **How it is useful:** Ties F1 into the assembly with one rule
  (min of the S2 corridor and the imported S7 window), turns row
  selection ("generating") into an explicit favorable hypothesis, and
  quarantines the one genuinely open F1 claim.
- **What to do next:** Turn 11: S5+S0 combined (per-rate theorem shapes +
  hypothesis table + object-equality axes), then S8/S9, then the final
  coherence pass.

### 2026-07-02 - Proof-sketch S3a: the regular window as crystallization testbed

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s3a_regular_window.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** SKETCH on verified arithmetic; falsifiable predictions.
- **What is being added:** Turn 9. The 4515-vs-6 reconciliation: 4515 is
  eliminant degree CAPACITY; FM (exact, Lemma FM1) puts the expected
  aligned-locator count per generic pair at 2^-16333..2^-21775 across the
  window, so by Markov the fraction of all pairs carrying any window
  alignment is <= ~2^-16000 — every real alignment is structured, and
  crystallization says structured = paid. Concrete prediction: the M3/M4/M5
  window theorem should end with aperiodic numerator 0 throughout (like the
  506/507 smoke packet). Front alpha: unstructured two-shift collisions
  have probability ~m^2/q = 2^-116.8 — P1 refined to P1a (gcd = 1
  everywhere) / P1b (collisions paid) / P1c (unpaid collision = a
  candidate_new_obstruction in the EASIEST regime, high evidential weight).
  Front beta: ambient pencil dim 29580 vs Hankel 512 (codim ~29068,
  verified) — realizability must be structure-forced, predicted paid
  (P-beta). Honest limit recorded: the window cannot probe fiber growth
  (kernels trivial) — Conjecture F's content is only tested by the
  deficiency ladder (PR #172).
- **How it is useful:** Gives the running M3 campaign a sharp end-state
  prediction and gives every scan outcome a defined evidential meaning for
  the in-band program.
- **What to do next:** Turn 10: S6 extension lift (F-valued witnesses,
  |F|/|B| denominator scale, sigma=1 calibration, safe-side classification).

### 2026-07-02 - Proof-sketch S7: the list side at the prize gate

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s7_list_side.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** PROVED-cited lower bounds + verified arithmetic; L1 input
  quarantined as CONJECTURE. No new theorem claimed.
- **What is being added:** Turn 8. (1) The poly-list threshold (slack
  ~n/log n, quotient cores) and the PRIZE gate (list crossing 2^-128 |F|)
  are different questions: at the gate both mechanisms land at the tau*
  scale ~1/log q. (2) The list-side unsafe half at the gate is
  UNCONDITIONAL: thm:qcore's C(n/M-1, k/M) codewords is a pure count
  (independent of q, no norm threshold) — verified exponent (n/M)H(rho);
  per-rate crossing windows [H/256, H/128] computed, sitting FARTHER from
  capacity than the MCA corridor because lists pay full entropy H while
  MCA value sets compress to beta < H. Consequence: grand challenge 2's
  safe side binds before grand challenge 1's, and only the list SAFE side
  is open. (3) Interleaved conversion budgets re-derived at n = 2^40,
  mu = 2: base-list exponent B <= 1.60 (worst) / 3.20 (a-regular) — the
  worst-case branch is TIGHTER than R2's B <= 3, making a-regularity
  reduction worth a full exponent point (fork F4). (4) The L1 full-petal
  sunflower battle mapped into the sketch: petal extras are structured
  plane sections of the divisor set — Conjecture F's fourth appearance.
- **How it is useful:** Separates the two threshold scales cleanly (a
  likely community confusion), records that the list unsafe half at the
  gate needs only convention checks, and prices the a-regularity question
  in exponent points.
- **What to do next:** Turn 9: S3a (why FM + paid structure predicts
  fronts alpha/beta land paid-or-empty; the 4515-vs-6 reconciliation).

### 2026-07-02 - Proof-sketch S4: the reserve dictionary

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s4_reserve_dictionary.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** VERIFIED-DICTIONARY core + textually grounded correspondences
  + named GAPs. No new theorem claimed.
- **What is being added:** Turn 7. (1) The identity: the sketch's FM
  crossover equation is def:taustar's equation via H(x) = H(1-x) — solved
  numerically, matches to six digits at all four rates. The list-side
  pigeonhole scale and the MCA-side alignment first moment are ONE entropy
  budget; spine S4 upgraded from CONJECTURE to verified dictionary.
  (2) thm:normalform quoted: emca = (1/q) max_t Lambda^NC exact, so packing
  numbers = per-line slope counts after the max; the three distinct t's
  (denominator degree, monomial slack, syndrome window) disambiguated;
  def:residue's noncontainment = the degenerate-pencil exclusion.
  (3) GAP-2 closed at sketch level: a pullback denominator forces
  M | t_denom, so rem:aper's line-side strip coincides with the
  rate-preserving support-side strip; non-rate-preserving folds stay
  aperiodic (no boost mechanism). (4) The 128 bits move the crossover by
  ~2^-42 (sharp transition, ~2^49 bits per unit delta) — invisible; the
  real cross-lane asymmetry is the field argument (tau* of q_gen vs
  q_line); pinned row generates (ord(17 mod 512) = 32, verified), general
  rows need both columns in the S5 tables.
- **How it is useful:** Makes cross-lane bookkeeping mechanical (MCA, list,
  L1, assembly all in one reserve currency); closes a definitional seam;
  flags the q_gen split as an official-family check.
- **What to do next:** Turn 8: S7 list side (L2 codegree consumption, L1
  ImgFib target, full-petal growth sub-battle, FM at q_gen).

### 2026-07-01 - Proof-sketch S3b.ii: the strip-periodic step

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s3b_ii_strip_periodic.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** PROVED-cited backbone + verified combinatorics + named GAPs.
- **What is being added:** Turn 6. Exact statement of the aperiodic stratum.
  Support-side vs line-side (rem:aper) periodicity distinguished, bridged by
  the proved x1 confinement/equivariance theorems, exact only on the
  equivariant stratum (isotypic refinement). Verified: periodic strata have
  size C(n/M, j/M); for unstructured pairs they carry no alignment boost
  (FM1), so paid mass comes from structured pairs via the proved
  Q_M = Q_1(quotient) recursion. Three verified exchange-dynamics facts:
  the periodic stratum is an INDEPENDENT SET in the Johnson exchange graph,
  every one-exchange exits it, and coset-moves restore exactly the quotient
  Johnson graph — the dynamics factor through the quotient precisely as the
  counting does (the same multi-scale recursion twice). Two named holes:
  GAP-1 (non-equivariant periodic mass not priced by quotient value sets;
  needs poly bound or a new ledger) and GAP-2 (gcd(n,j) vs gcd(n,k)
  definitional seam; thm:normalform check queued). Operative post-strip R2
  stated; the Lambda^aper quantifier dictionary explicitly deferred to S4,
  not asserted.
- **How it is useful:** Turns "after quotient removal" from a phrase into a
  checkable stratification with verified combinatorial structure; hands the
  M4 dedup its convention decision; isolates the two places the strip can
  leak.
- **What to do next:** Turn 7: S4 reserve dictionary (per-pair counts <->
  Lambda^aper <-> L1 reserve; read thm:normalform/def:residue; where the
  128 bits sit).

### 2026-07-01 - Proof-sketch S2: Paid(A) + refined threshold bracket

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s2_paid_ledger.md`;
  corrections + queue update in `prize_proof_sketch_spine.md`.
- **Status:** one PROVABLE-elementary lemma (toy-verified exactly),
  PROVED-cited ledgers, CONJECTURE zone; one recorded CORRECTION.
- **What is being added:** Turn 5. (1) **Lemma FM1**: the aperiodic first
  moment is exact — E[#aligned] = C(n,j)(1-q^-t)q^(1-t) for uniform pairs,
  via per-locator syndrome-map surjectivity (all 495 toy maps full-rank;
  empirical mean 0.017333 vs exact 0.017333 over 1500 pairs). All remaining
  heuristic content is relocated to worst-case-vs-mean and fiber-to-slope
  conversion. (2) Quotient term in three zones: norm-threshold-proved
  (N' <= ~80 at 2^256, mass <= 2^63.4 << B*), collision-uncertain
  (bracketed DdH vs 2^{beta N'}), and the cap. Zone-(b) collisions are
  prob:perfiber at sigma=1 — both sides of the threshold reduce to the same
  collision family. (3) Verified crossing table: quotient(collision-free) <
  FM < cap at every rate; refined bracket R1'. (4) CORRECTION: the turn-1
  P2 prediction mislabeled the A=265 target — the raw row is tangent-unsafe
  at 265 (LD_sw >= 248); the open conjecture concerns the quotient/tangent-
  stripped slack instance, and FM supports THAT; spine restated.
- **How it is useful:** Gives the assembly compiler its Paid(A) spec (M4
  tables must print zone-(b) as intervals); locates exactly which unproved
  statement decides the corridor; keeps the sketch honest about small-q vs
  prize-scale regimes.
- **What to do next:** Turn 6: S3b.ii strip-periodic (exact aperiodic
  stratum via the proved confinement/equivariance results + rem:aper).

### 2026-07-01 - Proof-sketch S3b.iii.3: fiber rigidity + noanchor ground-truth

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md`;
  corrections + queue update in `prize_proof_sketch_spine.md`.
- **Status:** SKETCH / CONJECTURE, with one recorded CORRECTION.
- **What is being added:** Turn 4. (1) Fiber bookkeeping: fibers are
  linear-plane sections of the divisor set; toy-verified planted-fiber law
  fiber = C(A_0, A_0-A) with ZERO unstructured extras, and the verified
  fact that tangent slopes are rank-drop singularities whose fibers are
  common-divisor planes. Also caught and fixed a window off-by-one: the
  alignment window is m = 1..t, not 0..t-1. (2) Conjecture F (fiber
  rigidity for linear sections) installed as the PARENT of the paper's
  frozen core: prob:perfiber is exactly F for coordinate/prefix planes
  (e_i(A) = locator coefficients), fiber(Z) is F for kernel planes, and
  L1/#106 Q_1 is the list-side sibling. (3) prop:noanchor read from source:
  it forecloses characteristic-zero-anchor/prime-averaging only; the
  four-tool termination list lives in prob:perfiber with per-tool reasons —
  earlier paraphrase corrected in the spine. Assessment: ES-incidence and
  exchange/expansion are fixed-prime technology (the category noanchor
  demands), but any moments-only version reduces to the foreclosed
  even-moment counts — the mechanisms' essential content must be the
  structure-crystallization step; odd-moment inputs (Hooley-Katz lane) are
  the cheapest rigid information beyond that line. beta(rho) constants for
  the quotient-paid term machine-verified for the S2 turn.
- **How it is useful:** Ties the sketch's fiber step and the paper's frozen
  core into one statement family; grounds the toolkit-foreclosure claims in
  the actual source text; sharpens where the genuinely new idea must live.
- **What to do next:** Turn 5: S2 — Paid(A) as one computable function
  (tangent staircase + quotient-profile term with beta(rho) + extension
  floor; conj:B's two-term bound as the template).

### 2026-07-01 - Proof-sketch S3b.iii.2: displacement/spectral exchange-rigidity

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_2_displacement_spectral.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** SKETCH / CONJECTURE / GAP-WALL (no result claimed).
- **What is being added:** Turn 3 of the proof-sketch loop: the
  dimension-free rigidity mechanism. Machine-verified backbone: subgroup
  Hankels factor as V^T diag(u) V (F_13/mu_12 entrywise check), so alignment
  = "the windowed product w_Z * ell misses Fourier frequencies 0..t-1"
  (verified), with no deficiency variables anywhere. One-exchange of a
  co-support point is a Cauchy rank-one update (the #152 t=2 ledger and
  #170 replacement/Cauchy-Binet sums are instances). Johnson graph J(n,j)
  spectra verified (trace checks; exact gap lam_0 - lam_1 = n at every j).
  Freezes the XR wall (exchange-rigidity hypothesis): dense aligned
  neighborhoods force tangent/quotient structure; consumer chain identical
  to SPI (either wall gives R2). Front alpha identified as XR's
  regular-window shadow; averaged XR laid out as a Johnson-scheme second
  moment (Hooley-Katz-shaped, plausibly provable now). Fork F2 notes that
  a small-t partial XR (generalizing #152 beyond t=2) targets exactly the
  A=265 / P2 prediction — a concrete bottom-up lemma hand-off.
- **How it is useful:** Complements mechanism 1 (same wall, two languages);
  supplies the counting language that survives in-band dimensions; names
  the #152-generalization as a Codex-lane-shaped lemma; gives the alpha
  scan a sharper interpretation.
- **What to do next:** Turn 4: S3b.iii.3 — fiber bookkeeping ("unpaid
  fibers are O(1)") + prop:noanchor re-read against incidence/exchange
  methods; then S2 Paid(A).

### 2026-07-01 - Proof-sketch S3b.iii.1: divisor/pencil incidence mechanism

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_1_divisor_pencil_incidence.md`;
  queue update in `prize_proof_sketch_spine.md`.
- **Status:** SKETCH / CONJECTURE / GAP-WALL (no result claimed).
- **What is being added:** Turn 2 of the proof-sketch loop: the first
  rigidity-mechanism child. Frames the aperiodic count exactly as
  `#(D_j cap X_{u,v})` — the C(n,j)-point divisor set (the WP-2.6 remainder
  system with the locator free) against the alignment variety cut by the
  t(t-1)/2 quadratic 2x2 minors of (H_u l ; H_v l), of dimension exactly the
  deficiency d (machine-checked). States Conjecture R2 (incidence rigidity,
  poly exponent budget B <= 3 at n = 2^41, verified) and freezes the SPI
  wall (structured-pencil incidence hypothesis) with its consumer chain.
  Identifies paid ledgers with Elekes-Szabo-type special/group-structured
  exceptional varieties, and WP-2.6/PR #172 as SPI at dimension 1 (eliminant
  degree 49408 = the provable base case). Honest stall risk recorded:
  without a dimension-free form the route never reaches the band (d = 239
  already at A=265); forks F1-F4 recorded, incl. re-reading prop:noanchor
  against incidence methods.
- **How it is useful:** Connects the running PR #172 ladder, the paid
  ledgers, and the aperiodic core as one incidence statement; gives the M1
  lane a precisely shaped worst-case target and the Hooley-Katz lane its
  averaged version.
- **What to do next:** Turn 3: mechanism 2 (displacement/spectral route —
  the #170 identities as a dimension-free handle); then the unpaid-fibers
  O(1) sub-sketch; then the prop:noanchor-vs-incidence check.

### 2026-07-01 - Prize proof-sketch spine (heuristic, NOT rigorous)

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proof_sketch/prize_proof_sketch_spine.md`.
- **Status:** CONJECTURAL / SKETCH (labelled per node: PROVED-cited / SKETCH /
  CONJECTURE / GAP-WALL). No result claimed or promoted.
- **What is being added:** Turn 1 of a top-down proof-sketch loop: the spine
  of a heuristic path from current results to a prize resolution. Core frame
  (machine-checked arithmetic): valid locators are the C(n,j) squarefree
  degree-j divisors of X^n-1; the Hankel pencil is linear in the slope, so
  each locator yields at most one uncontained bad slope (the v8
  one-support-one-slope ledger; the degenerate pencil case is exactly the
  noncontainment exclusion). First-moment model E[B_ap] ~ C(n,j) q^(1-t)
  gives a per-rate crossover reserve 2^-8.00 / 2^-8.29 / 2^-8.86 / 2^-9.55
  vs the proved Paper D caps 2^-9 / 2^-9 / 2^-9 / 2^-10 — conjectured-unsafe
  contains proved-unsafe with a thin corridor (Conjecture R1: delta* =
  1 - rho - c_rho/log2 q). Pinned-row consistency: FM ~ 0 at A=506 (matches
  the smoke packet's aperiodic numerator 0); FM ~ 2^-542 at A=265 (predicts
  the open LD_sw(C,265) <= 6 TRUE); FM crossover A=261->260 vs proved cap
  A<=258. Spine nodes S0-S9 with forks; falsifiable predictions P1-P4;
  negative-resolution branch kept first-class.
- **How it is useful:** Gives the M1/M3/M5/L1 lanes one shared quantitative
  target (make the first moment rigorous on the aperiodic stratum after paid
  removal) and concrete falsification tests the existing fronts
  (alpha/beta, A=265, WP-2.6 rung 1) already exercise.
- **What to do next:** Loop turns refine spine nodes into child files,
  starting with S3b.iii (divisor-variety/pencil-incidence rigidity, then the
  displacement-rank route), then S2 Paid(A), S3b.ii strip-periodic, S7 list
  side. Maintainer review of the spine's labels welcome.

### 2026-07-01 - Execution roadmap r2 + first L3 detail note (top-down plan)

- **Agent/model:** AllenGrahamHart / Claude (Fable 5).
- **Files added or changed:**
  `experimental/notes/roadmaps/proximity_prize_execution_roadmap_post_v10_r2.md`;
  `experimental/notes/roadmaps/wp_detail/wp2_6_underdetermined_program.md`.
- **Status:** AUDIT (proposed working roadmap; no results claimed).
- **What is being added:** Revision 2 of the post-v10 execution roadmap
  (self-contained; does not supersede `towards-prize.md`). Key deltas vs the
  r1 draft: a verified structural section showing the open prize band is
  entirely underdetermined for every official rate (the regular branch ends at
  `delta = (1-rho)/2`, strictly below Johnson by exactly `(1-sqrt(rho))^2/2`),
  a new critical-path work package WP-2.6 (underdetermined deficiency ladder,
  running as PR #172), integration re-scoped as maintainer-gated with agent
  replay audits, fronts alpha/beta gated on independent replay, asset lists +
  executability tags on every work package, and a refinement protocol
  (L0-L3 with a leaf DONE-definition). Plus the first L3 detail note: the full
  rung-1 lemma DAG for A=384 (Cramer kernel U1, pencil nondegeneracy U2,
  validity=divisibility U3, pseudo-remainder chart U4 with deg_Z <= 49408,
  eliminant-or-identically-valid-pencil dichotomy U5, side charts, exhaustive
  F_97/mu_16 acid test, F_17^32 instantiation strategy, deficiency-growth
  rung 2, symbolic rung 3).
- **How it is useful:** Gives the project a top-down decomposition that meets
  the bottom-up lemma-at-a-time lane in the middle; makes the
  regular-window-vs-prize-band distinction explicit so proving-ground results
  are not mistaken for band results; turns WP-2.6 into a hand-off-ready
  program with acceptance tests.
- **What to do next:** Refine the queued detail notes (wp0_1 object
  reconciliation next, then wp2_1/wp2_2 replay-gated fronts, wp2_3, wp5_1,
  wp4_3); maintainer review of the roadmap posture; resume the PR #172 loop
  per the turn schedule in the wp2_6 detail note.

### 2026-07-01 - v10 guide and site metadata sync

- **Agent/model:** Codex.
- **Files added or changed:** `AGENTS.md`; `README.md`/`readme.md`;
  `site/index.html`; `site/papers/cs25_cap_v10.pdf`;
  `towards-prize.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / DOCUMENTATION.
- **What is being added:** The agent guide, repo overview, prize roadmap, and
  site paper metadata now point at Paper D v10 as the current cap/Hankel-ledger
  package.  `AGENTS.md` also names the next concrete prize task: an M3/M4
  root-table and paid-root-subtraction packet for the `F_17^32`, `n=512`,
  `k=256` row over agreements `385 <= A <= 426`.
- **How it is useful:** Prevents new agents and site readers from treating v9,
  strict264, or strict352 as the active frontier.  The current route is v10
  safe-side Hankel packets, singular-bucket classification, and exact ledger
  subtraction against the six-slope `F_17^32` budget.
- **What to do next:** Build the first M3/M4 table for selected agreements in
  `385 <= A <= 426`, including regular roots, tangent/quotient/extension
  subtraction, and residual chart labels.

### 2026-07-01 - PR 161--169 frontier integration

- **Agent/model:** Codex, integrating contributions from holmbuar,
  AllenGrahamHart, DannyExperiments, and Gia.
- **Files added or changed:** `tex/slackMCA_v3.tex`;
  `tex/slackMCA_v4.tex`; `tex/snarks_v4.tex`; `tex/snarks_v5.tex`;
  `experimental/notes/audits/pr161_169_integration_audit.md`;
  `experimental/notes/l1/l1_full_petal_growing_defect_witnesses.md`;
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`;
  `experimental/data/certificates/l1-monomial-dyadic-descent/`;
  `experimental/notes/m1/m1_full_overlap_low_tail_completion_projection_wall.md`;
  `experimental/notes/m1/m1_beta2_conditional_close.md`;
  `experimental/notes/m1/m1_beta2_obstruction_floor.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_generic_regular_minor.md`;
  `experimental/notes/m1/f17_32_hankel_row_descriptor.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/thresholds/f17_32_high_agreement_tangent_table.md`;
  `experimental/lean/rs_mca_formalization/RsMca.lean`;
  `experimental/lean/rs_mca_formalization/RsMca/F1ExtensionLedger.lean`;
  `experimental/lean/rs_mca_formalization/RsMca/BetaTwoReductionLedger.lean`;
  selected verifier scripts and Hankel/L1 data packets.
- **Status:** AUDIT / PROVED-SUBPACKETS / CONDITIONAL / EXPERIMENTAL.
- **What is being added:** The L1 target in Papers B/C is repaired from raw
  support fibers to image fibers; full-petal L1 witnesses and a monomial
  dyadic replay packet are banked; M1 full-overlap and BETA_2 route-cut notes
  are integrated; F1/BETA Lean ledgers are wired; and selected M3 regular
  Hankel row-descriptor/window/minor artifacts are added from the large
  regular-minor PR.
- **How it is useful:** This turns the current PR wave into usable proof
  infrastructure for the v10 prize plan: L1 is now stated against the right
  object, M1 route cuts are named, F1/BETA algebra cores are formalized, and
  the `F_17^32` non-tangent regular window has compact row and generic-minor
  artifacts.
- **What to do next:** Use the M3 row descriptor and regular-minor extractor
  to compute actual root tables in `385 <= A <= 426`; compress any remaining
  generated PR #161 material into small audited proof packets before adding it;
  and seek a genuine BETA_2 monodromy/conductor theorem rather than promoting
  finite local data.

### 2026-07-01 - Paper D v10 milestone integration

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v10.tex`;
  `cs25_cap_v10.pdf`; `scripts/cs25_v10_*.py`;
  `experimental/data/certificates/cs25-v10-regular-hankel-examples/`;
  `experimental/notes/audits/paperD_v10_milestone_integration_audit.md`;
  `towards-prize.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED-CERTIFICATE-FRAMEWORK.
- **What is being added:** Integrated the four v10 milestone folders into Paper
  D v10: quantitative deep-list floors, heaviest prefix-fiber quotient lower
  ledgers, exact divisor-block support-union coefficients, gcd/lcm quotient
  image ledgers, extension-pole simple-pole witnesses, and canonical regular
  Hankel rank-drop gcd/lcm ledgers.
- **How it is useful:** This strengthens Paper D's completion program from a
  v9 chart atlas into scanner-ready lower, quotient, extension, and regular
  Hankel ledgers.  It also narrows the remaining prize-side work to structural
  exhaustion, singular buckets, and safe-side extension classification.
- **What to do next:** Run the regular Hankel checker on the `F_17^32` row in
  the `385 <= A <= 426` window, combine paid-root subtraction with quotient and
  tangent ledgers, and build pivot eliminants for any singular buckets.

### 2026-06-30 - M2 Hankel smoke packet

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/certificates/hankel-smoke-f17-506-507/`;
  `experimental/notes/thresholds/hankel_smoke_f17_506_507.md`;
  `experimental/scripts/verify_hankel_smoke_f17_506_507.py`;
  `towards-prize.md`; `tex/cs25_cap_v9.pdf`.
- **Status:** PROVED-SMOKE-PACKET / AUDIT.
- **What is being added:** The duplicate `tex/cs25_cap_v9.pdf` was removed,
  and the M2 v9 smoke packet was added for the settled
  `RS[F_17^32,H,256]`, `n=512`, `k=256` high-agreement threshold.  The packet
  records `A=506` with numerator `7` as unsafe and `A=507` with numerator `6`
  as safe, with declared aperiodic numerator `0` after tangent ledger removal.
- **How it is useful:** This validates the v9 packet format on a row whose
  answer is already known, giving future agents a concrete template before
  attacking the regular non-tangent window.
- **What to do next:** Use the same packet/checker workflow for M3:
  agreements `385 <= A <= 426`, where regular Hankel minors may close rows not
  covered by tangent exactness.

### 2026-06-30 - Aperiodic Hankel packet checker

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/aperiodic-hankel-regular-minor-toy/`;
  `experimental/notes/m1/aperiodic_hankel_regular_minor_toy_certificate.md`;
  `experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED for the toy certificate.
- **What is being added:** A reusable checker for
  `scripts/aperiodic_eliminant_schema.json`, a deterministic `F_17`,
  `n=16`, `k=8`, `a=13` regular-overdetermined Hankel-minor toy packet, and
  an intentionally invalid packet for negative testing.
- **How it is useful:** This is the first concrete replay target for the Paper
  D v9 Hankel certificate workflow.  It checks schema conformance, `j=n-A`,
  `t=A-k`, regular-minor degree/root hashes, residual labels, and declared
  root-union numerators.
- **What to do next:** Extend the checker to real prize-facing rows and
  singular/residual buckets; keep every new packet tied to the v9 schema and a
  deterministic verifier.

### 2026-06-30 - Late PR M1/audit integration

- **Agent/model:** Codex, auditing and distilling PRs from AllenGrahamHart and
  Scott Hughes.
- **Files added or changed:** M1/audit notes and verifiers from PRs #150--#156
  and #158 under `experimental/notes/` and `experimental/scripts/`;
  `experimental/data/step5-envelope-map/envelope_map.json`;
  `experimental/notes/m1/m1_packet_sift_popularity_digest.md`;
  `experimental/scripts/verify_m1_packet_sift_popularity_digest.py`;
  `experimental/notes/m1/m1_a327_rim_route_cut_digest.md`;
  `experimental/data/m1_a327_rim_route_cut_digest.json`;
  `experimental/scripts/verify_m1_a327_rim_route_cut_digest.py`;
  `experimental/notes/triage/pr-triage-2026-06-30-late.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** AllenGrahamHart's M1 local lemmas, sampler
  reconciliation audit, Step 5 high-agreement envelope map, and agreement-265
  status audit were integrated as experimental material.  Allen's oversized
  packet-sift PR #157 was distilled to a compact packet-overlap/popularity-gate
  digest.  Scott Hughes's draft a=327 RIM obstruction PR #145 was distilled to
  a compact interleaved-list route-cut digest and self-contained JSON ledger.
- **How it is useful:** The batch preserves useful local M1 proof machinery,
  audit corrections, and high-agreement bookkeeping without promoting any
  conditional packet branch to a full M1 theorem or leaderboard row.
- **What to do next:** Rebase future M1 packets against the v9 Hankel
  certificate schema.  For the packet-sift branch, prove the nonlocal
  model-entry/multiplicity theorem or isolate a new residual obstruction.  For
  the a=327 RIM branch, turn RREF-derived pivots into deterministic pivot
  schedules before claiming a global bound.

### 2026-06-30 - Paper D v9 Hankel certificate atlas promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v9.tex`,
  `scripts/aperiodic_eliminant_schema.json`,
  `experimental/notes/audits/paperD_v9_vs_v8_audit.md`, `AGENTS.md`,
  `README.md`, site paper/update metadata, and compiled Paper D v9 PDFs.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED-CERTIFICATE-FRAMEWORK.
- **What is being added:** Paper D v9 preserves the v8 universal cap,
  first-grid cap, quotient-support ledger, and quotient-image ledger, then adds
  the aperiodic Hankel chart atlas: regular overdetermined minors, affine
  pivots, projective infinity, curve coefficient pivots, and named singular
  residual buckets.
- **How it is useful:** It turns the M1 safe-side task into concrete Hankel
  certificate packets. Contributors can now emit JSON against
  `scripts/aperiodic_eliminant_schema.json` instead of inventing an atlas or
  hiding singular charts under a generic aperiodic label.
- **What to do next:** Build actual eliminant certificates for meaningful rows,
  starting with exact agreements where the regular minor test applies. Every
  unresolved chart should be labelled as quotient, tangent, extension,
  candidate new obstruction, or unknown.

### 2026-06-30 - PR #137--#149 integration and triage

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Holm Buar,
  Jose Brox, and Scott Hughes.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-30.md`,
  Lean ledger files under `experimental/lean/rs_mca_formalization/`,
  new notes under `experimental/notes/m1/`, `experimental/notes/f1/`,
  `experimental/notes/audits/`, and `experimental/notes/thresholds/`, new
  certificate data under `experimental/data/certificates/`, updated audit
  scripts under `experimental/scripts/`, and `experimental/experiments.tex`.
- **Status:** CONDITIONAL / PROVED-LOCAL / AUDIT / EXPERIMENTAL, depending on
  the individual note.  No full M1, F1, exact-threshold, or prize-solve claim is
  promoted.
- **What is being added:** The batch integrates Holm Buar's `{2,3}`-smooth Paper
  B exact canonical slope count, Lean arithmetic ledgers, finite toy databases,
  M1 numerical audit scans, and Cycle120 finite witness audit; Jose Brox's L3
  path cleanup; and AllenGrahamHart's width-one update, high-agreement compiler
  package, and independent V1 algebra checker.
- **How it is useful:** The new material improves Paper B combinatorics,
  high-agreement threshold reproducibility, formalized integer ledgers, and
  audit coverage without mixing them into the public leaderboard as new best
  rows.
- **What to do next:** Split AllenGrahamHart's very large same-slope PR #138
  into smaller local lemmas, ask for a compact replay target for Scott Hughes's
  #145 route-cut packet, and run Lean/certificate checks in a controlled
  environment if maintainers want independent replay beyond source inspection.

### 2026-06-30 - Paper D v8 quotient ledger promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v8.tex`, `cs25_cap_v8.pdf`,
  `site/papers/cs25_cap_v8.pdf`,
  `experimental/notes/audits/paperD_v8_vs_v7_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V8_CAP /
  PROVED_PAPERD_V8_FIRST_GRID.
- **What is being added:** Paper D v8 is promoted as the current public Paper D
  source. It preserves the v7 universal and first-grid caps, restores the
  explicit `q>n` and endpoint-radius fixes, and adds quotient-support plus
  distinct-parameter quotient image ledgers.
- **How it is useful:** The new ledgers give future staircase scanners and
  proof notes a safe way to account for declared quotient-remainder branches
  without double-counting supports or slope images.
- **What to do next:** Treat these ledgers as branch accounting only. The
  full safe-side theorem still needs the aperiodic Hankel-packing and
  extension-line completion inputs.

### 2026-06-29 - Paper D v7 first-grid cap promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v7.tex`, `cs25_cap_v7.pdf`,
  `site/papers/cs25_cap_v7.pdf`,
  `experimental/notes/audits/paperD_v7_vs_v6_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V7_CAP /
  PROVED_PAPERD_V7_FIRST_GRID.
- **What is being added:** Paper D v7 is promoted as the current public Paper D
  source. It preserves the v6 universal fixed-divisor MCA cap, extends the
  no-loss CA endpoint to `floor(delta n) <= n-k-1`, and adds the first-grid
  deep-point cap for large official-envelope rows.
- **How it is useful:** The public board can now show two Paper D theorem
  layers: the older uniform fixed-divisor cap and the stronger large-row
  first-grid cap `delta*_C(2^-128) <= 1-rho-1/n`.
- **What to do next:** Keep first-grid rows separate from exact-threshold
  claims. The missing safe-side work remains the L1/M1/F1/M2 completion package.

### 2026-06-29 - PR #136 width-one fixed-root closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/notes/m1/m1_width_one_fixedroot_closure.md`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`, and
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.
- **What is being added:** A compact width-one M1 closure note: width-one
  maximal root shadows are bounded-complement rank tests, descend losslessly
  under fixed-root absorption, and inject into one-root fixed-divisor/root-slice
  ledgers.
- **How it is useful:** It reduces the width-one critical-tail branch to the
  existing one-root fixed-root ledger in fixed surplus, giving a smaller target
  for the M1 proof program without promoting a full all-line theorem.
- **What to do next:** Prove or import the polynomial fixed-surplus bound for
  `FixedRootOneRoot_{r1}` after quotient-periodic, tangent, fixed-root, and
  aperiodic charges; do not treat this as a leaderboard row.

### 2026-06-29 - PR #131--#135 triage and frontier rows

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes, and
  Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-29.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_a507_adjacent_bridge_theorem.md`,
  `experimental/notes/m1/m1_a507_plus_one_slope_hunt.md`,
  `experimental/notes/m1/m1_interleaved_list_*.md`,
  `experimental/notes/m1/m1_random_simple_pole_entropy_floor.md`,
  `experimental/notes/m1/m1_coset_packet_finite_slope_floors.md`,
  matching JSON certificates under `experimental/data/`, matching verifiers
  under `experimental/scripts/`, `experimental/experiments.tex`, and site data.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / PROOF_RECORD / LOWER_BOUND /
  ROUTE_CUT / AUDIT.
- **What is being added:** The PR wave adds three useful frontier-facing
  packets: Scott Hughes's interleaved-list hybrid certificate
  `Lambda_mu(C,326) >= 7`, Vadim Avdeev's random simple-pole finite-slope floors
  for `a=257..260`, and Vadim Avdeev's coset-packet finite-slope floors for
  `a=261..288`. AllenGrahamHart's boundary-off external-anchor M1 normal form is
  distilled into a compact proof-program audit, and Scott Hughes's `a=507`
  adjacent-bridge packet is integrated as a route cut rather than a new row.
- **How it is useful:** The finite-slope floors strengthen the low-agreement
  side of the `F_17^32, n=512, k=256` MCA ledger, while the interleaved-list
  packet moves the separate list-track lower-bound row up to agreement `326`.
  The route-cut notes prevent accidental mixing of adjacent line/list
  numerators into the same finite-slope MCA denominator.
- **What to do next:** Human-review the finite-slope-to-MCA noncontainment
  convention before paper promotion, keep #131 as proof-program material until
  it proves a global M1 bound, and treat the Sage scripts in #133 as optional
  independent audits rather than required local verification.

### 2026-06-29 - Paper D v6 promotion and completion-program audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v6.tex`, `cs25_cap_v6.pdf`,
  `site/papers/cs25_cap_v6.pdf`,
  `experimental/notes/audits/paperD_v6_vs_v5_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V6_CAP.
- **What is being added:** Paper D v6 is promoted as the current public Paper D
  source. It keeps the v5 universal MCA cap constants and CS25-free route,
  tightens the conversion collision-count derivation, and adds the
  prize-facing integer-staircase/completion program.
- **How it is useful:** Public rows now cite the strongest Paper D package:
  same cap theorem, clearer prize posture, and explicit conditional MCA/list
  completion theorems for turning the one-sided cap into a full threshold
  determination.
- **What to do next:** Use `PROVED_PAPERD_V6_CAP` for verified Paper D cap rows,
  while keeping the missing L1/M1/F1/M2 completion obligations separate from
  the proved cap itself.

### 2026-06-27 - Root-level paper PDF relocation

- **Agent/model:** Codex.
- **Files added or changed:** `cs25_cap_v5.pdf`, `slackMCA_v4.pdf`,
  `snarks_v5.pdf`, removed generated PDF outputs from `tex/`,
  `site/data/papers.json`, `site/index.html`, `experimental/agents-log.md`.
- **Status:** AUDIT / RELEASE-HYGIENE.
- **What is being added:** The generated Paper B/C/D PDFs are moved out of
  `tex/` into the repository root, matching the README convention that TeX
  sources live under `tex/` and PDFs live at the root. Site-local mirrors under
  `site/papers/` remain for static hosting.
- **How it is useful:** Keeps GitHub PDF links and repository layout aligned
  with the public paper set: B v4, C v5, and D v5.
- **What to do next:** Keep future TeX compile outputs copied to root and, when
  needed, mirrored into `site/papers/` for static-site serving.

### 2026-06-27 - Paper B/C/D version promotion and leaderboard source audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/slackMCA_v4.tex`,
  `slackMCA_v4.pdf`, `tex/snarks_v5.tex`, `snarks_v5.pdf`,
  `site/papers/slackMCA_v4.pdf`, `site/papers/snarks_v5.pdf`, `readme.md`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Two clarification edits are added to the promoted
  Paper B/C versions: the Paper B unsplit curve-envelope lower bound is
  explicitly the line witness embedded as a degree-`d` curve, and Paper C now
  says the curve compiler applies to the finite power-curve/evaluation-domain
  model rather than arbitrary protocol samplers. The README records the current
  public versions B v4, C v5, and D v5.
- **How it is useful:** Keeps the paper prose aligned with the public board:
  Paper D v5 cap rows are proved under their printed scanner hypotheses,
  high-agreement/list rows cite Paper B v4 after promotion, and Paper C v5 is
  framed as protocol-ledger packaging rather than a new cap row.
- **What to do next:** Commit the version promotion after final review, and
  keep future leaderboard rows explicit about whether they are Paper B
  high-agreement theorem rows, Paper D v5 cap rows, or Paper C protocol-ledger
  packaging rows.

### 2026-06-27 - M1 variable-line packet and singleton lemmas

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/experiments.tex`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Local packet lemmas for non-fixed variable Hankel
  determinant lines: active-new packet mass is reduced to active domain
  singletons, quotient defects, and a different-slope two-exchange codegree
  image.  The singleton term is then reduced to contained/tangent and
  one-outside target images, with the zero-lower class eliminated in the
  high-agreement range `a>(n+1)/2`.
- **How it is useful:** This extracts a reviewable M1 reduction from the
  all-line Hankel packet while keeping it out of the leaderboard.  It narrows
  the remaining non-fixed variable-line branch to explicit target-image and
  codegree estimates.
- **What to do next:** Prove polynomial bounds for the active different-slope
  two-exchange codegree and the one-outside boundary target image inside the
  quotient-aware residue-line ledger; do not cite this as the final M1 theorem.

### 2026-06-27 - Paper D v5 cap status promotion in scanner and board

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `experimental/notes/certificate_scanner/README.md`,
  `experimental/notes/certificate_scanner/outputs/`,
  `experimental/notes/audits/a0_cs25_rational_constant_derivation.md`,
  `experimental/notes/audits/theorem_label_map.md`,
  `experimental/notes/audits/codex-f1-l1-20260617/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT.
- **What is being added:** The scanner now emits `PROVED_PAPERD_V5_CAP` for
  active Paper D v5 cap rows whose divisor, binomial, and field hypotheses pass,
  and `NO_ACTIVE_PAPERD_V5_CAP` when no such row is found. Existing scanner
  reports and leaderboard-sweep outputs are regenerated or mechanically updated
  to remove the old draft/CS25-import status, and stale experimental audit notes
  now mark that import route as relevant only to older CA/list comparisons.
- **How it is useful:** Aligns the public leaderboard and scanner with Paper D
  v5's self-contained MCA cap route. Verified Paper D cap rows are no longer
  marked with the older conditional-import or draft-example statuses.
- **What to do next:** Keep CA/list comparison statements separate from the MCA
  cap status, and update any remaining paper-level prose that still discusses
  the older CS25-dependent route as the main Paper D theorem.

### 2026-06-27 - Finite-row threshold note and pure-MCA scanner profile

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`,
  `experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf`,
  `experimental/notes/certificate_scanner/examples/f17_512_mca_only.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL-SCANNER.
- **What is being added:** A standalone finite-row threshold note packages the
  \(\F_{17^{32}}, n=512,k=256\) row as an exact finite-slope support-wise MCA
  threshold: agreement \(506\) is unsafe, agreement \(507\) is safe, and the
  closed-real safe interval is \([0,6/512)\). A pure-MCA scanner profile is
  added so the 506/507 endpoint is not mixed with the optional line-plus-list
  protocol ledger.
- **How it is useful:** Supersedes the old strict264-next threshold plan for
  this finite row and gives the clean packaging needed for the public board and
  `towards-prize.md`. It also isolates the next theorem target: the
  row-independent high-agreement threshold compiler with
  \(B_Q=\lfloor Q/2^{128}\rfloor\).
- **What to do next:** Audit the official MCA sampler definition against the
  finite/projective slope conventions and decide whether to promote the
  row-independent compiler from experimental notes into a paper-level theorem.

### 2026-06-27 - Prime192 leaderboard sweep rows

- **Agent/model:** Codex, auditing `leaderboard_sweep_192`.
- **Files added or changed:** `experimental/notes/certificate_scanner/outputs/leaderboard_sweep_192/`,
  `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`, and
  `site/index.html`.
- **Status:** PROVED_PAPERD_V5_CAP / AUDIT.
- **What is being added:** The scanner sweep contributes four concrete
  prime-field rows with `q` near `2^192`, `k=2^40`, smooth power-of-two
  subgroup domains, and one row per official prize rate. It also records a
  small `F_17^32` Paper D example at agreement `258`.
- **How it is useful:** These rows instantiate the Paper D v5 cap with exact
  field/domain arithmetic, making the theorem-envelope rows concrete without
  claiming a new theorem beyond Paper D or an explicit slope census.
- **What to do next:** Regenerate the sweep from a checked-in sweep script if
  the scanner API changes, and keep CA/list comparison statements separate from
  the proved MCA cap status.

### 2026-06-27 - PR #122--#129 triage and selective integration

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes,
  and Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-27.md`,
  `experimental/notes/l1/l1_prefix_dual_d3_subgroup_twisted_collision_bound.md`,
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`,
  `experimental/notes/f1/f1_arbitrary_anchor_locator_split.md`,
  `experimental/notes/m1/m1_all_line_hankel_aperiodic_packet_audit.md`,
  `experimental/data/adjacent-ledgers/`, selected verifier scripts, and
  `experimental/experiments.tex`.
- **Status:** PROVED / IMPORTED-STANDARD-INPUT / AUDIT / PROOF PROGRAM /
  EXPERIMENTAL.
- **What is being added:** New bounded L1/F1/M2 notes are integrated, while
  PR #127's large M1 generated packet is distilled into a smaller audit note.
  The public board is updated only for tangent-floor-backed status corrections:
  Cycle116/119 gates are unconditional but their exact Cycle84 numerator remains
  conditional, and reserve272/288/313 are marked as proved only because they are
  subsumed by tangent/strict352 floors.
- **How it is useful:** Adds useful L1 `d=3` proper-subgroup and monomial-prefix
  toy theorems, sharpens the F1 arbitrary-anchor ledger, and records
  challenge-map pullback accounting for protocol-facing high-agreement ledgers
  without promoting non-verified material to theorem status.
- **What to do next:** Split the M1 all-line aperiodic packet into small
  separately auditable verifiers before considering any stronger theorem claim;
  human-review the imported Katz/Gauss inputs in the L1 `d=3` note before moving
  it toward Paper B.

### 2026-06-27 - Promoted high-agreement TeX split

- **Agent/model:** Codex, verifying and promoting the user-supplied
  `experiments_v2.tex` split.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/notes/high_agreement/`,
  `experimental/scripts/verify_promoted_high_agreement_ledgers.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / AUDIT.
- **What is being added:** The bulky high-agreement tangent, CA/projective,
  curve, interleaved-list, current-row protocol, and general threshold compiler
  material is split into reusable TeX fragments under
  `experimental/notes/high_agreement/` and included from the canonical
  `experimental/experiments.tex` wrapper.
- **How it is useful:** Keeps the stable high-agreement theorem package
  reviewable in smaller files while preserving the compiled experimental memo.
  The split also fixes the stale missing backslash before the
  `Towards-Prize Finite-Threshold Theorems` section header.
- **What to do next:** Human-review the curve sampler caveat before citing the
  curve statements in protocol settings, and keep protocol query/folding,
  extension-lift, challenge-field, and cryptographic losses as separate ledger
  terms.

### 2026-06-26 - Generalized high-agreement ledgers

- **Agent/model:** GPT-5.5 Pro generalized-ledgers packet, audited and
  integrated by Codex.
- **Files added or changed:** `experimental/data/generalized-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/data/README.md`, `site/data/updates.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** A row-independent high-agreement ledger calculus for
  `RS[F,D,k]` rows: with `R=n-k`, `r=n-a`, and `B_Q=floor(Q/2^128)`, the exact
  line/CA/projective numerator is `r+1` in the range `r <= floor(R/3)`, the
  degree-`d` curve numerator is `d(r+1)` in the range
  `r <= floor(R/(d+2))`, and interleaved-list uniqueness holds for
  `r <= floor(R/2)`.
- **How it is useful:** This moves the adjacent-ledger conclusions beyond the
  special `F_17^32` row.  It gives a reusable integer calculator for deciding
  when tangent-star high-agreement terms alone can pin a `2^-128` threshold,
  and shows that at prize-scale dimensions the method stops pinning thresholds
  once field sizes are roughly above `2^166` to `2^170`, depending on rate.
- **What to do next:** Use this calculator before adding any new row to the
  public board, and keep quotient-core, generated-field entropy, challenge
  field, folding, query, and cryptographic terms as separate ledgers.

### 2026-06-26 - High-agreement adjacent CA/curve/list ledgers

- **Agent/model:** GPT-5.5 Pro adjacent-ledgers packet, audited and integrated
  by Codex.
- **Files added or changed:** `experimental/data/adjacent-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** The high-agreement tangent staircase is extended to
  no-loss CA, projective-slope support-wise MCA, finite-parameter degree-`d`
  curve CA/MCA, and MDS interleaved-list uniqueness.  For
  `RS[F_17^32,H,256]`, the line-plus-list coding ledger is unsafe at
  agreement `a=507` and safe at `a=508` when no query/folding loss is added.
- **How it is useful:** This answers the immediate adjacent-ledger question
  past the finite-slope `506/507` gate: the high-agreement CA/projective/curve
  and interleaved-list coding objects are now pinned by explicit integer
  formulae, rather than left as open checks.
- **What to do next:** Human-review protocol reductions before using the
  conditional ledger in SNARK claims, and add any query, folding, hash,
  extension-lift, or cryptographic error terms explicitly.

### 2026-06-26 - Tangent-star extremizer barrier

- **Agent/model:** GPT-5.5 Pro tangent-star packet, audited and integrated by
  Codex.
- **Files added or changed:** `experimental/data/tangent-star/`,
  `experimental/experiments.tex`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / NEW-LOCAL / FINITE-SLOPE STRUCTURAL BARRIER.
- **What is being added:** A refinement of the high-agreement tangent
  staircase: in the exact range `3a-2n >= k`, extremal finite-slope
  support-wise `LD_sw` lines are tangent-star lines.  For
  `RS[F_17^32,H,256]`, this rules out a seventh finite-slope bad branch at
  every agreement `a >= 507`.
- **How it is useful:** It closes the previous finite-slope follow-up question
  left by the tangent staircase: no non-tangent mechanism can push the current
  `F_17^32`, `n=512`, `k=256` row past the `506/507` gate under the
  finite-slope support-wise MCA convention.
- **What to do next:** Use the adjacent-ledgers packet for the high-agreement
  CA/projective/curve/list coding objects, and keep protocol, challenge-field,
  extension-lift, folding, query, and cryptographic losses as separate ledgers.

### 2026-06-26 - High-agreement tangent staircase

- **Agent/model:** GPT-5.5 Pro tangent packet, audited and integrated by Codex.
- **Files added or changed:** `experimental/data/tangent/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT / FINITE-SLOPE-THRESHOLD.
- **What is being added:** A generic moving-root tangent floor
  `LD_sw(C,a) >= n-a+1` for Reed--Solomon codes, plus a matching upper bound in
  the very-high-agreement range `3a-2n >= k` using the common code-line
  residual budget.
- **How it is useful:** For `RS[F_17^32,H,256]` with `|H|=512`, this proves
  `LD_sw(C,a)=513-a` for every `a>=427`, so `LD_sw(C,506)=7` and
  `LD_sw(C,507)=6`.  Thus the finite-slope support-wise `2^-128` staircase is
  pinned between agreements `506` and `507`; agreement `353` and the strict352
  quotient-core frontier are superseded by the tangent floor.
- **What to do next:** Human-review the endpoint convention and use the
  adjacent-ledgers packet for the high-agreement CA/projective/curve/list
  coding objects; protocol-facing losses still need separate ledgers.

### 2026-06-26 - L1 d=2 cubic subgroup twisted bound

- **Agent/model:** Scott Hughes PR #121, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`,
  `experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_d2_cubic_subgroup_twisted_bound.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / STANDARD-WEIL-INPUT / AUDIT.
- **What is being added:** A `d=2` cubic proper-subgroup collision bound for
  the actual `H^{2k}` object, using exact Fourier reconstruction,
  multiplicative-character expansion of `1_H`, and a conservative
  one-variable mixed character-sum bound.
- **How it is useful:** Separates proper-subgroup counting from full-affine
  Hooley--Katz geometry and gives an L1 template for higher odd-moment twisted
  subgroup bounds.  It is not a new MCA leaderboard row.
- **What to do next:** Pin the imported Katz/Gauss source constants and test
  whether the method extends to higher odd moments with reserve-scale margins.

### 2026-06-26 - L1 odd-moment Hooley-Katz audit

- **Agent/model:** Scott Hughes PR #120, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_odd_moment_projective_geometry.md`,
  `experimental/notes/triage/l1-prefix-dual-odd-moment-hooley-katz-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_odd_moment_hooley_katz_audit.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / IMPORTED-VERIFIED / AUDIT / ROUTE CUT.
- **What is being added:** A projective odd-moment collision-geometry theorem
  for `k>d`, affine-cone conversion, and a Hooley--Katz/Ghorpade--Lachaud
  constant ledger for the full-affine point-count route.
- **How it is useful:** Records why the generic full-affine point-count route
  is not enough for the subgroup L1 reserve-scale problem and prevents ledger
  mixing between full-affine, full-torus, and proper-subgroup counts.
- **What to do next:** Human-check imported theorem citations and use the
  audit as a route cut unless sharper geometry-specific constants are found.

### 2026-06-26 - Strict352 dyadic quotient-core MCA floor audit

- **Agent/model:** Codex, auditing user-supplied strict352 packet.
- **Files added or changed:** `experimental/data/strict352/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / SUPPORT-WISE-MCA-LOWER-BOUND.
- **What is being added:** A dyadic quotient-core proof packet for
  `RS[F_17^32,H,256]`, `|H|=512`, showing `LD_sw(C,a) >= 7` for every
  agreement `264 <= a <= 352`, with `LD_sw(C,352) >= 16` under the
  finite-slope support-wise MCA convention.
- **How it is useful:** Records a quotient-core mechanism for agreements up to
  `352`.  This was briefly the lower-bound frontier, but it is now superseded
  by the generic tangent floor, which gives `LD_sw(C,352) >= 161` and
  `LD_sw(C,353) >= 160`.
- **What to do next:** Keep the packet as a quotient-core mechanism record and
  compare it against any non-tangent mechanisms that might survive past
  agreement `507`.

### 2026-06-26 - Strict264 quotient-floor proof packet

- **Agent/model:** Codex, with user-supplied strict264 packet.
- **Files added or changed:** `experimental/data/strict264/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A strict264 quotient-core proof packet: generated
  field entropy/list-floor notes, a deep-point list-to-MCA conversion section,
  a calculator for entropy/MCA floors, and the concrete
  `RS[F_17^32,H,256]`, `|H|=512`, agreement-264 quotient-floor obstruction.
  The local audit fixed two TeX transcription errors and regenerated the saved
  calculator output with the exact value `log2(17^32)`.
- **How it is useful:** Gives a direct quotient-core route to
  `epsilon_mca(C,31/64)>2^-128`: `binom(64,33)` augmented-code list points
  imply at least nine support-wise bad slopes after the deep-point conversion,
  while seven slopes already clear the `F_17^32` denominator.
- **What to do next:** Keep the theorem package as a quotient-core mechanism
  record.  The moving-root tangent floor supersedes the old strict264/265
  target by giving `LD_sw(C,264) >= 249`.

### 2026-06-26 - Towards-prize finite-threshold theorem section

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A new `Towards-Prize Finite-Threshold Theorems`
  section for `experiments.tex`: certificate-to-`LD_sw`, fixed-locator
  unique-slope, base-valued subfield confinement, the exact seven-slope
  arithmetic gate over `F_17^32`, and the one-step staircase pinning criterion.
- **How it is useful:** Converts the strict264 and 265 goals into theorem-level
  proof obligations that agents can attack without claiming a new numerator or a
  corrected-reserve MCA theorem.
- **What to do next:** Use the fixed-locator principle to build
  duplicate-aware strict264 and 265 search certificates.

### 2026-06-26 - One-by-one experiment run

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/experiment-run-2026-06-26.json`,
  `experimental/notes/triage/experiment-run-2026-06-26.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/updates.json`.
- **Status:** AUDIT / EXPERIMENTAL RUN.
- **What is being added:** A sequential run of the current Cycle120,
  strict264, reserve-ladder, F1, L2, A0, and M2 validators.  All executed
  scripts passed, but no script produced a new retained-slope certificate or
  improved frontier numerator.
- **How it is useful:** Confirms that the current proof infrastructure is
  internally consistent and isolates the exact next strict264 blocker:
  seven explicit retained bad slopes at agreement `264` for the
  `RS[F_17^32,H,256]` row.
- **What to do next:** Build the strict264 seven-slope certificate and an
  independent replayable certificate for the existing `52,747,567,092` count.

### 2026-06-26 - PR #108--#119 proof and audit integration

- **Agent/model:** AllenGrahamHart PRs #108--#112, #114--#118, Scott Hughes
  PRs #113 and #119, reviewed and integrated by Codex with topic-split validity
  checks.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-26.md`,
  `experimental/data/pr-triage-2026-06-26.json`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2}/` and
  `experimental/scripts/`.
- **Status:** PROVED / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** A one-by-one integration of PRs #108--#119.  The
  theorem-level additions are the F1 syndrome-pencil normal form, the L2
  codegree reduction, the A0 deep-point MCA-cap dependency split, and the M2
  common code-line residual budget.  The remaining material is kept as route
  cuts, audits, or proof programs.
- **How it is useful:** Gives future theory work cleaner local statements for
  F1, L2, Paper D/A0, and M2, while preserving conservative public status.  No
  new prize-worthy numerator or frontier point is claimed.
- **What to do next:** Human-review the theorem-level additions before any
  main-paper promotion, citation-check the mixed-Weil route in PR #119, and
  require a retained-slope proof before treating strict264 as more than a
  target.

### 2026-06-25 - Latest PR integration and estimate audit

- **Agent/model:** AllenGrahamHart PRs #101--#107, ScottDHughes PR #99, and
  Cycle120 audit material from PR #100/#105, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-25.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2,x1}/`,
  `experimental/scripts/`, and `experimental/lean/rs_mca_formalization/`.
- **Status:** AUDIT / EXPERIMENTAL / PROOF-CHECK-NEEDED / CONDITIONAL.
- **What is being added:** A one-by-one integration of PRs #99--#107. The
  Cycle120 numerator is unchanged at `52,747,567,092`; the useful improvements
  are the standalone Cycle120 `LD_sw` proof note, the exact M2
  `epsilon_mca = LD_sw/|F|` bridge, stronger F1 extension-line lower floors,
  an M1 beta-pushforward spectral audit, and sharper L1/L2 proof-program
  targets.
- **How it is useful:** Gives future theory work better normalized estimates
  without editing Papers A--D. In particular, the current ABF-row obstruction
  still points to `epsilon_mca(C,125/256)>2^-128` and the Cycle119 strict
  endpoint `delta*_C <= 249/512`, while L1/L2/F1/X1 now have cleaner
  follow-up notes and standard-library verifiers.
- **What to do next:** Do a human proof review of the standalone Cycle120
  proof chain, then run selected nonmutating verifiers in a controlled pass.
  Treat PR #100's raw generated packet as superseded by the compact audit and
  standalone proof note unless a reviewer explicitly needs the raw replay
  material.

### 2026-06-23 - Cycle119 admissibility review

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus wording cleanup
  in the prior Cycle84 public replay audit.
- **Status:** AUDIT / PROOF-CHECK-NEEDED / COMPUTATION-DEPENDENT.
- **What is being added:** A compact review of the Cycle119 strict-263 claim:
  `LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092`, with `|H|=512`, and an
  admissibility check against the local ABF-aligned definitions and public
  Proximity Prize page.
- **How it is useful:** Separates the potentially important theorem claim from
  Danny's raw/generated PR branch. The branch is not integrable as-is, but the
  two-ended locator transfer is now the right object to demand as a clean proof.
  If the proof and finite computation check out, the right public framing is a
  prize-facing negative counterexample candidate under the printed ABF
  formulation, not an accepted prize solution.
- **What to do next:** Independently fetch and check the ABF PDF, then ask Danny
  for a standalone human-readable proof of the two-ended locator transfer and a
  separate minimal record of the Cycle84 finite computation it consumes.

### 2026-06-23 - Cycle120 ABF counterexample candidate integration

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md`,
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, and `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROOF-SPINE-CHECKED / COMPUTATION-DEPENDENT /
  SOURCE-AUDIT.
- **What is being added:** A cleaned integration of the Cycle120 ABF-facing
  negative result. It records that Cycle116 agreement `262` is enough for the
  printed ABF closed threshold at `delta=125/256`, while Cycle119 agreement
  `263` checks as a strict-ball strengthening. The note now states explicitly
  that this is only a negative obstruction to
  `epsilon_mca(C,125/256) <= 2^-128` for one row, not ordinary list decoding,
  protocol soundness, or an exact determination of `delta*_C`. It also records
  the endpoint nuance: Cycle116 gives `delta*_C <= 125/256` under a supremum
  convention, while Cycle119 gives `delta*_C <= 249/512 < 125/256`.
- **How it is useful:** Moves the useful part of PR #96 into a compact
  experimental note without importing zips, generated checkers, copied PDFs,
  rendered pages, or raw prompt archives. It gives the project a concrete
  human-review target: the Cycle84/Cycle116 finite proof chain plus the
  optional Cycle119 strict-ball proof.
- **What to do next:** Independently retrieve the ABF PDF, review the finite
  count and fixed-jet transfer, and ask Danny for a minimal nonmutating reviewer
  packet in proof/computation/audit language.

### 2026-06-22 - PR #96-#98 experimental triage

- **Agent/model:** DannyExperiments, avdeevvadim, scottdhughes; integrated by
  Codex.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-06-22.md`,
  `experimental/notes/m1/m1_cycle84_public_replay_audit.md`,
  `experimental/notes/f1/f1_deep_point_list_to_ca_mca.md`,
  `experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py`,
  `experimental/notes/l1/l1_prefix_fourier_orbit_cancellation.md`,
  `experimental/scripts/verify_l1_fourier_orbit_cancellation.py`,
  `experimental/SUMMARY.md`, `experimental/README.md`,
  `experimental/scripts/README.md`, and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE_MODEL_PROOF / PROVED / CONDITIONAL /
  EXPERIMENTAL.
- **What is being added:** A conservative triage of PRs #96--#98. PR #96's
  useful Cycle84 public replay record is kept as an inert audit note:
  `m_max(beta)=2`, `Occ(beta)=52,747,567,092`, `D=24`, twelve double fibers,
  and no fibers of size at least three. PR #97 adds the F1 simple-pole
  deep-point list-to-CA/MCA conversion note and sanity script. PR #98 adds the
  L1 dual-dilation Fourier orbit-kernel reduction note and verifier.
- **How it is useful:** Cycle84 now has a public replay record for the finite
  M1 wall without importing the live workflow or raw archive. The F1 note gives
  a direct special list-to-CA/MCA mechanism to audit against Paper D. The L1
  note moves prefix-local work from individual Fourier frequencies to orbit
  kernels and records a concrete route cut for pointwise kernel saving.
- **What to do next:** Do not treat Cycle84 as a prize-level theorem until a
  transfer theorem is proved. Audit #97 against the exact main-paper `eca` and
  `emca` predicates before any promotion. Run the new scripts only after
  reviewer approval; this triage pass inspected them as text but did not
  execute PR code.

### 2026-06-19 - Experimental folder streamlining

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/README.md`,
  `experimental/notes/README.md`, `experimental/scripts/README.md`,
  `experimental/data/README.md`, plus repository moves under
  `experimental/notes/`, `experimental/scripts/`, `experimental/data/`, and
  `experimental/lean/`.
- **Status:** AUDIT.
- **What is being added:** Reorganized the experimental workspace into four
  durable buckets: notes, scripts, compact data, and Lean. Removed generated
  Python caches and raw/prompt transcript dumps from dated AI-loop outputs.
- **How it is useful:** Future agents now have a small root surface and a clear
  placement policy. Audited summaries and reproducible scripts remain, while
  bulky model-run provenance that was not needed for review is gone.
- **What to do next:** Keep new work inside the existing buckets, update
  `README.md` if a genuinely new bucket is needed, and avoid adding raw
  transcript archives unless they are the only reproducibility record.

### 2026-06-19 - PR #82/#84-#95 experimental integration

- **Agent/model:** AllenGrahamHart, scottdhughes, latifkasuli,
  DannyExperiments PRs, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-19.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/notes/l1/l1_prefix_divisor_count.md`,
  `experimental/notes/l1/l1_quotient_defect_closure.md`,
  `experimental/notes/l1/l1_repaired_locator_theorem_package.md`,
  `experimental/notes/l2/l2_interleaved_dilation_constants.md`,
  the NFB frontier JSON data folder,
  `experimental/notes/m1/m1_residue_line_roadmap.md`, M1 depth-two Kummer notes and
  verifiers, L1/L2 verifier scripts, and the selected
  `experimental/notes/f1/fable-loop/PRZ_REVIEW_INDEX.md` Cycle 49--57 audit
  layer.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT, as
  marked per file.
- **What is being added:** Manual integration of the useful recent PRs:
  PR #93 supersedes #85--#91 as the Scott L1 consolidation; PR #84 adds the
  L1 prefix/divisor/Fourier split; PR #92 adds L2 interleaved dilation and
  quotient-core constants; PR #94 adds a compact `F\B` deep-hole proof
  record; PR #82 adds the M1 low-slack Kummer/depth-two packet; PR #95 is
  integrated only as review index plus cycle audits, not as a raw 225k-line
  archive.
- **How it is useful:** Gives future work clear entry points: L1 quotient
  floors versus aperiodic Fourier cancellation, M1 two-coordinate/conductor
  targets, L2 aligned interleaved constants, an F1/Paper D explicit-line
  proof target, and a compact Fable-loop upper-side route map.
- **What to do next:** Run and review the integrated verifiers, add a
  standalone verifier for the NFB JSON record, audit the M1 Kummer imports
  before consuming constants, and continue the Fable-loop program from the
  high-`j` constant-rate prompt rather than the cut `t=2,j=2` toy regime.

### 2026-06-18 - PR #79-#81 experimental integration

- **Agent/model:** AllenGrahamHart and scottdhughes PRs, integrated by Codex.
- **Files added or changed:** `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_kummer_divisor_geometry.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/l1_arbitrary_fiber_repair.md`,
  `experimental/verify_l1_arbitrary_fiber_repair.py`,
  `experimental/a0_external_import_source_check_20260618.md`,
  `experimental/a0_import_source_probe.py`,
  `experimental/pr-triage-2026-06-18-round3.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL / COUNTEREXAMPLE.
- **What is being added:** Manual integration of PR #79's M1 depth-two
  Kummer-window material, PR #80's L1 arbitrary-fiber repair note, and PR
  #81's A0 external-import source check.  The M1 material is explicitly
  conditional on the isolated Kummer-Weil import; the L1 material repairs a
  false raw-support arbitrary-fiber route; the A0 material records source
  reachability without closing the Paper D import audit.
- **How it is useful:** Narrows three active ledgers without editing Papers
  A--D: M1 gains a sharper lift-window/saturation audit, L1 gets a corrected
  list-object target, and A0 has a reproducible source-access record for the
  universal-cap import chain.
- **What to do next:** Prove or cite the M1 `16p` Kummer estimate, decide
  whether Paper B should promote `ImgFib_U(s)` or another repaired L1 object,
  and obtain the CS25/ABF PDFs needed to close the remaining A0 checks.

### 2026-06-18 - Four-item packet label clarification

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / CLARIFICATION.
- **What is being added:** Adds a self-contained explanation of what the
  AI-packet labels (a)--(d) mean: weak-slack positive regime, finite
  Fermat-prime packet, exponential-field construction, and imported BCHKS
  quotient-locator packet.
- **How it is useful:** Makes the experimental PDF readable without knowing
  the earlier discussion, and separates imported locator material from the
  independent local Paper B divisibility-gate theorem.
- **What to do next:** If the original four-item packet is archived in the
  repo, cross-link this clarification to the exact source file or PR.

### 2026-06-18 - Streamlined imported-locator ledger

- **Agent/model:** Human-provided streamlined note, logged by Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / IMPORTED / WRAPPER / TARGET / NEW-LOCAL.
- **What is being added:** Replaces the narrower attribution note with a
  unified experimental ledger titled *Experimental Theorems and
  Imported-Locator Ledger for RS-MCA*.  The note explicitly imports the
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf quotient-locator construction,
  gives the smooth-quotient notation dictionary, records the shared locator
  identity as imported rather than new, adds a list-fiber pigeonhole wrapper,
  states a slack-two/subfield target for the Paper D route, and preserves the
  Cycle 14--18 Paper B divisibility-gate theorem.
- **How it is useful:** Streamlines promotion decisions for Papers A--D:
  locator proofs from BCHKS must be cited at theorem and proof entry points;
  repository-side contributions are limited to dictionary/wrapper/ledger
  packaging unless separately proved; Paper D gets a precise augmented-code
  and subfield-pigeonhole target; Paper B keeps the independent restricted
  resonance gate as local experimental mathematics.
- **What to do next:** When editing the main papers, add the `BCHKS25`
  bibliography entry and cite Theorems 7.1 and 1.13 exactly where the locator
  construction is used.  Audit the augmented-code rung, slope field
  (`B` versus `F`), locator-codeword distinctness, and slack normalization
  before promoting any wrapper to a theorem.  Continue scanner work on the
  `G==0` divisibility-gate branch for the Paper B resonance window.

### 2026-06-18 - Proximity-gap attribution audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / ATTRIBUTION.
- **What is being added:** Records that the AI-generated result (d) should be
  treated as an imported adaptation of Theorem 1.13 of
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf, *On proximity gaps for
  Reed--Solomon codes*, rather than as a new repository contribution.  Also
  records the limitations of items (a)--(c): `1/sqrt(n)` slack, only three
  Fermat primes, and exponential field size.
- **How it is useful:** Gives Papers B/D/C a conservative integration plan:
  cite the external theorem, separate it from the Crites--Stewart import, and
  audit the consumed object before any MCA, line-decoding, or protocol ledger
  claim.
- **What to do next:** Add the bibliographic entry and exact theorem
  cross-reference when the main papers are edited, then verify whether item
  (d) converts to the RS-MCA object actually needed by Paper B.

### 2026-06-18 - PR #78 M1 residual-depth hierarchy

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_full_domain.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Integrated Allen's PR #78 M1 residual-depth
  hierarchy: the depth-two/next-slack transition theorem, terminal pure-zero
  residual-depth ledger, first-nonzero frontier partition, full-domain
  slack-two depth-two saturation verifier, and a high-index ceiling for the
  slack-two depth-two frontier.
- **How it is useful:** Separates inherited zero strata from genuinely new
  first-nonzero coefficient images in the M1 canonical-support scanner, giving
  sharper targets for Paper B's corrected MCA residue-line program.
- **What to do next:** Use the new verifier and scanner fields to attack
  proper-subgroup coset-image bounds, especially intermediate-index cases not
  decided by full-domain saturation or the coarse high-index ceiling.

### 2026-06-18 - Experimental theorem note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / HEURISTIC / AUDIT.
- **What is being added:** A standalone LaTeX note collecting restricted
  Cycle 14--18 theorems and heuristics, including the Cycle 18
  divisibility-gate theorem with proof.
- **How it is useful:** Gives the experimental proof material a citable,
  compiled form without editing Papers A--D.
- **What to do next:** Extend the scanner to test the `G==0` gate and decide
  whether any source-valid growing-prime family has two-dimensional slope-map
  image.

### 2026-06-18 - Cycle 18 resonance slope-map reconstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/f1/fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/scripts/fable_loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/notes/f1/fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROOF-SKETCH / EXACT_NEW_WALL / AUDIT.
- **What is being added:** A local reconstruction of Danny's Cycle 18
  `t=2,j=3` resonance reduction: `Delta` becomes a monic quadratic in
  `tau3`, the alpha component is at most linear, and the non-coprime branch
  reduces to either `Delta1==0` or the graph `tau3=-h/s`. The audit also
  records the divisibility-gate theorem: if the cleared graph polynomial
  `G=s^2 Delta0(tau1,tau2,-h/s)` is nonzero, the branch is already
  curve-sized and contributes only `O(p)` slopes.
- **How it is useful:** Sharpens the Paper B/F1 restricted toy-window wall
  from the Cycle 16 `Q==0` split to a concrete rational slope-map collapse
  question.
- **What to do next:** Extend the Cycle 17 scanner to compute the graph branch
  and projective map image on source-valid split cubics across growing primes,
  with `G==0` as the first exact gate for possible `Theta(p^2)` behavior.

### 2026-06-18 - Paper B counterexample comparison

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/paper_b_counterexample_comparison.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A theory-side comparison between recent
  experimental counterexamples and Paper B's locator-fiber, residue-line,
  extension-field, tangent-floor, and line-decoding statements.
- **How it is useful:** Identifies the raw arbitrary locator-fiber conjecture
  as needing repair, while separating route-cut counterexamples from genuine
  threats to the corrected MCA conjecture.
- **What to do next:** Review the proposed Paper B repairs, especially the
  replacement of raw `Fib_U` by a pruned/full-support arbitrary-word object.

### 2026-06-18 - Experimental summary

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/SUMMARY.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A high-level summary of the recent PR wave and the
  current contents of `experimental/`, organized by how the material advances
  the corrected MCA program.
- **How it is useful:** Gives new agents and human reviewers a map of which
  experimental notes support L1, M1, M2, F1, L2, A0/A1, protocol ledgers, and
  formalization, while keeping proof status conservative.
- **What to do next:** Use the summary as an orientation map, then verify
  individual claims from their source notes and scripts before promotion.

### 2026-06-18 - New PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #67,
  #69, #70, #71, #72, #73, #74, #75, and #77; recorded #68 and #76 as
  superseded by #77; added `experimental/pr-triage-2026-06-18.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Second open-PR triage pass covering M1, F1, L2,
  M2, L1, A1, Fable-loop, and locator-fiber cross-check contributions.
- **How it is useful:** Banks useful experimental notes, verifiers, scanners,
  and audit provenance while preserving the rule that main papers remain
  unchanged and new material stays in `experimental/`.
- **What to do next:** Run full verifier coverage, review mathematical claims
  before promotion, and close the source PRs as manually integrated or
  superseded once this commit is pushed.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, proof records, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
