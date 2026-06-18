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
- **What is being added:** State the claim, note, scan, script, or certificate
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-19 - L1 arbitrary-word lift: dilation symmetry and folding source

- **Agent/model:** Claude Opus 4.8 (L1 loop, branch `allen/l1-prefix-divisor-count`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md` (new §9),
  `experimental/verify_l1_arbitrary_word_lift.py` (new),
  `experimental/agents-log.md`.
- **Status:** PROVED (two theorems) / EXPERIMENTAL (verifier).
- **What is being added:** Lifts the symmetry/quotient theory from the
  monomial-prefix fiber to the honest list `ImgFib_U` for arbitrary received
  words. (1) Dilation symmetry: `U^h(x)=U(h^{-1}x)`, `P|->P(h^{-1}x)` is a
  list-size-preserving bijection, so `Lst` is dilation-orbit-invariant and the
  aperiodic-codeword count is divisible by `per(U)`. (2) Folding source: for
  `U=V(X^d)`, `W|->W(X^d)` injects the folded list `ImgFib_V(s/d)` over
  `RS[mu_{n/d}, k/d]` into `ImgFib_U(s)` --- the field-independent quotient-core
  floor for arbitrary words. Verifier confirms both at `F_17, n=16` (dilation
  invariance; folding lift for d=2,4).
- **How it is useful:** Extends §§5-7 from prefix words to all words, identifying
  periodic received words as the quotient-core source and isolating the
  aperiodic (trivial-stabilizer) arbitrary-word list as the remaining target.
- **What to do next:** Bound the aperiodic arbitrary-word list above the reserve;
  note that listed codewords need not be periodic, so the folded copy is a lower
  bound only.

### 2026-06-18 - L1 non-enumerative DP counter and first sub-Johnson evidence

- **Agent/model:** Claude Opus 4.8 (L1 loop, branch `allen/l1-prefix-divisor-count`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md` (new §8),
  `experimental/verify_l1_prefix_divisor_count.py`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL (tool + data) / AUDIT (closed-form cross-check).
- **What is being added:** A non-enumerative DP counter carrying
  `(size, e_1..e_eff mod q)` via `e'_i = e_i + h e_{i-1}`, reaching `n=32`
  (and `n=64` for sigma<=2) far beyond brute force, plus a closed-form
  structured-count function. Verified to reproduce the brute-force size
  distribution at `n=16` and to sum to `binom(n,m)`. Over `F_257, n=32, k=2,
  sigma=2` (entropy +0.88 bits AND sub-Johnson `a^2=16 < n(k-1)=32`): global
  max fiber `8 = binom(8,7)` = the quotient-core floor, while the max APERIODIC
  (`g_c=1`) fiber is only `5`.
- **How it is useful:** First direct evidence that conj:prefix-local holds
  beyond the Johnson radius, with the quotient core as the sole large-fiber
  source --- a regime `n=16` cannot reach. Validates §2-§7 at new parameters.
- **What to do next:** Coset-folded DP (`Y=X^d`) or character-sum evaluation to
  push sigma higher; the asymptotic `sigma=Theta(n/log n)` regime still needs
  the analytic aperiodic bound (out of exact-computation reach).

### 2026-06-18 - L1 prefix-space localization of the quotient core

- **Agent/model:** Claude Opus 4.8 (L1 loop, branch `allen/l1-prefix-divisor-count`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md` (new §7),
  `experimental/verify_l1_prefix_divisor_count.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED (theorem) / EXPERIMENTAL (verified).
- **What is being added:** The prefix stabilizer `H_c = Stab_star(c) = K_{g_c}`
  with `g_c = gcd(n, {j : c_j != 0})` acts on the fiber, and any divisor's
  dilation stabilizer satisfies `Stab_H(A) ⊆ H_c`, i.e. `per(A) | g_c`. Hence
  (i) `g_c = 1` (e.g. `c_1 != 0`) fibers are purely aperiodic; (ii) period-`d`
  mass lives only where `c_j = 0` for all `d ∤ j` (a `q^{-ceil(sigma/2)}` slice
  for dyadic n); (iii) `K_{g_c}`-orbit of `A` has size `g_c/gcd(g_c,per(A))`, so
  the per=1 count in any fiber is divisible by `g_c`. All three verified across
  the 35-case sweep.
- **How it is useful:** Complements §5 (divisor-space localization) by pinning
  the quotient core in prefix space: the remaining open step (the aperiodic
  upper bound for conj:prefix-local) is now isolated to the *generic*
  quotient-free fibers, where no quotient correction can occur.
- **What to do next:** Bound the generic purely-aperiodic fiber by
  `binom(n,s)/q^sigma + O(n^B)`, using the §7(iii) orbit-divisibility and §6
  large-orbit structure against Paper B's sec:pairwise barrier.

### 2026-06-18 - L1 dilation equivariance and the period stabilizer

- **Agent/model:** Claude Opus 4.8 (L1 loop, branch `allen/l1-prefix-divisor-count`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md` (new §6),
  `experimental/verify_l1_prefix_divisor_count.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED (lemma + proposition) / EXPERIMENTAL (verified).
- **What is being added:** The dilation action `h.A = {ha}` satisfies
  `e_j(h.A) = h^j e_j(A)`, so prefix keys transform by the star-action
  `h*(c_1,...,c_sigma) = (h c_1,...,h^sigma c_sigma)` and fiber sizes are
  constant on star-orbits (worst-case reduction by up to a factor n). Proves
  `Stab_H(A) = K_{per(A)}` is exactly the maximal coset-union period, so
  quotient-periodic <=> per(A) > sigma; the aperiodic family then has dilation
  orbits of size >= n/sigma. Also hardened the key for the degenerate sigma>=m
  branch (now correctly all-singletons).
- **How it is useful:** Unifies the dilation symmetry with the §2-§5
  quotient-core separation, explains the dilation-orbit structure of the F_17
  collisions, and gives a non-pairwise handle (orbit/divisibility constraints)
  that is the most promising route past Paper B's sec:pairwise barrier toward
  the aperiodic-remainder bound.
- **What to do next:** Use the star-action of Stab_star(c) on a single fiber to
  derive divisibility/orbit constraints on aperiodic fiber sizes beyond Johnson.

### 2026-06-18 - L1 exact quotient-core count via subgroup-lattice Mobius

- **Agent/model:** Claude Opus 4.8 (L1 loop, branch `allen/l1-prefix-divisor-count`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md` (new §5),
  `experimental/verify_l1_prefix_divisor_count.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED (lemma + theorem + corollary) / EXPERIMENTAL (verified).
- **What is being added:** Upgrades the per-`d` quotient-core floor to the
  *exact* structured-divisor count. Proves the lcm-closure lemma
  (`CU_d ∩ CU_e = CU_{lcm(d,e)}`), hence the exact count of divisors that are
  `K_d`-coset-union for some active `d > sigma` is the subgroup-lattice Möbius
  sum `sum_{∅≠T⊆S} (-1)^{|T|+1} binom(n/lcm(T), m/lcm(T))`, and the dyadic
  collapse `binom(n/d_*, m/d_*)` for `n = 2^{m_0}`. The aperiodic divisor count
  is then exact. Verifier confirms direct == incl-excl and the collapse across
  the 35-case sweep, and reports the maximal *aperiodic* fiber and the random
  baseline.
- **How it is useful:** Gives the exact field-independent quotient-core mass in
  `conj:prefix-local` (not just a one-subgroup lower bound), and isolates the
  aperiodic remainder numerically at the predicted `binom(n,s)/q^sigma` scale,
  sharpening the next analytic target.
- **What to do next:** Worst-case second-moment / Plotkin bound on the
  *aperiodic* sub-family (coset-union mass removed) beating the Johnson anchor;
  then scale-up counter for `n=32,64`; then lift to `ImgFib_U`.

### 2026-06-18 - L1 prefix fibers as divisor counts, with exact quotient-core floor

- **Agent/model:** Claude Opus 4.8 (parallel L1 loop, branch
  `allen/l1-prefix-divisor-count` off `origin/main`).
- **Files added or changed:**
  `experimental/l1_prefix_divisor_count.md`,
  `experimental/verify_l1_prefix_divisor_count.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED (lemma + corollary) / EXPERIMENTAL (scan) / AUDIT.
- **What is being added:** Recasts the Paper B monomial-prefix fiber
  `Phi_sigma^{-1}(c)` (`conj:prefix-local`) as a divisor-coefficient count:
  monic degree-`m` divisors of `X^n-1` over `F_q` with prescribed top `sigma`
  coefficients, via the complement-locator bijection. Proves the
  quotient-periodic locator lemma (`K_d`-coset-union locators are polynomials in
  `X^d`, bijecting onto degree-`m/d` divisors of `Y^{n/d}-1`) and the exact
  field-independent quotient-core floor
  `max_c |Phi_sigma^{-1}(c)| >= binom(n/d, m/d)` for every `d | gcd(n,k+sigma)`
  with `d > sigma`. A standard-library scanner verifies both, reproduces the
  `F_17` certificate of `l1_aperiodic_prefix_collision.md`, and isolates the
  aperiodic remainder.
- **How it is useful:** Quantifies the `Quot_{sigma,c}` term of
  `conj:prefix-local` on the list/locator side (parallel to Codex's M1
  residue-line work on the MCA side); ties the floor to the L3 dither target
  `gcd(n,k+sigma) <= sigma`; and identifies the aperiodic divisor remainder as
  the next analytic target.
- **What to do next:** Bound the aperiodic remainder beyond the Johnson anchor;
  add a non-enumerative counter to reach `n=32,64` and `q=257`; compute the
  exact Mobius union of coset-union floors over the subgroup lattice.

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
  `experimental/2026-06-18-fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/2026-06-18-fable-loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/2026-06-18-fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.
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
  integration of accepted experimental notes, scanners, certificates, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
