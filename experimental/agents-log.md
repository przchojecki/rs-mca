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

### 2026-06-24 - Cycle84 finite-source closure in exact occupancy

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py`,
  `experimental/notes/m1/m1_cycle84_exact_occupancy_chain.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-EXACT-OCCUPANCY-CHAIN / CONDITIONAL.
- **What is being added:** The Cycle84 exact occupancy verifier now imports and
  checks the projected replay algorithm audit in the same chain as the generated
  C++ source contract, saved all-shards receipt, projected-log certificate, and
  kernel-lift filter.
- **How it is useful:** Narrows the Cycle84 finite-source boundary for the M1
  numerator: the exact occupancy chain now explicitly composes algorithm proof,
  generated source identity, full replay receipt, and true-collision lift.
- **What to do next:** Review the finite-source closure audit and official ABF
  source gates; this does not rerun the full all-shards census.

### 2026-06-24 - Cycle116 external transfer replay

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle116_external_transfer_replay.py`,
  `experimental/notes/m1/m1_cycle116_external_transfer_replay_audit.md`,
  `experimental/notes/m1/m1_cycle116_external_packet_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXTERNAL-CYCLE116-TRANSFER-REPLAYED.
- **What is being added:** A wrapper that materializes the hash-pinned PR #96
  Cycle116 packet in a temporary directory, runs its `verify_transfer.py`, and
  compares the returned native/smooth `LD_sw`, field-ledger, density, and
  affine-line receipt to the local Cycle120 chain.
- **How it is useful:** Reduces the external Cycle116 boundary from executable
  provenance to proof-logic review: the external verifier is now replayed from
  recorded Git objects and its theorem ledger is checked against this PR.
- **What to do next:** Review the external verifier proof logic and official
  ABF source gates; this replay does not replace human proof review.

### 2026-06-24 - Cycle116 external packet source hashes

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle116_external_packet_sources.py`,
  `experimental/notes/m1/m1_cycle116_external_packet_source_hash_audit.md`,
  `experimental/notes/m1/m1_cycle116_external_packet_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXTERNAL-CYCLE116-SOURCE-HASHES-VERIFIED.
- **What is being added:** A Git-object source-hash verifier for the four PR #96
  files behind the compact Cycle116 external packet contract. It checks blob
  ids, file modes, byte sizes, SHA256 digests, and exact copies of the two JSON
  inputs embedded in the local contract.
- **How it is useful:** Removes a provenance ambiguity in the M1 Cycle120 finite
  chain: the compact external packet contract is now mechanically tied to the
  recorded PR #96 source objects when that commit is fetched locally.
- **What to do next:** Review the external proof text/verifier content and the
  official ABF source gates; this audit only closes the hash/source-binding
  part of the boundary.

### 2026-06-24 - Cycle120 domain-generated field ledger

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle120_domain_field_ledger.py`,
  `experimental/notes/m1/m1_cycle120_domain_field_ledger.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / DOMAIN-GENERATED-FIELD-LEDGER.
- **What is being added:** A field-ledger verifier showing that `eta` generates
  `F_17^16` and `theta` generates `F_17^32` over `F_17`: `ord_256(17)=16`,
  `ord_512(17)=32`, plus Frobenius noncontainment in every proper subfield.
- **How it is useful:** Closes a ledger ambiguity for the Cycle120 row: the
  smooth-domain generator itself generates the full ambient field, so
  `q_gen=q_code=q_line=17^32` locally.
- **What to do next:** Keep official ABF source verification separate from
  this local finite-field ledger; the remaining promotion gates are unchanged.

