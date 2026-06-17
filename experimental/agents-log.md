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

### 2026-06-17 - Tiny interleaved-list enumerator

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `scripts/interleaved_list_enum.py`,
  `experimental/interleaved_list_enum_certificate.md`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** Adds an exhaustive tiny-parameter enumerator for
  comparing direct interleaved RS list counts with the trivial base-list product
  bound.
- **How it is useful:** Supports the L2/Paper C interleaved-list lane by
  producing exact small-case data for the overcharge of `L_mu <= L_1^mu`.
- **What to do next:** Run grids of tiny prime-field examples and compare the
  observed ratios with candidate multi-fiber injection bounds.
