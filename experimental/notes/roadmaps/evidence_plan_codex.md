# Evidence-gathering plan — targeted falsifications and toy proofs (for Codex / any lane)

- **Status:** AUDIT / experiment campaign spec. Companion to
  `execution_queue.md`, `redteam_attack_plan.md`, `enumeration_routes.md`
  and the prize DAG.
- **Objective:** these tasks exist to move PRIORS, not to prove the prize:
  each targets a question where the roadmap-maker is genuinely unsure and
  the two outcomes lead to DIFFERENT route choices. Results feed DAG
  updates (gate reweighting, new grounded conjectures, or S9 ledger
  events). Tasks where both outcomes imply the same next action were
  deliberately excluded — they carry no decision information.
- **Pre-registration discipline (mandatory):** each packet states, BEFORE
  the run: the search space, pinned seeds, the acceptance computation, and
  the interpretation table below verbatim. Negative results are results —
  publish them identically. A falsification hit is a first-class
  COUNTEREXAMPLE contribution (S9 protocol; see redteam_attack_plan.md).
- **Deliverable format:** repo-standard packet (note + verifier + JSON
  artifacts + agents-log), one task per PR, citing the DAG node id and the
  E-number here. Outcome classification printed by the verifier itself.
- **NOTE:** PR #176 already supplies the SPI base-case evidence stream
  (deficiency-1 ladder / prediction P3) — not duplicated here; its outcome
  slots into the same update framework (P3 pass => SPI route prior UP;
  unpaid identically-valid pencil => R2-as-stated falsified).

## E1 — Zone-(b) Row-C sampling: WHICH END OF THE CORRIDOR IS REAL?

```text
TARGET    zone_b / e1_fullness (CRITICAL; four-way route gate)
QUESTION  are e1 value sets (1-o(1))-full or heavily collided for
          quotient orders 80 < N' < 512 at prize-scale p?
PRIOR     ~50/50 in-corridor — the single most information-dense
          unknown on the board
METHOD    numerical, birthday sampling: n = 2^10 row, log2 p ~ 250,
          N' restricted to DIVISORS of n (spec corrected per PR #180's
          compatibility finding: 96/192 invalid on 2-power rows);
          pilot done (#180): zero collisions at 2^18/cell, support
          >= 2^33.4. DECISIVE FOLLOW-UP: N'=64 full birthday run
          (~2^25-2^26 samples reaches the 2^49.7 class count); open
          in-corridor cells (N'=128+) exceed birthday scale — use
          structured-subfamily collision estimators or the
          collision_norm_criterion route instead
INTERPRET density -> 1:      e1_fullness prior UP strongly; corridor
                             lands at the quotient crossing; prioritize
                             norm/amplification extensions (QZ tier);
                             averaged_slope_conversion deprioritized
          heavy collisions   collided branch REAL: averaged_slope_
          at some N':        conversion becomes load-bearing (unsafe
                             side), collision structure gets a new
                             grounded conjecture node (what divides the
                             norms), R4 conspiracy search escalates
          mixed by N':       zone charts gain an interval structure —
                             new stratified conjecture, per-N' gates
```

## E2 — Toy XR inverse: DOES THE ENERGY ROUTE HAVE CLEAN CONTENT?

```text
TARGET    xr_inverse (the XR pipeline's core bet)
QUESTION  at toy scale, is every E_3-large pair structured
          (folded/equivariant or tangent), or do unstructured
          energy-large pairs exist?
PRIOR     ~60% clean — the E_3 functional is OUR invention; this is
          the cheapest kill-or-confirm on the whole XR route
METHOD    numerical + exact algebra: n = 16 (mu_16 in F_97) exhaustive
          over pair orbits; n = 32 sampled; compute the E_3 spectrum
          (definition per QX.1/xr_e3_calculus — build it first or
          co-develop), list top-decile pairs, classify each against
          the known structure taxonomy (verifier prints the residue)
INTERPRET all structured:    XR route prior UP strongly; invest
                             xr_gvn/QE.1 next; C_XR content conjecture
                             added to the DAG (grounded)
          unstructured pair  DECISIVE either way: (a) if it has unpaid
          found:             alignment mass -> fifth-mechanism preview
                             through the energy lens (S9-relevant!);
                             (b) if paid -> E_3 needs redefinition;
                             xr_gvn spec revises BEFORE anyone builds
                             the Cauchy-Schwarz chain
```

