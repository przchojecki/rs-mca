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

### 2026-06-17 - L2 exact-support diagonalization

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/l2_exact_support_diagonalization.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A deterministic L2 lemma showing that exact-support
  base-list certificates lift to equal-row interleaving diagonally, plus an
  exact inclusion-exclusion count for off-diagonal quotient tuples at lower
  agreement thresholds.
- **How it is useful:** Directly addresses the `agents.md` L2 question of
  whether quotient-core lower bounds multiply under interleaving or share the
  same support structure.
- **What to do next:** Use this as a guardrail for interleaved lower-bound
  ledgers; charge quotient-core interleaving by the explicit intersection
  count rather than by an unsupported Cartesian-product exponent.
