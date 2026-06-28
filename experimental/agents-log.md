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

### 2026-06-28 - M1 b=2 near-fiber ledger descends to quotient lines

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that the near-projective-fiber exceptional
  term in the `b=2` cutoff ledger is an incidence sum over fixed projective
  fiber subsets, and each nonempty fixed-subset fiber descends to a
  one-dimensional quotient line of width `A_0+c-1`.
- **How it is useful:** Completes the structural descent of both exceptional
  terms in the cutoff ledger: base-heavy supports become fixed-divisor
  quotient fibers, and near-fiber supports become bounded-width quotient-line
  fibers.
- **What to do next:** Bound the generic determinant-gate count and these
  quotient ledgers uniformly in the all-line M1 residue-packing setting.

### 2026-06-28 - M1 b=2 common-base ledger descends by incidence

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that the common-base exceptional term in the
  `b=2` cutoff ledger is an exact fixed-subset incidence sum over descended
  quotient fibers: supports with many base roots are counted by subsets
  `C subset B_0 cap roots(L_0)` and quotient supports after dividing by
  `ell_C`.
- **How it is useful:** Turns the base-heavy ledger from the cutoff reduction
  into lower-width fixed-divisor quotient fibers, leaving no new residual
  enumeration in that branch.
- **What to do next:** Bound the descended fixed-divisor quotient fibers
  uniformly in the all-line M1 residue-packing setting.

### 2026-06-28 - M1 b=2 cutoff ledger reduction

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / REDUCTION.
- **What is being added:** Combines the global determinant-gate ledger, the
  weight escape filter, and the dominant-slice quotient certificates into a
  cutoff inequality for the whole `b=2` branch.
- **How it is useful:** Reduces the branch to three explicit inputs: an
  unweighted generic determinant-gate count, a common-base fixed-divisor
  ledger, and a bounded-complement projective-fiber quotient ledger.
- **What to do next:** Prove polynomial bounds for these three ledgers using
  the all-line fixed-root, quotient-periodic, tangent, and aperiodic M1
  charges.

### 2026-06-28 - M1 b=2 non-generic determinant gates have quotient certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Shows that the non-generic pieces from the
  determinant-weight escape filter carry explicit fixed-divisor certificates:
  base-heavy supports give common-base quotient slices, while near-fiber
  supports give bounded-complement projective-fiber quotient kernels of width
  at most `A_0+c-1`.
- **How it is useful:** Converts the exceptional weighted determinant-gate
  mass into concrete quotient/fixed-divisor ledgers, leaving the remaining
  generic mass with the reciprocal saving from the previous entry.
- **What to do next:** Bound the resulting base-heavy and bounded-complement
  quotient ledgers with the existing fixed-root, quotient-periodic, tangent,
  and aperiodic M1 charges.

### 2026-06-28 - M1 b=2 determinant-gate weights force escape concentration

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves the support-local escape inequality
  `g_A(R) >= L_A(R)e_A(R)/2` for the reciprocal weights in the global `b=2`
  determinant-gate ledger, where `e_A(R)` counts non-base roots outside the
  largest projective fiber.
- **How it is useful:** Splits the remaining weighted determinant-gate family
  into a generic part with explicit reciprocal saving and two structural parts:
  base-heavy supports and near-projective-fiber supports, both already shaped
  like fixed-divisor/residue-line M1 charges.
- **What to do next:** Use this filter to charge the global determinant-gate
  ledger by bounding the base-heavy and near-fiber pieces after quotient,
  tangent, fixed-root, and aperiodic reserves.

### 2026-06-28 - M1 b=2 global determinant-gate ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / SYNTHESIS.
- **What is being added:** Sums the `b=2` fixed-anchor endpoint across a family
  of anchors, giving an exact weighted ledger over split good-pair determinant
  gates.
- **How it is useful:** Identifies the precise global object left to charge in
  the `b=2` branch of M1: weighted determinant gates after fixed-root,
  quotient-periodic, tangent, and aperiodic reserves.
- **What to do next:** Prove polynomial bounds for this weighted split
  determinant-gate family in the all-line residue-packing setting.

### 2026-06-28 - M1 b=2 fixed-anchor endpoint theorem

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / SYNTHESIS.
- **What is being added:** Records the endpoint theorem for `b=2` fixed
  anchors: zero-good supports vanish, residual supports are the weighted split
  image of good-pair interpolation, and each image is a two-root absorbed
  quotient/determinant-gate split test.
- **How it is useful:** Clarifies that the local `b=2` obstruction has been
  reduced to a global good-pair determinant-gate ledger.
- **What to do next:** Charge the resulting determinant gates across anchors by
  fixed-root, quotient-periodic, tangent, or aperiodic M1 residue-packing
  estimates.

### 2026-06-28 - M1 b=2 determinant gates normalize good-pair quotients

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that the `3 x 3` determinant gate for a good
  pair is exactly the good-pair determinant times the interpolated locator, and
  after dividing by the pair locator is the same scalar times the quotient
  locator.
- **How it is useful:** Shows the determinant gate and two-root quotient form
  are equivalent normalizations of the same endpoint object.
- **What to do next:** Use whichever normalization is more convenient when
  charging the remaining b=2 good-pair ledger globally.

### 2026-06-28 - M1 b=2 quotient roots are determinant-gate roots

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that after fixing a `b=2` good pair, the
  remaining quotient roots are exactly the roots of a `3 x 3` determinant gate
  built from the origin locator and the two residual directions.
- **How it is useful:** Turns the lower-width split test into an explicit
  one-variable determinant condition, giving a sharper target for the remaining
  M1 good-pair ledger.
- **What to do next:** Bound or classify these determinant gates using
  fixed-root, quotient-periodic, tangent, or aperiodic residue-line input.

### 2026-06-28 - M1 b=2 good-pair images descend by two roots

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that every interpolated good-pair locator
  factors as `ell_e M_e`, where `M_e` is a degree-`q-2` quotient satisfying the
  absorbed fixed-divisor Hankel identity.
- **How it is useful:** Reduces the remaining `b=2` split-image test to a
  two-root absorbed quotient-locator problem of width `q-2`.
- **What to do next:** Use this lower-width quotient form to connect the
  good-pair endpoint with fixed-root, quotient-periodic, and aperiodic M1
  ledgers.

### 2026-06-28 - M1 b=2 split-image fibers are good-pair sets

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that the preimage of a `b=2` residual support
  under the split-good-pair interpolation map is exactly the set of good pairs
  contained in that support.
- **How it is useful:** Gives an exact weighted good-pair ledger
  `|I|=sum_R g(R)` for the remaining `b=2` branch.
- **What to do next:** Use this weighted split-image form to charge the global
  good-pair image in the all-line M1 residue-packing argument.

### 2026-06-28 - M1 b=2 fibers are split good-pair images

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that a `b=2` fixed-anchor residual fiber is
  exactly the set of good-pair interpolation locators that split into `q`
  distinct available roots.
- **How it is useful:** Replaces residual `q`-subset enumeration by a two-root
  interpolation and split-locator image, sharpening the remaining M1 good-pair
  ledger.
- **What to do next:** Study the split-locator image condition globally and
  charge its good-pair domain in the all-line residue-packing argument.

### 2026-06-28 - M1 b=2 good pairs interpolate residual locators

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that after the zero-good branch is eliminated,
  every `b=2` residual support is reconstructed from any contained good pair by
  solving a `2 x 2` interpolation system in the residual direction basis.
- **How it is useful:** Turns the remaining `b=2` fixed-anchor fiber into an
  explicit image of the good-pair ledger, rather than a nonconstructive count.
- **What to do next:** Use the good-pair interpolation image to charge the
  remaining global `b=2` ledger in the M1 residue-line packing argument.

### 2026-06-28 - M1 b=2 degree gap eliminates zero-good supports

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that in a genuine `b=2` residual direction
  space, every base-plus-projective-fiber shadow is the zero set of a nonzero
  degree-`<q` direction, so no zero-good `q`-support exists.
- **How it is useful:** Closes the zero-good branch of the `b=2` fixed-anchor
  residual problem and sharpens the closure to `|F(U,W)|<=G_tot`.
- **What to do next:** Charge the remaining good-pair ledger globally in the
  M1 residue-line packing argument.

### 2026-06-28 - M1 b=2 half-certificate completions are local

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Refines the `b=2` zero-good half-certificate bound:
  base certificates complete only inside the base locus plus one projective
  fiber, and fiber certificates complete only inside that fiber plus the base.
- **How it is useful:** Removes the artificial all-domain completion factor
  from the zero-good ledger and keeps the remaining M1 obstruction attached to
  local root-shadow slices.
- **What to do next:** Bound the local base and fiber shadow ledgers by
  quotient-periodic, tangent, fixed-root, or aperiodic residue-packing input.

### 2026-06-28 - M1 b=2 zero-good supports are half-certificate incidences

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that the `b=2` zero-good envelope is bounded
  by `H_c binom(N-c,q-c)`, where `c=ceil(q/2)` and `H_c` counts `c`-subsets in
  the base locus or one projective fiber.
- **How it is useful:** Rewrites the remaining zero-good fixed-anchor term as a
  half-width fixed-divisor certificate count times residual completions.
- **What to do next:** Bound the half-certificate ledger by quotient-periodic,
  tangent, fixed-root, or aperiodic residue-packing estimates.

### 2026-06-28 - M1 b=2 zero-good envelope closes fixed anchors

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Gives an explicit zero-good envelope
  `Z_0^{env}` for `b=2` fixed-anchor fibers and proves
  `|F(U,W)|<=G_tot+Z_0^{env}`.
- **How it is useful:** Converts the `b=2` residual fiber into a good-pair
  packing term plus a concrete half-width certificate envelope.
- **What to do next:** Bound the zero-good envelope by quotient-periodic,
  tangent, fixed-root, or aperiodic half-width certificate ledgers.

### 2026-06-28 - M1 b=2 zero-good supports carry certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that every `b=2` residual support with zero
  cross-fiber good pairs is half-heavy in the base locus or in one projective
  fiber, and therefore carries a support-local half-width quotient-kernel
  certificate.
- **How it is useful:** Splits the fixed-anchor fiber into a packable part
  (`g(R)>0`) and an explicit certified part, eliminating diffuse zero-good
  residual supports from the remaining M1 obstruction.
- **What to do next:** Count or charge the resulting half-width certificates
  against quotient-periodic, tangent, fixed-root, or aperiodic ledgers.

### 2026-06-28 - M1 b=2 half-height base loci descend the pencil

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that if the `b=2` base locus has height
  `h>=q/2`, then the whole residual direction pencil factors as
  `V(U,W)=ell_{B_0}V'` with `dim V'=2` and degree width `<q-h<=q/2`, while the
  projective evaluation map is unchanged off the base locus.
- **How it is useful:** Separates the half-height survivor into a lower-width
  quotient-pencil descent for large base loci and a single short quotient
  direction for large non-base fibers.
- **What to do next:** Bound the descended quotient pencils or classify the
  remaining half-height non-base fiber directions.

### 2026-06-28 - M1 b=2 half-height shadows give short quotient kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Shows that any b=2 root shadow of height
  `h>=q/2` gives a fixed-divisor quotient kernel
  `H_{q,q+d-h}(s)(ell_W ell_S R_S)=0` with quotient degree `<q-h<=q/2`.
- **How it is useful:** Converts the only branch not closed by good-pair
  packing into a concrete half-width Hankel-kernel certificate.
- **What to do next:** Bound or classify these half-width quotient kernels
  using quotient-periodic, tangent, fixed-root, or aperiodic M1 ledgers.

### 2026-06-28 - M1 b=2 small root shadows force packing

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves a root-shadow-height packing bound for the
  `b=2` residual branch: if the largest base locus or projective fiber has
  height `h`, then every residual support has at least `gamma_2(q,h)`
  cross-fiber good pairs, giving `|F(U,W)|<=floor(G_tot/gamma_2(q,h))` when
  this lower bound is positive.
- **How it is useful:** Shows that the only `b=2` branch not closed by
  good-pair packing requires a fixed-divisor slice of height at least `q/2`,
  turning the remaining obstruction into a large root-shadow ledger.
- **What to do next:** Bound or classify half-size fixed-divisor root shadows
  in the actual M1 Hankel-pencil kernels.

### 2026-06-28 - M1 b=2 concentration gives fixed-divisor slices

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Identifies the two b=2 concentration alternatives
  as fixed-divisor slice ledgers: base-locus roots are common zeros of the
  residual direction space, and a projective fiber `[a:b]` is cut out by the
  nonzero direction `bP-aQ`.
- **How it is useful:** Removes concentration as a separate residual-kernel
  obstruction and routes it to the existing fixed-root, quotient-periodic, and
  aperiodic M1 slice ledgers.
- **What to do next:** Bound the fixed-divisor base and projective-fiber slice
  ledgers strongly enough to close the b=2 packing branch.

### 2026-06-28 - M1 b=2 good pairs force concentration alternatives

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Gives an exact support-level formula for the number
  of good cross-fiber pairs in a `b=2` residual support and a lower bound in
  terms of maximum base-locus occupancy and maximum projective-fiber occupancy.
- **How it is useful:** Shows that failure of the b=2 good-pair packing bound
  forces concentration in the base locus or in a small number of projective
  fibers, isolating the next fixed-root/quotient/aperiodic obstruction.
- **What to do next:** Prove base-occupancy and fiber-occupancy bounds for
  actual M1 fixed-divisor residual supports.

### 2026-06-28 - M1 cross-fiber good pairs pack b=2 residual supports

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** For residual direction dimension `2`, proves that
  good cross-fiber pairs are used by at most one residual support, yielding
  `|F(U,W)| <= floor(G_tot/g_min)` whenever each residual support contains at
  least `g_min>0` good pairs.
- **How it is useful:** Gives a sharper packing bound than the raw bad-pair
  DMB ledger when residual supports are not concentrated in the base locus or a
  single projective fiber.  Concentration is thereby isolated as the next
  fixed-root/quotient/aperiodic obstruction.
- **What to do next:** Bound base occupancy and projective-fiber occupancy for
  actual M1 residual supports.

### 2026-06-28 - M1 higher residual direction equals persistent one-root

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that `b(U,W)>=2` makes every available root
  one-root-bad, so for produced anchors in the usual `|F|>q-1` range the
  one-root absorbed pencil is persistent exactly when `b(U,W)>=2`.
- **How it is useful:** Collapses the remaining one-root persistent branch and
  the higher-dimensional residual-direction branch into the same object.  This
  removes a bookkeeping split from the fixed-anchor M1 residual route.
- **What to do next:** Work on the first surviving case `b(U,W)=2` by bounding
  projective evaluation fibers and separating quotient-periodic from aperiodic
  fibers.

### 2026-06-28 - M1 projective fibers give exact bad-pair counts

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** For residual direction dimension `2`, derives the
  exact bad-pair count from the projective evaluation base locus and fiber
  sizes, and records the max-fiber envelope for `|Z_2^{dir}|`.
- **How it is useful:** Converts the first higher-dimensional residual bad
  ledger into a concrete rational-fiber counting problem.  Base-free injectivity
  gives direction-MDS, while bounded projective fibers give a linear bad-pair
  ledger outside the base locus.
- **What to do next:** Prove projective fiber-size bounds for the actual
  fixed-divisor M1 direction spaces, separating quotient-periodic fibers from
  aperiodic fibers.

### 2026-06-28 - M1 two-dimensional residual directions are projective fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** For residual direction dimension `2`, identifies
  bad pairs exactly as common-zero base points plus equal-value fibers of the
  projective evaluation map `x -> [P(x):Q(x)]` for a basis `P,Q` of
  `Dir K(U,W)`.
- **How it is useful:** Turns the first genuinely higher-dimensional persistent
  branch into a rational-fiber packing problem.  This is the form that can be
  attacked by quotient-periodic, fixed-root, tangent, or aperiodic fiber
  bounds.
- **What to do next:** Bound the projective evaluation fibers for actual M1
  fixed-divisor residual direction spaces, or classify their quotient-periodic
  components.

### 2026-06-28 - M1 persistent one-root pencils force higher direction

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Shows that, when full-field probing certifies a
  genuinely persistent one-root absorbed pencil, a produced deficit anchor has
  endpoint defect and residual direction dimension at least `2`.
- **How it is useful:** Rules out the line-kernel case for the remaining
  persistent one-root obstruction.  After the finite branch is closed, the only
  surviving one-root absorbed obstruction must be a genuinely
  higher-dimensional fixed-divisor residual direction space.
- **What to do next:** Classify persistent moving-kernel certificates with
  `b(U,W)>=2`, or charge them to quotient-periodic, tangent, or aperiodic M1
  structure.

### 2026-06-28 - M1 nonpersistent one-root pencils close higher bad ledgers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Combines the one-root envelope with the
  finite/persistent absorbed-pencil dichotomy: in the nonpersistent branch
  `|Z_1(U,W)|<=q-1`, hence `|Z_b^{dir}(U,W)|<=binom(q-1,b)` and the DMB
  residual-fiber bound has a field-size-free bad-subset term.
- **How it is useful:** Shows that higher-dimensional direction-MDS bad ledgers
  are closed once the one-root absorbed pencil is finite.  The remaining
  obstruction is the persistent one-root moving-kernel branch already linked to
  endpoint/residual-direction defects.
- **What to do next:** Classify or exclude persistent one-root absorbed pencils
  using quotient-periodic, tangent, and aperiodic M1 structure.

### 2026-06-28 - M1 higher bad subsets charge to one-root slices

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that every direction-bad `b`-subset is
  contained in the one-root bad-slice set `Z_1(U,W)`, hence
  `|Z_b^{dir}(U,W)| <= binom(|Z_1(U,W)|,b)`.
- **How it is useful:** Charges higher-dimensional direction-MDS bad ledgers to
  the existing one-root fixed-root/absorbed-rank ledger.  If the one-root bad
  set has size `<b`, the direction-MDS packing bound applies automatically.
- **What to do next:** Bound the one-root absorbed-rank defects after
  quotient-periodic, tangent, and aperiodic charges; the higher bad-subset
  ledgers then follow from this envelope.

### 2026-06-28 - M1 bounded residual direction has projective root closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Combines the projective-shadow formula with the
  elementary root bound for nonzero degree-`<q` directions to prove
  `|Z_b^{dir}| <= ((|F|^b-1)/(|F|-1)) binom(min(N,q-1),b)`, and records the
  resulting explicit DMB closure bound.
- **How it is useful:** Shows that fixed anchors with bounded residual
  direction dimension are polynomially controlled in the polynomial-field
  window, reducing the residual M1 task to controlling the frequency of such
  fixed-divisor kernels and classifying unbounded or persistent direction
  families.
- **What to do next:** Sharpen the coarse projective root-count ledger for
  actual M1 fixed-divisor kernels, or prove structural exclusions for
  high-dimensional residual direction spaces.

### 2026-06-28 - M1 bad direction subsets are absorbed multi-root defects

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that a bad `b`-subset in the direction-MDS
  residual-kernel theorem is equivalently a rank defect of the absorbed
  multi-root matrix `A_C(U,W)` built from the fixed divisor `ell_W ell_C`.
- **How it is useful:** Identifies the evaluation-rank, projective-root-shadow,
  and fixed-divisor Hankel descriptions of the DMB bad-set term.  This makes the
  residual obstruction directly usable by fixed-root, quotient-periodic, and
  aperiodic M1 ledgers.
- **What to do next:** Use the absorbed multi-root matrices to bound or
  classify projective direction root shadows for positive-dimensional residual
  anchors.

### 2026-06-28 - M1 bad direction subsets are projective root shadows

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Identifies the bad `b`-subsets in the
  direction-MDS residual-kernel theorem exactly as projective root shadows:
  `Z_b^{dir}(U,W)=union_[Q in P(V(U,W))] {C subset Z_{D'}(Q): |C|=b}`.
- **How it is useful:** Turns the DMB bad-set term from an abstract
  evaluation-rank defect count into a projective fixed-divisor root-count
  ledger, matching the fixed-root, quotient-periodic, and aperiodic charges
  needed for the M1 all-line residue-packing target.
- **What to do next:** Bound the projective direction root shadows arising from
  M1 residual anchors using fixed-divisor short-kernel structure.

### 2026-06-28 - M1 direction-MDS residual kernels give b-packings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** For residual direction dimension `b`, identifies
  bad `b`-subsets as evaluation-rank defects of `Dir K(U,W)` and proves the
  packing bound
  `|F(U,W)| binom(q,b) <= binom(N,b)-|Z_b|+|Z_b| binom(N-b,q-b)`.
- **How it is useful:** Generalizes the line-kernel result to higher residual
  direction spaces.  In the direction-MDS case it gives the sharper
  `floor(binom(N,b)/binom(q,b))` bound, and otherwise it charges the obstruction
  to explicit fixed-divisor `b`-root slices.
- **What to do next:** Prove direction-MDS behavior, or bounded bad-subset
  ledgers, for the fixed-divisor residual direction spaces arising in M1 after
  quotient-periodic and tangent charges.

### 2026-06-28 - M1 line residual kernels are root-slice packings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Proves that if a fixed deficit anchor has residual
  direction dimension `b(U,W)=1`, then the unique direction polynomial `Q`
  contains every possible overlap root between two residual supports, yielding
  `|F(U,W)| <= floor((|D'|-z)/(q-z))` with `z=|{x in D':Q(x)=0}|`.
- **How it is useful:** Sharpens the first positive-dimensional residual-kernel
  obstruction from a coarse hyperplane-arrangement count to an explicit
  root-slice packing.  Dimension-one residual kernels are therefore charged by
  the fixed-root/root-slice ledger, not treated as unstructured multiplicity.
- **What to do next:** Extend this root-slice stratification from `b=1` to
  higher-dimensional residual direction spaces, or classify the higher
  directions via quotient-periodic and aperiodic M1 structure.

### 2026-06-28 - M1 endpoint defects are residual directions

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Shows that the endpoint matrix forced by a
  persistent absorbed moving kernel is the first `q-1` columns of the residual
  moment matrix, so endpoint nullity is at most the residual-kernel direction
  dimension.
- **How it is useful:** Collapses persistent absorbed-rank pencils into the
  already named fixed-divisor residual direction ledger: a persistent absorbed
  defect forces `b(U,W)>0`, so there is no independent moving-kernel branch once
  positive-dimensional residual kernels are charged.
- **What to do next:** Bound or classify positive-dimensional fixed-divisor
  residual kernels via fixed-root, quotient-periodic, tangent, or aperiodic M1
  structure.

### 2026-06-28 - M1 moving kernels force endpoint ranks

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / AUDIT.
- **What is being added:** Expands a persistent moving-kernel certificate
  `Q_z(X)=sum z^m R_m(X)` into a coefficient ladder and shows that its top
  coefficient is a nonzero kernel of the endpoint map
  `R -> H_{q,q+d-1}(s)(ell_W R)`.
- **How it is useful:** Gives a simple rank test that rules out the persistent
  absorbed-rank branch for any fixed deficit anchor; the verifier now records
  this endpoint-rank audit for produced anchors.
- **What to do next:** Classify anchors where the endpoint map is not full
  column rank, or prove such endpoint defects are already charged by the
  fixed-root, tangent, or quotient-periodic M1 ledgers.

