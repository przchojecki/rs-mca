# Q/R1 Closing Finite-Input Audit

## Claim

The current statement `cor:capfr1-Q-R1-closing` is a conditional one-step
compiler, not a replayable finite certificate in the current tree.  Its exact
thresholds and lower-side rows are present and recompute exactly, but the named
upper summands

```text
U_paid(a0+1) + U_Q(a0+1) + U_R1(a0+1)
```

are not instantiated as exact integer inputs.  Therefore the one-step
inequality cannot be checked from current artifacts alone.

## Status

EXPERIMENTAL / AUDIT.  This is a finite-input availability audit of
`cor:capfr1-Q-R1-closing`; it does not verify the one-step inequality, does not
establish the safe side of any adjacent row, and does not resolve or advance
`prob:band`.

## Band Re-Reading (Author's Own Directive)

The corollary's original band input is `prob:band`.  The current raw file
re-points it: `rem:capg-band` (`experimental/cap25_cap_v13_raw.tex` lines
9415-9421) lists `cor:capfr1-Q-R1-closing` among the statements whose band input
becomes `prob:capfr1-normalized-band` -- item (i) records this as the operative
band input "now by necessity rather than by convention," and item (ii) sets the
finite deployed target at "the new adjacent values of `cor:capg-adjacent-pairs`."
Lines 9456-9459 record the substitution as "a restatement of what those rows in
fact require, not a weakening."  This audit is therefore scoped to the finite
inputs of the corollary under its normalized-band reading.

## Pinned Statements

- `prop:capfr1-slope-elimination`, `experimental/cap25_cap_v13_raw.tex`,
  lines 7801-7807: non-common rank-one supports bound unpaid finite slopes
  after paid cells and common supports are removed.
- `cor:capfr1-Q-R1-closing`, lines 7829-7838: finite adjacent closure requires
  the exact inequality
  `U_paid(a0+1)+U_Q(a0+1)+U_R1(a0+1) <= B_* < L(a0)`.
- `cor:capg-adjacent-pairs`, lines 8680-8704: the current adjacent rows are
  KoalaBear MCA 1116047/1116048, KoalaBear list 1116046/1116047,
  Mersenne-31 MCA 1116023/1116024, and Mersenne-31 list 1116022/1116023.
- `prop:capg-census-floor`, lines 9727-9742: the live census correction uses
  base-field scale for the stated floor model.

## Exact Row Audit

All rows satisfy the expected lower-side pattern: the lower floor exceeds
`B_*` at `a0`, and the same lower mechanism is quiet at `a0+1`.

| row | a0 | a0+1 | B_* | lower at a0 | lower at a0+1 | gap to exceed at a0+1 |
|---|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA | 1116047 | 1116048 | 274980728111395087 | 138634741058327852652 | 57198030366 | 274980670913364722 |
| KoalaBear list | 1116046 | 1116047 | 274980728111395087 | 157702518233425975347 | 65065153468 | 274980663046241620 |
| Mersenne-31 MCA | 1116023 | 1116024 | 16777215 | 4281388998575706 | 1752700 | 15024516 |
| Mersenne-31 list | 1116022 | 1116023 | 16777215 | 4870025984688527 | 1993678 | 14783538 |

## Finite-Input Availability

The current tree contains the exact `B_*` thresholds and enough data to replay
the lower-side floor comparisons.  It does not contain a complete exact upper
summand ledger for the live one-step row:

| input | audit result |
|---|---|
| `B_*` | present and recomputed exactly |
| `L(a0)` | present and recomputed exactly |
| `U_paid(a0+1)` | not instantiated as a complete one-step integer total |
| `U_Q(a0+1)` | not instantiated as a finite Q integer certificate |
| `U_R1(a0+1)` | not instantiated as a finite R1 integer certificate |

The compact companion states the certificate grammar in integer form, but also
states that Q, balanced-core, and shift-pair constants must be supplied before
the final arithmetic is accepted.  The existing frontier-adjacent packets keep
the safe-side status open, and the corrected KoalaBear packet explicitly says
that no finite `U(1116048) <= B_*` statement is claimed.

## Proof Idea Or Experiment

The generator recomputes `B_*`, the identity/list floor, and the MCA
deep-list converted lower count with exact integers.  It then pins the current
TeX statement blocks by label and hashes, checks the compact finite-certificate
interface, and reads the existing frontier-adjacent packet statuses.  The
independent checker recomputes the same row arithmetic by a separate descending
binomial recurrence and rescans the source markers without importing the
generator.

## Ledger Impact

This packet turns `cor:capfr1-Q-R1-closing` into a concrete finite-input
checklist result: the replayable part is the lower staircase and current row
thresholds; the missing part is the exact upper numerator input.  That makes
the live follow-up narrow: supply the missing exact `U_paid`, `U_Q`, and `U_R1`
summands, or keep the corollary explicitly conditional.

## Non-Overlap

This does not redo the reachability scope map, the rung-margin audit, the
prefix-collision ledgers, the growing-dimension census, the annulus packets, or
the finite-testability mining map.  It audits only the live finite-input
availability of `cor:capfr1-Q-R1-closing` after the current adjacent rows moved.

## Self-Red-Team

An adversarial reviewer could object that this only proves an input ledger is
missing, not that the mathematical statement is false.  That objection is
correct and is the framing used here: this packet is not a witness against the
corollary.  It says only that the current tree does not yet supply the exact
finite numerator data needed to replay the corollary's one-step inequality.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_q_r1_closing_audit.py --emit-defaults --check
py -3.13 experimental/scripts/verify_q_r1_closing_audit_check.py --check
```
