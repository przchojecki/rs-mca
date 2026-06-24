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

### 2026-06-24 - X1: explicit deep-point line = constructive form of the whole universal cap (thm:main)

- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_prob_explicit_universal.py` (new),
  `experimental/notes/x1/x1_prob_explicit_deep_point.md` (generalization section),
  `experimental/agents-log.md`.
- **Status:** PROVED-by-arithmetic (correspondence with thm:main) / AUDIT.
- **What is being added:** Generalizes the prob:explicit construction from
  cor:deployed to the ENTIRE universal cap (thm:main). Key exact correspondence:
  thm:main's hypothesis eq:hyp (binom(N,rhoN+2) >= |B|(q/k+1)) IS the averaging-
  saturation condition L >= q/k+1, and at that boundary the best-alpha deep-image
  density is 1/(2k) = thm:main's exact bound (1/(2k))(1-n/q). So the explicit
  deep-point line recovers thm:main's bound under thm:main's hypothesis, via an
  explicit line (no CS25/augmented code/eta) -- making the WHOLE universal cap
  constructive, clearing 2^-128 throughout (1/(2k)>=2^-41 for k<=2^40). Verified
  at 4 cap-regime points (cor:deployed e=6, e=2 rho=1/4, subgroup q~2^64, large
  k=2^40 e=2). REFINEMENT: non-B-rational (prob:explicit/cor:Fvalued) holds in the
  extension regime exactly when v2(q-1)>=v2(a_q) (so alpha^{a_q} keeps full degree
  e); subgroup case isn't non-B-rational; large-a_q e=2 fails the 2-power cond
  (cap bound still holds, slopes may confine). [Corrected an earlier loose
  "uniformly 1/k": the bound is (1/(2k))(1-n/q), regime-dependent, = thm:main.]
- **How it is useful:** Upgrades the result from "explicit cor:deployed witness"
  to "explicit/constructive form of the entire universal cap" -- the deep-point
  line is the constructive replacement for the CS25 conversion in thm:main.
- **What to do next:** Consider whether the subgroup-case explicit line (cap but
  B-rational) is worth a separate note; or pivot. Could flag the thm:main-level
  generalization to the Paper D thread.

### 2026-06-24 - X1: explicit non-B-rational MCA-bad lines for Paper D prob:explicit

- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_prob_explicit_deep_point.md` (new),
  `experimental/scripts/verify_x1_prob_explicit_mechanism.py` (new),
  `experimental/scripts/verify_x1_prob_explicit_deployed.py` (new),
  `experimental/agents-log.md`.
- **Status:** PROVED (density bound) / AUDIT. Explicit family + rigorous
  generic-alpha density; not a single brute-certified F_{p^6} line.
- **What is being added:** A constructive advance on Paper D `prob:explicit`
  (`cs25_cap_v4.tex`): the simple-pole deep-point line f=u_z/(x-alpha),
  g=-1/(x-alpha) on Paper D's own lem:fiber heavy word, with denominator
  X-alpha not over B. By the deep-point identity its MCA-bad slopes are the deep
  image {P(alpha)}; at cor:deployed params (KoalaBear sextic F_{p^6}, n=2^21,
  k=2^20, gap 2^-7) the averaging saturates M >= |Omega|/k ~ 2^165.9, density
  ~2^-20 (best alpha) / ~2^-21 (>=1/2 of alpha by Markov), both > 2^-22 -- the
  same 1/k as cor:deployed's CS25 bound but via an EXPLICIT line (no augmented
  code, no eta). Refinement: slopes are genuinely F-valued iff alpha^{a_q} notin B
  (quotient-periodic confinement extending lem:confine); v2(p^6-1)=25>=13 so a
  generator works. Mechanism brute-validated over F_{17^2} (identity +
  characterization F-valued <=> alpha^{a_q} notin B); deployed density by exact arithmetic.
