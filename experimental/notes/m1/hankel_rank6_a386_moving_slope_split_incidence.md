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

The high-core quotient branch has a more precise forced-core structure.  Let
`W` be the three-dimensional vector space of `Q`'s, and let

```text
ev_s: W -> F,        Q |-> L_Q(s)
```

be the external evaluation functional.  Then `E_s` is the projectivized kernel
of `ev_s` when `ev_s` is nonzero, and is the whole `Q`-plane when `ev_s=0`.

For a line component `G=P(U)`, a forced external root is exactly an `s` for
which

```text
ev_s|_U = 0.
```

Equivalently, the forced core is a dual-evaluation fiber, and `C_E` is a common
divisor of the two basis kernel polynomials spanning the line subspace `U`.
After factoring `C_E`, the residual split problem is a projective-line quotient
pencil of degree at most `54`.

For an irreducible conic component, containment in a root hyperplane can occur
only when `ev_s=0` on the whole `Q`-plane: a nonzero linear equation cuts a
line, and an irreducible conic is not contained in a line.  Thus the high-core
conic residual is not component-specific; its forced core is a global common
divisor of all three basis kernel polynomials in the `Q`-plane.  After factoring
that global core, the residual split problem is a projective-plane quotient
family of degree at most `57`.

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

At the residual thresholds this is only a tangent-ledger eligibility statement
on the punctured row: the numerators `55` and `58` are far above the original
budget `6`.  However the same formula closes the very-high-core tail.  The
projective high-agreement tangent staircase applies to the punctured row, so
finite slopes and the point at infinity are bounded together by

```text
projective slopes on the branch <= r'+1 = 127-|E|.
```

The branch is projective-safe whenever

```text
127-|E| <= 6,
```

that is,

```text
|E| >= 121.
```

Thus the tangent staircase alone closes `|E|>=121`.  The boundary row
`|E|=120` is also closed by a cofactor-span obstruction.  If it contributed
seven projective slopes, puncturing the forced core would give

```text
n' = 392,      a' = 386,      r' = 6.
```

Choose a nonbad projective point as infinity.  The finite tangent-star
extremizer corollary would then force a common support of size `385`, with the
seven punctured residual coordinates bijecting with the seven bad slopes.  The
corresponding residual quotient locators are the seven degree-`6` cofactors

```text
R_i(X)=prod_{m != i}(X-omega_m)
```

of a seven-point residual set.  These cofactors are linearly independent:
evaluation at `omega_i` kills all `R_m` for `m != i` and leaves
`R_i(omega_i) != 0`, so every subset of them is independent.  At most one of
the seven projective bad points is the original endpoint, hence at least six
bad points are finite `Q`-classes on the component.  But after the fixed forced
core is factored, a line component supplies at most a `2`-dimensional vector
space of quotient locators, and an irreducible conic lies in the ambient
`3`-dimensional `Q`-plane.  Six independent finite cofactors cannot lie in
either family.  Therefore the `|E|=120` tail contributes at most six projective
slopes and is projective-safe.

The same argument is a top-saturation exclusion throughout the high-core
quotient tail.  If the punctured radius is `r'=126-|E|`, the raw projective
tangent staircase gives `r'+1` slopes.  Saturating that bound would force at
least `r'` finite component classes after discarding the possible original
endpoint.  Their tangent-star cofactors are independent, so top saturation is
impossible whenever `r'` exceeds the fixed quotient-family dimension (`2` for a
line, `3` for an irreducible conic).  Thus the tangent-tail bound improves from
`r'+1` to `r'` in the high-core range.  In particular, `|E|=120` is safe and
`|E|=119` is the next cofactor-current one-over tangent-tail core.

The packet records both the raw intermediate profile and the cofactor-current
profile.  In the cofactor-current profile the live one-over ranges are the
finite-incidence ranges `72<=|E|<=80` for lines and `69<=|E|<=76` for conics,
together with the tangent-tail core `|E|=119` for both component types.  The
core `|E|=120` is projective-safe, and the largest conic projective bound drops
from `26` to `25`.

The cofactor-current tangent tail is also sharpened after imposing exact
agreement.  It closes line cores `97<=|E|<=119` and conic cores
`103<=|E|<=119`.  Put `r'=126-|E|`.  If seven projective slopes survived,
choose a nonbad projective point as infinity, so the seven bad points become
finite on the punctured row.

For `115<=|E|<=119`, the tangent-staircase residual-budget proof leaves at
most one private residual coordinate beyond the common-support complement.  As
before, `d<r'` is higher-agreement, `d=r'` is same-support-contained at exact
`A`, and the `d=r'+1` cofactors are independent enough to exceed both fixed
quotient-family dimensions.

