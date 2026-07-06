# Adjacent-Pair Margin Audit

## Claim

The current `cor:capg-adjacent-pairs` row arithmetic reproduces exactly from
integer computations.  In all four rows the lower floor exceeds `B_*` at the
printed unsafe `a0` and is quiet at `a0+1`; the exact millibit intervals round
to the fail margins printed in the raw file.

## Status

EXPERIMENTAL / AUDIT.  This independently checks the printed adjacent-pair
arithmetic; it is not a proof that `a0+1` is safe, not a complete upper ledger,
and not a resolution of `prob:band`.

## Pinned Statements

- `prop:capg-moved-frontier`, `experimental/cap25_cap_v13_raw.tex`, lines
  8559-8678: moves the MCA unsafe edges using the identity-prefix floor.
- `cor:capg-adjacent-pairs`, lines 8680-8704: prints the four current
  adjacent pairs and their approximate fail margins.

## Exact Margins

The margin interval is an exact integer millibit bracket for
`log2(B_*/lower(a0+1))`; no floating-point arithmetic is used.

| row | a0 | a0+1 | B_* | lower(a0+1) | exact fail interval | printed |
|---|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA | 1116047 | 1116048 | 274980728111395087 | 57198030366 | [22.196, 22.197) | 22.2 |
| KoalaBear list | 1116046 | 1116047 | 274980728111395087 | 65065153468 | [22.010, 22.011) | 22.0 |
| Mersenne-31 MCA | 1116023 | 1116024 | 16777215 | 1752700 | [3.258, 3.259) | 3.3 |
| Mersenne-31 list | 1116022 | 1116023 | 16777215 | 1993678 | [3.072, 3.073) | 3.1 |

The tightest printed row is the Mersenne-31 list row.  The Mersenne-31 MCA row
is next, within the same low-single-digit bit range.

## Proof Idea Or Experiment

The generator recomputes the current row thresholds, exact binomial floors, and
MCA deep-list conversion from `n=2^21`, `k=2^20`, the base primes, and the
printed agreements.  It represents each bit margin as the integer floor of
`1000*log2(num/den)`, found by exact comparisons of integer powers.

The independent checker recomputes the binomial values by a descending
recurrence and repeats the exact millibit comparisons without importing the
generator.  A hand-sized oracle row has margin exactly `2` bits and validates
the logarithm bracketing code before the deployed rows are accepted.

## Ledger Impact

This confirms the arithmetic printed in `cor:capg-adjacent-pairs`: the listed
fail margins are exact rounded summaries of the current lower-floor shortfall
at `a0+1`.  It also keeps the scope clear: a quiet lower floor is not an upper
certificate.

## Non-Overlap

This does not redo the finite-testability map, the Q/R1 input audit, the
split-pencil floor audit, prefix-collision ledgers, annulus packets, or
rung-margin audits.  It checks only the printed current adjacent-pair
arithmetic.

## Self-Red-Team

An adversarial reviewer could say this merely confirms the file's own row
arithmetic and does not test the missing safe-side inputs.  That is correct and
is the intended claim: the packet verifies a load-bearing printed number, not
the conjectural upper bound that would make the row safe.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_capg_adjacent_pair_margins.py --emit-defaults --check
py -3.13 experimental/scripts/verify_capg_adjacent_pair_margins_check.py --check
```
