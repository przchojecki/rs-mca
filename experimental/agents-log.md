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

### 2026-06-18 - L1 aperiodic prefix-collision certificate

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/l1_aperiodic_prefix_collision.md`,
  `experimental/verify_l1_aperiodic_prefix_collision.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / COUNTEREXAMPLE.
- **What is being added:** Promotes a finite `F_17` monomial-prefix
  route cut into a standalone proof note and verifier: for `n=16`, `k=6`,
  `sigma=4`, the full `Phi_4` fiber distribution has forty aperiodic
  two-point collisions and no larger fibers, despite positive generated-field
  entropy margin and empty quotient-core profile.  The verifier also compresses
  the collisions into three dilation orbits of complement locator pairs with
  linear gaps `L_A-L_B`, using the general complement-prefix lemma for
  multiplicative subgroups, records the exact divisor-gap parametrization, and
  records the equivalent divisor-gap graph formulation and co-large prefix bound
  `|Phi_sigma^{-1}(c)| <= q^max(n-k-2sigma,0)`.
- **How it is useful:** Targets L1 by showing that quotient-core removal
  cannot be strengthened to finite-field aperiodic injectivity; the surviving
  local-limit theorem must be a multiplicity bound for aperiodic prefix
  collisions.
- **What to do next:** Use the verifier shape as a tiny scanner target for
  larger monomial-prefix cases and separate isolated aperiodic collisions from
  quotient-periodic families.

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
