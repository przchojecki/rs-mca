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

### 2026-06-18 - M2 exact-support residue-line equivalence

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m2_line_decoding_mca_bridge.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Defines the exact-support residue-line packing
  number `RL_NC^=(D,k,a)` and records the equality
  `LD_sw(RS[F,D,k],a)=RL_NC^=(D,k,a)=RL_NC(D,k,a)` for `a >= k+1`.
- **How it is useful:** This pins the M2 target to the exact-support object
  consumed by M1 support-overlap ledgers and avoids a separate larger-support
  accounting layer in future scanners.
- **What to do next:** Use `RL_NC^=` as the default residue-line object in
  exact-support line-decoding/MCA certificate tooling.

### 2026-06-18 - M2 exact-support witness reduction

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m2_line_decoding_mca_bridge.md`,
  `experimental/m2_line_decoding_separation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Proves that for Reed-Solomon codes and
  `a >= k+1`, every support-wise noncontained witness on a support of size at
  least `a` contains an exact-size `a` witness.  The verifier now compares
  exact-size witness projection with all large-support projection.
- **How it is useful:** This lets M2 certificates work with exact support
  families, matching the M1 support-profile and residue-line ledgers instead
  of having to scan every larger support size separately.
- **What to do next:** Use exact-size support families in future
  line-decoding/residue-line scanners and reserve ledgers.

### 2026-06-18 - M2 support-witness projection certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m2_line_decoding_mca_bridge.md`,
  `experimental/m2_line_decoding_separation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds a finite support-witness projection
  certificate for `LD_sw`: the support-wise bad slopes are the projection of
  witness pairs `(S,z)`, and slope-fiber multiplicity can improve the naive
  support-count bound.
- **How it is useful:** This connects the M2 line-decoding numerator to the
  support-family machinery used in M1.  A certificate can count noncontained
  witness supports, then divide by verified witness multiplicity when many
  supports project to the same bad slope.
- **What to do next:** Use this projection certificate in residue-line scans
  to distinguish support-pair mass from the distinct slope numerator consumed
  by the protocol ledger.

### 2026-06-17 - M2 close-point line-decoding separation

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m2_line_decoding_mca_bridge.md`,
  `experimental/m2_line_decoding_separation.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Strengthens the M2 bridge note with an explicit
  Reed-Solomon spike-line separation: at agreement `a=n-1`, ordinary
  close-point line-decoding can see all `|F|` slopes on a line not contained
  in the code, while the support-wise noncontained numerator for the same
  line is exactly one. Adds the agreement-coordinate residue-line equivalence
  `LD_sw(RS[F,D,k],a)=RL_NC(D,k,a)` under the same denominator hypothesis used
  in Paper B's normal form. Adds a tiny enumerator that verifies the
  separation and the residual code-line-exception bound.
- **How it is useful:** Shows that close-point line-decoding with only a
  contained-line exception is strictly stronger than the support-wise MCA
  numerator consumed by the Paper C ledger. The corrected M2 target should
  therefore be stated in the support-wise/common-support form unless an
  external line-decoding theorem has a stronger exception that rules out this
  spike-line phenomenon. The residue-line equivalence identifies that
  support-wise form exactly with the corrected M1 residue-line packing object.
  The residual bound explains how a common code-line proximity exception can
  still leave a smaller support-wise numerator to budget.
- **What to do next:** Match protocol line-decoding imports against this
  support-wise predicate and record whether their exceptional case is strong
  enough for the corrected reserve certificate.

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
