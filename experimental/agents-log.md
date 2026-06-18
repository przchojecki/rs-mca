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

### 2026-06-18 - M1 fixed-dither slack-window ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Generalizes the adjacent-slack obstruction to every
  dyadic scale `m`: for a fixed dither `r`, active whole-fiber quotient slacks
  in an eligible window are exactly the residue class `u == r mod m`, with
  first-exchange codegree `s_u(n-s_u)/m^2`.
- **How it is useful:** This turns dimension dithering from a one-slack trick
  into a finite slack-window ledger.  Any L3 scanner can now report the exact
  set `L_win(r)` of dyadic quotient scales that reappear across a target slack
  window, and budget their first-exchange random-line terms explicitly.
- **What to do next:** Compare candidate proof-system dimensions by minimizing
  the window ledger over allowed dithers `r`, then combine the surviving
  whole-fiber terms with the one-remainder profile already proved in this PR.

### 2026-06-18 - M1 adjacent-slack dither obstruction

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds a dyadic obstruction showing that a fixed
  dimension dither cannot eliminate all whole-fiber quotient-periodic
  strict-overlap scales at two adjacent slack radii: when the relevant support
  sizes stay away from the scale-two endpoints, scale `m=2` survives at
  exactly one parity class of slacks, with codegree `s_u(n-s_u)/4`.
- **How it is useful:** This prevents the maximal-dither corollary from being
  overread as a uniform slack-window cure.  It tells the M1/L3 ledger that
  dimension dither must be chosen per target slack, or else the surviving
  scale-two quotient term must be budgeted explicitly.
- **What to do next:** Combine the adjacent-slack obstruction with concrete
  proof-system degree constraints, so scanners report not only the best
  one-slack dither but also the quotient scales that reappear over the full
  slack window being targeted.

### 2026-06-18 - M1 maximal-dither all-scale random-line ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Converts the maximal-dither all-scale remainder
  profile into an explicit random-line missing-slope certificate at every
  dyadic quotient scale.  The verifier checks the weighted correction
  `R_MAX(m,t,q)` and its large-tail and boundary closed forms.
- **How it is useful:** This closes the remaining gap between the exact
  quotient-remainder profile and the M1 random-line support-family ledger: at
  maximal dither every dyadic scale now has a closed certificate numerator,
  with nonlinear terms confined to the finite small-scale prefix.
- **What to do next:** Use the all-scale ledger to rank dyadic quotient scales
  at concrete protocol parameters and compare the resulting missing-slope
  numerators with aperiodic residue-line scans.

### 2026-06-18 - M1 maximal-dither scale confinement

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Extracts a finite-prefix theorem from the maximal
  dither all-scale formula: at dyadic maximal dither, every quotient scale
  `m>t` has the same linear strict one-remainder profile, `m=t` has one
  boundary term, and all nonlinear terms are confined to dyadic scales `m<t`.
- **How it is useful:** This turns the remaining maximal-dither M1 quotient
  hierarchy into a uniform large-scale tail plus an explicitly bounded
  small-scale prefix, making the quotient-periodic exception finite and
  explicit at fixed slack.
- **What to do next:** Combine this scale confinement with finite small-scale
  scanners and the random-line certificate ledger to budget maximal-dither
  quotient packets before attacking the aperiodic residue-line contribution.

### 2026-06-17 - M1 quotient-periodic overlap profile

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Gives the exact overlap, strict high-overlap, and
  max exchange-codegree profile for support families formed by unions of equal
  quotient fibers, including the exact-support divisibility guardrail that this
  whole-fiber family is absent unless the fiber size divides `s = k+t` and the
  finite quotient-prefix form of the strict-overlap correction. Adds the
  dyadic dither corollary: for `k=k0-(t-1)`, every nontrivial dyadic
  whole-fiber scale `m <= k0` fails the exact-support divisibility test, and
  more generally surviving dyadic scales are counted by `v2(t-r)`. Adds the
  exact one-remainder-fiber exchange enumerator, the large-fiber strict
  remainder truncation, the stable large-scale dither hierarchy, the
  maximal-dither all-scale strict profile, and a verifier for the formulas.
  Adds random-line certificate corollaries obtained by substituting `R_QP` and
  `R_REM` into the support-family variance ledger, including an explicit
  maximal-dither large-scale missing-slope bound.
- **How it is useful:** Supplies the quotient-periodic input to the M1
  support-family ledger, so this structured exception can be separated
  quantitatively before attacking the aperiodic residue-line local-limit
  problem; it also records the exact-support form of dimension/slack dithering
  and the smaller remainder profile that survives after whole-fiber supports
  are absent. The large-fiber truncation shows that maximal dyadic dither
  leaves only a linear one-remainder strict codegree at scales `m>t`; the
  hierarchy formula shows that nonmaximal dither with `d=t-r0` retains
  unweighted mass `((n-k0)/m)binom(m,d)-1` at stable large scales. The
  maximal-dither all-scale formula gives the exact strict profile at every
  nontrivial dyadic quotient scale when `s=k0+1`. The certificate corollaries
  turn these profiles into the actual random-line missing-slope quantities
  consumed by the M1 support-family framework.
- **What to do next:** Have a tiny M1 scanner emit `|A|`, `Delta_j(A)`, and
  `Gamma_j(A)` by labelled support class, verifying that the quotient-periodic
  class matches the closed formulas here.

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
