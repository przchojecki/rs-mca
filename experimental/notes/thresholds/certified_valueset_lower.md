# Certified Valueset Lower

Status: PROVED.

Source DAG node: `certified_valueset_lower`.

## Statement

For a knife-edge row with row prime `p`, a certificate exhibits a quotient-class
family `F` with

```text
|F| > B*
```

and proves that the map

```text
B |-> e1(B) mod p
```

is injective on `F`.  Therefore

```text
|{e1(B) mod p : B in F}| > B*.
```

This is the value-set lower bound needed by the knife-edge census.

## Dependency Sub-DAG

Generator-design route:

```text
graded_collision_radius -> certified_valueset_lower
far_pair_separation     -> certified_valueset_lower
certifier_uniformity    -> certified_valueset_lower
```

Alternative lattice route:

```text
kernel_lattice_reframing -> lattice_cone_certificate
weight_graded_mitm       -> lattice_cone_certificate
integer_code_distance_cert -> lattice_cone_certificate
lattice_cone_certificate -> certified_valueset_lower
lattice_cone_certificate -> certifier_uniformity
```

The integrated prize DAG marks all named predicates above as `PROVED`.  The
generator-design route is enough for the assembly; the lattice route is a
separate certificate path that can certify full injectivity of the row cell
directly.

## Proof

The target is a lower bound on a value set.  It is enough to certify a family
`F` whose image under `e1 mod p` is pairwise distinct and whose size exceeds
`B*`.

The generator-design route supplies this as follows.  The
`graded_collision_radius` predicate certifies local collision-freeness: pairs
inside the small swap-radius cells have nonzero `e1` difference whose norm is
below `p`, so they cannot collide modulo `p`.  The `far_pair_separation`
predicate supplies a large family whose cross-cell differences reduce to a
polynomial list of generator checks.  The `certifier_uniformity` predicate
ensures that those finite row checks are emitted as proof-producing
certificates, not empirical samples.

Thus every pair of distinct classes in `F` has distinct `e1` value modulo `p`.
Since `|F| > B*`, the image value set has size at least `|F|`, hence is larger
than `B*`.

On the alternative route, `lattice_cone_certificate` proves directly that the
row kernel has no forbidden sparse ternary vector beyond the cyclotomic
relations.  That is exactly the same injectivity conclusion on the relevant
row cell; the lower bound then follows from the exact cell count.

## Non-Claims

This packet is an assembly certificate.  It does not print a deployed row
family, does not run lattice enumeration, does not count primes inside census
windows, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_certified_valueset_lower.py --emit
python3 experimental/scripts/verify_certified_valueset_lower.py \
  --check experimental/data/certificates/certified-valueset-lower/certified_valueset_lower.json
```
