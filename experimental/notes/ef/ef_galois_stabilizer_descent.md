# EF Galois Stabilizer Descent

Status: PROVED.

Source DAG node: `ef_galois_stabilizer_descent`.

## Statement

For the `B`-defined extension-fiber alignment incidence over an admissible
row `B <= E`, every horizontal irreducible component is classified by its
stabilizer under `Gal(E/B)`:

- full stabilizer gives a base-descended component;
- a proper nontrivial stabilizer gives an intermediate-subfield or
  tower-confined component; and
- trivial stabilizer gives the genuinely full-field full-orbit case.

## Proof

Let `G = Gal(E/B)`.  The extension-fiber alignment incidence is defined over
`B`, so `G` acts on its horizontal irreducible components.

For a horizontal irreducible component `X`, let

```text
H = { g in G : gX = X }
```

be its stabilizer, and let `K = E^H` be the fixed field.

If `H = G`, then `X` is invariant under every `B`-automorphism.  Its
homogeneous ideal is `G`-stable, so by Galois descent it has equations over
`B`.  This is the base-descended case.

If `H` is a proper nontrivial subgroup, then the same descent argument gives
equations over the intermediate fixed field `K`, with `B < K < E`.  Thus the
component is confined to an intermediate subfield and belongs to the tower
case.

If `H` is trivial, then the orbit of `X` has full size `|G|`.  This is exactly
the genuinely full-field case not explained by base descent or tower
confinement.

These alternatives are exhaustive by the Galois correspondence.  Therefore the
only horizontal component class not already base-descended or
subfield-confined is the full-orbit case routed to the pole-forcing branch.

## Non-Claims

This packet does not exclude the full-orbit case.  It only proves the
stabilizer trichotomy that routes components to base, tower, or full-orbit
cases.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_ef_galois_stabilizer_descent.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_ef_galois_stabilizer_descent.py \
  --check experimental/data/certificates/ef-galois-stabilizer-descent/ef_galois_stabilizer_descent.json
```

The verifier checks the proof-note anchors and the cyclic-subgroup trichotomy
for small extension degrees.
