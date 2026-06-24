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

### 2026-06-24 - L1 cofactor-budgeted full-petal layers

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A full-petal layer bound derived from the cofactor
  injection.  The number of full-petal extras with `ell<=d<=ell+E` is at most
  `binom(M,2)q + 2^M sum_{e=1}^E q^{e+1}`.
- **How it is useful:** Refines the bounded-excess analysis by showing that
  the residual full-petal obstruction must have cofactor excess beyond the
  explicit budget `2^M q^{E+1}<=n^{O(1)}`, not merely sit at the CRT boundary.
- **What to do next:** Attack the genuinely growing-excess split-locator
  concentration problem, or turn to the diffuse partial-petal residual.

### 2026-06-24 - L1 uniform full-petal cofactor injection

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A uniform cofactor-injection lemma for full-petal
  sunflower layers.  For fixed `I` and `d`, actual monic missed-core locators
  inject into the cofactor space of dimension `d-ell+1`, giving the bound
  `q^{d-ell+1}` for all `ell<=d<=(t-1)ell`.
- **How it is useful:** Removes the apparent extra `q` factor at the
  top-defect boundary by using monicity of split locators, so the full-petal
  residual is cleanly a split-locator concentration problem rather than a CRT
  boundary artifact.
- **What to do next:** Bound or structurally classify split monic locators in
  the growing-excess cofactor images.

### 2026-06-24 - L1 full-petal top-defect rank

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A top-defect rank lemma for the full-petal CRT map.
  At `d=(t-1)ell`, the top-coefficient map has full target rank `ell-1`,
  giving the fixed-`I` bound `q^(d-ell+2)`.
- **How it is useful:** Completes the rank analysis of the full-petal CRT map:
  both below and at the top-defect boundary, the remaining issue is
  split-locator concentration inside an explicit kernel, not CRT rank loss.
- **What to do next:** Bound split core locators inside the full-petal CRT
  kernels, or classify kernel concentration as quotient/defect structure.

### 2026-06-24 - L1 full-petal high-rank lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A high-rank lemma for the full-petal CRT map below
  the top-defect boundary.  For `t>=3` and `d<(t-1)ell`, the map has rank at
  least `ell`, so fixed `(I,d)` full-petal extras are bounded by
  `q^(d-ell+1)`.
- **How it is useful:** Shows the residual full-petal regime below top defect
  is not a low-rank CRT failure; any large family must instead be a
  split-locator concentration inside a growing kernel.
- **What to do next:** Study split core locators inside those kernels, and
  treat the exact top-defect boundary separately.

### 2026-06-24 - L1 background-free residual normal form

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A residual normal-form proposition for the
  background-free sunflower obstruction.  After unioning the proved polynomial
  layers, any remaining super-polynomial family must be either a
  growing-excess full-petal CRT-kernel family or a diffuse partial-petal
  family with no bounded-deficit petal pair.
- **How it is useful:** Consolidates the sunflower proof program into a clear
  endpoint: it identifies exactly which regimes are already controlled and
  which two regimes remain as genuine targets.
- **What to do next:** Attack the two residual regimes directly, or focus
  counterexample searches only on those regimes instead of already-controlled
  scan profiles.

### 2026-06-24 - L1 two-petal syzygy compression

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A two-petal syzygy compression for arbitrary
  partial-petal sunflower extras, plus a counted near-saturated corollary.  If
  two touched petals have bounded deficits and `d-ell` is bounded, the family
  has polynomially many syzygy certificates.
- **How it is useful:** Extends the full-petal proof mechanism to partial
  petals and rules out small perturbations of the full-petal obstruction as a
  super-polynomial family.
- **What to do next:** Study partial-petal extras with no two near-saturated
  petals, where any remaining large family must distribute agreement more
  diffusely across petals or have growing defect excess.

### 2026-06-24 - L1 bounded-excess full-petal count

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A polynomial bound for background-free full-petal
  sunflower extras with bounded excess core defect `d-ell<=e0`, using a
  two-petal syzygy certificate.  The bound is
  `binom(M,2) sum_{e<=e0} q^{2(e+1)}`.
