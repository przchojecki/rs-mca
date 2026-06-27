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

### 2026-06-27 - M1 domain-singleton escape-mass charge

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Geometric domain-singleton non-fixed variable lines
  now carry an escape-mass identity: in the `t=3` two-exchange ledger, each
  singleton contributes `|D|-j` roots in the contained/core-hit/off-domain/fixed
  or pole buckets.
- **How it is useful:** The active singleton residue is reduced to bounding
  escape-root mass, which is more structural than directly counting singleton
  packet points.
- **What to do next:** Bound contained/core-hit/off-domain/fixed-pole escape
  mass globally or charge it to existing quotient and edge-energy ledgers.

### 2026-06-27 - M1 non-fixed variable-line orbit census

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Every non-fixed variable proper line now has an
  audited involution-root census: noncontained domain two-cycles, contained
  domain two-cycles, core-hit roots, off-domain roots, and fixed/pole roots.
- **How it is useful:** It identifies geometric domain singletons exactly as
  the case where the noncontained domain two-cycle bucket has two roots, and
  classifies the current active singleton witness as product-Mobius.
- **What to do next:** Bound the product/sum domain-singleton census globally
  or relate it to quotient and edge-energy reserves.

### 2026-06-27 - M1 active domain-singleton variable-line witness

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **What is being added:** A deterministic `F_13,n=12,j=5,t=3` probe shows
  that the active geometric domain-singleton term in (VN) is necessary.
- **How it is useful:** The witness has a product-Mobius line
  `(x-4)(y-4)=3` over core `{2,6,11}` with exactly one active new aperiodic
  domain-pair member, so no packet-edge charge is available.
- **What to do next:** Classify or bound geometric domain-singleton
  product/sum involution lines in the all-line M1 reduction.

### 2026-06-27 - M1 active new variable-line packet bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The non-fixed variable-line ledger now counts only
  active new slopes after root/full-plane/fixed-root charges and checks
  `r_i <= 1_{d_i=m_i=r_i=1} + (d_i-m_i) + 1_{m_i=2,r_i=2} + binom(m_i,2)`.
- **How it is useful:** This charges the actual residual variable-line
  contribution to the injected different-slope edge ledger, leaving only true
  domain singletons, quotient defects, and fully active two-point packets.
- **What to do next:** Classify active two-point packets and geometric
  domain-singleton packets, then bound the global different-slope edge ledger.

### 2026-06-27 - M1 variable-line packet-edge injection

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The non-fixed variable-line packet-edge charge is
  made injective into the global different-slope two-exchange edge ledger.
- **How it is useful:** This removes a possible double-counting loophole in
  the edge-energy reduction: a charged edge determines its unique `(j-2)` core
  and the unique affine line through its two pair-coordinate points.
- **What to do next:** Bound the global different-slope two-exchange edge
  energy, and classify any true geometric domain-singleton variable lines.

### 2026-06-27 - M1 variable-line quotient-aware singleton reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The non-fixed variable-line singleton term is split
  into geometric domain-singleton packets and charged quotient defects:
  `sum_i m_i <= #{i:d_i=m_i=1} + sum_i(d_i-m_i) + 2 sum_i binom(m_i,2)`.
- **How it is useful:** This shows that, once quotient-periodic packet members
  are charged, the only singleton residue left in the variable-line M1 branch
  is the true domain-singleton case; all packets of size at least two remain
  controlled by different-slope two-exchange edge energy.
- **What to do next:** Classify or bound geometric domain-singleton non-fixed
  variable lines, and separately bound the global different-slope edge energy.

### 2026-06-27 - M1 variable-line singleton plus edge bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The non-fixed variable-line packet ledger now
  checks the bound `sum_i m_i <= #{i:m_i=1} + 2 sum_i binom(m_i,2)`, globally
  and core-by-core.
- **How it is useful:** This separates the remaining M1 residual-line task
  into singleton packets and different-slope two-exchange edge energy.  In the
  current deterministic `t=3` probes, the singleton term is `0`.
- **What to do next:** Search for singleton non-fixed variable packets; if
  they exist, classify them, otherwise prove a no-singleton or recursive-charge
  lemma.

### 2026-06-27 - M1 unanchored variable-line obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **What is being added:** A deterministic `F_13,n=12,j=5,t=3` probe shows
  that non-fixed variable proper lines need not be anchored in the core.  The
  witness has core `{2,11,12}` and product-Mobius line `(x-6)(y-6)=3`, with
  `6` outside the core.
- **How it is useful:** This corrects the anchored-only interpretation of the
  residual packet branch.  The packet and edge-charge reductions survive
  unchanged, but the next theorem must handle general non-fixed involution
  packets, not just anchored ones.
- **What to do next:** Bound unanchored and anchored product-Mobius/fixed-sum
  packet energy using the different-slope two-exchange ledger.

### 2026-06-27 - M1 variable-line packet edge charge

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Non-fixed variable proper-line packets now carry an
  exact different-slope two-exchange edge charge: a packet of size `m`
  contributes `binom(m,2)` strict different-slope two-exchange edges.
- **How it is useful:** This converts large residual variable-line slope
  packets into quadratic edge energy already visible in the two-exchange
  determinantal ledger.  The audited same-slope and residual-witness probes
  charge `6` and `3` packet edges respectively.
- **What to do next:** Use the different-slope two-exchange quadratic-slice
  ledger to bound the total edge energy of non-fixed variable-line packets.

### 2026-06-27 - M1 anchored variable-line packet bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The variable proper-line residual is refined to an
  exact involution-packet bound: on each variable proper line, injectivity gives
  `|Z_L^new| <= |Z_L| <= |P_L^nc(R)|`, where `P_L^nc(R)` is the set of
  noncontained domain-pair points on the product-Mobius or fixed-sum
  involution.
- **How it is useful:** This replaces the crude field-line size with the
  actual packet size in the audited `t=3` obstruction.  At the time of this
  entry, the audited examples were anchored, with maximum packet size `3`;
  this anchored-only pattern is superseded by the unanchored obstruction above.
- **What to do next:** Superseded by the unanchored variable-line obstruction:
  prove a uniform packing or recursive charge for general non-fixed
  product-Mobius/fixed-sum packets.

### 2026-06-27 - M1 variable proper-line residual obstruction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **What is being added:** A deterministic `F_13,n=12,j=5,t=3` probe shows
  that `Z_varline^new` need not be empty: after one full-plane lift and
  fixed-root charges, one product-Mobius variable proper line leaves one new
  residual slope.
- **How it is useful:** This rules out the tempting stronger claim that the
  variable proper-line branch always disappears after the current charges,
  while keeping the obstruction localized to a one-dimensional
  projective-linear slope image.
