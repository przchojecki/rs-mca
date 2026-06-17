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

### 2026-06-17 - Consolidated TeX integrity audits

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/cross_citation_phrase_audit.py`,
  `experimental/bibkey_drift_audit.py`,
  `experimental/tex_reference_integrity_audit.py`,
  `experimental/tex_citation_integrity_audit.py`, and
  `experimental/tex_macro_definition_audit.py`.
- **Status:** AUDIT.
- **What is being added:** Consolidates citation phrase, bibkey drift,
  reference integrity, citation integrity, and macro-definition drift scanners
  for the stable TeX manuscripts.
- **How it is useful:** Gives reviewers a coherent manuscript-integrity audit
  bundle without modifying stable TeX.
- **What to do next:** Review diagnostics and decide which findings deserve
  stable manuscript edits or style normalization.
