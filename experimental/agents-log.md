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

### 2026-06-17 - F1 extension-line slope sweep

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/f1_extension_slope_sweep.py`,
  `experimental/f1_extension_slope_sweep.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** An exact quadratic-extension sweep for
  `f_beta(x)=1/(x-beta)` and `g=x^k`, counting same-support bad slopes for all
  `beta in F \ B` in small `F_p` toy windows.
- **How it is useful:** This probes the F1 extension-line MCA lift problem by
  separating base-field slopes from genuinely extension-valued slopes, and turns
  a single-witness search direction into a reproducible family sweep.
- **What to do next:** Extend the sweep to cubic extensions, larger supports,
  and other directions `g`, then compare the results with the residue-line
  normal forms used by the corrected MCA conjecture.
