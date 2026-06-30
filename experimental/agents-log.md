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

### 2026-06-30 - Proportional residual extractor classification

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_scalar5_rank_pivot_tangent_residual_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/`;
  `experimental/notes/m1/m1_hankel_proportional_pencil_tangent_lemma.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for a finite toy packet.
- **What is being added:** The regular-minor extractor now classifies singular
  scalar-multiple buckets using the proportional-window lemma.  The toy packet
  has `u=5v` and rank-one `H(v)`, so rank-at-nodes proves every maximal regular
  minor vanishes, while the residual audit labels the bucket as
  tangent/common-code-line with single slope `12=-5`.
- **How it is useful:** Converts a class of singular buckets from `unknown` to
  a checked tangent residual, which is directly aligned with the v9 M5
  residual-classification program.
- **What to do next:** Apply the same classifier to actual M3 row packets only
  when the full-syndrome/tail condition proves the tangent charge is valid.

### 2026-06-30 - Hankel proportional-window root compression

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py`;
  `experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/`;
  `experimental/notes/m1/m1_hankel_proportional_pencil_tangent_lemma.md`;
  `experimental/data/certificates/hankel-f17-32-m3-proportional-a426/README.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A reusable v9 classification lemma for proportional
  Hankel windows: if `u_m=c v_m` on the visible exact-bucket window `m<t+j`,
  then regular minors have shape `det(H(v)_R)(Z+c)^(j+1)`, affine pivots with
  `B_T != 0` have slope `-c`, and `B_T=0` is contained.  Full-syndrome
  proportionality is recorded as the extra condition needed to charge `Z=-c`
  to the common-code-line ledger.
- **How it is useful:** Turns the previous scalar `F_17^32` packet into a
  general removed-ledger rule for future M3/M4 v9 packets, including singular
  proportional buckets, while avoiding overcharging merely local proportional
  windows to tangent.
- **What to do next:** Apply this only as a tangent residual classification
  inside actual row packets after the full syndrome/tail check; non-proportional
  aperiodic buckets remain the main M3 problem.

### 2026-06-30 - F17^32 proportional Hankel root subtraction

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/emit_f17_32_m3_rank_witness_input.py`;
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/scripts/verify_f17_32_m3_proportional_slope_subtraction.py`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_scalar5_rank_witness_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-proportional-a426/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for a synthetic F17^32 packet.
- **What is being added:** A closed-form proportional-pencil certificate:
  for `u=c v`, the regular determinant has shape
  `Delta_A(Z)=det(H(v)_R)(Z+c)^(j+1)`.  The new `A=426`, `c=5` packet over the
  pinned `F_17^32` row has exact root union `{12}`, and the subtraction
  verifier checks that this root is paid by the tangent/common-code-line ledger
  because the stored syndrome vanishes at `Z=-5`.
- **How it is useful:** Generalizes the zero-slope synthetic packet to
  nonzero common-code-line roots and makes repeated-root closed-form packets
  more audit-ready without enumerating `F_17^32`.
- **What to do next:** Use this only as a removed-ledger check inside actual
  M3 row packets; it is not itself a worst-case MCA bound.

### 2026-06-30 - v9 packet claim-scope guardrail

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `scripts/aperiodic_eliminant_schema.json`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A structured optional `claim_scope` field for v9
  Hankel packets, with checker logic rejecting packets that mark synthetic,
  toy, degree-only, or unenumerated evidence as threshold-pinning material.
  The regular-minor toy packet now declares itself as non-pinning
  `toy_mechanism` evidence, and an expected-failure fixture exercises the
  synthetic-as-threshold-bound rejection.
- **How it is useful:** This protects the M3/M4 workflow from treating
  mechanism tests or synthetic row pencils as actual safe-side row bounds.
- **What to do next:** Use `claim_scope` on future actual-row packets and set
  `may_be_used_for_threshold_pinning=true` only when the packet has
  theorem-backed row data and enumerated or closed-form root accounting.

