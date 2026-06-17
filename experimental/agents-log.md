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

### 2026-06-17 - L1/L2 random simultaneous support-fiber baseline

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_l2_random_support_fiber_baseline.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Exact first- and second-moment formulas for random
  simultaneous support fibers: independent `mu`-row received words have
  `E |Fib_U^cap(k+sigma)| = binom(n,k+sigma) / q^(mu sigma)`, with variance
  controlled exactly by pairs of supports intersecting in at least `k` points;
  the interleaved list size injects into this simultaneous support fiber.
- **How it is useful:** Advances L1 and L2 by giving the entropy-scale random
  baseline and showing why column-distance interleaving pays one common
  support family rather than a Cartesian product of `mu` base families.
- **What to do next:** Compare worst-case quotient-periodic and structured
  received rows against the first/second-moment baseline; use it to calibrate
  future L2 scanner output and protocol list ledgers.
