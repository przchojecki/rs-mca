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

### 2026-07-02 - M3 A386 component-cut safety criterion

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_a386_component_cut_safety.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/`;
  `experimental/notes/m1/hankel_rank6_a386_component_cut_safety.md`;
  `experimental/notes/m1/hankel_rank6_a386_conic_pair_safety.md`;
  `experimental/notes/m1/hankel_rank6_boundary_low_degree_transfer.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A component-cut criterion for the `A=386` separated
  rank-6 residual: if each irreducible component of a common component of two
  direction conics is cut by some direction conic, finite roots are `<=4` and
  endpoint gives total `<=5<=6`.
- **How it is useful:** It narrows the `A=386` residual from arbitrary common
  components to irreducible components contained in all direction-consistency
  conics.
- **What to do next:** Classify or scan the global-component residual, then
  attempt the harder `A=385` `Q`-space.

### 2026-07-01 - M3 rank-6 endpoint uniformity

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_projective_endpoint_uniform.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/`;
  `experimental/notes/m1/hankel_rank6_projective_endpoint_uniform.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A support- and weight-uniform rank-6 projective
  endpoint theorem: for any disjoint base support of size `j+1`, any six
  direction nodes, and nonzero weights in the M3 window, `[0:1]` has a genuine
  split-locator witness.
- **How it is useful:** It shows rank-6 endpoint nonemptiness is robust and not
  a prefix/unit-weight artifact; finite-root refinement or payment is still
  needed for general rank-6 closure.
- **What to do next:** Pair this endpoint theorem with finite-root
  table/refinement results for broader rank-6 Hankel families.

### 2026-07-01 - M3 separated rank-6 tall closure

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_separated_six_spike_closure.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-separated-six-spike-closure/`;
  `experimental/notes/m1/hankel_rank6_separated_six_spike_closure.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A support- and weight-uniform closure for separated
  six-spike rank-6 Hankel families on `388 <= A <= 426`: every finite slope has
  full column rank by weighted Vandermonde factorization, and the only
  projective contribution is the endpoint `[0:1]`.
- **How it is useful:** It pairs the endpoint-uniform theorem with a finite-root
  emptiness theorem in the tall range, closing a robust rank-6 subfamily without
  relying on prefix supports or unit weights.
- **What to do next:** Attack the boundary agreements `A=385,386,387` for the
  same support/weight-uniform family, or move to overlapping-support rank-6
  cancellation strata.

### 2026-07-01 - M3 rank-6 boundary barycentric obstruction

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_boundary_barycentric_obstruction.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/`;
  `experimental/notes/m1/hankel_rank6_boundary_barycentric_obstruction.md`;
  `experimental/notes/m1/hankel_rank6_separated_six_spike_closure.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / PROVED.
- **What is being added:** A boundary obstruction for the support/weight-uniform
  separated rank-6 closure: for `A=385,386,387`, barycentric-residue weights on
  `S=X union Y` put the constant locator in `ker H(u+v)` at finite slope `z=1`.
- **How it is useful:** It proves the tall cutoff `A>=388` in the separated
  six-spike closure is sharp and prevents wasting effort on a false uniform
  empty finite-root extension at the boundary.
- **What to do next:** Treat the boundary agreements with a paid-root argument,
  exact finite-root classification, or additional hypotheses on the weights.

### 2026-07-01 - M3 barycentric split-locator filter

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_barycentric_split_filter.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/`;
  `experimental/notes/m1/hankel_rank6_barycentric_split_filter.md`;
  `experimental/notes/m1/hankel_rank6_boundary_barycentric_obstruction.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A split-locator filter for the barycentric boundary
  root: at `A=385,386,387`, the displayed ambient root `z=1` has kernel
  polynomials only of degree `< |S|-t` (`5,3,1`), so it contains no degree-`j`
  split locator.
- **How it is useful:** It separates ambient rank-drop sharpness from actual
  support-wise split-locator witnesses, showing the barycentric obstruction's
  displayed root is not itself an MCA bad slope.
- **What to do next:** Continue boundary rank-6 work with exact root tables or
  paid-root audits for other roots and other weight strata.

### 2026-07-01 - M3 barycentric exact root table

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_barycentric_exact_root_table.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/`;
  `experimental/notes/m1/hankel_rank6_barycentric_exact_root_table.md`;
  `experimental/notes/m1/hankel_rank6_barycentric_split_filter.md`;
  `experimental/notes/m1/hankel_rank6_boundary_barycentric_obstruction.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** An exact finite root table for the boundary
  barycentric separated rank-6 family: the ambient finite roots are exactly
  `{1}`, that root is split-filtered, and the endpoint-uniform theorem leaves
  support-wise projective total `1`.
