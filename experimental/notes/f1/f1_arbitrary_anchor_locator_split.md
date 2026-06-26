# F1 Arbitrary-Anchor Residue Cloud And Locator Split

## Residual-Slack List Reduction

Let `F` be a finite field, let `D subset F` have size `n`, and let
`C = RS[F,D,k]`. Fix integers

```text
1 <= t <= sigma,        a = k + sigma <= n.
```

A degree-`t` residue-line datum consists of a denominator `E in F[X]` of
degree `t`, nonzero on `D`, a numerator `N in F[X]` with `deg N < t` and
`[N]_E != 0`, and an anchor word `w:D->F`. A slope `z` has a witness at
agreement `a` if there are a polynomial `Q in F[X]` and a set `S subset D`
such that

```text
deg Q < k+t,        |S| >= a,
Q = w on S,        [Q]_E = z [N]_E.
```

Define the residual list set

```text
List_{t,sigma}(w)
  = { Q in F[X] : deg Q < k+t,
        |{ x in D : Q(x)=w(x) }| >= k+sigma }.
```

Then the number of support-wise MCA-bad slopes contributed by this datum at
radius `delta = 1-a/n` is at most `|List_{t,sigma}(w)|`.

Equivalently, unbalanced residue-line data inject into the ordinary list of
the anchor word `w` for the larger code `RS[F,D,k+t]` at agreement

```text
k + sigma = (k+t) + (sigma-t).
```

The relevant list slack is therefore the residual slack `sigma-t`, not the
original MCA slack `sigma`.

Proof.  Every support-wise bad slope is, in particular, witnessed by some
pair `(Q,S)` satisfying the displayed conditions, so `Q` lies in
`List_{t,sigma}(w)`. Choose one such polynomial `Q_z` for each bad slope `z`.
If the same polynomial were chosen for two slopes `z` and `z'`, then

```text
(z-z') [N]_E = 0
```

in the `F`-vector space `F[X]/(E)`. Since `[N]_E != 0`, this forces `z=z'`.
Thus `z -> Q_z` is injective.

The consequence is structural rather than a new unconditional list theorem:
any proven bound for the above list size immediately bounds the unbalanced F1
datum. In particular, degree-one denominators are above-reserve safe exactly
to the extent that the extension/list local limit is available for residual
slack `sigma-1`. When `t=sigma`, the residual slack is zero and this reduction
can be as large as the family of all `a`-subset interpolants; that is why the
balanced residue-cloud problem below is the live F1 wall.

## Exact Balanced Residue-Cloud Form

Let `F` be a finite field, let `D subset F`, and let `C = RS[F,D,k]`.
Fix a balanced residue-line datum degree

```text
t = sigma,        a = k + t,
```

with denominator `E in F[X]` of degree `t`, nonzero on `D`, and numerator
`N in F[X]` with `deg N < t` and `[N]_E != 0`. Let `w:D->F` be an arbitrary
anchor word, and put

```text
delta = 1 - a/|D|.
```

For every `a`-subset `S subset D`, let `Q_S^w` be the unique polynomial of
degree `< a` interpolating `w` on `S`. Define the balanced residue cloud

```text
Cloud_E(w,a) = { [Q_S^w]_E : S subset D, |S| = a }
```

inside `F[X]/(E)`. Then the support-wise MCA-bad slopes of the datum
`(E,N,w)` at radius `delta` are in bijection with

```text
Cloud_E(w,a) cap F * [N]_E,
```

via

```text
z |-> z [N]_E.
```

Equivalently, a slope `z` is bad if and only if some `a`-subset `S` satisfies

```text
[Q_S^w]_E = z [N]_E.
```

Whenever this holds, the same support is automatically noncontained.

## Locator-Split Claim

Let `S,T subset D` be two `a`-subsets with

```text
|S cap T| <= k.
```

Then for every pair of distinct slopes `z_S,z_T in F`, there is an anchor word
`w:D->F` such that the same residue-line datum `(E,N,w)` has support-wise
noncontained witnesses for both slopes:

```text
z_S on S,        z_T on T.
```

Consequently arbitrary anchors cannot, in general, be controlled only by the
monic-anchor locator readout `S -> [L_S]`. Even if two supports have the same
locator residue modulo the base-core polynomial `hatE = lcm(E,E^tau)`, an
arbitrary anchor can split that single locator class into different bad slopes.

