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

### 2026-06-17 - Interleaved budget calculator

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/interleaved_budget.py`,
  `experimental/interleaved_budget_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED.
- **What is being added:** Adds a dependency-free calculator for Paper C's
  interleaved-list, MCA, and toy query-count soundness budgets.
- **How it is useful:** Supports the P2 certificate-scanner lane by converting
  list and MCA numerator bounds into a minimum `q_line` bit width and query
  count.
- **What to do next:** Feed outputs from the entropy, quotient-profile, and
  failure-ladder scanners into this calculator or a future certificate emitter.
