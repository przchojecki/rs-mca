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

### 2026-06-17 - A0 Crites-Stewart rational constant derivation

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/a0_cs25_rational_constant_derivation.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / CONDITIONAL.
- **What is being added:** A short algebra note deriving Paper D's relaxed
  `q * epsilon / (1 - theta)` list bound from the exact rational
  Crites-Stewart-style formula, including the `theta = 1/2` contrapositive.
- **How it is useful:** Advances A0 by isolating the constant manipulation in
  the universal-cap import; if the primary theorem has the displayed rational
  interface, the local `1/(2k) * (1 - n/q)` threshold follows exactly.
- **What to do next:** Check the primary Crites-Stewart theorem for radius
  range, augmented-code definition, CA normalization, field generality, and
  strictness conventions before treating the cap import as source-certified.