- **How it is useful:** Makes cor:Fvalued constructive (the residue-line normal
  form prob:explicit names, made explicit), and unifies lem:confine/cor:Fvalued
  as the deep-point dichotomy alpha^{a_q} in/notin B. Builds on Codex #103.
- **What to do next:** push the construction toward a single pinned alpha if a
  feasible partial certificate exists; or pivot. Consider a PR comment flagging
  this to the Paper D / cor:Fvalued thread.

### 2026-06-24 - AUDIT of PR #100 (Cycle120 gate): arithmetic VERIFIED, result CONDITIONAL

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/audits/audit_pr100_cycle120_gate.md` (new),
  `experimental/scripts/verify_audit_pr100_cycle120_gate.py` (new),
  `experimental/agents-log.md`.
- **Status:** AUDIT / arithmetic VERIFIED (15/15) / result CONDITIONAL on imports.
- **What is being added:** Independent big-integer recomputation of the Cycle120
  deterministic gate layer: thresholds ((1-delta)n=262, delta*n=250, Cycle119
  distance 249<250), parameter envelope (17^32<2^256, |H|=2^9, rate 1/2, k<=2^40),
  the denominator crux (floor(17^32/2^128)=6, N=52.7e9>6, density -95.18), and the
  support-wise implication emca>=N/|K|>2^-128 => delta*_C<=125/256 (<=249/512 under
  Cycle119). All check. The list->MCA step is the same normalization as the
  deep-point/CA-MCA bridges. CONDITIONAL on: N itself (Cycle84 census, NOT
  reproduced -- the critical gate), Cycle116/119 transfer proofs, official ABF
  ePrint wording, H=<theta> certification.
- **How it is useful:** Confirms Codex's gate arithmetic is exactly right and its
  labeling conservative/accurate; pins the remaining gate to the unreproduced
  finite count N + transfer proofs (what Przemek wants from Danny). Independent
  second-agent check of a prize-facing candidate.
- **What to do next:** The three audit/reconcile tasks are complete. Highest-
  leverage open item repo-wide: independent reproduction of the Cycle84 count N.

### 2026-06-24 - AUDIT of PR #103 (F1 sigma=1 counterexample): VERIFIED

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/audits/audit_pr103_f1_sigma_one.md` (new),
  `experimental/scripts/verify_audit_pr103_f1_sigma_one.py` (new),
  `experimental/agents-log.md`.
- **Status:** AUDIT / VERIFIED (sigma=1 core).
- **What is being added:** Independent verification of PR #103's headline sigma=1
  extension-line counterexample. Re-derived the construction from scratch
  (monic degree-(k+1) poly vanishing on S forces z=Q_S(alpha); closing codeword
  c_S=(Q_S-z_S)/(X-alpha) is deg<k over F; far condition; distinctness via
  injective elementary-symmetric (x+y,xy)). Brute-verified over F_{p^2} for
  (p,k) in {(11,3),(13,4),(11,2)}: emca >= binom(p-a+1,2)/p^2. CROSS-CONFIRMED:
  z_S is exactly the deep image of the monomial word U=x^a, so #103's sigma=1
  family is the monomial instance of the notes/x1 §1 deep-point identity.
- **How it is useful:** Independently confirms a prize-facing F1 obstruction
  (what Przemek wants for counterexample candidates), and ties #103 to the X1
  bridge framework. Caught (and documented) one subtlety: C_F is the EXTENSION
  code, so c_S is legitimately F-valued, not base-field.
- **What to do next:** sigma=2 and slow-slack asymptotic sub-claims not brute-
  checked (same mechanism, plausible); e>=2 follows from the same numerator.
  Next audit target: PR #100 (Cycle120 gate arithmetic + list->MCA step).

### 2026-06-24 - X1 bridge: reconcile with Codex's M2 (#102) and F1 (#103) PRs

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (lane deference +
  §2.7/§2.10 cross-refs), `experimental/agents-log.md`.