### 2026-06-24 - Cycle116 smooth padding transfer audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py`,
  `experimental/notes/m1/m1_cycle116_smooth_padding_transfer_audit.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / SMOOTH-PADDING-TRANSFER.
- **What is being added:** A concrete verifier for the Cycle116 smooth-padding
  lift: `H=D0 disjoint_union theta D0`, the `A`/`R` odd-coset partition,
  nonzero `P_A(beta)` and `P_R(beta)`, and the degree inequalities preserving
  the same bad parameters in the `[512,256]` row.
- **How it is useful:** Makes the native-to-smooth lift executable rather than
  only prose: agreement `143+119=262`, dimension `137+119=256`, co-support
  `113+137=250`, and fixed-jet loss `244=250-6` are checked in one layer.
- **What to do next:** Keep the remaining promotion gates focused on Cycle84
  generated-source review, external Cycle116 contract provenance, and official
  ABF source verification.

### 2026-06-24 - Cycle116 fixed-jet transfer audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle116_fixed_jet_transfer.py`,
  `experimental/notes/m1/m1_cycle116_fixed_jet_transfer_audit.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / FIXED-JET-TRANSFER-ALGEBRA.
- **What is being added:** A verifier and note for the native Cycle116
  fixed-jet transfer algebra: the common complement-locator truncation `W`, the
  formula `z_T=W(beta)-V_D(beta)/P_T(beta)`, nonzero denominator checks, and
  injectivity from distinct `Phi(T)` values to distinct bad line parameters.
- **How it is useful:** Removes an implicit algebra step between the slot-block
  fixed-jet/scalar identities and the native `LD_sw(RS[F0,D0,137],143)>=N`
  conclusion used by the M1 Cycle120 chain.
- **What to do next:** Keep the remaining dependencies focused on the 336
  slot-identity replay, Cycle84 exact occupancy/source review, and official ABF
  source verification.

### 2026-06-24 - Cycle120 support-wise MCA bridge

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py`,
  `experimental/notes/m1/m1_cycle120_supportwise_mca_bridge.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / LD-SW-TO-EPSILON-MCA-BRIDGE.
- **What is being added:** A standalone bridge from the finite
  `LD_sw(C,262)>=N` statement to the ABF-facing normalized lower bound
  `epsilon_mca(C,125/256)>=N/17^32`, with a verifier for the closed threshold,
  denominator, and numerator alignment.
- **How it is useful:** Removes a notation gap in the M1 Cycle120 chain: the
  PR now explicitly checks that the finite bad-line count is the same object
  consumed by support-wise `epsilon_mca`.
- **What to do next:** Keep the remaining promotion gates focused on official
  ABF source verification, the Cycle84 generated-source contract, and external
  Cycle116 contract provenance.

### 2026-06-24 - Cycle116 external packet contract comparison

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle116/external_packet_contract.json`,
  `experimental/scripts/verify_m1_cycle116_external_packet_contract.py`,
  `experimental/notes/m1/m1_cycle116_external_packet_contract.md`,
  `experimental/scripts/verify_m1_cycle116_slot_assembly.py`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXTERNAL-CYCLE116-PACKET-CONTRACT-COMPARED.
- **What is being added:** A compact, hash-pinned contract extracted from the
  closed PR #96 Cycle116 packet, plus a verifier comparing its field model,
  slot data, co-support clause, native fixed-jet bridge, smooth lift, and
  Cycle84 finite values against the local M1 chain.
- **How it is useful:** Removes the prior loose source-comparison boundary
  that the external Cycle116 packet might use a different co-support; the
  remaining issue is provenance review of the compact contract itself.
- **What to do next:** Review that the compact JSON faithfully records the
  hash-pinned PR #96 files, then keep official ABF source verification and the
  Cycle84 generated-source review as the remaining promotion gates.

### 2026-06-24 - Cycle84 generated replay source contract

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle84_generated_replay_source_contract.md`,
  `experimental/scripts/verify_m1_cycle84_generated_replay_source.py`,
  `experimental/scripts/verify_m1_cycle84_projected_replay_algorithm.py`,
  `experimental/scripts/verify_m1_cycle84_projected_full_replay_receipt.py`,
  `experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/data/witnesses/m1-cycle84/README.md`, M1 Cycle84/Cycle116/Cycle120
  notes, and `experimental/agents-log.md`.
- **Status:** AUDIT / GENERATED-CYCLE84-CXX-SOURCE-CONTRACT.
- **What is being added:** A verifier for the generated Cycle84 C++ replay
  source at `--threads 16`, checking the source SHA256, injected log/color
  tables, tau guards, five-two split, shard intervals, canonical-key map,
  duplicate-energy accounting, OpenMP shard loop, and JSON output landmarks.
- **How it is useful:** Replaces an opaque generated-source review boundary
  with a reproducible source contract tied to the algorithm audit and saved
  full-replay receipt.
- **What to do next:** Decide whether this source contract is sufficient for
  promotion beyond audit status; otherwise perform a manual source review
  against the same checklist.

### 2026-06-24 - Cycle116 slot-block assembly audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_slot_assembly_audit.md`,
  `experimental/scripts/verify_m1_cycle116_slot_assembly.py`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-SLOT-ASSEMBLY-VERIFIED.