- **How it is useful:** Closes a growing-defect neighborhood of the minimal
  layer.  Any remaining full-petal super-polynomial obstruction must have
  both `t>=3` and `d-ell` growing with `n`.
- **What to do next:** Attack genuinely growing-excess full-petal rank defects
  or move to partial-petal agreement patterns using the same core-defect
  framework.

### 2026-06-24 - L1 minimal-defect full-petal count

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A polynomial bound for all background-free
  full-petal sunflower extras with minimal core defect `d=ell=sigma+1`,
  including extras touching three or more petals: at most `binom(M,2)q`.
- **How it is useful:** Closes a growing-defect layer, not just a fixed-defect
  layer.  Any remaining full-petal super-polynomial obstruction must have both
  `t>=3` touched petals and defect `d>ell`.
- **What to do next:** Analyze the higher-defect many-petal rank problem from
  the CRT top-coefficient map, or identify quotient/defect structures causing
  rank loss.

### 2026-06-24 - L1 full-petal rank certificate

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A rank-certificate formulation for full-petal
  sunflower extras.  For fixed touched petals `I` and defect `d`, extras inject
  into split core locators in the kernel of the CRT top-coefficient map, giving
  the bound `q^(d+1-r_{I,d})`.
- **How it is useful:** Reduces the remaining full-petal amplification problem
  to proving high rank for an explicit finite-dimensional linear map, or
  classifying its quotient/low-defect rank defects.
- **What to do next:** Analyze the rank of `pi_{>d}R_{I,d}` for `t>=3`, and
  compare low-rank cases with known quotient or defect-closure structures.

### 2026-06-24 - L1 full-petal CRT compression

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A CRT compression for background-free sunflower
  extras whose touched petals are all full.  Such extras are equivalent to a
  low-degree representative of the CRT residues
  `W = c_iL_D mod L_{T_i}` on the touched petals.
- **How it is useful:** Converts the remaining full-petal `t>=3` obstruction
  into explicit top-coefficient vanishing conditions on a CRT residue,
  recovering the two-petal pencil as the first case.
- **What to do next:** Bound how often core locators make these CRT top
  coefficients vanish, or prove that many such events force quotient or
  low-defect structure.

### 2026-06-24 - L1 background-free two-petal count

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A polynomial bound for the exact background-free
  two-petal sunflower subcase: at most `binom(M,2)q` non-planted listed
  codewords touch exactly two petals.
- **How it is useful:** Closes the two-petal profile as a possible
  super-polynomial sunflower obstruction in the generated-field window
  `q=poly(n)`, reducing the remaining background-free cases to three-or-more
  petals or different structured degeneracies.
- **What to do next:** Attack the three-or-more-petal incidence problem, using
  the core-defect reduction and petal-support tradeoff to organize the count by
  defect and number of touched petals.

### 2026-06-24 - L1 background-free two-petal pencil

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A classification of background-free two-petal
  sunflower extras.  Such an extra has core defect `ell=sigma+1`, fills two
  petals, and is equivalent to the missed-core locator lying in the affine
  pencil `(1+beta)L_{T_i}-beta L_{T_j}`.
- **How it is useful:** Converts the exact two-petal obstruction into a
  one-parameter locator-pencil problem, matching the two-full-petal profile
  seen in the `F_97,n=16,k=8,s=10` sunflower scan.
- **What to do next:** Count core subsets whose locators split inside these
  petal pencils, or show that many such split fibers imply quotient or other
  structured degeneracy.

### 2026-06-24 - L1 sunflower petal-support tradeoff

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A petal-support tradeoff for non-planted sunflower
  extras: if an extra misses `d` core points, has `r` background agreements,
  and touches `t` petals, then `(t-1)d >= sigma+1-r`.
- **How it is useful:** Rules out one-petal non-planted extras in maximal
  sunflowers and shows that few-petal extras must pay large core defect.  This
  organizes the remaining mixed-petal amplification problem by `(d,t)`.
- **What to do next:** Prove a large-defect incidence estimate for the
  shifted petal equations, using the tradeoff to split the many-petal and
  few-petal regimes.

