# M1 root-slice lift

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts the first local lemma from the broad same-slope packet in
PR #138, following the triage request in
`experimental/notes/triage/pr-triage-2026-06-30.md`.  The purpose is to make
one reviewable M1 building block: same-slope one-exchange collisions in the
Hankel-pencil normal form are root-slice phenomena, and those slices lift to a
higher-slack Hankel core.

## Scope and non-claims

This is local algebra inside the Hankel-pencil normal form.  It does not prove
the all-line M1 aperiodic local limit, does not bound the residual aperiodic
slope image, and does not add a leaderboard or threshold row.

Field ledger: the lemma is over an arbitrary field `F`.  In an MCA application
the slope `z` is a finite line slope in `q_line`; no generated-field,
challenge-field, denominator, or endpoint convention is used by this local
step.  The active noncontainment condition is a separate filter and is not used
in the root-slice forcing argument.

## Setup

Let `D subset F`, fix complement size `j`, slack `t`, and work with the
finite-slope Hankel-pencil map

```text
L_z = H_{t,j}(u) + z H_{t,j}(v).
```

Thus a split complement `T` with monic locator `ell_T` satisfies the finite
slope equation when

```text
L_z ell_T = 0.
```

Fix a `(j-1)`-core `R` with locator `ell_R`.  A one-root extension by `x` has

```text
T_x = R union {x},        ell_{T_x} = (X-x) ell_R.
```

When applying this to split complements in `D`, take `x in D\R`.  The algebraic
identity below holds for every scalar `x in F`.

## Lemma: same-slope one-exchange root slice

Suppose `x != y` and the two one-root extensions through the same core satisfy

```text
L_z ell_{T_x} = 0,
L_z ell_{T_y} = 0.
```

Then

```text
L_z ell_R = 0,
L_z (X ell_R) = 0.
```

Consequently

```text
L_z ell_{T_a} = 0        for every a in F.
```

So every same-slope one-exchange edge is contained in the full fixed-slope
root slice through its common `(j-1)`-core.

### Proof

Since

```text
ell_{T_a} = (X-a)ell_R = X ell_R - a ell_R,
```

subtracting the two endpoint equations gives

```text
0 = L_z(ell_{T_y} - ell_{T_x})
  = (x-y) L_z ell_R.
```

As `x-y != 0`, this implies `L_z ell_R = 0`.  Substituting into either endpoint
equation gives

```text
0 = L_z(X ell_R - x ell_R) = L_z(X ell_R).
```

Therefore, for every scalar `a`,

```text
L_z ell_{T_a}
  = L_z(X ell_R - a ell_R)
  = L_z(X ell_R) - a L_z ell_R
  = 0.
```

This proves the root-slice claim.

## Higher-slack Hankel lift

Put

```text
w_z = u + z v.
```

The two equations from the root-slice lemma can be read as padded
`H_{t,j}(w_z)` equations:

```text
H_{t,j}(w_z)(ell_R, 0) = 0,
H_{t,j}(w_z)(0, ell_R) = 0.
```

These are equivalent to the lifted Hankel-core equation

```text
H_{t+1,j-1}(w_z) ell_R = 0.                         (RSLIFT)
```

Indeed, the first padded equation gives rows `0,...,t-1` of `(RSLIFT)`, while
the second padded equation gives rows `1,...,t`.  Conversely, the lifted
equation gives both padded equations by the same row identities.

Thus a fixed-slope root slice is not a new residual `t`-level aperiodic
multiplicity.  It is charged to the higher-slack `(t+1,j-1)` Hankel core at the
same finite slope.

## Residual use in M1

After fixed-slope root slices have been charged or removed, the residual
one-exchange graph has no same-slope one-exchange edges.  Any remaining
one-exchange edge belongs to the different-slope ledger or to later packet
structure.  This is exactly the first split requested by the June 30 triage:
it isolates root-slice charging before the rank-defect packet normal form and
before any Kummer or endpoint gates.

## Verification

The companion verifier checks the coefficient identities and the Hankel-row
lift over sampled prime fields:

```sh
python3 experimental/scripts/verify_m1_root_slice_lift.py
```
