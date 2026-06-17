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

### 2026-06-17 - Paper A no-slack proof audit

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/no_slack_proof_audit.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT.
- **What is being added:** A lemma-by-lemma audit table for Paper A's no-slack
  obstruction proof, separating symbolic arguments from finite computation
  certificates that still need reproducible commands.
- **How it is useful:** Supports M1 in `tex/proximity_blueprint_v3.tex` and A1
  in `agents.md`, giving future agents a concrete checklist for machine
  verification of deployed, Fermat, q=17, sieve, and extension-tower claims.
- **What to do next:** Attach exact script commands or JSON certificates for
  each finite claim, then update the audit rows from `AUDIT` to proved where
  the evidence is reproducible.
