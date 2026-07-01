# F17^32 M3 Rank-6 A386 Global-Component Slope Dichotomy

Status: PROVED / AUDIT.

This packet refines the residual left after the `A=386` component-cut packet.
It applies to an irreducible component `G` in the `Q`-plane contained in all
pairwise direction-consistency conics.

For each direction node `y`, write

```text
N_y(Q) = Omega_y Q(y),
D_y(Q) = b_y L_Q(y).
```

Both are linear forms in the projective `Q`-plane, and finite consistency is

```text
z D_y(Q) = N_y(Q)
```

for all six direction nodes.  The pairwise consistency conics are

```text
N_y D_y' - N_y' D_y = 0.
```

If some pair `(N_y,D_y)` is not identically zero on `G`, then `[N_y:D_y]`
defines a rational projective slope map on `G`, independent of `y` on common
domains of definition.  If this map is constant, the non-base part of `G`
contributes at most one finite slope; the endpoint-uniform theorem adds at
most one projective endpoint, so that non-base branch has total at most

```text
1 + 1 = 2 <= 6.
```

The remaining residuals are now explicit:

```text
determined nonconstant slope map;
slope-free base locus or global component, where all six pairs (N_y,D_y) vanish.
```

The companion packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/
```

filters the displayed slope-free transfer vectors: they satisfy
`H(v)L_Q=H(u)L_Q=0`, hence fail finite and projective noncontainment gates.

The next companion packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/
```

applies the split-locator divisor gate to the moving-slope component.  It
uses the base-support fact that nonzero `Q` has at most two roots on `X` and
closes line components whose forced external split-root core has size at most
`71` in projective accounting.  For irreducible conics, pair-overlap packing
closes forced external core up to `68`; large-external-core lines and conics
remain residual.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_global_component_slope_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json
```

Nonclaims:

```text
does not prove all global components have constant slope;
does not close moving-slope global components;
does not close slope-free base points or global components;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
