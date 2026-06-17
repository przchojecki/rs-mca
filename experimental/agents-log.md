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

### 2026-06-17 - Consolidated consistency audits

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/domain_convention_audit.py`,
  `experimental/security_mode_label_audit.py`,
  `experimental/frontier_problem_inventory.py`, and
  `experimental/field_ledger_vocabulary_audit.py`.
- **Status:** AUDIT.
- **What is being added:** Consolidates domain-convention, security-mode,
  frontier/problem, and field-ledger vocabulary scanners across the stable TeX
  manuscripts.
- **How it is useful:** Gives reviewers one consistency-audit bundle for the
  project vocabulary and problem frontier without editing stable TeX.
- **What to do next:** Review the consistency diagnostics and decide whether
  any terminology or problem-ledger normalization should be promoted.
