# KoalaBear rank-eleven quotient-pair plane cap

Status: **PROVED CONDITIONAL ROUTE CUT / ZERO DEPLOYED LEDGER MOVEMENT**

Research source:
`AllenGrahamHart/rs-mca-prize-dag@f557775d53192f027730b15c2f70330e1a56c116`.
The two source-node trees are
`2b2e264afd74e65cbde43b4c79e1702c04c7db4d` and
`3d2ecbdee129e5422c6cb7e7686384446977a34b`.
The pure-power extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@b5e3a90d8415ea7de6c144d1fcd56c0e5c50b7d2`,
node tree `d47d9281c12e629b3c700f70b5ba30da711d9e10`.
The dimension-three rich-plane extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@d79701f94add274e6c7fbf2f4744980d77817f4b`,
node tree `40b4d860ac0cd50dbe2c43e883ede75b0b85ac84`.
The dimension-three pair-overlap extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@473f41afc6b76d747e534cb8e509a0353dcde3aa`,
node tree `43fc63b7c2f721ec79c4c2b451aef9a2eb17eb01`.
The complete type-population extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@1d52ff3013b6ab4e94f39cf9d6627f7562d65cf8`,
node tree `1bef7e27ed86ed76d5391e616bcb0a39e1681336`.
The endpoint plane-line extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@f0a13cc6e33399aa8192bf4879b9a9e7941371e3`,
node tree `1763c945b9e4031424099486ecf7d44a9bc021a2`.
Its direction-saturation extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@1db90bbbef8c8e31b881de04dc9cedb387728c0f`,
node tree `ddcb65d9d490042a6215457db9c1214246d2b456`.
The projective-image extension is sourced separately from
`AllenGrahamHart/rs-mca-prize-dag@121e75fa14d2b58968ca398f352437e1357b16fb`,
node tree `0537b44d0ff8240f47d08942467febeb6ca57cd6`.

This note is a finite, base-field-normalized split-pencil theorem.  Its
source interface is printed in full below.  In particular, this packet does
not assert that the current rank-eleven route has already produced that
interface.

## 1. Source interface

Let `D` be the official KoalaBear evaluation domain and set

```text
n = |D| = 2,097,152,
K = 1,048,576,
m = 1,116,048,
s = m-2 = 1,116,046.
```

Suppose there are 520 distinct selected quotient pair types indexed by
scalar polynomials `R_p`.  Their pair codewords have the coprime-direction
normal form

```text
(a_p,b_p)=(a_0,b_0)+R_p(U,V),       gcd(U,V)=1,       (1.1)
```

and every complete received-pair core

```text
H_p={x in D:(r_0,r_1)(x)=(a_p,b_p)(x)}
```

has size `s`.  Assume also:

1. the affine span of the selected `R_p` has dimension at most four;
2. every affine scalar line contains at most 15 selected types;
3. every selected type owns at least 29 chronology-disjoint records.

Only the first two assumptions are used for the plane cap and endpoint bank.
The 29-record floor is used solely in the dimension-four router.

## 2. Plane occupancy is at most 218

Assume that one affine scalar plane contains 219 selected points and retain
exactly 219 of them.  They span the plane because an affine line contains at
most 15 selected points.  Factor the gcd of the two-dimensional difference
space.  Let `J_A` be the coordinates at which that gcd vanishes and the
received pair equals the common pair-codeword value, and put `c=|J_A|`.

At a coordinate in `J_A`, all 219 cores occur.  At a nonmatching gcd root,
none occurs.  At every other coordinate the core owners form one affine line,
so there are at most 15.  Two distinct pair codewords agree on at most `K-1`
coordinates; hence `c<=K-1`.  Counting core incidences gives

```text
219s <= 219c+15(n-c),
c >= ceil((219s-15n)/(219-15)) = 1,043,906.          (2.1)
```

Shorten by the actual common core.  This subtracts one common pair, punctures
`J_A`, and divides every difference by its squarefree locator.  Put

```text
k' = K-c,       1 <= k' <= 4,670,
n' = n-c = 1,048,576+k',
s' = s-c = 67,470+k'.                                (2.2)
```

