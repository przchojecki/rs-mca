# Hankel Rank-6 A386 Moving-Slope Split Incidence

Status: PROVED / AUDIT.

This note records a split-locator incidence budget for the remaining
moving-slope part of the separated rank-6 boundary at

```text
A = 386.
```

It consumes the global-component slope dichotomy and the slope-free containment
filter.  It does not close every moving-slope component.

At `A=386`, the low-degree transfer gives

```text
j = 126,       h = 3,       [Q] in P^2.
```

For a moving-slope residual component `G` in the `Q`-plane, write

```text
L_Q
```

for the interpolated degree-`<127` kernel polynomial.  For each subgroup point
`s in H`, define the root hyperplane

```text
E_s = { Q : L_Q(s) = 0 }.
```

The split-locator gate requires `L_Q` to normalize to a monic degree-`126`
divisor of `X^512-1`.  Thus a valid `Q` must lie on root hyperplanes for at
least `126` subgroup points.

Let `G` be an irreducible positive-dimensional component of degree

```text
c in {1,2}.
```

Let `r_G` be the forced split-root core: the number of subgroup points `s` for
which

```text
G subset E_s.
```

The base interpolation map `Q -> L_Q` is injective.  Indeed, if `L_Q=0`, then
`Q` vanishes on the base support `X`, which has size `127`; since `deg Q<3`,
this forces `Q=0`.  Consequently a positive-dimensional component cannot have
`r_G >= 126`: all `L_Q` would then be scalar multiples of the same degree-126
divisor, contradicting projective injectivity.

For `r_G < 126`, each valid split locator on `G` needs at least

```text
126 - r_G
```

additional intersections with the non-forced root hyperplanes.  Every
non-forced root hyperplane cuts `G` in length at most `c` by Bezout.  Therefore
the number of valid `Q`-classes on `G`, and hence the number of finite slopes
represented by this component, is at most

```text
floor( c (512-r_G) / (126-r_G) ).
```

This first incidence budget is useful, but it ignores an extra feature of the
base support.  On `X`,

```text
a_x L_Q(x) = Omega_x Q(x),
```

with nonzero `a_x` and `Omega_x`.  Hence `L_Q(x)=0` on `X` exactly when
`Q(x)=0`.  Since `Q` is a nonzero polynomial of degree `<3`, a valid `Q` has
at most two roots on the base support.

Let `e_G` be the forced split-root core outside `X`, among the `385` external
subgroup points.  A valid degree-`126` split locator must then obtain at least

```text
124 - e_G
```

additional roots outside `X`.  If `e_G<124`, the external root hyperplanes give
the sharper bound

```text
finite Q-classes on G <= floor( c (385-e_G) / (124-e_G) ).
```

This gives the projective-safe line criterion:

```text
c = 1 and e_G <= 71
  => finite slopes <= 5,
     endpoint contribution = 1,
     total projective contribution <= 6.
```

The finite-only line criterion is slightly weaker:

```text
c = 1 and e_G <= 80
  => finite slopes <= 6.
```

For an irreducible conic component (`c=2`), the base-sharpened incidence budget
is close but not enough by itself: at `e_G=0` it gives `floor(770/124)=6`
finite `Q`-classes, and the endpoint would give total `7`.  The missing saving
comes from pair overlap.  Two distinct `Q`-classes on an irreducible conic can
share at most one non-forced external root hyperplane; otherwise two distinct
lines `E_s,E_t` would both pass through the same two points.

Thus, if there are `M` valid `Q`-classes on the conic and each requires
`R=124-e_G` non-forced external roots, the union of their external root lines
has size at least

```text
M R - binomial(M,2).
```

Only `385-e_G` non-forced external root lines are available.  Six valid
`Q`-classes are therefore impossible for `e_G<=68`, and seven valid
`Q`-classes are impossible for `e_G<=76`.  Hence

```text
c = 2 and e_G <= 68
  => finite slopes <= 5,
     endpoint contribution = 1,
     total projective contribution <= 6.
```

Irreducible conics with `e_G>=69` remain residual unless a sharper
split-locator, paid-ledger, or exact-root-table argument cuts them further.

The high-core residual has an exact quotient normal form.  Let `E` be the
forced external split-root core and

```text
C_E(X) = prod_{s in E} (X-s).
```

For every `Q` on the residual component,

```text
L_Q(X) = C_E(X) R_Q(X),        deg R_Q <= 126-|E|.
```

Since `C_E` is a squarefree divisor of `X^512-1`, the split-locator gate for
`L_Q` is equivalent, after normalization and the exact-degree check, to the
quotient split-locator condition

```text
R_Q | (X^512-1)/C_E.
```

Thus the remaining line residuals (`e_G>=72`) are quotient-locator pencils of
degree at most

```text
126-72 = 54,
```

and the remaining irreducible conic residuals (`e_G>=69`) are quotient-locator
families of degree at most

```text
126-69 = 57.
```

This is not a closure, but it makes the remaining branch a low-degree quotient
split problem rather than a full degree-126 locator problem.

The same high-core branches also lie in the high-agreement tangent range after
puncturing away the forced external core.  Deleting a core `E` leaves a row of
length

```text
n' = 512-|E|,
```

while the represented witness still has exact agreement

```text
a' = 386
```

on the punctured row, with co-support radius

```text
r' = n'-a' = 126-|E|.
```

The very-high-agreement tangent staircase applies when

```text
r' <= floor((n'-256)/3),
```

and this holds for every `|E|>=61`.  In particular, it holds for both residual
thresholds:

```text
line residuals:  |E|>=72, r'<=54, tangent numerator <=55;
conic residuals: |E|>=69, r'<=57, tangent numerator <=58.
```

This is a tangent-ledger eligibility statement on the punctured row.  It does
not by itself prove that the original-row projective numerator is within the
budget `6`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
no proof that every moving-slope component is a line;
no closure of line components with forced external split-root core >=72 in projective accounting;
no closure of irreducible conic moving-slope components with forced external split-root core >=69 in projective accounting;
no proof that the high-core quotient split problem is empty or paid;
no claim that the punctured tangent numerator is within the original row budget;
no exclusion of another independent noncontained vector at the same finite slope;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
