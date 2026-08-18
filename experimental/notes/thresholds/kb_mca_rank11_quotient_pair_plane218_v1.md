# KoalaBear rank-eleven quotient-pair plane cap

Status: **PROVED CONDITIONAL ROUTE CUT / ZERO DEPLOYED LEDGER MOVEMENT**

Research source:
`AllenGrahamHart/rs-mca-prize-dag@f557775d53192f027730b15c2f70330e1a56c116`.
The two source-node trees are
`2b2e264afd74e65cbde43b4c79e1702c04c7db4d` and
`3d2ecbdee129e5422c6cb7e7686384446977a34b`.

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

In scalar dimension four, either the same common-core floor holds or one
actual noncommon coordinate has at least 219 owners.  Those owners lie in an
affine three-space but, by the plane cap, not in an affine plane.  They thus
have exact affine dimension three and own at least

```text
219*29=6,351
```

chronology-disjoint records whose exact supports all contain that coordinate.

Neither output is paid by this packet.

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

## 5. Exact frontier and nonclaims

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

## 6. Replay

The standard-library primary and independent implementations are

```text
experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1.py
experimental/scripts/verify_kb_mca_rank11_quotient_pair_plane218_v1_independent.py
```

They recompute every displayed integer, scan all 2,982 endpoint values of
`k'`, and verify the frozen source hashes when a prize-DAG checkout is
provided.  The primary also rejects twelve hostile contract mutations.

