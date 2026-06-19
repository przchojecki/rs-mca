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

### 2026-06-19 - M1 line-conic kernel Mellin magnitudes

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Classifies the exact magnitudes of the descended
  kernel Mellin spectrum: `|M(epsilon)|=p`, `|M(chi_2)|=1`,
  `|M(theta)|=sqrt(p)` when `theta^2=nu`, and `p` otherwise.
- **How it is useful:** Shows the kernel spectrum is generically full
  `p`-size, so the nonsplit p-scale theorem cannot be won by proving most
  kernel coefficients small; the saving must come from correlation with the
  outer spectrum.
- **What to do next:** Use the magnitude ledger to isolate any remaining
  diagonal/special-theta terms before attacking generic theta cancellation.

### 2026-06-19 - M1 line-conic outer Mellin bound

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the outer Mellin coefficient bound
  `|A_{eta,nu}(theta)| <= 4sqrt(p)` by decomposing `A` into two
  three-point genus-zero Kummer sums, each bounded by `2sqrt(p)`.
- **How it is useful:** Supplies the proof-level termwise input behind the
  nonsplit spectral normal form's `O(p^{3/2})` fallback and confirms that
  the remaining p-scale target must use correlation cancellation.
- **What to do next:** Use the spectral normal form to study the theta-phase
  correlation between the Jacobi-product kernel spectrum and the outer
  Kummer spectrum.

### 2026-06-19 - M1 line-conic spectral energy ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Computes exact Parseval energies for the nonsplit
  spectral normal form:
  `sum|A|^2=2(p-1)(p-2+chi_2(-2))` and
  `sum|M|^2=(p-1)(p^2-2p-1-p nu(-1))`.
- **How it is useful:** Quantifies the best separate-spectrum Cauchy fallback
  as `O(p^{3/2})`, proving that the desired p-scale nonsplit result requires
  cancellation in the correlation across the Mellin parameter.
- **What to do next:** Analyze that spectral correlation directly rather than
  only bounding the two spectra separately.

### 2026-06-19 - M1 line-conic nonsplit spectral normal form

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Writes the nonsplit quotient-line projector as an
  exact Mellin convolution
  `eta(-2)G(2)+chi_2(-3)/(p-1)sum_theta A(theta^{-1})M(theta)`, with
  `M` the Jacobi-product kernel spectrum and `A` a sum of two three-point
  Kummer coefficients.
- **How it is useful:** Localizes the remaining nonsplit M1 obstruction to
  cancellation across the Mellin parameter instead of an opaque one-variable
  trace, and records the termwise `p^{3/2}` fallback as insufficient for the
  desired p-scale theorem.
- **What to do next:** Prove cancellation in this spectral sum, or identify
  a structural diagonal/off-diagonal split that yields the p-scale bound.

### 2026-06-19 - M1 line-conic quotient-line Mellin spectrum

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Computes the full multiplicative Mellin spectrum
  of the descended quotient-line kernel `J` as
  `chi_2(-4delta)nu(-1)(1_{theta=1}(p-1)
  + theta(4delta)Jac(theta,chi_2)Jac(theta^{-2},nu))`.
- **How it is useful:** Identifies `J` as an explicit hypergeometric Mellin
  object and proves every multiplicative coefficient is bounded by `p`,
  giving a sharper structural handle for the outer nonsplit Kummer transform.
- **What to do next:** Use this Mellin spectrum to analyze the remaining
  rational `eta,nu` twist in the nonsplit projector.

### 2026-06-19 - M1 line-conic quotient-line kernel moment

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the exact descended-kernel identities
  `J(0)=0` and
  `sum_s |J_{nu,delta}(s)|^2 = p^2 - 2p - 1 - p nu(-1)` for every
  nonprincipal `nu`.
- **How it is useful:** Gives the quotient-line nonsplit conductor target its
  own p-scale RMS certificate, showing the descended `s`-line kernel has no
  hidden large average before the outer `eta,nu` twist is applied.
- **What to do next:** Use this quotient-line moment with the five-point
  support ledger to attack the pointwise nonsplit projector transform.

### 2026-06-19 - M1 line-conic quotient-line descent

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Descends the nonsplit twisted `t`-line through
  `s=t^2`: `K(t)=nu(t)J(s)` for
  `J(s)=sum_r nu(r-1)chi_2(sr^2-4delta)`, giving an exact quotient-line
  formula for `C^-` with projector factor `1+chi_2(s)`.
- **How it is useful:** Removes the auxiliary two-cover from the nonsplit
  conductor target and leaves a single `s`-line trace with five projective
  support points `{0, delta, -delta/2, 4delta, infinity}`.
- **What to do next:** Prove the p-scale conductor bound for this descended
  quotient-line trace.

### 2026-06-19 - M1 line-conic projector moments

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Computes exact full-character second moments for
  the split and nonsplit projectors and their cross moment:
  `S_- = 2p^2-4p+1+2(p-1)chi_2(-2)`,
  `S_+ = 2p^2-15p+31-2(p-3)chi_2(-2)`, and `S_{-,+}=2p-3`, each times
  `(p-1)^2`.
- **How it is useful:** Shows the split/nonsplit projectors are p-scale on
  average and nearly orthogonal, so the nonsplit pointwise obstruction is not
  caused by hidden large average mass.
- **What to do next:** Use the projector moment and nonsplit kernel moment
  to guide a pointwise conductor proof for the outer Mellin transform.

### 2026-06-19 - M1 line-conic twisted kernel moment

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the exact first and second moments of the
  nonsplit translated kernel:
  `sum_t K(t)=0` and `sum_t |K(t)|^2=p^2-1` for every nonprincipal `nu`.
- **How it is useful:** Shows the nonsplit kernel has RMS
  `sqrt(p-1/p)`, so the remaining obstruction is the outer Mellin transform
  rather than hidden large average mass inside the rank-two kernel.
- **What to do next:** Use the exact moment with the deck-invariant
  descended trace to attack the p-scale nonsplit projector bound.

### 2026-06-19 - M1 line-conic twisted deck symmetry

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the nonsplit kernel symmetry
  `K(-t)=nu(-1)K(t)`, hence invariance of the full twisted-line finite
  summand under the deck involution `t -> -t`; also records the standard
  rank-two pointwise bound `|K(t)| <= 2sqrt(p)`.
- **How it is useful:** Shows the two nonsplit preimages over a `y` value
  are paired exactly, so the twisted-line model can descend through `t^2`
  without a deck-asymmetry loss.
- **What to do next:** Use the deck-invariant descended trace and the
  nonsplit divisor table to prove the p-scale outer conductor bound.

### 2026-06-19 - M1 line-conic twisted outer divisor

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Records the Kummer outer-twist divisor on the
  nonsplit `t`-line: local characters `nu` at `t=0` and infinity,
  `(eta nu)^(-1)` at `t^2=delta`, and `eta` at `t^2=-delta/2`, with the
  `K(t)` collision pair `t^2=4delta` separated.
- **How it is useful:** Gives the nonsplit projector a conductor checklist
  matching the split-side lambda ledger and shows no outer-twist support point
  disappears on the admissible `C_2^lc` character range.
- **What to do next:** Combine this divisor table with the translated
  hypergeometric local table to prove the nonsplit p-scale conductor bound.

