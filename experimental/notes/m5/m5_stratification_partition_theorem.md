# M5 Stratification Partition Theorem

- **Status:** PROVED / COMBINATORIAL, with finite replay.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable execution queue `Q2.10
  [stratification_partition_thm]`; `towards-prize.md` M5/M6.
- **Verifier:** `experimental/scripts/verify_m5_stratification_partition.py`.
- **Artifact:**
  `experimental/data/certificates/m5-stratification-partition/m5_stratification_partition_certificate.json`.

This note records the bookkeeping theorem behind the v12 M5 chart tree.  It is
not a theorem about any particular Hankel bucket.  Its role is to make the
dedup convention explicit before later packets attach geometric predicates and
root tables.

## Ordered Leaves

For a fixed row, exact agreement, sampler, and candidate finite set `Omega`
of slopes or chart instances, suppose the chart routine emits the following
ordered predicates:

```text
T0 containment_excluded
T1 degenerate_pair
T2 tangent_paid
T3 quotient_paid
T4 extension_paid
T5 higher_agreement_dedup
T6 closed_chart          status in {eliminant, empty, dimension_degree}
T7 named_residual        residual label in
                         {quotient,tangent,extension,
                          candidate_new_obstruction,unknown}
```

The order is part of the definition.  A candidate is charged to the first
predicate that claims it.  The final residual predicate is total; if no earlier
predicate applies, the candidate receives the emitted residual label, defaulting
to `unknown`.

For `0 <= i <= 7`, define

```text
L_i = T_i \ (T_0 union ... union T_{i-1}).
```

## Theorem

The leaves `L_0,...,L_7` are pairwise disjoint and their union is `Omega`.
Consequently every M4/M5 table using this first-match convention can sum
contributions over leaves without double-counting a root that is simultaneously
tangent, quotient, extension-confined, closed by an eliminant, or residual.

Moreover, the allowed terminal labels are exactly:

```text
excluded
paid:degenerate
paid:tangent
paid:quotient
paid:extension
dedup:higher_agreement
eliminant
empty
dimension_degree
residual:quotient
residual:tangent
residual:extension
residual:candidate_new_obstruction
residual:unknown
```

## Proof

For every `x in Omega`, scan the ordered list.  If `x` lies in an earlier
predicate, it is removed from all later leaves by definition.  If no proper
predicate claims `x`, the total residual predicate `T7=Omega` claims it.
Therefore `x` lies in at least one leaf and cannot lie in two distinct leaves.
This proves totality and disjointness.

The terminal-label statement follows from the displayed allowed status and
residual-label sets.  In particular, an unproved or unresolved bucket is not
silently discarded: it lands in `residual:unknown`.

## Replay

The verifier checks:

```text
all 2^7 overlaps among the non-residual predicates;
invalid closed-chart and residual labels are rejected;
500 seeded random root-set partitions over F_97;
a mixed tangent/quotient/extension/eliminant/residual example where naive
overlap counting overcounts but first-match counting partitions the roots.
```

Run:

```bash
python3 experimental/scripts/verify_m5_stratification_partition.py
python3 experimental/scripts/verify_m5_stratification_partition.py --emit
python3 -m py_compile experimental/scripts/verify_m5_stratification_partition.py
```

The v12 packet checker also accepts an optional `stratification_leaf_table`
field.  When present, it verifies first-match leaf assignment, rejects duplicate
candidate rows, and recomputes the optional `stratification_counted_union` from
the declared counted terminal labels.  The same checker update verifies that
local `removed_ledgers[*].certificate_ref` paths exist.  The regression packets
are:

```bash
python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/m5-stratification-partition/valid_stratified_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/m5-stratification-partition/invalid_wrong_leaf_stratified_packet.json
python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/m5-stratification-partition/invalid_missing_removed_ledger_ref_packet.json
```

## Nonclaims

This packet does not prove tangent, quotient, extension, low-rank, regular,
or split-locator predicates for an actual Hankel row.  It proves only the
ordered accounting layer that those later geometric packets should use.