- **What to do next:** Bound or recursively charge the residual
  product-Mobius/fixed-sum proper-line slope image, rather than trying to
  prove it is always empty.

### 2026-06-27 - M1 variable proper-line new-slope ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** The `t=3` proper-line ledger now reports
  `Z_varline^new`, the variable proper-line aperiodic slope set left after
  one-exchange root-slice, constant full-plane, and fixed-root proper-line
  charges.
- **How it is useful:** This isolates whether product-Mobius/fixed-sum proper
  lines create genuinely new M1 slopes after existing charges.  In the
  `F_13,n=12,j=5,t=3` probe, the variable proper-line aperiodic slope set has
  size `3`, but the new-slope count is `0`.
- **What to do next:** Superseded by the variable proper-line residual
  obstruction entry above; the empty-new-slope phenomenon is not structural.

### 2026-06-27 - M1 variable proper-line injectivity

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Variable proper `t=3` two-exchange determinant
  lines are now checked to have injective finite slope maps, at most one
  contained pole, and no repeated aperiodic domain-pair slopes.
- **How it is useful:** The remaining product-Mobius/fixed-sum proper-line
  obstruction is slope-injective, so it is not a hidden high-multiplicity
  slope fiber.  In the `F_13,n=12,j=5,t=3` probe, the two variable proper
  lines each have one pole, `12` finite line slopes, and `3` aperiodic
  domain-pair slopes.
- **What to do next:** Bound how many aperiodic domain-pair members can lie on
  quotient-clean product-Mobius or fixed-sum proper lines, or charge such
  lines to a higher recursive locator object.

### 2026-06-27 - M1 proper determinant-line bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The `t=3` two-exchange determinant-line ledger now
  separates full determinant pair-planes from proper line components.  Constant
  full planes are checked against the lifted `H_{5,j-2}` core pencil, and
  every non-plane core is asserted to have at most two proper determinant
  lines.
- **How it is useful:** This removes the misleading line-count explosion from
  full planes.  In the `F_13,n=12,j=5,t=3` probe, the old `219` determinant
  lines split into one lifted full plane plus `37` proper lines, with the only
  variable proper lines being one product-Mobius and one fixed-sum component.
- **What to do next:** Bound or recursively charge the variable proper
  product-Mobius/fixed-sum slope images; these are now the localized
  one-dimensional obstruction in the audited `t=3` branch.

### 2026-06-27 - M1 two-exchange determinant-line components

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The `t=3` two-exchange verifier now enumerates
  affine lines contained in the three-quadratic determinantal locus over each
  `(j-2)` core, classifies them as fixed-root, product-Mobius, or fixed-sum
  components, and records constant versus variable slope images.
- **How it is useful:** This extends the line classification from same-slope
  clusters to the different-slope line-component branch: every such component
  is an explicit one-parameter involution with projective-linear slope image,
  not an arbitrary two-dimensional packing set.
- **What to do next:** Prove a quotient/root-slice bound for variable
  determinant-line slope images, or show they must be charged to a higher
  recursive object in the final M1 ledger.

### 2026-06-27 - M1 two-exchange line involution models

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** One-dimensional same-slope `t=3` two-exchange
  line components are classified as fixed-root root-slice lines, product
  Möbius involutions `(x-alpha)(y-alpha)=kappa`, or fixed-sum involutions
  `x+y=s_0`.
- **How it is useful:** This finishes the local structural split after the
  affine-plane lift: same-slope two-exchange structure is now either charged
  recursively, reduced to fixed-root one-exchange slices, or localized to a
  single explicit involution on exchanged roots.
- **What to do next:** Bound or rule out persistent non-fixed involution
  components after quotient/root-slice charging, and then turn to the
  different-slope two-exchange branch.

### 2026-06-27 - M1 same-slope two-exchange affine lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Same-slope `t=3` two-exchange clusters over a fixed
  `(j-2)` core are classified by affine rank in `(s,p)=(x+y,xy)`: line
  clusters are one-dimensional components, while affine-rank-two clusters lift
  to the `(t+2,j-2)` Hankel core-locator image.
- **How it is useful:** This gives a recursive charge for the dangerous
  two-dimensional same-slope two-exchange branch in the all-line M1 route,
  reducing it to the higher-slack core image rather than a new packing object.
- **What to do next:** Analyze the remaining one-dimensional line components,
  especially whether non-fixed-root Möbius lines can survive quotient and
  root-slice charges in larger `t=3` instances.

### 2026-06-27 - M1 two-exchange determinantal slices

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For `t=3`, two-root exchanges over a fixed
  `(j-2)` core are expressed in elementary coordinates `(s,p)=(x+y,xy)`;
  the projective slope gate is certified by three quadratic `2x2` minor
  equations in `(s,p)`.
- **How it is useful:** This localizes the first higher-slack multi-exchange
  obstruction to a concrete low-degree determinantal slice, separating it from
  the same-slope one-exchange root-slice recursion.
- **What to do next:** Analyze when these three quadrics can have large
  structured components, or prove quotient/root-slice charges eliminate the
  dangerous components in the all-line M1 setting.

### 2026-06-27 - M1 arbitrary-slack root-slice lift

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The same-slope one-exchange root-slice lift is
  generalized from `t=2` to arbitrary slack `t`: every such collision maps to
  the `(t+1,j-1)` Hankel core-locator image.  The verifier now audits this
  on all rows, including a nontrivial `F_13`, `j=7`, `t=3` row.
- **How it is useful:** This makes the recursive root-slice mechanism a
  genuine higher-slack invariant rather than a slack-two-only observation,
  directly supporting the all-line aperiodic residue-packing route for M1.
- **What to do next:** Analyze higher-slack multi-exchange overlaps
  separately; the new lemma covers one-root exchanges but not all strict
  overlaps when `t>2`.

### 2026-06-27 - M1 root-residual overlap reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The slack-two aperiodic slope ledger now charges
  only root-slice slopes not already present in the residual slope image:
  `|AperSlope| <= |Z_3 \ Z_res| + N_face + |Z_esc \ Z_lift|`.
- **How it is useful:** This removes double counting at the root/residual
  boundary and sharpens the best audited local M1 reduction on the full
  `F_17` rows and the rank-one zero-slice probe.
- **What to do next:** Seek a structural bound for `Z_3 \ Z_res`, or prove
  that large portions of the higher-slack root-slice image are always already
  realized residually in the all-line setting.

### 2026-06-27 - M1 face-exact active reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The active lifted term is sharpened from the
  coarse face budget `(j+1)N_active` to
  `N_face=sum_W |A_W|`, the exact number of surviving active residual
  coordinates in lifted common cores.  The note records
  `|AperSlope| <= |Z_3| + N_face + |Z_esc \ Z_lift|`.