The residual coordinate multiplicity is at most 15.  Its total deficit from
full 15-fold occupancy is

```text
Delta = 15n'-219s' = 952,710-204k'.                  (2.3)
```

Thus at least

```text
F >= n'-Delta = 95,866+205k'                         (2.4)
```

coordinates have multiplicity exactly 15.  Each such coordinate gives a
15-point affine line in the selected scalar plane.  Through any selected
point there are at most `floor(218/14)=15` full lines, since their other
14-point sets are disjoint.  Double counting point-line incidences therefore
gives at most 219 full lines.

One fixed full line can occur at no more than `k'-1` coordinates: the
difference of two points on that line is a nonzero residual scalar polynomial
of degree at most `k'-1` and vanishes at every coordinate realizing the line.
Consequently

```text
F <= 219(k'-1).                                       (2.5)
```

Equations (2.4)--(2.5) would require

```text
0 >= 96,085-14k' >= 96,085-14*4,670 = 30,705,
```

a contradiction.  Therefore every affine scalar plane contains at most 218
selected quotient types.

## 3. Dimension-three and dimension-four outputs

In scalar dimension three, factor the gcd of the full difference space and
let `J` be its common received-pair core.  Every coordinate outside `J` has
at most 218 owners because a nonzero evaluation fiber is an affine plane.
Therefore

```text
520s <= 520|J|+218(n-|J|),
|J| >= 407,831.                                      (3.1)
```

At the minimum floor, shortening gives

```text
(n',K',m',s')=(1,689,321,640,745,708,217,708,215),
218n'-520s'=178.                                     (3.2)
```

This common-core floor sharpens without changing the source interface.
After shortening by the complete common core, three distinct affine owner
planes containing at least 189 selected types would have pairwise selected
overlap at most 15 and therefore union size at least

```text
3*189-3*15=522>520.
```

Thus at most two 189-rich planes occur.  Each spans a two-dimensional
direction space.  Two independent direction polynomials have gcd degree at
most `k'-2`, so one rich plane recurs at most `k'-2` times.  If `N_189`
counts coordinates of multiplicity at least 189, then

```text
N_189<=2(k'-2),
520(67470+k')<=188(1048576+k')+60(k'-2).             (3.3)
```

Consequently

```text
k'<=595763,       |J|>=452813.                       (3.4)
```

The capacity slack at `k'=595763` is 232; at `k'=595764` the same ledger
has deficit 40.  This is adjacency for the conditional incidence formula,
not an MCA safe/unsafe certificate.

There is also an exact lower endpoint for the shortened dimension-three
family.  Distinct residual pair cores meet in at most `k'-1` coordinates.
Writing `d_x` for residual core multiplicity gives

```text
I=sum_x d_x=520(67470+k'),
sum_x C(d_x,2)<=C(520,2)(k'-1).                     (3.5)
```

For fixed `I` on `1048576+k'` coordinates, the left side is minimized by
balanced integer multiplicities.  If

```text
I=a(1048576+k')+r,       0<=r<1048576+k',
```

that minimum is

```text
aI-C(a+1,2)(1048576+k').                            (3.6)
```

Exact division gives `a=33` on `3..1167`, `a=34` on `1168..3331`, and
`a=35` on `3332..4835`.  Pair capacity minus (3.6) is increasing on each
interval but remains negative through

```text
gap(4835)=-2110,       gap(4836)=115260.             (3.7)
```

Together with (3.4), the complete conditional interval is therefore

```text
4836<=k'<=595763,
452813<=|J|<=1043740.                               (3.8)
```

The 87 rows `k'=4836..4922` overlap numerically with a separate
large-shared-pair-core payment threshold.  No transport is claimed: that
payment quantifies over every low-margin minimizing pair in the complete
post-near rank-eleven family, while this packet controls the retained
synchronized quotient-type source interface.  The current dependency chain
does not supply the missing inclusion or a disjoint complementary charge.

If the selected scalar family is the complete retained quotient-type family,
let `q` be its cardinality and assume the chronology-disjoint retained mass
is the proved value `M=255011043`.  The same two ledgers then bound `q`
itself. Plane incidence gives

