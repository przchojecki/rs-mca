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

### 2026-06-17 - M1 average support-collinearity bound

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_average_support_collinearity.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Exact average-case and overlap bounds for random
  lines: support/slope MCA incidences have expectation
  `binom(n,k+t) * (q^t - 1) / q^(2t - 1)`, expected bad-slope density is at
  most `binom(n,k+t) / q^t`, and support-pair covariance can begin only when
  the two supports intersect in at least `k` points. The note also includes a
  fixed-base/random-direction formula showing that base-word support-list mass
  contributes only to the zero slope `z = 0`.
- **How it is useful:** Gives a rigorous random-line baseline for the M1
  residue-line packing problem, matching the entropy-scale density heuristic
  while isolating the codimension `t-1` support-collinearity cost and the
  basepoint slope contribution.
- **What to do next:** Build a tiny-field `Pi_S` collinearity scanner and
  compare tangent, quotient-periodic, and aperiodic support sources against
  the expectation and high-overlap covariance baseline.
