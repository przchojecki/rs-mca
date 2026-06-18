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

### 2026-06-18 - M1 slack-two first-superboundary shape ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the slack-two shape reduction; CONDITIONAL on the
  standard Jacobi-sum estimate for the cyclotomic bound; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Shows that all `T=2`, `|P|=3` residual packets are
  the six-to-one image of unit-equation shapes `u in D`, `-1-u in D`, with
  slope multiplier `alpha(u)=-(1+u+u^2)`, exact quotient-lift weight, and a
  square-coset slope-count bound. It also records the cyclotomic/Jacobi
  estimate for the unit-equation shape count over prime fields.
- **How it is useful:** Turns the first nonzero superboundary catalog from
  support enumeration into a finite multiplicative unit-equation problem plus
  the square-image map on `D`.
- **What to do next:** Bound the unit-equation shape set `C_2(D)` for smooth
  domains and compare its slope image against the corrected M1 reserve.

### 2026-06-18 - M1 first-superboundary zero-slope packets

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the first-superboundary zero-slope classification;
  AUDIT / EXPERIMENTAL for scanner verification.
- **What is being added:** Shows that residual packets of size `T+1` have
  sparse polynomial `X^(T+1)+zX-c`; the zero-slope packets are exactly
  `(T+1)`-power cosets, with an exact cyclic-domain count and lift count.
- **How it is useful:** Splits the first superboundary into a solved
  zero-slope power-coset ledger and the genuinely new nonzero-slope sparse
  trinomial residual catalog.
- **What to do next:** Bound or classify the nonzero-slope `D`-split
  trinomials `X^(T+1)+zX-c` in small slack cases.

### 2026-06-18 - M1 canonical residual-packet lift

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the residual-packet lift factorization; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Proves that for the canonical line with `T<m`,
  every residual zero-prefix packet `P` has exactly
  `binom(N-tau(P),(s-|P|)/m)` whole-fiber lifts, all with slope
  `(-1)^T e_T(P)`.
- **How it is useful:** Reduces the unresolved superboundary range `T<|P|<m`
  to the residual packet catalog itself; the quotient-core lift and slope
  multiplicity are no longer part of the unknown.
- **What to do next:** Classify or bound the first superboundary residual
  packet catalog, starting with `|P|=T+1`.

### 2026-06-18 - M1 canonical small-residual ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the closed small-residual ledger; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Packages the canonical large-fiber small-residual
  cases for support residues `b<=T`: whole-fiber residue `b=0` gives only
  slope `0`, subboundary residues `0<b<T` give no canonical small-residual
  supports, and boundary residue `b=T` gives the counted `-D^T` slope image.
- **How it is useful:** Gives dither scans a direct decision rule for all
  canonical residual packets below one quotient fiber except the genuinely
  partial superboundary regime `b>T`.
- **What to do next:** Attack the first unclassified superboundary case
  `T<b<m`, where partial-fiber zero-prefix solutions can exist.

### 2026-06-18 - M1 canonical subboundary residue floor

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the residue-floor corollary; AUDIT / EXPERIMENTAL for
  scanner verification.
- **What is being added:** Proves that if `T<m` and the support residue
  `b=(k+T) mod m` satisfies `0<b<T`, then every canonical residual support has
  at least `m+b` residual points; in particular maximal one-step dither
  forces at least `m+1` residual points at large quotient scales.
- **How it is useful:** Converts dimension dither into a precise canonical
  small-residual exclusion: whole-fiber, one-remainder, and boundary-coset
  canonical sources are all absent in the subboundary residue regime.
- **What to do next:** Use this floor to separate large-residual canonical
  incidences from the exact small structured ledgers in future M1 scans.

### 2026-06-18 - M1 canonical boundary slope image

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the cyclic-domain boundary slope image; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Shows that the boundary residual canonical slope
  image is exactly `-D^T`, of size `n/T` when `T|n`, and that each such slope
  has witness multiplicity `binom(N - T/gcd(T,m), L)` at support size
  `Lm+T`.
- **How it is useful:** Converts the remaining canonical boundary obstruction
  from support bookkeeping into an exact bad-slope count with uniform
  multiplicity, which is the quantity consumed by M1.
- **What to do next:** Compare this exact boundary slope image with arbitrary
  line support-occupancy scans to separate canonical quotient residuals from
  genuinely aperiodic slope concentration.

