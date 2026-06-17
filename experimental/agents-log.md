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

### 2026-06-17 - Deployed-field DSH divisor certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/deployed_dsh_certificate.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** A stdlib-only exact integer certificate for the
  deployed-field DSH divisor claims in Paper A, checking `N | p-1`,
  `rho*N in Z`, and the bound
  `(rho*N+1)*((1-rho)*N-1)+1 >= p`.
- **How it is useful:** Replaces one hand arithmetic step in
  `tex/RS_disproof_v3.tex` `thm:main(a)` with reproducible output for
  BabyBear, KoalaBear, and `3*2^30+1`.
- **What to do next:** Link this certificate from a future Paper A audit table,
  and add separate certificates for the Fermat and extension-tower rows.
