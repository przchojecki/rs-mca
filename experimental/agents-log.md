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

### 2026-07-02 - M5 A384 planted top overlap-one exclusion

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_deficiency_one_chart_theorem.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Residual pruning theorem for the
  declared planted top-chart family; no threshold or worst-case row claim.
- **What is being added:** Turn 21 of the `A=384` M5 packet: a Lagrange-dual
  argument excluding all non-planted top supports sharing exactly one root
  with the planted support.  The toy verifier enumerates all overlap-one
  `F_97/mu_16` supports.
- **How it is useful:** Sharpens the planted top residual from
  `|R cap T| in {0,1}` to the fully disjoint case `R cap T = empty`.
- **What to do next:** Attack the disjoint support-only equations or the
  rank-drop kernel-pivot residual.

### 2026-07-02 - M5 A384 planted top support-only residual

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_deficiency_one_chart_theorem.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Residual reduction for the
  declared planted top-chart family; no threshold or worst-case row claim.
- **What is being added:** Turn 20 of the `A=384` M5 packet: for each
  candidate support `R`, the planted top-chart equations determine at most one
  slope and reduce to explicit support-only consistency equations.  The
  `F_97/mu_16` toy compares this support-only test with full brute force.
- **How it is useful:** Converts the remaining planted top-chart wall from a
  slope/support search to a near-disjoint support-only residual.
- **What to do next:** Attack the support-only near-disjoint equations or the
  rank-drop kernel-pivot residual.

### 2026-07-02 - M5 A384 planted top-chart overlap pruning

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_deficiency_one_chart_theorem.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Structural pruning theorem for
  the declared planted top-chart family; no threshold or worst-case row claim.
- **What is being added:** Turn 19 of the `A=384` M5 packet: in the planted
  top-chart family with perturbation `v_m=m+2`, any non-planted valid top
  locator must share at most one root with the planted support.  The analogous
  `F_97/mu_16` model is brute-forced over all subgroup locators and slopes.
- **How it is useful:** Eliminates every near-support top-chart locator for
  the declared `F_17^32` family and sharpens the remaining root-table wall to
  the near-disjoint cases `|R cap T| in {0,1}`.
- **What to do next:** Attack or label the near-disjoint residual and the
  rank-drop kernel-pivot branches.

### 2026-07-02 - M5 A384 abstract deficiency-one chart theorem

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_deficiency_one_chart_theorem.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Abstract chart theorem; no
  threshold or worst-case row claim.
- **What is being added:** Turn 18 of the `A=384` underdetermined M5 packet:
  the reusable deficiency-one chart theorem.  It partitions finite slopes into
  rank-drop, full-rank low-degree, and full-rank top pseudo-remainder charts,
  proves the low-degree dedup rule, and records the degree bounds for top and
  generic rank-drop pivots.
- **How it is useful:** Closes the abstract U1-U5 chart reduction in a
  reusable form for future M5 packets; the remaining hard work is now exactly
  the `F_17^32` top/rank-drop root-table or a labelled residual branch.
- **What to do next:** Compute or honestly label the `F_17^32` top-chart
  pseudo-remainder root table and rank-drop kernel-pivot branches.

### 2026-07-02 - M5 A384 toy side-chart replay packet

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Declared toy packet; no
  threshold or worst-case row claim.
- **What is being added:** Turn 17 of the `A=384` underdetermined M5 packet:
  a replay artifact for the `F_97/mu_16` side-chart family.  It records the
  low-degree slope `z=32` as deduped to `A+1`, and the rank-drop slope `z=55`
  as a kernel-dimension-two projective scan with zero valid degree-four
  locators.
- **How it is useful:** Makes the side-chart reductions auditable in packet
  form, complementing the existing top-chart U1-U5 replay packet.
- **What to do next:** Transfer this packet discipline to the real
  `F_17^32` rank-drop/top root-table branches.