- **Status:** AUDIT / coordination (no new claim).
- **What is being added:** Coordination pass after Codex opened #102 (M2 ABF/GG
  line-decoding parameter match) and #103 (F1 extension-line counterexamples).
  Adds a "deference" paragraph: this note's M2 touch (§2.7) defers to #102 for the
  protocol parameter ledger, and its F1 touch (§2.9-§2.10) is the *upper*
  structure complementing #103's *lower* bound -- a new §2.10 remark proves the
  two are consistent (the extension line is a counterexample regime; the bridge
  transfers it faithfully, it does not make emca small). Keeps #101 focused on its
  unique L2/X1 core.
- **How it is useful:** Prevents duplicate/conflicting claims across the parallel
  PRs; records that #102 owns the M2 parameter ledger and #103 owns the F1
  lower-bound. Sets up the independent audit of #103/#100 (next).
- **What to do next:** Independently audit #103 (F1 extension counterexample),
  then #100 (Cycle120 gate arithmetic + list->MCA step).

### 2026-06-24 - X1 bridge: paper-label crosswalk (promotion aid); line complete

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (crosswalk),
  `experimental/agents-log.md`.
- **Status:** AUDIT / consolidation (no new claim).
- **What is being added:** A focused paper-label crosswalk mapping §1-§2.10 to the
  exact paper statements they bear on (prob:X1; conj:prefix-local /
  conj:arbitrary-local; Paper C thm:ledger and line-decoding ledger; prob:F1,
  ass:extension-mca-lift, cor:Fvalued), so a maintainer can see for promotion that
  this note supplies the forward direction of prob:X1 and reduces the L2
  interleaved-list ledger to the L1 conj:prefix-local target.
- **How it is useful:** Makes the 15-commit X1/L2/M2/F1 + Lean contribution
  promotable by tying each result to its paper label. Disjoint from M1 #100, L1 #99.
- **What to do next:** The forward-bridge line (X1/L2/M2/F1 + protocol budget +
  Lean cores) is COMPLETE. Remaining high-value work needs mathlib (excluded) or
  is crowded (L1) / already built (L3). Recommend pausing for human direction.

### 2026-06-24 - Lean: identity/collapse statements + collision bound; gitignore

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/lean/rs_mca_formalization/RsMca/DeepPoint.lean` (extended),
  `experimental/lean/rs_mca_formalization/README.md`,
  `experimental/lean/rs_mca_formalization/.gitignore` (new),
  `experimental/agents-log.md`.
- **Status:** PROVED (Lean, no `sorry`) for the arithmetic/collision cores;
  the identity/collapse are recorded as `Prop` statements (targets).
- **What is being added:** Rounds out `RsMca.DeepPoint` (builds green): the exact
  statements `DeepPointIdentity` (MCA-bad slopes = deep image) and
  `ARegularCollapse` (interleaved list = base list) as `Prop`s, plus the proved
  `mu`-independent collision bound (`simultaneousCollision_le_k`,
  `collision_bound_mu_independent`). Adds a `.gitignore` so `.lake/`/`build/`
  artifacts are never committed.
- **How it is useful:** Records the bridge's exact theorem statements in Lean
  (agents.md "formalize definitions and exact statements") and proves the
  collision arithmetic; the finite-field/finite-set proofs need mathlib and stay
  targets. Disjoint from M1 #100, L1 #99.
- **What to do next:** A mathlib-backed layer would let the identity/collapse and
  the tight-support uniqueness be proved; heavy build, deferred. The X1/L2/M2/F1
  contribution + Lean cores are a substantial, complete body of work.

### 2026-06-24 - Lean: formalize the bridge's clique-cap and budget arithmetic (no sorry)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/lean/rs_mca_formalization/RsMca/DeepPoint.lean` (new),
  `experimental/lean/rs_mca_formalization/RsMca.lean` (import),
  `experimental/lean/rs_mca_formalization/README.md`,
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (Lean pointers),
  `experimental/agents-log.md`.
