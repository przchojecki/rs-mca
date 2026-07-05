# Exact Counting Frame Packet

- **Status:** PROVED / finite locator-slope frame.
- **DAG node:** `counting_frame`.
- **Certificate:** `experimental/data/certificates/counting-frame/counting_frame.json`.
- **Verifier:** `python3 experimental/scripts/verify_counting_frame_packet.py --check experimental/data/certificates/counting-frame/counting_frame.json`.

This packet records the exact counting frame used by the v10 Hankel/MCA
safe-side ledger: the divisor/locator set is finite, the slope condition is a
linear pencil, and each nondegenerate locator contributes at most one finite
slope.

## Claim

For an evaluation domain of size `n` and exact-agreement complement size `j`,
the possible support locators are indexed by a finite divisor set of size

```text
binom(n, j).
```

For each fixed locator, the Hankel/VTDV setup gives a linear finite-slope
pencil

```text
A + z B = 0.
```

The noncontainment packet identifies the all-slope case as the degenerate
endpoint pencil `A=B=0`; this case is removed before finite-slope counting.
After that removal, the V8 ledger gives at most one finite slope per fixed
locator.

Therefore the counting frame is exact:

```text
finite noncontained slope events inject into the finite locator/divisor set.
```

## Dependency Boundary

This branch carries the local dependencies `v8_ledger` and
`noncontain_degeneracy`. The VTDV Hankel factorization dependency is packaged
separately in PR #317 (`codex/vendor-vtdv-fm1`), and the F1 pencil-normal-form
material already exists upstream under `experimental/notes/f1/`.

## DAG Use

`mca_safe` consumes this counting frame as the bookkeeping layer before paid
ledgers and aperiodic residual bounds are applied. This packet does not decide
which locators occur; it supplies the exact finite frame in which later
certificates count or eliminate them.

## Non-Claims

- This packet does not count root tables for the `F_17^32` M3/M4 window.
- This packet does not classify locators as tangent, quotient, extension, or
  aperiodic.
- This packet depends on the VTDV factorization packet in PR #317.
- This packet does not edit Papers A-D.
