# External calibration packet for row-sharp Q: fiber censuses, shift-pair
# top stratum, and a mode-at-null datum

- **Status:** AUDIT / EXPERIMENTAL / calibration (enters no proof); one
  COUNTEREXAMPLE-shaped datum against the *raw* mode-at-null form at a toy
  row, stated precisely below.
- **Scripts:** `experimental/scripts/qsp_fiber_census.py` (exact DP;
  int64 with checksums where C(N,m) < 2^62, flagged float64 beyond,
  validated on overlapping exact rows),
  `experimental/scripts/qsp_modeatnull_structure.py` (independent
  exhaustive recomputation + structure classification).
- **Data:** `experimental/data/rowsharp_q_external_calibration.json`,
  `experimental/data/rowsharp_q_modeatnull_datum.json`.

These are runs of an external falsification fleet on the two
pre-registered falsifier objects named in cap25_cap_v13_raw.tex ("a
super-polynomial primitive prefix fiber, refuting (Q)" and the primitive
shift-pair family of thm:capg-second-moment). Both hunts came back
NEGATIVE (supporting (Q) and the SP ledger); the by-catch is a
route-discriminating datum for prob:capfr1-mode-null.

## 1. Replay of the printed calibration, then three new scales

The power-sum prefix DP (Newton-equivalent to the elementary-symmetric
prefix for w < p) reproduces rem:capff1-collision-gap's printed
max-to-mean table digit-exact — 1.0012 / 1.2126 / 2.6722 at (17,16,8),
depths 1–3; 1.0022 / 1.2101 / 4.1034 at (41,20,10); Poisson row max 11
vs mean 2.68; 1 + 2.5e-12 and 1 + 6.9e-9 at (257,64,34), depths 1–2 —
and extends the dense-bulk ladder three scales beyond the printed table
(w = 2, m = N/2, geometry N/√p ≈ 3–5):

    (17,16):  2.1e-1     (41,20):  2.1e-1     (101,50):  2.9e-6
    (257,64): 6.9e-9     (577,96): 6.1e-13    (1153,128): ≤ 1e-15 (f64 floor)

The collapse toward 1 accelerates with scale. No super-polynomial
primitive fiber anywhere reachable: the falsifiable prediction ("any
violation must place a super-polynomial fiber inside the dense bulk of a
primitive scale") is consistent with every measured point.

## 2. Shift-pair top stratum at model scale

Exact sp_w(w+1; D) (ordered disjoint (w+1)-subset pairs, matching
depth-w prefixes) via a joint (|S|,|T|,Δ-prefix) DP:

    w = 2: sp/model = 1.270, 1.084, 1.037, 1.009, 1.037, 0.955  (p = 17..1153)
    w = 3: sp/model = 1.374, 1.876, 1.035                       (p = 17, 41, 101)

(model = C(N,k)C(N−k,k)/p^w). Small-N inflation dies at scale; the
(−1)-dilation pullback class is a tiny fraction at w = 2 and empty at
w = 3. No super-polynomial primitive shift-pair family.

## 3. The datum: raw mode-at-null fails by NULL SUPPRESSION at (41,20,10,2)

Computed twice (DP + independent exhaustive enumeration):

    D = mu_20 ⊂ F_41* (the quadratic residues), m = 10, w = 2:
    N(0,0) = 66,  N(11,0) = 133 = max,  mean = 109.9.

Precisely graded:

- the MAX is unremarkable: 133 = mean + 2.2σ, BELOW the Poisson-expected
  maximum (≈150 over 41² cells). The max-fiber form of (Q) is untouched
  here (max/mean = 1.21, matching the printed table).
- the NULL fiber is the anomaly: 66 = mean − 4.2σ. The raw inequality
  N_w(z) ≤ N_w(0) of prob:capfr1-mode-null fails by a factor 2.02, and it
  fails because the null fiber is suppressed, not because any fiber
  spikes.
- the argmax fiber carries no obvious quotient structure: 0 members are
  coset unions (unions of antipodal mu_2-pairs), 0 members are
  dilation-stable; the whole line (mu_20·11, 0) carries uniform 133s
  (consistent with the dilation equivariance fib(gz1, g²z2) = fib(z)).
- row-specific: the sibling half-group row (101,50,25,2) — also
  p = 2N+1 — has null = max to exact arithmetic. The suppression is
  finer row arithmetic than the p = 2N+1 pattern; explanation open.

Consequence for prob:capfr1-mode-null: either the quotient-rung
separation is meant to charge prefixes on the (·, 0) line to a rung (in
which case it would help to state which rung), or the exchange-
compression alternative is the safer route at rows of this shape. At the
binding deployed rows the atom bound binds the MAX, not the null, so
null suppression — if it recurs at scale — is favorable rather than
harmful to the finite program.

## What to do next

Sweep the null/mean ratio over more subgroup rows (the DP makes this
cheap) to map where null suppression occurs; decide whether the (·,0)
line at (41,20,10) is rung-charged under the intended reading of
"quotient rungs separated"; if not, prefer the exchange-compression
formulation for the finite input.