- **How it is useful:** It converts the barycentric boundary obstruction into a
  closed harmless family after the split-locator gate, clarifying what remains
  open in the rank-6 boundary.
- **What to do next:** Apply the same exact-root plus split-filter pattern to
  other boundary weight strata, or identify a stratum where a degree-`j` split
  locator genuinely survives.

### 2026-07-01 - M3 rank-6 boundary low-degree transfer

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_boundary_low_degree_transfer.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/`;
  `experimental/notes/m1/hankel_rank6_boundary_low_degree_transfer.md`;
  `experimental/notes/m1/hankel_rank6_barycentric_exact_root_table.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A general transfer theorem for separated rank-6
  boundary finite roots: arbitrary nonzero weights at `A=385,386,387` reduce
  to an auxiliary polynomial `Q` of degree `< h` with `h=5,3,1`, six
  direction-node consistency equations, and then the split-locator gate.
- **How it is useful:** It turns the remaining separated boundary root-table
  problem into projective `Q`-spaces of dimensions `4,2,0`, making future
  exact-root or counterexample searches much smaller and more structured.
- **What to do next:** Solve or falsify the six consistency equations for
  natural weight strata, then apply the split-locator divisor gate to `L_Q`.

### 2026-07-01 - M3 A387 separated rank-6 safety

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_a387_separated_boundary_safety.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-a387-separated-boundary-safety/`;
  `experimental/notes/m1/hankel_rank6_a387_separated_boundary_safety.md`;
  `experimental/notes/m1/hankel_rank6_boundary_low_degree_transfer.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A projective-safety theorem for arbitrary nonzero
  separated rank-6 weights at `A=387`: the low-degree transfer has `h=1`, so
  there is at most one finite split-locator root and the endpoint adds one more
  parameter, giving total `<=2<=6`.
- **How it is useful:** It closes one of the three separated boundary
  agreements for arbitrary weights, leaving only the harder `A=385,386`
  consistency spaces in this separated rank-6 boundary lane.
- **What to do next:** Attack `A=386` next, where the transfer leaves a
  projective `Q`-plane and six consistency equations before the split gate.

### 2026-07-01 - M3 A386 conic-pair safety criterion

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_a386_conic_pair_safety.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/`;
  `experimental/notes/m1/hankel_rank6_a386_conic_pair_safety.md`;
  `experimental/notes/m1/hankel_rank6_boundary_low_degree_transfer.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A projective-safety criterion for separated rank-6
  weights at `A=386`: if two direction consistency conics in the transferred
  `Q`-plane have no common component, Bezout gives at most four finite roots;
  with the endpoint, total contribution is `<=5<=6`.
- **How it is useful:** It closes the generic `A=386` separated case and names
  the common-component conic case as the residual to classify.
- **What to do next:** Analyze the common-component residual or implement a
  small scanner to test how often it appears in structured weight families.

### 2026-07-01 - M3 rank-6 boundary dual gcd

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/`;
  `experimental/notes/m1/hankel_rank6_boundary_dual_gcd.md`;
  `experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/`;
  `experimental/notes/m1/hankel_rank6_projective_witness.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / COMPUTATIONAL.
- **What is being added:** An exact dual-gcd computation for the
  prefix-plus-six-spikes rank-6 family at `A=385,386,387`, proving the finite
  canonical root table is empty there and upgrading the projective witness
  family to the full `385 <= A <= 426` regular window.
- **How it is useful:** It removes the only gap in that synthetic rank-6
  endpoint family and clarifies that the remaining rank-6 wall is not this
  family, but simultaneous finite-root sharpness or endpoint payment in more
  general Hankel pencils.
- **What to do next:** Use the same small dual-pencil method on other
  rank-6 structured families when direct full-support Vandermonde rank is not
  available.

### 2026-07-01 - M3 rank-6 projective witness family

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/`;
  `experimental/notes/m1/hankel_rank6_projective_witness.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for this synthetic family.
- **What is being added:** A rank-6 Hankel-realizable prefix-plus-six-spikes
  family for `385 <= A <= 426` with empty finite canonical root table and a
  genuine split-locator projective endpoint; the three boundary agreements are
  closed by a dual-gcd companion.
- **How it is useful:** It shows the rank-6 endpoint-sensitive boundary cannot
  be closed by claiming endpoint emptiness from Hankel realizability alone;
  future work needs endpoint payment, exact finite root tables, or sharper
  Hankel-specific classification.
- **What to do next:** Search for or rule out simultaneous Hankel-realizable
  six finite roots plus a split projective endpoint; this remains a synthetic
  family result, not a worst-case row bound.

