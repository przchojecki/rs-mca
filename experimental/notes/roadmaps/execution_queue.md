# Execution queue — hand-off items derived from the prize DAG

> **MORNING STATE 2026-07-03:** ~20 of the 26 fresh PROVABLE nodes and all
> wave-1/2 evidence tasks are IN FLIGHT across PRs #180-#206 — check open
> PRs before claiming anything below. Newly available and NOT yet claimed:
> the unsafe side of the A=426 second pin (second_pin_a426 — the strongest
> partial on the board), QF.10 scoped-F proofs for the two audited
> families, the E12 pivot (multiplicative template compression /
> difference-set imports), and the QF.5 induction assembly now that E9
> fixed the case list.

- **Status:** AUDIT / work queue. Derived mechanically from
  `experimental/data/prize-dag/prize_dag.json` (149 nodes @ this writing):
  the RIPE list (requirements met), the PROVABLE tier (routes pinned), the
  ready TEST nodes, and the named hard targets. Regenerate the source lists
  with `verify_prize_dag.py` as statuses flip.
- **Who this is for:** any agent/lane picking up tractable work. Each item
  is self-contained: what to do, inputs, acceptance test, size
  (S = a session, M = a few sessions, L = open-ended), and which DAG node
  flips on completion.
- **Claiming protocol:** one item (or one listed bundle) per PR (standing
  order 6); verify-first (the acceptance test must pass before commit);
  agents-log entry; CITE THE DAG NODE ID in the PR body so the map gets
  updated on integration. Honest labels; nothing here authorizes promoting
  SKETCH/CONJECTURE content.

## Tier 0 — lookups and gates (minutes to hours each)

```text
Q0.1 [field_cap_check] (S)  Read ePrint 2026/680; confirm or refute the
     working constants k <= 2^40 and |F| < 2^256 (absent from the live
     prize page). Acceptance: quotes + section refs recorded in the
     wp0_2-format freeze table. Flips: field_cap_check; unblocks exact
     B* statements in every dossier table.
Q0.2 [rules_freeze] (S)  Build prize_rules_freeze.md + the SHA-256 drift
     detector per wp_detail/wp0_2 §2. Acceptance: verifier green; all
     quote hashes pinned. Flips: rules_freeze; hardens S0 axes 8/9.
Q0.3 [replay_170_171] (M)  Execute the wp0_3 six-step replay protocol on
     PRs #170/#171 (pin SHAs; independent re-derivation of Phi and the
     rank-6 example — diff against the s3b_iii_2 factorization).
     Acceptance: divergence tables published. Flips: replay_170_171;
     UNBLOCKS alpha_front and beta_front scans; upgrades #173-adjacent
     statuses when its turn comes.
```

## Tier 1 — RIPE builds (all prerequisites proved; engineering + write-up)

```text
Q1.1 [bridge_ledger] (S)  Write experimental/notes/audits/bridge_ledger.md
     per wp5_2_wp6_2_wp6_3 §3 (rows already enumerated there) + the
     keyword checker. Acceptance: checker fails a doc using an unlisted
     bridge; passes current notes. Flips: bridge_ledger.
Q1.2 [paid_tan_fn + paid_quot_fn + paid_ext_fn -> paid_closure] (M, one
     bundle)  Implement Paid(A) per s2 §5: staircase formula; quotient
     zones with INTERVAL cells (point values stay conditional — print
     them as intervals, never numbers); the s6 extension import rule
     (0 if generating). Acceptance: deterministic regeneration; WP-0.4
     checker H2/H5 logic green on the emitted table for the pinned row
     (regression: tangent term reproduces 506/507). Flips: 4 nodes; the
     M4 table generator (wp2_4) becomes a formatting exercise.
Q1.3 [window_m5_charts] (M)  Per-point cleanup of the M3 window using the
     integrated lemma kit (m1_packet_transport, m1_rank_defect_nf): at
     each rank-drop Z of each bucket, decide kernel-contains-valid-
     locator; emit the per-A bucket log (wp2_5 §1). Acceptance: zero
     'unknown' leaves 385 <= A <= 426 OR named residuals with minimal
     reproductions. Flips: window_m5_charts; tests window_pred_aper0.
Q1.4 [dossier_partial] (M; do LAST in this tier)  Assemble v-PARTIAL per
     wp7_2_wp7_3_wp7_4 §3 from wp1_1's note spec + Q1.1/Q1.2 outputs +
     lean_tier1 (Q2.6). Acceptance: build script refuses if any gate
     fails; S0 conditioning language per wp1_1 §4. Flips: dossier_partial
     — the program's first submission-shaped artifact.
```

