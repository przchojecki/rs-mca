# SPI Component-Control Packet

- **Status:** PROVED / component inventory.
- **DAG node:** `spi_component_control`.
- **Certificate:** `experimental/data/certificates/spi-component-control/spi_component_control.json`.
- **Verifier:** `python3 experimental/scripts/verify_spi_component_control_packet.py --check experimental/data/certificates/spi-component-control/spi_component_control.json`.

This packet records the effective component-control input for the SPI
alignment-incidence route. It is a scroll/component inventory theorem, not a
point-counting theorem.

## Claim

For the Hankel alignment pencil

```text
M(Z) = Z0 M_u + Z1 M_v,
I_{u,v} = { (Z, [l]) in P^1 x P^j : M(Z) l = 0 },
```

let `r` be the generic rank over `K(Z)`. A nonzero `r x r` minor
`Delta(Z)` has degree at most `r`, because every matrix entry is linear in
`Z`, and `r <= t`.

On the open set `{Delta != 0}`, the kernel is a projective bundle over an
irreducible rational base. Its closure is one horizontal scroll, with Segre
degree at most `j + 1`.

Every other component lies over the rank-drop locus `{Delta = 0}`. That locus
has at most `r <= t` slopes, and over each such slope the extra kernel is a
single linear space.

Therefore

```text
#Irr(I_{u,v}) <= t + 1,
Segre degree <= j + t + 1.
```

The same bound applies after restriction to a paid stratum presented as
polynomially many algebraic families in locator-coefficient space.

## Verification Boundary

The working record checked `2500` random `F_17` Hankel pencils with `t=3` and
`j=4`; in every case the number of rational rank-drop slopes was at most the
generic rank `r`, with worst observed count `1` and bound `r=3`.

## DAG Use

`spi_exceptional_class` consumes this packet as its component inventory input.
The later classification separates the generic row-full horizontal component
from vertical rank-drop fibers and row-deficient horizontal scrolls.

## Non-Claims

- This packet does not count `D_j` points on the generic horizontal scroll.
- This packet does not classify exceptional components as paid or empty.
- This packet does not enumerate supports; paid strata must be algebraic
  locator-coefficient families.
- This packet does not edit Papers A-D.