### 2026-06-28 - M1 persistent absorbed defects have moving kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL.
- **What is being added:** Shows that a persistent absorbed-rank defect is
  equivalent to a bounded-degree moving kernel
  `Q_z(X)` satisfying `H_{q,q+d-1}(s)(ell_W (X-z) Q_z)=0` identically.
- **How it is useful:** Turns the persistent low-rank pencil branch into a
  finite certificate object.  The remaining residual obstruction can now be
  attacked by classifying bounded-degree moving denominators.
- **What to do next:** Prove that such moving kernels are quotient-periodic,
  fixed-root/tangent, or aperiodically sparse after the existing M1 charges.

### 2026-06-28 - M1 absorbed-rank defects are finite or persistent

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL.
- **What is being added:** Proves that for each fixed deficit anchor, the
  absorbed bad-root set either has size at most `q-1`, or all maximal minors
  of the affine absorbed Hankel pencil vanish identically.
- **How it is useful:** Converts the absorbed-rank defect ledger into a finite
  exceptional-root term plus one named persistent low-rank pencil obstruction.
  Nonpersistent anchors are therefore polynomially packing-bounded.
- **What to do next:** Classify or charge persistent absorbed-rank pencils to
  quotient-periodic, fixed-root, tangent, or aperiodic M1 ledgers.

### 2026-06-28 - M1 absorbed-rank defects bound residual fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves a fixed-anchor closure bound in terms of
  absorbed-rank defect roots:
  `|F(U,W)| <= floor(((N-z)+z binom(N-1,q-1))/q)`.
- **How it is useful:** Converts the residual-fiber problem into a packing
  term plus a weighted absorbed-rank-defect ledger.  If absorbed defects are
  absent or polynomially charged, residual completions are controlled.
- **What to do next:** Bound the total absorbed-rank defect ledger across
  anchors after quotient-periodic, fixed-root, and aperiodic charges.

### 2026-06-28 - M1 bad residual root slices are absorbed-rank defects

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Identifies the bad one-root residual-slice test
  with failure of full column rank for the absorbed-anchor matrix
  `A_x(U,W)=(h^{W,x}_{i+j})_{0<=i<q,0<=j<q-1}`.
- **How it is useful:** Replaces the remaining bad-root condition by a
  concrete one-extra-row filtered Hankel rank test.  If every absorbed root has
  full column rank, same-anchor residual completions are pairwise disjoint.
- **What to do next:** Prove uniform full-column-rank criteria after
  quotient-periodic and fixed-root charges, or classify the absorbed-rank
  defects as the next residual obstruction.

### 2026-06-28 - M1 residual collisions charge to root slices

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves that two residual completions over the same
  deficit anchor differ by a lower-degree residual-kernel direction, and any
  shared residual root forces a one-root divisible short-kernel slice.
- **How it is useful:** Turns same-anchor residual overlap into explicit
  fixed-root charges.  After bad root slices are charged, residual supports
  satisfy an elementary packing bound rather than creating uncontrolled
  completion multiplicity.
- **What to do next:** Bound the bad root-slice sets uniformly, or show they
  are already covered by the fixed-root/root-slice M1 ledger.

### 2026-06-28 - M1 residual kernels are divisible short kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves the convolution identity
  `H_{q,q}(h^W)Q = H_{q,q+d}(s)(ell_W Q)`, identifying filtered residual
  kernels with short Hankel kernels divisible by the anchor locator.
- **How it is useful:** Converts positive-dimensional residual-kernel fibers
  into fixed-divisor short-kernel directions, so any remaining high-rank
  deficit-anchor obstruction can be charged to fixed-root, quotient-periodic,
  or aperiodic ledgers rather than treated as new multiplicity.
- **What to do next:** Classify or bound the fixed-divisor short-kernel
  directions that survive the existing root-slice and quotient charges.

### 2026-06-28 - M1 residual kernel dimension bounds anchors

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves an arrangement bound for fixed deficit
  anchors: if the filtered monic residual-kernel space has direction
  dimension `b`, then its squarefree residual supports are bounded by
  `sum_{i<=b} binom(|D'|,i)`.
- **How it is useful:** Turns the short-core residual into a rank/dimension
  ledger.  Bounded residual-kernel dimension gives polynomial completion
  counts for each deficit anchor.
- **What to do next:** Prove rank lower bounds or charge high-dimensional
  filtered kernels to quotient-periodic, tangent, root-slice, or aperiodic
  ledgers.

### 2026-06-28 - M1 deficit anchors are residual Hankel kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Shows that a deficit anchor `(U,W)` converts the
  short-core residual to an ordinary filtered Hankel-kernel problem: with
  `q=tau+|U|`, the remaining marked locator is the unique monic degree-`q`
  annihilator of `H_{q,q}(H_{2q,d}(s)ell_W)`.
- **How it is useful:** Replaces the remaining short-core ledger by a
  concrete count of anchors whose filtered sequences have admissible
  squarefree kernel locators disjoint from the anchor.
- **What to do next:** Bound these filtered-kernel anchors using quotient,
  tangent, root-slice, or aperiodic residue-line structure.

### 2026-06-28 - M1 deficit anchors reconstruct short-core fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Shows that for deficit
  `d=r-tau-|U|>0`, a fixed canonical core `U` plus any `d` marked roots
  reconstructs the whole marked frontier by applying the anchor locator and
  using a `2(r-d)`-moment Prony recovery.
- **How it is useful:** Turns the moment-short packing bound into an explicit
  deficit-anchor injection, giving a concrete object to count in the
  remaining M1 short-core ledger.
- **What to do next:** Bound admissible deficit anchors after
  quotient-periodic, tangent, and endpoint charges.

### 2026-06-28 - M1 deficit-weighted core closure criterion

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL.
- **What is being added:** Extends the canonical core closure criterion from
  the `|M(S)|<=tau+1` boundary range to all marked-frontier sizes by summing
  the deficit-packing fiber bound
  `floor(binom(n-|U|,d)/binom(r,d))` over `Core_r(s)`.
- **How it is useful:** Rephrases the remaining split-support M1 obstruction
  as a deficit-weighted canonical core ledger problem, so repeated marked
  frontiers over one core are no longer an uncontrolled source.
- **What to do next:** Bound the weighted `Core_r(s)` ledgers after
  quotient-periodic, tangent, and empty-core endpoint charges.

### 2026-06-28 - M1 moment-short fibers are deficit packings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves that if a fixed canonical core `U` has
  marked count `r` and deficit `d=r-tau-|U|>0`, then two distinct marked
  frontiers over `U` have intersection `< d`.  Hence the fiber is bounded by
  `floor(binom(n-|U|,d)/binom(r,d))`.
- **How it is useful:** Unifies moment-complete uniqueness and boundary
  matching, and shows the remaining short-core obstruction is a controlled
  packing ledger rather than arbitrary same-core branching.
- **What to do next:** Use the deficit-packing bound to formulate global
  core-count closure criteria for high-frontier M1 supports.

### 2026-06-28 - M1 moment-complete cores are support-unique

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves that a canonical unmarked core `U` with
  `r` marked exits has a unique marked frontier whenever
  `|U| >= max(0,r-tau)`.  Mixed marked/unmarked faces supply at least `2r`
  moments, so Prony uniqueness recovers the marked locator.
- **How it is useful:** Reduces possible same-core branching with many marked
  exits to moment-short cores satisfying `|U| < r-tau`, isolating the
  remaining large-frontier obstruction for M1.
- **What to do next:** Analyze or charge the moment-short core regime after
  quotient-periodic, tangent, and empty-core endpoint ledgers are removed.

### 2026-06-28 - M1 empty-core endpoint is the boundary moment map

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Identifies the only remaining boundary exception:
  empty-core full-marked supports are exactly nonzero boundary sparse-moment
  representations.  General fibers are matchings, and full-domain nontrivial
  fibers are root-linear complement pairs.
- **How it is useful:** Completes the canonical-core boundary analysis:
  nonempty cores are support-unique and the empty core is a known endpoint
  ledger, rather than a new M1 packet mechanism.
- **What to do next:** Use this endpoint classification when comparing the
  canonical-core ledger against quotient-periodic and aperiodic M1 bounds.

### 2026-06-28 - M1 nonempty boundary cores are support-unique

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Uses the canonical-core simple-pole lift to show
  that the boundary marked count `r=tau+1` has unique marked support over
  every nonempty unmarked core.  Matching ambiguity remains only for the empty
  core endpoint.
- **How it is useful:** Sharpens the canonical-core closure criterion: the
  boundary no longer contributes a matching factor over every core, reducing
  the split-support branch to core counts plus one full-marked endpoint.
- **What to do next:** Attack the remaining empty-core full-marked endpoint
  and prove polynomial bounds for the nonempty canonical core ledgers.

### 2026-06-28 - M1 canonical cores have simple-pole packet lifts

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For a canonical unmarked core `U` with marked
  exits `M`, the full marked face is one sparse packet, and every unmarked
  root `u in U` gives the same packet with amplitudes divided by `y-u` and
  one extra visible row.  The verifier audits these packet and simple-pole
  lift identities.
- **How it is useful:** Refines the `Core_r(s)` closure target: canonical
  cores are simultaneous simple-pole packet-lift supports, which is closer to
  the quotient-periodic/aperiodic residue-packing input needed for M1.
- **What to do next:** Bound or classify supports admitting many compatible
  simple-pole lifts after quotient-periodic and tangent cores are charged.

### 2026-06-28 - M1 split-support closes under canonical core counts

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE.
- **What is being added:** Adds a canonical core closure criterion: the number
  of split-support certificates with marked frontier size at most `tau+1` is
  bounded by the canonical unmarked core ledgers, with uniqueness below the
  boundary and matching-bounded fibers at the boundary.
- **How it is useful:** Turns the two-color normal form into a summable M1
  target.  Once canonical unmarked cores are charged to lower-core,
  quotient-periodic, tangent, or aperiodic ledgers, this split-support branch
  is polynomial for fixed `tau`.
- **What to do next:** Prove or falsify polynomial bounds for the canonical
  core ledgers `Core_r(s)`, and separately look for active supports with more
  than `tau+1` marked exits.

### 2026-06-28 - M1 split-support faces have two-color normal form

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / DERIVED FROM EXACT FINITE AUDIT.
- **What is being added:** Packages the marked and unmarked cube lemmas into
  a complete two-color face classification: faces deleting no marked exits are
  zero, while faces deleting marked exits are forced nonzero sparse packets
  after an additive row shift.
- **How it is useful:** Makes the internal split-support recursion explicit:
  there is no third hidden face type and no repeated packing problem along
  unmarked deletion chains.
- **What to do next:** Use this normal form to bound canonical unmarked cores
  carrying large marked frontiers, or to charge such cores to lower-core,
  quotient-periodic, tangent, or aperiodic ledgers.

### 2026-06-28 - M1 unmarked deletion preserves marked frontier

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** If `E subset U(S)` is deleted from an active
  split support, the shifted active support `S\E` has the same marked exits
  `M(S)`, with scalars rescaled by `1/ell_E(y)`.
- **How it is useful:** Gives the exact local additivity invariant: unmarked
  deletion consumes row depth but does not create a new marked-frontier problem
  at each rung.
- **What to do next:** Use this invariant to turn long unmarked-deletion
  chains into one lower-core/root-slice charge plus the preserved marked
  sparse-packet frontier.

### 2026-06-28 - M1 mixed marked-unmarked faces are lossless

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For `E subset U(S)` and `Y subset M(S)`, deleting
  the unmarked roots `E` shifts the row depth by `|E|` and rescales marked
  packet amplitudes by `1/ell_E(y)`, with no loss of nonzero marked faces.
- **How it is useful:** Unifies the nonzero marked-exit cube and zero
  unmarked-root cube into a two-color additive-depth object, matching the M1
  goal of avoiding multiplicative frontier loss.
- **What to do next:** Use the two-color cube normal form to bound canonical
  unmarked cores carrying many marked exits, or charge them to lower-core,
  tangent, quotient-periodic, or aperiodic ledgers.

### 2026-06-28 - M1 unmarked roots form zero descent cubes

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For an active total split support `S`, every
  nonempty subset of unmarked roots `E subset U(S)` satisfies the deeper zero
  relation `H_{tau+|E|}(s)ell_{S\E}=0`.
- **How it is useful:** Splits active supports into a nonzero marked-exit
  packet cube and a zero unmarked-root descent cube, giving a direct
  lower-core/root-slice charge for unmarked mass.
- **What to do next:** Bound the remaining canonical unmarked cores carrying
  large marked-exit cubes after these zero descents are charged.

### 2026-06-28 - M1 canonical marked-core fibers are matching-bounded

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** After deleting all marked exits from an active
  total split support, the canonical unmarked core has unique full marked
  support below the boundary and matching-bounded fibers at the boundary.
- **How it is useful:** Removes another possible multiplicity source:
  repeated marked-exit cubes over one unmarked core cannot form overlapping
  clusters.
- **What to do next:** Bound how many canonical unmarked cores can carry
  large marked-exit cubes after quotient-periodic, tangent, and lower-core
  charges.

### 2026-06-28 - M1 marked exits form lossless cubes

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For a fixed active total split support `S`, every
  nonempty subset of the marked exits `M(S)` gives a forced nonzero sparse
  packet face over the complementary anchor.
- **How it is useful:** Replaces many-anchor ambiguity by a canonical
  zero-free marked-exit cube, making large marked-exit supports the next
  explicit M1 object to bound or classify.
- **What to do next:** Prove quotient-periodic, tangent, lower-core, or
  aperiodic restrictions on active supports that carry large marked-exit
  cubes.

### 2026-06-28 - M1 total split-support marked-exit factorization

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For a fixed active total split support `S`,
  split-support certificates of mode size `m` are exactly `m`-subsets of the
  nonzero root-marked exits `M(S)`, with forced Lagrange amplitudes.
- **How it is useful:** Converts internal anchor/mode multiplicity into the
  concrete task of bounding active supports with many marked exits.
- **What to do next:** Bound or classify large marked-exit active supports
  through quotient-periodic, tangent, lower-core, or aperiodic packing input.

### 2026-06-28 - M1 fixed-anchor split-support fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** For a fixed collapsed anchor `A`, split-support
  certificates are sparse representations of one fixed moment vector.  They
  are unique for `m<=tau`, and boundary fibers have matching size at most
  `floor((n-|A|)/m)`.
- **How it is useful:** Removes fixed-anchor multiplicity from the global M1
  production problem except for the already matching-type boundary endpoint.
- **What to do next:** Bound the remaining number of anchor bases carrying
  certificates, or classify large anchor families as quotient-periodic,
  tangent, or lower-core.

### 2026-06-28 - M1 split-support packet equivalence

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Completes the converse direction: an active split
  support `A union Y` with nonzero root-marked boundaries on every selected
  mode reconstructs the sparse anchor-base packet by the Lagrange formula.
- **How it is useful:** Turns the split-support certificate into an exact
  equivalence, giving a direct M1 target independent of deletion-tree
  presentation.
- **What to do next:** Bound the number of equivalent split-support
  certificates, or classify large families as quotient-periodic, tangent, or
  lower-core.

### 2026-06-28 - M1 split-support zero-free mode cubes

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Derives from partial absorption that every ordering
  of the packet mode set is zero-free inside the collapsed split-support
  chart, so a size-`m` split-support packet contains exactly `m!` intrinsic
  ordered mode flags.
- **How it is useful:** Makes the internal cube structure of a split-support
  packet explicit while keeping it separate from original deletion-tree
  multiplicity; the only zero vertex is full absorption.
- **What to do next:** Use this finite internal cube to separate bounded
  mode-order multiplicity from the global problem of counting split-support
  certificates.

### 2026-06-28 - M1 split-support partial absorption

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves that absorbing any subset `E` of packet
  modes into the anchor gives the predicted smaller sparse packet on
  `Y\E`; proper absorptions remain nonzero and full absorption is the active
  split-support equation.
- **How it is useful:** Gives an induction-ready split-support object for M1:
  modes can be moved into the anchor without leaving the packet category or
  creating hidden zero collapses.
- **What to do next:** Use the partial-absorption structure to bound families
  of split-support certificates, especially by charging large families to
  quotient-periodic, tangent, or lower-core kernels.

### 2026-06-28 - M1 anchor-base packets are split-support certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Proves the converse anchor-base packet statement:
  a sparse moment packet `H_{tau+m,|A|}(s)ell_A=sum_y a_y y^i` with nonzero
  amplitudes makes `A union Y` active, and every `y in Y` is a nonzero
  root-marked split boundary.
- **How it is useful:** Replaces deletion-tree language by an intrinsic
  split-support certificate.  Terminal packet production can now be attacked
  as a direct M1 packing problem over split supports `A union Y`.
- **What to do next:** Bound the number of such split-support certificates,
  or prove that large families force quotient-periodic, tangent, or lower-core
  structure.

### 2026-06-28 - M1 anchor-base exchange-distance charges

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Refines the anchor-base kernel drop by exchange
  distance: if `A=I union U` and `A'=I union V`, then
  `ell_A-ell_A'=ell_I(ell_U-ell_V)` with `deg(ell_U-ell_V)<|U|`.  The
  one-exchange case forces the common anchor core itself into the Hankel
  kernel.  In the largest `F_7^*` audit, all `30240` one-exchange common-core
  checks have no kernel hit, including all `28080` productive checks.
- **How it is useful:** Charges adjacent collapsed-anchor production
  collisions to lower-core Hankel kernels, and identifies higher exchange
  collisions as bounded-degree balanced-difference kernel events over a common
  anchor core.
- **What to do next:** Bound the bounded-degree balanced-difference kernel
  events, starting with whether their split support forces quotient-periodic
  or tangent structure.

### 2026-06-28 - M1 anchor-base kernel drop for packet collisions

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Collapses a terminal branch anchor to
  `A=X union R` and proves that the visible packet equals
  `H_{tau+m,|A|}(s) ell_A`.  Distinct collapsed anchor bases producing the
  same visible moment sequence therefore give a nonzero lower-degree Hankel
  kernel vector `ell_A-ell_A'`.
- **How it is useful:** Moves genuine repeated production across distinct
  anchor bases into a lower-degree kernel ledger, separating it from same
  collapsed-anchor ordering multiplicity and the already isolated boundary
  disjoint-alias ledger.
- **What to do next:** Bound these lower-degree locator-difference kernels or
  show that their split-anchor points force quotient-periodic, tangent, or
  lower-core structure.

### 2026-06-28 - M1 visible packet production fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** STRUCTURAL / EXACT FINITE AUDIT.
- **What is being added:** Classifies visible terminal-packet collisions as
  same-support scalar-cut equalities, except for the already isolated maximal
  boundary disjoint-alias scalar fit.  The verifier now counts, syndrome by
  syndrome, the production fibers of unanchored visible sparse-packet labels;
  in the largest `F_7^*` audit all `34560` visible productions, including all
  `32400` productive productions, are singleton fibers.
- **How it is useful:** Turns the remaining repeated-production problem into
  a concrete scalar-collision target across distinct anchors, with boundary
  aliases separated into their own ledger.
- **What to do next:** Use the scalar-cut collision form to bound repeated
  production across anchors, or prove that surviving collisions force
  quotient-periodic, tangent, or lower-core structure.

### 2026-06-28 - M1 anchored packets reconstruct branch data

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Shows that for a fixed lower-core anchor `(X,R)`,
  a terminal packet label `(R,Y,(a_y))` reconstructs the branch core
  `C=R union Y` and the first-row exit scalars
  `c_X(y;C)=a_y prod_{z!=y}(y-z)`.
- **How it is useful:** Localizes the remaining repeated-production problem:
  multiplicity cannot come from ambiguity at one anchor, so repeated labels
  must arise from different anchors or global relations between anchors.
- **What to do next:** Bound or classify repeated production across distinct
  anchors, especially cases forcing quotient-periodic, tangent, or lower-core
  structure.

### 2026-06-28 - M1 visible terminal packet-type ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Combines the `2m`-moment recovery theorem with the
  boundary matching-fiber ledger to show that visible terminal branch packet
  labels at row level `tau` lie in an ambient space of size
  `sum_{m=2}^{tau+1} (q-1)^m binom(n,m)`.
- **How it is useful:** Gives a polynomial packet-type ledger for fixed
  `tau` and polynomial field size after terminal branching has been reduced to
  visible sparse packets, while preserving the separate obligation to bound
  repeated production of packet labels by deletion trees.
- **What to do next:** Attack repeated production: show that many occurrences
  of the same packet force quotient-periodic, tangent, or lower-core
  structure, or add an explicit multiplicity ledger.

### 2026-06-28 - M1 boundary packet endpoint ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Combines the boundary fiber matching bound with the
  labeled packet count: the nonzero `m`-mode boundary packet family has
  `(q-1)^m binom(n,m)` labels and fibers of size at most `floor(n/m)`.
- **How it is useful:** Gives the terminal sparse-packet endpoint a local
  polynomial ledger for fixed `m=tau+1` in the polynomial-field window, while
  keeping clear that global M1 still needs to control how deletion trees
  produce these packets.
- **What to do next:** Feed this endpoint ledger into the terminal deletion
  tree accounting and separate repeated production of the same visible packet
  from genuinely new boundary packet labels.

### 2026-06-28 - M1 boundary fibers are matchings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that in the `2m-1` boundary moment map, all
  supports inside one fiber are pairwise disjoint; hence every fiber has size
  at most `floor(n/m)`.
- **How it is useful:** Shows boundary ambiguity is matching-type rather than
  an overlapping support cluster, giving a general non-multiplicative endpoint
  ledger even away from the full-domain `n=2m` case.
- **What to do next:** Classify or bound the disjoint-alias matching families
  for non-full-domain boundary packets, using the scalar-fit criterion as the
  next local obstruction.

### 2026-06-28 - M1 full-domain boundary image count

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Counts the image of the full-domain `2m-1` moment
  boundary map: all fibers are singleton except root-linear complement pairs,
  so the exact image size is
  `((|F|-1)^m-(|F|-1)) binom(n,m) + (|F|-1) binom(n,m)/2`.
- **How it is useful:** Closes the full-domain boundary endpoint locally for
  fixed `m=tau+1` in the polynomial-field window: the non-root-linear part is
  support-recoverable and the root-linear part is an explicit complement-pair
  ledger.
- **What to do next:** Use this endpoint image count as the terminal charge in
  the same-slope M1 ladder, then extend or falsify analogous image-count
  statements away from the full-domain `n=2m` boundary.

### 2026-06-28 - M1 full-domain boundary dichotomy

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves the full-domain boundary dichotomy:
  `2m-1` visible moments either determine the domain `m`-support uniquely, or
  the packet is root-linear and has exactly the complementary support alias.
- **How it is useful:** Converts the final full-domain boundary ambiguity into
  an explicit exceptional ledger while making all other boundary packets
  support-identifiable.  The current audit records `4200` support-unique
  packets and `120` root-linear complementary-alias packets.
- **What to do next:** Use support-identifiability to charge non-root-linear
  boundary packets to recovered support ledgers, and charge the root-linear
  complement pairs to the polynomial endpoint ledger.

### 2026-06-28 - M1 root-linear endpoint is polynomial-sized

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Counts the full-domain root-linear alias locus:
  labeled aliased boundary packets are exactly `(Y,nu)` with
  `a_y=nu y`, hence there are `(|F|-1) binom(n,m)` of them, paired by
  complement in visible moments.
