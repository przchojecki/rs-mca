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

### 2026-06-18 - Paper A finite-verification crosswalk

- **Agent/model:** Codex.
- **Files added or changed:** Added
  `experimental/a1_paperA_finite_verification_crosswalk.md`.
- **Status:** AUDIT / PROVED for the finite computations cited in the
  crosswalk.
- **What is being added:** A review map from Paper A Appendix A finite claims
  V1-V5 to the repository scripts that reproduce them, with notes on the
  Claude Opus 4.8 export package and its missing/stale verifier handles.
- **How it is useful:** Supports A1 by making the finite verification route
  explicit, avoiding the `Q=<2>` versus full-group confusion in V1, and keeping
  Paper B verifier material out of the Paper A audit lane until separately
  reviewed.
- **What to do next:** If the Claude standalone verifier scripts are recovered,
  review them as optional convenience wrappers against this crosswalk before
  adding them to `experimental/`.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, certificates, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