### 2026-07-01 - M3 projective split-locator gate

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m3_projective_split_locator_gate.py`;
  `experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/`;
  `experimental/notes/m1/hankel_projective_split_locator_gate.md`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A projective-infinity split-locator gate for M3:
  ambient endpoint vectors satisfy `H(v)ell=0, H(u)ell!=0`, but actual
  support-wise endpoint witnesses must normalize to monic degree-`j` divisors
  of `X^512-1`.
- **How it is useful:** It sharpens the rank-6 endpoint-sensitive boundary by
  separating large ambient endpoint kernels from genuine split-locator
  endpoints that future beta packets may count or pay.
- **What to do next:** Apply this gate to rank-6 Hankel endpoint searches and
  compressed root-table packets; this entry does not claim endpoint
  payment or emptiness.

### 2026-07-01 - M3 null-polynomial split-locator gate

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py`;
  `experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/`;
  `experimental/notes/m1/hankel_nullpolynomial_split_locator_gate.md`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A null-polynomial gate for M3 finite roots: ambient
  regular roots are Hankel kernel polynomials, and actual split-locator bad
  slopes must pass the divisor gate `L | X^512-1` and the noncontainment gate
  `H(v)ell != 0`.
- **How it is useful:** It tells future root-table packets how to filter
  ambient regular roots into genuine split-locator witnesses instead of
  conflating rank drop with support-wise noncontainment.
- **What to do next:** Apply the gate to concrete M3 root tables or singular
  pivot packets.

### 2026-07-01 - M3 rank-node dichotomy

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/`;
  `experimental/notes/m1/hankel_rank_node_dichotomy.md`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A finite rank-node dichotomy for M3 regular buckets:
  one full-rank finite specialization gives a nonzero maximal minor, while
  rank deficiency at `j+2` distinct finite nodes forces every maximal minor to
  vanish identically.
- **How it is useful:** It gives future M3/M4 packets a replayable
  regular-versus-singular gate before root-table computation or M5 pivot charts.
- **What to do next:** Use the gate on concrete arbitrary syndrome pencils to
  produce actual root tables or singular residual declarations.

### 2026-07-01 - M3 subgroup syndrome section

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_subgroup_syndrome_section.py`;
  `experimental/data/certificates/subgroup-syndrome-section/`;
  `experimental/notes/m1/subgroup_syndrome_section.md`;
  `experimental/scripts/verify_f17_32_m3_syndrome_realizability.py`;
  `experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A reusable subgroup-section theorem for the pinned
  `F_17^32` M3 row: every length-256 syndrome vector has explicit received-line
  values on the order-512 subgroup.
- **How it is useful:** It removes the row-data ambiguity for future M3
  regular-window packets; the remaining hard work is root-table and residual
  classification, not realizing syndrome pencils as line values.
- **What to do next:** Use this section theorem when constructing actual
  M3/M4 root-table or singular-pivot packets.

### 2026-07-01 - M4 affine-pivot gcd equivalence

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A bridge from affine-pivot compression to the v10
  canonical gcd: nonzero rank-6 minors have at most six bad finite pivots, and
  replacing each chart by its compressed determinant translated back to the
  global slope variable preserves the monic gcd root set.
- **How it is useful:** It makes the compressed `6 x 6` rank-6 chart
  determinants usable for canonical root-table computation, not just for
  individual selected minors.
- **What to do next:** Choose concrete rank-6 Hankel charts and compute the
  compressed canonical gcd/root table, or combine with an endpoint payment.

### 2026-07-01 - M4 affine-pivot compression

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A chart-local affine-pivot compression theorem:
  if `M_R(z0)` is invertible and `H_R(v)=P_R Q_R` has rank `r`, then
  `det M_R(z0+w)` equals `det M_R(z0)` times an `r x r` determinant.
- **How it is useful:** It turns the rank-6 endpoint-sensitive finite-root
  problem from an `87..128` dimensional determinant problem into a `6 x 6`
  compressed determinant problem on each affine pivot chart.
- **What to do next:** Use this compression to compute or bound the common
  rank-6 finite root table, or pair it with an endpoint payment/emptiness
  certificate.

### 2026-07-01 - M4 rank-6 ambient sharpness

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/README.md`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** COUNTEREXAMPLE / AUDIT.
- **What is being added:** An ambient regular-pencil sharpness construction
  for the rank-6 boundary: rank `6`, six finite canonical roots, and one
  projective endpoint can occur simultaneously in the M3 dimensions.
- **How it is useful:** It shows that the rank-6 endpoint-sensitive boundary
  cannot be closed using only direction rank, regularity, and one-point
  projective accounting; the next step must use Hankel structure, exact root
  tables, or paid endpoint ledgers.
- **What to do next:** Attack rank `6` with genuinely Hankel-specific root
  tables or endpoint-payment/emptiness certificates.

