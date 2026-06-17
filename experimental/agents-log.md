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

### 2026-06-17 - Script reproducibility audit

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/script_reproducibility_audit.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A deterministic stdlib scanner for `scripts/*.py`
  that reports CLI shape, proof-status and reproducibility markers, JSON or
  certificate markers, third-party imports, and relative file writes.
- **How it is useful:** Checks the current script layer against the repo
  convention that computational contributions should report input parameters,
  exact checked objects, results, certificates or seeds, theorem/problem IDs,
  and proof status.
- **What to do next:** Use the findings to decide whether existing scripts
  should gain argparse metadata, explicit proof-status output, JSON output, or
  clearer output-path handling.
