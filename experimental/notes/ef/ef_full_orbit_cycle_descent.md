# EF Full-Orbit Cycle Descent

Status: PROVED.

Source DAG node: `ef_full_orbit_cycle_descent`.

## Statement

In the `B`-defined extension-fiber alignment incidence, with the extension-pole
divisor also defined over `B`, any full Galois orbit of horizontal components
avoiding the pole divisor has a `B`-defined reduced cycle as its union.  That
reduced cycle is still disjoint from the pole divisor.

## Proof

Let `X` be the extension-fiber alignment incidence over the base field `B`, and
let `D` be the extension-pole divisor.  Both `X` and `D` are defined over `B`.
Let `G = Gal(E/B)`.

Take a horizontal irreducible component `C` whose stabilizer in `G` is trivial,
so its conjugates form a full orbit

```text
O(C) = { gC : g in G }.
```

The reduced union

```text
Z = union_{g in G} gC
```

is stable under `G`, because applying any `h in G` only permutes the orbit:

```text
hZ = union_{g in G} hgC = union_{g in G} gC = Z.
```

For a finite Galois extension, a reduced closed subscheme of a variety defined
over `E` that is stable under `Gal(E/B)` descends to a reduced closed subscheme
over `B`: equivalently, its radical ideal is `G`-stable and hence is generated
by its descended `B`-ideal after base change.  Thus `Z` is a `B`-defined reduced
horizontal cycle.

Now assume each conjugate component avoids the pole divisor.  Since `D` is
`B`-defined, `gD = D` for every `g in G`.  If `C` is disjoint from `D`, then each
`gC` is also disjoint from `D`; their finite union is therefore disjoint from
`D`.

Hence any full Galois orbit avoiding the pole divisor descends to a `B`-defined
reduced horizontal cycle in the pole complement.

## Non-Claims

This packet does not exclude pole-free descended cycles.  It only proves that
the full-orbit branch descends to a `B`-defined cycle which can then be handled
by the descended-cycle classification payload.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_ef_full_orbit_cycle_descent.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_full_orbit_cycle_descent.py \
  --check experimental/data/certificates/ef-full-orbit-cycle-descent/ef_full_orbit_cycle_descent.json
```

The verifier checks the proof-note anchors and finite orbit-permutation
samples.
