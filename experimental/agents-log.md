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

### 2026-06-18 - M1 exact dither-menu capacity

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the exact capacity theorem; AUDIT / EXPERIMENTAL for
  scanner reporting.
- **What is being added:** Sharpens the finite dither-menu bound to the exact
  safe covering capacity
  `Cap(C,D)=floor(C/2)(3D+1)+(C mod 2)D`, accounting for the forbidden exact
  support point `t=r`.
- **How it is useful:** Removes the factor-two slack in the previous menu
  bound and makes the stable-tail floor depend on the exact forced safe gap
  `min{D: |W|<=Cap(C,D)}`.
- **What to do next:** Use the exact capacity certificate, not the coarse
  counting bound, when comparing finite deployed-dimension menus.

### 2026-06-18 - M1 weighted finite-menu tail floor

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the weighted lower-bound corollary; AUDIT /
  EXPERIMENTAL for scanner reporting.
- **What is being added:** Lifts the finite-menu stable-tail mass floor to the
  random-line weighted correction: the forced mass floor contributes at least
  `q_line^(t_- - D)` times its mass in the stable range.
- **How it is useful:** The M1 variance ledger consumes weighted corrections,
  so bounded dither menus now have an explicit line-field-size-dependent tail
  floor, not only an unweighted quotient-remainder mass floor.
- **What to do next:** Compare this weighted floor against concrete M1
  random-line certificate budgets for protocol slack windows.

### 2026-06-18 - M1 finite-menu stable-tail floor

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the stable-tail floor theorem; AUDIT / EXPERIMENTAL
  for scanner reporting.
- **What is being added:** Combines the finite dither-menu covering bound with
  the two-sided stable-tail formula. A `C`-value menu covering a window with
  safe gap at most `D` forces some large dyadic scale to pay mass at least
  `min(k0/m,(n-k0)/m) binom(m,ceil(|W|/(2C))) - 1` in the stable range.
- **How it is useful:** Converts menu size directly into a quotient-remainder
  tail lower bound, clarifying the quantitative cost of replacing per-slack
  dither by a bounded menu of deployed dimensions.
- **What to do next:** Run `--target-stable-gap D --dither-menu-size C` on
  concrete protocol slack windows and compare the forced tail floor against
  the M1 random-line ledger budget.

### 2026-06-18 - M1 finite dither-menu covering bound

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the menu covering bound; AUDIT / EXPERIMENTAL for
  scanner reporting.
- **What is being added:** Proves that a dither menu keeping every slack in a
  window `W` within safe one-remainder gap `D` needs at least
  `ceil(|W|/(2D))` allowed dithers, with a block construction using
  `ceil(|W|/D)`.
- **How it is useful:** Shows that replacing per-slack maximal dither by a
  small fixed menu still leaves growing stable-tail degree over long slack
  windows, unless the menu size grows with the window.
- **What to do next:** Compare realistic protocol degree menus against the
  scanner's `--target-stable-gap` certificate.

### 2026-06-18 - M1 fixed-window stable-tail minimax

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the minimax gap lemma and endpoint stable-tail
  formulas; AUDIT / EXPERIMENTAL for scanner reporting.
- **What is being added:** Proves the fixed-window minimax dither obstruction:
  a center dither minimizes max `|t-r|` but hits exact support `k0`, while any
  dither avoiding exact-`k0` slack over a window of length `L_W` has endpoint
  gap `L_W` and hence, in the stable range, a degree-`L_W` one-remainder tail.
- **How it is useful:** This turns the adjacent-slack obstruction into a
  general finite-window theorem, clarifying why per-slack dimension dither is
  structurally stronger than one fixed dither across a protocol slack window.
- **What to do next:** Use the minimax certificate with weighted stable-tail
  scanner output on concrete protocol slack windows.

### 2026-06-18 - L3 weighted stable-tail scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the stable-tail formula; AUDIT / EXPERIMENTAL for
  scanner ranking.
- **What is being added:** Adds `--line-field-size q` to the slack-window
  dither scanner, reporting the two-sided stable weighted correction
  `R_stable(t,r0,m,q)` for stable large-scale one-remainder entries.
- **How it is useful:** Fixed-window dither comparisons can now rank by the
  weighted M1 variance term consumed by the random-line ledger, not only by
  unweighted remainder mass.
- **What to do next:** Run the weighted scanner on concrete protocol slack
  windows and compare fixed-dither choices against per-slack maximal dither.