```text
(q-218)k'<=218*1048576-q*67470.                     (3.9)
```

For `0<=d<=218`, the exact identity

```text
C(d,2)=217d-C(218,2)+C(218-d,2)
```

and pair intersections at most `k'-1` give a second linear inequality in
`k'`.  The doubled compatibility cross-product factors as

```text
-109q(q-218)(619q-1962831).                        (3.10)
```

It is positive at `q=3170` and negative at `q=3171`. Consequently

```text
520<=q<=3170,
max_p records(p)>=ceil(255011043/3170)=80446.       (3.11)
```

At the adjacent population endpoint,

```text
q=3170 => 4960<=k'<=4982,
          #{x:d_x=218}>=985788.                    (3.12)
```

The first excluded population has doubled cross-product deficit
18,372,095,406. This is a dense-owner and saturated-plane router, not a
payment for that owner or the retained family.

The extremal population admits a further exact design reduction.  A full
218-owner plane `A` occurs on exactly `|J_A\J|` residual coordinates.  Its
own endpoint shortening has local dimension at least 2,044, so it recurs at
most `k'-2044` times.  The full-coordinate floor therefore requires 339 to
358 distinct 218-point planes.  Balancing their incidences over 3,170 types
forces at least 22,752 plane pairs to meet in a saturated 15-point line,
hence at least 217 distinct saturated lines.  Every saturated line has at
least

```text
k'-2609>=2351                                       (3.13)
```

residual common-core coordinates.

Using each plane's internal bank is much stronger.  Every full coordinate
contributes at least 210 distinct projective direction roots.  One direction
polynomial has at most `k'-1` roots, while each represented saturated
direction consumes 105 selected-point pairs.  Consequently

```text
41746<=R<=47836,                                    (3.14)
roots(T_eta)>=2351 for every represented eta,
aggregate unused direction degree <=30203244,
aggregate root saturation >=5750430/6589409>0.8726. (3.15)
```

Thus `q=3170` is a calibrated finite `(Q)`/split-pencil direction bank.  The
packet does not classify it as quotient-periodic, force a further common
factor, or pay the endpoint.

There is now an exact projective-image refinement. Let `W_0` be the residual
three-dimensional scalar direction space and `G=gcd(W_0)`. A residual
official-domain root of `G` has owner multiplicity zero, so the exact
218-fold occupancy deficit gives

```text
|D' intersection Z(G)|<=310.                        (3.16)
```

After dividing by `G`, homogenization defines a basepoint-free map
`phi:P^1->P^2`. If `d` is its polynomial degree, `c` its image-curve degree,
and `e` its map degree, pullback of a projective line gives

```text
d=ec,       c>=2.                                   (3.17)
```

The primitive member of every represented direction retains at least 2,041
official roots. If `c=2`, the image is a base-field rational conic and a
base-field projective change gives

```text
W_hom=span(A^2,AB,B^2),       1021<=deg(A/B)<=2490. (3.18)
```

Thus all 41,746 or more represented directions are binary quadratics in one
rational function. If `c>=3`, one evaluation normal has at most
`floor((K'-1)/3)` full preimages, so the 23 rows force 597 through 633
distinct full evaluation normals. Neither branch is excluded or paid; in
particular `(3.18)` is not yet a quotient-periodic classification of `A/B`.

In scalar dimension four, either the original `407,831` common-core floor
from (3.1) holds or one actual noncommon coordinate has at least 219 owners.
Those owners lie in an
affine three-space but, by the plane cap, not in an affine plane.  They thus
have exact affine dimension three and own at least

```text
219*29=6,351
```

chronology-disjoint records whose exact supports all contain that coordinate.

Neither dimension-three output nor the dimension-four output is paid by this
packet.

## 4. Equality forces a projective direction bank

Now suppose an affine scalar plane contains exactly 218 selected points.
Repeating the common-core count gives

```text
c >= ceil((218s-15n)/(218-15)) = 1,043,551,
1 <= k'=K-c <= 5,025.                                (4.1)
```

After shortening, the number of multiplicity-15 coordinates obeys