### 2026-06-30 - Singular pivot toy packet

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_singular_pivot_toy_packet.py`;
  `experimental/data/certificates/singular-pivot-toy/`;
  `experimental/notes/m1/singular_pivot_toy_packet.md`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for a finite toy packet.
- **What is being added:** A nonzero `F_17` pivot-atlas packet where the
  regular Hankel bucket is genuinely singular but affine pivots close the
  finite-slope contribution.  The verifier proves
  `H(u)+Z H(v)=(Z+5)H(v)`, `rank H(v)=2`, enumerates all 45 split co-supports,
  and obtains exact root union `{12}`.  The v9 checker now also rejects
  eliminant pivot records that omit `eliminant_ref` or degree metadata,
  recomputes pivot eliminant root tables when coefficient data are present,
  and compares the packet root-union table against those pivot roots.
- **How it is useful:** This is the first checked `pivot_atlas` shape in the
  branch, exercising the v9 singular-bucket workflow without calling an
  unresolved singular bucket aperiodic evidence.
- **What to do next:** Apply the same pivot packet discipline to an actual
  lower-agreement row only after a genuine singular bucket appears there.

### 2026-06-30 - F17^32 high-agreement tangent table

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_high_agreement_tangent_table.py`;
  `experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/`;
  `experimental/notes/thresholds/f17_32_high_agreement_tangent_table.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A checked item-5 ledger table for every
  high-agreement exact row `A=427..512` of `RS[F_17^32,H,256]`.  It rewrites
  the proved tangent staircase as columns `B_tan`, `B_quot_support`,
  `B_quot_image`, `B_ap_regular`, `B_ap_pivot`, `B_ext`, and the deduped total.
- **How it is useful:** This gives the F17^32 row a complete theorem-backed
  subtraction table in the high-agreement range and a template for the
  lower-agreement M4 table, where actual v9 root counts and singular-pivot
  packets are still missing.
- **What to do next:** Build the same ledger columns for `A<427` only when
  actual regular-minor root counts, quotient/tangent deduplication, or
  singular-pivot certificates are available.

### 2026-06-30 - F17^32 M3 extension-denominator audit

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_extension_denominator_audit.py`;
  `experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/`;
  `experimental/notes/f1/f17_32_m3_extension_denominator_audit.md`;
  `experimental/scripts/verify_f17_32_m3_regular_window_status.py`;
  `experimental/data/certificates/hankel-f17-32-m3-regular-window-status/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A checked denominator audit for the fixed synthetic
  top-window line-value lift.  It verifies that `f` is the zero base-field
  vector while all 512 values of `g` are outside `F_17`, so finite affine
  slopes are sampled over `F_17^32` and the denominator is `17^32`.
- **How it is useful:** This addresses the F1 accounting hazard for the first
  extension-valued v9 packet in this branch and prevents comparing its
  numerator to a base-field slope denominator.
- **What to do next:** Apply the same denominator audit to actual-row and
  Prime192 v9 packets before combining tangent, quotient, and aperiodic
  ledgers.

### 2026-06-30 - F17^32 M3 zero-slope subtraction

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py`;
  `experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/`;
  `experimental/notes/m1/f17_32_m3_zero_slope_subtraction.md`;
  `experimental/scripts/verify_f17_32_m3_regular_window_status.py`;
  `experimental/data/certificates/hankel-f17-32-m3-regular-window-status/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A checked M4-style sidecar for the fixed synthetic
  top-window packet.  It verifies that the packet's sole regular-minor root
  `{0}` is the zero-codeword tangent slope because the line-value lift has
  `f=0`, so the residual synthetic aperiodic numerator is `0` after that paid
  branch is removed.
- **How it is useful:** This exercises the no-double-counting convention
  between v9 regular roots and removed tangent ledgers before actual M3 row
  data or Prime192 packets are available.
- **What to do next:** Repeat the same subtraction discipline for actual
  `F_17^32` row pencils, add quotient-image roots, and only then claim a full
  M4 row table.

### 2026-06-30 - Subgroup syndrome section

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_subgroup_syndrome_section.py`;
  `experimental/data/certificates/subgroup-syndrome-section/`;
  `experimental/notes/m1/subgroup_syndrome_section.md`;
  `experimental/scripts/verify_f17_32_m3_regular_window_status.py`;
  `experimental/data/certificates/hankel-f17-32-m3-regular-window-status/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A reusable proof that for a multiplicative subgroup
  `H` of order `n`, the weighted RS syndrome map has the explicit section
  `y_s(x)=sum_m s_m x^(-m-1)`, because `lambda_x=x/n` and subgroup power sums
  are orthogonal.
- **How it is useful:** This turns the line-values-to-syndrome adapter used by
  the M3 top-window packet into a general subgroup-row theorem rather than a
  one-off construction.
- **What to do next:** Use this section theorem to feed actual tangent/quotient
  deduped subgroup-row line data into v9 packets.

### 2026-06-30 - F17^32 M3 line-value lift

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_line_value_lift.py`;
  `experimental/data/certificates/hankel-f17-32-m3-line-value-lift/`;
  `experimental/scripts/verify_f17_32_m3_regular_window_status.py`;
  `experimental/data/certificates/hankel-f17-32-m3-regular-window-status/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic line-value lift.
- **What is being added:** An explicit `f,g:H -> F_17^32` line-value lift of
  the fixed top-window syndrome packet.  The verifier uses
  `lambda_x=x/512` and the inverse Fourier section
  `y(x)=sum_m s_m x^(-m-1)` to replay the exact fixed top-window syndromes.
- **How it is useful:** This closes the adapter gap between Paper D's
  line-value formulation and the regular-minor extractor's syndrome input for
  the current `A=421..426` packet.
- **What to do next:** Use the same adapter boundary for tangent/quotient
  deduped row data, then replace the remaining `actual_row_outcome = not
  supplied` entries by root tables or singular-bucket declarations.

### 2026-06-30 - F17^32 M3 regular-window status ledger

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_regular_window_status.py`;
  `experimental/data/certificates/hankel-f17-32-m3-regular-window-status/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A compact ledger that hashes the M3 regular-window
  plan, generic all-row-set certificate, synthetic rank-witness family, and
  fixed top-window v9 packet.  It records, for every `A=385..426`, which
  generic/synthetic facts are proved and that actual-row root/singularity
  outcomes are still not supplied.
- **How it is useful:** This makes the M3 frontier reviewable without
  overclaiming that synthetic packets prove a worst-case MCA bound.
- **What to do next:** Supply actual `F_17^32` syndrome vectors and replace
  the `actual_row_outcome = not supplied` entries by root tables or singular
  bucket declarations.

### 2026-06-30 - F17^32 M3 fixed top-window packet

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/scripts/emit_f17_32_m3_rank_witness_input.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a421_426_fixed_prefix92_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** A fixed-syndrome v9 packet for `A=421..426` using
  one `u=0` moment syndrome from the first `92` pinned domain elements.  The
  extractor verifies nonzero prefix leading coefficients for minor sizes
  `87..92`, so the packet has exact synthetic root union `{0}` and declared
  numerator `1`.
- **How it is useful:** This is the first single-pencil multi-agreement M3
  stress packet over `F_17^32`, closer to the eventual regular-window packet
  shape than separate endpoint probes.
- **What to do next:** Replace this synthetic pencil by actual M3 row data and
  combine root counts with tangent and quotient subtraction.

### 2026-06-30 - F17^32 M3 endpoint closed-form v9 packets

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/scripts/emit_f17_32_m3_rank_witness_input.py`;
  `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** The endpoint `F_17^32` M3 packets now use a
  `zero_u_monomial_roots` extractor mode.  Because `u=0`, the selected prefix
  determinant is `c_A Z^(j+1)` with computed nonzero `c_A`, so the v9 packets
  record exact synthetic root union `{0}` and declared numerator `1`.
- **How it is useful:** This promotes the compressed-root idea from the
  sidecar family certificate into ordinary v9 packets and gives the checker a
  large-field monomial completeness gate.
- **What to do next:** Replace the synthetic syndrome pencils by actual M3 row
  data and combine their root counts with tangent and quotient subtraction.

### 2026-06-30 - F17^32 M3 synthetic closed-form roots

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank_witness_family.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** The all-window synthetic M3 family certificate now
  records the closed-form determinant `Delta_A(Z)=c_A Z^(j+1)` with
  `c_A != 0`, so every agreement in `385..426` has exact synthetic root table
  `{0}`.
- **How it is useful:** This demonstrates a compressed root-table certificate
  over the pinned `F_17^32` model and sharpens the synthetic stress family from
  degree-only bounds to exact roots.
- **What to do next:** Apply the same root-certificate discipline to actual M3
  row-data pencils, then combine the resulting aperiodic counts with the
  tangent and quotient ledgers.

### 2026-06-30 - Small-field root-table completeness audit

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The v9 packet checker now enumerates prime fields
  and small polynomial-basis extension fields to verify that inline root tables
  are complete, not just sound.  A corrupted `F_17^2` packet that omits the
  root `272` from the determinant `Z^2-3` is rejected.
- **How it is useful:** This prevents small-field proof packets from lowering
  a declared aperiodic numerator by silently omitting roots, and gives a model
  for future compressed root-table certificates over large fields.
- **What to do next:** Large fields such as `F_17^32` still need explicit
  compression or independent root-count certificates; the checker intentionally
  does not brute-force those fields.

### 2026-06-30 - Rank-witness packet hash audit

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/regular-minor-extractor-rank-witness-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The v9 packet checker now verifies
  `rank_witness_bound` packets by recomputing the deterministic hash of
  `roots=not_enumerated`, the degree bound, row set, and rank-pivot node.
  A deliberately corrupted toy packet checks that stale witness hashes are
  rejected.
- **How it is useful:** This makes the cheap M3 rank-witness certificates
  replay-checkable instead of relying only on conventionally formatted JSON.
- **What to do next:** Use the same checker path on any actual `F_17^32`
  rank-witness or pivot-chart packets before comparing them with the Paper D
  ledgers.

### 2026-06-30 - F17^32 M3 rank-witness family certificate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_rank_witness_family.py`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** A compact all-window certificate showing that, for
  every `385<=A<=426`, the synthetic moment syndrome over the pinned
  `F_17^32` domain has a full-rank prefix regular minor at slope `1`.  It
  records all 42 degree bounds, degree sum `4515`, and endpoint v9 packet
  hashes for `A=385` and `A=426`.
