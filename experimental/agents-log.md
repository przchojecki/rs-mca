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

### 2026-06-17 - Quotient-profile scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/quotient_profile.py`,
  `experimental/quotient_profile_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED.
- **What is being added:** Adds a deterministic scanner for the exact
  quotient-core profile `Qprof_H(a,k)` and a certificate note proving that the
  divisor enumeration matches the Paper C profile definition.
- **How it is useful:** Supports the L3/P2 quotient-profile and dimension
  dithering lane without touching the active entropy, restricted-sum,
  locator-fiber, or F1 witness PR lanes.
- **What to do next:** Review generated rows against protocol parameter tables
  and add a separate scanner for the non-exact remainder variant if needed.