### 2026-06-19 - M1 line-conic twisted fiber trace

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Pushes the nonsplit twisted-line model through
  the quadratic fiber: with `D=t^2-delta`,
  `G(y_delta(t))=chi_2(-3)nu(t/D)K(t)` where
  `K(t)=sum_x nu(x-t)chi_2(x^2-4delta)`.
- **How it is useful:** Replaces the nonsplit companion projector by a
  translated rank-two hypergeometric trace with explicit collision locus
  `t^2=4delta`, plus the already listed outer Kummer twist points.
- **What to do next:** Use this local table to prove a p-scale bound for
  the nonsplit projector or combine it with the split lambda-line in one
  quadratic-pushforward conductor argument.

### 2026-06-19 - M1 line-conic twisted nonsplit line

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Gives an exact quadratic-twist parameterization
  of the nonsplit projector: for a nonsquare `delta`,
  `y_delta(t)=(2t^2+delta)/(t^2-delta)` hits exactly the nonsplit
  discriminant fibers two-to-one, and
  `C^-=eta(-2)G(2)+sum_t eta(-y_delta(t))G(y_delta(t))`.
- **How it is useful:** Converts the missing companion projector from an
  unnamed quadratic-twist obstruction into a rational-line conductor target,
  with geometric support at `t=0`, `infinity`, `t^2=-delta/2`,
  `t^2=4delta`, and `t^2=delta`.
- **What to do next:** Prove the p-scale conductor bound on this twisted
  line, or combine it with the split lambda-line analysis in a direct
  quadratic-pushforward estimate.

### 2026-06-19 - M1 line-conic split/nonsplit projectors

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Refines the pullback descent into exact
  split/nonsplit projectors: `C^+=C+C^quad-eta(-3)G(3)` is the finite
  lambda-pullback trace, `C^-=C-C^quad` is the nonsplit projector, and
  `C` is reconstructed from `C^+`, `C^-`, and the single Jacobi term.  The
  verifier also records that the nonsplit projector can exceed `4p` in the
  audited grid, so the viable separate-projector route must balance the two
  constants rather than prove identical `4p` bounds.
- **How it is useful:** Turns the companion quadratic twist obstruction into
  a precise descent problem: the finite singular budgets are harmless, and a
  proof must either control the nonsplit projector or descend the quadratic
  pushforward without a square-root loss.
- **What to do next:** Prove a p-scale conductor bound for the nonsplit
  projector, or replace the split/nonsplit separation by a direct
  middle-extension pushforward bound.

### 2026-06-19 - M1 line-conic pullback descent

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the finite-field descent identity
  `P_{eta,nu}=C_{eta,nu}+C^quad_{eta,nu}-eta(-3)G_nu(3)` for the
  `lambda`-pullback trace.
- **How it is useful:** Clarifies exactly what the hypergeometric pullback
  controls: the split-projected combination of the core and its quadratic
  discriminant twist, up to the already evaluated `y=3` Jacobi term.
- **What to do next:** Control the companion quadratic twist or descend the
  quadratic pushforward sheaf without square-root loss.

### 2026-06-19 - M1 line-conic twist nontriviality

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves that all Kummer twist characters in the
  pulled-back `lambda`-line divisor are nonprincipal on the admissible
  `C_2^lc` character range.
- **How it is useful:** Shows that none of the eight-point conductor
  checklist disappears by a character-specialization shortcut; any saving
  must come from the hypergeometric local table or pushforward structure.
- **What to do next:** Combine the nontrivial twist ledger with the
  hypergeometric local table to estimate the final conductor.

### 2026-06-19 - M1 line-conic twist divisor

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Records the Kummer twist divisor multiplying the
  pulled-back three-point trace on the `lambda`-line, including local
  characters `nu`, `(eta nu)^(-1)`, and `eta` at the support points.
- **How it is useful:** Turns the eight-point checklist into a local
  monodromy ledger for the future conductor proof of the line-conic
  `4p` target.
- **What to do next:** Combine this twist table with the standard local
  table of `H_nu(lambda)` to bound the quadratic pushforward conductor.

### 2026-06-19 - M1 line-conic lambda conductor ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Computes the rational map from the discriminant
  double cover to the hypergeometric `lambda`-line and records its special
  points: `0`, `infinity`, `1`, `-1`, `-3`, `-1/3`, and the roots of
  `9lambda^2+14lambda+9`.
- **How it is useful:** Converts the remaining line-conic conductor target
  into an explicit eight-point `lambda`-line checklist after the
  hypergeometric pullback.
- **What to do next:** Turn this checklist into a theorem-grade conductor
  ledger for the quadratic pushforward with Mellin twist.

### 2026-06-19 - M1 line-conic hypergeometric pullback

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves that after the double cover
  `z^2=(y-2)(y+1)`, every split nonsingular fiber satisfies
  `G_nu(y)=chi_2(-3)nu(r_+)H_nu(r_-/r_+)` for the three-point trace
  `H_nu(lambda)=sum_x nu(x)chi_2((x-1)(x-lambda))`.
- **How it is useful:** Replaces the lisse part of the line-conic wall by an
  explicit quadratic pushforward of a standard hypergeometric/Jacobi trace,
  which is the object a theorem-grade conductor proof should bound.
- **What to do next:** Prove the conductor bound for this quadratic
  pushforward with the outer Mellin twist and the filtered character range.

### 2026-06-19 - M1 line-conic character filter

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Records the exact transformed character filter
  for actual asymmetric line-conic-resonant terms:
  `a,b != 0`, `b != a`, `b != -a`, `b != 2a`, and `2b != a`.
- **How it is useful:** Identifies the precise `(eta,nu)` range that a
  theorem-grade `4p` conductor bound must cover and rederives the
  `C_2^lc=9R(e)` count from the character relations.
- **What to do next:** Prove the pointwise conductor estimate on this
  filtered nonprincipal range.

### 2026-06-19 - M1 line-conic principal rows

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Gives exact formulas for the excluded principal
  `eta=1`, `nu=1`, and `(eta,nu)=(1,1)` rows of the line-conic core.
- **How it is useful:** Explains the full-character/nonprincipal RMS gap:
  the `nu=1` row contains the two `p`-scale degenerate conic terms, while the
  actual `C_2^lc` target excludes this leakage.
- **What to do next:** Continue toward the pointwise nonprincipal conductor
  bound for the lisse open trace.

### 2026-06-19 - M1 line-conic singular fibers

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Evaluates the finite singular fibers of the
  transformed line-conic trace family: `G_nu(-1)=0`, `G_nu(2)` has size
  one, and `G_nu(3)` is a single Jacobi sum.
- **How it is useful:** Shows that no finite singular value carries a
  `p`-sized exceptional contribution; the `4p` target is genuinely a lisse
  open-trace conductor problem on the punctured `y`-line.
- **What to do next:** Prove the middle-extension conductor bound on
  `P^1_y \ {0,-1,2,3,infinity}`.

### 2026-06-19 - M1 line-conic nonprincipal moment

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves and verifies the exact second moment of
  the line-conic-resonant core after excluding principal `eta` and `nu`,
  using the fixed-`v` and fixed-`x=A/u` marginal conic counts.
- **How it is useful:** Removes principal-character leakage from the previous
  full-character average: the actual nonprincipal target has RMS `p+O(1)`,
  not `sqrt(2)p+O(1)`.
