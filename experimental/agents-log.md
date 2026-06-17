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

### 2026-06-17 - q=17 locator/MCA exhaustive checker

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/q17_locator_mca/README.md`,
  `experimental/q17_locator_mca/verify_q17_locator_mca.py`,
  `experimental/q17_locator_mca/q17_locator_mca_certificate.json`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A pure-Python exhaustive checker and certificate for
  `q=17`, `n=16`, and rates `rho=1/2,1/4`, covering locator restricted-sum
  fibers and support-wise canonical-line MCA bad slopes.
- **How it is useful:** Supplies a reproducible finite certificate for the
  good-first `q=17` item in `agents.md`, and separates direct slack-one MCA
  checks from slack-two `C+` list-fiber checks used by Paper D.
- **What to do next:** Compare the tiny exhaustive data with larger locator
  sweep outputs once those experimental sweep PRs land.