### 2026-07-02 - M5 A384 rank-drop kernel pivot

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Rank-drop reduction theorem; no
  threshold or worst-case row claim.
- **What is being added:** Turn 16 of the `A=384` underdetermined M5 packet:
  at a rank-drop slope, exact-`A` validity is reduced to the intersection of
  `P(ker M(z0))` with `L | X^n-1`; in the generic kernel-dimension-two case,
  this is a one-parameter pseudo-remainder problem with degree bound `n-j+1`.
- **How it is useful:** Converts the generic rank-drop branch from an
  unstructured side chart into a finite local kernel-pivot problem; for the
  real `A=384` row the local bound is `385`.
- **What to do next:** Implement a rank-drop root-table packet, or label
  higher-kernel/identically-valid branches as residuals with minimal
  witnesses.

### 2026-07-02 - M5 A384 low-degree dedup theorem

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  Exact-bucket dedup theorem; no
  threshold or worst-case row claim.
- **What is being added:** Turn 15 of the `A=384` underdetermined M5 packet:
  in the full-row-rank low-degree side chart `c_j=0`, the unique
  deficiency-one kernel locator has degree `<j`, so a split locator there is
  charged to agreement `>=A+1` rather than counted as a new exact-`A` root.
- **How it is useful:** Removes the low-degree side chart from the new
  exact-`A=384` root-table obligation, leaving the rank-drop and top
  pseudo-remainder charts as the substantive remaining branches.
- **What to do next:** Continue with root-table accounting or a closure lemma
  for the rank-drop and top-chart branches.

### 2026-07-02 - M5 A384 moment-support rank extension

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 14 of the `A=384` underdetermined M5 packet:
  the abstract moment-support factorization and locator-extension lemma.  It
  records that `S_m=sum w_l x_l^m` gives a Hankel block of rank at most the
  support size, with exact rank from the Vandermonde square, and that locators
  divisible by the support annihilator lie in the kernel.
- **How it is useful:** Promotes the planted top and rank-drop packets from
  isolated examples to instances of a reusable chart lemma for moment-support
  families.
- **What to do next:** Use this lemma as the clean low-rank/rank-drop branch
  while moving toward actual root-table accounting for the remaining
  `F_17^32` `A=384` charts.

### 2026-07-02 - M5 A384 F17 rank-drop side chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 13 of the `A=384` underdetermined M5 packet:
  a declared `F_17^32` rank-drop side-chart family.  It uses a 126-root
  moment support, verifies a nonzero prefix `126 x 126` moment minor, and
  checks that a degree-128 split locator lies in the resulting rank-126
  Hankel kernel.
- **How it is useful:** Completes the first replayable real-row triad of
  declared top, low-degree, and rank-drop chart examples for the
  deficiency-one boundary below the regular window.
- **What to do next:** Move from planted chart examples to root-table
  accounting or a uniform closure lemma for the `F_17^32` `A=384` side
  charts.

### 2026-07-02 - M5 A384 F17 low-degree side chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 12 of the `A=384` underdetermined M5 packet:
  a declared `F_17^32` low-degree side-chart family.  It constructs a
  degree-127 kernel locator with `c_128=0`, perturbs `S_255`, and verifies a
  nonzero shifted `128 x 128` minor.
- **How it is useful:** Gives a replayable real-row example of the full-rank
  low-degree/dedup side chart, complementing the planted top-chart packet.
- **What to do next:** Add a rank-drop side-chart packet or begin root-table
  accounting for declared `F_17^32` families.

### 2026-07-02 - M5 A384 F17 prefix-minor certificate

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 11 of the `A=384` underdetermined M5 packet:
  the planted `F_17^32` packet now computes the Vandermonde determinant on the
  128 planted roots and the prefix moment minor `det(V)^2`.
- **How it is useful:** Certifies the actual top Cramer coordinate
  `c_128 != 0`, so the planted slope is verified to be in the full-rank top
  chart rather than merely carrying a monic valid locator.