- **Status:** PROVED (Lean, no `sorry`) -- the arithmetic cores only.
- **What is being added:** First real Lean content beyond the seed: a new module
  `RsMca.DeepPoint` (stdlib-only, builds with `lake build` in ~0.5s) formalizing
  the quantitative cores of the X1/L2 forward bridge -- the deep-image predicate,
  the §2.6(C) K_{m,m} clique-cap arithmetic (`cliqueGridSize = k+m^2(a-k)`,
  `cliqueSupport_over_a`: support > a for m>=2, a>k; `cliqueGridSize_mono`), and
  the §2.6(R)/§2.8 budget exponent arithmetic (`listExponent_areg_le_worst`:
  1<=mu; `budgetClears_mono`). All theorems compile with no `sorry`.
- **How it is useful:** Answers the agents.md / readme good-first-PR #9 Lean ask
  ("not done yet"), machine-checking the bridge's Nat-arithmetic claims. The
  finite-field/combinatorial proofs (the identity, a-regular collapse) remain
  stated targets. Disjoint from M1 #100, L1 #99.
- **What to do next:** Extend the Lean module incrementally -- formalize the
  a-regular bijection's set-theoretic core and the deep-point identity statement;
  eventually connect to a finite-field layer when Mathlib is added.

### 2026-06-24 - X1/F1: extension-line forward case realized over a quadratic extension

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_extension_line.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.10 + ledger
  + status), `experimental/agents-log.md`.
- **Status:** PROVED-by-check.
- **What is being added:** Develops the §2.9 outlook into a verified F1 forward
  result over `B=F_17, F=F_17^2, alpha=t`. Confirms (1) the base identity over the
  genuine extension `Bad_MCA_F = Deep_alpha^F` (extension-valued alpha + F-words,
  planted list size 5); (2) list control `|Deep^F| <= C_{F,+} list`, governed via
  the extension-coordinate identity by the 2-interleaved BASE list (mu=e=2);
  (3) the multiplication-slice transfer (closing F-codeword's coordinates are
  deg<k over B, i.e. Phi(f)+M_z Phi(g) in C_B^2). So the extension F-line is the
  M_z-coupled slice of the e=2 interleaved bridge.
- **How it is useful:** Realizes the F1 forward direction (prob:F1) for the
  simple-pole family and ties it to the L2/X1 interleaved bridge; composes the
  deep-point identity + extension-coordinate identity + F1 transfer into one
  verified statement. General (non-simple-pole) F1 lift stays open. Disjoint from
  M1 #100, L1 #99; files in notes/x1 + scripts/verify_x1_*.
- **What to do next:** The forward-bridge note now spans X1/L2/M2/F1 (simple-pole)
  and is at a complete endpoint. Live frontier is the L1 base-list bound.

### 2026-06-24 - X1/L2: Quot_mu clarification + proof audit (forward-bridge note finalized)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (§2.2 Quot_mu note),
  `experimental/agents-log.md`.
- **Status:** AUDIT / clarification (no new claim).
- **What is being added:** Resolves the §2.2 "later pass" TODO precisely: the L2
  `Quot_mu` = `L_mu(a,tau)` (`verify_l2_quotient_core_count.py`, brute-validated,
  re-run green) is the COMBINATORIAL MAXIMUM of the structured contribution (count
  of all coset-union packet tuples), an upper bound `structured part of Lst(Int)
  <= Quot_mu`, NOT a per-word equality -- e.g. at n=16,k=8,M=2 the diagonal
  L_mu=binom(7,4)=35 while the heavy quotient-locator word realizes only 4. So no
  separate alignment is needed. Also audited the §2.3 (a-set coincidence) and
  §2.6 (`<= prod row lists <= Lst^mu`, clique cap) proofs -- sound.
- **How it is useful:** Removes a loose end and prevents a Quot_mu mis-reading
  (combinatorial max vs per-word list) before any promotion. Finalizes the
  forward-bridge note. Disjoint from #100, #99.
- **What to do next:** PR #101 is complete and audited. Live frontier is the L1
  base-list bound (everything reduces to it); full F1 dev is a separate lane.

