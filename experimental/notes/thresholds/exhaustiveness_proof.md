# Exhaustiveness proof (W56-M2, hard input a)

## Status
EXPERIMENTAL. **Rung: PROVED-SPECIAL** (full secant atlas).

## Phase 0
def:first-match L1453; thm:syndrome-secant-exact L1607;
thm:canonical-partial-occupancy-atlas L3744.

## Lemma A
Full atlas of all |E|<=t cells: B = union Z_E by thm:syndrome-secant-exact;
first-match projections partition B. Exhaustive.

## Lemma B
t=1 special case is the full |E|<=1 atlas.

## Lemma C
Canonical PO atlas exhaustive CONDITIONAL on L3744; secant half verified on toys.

## REDUCED
Incomplete atlases omit witnessing E and can leave bad slopes uncovered
(|E|=t-only model).

## Dual routes
Lemmas + dual bad-slope toys.

## Reproducibility
payload_sha256: e1f326f0015910ceacf584727d462d0d2420e2995f4bfdd23be51386db428361
