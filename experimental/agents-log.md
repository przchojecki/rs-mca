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

### 2026-06-17 - X1 tangent CA/MCA separation

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/x1_tangent_ca_mca_separation.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A tangent-floor separation lemma showing that one
  explicit line has at least `floor(delta n)` support-wise MCA-bad slopes while
  the same pair has no CA-bad slopes at no-proximity-loss radius `delta`.
- **How it is useful:** Supports X1/M1 by proving that CA-to-MCA bridges need
  an additive `n/q`-scale tangent correction, support memory, or a separate
  tangent-pattern certificate.
- **What to do next:** Use this as a constraint when formulating any
  list/CA/MCA equivalence theorem; do not collapse CA and support-wise MCA
  without paying the tangent floor.