### 2026-06-24 - X1/F1: extension-line outlook -- the F-line is a slice of the e-fold bridge

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.9 + ledger
  + status), `experimental/agents-log.md`.
- **Status:** OUTLOOK / connection (composes proved pieces; no new claim).
- **What is being added:** A concise extension-line outlook connecting the
  forward bridge to F1. Under the coordinate map Phi (Phi(C_F)=C_B^e), the
  simple-pole extension F-line is the M_z-coupled multiplication-slice of the
  e-fold interleaved bridge of §2 (mu=e): its MCA-bad slopes are the F-valued
  deep image, list-controlled by the e-interleaved base list
  (l2 §6 / snarks eq:extension-list), matching the existing F1 transfer
  (`f1_extension_coordinate_transfer.md`). The only difference from the free F^e
  slope vectors is the M_z coupling -- the extension challenge restricts to the
  1-parameter slice. No new verifier (composition of proved results).
- **How it is useful:** Shows prob:F1 (extension-line MCA) is the
  matrix-parameter restriction of the L2/X1 object developed here, so a sharp F1
  constant specializes the §2.6 reduction. Closes the forward-bridge note as
  self-contained (§1-§2.9). Disjoint from M1 #100, L1 #99; F1 lane untouched.
- **What to do next:** PR #101 (forward interleaved deep-point bridge) is at a
  clean, complete endpoint. Full F1 development is a separate lane; otherwise
  the L1 base-list bound (which everything now reduces to) is the live frontier.

### 2026-06-24 - X1/L2: conditional protocol budget (an L1 bound buys the prize regime)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_conditional_budget.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.8 + ledger),
  `experimental/agents-log.md`.
- **Status:** PROVED (conditional on the open L1 bound).
- **What is being added:** The forward bridge (§1-§2) and L2->L1 reduction (§2.6)
  compose into a conditional protocol statement: IF `Lst(C_+) <= n^B` (the open
  L1 / conj:prefix-local target) THEN the Proximity-Prize interleaved term
  `|interleaved_list|/q` is bounded by `n^{mu B}/q` (worst case) or `n^B/q`
  (a-regular), with the interleaved-MCA count `<=` the interleaved list (no sqrt
  loss). A budget calculator prints, for the prize regime (2^-128, |F|<2^256),
  the largest L1 exponent B already clearing 2^-128: e.g. n=2^40, mu=2 needs only
  B<=1.6 (worst) / 3.2 (a-regular). A modest polynomial L1 bound suffices.
- **How it is useful:** Lands the protocol impact -- an L1 list theorem converts
  DIRECTLY into the interleaved-MCA / interleaved-list soundness budget Paper C
  consumes, no separate MCA theorem and no Cartesian exponent. Closes the
  forward-bridge line. Disjoint from M1 #100, L1 #99.
- **What to do next:** The forward-bridge note is complete (§1-§2.8); a clean
  endpoint. Pivot to a fresh thread or wind down.