## Tier 2 — PROVABLE write-ups (routes pinned in the notes; execute them)

One-page lemma notes (S each):

```text
Q2.1 [fm1]  Write the exact-first-moment lemma (surjectivity + linearity;
     route in s2 §2) + commit the toy verifier (numbers already exactly
     verified: 0.017333 = 0.017333). Flips fm1 -> PROVED.
Q2.2 [gap2_seam]  The pullback => M | t_denom derivation (s4 §3) as a
     lemma note. Flips gap2_seam.
Q2.3 [spi_genericity]  Post-strip stratum carries no subgroup symmetry
     (from the PROVED strata combinatorics, s3b_ii §4). Flips
     spi_genericity.
Q2.4 [ext_import]  The N(L) crossing arithmetic + B-rational linearity
     argument (s6 §1-2) as a note + verifier. Flips ext_import.
```

Verifier-backed builds (S-M each):

```text
Q2.5 [displacement_uniform]  The three-field verifier ((F_13, mu_4),
     (F_17, mu_16), (F_49, mu_16)) deriving the #170 identities FROM the
     V^T D V factorization, with printed nonvanishing hypotheses
     (wp2_5_wp4_1 §2). Independent of mega-PR integration. Flips
     displacement_uniform; strengthens xr_wall's foundations.
Q2.6 [lean_tier1]  The gate addition certificates (witnesses computed and
     verified in wp1_1_wp1_2 §2), staircase arithmetic, endpoint Rat
     facts; lake build green, zero sorry, CERTIFICATION_MAP.md. Flips
     lean_tier1.
```

The deficiency-1 ladder (M as a bundle; = RESUME PR #172, task #13's
parked resume point; each rung is one loop turn per wp2_6):

```text
Q2.7 [u1_cramer, u2_nondegeneracy, u3_divisibility, u4_pseudoremainder,
      u5_dichotomy, acid_test, spi_dim1]  Execute rungs U1-U5 on the toy
     row, run the EXHAUSTIVE acid test (1820 supports x 97 slopes brute
     force == chart prediction), then the declared F_17^32 family packet.
     Acceptance per rung in wp2_6. Flips 7 nodes and tests prediction P3
     — the base case of the SPI mechanism.
```

Medium mathematics (M each; more thought, still route-pinned):

```text
Q2.8 [averaged_xr]  The Johnson-scheme second-moment computation (s3b_iii_2
     §5): variance of |A_{u,v}| over pairs, graded by intersection size,
     using the exact gap lam0 - lam1 = n. Acceptance: a toy-verified
     moment formula + the averaged-XR statement. Flips averaged_xr;
     upgrades the FM model to almost-all-pairs.
Q2.9 [petal_fixed_excess]  Enumerate/bound full-petal extras at fixed
     d-ell <= 3 on toy rows (CRT compression, L1 Lemmas 7/8, makes this
     finite). Acceptance: exact counts + a growth table vs d-ell.
     Flips petal_fixed_excess; first data on the petal escape route.
```

## Tier 3 — experiments ready to run

```text
Q3.1 [row_c_experiment] (M)  Build the Row-C birthday-sampling harness
     (wp3_1 §1: n = 2^10, log2 q ~ 250; e_1 value-set density at
     N' = 64..256; ~sqrt(V) samples; pinned seeds; confidence intervals).
     THE highest-information experiment on the board: it measures the
     zone-(b)/e1_fullness question that decides the corridor.
Q3.2 [alpha_front / beta_front] (M; blocked on Q0.3)  The full-grid alpha
     scan and the rank-6 Hankel-realizability search, on REPLAYED
     definitions, with P1a/b/c and P-beta outcome classification (s3a).
```

## Tier 4 — named hard targets (for strong sessions; standing order 8 applies)