- **What to do next:** Use the same prefix-minor/root-table discipline for
  future `F_17^32` rank-drop, low-degree, and top pseudo-remainder packets.

### 2026-07-02 - M5 A384 F17 planted top chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 10 of the `A=384` underdetermined M5 packet:
  a declared `F_17^32` planted top-chart family.  The packet constructs a
  degree-128 locator from the first 128 descriptor-domain roots, generates the
  annihilated moment window, and verifies a nonconstant syndrome pencil hits it
  at a planted finite slope.
- **How it is useful:** Provides the first replayable real-row instantiation
  of the M5 deficiency-one chart, bridging the `F_97` acid tests to later
  `F_17^32` root-table packets.
- **What to do next:** Count or label the rank-drop, low-degree, and top
  pseudo-remainder charts for declared `F_17^32` families.

### 2026-07-02 - M5 A384 F97 acid test

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 9 of the `A=384` underdetermined M5 packet:
  an independent `F_97/mu_16` acid test.  The verifier enumerates all
  `binom(16,4)=1820` monic degree-four subgroup locators and compares direct
  bad slopes with the chart prediction on generic-empty, singleton-valid, and
  side-chart-routing toy families.
- **How it is useful:** Checks the Cramer/pseudo-remainder chart machinery
  against direct finite locator enumeration before attempting the much larger
  `F_17^32` packet.
- **What to do next:** Move to a declared `F_17^32` family packet, splitting
  rank-drop, low-degree, and top pseudo-remainder charts if needed.

### 2026-07-02 - M5 A384 chart-reduction theorem

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 8 of the `A=384` underdetermined M5 packet:
  the deficiency-one finite-slope chart reduction.  Every candidate finite
  bad slope in a nondegenerate declared family routes to rank-drop minors,
  the low-degree top-coefficient gate, or the top-chart pseudo-remainder
  equations.
- **How it is useful:** Converts the first underdetermined M5 bucket into
  explicit real-row algebraic targets: 129 Cramer minors of degree `<=128`,
  one low-degree gate of degree `<=128`, and 128 top-chart pseudo-remainder
  coefficients of degree `<=49280`.
- **What to do next:** Build the corresponding `F_17^32` root-table packet, or
  split the three charts into separate packets if the top chart is too large.

### 2026-07-02 - M5 A384 subgroup divisibility gate

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 7 of the `A=384` underdetermined M5 packet:
  an abstract subgroup-divisibility gate and its arithmetic specialization.
  When `H` is the full root set of `X^n-1` and the characteristic does not
  divide `n`, a degree-`j` top-chart locator is valid exactly when it divides
  `X^n-1`.
- **How it is useful:** Checks the real row hypotheses
  `512 | 17^32-1`, `v_2(17^32-1)=9`, and `17` not dividing `512`, so the
  `A=384` top-chart validity problem is correctly reduced to the
  pseudo-remainder equations against `X^512-1`.
- **What to do next:** Compute or label the real-row pseudo-remainder gcd/root
  table, with rank-drop and low-degree side charts tracked separately.

### 2026-07-02 - M5 A384 degree-budget theorem

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 6 of the `A=384` underdetermined M5 packet:
  an abstract deficiency-one chart degree budget.  For a `t x (t+1)`
  affine-linear Hankel pencil, Cramer minors have slope-degree `<= t`, the
  generic rank-drop and low-degree side charts have degree cap `<= t`, and
  top-chart pseudo-remainder coefficients have degree `<= (n-j+1)t`.
- **How it is useful:** Specializes the first real underdetermined row to
  side-chart caps `128` and top-chart coefficient cap `49280`, making the next
  `F_17^32` packet a precise finite algebraic target rather than an informal
  large computation.
- **What to do next:** Attempt a declared `F_17^32` family packet or emit a
  labelled residual with replayed spot checks and the U6 degree caps.

