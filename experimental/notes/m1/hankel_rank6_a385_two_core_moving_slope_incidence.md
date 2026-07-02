# Hankel Rank-6 A385 Two-Core Moving-Slope Incidence

Status: PROVED / AUDIT.

This note records the first incidence budget for the remaining fixed two-core
moving-slope residual at

```text
A = 385.
```

It consumes

```text
experimental/notes/m1/hankel_rank6_a385_two_core_global_component_slope_dichotomy.md
experimental/notes/m1/hankel_rank6_a385_two_core_slope_free_empty.md
```

and does not close the high-core moving-slope branch.

After a fixed forced two-point base core is factored, write

```text
Q = E R,       deg R < 3.
```

The residual space is a projective plane.  Let `G` be an irreducible
positive-dimensional moving-slope component in that plane, of degree

```text
c in {1,2}.
```

For each subgroup point `s`, put

```text
E_s = { R : L_{E R}(s) = 0 }.
```

The split-locator gate asks for `L_{E R}` to normalize to a monic degree-`127`
divisor of `X^512-1`.

The map

```text
R |-> L_{E R}
```

is injective.  If `L_{E R}=0`, then on the base support `X`,

```text
E(x)R(x)=0.
```

Outside the two fixed core nodes, `E(x)` is nonzero, so `R` has `126` roots.
Since `deg R<3`, this forces `R=0`.

On the base support, every candidate has the two fixed core roots, and nonzero
`R` contributes at most two further base roots.  Thus a valid degree-`127`
split locator has at most four base-support roots.  If `e_G` external roots
are forced along the whole component, then every valid class on `G` still needs

```text
123 - e_G
```

additional non-forced external roots.

Each non-forced external root hyperplane cuts `G` in length at most `c`.  Hence
for `e_G<123`,

```text
# valid Q-classes on G <= floor( c(384-e_G)/(123-e_G) ).
```

For a line component, this gives

```text
e_G <= 70  =>  at most 5 finite classes;
e_G <= 79  =>  at most 6 finite classes.
```

After adding the endpoint-uniform contribution, line components with
`e_G<=70` are projective-budget safe.  The line one-over diagnostic range left
by incidence alone is

```text
71 <= e_G <= 79.
```

For an irreducible conic, the simple incidence bound is one short at
`e_G=0`, so the same pair-overlap packing used in the `A=386` branch is
needed.  Two distinct `Q`-classes on an irreducible conic share at most one
non-forced external root line.  Therefore `M` valid classes, each requiring
`R=123-e_G` non-forced external roots, use at least

```text
M R - binomial(M,2)
```

external root lines.  Since only `384-e_G` are available, six classes are
impossible for `e_G<=67`, and seven classes are impossible for `e_G<=75`.
Thus irreducible conic components with `e_G<=67` are projective-budget safe;
the conic one-over diagnostic range left by incidence alone is

```text
68 <= e_G <= 75.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_moving_slope_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json
```

Nonclaims:

```text
no closure of the full fixed two-core nonconstant moving-slope branch;
no A385 high-core product-collapse theorem;
no proof that high-core quotient diagnostics are empty or paid;
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment theorem, only endpoint-budget accounting;
no row-level M3 safe-side bound.
```