- **How it is useful:** This is the sharpest current local M1 reduction in
  the PR: it charges only surviving lifted residual coordinates and only
  genuinely new boundary escape slopes.
- **What to do next:** Bound `N_face` structurally, or replace it by an
  endpoint one-row theorem with enough savings for the final reserve.

### 2026-06-27 - M1 overlap-aware escape slopes

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The residual slope split is sharpened from
  `Z_res = Z_lift union Z_esc` to the exact count
  `|Z_res| = |Z_lift| + |Z_esc \ Z_lift|`.  The verifier now asserts
  overlap-aware residual and recursive bounds using the new escape image
  instead of charging every escape slope.
- **How it is useful:** Boundary escapes which already occur as active
  common-core residual ratios no longer consume a separate M1 budget.  The
  remaining boundary obstruction is only the genuinely new escape slope image.
- **What to do next:** Seek a structural bound for `Z_esc \ Z_lift`, or prove
  that in important strata every escape slope is already realized by the
  active lifted image.

### 2026-06-27 - M1 active common-core partition

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The active residual-ratio ledger is strengthened
  from a covering bound to an exact partition: each residual lifted face has
  the unique active common core `T union {xi_T}`, where
  `xi_T=beta_1/beta_0`, and `Z_lift` is exactly the union of the active
  ratio images.
- **How it is useful:** This removes possible overcounting between common
  bases and makes the no-loss lifted-side recursion genuinely additive at the
  face level.
- **What to do next:** Use the exact partition to seek a direct bound on
  active common cores or on the active ratio image, beyond the coarser
  endpoint one-row fiber bound.

### 2026-06-27 - M1 active residual-ratio ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The active common-core term is rewritten as an
  exact residual-coordinate ratio ledger: for each active lifted common core
  `W`, surviving residual faces are the coordinates `x` where
  `rho_W(x)=-(f(x)-F_0(x))/(g(x)-G_0(x))` survives the prior charges, and
  root-slice peeling makes `rho_W` injective on that active set.
- **How it is useful:** This localizes the M1 all-line obstruction to active
  residual ratios instead of all one-row common bases, sharpening the no-loss
  explanation behind `|Z_lift| <= (j+1)N_active`.
- **What to do next:** Seek a structural bound on the number of active
  residual-ratio cores, or prove that the active ratio sets are controlled by
  the endpoint one-row fiber theorem used in the two-input reduction.

### 2026-06-27 - M1 active common-core reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The lifted-common term is sharpened from all common
  one-row bases `N_common` to active common cores `N_active`, those with at
  least one residual face after contained, quotient, and root-slice charges.
  The note records
  `|AperSlope| <= |Z_3| + (j+1)N_active + (|F|+1)^2`.
- **How it is useful:** This avoids charging inactive common bases, which can
  be numerous in degenerate endpoint cases but do not contribute lifted
  residual slopes.  It gives a more faithful local obstruction inside the M1
  all-line route.
- **What to do next:** Seek structural bounds for active common cores, or
  continue with the coarser two-input route through endpoint one-row fibers.

### 2026-06-27 - M1 two-input polynomial-field reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The slack-two all-line aperiodic slope image is
  reduced to two polynomial-field inputs:
  `|AperSlope| <= |Z_3| + (j+1)min(|Fib_1(f)|,|Fib_1(g)|) + (|F|+1)^2`.
- **How it is useful:** This packages the current M1 route into the exact
  remaining targets after boundary closure: a higher-slack slope-image bound
  and a one-row endpoint locator-fiber bound.  It also records that this rung
  is additive, not multiplicative, in the lifted/common-base term.
- **What to do next:** Attack either `Z_3` by the higher-slack M1 route or
  the endpoint one-row fiber bound via the L1 machinery.

### 2026-06-27 - M1 polynomial-field boundary closure

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The isolated boundary escape term is bounded by
  active projective boundary anchors:
  `|Z_esc| <= (|F|+1)A_boundary <= (|F|+1)^2`.  The note records the resulting
  recursive reduction
  `|AperSlope| <= |Z_3| + (j+1)N_common + (|F|+1)A_boundary`.
- **How it is useful:** In the polynomial-field window this removes boundary
  escapes as an obstruction to Przemek's all-line aperiodic packing target,
  leaving the higher-slack slope image and one-row common-base terms as the
  main remaining inputs.  The full-domain monomial floors show the field-size
  factor is unavoidable in general.
- **What to do next:** Focus on polynomial bounds for `Z_3` and `N_common`,
  while using the sharper boundary arrangement budgets only for reserve-scale
  refinements.

### 2026-06-27 - M1 boundary slope-image budget

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The boundary arrangement budget is sharpened from
  point counting to slope-image counting.  Each heavy projective flat is
  charged by the image of a projective linear ratio, hence by at most `|F|+1`
  slopes, giving `B_boundary^slope <= B_boundary`.
- **How it is useful:** This prevents higher-dimensional heavy boundary flats
  from contributing their full point count to M1.  The recursive reduction now
  uses `|Z_3| + (j+1)N_common + B_boundary^slope`.
- **What to do next:** Combine this slope-image budget with quotient-aware
  heavy-flat counts or symmetry reductions.

### 2026-06-27 - M1 boundary arrangement budget

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The isolated escape slope image now has an explicit
  rank-stratified boundary budget `B_boundary`, obtained by summing the
  arrangement covers over active off-domain, repeated-root, and infinity
  boundary anchors.  The note records
  `|AperSlope(f,g;2,j)| <= |Z_3| + (j+1)N_common + B_boundary`.
- **How it is useful:** This replaces the previously unbounded `|Z_esc|` term
  in the recursive M1 reduction by a concrete heavy-flat ledger.  The
  remaining boundary task is therefore a quotient-aware estimate for
  `B_boundary`.
- **What to do next:** Sharpen `B_boundary` by exploiting quotient charging,
  fixed domain symmetries, or low-dimensional boundary kernels.

### 2026-06-27 - M1 all-boundary arrangement reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The isolated escape term is reduced to three
  projective rich-point slope images: off-domain fixed anchors, repeated-root
  in-domain anchors, and the infinity anchor.  Repeated and infinity escapes
  now satisfy the same rank-stratified arrangement cover previously used for
  off-domain anchors.
- **How it is useful:** This turns `Z_esc` into a uniform boundary
  arrangement problem.  The remaining M1 work is to sharpen or quotient-filter
  these arrangement slope images to the final reserve scale, not to classify
  more boundary escape types.
- **What to do next:** Seek reserve-scale bounds for the boundary arrangement
  slope images, starting with quotient-aware heavy-flat counts.

