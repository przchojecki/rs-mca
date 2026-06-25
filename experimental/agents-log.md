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

### 2026-06-24 - L2 sharp target exactification

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/l2/l2_sharp_target_conjecture.md`,
  `experimental/scripts/verify_l2_sharp_target.py`, and
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL / EXPERIMENTAL / FALSIFICATION.
- **What is being added:** A standalone version-0 L2 sharp interleaved-list
  target with explicit fixed-arity setup, generated-field reserve, an
  all-remainder aligned quotient budget `Quot_rem_mu`, and a polynomial
  over-agreement/codegree error. The quotient budget now includes
  dimension-dithered scales `M|n` with `M` not necessarily dividing `k`, using
  `ell=floor(a/M)` full cosets plus a partial omitted coset of size
  `a mod M`; the old divisible-only budget is just a sub-sum. The target now
  names the `mu=2` codegree error exactly as a sum of
  punctured Reed-Solomon list sizes over row-1 full supports and proves an
  elementary punctured Johnson/codegree bound:
  `L_A <= floor(s(s-k+1)/(a^2-s(k-1)))` when `a^2>s(k-1)`, with unique
  decoding when `2a>s+k-1`. It also isolates the exact large-anchor threshold:
  for `a=k+sigma`, Johnson controls all anchors through
  `s=ceil(a^2/(k-1))-1`, so the remaining tail starts only after
  `ceil(a(sigma+1)/(k-1))` extra agreements above `a`. A deterministic two-row
  shell bound now separates Johnson-controlled shells from this tail and bounds
  the tail anchor count by the exact-`a` one-row locator multiplicity divided by
  `binom(s_J,a)`. A new L1-to-L2 shell corollary proves that a uniform one-row
  list bound at the original threshold `a` implies a two-row codegree bound
  `n^{B_L+2}(2+log n)+n^{2B_L}`; the controlled Johnson shell weight is
  `O(n^2 log n)`. The same argument is extended to fixed protocol arity `mu`:
  the powered shell weight `sum_s J(s;k,a)^(mu-1)` is
  `O_mu(n^{2(mu-1)} log n)`, so the repaired one-row L1 bound at `a` implies a
  polynomial fixed-arity L2 codegree bound. This is now stated as a conditional
  theorem: after quotient packets are removed or charged to `Quot_rem_mu`,
  the L1 local limit supplies the `n^B` error term in L2-Sharp. The
  verifier stress-tests the exact quotient budget, natural
  `K_{m,m}` grid over-agreement attacks, and a realized `F_29` Reed-Solomon
  `K_{2,2}` gluing witness with punctured codegrees `[2,2]` satisfying the
  Johnson bound `5`, exact shell bound `10`, and L1-shell reduction bound
  `372`; for `(n,k,a)=(64,16,18)`, the `mu=3` powered shell weight is `199`.
  At the dithered example `(n,k,a)=(64,15,17)`, the divisible-only quotient
  budget is `0` but the all-remainder budget is `1389`. The verifier also
  realizes an actual dithered packet over `F_17`, `n=16`, `k=7`, `a=9`, `M=4`
  with `M` not dividing `k`: it constructs the three expected codewords, with
  maximum degree `5<k` and agreement at least `9`. The active all-remainder
  scales are now characterized exactly by interval-divisor clearance:
  `M|n` and `a-k<M<=a`; for the dithered `(64,15,17)` example these are
  `{4,8,16}`. For dyadic `n`, this becomes a next-power threshold:
  all all-remainder packets are absent exactly when `a` falls below the first
  power of two larger than `sigma`; in the verifier scan
  `(n,k_0,sigma)=(64,16,2)`, this first happens only after the large dither
  `r=15`. The latest refinement splits the L2 count into a regular exact-row
  core and a row-irregular shell. Regular tuples have all row supports equal to
  the same `a`-set and are the only place where the sharp random term plus
  `Quot_rem_mu` must be proved. Row-irregular tuples have at least one row
  support of size `>a`, so the fixed-arity Johnson/L1 shell reduction bounds
  them by a polynomial. The `F_29` `K_{2,2}` witness now verifies this split:
  regular count `0`, row-irregular count `4`, common-intersection profile
  `{5:4}`. The regular core is now identified exactly as a simultaneous
  support-fiber subproblem: an `a`-set feasible for all rows determines a unique
  interleaved tuple, and it contributes to `Reg_mu` precisely when every induced
  full row support is that same `a`-set. This subproblem is now written in
  locator-syndrome form: interpolate each row on `S` to degree `<a`, then set
  the `sigma=a-k` top coefficients in degrees `k,...,a-1` to zero. The verifier
  records that the `K_{2,2}` witness has `4` simultaneous feasible
  zero-syndrome `a`-sets, all row-irregular, with unique row choices and no
  mismatch against the enumerated support families. The top-coefficient
  syndromes are further identified with a unit-triangular transform of the
  weighted residue moments
  `sum_{s in S} U_i(s)s^j/L_S'(s)` for `0<=j<sigma`; the same verifier checks
  zero formula mismatches and zero zero-locus mismatches. The all-remainder
  quotient packets are also now identified inside this zero-moment locus: for
  the dithered `F_17` packet, the verifier checks that every advertised support
  interpolates to the constructed degree-`<k` codeword and has zero top
  syndrome and zero residue moments. Exhausting all `binom(16,9)` supports for
  that same word gives `42` exact zero-moment supports and `42` distinct
  degree-`<k` codewords, all with exact agreement size `9`. The `3` advertised
  quotient codewords are disjoint from `39` residual aperiodic codewords, whose
  quotient-coset occupancy profiles include `(3,2,2,2)` and `(3,3,2,1)`. This
  residual is non-quotient by the active-scale shape test: the active shapes at
  `M=4` and `M=8` account for the same `3` advertised quotient supports in
  union, leaving all `39` residual codewords outside active quotient shapes.
  Equal-row interleaving of the exact-support family remains diagonal: `42`
  one-row zero-moment supports give `42` listed pairs, with `3` quotient pairs,
  `39` residual pairs, and no mixed quotient/residual listed pairs.
  Nontrivial dilation correlations also vanish in this finite family: among
  the `16` domain rotations, only the identity maps zero-moment supports back
  into the family, and the maximum non-identity residual overlap is `0`.
  This records that `Quot_rem_mu` is a structured budgeted subfamily, not an
  exhaustive finite classification of the zero-moment locus.
  The V0 note now also proves the two leading terms exactly: the random
  simultaneous-fiber mean is `binom(n,a)q^{-mu(a-k)}`, the exact-regular random
  mean has the additional `(1-1/q)^{mu(n-a)}` factor, and each all-remainder
  quotient packet has exact support with interleaved count `L_{M,mu}(a,tau)`;
  the verifier checks exact advertised support in the dithered `F_17` packet.
  The random regular-core pair correlations are also now exact: two `a`-sets
  with intersection `r` are independent for `r<k`, while for `r>=k` the only
  surplus is `q^{mu(r-k)}`; the verifier brute-checks the support-pair rank law
  over `F_7`, `n=6`, `k=2`, `a=3`.
  A multi-support cluster-rank lemma now bounds any collection of candidate
  regular supports by `q^{mu(k c-|V|)}`, where `c` is the number of connected
  components in the graph of pairwise intersections of size at least `k`; the
  diagonal zero-loss case is isolated as the only connected cluster with
  `|V|=a`, while every non-diagonal connected cluster pays at least one extra
  `q^{-mu}` factor. The verifier checks tight and loose three-support examples
  over the same field.
  This has been sharpened to a union-excess tradeoff: a connected cluster with
  union size `a+d` costs `q^{-mu d}` beyond one support and contains at most
  `binom(a+d,a)` distinct supports; the verifier adds a four-support chain
  example realizing the predicted exponent.
  A connected-cluster moment corollary now bounds the union-excess `d` part of
  random `t`-th moments by
  `binom(n,a+d) binom(a+d,a)^t q^{-mu(a-k+d)}`; the verifier counts connected
  ordered triples by `d` in the finite `F_7` model.
  A finite-moment clearance corollary shows that if
  `q^mu >= 2 rho_0^{-1} n^t`, the positive-excess connected contribution is at
  most one diagonal scale; the verifier checks this exactly for `q=31, mu=2`.
  The cluster rank bound now also has a `k`-closure refinement: raw high-overlap
  components whose unions overlap in at least `k` points must merge to one
  degree-`<k` polynomial; the verifier includes an aggregate-overlap example
  where this strictly sharpens the exponent.
  The same closure ledger is now stated for arbitrary tuples: with `c`
  `k`-closed parts and global excess `D=|V|-ac`, the random-row probability is
  at most `q^{-(c(a-k)+D)}`; the verifier enumerates all triples by closure
  signature and records negative/zero/positive `D` cases.
  A rank-corrected closure ledger now adds the exact cross-component equality
  rank `r_cross`; forest overlap graphs, including all two-component cases,
  satisfy `D+r_cross=sum_alpha(|V_alpha|-a)`, so only cyclic low-overlap
  closed-part intersections remain as a separate rank-analysis issue.
  That boundary is now shown to be real: the note gives a three-cycle
  low-overlap counterexample to naive closed-part factorization, and the
  verifier checks an `F_17` sweep where the cyclic rank deficit is `k-3`.
  The generic triangle family is then counted exactly and shown to be
  random-model harmless under `q^mu>27/rho_0`, shifting the remaining cyclic
  issue to lower-rank structured cycles such as constant locator-ratio cases.
  The constant locator-ratio subfamily is now also counted by fixing `A,B` and
  the ratio, which forces `C` through a degree-`r` locator equation; the
  verifier enumerates the `F_17` cases and checks the resulting bound.
  Combining the generic and constant-ratio cases gives a full clearance
  corollary for symmetric three-block cyclic triangles, with exact and bounded
  diagonal-relative ratios checked in the verifier. The same low-overlap
  mechanism is now extended to fixed-length cyclic necklaces: if the
  edge-block locator polynomials have full rank, then the cycle forces all
  closed-part polynomials to collapse to one degree-`<k` polynomial, giving an
  exponent gap `(m-2)r` over the diagonal and a diagonal-relative bound
  `(m^m rho_0^{-(m-2)} q^{-mu(m-2)})^r` for fixed cycle length `m`. The
  verifier checks representative full-rank `F_31` necklaces, including the
  cross-rank formula and the below-diagonal finite ratios. The complementary
  rank-deficient necklaces are now counted by choosing a pivot in a nontrivial
  locator dependency, the other `m-1` edge blocks, and `q^{m-2}` normalized
  dependency coefficients. Since the locator rank is always at least `2`, this
  gives exponent gap at least `(m-2)(r-1)` and a diagonal-relative bound
  `m q^{(mu+1)(m-2)} ((m-1)^{m-1} rho_0^{-(m-3)}
  q^{-mu(m-2)})^r`. Together with the full-rank case this clears the
  fixed-length edge-block necklace family in the polynomial-field, linear-`r`
  regime; the verifier checks the dependency-count bound over `F_31`. The
  cyclic analysis is now generalized to clean simple cycles with arbitrary
  adjacent edge sizes `e_i<k`: if
  `W_i={Q in F_q[X]_<k : Q|_{E_i}=0}` and
  `R_cyc=dim(W_0+...+W_{m-1})`, then the cross-rank is exactly
  `sum_i e_i+R_cyc-k` and the exponent gap over diagonal is
  `(m-1)(a-k)+R_cyc-k`. The verifier checks uneven and private-mass cycle
  examples over `F_31`. The clean-cycle defect is now identified dually:
  `k-R_cyc=dim(U_0 cap ... cap U_{m-1})`, where `U_i` is the span of
  evaluation functionals on edge overlap `E_i`; equivalently, rank deficiency
  requires a nonzero linear functional on degree-`<k` polynomials supported on
  every edge overlap. A two-edge lower bound now shows
  `R_cyc >= k-max(0,s_2-k)`, where `s_2` is the minimum pair sum of edge
  sizes; in particular, if two edge overlaps have total size at most `k`, then
  `R_cyc=k`. Thus rank-deficient clean cycles can only occur in the
  near-necklace regime where the two smallest edge overlaps already sum to
  more than `k`.
- **How it is useful:** Turns the L2 objective from a broad "avoid Cartesian
  overcharge" principle into a concrete conjectural inequality that can be
  falsified or promoted. The `K_{2,2}` witness records that local Cartesian
  blocks are real, so the correct target is a global sharp bound with those
  blocks charged to the polynomial codegree term.
- **What to do next:** Prove the simultaneous exact-support fiber local limit
  for the regular core,
  `Reg_mu <= binom(n,a)q^{-mu(a-k)} + Quot_rem_mu + n^B`, prove/import the
  repaired one-row L1 list bound at `a=k+sigma`, and reconcile the final
  statement with the active X1/L2 bridge PR #101 before promotion.
  For the regular-core cluster route, bound or count the near-necklace
  dependency loci where the two smallest clean-cycle edge overlaps have total
  larger than `k`, then extend the reduction to cyclic diagrams with chords,
  shared edge intersections, or larger closure parts.

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
