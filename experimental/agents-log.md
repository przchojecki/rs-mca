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

### 2026-06-17 - Lean formalization starter

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/lean_formalization/README.md`,
  `experimental/lean_formalization/lakefile.lean`,
  `experimental/lean_formalization/lake-manifest.json`,
  `experimental/lean_formalization/lean-toolchain`,
  `experimental/lean_formalization/RsMca.lean`,
  `experimental/lean_formalization/RsMca/Basic.lean`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL.
- **What is being added:** A stdlib-only Lean 4 starter project formalizing
  proof-status labels, support agreement predicates, support-wise MCA
  bad-support predicates, quotient-locator parameter arithmetic, and script
  certificate records.
- **How it is useful:** Starts the good-first Lean formalization track without
  touching the papers or relying on `mathlib`; later agents can extend it toward
  finite-field/domain descriptors and exact certificate statements.
- **What to do next:** Connect the abstract `code` and `combine` parameters to
  concrete finite-field and Reed--Solomon definitions, then formalize checked
  JSON certificate claims.
