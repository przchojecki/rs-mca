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

### 2026-06-17 - Consolidated repo, release, and script hygiene

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/script_reproducibility_audit.py`,
  `experimental/release_bundle_inventory.py`,
  `experimental/readme_script_layer_inventory.py`, `scripts/run_frontier.py`,
  and `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Consolidates source-level script reproducibility,
  release-bundle, README script-manifest, and frontier-scanner CLI metadata
  work into one repo-hygiene PR.
- **How it is useful:** Gives reviewers one coherent project-hygiene bundle;
  only the existing `scripts/run_frontier.py` is edited in `scripts/`, while
  new audit scripts stay under `experimental/`.
- **What to do next:** Review whether the frontier CLI metadata is sufficient
  and decide which audit checks should become CI gates.
