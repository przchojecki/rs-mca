# Corank-Stratified SPI Eliminant Ledger

## Claim

The packet records finite corank-at-least-two Hankel-pencil strata with
nonzero eliminants and exact split-locator occupancy. The recorded rows include
aperiodic occupants, reported as named finite obstruction templates.

## Status

EXPERIMENTAL / AUDIT. This is a finite ledger and obstruction-template packet,
not a full classification of corank-at-least-two charts.

## Parameters

- Prime fields `F_7`, `F_11`, `F_13`, and `F_17`.
- `q_gen = q_line = q_chal = p` in every row.
- Domains are multiplicative subgroups `mu_n <= F_p^*`.
- Each row records a Hankel pencil whose rank drops to corank at least two at
  a finite slope.

## Existing Paper Dependency

This is a finite ledger for the corank-at-least-two SPI eliminant branch left
outside the corank-one analysis.

## Proof Idea Or Experiment

For each row, the scanner constructs a pencil `H_0 + Z H_1` whose rank drops
at the recorded finite slope. The ledger records the constructed nonzero
polynomial `Q(Z)=Z-z0` and its `deg gcd(Q, Z^q - Z)` contribution; it does
not derive `Q` by resultant or Groebner elimination. At each
corank-at-least-two slope, every split locator in `Dloc_j(mu_n)` is tested
against the kernel equations and tagged by periodicity scale.

The verifier rebuilds the Hankel matrices, recomputes ranks at every finite
slope, checks the eliminant contribution, and re-enumerates all occupants.

The committed scanner uses exact CPU enumeration for these small rows. It does
not implement a CuPy or RawKernel accelerator path.

## Ledger Impact

The packet supplies finite corank-at-least-two rows with explicit aperiodic
occupants. These are obstruction templates for the residual chart family, not
a proof that such templates survive in the full parameter range.

## Constants

```text
F_7,n=6,j=2
F_11,n=10,j=2
F_13,n=12,j=2
F_17,n=16,j=3
```

The `F_17` row is the split-locator oracle gate.

In that row the recorded drop is exactly corank three, and the recorded
eliminant is the radical for the finite-slope contribution, not the minor-gcd.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/corank_stratified_spi_eliminant.py --emit-defaults
py -3.13 experimental/scripts/verify_corank_spi_eliminant.py --check experimental/data/certificates/corank-spi-eliminant/corank_spi_rows.json
```

## Non-Claims

This does not classify all corank-at-least-two charts, does not prove an
asymptotic incidence theorem, and does not resolve `prob:band`.