### 2026-06-24 - X1/M2: line-decoding reading -- MCA = CA = line-decoding coincide

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_line_decoding.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.7 + ledger),
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED-by-check.
- **What is being added:** The line-decoding reading of the bridge for M2. The
  simple-pole line's decoding list `LD(alpha;delta_a)` equals `Bad_MCA = Bad_CA =
  Deep_alpha(U,a)` -- so support-wise MCA, no-loss CA, and line-decoding COINCIDE
  on the simple-pole family; no MCA-vs-line-decoding separation occurs there, so
  any separation must come from other line families. A slope may carry several
  closing codewords (distinct C_+ list elements with equal P(alpha)), so the
  (z,c) incidence multiplicity tracks list size while the slope count is
  `<= |Lambda(C_+,delta_a,U)|`. Verified across 3 configs (306 coincidence checks).
- **How it is useful:** Connects the X1 bridge to the M2 line-decoding ledger
  Paper C consumes, gives the explicit line family + radius, and localizes any
  MCA/line-decoding separation away from the simple-pole lines. Disjoint from
  M1 #100, L1 #99; M2 has no active PR.
- **What to do next:** The forward-bridge line is at a clean endpoint (§1-§2.7);
  pivot options: align the structured count to exact L2 Quot_mu at prize params,
  or a fresh thread (M2 other line families, A0 Crites-Stewart audit).

### 2026-06-24 - X1/L2: L2 -> L1 reduction and the K_{m,m} clique-amplification cap

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_clique_cap.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.6 + ledger),
  `experimental/agents-log.md`.
- **Status:** PROVED (reduction, cap) / PROVED-by-check (grid designs).
- **What is being added:** Two honest statements closing the over-agreement core.
  (R) Reduction: `Lst(Int(C_+,mu)) <= Lst(C_+)^mu` (= `Lst(C_+)` when a-regular),
  so the worst-case interleaved list is polynomial iff the L1 base list is --
  L2 reduces to L1 with exponent in [1,mu]. (C) Clique cap: the K_{m,m} two-sided
  over-agreement design needs `n >= k+m^2(a-k)`, so its amplification `m^2` is
  linear in n and cannot beat a large base list. Grid designs for m=2,3,4
  (n=20,40,68; edges=4,9,16) verified, cross-checked vs the field-realized m=2.
- **How it is useful:** Recasts the open L2 separation question as L1-governed:
  no separate L2 theorem is needed beyond an L1 list bound, and the only
  constructive amplification route is capped. Capstone of the forward-bridge
  line. Disjoint from M1 #100 and L1 #99.
- **What to do next:** The residual (non-clique worst-case exponent > 1) is an
  L1-governed question; otherwise pivot (M2 line-decoding, Quot_mu alignment).

### 2026-06-24 - X1/L2 bridge consolidation: results ledger + PR refresh

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (top-level
  "Claim and results ledger" + proved/open boundary), `experimental/agents-log.md`;
  PR #101 description refreshed.
- **Status:** AUDIT / consolidation (no new claims).
- **What is being added:** A results-ledger table cross-referencing §1-§2.5 with
  per-section status, and a crisp proved/open statement: the forward interleaved
  bridge is complete and mu-clean (no sqrt loss, no interleaving exponent); the
  a-regular worst-case interleaved list equals the base list (exponent 1, the
  L2 -> L1 reduction); the only open piece is whether over-agreement K_{m,m}
  designs ever beat the base (Lst(Int) > Lst(C_+)).
- **How it is useful:** Makes the six-commit PR reviewable at a glance and states
  the proved/open boundary precisely; marks a clean endpoint for the forward
  bridge line. All seven verifiers re-run green.
- **What to do next:** Attack the K_{m,m} scaling open core (larger n or a
  counting bound), or pivot to an adjacent thread (align L to exact Quot_mu;
  M2 line-decoding; A0 Crites-Stewart audit).

### 2026-06-24 - X1/L2 interleaving amplification: concrete K_{2,2} over-agreement witness

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_interleaving_amplification.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.5),
  `experimental/agents-log.md`.
- **Status:** PROVED-by-check (construction) / honest negative on global separation.
- **What is being added:** Realizes the smallest two-sided over-agreement design
  with actual codewords: a K_{2,2} overlap pattern over F_41,n=20,k=4,a=8 (four
  size-12 supports, all cross-overlaps = a = 8, within-row = k = 4). Measured:
  interleaved list = 4 = edges, row lists L1=3, L2=2, supports (12,12) > a. So
  interleaved = 4 > max(L1,L2) = 3 -- interleaving STRICTLY amplifies beyond both
  participating rows, impossible in the a-regular regime (§2.3). BUT a single
  quotient-locator word already lists 10, so interleaved=4 does NOT beat the
  global base: no Lst(Int) > Lst(C_+) separation at toy scale.
- **How it is useful:** Settles that over-agreement genuinely breaks the
  a-regular collapse (concrete witness), while showing the amplification is below
  base here; a true separation needs a K_{m,m} design with m^2 > Lst(C_+), i.e.
  the overlap design must out-scale the base list -- the sharp open core, now a
  concrete combinatorial-design question. Disjoint from #100, #99.
- **What to do next:** Test whether K_{m,m} scales (larger n) past Lst(C_+), or
  prove a counting bound interleaved <= f(Lst) forbidding a worst-case separation.

### 2026-06-24 - X1/L2 interleaved list as overlap-graph edge count; open core localized

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_overlap_graph.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.4),
  `experimental/agents-log.md`.
- **Status:** PROVED (edge-count identity, tight-degree bound) / PROVED-by-check.
- **What is being added:** For mu=2 the interleaved list = #edges of the bipartite
  ">=a-overlap" graph between the two row lists. Tight (size-a) supports have
  degree <= 1, so a-regular rows make the graph a MATCHING (re-deriving §2.3 from
  the graph view); an over-agreement codeword (support > a) can have degree >= 2,
  so the a-regular hypothesis is NECESSARY. Constructed degree-2 witness over
  F_97,n=16,k=4,a=8 (over-agreeing c_2 of support 2a-k=12 adjacent to two tight
  row-1 codewords); edge-count identity verified in both regimes.
- **How it is useful:** Reduces the open L2 over-agreement core to a precise
  bipartite/hypergraph overlap-density question: a worst-case interleaved list
  beating the base list needs SIMULTANEOUS two-sided over-agreement (n >~ 2a),
  not a vague Cartesian exponent. Replaces a hand-wave with a concrete target.
  Disjoint from M1 cap audit (#100) and L1 (#99).
- **What to do next:** Search for `Lst(Int(C_+,mu)) > Lst(C_+)` at n >~ 2a with
  two-sided over-agreement, or prove a Koenig/matching-type bound forbidding it.

### 2026-06-24 - X1/L2 worst-case interleaved list = base list (a-regular)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_worst_case_interleaved.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.3),
  `experimental/agents-log.md`.
- **Status:** PROVED (theorem (i),(ii)) / PROVED-by-check.
- **What is being added:** Theorem pinning the worst-case interleaved list.
  (i) diagonal lower bound `Lst(Int(C_+,mu)) >= Lst(C_+)` all mu (off-diagonal
  impossible: distinct codewords share <=k<a points). (ii) a-regular upper bound:
  if no row codeword over-agrees (agreement exactly a) then the interleaved list
  equals `|intersect_i Supp_{U_i}^{=a}|` <= min row list, via the bridge note's
  full-agreement formula. Hence in the a-regular regime the worst-case
  interleaved list EQUALS the base-code list for every mu -- interleaving
  exponent exactly 1, not mu. Brute-verified over F_97/F_193 (mu=1,2,3, base=4,
  interleaved=4 throughout).
- **How it is useful:** Sharpest possible L2 worst-case constant in the generic
  (a-regular) regime, and the honest reduction L2 -> L1: via the deep-point
  bridge the interleaved-MCA count is governed by the base-code (L1)
  locator-fiber list, mu-independently. Disjoint from the M1 cap audit (PR #100).
- **What to do next:** the non-a-regular (over-agreement) residual -- the only
  place a genuine L2-vs-L1 separation could live; or align the structured count
  to the exact L2 Quot_mu at prize parameters.

### 2026-06-23 - X1 forward interleaved-MCA count chain (list -> MCA, L2 saving)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_forward_interleaved_count.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new §2.2),
  `experimental/agents-log.md`.
- **Status:** PROVED-by-check.
- **What is being added:** The explicit forward count chain
  `ceil(L/(1+k(L-1)/|Omega|)) <= BadVec_max = max_alpha |Deep_alpha^mu| <= L
  (interleaved C_+ list) <= prod_i L_row_i (Cartesian)`, verified on structured
  quotient-locator words over F_97 and F_193 (n=16,k=8,a=12). The interleaved
  list L=4 is CONSTANT in mu while the Cartesian product grows as 4^mu, so the
  forward interleaved-MCA bad-slope-vector count inherits the L2 no-Cartesian
  saving; density |BadVec|/q^mu <= L/q^mu, not (L_row/q)^mu.
- **How it is useful:** Closes the forward X1 chain for the interleaved object:
  an interleaved *list upper bound* (L2) bounds the interleaved-MCA bad-slope
  count at the same radius, square-root-loss-free, with no interleaving exponent
  -- the soundness term Paper C needs. Disjoint from the M1 cap audit (PR #100).
- **What to do next:** Either align L to the exact L2 Quot_mu count at prize
  parameters, or push the aperiodic mu-fold remainder (the open L2 core), now
  carrying MCA meaning through the bridge.

### 2026-06-23 - X1 interleaved deep-point identity (proved + verified)

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/scripts/verify_x1_interleaved_deep_point.py` (new),
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (§2.1 + status),
  `experimental/agents-log.md`.
