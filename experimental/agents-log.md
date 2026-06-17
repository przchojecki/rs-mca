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

### 2026-06-17 - M1 support coefficient test

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A finite-dimensional proof note showing that, for
  fixed support size, arbitrary-line support-wise MCA witnesses are exactly
  collinearities between the top-coefficient vectors `Pi_S(f)` and `Pi_S(g)`.
- **How it is useful:** Advances M1 by giving a scanner-ready invariant for
  residue-line packing and recovering the canonical slack multi-symmetric
  formula as a special case.
- **What to do next:** Implement a tiny-field scanner that enumerates
  `Pi_S` collinearities and labels tangent, quotient-periodic, and aperiodic
  support sources.