### 2026-06-18 - M1 canonical boundary-coset count

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the cyclic-domain boundary-coset count; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Classifies boundary residual canonical supports in
  a cyclic multiplicative domain: they exist only when `T|n`, are cosets of
  the subgroup of size `T`, touch `T/gcd(T,m)` quotient fibers, and at support
  size `Lm+T` are counted by
  `(n/T) binom(N - T/gcd(T,m), L)`.
- **How it is useful:** Turns the first residual canonical obstruction after
  quotient-core removal into an exact finite quotient-level family rather than
  an unstructured partial-fiber source.
- **What to do next:** Combine this count with the boundary slope
  decomposition to enumerate the actual canonical slope image of boundary
  residual cosets in larger toy scans.

### 2026-06-18 - M1 canonical quotient-core slope decomposition

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the slope decomposition; AUDIT / EXPERIMENTAL for
  scanner verification.
- **What is being added:** Proves that, for the canonical slack line, the
  slope below the fiber boundary `T<m` is computed entirely from the residual
  partial-fiber set; at `T=m`, the whole quotient core contributes only the
  additive quotient-level term `-sum y_i`.
- **How it is useful:** Makes the canonical quotient cleanup sharper: after
  whole fibers are stripped away, both incidence and slope data are residual
  except at a controlled boundary where the remaining whole-fiber dependence
  is quotient-level.
- **What to do next:** Use this slope decomposition to compare boundary
  canonical slopes with the cross-histogram occupancy ledger and isolate any
  residual boundary-coset families in larger toy scans.

### 2026-06-18 - M1 canonical low-residual exclusion

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the low-residual exclusion and boundary
  classification; AUDIT / EXPERIMENTAL for scanner verification.
- **What is being added:** Proves that, for the canonical slack line with
  `T<=m`, any residual partial-fiber set of size `0<|R|<T` cannot satisfy the
  zero-prefix equations over a multiplicative domain; at `|R|=T`, the residual
  set must be a full root set of `X^T-c`.
- **How it is useful:** Shows that maximal and more general low-residual
  dithers remove canonical quotient-locator incidences, leaving the first
  possible residual canonical obstruction as a rigid boundary coset rather
  than an arbitrary partial-fiber packet.
- **What to do next:** Use the boundary-coset diagnostic to identify whether
  residual canonical obstructions at `|R|=T` survive in larger toy scans, and
  separate them from arbitrary-line occupancy incidences.

### 2026-06-18 - M1 canonical quotient-core factorization

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the canonical quotient-core factorization; AUDIT /
  EXPERIMENTAL for scanner verification.
- **What is being added:** Proves that whole quotient fibers are invisible to
  low elementary-symmetric coefficients `e_d` for `d<m`, so for the canonical
  slack line with `T<=m` the bad-slope zero-prefix equations depend only on
  the residual partial-fiber set.
- **How it is useful:** Separates the canonical quotient-locator source from
  the residual aperiodic obstruction: after exact whole-fiber supports are
  removed by dither, the remaining canonical condition is an explicit
  partial-fiber symmetric-zero problem.
- **What to do next:** Use the support-occupancy scanner to search tiny
  canonical examples for residual zero-prefix supports beyond the one-point
  maximal-dither case, then compare their histogram classes with the exact
  occupancy overlap ledger.

### 2026-06-18 - M1 cross-histogram occupancy ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/m1_occupancy_profile_scan.py`,
  `experimental/m1_occupancy_profile_scan.md`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the cross-histogram coefficient formula and union
  ledger; AUDIT / EXPERIMENTAL for scanner reporting.
- **What is being added:** Extends the occupancy-profile theorem from
  within-histogram covariance to exact source-to-target histograms
  `H_{h->g}` and gives closed `Delta_j` and `Gamma_j` ledgers for unions of
  content classes, with full-layer Johnson recovery as a verifier check.
- **How it is useful:** Removes the remaining cross-content caveat from the
  quotient-fiber occupancy cleanup: full support layers can now be audited by
  histogram transitions rather than support-pair enumeration.
- **What to do next:** Use the union ledger alongside the support-occupancy
  incidence scanner to compare actual bad-slope concentration against the
  structured quotient-content covariance budget.

### 2026-06-18 - M1 support-occupancy incidence scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the quotient-occupancy incidence decomposition;
  AUDIT / EXPERIMENTAL for the scanner.
- **What is being added:** Decomposes exact support-coefficient incidences by
  quotient-fiber occupancy and adds a tiny-field scanner that computes
  `Pi_S(f), Pi_S(g)`, contributed slopes, and histogram labels.
- **How it is useful:** Connects the quotient occupancy ledger to actual M1
  bad-slope supports, making it possible to distinguish whole-fiber,
  one-remainder, mixed-partial, and candidate aperiodic incidence sources in
  toy cases.