```text
Q4.1 [exchange_ledger_gen_t]   generalize the #152 one-exchange residual
                               ledger past t = 2 (feeds xr_expansion;
                               small-t version targets the stripped A=265)
Q4.2 [acl_second_order]        explicit second-order term for Acl (makes
                               the S2 bracket's quotient end a number)
Q4.3 [norm_threshold_ext]      extend qfloor exactness past N' ~ 80
                               (each step narrows zone-(b) from the left)
Q4.4 [a_regularity_forcing]    force a-regularity or bound the irregular
                               stratum (REQUIRED for m >= 4 for-all lists)
Q4.5 [petal_mixed_amplification] the mixed-petal theorem (with Q2.9's
                               data as the guide)
Q4.6 [beta2_primitivity_trace] compute ONE integer, Tr(gamma|V) at z = -2,
                               by any route not yet foreclosed (the
                               elementary Lefschetz route is proven dead —
                               do not re-walk it; see beta2_dead_routes)
Q4.7 [xr_crystallization = spi_exceptional_class]  the shared core:
                               dense alignment => paid structure. The one
                               genuinely new idea the program needs;
                               odd-moment inputs (Q4.1, Hooley-Katz) are
                               the cheapest rigid information.
```

## Addendum — items from DAG depth passes 5-6 (2026-07-02)

```text
Q2.10 [stratification_partition_thm] (S)  Write the T0-T7 partition theorem
      (totality + first-match disjointness; true by construction) + the
      fuzz acceptance from wp2_3 §4. Load-bearing: the final theorem sums
      over these strata. Flips stratification_partition_thm; makes
      strat_tree's ripeness formal.
Q2.11 [dyadic_profile_evaluation] (S-M)  Compute Q_H(eta) exactly for
      2-power domains at the four official rates (pure divisor counting;
      verifier + note). Without it conj:B's profile hypothesis is
      unverifiable on official rows. Flips dyadic_profile_evaluation.
Q2.12 [averaged_slope_conversion] (M)  Second moment + paid-fiber
      exclusion => a many-SLOPE pair exists whenever the FM locator mean
      crosses B* (route: s2 fork F2). This is the unsafe side's needed
      tool in the COLLIDED branch of zone-(b). Flips
      averaged_slope_conversion; with e1_fullness it makes
      unsafe_at_crossing's any-gate exhaustive.
Q4.8  [amplification_range_ext] (L)  Extend the split-prime transfer
      (finite collisions = char-0 collisions) from p > exp(Cn log n/sigma)
      toward prize-scale p ~ 2^256. The proved foundation (thm:upstairs +
      Galois amplification) is fully in place — RIPE in the well-posed
      sense. Every range improvement is direct corridor progress.
NOTE  Q1.1 (bridge ledger) gains a MANDATORY row: the proved LD_sw vs
      ABF/GG separation (forward-only import; see ldsw_ld_separation).
```

## Addendum — the Conjecture-F skeleton and the norm criterion (2026-07-02)

```text
Q2.13 [f_gcd_reduction] (S)  Prove the WLOG reduction: dividing a plane's
      D_j-points by their gcd is a linear injection into a smaller
      instance with trivial image gcd (multiples-of-ell_W form a
      subspace). One page + a toy verifier. Flips f_gcd_reduction; makes
      the tangent branch of Conjecture F a reduction, not a case.
Q2.14 [f_scale_recursion] (S)  Prove the pullback embedding: an
      M-pullback places g's coefficients at multiples of M, so plane
      sections of the periodic stratum ARE plane sections at scale n/M.
      One page + toy check. Flips f_scale_recursion; with Q2.13 the full
      Conjecture F reduces to its primitive core (f_primitive_case).
Q2.15 [collision_norm_criterion] (S-M)  Isolate prop:qfloor's mechanism
      as a standalone statement: non-quotient e1-collisions mod p occur
      iff p divides an explicit nonzero cyclotomic norm of height
      <= (2l')^{N'/2}. Note + verifier over small N'. Flips
      collision_norm_criterion; zone-(b) becomes concrete algebraic
      number theory (count prime divisors of a bounded family).
```

## Addendum — falsifier tests (precision pass, 2026-07-02)

```text
Q3.3 [gap1_toy_test] (S)  Enumerate non-equivariant (multi-isotypic)
      periodic alignments on toy rows (F_13, F_97): count aligned pairs
      whose locator root set is K_M-stable but whose word data is not
      zeta-equivariant. Falsifies gap1_noneq_mass if the mass outgrows
      poly; grounds it otherwise. Ev-wired to the critical GAP-1 node.
Q3.4 [a_regularity_test] (S)  Measure a-regularity frequency and the
      irregular stratum's contribution on random toy interleaved
      configurations. Informs whether forcing (Q4.4) or an
      irregular-stratum bound is the right attack; note the m-quantifier
      lookup (Q0.1/rules_m_reading) may obviate the whole question for
      bounded m.
```