- **What to do next:** Use the marginal conic geometry as a guide for the
  pointwise middle-extension conductor proof of the `4p` core target.

### 2026-06-19 - M1 line-conic resonant wall scan

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/search_m1_remaining_two_coordinate_wall.py`,
  `experimental/m1_remaining_two_coordinate_wall_experiment.md`,
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Adds a dedicated
  `asymmetric_line_conic_resonant_wall` scan mode for the exact `C_2^lc`
  slice and records the report-grid maximum `2.7649691518p`.
- **How it is useful:** This is a counterexample-first stress test for the
  new line-conic transformed-core target; the resonant slice is well below
  the `4p` target in the current grid and below the nonresonant asymmetric
  maximum.
- **What to do next:** Use the largest resonant rows to guide the
  one-dimensional conductor proof or extend the resonant grid.

### 2026-06-19 - M1 line-conic second moment

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves and verifies an exact full-character
  second moment for the line-conic-resonant core:
  `(p-1)^2(2p^2-8p+13-chi_2(-3)p+9chi_2(-3)+chi_2(-2))`.
- **How it is useful:** This gives structural evidence for the transformed
  `C_2^lc` conductor target: the full-family RMS core size is below
  `sqrt(2)p`, so a `4p` counterexample would be exceptional rather than
  average-driven.
- **What to do next:** Use the collision geometry behind the moment formula
  to pursue the rank-two middle-extension conductor bound.

### 2026-06-18 - M1 line-conic resonant conditional ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** Reports the optional raw M1 ledger obtained if the
  transformed line-conic-resonant core satisfies `|C|<=4p`; the open-sum
  replacement is then `4p+3sqrt(p)` on `C_2^lc`.
- **How it is useful:** This identifies the exact remaining conductor import
  that would let the conditional two-coordinate ledger charge all of
  `C_2^peq+C_2^asym` at `4p+3sqrt(p)` instead of leaving `C_2^lc` at `9p`.
- **What to do next:** Prove the rank-two one-dimensional conductor bound
  for the transformed line-conic family, or find a `4p` counterexample.

### 2026-06-18 - M1 line-conic resonance reduction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_line_conic_resonance_reduction.md`,
  `experimental/verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Proves the exact transform for the
  line-conic-resonant core `mu eta=1`, reducing it to a Mellin transform of
  a one-dimensional quadratic-fiber trace family with candidate singular
  support `{0,-1,2,3,infinity}`.
- **How it is useful:** This removes the `C_2^lc` slice from the category of
  opaque two-variable imports and gives a concrete one-dimensional conductor
  target for the last residual two-coordinate mass in the combined M1 ledger.
- **What to do next:** Prove the conductor bound for the resulting
  quadratic-fiber trace family or search this resonant family for a sharp
  obstruction.

### 2026-06-18 - M1 nonresonant wall conditional ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Reports the combined conditional certificate
  ledger obtained by charging the projective equal-pair slice and the clean
  asymmetric nonresonant slice at `4p+3 sqrt(p)`, while leaving the
  line-conic-resonant asymmetric slice at the conservative `9p` import.
- **How it is useful:** This quantifies the exact certificate payoff of the
  next nonresonant line/conic conductor theorem without promoting it to an
  active proof ingredient.
- **What to do next:** Prove the `C_2^anr` nonresonant conductor bound or
  find a counterexample in the reported nonresonant wall.

### 2026-06-18 - M1 asymmetric line-conic resonance split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/search_m1_remaining_two_coordinate_wall.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_remaining_two_coordinate_wall_experiment.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Splits the asymmetric M1 two-coordinate wall into
  the exact line-conic-resonant mass `C_2^lc` and the nonresonant complement
  `C_2^anr`, with closed-form counts and direct verifier checks.
- **How it is useful:** The clean normal-crossing conductor target now has
  explicit dense-edge nonresonance hypotheses, while the residual
  line-conic-resonant slice is named and counted separately.
- **What to do next:** Attack the `C_2^anr` conductor bound directly, and
  separately look for a reduction of the smaller line-conic-resonant slice.

### 2026-06-18 - M1 asymmetric wall closed ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Replaces the hidden coordinate-diagonal and
  equal-line loops in the projective equal-pair ledger by closed forms, and
  records the resulting exact formula for `C_2^asym` and its free
  line-permutation orbit count.
- **How it is useful:** The remaining M1 two-coordinate wall is now an
  explicit residual after the proved `C_2^0` and `C_2^rec` reductions and the
  conditional `C_2^peq` ledger, so the next conductor target is isolated
  without relying on scanner enumeration.
- **What to do next:** Prove or refute a conductor bound for the genuinely
  asymmetric projective line orbit class.

### 2026-06-18 - M1 asymmetric wall scan split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/search_m1_remaining_two_coordinate_wall.py`,
  `experimental/m1_remaining_two_coordinate_wall_experiment.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Extends the remaining two-coordinate wall scanner
  with an `asymmetric_wall` pass that removes projective equal-pair tuples
  already isolated by the conditional `C_2^peq` ledger.
- **How it is useful:** The report grid now separates the old
  ramified-nonreciprocal wall from the actual post-reduction `C_2^asym` wall.
  In the current report range, every near-`4p` top row lies in the equal-line
  slice, while the largest asymmetric-only ratio is `3.2173609608p`.
- **What to do next:** Extend the asymmetric-only scan range or prove a
  conductor bound for the asymmetric wall that does not need to account for
  the near-`4p` equal-line phenomenon.

### 2026-06-18 - M1 additive frontier criterion

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_residual_depth_frontier_shift.md`,
  `experimental/m1_low_slack_packet_template_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROVED.
- **What is being added:** Adds the additive error criterion following from
  the weighted frontier-shift identity: any subadditive certificate functional
  satisfies `E(C_T(r)) <= sum_{a=T}^{r-1} E(F_a(r)) + E(C_r(r))`.
- **How it is useful:** This localizes the M1/X1 no-square-root-loss question.
  Once each newly exposed nonzero frontier has a depth-uniform `K_r sqrt(p)`
  conductor estimate, the recursion pays `(r-T)K_r sqrt(p)` plus the explicit
  terminal power-coset ledger, not a multiplicative depth factor.
- **What to do next:** Prove or refute the required depth-uniform
  nonzero-frontier conductor bounds, starting with the asymmetric
  two-coordinate residual wall.

### 2026-06-18 - M1 weighted frontier-shift identity

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_residual_depth_frontier_shift.md`,
  `experimental/m1_low_slack_packet_template_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Strengthens the residual-depth shift note with a
  weighted ladder identity: for fixed residual packet size, the zero-frontier
  catalog at slack `T` is exactly the catalog at slack `T+1`, with the same
  binomial exact-support quotient-lift weight.
- **How it is useful:** This proves the bookkeeping part of the additive M1/X1
  route.  Inherited zero-frontier packets are carried through the ladder
  without a multiplicative factor; only the newly exposed nonzero frontier at
  each rung needs a fresh analytic estimate.
- **What to do next:** Attack the remaining nonzero-frontier problem by proving
  a depth-uniform `O(sqrt(p))` conductor bound, or search for a finite family
  where that nonzero-frontier estimate compounds.

### 2026-06-18 - M1 residual-depth ladder audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/verify_m1_residual_depth_ladder.py`,
  `experimental/m1_residual_depth_frontier_shift.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Adds a counterexample-first finite ladder audit for
  the residual-depth shift.  For fixed residual packet size, it compares the
  inherited zero-frontier packet set, exact quotient-lift weight, and shifted
  slope histogram at slack `T` with the full catalog at slack `T+1`.
- **How it is useful:** Supports the additive-error M1 route by checking that
  the zero-frontier shift is lossless at the packet/lift-weight level in
  several low-depth ladders; any mismatch would refute this bookkeeping
  mechanism.
- **What to do next:** Prove the same lossless shift as a theorem-grade global
  invariant, then focus analytic work on a depth-uniform conductor bound for
  each newly exposed nonzero frontier.

### 2026-06-18 - M1 asymmetric residual orbit ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / LEDGER.
- **What is being added:** Defines and verifies the exact remaining
  asymmetric two-coordinate mass
  `C_2^asym=C_2-C_2^0-C_2^rec-C_2^peq`.
- **How it is useful:** Every term in this residual class has nonzero
  projective line monodromies with no equal or reciprocal pair, so projective
  line permutation acts freely; the verifier records the exact orbit count
  `O_2^asym=C_2^asym/6`.
- **What to do next:** Attack this genuinely asymmetric orbit class, which is
  now the remaining two-coordinate wall after the proved reductions and the
  conditional projective equal-pair ledger.

### 2026-06-18 - M1 projective equal-pair conditional ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/verify_m1_depth_two_reciprocal_two_coordinate_lemma.py`,
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Extends the diagonal conditional ledger from
  coordinate-equal active lines to the full projective equal-pair mass
  `C_2^peq = 3C_2^diag - 2C_2^eq`.