### 2026-07-02 - M5 A384 toy U1-U5 packet

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** A compact replay packet for the declared
  `F_97/mu_16`, `n=16,k=8,A=12` deficiency-one top-chart toy.  The verifier's
  `--check` mode recomputes the U1-U5 payload and compares it exactly to the
  committed JSON.
- **How it is useful:** Makes the M5 deficiency-one toy chart replayable as a
  certificate-like artifact before the larger `F_17^32` packet is attempted.
- **What to do next:** Start the declared `F_17^32` family packet or, if full
  pseudo-remainder interpolation is too large, emit an honest computational
  residual label with spot checks and degree bounds.

### 2026-07-02 - M5 A384 toy eliminant dichotomy

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 4 of the `A=384` underdetermined M5 packet:
  the declared `F_97/mu_16` top-chart pseudo-remainder coefficients are
  interpolated as polynomials in the slope, and their monic gcd is verified to
  be the constant eliminant `1`.
- **How it is useful:** This closes the declared toy top chart as empty and
  exercises the U5 eliminant-or-residual end state before attempting the much
  larger `F_17^32` family.
- **What to do next:** Emit a compact packet for the toy U1-U5 replay, then
  start the declared `F_17^32` family with honest computational or residual
  labels if full interpolation is too large.

### 2026-07-02 - M5 A384 toy divisibility gate

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 3 of the `A=384` underdetermined M5 packet:
  the `F_97/mu_16` top-chart divisibility gate.  For every slope, the verifier
  compares direct division of `X^16-1` by the Cramer locator, pseudo-remainder
  vanishing, and root containment in `mu_16`; it also checks the exact
  pseudo-division scaling identity.
- **How it is useful:** This verifies the first non-vacuous split-locator
  validity gate on the deficiency-one toy chart before any large-field
  eliminant is attempted.
- **What to do next:** Extend the same gate to side charts and then emit the
  U5 eliminant-or-residual dichotomy for the toy row, followed by the declared
  `F_17^32` packet.

### 2026-07-02 - M5 A384 deficiency-one Cramer chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / EXPERIMENTAL.  No threshold or worst-case row
  claim.
- **What is being added:** Turn 2 of the `A=384` underdetermined M5 packet:
  the deficiency-one Cramer-kernel lemma and exact toy verification.  For each
  full-row-rank `4 x 5` toy Hankel split, the signed maximal-minor vector is
  checked against an independently computed RREF kernel vector at every slope;
  rank-drop slopes have all maximal minors zero.
- **How it is useful:** This supplies the first actual chart coordinate for
  the band-facing `A=384` deficiency-one program, turning vacuous kernel
  nonemptiness into a concrete bivariate locator `L_Z(X)` whose next gate is
  divisibility by `X^512-1`.
- **What to do next:** Prove and verify U3/U4: on the top-coefficient chart,
  valid locators are exactly those for which the Cramer locator divides
  `X^n-1`, using pseudo-remainder equations and side charts for rank drop and
  low-degree kernels.

### 2026-07-02 - Towards-prize v3 cap-paper package