## Sunflower Floor Claim

Let `c <= k`, and suppose `I subset D` has size `c`. If

```text
m <= floor((|D|-c)/(a-c)),
```

then there are `m` supports

```text
S_j = I union P_j,        |S_j| = a,
```

with pairwise disjoint petals `P_j subset D \ I`. For any distinct slopes
`z_1,...,z_m in F`, there is an anchor word `w:D->F` such that the same
balanced datum `(E,N,w)` has support-wise noncontained witnesses for all
`z_j` on the supports `S_j`.

Taking `c=k` gives the explicit floor

```text
Lambda_NC >= floor((|D|-k)/sigma)
```

for arbitrary balanced anchors whenever the field has at least that many
distinct slopes. This is not an above-reserve counterexample: at
`sigma >= C |D|/log |D|` the floor is only `O(log |D|)` at fixed rate. It is,
however, a structural lower term that any sharp repaired F1 theorem must allow.

This is the strongest lower term delivered by this sunflower construction.
Indeed, for fixed `n=|D|`, `a=k+sigma`, and core size `0<=c<=k`, the construction
gives

```text
m(c) = floor((n-c)/(a-c)).
```

Since `a<=n`, the real function `(n-c)/(a-c)` is nondecreasing in `c` on
`0<=c<a`.  Thus `m(c)` is maximized by the largest allowed core `c=k`, giving

```text
max_{0<=c<=k} m(c) = floor((n-k)/sigma).
```

So the `floor((|D|-k)/sigma)` term is not an artifact of a particular core
choice; it is the optimized sunflower lower floor for this arbitrary-anchor
construction.

## Degenerate Support-Packing Sharpening

The same floor exhausts a larger interpolation-free support-packing mechanism.
Call an ordered family of `a`-subsets

```text
S_1,...,S_m subset D
```

`k`-degenerate if, for each `i>1`,

```text
|S_i cap (S_1 union ... union S_{i-1})| <= k.
```

For every `k`-degenerate family and every choice of distinct slopes
`z_1,...,z_m in F`, there is an anchor word `w:D->F` such that the same
balanced datum `(E,N,w)` has support-wise noncontained witnesses for all
slopes `z_i` on the supports `S_i`.

Indeed, build the anchor inductively.  Suppose `w` has already been defined
on the union of the previous supports.  On

```text
J_i = S_i cap (S_1 union ... union S_{i-1})
```

we need a degree-`<k` polynomial `P_i` satisfying

```text
E(x) P_i(x) + z_i N(x) = w(x),        x in J_i.
```

Since `E` is nonzero on `D` and `|J_i|<=k`, ordinary interpolation gives such
a `P_i`.  Then

```text
Q_i = z_i N + E P_i
```

has degree `<k+t=a`, agrees with the old anchor on `J_i`, and defines the
new anchor values on `S_i \ J_i`.  The same divisibility argument as above
shows every active support is noncontained: if the direction were explained
by a degree-`<k` polynomial `G` on `S_i`, then `E G+N` would have degree `<a`
and `a` roots, forcing `E|N`, impossible because `deg N < deg E` and
`[N]_E != 0`.

This broader construction has the same exact packing ceiling.  A
`k`-degenerate family satisfies

```text
|S_1 union ... union S_m| >= a + (m-1)(a-k) = k + m sigma,
```

so necessarily

```text
m <= floor((|D|-k)/sigma).
```

The sunflower with core size `k` attains this ceiling.  Therefore the
`floor((|D|-k)/sigma)` term is not merely the best common-core sunflower
floor; it is the exact maximum for every ordered support family whose slopes
can be added freely by at most `k` old interpolation constraints at each step.
Any larger arbitrary-anchor obstruction must use a dense-overlap packet, where
each remaining support meets the previous union in more than `k` points and
the compatibility equations no longer decouple by interpolation.

## High-Overlap Pair Gate

The dense-overlap condition has an exact local test.  Fix two `a`-subsets
`S,T subset D` and two distinct slopes `z_S != z_T`.  Put

```text
J = S cap T.
```

There is an anchor word `w` and degree-`<k` polynomials `P_S,P_T` such that

```text
Q_S = z_S N + E P_S,        Q_T = z_T N + E P_T
```

agree with `w` on `S` and `T`, respectively, if and only if the function