### 2026-06-24 - L1 fixed-defect sunflower layer bound

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A fixed-defect counting lemma for sunflower
  received words.  For any fixed `d0`, listed codewords missing at most `d0`
  core points are bounded by
  `sum_{d<=d0} binom(k-1,d) binom(n-k+1,d+1)`.
- **How it is useful:** Shows that the mixed-petal obstruction is already
  polynomial on every fixed missed-core layer, so any super-polynomial
  sunflower counterexample must have core defect growing with `n`.
- **What to do next:** Attack the large-defect incidence problem for
  `W-c_iL_D` on the petals, or show that large-defect concentration forces
  quotient, low-defect, or another budgeted structured family.

### 2026-06-24 - L1 sunflower core-defect reduction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A proved sunflower core-defect reduction.  Every
  non-planted mixed-petal extra codeword factors through a degree-`d`
  polynomial, where `d` is the number of missed core points, and it can hit at
  most `d` points in any one petal.
- **How it is useful:** Converts the first mixed-petal obstruction from a scan
  pattern into a lower-dimensional interpolation problem.  Full-petal
  non-planted extras must miss at least `sigma+1` core points, sharpening the
  next amplification bound.
- **What to do next:** Count degree-`d` polynomials `W` with many roots across
  the shifted petal families `W-c_iL_D`, or show that large counts force
  quotient or low-defect structure.

### 2026-06-24 - L1 full-list quotient proof program

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_proof_program.md`,
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL.
- **What is being added:** A compact proof-program note stating Conjecture 1,
  the full-list quotient-budgeted L1 primitive-remainder target, and the
  intended proof chain through sparse syndromes, high-multiplicity
  certificates, quotient/low-defect removal, aperiodic extension counting, and
  packing closure.
- **How it is useful:** Gives the current L1 branch a single canonical theorem
  statement and proof roadmap, separate from the falsification evidence note,
  while keeping the first concrete lemma target focused on mixed-petal
  sunflower amplification.
- **What to do next:** Try to prove or refute the mixed-petal sunflower
  amplification lemma, then use the outcome to sharpen the general aperiodic
  extension-counting target.

### 2026-06-24 - L1 sunflower support decoder summaries

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_falsification.md`,
  `experimental/scripts/scan_l1_full_list_quotient_conjecture.py`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / COUNTEREXAMPLE-FIRST.
- **What is being added:** A seed-sweep mode for sunflower full-list rows,
  aggregate mixed-petal profile summaries across sunflower seeds, and an
  explicit proof target after the final first-pass falsification layer: bound
  mixed-petal amplification over sunflower floors.
- **How it is useful:** Gives a deterministic summary of the only obstruction
  pattern found so far.  The `F_97,n=16,k=8,s=10` four-seed sweep reached
  primitive remainder `8`, still below the alert threshold, so the note now
  identifies a concrete lemma to try proving next instead of continuing broad
  random falsification.
- **What to do next:** Attempt the mixed-petal amplification lemma, using
  support-profile equations from the sunflower construction; return to scans
  only if the proof attempt suggests a growing family.