- **How it is useful:** The verifier checks that the non-coordinate cases
  `mu=lambda` and `nu=lambda` are carried exactly to a coordinate-diagonal
  open sum by a projective chart change, so the same conditional
  `4p+3sqrt(p)` replacement applies to a larger two-coordinate submass.
- **What to do next:** Attack the remaining ramified nonreciprocal
  two-coordinate wall where no projective line pair is equal or reciprocal.

### 2026-06-18 - M1 full coordinate-diagonal conditional ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Promotes the ramified nonreciprocal
  coordinate-diagonal mass `C_2^diag` into a separate conditional certificate
  ledger with replacement `4p+3sqrt(p)` instead of `9p`.
- **How it is useful:** The finite conductor entries are now audited for the
  whole diagonal slice: `s=0` costs one unit because `mu^2=1` was already
  removed as projective reciprocal, `C(s)=0` costs at most one unit per root,
  `B(s)=0` uses the corrected `2F1` table, and infinity has nontrivial
  `alpha^(-2)`.
- **What to do next:** Attack the remaining non-diagonal ramified
  nonreciprocal two-coordinate wall, or promote the imported `2F1` table from
  conditional to theorem-grade if an accepted citation/proof is added.

### 2026-06-18 - M1 coordinate-diagonal degeneracy audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Audits the first obstruction to promoting the
  coordinate-diagonal mass: in the ramified nonreciprocal diagonal slice,
  `alpha^2=1` and `2F1` numerator-denominator cancellation both have zero
  mass.
- **How it is useful:** The nontrivial scalar monodromy `alpha^(-2)` at
  `s=infinity` rules out global invariants from this source and keeps the
  imported `2F1(chi_2,mu;alpha;t)` table nondegenerate on the diagonal
  remainder.
- **What to do next:** Audit the remaining local conductor entries for the
  general coordinate-diagonal pullback before consuming
  `C_2^diag-C_2^eq`.

### 2026-06-18 - M1 coordinate-diagonal mass audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The raw projective two-coordinate split now reports
  the full coordinate-diagonal ramified nonreciprocal mass, its non-equal
  remainder, and the existing equal-line submass.
- **How it is useful:** Makes clear that the symmetric-coordinate
  hypergeometric reduction is not equal-line-specific; the equal-line result
  is the first certificate-ready sub-slice of a larger diagonal target.
- **What to do next:** Audit global invariants and degenerate parameters for
  the general coordinate-diagonal pullback before promoting the
  `C_2^diag-C_2^eq` remainder into a conditional certificate ledger.

### 2026-06-18 - M1 equal-line conditional certificate ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The raw slack-two depth-two certificate now reports
  a separate conditional equal-line ledger: the audited `C_2^eq` submass
  drops the leading L1 weight by `5C_2^eq` and adds square-root mass
  `3C_2^eq`.
- **How it is useful:** Quantifies the exact certificate impact of accepting
  the equal-line `2F1` local-monodromy import without changing the active
  conservative `saturation_certificate`.
- **What to do next:** After review of the local-monodromy import, decide
  whether to promote the conditional equal-line ledger into the consumed raw
  certificate constants.

### 2026-06-18 - M1 `2F1` local table import contract

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Records the exact standard `2F1` local-monodromy
  table consumed by the equal-line conductor ledger: for
  `2F1(A,B;C;t)`, the `t=0` characters are `1` and `C^(-1)`.
- **How it is useful:** Pins the two-unit conductor saving at
  `lambda=infinity` to a named import, so the audited `C_2^eq`
  improvement has a clear theorem dependency before certificate constants
  are changed.
- **What to do next:** Have a human reviewer accept the local-table
  convention, then decide whether to consume the `4p+3sqrt(p)` equal-line
  replacement in the certificate ledger.

### 2026-06-18 - M1 equal-line submass full-term correction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Corrects the certificate-facing use of
  `C_2^eq`: the equal-line conductor result gives `3p` for the residual
  pullback main, but the full two-coordinate open sum also has a Jacobi part.
- **How it is useful:** The usable replacement for the current `9p` charge on
  `C_2^eq` is therefore `4p+3sqrt(p)`, giving leading drop `5C_2^eq` and
  square-root L1 mass `3C_2^eq`.
- **What to do next:** Record the standard-`2F1` local-monodromy citation
  cleanly before changing certificate constants.

### 2026-06-18 - M1 equal-line L1 submass split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The raw two-coordinate full-domain ledger now
  isolates the equal-line diagonal submass
  `C_2^eq = 3 #{a,d : 3ga+2d=0, 2ga != 0}` inside the ramified
  nonreciprocal remainder.
- **How it is useful:** This is the exact L1 mass to which the corrected
  equal-line full-open-sum import applies.
- **What to do next:** Use the corrected full-term constants recorded above.

### 2026-06-18 - M1 equal-line conductor correction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Corrects the local `2F1` cusp used in the
  equal-line conductor audit.  For `2F1(chi_2,mu;alpha;t)`, the `t=0`
  local characters are `1` and `alpha^(-1)`.  After the visible twists,
  each `B(s)=0` point has local characters `alpha` and `1`, so it contributes
  one conductor unit, not two.
- **How it is useful:** Supersedes the previous conservative `dim H^1 <= 5`
  obstruction for this equal-line diagonal subtarget.  The corrected ledgers
  are `1+2+2+2=7` on the rank-two `s`/`z` line and `2+1+2+2+4=11` on the
  rank-four y-pushforward, giving `dim H^1 <= 3` in both forms.
- **What to do next:** Turn this conditional local-monodromy audit into a
  clean proof citation/import, then propagate the equal-line diagonal
  `3p+O(sqrt(p))` estimate back into the remaining two-coordinate wall
  certificate.

