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

### 2026-06-17 - Interleaved support-fiber bridge

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/l2_interleaved_support_bridge.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL.
- **What is being added:** A finite support-fiber injection showing that
  interleaved lists at column agreement `a>=k` inject into simultaneous
  feasible agreement supports, so a uniform support-fiber bound transfers to
  `Int(C,mu)` without a Cartesian-product `mu` exponent.
- **How it is useful:** This targets L2 by separating list-size product bounds
  from support-fiber bounds, clarifying when the protocol interleaved-list
  ledger can avoid overcharging concrete arities.
- **What to do next:** Match the locator local-limit assumption to this
  support-fiber predicate and test tiny `mu=2` examples where the product bound
  is loose.
