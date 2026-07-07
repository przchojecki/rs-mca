# CAP25 v13 row-sharp Q atom: binding-row kappa calibration

Status: EXPERIMENTAL / MEASUREMENT (enters no proof).

Per-claim labels are attached inline. `grande_finale.tex` states the remaining
Q input in max-fiber form with constant kappa (`thm:q-implies-sp`):

```text
max_z N_w(z) <= kappa * Fbar,    Fbar = C(n,m) |B|^{-w},
```

after quotient-pulled-back and planted strata are removed -- with
`kappa = e^{o(n)}` as the conclusion of the CONDITIONAL moment criterion
`thm:moment-q` (its moment inputs `A = o(rn)`, `B/r = o(n)` are currently
missing; nothing asymptotic is established) and explicit per-row budget
constants fitting the four finite adjacent margins (`prop:q-exact-target`,
`def:q-row-atom`). This packet MEASURES that kappa exactly on 59 scaled-down
rows: the primitive ratio `R_prim` below is the measured value of kappa at an
exact row. Measured kappa `<= 1.221` on every heavy row, against the binding
budget kappa `<= 8.4152` at the Mersenne-31 list row. No falsifier within
stated coverage. It does not prove the adjacent safe rows; `def:q-row-atom`
remains the missing theorem.

- Data: `experimental/data/cap25_v13_q_atom_binding_row_calibration.json` (full 59-row table + structured sweep + fit).
- Verifier: `experimental/scripts/verify_cap25_v13_q_atom_binding_row_calibration.py` (zero-arg, stdlib, ~27 s, exit 0 = PASS).

## Object