- **What is being added:** A finite-field assembly verifier proving that the
  Cycle116 co-support is `{1}` plus seven disjoint active 16-point slot blocks,
  hence has size `113` for every seven-slot tuple.
- **How it is useful:** Removes the co-support geometry as an opaque internal
  assumption in the M1 Cycle116/Cycle120 chain; the remaining boundary is now
  source comparison that the external Cycle116 packet uses this exact assembly.
- **What to do next:** Compare the external Cycle116 source statement against
  the verified assembly, then continue source review of the generated Cycle84
  projected-census replay implementation.

### 2026-06-24 - Cycle120 end-to-end finite chain

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/scripts/verify_m1_cycle120_end_to_end_chain.py`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / END-TO-END-FINITE-CHAIN.
- **What is being added:** A composed verifier and short note checking that the
  Cycle84 exact occupancy numerator, Cycle116 fixed-jet/native threshold,
  smooth lift to `[512,256]`, and Cycle120 density gate align.
- **How it is useful:** Turns the M1 Cycle120 audit from separate local checks
  into one runnable finite-chain contract, with the remaining promotion
  boundaries isolated to official ABF source review, generated replay-source
  review, and Cycle116 packet-to-slot assembly review.
- **What to do next:** Review the three remaining promotion boundaries, then
  decide whether the finite-chain audit can be promoted or whether the optional
  Cycle119 strict-radius strengthening should be pursued.

### 2026-06-24 - Cycle84 exact occupancy chain

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle84_exact_occupancy_chain.md`,
  `experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-EXACT-OCCUPANCY-CHAIN / CONDITIONAL.
- **What is being added:** An end-to-end verifier that composes the color-shell
  witnesses, projected-log certificate, full projected-census replay receipt,
  and kernel-lift filter to derive the exact Cycle84 product occupancy.
- **How it is useful:** Makes the finite numerator consumed by Cycle116/Cycle120
  explicit in one place: `52,747,567,092` distinct products, true energy `24`,
  `m_max=2`, and no fibers of size at least `3`.
- **What to do next:** Review the generated projected-census replay source
  against the replay algorithm audit, then decide whether the Cycle84 finite
  anchor can be promoted beyond conditional audit.

### 2026-06-24 - Cycle84 projected replay algorithm audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle84_projected_replay_algorithm_audit.md`,
  `experimental/scripts/verify_m1_cycle84_projected_replay_algorithm.py`, and
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / FINITE-MODEL-ALGORITHM.
- **What is being added:** A proof-style audit of the generated projected
  census replay algorithm, plus exact toy-model checks comparing circular
  slices, shard canonicalization, and duplicate-energy accounting against brute
  force.
- **How it is useful:** Reduces the remaining Cycle84 projected-census boundary
  from an opaque generated C++ implementation to human review against explicit
  invariants and independently checked small exact models.
- **What to do next:** Have a reviewer compare the generated Cycle84 C++ source
  to the audit note, then decide whether to promote the projected-census replay
  from conditional audit to reviewed finite proof.

### 2026-06-24 - Cycle84 full projected-census replay

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/data/witnesses/m1-cycle84/projected_census_full_replay_receipt.json`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_projected_full_replay_receipt.py`,
  and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-PROJECTED-CENSUS-FULL-REPLAYED /
  CONDITIONAL.
- **What is being added:** A saved receipt for a completed all-shards run of
  `verify_m1_cycle84_projected_census_shard_replay.py --all-shards --threads
  16`, plus a lightweight verifier for that receipt.