```text
F >= 28,396+204k'.                                   (4.2)
```

There are at most 218 full affine lines.  Group them by projective direction.
For one represented direction `eta`, let `z_eta` count all full coordinates
whose fiber is parallel to `eta`.  A nonzero residual direction polynomial
vanishes at every such coordinate, so

```text
z_eta <= k'-1.                                       (4.3)
```

Since `sum_eta z_eta=F`, equations (4.2)--(4.3) first force

```text
2,044 <= k' <= 5,025,
1,043,551 <= c <= 1,046,532.                         (4.4)
```

Moreover

```text
28,396+204k' > 209(k'-1)
```

throughout this interval.  Hence the full fibers use between 210 and 218
affine lines and at least 210 distinct projective directions.  Their aggregate
unused direction-degree capacity is at most

```text
sum_eta ((k'-1)-z_eta)
 <= 218(k'-1)-(28,396+204k')
 <= 41,736.                                          (4.5)
```

Uniformly, the aggregate root saturation is at least

```text
(28,396+204*5,025)/(218*(5,025-1))
 = 131,687/136,904 > 0.9618.                         (4.6)
```

Dualizing the 218 scalar points gives an arrangement of 218 lines with at
least 210 multiplicity-15 points.  Those points consume at least
`210*C(15,2)=22,050` of the `C(218,2)=23,653` line pairs, leaving at most
1,603 pairs for every other intersection.

## 5. Pure-power quotient-periodic router

There is one exact reduction inside the first frontier branch.  Assume, in
addition to the source interface, that after a projective change of basis
the coprime residual direction pencil is generated on `mu_N` by

```text
X^e, 1,
```

where `e` is a power-of-two divisor of `N=2^21` and `e<=k'-1`.  A represented
direction has polynomial `X^e-y`; if it has a domain root, it has exactly
`e` simple roots in `mu_N`.  Thus the full-coordinate count also obeys

```text
F<=r e<=218e.                                       (5.1)
```

Combining (5.1) with (4.2), (4.4), and the degree cap leaves exactly

```text
e in {2048,4096}.                                   (5.2)
```

For `e=2048`, capacity and degree force `k'=2049`.  Then `F>=446392`,
whereas `217e=444416`, so all 218 directions occur.  The 218-line ceiling
then gives exactly one full line per direction, and

```text
218e-F<=72.                                         (5.3)
```

For `e=4096`, the surviving interval and direction floor are

```text
4097<=k'<=4237,       r>=211.                       (5.4)
```

There are at most seven full lines beyond the first in each represented
direction, and direct fiber capacity gives

```text
re-F<=218*4096-(28396+204*4097)=28744.              (5.5)
```

This theorem neither proves that the endpoint pencil is pure-power nor
excludes or pays either surviving degree.  General quotient-periodic
rational maps remain outside its scope.

## 6. Exact frontier and nonclaims

The equality branch is now a near-complete base-field split-pencil object:
at least 210 members of one projective polynomial pencil spend more than
96.18 percent of their aggregate degree on distinct official-domain roots.
This is the natural finite input for either:

1. a quotient-periodic rational-fiber classification and payment; or
2. a finite-characteristic arrangement theorem valid for this represented
   polynomial pencil.

The usual complex Hirzebruch line-arrangement inequality would contradict
the dual pair budget, but it is not imported here: its standard form is not
a field-uniform theorem, and positive-characteristic line arrangements need
separate hypotheses.

This packet does **not** prove that the source interface is reached by the
current rank-eleven route, exclude the 218-plane over the official field,
pay either shortened branch, move an active-v4 atom, close KoalaBear, or
resolve either prize problem.

## 7. Replay

The standard-library primary and independent implementations are

```text
experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py
experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1_independent.py
```

They recompute every displayed integer, scan all 4,833 excluded pair-moment
rows, all 2,868 population-factor rows, all three endpoint ledgers on all
23 population-endpoint rows, all 2,982 plane-endpoint values of `k'`, and
every power-of-two pure-power degree. They verify the frozen source hashes
when a prize-DAG checkout is provided. The primary also rejects forty-seven hostile
contract mutations.
