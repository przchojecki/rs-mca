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

### 2026-06-17 - Generated-field entropy margin checker

- **Agent/model:** Codex acting autonomously.
- **Files added or changed:** `scripts/entropy_margin.py`,
  `experimental/entropy_margin_certificate.md`, `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED.
- **What is being added:** Adds a generated-field entropy margin checker and a
  proof note for the finite binomial-entropy interval certificate used by the
  checker.
- **How it is useful:** Supports the Paper C generated-field ledger and the P2
  certificate-scanner task without touching the main papers or overlapping the
  active locator-fiber and F1 witness PRs.
- **What to do next:** Review the certificate semantics, then use the script to
  reproduce Paper C entropy-feasibility rows and decide whether it should feed a
  future unified certificate emitter.