### 2026-06-24 - L1 sunflower mixed-petal extras

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_falsification.md`,
  `experimental/scripts/scan_l1_full_list_quotient_conjecture.py`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / COUNTEREXAMPLE-FIRST.
- **What is being added:** The full-list sunflower scanner now has an exact
  support-subset decoder and classifies accidental non-planted codewords by
  agreement size, core intersection, total petal hits, number of petals
  touched, largest petal intersection, and number of full petals.  Seeded
  `F_97,n=16,k=8,s=10` sweeps show a repeated mixed-petal pattern; the
  strongest current row reaches primitive remainder `8` from a planted floor
  of `3`, still below the alert threshold.
- **How it is useful:** Converts the first sunflower amplification from an
  unexplained scan artifact into a concrete subproblem: bound accidental
  mixed-petal codewords over a planted sunflower floor.
- **What to do next:** Try to prove a mixed-petal amplification bound or use a
  faster decoder to search for growing mixed-petal families at larger `n`.

### 2026-06-24 - L1 glued-codeword sunflower attack

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_falsification.md`,
  `experimental/scripts/scan_l1_full_list_quotient_conjecture.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED CONSTRUCTION / EXPERIMENTAL / COUNTEREXAMPLE-FIRST.
- **What is being added:** A glued-codeword sunflower attack for the repaired
  full-list quotient conjecture.  A common `k-1` point core and disjoint
  petals of size `sigma+1` force
  `min(q-1, floor((n-k+1)/(sigma+1)))` listed codewords, and primitive
  agreement sets when the planted supports have trivial cyclic stabilizer.
  The scanner now includes deterministic and random sunflower received words
  and reports accidental extra list elements beyond the planted floor.
- **How it is useful:** Establishes a logarithmic primitive lower floor near
  the corrected reserve and gives a more adversarial falsification pattern
  than random or folded sampling.  The first `F_97,n=16,k=8,s=10` sunflower
  sweep found primitive remainder `5`, still below the alert threshold.
- **What to do next:** Classify the accidental sunflower extras and optimize
  the full-list decoder enough to test larger high-field near-boundary rows.

### 2026-06-24 - L1 full-list quotient falsification scanner

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_full_list_quotient_falsification.md`,
  `experimental/scripts/scan_l1_full_list_quotient_conjecture.py`,
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL / EXPERIMENTAL / COUNTEREXAMPLE-FIRST.
- **What is being added:** A repaired arbitrary-word/full-list falsification
  scanner for the quotient-budgeted L1 conjecture.  It scans the actual
  Reed--Solomon list/image fiber, decomposes listed codewords by the cyclic
  stabilizer of their maximal agreement sets, and separates exact quotient
  budget from primitive remainder.  It supports exact sparse-syndrome scans
  when the low-weight ball is small and sampled/random/folded received-word
  scans near the entropy boundary.
- **How it is useful:** Moves the conjecture-testing loop from the monomial
  prefix toy model to the repaired full arbitrary-word object while avoiding
  the already-refuted raw support fiber.
- **What to do next:** Add meet-in-the-middle sparse-syndrome scans for
  near-boundary radii and more adversarial glued-codeword received words; any
  large reserve-cleared primitive family should be recorded as a refinement or
  counterexample.

### 2026-06-24 - L1 quotient-budgeted conjecture scanner

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_quotient_budgeted_locator_conjecture.md`,
  `experimental/scripts/scan_l1_quotient_budgeted_conjecture.py`,
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL / EXPERIMENTAL / COUNTEREXAMPLE-FIRST.
- **What is being added:** A precise quotient-budgeted L1 locator conjecture:
  decompose each locator fiber by exact cyclic stabilizer via Mobius inversion,
  budget the nontrivial stabilizer mass, and target a polynomial bound for the
  stabilizer-primitive remainder.  The companion scanner enumerates
  split-prime monomial-prefix complement fibers and searches for
  reserve-cleared primitive remainders that would falsify or refine the
  conjecture.
- **How it is useful:** Converts the informal "quotient budget" into an exact
  ledger and gives the L1 program a concrete counterexample-first target that
  can be refined before attempting a proof.
- **What to do next:** Run larger dyadic and non-dyadic scans; if no
  reserve-cleared primitive family appears, try to prove the primitive
  remainder bound from bad-prime certificates plus density-over-primes.

### 2026-06-24 - L1 prefix bad-prime certificate

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_bad_prime_certificate.md`,
  `experimental/scripts/verify_l1_prefix_bad_prime_certificate.py`, and
  `experimental/agents-log.md`.
