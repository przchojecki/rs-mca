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

### 2026-06-17 - Quotient-profile dither scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/quotient_profile.py`,
  `experimental/quotient_profile.md`, `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A finite-length dyadic divisor scanner for the exact
  quotient-core profile `Qprof_H(a,k)` and a separate remainder-variant
  diagnostic for dimensions `k=rho*n-r`.
- **How it is useful:** This targets L3 by making quotient hygiene and
  dimension dithering checkable at actual finite parameters, including the
  deployed-rate comparison between exact `k=rho*n` and one-step dithered
  `k=rho*n-1`.
- **What to do next:** Compare the scanner output with concrete AIR/R1CS or
  Plonkish degree bounds, and promote the script to `scripts/` after review if
  maintainers want it as stable certificate tooling.