```text
x |-> N(x)/E(x),        x in J,
```

is the restriction to `J` of a degree-`<k` polynomial.  For `|J|<=k` this is
automatic, recovering the free interpolation used above.  For `|J|>k` it is a
genuine residue-direction gate.

The proof is just the overlap equation.  If the two witnesses agree on `J`,
then for every `x in J`

```text
E(x)(P_T(x)-P_S(x)) = (z_S-z_T)N(x),
```

so `(P_T-P_S)/(z_S-z_T)` is a degree-`<k` interpolant for `N/E` on `J`.
Conversely, if `R_J` is such an interpolant, then taking `P_S=0` and
`P_T=(z_S-z_T)R_J` makes `Q_S` and `Q_T` agree on `J`; the anchor is then
defined by these two witnesses on `S union T`.  Noncontainment on the full
supports is automatic in the balanced datum: if `N/E` agreed with a
degree-`<k` polynomial on all of an `a`-subset, then `E P-N` would have
degree `<a` and `a` roots, hence would vanish identically, contradicting
`deg N < deg E` and `[N]_E != 0`.

Thus any super-floor arbitrary-anchor packet must be supported on a dense
overlap graph whose high-overlap edges all pass this residue-direction gate.
In the explicit `F_17^2` packet below with `k=3` and `a=5`, exactly four
four-point overlaps pass the gate for `N=1` and `E=X(X-alpha)`, while no
five-point support is contained.  The verifier records this as the first
finite dense-overlap audit target.

## Gated-Core Lower Floor

The high-overlap gate is not only necessary; when a large gated core exists it
produces a stronger lower floor.

Let `J subset D` have size

```text
k < c = |J| < a,
```

and suppose that `N/E` on `J` is the restriction of a degree-`<k` polynomial
`R_J`.  If

```text
m <= floor((|D|-c)/(a-c)),
```

then there are `m` supports

```text
S_i = J union P_i,        |P_i|=a-c,
```

with pairwise disjoint petals `P_i subset D\J`.  For any distinct slopes
`z_1,...,z_m`, the same balanced datum `(E,N,w)` has support-wise
noncontained witnesses for all `z_i`.

Take the anchor to be zero on `J` and set

```text
Q_i = z_i N - z_i E R_J.
```

Then `Q_i` has degree `<a`, satisfies `Q_i == z_i N mod E`, and vanishes on
`J`.  The disjoint petals define the remaining anchor values independently.
The noncontainment argument is the same as before: a degree-`<k` explanation
of the direction on an active support would make `E G+N` a degree-`<a`
polynomial with `a` roots, forcing `E|N`, impossible.

This is the dense-overlap analogue of the sunflower construction.  For a
gated core of size `c>k`, its floor

```text
floor((|D|-c)/(a-c))
```

can be strictly larger than the free support-packing floor
`floor((|D|-k)/sigma)`.  In the explicit `F_17^2` packet below, one gated
core has

```text
c=4,        k=3,        a=5,
```

so it realizes

```text
floor((16-4)/(5-4)) = 12
```

distinct bad slopes, twice the core-`k` sunflower floor `6`.  Thus the sharp
arbitrary-anchor lower ledger must include gated dense cores, not only
freely attached support packings.

## Multi-Support Compatibility System

The previous constructions are all instances of one exact finite linear
criterion.  Fix `a`-subsets

```text
S_1,...,S_m subset D
```

and slopes `z_1,...,z_m`.  There is an anchor word `w:D->F` and
degree-`<k` polynomials `P_i` such that

```text
Q_i = z_i N + E P_i
```

agrees with `w` on `S_i` for every `i` if and only if the following overlap
system has a solution in the coefficients of the `P_i`:

```text
P_i(x) - P_j(x) = (z_j-z_i) N(x)/E(x),
        x in S_i cap S_j,        1 <= i < j <= m.        (Compat)
```

Proof.  If a common anchor exists, then `Q_i(x)=Q_j(x)` on every overlap, and
dividing by the nonzero value `E(x)` gives `(Compat)`.  Conversely, if
`(Compat)` has a solution, then the values `Q_i` agree on all pairwise
overlaps.  Hence they glue to a well-defined word on `S_1 union ... union
S_m`, which can be extended arbitrarily to an anchor on all of `D`.
Noncontainment on each active support is still automatic for the balanced
datum by the same divisibility argument.

