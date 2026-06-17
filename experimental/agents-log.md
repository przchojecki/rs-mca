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

### 2026-06-17 - Consolidated proof notes and formalization scaffolding

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/cs25_import_audit.md`,
  `experimental/theorem_label_map.md`, `experimental/lean_formalization/`,
  `experimental/protocol_ledger_template.md`,
  `experimental/common_notation_ledger.md`, and
  `experimental/no_slack_proof_audit.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Consolidates theorem-label maps, import-audit notes,
  protocol-ledger templates, notation ledgers, Paper A proof-audit notes, and a
  Lean starter scaffold into one proof-support PR.
- **How it is useful:** Gives reviewers a coherent proof-audit and
  formalization starting point without modifying the stable manuscripts.
- **What to do next:** Check the notes against the manuscripts and decide which
  items should become stable proof edits or formalization tasks.
