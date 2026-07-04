# SP-CENSUS: domain-wide split-pair census

- **DAG nodes:** `u1_alpha_active_core_incidence`,
  `u1_beta_band_trade_reduction`, `t_laurent_ritt_toral_stabilizer`.
- **Task:** SP-CENSUS.
- **Status:** EVIDENCE / CENSUS.  This is an exact toy census, not a proof.
- **Verifier:** `experimental/scripts/verify_sp_census_split_pairs.py`.
- **Certificate:**
  `experimental/data/certificates/sp-census-split-pairs/sp_census_split_pairs.json`.

## Scope

The verifier enumerates every ordered disjoint split pair

```text
(Q, P),       |Q| = |P| = h,
e_i(Q) = e_i(P), 1 <= i <= t,
t < h <= floor(log2 n)^2,
h <= n/2.
```

This is domain-wide.  It is deliberately not conditioned on a base locator
`S0`, unlike P-A.  The counts are therefore the raw supply that X-10's
activity filter must compress.

## Charged Classifier

The charged classifier is the X-9 toral normal-form dictionary on `mu_n`:

```text
cyclic:    psi = F(x^m)
dihedral:  psi = F(x^m + alpha x^-m)
```

All domain scalings are included by enumerating the dihedral offset
`alpha`.  A pair is charged only when both `Q` and `P` are unions of fibers for
one common cyclic or dihedral partition in the frozen degree window.

Everything else is recorded as uncharged.  For every uncharged ordered pair,
the certificate stores compact anatomy

```text
[h, Q_mask, P_mask, route_code, defect_degree,
 Q_derivative_zero_mask, P_derivative_zero_mask].
```

Here `route_code=1` means the pair contains a minimal size-`(t+1)` subtrade,
and `route_code=3` means primitive moment/PTE handoff.

## Results

```text
row                    ordered  charged  uncharged  uncharged/n^2
F17 / mu8,  t=3              2        2          0        0.0000
F13 / mu12, t=3             32        8         24        0.1667
F17 / mu16, t=3          1,042       66        976        3.8125
F97 / mu16, t=3             18       18          0        0.0000
F41 / mu20, t=3          5,708      228      5,480       13.7000
F97 / mu24, t=3         30,756      756     30,000       52.0833
```

The small-characteristic warning is visible at fixed `n=16`:

```text
F17 / mu16: 976 uncharged ordered split pairs
F97 / mu16:   0 uncharged ordered split pairs
```

So the raw domain-wide split-pair supply can grow as `q` shrinks.  This does
not falsify A or B by itself: X-10 still needs the activity filter, because
the active theorems count the split pairs actually realized through bases,
cores, or band families.

## Anatomy

The uncharged routes are:

```text
F13 / mu12: all 24 are minimal-subtrade route
F17 / mu16: 224 minimal-subtrade, 752 primitive moment/PTE
F41 / mu20: 360 minimal-subtrade, 5,120 primitive moment/PTE
F97 / mu24: 360 minimal-subtrade, 29,640 primitive moment/PTE
```

Derivative-zero masks are mostly sparse.  For example, at `F97 / mu24`,
`21,168` of the `30,000` uncharged ordered pairs have no domain zero in either
`L_Q'` or `L_P'`; this is the cleanest data route for X-10's derivative
filter.

## Interpretation

The census says the raw split-pair problem is not a simple global
`O(n^2)` count.  The useful statement must be activity-sensitive:

```text
raw split pairs may exceed n^2;
active split pairs after the strip should be budget-bounded,
unless many pairs cluster into the cyclic/dihedral/moment paid columns.
```

This is consistent with P-A and OCC-2: the formal lattice is large, but active
objects were rare in the base-conditioned probes.

## Verification

Run:

```bash
python3 experimental/scripts/verify_sp_census_split_pairs.py
```

The certificate-writing run took about 50 seconds on this machine and peaked
at roughly 362 MB RSS with no swap.
