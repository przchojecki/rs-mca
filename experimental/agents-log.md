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

### 2026-06-17 - p=257 locator end-to-end certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/p257_locator_certificate.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A stdlib-only exact certificate for Paper A
  verification item V2, checking all `9`-subsets of `Q=<2>` in `F_257` for the
  locator top coefficients and the 144-point agreement identity.
- **How it is useful:** Supports `tex/RS_disproof_v3.tex` `app:verify` V2,
  `ex:257`, and `lem:locator` with reproducible finite output.
- **What to do next:** Link this certificate from the Paper A finite-claim
  audit, while keeping restricted-sum coverage certificates separate.