### 2026-06-18 - M1 two-sided weighted tail

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Upgrades the two-sided fixed-dither stable tail
  from unweighted mass to the exact random-line correction
  `R_stable(t,r0,m,q)`, with the same side coefficient split according to
  the sign of `d_t=t-r0`.
- **How it is useful:** The M1 support-family variance ledger consumes
  weighted corrections, not just profile mass. Fixed slack-window scans can now
  plug stable one-remainder tails directly into the random-line certificate.
- **What to do next:** Use this closed `R_stable` term when ranking fixed
  dithers over slack windows in the quotient-profile scanner.

### 2026-06-18 - M1 two-sided fixed-dither tail

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Gives the stable large-scale one-remainder mass
  directly in fixed-dither coordinates. For `d_t=t-r0`, `1<=|d_t|<t`, and
  `m>=t+|d_t|`, the mass is `((n-k0)/m)binom(m,d_t)-1` if `d_t>0` and
  `(k0/m)binom(m,|d_t|)-1` if `d_t<0`.
- **How it is useful:** Fixed-window dithers now have an explicit two-sided
  large-scale remainder ledger. Slacks above the dither charge the unused
  quotient side, while slacks below the dither charge the occupied side, which
  matters at biased rates.
- **What to do next:** Add this two-sided tail to the slack-window scanner's
  dither ranking so windows are not optimized only on one side of the dither.

### 2026-06-18 - M1 one-remainder complement duality

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Proves the complement duality
  `H_REM(N,m,L,b)=H_REM(N,m,N-L-1,m-b)` and extracts the stable near-full
  remainder formula: for `b=m-d` and `m>=t+d`,
  `H_REM^{<t}(1)=(L+1)binom(m,d)-1`.
- **How it is useful:** This completes the large-scale one-remainder hierarchy
  on both sides of a fixed dither. The existing under-dithered tail has
  coefficient `N-L`; the over-dithered tail has coefficient `L+1`, so slack
  windows can now budget both directions explicitly.
- **What to do next:** Add the co-remainder stable flag to finite
  slack-window scanners when comparing fixed and per-slack dithers.

### 2026-06-18 - M1 adjacent-slack remainder obstruction

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds the fixed-window remainder obstruction: if a
  dither is maximal at slack `t0`, then at adjacent slack `t0+1` the stable
  large-scale one-remainder mass is `(n-k0)(m-1)/2-1` for every dyadic
  `m | k0` with `m >= t0+3`.  The verifier checks this against the full
  `H_REM` enumerator, and the scanner flags entries where the stable formula
  applies.
- **How it is useful:** This shows that fixed-window dithering cannot be judged
  only by whole-fiber quotient scales: even when those are removed at one
  slack, the adjacent slack can restore scale-dependent one-remainder mass.
- **What to do next:** Use the scanner's stable-entry flag to compare
  per-slack maximal dither against fixed-window dither choices under actual
  proof-system degree constraints.

### 2026-06-18 - L3 one-remainder window scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the strict `H_REM` coefficient formula; AUDIT /
  EXPERIMENTAL for the executable scan report.
- **What is being added:** Extends the slack-window dither scanner to compute
  the exact one-remainder strict codegree mass
  `sum_{1 <= j < t} [y^j] H_REM(y)` for each fixed dither, slack, and dyadic
  scale with nonzero support remainder.
- **How it is useful:** This budgets the quotient packet that remains after
  exact whole-fiber scales are removed by dimension dithering.  It lets L3
  scans distinguish a dither that merely kills whole-fiber supports from one
  that also keeps the one-remainder strict codegree mass small across the
  target slack window.
- **What to do next:** Compare the best fixed dither under the whole-fiber
  window ledger with the best dither under the one-remainder mass ledger, then
  decide whether the proof-system should use per-slack or fixed-window
  dimension choices.

### 2026-06-18 - L3 slack-window dither scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:** `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the `L_win(r)` divisor predicate; AUDIT /
  EXPERIMENTAL for the executable scan report.
- **What is being added:** Extends the existing quotient-profile dither
  scanner with `--slack-window START:END`, which emits the proved
  fixed-dither first-exchange ledger `L_win(r)` and ranks candidate dithers by
  the maximum active first-exchange quotient codegree in the target window.
- **How it is useful:** This directly implements the L3 instruction to compare
  dithered dimensions across finite parameters and record which quotient
  scales remain active, now using the theorem proved in the M1 quotient-profile
  note rather than an ad hoc divisibility scan.
- **What to do next:** Run the window scanner on concrete proof-system degree
  budgets and decide whether the allowed dither set is chosen per target slack
  or fixed over an entire verifier slack window.

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