- **How it is useful:** Shows the only ambiguous full-domain endpoint isolated
  so far is polynomial-sized for fixed `m=tau+1` in the polynomial-field
  window, rather than an arbitrary `(F^*)^m` amplitude family.
- **What to do next:** Use this polynomial endpoint ledger as the terminal
  charge after non-aliased packets are made support-identifiable, and test
  whether analogous low-dimensional amplitude loci occur for non-full-domain
  boundary packets.

### 2026-06-28 - M1 full-domain aliases are root-linear

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Specializes the boundary alias criterion to the
  full root-of-unity domain with `n=2m`: the complementary alias exists exactly
  when the packet amplitudes are root-linear, `a_y/y` constant on the mode set.
- **How it is useful:** Turns the current `F_7^*`, mode-size-`3` endpoint into
  a named amplitude locus rather than an arbitrary disjoint-alias problem.  The
  verifier checks all `4320` boundary packets and finds the root-linear
  histogram `4200/120`, exactly matching the alias histogram.
- **What to do next:** Try to prove that root-linear terminal packets are
  forced into quotient-periodic, tangent, or lower-core ledgers, or bound them
  directly as a small exceptional endpoint family.

### 2026-06-28 - M1 boundary aliases are scalar fits

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Refines the boundary-alias criterion for terminal
  sparse packets: a disjoint candidate locator `ell_Z` aliases the branch mode
  set `Y` exactly when the deletion-tree scalars satisfy
  `c_X(y;C) ell_Z(y)=mu` for all `y in Y`.
- **How it is useful:** Converts the endpoint moment ambiguity into a concrete
  scalar-cut interpolation problem on the terminal deletion tree.  The current
  `F_7^*` audit checks `4320` boundary candidates and finds the same
  `4200/120` histogram for scalar fits as for moment aliases.
- **What to do next:** Use the scalar-fit form to bound or charge boundary
  aliases, especially by proving that persistent fits force quotient-periodic,
  tangent, or lower-core structure.

### 2026-06-28 - M1 terminal packet boundary aliases

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / COUNTEREXAMPLE-MECHANISM / EXACT FINITE
  VERIFICATION.
- **What is being added:** Proves that the `2m`-moment locator recovery
  threshold is sharp for terminal sparse packets: a boundary packet with only
  `2m-1` moments can have a disjoint equal-size alias, while any alias sharing
  a root is ruled out by a square Vandermonde argument.  The note also records
  the kernel-weight alias criterion `a_y=mu/P_W'(y)`.
- **How it is useful:** Identifies the precise obstruction left by
  mode-size-`tau+1` terminal packets.  Rank visibility alone cannot recover
  these modes, so an M1 proof must obtain one further structural moment, charge
  possible disjoint aliases, or exploit branch-amplitude constraints to bound
  the boundary packet family directly.  In the current `F_7^*` audit, only
  `120` of `4320` boundary packets alias; `4200` are support-identifiable
  among domain `3`-sets.
- **What to do next:** Develop a charge or bound for boundary disjoint-alias
  packets, starting with the `t=2`, mode-size-`3` branch-amplitude restrictions
  in the `F_7^*` audit.

### 2026-06-28 - M1 visible packets recover their mode locator

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that once `2m` moments of a terminal sparse
  packet are visible, the nonsingular moment system recovers the unique monic
  degree-`m` annihilator, namely the branch-mode locator.
- **How it is useful:** Makes visible productive terminal packets intrinsic:
  their mode set is recoverable from the lower-boundary moments, and no
  lower-degree recurrence collapse can explain them.
- **What to do next:** Extend visibility or rank/minor control to higher-mode
  productive packets, then charge recoverable packets to quotient-periodic,
  tangent, or aperiodic sparse-moment ledgers.

### 2026-06-28 - M1 sparse packets peel losslessly

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that applying any subset locator inside a
  terminal sparse mode packet removes exactly those modes; every proper peel
  remains nonzero, while peeling all modes gives the active annihilator.
- **How it is useful:** Rules out hidden premature zero-boundary collapse
  inside productive terminal packets and makes the fixed-root frontier shift
  visibly lossless at the packet level.
- **What to do next:** Use the lossless peeled packets to bound productive
  determinant-nondegenerate packets or charge persistent ones to quotient and
  tangent ledgers.

### 2026-06-28 - M1 sparse packets have rank certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that any visible terminal sparse mode packet
  carries a nonzero moment-Hankel determinant equal to the product of the mode
  coefficients times the squared Vandermonde product.
- **How it is useful:** Shows productive terminal packets are
  determinant-nondegenerate sparse moment objects, giving a concrete rank/minor
  obstruction for the next M1 bound rather than only a sparse expansion.
- **What to do next:** Attack the determinant-nondegenerate sparse packet locus
  by rank/minor ledgers, inverse Littlewood-Offord input, or
  quotient-periodic/tangent charges.

### 2026-06-28 - M1 branch vertices are sparse mode packets

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Generalizes the terminal branch-pair normal form to
  an all-exit sparse mode-packet identity: every branch vertex with nonzero
  exit set `Y` gives a lower-boundary moment packet supported on the roots in
  `Y`, with coefficients determined by the exit scalars and the Vandermonde
  denominators.
- **How it is useful:** Turns productive terminal branching into a sparse
  moment-packet object, matching the inverse Littlewood-Offord style M1 target
  more directly than pairwise branching data.
- **What to do next:** Bound productive sparse packets or charge their
  persistent cases to quotient-periodic/tangent ledgers.

### 2026-06-28 - M1 branch pairs have two-mode lower boundaries

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that any pair of nonzero terminal deletion
  exits forces an explicit two-mode lower-boundary vector on the core obtained
  by deleting both roots, and distinguishes productive branch pairs whose two
  children both have terminal completions.
- **How it is useful:** Pushes the terminal residual below mere branching:
  terminal multiflag mass is carried by productive two-mode packets inside the
  fixed-root Hankel ladder.
- **What to do next:** Bound the productive two-mode lower-boundary packets,
  or show that quotient-periodic/tangent components account for the persistent
  productive branch pairs.

### 2026-06-28 - M1 terminal flags have deletion-tree recursion

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Defines the terminal deletion tree whose outgoing
  edges are the nonzero first-row scalar cuts, proves the exact recursion for
  terminal flag counts, and identifies multiflag supports with explicit
  branching vertices.
- **How it is useful:** Replaces the apparent factorial terminal-ordering
  residual by a concrete branching obstruction inside fixed-root kernels.  This
  gives the next M1 target: bound or collapse those scalar-cut branching
  vertices.
- **What to do next:** Attack the branching vertices directly, looking for a
  quotient-periodic charge, a conductor-uniform character-sum bound, or a
  counterexample family showing genuine multiplicative branching.

### 2026-06-28 - M1 terminal flags are zero-free scalar chains

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Clarifies that the terminal bottom-support
  condition is equivalent to the fixed-root kernel by the iterated identity,
  and identifies the true terminal residual as a zero-free chain of explicit
  first-row boundary scalars.
- **How it is useful:** Prevents overclaiming a support saving from the bottom
  condition and isolates the actual remaining M1 object: zero-free flags inside
  fixed-root/root-difference support kernels.
- **What to do next:** Bound or structurally collapse these zero-free scalar
  flag sets using quotient-periodic or aperiodic M1 input.

### 2026-06-28 - M1 terminal flags reduce to bottom supports

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Defines the terminal bottom support set
  `Bot^{X}_{tau,q}` and proves that terminal zero-free flags map to it with at
  most the explicit `q!` ordering factor.
- **How it is useful:** Converts the terminal residual left by the fixed-root
  filtration into a bottom root-difference support count, the kind of object
  that can be attacked by quotient-periodic or aperiodic M1 estimates.
- **What to do next:** Prove a polynomial bound for the bottom support sets or
  identify quotient-periodic collapse in these terminal kernels.

### 2026-06-28 - M1 first-zero paths charge to deeper zero ledgers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Turns the fixed-root stopping decomposition into an
  ordered first-zero ledger: ordered active paths split exactly into first-zero
  stops and terminal zero-free flags, and every first-zero stop charges to a
  one-row deeper zero-boundary kernel.
- **How it is useful:** Separates the same-slope fixed-root ladder into
  already-controlled deeper zero-boundary ledgers plus a named terminal
  zero-free flag residual, avoiding an opaque multiplicative path count.
- **What to do next:** Attack the terminal zero-free flags directly, or prove
  that quotient-periodic/aperiodic M1 structure makes their bottom conditions
  sparse.

### 2026-06-28 - M1 fixed-root filtration has first-zero stopping

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Iterates the fixed-root filtration identity into a
  first-zero stopping decomposition: every ordered deletion path either first
  hits a zero-boundary star or reaches the terminal bottom condition
  `H_{tau,0}(Delta_{X union C}s)1=0`.
- **How it is useful:** Gives the same-slope fixed-root ladder a finite
  stopping structure; nonzero marked steps move to the next fixed-root layer
  instead of creating an independently compounding packet family.
- **What to do next:** Bound the terminal bottom-difference paths or show
  that quotient-periodic/aperiodic structure collapses them in the M1 window.

### 2026-06-28 - M1 fixed-root filtration incidence is exact

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Refines the recursive fixed-root ledger to a
  set-level identity: active incidences on a fixed-chain kernel equal the
  disjoint union of zero-boundary star incidences and nonzero root-marked
  incidences, equivalently the next fixed-root layer.
- **How it is useful:** Shows that the marked residual at each rung is the
  nonzero part of the next fixed-root incidence sequence, not a new packet
  family that can compound independently.
- **What to do next:** Use this filtration identity to seek a terminal
  quotient-periodic or aperiodic packing bound for the bottom fixed-root
  layers.

### 2026-06-28 - M1 fixed-root rungs keep first-boundary ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that after any fixed-root chain
  `X=(x_1,...,x_m)` is stripped, the active kernels for
  `Delta_{x_m}...Delta_{x_1}s` satisfy the same exact first-boundary
  incidence identity with extension factor `n-j+1`.
- **How it is useful:** Makes the fixed-root residual ladder recursively
  additive: every rung splits into zero-boundary cores and root-marked
  incidences, rather than accumulating a multiplicative packet loss.
- **What to do next:** Use the recursive ledger to seek a uniform bound or
  quotient-periodic collapse for the iterated marked-boundary residuals.

### 2026-06-28 - M1 fixed-root deletion iterates by root differences

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves and audits the iterated identity
  `H_{tau,j}(s)((X-x_1)...(X-x_m)L)
   = H_{tau,j-m}(Delta_{x_m}...Delta_{x_1}s)L`.
- **How it is useful:** Gives the fixed-root/root-slice residual ladder a
  precise algebraic backbone: repeated root stripping is ordinary Hankel
  testing on iterated root-difference syndromes, not a new packet mechanism.
- **What to do next:** Use this iterated form to state uniform bounds for the
  residual marked-boundary ladder or to identify quotient-periodic collapse.

### 2026-06-28 - M1 isolated one-row residual has second boundary

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Gives the isolated-vertex criterion for the
  one-row root-marked residual: after non-isolated residual edges descend,
  isolated residual cores are exactly those whose lower
  `H_{tau+1,j-2}(Delta_x s)` deletion-boundaries are all nonzero.
- **How it is useful:** Repeats the original same-slope support split one
  level down: residual branching descends additively, while isolated residual
  mass becomes a second marked-boundary ledger.
- **What to do next:** Bound or structurally classify the second marked
  boundary object, especially in the aperiodic quotient-normal setting.

### 2026-06-28 - M1 root-marked residual edges descend

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves that a one-exchange edge inside a fixed-root
  root-marked residual slice forces
  `H_{tau+1,j-2}(Delta_x s)ell_R=0` on the common lower core, and records the
  corresponding non-isolated residual support ledger.
- **How it is useful:** Shows that branching inside the remaining one-row
  residual descends additively in the root-difference Hankel ladder; it is not
  a new primitive same-slope growth source.
- **What to do next:** Analyze the isolated vertices of the one-row residual
  or relate the descended lower cores to quotient-periodic/root-slice charges.

### 2026-06-28 - M1 root-marked residual is one-row slice

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Sharpens the fixed-root difference-kernel form:
  inside `K^x_{tau,j-1}(s)`, the zero-boundary subkernel is exactly the single
  row `H_{1,j-1}(s)ell_C=0`, and the root-marked residual is the complementary
  nonzero row slice.
- **How it is useful:** Converts the remaining local root-marked mass into an
  explicit rank-testable root-slice problem, rather than an opaque boundary
  object.
- **What to do next:** Bound this one-row nonzero slice uniformly, or show
  that high multiplicity forces quotient-periodic or lower-core structure.

### 2026-06-28 - M1 fixed-root slices are root-difference Hankel kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Identifies each fixed-root active slice with the
  Hankel kernel for the root-difference syndrome
  `(Delta_x s)_i=s_{i+1}-x s_i`, via
  `H_{tau,j}(s)((X-x)L)=H_{tau,j-1}(Delta_x s)L`.
- **How it is useful:** Turns the root-marked residual into a concrete
  root-slice difference-kernel problem with the zero-boundary subkernel
  removed, matching the M1 fixed-root/root-slice proof route.
- **What to do next:** Apply fixed-root/root-slice or quotient-aware bounds to
  these difference kernels uniformly over the domain roots.

### 2026-06-28 - M1 root-marked chart is fixed-root residual

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves the rootwise decomposition
  `|A^x_{tau,j}(s)| = |Z^x_{tau+1,j-1}(s)| + |B^x_{tau+1,j-1}(s)|`.
  Thus the root-marked first-boundary chart is exactly the fixed-root active
  slice after zero-boundary star cores are removed.
- **How it is useful:** Moves the remaining same-slope root-marked residual
  into the fixed-root/root-slice ledger family requested by the M1 proof
  program, rather than treating it as a new primitive packet.
- **What to do next:** Use fixed-root/root-slice or quotient-aware M1 reserve
  bounds to control the fixed-root active slices uniformly.

### 2026-06-28 - M1 first-boundary incidence identity is exact

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Sharpens the same-slope support ledger to the exact
  first-boundary identity
  `j |A_{tau,j}(s)| = (n-j+1)|E_{tau+1,j-1}(s)| + |B^rm_{tau+1,j-1}(s)|`,
  where the active edge cores are exactly the zero first-boundary cores.
- **How it is useful:** Removes slack from the local same-slope split:
  root-marked boundary incidences are precisely the one-extension part of the
  first-boundary chart, while zero-boundary cores account for every active
  star incidence.
- **What to do next:** Bound the nonzero root-marked chart using quotient,
  aperiodic, or fixed-root structure; the local deletion-incidence accounting
  itself is now exact.

### 2026-06-28 - M1 same-slope active support has one ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Combines the non-isolated edge-core ledger with
  the isolated root-marked boundary ledger into
  `j |A_{tau,j}(s)| <= j(n-j+1)|E_{tau+1,j-1}(s)| + |B^rm_{tau+1,j-1}(s)|`.
- **How it is useful:** Packages the local same-slope support split as a
  single M1 accounting statement: every active support is charged either to a
  one-row lower edge core or to a root-marked first-boundary incidence.
- **What to do next:** Bound the root-marked boundary ledger by the
  boundary-off target-image or fixed-root reserve machinery, then connect this
  local support ledger to the all-line aperiodic residue-packing target.

### 2026-06-28 - M1 isolated locator mass has marked-boundary ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Converts the isolated active locator criterion into
  a counting ledger: `j |Iso_{tau,j}(s)| <= |B^rm_{tau+1,j-1}(s)|`, where
  `B^rm` is the nonzero root-marked first-boundary ledger.
- **How it is useful:** Completes a local summable split of same-slope support
  mass: non-isolated vertices are charged to lower Hankel component ledgers,
  while isolated vertices are charged to root-marked first-boundary incidences.
- **What to do next:** Bound the root-marked boundary ledger using the
  boundary-off target-image and fixed-root reserve machinery.

### 2026-06-28 - M1 isolated active locators are root-marked boundaries

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Identifies the exact local criterion for isolated
  same-slope active locators.  For active `T` and `x in T`, the one-row deeper
  deletion-core vector has the form
  `c_x(1,x,...,x^tau)`, and `T` is isolated iff all these scalars are nonzero.
- **How it is useful:** Completes the local split after the non-isolated
  component ledger: residual isolated mass is a root-marked first-boundary
  object, not an unstructured same-slope packet.
- **What to do next:** Bound or charge the root-marked first-boundary residual
  using boundary-off, fixed-root, or quotient-aware target-image ledgers.

### 2026-06-28 - M1 same-slope component ledger is summable

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL / EXACT FINITE VERIFICATION.
- **What is being added:** Converts the row-level component descent into a
  counting ledger.  Non-isolated active `j`-locators are bounded by
  `(n-j+1)` times the number of one-row lower active edge cores, while non-star
  components inject into two-row lower-core witnesses.
- **How it is useful:** Makes the same-slope packet recursion summable:
  support mass and branching component count are charged to lower Hankel
  ledgers with explicit local polynomial factors, not to an uncontrolled
  multiplicative component tree.
- **What to do next:** Combine this support-mass ledger with isolated
  locator estimates and the quotient-periodic/fixed-root reserve charges.

### 2026-06-28 - M1 same-slope components have row-level additive ledgers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL.
- **What is being added:** Generalizes the `t=2` component dichotomy to
  arbitrary Hankel row level.  A nontrivial component in the active
  one-exchange graph for `H_{tau,j}` is either a star component with
  `H_{tau+1,j-1}` on the common core, or it contains a distinct-root corner
  forcing `H_{tau+2,j-2}` on a lower core.
- **How it is useful:** Turns the same-slope packet recursion into an additive
  graph ledger at every row level.  Residual components are one-row-deeper
  star packets after the two-row lower-core branch is charged.
- **What to do next:** Sum this component ledger over row levels and relate the
  resulting star/lower-core charges to the M1 fixed-root and quotient-periodic
  ledgers.

### 2026-06-28 - M1 Hankel corners descend additively at all row levels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / STRUCTURAL.
- **What is being added:** Proves the row-level version of the corner descent:
  three active `j`-locators forming a distinct-root two-edge corner for
  `H_{tau,j}` force the lower-core recurrence `H_{tau+2,j-2}`.
- **How it is useful:** This is the structural additive-depth mechanism behind
  the `t=2` same-slope packet audit.  Branching does not create an independent
  multiplicative packet; it moves two rows deeper and two roots lower in the
  Hankel ladder.
- **What to do next:** Use this row-level descent to organize iterated
  same-slope packet ladders and compare the resulting lower-core charges with
  the fixed-root/root-slice reserve.

### 2026-06-28 - M1 same-slope components are star or lower-core

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Globalizes the two-edge corner dichotomy to
  connected components of the fixed-slope `t=2` active one-exchange graph.
  A nontrivial component is either contained in one star with
  `H_{3,j-1}(Syn(w_lambda))ell_C=0`, or it contains a lower-core witness
  `H_{4,j-2}(Syn(w_lambda))ell_R=0`.
- **How it is useful:** Converts local additive descent into a component-level
  packet statement: after lower-core charges, same-slope components are single
  star packets of size at most `n-j+1`, not multiplicatively branching
  variable-line families.
- **What to do next:** Use the component dichotomy to sum same-slope packets
  against the star-core and lower-core ledgers, then connect lower-core events
  to the existing fixed-root/root-slice reserve.

### 2026-06-28 - M1 two-edge same-slope corners descend additively

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Extracts the two-edge corner dichotomy from the
  fixed-slope `t=2` core-plane classification.  If two active one-exchange
  neighbors of a complement replace the same root, the corner is charged to the
  `H_{3,j-1}` star core; if they replace two distinct roots, the corner forces
  the lower recurrence `H_{4,j-2}(Syn(w_lambda))ell_R=0`.
- **How it is useful:** Makes the same-slope packet recursion additive at the
  first branching point.  Local graph branching either remains in a star ledger
  or descends one Hankel rung; it cannot create a separate non-fixed
  variable-line same-slope packet.
- **What to do next:** Turn the local corner dichotomy into a global
  component/energy charge for same-slope one-exchange components, then relate
  the remaining lower-core events to the fixed-root/root-slice ledger.

### 2026-06-28 - M1 fixed-slope core planes are fixed-root or lower-core

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Proves the fixed-slope `t=2` core-plane
  classification.  For a fixed `(j-2)`-core, the two-root extension equations
  in `(sigma,pi)=(x+y,xy)` are consecutive Hankel equations; any consistent
  rank-one line is forced to be `pi=q sigma-q^2`, hence fixed-root, while the
  fully degenerate compatible case is exactly
  `H_{4,j-2}(Syn(w_lambda))ell_R=0`.
- **How it is useful:** Rules out non-fixed product-Mobius/fixed-sum
  variable-line packets inside one fixed same-slope fiber.  Positive-dimensional
  same-slope core planes are therefore charged to fixed-root/root-slice or
  deeper lower-core Hankel ledgers.
- **What to do next:** Use this classification to separate residual same-slope
  packet mass from the different-slope variable-line branch and then bound the
  lower-core/full-plane alternatives.

### 2026-06-28 - M1 nonzero top packets have bounded size

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Records the immediate corollary of the full-top
  zero-syndrome lemma: at nonzero combined syndrome, a `(j+1)`-top set can
  have at most `j` active `j`-subcomplements.  The verifier now reports the
  nonzero top active-size profile and enforces the `<=j` cap.
- **How it is useful:** Closes the local full-top growth mechanism in the
  `t=2` same-slope packet route.  Residual top packets are necessarily partial
  and linearly bounded in `j`, while full top cliques are tangent/global-codeword
  events.
- **What to do next:** Move the packet analysis from local top cliques to
  variable-line components or optimize larger partial-top scans.

### 2026-06-28 - M1 full top packets are zero-syndrome

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Strengthens the `t=2` triangle packet analysis:
  if every `j`-subcomplement of a `(j+1)`-top set is active at the same slope,
  then the combined syndrome vanishes.  The triangle verifier now counts full
  top cliques and asserts that none occur at nonzero combined syndrome.
- **How it is useful:** Rules out full top packets as residual primitive
  same-slope growth.  They are global-codeword/tangent ledger events, leaving
  only partial top components and variable-line packets for the next M1
  same-slope analysis.
- **What to do next:** Attack partial top components in larger `j`, or move to
  the non-fixed variable-line packet residual where the existing packet lemma
  reduces growth to different-slope two-exchange energy and boundary targets.

### 2026-06-28 - M1 t=2 triangle packet lifts

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_triangle_packets.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Extends the `t=2` Hankel packet extraction from
  one-exchange edges to pairwise one-exchange triangles.  Star triangles lift
  to the `H_{3,j-1}` core recurrence, while top triangles lie in the common
  lifted `H_{1,j+1}` kernel of their `(j+1)`-top set.
- **How it is useful:** Handles the next collision shape in the M1
  same-slope packet route.  The exact syndrome verifier checks the first
  genuine top-packet case `F_7^*`, `(n,k,a,j)=(6,2,4,2)`, where all nonzero
  same-slope triangles are star/root-slice events and top triangles occur only
  on the zero combined syndrome.
- **What to do next:** Move from triangle packets to variable-line/top-packet
  components in larger `j`, using the lifted `t=1` and `t=3` kernels as the
  charged ledgers.