This criterion is the right normal form for the remaining arbitrary-anchor
search.  Free support packing is the case where every new overlap contributes
at most `k` interpolation constraints.  A gated core is the case where many
overlap constraints are compatible because `N/E` has a low-degree trace on
the common core.  Any denser packet that is not explained by a common gated
core must be a genuine compatibility-system solution with nontrivial cycle
relations among the overlaps.

## Status

PROVED residual-slack reduction for `t <= sigma`; PROVED / COUNTEREXAMPLE to
the naive promotion of the monic-anchor base-core reduction to arbitrary
balanced anchors; PROVED `k`-degenerate support-packing sharpening of the
sunflower lower floor; PROVED high-overlap pair gate for the remaining dense
overlap obstruction; COUNTEREXAMPLE to universality of the free-packing floor
via a gated-core lower floor; PROVED multi-support linear compatibility
criterion for arbitrary-anchor packets.

This does not refute the repaired F1 conjecture above the corrected reserve.
For `t<sigma`, it routes the datum to the extension list ledger with residual
slack `sigma-t`. It shows that the arbitrary-anchor balanced stratum is a
genuinely separate object from the monic-anchor locator-image stratum.

## Proof Of The Residue-Cloud Form

First fix an `a`-subset `S`. If `Q_S^w` satisfies

```text
[Q_S^w]_E = z [N]_E,
```

then `Q_S^w` is a witness for slope `z` on `S`: it has degree `< a = k+t`,
it agrees with `w` on `S`, and it has the required residue modulo `E`.

Conversely, suppose a slope `z` has a witness `(Q,T)` with `|T| >= a`,
`deg Q < a`, `Q=w` on `T`, and `Q == zN mod E`. Choose any `a`-subset
`S subset T`. By uniqueness of interpolation on `S`, one has `Q=Q_S^w`.
Thus `[Q_S^w]_E=z[N]_E`, so every witnessed slope appears in the residue
cloud intersection.

The map `z |-> z[N]_E` is injective because `[N]_E` is a nonzero vector in the
`F`-vector space `F[X]/(E)`. It remains only to check noncontainment. Suppose
the direction `-N/E` were explained on an `a`-subset `S` by a degree-`<k`
polynomial `G`. Then

```text
E G + N
```

has degree `< k+t = a` and vanishes on the `a` points of `S`, so it is the
zero polynomial. This would imply `E | N`, contradicting `[N]_E != 0` and
`deg N < deg E`. Hence the direction is not explained on any active support,
and every cloud-intersection slope is support-wise noncontained.

## Proof Of The Locator-Split Claim

Put

```text
I = S cap T.
```

Choose any polynomial `P_S` of degree `< k`, say `P_S=0`. Since `|I| <= k`,
there exists a polynomial `P_T` of degree `< k` satisfying

```text
E(x) P_T(x) + z_T N(x)
  = E(x) P_S(x) + z_S N(x)
```

for every `x in I`. This is ordinary interpolation on at most `k` points,
using `E(x) != 0` on `D`.

Define

```text
Q_S = z_S N + E P_S,
Q_T = z_T N + E P_T.
```

Both have degree `< k+t = a`, and they agree on `I` by construction. Define
the anchor word `w` by

```text
w(x) = Q_S(x)  for x in S,
w(x) = Q_T(x)  for x in T,
```

which is consistent on the overlap, and define `w` arbitrarily on
`D \ (S union T)`.

Then `Q_S` is a witness for slope `z_S` on support `S`, because

```text
Q_S = w on S,        Q_S == z_S N mod E.
```

Likewise `Q_T` is a witness for slope `z_T` on `T`.

It remains to check same-support noncontainment. Suppose the direction
`-N/E` were explained on either support `U in {S,T}` by a degree-`<k`
polynomial `G`. Then

```text
E G + N
```

has degree `< k+t = a` and vanishes on the `a` points of `U`, so it is the
zero polynomial. This would imply `E | N`, contradicting `[N]_E != 0` and
`deg N < deg E`. Thus both witnessed slopes are support-wise noncontained.

## Proof Of The Sunflower Floor

Choose disjoint petals `P_j subset D\I` of size `a-c`, and set

```text
S_j = I union P_j.
```

Fix common target values `h:I->F` on the core, for instance `h=0`. For each
`j`, interpolate a polynomial `R_j` of degree `< k` satisfying

