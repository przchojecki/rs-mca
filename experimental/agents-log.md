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

### 2026-06-17 - M2 line-decoding to MCA bridge

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/m2_line_decoding_mca_bridge.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A finite-support bridge defining the exact
  support-wise line-decoding numerator `LD_sw(C,a)` and proving
  `eps_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|`.
- **How it is useful:** This targets the M2 open problem by making precise
  which line-decoding statement implies the MCA ledger bound consumed by the
  SNARK certificate.
- **What to do next:** Match external `(delta,a_LD,n+1)` line-decoding
  definitions against `LD_sw`, then express the residue-line packing conjecture
  directly in this numerator.