### 2026-06-28 - M1 t=2 one-exchange Hankel core lift

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_t2_one_exchange_lift.md`,
  `experimental/scripts/verify_m1_hankel_t2_one_exchange_lift.py`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXACT FINITE VERIFICATION.
- **What is being added:** Extracts the `t=2` determinant gate and proves that
  a same-slope one-exchange collision lifts to the `t=3` Hankel recurrence on
  the common core.  The verifier checks the determinant gate against the
  slope-loop classifier and verifies every same-slope one-exchange lift in the
  exact `F_5^*` and `F_7^*` tiny scans.
- **How it is useful:** Turns the first local collision mechanism in the M1
  Hankel packet route into a chargeable next-slack/root-slice object, reducing
  the amount of unexplained primitive slope growth that a counterexample could
  use.
- **What to do next:** Optimize and run the richer `j=2` case, then extract
  the residual top-packet or variable-line packet verifier after same-slope
  root-slice lifts are charged.

### 2026-06-28 - M1 exact target Hankel equivalence verifier

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/scripts/verify_m1_exact_target_hankel_equivalence.py`,
  `experimental/notes/m1/m1_exact_target_v0.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL CHECK.
- **What is being added:** Records the exact support-locator Hankel form of
  the M1-v0 quotient-normal target and adds a verifier comparing the direct
  restricted-code definition against the Hankel-pencil classification on the
  full `F_5^*` and `F_7^*` tiny scans.
- **How it is useful:** Bridges the concrete `Bad_nc`/`Prim_M1` conjecture to
  Przemek's target object `(H(u)+zH(v))ell_T=0`, so future falsification can
  search split-locator Hankel packets without changing the predicate.
- **What to do next:** Use the verified Hankel form to build a `t=2`
  aperiodic split-locator packet scanner, with quotient-periodic support
  packets charged before primitive slope-image growth is tested.

### 2026-06-28 - M1 exact target v0 quotient-normal scanner

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/scripts/scan_m1_exact_target_v0.py`,
  `experimental/notes/m1/m1_exact_target_v0.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / FALSIFICATION-FIRST.
- **What is being added:** Adds a tiny-field exact scanner for the M1-v0
  primitive slope target.  The scanner enumerates quotient-normal endpoint
  pairs, computes exact noncontained `a`-support slope witnesses, splits slopes
  by support stabilizer, and reports endpoint root-free denominator counts for
  max-primitive examples.
- **How it is useful:** Gives the M1-v0 conjecture a reproducible
  counterexample-first harness.  The first full scans over `F_5^*` and `F_7^*`
  find no primitive alert under the default `n^2` guard, while showing that
  full field-sized primitive slope images can already occur in tiny normalized
  examples.
- **What to do next:** Extend the scanner toward the actual Hankel-pencil
  packet object, especially low-slack `t=2` split-locator cases, so it can
  search for growth mechanisms rather than only slope-image maxima.

### 2026-06-28 - M1 exact target v0 as primitive slope packing

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/notes/m1/m1_exact_target_v0.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** CONJECTURAL / FALSIFICATION-FIRST / PROOF-PROGRAM.
- **What is being added:** Formulates a concrete M1-v0 target: split finite
  support-wise noncontained slopes into an exact quotient-periodic support
  budget and a stabilizer-primitive remainder, then conjecture a polynomial
  bound on the primitive remainder in the high-slack polynomial-field window.
- **How it is useful:** Turns M1 into a falsifiable theorem-shaped target
  analogous to the accepted L1/L2 target notes; a counterexample must now
  produce many quotient-normal primitive slopes rather than presentation,
  reciprocal, gauge, alias, or quotient-periodic multiplicity.
- **What to do next:** Build the direct scanner promised in the note and use
  it to refine the target if primitive counterexamples appear.

### 2026-06-28 - M1 endpoint quotient denominators are Hankel kernels

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that a root-free degree-`e` denominator
  presents the endpoint quotient class `[-y]` iff `Qy in RS[F,D,k+e]`,
  equivalently iff `H_{n-k-e,e}(Syn(y))Q=0`.
- **How it is useful:** Turns the denominator side remaining after
  quotient-gauge normalization into a concrete endpoint Hankel-kernel target
  for `f` and `g`, rather than a separate coefficient or slope ledger.
- **What to do next:** Bound these root-free endpoint multiplier kernels after
  quotient-periodic and active-incidence branches are charged.

### 2026-06-28 - M1 endpoint rank-one charts glue by reciprocal inversion

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that inversion bijects the nonzero
  coefficients of `Mu_phi(Y)` with those of `Mu_{-Y}(-phi)`.
- **How it is useful:** Identifies the quotient-normal `Qg` and reciprocal
  `Qf` endpoint ledgers as the same projective slope ledger away from the
  original zero slope, preventing an independent double count of standard
  nonzero scalar branches.
- **What to do next:** Count the quotient-normal endpoint ledger once, with a
  separate explicit zero-slope check.

### 2026-06-28 - M1 rank-one coefficient ledgers are quotient-gauge invariant

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that rank-one support-wise noncontained
  coefficient sets are unchanged after adding global Reed-Solomon codewords to
  the direction and target.
- **How it is useful:** Shows that standard `Qg` and nonzero `Qf`
  residue-line presentations are quotient gauges of the endpoint rank-one
  problems `Mu_{-g}(f)` and `Mu_{-f}(g)` rather than distinct coefficient
  ledgers.
- **What to do next:** Use quotient-normal endpoint classes as the object to
  pack; keep denominator charts only for active-incidence and
  quotient-periodic structure.

### 2026-06-28 - M1 divided-evaluation fibers are coefficient-lossless

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that all primitive presentations with the
  same divided evaluation datum `(B/Q,w/Q)` have the same support-wise
  noncontained coefficient set.
- **How it is useful:** Removes finite-domain alias multiplicity from the
  actual slope/coefficient ledger: after choosing one representative per
  divided-evaluation fiber, a cutoff family pays only `sum_s W(e_s)`, and in
  the one-coefficient range pays at most `|Ev(A_{<=E})|`.
- **What to do next:** Use the remaining tail chart as active
  denominator/incidence geometry rather than as a multiplicative slope loss.

### 2026-06-28 - M1 cutoff tail aliases are upper defect-quotient charts

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Identifies every nontrivial cutoff alias over a
  minimal representative as an upper defect-quotient chart
  `Q'=rem_{Q_s}(L_D R B_s^{-1})+Q_sH`, with projective parameter dimension
  `2E-n+1`.
- **How it is useful:** Turns the remaining high-minimal-degree tail from a
  cardinality budget into an explicit algebraic object that active incidence
  or aperiodic packing arguments can attack.
- **What to do next:** Intersect these upper tail charts with the active M1
  Hankel/residue-line incidence conditions.

### 2026-06-28 - M1 one-coefficient cutoffs have only tail-alias loss

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Combines the high-minimal-degree tail split with
  the one-coefficient fixed-class range, proving
  `|Lambda(A_{<=E})| <= |Ev(A_{<=E})| + Pi_q(2E-n+1)|S_tail|`
  for `1<=E<=t-j`.
- **How it is useful:** Shows that, throughout the one-coefficient primitive
  range, the only possible loss beyond divided-evaluation counting is
  finite-domain aliasing over high-minimal-degree representatives.
- **What to do next:** Bound the high-minimal-degree tail image or rule it out
  with active M1 incidence constraints.

### 2026-06-28 - M1 skeleton ledger uses tail-local weights

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Sharpens the minimal-representative skeleton
  ledger by replacing the global cutoff weight `W_E` on alias terms with the
  tail-local weight `W_{s,E}=max_{e_s<=e<=E} W(e)`.
- **How it is useful:** Preserves more denominator-degree information inside
  each divided-evaluation fiber, so later active-class counts do not overpay
  low minimal-degree fibers by the global cutoff weight.
- **What to do next:** Use tail-local weights together with high-minimal-degree
  tail constraints in the next active incidence reduction.

### 2026-06-28 - M1 nontrivial cutoff fibers live on high-minimal-degree tail

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Splits minimal divided-evaluation representatives
  into `e_s+E<=n` and `e_s+E>n`, proving that only the high-minimal-degree
  tail can carry nontrivial primitive alias multiplicity inside a cutoff
  family.
- **How it is useful:** Identifies the remaining finite-domain alias
  obstruction after skeletonization as the tail `e_s>n-E`, while low minimal
  representatives are singleton fibers.
- **What to do next:** Target the high-minimal-degree tail with active
  incidence or aperiodic packing arguments.

### 2026-06-28 - M1 minimal representatives give a sharper cutoff ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Gives a degree-sensitive skeleton bound: choose a
  minimal-degree representative in each divided-evaluation fiber, then the
  fiber pays `W(e_s)` for that representative and only `W_E U_q(e_s,E)` for
  same-or-upward aliases.
- **How it is useful:** Refines the uniform cutoff multiplier by preserving
  the actual minimal denominator degrees of fibers; fibers with `e_s+E<=n`
  become singleton within the cutoff family.
- **What to do next:** Use the skeleton form when an incidence argument can
  control the minimal denominator degrees of divided evaluation fibers.

### 2026-06-28 - M1 minimal representatives sharpen cutoff alias multipliers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Sharpens the cutoff active-ledger multiplier by
  choosing a minimal-degree representative in each divided evaluation fiber,
  removing the lower-alias budget from `M_q(E)`.
- **How it is useful:** Improves the cutoff reduction from a two-budget
  uniform multiplier to `M_q(E)=1+Pi_q(2E-n+1)` in the high-total-degree
  range, while preserving `M_q(E)=1` when `2E<=n`.
- **What to do next:** Use the sharpened multiplier in degree-slab active
  primitive-class counts.

### 2026-06-28 - M1 degree-slab ledgers pay local alias multipliers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Extends the cutoff active-ledger reduction to a
  degree-slab decomposition: each slab `E_{r-1}<deg Q<=E_r` contributes at
  most `W_r M_q(E_r)|Ev_r|`.
- **How it is useful:** Lets later M1 arguments charge alias-free low-degree
  slabs and high-degree alias-prone slabs separately, avoiding a global
  worst-cutoff multiplier.
- **What to do next:** Choose degree slabs adapted to the active
  quotient/aperiodic incidence problem and bound the divided evaluation images
  on each slab.

### 2026-06-28 - M1 low one-coefficient cutoff has no multiplicity loss

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Combines the cutoff active-ledger reduction with
  the one-coefficient fixed-class range: if `1<=E<=t-j` and `2E<=n`, then
  `|Lambda(A_{<=E})| <= |Ev(A_{<=E})|`.
- **How it is useful:** Identifies a genuinely lossless low-denominator
  subrange of M1 where both finite-domain alias multiplicity and fixed-class
  coefficient multiplicity vanish.
- **What to do next:** Bound or classify the divided evaluation image in this
  low range using aperiodic or Hankel incidence constraints.

### 2026-06-28 - M1 cutoff active ledgers reduce to divided evaluations

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Derives a uniform cutoff multiplier `M_q(E)` from
  the primitive alias-fiber bound and proves
  `|A_{<=E}| <= M_q(E)|Ev(A_{<=E})|`, then combines it with the active
  fixed-class weights to bound `|Lambda(A_{<=E})|`.
- **How it is useful:** Turns the M1 cutoff active primitive-class problem
  into a divided-evaluation counting problem with an explicit finite-domain
  alias multiplier, trivial when `2E<=n`.
- **What to do next:** Use quotient/aperiodic or Hankel incidence arguments to
  bound the divided evaluation image `Ev(A_{<=E})`.

### 2026-06-28 - M1 cutoff primitive alias fibers have two defect budgets

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the primitive alias chart into a cutoff
  fiber bound: for a fixed positive-degree primitive datum, aliases of degree
  at most `E` split into a lower-defect budget `Pi_q(e+min(E,e-1)-n)` and a
  same-or-upward defect-quotient budget `Pi_q(2E-n+1)` when applicable.
- **How it is useful:** Gives the active primitive-class ledger an explicit
  finite-field multiplicity bound for evaluation fibers below a denominator
  cutoff, with no extra target-vector multiplicity.
- **What to do next:** Combine this cutoff fiber bound with active incidence
  constraints to turn divided-evaluation counts into primitive-class counts.

### 2026-06-28 - M1 direction-alias admissibility audit

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED-LOCAL.
- **What is being added:** Makes the reduced-numerator condition explicit in
  the base defect-congruence parametrization of primitive direction aliases,
  including the polynomial-direction endpoint convention.
- **How it is useful:** Keeps the source alias congruence aligned with the
  later fixed-degree chart and prevents inadmissible numerator presentations
  from being read as primitive aliases.
- **What to do next:** Use the explicit admissibility language in any further
  active primitive-class counts.

### 2026-06-28 - M1 lower-alias chart admissibility audit

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED-LOCAL.
- **What is being added:** Tightens the lower-alias union statement to make
  the retained defect-degree, root-free, degree-of-numerator, and coprimality
  conditions explicit.
- **How it is useful:** Prevents the aggregate lower-alias bound from being
  read as accepting every defect in the ambient projective space; only the
  fixed-degree chart's admissible candidates are aliases.
- **What to do next:** Keep using the corrected retained-defect formulation
  when connecting alias bounds to active primitive-class counting.

### 2026-06-28 - M1 full primitive aliases lift from direction aliases

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that, for a fixed primitive datum
  `(Q_1,B_1,w_1)`, once a primitive direction alias `(Q_2,B_2)` is fixed,
  divided target agreement uniquely determines `w_2` on `D`.
- **How it is useful:** Transfers the defect-congruence and lower-alias bounds
  from primitive direction pairs to full primitive residue-line triples, ruling
  out hidden target multiplicity inside an evaluation fiber.
- **What to do next:** Apply the full-data alias bounds to active primitive
  class counting in the M1 ledger.

### 2026-06-28 - M1 lower aliases start above the half-degree threshold

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Sums the lower side of the fixed-direction alias
  chart: a degree-`e_1` primitive direction has no lower-degree alias unless
  `2e_1>n+1`, and otherwise all lower aliases are controlled by defects in
  `F[X]_{<2e_1-n-1}`.
- **How it is useful:** Shows downward finite-domain aliasing only appears
  above the half-domain threshold, with a single small projective defect-space
  bound for all lower aliases of a fixed direction.
- **What to do next:** Combine the lower-alias defect bound with active
  primitive-class incidence constraints to test whether these downward aliases
  can occur in the M1 active ledger.

### 2026-06-28 - M1 fixed-direction aliases have a defect-quotient chart

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Parameterizes all high-degree primitive direction
  aliases of a fixed `(Q_1,B_1)` and fixed denominator degree `e_2` by a short
  defect `R` plus, when `e_2>=e_1`, a quotient polynomial `H`.
- **How it is useful:** Turns the high-degree finite-domain alias obstruction
  into an explicit low-dimensional chart and gives finite-field projective
  bounds depending on `d=e_1+e_2-n`.
- **What to do next:** Combine this chart with active-class constraints or
  Hankel incidence equations to rule out most chart parameters.

### 2026-06-28 - M1 first lower aliases have an exact remainder test

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Gives an exact admissibility test for the unique
  lower first-layer alias: compute
  `S_Q == L_D B_1^{-1} mod Q_1`, then check its degree, root-freeness, and
  coprimality with `B_Q=(B_1S_Q-L_D)/Q_1`.
- **How it is useful:** Converts the nearest high-degree primitive alias
  obstruction from an existence-over-a-family question into a single
  checkable candidate.
- **What to do next:** Apply this remainder test to active primitive
  directions, and look for structural reasons the forced candidate cannot pass
  the admissibility checks.

### 2026-06-28 - M1 first alias layer is one-sided rigid

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that in the first high-degree alias layer
  `e_1+e_2=n+1`, if `e_2<e_1`, then a fixed primitive direction
  `(Q_1,B_1)` has at most one projective primitive alias of denominator degree
  `e_2`.
- **How it is useful:** Turns the nearest finite-domain alias obstruction into
  an existence problem for a single lower-degree candidate rather than a
  family of candidates.
- **What to do next:** Analyze when the forced residue
  `L_D B_1^{-1} mod Q_1` has the required degree, root-freeness, and
  coprimality properties.

### 2026-06-28 - M1 high-degree direction aliases are defect congruences

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that a high-degree primitive direction alias
  satisfies `B_1Q_2-B_2Q_1=L_D R` with `deg R<e_1+e_2-n`, and for fixed
  `(Q_1,B_1)` is equivalently controlled by
  `Q_2 == L_D R B_1^{-1} mod Q_1`.
- **How it is useful:** Gives the remaining finite-domain aliasing obstruction
  an explicit short-defect parameter and modular denominator congruence,
  making the first alias layer a constant-defect problem.
- **What to do next:** Use the defect congruence to count, rule out, or scan
  high-degree aliases in the active primitive class ledger.

### 2026-06-28 - M1 primitive evaluation fibers have a high-degree alias gap

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Records the consequence of low-total-degree
  primitive injectivity: distinct primitive residue-line data with the same
  divided evaluation datum must have denominator degrees `e,e'` satisfying
  `e+e'>n`.
- **How it is useful:** Separates the M1 active primitive ledger into a clean
  low/support-packing range and a genuinely high-total-degree finite-domain
  aliasing obstruction.
- **What to do next:** Use the gap to focus active-class counting on
  high-degree aliases or on structural arguments that rule those aliases out.

### 2026-06-28 - M1 low-total-degree primitive data are evaluation-injective

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that two primitive residue-line data with
  denominator degrees `e_1,e_2` satisfying `e_1+e_2<=n` are projectively equal
  if their divided direction and target evaluations agree on `D`.
- **How it is useful:** Removes finite-domain evaluation collisions from the
  low-total-degree active primitive class ledger; active class counting can be
  done at the level of primitive rational data in this range.
- **What to do next:** Use this injectivity range to separate low-degree
  active classes from genuinely high-degree finite-domain aliasing.

### 2026-06-28 - M1 active primitive classes are the remaining ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the fixed-class residue-line results into
  an active primitive-class closure criterion: a finite active family
  `A_prim` contributes at most the sum of explicit weights `W(deg Q_0)`, with
  low-degree primitive classes using the support-packing weight and all
  positive-degree classes bounded by `binom(n,j)`.
- **How it is useful:** Identifies the remaining all-line M1 problem after the
  fixed-class normal forms: bound the active primitive classes themselves;
  coefficient, exchange-multiplier, complement-root, and product-factor
  multiplicities have been removed inside each class.
- **What to do next:** Attack the active primitive class count using quotient
  periodicity, aperiodic packing, or denominator/residue-line structure.

### 2026-06-28 - M1 product split collapses to denominator coprimality

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Gives the direct inclusion-exclusion count for
  `P_v^x(Q_0)` over the distinct irreducible factors of `Q_0` and identifies
  it with the domain-root/root-free product-split sum.
- **How it is useful:** Clarifies that the `D`-root split is an accounting
  decomposition of the same denominator-coprime residual multiplier set, not
  an additional raw count.
- **What to do next:** Use the direct denominator-coprime count when comparing
  fixed-class residual multipliers with active all-line base-class budgets.

### 2026-06-28 - M1 exact residual product count with denominator coprimality

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Uses the canonical `D`-root split to give an exact
  finite-field count for `P_v^x(Q_0)`: sum over total domain-root
  multiplicity `s` of `binom(n+s-1,s) RFPhi_{D,Q_0}(R-s)`, with
  `RFPhi_{D,Q_0}` computed by inclusion-exclusion over `D` and the distinct
  irreducible factors of `Q_0`.
- **How it is useful:** Converts residual multiplier bookkeeping into a
  precise product-count ledger that also charges fixed denominator
  coprimality, rather than using a raw projective multiplier space.
- **What to do next:** Compare this fixed-denominator product count with the
  active all-line base-class/residue-line packing budget.

### 2026-06-28 - M1 residual products have canonical D-root split

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that the product map `([H],m) -> [H L_m]`
  from a root-free quotient `H` and a domain-root multiplicity vector `m` is a
  bijection onto the residual multiplier classes `P_v^x(Q_0)`.
- **How it is useful:** Removes artificial multiplicity from separately
  tracking root-free factors and support-side domain roots; the total residual
  product class is the canonical packet index.
- **What to do next:** Use the canonical product index to formulate the
  remaining all-line active base-class packing target.

### 2026-06-28 - M1 fixed-class complement-root dichotomy closes

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Combines the non-core normal form and root-heavy
  core descent into a single fixed-class complement-root dichotomy, with
  accounted bound
  `binom(n,j+u)(sum_{s=0}^u binom(j+u,s)+binom(j+u,u))`.
- **How it is useful:** Gives a compact closure statement: complement roots
  cost only explicit root choices before the residual becomes either a reduced
  product-class packet or a depth-zero core packet.
- **What to do next:** Move from fixed primitive classes to the all-line
  active base-class/residue-line packing problem.

### 2026-06-28 - M1 root-heavy landings descend to core packets

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that exchange-`u` landings whose multiplier
  has more than `u` roots in the current complement inject into a labeled
  depth-zero core ledger after choosing `u` of those roots.
- **How it is useful:** Closes the root-heavy alternative excluded by the
  fixed-class normal form; both complement-root branches are now explicit
  root-choice packet charges.
- **What to do next:** Combine the non-core and root-heavy branches into a
  compact fixed-class complement-root closure statement.

### 2026-06-28 - M1 fixed-class root residual normal form

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the complement-root machinery into an
  exact normal form: every non-core-descending exchange-`u` landing is a unique
  charged root set `S`, residual product class `[P]`, and reduced complement
  `C_0` with `P` nonvanishing on `C_0`.
- **How it is useful:** Converts the previous packet lemmas into a single
  fixed-class reduction theorem and isolates the core-depth descent as the
  only excluded root-heavy case.
- **What to do next:** Use the normal form to state which root-free product
  families must still be bounded for the all-line M1 residue-packing target.

### 2026-06-28 - M1 root-set stratification has only root-choice cost

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves a labeled root-set ledger bound: for any
  family of charged complement-root sets `S` and residual product classes
  `T_S`, the total ledger is bounded by
  `sum_S binom(n-|S|,j+u-|S|)`, equivalently
  `binom(n,j+u) sum_s binom(j+u,s)` when all sizes in a set are allowed.
- **How it is useful:** Separates the real cost of choosing complement-root
  charges from residual multiplier/root-free/support-root multiplicity in the
  fixed-class M1 ledger.
- **What to do next:** Use this root-choice cost formula to state a compact
  fixed-class residual reduction theorem.

### 2026-06-28 - M1 mixed root-free residual packets are product-disjoint

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that after a fixed complement-root deletion,
  a family with varying root-free twist `H` and varying residual multiplier
  `N` is still one small-complement packet whenever the total product classes
  `[HN]` are distinct.
- **How it is useful:** Combines the root-free twisting and support-root
  residual ledgers into one product-indexed packet, removing a possible
  artificial multiplicity from separating `H` and `N`.
- **What to do next:** Apply the product-indexed packet theorem to a global
  root-set stratification of the fixed-class M1 ledger.

### 2026-06-28 - M1 domain-root residuals are one packet

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Generalizes the budget-two and budget-three
  support-root slice closures: for any residual budget `R`, all pure
  domain-root residual multipliers of degree `<R`, with no root in the current
  complement, form one disjoint small-complement packet.