For `109<=|E|<=114`, the new branch is `d=r'+2`.  In that branch the six
finite component cofactors restrict to six distinct two-supported edge vectors
on the residual set.  The verifier records the signed-incidence rank
calculation: after barycentric scaling, the two nonzero entries have opposite
orientation, and over characteristic `17` a connected graph component
contributes `|V|-1` to signed-incidence rank.  A rank-at-most-two signed
incidence matrix supports at most three distinct simple edges, so six distinct
edges span dimension at least `3`.  This closes the line tail because the line
quotient-family dimension is `2`.  It does not close conic cores
`109<=|E|<=114` by dimension alone, because a `K4` edge configuration has six
edges and signed-incidence rank `3`, matching the conic quotient-family
dimension.  Conversely, this is the only sharp shape: any surviving conic tail
witness in this range must use all six edges of a `K4` on four residual
coordinates.

For line cores `97<=|E|<=102`, the first possible exact-agreement survivor is
`d=r'+4`.  A surviving line component would put six quotient locators in a
two-dimensional pencil.  After the common residual zero set is factored, any
two independent members of such a pencil have disjoint residual zero sets on
the remaining active residual coordinates.  Thus six four-private cofactors on
`m` active coordinates would force `6(m-4)<=m`, while six distinct
four-private supports require `m>=6`.  This contradiction closes the line tail
through `|E|=97`.

For line cores `103<=|E|<=108`, the first possible exact-agreement survivor is
`d=r'+3`.  The packet checks the three-private cofactor capacity: six distinct
three-private cofactors span dimension at least `3`.  This again exceeds the
line quotient-family dimension `2`.

The `K4` boundary is then closed by a conic-determinant obstruction.  After
factoring the common residual zero set, the six finite classes become the six
pair quadratics `(T-x_i)(T-x_j)` from four distinct residual coordinates.  The
determinant of the six conic-evaluation rows in the basis
`X^2,Y^2,Z^2,XY,XZ,YZ` is

```text
prod_{0<=i<j<=3} (x_j-x_i)^2.
```

This is nonzero in characteristic `17`, so no projective conic can contain all
six image points.  Hence the conic tangent-tail rows `109<=|E|<=114` are also
closed.

The conic cores `103<=|E|<=108` are also closed by a root-star Bezout
obstruction.  In this three-private branch, the six finite classes become six
pair quadratics chosen from the ten pairs of five residual coordinates.  Six
edges on five vertices have degree sum `12`, so some residual coordinate occurs
in at least three selected pairs.  The corresponding three pair-quadratic
points are distinct and lie on the root-star line

```text
x_i^2 X + x_i Y + Z = 0.
```

An irreducible conic in the quotient plane can meet a line in at most two
points unless the line is a component, which is impossible for an irreducible
component.  Hence the conic tangent-tail rows `103<=|E|<=108` close as well.

For conic cores `97<=|E|<=102`, the first surviving exact-agreement branch is
`d=r'+4`.  After common zero factoring, six finite classes give six pair
quadratics among the fifteen pairs on six residual coordinates.  If the
selected graph has maximum degree at least `3`, root-star Bezout closes it.
The no-root-star graphs are only a six-cycle or two disjoint triangles.  The
two-triangle determinant is identically zero, and a six-cycle can survive only
if after affine normalization to `0,1,a,b,c,d` the hexagon factor

```text
a*b*d-a*c*d+a*c-a*d-b*c+c*d
```

vanishes.  Thus this branch is not closed, but it is reduced to two explicit
quotient residuals.

The packet also records a deterministic subgroup-coordinate sharpness witness
for the six-cycle residual.  The order-512 subgroup exponents
`0,255,417,261,6,356`, taken in that cyclic order, are distinct and after
affine normalization make the same hexagon factor vanish.  Therefore the
six-cycle residual cannot be closed by proving this factor is nonzero on the
subgroup.  Any closure must use more structure: quotient-family equations,
Hankel constraints, endpoint payment, or split-locator noncontainment.  This
witness is not an MCA bad-slope witness.

Thus the unclosed high-core quotient range is finite:

```text
line residuals:  72 <= |E| <= 96;
conic residuals: 69 <= |E| <= 102.
```

This uses the projective high-agreement tangent theorem on the punctured row,
not a separate finite-plus-endpoint overcount.

Within the remaining intermediate range, the raw audit profile splits the
residual further.  Combining the external incidence bound (for lines), the
pair-overlap packing bound (for irreducible conics), and the unrefined
punctured projective tangent bound gives the following pre-cofactor
projective upper-bound profile.