### 2026-07-01 - M4 projective direction-rank budget split

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A projective budget split for arbitrary nonsingular
  regular buckets: direction rank `<=5` is projective-safe before endpoint
  payment, while direction rank `6` is finite-safe but endpoint-sensitive.
- **How it is useful:** It tightens the M4 regular-bucket decision table by
  turning the former rank-`<=6` projective gap into a precise rank-`<=5` safe
  class plus a named rank-`6` boundary.
- **What to do next:** Attack the endpoint-sensitive rank-`6` boundary by
  proving endpoint payment/emptiness or by computing exact finite root tables.

### 2026-07-01 - M0 prize MCA definition freeze

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/notes/audits/m0_prize_mca_definition_freeze.md`;
  `towards-prize.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A compact M0 convention note for the
  prize-facing `RS[F_17^32,H,256]` row, including the support-wise MCA object,
  same-support noncontainment, finite/projective samplers, endpoint convention,
  and `q_gen/q_line/q_chal` separation.
- **How it is useful:** It satisfies the current `towards-prize.md` M0 exit
  criterion and gives later M1/M3/M4 packets a single convention reference.
- **What to do next:** Human-review the predicate-level match to the external
  sampler and keep future packets explicit about sampler, denominator, and
  endpoint choices.

### 2026-07-01 - M3 support-uniform one-spike theorem

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_one_spike_uniform.py`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-uniform/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A support-and-weight uniform one-spike theorem for
  every `385 <= A <= 426`: arbitrary base support of size `j+1`, arbitrary
  spike outside it, and arbitrary nonzero weights have empty finite canonical
  root table and exact projective endpoint contribution `1`.
- **How it is useful:** It upgrades the one-spike chain from a prefix synthetic
  example to a reusable family theorem in the M3 regular-window atlas.
- **What to do next:** Look for the next family where selected-minor root
  evidence can be promoted to a canonical-gcd theorem, or move to the first
  genuine singular/pivot chart.

### 2026-07-01 - M3 one-spike projective witness

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_one_spike_projective_witness.py`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/`;
  `experimental/scripts/verify_f17_32_m3_one_spike_m4_budget.py`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** An explicit split-locator witness for the one-spike
  projective-infinity endpoint at every `385 <= A <= 426`.
- **How it is useful:** It upgrades the one-spike projective endpoint from an
  M5 one-point upper bound to an exact contribution `1`, and the M4 budget
  table now records this lower/upper match.
- **What to do next:** Use the same explicit chart-closure standard for the
  next projective or singular M5 packet.

### 2026-07-01 - M3 one-spike M4 budget table

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_one_spike_m4_budget.py`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for this synthetic family.
- **What is being added:** A finite/projective M4 budget table for the
  one-spike canonical-empty family: finite numerator `0`, projective numerator
  at most `1`, and both denominators have `2^-128` budget `6`.
- **How it is useful:** It turns the one-spike rank closure into a complete
  local safe-side upper-bound packet with endpoint and denominator conventions
  printed.
- **What to do next:** Repeat this root-table plus budget-table pattern for a
  less structured non-proportional family or for the first genuine singular
  pivot packet.

