# DLI Artin-Schreier Conductor Criterion

Status: PROVED.

Source DAG node: `dli_artin_schreier_conductor_criterion`.

## Statement

Let `f` be a rational additive phase on a smooth curve component in
characteristic `p`. The associated Artin-Schreier trace sheaf is
geometrically trivial exactly when

```text
f = g^p - g + c
```

for some rational function `g` and constant `c` over the geometric field. If
`f` is not of this form, then after Artin-Schreier reduction its conductor is
bounded by the reduced polar divisor of `f`, up to the fixed component
bookkeeping constants.

## Proof

Fix a smooth curve component `C` over a field of characteristic `p`, and a
rational function `f` in its function field. The additive phase used in the
DLI Weyl sums is the trace function of the Artin-Schreier sheaf
`L_psi(f)`.

Artin-Schreier sheaves satisfy the standard geometric equivalence

```text
L_psi(f) is geometrically trivial
    iff f = g^p - g + c.
```

Subtracting a coboundary `g^p - g` gives an isomorphic additive local system,
and the constant phase is geometrically trivial up to a scalar trace. Conversely,
a geometrically trivial Artin-Schreier torsor represents the zero class in the
geometric quotient by `Frob - 1`, modulo constants, so it has this form.

For a nontrivial class, choose an Artin-Schreier-reduced representative, meaning
that no remaining polar order is divisible by `p`. At each pole, the local Swan
conductor is the reduced pole order. Away from the reduced polar divisor and
the fixed singular/component bookkeeping points there is no additional
ramification. Thus the global conductor is controlled by the reduced polar
divisor plus the fixed bookkeeping constants.

This is the criterion consumed by the DLI odd-phase packets: nontriviality is
certified by ruling out the form `g^p - g + c`, and conductor size is certified
by bounding the reduced polar divisor.

## Non-Claims

This packet proves the local Artin-Schreier/conductor criterion only. It does
not construct a DLI reduced-phase manifest, does not verify a deployed row, and
does not prove the remaining harmonic conductor ledger.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_artin_schreier_conductor_criterion.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_artin_schreier_conductor_criterion.py \
  --check experimental/data/certificates/dli-artin-schreier-conductor-criterion/dli_artin_schreier_conductor_criterion.json
```

The verifier checks note anchors and a finite-field sanity case showing that
`g^p - g + c` has constant additive trace over `F_p`.