- **How it is useful:** This avoids adding 42 bulky generated packets while
  still proving that the rank-witness construction covers every M3 minor size
  over the actual degree-32 field model.
- **What to do next:** Replace synthetic family witnesses by actual M3 line
  data or by root/pivot certificates strong enough to compare with the
  finite-slope budget.

### 2026-06-30 - F17^32 M3 rank-witness packet at A=385

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a385_rank_witness_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** A concrete `F_17^32` M3 endpoint packet at `A=385`,
  where the regular minor size is `128`, the largest in the `385<=A<=426`
  window.  The synthetic moment syndrome gives a full-rank prefix
  specialization at slope `1` and emits the rank-witness degree bound `128`.
- **How it is useful:** Together with the `A=426` packet, this stress-tests the
  v9 regular-minor pipeline at both endpoint minor sizes over the pinned
  `F_17^32` field/domain model.
- **What to do next:** Move from synthetic endpoint witnesses to actual M3 line
  data, then replace endpoint degree-only bounds by root tables or pivot-chart
  certificates.

### 2026-06-30 - F17^32 M3 rank-witness packet at A=426

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/scripts/emit_f17_32_m3_rank_witness_input.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_rank_witness_input.json`;
  `experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/`;
  `experimental/notes/m1/f17_32_m3_rank_witness_packet.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the synthetic finite replay.
