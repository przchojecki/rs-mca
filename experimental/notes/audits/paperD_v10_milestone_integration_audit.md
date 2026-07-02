# Paper D v10 Milestone Integration Audit

**Date:** 2026-07-01.

**Status:** AUDIT / VERSION-PROMOTION / PROVED-CERTIFICATE-FRAMEWORK.

This note records the historical integration of the four
`cs25_cap_v10_milestone*` folders into `tex/cs25_cap_v10.tex`.  Paper D v12 now
supersedes v10 as the current cap-paper draft; use this note as provenance for
the v10 ledger package, not as the active citation target.

## Integrated content

### Milestone 1: quantitative lower ledgers

Integrated into v10:

```text
quantitative deep-list floor;
deep-list trigger/ceiling;
heaviest quotient-remainder prefix fibers;
quotient-remainder deep floor.
```

Why it is strictly stronger than v9: v9 used the threshold-grade
contrapositive trigger.  v10 keeps the actual list size `L`, producing a
numerator

```text
ceil(L(q-n)/(q-n+kL))
```

and allowing scanners to record nonzero lower mass even below the old trigger.

### Milestone 2: exact quotient support-union ledger

Integrated into v10:

```text
block support-profile polynomial;
exact divisor-lattice support-union formula;
divisor-block support-ledger certificate.
```

Why it is strictly stronger than v9: overlapping quotient descriptions across
different divisor scales are counted by one common lcm-block coefficient
extraction instead of by a raw safe sum.

### Milestone 3: quotient image and extension-pole ledgers

Integrated into v10:

```text
fixed-support parameter gcd;
quotient image lcm polynomial;
finite, projective, and curve quotient-image certificates;
punctured simple-pole conversion;
extension-pole deep-list floor.
```

Why it is strictly stronger than v9: inside a declared quotient branch, duplicate
finite slopes, projective slopes, and finite curve parameters are coalesced
before printing the numerator.  Separately, the extension-pole theorem turns any
large list over `D subset B` into a genuinely `F`-valued simple-pole witness by
averaging over `F \ B`, with numerator

```text
ceil(L(|F|-|B|)/(|F|-|B|+kL)).
```

This strengthens the F1 discussion from nonconstructive existence to a
certificate format: print the pole and its value-bucket table.

### Milestone 4: regular Hankel rank-drop ledger

Integrated into v10:

```text
canonical affine rank-drop gcd;
closed-ball rank-drop lcm;
paid-root removal;
finite-parameter curve rank-drop gcd;
regular rank-drop certificate.
```

Why it is strictly stronger than v9: the regular overdetermined Hankel bucket no
longer relies on one chosen maximal minor.  The v10 ledger takes the gcd of all
nonzero maximal minors at each exact agreement and then an lcm across exact
agreements.  This is canonical and never worse than a one-minor certificate.

## Scripts moved to `scripts/`

Reusable milestone scripts were copied out of `tex/`:

```text
scripts/cs25_v10_quotient_support_ledger.py
scripts/cs25_v10_quotient_image_ledger_prime.py
scripts/cs25_v10_dual_cosupport_ledger.py
scripts/cs25_v10_extension_pole_floor.py
scripts/cs25_v10_regular_hankel_eliminant.py
```

The one-off milestone generators and patch bundles were not retained as source
artifacts because `tex/cs25_cap_v10.tex` was the integrated manuscript at that
stage.  Current active citations should point to `tex/cs25_cap_v12.tex`.

## Remaining open pieces

The integration does not claim the full Proximity Prize.  The open pieces are
now sharper:

```text
quotient structural exhaustion beyond declared branch ledgers;
regular-window scans for meaningful rows, especially 385 <= A <= 426;
underdetermined and rank-drop singular Hankel buckets;
safe-side classification of genuinely extension-valued lines;
aperiodic curve and projective pivot eliminants.
```