## Tier R — red-team attacks (see redteam_attack_plan.md for full specs)

```text
QR.1 [redteam_multiscale] (M)  The headline attack: multi-scale resonance
     constructions at n = 2^10..2^12 vs payment_completeness — the
     hypothesis whose class has already failed three times in this
     project's history. Hit = COUNTEREXAMPLE contribution (S9 protocol);
     sustained miss = the first evidence in the actual hiding room.
QR.2-QR.7  the per-conjecture attacks (gap-1 pumping, petal pushing,
     collision conspiracies, spread designs, plane census, irregularity
     maximizers) — each a verifier-backed search, each cheap relative to
     what it de-risks. Attack statements, not lanes; a hit is a
     contribution, not a failure.
```

## Tier E — enumeration-route stages (see enumeration_routes.md)

```text
QE.1 [xr_gvn] (M, RIPE)   iterated exchange energies + the Cauchy-Schwarz
                          chain; k=2 exists (averaged_xr), extend to k=3
QE.2 [spi_component_control] (M)  effective Bezout component/degree bounds
QE.3 [es_regularity] (S)  feasibility memo: bounded-complexity encoding of
                          alignment (V^T D V shape) — yes/no before investing
QE.4 [monodromy_realization] (M)  scoping note: the sheaf family for the
                          general count (gap between BETA_2's instance and
                          the general problem; expert-consultable)
```

## Tier P — the mixed-petal subDAG (hard-problem decomposition #1, 2026-07-02)

The single point of failure (petal_mixed_amplification, R4) decomposed:
the amplification count IS list decoding one level down.

```text
QP.1 [pma_aux_list_reduction] (S)  Write the reduction: extras inject
     into the RS list of the auxiliary pieced word U* = c_i L_D on T_i
     at degree d, agreement N = d+1+sigma-|R_P| (elementary from the
     PROVED core-defect lemma; D-choice entropy charged to the reserve).
     Acceptance: note + toy verifier checking the injection on the
     d-ell = 2, 5 witnesses.
QP.2 [pma_johnson_regime] (S)  The few-petal regime M below
     ~(d+sigma)^2/(d(sigma+1)) is CLASSICAL: cite Guruswami-Sudan on the
     auxiliary word (forward import; add the bridge-ledger row).
     Acceptance: the threshold formula verified on toys; GS list bound
     instantiated with explicit constants.
QP.3 [pma_wide_residual] (M-L)  The genuinely open residue: many-petal,
     sub-Johnson, CORRELATED targets (all c_i L_D share one L_D). Two
     independent angles queued as separate attempts: (a) one-dimensional-
     target strengthening of GS; (b) descent — the auxiliary extras are
     the SAME problem at strictly smaller degree; iterate to Johnson-safe
     territory. Q2.9 data first.
```

## Tier F/X/Z — hard-problem decompositions #2-#4 (2026-07-02)

Conjecture F's primitive core:

```text
QF.1 [f_dim1] (S)  Write the VOTING argument: gcd-trivial pencils meet
     D_j in <= n/j points (each x in H votes for one parameter; members
     need j votes). Toy verifier at n = 16. The base case of the map's
     one unavoidable conjecture, true with room to spare.
QF.2 [f_concurrency_equiv] (S)  Write the exact reformulation: F-primitive
     = j-fold concurrency bound for the evaluation-hyperplane arrangement.
     Deliverable includes a literature scan: multiplicity point-hyperplane
     incidences / Furstenberg-type sets over F_q — the dim >= 2 attack
     inherits an existing field.
```

XR inverse, k = 3 entry:

```text
QX.1 [xr_e3_calculus] (M)  Define E_3 (odd-order exchange energy;
     E_2 = averaged_xr), prove the structured lower-bound direction
     (folded + tangent pairs are E_3-large). The EASY half of the
     inverse theorem, delegable now.
QX.2 [xr_inverse_toy] (M)  Exhaustive toy inverse at n = 16/32: every
     E_3-large pair is structured. Falsifier + C_XR content preview.
```

Zone-(b) range extension, staged:

