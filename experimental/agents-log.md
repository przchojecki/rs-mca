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

### 2026-06-17 - Chebyshev circle-domain fiber verifier

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/chebyshev_circle_fiber_verify.py`,
  `experimental/chebyshev_circle_fiber_verify.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** A finite-field verifier for the Dickson--Chebyshev
  identities `D_m(X_N)=X_{N/m}` and
  `locator(D_m^{-1}(w) cap X_N)=D_m(X)-w` on small circle `x`-coordinate
  domains.
- **How it is useful:** This targets the circle/Chebyshev analogue direction by
  making the fiber-locator transfer mechanism reproducible before using it in
  quotient-core or slack-one experiments.
- **What to do next:** Extend the verifier to enumerate the corresponding
  quotient-core and slack-one bad-slope counts over circle-domain toy
  instances.
