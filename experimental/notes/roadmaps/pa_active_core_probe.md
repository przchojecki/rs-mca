# P-A: active-core probe

- **DAG node:** `u1_alpha_active_core_incidence`.
- **Task:** P-A.
- **Status:** EVIDENCE / PROBE.  This calibrates the active-core incidence
  theorem; it is not a proof.
- **Verifier:** `experimental/scripts/verify_pa_active_core_probe.py`.
- **Certificate:**
  `experimental/data/certificates/pa-active-core-probe/pa_active_core_probe.json`.

## Definition Used

For a base locator `S0` and a same-top-`t` target locator `S`, write the
canonical star trade as

```text
S0 = C union Q,
S  = C union P.
```

The minimal full-fiber band is

```text
|P| = |Q| = h = t+1.
```

In this band the same-top condition is exactly

```text
e_r(P) = e_r(Q),      1 <= r <= t,
```

so the monic degree-`h` locator polynomials `L_P` and `L_Q` differ only in
their constant term.  Thus each fixed `Q subset S0` is a full-fiber core in
the sense of `u1_alpha_active_core_incidence`.

The probe calls a core active when it admits at least one minimal full-fiber
trade not charged by H1's explicit v1 quotient/dihedral filters.  Its
multiplicity is

```text
K_Q = #{P : (P,Q) is such a sporadic minimal full-fiber trade}.
```

## Results

The strongest observed values over all H1 toy rows are:

```text
max active cores per base:                 6
max K_Q:                                   2
max (active cores)*(max K_Q):              6
max total sporadic minimal trades/base:    6
```

The largest budget ratio is tiny:

```text
max (active cores)*(max K_Q)/n^2 = 4/256 = 0.015625
```

or, using total sporadic minimal trades per base,

```text
max total/n^2 = 6/400 = 0.015.
```

Representative row summaries:

```text
F17/mu16, A=8:  max active=4, max K_Q=2, mass=4, n^2=256
F41/mu20, A=8:  max active=5, max K_Q=1, mass=5, n^2=400
F41/mu20, A=10: max active=6, max K_Q=1, mass=6, n^2=400
F97/mu24, A=8:  max active=3, max K_Q=1, mass=3, n^2=576
```

Rows over larger characteristic often have no sporadic active cores at all:

```text
F17/mu8, A=4: 0 active bases
F97/mu16, A=8: 0 active bases
```

## Interpretation

No toy base comes close to the `n^2` budget.  The active-core distribution is
not driven by large per-core multiplicity: `K_Q` is almost always `1`, and
the maximum observed value is `2`.  The incidence theorem should therefore
focus first on bounding the number of active cores, with multiplicity treated
as a secondary or energy-level correction.

The observed scaling is much smaller than linear in `n` at these rows:

```text
max active cores / n <= 6/20 = 0.3.
```

This suggests the decomposition seed for `u1_alpha_active_core_incidence`:

1. control active-core support in the base `S0`;
2. separately rule out high-multiplicity cores `K_Q >> 1`;
3. use shared-toral/pullback structure as the escape route if many cores turn
   active simultaneously.

## Verification

Run:

```bash
python3 experimental/scripts/verify_pa_active_core_probe.py
```

To refresh the pinned certificate:

```bash
python3 experimental/scripts/verify_pa_active_core_probe.py --write-certificate
```