## E3 — Spread-regime designs: TRY TO KILL THE CRYSTALLIZATION RESIDUE

```text
TARGET    spread_regime_bound (the open half of crystallization;
          DATA-FIRST by standing decision)
QUESTION  can combinatorial designs (pairwise support intersections
          < k) realize super-poly many aligned slopes?
PRIOR     ~75% true — but with essentially NO evidence in the
          all-small-intersections regime; the two-slope lemma provably
          cannot see it
METHOD    algebraic + numerical: n = 16..64; build co-support families
          from packings/Steiner-like systems; solve the alignment
          linear systems for (u,v); record max #slopes vs family size
          and n; adversarially optimize (this is R5 with growth
          tracking added)
INTERPRET max slopes O(n^c), pattern documents WHICH designs saturate:
          small c stable:    spread_regime prior UP strongly; the c
                             value becomes the conjectured exponent
                             (new grounded statement); XR/SPI
                             classification stages inherit the bound
          growing trend:     falsification track: minimal reproduction,
                             COUNTEREXAMPLE packet; r2_rigidity
                             restates (paid taxonomy gains the design
                             mechanism); corridor arithmetic recomputes
```

## E4 — Auxiliary-list wide regime: THE MIXED-PETAL RESIDUE, MEASURED DIRECTLY

```text
TARGET    pma_wide_residual (single-point-of-failure chain for the
          list challenge)
QUESTION  in the many-petal, sub-Johnson regime, do the auxiliary
          pieced-word lists stay poly (correlated-target structure
          working) or grow?
PRIOR     ~80% poly — but the wide regime is exactly where no data
          exists; the aux-word reduction (QP.1) makes this experiment
          CLEAN for the first time
METHOD    numerical: toy sunflowers (n = 32..128), petal count M swept
          ACROSS the Johnson threshold (d+sigma)^2/(d(sigma+1));
          directly enumerate degree-<=d polynomials near the pieced
          word U* = c_i L_D on T_i; plot list size vs M
INTERPRET bounded/poly:      pma_wide_residual prior UP; the M-scaling
                             data selects between correlated-GS and
                             descent (attack angles a vs b) — the
                             winning angle gets the next decomposition
          super-poly growth: imgfib in danger AS STATED: escalate R3
                             (structured vs unstructured hit); if
                             unstructured, the list-side threshold
                             conjectures revise (major S9-list event)
```

## E5 — Multi-scale resonance: FIRST EVIDENCE IN THE HIDING ROOM

```text
TARGET    payment_completeness (CRITICAL; the 3-strikes hypothesis)
QUESTION  can phase-locked structure across MANY dyadic scales create
          unpaid alignment mass invisible to per-scale ledgers?
PRIOR     ~65-70% no fifth mechanism — the least-tested load-bearing
          assumption (all prior failures of its class were found by
          construction)
METHOD    numerical construction search (R1): n = 2^10..2^12 (8-10
          nested scales, no toy analogue); words assembled from
          isotypic components across several K_M simultaneously,
          phases locked so each single-scale ledger sees
          sub-threshold mass; measure unpaid alignment vs FM baseline;
          structured search space PRINTED (no silent caps)
INTERPRET nothing above FM   payment_completeness prior UP — the first
          by poly factors:   evidence that touches the actual hiding
                             room; red-team pressure shifts elsewhere
          super-FM mass:     FIFTH MECHANISM candidate: minimal
                             reproduction, S9 protocol (ledger node,
                             taxonomy version bump, corridor moves)
```

## E6 — GAP-1 amplification: PUMP THE KNOWN CRACK

```text
TARGET    gap1_noneq_mass (CRITICAL; strip's conditionality)
QUESTION  does non-equivariant periodic mass grow poly or can the
          isolated witnesses be amplified into families?
PRIOR     ~80% poly — but the witnesses exist and nobody has tried to
          amplify them (Q3.3 measurement + R2 construction combined)
METHOD    exact enumeration at F_13/F_97 toys (all K_M-stable supports,
          count multi-isotypic aligned pairs) + constructive
          amplification attempts at n = 64..256; fit growth in n
INTERPRET poly fit:          gap1 prior UP; strip conditionality
                             quantified (the fitted exponent becomes
                             the conjectured constant — grounded)
          super-poly:        GAP-1 ledger required: strip pricing
                             incomplete; paid_closure gains a column;
                             mca_safe assembly restates
```