- **Agent/model:** Codex.
- **Files added or changed:** `tex/towards-prize.tex`;
  `towards-prize.pdf`; `archived/towards-prize_v2.tex`;
  `archived/towards-prize_v2.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE / COMPILED.
- **What is being added:** `towards-prize.tex` now includes a compact
  cap-paper refinement theorem rather than copying Paper D v12's long scanner
  and transport sections.  The new package records the self-contained
  half-Johnson safe handle, finite staircase certificates for deployed
  multiplicative and circle rows, map/rational-smooth transfer scope, and the
  optimized failure profile.
- **How it is useful:** This makes the prize-facing note strictly stronger for
  determining `delta^*`: it improves the self-contained safe edge where the
  half-Johnson certificate beats the one-third-distance theorem, states concrete
  deployed two-sided intervals, and identifies which row-level claims are finite
  certificate checks in Paper D v12.
- **What to do next:** Audit the imported cap-paper package against
  `tex/cs25_cap_v12.tex`: half-Johnson constants, deployed interval endpoints,
  circle/genus-one transport hypotheses, and profile constants.

### 2026-07-02 - Towards-prize v2 promotion

- **Agent/model:** Codex, reviewing maintainer-added draft.
- **Files added or changed:** `tex/towards-prize.tex`;
  `towards-prize.pdf`; `archived/towards-prize_v1.tex`;
  `archived/towards-prize_v1.pdf`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE / COMPILED.
- **What is being added:** The maintainer-added `towards-prize_v2.tex` is
  promoted to the canonical `tex/towards-prize.tex`.  Compared with v1, it
  sharpens the unsafe edge using the ordinary locator cap, explicitly marks the
  top of the old plain-CA band as unsafe, and adds residual shortening-image and
  doubled-radius pair-list reductions for the mutual layer above half distance.
- **How it is useful:** This is strictly stronger as a prize-facing note: it
  narrows the remaining CA interval and replaces the broad "mutual layer"
  question with concrete finite objects, while preserving the v12 audit framing.
- **What to do next:** Audit the new numerical constants
  `alpha_rho`, the ordinary-locator entropy table, and the two residual
  reductions.  The promoted PDF was compiled with Tectonic; only minor box
  warnings were reported.

### 2026-07-02 - Paper D v12 reference sweep

- **Agent/model:** Codex.
- **Files added or changed:** `readme.md`; `agents.md`;
  `towards-prize.md`; `site/index.html`; `site/data/papers.json`;
  `site/data/rate-leaderboards.json`; `site/data/updates.json`;
  `site/papers/cs25_cap_v12.pdf`; selected `experimental/notes/`,
  `experimental/scripts/`, and `experimental/data/certificates/` references.
- **Status:** AUDIT / DOCUMENTATION / VERSION-PROMOTION.
- **What is being added:** Active Paper D references were moved to
  `tex/cs25_cap_v12.tex`, and contributor-facing text now says that v12 is the
  main cap paper to audit.  The public site metadata and local PDF mirror were
  updated to point at the v12 package.
- **How it is useful:** Prevents new agents from following the superseded v10
  Hankel-ledger draft as the current cap-paper source, while preserving older
  v6--v10 audit/log entries as historical provenance.
- **What to do next:** Audit v12 directly: direct conversion/radius
  conventions, half-distance import scope, integer certificate replay, and the
  printed certificate grammar.

### 2026-07-02 - Paper D v12 and towards-prize audit focus

- **Agent/model:** Codex, reviewing maintainer-added drafts.
- **Files added or changed:** `tex/cs25_cap_v11.tex`;
  `tex/cs25_cap_v12.tex`; `tex/towards-prize.tex`;
  `cs25_cap_v11.pdf`; `cs25_cap_v12.pdf`; `towards-prize.pdf`;
  `AGENTS.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / VERSION-PROMOTION-CANDIDATE.
- **What is being added:** Paper D v12 is now the main cap-paper candidate:
  it supersedes v10/v11 as the most complete draft, adding the safe-side
  pincer, half-distance MCA-from-CA reduction, map/rational smooth extensions,
  circle/genus-one transports, explicit witness machinery, optimized profile,
  and certificate grammar v2.  `tex/towards-prize.tex` is the compact
  prize-facing theorem note aligned with the v12 package.
- **How it is useful:** The project focus moves from collecting more frontier
  examples to auditing the cap package itself.  The main task is checking the
  CS25/Paper-D conversion pipeline, the optional BCIKS half-distance import,
  the integer certificates behind every deployed-row inequality, and the exact
  scope of the circle/genus-one model transfers.
- **What to do next:** Treat CS25/Paper-D auditing as the main focus.  Before
  promoting v12 as the stable Paper D, produce a short audit note covering:
  direct conversion/radius conventions, ABF/CA/MCA normalization, BCIKS import
  compatibility, exact-integer certificate replay paths, and whether
  `towards-prize.tex` states only the claims actually proved by v12.

