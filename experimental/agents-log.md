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

### 2026-06-17 - Canonical-line MCA slope scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/mca_slope_scan.py`,
  `experimental/mca_slope_scan_certificate.md`, `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A pure-Python scanner for small prime-field
  canonical-line support-wise MCA bad slopes, plus a `p=13`, `n=12`, `k=6`
  certificate run.
- **How it is useful:** Implements the planned `mca_slope_scan.py` script from
  `agents.md`, supports the quotient-locator lemma and M1 finite checks, and is
  separate from locator-fiber/list scanning.
- **What to do next:** Extend the scanner to residue-line normal forms or use
  it as an oracle for future extension-line searches.