## E7 — Conjecture F at dimension 2: THE UNAVOIDABLE CONJECTURE'S FIRST OPEN INSTANCE

```text
TARGET    f_primitive_case (dim 1 is PROVABLE at n/j; dim 2 is the
          first unknown)
QUESTION  what is the actual max count of gcd-trivial aperiodic D_j
          points on PAIR-GENERATED planes (kernel/fiber planes — the
          planes the proof actually consumes)?
PRIOR     ~85% poly with small exponent; the VALUE of B_F is unknown
          and matters for every budget downstream
METHOD    exhaustive at n = 16 over pair-generated kernel planes
          (finite: pairs -> planes -> count D_j points, classify
          against paid shapes); sampled at n = 32; tabulate the top
          offenders and their structure
INTERPRET max bounded small: F prior UP + FIRST EXPONENT ESTIMATE
                             (B_F conjecture becomes a number — new
                             grounded node); budget_b3 cross-checked
          a rich plane       INSPECT ITS SHAPE: if it matches a known
          found:             paid stratum, the classifier was
                             incomplete (fix); if genuinely new -> the
                             conj_f statement itself revises — the
                             most consequential possible outcome of
                             this whole campaign
```

## E8 — Mixed-radix toy row: OFF THE 2-POWER CHAIN FOR THE FIRST TIME

```text
TARGET    mixed_radix_frontier (NEW: the family-uniformity gap)
QUESTION  does the base machinery survive when quotient scales form a
          lattice (incomparable M) instead of a chain? EVERY existing
          artifact is a 2-power row; the prize family quantifier is not.
PRIOR     ~90% VACUOUS: the standard FRI/STARK reading of 'smooth' is
          2-power, which the Q0.1 ePrint check confirms; and wp0_2's
          conservativity sketch says 2-power is the quotient-richest
          (hardest) case anyway. Run this ONLY if the rules freeze
          lands on a broader definition.
METHOD    F_97 supports n = 48 = 2^4 * 3. Rerun: FM exact means;
          periodic strata counts over the full divisor lattice
          (including incomparable 2^a*3^b); dedup totality/disjointness
          fuzz; coset-move dynamics. Name every invariant that fails
          to reproduce.
INTERPRET all reproduce:     uniformity prior UP; the frontier's
                             attack surface narrows to the zone-cell /
                             corridor arithmetic on lattices
          named breakage:    the single most valuable negative result
                             available — it localizes exactly which
                             statements silently assumed chain
                             structure, BEFORE the rules freeze
                             potentially makes mixed radix official
NOTE      cheap (toy scale) and high-information in BOTH directions;
          also previews the lattice-forced analogue of E5's resonance.
```

## Suggested order (expected information per unit cost)

```text
1. E1 (corridor decider — highest single-number information)
2. E2 (kill-or-confirm on a whole route, cheap)
3. E3 (the falsifiable core; no evidence exists either way)
4. E7 (data on the one unavoidable conjecture + an exponent)
5. E4 (single-point-of-failure chain, newly measurable)
6. E6 (known crack, cheap enumeration first)
7. E5 (low hit-prior but program-level impact; run in background)
8. E8 (INSURANCE ONLY — skip unless the Q0.1 freeze lands on a
   broader-than-2-power smoothness definition)
```

The roadmap-maker lane commits to processing every completed packet into
the DAG within one maintenance pass: gate reweighting notes, grounded
conjecture nodes (with the measured constants), or S9 events — with the
packet cited as the evidence edge.

# WAVE 3 (2026-07-03) — evidence for the morning decompositions

Same discipline: pre-registered tables, one PR per task, negative
results publish identically. Ranked by expected information.

## E17 — Hankel-kernel support patterns (gates f_termination_hankel)

```text
TARGET    f_termination_hankel / f_descent_termination
QUESTION  are sparse-dual-word supports of Hankel-kernel flats always
          COSET UNIONS (the displacement-structure prediction)?
PRIOR     ~80% yes — E7's kernel twins were exactly coset pairs
METHOD    E9-style census RESTRICTED to Hankel-pencil kernel flats
          (n = 16, j <= 5; the #183 kernel-sample machinery reruns);
          record every sparse word's support against the coset lattice
INTERPRET all coset unions => the lattice bound (QF.14) proceeds on
          the divisor poset; ONE non-coset support => the prediction
          dies and termination needs the general lattice argument
```

## E18 — Full pair-orbit E_3 scanner (the c_xr_content kill-switch)

