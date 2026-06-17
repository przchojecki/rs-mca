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

### 2026-06-17 - Table environment inventory

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/table_environment_inventory.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A deterministic stdlib scanner that inventories
  table-like environments in stable TeX, including captions, labels, section
  context, status vocabulary, and raw tabular blocks.
- **How it is useful:** Gives reviewers a mechanical table-surface view for
  release hygiene, status-ledger tables, and hand-computed tables that may
  eventually need script-backed certificates.
- **What to do next:** Review any caption or label diagnostics and decide
  which hand-maintained tables should be paired with generated certificates.