### 2026-07-01 - M3 one-spike canonical finite closure

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_one_spike_canonical_empty.py`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/README.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A proof that the non-proportional one-spike family
  has no finite v10 canonical regular roots for any `385 <= A <= 426`, even
  though a selected prefix minor can have a root.
- **How it is useful:** It converts the one-spike packet from selected-minor
  evidence into a canonical-gcd lesson: selected minors can overcount, while
  the full overdetermined Hankel rank stays maximal at every finite slope.
- **What to do next:** Use canonical-gcd/rank-drop closure rather than
  selected-minor roots when building the next M3 root-table or M4 subtraction
  packet.

### 2026-07-01 - M3 one-spike endpoint root table

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for this synthetic finite replay.
- **What is being added:** A non-proportional `F_17^32` one-spike syndrome
  pencil at `A=426`.  The prefix regular determinant is affine in the slope,
  and the packet records the exact split-linear root table with one encoded
  root.
- **How it is useful:** This is the first concrete non-proportional selected
  finite root table in the M3 regular-window branch of PR 171.  It exercises
  the root-table machinery beyond the zero-`u`/proportional packets.
- **What to do next:** Extend from selected synthetic prefix packets toward
  broader root-table families, quotient/extension subtraction, or singular
  pivot packets as directed by `towards-prize.md`.

### 2026-07-01 - M5 regular-root rank-drop bridge

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m5_regular_root_rank_drop.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED bridge theorem.
- **What is being added:** A proof that finite roots of the v10 canonical
  regular gcd are exactly finite rank-drop slopes in nonsingular regular
  buckets.  Hence a root table is a rank-drop table before the M5 kernel filter
  is applied.
- **How it is useful:** It connects M3 root-table packets to M5
  noncontainment accounting.  In particular, full-direction-rank regular roots
  automatically survive the finite-affine kernel filter and require actual root
  counts plus quotient, extension, subfield, or split-locator audits.
- **What to do next:** Produce the first non-proportional finite root-table
  packet that includes rank-drop and kernel-filter fields.

### 2026-07-01 - M5 finite-affine rank stratification

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED corollary of the finite-affine kernel chart.
- **What is being added:** A rank-stratification consequence:
  `rank H(v) > rank(H(u)+zH(v))` forces the finite root `z` to survive the
  ambient noncontainment filter.  Containment can only occur when
  `rank H(v) <= rank(H(u)+zH(v))`, where the stacked-rank equality test
  decides the case.
- **How it is useful:** This rules out same-support kernel subtraction as a way
  to shrink full-direction-rank regular root tables; those roots need actual
  root computation and then quotient, extension, subfield, or split-locator
  audits.
- **What to do next:** Use this rank stratification when choosing the first
  non-proportional root-table packet: low-rank directions may benefit from the
  kernel filter, while full-rank directions will not.

### 2026-07-01 - M5 finite-affine kernel chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m5_finite_affine_kernel_chart.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED for the ambient finite-affine noncontainment chart; AUDIT
  update for the M4 synthesis table.
- **What is being added:** A per-root finite-affine filter: for
  `M_z=H(u)+zH(v)`, the chart `M_z ell=0, H(v)ell!=0` is empty iff
  `ker M_z subset ker H(v)`, equivalently
  `rank stack(M_z,H(v)) = rank M_z`.  If containment fails, the fixed root
  contributes at most one finite parameter.
- **How it is useful:** Future regular root tables can subtract contained
  roots before charging them to the aperiodic support-wise numerator.  This is
  the finite-affine companion to the projective-infinity kernel chart.
- **What to do next:** Compute or certify actual finite root tables for
  non-proportional regular buckets, then apply the kernel filter and quotient
  or extension overlap audits.

### 2026-07-01 - M5 projective-infinity kernel chart

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m5_projective_infinity_kernel_chart.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/`;
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED for the ambient linear projective-infinity chart; AUDIT
  update for the M4 synthesis table.
- **What is being added:** A kernel-containment criterion for the M5
  projective-infinity chart: `H(v) ell=0, H(u) ell!=0` is empty iff
  `ker H(v) subset ker H(u)`, equivalently
  `rank stack(H(v),H(u)) = rank H(v)`.  If containment fails, the projective
  contribution is bounded by the single endpoint `[0:1]`.
- **How it is useful:** This removes the rank-deficient infinity endpoint from
  the undifferentiated residual list.  Proportional rank-deficient pencils now
  have empty infinity chart, and arbitrary deficient directions have an exact
  empty-or-one-point M5 end state.
- **What to do next:** Attack the remaining finite affine residuals: rank-
  deficient finite buckets, high-direction-rank non-proportional root tables,
  and quotient/extension/subfield overlap.

### 2026-07-01 - M3/M4 regular-bucket synthesis

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py`;
  `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT synthesis for the current M3/M4 regular-bucket packet,
  composing proved local certificates.
- **What is being added:** A composed decision table for regular buckets:
  zero-`v` full-rank and proportional full-rank branches are closed; low
  direction-rank non-proportional nonsingular buckets are finite-root safe but
  still need projective-infinity/other ledgers; rank-deficient and high-rank
  non-proportional buckets remain named residuals.
- **How it is useful:** This turns the individual local lemmas in PR #171 into
  the M4-style audit surface requested by `agents.md`: it separates closed,
  finite-safe, and still-open branches without hiding singular buckets.
- **What to do next:** Use the table to choose concrete non-proportional root
  packets or M5 projective/affine pivot charts, rather than adding more
  isolated accounting lemmas.

### 2026-07-01 - M3 direction-rank degree cap

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_direction_rank_degree_cap.py`;
  `experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for finite affine regular minors in the
  `F_17^32` M3 window.
- **What is being added:** A rank-theoretic finite-root cap: if
  `r=rank H_{t,j}(v)`, then every maximal regular minor
  `det(H_R(u)+Z H_R(v))` has degree at most `r`, so the v10 canonical gcd of
  nonzero minors also has degree at most `r`.  Direction rank `r<=6` is
  finite-budget safe for this row.
- **How it is useful:** This gives arbitrary low-direction-rank pencils a
  finite affine root bound independent of the synthetic support model and
  explains why low-rank directions are worth isolating before building pivot
  charts.
