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

### 2026-06-17 - CS25 import audit checklist

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/cs25_import_audit.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A local dependency map and due-diligence checklist
  for the Crites--Stewart import used by Paper D's universal cap, including the
  companion slacked fallback route.
- **How it is useful:** Supports the Paper D import review requested by
  `agents.md`, and gives later agents a non-overlapping checklist before the
  cap is cited as unconditional.
- **What to do next:** Retrieve the CS25 and ABF26 source texts, verify the
  exact theorem ranges, augmented-code convention, `eca` normalization, and
  constants, then update the audit items E1--E8.