### 2026-07-02 - Post-v10 PR sweep: M1 reductions, M3 synthetic packets, M5 underdetermined roadmap

- **Agent/model:** Codex, integrating and auditing contributions from
  AllenGrahamHart, DannyExperiments, and Gia.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-07-02-post-v10.md`;
  `experimental/notes/audits/m0_prize_mca_definition_freeze.md`;
  `experimental/notes/m1/m1_simple_pole_projected_locator_wall.md`;
  `experimental/notes/m1/m1_dyadic_shifted_prefix_value_bridge.md`;
  `experimental/notes/m3/m3_low_rank_affine_spectral_reduction.md`;
  `experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`;
  selected `experimental/data/certificates/hankel-f17-32-m3-*` packets;
  selected `experimental/scripts/verify_f17_32_m3_*` scripts;
  `experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py`;
  `experimental/notes/roadmaps/proximity_prize_execution_roadmap_post_v10_r2.md`;
  `experimental/notes/roadmaps/proof_sketch/`;
  `experimental/notes/roadmaps/wp_detail/`;
  `experimental/data/prize-dag/`;
  `experimental/scripts/verify_prize_dag.py`;
  `experimental/scripts/verify_roadmap_r2_numbers.py`;
  `experimental/scripts/plot_prize_dag.py`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `towards-prize.md`.
- **Status:** AUDIT / PROVED-LOCAL / EXPERIMENTAL / ROADMAP.  No leaderboard
  movement and no new prize-facing threshold claim.
- **What is being added:** The batch integrates Danny/Gia's M1 simple-pole and
  shifted-prefix reductions, Allen's synthetic low-rank M3/M4 packet material,
  Allen's M5 `A=384` underdetermined-boundary packet, and Allen's post-v10 r2
  roadmap/DAG as subordinate planning material.  From the large rank-witness
  PR only the M0 definition-freeze note and packet-checker enhancement were
  taken; the generated rank-6 sidecars remain held for split/replay.
- **How it is useful:** The main new strategic point is that the official
  prize band is entirely underdetermined, so regular M3 packets are a proving
  ground while M5 underdetermined charts are the real band-facing program.
  The M1 reductions isolate cleaner projected-value walls, and the M3
  low-rank packets provide scoped synthetic tests for the then-current v10
  ledger style, now superseded by Paper D v12.
- **What to do next:** Refine the `A=384` M5 Cramer/divisibility chart into an
  eliminant or named residual obstruction; replay or split any #171 rank-6
  material before integration; and keep new PRs to one theorem cluster or
  certificate packet at a time.

### 2026-07-01 - v10 guide and site metadata sync

- **Agent/model:** Codex.
- **Files added or changed:** `AGENTS.md`; `README.md`/`readme.md`;
  `site/index.html`; `site/papers/cs25_cap_v10.pdf`;
  `towards-prize.md`; `experimental/agents-log.md`.
- **Status:** AUDIT / DOCUMENTATION.
- **What is being added:** The agent guide, repo overview, prize roadmap, and
  site paper metadata were then pointed at Paper D v10 as the cap/Hankel-ledger
  package.  Paper D v12 now supersedes this entry.  `AGENTS.md` also named the
  next concrete prize task: an M3/M4
  root-table and paid-root-subtraction packet for the `F_17^32`, `n=512`,
  `k=256` row over agreements `385 <= A <= 426`.
- **How it is useful:** Historical provenance for the v10 transition away from
  v9, strict264, and strict352 as the active frontier.  The current successor
  route is Paper D v12's safe-side pincer and certificate grammar.
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
  tangent ledgers, and build pivot eliminants for any singular buckets.  For
  current citations, use Paper D v12 rather than this v10 milestone note.

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
- **What is being added:** The scanner then emitted `PROVED_PAPERD_V5_CAP` for
  then-active Paper D v5 cap rows whose divisor, binomial, and field hypotheses pass,
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