- **What to do next:** Run the scanner on additional tiny fields and line
  families, then compare observed incidence histograms with the exact
  occupancy-profile random-line ledgers.

### 2026-06-18 - M1 occupancy-profile scanner

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_occupancy_profile_scan.py`,
  `experimental/m1_occupancy_profile_scan.md`,
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the histogram-enumeration corollary; AUDIT /
  EXPERIMENTAL for the scanner.
- **What is being added:** Adds a complete quotient-fiber occupancy scanner
  that enumerates all feasible histograms at fixed support size and evaluates
  the exact strict exchange ledger for each content class.
- **How it is useful:** Makes the M1 quotient-structured cleanup executable:
  toy scans can now account for every within-content quotient-fiber class
  before treating any remaining profile as aperiodic.
- **What to do next:** Combine this histogram scanner with a small
  top-coefficient `Pi_S` line scanner to label actual bad-slope supports by
  quotient-fiber content.

### 2026-06-18 - M1 general fiber-occupancy profile

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the coefficient formula; AUDIT for verifier
  specializations.
- **What is being added:** Proves an exact exchange enumerator for every fixed
  quotient-fiber occupancy histogram, with the whole-fiber and one-remainder
  profiles as special cases.
- **How it is useful:** Turns the proposed M1 scanner step into a finite
  coefficient calculation for each quotient-fiber content class before any
  remaining profile is treated as aperiodic.
- **What to do next:** Implement the full occupancy-histogram grouping scanner
  for small M1 toy cases and compare the leftover profile against the
  quotient-structured ledgers.

### 2026-06-18 - M1 finite-menu large-scale dichotomy

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the dichotomy; AUDIT / EXPERIMENTAL for scanner
  reporting.
- **What is being added:** Consolidates the finite-menu theory into two
  large-scale regimes: gap-one finite-prefix linearity, or a forced
  super-linear stable tail of degree `D_C>=2`.
- **How it is useful:** Gives a compact decision rule for scanner output and
  protocol-window comparisons, reducing the many finite-menu threshold lemmas
  to one operational dichotomy.
- **What to do next:** Apply the dichotomy to concrete proof-system slack
  windows and check whether the required gap-one menu size is feasible.

### 2026-06-18 - M1 gap-one window finite prefix

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Shows that a gap-one finite menu confines all
  nonlinear dyadic quotient-remainder terms over a slack window to the finite
  prefix `m <= t_+`; all larger dyadic scales are linear for both adjacent
  choices.
- **How it is useful:** Completes the adaptive-competitive picture by proving
  that the exact gap-one menu has no nonlinear large-scale tail, while smaller
  menus force one.
- **What to do next:** Use this finite-prefix ledger as the quotient-periodic
  cleanup step before applying any future aperiodic M1 local-limit scanner.

### 2026-06-18 - M1 co-maximal all-scale ledger

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED.
- **What is being added:** Adds the complement-dual all-scale formula for the
  over-dithered adjacent choice `s=k0-1`, including the large-scale linear
  tail, boundary term, and finite small-scale prefix.
- **How it is useful:** Completes the all-scale quotient-remainder ledger for
  gap-one finite menus: both `r=t-1` and `r=t+1` now have exact random-line
  certificate inputs at every dyadic quotient scale.
- **What to do next:** Use the two-sided gap-one all-scale ledger when
  comparing finite-menu designs against per-slack maximal dither at concrete
  protocol windows.

### 2026-06-18 - M1 gap-one finite-menu sufficiency

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the sufficiency theorem; AUDIT / EXPERIMENTAL for
  scanner reporting.
- **What is being added:** Gives the exact stable profile of a gap-one
  capacity-achieving finite dither menu. Every served slack has a choice
  `r=t-1` or `r=t+1`, producing a linear stable tail no larger than the
  adaptive maximal-dither baseline in the standard rate range.
- **How it is useful:** Completes the finite-menu characterization: the
  gap-one capacity inverse `C_ad(L_W)` is both necessary and sufficient for
  asymptotic adaptive competitiveness over unbounded dyadic quotient scales.
- **What to do next:** Compare this exact menu-size requirement with real
  protocol degree windows before deciding whether finite-menu or per-slack
  adaptive dithering is the viable design.

### 2026-06-18 - M1 window-weighted adaptive threshold

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the threshold lemma; AUDIT / EXPERIMENTAL for scanner
  reporting.
- **What is being added:** Compares the finite-menu weighted lower bound to
  the maximum adaptive weighted baseline over the whole slack window. The
  exact conservative threshold pays `q^(|W|+D-2)` instead of the same-slack
  factor `q^(D-1)`.
- **How it is useful:** Separates same-slack intuition from protocol-level
  window budgeting, making the line-field and slack-window penalties explicit.
- **What to do next:** Use the window-weighted scanner fields to find concrete
  parameter ranges where finite menus dominate even after the whole-window
  adaptive penalty.

### 2026-06-18 - M1 adaptive-competitive menu size

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the menu-size corollary; AUDIT / EXPERIMENTAL for
  scanner reporting.
- **What is being added:** Shows that scale-unbounded adaptive competitiveness
  for a finite dither menu is equivalent to forced safe gap one, and records
  the exact gap-one capacity inverse `C_ad(L_W)`.
- **How it is useful:** Converts the finite-menu separation into an operational
  lower bound on menu size: any smaller menu eventually reintroduces a
  super-linear stable tail at large dyadic quotient scales.
- **What to do next:** Compare the exact `C_ad(L_W)` requirement against
  real protocol degree windows and decide whether adaptive dither or a larger
  menu is viable.

### 2026-06-18 - M1 adaptive separation scale threshold

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the threshold lemma; AUDIT / EXPERIMENTAL for scanner
  reporting.
- **What is being added:** Gives the exact binomial threshold
  `K_side binom(m-1,E-1) > E(n-k0)` for when a forced finite-menu gap beats
  the adaptive linear mass, plus the corresponding weighted inequality.
- **How it is useful:** Sharpens the previous asymptotic separation into a
  finite-scale rule, identifying the first dyadic quotient scale where a small
  dither menu is provably worse than adaptive maximal dither.
- **What to do next:** Use the first-separating-scale scanner fields to compare
  finite menus against concrete protocol degree windows and line-field sizes.

### 2026-06-18 - M1 finite-menu adaptive separation

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the separation criterion; AUDIT / EXPERIMENTAL for
  scanner reporting.
- **What is being added:** Compares the finite-menu stable-tail floor to the
  adaptive maximal-dither linear baseline. If the exact menu capacity forces
  gap `E>=2`, the finite-menu mass floor grows like `m^(E-1)` relative to the
  adaptive baseline on large quotient scales.
- **How it is useful:** Turns the adaptive-vs-menu comparison into a concrete
  scale criterion, showing when a bounded dimension menu cannot emulate
  per-slack maximal dither.
- **What to do next:** Use the scanner's adaptive comparison fields to locate
  protocol windows where finite menus already dominate the adaptive linear
  baseline.

### 2026-06-18 - M1 adaptive maximal-window baseline

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED for the adaptive maximal-dither baseline; AUDIT /
  EXPERIMENTAL for scanner reporting.
- **What is being added:** Shows that the per-slack maximal dither rule
  `r(t)=t-1` keeps every dyadic scale `m>t_+` in a slack window at the uniform
  linear tail `H=(n-k0-1)y`, with weighted maximum
  `(n-k0-1)q^(t_+-1)`.
- **How it is useful:** Provides the clean adaptive baseline against which the
  finite-menu exact-capacity obstruction and forced stable-tail floors should
  be compared.
- **What to do next:** Use the scanner's adaptive baseline and finite-menu
  floor side by side on concrete protocol slack windows.

### 2026-06-18 - M1 dither-menu capacity inverses

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/quotient_profile_dither.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Records the closed inverse formulas for the exact
  dither-menu capacity: minimum menu size for a target safe gap, and forced
  safe gap for a fixed menu size.
- **How it is useful:** Makes the finite-menu stable-tail floor directly
  computable from `(L_W,C,D)` without a minimization step or scanner-specific
  interpretation.
- **What to do next:** Use the closed inverse formulas in protocol parameter
  comparisons and keep the verifier grid as the executable cross-check.

### 2026-06-18 - M1 exact capacity proof audit

- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Files added or changed:**
  `experimental/m1_quotient_periodic_overlap_profile.md`,
  `experimental/verify_m1_quotient_remainder_profile.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Expands the proof of the exact dither-menu capacity
  upper bound and adds an exhaustive small-grid verifier for the closed
  capacity formula and forced-gap inverse.
- **How it is useful:** Strengthens the sharp finite-menu theorem that now
  drives the stable-tail mass and weighted lower-bound scanner fields.
- **What to do next:** Keep using the exact capacity formula in scanner output;
  any future bounded-dither claims should check against this grid verifier.

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
