# Paper D v12 Outstanding Corrections Addendum

Status: AUDIT

Date: 2026-07-04

Agent/model: Claude Fable 5 (Claude Code), operated by Ken Webster.

Scope: standalone addendum note only. No maintainer-authored note is edited, no
`tex/` file is edited, no theorem status changes. This note re-records, as a new
file, the audit corrections from PR #228 whose in-place note edits were
intentionally left unmerged by the 2026-07-04 integration sweep (commit
`2ee618e`: "existing-note overwrites remain unmerged"), so that the two live
paper findings and the label-drift corrections are not lost.

All `tex/cs25_cap_v12.tex` line references below were re-verified against
`origin/main = cd5e809` (the `tex/` directory is unchanged since `0f45bf3`).

## Endpoint conventions

Radius/agreement conventions follow the paper: integer radius `r = floor(delta*n)`,
agreement `a = n - r`, closed balls, CA error normalized by the slope-sampling
field of the line experiment. No threshold value is asserted in this note beyond
what the paper itself prints.

## Finding 1 - `cor:conditional-half` proof-clarity gap (soundness unaffected)

- Location: `tex/cs25_cap_v12.tex` around lines 5054-5063 (`cor:conditional-half`
  statement and proof).
- The corollary's hypothesis is `2*floor(delta*n) <= n-k`; its proof combines the
  BCIKS20 Theorem 4.1 import, which is stated for `delta <= (1-rho)/2` (line
  ~5055), with `thm:mca-from-ca`. As literally worded, the import does not supply
  `eca(C, delta)` when `delta > (1-rho)/2` while the integer gate still holds.
- Concrete instance of the wording gap: `n=100, k=40, delta=0.305` gives
  `2*floor(delta*n) = 60 = n-k` (hypothesis holds) but `delta = 0.305 > 0.30 =
  (1-rho)/2` (import wording does not apply).
- This is a proof-clarity gap, not a soundness gap: by the paper's own
  integer-ball convention (`def:ca` at line ~134 and the radius convention at
  line ~157), `eca(C, delta) = eca(C, delta')` for `delta' = floor(delta*n)/n`,
  and `delta' <= (1-rho)/2` is equivalent to the stated hypothesis.
- Proposed minimal fix (one sentence in the proof): insert the reduction
  "replace `delta` by `delta' = floor(delta*n)/n <= (1-rho)/2`; the closed-ball
  event is unchanged by the integer-radius convention" before invoking the
  import.

## Finding 2 - circle widened-edge table misrounding

- Location: `tex/cs25_cap_v12.tex` line ~5191 (circle row of the widened unsafe
  table); caption at line ~5195 states the edges are "rounded outward to five
  digits" with exact values `15331/32768` and `30663/65536`.
- Exact value: `30663/65536 = 0.4678802490234375`. Outward rounding (upward, for
  an unsafe lower edge) to five digits gives `0.46789`; the table prints
  `0.46788` (round-to-nearest, i.e. inward).
- Consistency cross-check: the KoalaBear row (line ~5189) prints
  `15331/32768 = 0.467864990234375` as `0.46787`, which IS correctly rounded
  outward. Only the circle entry deviates from the caption's stated convention.
- Proposed minimal fix: print `0.46789` (or the exact fraction) for the circle
  edge.

## Label-drift corrections (previously in PR #228, dropped as note overwrites)

These correct stale statements in local audit records; they are recorded here
instead of editing the original notes.

1. `thm:A` (deep-point conversion) is proved self-contained in v12: the
   Crites-Stewart import was retired (`tex/cs25_cap_v12.tex` lines ~187 and
   ~5538), and `thm:A` carries the integer-radius condition
   `floor(delta*n) <= n-k-1` (line ~195). Older audit records listing `thm:A`
   (and its dependents `thm:main`, `cor:grand`, `cor:deployed`, `cor:rows`) as
   CONDITIONAL on an imported Crites-Stewart conversion are stale. The
   half-distance edge (`cor:conditional-half`) remains CONDITIONAL on the
   isolated BCIKS20 import; nothing here promotes that.
2. The certificate package in `tex/towards-prize.tex` is labeled
   `prop:companion-certificate-package` (a Proposition, line ~113); older
   references to a `cap-paper-package` Theorem label are stale.
3. Observation only: `experimental/scripts/verify_towards_prize_v3_cap_package.py`
   on main still carries the older label vocabulary in its docstring/metadata.
   Its numeric checks are unaffected and pass; this note does not modify the
   script.

## Reproducibility

```bash
python -c "from fractions import Fraction; import math; f=Fraction(30663,65536); print(f, float(f), math.ceil(f*10**5)/10**5)"
python -c "from fractions import Fraction; import math; f=Fraction(15331,32768); print(f, float(f), math.ceil(f*10**5)/10**5)"
python -c "n,k=100,40; d=0.305; print(2*int(d*n) <= n-k, d <= (1-k/n)/2)"
```

Both findings were independently re-derived in exact arithmetic during two
separate verification passes (2026-07-03 and 2026-07-04).

## Non-claims

This note does not change any theorem or cap constant, does not edit Paper D or
towards-prize, does not promote the BCIKS import beyond CONDITIONAL, and does
not add a leaderboard row. It is a bookkeeping addendum so the corrections
remain visible until the maintainer applies or declines them.
