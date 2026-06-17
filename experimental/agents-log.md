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

### 2026-06-17 - Sieve mechanism finite certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/sieve_mechanism_certificate.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A stdlib-only exact enumeration certificate for
  Paper A verification item V5, checking the `N=16`, `r=9` cyclotomic value
  count `3280` and the six listed finite-field reductions.
- **How it is useful:** Supports `tex/RS_disproof_v3.tex` `app:verify` V5 and
  `lem:value-family` with reproducible finite output for the sieve mechanism.
- **What to do next:** Link this certificate from the Paper A finite-claim
  audit and keep broader restricted-sum DP experiments separate.