```text
QZ.1 [are_sharp_constant] (S-M)  Recompute the transfer height bound
     with explicit constants; determine the true exponent shape.
QZ.2 [are_exceptional_density] (M)  The almost-all-primes partial:
     Sum_p collisions <= pairs x log(height) => in any dyadic range all
     but poly-many primes are collision-light. Dossier-grade partial.
QZ.3 [are_subfield_amp] (M-L)  Classify collision classes admitting
     subfield norm descent; each class extends its transfer range.
```

Monodromy realization, scoping (no DAG nodes — deliverables are memos):

```text
QM.1 (S)  Inventory Katz-toolbox trace-function realizations matching
     the alignment sum's shape (literature + repo scan; collectible by
     any lane).
QM.2 (M)  Gap analysis: what made BETA_2's slack-line instance
     realizable (one-parameter family) vs the general pair problem
     (multi-parameter) — does a fibration exist? Expert-consultable memo.
```

## Tier L — evidence-grounded leap paths (2026-07-02 evening)

Three calculated leaps laid down after the E-campaign's first wave; each
cites its evidence, carries a falsifier, and decomposes into rungs:

```text
QS.1 [spread_exception_classification rung 1] (M)  Exhaustive exception
     census at n = 16..32: extend E3's search to ALL below-cap
     configurations; test whether every exception embeds in a
     finite-geometry (AG/net) family. Outcome feeds rung 2
     (classification via the proved row-space cap kernels).
QG.1 [gap1_product_model rung 1] (M)  Extend the E6 base-line rank
     lemma from alpha^M-in-base-field to intermediate fields (tower
     recursion — the pattern's fourth appearance). With it, the
     per-character product model closes GAP-1 at the fitted constant.
QF.3 [f_pair_bound_envelope rung 1-2] (M)  Adopt the E7 packet's
     PairBound definition; attempt the dim-2 proof: pencil
     decomposition through the top concurrency point + the proved n/j
     voting bound; the weighting must absorb pencil overlap. The j=4
     Grassmannian refinement doubles as this leap's falsifier run.
```

## Tier A — the adjacency endgame (decomposed 2026-07-02 evening)

The proved-results survey insight: every precision result in the repo is
EXACTNESS-ON-A-STRATUM, and B_C is an integer staircase with ~q-factor
steps — so the endgame is <= 3 pointwise decisions per rate, with
integrality converting any-poly bounds into exact zeros.

```text
QA.1 [crossing_localization] (S)  The staircase note: monotone integer
     B_C => unique adjacent crossing exists unconditionally; extract
     the per-rate candidate lists from the corridor arithmetic.
QA.2 [staircase_steepness] (S)  The q-factor step note from the exact
     count shapes; defines the knife-edge condition precisely.
QA.3 [aperiodic_zero FM table] (S-M)  Evaluate the FM mean at every
     candidate point of every official rate; verify n^3 * FM < 1
     everywhere (expected ~2^-thousands). The computational half of
     aperiodic_zero_at_crossing.
QA.4 [knife_edge_census] (M; after Q4.2/acl_second_order)  SYMBOLIC
     census (family unenumerable): arithmetic characterization of
     knife-edge (q, n, A) triples, with PROVED error control (the list
     is hostage to the error model). Ties exist systematically: B*
     sweeps all integers as q varies.
QA.7 [census_bounded_scales] (S)  The pinning lemma: forced ratio
     l'/N' = j/n => strictly monotone counts => ONE deciding scale in
     an ABSOLUTE window N' in [~120,~400], independent of n, k. Makes
     the census n-uniform and exact. One page + numeric check across
     rates.
QA.8 [census_exact_counts] (S)  Exact bignum K at bounded scales;
     verifier tabulating K per (rate, candidate A); retires expansions
     from tie decisions.
QA.9 [census_window_arithmetic] (M)  The window list [L, K) per
     (rate, A) + prime-counting size estimates + the dodge complement,
     parametrized by certification strength L.
QA.10 [census_dodge_selection] (S; after QA.8-9)  Verify every
     exhibited dossier row lands OUTSIDE all windows (Row C margins
     2^22 / 2^79 per E1 — expected clean). Upgrades exhibited-row
     partials to full adjacency grade with zero QA.6 dependence.
QA.5 [single_swap_injectivity] (S)  The free rung: single-swap e1
     differences have norm ~2^{N'/2} << p, hence provably NEVER
     collide at prize scale — unconditional, every admissible prime.
     One page + verifier over small N'.
QA.6 [certified_valueset_lower] (L)  The knife-edge core: compose
     pairwise height-certified distinctness into all-pairs-distinct
     families of size > B* (packing in the swap metric, or a block
     invariant). The safe side is collision-monotone (free); THIS is
     the entire hard half of every Diophantine near-tie.
```