### 2026-06-27 - M1 repeated and infinity escape one-row forms

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The two remaining isolated boundary escape types
  now have pinned one-row formulas.  Repeated-root escapes use the
  domain-pole twist of `(X-xi)L_T`, and infinity escapes use the shifted
  one-row quotient for `L_T`.
- **How it is useful:** Together with the existing off-domain external-pole
  reduction, this turns every isolated escape in the slack-two M1 ledger into
  a one-row Hankel object rather than an unstructured leftover case.
- **What to do next:** Use the three one-row descriptions to bound the
  isolated escape slope image uniformly.

### 2026-06-27 - M1 root slices as a higher-slack core pencil

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The peeled root-slice slope set `Z_root` is shown
  to lie in the higher-slack core-locator slope image
  `Z_3={(R,z):(H_{3,j-1}(u)+zH_{3,j-1}(v))ell_R=0,
  H_{3,j-1}(v)ell_R!=0}`.  Hence the slack-two reduction also has the
  recursive form `|AperSlope| <= |Z_3| + (j+1)N_common + |Z_esc|`.
- **How it is useful:** This removes root slices as an independent
  obstruction type.  Same-slope `t=2` packets are charged to a standard
  higher-slack Hankel-pencil image, leaving the lifted one-row fiber term and
  isolated escapes as the main slack-two-specific targets.
- **What to do next:** Bound `Z_3` by an inductive or higher-slack M1 input,
  and continue sharpening the isolated escape term.

### 2026-06-27 - M1 lifted-common term as one-row fiber intersection

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The lifted-common term in the slack-two M1
  reduction is identified as
  `N_common = |Fib_1(f) cap Fib_1(g)| <= min(|Fib_1(f)|,|Fib_1(g)|)`, where
  `Fib_1(y)` is the one-degree-up `t=1` locator fiber
  `H_{1,j+1}(Syn(y))ell_W=0`.
- **How it is useful:** This connects the lifted side of M1 directly to a
  one-row locator-fiber input.  Any uniform `t=1` fiber theorem controls the
  `(j+1)N_common` term in the slack-two reduction, leaving root-slice slopes
  and isolated escapes as the genuinely slack-two pieces.
- **What to do next:** Use existing L1 or one-row locator-fiber bounds to
  estimate `Fib_1`, and continue the isolated-escape analysis separately.

### 2026-06-27 - M1 slack-two slope-image reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The slack-two aperiodic slope image is reduced to
  three explicit terms:
  `|AperSlope(f,g;2,j)| <= |Z_root| + (j+1)N_common + |Z_esc|`.
  Here `Z_root` is the constant root-slice slope set, `N_common` is the
  one-degree-up lifted common-base count, and `Z_esc` is the isolated escape
  slope image.
- **How it is useful:** This packages the current M1 route as a concrete
  conditional theorem: bounding the root-slice slopes, lifted common bases,
  and isolated escape slopes after quotient charging would prove the desired
  polynomial all-line aperiodic packing bound for `t=2`.
- **What to do next:** Attack the three terms separately, with priority on
  quotient-aware estimates for isolated escapes and reserve-scale bounds for
  `N_common`.

### 2026-06-27 - M1 fixed-anchor rank-stratified incidence cover

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The fixed-anchor rich-point arrangement now has a
  general rank-stratified cover.  For `d=dim V_xi`, every `j`-rich point lies
  in a heavy rowspace generated by root hyperplanes, giving
  `sum_{q=1}^{d-1} h_q (|F|^(d-q)-1)/(|F|-1)` as a universal rich-point and
  slope-image bound.
- **How it is useful:** This removes higher fixed-anchor dimension as an
  unstructured escape mechanism: all fixed-anchor escapes are now represented
  by a concrete heavy-flat ledger inside the Hankel-pencil arrangement.  The
  remaining M1 problem is to prove reserve-scale bounds for the relevant
  dimensions and quotient-aware heavy-flat counts.
- **What to do next:** Compare the heavy-flat ledger with the corrected M1
  reserve and look for quotient-periodic or product-structure savings in the
  heavy flats that survive the current charges.

### 2026-06-27 - M1 fixed-anchor three-space incidence bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The fixed-anchor rich-point arrangement is bounded
  when `dim V_xi=4`.  In projective three-space, rich points are covered by
  heavy root planes, heavy pair-intersection lines, and triple intersections
  of distinct root planes, giving
  `h_2(|F|^2+|F|+1)+h_1(|F|+1)+binom(M,3)`.
- **How it is useful:** This covers the dimension of the `F_13` fixed-anchor
  boundary row by an incidence theorem, so the remaining fixed-anchor
  obstruction is either `dim V_xi>=5` or sharpening the polynomial incidence
  bound to the reserve scale required by final M1.  The verifier asserts the
  three-space bound for every audited external anchor with `dim V_xi=4`.
- **What to do next:** Compare this polynomial incidence bound with the final
  reserve budget, and look for quotient-aware refinements in the `F_13`
  product model where the raw three-space bound is far from sharp.

### 2026-06-27 - M1 fixed-anchor projective-plane bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The fixed-anchor rich-point arrangement is bounded
  when `dim V_xi=3`.  In the projective plane, rich points are covered by
  heavy root lines, contributing at most `|F|+1` slopes each, and by pairwise
  intersections of the remaining root lines, giving
  `h(|F|+1)+binom(M,2)`.
- **How it is useful:** This closes the projective-plane fixed-anchor
  boundary case in the polynomial-field window and moves the remaining
  fixed-anchor M1 obstruction to `dim V_xi>=4`, matching the `F_13` boundary
  row.  The verifier asserts the heavy-line/pair-intersection bound for every
  audited external anchor with `dim V_xi=3`.
- **What to do next:** Attack `dim V_xi=4`, where the `F_13` row lives, using
  quotient-aware point-plane/line-incidence structure or the product-model
  normal forms already proved in this PR.

### 2026-06-27 - M1 low-dimensional fixed-anchor pencil bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** If the fixed external-anchor common kernel
  `V_xi` has dimension at most two, then its `j`-rich points and finite
  slopes are bounded.  For `dim V_xi=2`, if `r_xi` domain roots are fixed
  by the pencil, then `r_xi<j` and the number of rich points is at most
  `floor((n-r_xi)/(j-r_xi))`.
- **How it is useful:** This closes the projective-point and projective-line
  cases of the fixed-anchor rich-point arrangement, so the remaining
  fixed-anchor M1 boundary difficulty starts only when `dim V_xi >= 3`.
  The verifier asserts this bound for every audited external anchor in that
  range.
- **What to do next:** Attack the first genuinely higher-dimensional case,
  especially projective planes `dim V_xi=3`, using pair-incidence or
  quotient-aware root-arrangement bounds.