- **What to do next:** Pair this finite cap with projective-infinity,
  tangent-overlap, quotient, and extension ledgers for concrete low-rank
  non-proportional packets.

### 2026-07-01 - M3 zero-v projective endpoint

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_zero_v_projective_endpoint.py`;
  `experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the zero-direction-syndrome branch in the
  `F_17^32` M3 regular window.
- **What is being added:** If `v=0`, then
  `M_A(Z)=H_{t,j}(u)` and `M_A[Z0:Z1]=Z0 H_{t,j}(u)`.  Full rank of
  `H_{t,j}(u)` gives no finite affine roots; rank deficiency is a finite
  singular bucket.  In both cases the projective endpoint `[0:1]` has zero
  direction syndrome and is paid by the tangent/common-code-line ledger.
- **How it is useful:** This closes the projective endpoint accounting for
  codeword directions and keeps the remaining zero-`v` difficulty localized to
  finite rank-deficient singular buckets.
- **What to do next:** Combine zero-`u`, zero-`v`, proportional, tangent
  overlap, and infinity criteria into complete M4 tables for concrete
  non-proportional root packets.

### 2026-07-01 - M3 projective-infinity rank criterion

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_projective_infinity_rank_criterion.py`;
  `experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for projective infinity in the `F_17^32`
  M3 regular window.
- **What is being added:** A projective endpoint criterion: after
  homogenizing the regular pencil as
  `Z0 H_{t,j}(u)+Z1 H_{t,j}(v)`, every maximal minor satisfies
  `Delta_R(0,1)=det(H_R(v))`.  Thus full column rank of `H_{t,j}(v)`
  excludes `[0:1]`; rank deficiency is exactly the singular infinity chart.
- **How it is useful:** This gives M4 projective accounting a clean endpoint
  rule: full-rank direction pencils contribute no projective-infinity point,
  while direction-rank-deficient endpoints must be handled by pivot charts or
  a separate paid classification.
- **What to do next:** Combine finite root tables with this infinity criterion
  and the tangent-overlap criterion to build complete projective residual
  tables for non-proportional packets.

### 2026-07-01 - M3 finite tangent-overlap criterion

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_finite_tangent_overlap_criterion.py`;
  `experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for finite tangent overlap in the `F_17^32`
  M3 regular window.
- **What is being added:** A no-double-counting criterion: because `t+j=256`
  for every `385 <= A <= 426`, the regular Hankel chart sees the full stored
  syndrome.  Thus a finite slope is tangent/common-code-line iff
  `u+zv=0`; for `v!=0` this is exactly the proportional case `u=c v` with
  unique slope `z=-c`, while non-proportional pencils have zero finite tangent
  overlap.
- **How it is useful:** Future non-proportional M3 root-table packets can cite
  this certificate to subtract no finite roots as tangent/common-code-line,
  leaving quotient, extension, and singular-pivot ledgers as the remaining
  overlap checks.
- **What to do next:** Build or audit non-proportional regular root tables and
  apply this criterion as the tangent-overlap exclusion.

### 2026-07-01 - M3 proportional-pencil tangent lemma

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py`;
  `experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for proportional regular Hankel pencils in the
  `F_17^32` M3 window.
- **What is being added:** A finite common-code-line translation lemma: if the
  full stored syndrome vectors satisfy `u=c v`, then every maximal regular
  minor has
  `Delta_R(Z)=(Z+c)^(j+1) det(H_R(v))`.  Full column rank gives canonical gcd
  `(Z+c)^(j+1)` and the only root `Z=-c`, paid by the
  tangent/common-code-line ledger; rank deficiency is the singular boundary.
- **How it is useful:** This turns the zero-`u` dichotomy into a reusable M4
  paid-root subtraction rule for any finite common-code-line slope in the
  regular M3 window, and makes the existing proportional-branch reference in
  the regular-window plan replayable.
- **What to do next:** Attack genuinely non-proportional pencils or the
  rank-deficient singular buckets that are not covered by a separate paid
  classification.

### 2026-07-01 - M3 zero-u regular-rank dichotomy

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_zero_u_rank_dichotomy.py`;
  `experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for arbitrary zero-`u` regular buckets.
- **What is being added:** A dichotomy theorem for `385 <= A <= 426`: if
  `u=0`, every maximal regular minor is
  `Delta_R(Z)=Z^(j+1) det(H_R(v))`.  Full column rank of `H_{t,j}(v)` closes
  the regular bucket with canonical gcd `Z^(j+1)` and paid root `Z=0`; rank
  deficiency is exactly the singular boundary.
- **How it is useful:** This consolidates the special zero-`u` rank-witness,
  weighted, and lower-rank certificates into one v10 regular-bucket principle
  and cleanly identifies what still needs M5 pivot work.