- **How it is useful:** Shows that support-side domain-root multiplicities are
  not a source of field-size or multiplier multiplicity in the M1 fixed-class
  residue ledger; the remaining difficulty is root-free moving-base packing
  and charging root-set choices.
- **What to do next:** Combine the lossless root shift and domain-root packet
  theorem into a sharper fixed-class/global root-free residual reduction.

### 2026-06-28 - M1 fixed root-deletion is lossless

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that for any fixed complement-root set `S`
  and any residual multiplier subfamily `T`, deleting `S` gives an exact
  multiplier-preserving bijection to the lower-depth packet restricted by
  `C_0 cap S=empty`.
- **How it is useful:** Isolates the lossless frontier-shift invariant behind
  the low-budget M1 packet closures; fixed root deletion contributes no
  field-size or square-root loss.
- **What to do next:** Use the lossless shift to separate the cost of choosing
  root sets from the residual packing problem.

### 2026-06-28 - M1 budget-three residuals split into two packets

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that at residual budget `R=3`, the
  root-free linear/quadratic total-multiplier branch occupies one
  small-complement packet, and the reduced no-root-free branch is the disjoint
  packet of support-root slices of total multiplicity at most two.
- **How it is useful:** Removes the apparent linear/quadratic multiplier
  multiplicity from the next residual budget after the budget-two closure.
- **What to do next:** Use these budget-two and budget-three packet closures
  to formulate the next global fixed-class M1 ledger reduction.

### 2026-06-28 - M1 reduced budget-two residual is core-or-root-slice

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that for any fixed twisted numerator
  `B_star`, the reduced residual-budget-two ledger is the disjoint union of
  the core packet and support-side domain-root slices, with total size at most
  `binom(n,j+v)`.
- **How it is useful:** After external anchors and complement roots are
  charged, the budget-two residual has no remaining unweighted multiplicity;
  it is core-or-root-slice.
- **What to do next:** Move from the closed budget-two ledger to the
  budget-three linear/quadratic twist branch.

### 2026-06-28 - M1 budget-two external-anchor packets are disjoint

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Closes the root-free part of the residual-budget
  two branch: for fixed complement-side root set `S`, all linear external
  anchor fibers are disjoint and have total size at most `binom(n,j+v)`.
- **How it is useful:** Turns the budget-two external-anchor residual into a
  single small-complement packet after deletion and twisting, rather than a
  field-size anchor multiplicity.
- **What to do next:** Analyze the remaining budget-two constant/support-side
  root-slice branch and the budget-three linear/quadratic twist branch.

### 2026-06-28 - M1 small residual budgets classify root-free types

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Specializes the residual degree credit to the
  first budgets: no nonconstant root-free factors survive at budget `R<=1`,
  only one external linear anchor can occur at `R=2`, and only linear or
  quadratic root-free twists can occur at `R=3`.
- **How it is useful:** Turns the combined deletion/twist normal form into a
  concrete low-slack template classification for the fixed-class M1 ledger.
- **What to do next:** Use the low-budget classification to close or scan the
  first residual `N`-ledgers.

### 2026-06-28 - M1 root-free factors spend residual degree

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Sharpens the commuting normal form by recording
  the degree credit: if `[L_S H N] in P_u^x(Q_0)` and `d=deg H`, then after
  deleting `S` and twisting by `H`, the residual multiplier satisfies
  `deg N < r_{u-s}-d`.
- **How it is useful:** Shows external linear factors and irreducible
  root-free factors shrink the residual multiplier budget rather than merely
  moving the base class.
- **What to do next:** Use the residual degree credit when bounding the
  remaining `N`-ledger after combined root deletion and twisting.

### 2026-06-28 - M1 complement deletion commutes with twisting

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves a one-step normal form: if
  `[L_S H N] in P_u^x(Q_0)`, `S subset D`, `|S|<=u`, and `H` is root-free on
  `D`, then deleting `S` identifies the fiber over `[L_S H N]` for `B_0` with
  the lower-depth fiber over `[N]` for the twisted numerator
  `B_H == B_0 H^{-1} mod Q_0`.
- **How it is useful:** Packages complement-root descent and root-free
  twisting into one commuting reduction, leaving only the lower-depth residual
  multiplier against the moving primitive base class.
- **What to do next:** Bound the residual multiplier ledger after this
  combined reduction, especially the support-side root-slice components.

### 2026-06-28 - M1 fixed-residual twist packets are disjoint

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that for fixed residual `N`, the fibers
  `Comp_{v,[N]}(Q_0,B_H)` obtained from root-free twists `H` are pairwise
  disjoint and have total size at most `binom(n,j+v)`.
- **How it is useful:** Shows moving root-free base twists do not create
  unweighted complement multiplicity within a fixed residual packet; their
  fibers are just the original disjoint fixed-base product fibers
  `Comp_{v,[HN]}(Q_0,B_0)`.
- **What to do next:** Combine fixed-residual packet disjointness with a
  bound on the remaining residual multipliers `N`.

### 2026-06-28 - M1 low-degree base twists are injective

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that for `1<=h<=e_0`, the map
  `[H] |-> [B_0 H^{-1} mod Q_0]` is injective on projective classes
  `[H] in P(F[X]_<h)` coprime to `Q_0`.
- **How it is useful:** Counts the moving base twists from root-free
  multiplier factors by actual low-degree factor classes; in particular,
  distinct linear external anchors give distinct twists when `e_0>=2`.
- **What to do next:** Use this injective twist ledger to bound the active
  moving-class family or combine it with quotient-periodic/aperiodic charges.

### 2026-06-28 - M1 root-free multiplier factors are base twists

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that if `[HN] in P_v^x(Q_0)` and
  `B_H == B_0 H^{-1} mod Q_0`, then
  `Comp_{v,[HN]}(Q_0,B_0)=Comp_{v,[N]}(Q_0,B_H)`.
- **How it is useful:** After domain-root drop/slice reductions, split
  external roots and irreducible bounded-degree factors become moving
  primitive base-class twists rather than hidden coefficient multiplicity
  inside one fixed class.
- **What to do next:** Bound or classify the resulting family of twists
  `B_H mod Q_0` in the active residue-line packing ledger.

### 2026-06-28 - M1 split domain roots are drop-or-slice data

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Stratifies split in-domain multiplier roots in a
  fixed complement fiber: roots in the complement lower exchange depth after
  deletion, while roots outside the complement remain as explicit
  fixed-root/root-slice data on the support side.
- **How it is useful:** Makes the `D\\C` residual from the complement-root
  descent exact, reducing split domain-root factors to lower-depth ledgers and
  root-slice charges before the external/irreducible multiplier pieces are
  attacked.
- **What to do next:** Analyze the remaining non-split multiplier pieces:
  external roots and irreducible bounded-degree factors.

### 2026-06-28 - M1 higher exchange coefficient cores charge to U_u

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that at every exchange depth `u`, any
  repeated `(a-u)` coefficient core for a fixed primitive base class has
  complement in the disjoint residue-line ledger `U_u`, giving
  `|Lambda_{Q_0,B_0}^{nc,>=a}(w_0)| <= binom(n,j)`.
- **How it is useful:** Upgrades the unweighted complement ledger into a
  weighted coefficient-incidence ledger, so the same `U_u` object controls
  both repeated support cores and multiplier landings.
- **What to do next:** Use the complement-root descent to analyze the
  non-descending part of `U_u`: core-depth roots, roots outside the current
  complement, external roots, and irreducible bounded-degree factors.

### 2026-06-28 - M1 split complement roots descend iteratively

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Generalizes root descent: if
  `[M]=[L_R N]`, `|R|<=u`, and all split roots `R subset D` lie in the
  complement, then deleting `R` bijects the exchange-`u` fiber for `M` with the
  exchange-`u-|R|` fiber for `N`.
- **How it is useful:** Shows split complement-root factors are lower-depth
  data until core depth is reached, isolating core-depth complement roots,
  roots outside the complement, external roots, and irreducible bounded-degree
  factors as the genuinely new multiplier pieces.
- **What to do next:** Analyze the non-descending multiplier factors or
  connect them to active M1 quotient-periodic/tangent ledgers.

### 2026-06-28 - M1 higher base complement ledgers are disjoint

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Extends the fixed-class complement ledger to every
  exchange depth `u<=t`: the projective multiplier fibers are disjoint and
  have total size at most `binom(n,j+u)`.
- **How it is useful:** Removes unweighted multiplier multiplicity at all
  fixed exact exchange depths, and proves in-domain complement roots descend
  from exchange depth `u` to `u-1` after deleting the root.
- **What to do next:** Analyze multiplier pieces with no root in the
  complement, especially external-root and irreducible bounded-degree factors.

### 2026-06-28 - M1 first-unpacked base one-exchange coefficients are q-free

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Uses the disjoint first-unpacked complement ledger
  to bound weighted coefficient-core incidence:
  `|Lambda| <= (binom(n,j+1)+j|U_1|)/(n-j) <= binom(n,j)`.
- **How it is useful:** Shows the fixed first-unpacked base class has no
  weighted one-exchange obstruction on the support-wise noncontained side;
  all linear landing types are controlled by the unweighted complement ledger.
- **What to do next:** Move from fixed-class incidence to active primitive
  class counting or to higher exchange depth `u>1`.

### 2026-06-28 - M1 first-unpacked base complement ledger is disjoint

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the first-unpacked fixed base class:
  the `(j+1)`-complement fibers over all projective linear multipliers are
  disjoint, so their union has size at most `binom(n,j+1)`.
- **How it is useful:** Shows that external anchors and repeated-domain roots
  do not create unweighted field-size multiplicity inside a fixed primitive
  base class; the descended domain-anchor core fiber is bounded by
  `binom(n,j)/(j+1)`.
- **What to do next:** Move from fixed-class unweighted ledgers to bounding
  active primitive classes or weighted incidences in the actual M1 geometry.

### 2026-06-28 - M1 domain-anchor base landings descend

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the first unpacked base layer, proves that
  domain-anchor complements for `M=X-beta` and `beta in C` are in bijection,
  after deleting `beta`, with a descended `j`-complement core fiber.
- **How it is useful:** Shows in-domain anchor landings are a support-star
  over an existing core fiber, so the remaining first-unpacked ledgers are
  the constant core complement fiber plus repeated-domain-root and external
  anchor linear landings.
- **What to do next:** Analyze the repeated-root and external-anchor fibers,
  or prove active M1 geometry charges them to tangent/endpoint ledgers.

### 2026-06-28 - M1 base collision landings dualize to complements

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Dualizes high-degree base collision certificates
  `L_I M in F B_0 mod Q_0` to small-complement fibers
  `L_C in F L_D M B_0^{-1} mod Q_0`, with disjoint multiplier fibers for
  exchange depth `u<=t`.
- **How it is useful:** Turns the hard high-degree fixed-class residual into
  explicit primitive small-complement ledgers and separates the first
  unpacked one-exchange layer into core, domain-anchor, repeated-root, and
  external-anchor landing types.
- **What to do next:** Bound these complement fibers or show that the active
  M1 geometry only admits quotient-periodic/contained instances.

### 2026-06-28 - M1 high-degree base collisions give residue landings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that collisions in a primitive base
  residue-line class force short certificates `L_I M in F B_0 mod Q_0`; at
  `a=k+t` and intersection `a-u`, one has `deg M<e_0-t+u`.
- **How it is useful:** Converts the high-primitive-degree range `e_0>t`
  into a bounded-degree residue-landing ledger; the first unpacked layer has
  only core or finite-anchor one-exchange landings.
- **What to do next:** Bound the resulting small-complement primitive landing
  fibers, separating in-domain anchors, external anchors, and
  quotient-periodic classes.

### 2026-06-28 - M1 primitive base residue classes have k+e packing

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Proves that a primitive fixed base residue-line
  class of denominator degree `e_0` has packing dimension `d_0=k+e_0`;
  distinct noncontained coefficients cannot share `d_0` support points.
- **How it is useful:** Gives an explicit fixed-class packing charge for
  `e_0<=t` at the scalar cutoff and a one-coefficient charge for `e_0<=t-j`,
  leaving only primitive classes of degree `>t` outside this local charge.
- **What to do next:** Attack the remaining high-primitive-degree active class
  ledger using aperiodicity, quotient-periodic exclusion, or denominator
  incidence constraints.

### 2026-06-28 - M1 base residue-line classes primitive-compress

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that a fixed base residue-line datum
  `QA+lambda B=w` has the same noncontained coefficient set after dividing
  by `G=gcd(Q,B)`: `(Q/G)A+lambda(B/G)=w/G`.
- **How it is useful:** Prevents nonprimitive presentations from being
  counted as new M1 active classes; the class ledger can restrict to
  primitive root-free residue pairs plus the polynomial endpoint.
- **What to do next:** Bound or classify the primitive aperiodic active
  residue-pair classes left after quotient-periodic and contained branches.

### 2026-06-28 - M1 fixed base residue lines are q-free when noncontained

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Divides any fixed root-free base-dimension
  residue-line datum `QA+lambda B=w` by `Q` and applies the rank-one
  noncontained support injection, giving at most `binom(n,j)` finite
  noncontained coefficients in that fixed datum.
- **How it is useful:** Sharpens the scalar M1 residual: no fixed scalar
  cutoff datum has field-size noncontained multiplicity; the remaining
  all-line task is to control active denominator/residue-line classes after
  tangent, contained, and quotient-periodic branches are charged.
- **What to do next:** Work directly on the active class ledger, especially
  aperiodic primitive residue-line classes and quotient-periodic exclusions.

### 2026-06-28 - M1 scalar cutoff leaves no enlarged-code noncontained residual

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the scalar cutoff split: standard and
  zero-tail short denominators reduce to base-dimension residue-line data,
  constant endpoint branches with no high-tail window or zero high tail are
  global/contained, and nonzero high-tail-line branches are q-free by
  Corollary 40.112.
- **How it is useful:** Removes the full enlarged-code scalar list as an M1
  residual; before the fixed base-line closure, the remaining scalar branch
  was the ordinary base-dimension residue-line datum.
- **What to do next:** Focus the M1 all-line effort on the base-dimension
  residue-line class ledger after tangent, contained, and quotient-periodic
  branches are charged.

### 2026-06-28 - M1 high-tail-line scalar branches are q-free when noncontained

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Applies the rank-one support injection to every
  short scalar high-tail-line branch after the chart normalization
  `QA+lambda B=w`, proving at most `binom(n,j)` support-wise noncontained
  finite parameters in each branch.
- **How it is useful:** This extends the q-free noncontained closure beyond
  the one-row `L=1` layer to all one-dimensional high-tail return branches;
  high-tail codimension is only needed for unrestricted list bookkeeping.
- **What to do next:** Reclassify the remaining M1 scalar residuals into
  base-dimension residue-line data, collapsed high-tail branches, and these
  q-free high-tail-line branches.

### 2026-06-28 - M1 rank-one noncontained branches close by support injection

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Strengthens the direct bound to any rank-one
  extension direction:
  `|Mu_phi^{nc,>=a}(Y)| <= binom(n,a)=binom(n,j)`, by injecting each
  noncontained coefficient into a chosen noncontained `a`-support.
- **How it is useful:** This shows the actual support-wise noncontained
  one-row branch is q-free by pure linear algebra, without any exchange-depth
  or residue-packing bookkeeping; the weighted residue ledgers are only for
  the unrestricted coefficient/list object.
- **What to do next:** Avoid spending further effort on one-row
  noncontained exchange bookkeeping unless it is needed for another residual;
  move to higher-row or non-one-row M1 branches.

### 2026-06-28 - M1 noncontained one-row witnesses truncate to threshold

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Shows that any support-wise noncontained one-row
  witness on `|S|>=a` contains a noncontained `a`-subsupport, so the exact
  support coefficient bound applies to the actual threshold predicate.
- **How it is useful:** This closes a possible gap between exact-support
  bookkeeping and line-MCA agreement-at-least-`a` witnesses.
- **What to do next:** Treat the positive primitive one-row noncontained
  branch as closed at this exchange scale and move to the next M1 residual.

### 2026-06-28 - M1 one-row noncontained chart closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Packages the preceding one-row analysis into a
  chart-level closure theorem: in a positive primitive one-row residual chart,
  the one-exchange support-wise noncontained finite parameters contribute at
  most `binom(n,j)/q` to the line-MCA density.
- **How it is useful:** This gives a paper-ready endpoint for the one-row
  one-exchange branch and identifies the remaining field-size family as a
  local-contained/tangent charge, not a noncontained M1 witness family.
- **What to do next:** Use this q-free chart closure as a base case before
  attacking higher-exchange collisions or non-one-row scalar residual charts.

### 2026-06-28 - M1 support-wise noncontained one-row residual is q-free

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Defines the support-wise noncontained one-row
  coefficient set `Mu_h^nc(Y,a)` and proves
  `|Mu_h^nc(Y,a)| <= (binom(n,j+1)+jU_comp)/(n-j) <= binom(n,j)`.
- **How it is useful:** This removes the remaining q-factor from the actual
  noncontained one-exchange one-row branch; double-collapse multiplicity is
  shown to belong only to locally contained supports.
- **What to do next:** Promote this as the one-row noncontained closure inside
  the broader M1 residue-line packing program, then attack higher-exchange or
  non-one-row residuals.

### 2026-06-28 - M1 local-contained-free one-row residual is q-free

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** If the local-contained double-collapse supports
  are absent or already charged, then the one-exchange one-row residual has
  no field-size factor:
  `|Mu_h(Y,a)| <= ((j+2)/(j+1)) binom(n,j) <= 2 binom(n,j)`.
- **How it is useful:** This isolates the exact source of q-multiplicity and
  gives a q-free bound for the aperiodic/local-contained-free one-row branch.
- **What to do next:** Prove that the double-collapse locus is contained in
  the tangent/quotient-periodic charge ledger, or bound it separately.

### 2026-06-28 - M1 one-row residual has a two-ledger closure criterion

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The double-collapse support count is decomposed on
  `j`-complements as the disjoint intersection of the ordinary locator fiber
  of `Y` with normalized generator-collapse residue fibers.  This gives the
  bound
  `|Mu_h(Y,a)| <= (binom(n,j+1)+(j+1)U_comp+a(q-1)D_int)/(n-j)`.
- **How it is useful:** It packages the one-exchange one-row residual into
  two explicit unweighted ledgers: `(j+1)` complement residue packing and
  `j`-complement double-collapse intersections.
- **What to do next:** Attack `D_int` directly, either by proving transverse
  intersection with ordinary locator fibers or by finding a quotient-periodic
  obstruction.

### 2026-06-28 - M1 weighted excess reduces to double-collapse supports

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Fixed-support coefficient multiplicity is
  classified exactly: it is larger than one precisely when both the one-row
  generator and the received word restrict to `RS_k` on the same `a`-support.
  The root-anchor excess then satisfies
  `E_root=a sum_T (m_T-1)_+ <= a(q-1)|DoubleColl_h(Y,a)|`.
- **How it is useful:** This converts the weighted one-exchange complement
  ledger into unweighted small-complement packing plus a named
  double-collapse support count.
- **What to do next:** Bound `DoubleColl_h(Y,a)` by combining the
  generator-collapse complement fiber with ordinary locator/list bounds for
  `Y`.

### 2026-06-28 - M1 root-anchor fibers descend after deleting the root

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** If `[M]=[(X-beta)N]` with `beta in D`, then
  deleting `beta` gives a bijection between complements
  `C in Comp_[M]` containing `beta` and degree-dropped `j`-complement fibers
  `L_C0 in F L_D N B_prim^{-1} mod Q_prim`.
- **How it is useful:** This turns root-anchor weighted excess into a
  lower-multiplier-degree packing target after charging the actual domain
  root.
- **What to do next:** Combine this degree descent with unweighted
  small-complement residue packing to control the root-anchor excess ledger.

### 2026-06-28 - M1 adjacent collapse is root-anchored

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** If a generator-collapse same-support obstruction
  is adjacent to a one-exchange exceptional complement `C in Comp_[M]`, then
  the added point `beta in C` is an actual root of the one-exchange multiplier:
  projectively, `[M]=[(X-beta)N]`.
- **How it is useful:** This localizes weighted-incidence excess to in-domain
  roots of low-degree one-exchange multipliers; root-free multiplier fibers
  contribute only the trivial `j+1` adjacent supports.
- **What to do next:** Bound or charge the root-anchor excess ledger after the
  unweighted small-complement residue fibers are packed.

### 2026-06-28 - M1 same-support multiplicity is generator collapse

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A fixed support has at most one one-row coefficient
  unless the generator `hX^k-B_prim/Q_prim` restricts to `RS_k` on that
  support; this collapse gives a `j`-point complement residue certificate
  with multiplier degree `<ell+1`, plus the necessary top-coefficient
  normalization.
- **How it is useful:** This identifies the same-support multiplicity missing
  from the weighted ledger as another small-complement residue-line problem.
- **What to do next:** Bound the `j`-point generator-collapse complement
  fibers together with the `(j+1)` one-exchange complement fibers.

### 2026-06-28 - M1 correction: one-row ledger needs weighted incidence

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Corrects the previous unweighted
  packing-with-exceptions ledger.  The valid bound uses the weighted
  coefficient-core incidence mass `R_exc`, and in complement form the weighted
  mass `R_comp`, not merely `sum_[M] |Comp_[M]|`.
- **How it is useful:** This prevents a false q-free coefficient bound from
  being consumed without a same-support multiplicity theorem.
- **What to do next:** Bound the weighted complement incidence mass, or prove
  a separate same-support uniqueness/multiplicity result.

### 2026-06-28 - M1 one-exchange one-row ledger in complement form

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM, corrected to weighted form above.
- **What is being added:** The one-exchange one-row coefficient bound is
  expressed in complement form using the weighted incidence mass
  `R_comp(Y,a)=sum_[M] sum_{C in Comp_[M]} r_{D\C}`.
- **How it is useful:** This gives the explicit ledger target for this branch:
  bound the weighted small-complement residue-line incidence mass.
- **What to do next:** Prove a polynomial bound for `R_comp`, or control
  same-support coefficient multiplicities separately.

### 2026-06-28 - M1 exceptional fibers dualize to small complements

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Each exceptional `(a-1)` agreement-core residue
  fiber is equivalent, via `C=D\I`, to a `(j+1)` split-complement residue-line
  fiber `L_C in F L_D M B_prim^{-1} mod Q_prim`.
- **How it is useful:** This rewrites the remaining one-row exceptional
  ledger using small complement locators, matching the M1 split-locator
  packing language more directly.
- **What to do next:** Apply quotient-periodic/aperiodic residue-packing
  estimates to these `(j+1)` complement fibers.

### 2026-06-28 - M1 exceptional one-row cores split into residue-line fibers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The exceptional one-exchange core ledger is the
  disjoint union over projective primitive low-degree multipliers `[M]` of
  split-locator fibers `L_I in F B_prim M^{-1} mod Q_prim`.
- **How it is useful:** This identifies the exact remaining one-row
  exceptional object as ordinary residue-line packing, with no hidden
  multiplier multiplicity once the core is fixed.
- **What to do next:** Bound the fiber sizes `Core_[M]` using the all-line
  aperiodic residue-packing strategy, after separating quotient-periodic
  fibers.