### 2026-06-27 - M1 fixed-anchor rich-point arrangement reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For a fixed external anchor `xi`, the off-domain
  boundary problem is rewritten as a projective root-hyperplane arrangement
  inside the pinned common kernel
  `P(xi)=H_{1,j+1}(u)P=H_{1,j+1}(v)P=0`.  Fixed-anchor split locators are
  exactly the `j`-rich points, and the slope map is the projective linear
  ratio from the twisted one-row forms.
- **How it is useful:** This turns the remaining M1 boundary term from
  anchor-slope bookkeeping into a concrete rich-point/slope-projection
  incidence problem.  The verifier checks the incidence model directly; in
  the `F_13` boundary row it finds `2380` projective kernel points, `39`
  rich points, `9` finite rich slopes, and `24` residual rich classes after
  quotient charging.
- **What to do next:** Prove a quotient-aware bound for the finite slope image
  of these rich points, or identify a counterexample family showing the
  necessary reserve scale.

### 2026-06-27 - M1 residual slope-fiber packing bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Every residual slope fiber is one-exchange-free
  after quotient charging and fixed-slope root-slice peeling.  Therefore no
  `(j-1)`-core occurs in two residual complements of the same slope, giving
  `|F_z| * j <= binom(n,j-1)`.
- **How it is useful:** This globalizes the fixed-anchor fiber packing bound
  to all residual slopes and controls multiplicity inside each bad residual
  slope fiber after the standard M1 charges.  The verifier checks the
  `(j-1)`-core disjointness directly.
- **What to do next:** Bound the number of nonempty residual slope fibers,
  especially the fixed external-anchor escape fibers; this result controls
  fiber size, not the slope image size.

### 2026-06-27 - M1 fixed-anchor fiber packing bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Each fixed off-domain `(anchor,slope)` fiber is
  one-exchange-free after quotient charging and root-slice peeling.  Hence no
  `(j-1)`-core occurs in two locator complements in the same fiber, giving
  `|F_{xi,z}| * j <= binom(n,j-1)`.
- **How it is useful:** This bounds multiplicity inside one pinned
  fixed-anchor slope fiber and recasts those fibers as support packings.  The
  verifier checks the `(j-1)`-core disjointness directly, including the six
  size-four fibers in the `F_13` boundary row.
- **What to do next:** Bound the number of nonempty fixed-anchor slope fibers;
  the packing bound controls fiber size, not the slope image size.

### 2026-06-27 - M1 fixed-anchor slope-fiber reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For each off-domain external anchor `xi` and slope
  `z`, the isolated boundary locators are identified with pinned split
  polynomials `P_T=(X-xi)L_T` satisfying the common one-row kernel equations
  and the twisted `t=1` gate `H_{1,j+1}(u^xi+zv^xi)P_T=0`.  The verifier
  groups off-domain escapes by `(anchor,slope)` and checks the pinned gate.
- **How it is useful:** This turns the remaining fixed-anchor escape term into
  an explicit slope-fiber problem.  In the `F_13` boundary row it recovers six
  anchor-slope fibers of size four over the single external anchor `0`.
- **What to do next:** Try to bound the number of nonempty pinned
  anchor-slope fibers, or prove a product/top-coefficient theorem explaining
  when such fibers can be large.

### 2026-06-27 - M1 lifted-side recursion bound

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The `t=2` residual lifted-core slope image satisfies
  `|Z_lift| <= (j+1)N_common`, where `N_common` counts one-degree-up common
  bases satisfying `H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0`.  Consequently
  `|Z_res| <= (j+1)N_common + |Z_esc|`.
- **How it is useful:** This makes the lifted side of the M1 residual packing
  additive/recursive: it is charged to a `t=1` common-base incidence count,
  leaving the isolated boundary escape slope image as the separate
  non-recursive term.
- **What to do next:** Seek a direct upper bound for the isolated boundary
  escape slope image, especially the fixed external-anchor twisted one-row
  image exposed by the `F_13` boundary model.

### 2026-06-27 - M1 residual component theorem

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** In the `t=2` M1 residual one-exchange graph, after
  quotient-periodic charging and root-slice peeling, every nontrivial
  connected component is exactly one slope-injective squarefree lifted-core
  clique.  Projective boundary lifts, including off-domain external-anchor
  escapes, repeated-root lifts, and infinity lifts, are isolated vertices.
- **How it is useful:** This turns the remaining local M1 packing problem into
  a count of lifted-core clique faces plus isolated boundary escapes, rather
  than an arbitrary Johnson-graph collision problem.
- **What to do next:** Use this component theorem to seek an upper bound for
  the number of lifted common cores with residual faces and for the isolated
  fixed-anchor boundary slope image.

### 2026-06-27 - M1 j=3 cubic-character residual floor

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For primes `p == 1 mod 3`, after charging the
  size-`3` quotient triples, the `j=3` full-domain monomial boundary residual
  product image is all of `F_p^*` for `p>=31`.  The proof uses cubic
  characters applied to `-r(1+r)` and excludes only five normalized parameters;
  the verifier audits `p=31,37,43` and records `p=19` as an additional small
  exception beyond the existing `(13,3)` audit row.
- **How it is useful:** Together with the cube-bijective case, this completes
  the `j=3` fixed-anchor field-size floor except for explicit small primes:
  one external anchor carries all nonzero residual slopes in both congruence
  classes for large enough `p`.
- **What to do next:** Use the completed `j=3` and `j=4` floors as sharp
  lower-bound targets for any positive fixed-anchor M1 product-image theorem.

### 2026-06-27 - M1 quartic pair-product proof audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The `j=4` residual field-size floor proof is
  clarified to count ordered pair parameters `(x,u)`, not raw product values
  in `A={x(1-x)}`.  A new verifier audit checks the pair-product proof
  constants at `p=53,59,61`, confirming that representation counts exceed the
  `24` collision/antipodal exclusions.
- **How it is useful:** This strengthens the proof spine of the quartic
  fixed-anchor floor by making the large-prime character-sum step and finite
  threshold audit explicit.
- **What to do next:** Use this proof-audited floor as the lower-bound scale
  when formulating a positive fixed-anchor product-image theorem for M1.

### 2026-06-27 - M1 j=4 residual field-size floor

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For every prime `p>=17`, the full-domain monomial
  boundary model with `j=4` has residual product image all of `F_p^*` after
  the antipodal quotient family is charged.  The proof uses a pair-product
  character-sum lower bound for `p>=53`, and the verifier audits
  `p=17,19,23,29,31,37,41,43,47`.
- **How it is useful:** This upgrades the `j=4` fixed-anchor floor from a
  finite `F_17` example to an infinite theorem: one external anchor can carry
  `p-1` residual slopes even after quotient-periodic locators are removed.
