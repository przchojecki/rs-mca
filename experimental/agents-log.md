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

### 2026-06-17 - Result environment inventory

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/result_environment_inventory.py`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A deterministic stdlib scanner that inventories
  theorem-like environments in the stable TeX manuscripts. It reports line
  ranges, labels, optional titles, section context, duplicate labels, repeated
  titles, and unlabeled entries without modifying stable TeX.
- **How it is useful:** Complements the frontier problem inventory and theorem
  label map by giving a mechanical coverage view for proof/result environments
  such as theorems, lemmas, propositions, corollaries, definitions, facts,
  tasks, and milestones.
- **What to do next:** Review unlabeled and repeated-title diagnostics before
  deciding whether any stable TeX label cleanup or theorem-map promotion is
  warranted.
