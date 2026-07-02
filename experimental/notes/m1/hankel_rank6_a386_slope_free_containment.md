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
projective upper bounds in the middle are `18` and `26`, respectively.  The
endpoint-only finite-incidence subranges now have explicit saturation targets:
line six-class saturation has external slack `1..41`, and conic six-class
saturation needs `0..14` forced pair-overlap events before external excess.  A
genuine over-budget witness must also have six distinct finite slopes and an
unpaid endpoint; the strongest remaining pressure cases are line `e_G=72`
near-complete base splitting and conic `e_G=69` almost-complete secants.  The
line `e_G=72` case closes unless all six classes have a base root and at least
five have two; the conic `e_G=69` case closes unless at least `14` of `15`
pair secants occur, forcing at least `16` secant triangles.  Equivalently, line
`e_G=72` survival has base-root histogram `(0,0,6)` or `(0,1,5)`, and conic
`e_G=69` survival has secant graph `K6` or `K6` minus one edge.
Exact degree-`126` accounting leaves line `e_G=72` with either one unused
nonforced external root line or none, and conic `e_G=69` with either `14`
pair-overlaps or all `15`.
Combining the shape and root-budget constraints leaves two line partition
shapes and three conic secant-cover shapes.
Equivalently, the line multiplicity profiles are `(1,312,0)` and `(0,313,0)`,
while the conic multiplicity profiles are `(1,300,15)`, `(0,302,14)`, and
`(0,301,15)`.
The local line singleton sequences are `52^6` or `(53,52^5)`, and the local
conic secant/singleton profiles are `(5^6;50^6)`,
`((4,4,5,5,5,5);(51,51,50,50,50,50))`, or
`(5^6;(51,50,50,50,50,50))`.
Across the full endpoint-only one-over range, the line histogram counts are
`2,16,27,28^6` for `e_G=72..80`, and the conic counts are `2,16,27,28^5`
for `e_G=69..76`.
The packet also records a single-saving closure ledger for all `19` one-over
moving-slope residual rows: line `e_G=72..80`, conic `e_G=69..76`, and the
line/conic punctured-tangent tail at `e_G=120`.

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
