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

### 2026-06-17 - Consolidated reserve and certificate tooling

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/entropy_margin.py`,
  `experimental/restricted_sum_dp.py`, `experimental/quotient_profile.py`,
  `experimental/interleaved_budget.py`, `experimental/interleaved_list_enum.py`,
  `experimental/domain_descriptor.py`, `experimental/certificate_emit.py`,
  `experimental/reserve_certificate_schema.json`, and companion certificates
  and examples under `experimental/`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Consolidates the generated-field entropy,
  restricted-sum, quotient-profile, interleaved-list, field-domain, reserve
  schema, and certificate-emission tooling into one experimental-first PR.
- **How it is useful:** Gives reviewers a coherent tooling bundle for reserve
  certificates and scriptable ledger checks while avoiding premature promotion
  of new scripts into `scripts/`.
- **What to do next:** Review API shape and outputs before promoting stable
  utilities into `scripts/` or wiring them into CI.
