# Hankel Rank-6 A386 Slope-Free Containment

Status: PROVED / AUDIT.

This note records a containment filter for the slope-free part of the
separated rank-6 boundary at

```text
A = 386.
```

It consumes the low-degree transfer and the global-component slope-map
dichotomy.  It does not close the moving-slope residual.

At `A=386`, the transfer writes every boundary ambient kernel vector in terms
of a degree-`<3` auxiliary polynomial `Q`.  The associated polynomial `L_Q` is
defined by interpolation on the base support:

```text
a_x L_Q(x) = Omega_x Q(x),        x in X.
```

For each direction node `y`, put

```text
N_y(Q) = Omega_y Q(y),
D_y(Q) = b_y L_Q(y).
```

The slope-free condition is

```text
N_y(Q)=0 and D_y(Q)=0        for every y in Y.
```

Under this condition,

```text
H(v)L_Q = (sum_y b_y L_Q(y)y^a)_a = 0,
```

because every coefficient `b_y L_Q(y)=D_y(Q)` is zero.  Also

```text
H(u)L_Q = (sum_x a_x L_Q(x)x^a)_a = 0.
```

Indeed, the vector `(Omega_s Q(s))_{s in X union Y}` is in the first-`t`
Vandermonde nullspace by the low-degree transfer, and the direction part
vanishes because `N_y(Q)=0` for every `y`.

Therefore, for every finite slope `z`,

```text
H(u+zv)L_Q = 0,        H(v)L_Q = 0.
```

The displayed slope-free vector is an ambient kernel vector, but it fails the
finite-affine support-wise noncontainment gate.  It is in the contained branch
of the M5 finite-affine kernel chart.

At projective infinity the same vector also fails the endpoint gate:

```text
H(v)L_Q = 0,        H(u)L_Q = 0,
```

where an endpoint witness would require `H(u)L_Q != 0`.

Consequently slope-free transfer vectors contribute zero finite support-wise
noncontained slopes and zero projective endpoint witnesses.  This statement is
about the displayed vector.  If the same finite slope also has another
independent kernel vector with `H(v)ell != 0`, that other vector is outside
this slope-free filter and must be counted by another branch.

The moving-slope companion

```text
experimental/notes/m1/hankel_rank6_a386_moving_slope_split_incidence.md
```

handles the next non-slope-free branch by counting split-root hyperplane
incidences on the moving component, using the base-support cap that nonzero
`Q` has at most two roots on `X`.  It closes line components with forced
external split-root core `e_G<=71`.  A conic pair-overlap packing step closes
irreducible conics with `e_G<=68`; large-external-core lines and conics remain
residual but have sharper quotient structure.  A high-core line is a
dual-evaluation-fiber quotient pencil of degree at most `54`, while a high-core
irreducible conic has a global common forced core across the whole `Q`-plane
and becomes a quotient family of degree at most `57`.  After deleting the
forced core, those quotient branches lie in the very-high-agreement tangent
range of the punctured row.  The projective tangent staircase closes the tail
`e_G>=121`; the intermediate ranges `72<=e_G<=120` for lines and
`69<=e_G<=120` for irreducible conics remain unclosed.  The current projective
proof envelope is only one over budget for line cores `72<=e_G<=80` and
`e_G=120`, and for conic cores `69<=e_G<=76` and `e_G=120`; the worst current
projective upper bounds in the middle are `18` and `26`, respectively.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_slope_free_containment.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json
```

Nonclaims:

```text
no closure of nonconstant moving-slope components;
no exclusion of another independent noncontained vector at the same finite slope;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