- **What to do next:** Convert the floor into the positive target scale for a
  general fixed-anchor product-image bound in the M1 residue-packing theorem.

### 2026-06-27 - M1 j=3 cube-bijective field-size floor

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For every prime `p >= 11` with `p == 2 mod 3`,
  the full-domain monomial boundary model with `j=3` has residual product
  image all of `F_p^*`: the cube map is bijective and no size-`3` quotient
  charge exists.  The verifier audits the theorem at `p=11,17,23,29`.
- **How it is useful:** This upgrades the fixed-anchor M1 boundary floor from
  a single `F_17` example to an infinite family: one external anchor can carry
  `p-1` residual nonzero slopes even after quotient-periodic locators are
  removed.
- **What to do next:** Find the analogous saturation or obstruction theorem
  for the `j=4` binary cubic image after antipodal quotient charging.

### 2026-06-27 - M1 quotient-fiber product ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain monomial boundary model now records
  the exact product formula for quotient-periodic locators: if
  `T=union a_i K_m` is a union of `c=j/m` cosets of the size-`m` subgroup,
  then `sum(T)=0` and `prod(T)=(-1)^{c(m+1)} prod_i a_i^m`.  The verifier
  checks the formula, the scale count `binom((p-1)/m,j/m)`, and the
  scale-specific product image in the audited rows.
- **How it is useful:** This separates the charged quotient product ledger
  from the residual product image in the fixed-anchor M1 boundary obstruction,
  making clear which product cosets are paid by quotient-periodic locators.
- **What to do next:** Use the quotient product ledger together with the
  normalized residual product map to bound the non-quotient `j=4` cubic image.

### 2026-06-27 - M1 general zero-sum product normal form

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain monomial boundary model now has a
  general normalized product theorem: every zero-sum `j`-subset scales to
  `{1,r_1,...,r_{j-2},-1-sum r_i}`, so its product image is the `j`th-power
  closure of `-r_1...r_{j-2}(1+sum r_i)`.  The note also records the general
  additive-character count
  `(binom(p-1,j)+(p-1)(-1)^j)/p` for zero-sum `j`-subsets of `F_p^*`.
- **How it is useful:** This consolidates the `j=3` quadratic and `j=4`
  cubic reductions into one reusable fixed-anchor boundary theorem for the M1
  all-line residue-packing route.
- **What to do next:** Apply the normal form to bound residual product-coset
  images after quotient charges, beginning with the binary cubic `j=4` case.

### 2026-06-27 - M1 quadruple product cubic reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain `j=4` monomial boundary product
  image is reduced to a binary cubic modulo fourth powers: every zero-sum
  quadruple normalizes to `lambda{1,r,s,-1-r-s}`, so
  `prod(T)=lambda^4(-rs(1+r+s))`; the ordered normalized parameter count is
  `p^2-9p+26`.
- **How it is useful:** This is the two-variable counterpart of the `j=3`
  quadratic reduction, converting the fixed-anchor M1 boundary obstruction
  into a concrete low-dimensional product-image problem after quotient
  locators are charged.
- **What to do next:** Try to bound the residual cubic product-coset image
  after antipodal quotient charging, keeping locator charging distinct from
  product-value overlap.

### 2026-06-27 - M1 triple product quadratic reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain `j=3` monomial boundary product
  image is reduced to one variable: every zero-sum triple normalizes to
  `lambda{1,r,-1-r}`, so `prod(T)=lambda^3(-r(1+r))` with
  `r in {-1,1,-2,-1/2}` excluded.  The verifier also checks that an active
  size-`3` quotient charge has cube-subgroup product image.
- **How it is useful:** This turns one fixed-anchor M1 boundary obstruction
  from a three-root packing question into a quadratic image modulo cubes,
  matching the all-line aperiodic residue-packing target after quotient
  locators are charged.
- **What to do next:** Use this one-variable reduction as the model for
  bounding fixed-anchor product images in larger `j` boundary strata, where
  quotient charging removes locators but product values may still overlap.

### 2026-06-27 - M1 full-domain zero-sum boundary counts

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Closed zero-sum counts are recorded for the
  full-domain monomial boundary model: `(p-1)(p-5)/6` for `j=3`, and
  `(p-1)(p^2-9p+26)/24` for `j=4`.  After charging antipodal pairs in the
  `j=4` case, the residual zero-sum count is `(p-1)(p-5)(p-7)/24`.
- **How it is useful:** These counts normalize the fixed-anchor product-image
  floor: they separate locator volume from product/coset image size and make
  the quotient charge quantitatively explicit.
- **What to do next:** Compare these exact counts with product-coset counts
  to formulate a candidate positive fixed-anchor product-image bound.

### 2026-06-27 - M1 product-image power-coset symmetry

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain monomial boundary product image is
  shown to be closed under multiplication by `j`th powers: scaling a zero-sum
  locator by `lambda` preserves zero-sum and quotient status while multiplying
  `prod(T)` by `lambda^j`.  The verifier asserts that charged and residual
  product images are unions of `(F_p^*)^j` cosets in the audited rows.
- **How it is useful:** This reduces the fixed-anchor boundary product
  problem to coset counting, not arbitrary product-set counting.  In the
  audited rows the residual images are `2`, `1`, `4`, and `1` such cosets.
- **What to do next:** Try to bound the number of residual product cosets
  after quotient charging, which is a sharper target than raw locator or
  product-fiber counts.

### 2026-06-27 - M1 antipodal quotient charge in product model

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** In the full-domain monomial boundary family with
  `j=4`, the quotient-charged zero-sum locators are identified exactly as
  unions of two antipodal pairs `{a,-a,b,-b}`.  Their product image is the
  square subgroup, and the verifier asserts this in the audited full-domain
  cases.
- **How it is useful:** This separates the obvious square-product floor from
  the genuinely residual boundary product image.  The field-size residual
  floor in `F_17` remains after the antipodal square family has already been
  charged.
- **What to do next:** Study the residual zero-sum product image after the
  antipodal quotient family is removed, aiming for a positive bound compatible
  with the fixed-anchor floor.

### 2026-06-27 - M1 fixed-anchor field-size floor

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The full-domain monomial boundary family is
  sharpened into a field-size floor: in the audited `F_17` cases `j=3` and
  `j=4`, after quotient charging the single external anchor `xi=0` carries
  all `16` nonzero slopes.
- **How it is useful:** This rules out constant-size or anchor-count style
  fixed-anchor boundary targets.  A viable M1 boundary theorem must bound
  product images at the correct scale, allowing a single anchor to contribute
  linearly many slopes.
- **What to do next:** Seek a positive product-image bound for fixed external
  anchors that matches this floor while remaining small enough for the M1
  reserve.

