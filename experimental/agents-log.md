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

### 2026-06-17 - Domain-shattering quotient residual scan

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/domain_shatter_quotient_scan.py`,
  `experimental/domain_shatter_quotient_scan.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** A deterministic scanner for quotient-core lower
  bounds that survive puncturing a smooth cyclic domain, using intact quotient
  cosets and anchor cosets with enough retained points.
- **How it is useful:** This targets X3 by making quotient degeneracy testable
  for partially shattered domains, including small hitting-set patterns that
  delete one representative from every coset of a chosen quotient scale.
- **What to do next:** Compare residual profiles against FFT-friendly
  puncturing schedules and test whether any schedule destroys all deployed
  quotient-core scales while keeping acceptable rate and evaluation structure.