### 2026-06-18 - M1 y-pushforward local conductor audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The six singular values of the degree-two
  y-pushforward are refined to a local tame conductor ledger:
  `4+1+2+2+4=13` for rank `4`, hence the standard
  `dim H^1 <= 5` target remains.
- **How it is useful:** Shows that the y-pushforward reduction localizes the
  obstruction but does not itself supply the desired `3p+O(sqrt(p))` leading
  term; the missing two units must come from a non-generic cancellation or
  sharper middle-extension identification.
- **What to do next:** Look for a two-unit saving beyond the local ledger,
  especially involving the paired boundary contributions at `y=0` and
  `y=infinity` after the Mellin twist.

### 2026-06-18 - M1 y-pushforward singular values

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The degree-two pushforward trace `G(y)` now has a
  verified singular-value checklist: generically `y=0`, `y=1`, the roots of
  `9y^2+2y+1`, `y=3/4`, and `y=infinity`; `y=3` is an ordinary projective
  fiber except in characteristic `11`.
- **How it is useful:** Refines the next conductor target from a
  two-variable surface divisor to a six-point one-dimensional pushforward
  problem.
- **What to do next:** Compute the local conductor contribution of `G(y)` at
  these six values after the Mellin twist by `alpha chi_2`.

### 2026-06-18 - M1 resultant surface divisor audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The compactified y-line resultant is audited in
  `P^1_x times P^1_y`. It is a bidegree `(2,2)` curve with an ordinary node
  at `(x,y)=(infinity,0)`, and the boundary-plus-branch divisor has
  complement Euler target `6`.
- **How it is useful:** Rules out a naive two-variable Kummer surface route
  to the desired `3p` leading term and keeps focus on the degree-two
  pushforward trace `G(y)`.
- **What to do next:** Analyze the conductor of `G(y)` as a pushforward sheaf
  rather than through the full compactified kernel surface.

### 2026-06-18 - M1 y-line kernel resultant

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The `y`-pushforward is rewritten as an explicit
  finite kernel sum. The outer quadratic character cancels, leaving the
  radical `x+(3x-1)z^2`, whose split-fiber product has resultant
  `16x^2y^2-8xy^2+4xy+y^2-2y+1`.
- **How it is useful:** Gives a concrete divisor for the next conductor
  calculation of the degree-two pushforward trace `G(y)`.
- **What to do next:** Compute or bound the conductor contribution of this
  resultant divisor together with the projective boundary and branch lines.

### 2026-06-18 - M1 balanced y-line pushforward

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The completed `z`-line trace is pushed through
  `y=(1+3z^2)/(1-z)^2`. The balanced kernel becomes the ordinary character
  `(alpha chi_2)(y)`, and the paired hypergeometric parameters satisfy an
  explicit quadratic relation in `lambda` and `y`.
- **How it is useful:** Converts the remaining finite-cluster problem into a
  Mellin transform of a degree-two hypergeometric pushforward trace `G(y)`.
- **What to do next:** Analyze the conductor and possible quadratic-transform
  cancellation of `G(y)`.

### 2026-06-18 - M1 balanced z-line conductor audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The complete `z`-line trace now has an explicit
  conservative conductor ledger. Infinity has no Kummer ramification, but the
  regular point `z=1` carries scalar twist `alpha^(-2)`, while the two
  `1+3z^2=0` points retain local characters `alpha chi_2` and `alpha^(-1)`.
- **How it is useful:** Shows that the `z`-completion localizes the remaining
  obstruction but does not by itself reduce the generic `dim H^1 <= 5`
  estimate; the missing two-unit saving must be finite.
- **What to do next:** Look for a cancellation or middle-extension
  identification involving `z=1` and the two `1+3z^2=0` points.

### 2026-06-18 - M1 equal-line balanced z-line completion

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The paired equal-line pullback is completed on the
  `z=s/(s+2)` line as a balanced trace with kernel
  `chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)`, plus only the regular fibers
  `-H(1/4)` and `alpha(3) chi_2(3) H(1/3)`.
- **How it is useful:** This makes the `3p+O(sqrt(p))` target equivalent, up
  to square-root corrections, to a complete rank-two `z`-line trace whose
  Kummer part has no infinity ramification.
- **What to do next:** Use the finite singular support
  `z=0`, `1+2z^2=0`, `1+3z^2=0`, and `z=1` for the next conductor audit.

### 2026-06-18 - M1 equal-line hypergeometric conductor audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A rank-two line-sheaf conductor ledger for the
  pulled-back hypergeometric trace.  After the visible twists, the two
  `B(s)=0` points have local characters `alpha chi_2` and `alpha^(-1)`,
  hence no inertia invariants in the remaining equal-line wall. The same
  note records the deck involution `tau(s)=-s/(s+1)` and its Kummer-twist
  multiplier, then rewrites the paired sum in the quotient coordinate
  `z=s/(s+2)`.
- **How it is useful:** Shows that the standard local conductor calculation
  still gives the generic `dim H^1 <= 5` route, not the desired `3`.
  This pinpoints the missing saving: two conductor units must be recovered
  beyond the generic count, and bare deck symmetry is not enough because the
  twist becomes the auxiliary trace `sum_{z^2=q} alpha^(-2)(1-z)`.
- **What to do next:** Prove a cancellation or identification that saves the
  two `B(s)=0` conductor units, or find finite evidence showing that such a
  saving is impossible.

### 2026-06-18 - M1 equal-line plane-divisor audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The normalized equal-line pullback is compactified
  in `P^2`, with divisor
  `B_h`, `X=0`, `X=Z`, `D_h=4B_hX-S^2Z`, and sometimes infinity.
  The resulting plane-divisor complement has Euler target `5`, with or
  without the infinity line.
- **How it is useful:** Rules out the naive rank-one surface Kummer route for
  the desired `3p+O(sqrt(p))` leading term, forcing the proof to use the
  hypergeometric pullback or another sharper cancellation mechanism.
- **What to do next:** Prove the pulled-back hypergeometric conductor bound
  that explains the missing two top-dimensional units.

### 2026-06-18 - M1 equal-line pullback spectrum audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/search_m1_equal_line_pullback_spectrum.py`,
  `experimental/m1_equal_line_pullback_spectrum_experiment.md`,
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / COUNTEREXAMPLE / AUDIT.
- **What is being added:** An FFT-based spectrum scanner computes the
  normalized equal-line pullback main term for every multiplicative character
  of `F_p^*` at once, records the maximum equal-line domain size for each
  character, then filters the same data back to the M1 equal-line tuple
  families.
- **How it is useful:** The scan disproves the tempting unrestricted
  all-character exact `3p` pullback conjecture and shows that the corrected
  target should be `3p+O(sqrt(p))` with equal-line domain-size arithmetic
  kept explicit. This narrows the proof target toward the admissible
  character arithmetic or hypergeometric pullback structure.
- **What to do next:** Prove the `3p+O(sqrt(p))` pullback conductor bound
  with the fixed-domain character filter visible, or identify the next
  finite obstruction to that top-dimensional target.