- **Status:** PROVED (interleaved identity) / PROVED-by-check (verifier).
- **What is being added:** Proves and brute-verifies the mu-row interleaved
  deep-point identity `BadVec(alpha;a) = Deep_alpha^mu(U,a)` (shared-pole curves
  send interleaved column-distance lists to interleaved-MCA bad-slope vectors),
  the list bound `|Deep^mu| <= |interleaved C_+ list|`, and the mu-INDEPENDENT
  collision bound (distinct tuples agree on <= k deep points; constructively
  achieves exactly k, never more, identically for mu=1,2,3). Over F_97,n=16,k=8
  the structured list size is 4 at BOTH mu=2 and mu=3 (no Cartesian growth).
- **How it is useful:** Establishes the forward, square-root-loss-free
  list->MCA transfer in the interleaved setting (problem X1), with a constant
  that does not pay the interleaving exponent -- the object Paper C needs to read
  interleaved lists as interleaved MCA. Disjoint from the M1 cap audit (PR #100).
- **What to do next:** Commit 3 -- combine with the L2 numerator
  (`l2_interleaved_dilation_constants.md`, binom(n,a) q^{-mu(a-k)} + Quot_mu) for
  an explicit forward interleaved-MCA bad-slope-vector count vs. the list bound.

### 2026-06-23 - X1 deep-point bridge: base identity audit + interleaved target

- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Files added or changed:**
  `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (new),
  `experimental/scripts/verify_x1_deep_point_identity.py` (new),
  `experimental/agents-log.md`.
- **Status:** AUDIT (base identity) / TARGET (interleaved extension).
- **What is being added:** Independently re-derives and broadens the audit of the
  deep-point simple-pole identity `Bad_CA = Bad_MCA = Deep_alpha(U,a)` (Theorem 1.1
  of `notes/f1/f1_deep_point_list_to_ca_mca.md`): a prime-field reimplementation
  verifies it for ALL deep points `alpha in F_p \ D` and many words (312 identity
  checks, PASS, over four `(p,n,k,a)` configs), not just one extension-field word.
  States the new **interleaved (mu-row) deep-point identity** target: shared-pole
  curves convert interleaved (column-distance) lists into interleaved-MCA bad-slope
  vectors `(P_1(alpha),...,P_mu(alpha))`, with a `mu`-INDEPENDENT transfer constant
  (distinct tuples differ in some row, giving `<= k` simultaneous collisions).
- **How it is useful:** Opens the forward/positive half of the deep-point program
  for X1 and L2: list upper bounds -> interleaved MCA, the object Paper C consumes.
  Explicitly disjoint from the base-code *cap* direction in M1 audit PR #100
  (`codex/m1-cycle120-gate-audit`); different files, different inclusion direction.
- **What to do next:** Prove + verify the interleaved identity (commit 2:
  `verify_x1_interleaved_deep_point.py`, `mu=2,3` over `F_17`); then combine with
  the L2 numerator (`l2_interleaved_dilation_constants.md`) for an explicit
  forward interleaved-MCA count.

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