- **What is being added:** A concrete `F_17^32` M3 regular-window packet at
  `A=426`, plus compact encoded-integer syndrome input support for
  polynomial-basis extractor inputs.  The synthetic syndrome pencil has `u=0`
  and moment sequence `v_m=sum_i x_i^m` for the first `j+1=87`
  descriptor-domain elements; the extractor finds a full-rank specialization at
  slope `1` and emits the rank-witness degree bound `87`.
- **How it is useful:** This is the first non-toy `F_17^32` stress packet for
  the v9 regular-minor pipeline, using the pinned field model and domain hash
  rather than a small prime-field replay.
- **What to do next:** Extend from synthetic witnesses to actual M3 line data,
  then replace degree-only bounds by root tables, compressed root certificates,
  or pivot-chart classifications where needed.

### 2026-06-30 - Regular-minor rank-witness bound mode

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_witness_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-rank-witness-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED for the finite replay.
- **What is being added:** The extractor now has an optional
  `rank_witness_bound` mode for `rank_at_nodes`: a full-rank specialization
  certifies a nonzero regular minor and emits the `j+1` root-count bound without
  determinant interpolation.
- **How it is useful:** This gives the M3 regular-window audit a cheap first
  pass for large `F_17^32` pencils, separating nonsingularity detection from
  the more expensive root-table computation.
- **What to do next:** Use the mode on concrete `F_17^32` row data, then refine
  any bound that is too weak by interpolation, root tables, or pivot charts.