### 2026-06-18 - M1 equal-line diagonal reduction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_equal_line_diagonal_reduction.md`,
  `experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py`,
  `experimental/search_m1_equal_line_pullback.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_remaining_two_coordinate_wall_experiment.md`,
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The equal-line diagonal two-coordinate family is
  reduced by symmetric variables `s=u+v`, `t=uv` into a bounded Jacobi part
  and a residual trace, then the residual is rewritten as a pullback of a
  three-point hypergeometric trace with explicit branch divisor and a
  single-character normal form.
- **How it is useful:** Turns the numerically near-sharp remaining-wall
  subfamily into a sharper analytic target: prove a `3p`-level bound for the
  hypergeometric pullback to explain the observed near-`4p` behavior.
- **What to do next:** Prove the residual trace bound or identify the
  geometric obstruction responsible for the near-alignment of the two pieces.

### 2026-06-18 - M1 remaining-wall numerical stress scan

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/search_m1_remaining_two_coordinate_wall.py`,
  `experimental/m1_remaining_two_coordinate_wall_experiment.md`,
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** A targeted finite scan of the ramified
  nonreciprocal two-coordinate class left after the proved slice reductions.
  The report preset gives `946184` tuple evaluations with no `4p` violation.
- **How it is useful:** The largest rows all have equal projective line
  monodromies, suggesting a narrower analytic subtarget for the remaining
  M1 two-coordinate wall.
- **What to do next:** Prove the equal-line-monodromy diagonal case
  `S_{a,a,0,d}` with `d == -3a mod e`, or find a larger counterexample.

### 2026-06-18 - M1 remaining-family near-4p obstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/verify_m1_depth_two_two_coordinate_sharp_target.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** The two-coordinate sharp-target verifier now
  classifies audited tuples by projective line monodromy. The targeted
  `(p,n,e,h)=(421,20,21,42)` tuple with ratio `3.9771715522` is certified as
  `ramified_nonreciprocal`.
- **How it is useful:** Shows that the near-`4p` finite obstruction survives
  after all currently proved two-coordinate slice reductions, so the
  remaining M1 wall still needs a near-`4p` theorem.
- **What to do next:** Prove the normal-crossing trace bound for the remaining
  ramified nonreciprocal family or find an obstruction above `4p`.

### 2026-06-18 - M1 projective reciprocal line-pair slices

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_reciprocal_two_coordinate_lemma.py`,
  `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`,
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The reciprocal two-coordinate lemma is extended
  projectively: if any two of the three line monodromies `mu`, `nu`, and
  `(mu nu eta^2)^(-1)` are reciprocal, an affine chart reduces the core to
  the proved reciprocal slice. The raw scanner now also splits this exact
  ramified projective-reciprocal L1 mass and charges it by
  `4p+3 sqrt(p)`. The raw split is now recorded by closed forms for
  `q/e=1` and `q/e=2`, with the verifier checking the formulas against direct
  exponent enumeration. The roadmap records this as the active substep before
  attacking the remaining ramified nonreciprocal family.
- **How it is useful:** Removes the ramified slices `nu eta^2=1` and
  `mu eta^2=1` from the unresolved two-coordinate wall, in addition to the
  original `mu nu=1` slice, and improves the raw slack-two Kummer certificate
  arithmetic.
- **What to do next:** Prove the normal-crossing trace bound for the
  remaining ramified-infinity case with no reciprocal projective line pair.

### 2026-06-18 - M1 raw infinity-unramified ledger split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** The raw slack-two depth-two Kummer ledger now
  separates the exact two-coordinate L1 mass with trivial infinity monodromy
  `mu nu eta^2=1`. That mass is charged by the proved open-set bound
  `2p+5 sqrt(p)`, while only the ramified-infinity remainder still pays `9p`.
- **How it is useful:** Feeds the new infinity-unramified theorem into the
  actual full-domain certificate arithmetic, improving the raw uniform
  thresholds while leaving fixed-window and quotient-union ledgers
  conservative.
- **What to do next:** Derive safe fixed-window or quotient-window L1 splits
  by infinity monodromy, or prove the remaining ramified-infinity `4p`
  normal-crossing trace bound.

### 2026-06-18 - M1 infinity-unramified two-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_infinity_unramified_two_coordinate_lemma.py`,
  `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`,
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A proof-level reduction for the two-coordinate
  core when the infinity monodromy is trivial, `mu nu eta^2=1`. The ratio
  substitution `u=tv` and reciprocal variable `r=1/v` reduce the core to two
  genus-zero sums, giving `2p+2 sqrt(p)` plus the usual `3 sqrt(p)` line
  correction.
- **How it is useful:** Proves the whole `chi=2` branch predicted by the
  projective Euler calculation, leaving the infinity-ramified `chi=4`
  genuinely nonreciprocal family as the main two-coordinate target.
- **What to do next:** Prove the clean normal-crossing trace bound for the
  remaining infinity-ramified two-coordinate core, or find a finite
  obstruction above the near-sharp `4p` target.

### 2026-06-18 - M1 two-coordinate projective Euler target

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_projective_euler_target.md`,
  `experimental/verify_m1_kummer_divisor_geometry.py`,
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A projective Euler-characteristic calculation for
  the two-coordinate Kummer core. The infinity monodromy is
  `(mu nu eta^2)^{-1}`, giving expected top-dimensional coefficients `4`
  when infinity is ramified and `2` when `mu nu eta^2=1`.
- **How it is useful:** Explains why the audited `4p` target is the natural
  conductor target for the two-coordinate wall, and isolates a sharper
  infinity-unramified subtarget that contains the reciprocal quadratic slice.
- **What to do next:** Supply or prove the clean normal-crossing Kummer
  cohomology theorem that turns these Euler coefficients into uniform trace
  bounds for the genuinely nonreciprocal family.

### 2026-06-18 - M1 two-coordinate near-4p audit sharpening

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/verify_m1_depth_two_two_coordinate_sharp_target.py`,
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** The targeted near-`4p` audit row is sharpened to
  `(p,n,e,h)=(421,20,21,42)`, where `(a,b,c,d)=(5,5,0,6)` has open
  two-coordinate ratio `3.9771715522` to `p`.
- **How it is useful:** This makes the proposed `4p` target almost sharp in
  finite evidence: any future two-coordinate constant below `3.9771715522p`
  is already ruled out.
- **What to do next:** Use this as a guardrail for the two-coordinate
  conductor proof; it is not an exhaustive `p=421` scan.

### 2026-06-18 - M1 two-coordinate near-4p audit correction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/verify_m1_depth_two_two_coordinate_sharp_target.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** The targeted `(p,n,e,h)=(599,26,23,46)` audit
  row for `(a,b,c,d)=(20,20,0,9)` is made verifier-consistent, with ratio
  `3.8317392150` to `p`.
- **How it is useful:** Keeps the near-`4p` finite obstruction reproducible
  while making clear that the targeted row rules out constants below
  `3.8317392150p`, not a larger stale value.
- **What to do next:** Use this as a guardrail for the two-coordinate
  conductor proof; it is not an exhaustive `p=599` scan.

### 2026-06-18 - M1 reciprocal two-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_reciprocal_two_coordinate_lemma.py`,
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A ratio-variable reduction for the reciprocal
  two-coordinate subfamily `nu=mu^{-1}`. The core sum becomes a genus-zero
  Kummer sum in `t=v/u`, giving a `4p` bound in the nonquadratic conic case
  and a `2p+2 sqrt(p)` bound in the quadratic conic case, plus the existing
  `3 sqrt(p)` line correction.
