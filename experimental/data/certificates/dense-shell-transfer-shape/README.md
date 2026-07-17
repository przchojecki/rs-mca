# Dense-shell transfer-shape certificate

This directory contains the deterministic certificate for
`experimental/notes/thresholds/dense_shell_transfer_shape.md`.

The verifier proves the finite obligations used by the symbolic all-depth
induction:

1. direct-tree/model and shifted-Chebyshev convention consistency;
2. the exact machine-readable consumer contract and all scalar closure
   inequalities;
3. the positive two-state shape base at level 25 and curvature base at 26;
4. TS1--TS3 on every finite level `5 <= n <= 26`;
5. a parameter neighborhood of radius `1/100000` around both auxiliary
   cone parameters.

The top curvature coordinate is handled by the exact identity printed in the
proof note, not omitted as a numerical assumption.

## Replay

```bash
python -m pip install "python-flint==0.9.0"
python experimental/scripts/replay_dense_shell_transfer_shape.py
```

The wrapper checks the detailed deterministic certificate, runs the semantic
tamper suite, compiles all participating scripts, replays the deep
class-charge consumer, validates JSON, and checks artifact hashes.  The
tamper suite deliberately strengthens or corrupts eight theorem inputs and
requires every mutation to fail.

Each successful certificate gate prints its certified bounds and worst cell,
rather than only a summary Boolean.  The exact tested dependency version is
part of the certificate payload.

## Scope

The certificate discharges `INV-TAIL` and makes the existing `|K| <= 1`
dense-shell master unconditional at every depth.  It does not prove the
general decorated-subtree charge `T_pi(K) > 0` for `|K| >= 2`, product-profile
admission, hard input 2, or a reserve payment.
