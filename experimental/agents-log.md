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

### 2026-06-17 - F1 degree-1 residue-line toy witness

- **Agent/model:** Codex
- **Files added or changed:** `experimental/f1-extension-witness/README.md`,
  `experimental/f1-extension-witness/canonical-residue-witness.json`,
  `experimental/f1-extension-witness/verify_ext_witness.py`,
  `experimental/agents-log.md`.
- **Status:** EXPERIMENTAL / AUDIT.
- **What is being added:** A self-contained toy certificate for the degree-1
  residue line `f=1/(x-beta)`, `g=x^4` over `B=F_17`, `F=F_17^2`, `n=8`,
  `k=4`, with `beta=(0,1)`, slope `z*=(0,1) in F\B`, full-domain F-support,
  and `51` independently recounted `F\B` bad slopes.
- **How it is useful:** Supports the F1 extension-line MCA direction with a
  non-localized residue-denominator witness, matching the residue-line normal
  form more closely than a coordinate perturbation.
- **What to do next:** Determine whether the degree-1 residue mechanism scales
  to the quantitative Paper D regimes; search for richer companion directions
  `g` that reach fixed sub-capacity gaps; then test rates `1/4`, `1/8`, cubic
  extensions, and larger smooth domains before promotion.