## Tier LA — the LIST adjacency endgame (2026-07-02 late; mirror of Tier A)

The hardness swaps sides vs MCA: list unsafe witnesses are CONSTRUCTIVE
(planted families), the safe half is imgfib + integrality, and there is
NO zone-(b) analogue (planted counts are explicit formulas).

```text
QL.1 [list_crossing_localization] (S)  The list staircase note:
     monotone integer sup-list => unique adjacent crossing; candidates
     from the [H/128, H/256] window arithmetic.
QL.2 [worst_word_planted toy probe] (M)  Adversarial search at
     n = 16..64 for word families beating the planted list at matched
     radius. The list endgame's ONE leap — this is its falsifier run
     (pre-register: challenger structure gets priced by the sunflower
     machinery either way).
QL.3 [list_planted_arithmetic] (S-M)  Exact planted-count formulas per
     (rate, m, candidate radius) + the eps*|F| Diophantine windows +
     dodge lists for exhibited rows. Transfers the census machinery
     verbatim; no per-prime content.
QL.4 [list integrality table] (S)  The extras-FM evaluation at list
     candidates (mirror of QA.3): verify n^B x expected-extras < 1 at
     every candidate radius => extras exactly 0 under imgfib.
```

## Tier F2 — the F core: dim-2 skeleton + induction (2026-07-02 late)

```text
QF.4 [f_dim2_skeleton] (S-M)  Write the two-part elementary proof:
     distinct-trace double count => C(n,2)/C(j,2); twins => gcd
     reduction (uses #182's lemma). Verifier MUST test the
     pre-registered prediction on E7's own artifact: the j=5 kernel
     top planes (13 > 12) contain >= 1 twin pair; count them.
     Flips f_dim2_skeleton; proves f_pair_bound_envelope at dim 2.
QF.6 [f_dual_distance_frame + f_spread_moment_count] (M, one note)
     The dual-code frame: degeneracies = low-weight words of P-perp
     (gcd = w1, twins = w2); w* > r => r-wise moments =>
     C(n,r)/C(j,r), poly to LOG dim (scope printed honestly).
     Elementary linear algebra + double counting; verifier on toy
     flats cross-checking against the E7 census.
QF.7 [f_sparse_descent_step] (S)  The closure lemma + the accounting:
     degree drops w, dimension drops <= w-1 — net depth gain per
     step. One page, uses #182's reduction.
QF.8 [f_many_sparse_structure toy census] (M)  Exhaustive n = 16,
     dims 2-3: enumerate flats by sparse-dual-word count; classify
     the many-sparse ones vs pullback/tangent. PRE-REGISTERED
     INTERPRETATION: (a) all classified => conjecture grounded, the
     coding-theory decomposition proceeds along the OBSERVED case
     list; (b) a third structural class found => it gets a ledger and
     the classification restates (S9-style, the E3 pattern); (c) an
     UNSTRUCTURED many-sparse flat => the F induction's residue is
     false as stated — major revision, better to know now. Decomposition
     of the conjecture is DEFERRED until this returns (census-first
     discipline, per the E3 lesson).
QF.5 [f_dim_induction formulation] (M)  Formulate F_r + the
     spread-vs-coincidence step precisely (how much coincidence forces
     a divisor factor); toy r = 3 census extending E7 as the
     calibration/falsifier run. The residue merges into the mapped
     fiber/petal machinery at high dimension.
```

## Tier CV — certified value-set lower bounds, decomposed (2026-07-02 night)

```text
QA.11 [graded_collision_radius] (S)  The graded theorem + the d* table
      per (N', log p) + the unconditional-fullness corollary at the
      2l' < p^{1/phi} frontier (N' <= 64 for prize p; cites the
      prop:qfloor mechanism). Verifier over small N'. NOTE the honest
      consequence: E1's N'=64 zero-collision result was FORCED — that
      cell is decided, not evidence.
QA.12 [height_only_impossibility] (S)  The scoping negative: total
      height budget 2l' => pure-height certification caps below full
      strength at N' >= 128. One page; saves doomed attempts.
QA.13 [far_pair_separation design search] (M-L)  The reshaped residue:
      generator-factored difference designs (all pairwise e1-diffs =
      small unit x one of g generators; g per-row valuation checks
      certify everything). Toy search at small N': measure achievable
      |F| vs g; import candidates from the abelian difference-set
      literature. Partial designs convert to decided window fractions
      via census_window_arithmetic — proportional value, no
      all-or-nothing.
```