- **How it is useful:** Removes the unselected-shard gap from the Cycle84
  projected duplicate-bin census audit: all `16,384` shards replayed from the
  current `slot_logs.json` and matched the compact receipt.
- **What to do next:** Audit the generated C++ replay implementation itself,
  then decide whether the Cycle84 projected census import can be promoted from
  conditional finite audit to reviewed finite proof.

### 2026-06-24 - Cycle84 projected-census shard replay

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_projected_census_shard_replay.py`,
  and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-PROJECTED-CENSUS-SHARD-REPLAYED /
  CONDITIONAL.
- **What is being added:** A generated C++ replay for selected shards of the
  Cycle84 tau-folded projected duplicate-bin census, using the current
  `slot_logs.json` rather than archived headers.
- **How it is useful:** Recomputes the receipt's duplicate-containing shards
  from the current certificate fixtures and checks that no extra duplicates
  occur in those shards, while keeping the full census replay boundary explicit.
- **What to do next:** Run the same verifier with `--all-shards --threads N`,
  or audit the generated replay source, to remove the remaining
  unselected-shard import.

### 2026-06-24 - Cycle84 projected-census receipt

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/data/witnesses/m1-cycle84/projected_census_receipt.json`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_projected_census_receipt.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-PROJECTED-CENSUS-RECEIPT-VERIFIED /
  CONDITIONAL.
- **What is being added:** A compact receipt for the archived Cycle84
  tau-folded projected duplicate-bin scan, plus a verifier tying the receipt to
  the current projected-log certificate, color-shell count, and 30 kernel-lift
  candidates.
- **How it is useful:** Narrows the remaining Cycle84 finite import to the
  heavy census replay/source audit itself, rather than an unstructured archived
  output file.
- **What to do next:** Independently rerun or audit the optimized projected
  census generator that produced the receipt.

### 2026-06-24 - Cycle84 projected-log certificate

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/data/witnesses/m1-cycle84/README.md`,
  `experimental/data/witnesses/m1-cycle84/slot_logs.json`,
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_projected_log_certificate.py`,
  `experimental/scripts/verify_m1_cycle84_color_collision_witnesses.py`,
  `experimental/scripts/verify_m1_cycle84_kernel_lift_candidates.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-LOG-CERTIFICATE-VERIFIED.
- **What is being added:** A compact 336-row projected-log certificate for the
  Cycle84 normalized slot table. The verifier checks every discrete log by
  exponentiation in `F_17^16`, verifies colors and residue vectors, and checks
  the tau-pair projected-log structure used by the duplicate-bin census.
- **How it is useful:** Ties the remaining projected tau-folded census to
  actual finite-field slot products without importing the old workflow,
  generated archive, or full replay bundle.
- **What to do next:** Audit or rerun the projected tau-folded duplicate-bin
  enumeration over this certified log table.

### 2026-06-23 - Cycle84 kernel-lift candidate verification

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_kernel_lift_candidates.py`,
  `experimental/scripts/verify_m1_cycle84_color_collision_witnesses.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-KERNEL-LIFT-VERIFIED / CONDITIONAL.
- **What is being added:** A verifier for all 30 projected Cycle84 duplicate-bin
  lift candidates. It checks 60 normalized witnesses against the current slot
  table, verifies color shell membership, full-log exponentiation, congruence
  modulo `(17^16-1)/3`, and the kernel-difference test distinguishing the six
  true collision orbits from the 24 false projected collisions.
- **How it is useful:** Narrows the remaining Cycle84 finite import again: the
  kernel lift/filtering is now replayed locally, leaving projected tau-folded
  duplicate-bin completeness as the precise heavy census statement to audit.
- **What to do next:** Independently replay or audit the projected tau-folded
  census showing exactly these 30 projected duplicate bins, each of count 2.

### 2026-06-23 - Cycle84 color shell and collision witnesses

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle84_color_collision_witnesses.py`,
  `experimental/scripts/verify_m1_cycle116_fixed_jet_bridge.py`,
  `experimental/scripts/verify_m1_cycle116_field_lift_contract.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-WITNESS-VERIFIED / CONDITIONAL.
- **What is being added:** A compact verifier for the Cycle84 color shell and
  explicit collision witnesses, using the normalized slot table from the
  Cycle116 slot replay. It checks the exact color-shell size
  `52,747,567,104`, verifies six product-collision pairs and their tau partners,
  and records their ordered-energy contribution `24`.
- **How it is useful:** Reduces the remaining Cycle84 finite wall to the sharp
  energy upper bound `D <= 24`. If that imported bound holds, the verified
  witnesses saturate all collisions and give the exact downstream numerator
  `52,747,567,092`.
- **What to do next:** Independently replay or audit the Cycle84 ordered-energy
  upper bound for the normalized slot table; this is now the precise finite
  census bottleneck.

### 2026-06-23 - Cycle116 slot identity replay

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/scripts/verify_m1_cycle116_slot_identities.py`,
  `experimental/scripts/verify_m1_cycle116_fixed_jet_bridge.py`,
  `experimental/scripts/verify_m1_cycle116_field_lift_contract.py`,
  `experimental/scripts/verify_m1_cycle120_gate_arithmetic.py`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE-MODEL-IDENTITY-VERIFIED.