For line components, before applying the cofactor-span tail obstruction:

```text
one-over-budget: 72 <= |E| <= 80, and |E| = 120;
worst raw projective upper bound: 18, attained in the middle range.
```

For irreducible conic components, before applying the cofactor-span tail
obstruction:

```text
one-over-budget: 69 <= |E| <= 76, and |E| = 120;
worst raw projective upper bound: 26, attained in the middle range.
```

Thus the endpoint-only subranges are now separated from the genuinely larger
quotient/core residuals.  A single endpoint payment or one-root saving would
close the finite-incidence one-over-budget subranges, while the middle ranges
need a stronger quotient, tangent, or exact-root-table argument.  The
punctured-tangent one-over rows `|E|=120` and `|E|=119` are closed by the
cofactor-span and exact-agreement arguments above.

The saturation profile records the remaining finite-incidence obstruction
explicitly.  Six finite
line classes in the incidence one-over range require pairwise disjoint external
root sets with external slack between `1` and `41`.  Six finite conic classes
require between `0` and `14` forced pair-overlap events before any external
excess.  The former `|E|=120` tangent-tail obstruction is closed by the
cofactor-span argument above, and the next `|E|=119` tangent-tail obstruction is
closed by exact agreement.

Equivalently, a genuine over-budget witness in one of these rows must have six
distinct finite slopes and an unpaid projective endpoint.  The sharpest finite
survival targets are now small and explicit: line core `|E|=72` needs
near-complete base splitting among the six finite classes, while conic core
`|E|=69` needs an almost complete external-secant graph among the six conic
points.

The exact defect thresholds are now part of the packet.  The line `|E|=72`
case closes unless all six finite classes have a base root and at least five
have two.  The conic `|E|=69` case closes unless at least `14` of the `15`
pair secants occur before external excess, which forces at least `16` secant
triangles.

The extremal shapes are therefore completely finite.  For line `|E|=72`, the
six finite classes have base-root histogram either `(0,0,6)` or `(0,1,5)`,
where the coordinates count zero-, one-, and two-base-root classes.  For conic
`|E|=69`, the secant graph is either `K6` or `K6` with one edge deleted.
Exact degree-`126` root accounting sharpens this further: line histogram
`(0,0,6)` leaves exactly one nonforced external root line unused, line
histogram `(0,1,5)` uses every nonforced external root line, conic histogram
`(0,0,6)` requires `14` pair-overlaps, and conic histogram `(0,1,5)` requires
all `15` pair-overlaps.

Combining the shape and root-budget constraints leaves exactly two line design
targets and three conic design targets.  In the line case, either six size-`52`
classes cover all but one nonforced external root line, or one size-`53` class
and five size-`52` classes cover them all.  In the conic case, either six
size-`55` classes with secant graph `K6` leave one line unused, six size-`55`
classes with `K6` minus one edge cover all lines, or one size-`56` class and
five size-`55` classes with `K6` cover all lines.

Equivalently, the line external-root multiplicity profiles are exactly
`(1,312,0)` or `(0,313,0)` for multiplicities `(0,1,>=2)`.  The irreducible
conic profiles are exactly `(1,300,15)`, `(0,302,14)`, or `(0,301,15)` for
multiplicities `(0,1,2)`, with no multiplicity-`>=3` lines because a nonforced
external line meets the irreducible conic in length at most `2`.

The corresponding local profiles are exact.  The line singleton sequences are
`(52,52,52,52,52,52)` or `(53,52,52,52,52,52)`.  The conic
secant-degree/singleton sequences are `(5^6;50^6)`,
`((4,4,5,5,5,5);(51,51,50,50,50,50))`, or
`(5^6;(51,50,50,50,50,50))`.

For the extremal line `e_G=72` branch, this is now recorded as a quotient
pencil obstruction.  After the forced external core is factored, the line
component is a degree-`54` quotient pencil.  Any surviving over-budget witness
must contain six distinct fully split degree-`54` members: either six fibers
with `52` nonforced external roots and two base roots each, leaving one
nonforced external point unused, or one `53`-external-root fiber with one base
root plus five `52`-external-root fibers with two base roots, covering all
nonforced external points.

The same quotient-obstruction catalog is now recorded for the whole
exact-current finite-incidence one-over range.  Line cores `e_G=72..80` must
realize six distinct full-split members of quotient pencils of degrees
`54,53,...,46`, with pairwise disjoint external fibers and one of the printed
base-root histograms.  Irreducible conic cores `e_G=69..76` must realize six
full-split members on quotient conics of degrees `57,56,...,50`, with the
printed pair-overlap and missing-secant ranges.  Failure of the corresponding
full-split quotient family is a single-saving closure for that row.