`def:q-row-atom` sets `R_Q^max = |B|^w max_z |P_Q(z)| / C(n,a_+)` and asks for
`R_Q^max <= 2^{Delta_Q}`, equivalently `max_z |P_Q(z)| <= B*`; this is the
finite-row instance of the kappa form above (`R_Q^max` = the row's kappa). We
measure the exact scaled analogue

```text
R_prim = |B|^w * max_z |Fib_prim(z)| / C(n,m),   |B| = p,  m = a_+ = n/2 + w,
```

with the list route `K = n/2`. `Fib_prim` drops quotient / coeff-scale members
(non-primitive, `lem:coeff-scale`, `thm:coeff-quotient-extract`); `R_prim_np`
additionally drops planted-core strata. Both are `<= R_prim`, so `R_prim` is the
conservative upper proxy for the first-match residual `P_Q`, i.e. an upper
measurement of the row's kappa.

The binding target from `prop:q-exact-target` (MEASUREMENT, recomputed exactly by
the verifier from the proposition's own integers):

```text
Mersenne-31 list:  p = 2^31-1,  n = 2^21,  K = 2^20,  a_+ = 1116023,  w = 67447,
  avg = ceil( C(2^21, 1116023) / (2^31-1)^67447 ) = 1993678,
  B*  = floor( (2^31-1)^4 / 2^100 ) = 2^24-1 = 16777215,
  budget ratio  B*/avg = 8.4152     (= 3.0730 bits).
```

8.4152 is the tightest of the four adjacent rows (KB-MCA 4807520.93, KB-list
4226236.53, M31-MCA 9.5722, M31-list 8.4152), so it is the first attack (Q1).

## Method

MEASUREMENT. Exact stdlib enumeration of every `m`-subset of `D = mu_n subset
F_p^x` for each row: prefix key = top-`w` elementary symmetric coefficients mod
`p` (the deployed `verify_q2_heavy_fiber_fewness.py` locator `prefix_key` up to
a fixed per-coordinate sign bijection, fiber-preserving), fiber sizes tallied
exactly, the quotient (`+n/c` invariant) and planted (common-support) subclasses
split off exactly. No sampling; `R_prim` is the true primitive max.

Why the max fiber and not character sums: `prop:fourier-audit` proves a
triangle-inequality character route must reach the `p^{-w}` scale while uniform
square-root (Weil-type) estimates give only `p^{-w/2}` -- short by `p^{w/2}` --
so exact-row measurement of the max fiber itself is the informative instrument
(and `prop:q-moment-order-floor` rules out low-order moment substitutes, see
the #392 weave line).

Coverage: 59 rows, `n in {10,12,16,20,24,26,28}`, 3 primes per `n` where feasible
(`p in {11..113}`), `w in {1,2,3,4}`, `C(n,m)` up to 13123110 (= C(28,18), the
largest enumerated row; the `n <= 24` grid was capped at 3e6 and the five
`n in {26,28}` rows were run individually above that cap). Ten rows are heavy
(avg fiber `>= 100`); 27 have avg `>= 1` (a genuine max statistic); the rest are
sparse (avg `< 1`, max fiber usually 1).

## Measured kappa table (top rows; full table in the data JSON)

MEASUREMENT. `R_prim` = measured kappa. Every heavy row (avg `>= 100`) sits far
below the binding budget kappa `<= 8.4152`:

```text
  n    p   w        avg   max_prim   R_prim   R_prim_np
 16   97   1     117.94        144   1.2210     1.2210    <- heavy-max R_prim
 24   97   2     208.44        247   1.1850     1.1850
 24   73   2     368.03        408   1.1086     1.1086
 16  113   1     101.24        112   1.1063     1.1063
 20  101   1    1662.97       1720   1.0343     1.0343
 20   61   1    2753.44       2800   1.0169     1.0169
 24   73   1   34193.75      34248   1.0016     1.0016
 24   97   1   25733.44      25752   1.0007     1.0007
 20   41   1    4096.59       4099   1.0006     1.0006
 16   17   1     672.94        673   1.0001     1.0001
```

The largest `R_prim` at any avg `>= 1` is 7.6783 (still `< 8.4152`), and it
occurs only at near-unit heaviness:

```text
  n    p   w      avg   max_prim   R_prim
 24   97   3    1.433        11   7.6783   <- max over all avg>=1 rows
 20   41   3    1.125         6   5.3344
 24   73   3    3.361        13   3.8678
 20  101   2   12.349        40   3.2392
 28   29   4   18.554        56   3.0182
```

Sparse rows (avg `< 1`) show `R_prim` up to 282576 (row `10,41,4`), but there the
max fiber is a single subset over a vanishing average -- a small-count-over-tiny-
average artifact, not a heavy fiber. It is a different regime from the deployed
rows, whose avg fiber is `>= ~2e6`.

## Heaviness confound

NUMERIC. The apparent growth of `R_prim` with depth `w` is a heaviness confound,
not a depth effect. Fitting `ln(R_prim-1) = k(w) - beta(w) ln(avg)` on the 20
resolved excess points (avg `>= 1`, `R_prim > 1.02`, `max_prim >= 4`):

```text
  w = 1:  beta = 0.254   (n=7)
  w = 2:  beta = 0.467   (n=7)     beta rises ~0.21 per step
  w = 3:  beta = 0.667   (n=5)     linear: beta(w) = 0.2065 w + 0.047
```

`beta(w)` (the heaviness-decay exponent) INCREASES with `w`, so at fixed heavy
avg the deeper rows decay FASTER, not slower. The deep rows that look dangerous
in the raw table are all sparse (avg ~ 1). The critical heaviness `avg*` at which
the extrapolated excess would meet the budget saturates as `w -> inf`:

```text
  avg*  ->  exp(1.465 / 0.2065)  =  1205.
```

Deployed heaviness is far above this: M31-list avg `= 1993678` is ~1.65e3 * avg*
(~3.2 orders of magnitude); the KB rows (avg ~ 6e10) are ~7.7 orders above. So the
deployed rows sit 3-7 orders of magnitude deep in the `R_prim -> 1` regime, and
the de-confounded (w-dependent `beta`) extrapolation returns `R_prim ~ 1.0` at all
four rows. (Fit residuals: max ratio error 2.47x for the full `w + ln(avg) +
ln(p)` model, `R^2 = 0.94`; the naive `w`-free extrapolation instead reports an
alarming `R_prim ~ 197`, precisely because it ignores this confound -- it is the
wrong model, stated here only to name the trap.)

## Structured-family sweep

MEASUREMENT. Constructors do not beat random. On 7 heavy/moderate rows we compared
named structured seed families against the exhaustive primitive max (the true
optimum, not a sample):

```text
  families:   arc[0:m],  AP-step{2,3,5} (where gcd(step,n)=1),  mu2-antipodal (m even)
  rows:       (101,20,2) (61,20,2) (73,24,2) (97,24,3) (73,24,3) (17,16,2) (13,12,2)
```

In every row and every family, the seed's `R_prim_of_seed` is strictly below the
row's exhaustive `R_prim` (worst gap -0.036). The max-ALL winner is always the
symmetric-origin key (`[0,0]` / all-zero), whose members split into quotient +
planted subclasses that are already paid before Q -- e.g. at `(101,20,2)` the
origin cell is 40 primitive + 10 quotient, and that origin cell IS the primitive
max, so structured seeds land in strictly smaller cells. Twist stacking is a
symmetry of the fiber (it permutes members, preserving fiber size), an object
symmetry, not an amplifier.

Coverage note (stated precisely because all three constructor-undershoot reversals
in this program were ours): the baseline is exhaustive, so no family can exceed it
at a probed row by definition; the content is that the winner is a paid cell and
that these named families do not even concentrate mass up to the primitive max.
The residual risk is an unparametrized family; but a winning family would have to
realize a NEW primitive cell larger than the exhaustive primitive max, which does
not exist at these rows.

## Verdict and falsifier

- MEASUREMENT: at the binding M31-list row the budget kappa is 8.4152 (3.0730 bits), recomputed exactly from `prop:q-exact-target`'s own integers. Across 59 exact rows, every heavy row (avg `>= 100`) has measured kappa `= R_prim <= 1.221`, and no avg `>= 1` row reaches 8.4152 (max 7.678, at near-unit heaviness).
- NUMERIC: the measured kappa decays with heaviness; the crossover `avg* ~ 1205` sits 3-7 orders of magnitude below deployed heaviness; de-confounded extrapolation gives kappa `-> 1` at all four deployed rows.
- MEASUREMENT: structured constructors do not beat random/exhaustive; the fiber winners are already-paid quotient/planted cells.
- OPEN (`def:q-row-atom`): the atom conjecture at the M31-list row is SUPPORTED within coverage. **Falsifier**: any row -- structured or random -- with measured kappa `R_prim > 8.4152` at deployed-scale heaviness (avg `>> avg* ~ 1205`, i.e. comparable to the deployed `~2e6`) would refute it. None found within coverage.

## Weave

- **#405** (AllenGrahamHart, concurrent, same hour): independent external calibration on row-sharp Q -- digit-exact replays of the printed max-to-mean collision-gap calibration, a dense-bulk `max/mean-1` ladder to `<=1e-15` at `(1153,128)`, exact `sp_w` top-stratum counts, and a mode-at-null datum at `(41,20,10,2)`. Consistent nulls (no super-polynomial primitive fiber; their `max/mean ~ 1.21` matches our heavy measured kappa cap 1.221). Zero file contact. Ours is the complementary object: the budget-ratio atom `R_Q^max` (= row kappa) at the BINDING row (M31-list vs 8.4152) plus the heaviness-confound decomposition and the constructor sweep; their ladder is on dense-bulk rows, not the budget-ratio atom.
- **#397** (avdeevvadim, open) + integrated first-match ledger (`experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md`): that ledger frames the atom as a required multiplier `K_rem = 4805007` (max primitive Q-fin fiber `<= K_rem * avg`) at KB-MCA; our measurement is the M31-list-row sibling of the same framing (ratio 8.4152). `K_rem = 4805007 < 4807520.93` (the KB-MCA full-budget ceiling of `prop:q-exact-target`), consistent -- first-match payments consume the gap.
- **#402** (scottdhughes, open) NON-CONFLATION: his moment-column `k`-cap (Mersenne reciprocal-gap object) is a different object from the max-fiber atom ratio; this measurement makes no dependency on it.
- **#392** (ours, open): the moment-order floors (`r >= 641593` M31-MCA / `680397` M31-list, `prop:q-moment-order-floor`) explain why fixed / low-order moment routes cannot substitute for this direct max-fiber measurement.