### 2026-06-28 - M1 one-exchange multipliers are primitive modulo Q

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Any nonzero exceptional one-exchange multiplier
  `M` is coprime to `Q_prim`; hence exceptional cores satisfy
  `L_I in F B_prim M^{-1} mod Q_prim` for an invertible low-degree
  multiplier.
- **How it is useful:** This removes a possible shared-factor branch from the
  one-row residual and makes the exceptional core ledger a clean residue-line
  landing problem modulo the primitive denominator.
- **What to do next:** Bound these invertible low-degree multiplier residue
  lines, or identify quotient-periodic families among them.

### 2026-06-28 - M1 one-row coefficients reduce to exceptional core incidence

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM, corrected to weighted form above.
- **What is being added:** If `Exc_ell` is the set of `(a-1)`-cores with a
  nonzero one-exchange multiplier certificate, then the valid coefficient
  bound uses `R_exc=sum_{I in Exc_ell} r_I`:
  `|Mu_h(Y,a)| <= (binom(n,a-1)-|Exc_ell|+R_exc)/a`.
- **How it is useful:** This converts the one-row residual into an ordinary
  `(a-1)` support-packing term plus an explicit weighted exceptional core
  incidence ledger.
- **What to do next:** Bound `R_exc`, not just the unweighted set `Exc_ell`.

### 2026-06-28 - M1 one-exchange residuals have unique multipliers

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the unpacked one-row residual
  `deg(Q_prim)=t+ell`, each fixed one-exchange core has multiplier space
  `{M: deg M<=ell+1, L_I M in F B_prim mod Q_prim}` of dimension at most one.
- **How it is useful:** One-exchange scalar collisions are therefore governed
  by a unique projective multiplier certificate per core, not by an
  uncontrolled family of slopes or multipliers.
- **What to do next:** Bound or charge these projective core multipliers,
  splitting the cases where the multiplier has domain roots, external roots,
  or irreducible factors.

### 2026-06-28 - M1 first-unpacked one-exchange collisions are anchor landings

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the first unpacked layer `deg(Q_prim)=t`, a
  one-exchange coefficient collision has multiplier degree `<2`, hence is
  either a core landing `L_I` or a finite-anchor landing `L_I(X-beta)` modulo
  the primitive denominator.
- **How it is useful:** This connects the scalar one-row residual directly to
  the boundary-off external-anchor normal form: external `beta` gives the
  same boundary-anchor object, while `beta in D` is an all-domain exchange.
- **What to do next:** Charge these first-unpacked anchor landings using the
  existing core/external-anchor ledgers, then attack higher `e_prim-t`.

### 2026-06-28 - M1 one-row collisions give short residue certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Any collision between two coefficients in the
  primitive one-row rational extension yields a short quotient certificate
  `L_I M in F B_prim mod Q_prim`, with `deg M<d_prim-|I|`.
- **How it is useful:** This turns the remaining one-row scalar residual from
  a vague list problem into the same residue-line landing object used in the
  M1 packing program; first-unpacked one-exchange collisions are linear
  residue landings.
- **What to do next:** Bound these short quotient residue certificates in the
  primitive high-denominator range, separating quotient-periodic and aperiodic
  intersection locators.

### 2026-06-28 - M1 one-row residual has primitive degree at least t

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** After primitive packing, the constant one-row
  branch is charged and any remaining positive one-row scalar branch has
  `deg(Q_prim)>=t`; equivalently the packing charge applies iff
  `deg gcd(Q,B)>=j-r_hw-t`.
- **How it is useful:** This identifies the exact scalar one-row residual
  left for genuine M1 aperiodic residue-packing input: primitive
  high-denominator branches only.
- **What to do next:** Attack the `deg(Q_prim)>=t` residual using quotient
  periodicity or all-line aperiodic residue-packing estimates.

### 2026-06-28 - M1 one-row cutoff packing criterion

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The primitive one-row packing bound is specialized
  to the MCA cutoff threshold `a=k+t`: packing applies exactly when
  `deg(Q_prim)<=t-1`, and the one-coefficient charge exactly when
  `deg(Q_prim)<=t-j-1`.
- **How it is useful:** This turns the one-row scalar residual into explicit
  cutoff inequalities and shows where primitive compression can make the
  residual chargeable in the M1 parameter ledger.
- **What to do next:** Determine whether quotient-periodic or aperiodic
  structure forces `deg(Q_prim)<t` in the remaining scalar cutoff cases.

### 2026-06-28 - M1 one-row primitive-degree packing bound

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** For the primitive one-row rational extension
  `RS_k+F(hX^k-B_prim/Q_prim)`, distinct slope coefficients cannot have
  agreement supports intersecting in `d_prim=k+deg(Q_prim)+1` points; hence
  the usual support-packing bound uses `d_prim`.
- **How it is useful:** This gives an actual q-free bound for the one-row
  scalar residual and shows that common factors in the original presentation
  lower the packing dimension before any global M1 estimate is invoked.
- **What to do next:** Combine this primitive-degree packing with
  quotient-periodic/aperiodic separation to see whether the surviving
  primitive denominator degrees are small enough in the scalar cutoff window.

### 2026-06-28 - M1 one-row rational extensions primitive-compress

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** For the one-row rational generator
  `hX^k-B/Q`, the reduced denominator is exactly `Q/gcd(Q,B)`; the numerator
  `hX^kQ-B` has the same gcd with `Q` as `B` does.
- **How it is useful:** This prevents nonprimitive one-row scalar
  presentations from being counted as new M1 packing objects and identifies
  the `B=0` case with the polynomial `RS_{k+1}` endpoint.
- **What to do next:** State the remaining one-row scalar packing problem only
  for primitive pairs `(Q_prim,B_prim)` with `gcd(Q_prim,B_prim)=1`.

### 2026-06-28 - M1 one-row layer is a rank-one rational extension

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The `L=1` short scalar layer, after division by
  the root-free denominator `Q`, is exactly list decoding against
  `RS_k+F(hX^k-B/Q)`, with parameter `lambda=-top(A)/h`.
- **How it is useful:** This names the exact rank-one rational extension left
  by the scalar one-row residual, connecting the cutoff analysis back to the
  all-line residue-packing target rather than an arbitrary enlarged-code list.
- **What to do next:** Prove or import a high-agreement packing bound for
  these one-generator rational extensions, with tangent/contained and
  quotient-periodic components charged separately.

### 2026-06-28 - M1 one-row scalar layer is a linear-image list

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the `L=1` short scalar layer with nonzero
  controlling high tail, the slope parameter is eliminated by the top
  coefficient: `QA+lambda B=w` and `top(A)=-lambda h` become
  `T_h(A)=w` for the injective linear map
  `T_h(A)=QA-(top(A)/h)B`.
- **How it is useful:** This isolates the only short scalar layer without
  high-tail codimension saving as a concrete `k+1` dimensional linear-image
  list, rather than a free two-parameter incidence.
- **What to do next:** Bound these one-row linear-image lists directly, or
  relate them to the tangent/high-agreement ledgers already charged in M1.

### 2026-06-28 - M1 short scalar return slices have dimension k+1

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** All positive short and constant scalar return
  slices with nonzero controlling high tail lie in a subspace
  `W_h={A: tau_K(A) in Fh}` of dimension `k+1`; each fixed parameter is an
  affine `k`-dimensional fiber.
- **How it is useful:** This makes the remaining short scalar obstruction an
  effective `k+1` dimensional high-tail-line list inside the enlarged code,
  with codimension `L-1` unless the high-tail window has length one.
- **What to do next:** Focus the short scalar analysis on the one-row tail
  layer `L=1` and on bounding list intersections with `W_h` for `L>=2`.

### 2026-06-28 - M1 constant scalar cutoff branch is high-tail supercode list

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT / PROOF-PROGRAM.
- **What is being added:** The `deg Q=0` scalar cutoff case is separated from
  positive-degree residue-line data.  It is a supercode endpoint branch in
  `RS[F,D,k+j-r_hw]` cut by the high-tail line equation
  `tau_K(R)=-parameter*tau_K(P)`, with the usual reciprocal zero-slope
  exception in the `Qf` case.
- **How it is useful:** This corrects the short-denominator split and prevents
  treating a constant scalar witness as a positive-degree residue-line datum.
- **What to do next:** Bound this one-direction supercode high-tail list or
  show the endpoint high tail vanishes in the relevant scalar cutoff cases.

### 2026-06-28 - M1 scalar cutoff non-standard range is short denominator

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** At the scalar half-window cutoff, the positive
  non-standard scalar range is exactly `1<=deg Q<j-r_hw`, and the return-slice
  high-tail length is `j-r_hw-deg Q`; if `r_hw>=j`, there is no non-standard
  scalar cutoff range.
- **How it is useful:** This localizes the remaining scalar obstruction to a
  finite short-denominator range in the actual M1 cutoff parameters.
- **What to do next:** Attack the short-denominator high-tail incidences or
  show that the relevant applications have `r_hw>=j`.

### 2026-06-28 - M1 non-standard scalar return slice is a high-tail line

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The non-standard scalar return slice is exactly the
  high-tail equation `tau_K(C')=-parameter*tau_K(H)`.  If the quotient high
  tail vanishes, the branch collapses to the base-dimension residue-line
  datum; otherwise the enlarged witness high tail determines the slope.
- **How it is useful:** This turns the remaining non-standard scalar case into
  a one-dimensional high-tail incidence inside an enlarged residue-line list,
  a concrete rank/counting target.
- **What to do next:** Bound enlarged residue-line witnesses whose high tails
  lie on this fixed line, or show large families force quotient-periodic or
  paired endpoint structure.

### 2026-06-28 - M1 non-standard scalar strata are enlarged residue lines

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the complementary range `n-s>k+deg Q`, scalar
  rational-supercode strata are exact degree-`deg Q` residue-line data over
  the enlarged code dimension `K=n-s-deg Q`, cut by the affine return slice
  requiring the enlarged-code explanation to lie back in `F[X]_<k` after the
  quotient part is restored.
- **How it is useful:** This classifies the remaining scalar cutoff case
  instead of leaving it as an opaque supercode-list obstruction.
- **What to do next:** Bound the return-slice incidence or show that large
  return-slice families force quotient-periodic, paired, or endpoint-global
  structure.

### 2026-06-28 - M1 scalar standard-degree strata are residue lines

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** In the range `n-s<=k+deg Q`, a scalar
  rational-supercode stratum is exactly a degree-`deg Q` residue-line datum
  after subtracting the global quotient part of the represented endpoint; the
  `Qf` case uses reciprocal slope `y=1/z` for nonzero slopes and leaves the
  original zero slope separate.
- **How it is useful:** This folds a substantial scalar cutoff case back into
  the existing M1 residue-line normal form, so it can be attacked by the same
  quotient/aperiodic machinery rather than treated as a new obstruction.
- **What to do next:** Separate the remaining non-standard range
  `n-s>k+deg Q` and determine whether it is absent at the relevant cutoff
  parameters or requires a longer-Pade analogue.

### 2026-06-28 - M1 scalar constrained-list parametrization is exact

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Unless the scalar endpoint numerator already lies
  in `QF[X]_<k`, the generator coefficient in the constrained multiplier-list
  parametrizes exactly the explained scalar slopes; if the numerator does lie
  in `QF[X]_<k`, the `Qg` branch is contained, while the `Qf` branch has no
  nonzero noncontained slope and still leaves the zero-slope exception.
- **How it is useful:** This turns the scalar cutoff branch into an exact
  constrained-list target, not just an injection, making future closure
  criteria precise.
- **What to do next:** Bound the exact constrained-list coefficient set, or
  prove that large coefficient sets force quotient-periodic or paired endpoint
  structure.

### 2026-06-28 - M1 scalar list image is a multiplier-code extension

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The scalar list injection lands not in the full
  `RS[F,D,d]` list but in `List_d(Qf,a) cap (QF[X]_<k+F P_g)` or
  `List_d(Qg,a) cap (QF[X]_<k+F P_f)`, a one-generator extension of the
  multiplier code.
- **How it is useful:** This sharpens the scalar cutoff target from generic
  supercode list decoding to a constrained subcode-list problem with a
  one-dimensional residue line modulo `Q`.
- **What to do next:** Try to prove list bounds for these multiplier-code
  extension lists, or show that a large such list forces quotient-periodic or
  paired endpoint structure.

### 2026-06-28 - M1 scalar rational-supercode list injection

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A scalar rational-supercode stratum with
  `d=max(n-s,k+deg Q)<=n` injects its noncontained slopes into an ordinary
  `RS[F,D,d]` list for the multiplied opposite endpoint; in the `Qf` case the
  zero slope is the only possible extra element.
- **How it is useful:** This gives a structural route for scalar cutoff-kernel
  failures after the support-packing guardrail: prove or import a list bound
  for the multiplied endpoint in the larger RS supercode.
- **What to do next:** Compare the induced dimension `d` and agreement `a`
  with available or conjectural L1/list bounds, and isolate whether the
  multiplied endpoint has additional quotient/aperiodic restrictions.

### 2026-06-28 - M1 scalar support-packing reserve guardrail

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT / PROOF-PROGRAM.
- **What is being added:** The scalar support-packing ledger
  `binom(n,d)/binom(a,d)` is polynomial only when `d=O(log n)` at fixed
  agreement fraction bounded away from one; for fixed-rate scalar strata
  `d>=k=rho n`, pure support packing is exponential.
- **How it is useful:** This prevents overclaiming from the packing bound and
  identifies the remaining scalar M1 task as genuinely structural: exclude the
  scalar kernels or force quotient/aperiodic, paired, or endpoint-global
  collapse.
- **What to do next:** Attack the scalar root-free cutoff kernels using active
  M1 geometry rather than relying on support-packing alone.

### 2026-06-28 - M1 scalar rational-supercode support-packing bound

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** Below the one-slope pairwise-intersection
  threshold, a scalar rational-supercode stratum with
  `d=max(n-s,k+deg Q)<=a` has at most
  `floor(binom(n,d)/binom(a,d))` noncontained finite slopes.
- **How it is useful:** This converts the remaining scalar cutoff-kernel
  failures into an explicit support-packing ledger rather than a raw
  field-size slope count.
- **What to do next:** Compare this packing charge with the M1 reserve and
  isolate whether the remaining hard range is `d>a` or packings too large for
  the desired bound.

### 2026-06-28 - M1 scalar rational-supercode strata pairwise charge

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A one-sided scalar rational-supercode stratum
  `Qf in RS[F,D,n-s]` or `Qg in RS[F,D,n-s]` contributes at most one
  noncontained finite slope whenever `2a-n>=max(n-s,k+deg Q)`.
- **How it is useful:** This charges scalar cutoff-kernel failures in the
  high-agreement range by using pairwise support intersections, complementing
  the paired one-slope charge.
- **What to do next:** Compare the M1 cutoff parameters with the displayed
  threshold to identify which scalar failures remain genuinely uncharged.

### 2026-06-28 - M1 paired rational-supercode strata charge to one slope

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A paired rational-supercode denominator `Q` with
  `Qf,Qg in RS[F,D,n-s]` forces any explained slope above the interpolation
  threshold `a>=max(n-s,k+deg Q)` to be a global codeword; hence a
  noncontained line contributes at most one such slope.
- **How it is useful:** This gives a concrete charge for ordinary and shifted
  paired half-window cutoff-kernel failures when their denominator degree is
  below the interpolation threshold.
- **What to do next:** Identify whether the remaining paired cutoff failures
  always fall below this threshold, or isolate the larger-degree cases for
  quotient/aperiodic charging.

### 2026-06-28 - M1 cutoff kernels are rational-supercode strata

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A coding interpretation of cutoff kernel failure:
  `H_{s,m-1}(Syn(y))Q=0` iff the pointwise product `Qy` lies in the larger RS
  supercode `RS[F,D,n-s]`; root-free `Q` gives a rational representation
  `y=P/Q`.
- **How it is useful:** This identifies the remaining half-window minor
  obstruction as a low-degree rational-supercode stratum for one or both line
  endpoints, which is the kind of object quotient-periodic or aperiodic M1
  structure might charge.
- **What to do next:** Relate these rational-supercode strata to the active
  noncontained line geometry and determine when they are quotient-periodic,
  tangent, or genuinely aperiodic.

### 2026-06-28 - M1 cutoff-minor obstruction is syndrome-realizable

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** A guardrail for the four cutoff-minor target: if
  `|D|>=s+1`, one can choose nonzero local syndrome weights whose first `s`
  moments vanish, making the root-free constant polynomial `1` lie in all
  four cutoff kernels simultaneously.
- **How it is useful:** This shows the cutoff-minor route cannot be closed by
  row counts, moment expansions, or generic syndrome normalization alone; it
  must use active M1 geometry or quotient/aperiodic structure.
- **What to do next:** Look for the missing active-M1 input that prevents this
  constant-recurrence obstruction in the actual noncontained line setting.

### 2026-06-28 - M1 four cutoff minors close half-window route

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The exact half-window injectivity target is
  converted into four explicit full-column minor tests at the first
  half-window cutoff depth.  If one `m x m` minor is nonzero for each cutoff
  map with `m=h-L`, the root-free half-window ledger is at most
  `4 RFPhi_D(L)`.
- **How it is useful:** This gives a concrete scanner/proof target for the
  M1 half-window route: four Hankel minor nonvanishing checks after
  fixed-root/root-slice pieces are separated.
- **What to do next:** Try to prove these minors are nonzero from the active
  M1 syndrome structure, or run targeted scans to find whether a minor can
  fail outside charged fixed-root slices.

### 2026-06-28 - M1 half-window injectivity exact after fixed-root charges

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** A finite-field hyperplane-cover lemma shows that
  for `|D|<q`, a nonzero cutoff kernel with no common domain root always has a
  root-free element.  Hence, after fixed-root/root-slice charges, the
  half-window low-degree denominator target is equivalent to injectivity of
  `A_F(h-L)`.
- **How it is useful:** This upgrades the half-window injectivity test from a
  sufficient shortcut to the exact remaining target in the multiplicative M1
  regime, modulo already-separated fixed-root pieces.
- **What to do next:** Try to prove the four cutoff maps `A_F(h-L)` are
  injective on the charged-free ledger, or identify the fixed-root slice that
  accounts for any nonzero kernel.

### 2026-06-28 - M1 half-window root-slice kernel count

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The low-degree root-free cutoff kernels from the
  half-window denominator test are counted exactly by inclusion-exclusion over
  domain root slices, with each slice identified with a stripped Hankel kernel
  for `Delta_J u`, `Delta_J v`, or the shifted pair.
- **How it is useful:** This turns the condition `delta_F>=h-L` into an
  exact finite root-slice rank identity that can be audited or scanned, rather
  than only using the stronger injectivity shortcut.
- **What to do next:** Compute or prove these stripped-rank identities for
  the four active M1 cutoff families, starting with small `L`.

### 2026-06-28 - M1 half-window low-degree kernel test

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM.
- **What is being added:** The half-window primitive denominator threshold is
  recast as a cutoff Hankel kernel test: `deg D_F<m` holds exactly when the
  corresponding cutoff map has a nonzero root-free recurrence of degree
  `<m`; injectivity on degree `<h-L` is a concrete sufficient condition for
  the `4 RFPhi_D(L)` half-window ledger.
- **How it is useful:** This turns the half-window side of the M1 residual
  bottleneck into a finite rank target at the single cutoff depth, parallel to
  the bottom-route rank certificates.
- **What to do next:** Attack the four maps `A_F(h-L)` in actual M1
  instances, separating domain-root/root-slice kernels from genuine root-free
  low-degree recurrences.

### 2026-06-28 - M1 dual-gcd obstruction is syndrome-realizable

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** The formal trivial-gcd weights from the
  dual-annihilator limitation are shown to be realizable as local
  Reed-Solomon syndrome windows after absorbing the nonzero parity-check
  column scalars into the supported word values.
- **How it is useful:** This confirms that the bottom dual-gcd route needs
  special active-M1 syndrome structure; arbitrary local syndrome windows do
  not force the needed common roots.
- **What to do next:** Decide whether actual active M1 bottom syndromes have
  extra relations producing common roots, or shift effort to the half-window
  denominator route.

### 2026-06-28 - M1 dual-gcd limitation

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** A limitation for the dual-gcd bottom route: when
  `|D|>=s+2` and `h>=2`, there are formal moment weights whose scalar and
  paired dual annihilators contain both `1` and `X`, hence have common gcd
  `1`; with `0 notin D` the same holds for shifted paired annihilators.
- **How it is useful:** This prevents overclaiming the bottom-anchor route:
  the required common roots are genuine M1 structure, not a consequence of
  dimensions or moment formalism alone.
- **What to do next:** Either prove special common-root structure for actual
  M1 bottom syndromes or prioritize the half-window denominator route.

### 2026-06-28 - M1 dual-gcd bottom ledger

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** The scalar, paired, and shifted paired
  short-window dual annihilators are packaged into a bottom-route ledger.  If
  `a_F` is the number of distinct non-domain roots of the corresponding common
  gcd, then the family contributes at most `RFPhi_D(h-a_F)`, with zero
  contribution when the annihilator is zero or the gcd has a domain root.
- **How it is useful:** The bottom common-factor route is reduced to proving
  non-domain root lower bounds, or finding domain roots, for four explicit
  low-moment annihilator gcds.
- **What to do next:** Attack those four dual gcds in actual M1 bottom
  instances; failure to produce enough roots is evidence for using the
  half-window denominator route instead.

### 2026-06-28 - M1 short-window paired dual anchor test

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** The paired dual anchor test is extended to the
  genuinely short window `h<|D|`: a truncated anchor vector lies in the
  moment image of the short-multiplier space iff every degree-`<h` polynomial
  annihilating the `mu` and `nu` weighted moments through order `s-1` vanishes
  at the anchor.
- **How it is useful:** This makes the active M1 bottom-anchor search a
  common-gcd problem for an explicit degree-`<h` annihilator space, without
  relying on the full-domain Lagrange specialization.
- **What to do next:** Bound or falsify the common gcd of this short-window
  annihilator in actual M1 bottom families.

### 2026-06-28 - M1 full-domain paired dual anchor test

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Full-domain paired anchors are characterized by a
  dual annihilator space: `lambda_beta` lies in
  `mu P_<s + nu P_<s` iff every degree-`<n` polynomial whose `mu` and `nu`
  weighted moments vanish through order `s-1` also vanishes at `beta`.
- **How it is useful:** Anchor counting becomes a common-gcd degree problem
  for an explicit low-moment annihilator space, unless the paired row space is
  already full rank and the bottom kernel is zero.
- **What to do next:** Bound the common gcd of this annihilator in actual M1
  instances, or use it as a falsification target for the bottom-anchor route.

### 2026-06-28 - M1 full-window Lagrange anchor test

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** In the full-domain moment window `h=|D|`, a
  non-domain bottom anchor is equivalent to a Lagrange interpolation degree
  test: scalar anchors require `mu_x C(x)=lambda_beta(x)` on `D`, and paired
  anchors require `mu_x C_u(x)+nu_x C_v(x)=lambda_beta(x)`.  For `h>=|D|+1`,
  non-domain anchors from `D`-supported moment data are impossible.
- **How it is useful:** This sharply separates the bottom-anchor route into a
  short-window problem and an exact full-window interpolation test, ruling out
  one class of misleading long-window anchor searches.
