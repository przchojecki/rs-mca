# Overnight orders — 2026-07-03 (for Codex / any lane)

- **Status:** AUDIT / work orders. Two campaigns: (A) the 26 fresh PROVABLE
  nodes on proof paths to either grand target (computed, deduped against
  the 8 already in flight in #180-#192); (B) evidence wave 2 (E9-E16 +
  the A0 audit), each pre-registered.
- **Protocol:** one item per PR; verify-first; cite the DAG node id +
  order number; negative results publish identically; honest statuses.
- **DO-NOT list (provably doomed as of tonight — do not spend compute):**
  no N'=64 birthday run (graded_collision_radius decides that cell — a
  theorem, not a question); no pure-height fullness attempts at N' >= 128
  (height_only_impossibility); no naive single-step spectral/EML bounds
  (xr_anticode_toolkit scoping + #191's tight constant); no E8 mixed-radix
  work unless the rules freeze lands broader than 2-power.

## A0 — THE GATE (run first; biggest payoff per hour)

```text
A0 [f_consumer_scoped audit / QF.9] (S)  Audit r2's fiber argument and
   imgfib's plane sections: does every F-consumption lie in (a)
   coordinate-slice/fiber flats or (b) Hankel-pencil kernel flats?
   YES => general F demotes; QF.10 opens (fiber-side F via shortened-RS
   MDS duality + moments — potentially an unconditional proof);
   NO => name the escaping consumer; general F stays critical.
```

## Campaign A — the 26 fresh PROVABLE nodes (grouped; sizes S/M)

```text
A1 endgame arithmetic (highest leverage, mostly S):
   crossing_localization, staircase_steepness, census_bounded_scales,
   census_exact_counts, census_window_arithmetic,
   list_crossing_localization, list_planted_arithmetic
A2 the F ladder:
   f_concurrency_equiv, f_dim2_skeleton (MUST include the twin-count
   check on E7's existing j=5 kernel artifact — see E10),
   f_dual_distance_frame, f_spread_moment_count, f_sparse_descent_step
A3 certification stack:
   graded_collision_radius, cluster_certificates, are_sharp_constant
A4 XR foundations:
   xr_e3_calculus (respect #184's strip-first caveat), xr_anticode_toolkit,
   averaged_xr
A5 Paid(A) closure bundle (one PR, = queue Q1.2):
   paid_tan_fn + paid_quot_fn (INTERVAL cells) + paid_ext_fn
   (regression: tangent term reproduces 506/507)
A6 remaining:
   dyadic_profile_evaluation, spi_genericity, petal_fixed_excess,
   pma_aux_list_reduction, pma_johnson_regime (GS import: add the
   bridge-ledger row), staircase/census verifiers cross-checked against
   E1's exact class counts
```

## Campaign B — evidence wave 2 (pre-registered; one PR each)

```text
E9  [f_many_sparse_structure census / QF.8] (M)  Exhaustive n = 16,
    dims 2-3: enumerate flats by sparse-dual-word count; classify
    many-sparse flats vs pullback/tangent.
    INTERPRET: all classified => conjecture grounded, decompose along
    observed cases | third structural class => ledger + restate (E3
    pattern) | unstructured many-sparse flat => the F-induction residue
    is FALSE as stated — report immediately, halt QF.5.

E10 [dim-2 skeleton predictions / E7b] (M)  (i) Count twin pairs in
    E7's recorded j=5 top kernel planes. PREDICTION: >= 1 twin in any
    plane exceeding C(n,2)/C(j,2) = 12. (ii) j = 4 Grassmannian census
    at n = 16 vs the pair-bound envelope.
    INTERPRET: twins found => skeleton validated + kernel planes are
    twin-rich (structural note) | NO twins => f_dim2_skeleton has an
    ERROR — halt QF.4, report the offending plane | j=4 max vs
    envelope => calibrates f_pair_bound_envelope (breach = leap
    falsified, exactly what E7's next step was for).

E11 [stripped toy inverse / E2b] (M)  Per #184's caveat: strip paid
    quotient strata FIRST, then enumerate top-E_3 pairs at n = 16/32.
    Expected post-strip content: tangent-structured only (consistent
    with #191's k=1 dictator extremals).
    INTERPRET: all structured => XR prior UP strongly, build xr_gvn
    chain next | unstructured survivor with unpaid mass => C_XR
    content revision BEFORE anyone builds the Cauchy-Schwarz chain
    (cheapest possible time to learn it).

E12 [generator-economy design search / QA.15] (M-L)  Lift the
    root-difference germ (diffs = unit x (zeta^k - 1), g = N') from
    single roots to l'-sums at N' = 16/32; measure achievable
    all-pairs-certified family size |F| vs generator count g.
    INTERPRET: |F| ~ K/poly reachable => certification viable,
    knife-edge windows shrink parametrically | early cap => document
    the obstruction pattern; refocus on p-specific alternatives.
    GUARD: no fiber counts in existence arguments (circularity).

E13 [spread exception census / QS.1] (M)  ALL below-cap exceptions at
    n = 16..32 (extend #185's targeted search to exhaustive): does
    every exception embed in a finite-geometry (AG/net) configuration?
    INTERPRET: yes => spread_exception_classification grounded (rung 2
    opens: classification via the cap kernel) | a non-geometric
    exception => the leap's statement revises with the new class.

E14 [integrality margin tables / QA.3 + QL.4] (S)  Evaluate the FM
    mean at every candidate crossing point (all four rates), MCA and
    list sides; verify n^3 x FM < 1 everywhere.
    INTERPRET: margins astronomical (expected ~2^-thousands) =>
    aperiodic_zero/extras-zero computational halves DONE | any
    candidate with margin near 1 => flag: integrality does not absorb
    R2's constant there — the endgame needs sharper input at that point.

E15 [worst-word challenge / QL.2] (M)  Adversarial search at n = 16..64
    for word families beating the planted sunflower list at matched
    radius (structured challengers: multi-core, mixed-defect, folded).
    INTERPRET: nothing beats planted => worst_word_planted grounded |
    a beating family => classify it with the sunflower machinery; if
    it resists classification, the list endgame's leap revises.

E16 [petal growth table / Q2.9] (M)  Fixed-excess petal counts vs
    d - ell = c for c <= 6 on toy rows (CRT compression makes each
    finite).
    INTERPRET: flat/poly growth => imgfib prior up + selects between
    correlated-GS and descent for pma_wide_residual (the M-scaling
    exponent decides which) | growth in c => escalate R3 immediately.
```

## Priorities if time-limited

A0 first (one hour, gates the largest prize). Then interleave: E10
(tests tonight's skeleton against existing data — no new compute),
E9 (gates the F residue), A1 (endgame arithmetic — turns both
endgames into numbers), E11 (XR fork decider), A5 (unblocks the M4
table). Everything else as capacity allows. The roadmap lane will
process all completed packets into the DAG in the morning pass.