- **What is being added:** A self-contained replay of the 336 Cycle116 slot
  identities in `F_17[X]/(X^16+X^8+3)`. The verifier recomputes the three seed
  polynomials, all slot block locators, all normalized evaluations
  `R_tia(beta)=3^t u_tia`, full-slot product checks, single-slot injectivity,
  and a digest for the normalized 336-value table:
  `47ae84dc2df0fe0b4b43a7e0543b141fb940061fc48ccb80b40ce4e9483abc01`.
- **How it is useful:** Removes the 336 slot identities as an opaque import in
  PR #100. The remaining finite wall is now sharper: the Cycle84 product
  occupancy census must be audited for exactly this normalized slot table.
- **What to do next:** Compare the emitted table digest with the Cycle84 public
  replay/certificate data or independently rerun the Cycle84 occupancy census
  from this table.

### 2026-06-23 - Cycle116 fixed-jet slot-block reduction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle116_fixed_jet_bridge.py`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / SLOT-IDENTITY-DEPENDENT.
- **What is being added:** The Cycle116 fixed-jet/product-scalar import is
  narrowed to the 336 slot identities. A formal reduction shows that seven
  blocks `R_t=X^16+O(X^10)` plus the common `(X-1)` factor force
  `P_T=X^113-X^112+O(X^107)`, and that
  `R_t(beta)=3^t u_t` gives `P_T(beta)=4(beta-1)Phi(T)`.
- **How it is useful:** Makes PR #100 more reviewable by separating a short
  symbolic bridge from the remaining finite-computation burden. The live
  Cycle116 bottleneck is now the slot identities and the Cycle84 occupancy
  census, rather than an opaque fixed-jet statement.
- **What to do next:** Independently replay or audit the 336 slot identities
  and the Cycle84 product occupancy certificate; then keep the smooth lift and
  ABF source gates as separate review layers.

### 2026-06-23 - Cycle116 finite-chain contract

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle116_finite_chain_contract.md`,
  `experimental/scripts/verify_m1_cycle116_field_lift_contract.py`,
  `experimental/notes/m1/m1_cycle120_abf_source_gate_audit.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / FINITE-COMPUTATION-DEPENDENT.
- **What is being added:** A compact contract for the finite chain behind the
  Cycle120 candidate: Cycle84 exact product occupancy, the abstract fixed-jet
  locator-to-support-wise-MCA transfer, and a proved abstract smooth-padding
  lift to the smooth `[512,256]` row. The companion verifier checks the
  deterministic field and lift arithmetic
  (`X^16+X^8+3` irreducible over `F_17`, `eta` order `256`, nonsquare lift to
  `F_17^32`, `theta` order `512`, and the exact support/rate/density ledger).
- **How it is useful:** Moves PR #100 from a gate/arithmetic audit toward the
  actual mathematical bottleneck. The abstract fixed-jet transfer proof is now
  stated in reviewer form, the smooth padding lift is no longer a black-box
  imported clause, and the heavy Cycle84 census plus fixed-jet instantiation
  remain explicit imports to verify or falsify.