- **What to do next:** Focus any computational or analytic anchor search on
  the genuinely short-window regime `h<|D|`, or on the displayed Lagrange
  degree tests at `h=|D|`.

### 2026-06-28 - M1 bottom-anchor moment certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Bottom anchor row membership is rewritten as a
  short-multiplier truncated moment certificate.  For scalar windows, this is
  `sum_{a<s} c_a w_{a+b}=beta^b`; with a moment expansion it becomes
  `sum_x mu_x C(x)x^b=beta^b` for `0<=b<h`, with paired and shifted variants.
- **How it is useful:** This makes the anchor-span route an explicit
  quadrature problem on the actual syndrome moments, rather than an abstract
  row-space condition.
- **What to do next:** Try to prove or falsify the existence of many
  non-domain external point-mass certificates for the four bottom families.

### 2026-06-28 - M1 rank-matched anchor windows

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** If a nonzero bottom kernel has row-space rank
  `rho` and contains `g` distinct non-domain evaluation rows, then the bottom
  root-free family is bounded by `RFPhi_D(h-g)`.  If `g=rho`, the row space is
  exactly their span and the count is exact.
- **How it is useful:** This converts the external-anchor rank tests into a
  quantitative bottom-route certificate: a rank-`h-L` span of `h-L`
  non-domain anchors gives the ideal `RFPhi_D(L)` contribution.
- **What to do next:** Try to establish these rank-matched anchor spans for
  the actual four bottom Hankel matrices, or use failure as evidence that the
  half-window denominator route is the better M1 path.

### 2026-06-28 - M1 external-anchor common-root duality

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** For any bottom matrix `A` with kernel `K`,
  `ev_beta in row(A)` is shown equivalent to every `Q in K` vanishing at
  `beta`, i.e. `X-beta | gcd(K)`.  Higher multiplicity is detected by
  Hasse-jet rows.
- **How it is useful:** This makes split common-factor certificates directly
  searchable by one-row rank tests along the rational normal curve, while
  separating domain roots as empty root-free families.
- **What to do next:** Use the rank test to hunt for enough non-domain
  external anchors in the actual four bottom matrices, or prove a structural
  reason they must occur.

### 2026-06-28 - M1 split-anchor bottom certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Split bottom row-span certificates are identified
  with external-anchor evaluation rows: if
  `G=prod_i (X-beta_i)` is squarefree and split, then
  `row(Rem_G)=span(ev_{beta_i})`; repeated roots give the corresponding
  Hasse-jet rows after scalar extension.
- **How it is useful:** This ties the bottom common-factor route back to the
  external-anchor geometry of the PR.  For each nonzero bottom family, a large
  split common factor is now a concrete claim that many non-domain evaluation
  rows already lie in its actual bottom Hankel row span.
- **What to do next:** Try to prove or falsify existence of these external
  anchor row spans in the actual bottom matrices; if certificates are
  nonsplit, isolate the Galois/Hasse-jet replacement.

### 2026-06-28 - M1 bottom row-span certificates

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** The bottom common-factor residual-window target is
  recast as an exact Hankel row-span certificate: for a monic divisor `G` of
  degree `g`, `K_0(F) subset G F_q[X]_{<h-g}` is equivalent to
  `row(Rem_G) subset row(A_0(F))`, or the stacked rank equality
  `rank A_0(F)=rank[A_0(F); Rem_G]`.
- **How it is useful:** This turns the abstract gcd condition in the M1 bottom
  route into a finite determinantal target on the actual bottom Hankel
  matrices, matching the Hankel-pencil direction requested for M1.
- **What to do next:** Search for or prove these row-span certificates in the
  four bottom kernels; failure for small `L` would falsify the current bottom
  route and redirect effort to the half-window arrangement route.

### 2026-06-28 - M1 common-factor route minimum

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** The bottom common-factor residual-window estimates
  are plugged back into the M1 ladder bottleneck.  In the multiplicative-domain
  case the residual ledger is refined to
  `min(BCF_0, Charge(P_pre)+RFArrBudget_hw)+2h`, where `BCF_0` is the sum of
  root-free common-factor window charges over the four bottom kernels.
- **How it is useful:** This turns the current M1 route into two explicit
  parallel structural targets: prove small common-factor residual windows in
  the bottom kernels, or prove a small root-free half-window tail arrangement
  together with the chosen pre-half charge.
- **What to do next:** Attack one of these structural targets in the actual
  M1 kernels, rather than adding further abstract ledgers.

