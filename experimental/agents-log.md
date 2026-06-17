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

### 2026-06-17 - Certificate emitter utility

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/certificate_emit.py`,
  `experimental/certificate_emit_example.json`,
  `experimental/certificate_emit_example.md`,
  `experimental/certificate_emit_certificate.md`, `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A stdlib-only Markdown/TeX emitter for JSON script
  certificates following the `agents.md` output standard, plus a deterministic
  example.
- **How it is useful:** Implements the planned `certificate_emit.py` script
  without depending on the open reserve-schema PR, giving later scanners a
  common way to produce reviewable artifacts.
- **What to do next:** Wire future scanner outputs into this emitter and add
  schema validation once the reserve-certificate schema lands.