For the extremal conic `e_G=69` branch, the packet also records a classical
Pascal obstruction profile.  If the six finite classes really lie on an
irreducible conic and the secant graph is `K6`, every Hamiltonian cycle gives a
Pascal collinearity among intersections of opposite external-root secants,
giving `60` required collinearities.  In the `K6` minus one edge branch, the
same test gives `36` required collinearities.  Failure of these relations in
the actual external root-line arrangement would close the corresponding
extremal conic branch; the packet does not yet run that arrangement test.

The packet also records a compact exact catalog for the whole endpoint-only
finite-incidence one-over range.  For line cores `e_G=72..80`, the counts of
allowed base-root histograms are `2,16,27,28,28,28,28,28,28`; from `e_G=75`
onward all `28` histograms are possible and the remaining obstruction is
external slack, not base splitting.  For conic cores `e_G=69..76`, the counts
are `2,16,27,28,28,28,28,28`; from `e_G=72` onward all base histograms are
possible, and pair-overlap pressure disappears completely at `e_G=75,76`.

The same packet now includes abstract incidence-only sharpness witnesses for
every finite-incidence one-over core.  For each line core `72..80`, six
pairwise-disjoint abstract external-root classes satisfy the current base-root
cap and external-root budget.  For each irreducible conic core `69..76`, six
abstract classes satisfy the current conic incidence axioms: pairwise
intersections have multiplicity at most one, and no external root line is used
three times.  These witnesses are deliberately not Hankel-realizability
claims.  They show that the remaining one-over finite-incidence rows cannot be
closed by sharpening only the present incidence and pair-overlap counts; a
closure now needs endpoint payment, a finite-slope collision, or algebraic
quotient-fiber input.

Finally, the packet includes a single-saving closure ledger for every
finite-incidence row that is exactly one over budget, together with the formerly
raw punctured-tangent row `e_G=120` for both component types.  In each listed
finite-incidence row, any one listed saving lowers the projective count from
`7` to the budget `6`; for `e_G=120` that saving is supplied by the
cofactor-span obstruction.  The subsequent exact-agreement filter closes the
cofactor-current tangent-tail rows `e_G=97..119` for lines and `e_G=103..119`
for conics, using the four-private line-pencil obstruction on the line side
and the K4 determinant and three-private root-star arguments on the conic side,
while reducing the conic four-private rows `e_G=97..102` to the two-triangle
or hexagon-factor residuals above.  Thus the exact-current one-over rows are
only the finite-incidence ranges.

The packet now records these exact-current rows as a minimal obstruction
profile.  Any surviving projective over-budget witness must be one of the
line cores `72..80` or conic cores `69..76`, must have exactly six finite
source classes, must keep all six finite slopes distinct, and must keep the
projective endpoint unpaid.  The profile attaches the saturated base-root,
external-slack, and secant-overlap conditions for each row, so the next proof
step can target a concrete failure of this normal form.

The packet also records a multi-saving closure ledger for every exact-current
row still above budget.  Line cores `72..96` require saving depths `1..5`:
`72..80`, `81..86`, `87..91`, `92..94`, and `95..96` require respectively
`1,2,3,4,5` independent endpoint/finite-class savings.  Conic cores `69..102`
require saving depths up to `19`; the last two cores `101,102` are controlled
by the cofactor-improved projective tangent envelope rather than by the
pair-overlap envelope.  This ledger is a closure criterion: if the listed
number of counted projective parameters is removed, paid, or coalesced, the
row is safe.  It does not prove those savings occur.

The same ledger splits the next proof targets by first available mechanism:
line base-splitting pressure remains only for `e_G=72..74`; line cores
`75..80` need external-slack, duplicate-slope, endpoint, or paid-class input.
For conics, base plus secant pressure remains for `e_G=69..71`, secant-only
pressure remains for `e_G=72..74`, and cores `75,76` need an endpoint,
duplicate-slope, or paid-class input.  The `e_G=120` tail, the line
`e_G=97..119` tangent-tail rows, and the conic `e_G=103..119` tangent-tail
rows are now isolated as closed punctured-tangent tails rather than remaining
proof targets.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_moving_slope_split_incidence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json
```

Nonclaims:

```text
no proof that every moving-slope component is a line;
no closure of line components with forced external split-root core in 72..96 in projective accounting;
no closure of irreducible conic moving-slope components with forced external split-root core in 69..102 in projective accounting;
no proof that the high-core quotient split problem is empty or paid;
no claim that the punctured tangent numerator at the residual threshold is within the original row budget;
no exclusion of another independent noncontained vector at the same finite slope;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