### 2026-06-27 - M1 full-domain monomial boundary family

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** A general full-domain boundary family is recorded:
  on `D=F_p^*`, with `t=2`, the monomial directions `A X^{p-2-j}` and
  `B X^{p-2}` have bad locators exactly on `sum(T)=0`, external anchor `0`,
  and slope `-A/(B(-1)^j prod(T))`.  The verifier audits this for
  `(p,j)=(13,4),(13,3),(17,4),(17,3)`.
- **How it is useful:** This explains the F13 product obstruction as an
  instance of a reusable fixed-anchor floor model.  Any proposed M1
  per-anchor boundary bound must control product images of zero-sum deleted
  root sets after quotient-periodic sets are charged.
- **What to do next:** Turn this floor model into a candidate sharp bound for
  fixed external poles, comparing zero-sum product images against the reserve
  budget in larger smooth-domain toy cases.

### 2026-06-27 - M1 exact F13 boundary product model

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The `F_13`, `n=12`, `j=4`, `t=2` boundary-only
  row is upgraded from an aggregate counterexample to an exact finite model.
  For every seed, bad locators are exactly the zero-sum four-subsets of
  `F_13^*`; the common external anchor is `0`; and the bad slope is
  `-(2s+3)/((3s+1)prod(T))`.
- **How it is useful:** This identifies the six residual boundary slopes as
  a product/top-coefficient image inside a single external anchor.  It gives a
  concrete floor model for any proposed per-anchor M1 boundary bound.
- **What to do next:** Use the product model as a test case for fixed-pole
  slope-image bounds, especially arguments that try to control products or
  top interpolation coefficients after quotient-periodic subsets are charged.

### 2026-06-27 - M1 external-anchor twisted reduction

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For a fixed off-domain anchor `xi`, every residual
  boundary locator `T` with projective lift `P_T=(X-xi)L_T` is rewritten as a
  one-row slope for the twisted line `u/(X-xi),v/(X-xi)`.  The verifier checks
  `H_1(u/(X-xi))P_T=(H_2(u)L_T)_0`, the corresponding denominator identity,
  and equality with the original residual slope for every off-domain escape.
  It also checks the equivalent top-coefficient form on `B=D\T`: the anchor
  equation locks the top two interpolation coefficients, and the residual
  slope cancels both.
- **How it is useful:** This is a structural replacement for external-anchor
  counting in Przemek's M1 all-line aperiodic target.  The boundary term now
  reduces, anchor by anchor, to a twisted one-row slope-image problem with an
  explicit interpolation-coefficient form.
- **What to do next:** Try to bound the twisted one-row slope image for a
  fixed external pole, starting with the boundary-only `F_13` row where
  `xi=0` carries all `24` residual locators and `6` slopes.

### 2026-06-27 - M1 external-anchor slope counterexample

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **What is being added:** The boundary-only `F_13`, `n=12`, `j=4`, `t=2`
  row is refined by grouping off-domain residual locators by external anchor.
  In every seed, all `24` residual locators share the single external anchor
  `xi_T=0`, yet the row still has `6` residual escape slopes and no
  squarefree lifted side.
- **How it is useful:** This rules out the shortcut of bounding Przemek's
  all-line aperiodic boundary term by external-anchor count alone.  The
  remaining M1 boundary proof needs a per-external-anchor slope-image bound.
- **What to do next:** Try to prove a structural bound for the slope image
  carried by one fixed external anchor after quotient-periodic and tangent
  locators have been charged.

### 2026-06-27 - M1 boundary-only projective counterexample

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT / EXPERIMENTAL.
- **What is being added:** The `F_13`, `n=12`, `j=4`, `t=2` row is recorded
  as a counterexample to the shortcut that all residual slopes can be absorbed
  into squarefree lifted-core fibers.  In every seed, all `24` residual
  locators are off-domain boundary singleton fibers, with no lifted common
  cores or squarefree fibers, yet `6` residual slopes remain.
- **How it is useful:** This clarifies the remaining M1 route: the
  projective fiber reduction has two necessary slope-image terms, squarefree
  in-domain fibers and boundary singleton fibers.
- **What to do next:** Develop a separate bound for the boundary singleton
  slope image, rather than trying to discard it or absorb it into lifted cores.

### 2026-06-27 - M1 projective lift-fiber ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The unique projective residual lift map is grouped
  into fibers.  Boundary lifts (repeated-root, off-domain, and infinity) are
  proved singleton fibers, while every nontrivial fiber is a squarefree
  in-domain lifted core and its unordered pairs account exactly for residual
  strict edges.
- **How it is useful:** This recasts the remaining M1 residue-packing object
  as a projective lifted-kernel incidence problem: edges and packets only come
  from squarefree in-domain fibers, while boundary lifts can contribute only
  isolated slopes.
- **What to do next:** Use the fiber form to bound the slope image by
  separately controlling squarefree fiber slopes and singleton boundary slopes.

### 2026-06-27 - M1 unique projective residual anchors

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** For each residual locator, the full projective
  one-root lift pencil intersects the common one-row lifted Hankel kernel in
  exactly one anchor, namely `[beta_1:beta_0]`.  The verifier enumerates all
  `p+1` projective anchors for each residual locator and asserts uniqueness.
- **How it is useful:** This removes anchor multiplicity from the residual M1
  packing object: every residual locator has a forced squarefree,
  repeated-root, off-domain, or infinity lift, so the remaining slope-image
  problem can be treated as a filtered incidence problem with no projective
  choice left over.
- **What to do next:** Use the unique-anchor incidence form to bound how many
  residual locators can project to genuinely new boundary slopes outside the
  squarefree lifted-core slope image.

### 2026-06-27 - M1 homogeneous residual lift ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The projective residual lift is made homogeneous:
  every residual locator `T` with `H(v)ell_T=(beta_0,beta_1)` maps through
  `beta_0 X L_T-beta_1 L_T` into the common one-row Hankel kernel for both
  numerator and denominator syndromes.  The beta0-zero case is now the same
  statement with an infinity anchor.
- **How it is useful:** This removes the last separate case distinction at
  the lift stage: the full residual M1 family, including isolated escapes, is
  a filtered boundary/squarefree slice of a common projective lifted-kernel
  incidence problem.
- **What to do next:** Use this projective-kernel incidence form to bound the
  slope image, starting with overlap or exclusion results for repeated-root,
  off-domain, and infinity-anchor boundary lifts.

### 2026-06-27 - M1 projective residual lift ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The residual-anchor ledger is upgraded to a
  projective lift ledger: every finite anchor `xi_T=beta_1/beta_0` makes
  `L_T(X)(X-xi_T)` satisfy both one-row lifted Hankel gates, even when the
  lift is repeated-root or off-domain.  Beta0-zero escapes are checked as
  infinity anchors.
