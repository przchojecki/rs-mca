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

### 2026-06-17 - Consolidated finite-field experiment certificates

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/q17_locator_mca/`,
  `experimental/mca_slope_scan.py`, `experimental/deployed_dsh_certificate.py`,
  `experimental/goldilocks_density_certificate.py`,
  `experimental/extension_full_density_certificate.py`,
  `experimental/sieve_mechanism_certificate.py`,
  `experimental/p257_locator_certificate.py`, and companion certificates.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Consolidates small-field locator/MCA checks,
  canonical MCA slope scanning, and deployed-field density certificates into
  one experimental certificate bundle.
- **How it is useful:** Gives reviewers a coherent finite-field evidence layer
  for the no-slack obstruction and related locator/density mechanisms while
  keeping new scripts under `experimental/`.
- **What to do next:** Review certificate statements and decide which checks
  should be generalized, optimized, or promoted into stable scripts.
