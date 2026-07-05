# DLI Odd-Phase Polar Obstruction Soundness

Status: PROVED.

Source DAG node: `dli_odd_phase_polar_obstruction_soundness`.

## Statement

For each actual DLI odd-evaluation phase on each relevant square-root
component, suppose a certificate identifies a pole of the
Artin-Schreier-reduced phase with positive order not divisible by `p`. Then
the phase is not of Artin-Schreier form

```text
g^p - g + c.
```

## Proof

Fix one smooth square-root component and one actual DLI odd-evaluation phase
`f = P_lambda(sigma(y))`.

By `dli_artin_schreier_conductor_criterion`, the geometrically trivial
Artin-Schreier classes are exactly the rational functions of the form
`g^p - g + c`. After subtracting Artin-Schreier coboundaries, such a class
has a constant reduced representative and hence no positive reduced polar
divisor.

Locally, the leading polar terms of a raw coboundary `g^p - g` have order
divisible by `p`. Artin-Schreier reduction removes those `p`-divisible leading
polar terms until the representative is reduced. Therefore a positive pole in
the reduced representative whose order is not divisible by `p` proves that the
reduced representative is nonconstant.

Thus the certified reduced pole excludes the form `g^p - g + c`. Applying the
same local argument to every certified DLI tuple gives non-Artin-Schreier
triviality for every corresponding odd-evaluation phase.

## Non-Claims

This packet proves certificate soundness for a supplied reduced-pole
obstruction. It does not construct the reduced-phase manifest, enumerate the
DLI tuple universe, or prove the harmonic conductor budget.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_odd_phase_polar_obstruction_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_odd_phase_polar_obstruction_soundness.py \
  --check experimental/data/certificates/dli-odd-phase-polar-obstruction-soundness/dli_odd_phase_polar_obstruction_soundness.json
```

The verifier checks note anchors and the elementary reduced-pole predicate used
by the certificate format.