- **Status:** PROVED / FINITE-FIELD REDUCTION / NOT A FULL AGGREGATION BOUND.
- **What is being added:** A templatewise bad-prime theorem for monomial-prefix
  collisions: a finite-field prefix collision either lifts to a
  characteristic-zero prefix collision or the field characteristic divides an
  explicit cyclotomic resultant certificate. The split-prime case is then
  refined for row accounting. The note also records the associated norm bound,
  finite-family lcm aggregation handle, and the prime-ideal refinement via the
  modular gcd `gcd(Phi_n, Delta_1, ..., Delta_sigma)` needed to filter
  rational-certificate false positives.  It further adds the exact
  common-ideal/Fitting index `I_n,sigma(A,B)`, whose prime divisors away from
  `n` are exactly the rational primes with a simultaneous common-root factor;
  this removes the recorded `p=97` rational false positive.  The note then
  records the finite-family exact aggregation theorem: after
  characteristic-zero templates are removed, the lcm of the indices
  `I_n,sigma(A,B)` has exactly the bad rational-prime support for simultaneous
  primitive-root collisions away from primes dividing `n`.  It also proves the
  valuation incidence budget `deg G_p(A,B) <= v_p(I_n,sigma(A,B))`, converting
  degree-weighted common-prime-ideal incidence into an integer valuation budget.
  A radical Smith incidence index `J_n,sigma` sharpens this to an exact
  identity `v_p(J_n,sigma(A,B)) = deg G_p(A,B)` away from primes dividing `n`.
  Its finite-family product gives the exact degree-weighted incidence product
  away from primes dividing `n`, and `J_n,sigma` is invariant on affine orbits.
  Summing over rational primes gives a log-weighted density bound:
  `prod p^{d_T(p)}` divides the product of common-ideal indices over the
  finite template family.  For dilation-stable finite-field template families,
  the same budget gives the direct row bound
  `|Coll_T(h)| <= phi(n)^{-1} sum_T v_p(I_n,sigma(A,B))`, and hence an
  explicit max-fiber bound after structured row pairs are separately budgeted.
  The affine-orbit reduction is also extended from resultant/common-root
  degree invariance to common-ideal index and valuation invariance.
  At the full-prefix endpoint `sigma=m`, the common-ideal index has no prime
  support away from primes dividing `n`.
  The Newton bridge is strengthened from modular common-root factors to
  localized common-ideal indices: away from primes dividing `n sigma!`,
  elementary and power-sum/Fourier coordinates have the same valuation budgets.
  The same localized Newton change of generators also preserves radical
  incidence valuations, so the exact row-incidence ledger `J_n,sigma` can be
  read in Fourier power-sum coordinates away from the Newton denominators.
  The modular gcd degree is also
  recorded as the exact primitive-root embedding multiplicity at split and
  nonsplit primes, with the Frobenius-orbit quotient giving the rational
  prime-ideal count.
  The note additionally records affine-orbit invariance, the split-prime
  row-accounting identity equating row collision counts with degree-weighted
  common-prime-ideal incidence, its nonsplit extension-field analogue and
  affine-orbit quotient ledger, the Newton bridge from elementary prefixes to
  power-sum/Fourier prefixes, the prefix-depth filtration for certificates and
  common-root factors, the exact radical frontier-drop ledger for prefix-depth
  increments, the modular frontier factors
  `H_{p,sigma}=G_{p,sigma}/G_{p,sigma+1}` realizing those drops, the
  telescoping decomposition of radical incidence to the full-prefix rigid
  endpoint, its row-level and affine-orbit frontier-layer decompositions for
  dilation-stable families, the quotient-periodic frontier pullback reducing
  periodic lifted frontier mass to lower-order quotient domains, the primitive
  frontier remainder after exact common-support stabilizers are removed, its
  stabilizer Mobius ledger for overlap-safe primitive frontier extraction, and
  a bounded exact split-prime scan for the `n=16,m=6,sigma=4` row.
- **How it is useful:** This supplies the finite-field layer complementary to
  characteristic-zero L1 reductions. It turns robustly aperiodic modular
  collisions into algebraic norm/resultant divisibility events, matching a
  first attack in `agents.md`.
- **What to do next:** Prove a uniform aggregation or density-over-primes bound
  for the valuation budgets of these exact common-ideal indices after
  quotient-periodic and characteristic-zero templates are
  removed, using the prefix-depth filtration to shrink the candidate bad-prime
  support as `sigma` grows toward the full-prefix rigid endpoint and the
  quotient-periodic pullback to remove recursively induced periodic frontier
  layers before attacking the exact-stabilizer-one primitive frontier orbit
  representatives; use the stabilizer Mobius ledger when periodic strata
  overlap.

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