- **How it is useful:** Cuts a structured diagonal slice out of the
  two-coordinate residue-line wall; the unresolved family is now more sharply
  the genuinely nonreciprocal trace-family problem.
- **What to do next:** Look for further ratio or trace reductions for
  nonreciprocal pairs, or decide whether this reciprocal slice should affect
  a later L1 ledger split.

### 2026-06-18 - M1 two-coordinate fiber reduction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_fiber_reduction.md`,
  `experimental/verify_m1_depth_two_two_coordinate_fiber_reduction.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** An exact decomposition of each two-coordinate
  mixed term into a one-dimensional fiber trace sum plus the removed
  principal-coordinate line. The line term is proved to be at most
  `3 sqrt(p)` by a genus-zero Kummer bound, and the outer bad-parameter set
  is isolated as `u=0`, `u^2+u+1=0`, `-3u^2-2u-3=0`, and infinity.
- **How it is useful:** Sharpens the remaining degree-four `9p` wall: the
  unresolved part is now cancellation in a one-dimensional trace family, not
  the principal-coordinate line correction.
- **What to do next:** Prove a conductor/Euler-characteristic bound for this
  fiber trace family, or use it to test whether the current `9p` constant can
  be reduced.

### 2026-06-18 - M1 two-coordinate sharp-target audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`,
  `experimental/verify_m1_depth_two_two_coordinate_sharp_target.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A finite exact-sum audit for the sharper possible
  `4p` target on two-coordinate mixed Kummer terms. The verifier exhausts
  all such tuples on the baseline samples and selected larger samples; the
  largest exhaustive-sample ratio is `3.3896787506` at
  `(p,n,e,h)=(109,18,6,12)`. It also records a targeted near-sharp tuple at
  `(p,n,e,h)=(421,20,21,42)` with ratio `3.9771715522`, obstructing any
  future two-coordinate constant below this value.
- **How it is useful:** Identifies the next plausible strengthening after the
  one-coordinate lemmas: the current `9p` two-coordinate import may be
  conservative, while the possible `4p` replacement is already nearly sharp
  and the three-coordinate `16p` term remains separate.
- **What to do next:** Try to prove the two-coordinate `4p` target or find a
  finite obstruction above `4p` before changing any certificate constants.

### 2026-06-18 - M1 nonquadratic one-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_nonquadratic_one_coordinate_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** A one-dimensional reduction for the remaining
  nonquadratic one-coordinate mixed Kummer terms. The fixed-coordinate conic
  sum becomes a Jacobi factor times the discriminant sum
  `sum_u mu(u) chi_2(Delta(u)) eta(Delta(u))`, giving the `4p` bound from
  standard Jacobi and genus-zero Kummer estimates.
- **How it is useful:** Removes all one-coordinate mixed terms from the
  two-variable normal-crossing Kummer import, so the remaining conditional
  M1 depth-two wall starts at two active coordinate characters.
- **What to do next:** Attack the degree-four two-coordinate `9p` estimate
  or find a precise normal-crossing reference for the two- and
  three-coordinate mixed terms.

### 2026-06-18 - M1 quadratic one-coordinate lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_quadratic_one_coordinate_lemma.md`,
  `experimental/verify_m1_depth_two_quadratic_one_coordinate_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / EXPERIMENTAL.
- **What is being added:** A proof-level slice lemma for the slack-two
  depth-two mixed family where the conic character is quadratic and exactly
  one coordinate character is nonprincipal. The verifier checks the exact
  quadratic-fiber identity and the `4p` open-set bound on representative
  prime/index samples.
- **How it is useful:** Removes this mixed family from the external
  two-variable Kummer import, leaving only nonquadratic one-coordinate,
  two-coordinate, and three-coordinate mixed normal-crossing estimates.
- **What to do next:** Use the same proof/import boundary to attack the
  remaining one-coordinate nonquadratic `4p` term or the degree-four
  two-coordinate `9p` term.

### 2026-06-18 - M1 mixed Kummer finite obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_residue_line_roadmap.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/verify_m1_depth_two_kummer_constant_audit.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / COUNTEREXAMPLE.
- **What is being added:** A compact update to the four-point M1 roadmap and
  a verifier-backed finite obstruction to charging every mixed Kummer term by
  `4p`: for `(p,n,e,h)=(37,9,4,4)`, the three-coordinate tuple `(2,2,2,2)`
  has absolute value `185=5p`.
- **How it is useful:** Keeps PR #82 focused on the real remaining wall: the
  degree-stratified normal-crossing line/conic Kummer estimate, not a
  bookkeeping simplification of all mixed terms to the one-coordinate constant.
- **What to do next:** Prove or cite the uniform degree-stratified Kummer
  estimate, or sharpen the audit until the exact geometric input is isolated.

### 2026-06-18 - M1 depth-two elementary open-set lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_elementary_open_set_lemma.md`,
  `experimental/verify_m1_depth_two_elementary_open_set_lemma.py`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Isolates the proof of the elementary open-set
  correction in the slack-two depth-two Kummer ledger: the `d=0` Jacobi and
  conic-only masses each have a `p + 6 sqrt(p)` bound on the Kummer open set.
  Adds a finite verifier for the conic and coordinate-line correction terms.
- **How it is useful:** Makes the previous open-set ledger repair reviewable
  as a named lemma rather than only as scanner arithmetic, while keeping the
  genuinely mixed two-variable Kummer estimate separate.
- **What to do next:** Use this lemma as the elementary base case while
  looking for a uniform proof or citation of the remaining mixed
  normal-crossing line/conic Kummer estimate.

### 2026-06-18 - M1 depth-two Kummer open-set correction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_kummer_constant_audit.md`,
  `experimental/verify_m1_depth_two_kummer_constant_audit.py`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Repairs the slack-two depth-two Kummer ledger by
  adding the missing elementary open-set correction for the `d=0` Jacobi and
  conic-only character masses. Adds a finite exact character-sum verifier
  that exhausts representative small prime/index cases.
- **How it is useful:** Directly strengthens PR #82 by fixing the main
  conditional M1 depth-two certificate instead of merely adding another
  consequence. The mixed normal-crossing Kummer import remains isolated, but
  the elementary part of the certificate now matches the actual open set.
- **What to do next:** Look for a uniform proof or citation of the remaining
  mixed line/conic Kummer estimate, using this finite audit as a regression
  check for any proposed constants.

### 2026-06-18 - M1 slack-three genus-zero Kummer lemma

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_slack_three_genus_zero_kummer_lemma.md`,
  `experimental/verify_m1_slack_three_genus_zero_kummer_lemma.py`,
  `experimental/m1_slack_three_first_superboundary_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT.
- **What is being added:** Isolates the one-dimensional genus-zero Kummer
  input behind the slack-three proper-subgroup constants `6 sqrt(p)` and
  `12 sqrt(p)`, with a finite-field verifier for representative subgroup
  indices.
- **How it is useful:** Removes an unnamed import from the slack-three
  first-superboundary theorem and leaves the main remaining M1 character-sum
  dependency focused on the harder two-variable normal-crossing estimate.
- **What to do next:** Decide whether the standard `P^1` multiplicative Weil
  bound needs a formal citation before promotion, then return to the
  normal-crossing Kummer dependency or the aperiodic residue-line step.