- **What to do next:** Review the imported Cycle84 finite census and the two
  Cycle116 instantiation clauses:
  `P_T(X)=X^113-X^112+O(X^107)` and
  `P_T(beta)=4(beta-1)Phi(T)`, then independently replay or audit the compact
  Cycle84 finite certificate.

### 2026-06-23 - Cycle120 ABF source gate audit

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_abf_source_gate_audit.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`, and
  `experimental/agents-log.md`.
- **Status:** AUDIT / SOURCE-PARTIAL / PDF-EXTRACT-DEPENDENT.
- **What is being added:** A source-gate audit for the Cycle120 M1 candidate.
  It separates independently reachable public sources from the PR #96 ABF PDF
  extract: the Proximity Prize page and Giacomo Fenzi's author page confirm the
  challenge and paper identity, while Definitions 2.11, 2.12, and 4.3 are still
  treated as PDF-extract evidence because direct ePrint access is blocked by
  Cloudflare in this environment.
- **How it is useful:** Discharges the first promised follow-up on PR #100
  without importing copied PDFs, rendered pages, HTML snapshots, or generated
  packets. It narrows the live bottleneck: assuming the ABF extract is faithful,
  the Cycle120 row passes the grand MCA source gates, so the remaining hard
  audit is the Cycle84/Cycle116 finite proof chain.
- **What to do next:** Independently fetch the official ABF PDF/source with page
  references, then review the Cycle84 count and Cycle116 fixed-jet transfer
  directly. Keep Cycle119 as a strict-ball strengthening rather than the
  ABF-critical input.

### 2026-06-23 - Cycle120 gate arithmetic contract

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/scripts/verify_m1_cycle120_gate_arithmetic.py`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / SOURCE-CHECK-NEEDED.
- **What is being added:** A compact reviewer contract for the Cycle120
  ABF-facing M1 candidate, separating the deterministic gate/arithmetic layer
  from the imported Cycle84 count and Cycle116/Cycle119 transfer proofs. The
  companion verifier checks the exact threshold, field-size, rate, smooth-domain
  envelope, and `2^-128` denominator arithmetic without fetching sources or
  writing files.
- **How it is useful:** Turns the current Cycle120 obstruction into a minimal
  auditable packet: if the ABF source gates and finite proof chain survive
  independent review, the row
  `RS[F_17^32,<theta>,256]` violates the printed
  `epsilon_mca(C,125/256) <= 2^-128` target. It keeps the status conditional
  and avoids importing generated archives.
- **What to do next:** Independently fetch the official ABF source with page
  references, then review the finite certificate for `K`, `theta`, `H`, the
  Cycle84 numerator, and the Cycle116 fixed-jet transfer. Treat Cycle119 as the
  optional strict-ball strengthening.

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
### 2026-06-24 - M1 Cycle120 ABF extract source hash audit

- **Agent/model:** Codex acting autonomously.
- **Files added or changed:**
  `experimental/scripts/verify_m1_cycle120_abf_extract_sources.py`,
  `experimental/notes/m1/m1_cycle120_abf_extract_source_hash_audit.md`,
  `experimental/notes/m1/m1_cycle120_abf_source_gate_audit.md`,
  `experimental/notes/m1/m1_cycle120_gate_arithmetic_contract.md`,
  `experimental/notes/m1/m1_cycle120_end_to_end_finite_chain.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / ABF-PDF-EXTRACT-SOURCES-VERIFIED.
- **What is being added:** A nonmutating verifier for the PR #96 ABF
  PDF-extract evidence used by the Cycle120 gate audit. It checks Git object
  metadata, byte sizes, SHA256 digests, the packet zip checksum, rendered
  source pages 5/9/17, and both text-extract anchor checks for the grand MCA
  challenge, Definitions 2.11/2.12, and Definition 4.3.
- **How it is useful:** Converts the local ABF extract dependency from a
  prose-only import into an executable, hash-pinned provenance check while
  preserving the official ePrint/revision check as an explicit promotion
  boundary.
- **What to do next:** Independently fetch and review the official ABF
  ePrint source, then compare the official source to the PR #96 extract before
  promoting the Cycle120 row beyond source-conditioned audit status.