- **What to do next:** Attack nonzero-`u` pencils or rank-deficient zero-`u`
  buckets not covered by a separate contained/quotient/extension
  classification.

### 2026-07-01 - M3 lower-rank contained branch

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_lower_rank_contained.py`;
  `experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for lower-rank zero-`u` weighted power-sum
  branches.
- **What is being added:** A singular-bucket classification: if the weighted
  support rank is `r <= j`, every `(j+1)x(j+1)` regular minor vanishes, but
  any agreement-at-least-`A` explaining codeword has at least
  `A-r >= A-j >= 258 > k` zeros outside the rank support and is forced to be
  zero.  The branch is therefore contained/common-code-line, with zero
  support-wise noncontained aperiodic slopes.
- **How it is useful:** This names the first singular boundary adjacent to the
  weight-uniform rank-size formula and removes it from the aperiodic residual
  ledger instead of leaving it as unexplained regular-minor failure.
- **What to do next:** Move to higher-rank or genuinely non-proportional M3
  syndrome pencils, where regular minors need not be monomial and singular
  buckets may require pivot charts.

### 2026-07-01 - M3 weight-uniform canonical gcd formula

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_weight_uniform_canonical_gcd.py`;
  `experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for zero-`u` weighted power-sum syndromes from
  every distinct support subset of size `j+1`, with all weights nonzero.
- **What is being added:** A formula certificate showing that
  `(v_{r_a+b})` factors as `(x_i^{r_a}) diag(w_i) (x_i^b)`, so every maximal
  minor is `Z^(j+1)` times two alternants and `prod_i w_i`.  The prefix row
  set is nonzero by Vandermonde and nonzero weights, so the v10 canonical gcd
  is `Z^(j+1)`.
- **How it is useful:** This removes the unit-weight restriction from the M3
  support-uniform synthetic branch and classifies the full simple rank-size
  zero-`u` weighted power-sum family.
- **What to do next:** Move from simple rank-size weighted power sums to
  lower-rank paid ledgers, higher-rank nonsynthetic pencils, or the first
  non-proportional singular bucket.

### 2026-07-01 - M3 support-uniform canonical gcd formula

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_support_uniform_canonical_gcd.py`;
  `experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for zero-`u` power-sum syndromes from every
  distinct support subset of size `j+1`.
- **What is being added:** A formula certificate showing that, for any support
  `S={x_0,...,x_j}` and any maximal row set `R={r_0<...<r_j}`,
  `Delta_{A,S,R}(Z)` factors as `Z^(j+1)` times two alternants.  The prefix
  row set is nonzero by Vandermonde, so the v10 canonical gcd is `Z^(j+1)`
  uniformly over all such support choices.
- **How it is useful:** This removes the nested-prefix support restriction
  inside the synthetic M3 zero-`u` branch and turns the previous canonical-gcd
  formula into a support-uniform statement over the pinned row.
- **What to do next:** Classify supports of other ranks or move to arbitrary
  non-proportional M3 syndrome pencils after tangent, quotient, and extension
  subtraction.

### 2026-07-01 - M3 canonical all-row-set gcd formula

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_canonical_gcd_formula.py`;
  `experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic M3 zero-`u` nested-prefix
  family.
- **What is being added:** A formula certificate for the v10 canonical gcd
  over all nonzero maximal row-set minors across `385 <= A <= 426`.  For any
  maximal row set, the determinant factors as `Z^(j+1)` times two alternants,
  and the prefix row set is nonzero by Vandermonde, so the canonical monic gcd
  at agreement `A` is `Z^(j+1)` with root table `{0}`.
- **How it is useful:** This removes the contiguous-subatlas limitation for
  the synthetic family and exercises the actual v10 regular-gcd object across
  all formal row-set charts in the M3 window.
- **What to do next:** Move from this synthetic zero-`u` family to arbitrary
  M3 row data, or classify the first regular-rank-drop singular bucket that
  survives tangent, quotient, and extension subtraction.

### 2026-07-01 - M3 all-contiguous gcd formula window

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_all_contiguous_gcd_formula.py`;
  `experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic M3 contiguous subatlas.
- **What is being added:** A compact formula certificate for the zero-`u`
  nested-prefix family across the full M3 regular window `385 <= A <= 426`.
  It covers all `1806` contiguous maximal row sets and proves that the monic
  common gcd at agreement `A` is `Z^(j+1)` with root table `{0}`.
- **How it is useful:** This strengthens the M3 regular-window audit from an
  endpoint-only contiguous formula to a full-window synthetic subatlas, while
  keeping the nonclaim clear that arbitrary row data and the canonical
  all-row-set gcd/lcm ledger remain open.