### 2026-06-27 - M1 boundary-off external-anchor normal form

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_boundary_off_external_anchor_normal_form.md`,
  `experimental/experiments.tex`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** A local normal form for the one-outside
  `Boundary_off` target from the M1 variable-line packet lemma.  Writing a
  boundary target as `S union {beta}`, the Hankel landing condition becomes a
  one-variable external-anchor gate with quadratic minors in `beta`; for each
  fixed domain shadow `S`, either there are at most two external anchors or the
  full anchor pencil is a ruled rank-one artifact with common image or common
  kernel.  The nondegenerate branch is reduced to the first boundary-shadow
  image of the active locator family, and the common-image ruled branch is
  converted into explicit lower/upper row-cut equations on the shadow locator.
  The anchor quadrics are also expanded into constant, mixed, and quadratic
  Hankel-wedge coefficients, giving a concrete ruled-shadow test.  The
  common-kernel ruled branch is further identified as a fixed-slope boundary
  kernel slice, or as a boundary-contained pencil in the endpoint case.  On
  the common-image side, full shadow stars are shown to be evaluation row cuts,
  and star-free rank-one row cuts gain a fixed root-slice factor over the bare
  one-root-loss bound.  Finally, a polynomial-field closure criterion records
  that the reduced boundary-off target set is bounded by twice the
  nondegenerate shadow ledger plus `q=|F|` times the three ruled shadow ledgers.
  The common-image shadow ledger is further made rank-testable: a fixed
  projective image line with row-cut direction dimension `d_I` contributes at
  most `binom(n,d_I)` split shadows, so bounded direction dimension closes that
  branch in the bounded-slack polynomial-field window.  The finite
  common-kernel and endpoint-contained ruled ledgers get the same treatment:
  fixed-slope and endpoint row-cut systems with direction dimensions `d_z` and
  `d_infty` contribute at most `binom(n,d_z)` and `binom(n,d_infty)` shadows.
  For finite slopes, the low-rank locus also satisfies a determinantal
  dichotomy: at rank threshold `b`, either there are at most `m-b` exceptional
  slopes with `d_z>b`, or the row-cut pencil is persistently low-rank.
  If the persistent alternative is absent, then after the exceptional slopes
  are charged to the fixed-slope/root-slice ledger, the bounded-rank finite
  common-kernel residual contributes at most `q^2 binom(n,b)` boundary targets.
  If the persistent alternative is present algebraically, it is equivalent over
  `F(z)` to `b+1` independent polynomial moving-kernel certificates killed by
  both shifted Hankel equations.
  The persistent alternative also forces endpoint low rank: both the `H(u)` and
  `H(v)` shifted endpoint row-cut systems have direction dimension `>b`, and a
  moving kernel gives an explicit coefficient ladder from the `u` endpoint to
  the `v` endpoint.
  The common-image low-rank locus is likewise made projective-determinantal:
  for image line `[y]`, `d_I>b` is cut out by minors of the wedge map
  `Q -> y wedge H(w)ell_Q^sigma`; outside that locus, the common-image
  contribution is at most `q ((q^t-1)/(q-1)) binom(n,b)`.
  Combining the rank ledgers, after charging slopes with `d_z>b`, image lines
  with `d_I>b`, and assuming `d_infty<=b`, the uncharged ruled boundary-off
  targets are bounded by
  `(q^2 + q + q((q^t-1)/(q-1))) binom(n,b)`.
  A root-free row-rank refinement shows that, after common-root subledgers are
  charged to fixed-root/root-slice ledgers, any positive-dimensional affine
  row-rank stratum of direction dimension `d` contributes at most
  `(d/m) binom(n,d)` split shadows instead of the bare `binom(n,d)`.
  On the nondegenerate side, popular adjacent shadows are charged to the first
  three active exchange profiles: `Boundary_off^quad` is bounded by twice the
  unique-neighbor nondegenerate shadows plus `2(N_1E_1+N_2E_2+N_3E_3)`.
  A separated-family sharpness lemma shows this residual is real for exchange
  bookkeeping: if `E_1=E_2=E_3=0`, then all first boundary shadows are unique
  and `|Shadow_1(A)|=|A| binom(j,2)(n-j)`.
  A quadratic full-anchor-star test shows that, for a fixed external anchor,
  any row-pair minor vanishing on all shadows through a domain root `alpha`
  has the evaluation factor `L_S(alpha)`; hence full anchor stars are
  fixed-root/root-slice charges rather than a new aperiodic residual.  Since
  anchor minors are quadratic, repeated full stars are classified exactly: two
  distinct full stars force a scalar multiple of
  `L_S(alpha_1)L_S(alpha_2)`, and three force the minor to vanish identically.
  The full-star proof now isolates the finite interpolation input as a
  quadratic cofactor Vandermonde lemma: degree-`<=2` functions on monic
  degree-`r` locators are determined by the degree-`r` cofactors of any
  `(r+2)`-set.
  A complementary core-line bound is added for each fixed anchor minor: after
  charging `(m-1)`-cores on which the one-root extension polynomial vanishes
  identically, the remaining split zeros contribute at most
  `(2/m) binom(n,m-1)`.
- **How it is useful:** This sharpens one of the two live residual objects in
  the non-fixed variable-line branch.  It does not prove the final M1 bound,
  but it turns the boundary image into a precise quadratic-anchor/ruled-branch
  incidence target and states exactly which reduced shadow estimates would
  close this boundary-off piece in the polynomial-field regime.  It also
  isolates low-rank Hankel row-cut loci as the remaining ruled-branch
  obstructions and separates finite exceptional slopes from persistent
  low-rank pencil degeneracy, giving a polynomial closure route for the
  bounded-rank part and a concrete algebraic certificate for the persistent
  part.  It further shows that the persistent finite-slope case is not a new
  free-floating obstruction: it must be charged through endpoint low-rank
  ledgers.  The common-image branch is similarly reduced to a bounded-rank
  polynomial residual plus an explicit projective low-rank locus.  The latest
  combined corollary packages these into a single bounded-rank ruled-branch
  closure criterion, and the root-free refinement gives that bounded-rank
  residual a fixed-root saving once common-root pieces have been charged.  The
  nondegenerate branch is also sharpened: popular shadows are now
  active-codegree terms, leaving unique-neighbor shadows as the named residual,
  and the separated-family lemma shows that residual cannot be removed using
  low-exchange information alone.  The full-anchor-star test then removes the
  most obvious Hankel degeneracy from that residual by charging it to
  fixed-root/root-slice factors, with repeated full-star factors completely
  classified for each anchor minor.  The cofactor interpolation lemma makes
  this finite-star step auditable as a standalone quadratic interpolation
  fact.  The core-line bound further reduces each fixed-anchor minor's
  star-free zero set to a one-root-loss ledger plus explicit identically
  vanishing core-line degeneracies.  Those core-line degeneracies now have an
  explicit lower anchor-coefficient ledger: for a fixed `(m-1)`-core `R`, the
  restricted minor along `R union {Y}` expands as
  `W(A,C)-Y(W(B,C)+W(A,D))+Y^2 W(B,D)`, where `A,C` come from
  `(X-beta)X L_R` and `B,D` from `(X-beta)L_R`.  Hence an identically
  vanishing core-line is exactly three lower-dimensional Hankel-wedge
  coefficient equations.  When the whole rank-one anchor gate vanishes on the
  core-line, the obstruction is classified one level lower: it is either a
  `u`- or `v`-endpoint containment, a common-image line, or a fixed projective
  kernel with `C=lambda A` and `D=lambda B` for the two core-shift locators.
  The core-line reduction is now stated for the full rank-one gate, not just a
  fixed minor: for each external anchor `beta`, after charging cores on which
  the whole gate is identically rank one, the remaining rank-one shadows are
  bounded by `(2/m) binom(n,m-1)`.  Those charged full core-line ledgers also
  have row-rank certificates one level lower: endpoint, fixed-kernel, and
  projective-image systems on monic degree-`m-1` core locators contribute at
  most `binom(n,e)` split cores per direction dimension `e`, so bounded lower
  direction dimension gives a polynomial full-core charge.  The full core-line
  classification proof was also audited locally: in the two-dimensional
  `span{A,B}` case the fixed-kernel conclusion now follows directly from the
  three coefficient equations `A wedge C=0`, `B wedge D=0`, and
  `A wedge D+B wedge C=0`.  The lower fixed-kernel full-core ledger now has
  its own finite-slope low-rank dichotomy: for fixed `beta`, either at most
  `c-b` slopes have direction dimension `>b` on degree-`c=m-1` core locators,
  or the lower core pencil is persistently low-rank for every slope.  Outside
  the exceptional slopes, this gives a `q binom(n,b)` core bound before the
  extension factor to shadows.  The persistent lower-kernel alternative is now
  certificate-form as well: it forces both lower endpoint core systems to have
  direction dimension `>b`, and moving core kernels satisfy the endpoint ladder
  `R_v q_0=0`, `R_v q_i-R_u q_{i-1}=0`, `R_u q_D=0`.  The lower common-image
  full-core ledger is now also projective-determinantal: low-rank image lines
  are cut out by homogeneous minors in `[y]`, outside that locus each image
  line contributes at most `binom(n,b)` cores, and the fully persistent case is
  recorded as a moving-image core certificate.  These lower ledgers are now
  packaged into a fixed-anchor full-core closure criterion: after lower
  endpoint, fixed-kernel, projective-image, and moving-certificate charges, the
  remaining full-gate shadows for that anchor are bounded by the Corollary 25
  one-root-loss residual plus
  `(n-m+1)(2+q+(q^t-1)/(q-1)) binom(n,b)`.  A lower root-free refinement now
  shows that, after common-root lower core pieces are charged, any positive
  direction dimension `e` contributes at most `(e/c) binom(n,e)` cores for
  `c=m-1`; hence the bounded-rank full-core term gains a `b/c` factor in the
  range `1<=b<=n/2`.  The lower endpoint charges now also have an
  anchor-dichotomy: for each endpoint `w`, either at most `c-b` anchors have
  endpoint core dimension `>b`, or the affine endpoint-anchor pencil is
  persistently low-rank and admits moving endpoint-core certificates over
  `F(beta)`.  The lower finite fixed-kernel exceptions are also now global in
  the anchor-slope plane: for `(beta,lambda)`, the lower direction matrix has
  entries of bidegree at most `(1,1)`, so the locus with core direction dimension
  `>b` is cut out by minors of total degree at most `2(c-b)`.  If it is not
  identically persistent, it has at most `2(c-b)q` anchor-slope pairs; the
  persistent case is recorded as moving two-parameter core certificates over
  `F(beta,lambda)`.  The lower common-image exceptions now have the analogous
  global anchor-image incidence form over `F x P(F^t)`: the bad pairs
  `(beta,[y])` are cut out by minors of total degree at most `2(c-b)`, giving at
  most `2(c-b)q^t/(q-1)` rational anchor-image pairs unless the incidence is
  identically persistent, in which case it is recorded as moving certificates
  over `F(beta,y)`.  These global charges now combine into an all-anchor
  full-gate incidence closure: after endpoint-bad anchors, bad anchor-slope
  pairs, bad anchor-image incidences, persistent certificate ledgers, and
  common-root lower core pieces are charged, the uncharged root-free incidence
  is bounded by
  `q(2/m)binom(n,m-1) + q(n-m+1)(2+q+(q^t-1)/(q-1))(b/c)binom(n,b)`.
  The anchor projection is no larger than this incidence bound.  A direct
  anchor-multiplicity lemma now also isolates globally full two-variable
  core-lines: for each non-global `(m-1)`-core `R`, at most two anchors make the
  whole core-line full.  After globally full cores are charged, the all-anchor
  full-core incidence is therefore at most `2(n-m+1)binom(n,m-1)`, and together
  with the Corollary 25 residual this gives
  `((2q)/m + 2(n-m+1))binom(n,m-1)` for rank-one incidences with no globally
  full core.  The globally full cores themselves are now classified as
  three-shift ruled pencils: either the `u` or `v` three-shift endpoint vanishes,
  all six vectors `H(u)X^iL_R,H(v)X^iL_R` lie in one image line, or
  `H(v)X^iL_R=lambda H(u)X^iL_R` for `i=0,1,2`.  Thus they admit the same
  endpoint/common-image/fixed-kernel row-rank bounds, with
  `(2+q+(q^t-1)/(q-1))binom(n,b)` in bounded dimension and the usual root-free
  `b/c` improvement after common-root charges.  The high-dimensional three-shift
  charges are now determinantal too: finite slopes obey the same `c-b`
  finite-exception/persistent dichotomy, persistent slopes force both
  three-shift endpoint systems low-rank, and moving kernels satisfy the endpoint
  ladder `G_v q_0=0`, `G_v q_i-G_u q_{i-1}=0`, `G_u q_D=0`.  The three-shift
  common-image bad lines are cut out by homogeneous minors with at most
  `(c-b)q^(t-1)/(q-1)` projective lines unless persistent.  The endpoint and
  fixed-kernel three-shift ledgers are now identified with exact deeper Hankel
  windows: `H_{t,j}(w)X^iQ=0` for `i=0,1,2` is equivalent to
  `H_{t+2,c-1}(w)Q=0`, so `G_lambda=H_{t+2,c-1}(v-lambda u)`.  This records a
  lossless residual-depth frontier shift from `(t,j)` to `(t+2,j-2)`.  The
  identity now has the general consecutive-shift form
  `H_{t,c+r-1}(w)X^iQ=0` for `0<=i<=r` iff `H_{t+r,c-1}(w)Q=0`, so a
  consecutive frontier stack consumes a deeper endpoint rank bound once rather
  than introducing a per-shift algebraic loss.  The finite-slope charge now has
  the matching no-loss dichotomy: the bad set for
  `H_{t+r,c-1}(v-lambda u)` has size at most `c-b`, unless the deeper endpoint
  maps for `u` and `v` both have kernel dimension `>b` and a moving-kernel
  endpoint ladder appears.  The common-image reduction is
  now stable under the same consecutive shifts: the sliding space in
  `F^{t+r}` is nonzero only on the same `q+1` extended geometric shift lines,
  so off that curve the stack is the deeper endpoint intersection and on the
  curve it is a first-difference or infinity endpoint ledger.  The finite
  first-difference parameters have the same determinant dichotomy:
  `J_theta^(r)` has at most `c-b` high-dimensional parameters unless the
  ordinary and shifted stacked endpoint maps are both high-dimensional and a
  moving first-difference ladder appears.  These pieces now package into an
  additive consecutive-frontier closure: under the four endpoint checks
  `ker H_{t+r,c-1}(u)`, `ker H_{t+r,c-1}(v)`, `ker B^(r)`, and `ker A^(r)`
  having dimension `<=b`, charging at most `2(c-b)` finite parameter systems
  leaves all uncharged finite fixed-kernel and consecutive common-image
  frontier ledgers with direction dimension `<=b`, with no `r`-dependent or
  projective-image-line multiplier.  This endpoint package now has a short
  version: with `h=c-b`, injectivity of the four degree-`<h` maps
  `H_{t+r,h-1}(u)`, `H_{t+r,h-1}(v)`, `B_h^(r)`, and `A_h^(r)` implies the
  endpoint hypotheses and closes the same ledger after at most `2h` finite
  parameter charges.  For any finite ladder of depths `R` satisfying these
  short checks, the depth-indexed charge is additive, at most `2h|R|`, and
  after those systems are charged all remaining finite fixed-kernel and
  consecutive common-image frontier ledgers at depths in `R` have dimension
  `<=b`.  Failure of any short frontier check is now identified as a short
  denominator recurrence for `u`, `v`, `(u,v)`, or `(S u,S v)`, with
  domain-root factors stripping losslessly into fixed-root/root-slice charges
  and a root-free recurrence residual.  Thus, for a finite frontier ladder,
  after fixed-root/root-slice short recurrence pieces are charged, the only
  uncharged obstruction to additive closure is a root-free recurrence in one
  of those four families at one of the ladder depths.  In the half-window range
  `h<=t+r`, each such root-free residual compresses to a primitive
  reciprocal-domain-pole-free denominator for one of `u`, `v`, `(u,v)`, or
  `(S u,S v)`, with only the explicit multiplier ledger left for certificates.
  The ladder charge also sharpens by nesting: if the bottom depth `r_0=min R`
  satisfies the four short checks, then all deeper checks hold and
  `E_{r,>b} subset E_{r_0,>b}`, `Theta_{r,>b} subset Theta_{r_0,>b}`; charging
  the bottom bad sets of total size at most `2h` closes all depths in `R`.
  The root-free residual families themselves nest too: a deeper root-free
  recurrence witness is already a bottom-depth witness for the same one of
  `u`, `v`, `(u,v)`, or `(S u,S v)`, so the bottom primitive denominator
  targets control the whole ladder in the half-window range.  These pieces now
  give a bottom-rung closure criterion: fixed-root/root-slice short recurrence
  charges, four bottom root-free recurrence families, and at most `2h` bottom
  finite parameter systems close a finite nested frontier ladder without any
  `|R|`, projective-image-line, or per-rung multiplier; in the half-window
  range the root-free recurrence charges can be recorded as primitive
  denominator targets.  The ordinary and shifted paired residual targets now
  have an exact overlap rule: their common root-free witnesses are precisely
  the endpoint-pair residual witnesses, so any common primitive denominator in
  the half-window range is an endpoint-pair charge.  Consecutive blocks of
  shifted paired residuals likewise collapse to the deepest paired residual, so
  common primitive denominators across a block are charged once.  If a ladder
  enters the half-window range only after some initial depths, the half-window
  tail now has a first-cutoff rule: every later root-free residual is contained
  in the four residual families at the first half-window depth, so primitive
  denominator charges are paid once at that cutoff while earlier depths remain
  longer-Pade obligations.  This is now packaged as a mixed-ladder closure
  ledger: after those pre-half residuals and the first half-window primitive
  targets are charged, only the bottom finite parameter systems, total size at
  most `2h` on the remaining ledger, are needed for the consecutive
  fixed-kernel/common-image frontier systems.  The half-window tail also has
  primitive-denominator divisibility: every deeper primitive denominator in
  the same residual family is a multiple of the first half-window primitive
  denominator, so deeper denominators are refinements inside the cutoff
  multiplier ledger rather than new primitive bases.  Over `F_q`, if the
  cutoff primitive has degree `delta`, the ambient number of tail projective
  certificate-denominator classes, and hence primitive denominator classes, for
  that family is at most `(q^(h-delta)-1)/(q-1)` before the deeper truncation
  equations are imposed.  Summing over the four residual families gives a
  family-labelled half-window tail budget
  `sum_F (q^(h-delta_F)-1)/(q-1) <= 4(q^h-1)/(q-1)`, with absent cutoff
  families contributing zero.  Any projective certificate-denominator class
  common to the ordinary paired and shifted paired tails is now identified with
  an endpoint-pair residual certificate at the first half-window depth, so
  paired tail overlaps are endpoint-pair charges rather than new tail budget.
  The scalar-paired tail overlaps are also classified: they are one-sided
  cutoff endpoint residuals with one series in the longer `t+r` window and the
  other in the paired `t+r-1` window.  The scalar-scalar tail overlap is the
  cutoff endpoint-pair residual, completing the pairwise overlap classification
  for the unlabelled four-family tail budget.  After those named overlap residuals
  and their multiplier ledgers are charged, the remaining half-window tail is
  family-disjoint: each uncharged projective certificate-denominator class,
  and hence each primitive denominator class, has a unique residual-family
  label.  The named cutoff overlap charges are now also compressed into
  half-window Pade ledgers: at the cutoff depth `r_hw`, the endpoint-pair
  residual uses the paired parent `(u,v)` at window `t+r_hw`, while the four
  one-sided residuals use `(u,v)` or `(S u,S v)` at window `t+r_hw-1`.  Each
  active overlap system has one parent primitive vector denominator and an
  explicit multiplier ledger of size at most `(q^(h-delta)-1)/(q-1)`, with the
  one-sided extra row cutting this ledger further; crudely, all five overlap
  charges have ambient size at most
  `5(q^h-1)/(q-1)` before those extra cuts.  These overlap ledgers now refine
  the lcms of the existing cutoff family primitives: the endpoint-pair overlap
  uses `lcm(D_u,D_v,D_uv,D_S)`, and the one-sided overlaps use
  `lcm(D_u,D_uv)`, `lcm(D_v,D_uv)`, `lcm(D_u,D_S)`, and `lcm(D_v,D_S)`.
  Thus overlap costs are intersection ledgers of the four family primitives and
  improve with the lcm degrees.  The one-sided cutoff overlaps now also have a
  locator-space row-cut dichotomy: the missing endpoint row either cuts the
  parent paired kernel by one projective dimension, or the parent paired kernel
  is endpoint-persistent in that direction.  This persistence alternative is
  now a concrete stacked-Hankel row-span test, and the endpoint-pair overlap
  has the two-row version: its codimension inside the ordinary paired parent
  kernel is the rank of the two restricted endpoint rows.  These ranks now give
  a consumable cutoff-overlap budget
  `Phi(d_uv-r_EP)+Phi(d_uv-eps_u)+Phi(d_uv-eps_v)+Phi(d_S-eps_uS)+Phi(d_S-eps_vS)`,
  with `Phi(m)=(q^m-1)/(q-1)`, bounding both projective locator classes and
  root-free certificate-denominator classes.  Combining this with the lcm
  multiplier ledgers gives a termwise hybrid budget: each overlap summand is
  bounded by the minimum of its family-lcm multiplier count and its endpoint-row
  rank count, so large lcm degree and genuine endpoint-row cuts are independent
  savings mechanisms.  The rank side now has an inclusion-exclusion refinement:
  the endpoint-pair residual is contained in each one-sided overlap space, so
  the rank budget for the cutoff-overlap union omits it as a fifth independent
  summand and subtracts the ordinary and shifted two-row intersections.  The
  refined mixed-ladder closure now records the sharper
  consumable upper ledger: after pre-half residuals, the non-prehalf part is
  charged by the direct raw-tail ledger `ArrBudget_hw + 2h`, where
  `ArrBudget_hw <= FamilyBudget_hw` is the divisor-arrangement
  inclusion-exclusion budget for the raw half-window tail and intersections of
  the ambient family multiplier subspaces are counted by lcms of the active
  cutoff primitive denominators.  This arrangement now reduces to the distinct
  divisibility-minimal antichain of active primitives: dominated active
  families and duplicate primitive denominators contribute no new raw tail
  denominator classes, and a chain of active denominators collapses to the
  single term `Phi(h-delta_min)`.  If the surviving antichain has a common
  denominator core `C` of degree `gamma`, the whole arrangement factors through
  the quotient denominators `D/C` in the shorter window `h-gamma`, giving the
  one-parameter bound `ArrBudget_hw <= Phi(h-gamma)` and mixed ledger
  `Phi(h-gamma)+2h`; in particular the half-window tail vanishes when
  `gamma>=h`.  When those quotient denominators are pairwise coprime,
  `ArrBudget_hw` is the alternating degree-only sum over
  `h-gamma-sum deg(D/C)`.  Without coprimality, the minimum quotient degree
  still gives `ArrBudget_hw <= |M_min| Phi(h-gamma-e_min)`, and `e_min>=1`
  whenever at least two minimal denominators survive.  Consequently, proving
  `gamma+e_min >= h-L` reduces the direct mixed ledger to `4Phi(L)+2h`, and
  for `q<=n^a`, `h<=n`, fixed `L>=1`, to `4L n^{a(L-1)}+2n`.  In the
  two-denominator antichain case, the quotients after factoring the gcd are
  automatically coprime, giving the exact tail formula
  `Phi(h-gamma-e_1)+Phi(h-gamma-e_2)-Phi(h-gamma-e_1-e_2)`.  The mixed ladder
  also has a bottom residual route: charging the four root-free residual
  families at `r_0` removes every residual at every depth, so there is no
  `|R_pre|` factor and no half-window denominator ledger on that route.  Since
  the same ladder also has the half-window split route, the residual bottleneck
  is now packaged as the two-route ledger
  `min(Charge(B_0), Charge(P_pre)+ArrBudget_hw)+2h`: either prove the bottom
  longer-Pade family is small enough, or leave the pre-half family as the named
  obstruction and prove the half-window arrangement term is small.  In the
  multiplicative-domain case, the raw arrangement now has a root-free
  multiplier sharpening: each projective multiplier count `Phi(m)` can be
  replaced by the exact full-support MDS count `RFPhi_D(m)`, giving
  `RFArrBudget_hw<=ArrBudget_hw` and direct ledger `RFArrBudget_hw+2h`.
  Consequently the residual-tail criterion improves to
  `RFArrBudget_hw<=4RFPhi_D(L)` when `gamma+e_min>=h-L`; in particular
  `RFPhi_D(1)=1` and `RFPhi_D(2)=q+1-n`, giving ledgers `4+2h` and
  `4(q+1-n)+2h` respectively.  The common-core and two-denominator formulas
  now also have root-free analogues: after factoring `C=gcd(M_min)`, replace
  every `Phi(h-gamma-deg lcm(...))` term by
  `RFPhi_D(h-gamma-deg lcm(...))`; in the two-denominator case this gives
  `RFPhi_D(h-gamma-e_1)+RFPhi_D(h-gamma-e_2)-RFPhi_D(h-gamma-e_1-e_2)`.
  A new bottom-route criterion now counts root-free witnesses in any bottom
  recurrence kernel `K` by inclusion-exclusion over the root slices
  `K(-J)`.  If the four bottom residual kernels are in domain-MDS position
  with dimensions `d_F<=L`, then the bottom longer-Pade route closes with
  `sum_F RFPhi_D(d_F)+2h <= 4RFPhi_D(L)+2h`, without invoking the half-window
  arrangement.  The domain-MDS condition is then identified exactly with the
  stripped fixed-root/root-slice rank profile: multiplication by `L_J`
  identifies `K_0(F)(-J)` with the corresponding `Delta_J` bottom kernel, so
  the bottom route closes when these root-slice kernels have no excess
  dimension beyond `max(dim K_0(F)-|J|,0)`.
  This all-root-set test is further reduced to top root slices: a
  `d`-dimensional bottom kernel with `d<=|D|` is domain-MDS iff no nonzero
  element has `d` distinct domain roots, equivalently every `d x d`
  evaluation determinant of a basis is nonzero, equivalently the stripped
  top root-slice kernels `K_J(F)` vanish for `|J|=d_F`.
  The `d=2` case is now exact: if no evaluation functional is zero, then
  `|K^rf|=q+1-s_K`, where `s_K` is the number of distinct projective evaluation
  lines `[ev_alpha]`; hence the full `L=2` bottom-route defect is precisely
  repeated evaluation lines.  The two-dimensional defect is now bounded by
  the pair collision count `C_K`: `|K^rf|<=RFPhi_D(2)+C_K`, and each collision
  pair is exactly a nonzero two-root stripped kernel `K_{alpha,beta}(F)`.
  Factoring a two-dimensional kernel by its common divisor gives a projective
  map `[A:B]` of degree `r_K`; every evaluation fiber has size at most `r_K`,
  so `|K^rf|<=RFPhi_D(2)+(1-1/r_K)|D|` and
  `C_K<=((r_K-1)/2)|D|`.  Degree-one bottom kernels therefore have no
  collision defect.  The projective degree is now tied to the common factor:
  if `gamma_K=deg gcd(K)`, then either the common factor has a domain root and
  the root-free set is empty, or `r_K<=h-1-gamma_K`; in particular
  `gamma_K>=h-2` forces the exact `RFPhi_D(2)` count.
  This is generalized to all dimensions: for a `d`-dimensional bottom kernel,
  `deg gcd(K)<=h-d`, and equality forces `K/gcd(K)` to be the full
  degree-`<d` polynomial space, hence the ideal count `RFPhi_D(d)`.
  A weaker but more flexible residual-window criterion now bounds any bottom
  kernel by `RFPhi_D(h-deg gcd(K))`; thus if all four bottom kernels have
  common-factor residual window at most `L`, the bottom route closes with
  `4RFPhi_D(L)+2h` without a domain-MDS assumption.
  The non-claims section is updated through Corollary 40.56 to record that
  these formulas do not by themselves bound the bottom/pre-half residuals or
  force large common cores/quotient degrees.
  Since
  the named overlap systems are subsets of the same `TailUnion_hw`, the
  separation charge `OverlapSep_hw`, defined as the minimum of
  `SideHybridOverlap_hw` and `UnionRankOverlap_hw`, is now a structural
  diagnostic/family-disjoint route rather than an additional denominator-class
  charge in the direct raw-tail closure.  The final `2h` is the bottom finite
  frontier set `E_{r_0,>b} union Theta_{r_0,>b}`.
  The common-image three-shift ledger now has the analogous sliding-window
  reduction: for an image line `[y]`, the allowed deeper residuals form a space
  `W_y` of dimension at most one, nonzero only on the `q+1` extended geometric
  shift lines.  Off that shift curve, `ker C_y^G` is just
  `ker H_{t+2,c-1}(u) cap ker H_{t+2,c-1}(v)`.  The shift-persistent lines
  themselves are now endpoint ledgers too: for finite `theta`,
  `ker C_[1:theta:...:theta^(t-1)]^G` equals the intersection of the two
  first-difference kernels
  `ker H_{t+1,c-1}(Delta_theta u) cap ker H_{t+1,c-1}(Delta_theta v)`, and the
  infinity line is `ker H_{t+1,c-1}(u) cap ker H_{t+1,c-1}(v)`.  Combining
  these reductions, the whole three-shift common-image branch is now the union
  of `E_deep`, `E_infty`, and the `q` first-difference endpoint ledgers
  `E_theta`; under direction dimension `<=b`, this gives the endpoint-only
  bound `(q+2)binom(n,b)` before the usual root-free replacement.  Combining
  this with the globally full core classification gives an endpointized global
  full-core closure: the ledger is covered by `U`, `V`, `D_infty`, the `q`
  finite fixed-kernel endpoint systems `K_lambda`, and the `q`
  first-difference endpoint systems `D_theta`, giving
  `(2q+3)binom(n,b)` under direction dimension `<=b`, with the usual root-free
  replacement after common-root pieces are charged.  This now propagates to the
  all-anchor full-core incidence: after endpointized global charges,
  `|Z_all^{endpoint,<=b}| <= ((2q)/m+2(n-m+1))binom(n,m-1)
  + q(n-m+1)(2q+3)binom(n,b)`, with the final term gaining `b/c` after
  common-root global core pieces are charged.  The first-difference endpoint
  systems `D_theta` now have their own finite-exception/persistent dichotomy:
  either at most `c-b` parameters have direction dimension `>b`, or
  `J_theta=J_+-theta J_0` is persistently low-rank with moving kernels obeying
  the endpoint ladder `J_+q_0=0`, `J_+q_i-J_0q_{i-1}=0`, `J_0q_D=0`.  A final
  endpointized charge reduction now shows that if the four base endpoint spaces
  `ker H_{t+2,c-1}(u)`, `ker H_{t+2,c-1}(v)`, `ker J_0`, and `ker J_+` have
  dimension `<=b`, then both persistent alternatives are impossible and the
  finite bad-parameter sets satisfy `|Lambda_{K,>b}|, |Theta_{D,>b}| <= c-b`.
  The endpoint checks now have a short-annihilator certificate form: with
  `h=c-b`, any high-dimensional endpointized charge contains a nonzero
  degree-`<h` annihilator.  Hence `Lambda_{K,>b}` and `Theta_{D,>b}` are
  contained in the short systems `ker H_{t+2,h-1}(v-lambda u)!=0` and
  `ker J_theta^(h)!=0`, and failure of a base endpoint check forces one of
  `H_{t+2,h-1}(u)`, `H_{t+2,h-1}(v)`, `J_0^(h)`, or `J_+^(h)` to have
  nonzero kernel.  These short bad parameters are now organized as projective
  landing images: absent a common short endpoint kernel, each finite
  fixed-kernel parameter is the unique scalar from a short projective locator
  `[Q]` with `rank[U_h(Q) V_h(Q)]<=1`, and each first-difference parameter is
  the unique scalar from `[Q]` with `rank[P_0^h(Q) P_+^h(Q)]<=1`.  A further
  one-sided injection test shows that if either short fixed-kernel endpoint
  map `H_{t+2,h-1}(u)` or `H_{t+2,h-1}(v)` is injective, then
  `|Lambda_h|<=h`; if either `J_0^(h)` or `J_+^(h)` is injective, then
  `|Theta_h|<=h`.  Hence any larger short exception family must expose short
  endpoint annihilators on both sides of its pencil.  Short annihilators now
  have a lossless root-stripping identity: if `Q=L_A R`, then
  `H_{s,d}(w)Q=H_{s,d-|A|}(Delta_A w)R`.  Thus domain-root factors move to
  fixed-root/root-slice ledgers, while the remaining endpoint obstruction is a
  root-free short-annihilator family for differenced syndrome data.  The
  first-difference short parameters are now exactly marked roots of the common
  endpoint recurrence space
  `C_h^+={P: deg P<=h, H_{t+1,h}(u)P=H_{t+1,h}(v)P=0}`:
  `ker J_theta^(h)` is isomorphic to `{P in C_h^+ : P(theta)=0}` via
  `Q -> (X-theta)Q`.  Thus if `dim C_h^+=g` over `F_q`, then
  `|Theta_h| <= min(q, h(q^g-1)/(q-1))`.  The short fixed-kernel parameters
  now have the matching finite/persistent pencil dichotomy: either
  `|Lambda_h|<=h`, or every `h x h` minor of `V_h-lambda U_h` vanishes
  identically and there is a moving short kernel with coefficient ladder
  `V_hq_0=0`, `V_hq_i-U_hq_{i-1}=0`, `U_hq_D=0`.  Common root factors in
  moving short certificates now strip losslessly too: if
  `Q(parameter,X)=L_A(X)R(parameter,X)`, the certificate becomes the
  corresponding lower-order moving certificate for `Delta_A`-differenced
  syndrome data.  Thus the genuine moving-certificate obstruction can be
  taken common-root-free over `D` after fixed-root/root-slice charges.  These
  reductions now give a short-injectivity closure criterion: if
  `H_{t+2,h-1}(u)`, `H_{t+2,h-1}(v)`, `J_0^(h)`, and `J_+^(h)` are injective,
  then the base endpoint checks hold and
  `|Lambda_{K,>b}|, |Theta_{D,>b}| <= h`; after charging those at most `2h`
  endpointized exceptional systems, Corollaries 42 and 43 apply to the
  uncharged endpointized global full-core and all-anchor full-core ledgers.
  These injectivity checks are explicit Hankel-minor targets: a single
  `H_{s,h-1}` can be injective iff row count permits `h<=s`, while a stacked
  two-syndrome map can be injective iff `h<=2s`; in the feasible ranges the
  injectivity loci are nonempty determinantal open sets.  Since `h=c-b`, this
  gives the endpoint-short closure threshold
  `b_min=max(0,c-(t+2))`: below it the single endpoint maps cannot be
  injective by row count, and at or above it the remaining closure target is
  explicit nonvanishing of four `h x h` Hankel minors plus the finite `2h`
  exception charge.  The remaining short failures are now identified exactly
  as denominator recurrences: `H_{s,h-1}(w)Q=0` is the recurrence
  `sum_i q_i w_{a+i}=0`; after root stripping, the unresolved endpoint-short
  obstruction is a `D`-root-free denominator recurrence for `v-lambda u` or a
  common `D`-root-free denominator recurrence for `(Delta_theta u,
  Delta_theta v)`.  Equivalently, with
  `Q^*(T)=q_e+q_{e-1}T+...+q_0T^e` and
  `W_w(T)=sum_a w_aT^a`, the equation `H_{s,h-1}(w)Q=0` is the truncated
  rational-denominator certificate
  `Q^*(T)W_w(T)=N(T) mod T^{e+s}` with `deg N<e`.  Thus the root-free
  endpoint-short failures are Pade/residue-denominator objects for the
  combined or differenced syndrome series.  The root-free condition is also
  the reciprocal-pole condition: for `alpha!=0`,
  `Q(alpha)=alpha^e Q^*(1/alpha)`, while a root at `alpha=0` is a zero at the
  projective point `infty` for the degree-`e` denominator.  Thus fixed-root
  charges remove reciprocal-domain denominator factors before the root-free
  residue-denominator obstruction remains.  A half-window uniqueness lemma now
  compresses these families: if two denominator certificates
  `D_i W_w=N_i mod T^{e_i+s}` have `s>=max(e_1,e_2)`, then
  `N_1D_2=N_2D_1`, so all order-`<=s` certificates share one reduced rational
  function; componentwise, common certificates for a pair share one primitive
  vector denominator dividing every certificate denominator.  If that
  primitive denominator has degree `delta`, every order-`<h` certificate lies
  in the multiplier ledger `D_0M`, `deg M<=h-1-delta`; over `F_q` this costs
  at most `(q^{h-delta}-1)/(q-1)` projective multipliers before root-free and
  truncation cuts.  The primitive denominator itself remains a certificate
  after cancelling the invertible multiplier.  Parameter collisions are also
  endpoint charges: if two distinct `lambda` values share a denominator for
  `v-lambda u`, then that denominator works for both `u` and `v` at depth
  `t+2`; if two distinct `theta` values share a common denominator for
  `(Delta_theta u, Delta_theta v)`, it works for both `u` and `v` at depth
  `t+1`.  After charging those base endpoint intersections, bad parameters
  inject into primitive denominator classes.  The remaining primitive
  denominator classes are explicit rank-one landings: for fixed-kernel
  parameters, `V_D=lambda U_D` with
  `U_D=R_{t+2}(D;u)`, `V_D=R_{t+2}(D;v)` outside `U_D=V_D=0`; for
  first-difference parameters, `A_D=theta B_D` in the doubled
  `(u,v)` window outside `B_D=0`.  These are `2 x 2` minor loci in the
  denominator coefficients plus the root-free open condition.  This half-window
  reduction covers the entire row-count feasible endpoint-short closure
  threshold: if `h=c-b` and `b>=max(0,c-(t+2))`, then `h<=t+2`; fixed-kernel
  windows have `s=t+2`, and first-difference windows have `s=t+1` with every
  order `e<h` satisfying `e<=s`.  Thus the longer vector-Pade range is not an
  extra obstruction at the Corollary 55 threshold.  Order-layer finite
  landing is also explicit: the rank-one landing equations in `P_d` are
  homogeneous quadrics, so a zero-dimensional remaining order-`d` layer has
  at most `2^d` geometric points by Bezout.  Summing over `d<h` gives
  `2^h-1` bad parameters per family after endpoint collision charges, unless
  a positive-dimensional primitive rank-one landing component remains.  Such a
  component is now certificate-form: over its function field, the generic
  denominator `D_C` is root-free and has a unique parameter satisfying either
  `D_C W_{v-lambda_C u}=N_C mod T^{d+t+2}` or the paired first-difference
  congruences modulo `T^{d+t+1}`.  The parameter is either constant, hence a
  fixed-slice charge, or genuinely moving.  Constant-parameter positive
  components are exactly high-dimensional fixed-slice recurrence spaces:
  fixed `lambda` gives `dim {D:R_{t+2}(D;v-lambda u)=0}>=2`, and fixed
  `theta` gives the analogous simultaneous
  `Delta_theta u, Delta_theta v` recurrence space of dimension at least `2`.
  Nonconstant components descend to persistent one-parameter kernels: with
  `Z` indeterminate, a nonconstant fixed-kernel component forces
  `ker(D -> R_{t+2}(D;v-Zu)) != 0` over `F(Z)`, and a nonconstant
  first-difference component forces the analogous stacked
  `(Delta_Z u, Delta_Z v)` kernel over `F(Z)`.  Conversely such a generic
  kernel gives a landing family when the root-free, primitive, order, and
  base-free opens are nonempty.  In the row-count feasible range, persistent
  kernels force endpoint rank failure: for `V_d-ZU_d`, all full-column minors
  vanishing forces both endpoint maps `U_d,V_d` to have nonzero kernel, and
  similarly the stacked first-difference pencil forces nonzero kernels for
  `A_d` and `B_d`.  At the Corollary 64 threshold this means the four short
  endpoint injectivity checks rule out the persistent moving branch entirely.
  Constant-parameter positive slices have the analogous finite/persistent
  dichotomy at rank threshold `d-1`: for each order `1<=d<h`, either there are
  at most `d` fixed `lambda` values with `dim K_{d,lambda}>=2`, or both
  endpoint maps `U_d,V_d` have two-dimensional kernels; likewise for fixed
  `theta` and the stacked maps `A_d,B_d`.  After charging those two-dimensional
  endpoint-kernel cases, constant positive slices cost at most `h(h-1)/2`
  parameters per family.  These alternatives now combine into a finite
  endpoint-short denominator ledger under the four short injectivity checks:
  nonconstant positive-dimensional primitive landing components are ruled out
  by endpoint rank failure, constant positive slices cost at most `h(h-1)/2`
  parameters per family, and zero-dimensional primitive landing layers cost at
  most `2^h-1`.  A follow-up separation records that multipliers do not
  multiply bad parameters after base endpoint collision charges: cancelling a
  multiplier preserves the same primitive denominator and the same parameter,
  while a second parameter would be a charged collision.  The multiplier ledger
  is therefore certificate-only for this parameter-counting step.  This
  packages the denominator geometry; it does not improve the direct `h`
  exceptional-parameter bound from short injectivity.
- **What to do next:** Bound or charge the unique-neighbor nondegenerate
  star-free shadow ledger, then charge the four base endpoint spaces, the
  resulting short-annihilator endpoint systems, finite-exception endpoint
  systems, their projective short-locator landing varieties, the one-sided
  short endpoint annihilator failures, root-free short-annihilator families,
  low-dimensional common endpoint recurrence spaces, the corresponding
  primitive reciprocal-domain-pole-free denominator families, their endpoint
  collision charges, positive-dimensional moving denominator certificates,
  persistent one-parameter recurrence kernels, root-free multipliers, and the
  endpoint maps with two-dimensional short kernels, and the common-root-free
  fixed-kernel and first-difference moving-certificate loci to
  fixed-slope/root-slice, quotient-periodic, endpoint, or active-codegree
  ledgers.

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