### 2026-06-30 - External root-union numerator check

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/hankel-smoke-f17-506-507/`;
  `experimental/notes/m1/aperiodic_hankel_regular_minor_toy_certificate.md`;
  `experimental/notes/thresholds/hankel_smoke_f17_506_507.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The v9 checker now compares
  `declared_aperiodic_numerator` against externally referenced root-union
  tables when the reference resolves to a table or declared numerator.  A
  negative smoke-packet fixture verifies that mismatched external numerators
  fail.
- **How it is useful:** This closes the same numerator consistency check for
  non-inline M3/M4 packets that already existed for inline root tables.
- **What to do next:** Keep external root tables small and pointer-addressable
  in future regular-window and subtraction packets.

### 2026-06-30 - v9 packet reference checker

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/hankel-smoke-f17-506-507/`;
  `experimental/notes/m1/aperiodic_hankel_regular_minor_toy_certificate.md`;
  `experimental/notes/thresholds/hankel_smoke_f17_506_507.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The v9 packet checker now resolves local packet
  references, including JSON-pointer fragments such as removed-ledger
  certificate references.  A negative smoke-packet fixture confirms that a
  missing removed-ledger certificate is rejected.
- **How it is useful:** This completes another part of the roadmap's schema
  checker requirement before M3/M4 packets start subtracting tangent and
  quotient ledgers.
- **What to do next:** Use the same reference checker for concrete M3
  regular-window packets and for the later quotient/tangent subtraction table.

### 2026-06-30 - Rank-pivot audit checker hardening

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** The v9 packet checker now validates the
  `rank_at_nodes` proof audit: the required node count is `j+2`, successful
  regular-minor packets must name the pivot node, and singular declarations
  must have tested every required node.  An intentionally invalid packet shows
  that underchecked singular declarations fail.
- **How it is useful:** This tightens the M3 regular-minor extractor pipeline
  before genuine `F_17^32` regular-window packets are emitted.
- **What to do next:** Use the hardened checker while producing concrete M3
  row-data packets and pass any genuine singular bucket to the pivot-chart
  program.

### 2026-06-30 - Regular-minor rank-pivot selector

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_toy.json`;
  `experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_pivot_toy.json`;
  `experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/`;
  `experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/`;
  `experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT for the finite replay.
- **What is being added:** The regular-minor extractor now has a
  `rank_at_nodes` row-set strategy.  It evaluates the pencil at `j+2`
  deterministic finite slopes to find a full-rank maximal row set whenever one
  exists; if none appears, the degree bound proves all maximal minors vanish
  identically.
- **How it is useful:** Future M3 packets no longer have to rely on prefix or
  contiguous row sets before declaring a singular regular bucket.
- **What to do next:** Use `rank_at_nodes` on concrete `F_17^32` syndrome
  pencils, then pass genuine singular outcomes to the pivot-chart program.

### 2026-06-30 - F17^32 M3 generic regular minor

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/verify_f17_32_m3_generic_regular_minor.py`;
  `experimental/data/certificates/hankel-f17-32-generic-regular-minor/`;
  `experimental/notes/m1/f17_32_m3_generic_regular_minor.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A generic initial-monomial proof certificate showing
  that every maximal row-set minor in the M3 window is generically nonzero,
  with exact degree `j+1`, for every `385<=A<=426`.  The certificate covers
  `155193154203428426778689566118132250614039201839551` formal row-set charts
  and retains the shifted-Vandermonde audit for the `1806` contiguous charts.
- **How it is useful:** It shows regular row-set failure is a special
  determinant-zero stratum of the actual syndrome pencil, not an unavoidable
  failure of the v9 regular chart.
- **What to do next:** For concrete `F_17^32` syndrome pencils, either compute
  actual determinant/root data for a practical row-set subatlas or classify
  determinant-zero cases by pivot charts.

