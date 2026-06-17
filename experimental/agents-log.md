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

### 2026-06-17 - Field and domain descriptor

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/domain_descriptor.py`,
  `experimental/domain_descriptor_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / PROVED.
- **What is being added:** Adds a dependency-free descriptor for field sizes,
  subfield degrees, domain type, `n`, `k`, reserve data, and interleavings.
- **How it is useful:** Supports the P2 certificate-scanner lane by separating
  `q_arith`, `q_gen`, `q_line`, and `q_chal` before later ledgers consume them.
- **What to do next:** Feed the descriptor JSON into future certificate emitters
  together with entropy, quotient-profile, interleaving, and failure audits.