### 2026-06-18 - M1 low-slack packet-template theorem

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_low_slack_packet_template_theorem.md`,
  `experimental/verify_m1_low_slack_packet_template.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Extracts the common low-slack residual-packet
  theorem: exact packet-lift weights, first-nonzero frontier partition,
  terminal pure-zero power-cosets, and the positive-dither depth gate. Adds a
  tiny verifier covering representative slack-two and slack-three scans.
- **How it is useful:** Gives PR #82 a unifying template layer above the
  individual slack-two and slack-three packet theorems, making clear which
  parts of future M1 work are inherited bookkeeping and which are genuinely new
  coset-image estimates.
- **What to do next:** Use this template to keep future low-slack work focused
  on nonzero frontiers and avoid recounting inherited zero-slope strata.

### 2026-06-18 - M1 residual-depth frontier shift

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_residual_depth_frontier_shift.md`,
  `experimental/verify_m1_residual_depth_frontier_shift.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Extracts the residual-depth frontier shift theorem:
  zero-slope packets at `(T,k,d)` are exactly depth-`d-1` packets at
  `(T+1,k-1,d-1)`, with the same exact-support lift gate. Adds a verifier for
  the implemented `d=2` cases, including the slack-two/slack-three conic
  interface.
- **How it is useful:** Turns the low-slack packet work into a hierarchy: the
  slack-two depth-two theorem and slack-three first-superboundary theorem are
  adjacent frontiers, not isolated computations.
- **What to do next:** Use this shift as the organizing principle for a common
  low-slack template statement, then reserve new character-sum work for the
  genuinely nonzero frontiers.

### 2026-06-18 - M1 slack-three first-superboundary theorem

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_slack_three_first_superboundary_theorem.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Extracts a standalone theorem note for the
  slack-three first-superboundary packet: the conic shape reduction, the
  one-variable split-cubic beta ledger, full-domain saturation thresholds, and
  proper-subgroup cube-coset certificates.
- **How it is useful:** Advances the roadmap's fixed low-slack template step
  beyond the slack-two depth-two PR. It shows that the next low-slack frontier
  also decomposes into explicit packet templates and coset coverage ledgers
  before the aperiodic M1 packing problem is attacked.
- **What to do next:** Keep the proper-subgroup character-sum estimates
  clearly conditional, then look for a common low-slack template statement
  unifying the slack-two depth-two and slack-three first-superboundary ledgers.

### 2026-06-18 - M1 residue-line roadmap

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/m1_residue_line_roadmap.md`,
  `experimental/agents-log.md`.
- **Status:** CONJECTURAL / AUDIT.
- **What is being added:** Maintains a compact four-point working plan for the
  M1 residue-line packing program: keep PR #82 as one focused low-slack packet,
  close the two-coordinate trace-family wall, use finite audits as guardrails,
  and only then generalize to fixed low-slack templates.
- **How it is useful:** Keeps the high-level direction visible without
  changing Papers A--D or overloading the theorem note with strategy text.
- **What to do next:** Prove the conductor bound for the trace family with bad
  parameters `u=0`, `u^2+u+1=0`, `-3u^2-2u-3=0`, and infinity, or find a
  counterexample to the current near-sharp `4p` target.

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

### 2026-06-18 - M1 fixed-window principal-removed Parseval L1 bound

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Replaces the crude fixed-window Fourier L1 ledger
  with a principal-removed Parseval/Cauchy-Schwarz bound. For a quotient
  window of size `R` in quotient order `N`, the nonprincipal quotient Fourier
  L1 is at most `sqrt((N-1)R(N-R))`, so after ambient lifting the active
  one-dimensional L1 is bounded by
  `(e-1)R + e ceil(sqrt((N-1)R(N-R)))`. In the complement-window case
  `R=N-1`, this specializes to the exact value `(2e-1)R`. The two-fiber and
  fixed-window Kummer certificates tensor this bound into one-, two-, and
  three-coordinate masses.
- **How it is useful:** Keeps the same conditional Kummer input but sharply
  reduces the coefficient L1 paid by fixed-window certificates. The verifier
  now checks the new integer Parseval/complement ledger; the two-fiber
  threshold improves from `332` to `108`, and the fixed-window threshold from
  `808` to `96`. The remaining failed fixed-window audit at `p=97, N=6, R=3`
  tightens from `17608` to `13378`.
- **What to do next:** Look for an analogous non-crude L1 certificate for
  larger quotient windows or replace the remaining three-coordinate Kummer
  import.

### 2026-06-18 - M1 degree-stratified Kummer ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** Refines the M1 slack-two depth-two Kummer ledger by
  charging mixed terms according to the actual active radical degree. The
  existing elementary quadratic one-coordinate `4p` term is retained, remaining
  one-coordinate mixed terms pay the degree-three constant `4p`,
  two-coordinate mixed terms pay `9p`, and only three-coordinate mixed terms
  pay the full degree-five `16p`. The quotient-window union certificate now
  computes exact ambient Fourier L1 masses for one, two, and three active
  coordinates.
- **How it is useful:** Narrows the expensive conditional import to the truly
  three-coordinate mixed Kummer terms and improves the verified M1 saturation
  thresholds without broadening the PR. The verifier checks the new active
  coordinate ledger by independent ambient enumeration in the quotient-window
  cases.
- **What to do next:** Try to replace the remaining three-coordinate
  normal-crossing import with a cited theorem or direct cohomology calculation.

### 2026-06-18 - M1 quadratic one-coordinate split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A further split of the M1 depth-two Kummer error:
  when the conic character is quadratic and exactly one coordinate character
  is nonprincipal, the term is bounded elementarily by `4p` instead of the
  imported `16p` normal-crossing estimate. The scanner/verifier now reports
  `quadratic_one_coordinate_l1_bound` and subtracts that mass from the
  remaining imported `kummer_l1_bound` in the additive raw, two-fiber, and
  fixed-window certificates.
- **How it is useful:** Narrows the conditional part of the integrated M1
  Kummer ledger without changing the quotient-window union claim. The
  remaining external import is now focused on genuinely mixed terms not
  covered by the Jacobi, conic-only, or quadratic one-coordinate arguments.
- **What to do next:** Separate the quotient-window union L1 term by
  coordinate support if possible, or prove/cite the remaining mixed
  normal-crossing Kummer estimate.

### 2026-06-18 - M1 quotient-window one-coordinate split

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** Extends the quadratic one-coordinate `4p` split
  from the additive fixed-window certificates to the quotient-window union
  certificate. The scanner now computes the exact one-coordinate quotient L1
  term `O_R`, including characters that are quotient-principal but nontrivial
  on the kernel, and subtracts this mass from the remaining imported mixed
  Kummer term.
- **How it is useful:** Further narrows the conditional M1 depth-two union
  certificate without changing the external Kummer assumption. The verifier
  checks the new `quotient_one_coordinate_l1_bound` against direct ambient
  quotient-Fourier enumeration.
- **What to do next:** Look for higher-coordinate elementary mixed subcases or
  prove/cite the remaining normal-crossing Kummer estimate.

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
  `experimental/2026-06-18-fable-loop/audits/`
  `20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/2026-06-18-fable-loop/local_checks/`
  `20260618_cycle18_resonance_slope_symbolic.py`,
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