## Tier CV2 — far-pair separation, decomposed (2026-07-02 night)

```text
QA.14 [cluster_certificates] (S-M)  The two lemmas + the freebie:
      diameter-d* free cliques; everywhere-big center-difference =>
      one norm check certifies all cross-pairs (state the min-conjugate
      condition explicitly); integer factors self-certified. Verifier
      on toy scales; uses QA.11's graded radius.
QA.15 [generator_economy design search] (M-L)  Multiplicative
      difference-designs: centers whose difference set lies in
      units x <g bases>_mult. Start from the proved germ (root diffs
      = unit x (zeta^k - 1), g = N'); lift to l'-sums at toy N';
      measure |F| vs g. GUARD: no fiber counts in existence proofs
      (circularity). Partial designs convert to decided window
      fractions — proportional value.
```

## Tier X2 — xr_expansion staged (2026-07-02 night)

```text
QX.3 [xr_anticode_toolkit] (S)  Delsarte/EKR anticode bounds on J(n,j)
     + the scoping negative (single-step EML near-vacuous: gap n vs
     degree n^2/4; combinatorial bounds cap at (j/n)^s — q-scale must
     be algebraic). Classical note + verifier; prevents doomed
     naive-spectral attempts.
QX.4 [xr_expansion assembly] (M; after QX.3 + Q4.1)  The three-input
     assembly (anticode radius x ledger exclusion x v8 per-locator
     cap): compute which strata get FM-scale B_ap bounds at which
     exclusion radius; state the residual strata that hand off to the
     energy pipeline. The wall's two halves meet here — the meeting
     IS the wall, now stated without pretense.
```

## Tier F3 — consumer-scoped F (2026-07-02 night; the audit gates the prize)

```text
QF.9 [f_consumer_scoped audit] (S)  Verify every F-consumption in r2's
     fiber argument and imgfib's plane sections lies within (a)
     coordinate-slice/fiber flats or (b) Hankel-pencil kernel flats.
     If YES: general F demotes to nice-to-have; the fiber side reduces
     to MDS duality (shortened RS => large dual distance => NO sparse
     dual words => moments wholesale) and the kernel side to
     displacement-kernel classification (#191's identities). The
     criticality rewiring happens only after this audit passes.
QF.10 [fiber-side scoped proof attempt] (M; after QF.9)  The (a)
     branch: Singleton bound for shortened-RS duals + the r-wise
     moment count at r ~ log n. Potentially a complete unconditional
     proof of the fiber-side F instance.
```

## Tier D — deferred decompositions, unlocked by wave-2 evidence (2026-07-03 am)

```text
QF.11 [f_descent_termination] (M)  Branch-count bounds for the descent
      tree from E9's observed sparse-word multiplicities; toy check:
      no flat at n = 16..32 branches super-poly.
QX.5  [c_xr_content falsifier] (M)  The full pair-orbit scanner (E11's
      named next step): stripped top-E_3 orbits vs the fixed-core/
      fixed-hole class. Grounded-conjecture kill-or-confirm.
QS.2  [spread_syzygy_circuit_bound] (M)  Count/classify minimal
      full-support circuits per (n,j) from the proved circuit lemma;
      price their slope contribution. The exception taxonomy's last
      observed branch.
QL.5  [challenger-class arithmetic] (M)  Price the E15 structured
      challenger class alongside planted counts in
      list_planted_arithmetic; re-derive the list windows with both
      columns. The endgame absorbs its first falsification.
```

## Tier D2 — descent termination, decomposed (2026-07-03 am)

```text
QF.12 [f_support_lattice] (S)  The accounting identity: tree nodes =
      closed sets of the sparse-support lattice; chains bounded by
      dim + degree drop. Defuses the naive 2^depth objection.
QF.13 [f_termination_mds] (S)  One-paragraph corollary: MDS duals have
      no sparse words => trivial lattice => immediate moment count.
QF.14 [f_termination_hankel] (M)  EVIDENCE FIRST: E9-style census
      restricted to Hankel-kernel flats — record support patterns
      (predicted: coset unions, per E7's kernel twins). Then the
      lattice bound via #191's displacement identities.
```