```text
TARGET    c_xr_content / xr_inverse
QUESTION  E11 scanned a candidate DICTIONARY; do actual A_{u,v}
          pair-orbit alignment sets, post-strip, have top E_3 only at
          fixed-core/fixed-hole structures?
PRIOR     ~75% clean (dictionary + k=1 dictators both agree)
METHOD    exhaustive pair orbits at n = 16 (mu_16 in F_97), sampled at
          n = 32; strip quotient strata; compute E_3 of the true
          alignment sets; classify every top-decile set
INTERPRET clean => c_xr_content grounded at the object level; the KMS
          route proceeds with confidence | an unstructured top set =>
          C_XR needs a new member BEFORE the import note is written
```

## E19 — Globalness measurement (previews the XR shortcut)

```text
TARGET    xr_globalness_from_ledger
QUESTION  do post-strip alignment sets have link densities BELOW the
          KLLM globalness threshold at every core size r?
PRIOR     ~70% yes (the tangent ledger should enforce it; never measured)
METHOD    same pair-orbit data as E18: for each alignment set, tabulate
          density on every fixed-core link (r = 1..4) vs the paid
          tangent bound and vs the KLLM threshold formula
INTERPRET below threshold everywhere => the globalness certificate is
          real; QX.11 becomes a write-up | a leak at some r => either
          an unpaid tangent leak (R2-relevant — report loudly) or the
          strip is incomplete at that scale
```

## E20 — KMS/KLLM loss-exponent tables (statement arithmetic, no compute)

```text
TARGET    xr_kms_parameter_matching
QUESTION  do the published quantitative forms (KMS Johnson, DKKMS
          Grassmann, KLLM global hypercontractivity) survive FM-scale
          measure mu ~ q^{1-t}?
PRIOR     raw KMS ~25%; KLLM route ~65%
METHOD    literature statement extraction ONLY: tabulate each theorem's
          loss exponents; per rate, compare against the available FM
          gap; no experiments
INTERPRET KLLM survives => the import (QX.12) proceeds | both fail =>
          the XR wall needs a strengthened small-set theorem — named,
          honest, and known before anyone writes bridge notes
```

## E21 — Circuit census growth (calibrates the syzygy branch)

```text
TARGET    spread_syzygy_circuit_bound / circuit_locus_density
QUESTION  how does the minimal-circuit count grow in n (E13: 71 at
          n = 32, first 16 blocks)?
PRIOR     q-suppressed poly growth (~75%) per the determinantal-locus
          prediction
METHOD    extend the E13 census across n = 16..64, full block ranges,
          two field sizes (to see the q-dependence directly);
          also settle the flagged caveat: do the two identities
          involve (u,v) or locator data only
INTERPRET growth matches deg/q^c => QS.4's density argument is
          calibrated | faster growth => the locus argument misses
          circuit families — the branch needs its own taxonomy
```

## E22 — Challenger-class census (completes the E15 repair)

```text
TARGET    worst_word_planted (revised) / list_planted_arithmetic
QUESTION  does planted + the E15 structured challenger class EXHAUST
          the extremal words, and what is the challenger's exact count
          formula?
PRIOR     ~70% two classes suffice
METHOD    extend the E15 search at sigma = 1..3, n = 16..64: enumerate
          all words beating 0.9 x planted list; classify against the
          two known classes; extract the challenger count formula
INTERPRET two classes exhaust => QL.5's two-column arithmetic closes
          the repair | a THIRD class => iterate the E15 protocol
          (enlarge, price, re-census) — the endgame absorbs it
```

## E23 — The A=425 unsafe side (the strongest unclaimed item, now with compute)

```text
TARGET    second_pin_a426
QUESTION  is LD_sw(RS[F_p, D, 256], 425) > 87 at the #204 budget-prime
          row?
PRIOR     ~85% yes (the staircase steps by q-factors; 425 sits one
          step below a count that EQUALS B*)
METHOD    exact computation in the #204 framework one grid step down:
          the two-core structural numerator at A = 425, specialized to
          the budget prime; if exact evaluation is heavy, a certified
          witness family (qfloor at the active scale) suffices for >
INTERPRET > 87 => THE SECOND PIN IS COMPLETE — a window-edge
          threshold-pinned row, the strongest partial of the program;
          <= 87 => the crossing sits deeper: relocate the budget prime
          per the staircase table and re-run (the framework makes this
          a parameter change, not new mathematics)
```
