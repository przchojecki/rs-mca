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

### 2026-06-18 - L1 recursive Johnson packing bound

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Applies the recursive Johnson bound to the
  complement `r`-packings inside co-large monomial-prefix fibers:
  `J(n,m,r) <= floor((n/m)J(n-1,m-1,r-1))`.
- **How it is useful:** This gives a standard finite-design scanner bound
  sharper than the raw `binom(n,r)/binom(m,r)` ratio in many finite regimes.
  The verifier records deterministic dyadic cases, including the improvement
  from `1381` to `1027` at `(n,k,sigma)=(64,28,15)`.
- **What to do next:** Use the Johnson recursion as the default finite
  baseline before searching for actual low-degree divisor-gap components.

### 2026-06-18 - L1 integer Plotkin refinement

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds the integer second-moment refinement of the
  co-large Plotkin bound. For a putative fiber size `L`, the incidence degrees
  over `H` must have integer square sum at least the balanced composition
  lower bound; if this exceeds `Lm+L(L-1)(r-1)`, that `L` is impossible.
- **How it is useful:** This turns the rational Plotkin estimate into a
  finite scanner obstruction and records the near-design condition for any
  extremal co-large fiber. In the `F_17` certificate it improves the proved
  universal bound from `4` to `3`.
- **What to do next:** Use the near-design obstruction to focus future
  low-degree divisor-gap searches on incidence-balanced candidate fibers.

### 2026-06-18 - L1 affine RS list reduction

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Recasts each co-large monomial-prefix fiber as an
  affine Reed-Solomon list: for a base complement locator `L_0`, the fiber is
  exactly the set of `Q` with `deg Q<r` such that `L_0+Q` has `m` roots in
  `H`. The verifier exhausts all `17^2` perturbations for every `F_17`
  prefix fiber and matches the original fiber histogram.
- **How it is useful:** This identifies the co-large L1 core as a standard
  affine low-rate RS list-size problem. The Plotkin bound becomes the Johnson
  bound for that list, and the remaining gap is a non-Johnson local-limit
  problem for affine locator cosets.
- **What to do next:** Use this RS-list formulation when comparing the
  high-slack safe region with the full Paper B locator local-limit conjecture.

### 2026-06-18 - L1 co-large Plotkin bound

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds a second-moment/Plotkin bound for co-large
  monomial-prefix fibers. If `r=n-k-2sigma>0`, `m=n-k-sigma`, and
  `m^2>n(r-1)`, then every prefix fiber has size at most
  `n(m-r+1)/(m^2-n(r-1))`.
- **How it is useful:** This upgrades the co-large L1 anchor from
  exponential-in-`r` packing to constant-size fibers throughout the linear
  high-slack region `r/n < (1-sqrt(rho))^2`, far beyond the previous
  fixed-width/log-width corollaries.
- **What to do next:** Compare this safe high-slack region against the
  corrected reserve in Paper B to identify the remaining gap to the final
  `sigma=Theta(n/log n)` local-limit target.

### 2026-06-18 - L1 co-large packing-code profile

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Rephrases co-large prefix fibers as complement
  `r`-packings and support constant-weight codes with minimum distance
  `2(sigma+1)`. The verifier now records the internal ordered exchange profile
  `Delta_j` and maximum codegree profile `Gamma_j`; in the `F_17` certificate,
  `Delta_6=80`, `Gamma_6=1`, and all `j<=5` entries vanish.
- **How it is useful:** This makes the L1/M1 bridge ledger-ready: an internal
  co-large prefix fiber contributes no strict high-overlap mass, and its first
  nonzero exchange profile is explicit in the finite route-cut example.
- **What to do next:** Use this packing-code view when promoting co-large
  prefix-fiber bounds into support-family certificate language.

### 2026-06-18 - L1 co-large fiber separation

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Extracts the overlap consequence of the co-large
  complement-locator packing proof: distinct supports in one co-large
  monomial-prefix fiber exchange at least `sigma+1` points, hence intersect in
  at most `k-1` points.
- **How it is useful:** This connects the L1 prefix-fiber theorem to the M1
  support ledger. Co-large prefix fibers may have multiplicity, but their
  internal strict high-overlap correction at slack `sigma` is zero.
- **What to do next:** Use this separation lemma to split future M1/L1
  scanners into internal prefix-fiber pairs, which are harmless in the strict
  range, and cross-fiber pairs, where new aperiodic packing input is still
  needed.

### 2026-06-18 - L1 growing-width co-large prefix bound

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Extends the co-large packing bound from fixed
  width `r=n-k-2sigma` to a growing-width envelope:
  `|Phi_sigma^{-1}(c)| <= (2/(1-rho-r/n))^r` whenever `k <= rho n` and
  `r < (1-rho)n`. The verifier checks the rational inequality on the
  `F_17` certificate and a deterministic dyadic parameter grid.
- **How it is useful:** This turns the co-large L1 result into a polynomial
  fiber bound for `r=O(log n)` and a quasipolynomial bound for polylogarithmic
  `r`, giving a theorem-backed region between the tiny fixed-width examples
  and the full prefix local-limit conjecture.
- **What to do next:** Compare this co-large envelope with the reserve
  inequalities in Paper B/C to locate the first parameter regimes where the
  final L1 proof needs genuinely new aperiodic input.

### 2026-06-18 - L1 aperiodic prefix-collision certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / COUNTEREXAMPLE.
- **What is being added:** Promotes a finite `F_17` monomial-prefix
  route cut into a standalone proof note and verifier: for `n=16`, `k=6`,
  `sigma=4`, the full `Phi_4` fiber distribution has forty aperiodic
  two-point collisions and no larger fibers, despite positive generated-field
  entropy margin and empty quotient-core profile.  The verifier also compresses
  the collisions into three dilation orbits of complement locator pairs with
  linear gaps `L_A-L_B`, using the general complement-prefix lemma for
  multiplicative subgroups, records the exact divisor-gap parametrization, and
  records the equivalent divisor-gap graph formulation and co-large packing
  bound `|Phi_sigma^{-1}(c)| <= binom(n,r)/binom(m,r)` for
  `r=n-k-2sigma`, including the fixed-width constant-fiber corollary.
- **How it is useful:** Targets L1 by showing that quotient-core removal
  cannot be strengthened to finite-field aperiodic injectivity; the surviving
  local-limit theorem must be a multiplicity bound for aperiodic prefix
  collisions.
- **What to do next:** Use the verifier shape as a tiny scanner target for
  larger monomial-prefix cases and separate isolated aperiodic collisions from
  quotient-periodic families.

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