```text
E(x) R_j(x) + z_j N(x) = h(x)
```

for every `x in I`. This is possible because `|I|=c<=k` and `E` is nonzero
on `D`. Put

```text
Q_j = z_j N + E R_j.
```

Then `deg Q_j < k+t = a`, and all `Q_j` agree with `h` on the common core.
Define `w=Q_j` on each `S_j`; this is consistent because the petals are
pairwise disjoint and all overlaps are exactly the core. Define `w`
arbitrarily outside the union of the supports.

Each `Q_j` is a witness for slope `z_j` on `S_j`, since `Q_j=w` on `S_j` and
`Q_j == z_j N mod E`. The same noncontainment argument used above applies on
each support, so all `m` slopes are support-wise bad.

## Explicit Quadratic-Extension Packet

Take

```text
B = F_17,
F = B[alpha],        alpha^2 = 3,
D = B^*,
k = 3,
sigma = t = 2,
a = 5,
E = X(X-alpha),
N = 1.
```

The denominator is nonzero on `D`, and

```text
hatE = lcm(E,E^tau) = X(X-alpha)(X+alpha) = X(X^2-3).
```

Let

```text
S = {1,3,4,7,9},
T = {1,2,11,12,16}.
```

A direct calculation gives

```text
[L_S]_{hatE} = [L_T]_{hatE}.
```

Equivalently, the two locators agree at `0`, `alpha`, and `-alpha`:

```text
L_S(0)     = L_T(0)     = 9,
L_S(alpha) = L_T(alpha) = 2 + 5 alpha,
L_S(-alpha)= L_T(-alpha)= 2 + 12 alpha.
```

Thus the monic-anchor base-core readout cannot distinguish `S` from `T`.

Now assign slopes

```text
z_S = 0,        z_T = 1.
```

Since `S cap T = {1}`, choose

```text
P_S = 0,
P_T = -1/E(1) = 9 + 9 alpha.
```

Set

```text
Q_S = 0,
Q_T = 1 + E P_T.
```

Then `Q_S(1)=Q_T(1)=0`, so the anchor word

```text
w = 0 on S,
w = Q_T on T,
```

is well-defined on `S union T`, and can be defined arbitrarily elsewhere.
The polynomial `Q_S` witnesses bad slope `0` on `S`, while `Q_T` witnesses bad
slope `1` on `T`.

This is a finite, explicit separation:

```text
same locator readout modulo hatE,
different support-wise bad slopes under an arbitrary anchor.
```

The same parameters also give a sunflower-floor packet. Taking core

```text
I = {1,2,3}
```

and six disjoint two-point petals inside `D\I` realizes the six slopes

```text
0,1,2,3,4,5
```

because

```text
floor((16-3)/(5-3)) = 6.
```

## Ledger Impact

The residual-slack reduction separates the ledger cleanly. For `t<sigma`, a
degree-`t` residue-line datum should be charged to the extension list bound for
`RS[F,D,k+t]` with residual slack `sigma-t`. No separate extension-MCA object is
needed until this residual slack is too small for the list ledger to clear.

The previous monic-anchor base-core reduction is sharp in its anchor
hypothesis. In the balanced case `t=sigma`, the repaired F1 ledger cannot
replace arbitrary anchors by the locator image `S -> [L_S]_{hatE}` alone.

The remaining balanced F1 target should therefore be phrased using the
support-interpolation residue cloud

```text
S |-> [Q_S^w]_E,
```

where `Q_S^w` is the unique degree-`<a` interpolant of the arbitrary anchor
word `w` on `S`. Bounding rich intersections of this cloud with residue lines
is the actual arbitrary-anchor problem. The degenerate support-packing theorem
shows that even a successful upper bound should include at least the
`floor((|D|-k)/sigma)` free-packing term.  The gated-core construction shows
that this is not the universal arbitrary-anchor floor: compatible dense cores
can be larger, and any sharp repaired F1 ledger must budget the best
residue-compatible dense-core terms or prove that they cannot persist above
the corrected reserve.  The compatibility-system criterion gives the exact
finite object to attack next: dense packets not explained by a common gated
core correspond to nontrivial overlap-cycle solutions of `(Compat)`.

## Reproducibility

The finite packet above is checked by

```text
python3 experimental/scripts/verify_f1_arbitrary_anchor_split.py
```