## Tier D3 — c_xr_content via the KMS engine (2026-07-03 am)

The XR inverse's hard direction = a celebrated proved theorem plus
bridges: non-expanding Johnson-graph sets correlate with juntas
(Khot-Minzer-Safra, the 2-to-2 games engine).

```text
QX.6 [xr_e3_to_expansion] (S)   E_3 = cubed restricted-operator form;
      large energy => small expansion. Elementary spectral note.
QX.7 [xr_kms_import] (M)        The import note: KMS/DKKMS statement,
      conventions matched to the exchange graph, bridge-ledger row.
QX.8 [xr_junta_to_paid] (S)     Juntas = fixed-core cells = tangent
      structures; correlation transfer; #191's dictators as base case.
QX.9 [xr_kms_parameter_matching] (S first step)  The loss-exponent
      tables vs the FM gap per rate; KLLM global hypercontractivity
      as the small-set fallback. THE residue — everything else in
      this tier is bookkeeping around a proved engine.
```

## Tier D4 — parameter matching via the globalness shortcut (2026-07-03)

The identification: KMS's junta obstruction = our tangent stratum; the
PROVED payment ledger is the globalness certificate KLLM needs.

```text
QX.10 [engine comparison + loss tables] (S-M)  Tabulate the exact
      quantitative statements of KMS (Johnson), DKKMS (Grassmann), and
      KLLM global hypercontractivity; per rate, compare loss exponents
      against the available FM gap. The cheap first look that decides
      whether raw constants ever suffice.
QX.11 [xr_globalness_from_ledger] (M)  The real math: convert the
      ledger's per-cell tangent caps into link-density bounds at each
      core size r; verify they sit below KLLM's globalness threshold.
      Falsifier: an unpaid tangent leak at some core size.
QX.12 [xr_small_set_engine import] (M)  The KLLM import note:
      statement, conventions matched to J(n,j) links = fixed-core
      cells, bridge-ledger row.
```

## Tier D5 — syzygy circuits: nongeneric, suppressed, priced (2026-07-03)

```text
QS.3 [circuit census growth] (S-M)  Extend E13's count (71 at n=32,
      first 16 blocks) across n = 16..64: the empirical growth
      exponent calibrates the locus-density prediction. Evidence
      before assembly.
QS.4 [circuit_nongeneric + circuit_locus_density] (M, one note)
      Degree-count the two simultaneous identities => generic kernel
      zero => explicit determinantal locus; Schwartz-Zippel => q-power
      suppression. SETTLE the flagged caveat first: do the identities
      involve (u,v) or locator data only (read the E13 lemma).
QS.5 [circuit_pricing] (S)  The deficiency-1 reuse: minimal circuit =
      one-dimensional kernel => the #199 Cramer/eliminant dichotomy
      applies verbatim; O(1) slopes per circuit or a named paid branch.
```

## Tier D6 — the XR wall's final assembly (2026-07-03; the soft-wall push)

```text
QX.13 [xr_ledger_qpower] (S-M)  Formalize the q-factor-per-constraint
      suppression c(s,t) from the #152 residual-system ranks (t=2, s=1
      proved; parameterize the general shape).
QX.14 [xr_radius_arithmetic] (S, after QX.13's parameterization)  THE
      TABLE: per rate, ledger q-powers + anticode factors + structured
      absorption vs the FM target; solve for the required ledger reach
      s*(rate). One spreadsheet-grade computation that prices the
      entire wall: s* small => the wall is soft and exchange_ledger_
      gen_t knows exactly what to prove; s* growing with t => the
      wall is hard and we know WHERE.
QX.15 [xr_distance_dichotomy assembly note] (M; after QX.14)  The
      three-tool exhaustive split written as the wall's master
      statement, with the coverage table as its quantitative spine.
```

## Sequencing notes

STRATEGIC OVERLAY: see `strategic_recommendations.md` (computed from the
DAG) before claiming Tier-4 items — several are ROUTE-INTERNAL (pay their
tolls only if that route is chosen) and two are SUPPORT-ONLY (Graver,
Hooley-Katz-as-target). The four walls are alternatives: pick one.

Q0.x first (they gate honesty everywhere); Q1.2 before Q1.4; Q2.7 is one
resumable loop; Q3.1 is independent of everything and maximally
informative; Tier 4 items are deliberately unscheduled — they are the
targets the tractable tiers exist to feed.
