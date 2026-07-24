# Audit: KoalaBear pencil-census derivation direction (K3 route cut)

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The two pencil-chart constants in circulation for a rank-49-or-pencil payment of the K3 residual-geometry obligation are exactly the closure threshold solved backwards (30119370885234533 = (threshold - rank49Cap - 1)/2 and 68745081930314528 = threshold/2), so neither is census evidence; exact first-match ownership plus the two-slope pencil cap admits models with arbitrarily many pairwise-disjoint charts, so no chart census follows from the local pencil API; the one source-free ambient census (one chart per field slope) is independently derived but exceeds the threshold astronomically. Any rank-49-or-pencil payment of K3 therefore requires a new, independently derived chart census; the exact closure comparison it must feed is properRank49Cap + 1 + 2N <= threshold iff N <= 30119370885234533.
architecture: DIRECT
partition_digest: n/a (DIRECT)
atom_or_cell: DIRECT audit of the pencil-census derivation direction for the K3 residual-geometry obligation
quantifier: the derivation-direction certifications are exact integer identities; the independence theorem is universal over every natural chart bound; no received-line quantifier is asserted anywhere
projection_and_unit: normalized primitive-pencil chart keys and distinct affine bad slopes; the abstract models carry slope tokens, not Reed-Solomon slopes
claimed_bound: none; this packet pays nothing and produces no census
status: AUDIT
impact: ROUTE_CUT
falsifier: a source-bound theorem deriving either circulating chart constant from Reed-Solomon correction geometry rather than from the threshold; or a proof that duplicate-free keys, exact first-match ownership, and the two-slope cap alone bound the chart count
replay: cd experimental/lean/kb_pencil_census_route_cut && lake clean && lake build   (stdlib-only, no dependencies, clean build under 5 s; native_decide disclosed)
```

- **Date:** 2026-07-24.
- **Author:** Holm Buar.
- **Base:** `b13de81`.
- **Scope.** This is the narrow K3 audit form of a withdrawn broader packet.
  The withdrawn packet bundled a conjectural merged-residual architecture and
  Lean proposition; under the workboard stop rules those are not resubmitted,
  and nothing here proposes a closure architecture, a law, or a ledger. What
  remains is the audit content: three kernel-certified facts about where the
  circulating pencil-census numbers come from, and the exact comparison any
  genuine census must feed.

## Verdict

**OPEN GAP** on workboard item K3.

- **Smallest missing theorem:** a chart census for the post-tangent, post-Q
  normalized primitive-pencil family, derived from Reed-Solomon correction
  geometry — rank-flat incidence, correction components, or owner data — with
  no reference to `closureThreshold`, `properRank49Cap`, `B*`, or any target
  remainder. Given such an `N`, the proved comparison
  `closure_comparison_iff` settles the split immediately:
  `N <= 30119370885234533` closes it; an actual lower bound
  `N > 60238741770469066` meets the strong refutation criterion.

## Per-value status ledger

No conditional value is treated as banked anywhere in this packet. The table
is the packet's own provenance discipline:

| value | exact | status |
| --- | ---: | --- |
| `B*` | `274980728111395087` | frozen row budget (unconditional) |
| `U_paid` | `981104` | banked in the live synthesis (KoalaBear tangent theorem) |
| `U_Q` | `<= 400389155870` | **conditional** on `KB_TANGENT_ROOTED_Q_SHELL(3,7)`; **not banked**; the live synthesis does not carry this line |
| post-Q reserve | `274980327721258113` | conditional (inherits `U_Q`); named `postQReserveConditional` |
| closure threshold | `137490163860629056` | conditional (reserve halved); named `closureThresholdConditional` |
| proper rank-49 cap | `77251422090159989` | derived in-package from its falling-factorial formula (`rank49_cap_formula_exact`), unconditional as arithmetic |
| ambient field order | `93571093019388561295270373781649880353786165192103559169` | `fieldPrime^6`, unconditional |

The conditional threshold chain is reproduced *only* so that the derivation
direction of the withdrawn proposal's own constants can be certified. In the
Lean package every value downstream of `uQConditional` carries the
`Conditional` suffix, and the chain is derived step-by-step
(`threshold_chain_exact`), not pinned.

## The route removed from the live compiler residual

The live completion architecture leaves the higher-dimensional balanced-core
clause open under its final spread-component, large-owner, and
exception-routing inputs; K3 states the residual-geometry obligation in units
of distinct affine slopes, with the moving-root theorem paying only charts
proved to be genuine pencils.

**Removed:** paying that obligation by a rank-49-or-pencil decomposition whose
normalized chart count is inherited either

1. **from the closure target** — killed by
   `chart_constants_are_threshold_derived`: the circulating constant
   `30119370885234533` is exactly
   `(closureThresholdConditional - properRank49Cap - 1) / 2`, and the sibling
   all-pencil constant `68745081930314528` is exactly
   `closureThresholdConditional / 2`. Both derivation directions are
   target-to-count. Neither is evidence; or
2. **from the local pencil API** — killed by
   `local_conditions_do_not_bound_chart_count`: for every natural `bound`
   there is an explicit model with `bound + 1` normalized chart keys
   satisfying every local condition the pencil machinery provides
   (duplicate-free keys, duplicate-free two-slope fibres, exact first-match
   ownership, pairwise-disjoint fibres, exact flattened charge
   `2 (bound + 1)`). The moving-root two-slope cap and slope-level
   first-match disjointness therefore imply no numerical chart bound.

The one census that *is* independently derived — one chart per ambient field
slope, giving `N <= fieldOrder` by selecting a representative slope from each
nonempty disjoint chart — is certified nonclosing by
`ambient_field_chart_ceiling_is_nonclosing`: charging it exceeds the threshold
astronomically, and it even exceeds the census-refutation boundary.

Direct impact: any future rank-49-or-pencil payment of K3 must arrive with a
geometry-derived chart census. The exact comparison it must feed is proved
once and for all (`closure_comparison_iff`), with the first failing count
located exactly (`first_failing_chart_count_exact`: one chart beyond the
allowance overshoots the threshold by exactly `2`).

## The certified statements

All in `experimental/lean/kb_pencil_census_route_cut/`, namespace
`KBPencilCensusRouteCut.CensusRouteCut`, stdlib-only, no Mathlib, no `sorry`,
no custom axiom.

1. `rank49_cap_formula_exact` — `properCorrectionBound 49 = 77251422090159989`:
   the rank-49 cap is its formula value
   `floor(31 * 50 * ff(2097152, 50) / ff(1116048, 50))`, not a free pin.
2. `field_order_and_budget_exact` — the ambient order equals `fieldPrime^6`
   digit-for-digit and `fieldOrder / 2^128 = B*`.
3. `threshold_chain_exact` — the conditional chain
   `B* - U_paid - uQConditional = 274980327721258113` and its half
   `137490163860629056`, derived, with conditional naming.
4. `chart_constants_are_threshold_derived` — both circulating chart constants
   are target-derived, exactly.
5. `closure_comparison_iff` — for an independently derived `N`:
   `properRank49Cap + 1 + 2N <= threshold iff N <= 30119370885234533`.
6. `first_failing_chart_count_exact` — the first failing count overshoots by
   exactly `2`.
7. `ambient_field_chart_ceiling_is_nonclosing` — the ambient census is
   independent but nonclosing.
8. The model family (`modelCharts`, `modelPencilSlopes`, `modelOwner`) with
   `model_local_conditions`, `local_conditions_do_not_bound_chart_count`, and
   the boundary instantiation at `60238741770469067` charts
   (`obstruction_model_chart_count_exact`,
   `obstruction_model_slope_count_exact`, `obstruction_model_split_fails`).
9. `obstruction_model_direct_size_fits` — load-bearing separation: the
   boundary model's `120477483540938134` pairwise-disjoint slope tokens still
   fit below the threshold. The model refutes the local-API inference to a
   census, **not** the direct KoalaBear residual bound. It is a route cut, not
   a counterexample.

## Derivation-direction ledger

| number or bound | derived from | independent of the closure target? | evidentiary status |
| --- | --- | --- | --- |
| `77251422090159989` | falling-factorial formula at rank 49 | yes | valid proper-block cap, conditional on actual one-block coverage |
| `60238741770469066` | `threshold - rank49Cap - 1` | no | target remainder, not a census |
| `30119370885234533` | the remainder halved | no | maximum allowable count, not a census |
| `68745081930314528` | `threshold / 2` | no | sibling all-pencil constant, same direction, not evidence |
| `fieldOrder` | KoalaBear field cardinality | yes | ambient ceiling only, nonclosing |
| `60238741770469067` (model) | refutation boundary plus one | no | independence witness only, not an RS census |

## Nonclaims

- No chart census is produced. No input of the withdrawn proposal is
  discharged. The actual rank-or-pencil law is neither proved nor refuted.
- The abstract models intentionally erase primitive locator geometry; they are
  not admissible received-line configurations and refute only the inference
  from the local API to a census.
- Nothing here is a payment, an atom, or a row bound. The conditional
  threshold chain is audit data, not ledger state.
- The standing conditional `KB_TANGENT_ROOTED_Q_SHELL(3,7)` is carried by the
  chain's provenance and is neither used nor discharged by the structural
  theorems.

## Successor

The missing object is a producer theorem joining the correction-component
classification to a normalized chart key with a geometry-derived count. An
intermediate count that does not close should trigger a different
decomposition rather than another target-derived split.

## Replay

```bash
cd experimental/lean/kb_pencil_census_route_cut && lake clean && lake build
```

Stdlib-only, no dependencies, clean build under five seconds. `native_decide`
is disclosed: the closed-arithmetic theorems each report exactly one
theorem-local `native_decide` axiom; the structural model theorems use only
`propext`, `Classical.choice`, and `Quot.sound`; `closure_comparison_iff` is
closed by `omega`. Every theorem has an explicit `#print axioms` census at
module end. `git diff --check` is clean on this packet.
