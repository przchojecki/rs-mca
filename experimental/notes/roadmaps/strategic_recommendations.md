# Strategic recommendations from the prize DAG (computed, not opined)

- **Status:** AUDIT. Every claim below is the output of
  `experimental/scripts/prize_dag_strategy.py` over the current
  `prize_dag.json` (167 nodes; 67 open). Regenerate after any status flip.
- **Semantics, honestly:** these statements are GRAPH-RELATIVE. "Not on the
  path" means *not on any currently-mapped route*; a genuinely new proof
  strategy = new edges = recompute (and the classifier will say so).
  SUPPORT-ONLY does not mean worthless — it means the item de-risks,
  informs route choice, or earns partial-award credit, while formally
  satisfying no gate of the final theorem.

## R1 — Invest: Conjecture F is unavoidable

`conj_f` is CRITICAL: required on the MCA side (under R2) and the list side
(under ImgFib) simultaneously. There is no mapped resolution of either
grand challenge that avoids it. Anything that sharpens F — the fixed-excess
petal data (Q2.9), the deficiency-1 acid test (Q2.7), Row-C — has leverage
on the whole program.

## R2 — Do NOT try to beat all the walls; pick one, use the support layer to pick

`r2_rigidity` is critical, but NO individual wall is: SPI, XR, monodromy,
and the projected-locator wall are four live alternatives under one
any-gate. Concretely:

```text
- beta2_irreducibility and beta2_primitivity_trace (the SL_8 inputs) are
  ROUTE-INTERNAL: do not invest in l-adic monodromy unless the monodromy
  route is CHOSEN. Three other routes exist.
- likewise exchange_ledger_gen_t / xr_expansion / spread_regime_bound are
  XR-internal, and spi_exceptional_class / spi_dimension_free are
  SPI-internal — pick a lane before paying its tolls.
- the alpha/beta scans, the #172 ladder, and the acid test are exactly the
  cheap experiments that reveal WHICH wall is softest. Run them BEFORE
  choosing, not after.
```

## R3 — Likely not on the shortest path (per the current map)

```text
graver_wall        SUPPORT-ONLY. The projection-to-Graver question
                   obstructed ONE historical approach; no mapped route
                   needs it. Recommendation: do not attack Graver for the
                   prize. (If someone maps a Pade-Graver route as a fifth
                   R2 alternative, this reclassifies — the classifier will
                   show it.)
hooley_katz        SUPPORT-ONLY as a target: odd moments are an INPUT to
                   crystallization arguments, not a prize obligation.
                   Prove things WITH it; do not treat it as the goal.
window campaign    window_program / window_m5_charts / alpha / beta /
+ P3 slate         second_pin_or_wall / row_slate / #172 ladder are all
+ #172 ladder      SUPPORT-ONLY for the FULL resolution — they are the
                   de-risking, route-choosing, and PARTIAL-AWARD layer
                   (the rules explicitly credit partials). Budget them as
                   intelligence and submissions, not as obligations.
```

## R4 — Single point of failure: mixed-petal amplification

The `petal_growth` any-gate has exactly ONE live alternative
(`petal_mixed_amplification`) — its sibling was refuted. Until a second
route to petal growth exists, the amplification theorem is de facto
critical for the list challenge. Two rational responses, both cheap
relative to the risk: (i) prioritize Q2.9's fixed-excess data to ground
the amplification attempt; (ii) actively look for a second route to
`petal_growth` and map it — adding an edge is the cheapest insurance in
the whole program.

## R5 — zone-(b) is critical, but its resolution is a four-way choice

`zone_b` itself is unavoidable (the unsafe side needs the location), yet
all four listed resolutions (Acl second-order, norm-threshold extension,
perfiber directly, e1-fullness via amplification-range extension) are
alternatives. The cheapest next action is not a proof at all: the Row-C
measurement (Q3.1) tells you which end of the corridor is real before
anyone spends months on the wrong extension.

## R6 — Two rules lookups gate more than they appear to

`field_cap_check` and `rules_freeze` are CRITICAL (S0), and the tower case
`f1_case_tower` is critical ONLY IF the official family admits
non-generating rows — which the ePrint lookup decides. A one-hour reading
task can delete a critical node. Do Q0.1/Q0.2 first; everything else
inherits their answers.

## The computed classes (summary; regenerate for the live version)

```text
open: 67 | critical: 33 | route-choice/internal: 19 | support-only: 15
critical leaves (math):  conj_f, r2_rigidity, zone_b, imgfib,
                         petal_growth (+ its only live alt),
                         gap1_noneq_mass, f1_classification (+ tower case,
                         family-conditional), a_regularity_forcing,
                         unsafe_at_crossing, S0 axes 1/2/4 + rules gates
critical (packaging):    strat_tree, m4_table, paid_closure, descriptor,
                         compiler, harness, bridge_ledger, dossier_partial
route-internal clusters: monodromy inputs; XR internals; SPI internals;
                         zone-(b) route options; exp-sum import
support-only:            the window/slate/ladder/experiment layer +
                         graver_wall + hooley_katz
```