### 2026-06-30 - F17^32 Hankel row descriptor

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/emit_f17_32_hankel_row_descriptor.py`;
  `experimental/data/certificates/hankel-f17-32-row-descriptor/`;
  `experimental/data/certificates/hankel-regular-window-f17-385-426/`;
  `experimental/notes/m1/f17_32_hankel_row_descriptor.md`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A deterministic descriptor for the
  `RS[F_17^32,H,256]` row used in M3.  It pins the polynomial-basis field
  model, order-512 subgroup generator, encoded domain list, domain hash,
  finite-slope budget, and `385<=A<=426` regular-window arithmetic.
- **How it is useful:** Future regular-window proof packets can now refer to a
  replayable `row.domain_hash` and field model instead of an informal
  `F_17^32,H` row label.
- **What to do next:** Supply syndrome-pencil line data against this row
  descriptor, then run the regular-minor extractor on a selected M3 subrange.

### 2026-06-30 - Extension-root checker hardening

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:** `scripts/check_aperiodic_eliminant_packet.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED for the finite toy replay.
- **What is being added:** The v9 packet checker now evaluates encoded roots
  when a packet supplies an explicit polynomial-basis field model.  A tiny
  `F_17^2` replay has prefix minor determinant `Z^2-3`, whose roots are the
  non-base elements encoded as `17` and `272`, so the checker exercises genuine
  extension-root arithmetic.  The checker also verifies row-field/model
  compatibility and irreducibility of the supplied modulus, with a reducible
  negative packet included.
- **How it is useful:** This hardens the M3 regular-minor packet pipeline for
  `F_17^32`: future extension-field root tables will be arithmetically checked,
  not merely schema-checked and hash-counted, and their field model must define
  a genuine polynomial-basis field.
- **What to do next:** Use the same checker path on selected `F_17^32`
  regular-window packets once syndrome-pencil row data are supplied.

### 2026-06-30 - Extension-field regular-minor adapter replay

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-f17-2-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT / PROVED for the finite toy replay.
- **What is being added:** The regular-minor extractor now has a
  polynomial-basis extension-field path.  The new replay embeds the existing
  `F_17` scalar toy into `F_17^2 = F_17[x]/(x^2-3)`, interpolates regular
  determinant polynomials over the full extension field, enumerates all `289`
  finite slopes, and emits an encoded v9 root table accepted by the packet
  checker.
- **How it is useful:** This removes the extractor's prime-field-only
  limitation on the path to M3.  The remaining missing ingredient for the
  `385<=A<=426` prize-facing window is now row data over `F_17^32`, not the
  finite-field determinant/interpolation adapter.
- **What to do next:** Supply or derive the `F_17^32` syndrome-pencil row data
  and run the extension path on a selected agreement subrange, then compare
  actual roots or singular declarations with tangent and quotient ledgers.

### 2026-06-30 - F17 regular Hankel-window plan

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/plan_f17_regular_hankel_window.py`;
  `experimental/data/certificates/hankel-regular-window-f17-385-426/`;
  `experimental/notes/m1/hankel_regular_window_plan.md`;
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A deterministic audit packet for the M3
  `385<=A<=426` regular non-tangent window of
  `RS[F_17^32,H,256]`.  It records the exact `j`, `t`, prefix maximal minor
  sizes, degree bounds, interpolation cost, and syndrome-index requirements for
  every agreement in the window.
- **How it is useful:** This deepens the regular-minor extractor PR by fixing
  the prize-row target before the extension-field adapter is written.  It also
  records the key budget audit: the regular degree-bound sum is `4515`, while
  the finite-slope `2^-128` budget numerator is only `6`, so actual root tables
  or singular-bucket declarations are necessary.
- **What to do next:** Add the `F_17^32` syndrome/field adapter and run the
  regular extractor on a selected subrange, emitting root tables where minors
  are nonzero and pivot-chart residual labels where they vanish.

### 2026-06-30 - Regular Hankel-minor extractor

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/scripts/extract_regular_hankel_minors.py`;
  `experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json`;
  `experimental/data/certificates/regular-minor-extractor-toy/`;
  `experimental/notes/m1/hankel_regular_minor_extractor.md`;
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT / PROVED for the finite toy replay.
- **What is being added:** A reusable prime-field regular Hankel-minor
  extractor for the Paper D v9 atlas.  Given syndrome-pencil row data and exact
  agreements, it scans candidate maximal Hankel row minors, recovers the
  determinant polynomial by interpolation, emits a v9 packet, and in small
  cases enumerates roots and split co-support bad slopes for containment
  checks.
- **How it is useful:** Addresses the next `towards-prize.md` milestone after
  the checker and smoke packet: turning the regular overdetermined bucket into
  a replayable extraction tool before attacking the `385<=A<=426` window.
- **What to do next:** Add an `F_17^32` row-data/field-arithmetic adapter, then
  run the extractor on selected agreements in the non-tangent regular window
  and compare the resulting root bounds with tangent and quotient ledgers.

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