- **How it is useful:** This turns the isolated escape side into explicit
  boundary cases of the lifted common-core geometry, narrowing the M1 residue
  packing task to squarefree in-domain common cores plus repeated-root,
  off-domain, and infinity-anchor boundary lifts.
- **What to do next:** Bound the slope images of the boundary lifts, or prove
  that their slopes are forced to overlap the squarefree lifted-core side
  after the existing quotient and root-slice charges.

### 2026-06-27 - M1 residual slope-image ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The residual anchor partition is upgraded to a
  slope-image ledger `Z_res=Z_lift union Z_esc`, where lifted slopes come from
  residual faces of lifted common cores and escape slopes come from isolated
  anchor escapes.  The verifier also asserts that residual faces inside each
  lifted common core are slope-injective.
- **How it is useful:** This addresses the actual M1 target slope image rather
  than only locator counts, separating the remaining proof into injective
  common-core residual-coordinate slopes and isolated escape slopes.
- **What to do next:** Bound `Z_lift` and `Z_esc` separately, starting with
  common-base residual-coordinate slope structure on the lifted side.

### 2026-06-27 - M1 residual anchor ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** An exact residual-anchor partition for the
  root-slice-peeled `t=2` M1 locator family.  A residual locator whose anchor
  `xi_T=beta_1/beta_0` is addable in the domain lifts to a common `(j+1)`-core;
  beta0-zero, in-support, and outside-domain anchors are certified as isolated
  residual locators.
- **How it is useful:** This accounts for both top-packet and isolated
  residual locators in one ledger, reducing the remaining M1 obstruction to
  lifted common-core face counting plus isolated anchor-escape slope counting.
- **What to do next:** Bound the two resulting slope sources separately:
  common-base residual faces and anchor escapes.

### 2026-06-27 - M1 lifted common-base residual slopes

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** The lifted-common-core census is sharpened to a
  common-base residual-slope form: each lifted core `W` gives a common
  `k+1` support `D\W` for both line words, and each noncontained face slope is
  the single residual-coordinate cancellation slope over that base.
- **How it is useful:** This recasts Przemek's M1 all-line aperiodic packet
  obstruction as filtered residual-coordinate slope counting over common
  bases, after quotient-periodic and root-slice charges have been paid.
- **What to do next:** Prove a uniform bound for how many lifted common cores
  can have at least two residual faces, or find a counterexample family where
  the residual-coordinate slopes evade the current charges.

### 2026-06-26 - M1 all-line Hankel aperiodic ledger

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/m1/m1_all_line_hankel_aperiodic_packing.md`,
  `experimental/scripts/verify_m1_all_line_hankel_aperiodic.py`,
  `experimental/scripts/README.md`, `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** A finite normal-form ledger for Przemek's M1
  all-line aperiodic residue-packing target.  It uses the Hankel-pencil test
  to partition split complement locators into contained/tangent-core,
  whole-fiber quotient-periodic, and aperiodic slope images, with a verifier
  that sweeps twelve deterministic polynomial-family line samples plus one
  arbitrary rank-one zero-slice probe, verifies the `t=2` determinant gate,
  reports strict one-exchange profiles for residual
  aperiodic locators, proves same-slope strict edges extend to fixed-slope
  root slices, verifies that different-slope strict edges are either isolated
  nonzero quadratic-slice roots or lie on zero-determinant slices, classifies
  each zero-determinant slice by the direction-pencil rank as contained,
  or constant-slope using the Hankel overlap identity, peels root-slice packets
  from fixed-slope fibers, proves the residual `t=2` one-exchange degree bound
  `<= j`, certifies the quadratic companion map for residual different-slope
  edges, proves the common companion anchor `xi_T=beta_1/beta_0` for oriented
  residual edge endpoints, proves the lifted denominator gate
  `H_{1,j+1}(v)ell_W=0` for every nontrivial residual top packet, upgrades it
  to the common lifted kernel
  `H_{1,j+1}(u)ell_W=H_{1,j+1}(v)ell_W=0`, classifies residual triangles as
  top-type after excluding star triangles, proves that every `j`-face of a
  lifted common-core top packet is contained or determinant-bad, forms the
  residual top-packet edge/triangle/degree ledger, proves the exact
  lifted-common-core census for residual top packets, verifies top-packet
  hypergraph linearity and vertex-disjointness on residual locators, and
  cross-checks every reported bad slope by direct RS interpolation.
- **How it is useful:** This turns the MCA half of the prize into a concrete
  counterexample-first object: after tangent and quotient-periodic locators
  are charged, the remaining all-line obstruction is the aperiodic split-locator
  slope image in the Hankel pencil.  The root-slice lemma separates same-slope
  strict collisions from the genuinely residual slope-image packing problem,
  while the quadratic-slice check isolates different-slope collisions as the
  next finite-degree object to bound.  The zero-slice dichotomy shows the
  exceptional branch is either contained or already a constant-slope root-slice
  packet.  The root-slice peeling check leaves a residual aperiodic family with
  no same-slope one-exchange edges and maximum strict degree at most `j`,
  isolating the remaining slope-fiber problem as a sparse nonzero-quadratic
  graph whose edges are forced by core-wise quadratic involutions.  The
  residual triangle check shows the first surviving cycles are top packets,
  not star fibers, and the top-packet ledger accounts exactly for residual
  edges, triangles, and endpoint degrees by slope-injective `(j+1)`-packets.
  The common companion anchor shows every residual locator has at most one
  added-root anchor, so these packets are vertex-disjoint on the residual
  locator side and their two-sections are disjoint top cliques.  The lifted
  gates move every nontrivial residual top packet one degree up into the common
  one-row Hankel kernel of the numerator and denominator syndromes.  In the
  lifted `t=1`, `j+1` window, these packets are contained/tangent-core
  locators; the remaining M1 task is to bound how many of their `j`-faces can
  survive the quotient-periodic charges and root-slice peeling.  The full
  lifted-face check shows the determinant gate itself is automatic on every
  `j`-face of such a lifted core, so the residual obstruction is now a filtered
  face-counting problem inside these common lifted cores.  The exact census
  identifies residual top packets with the lifted common cores that have at
  least two residual faces; singleton lifted cores account for isolated
  residual locators rather than clique packets.  The arbitrary probe shows the
  rank-one zero-slice branch is not merely formal, while still being classified
  by the contained/constant ledger.
- **What to do next:** Extend the verifier to richer line families and prove
  structural bounds for the aperiodic slope image, starting with `t=2` and
  quotient scales already separated by the existing M1 quotient ledgers.

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
