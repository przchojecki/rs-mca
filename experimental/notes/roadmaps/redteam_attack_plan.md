# Red-team attack plan — how to try to BREAK the load-bearing conjectures

- **Status:** AUDIT / adversarial work queue. Companion to
  `strategic_recommendations.md` and the prize DAG.
- **Philosophy:** the repo's history contains three taxonomy failures
  (no-slack, one-scale entropy, raw fibers) — each discovered by
  construction, each fixed by adding a ledger. A red-team SUCCESS here is
  therefore a first-class contribution (COUNTEREXAMPLE status, S9 trigger:
  add the ledger, reissue statements, re-run the map), not a failure.
  A sustained, structured red-team FAILURE is evidence of a kind our
  passive tests cannot produce, because it searches the adversarial
  regime directly. Either outcome moves the program.
- **Rules of engagement:** attacks target STATEMENTS, not lanes; every
  attack is a verifier-backed search with pinned seeds and printed search
  space (no-silent-caps); a hit is reported with a minimal reproduction
  per standing order 8.

## The attacks, ranked by expected information

```text
R1 [payment_completeness] — MULTI-SCALE RESONANCE (the headline attack)
   Target: the exhaustiveness of tangent/quotient/extension.
   Attack: at n = 2^10..2^12 (8-10 nested dyadic scales — structure with
   no toy analogue), CONSTRUCT pairs with simultaneous structure at many
   quotient scales: e.g. words assembled from isotypic components across
   several K_M simultaneously, phase-locked so per-scale ledgers each see
   sub-threshold mass. Measure unpaid alignment vs the FM baseline.
   Hit = fifth mechanism. Sustained miss = first evidence in the hiding
   room. DAG: redteam_multiscale (ev -> payment_completeness, gap1).

R2 [gap1_noneq_mass] — PUMP THE KNOWN CRACK
   Target: non-equivariant periodic mass <= poly.
   Attack: the isotypic escape witnesses exist (isolated); try to AMPLIFY
   them — families of multi-isotypic words on stable supports with
   coordinated escapes across cosets. Extends Q3.3 from measurement to
   construction. Hit = GAP-1 ledger needed (strip pricing incomplete).

R3 [petal_mixed_amplification / imgfib] — PUSH THE POPULATED BRANCH
   Target: poly amplification of the sunflower escape.
   Attack: extend the d-ell = 2, 5 witnesses systematically — search for
   amplifying FAMILIES (not single extras) in the shifted-target
   incidence form (W - c_i L_D on T_i): adversarially choose petals/
   scalars to maximize the count. The note's own dichotomy says a hit
   must be quotient/low-defect/structured — verify the hit's structure;
   an UNSTRUCTURED hit falsifies imgfib as stated.

R4 [e1_fullness / zone_b] — COLLISION CONSPIRACIES
   Target: (1-o(1))-fullness of e1 value sets below saturation.
   Attack: hunt primes dividing MANY of the bounded-height norms
   N(e1(B) - e1(B')) (the collision_norm_criterion family): smooth/
   friable-norm searches, resonant subset pairs, CRT-aligned prime
   hunting. A conspiracy prime = heavy collisions = the corridor's
   quotient end weakens. Complements Row-C (which samples random
   behavior; this searches adversarial behavior).

R5 [spread_regime_bound / r2_rigidity] — SPREAD-ALIGNED CONSTRUCTIONS
   Target: all-small-intersections configurations have poly slopes.
   Attack: directly construct pairs with many aligned locators whose
   supports pairwise intersect in < k points: combinatorial designs
   (packings/Steiner-like systems) as co-support families + solve for
   (u,v) satisfying the alignment linear systems. The two_slope lemma
   forces structure for LARGE intersections; designs live exactly in
   the complementary regime the lemma cannot reach.

R6 [f_primitive_case] — EXHAUSTIVE SMALL-PLANE CENSUS + ADVERSARIAL PLANES
   Target: gcd-trivial aperiodic plane points are poly.
   Attack: (a) exhaustive census of ALL planes of dim <= 3 at n = 16, 32
   (finite; establishes the small-scale ground truth); (b) at larger n,
   adversarially design planes through many near-divisor points
   (interpolation through chosen D_j points, then count extras).

R7 [a_regularity_forcing] — IRREGULARITY MAXIMIZERS
   Target: the irregular stratum contributes <= poly.
   Attack: construct interleaved configurations maximizing irregular
   agreement patterns; measure interleaved counts vs regularized
   predictions (extends Q3.4 from measurement to construction).
   NOTE: the rules_m_reading lookup may moot this — check Q0.1 first.
```

## What a hit changes (the S9 protocol, made concrete)

```text
1. The construction is packaged with COUNTEREXAMPLE status + minimal
   reproduction + verifier (repo standard).
2. The new mechanism gets a ledger node; payment_completeness is
   reissued with the enlarged taxonomy (its statement is versioned);
   every 'unpaid' statement re-references it (one edit point — this is
   WHY the hypothesis is now a single explicit node).
3. Paid(A) gains a column; the S2 bracket recomputes; the corridor
   moves DOWN by the new mass; the strategy layer re-runs.
4. The prize remains a determination: thresholds move, the program
   does not break. (Negative resolutions are resolutions.)
```

## Honest cost accounting

These searches are cheap relative to what they de-risk: R1/R2/R5/R6 are
sampling + linear algebra at n <= 2^12; R4 is norm arithmetic; R3/R7
extend existing toy machinery. None requires new theory to RUN — only to
interpret. The expensive scenario is not running them and meeting the
fifth mechanism inside a submitted proof.
