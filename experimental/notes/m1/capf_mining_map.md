# CAP25 Raw Finite-Testability Map

## Claim

This packet triages finite and exact-integer statements in
`experimental/cap25_cap_v13_raw.tex` by reachability.  The map separates rows
where a finite check only confirms a proved fixed-parameter statement from rows
where a finite check tests an unproved active input.

## Status

EXPERIMENTAL / SCOPE-MAP.  The map is not a proof of any active input, not a
truth verdict on the raw statements, and not a resolution of `prob:band`.

## Parameters

The source is `experimental/cap25_cap_v13_raw.tex` at base
`0fa9427044fcd0a9e2fffade54dcb0c3f08253ca`.  The parsed rows are current
`capf-*`, `capfr1-*`, `capfp-*`, and `capg-*` statement labels with finite or
exact-integer content.

## Existing paper dependency

The reachability lens is the finite reachability scope map in #357: fixed
finite-parameter censuses under already proved bounds are confirmation-ceiling
checks.  The current raw file also supplies a base-field correction for earlier
challenge-field-scale census models at `prob:capg-split-pencil-B`.

Pinned current rows:

| label | line | classification | finite-testability role |
| --- | ---: | --- | --- |
| `thm:capf-first-moment` | 6544 | PROVEN / CONFIRMATION-CEILING | exact aligned-locator first moment |
| `thm:capf-fixeddim` | 6735 | PROVEN / CONFIRMATION-CEILING | fixed-dimensional incidence bound |
| `prob:capfr1-rank-one-census` | 7819 | SELF-CORRECTED / LOW-SKIP | earlier challenge-field scale; corrected later |
| `cor:capfr1-Q-R1-closing` | 7829 | REDUCTION / HIGH | one-step inequality using paid, quotient, and rank-one numerators |
| `prob:capfr1-balanced-core` | 7960 | SELF-CORRECTED / LOW-SKIP | earlier challenge-field scale; corrected later |
| `prob:capfr1-split-pencil` | 8012 | SELF-CORRECTED / LOW-SKIP | earlier challenge-field scale; corrected later |
| `cor:capg-adjacent-pairs` | 8680 | PROVEN / HIGH | printed adjacent-row margins needing independent arithmetic audit |
| `prob:capg-shiftpairs` | 9667 | STATED / HIGH | primitive shift-pair ledger behind the exact second-moment stratification |
| `prob:capg-split-pencil-B` | 9842 | STATED / HIGH | corrected base-field-normalized interior split-pencil model |
| `prob:capg-active-Q` | 9900 | STATED / MEDIUM | active interface; subroutes partly occupied |
| `prob:capg-active-BC` | 9919 | STATED / MEDIUM | active interface pointing to `prob:capg-split-pencil-B` |
| `prob:capg-active-shiftpairs` | 9926 | STATED / MEDIUM | active interface pointing to `prob:capg-shiftpairs` |

## Proof idea or experiment

The generator parses theorem-like environments from the raw source, extracts
labels and line anchors, and records a compact triage row.  Curated overrides
are used only for the named frontier labels and occupation data from prior
packets.  The checker independently re-reads the source, verifies each line
anchor, rechecks the short quote anchors, and recomputes two exact toy gates:

| gate | row | result |
| --- | --- | --- |
| `thm:capf-first-moment` | `F_5`, `n=4`, `j=2`, `t=1` | brute-force average `24/5`, matching the theorem |
| `thm:capf-fixeddim` | `F_5^*`, `j=2`, projective dimension `2` | incidence `6 <= binom(4,2)=6` |
| `prob:capg-active-BC` | line 9919 | no following proof environment; explicit input body present |
| `prob:capg-active-shiftpairs` | line 9926 | no following proof environment; explicit input body present |

## Ledger impact

The high-priority fresh finite targets from this map are:

1. `cor:capfr1-Q-R1-closing`, line 7829: the one-step inequality using paid,
   quotient, and rank-one numerators.  The q-scale census correction does not
   by itself test the exact `a_0+1` numerator.
2. `prob:capg-split-pencil-B`, line 9842: the author's base-field-normalized
   correction of the split-pencil census model, using `prop:capg-census-floor`
   as a proved fixture.
3. `cor:capg-adjacent-pairs`, line 8680: the printed adjacent-row margins,
   especially the tight Mersenne-31 margins.
4. `prob:capg-shiftpairs`, line 9667: the primitive shift-pair ledger behind
   the exact second-moment stratification.

The active-interface rows `prob:capg-active-Q`, `prob:capg-active-BC`, and
`prob:capg-active-shiftpairs` remain important context, but the sharper finite
targets above are the recommended next packets.

The old challenge-field-scale rows `prob:capfr1-rank-one-census`,
`prob:capfr1-balanced-core`, `prob:capfr1-split-pencil`, `prob:capfp-R1`,
`prob:capfp-balanced`, and `prob:capfp-split` are recorded as SELF-CORRECTED
and LOW/SKIP.  Finite work on those rows as originally scaled would only
reproduce the raw file's own correction to the base-field model.

## Constants

The certificate records 168 current-frontier finite rows:

| count type | values |
| --- | --- |
| proof status | PROVEN 85; STATED 56; REDUCTION 20; SELF-CORRECTED 6; CONDITIONAL 1 |
| reachability | CONFIRMATION-CEILING 84; GENUINE-TEST 84 |
| priority | HIGH 4; MEDIUM 71; LOW/SKIP 93 |

## Reproducibility

Certificate:
`experimental/data/certificates/capf-mining-map/capf_mining_map.json`

Commands:

```bash
py -3.13 experimental/scripts/verify_capf_mining_map.py --emit-defaults --check
py -3.13 experimental/scripts/verify_capf_mining_map_check.py --check
```

## Overclaim check

A possible overclaim would be to read the four HIGH rows as mathematical
evidence for those inputs.  The packet does not do that: it only identifies
which current statements are worth finite testing and which rows are already
proved, occupied, or self-corrected.  A later finite packet still needs its own
canonical object, oracle gate, independent checker, and bounded certificate.
