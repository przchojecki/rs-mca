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

### 2026-06-17 - Extension full-density arithmetic certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/extension_full_density_certificate.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A stdlib-only exact arithmetic certificate for the
  Fermat and deployed Proth-style base fields in Paper A's extension-tower
  full-density corollary, checking the base prerequisites and coordinate-wise
  DSH inequalities at all four prize rates.
- **How it is useful:** Supports `tex/RS_disproof_v3.tex`
  `thm:ext-smooth-towers` and `cor:fermat-proth-towers` by replacing the
  `m^2 >= 18p` and rate-by-rate DSH arithmetic with reproducible output.
- **What to do next:** Link this certificate from the Paper A finite-claim
  audit, and keep extension-line witness searches separate from this
  theorem-backed full-density family.