- **What to do next:** Move from synthetic contiguous subatlases toward actual
  root tables for arbitrary M3 row data, or identify the first singular bucket
  that requires affine/projective pivot charts.

### 2026-07-01 - A=426 all-contiguous gcd formula

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_a426_contiguous_gcd_formula.py`;
  `experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic A=426 contiguous subatlas.
- **What is being added:** A formula certificate extending the A=426
  four-window gcd packet to all `84` contiguous maximal row sets.  For
  `R_s={s,...,s+86}`, the leading determinant factors as
  `(prod_X x)^s * Vandermonde(X)^2`, so every contiguous determinant is
  nonzero and the monic common gcd is `Z^87` with root table `{0}`.
- **How it is useful:** This is a stronger mathematical step toward the v10
  common-gcd branch than the bounded replay alone, while remaining compact and
  explicitly scoped to the contiguous subatlas.
- **What to do next:** Extend from contiguous subatlases toward canonical
  all-row-set gcd/lcm ledgers, or identify the first singular buckets that
  force pivot charts.

### 2026-07-01 - A=426 contiguous-gcd M3 packet

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_contiguous_gcd4_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-a426/`;
  `experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py`;
  `experimental/scripts/verify_f17_32_m3_syndrome_realizability.py`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic bounded common-gcd replay.
- **What is being added:** The packet checker now validates inline
  `regular_minor_gcd` data.  A compact A=426 packet checks the first four
  contiguous maximal row sets for the zero-`u` synthetic pencil and records
  common gcd `Z^87`, exact root table `{0}`.
- **How it is useful:** This moves the M3 synthetic stress packet from a
  selected prefix-minor replay toward the v10 regular common-gcd branch,
  while preserving the bounded-subatlas nonclaim.
- **What to do next:** Replace bounded synthetic contiguous scans by canonical
  row-data gcd/lcm ledgers or classify the singular buckets that obstruct that
  computation.

### 2026-07-01 - M3 syndrome-realizability sidecar

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_syndrome_realizability.py`;
  `experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the listed synthetic syndrome inputs.
- **What is being added:** A subgroup-section certificate showing that the
  A=385, A=426, A=421..426, and A=426 contiguous-gcd synthetic M3
  rank-witness syndrome pencils are realized by received-line values on the
  pinned order-512 subgroup row.  The verifier audits the generator orbit and
  character orthogonality for exponents `-255..255`.
- **How it is useful:** This removes the possible ambiguity that the
  rank-witness packets are only formal syndrome vectors.  The remaining M3
  gap is universal classification of arbitrary length-256 syndrome pencils,
  not realization of these packet inputs as row data.
- **What to do next:** Use the same section lemma when building non-synthetic
  M3 packets, then combine their root tables with tangent, quotient, and
  extension ledgers.

### 2026-07-01 - M3 zero-slope subtraction sidecar

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py`;
  `experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic rank-witness packets.
- **What is being added:** A deterministic M4 sidecar for the M3 endpoint and
  top-window rank-witness packets.  It verifies that every source input has
  zero `u` syndrome, so the unique raw root `Z=0` is a
  tangent/common-code-line slope and leaves residual synthetic aperiodic
  numerator `0`.
- **How it is useful:** This adds the paid-root subtraction step requested by
  the M3/M4 roadmap for the selected synthetic root-table packets, while
  keeping the nonclaim clear that arbitrary M3 pencils remain unclassified.
- **What to do next:** Move from synthetic zero-slope packets to adversarial or
  universally quantified M3 syndrome pencils, and combine any resulting roots
  with quotient, tangent, and extension ledgers.

### 2026-07-01 - M3 rank-witness endpoint and top-window packets

- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Files added or changed:**
  `experimental/data/hankel-regular-minor-inputs/`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/`;
  `experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** Selected M3 regular-window packets for the pinned
  `F_17^32`, `n=512`, `k=256` row: endpoint replays at `A=385` and `A=426`,
  plus a fixed-prefix top-window replay for `421 <= A <= 426`.  The extractor
  checks the declared prefix row sets and records exact finite root tables
  `Delta_A(Z)=c_A Z^(j+1)`, with root union `{0}`.
- **How it is useful:** This addresses the immediate M3 instruction in
  `towards-prize.md` to begin replacing degree-only regular-minor evidence by
  actual selected-agreement root tables.  The top-window packet also tests one
  multi-agreement root-union packet shape.  These are checker replays and
  stress packets, not worst-case row bounds or safe-side closures.
- **What to do next:** Extend from this synthetic selected-agreement packet to
  row-level/adversarial M3 pencils, combine the roots with tangent/quotient/
  extension subtraction, and classify singular buckets when the regular
  extractor fails.

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
