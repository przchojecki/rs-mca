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

### 2026-06-17 - F1 monic-anchor base-core reduction

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/f1_monic_anchor_base_core_reduction.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the monic-anchor balanced stratum.
- **What is being added:** Extracts a clean finite theorem showing that
  balanced extension-valued monic-anchor F1 lines have bad slopes exactly
  given by incidences between locator readouts modulo
  `hatE = lcm(E,E^tau)` and an affine slope target.
- **How it is useful:** Sharpens the repaired F1 path after the fixed-rate
  counterexample: extension denominators increase the base readout degree by
  at most a factor of two in this stratum, while the arbitrary-anchor balanced
  gap remains explicitly open.
- **What to do next:** Attack the arbitrary-anchor balanced F1 gap in the full
  residue-line normal form, or prove no-rich-line bounds for the base-core
  incidence set above the corrected reserve.

### 2026-06-17 - F1 fixed-rate extension-line counterexample

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/f1_fixed_rate_extension_counterexample.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / COUNTEREXAMPLE.
- **What is being added:** Extracts a clean fixed-rate sigma-one proof that
  genuinely extension-valued denominators over `F_{p^2}` give constant
  support-wise MCA bad-slope density, refuting the unrestricted
  numerator-preserving extension-line lift.
- **How it is useful:** Resolves the unrestricted F1 lift direction negatively
  at fixed rate and identifies the needed repair: prove over the actual
  extension line field, add an extension-valued numerator term, or impose a
  corrected-reserve restriction.
- **What to do next:** Attack the repaired F1 problem above the corrected
  reserve, where this sigma-one construction is excluded, or reformulate these
  extension-valued lines as structured interleaved-base objects over `B`.

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
