# L2 Interleaved Support-Fiber Bridge

**Status:** PROVED for the finite support injection; CONDITIONAL when a future
locator-fiber theorem is used as input.

This note isolates a useful L2 bridge.  The trivial protocol ledger bound

```text
|Lambda(Int(C,mu),delta)| <= |Lambda(C,delta)|^mu
```

can overcharge the interleaving arity.  If the available theorem bounds
agreement supports rather than only codewords, then column-distance interleaving
does not multiply the exponent by `mu`: all rows must agree on the same columns.

## Setup

Let `C=RS[F,H,k]` with `|H|=n`.  The same argument applies to any code whose
restriction to every support of size at least `k` is injective.  For a received
word `U:H -> F` and `a >= k`, write

```text
Fib_U(a) = {S subset H : |S|=a and U|S agrees with some c in C}.
```

For a `mu`-row received word

```text
U = (U_1,...,U_mu) in (F^H)^mu,
```

define the simultaneous feasible-support fiber

```text
Fib_U^cap(a) = Fib_U1(a) cap ... cap Fib_Umu(a).
```

The interleaved code `Int(C,mu)` uses column distance: a tuple
`(c_1,...,c_mu)` is within radius `1-a/n` of `U` iff there is a support
`A subset H` of size at least `a` on which every row agrees.

## Bridge Lemma

For every `mu >= 1`, every `a >= k`, and every interleaved received word `U`,

```text
|Lambda(Int(C,mu),1-a/n,U)| <= |Fib_U^cap(a)|.
```

Consequently,

```text
|Lambda(Int(C,mu),1-a/n,U)|
  <= min_i |Fib_Ui(a)|.
```

If a uniform support-fiber theorem proves

```text
|Fib_V(a)| <= n^B
```

for every received word `V`, then

```text
|Lambda(Int(C,mu),1-a/n)| <= n^B.
```

No `mu B` exponent is lost.

## Full-Agreement Support Formula

The feasible `a`-subset fiber above is a useful upper-bound object, but it can
overcount badly when a row agrees with a codeword on many more than `a`
positions.  The exact repaired object is the full agreement-support profile.

For a received word `V:H -> F`, define

```text
Supp_V^{>=a}
  = { A_V(c) : c in C, |A_V(c)| >= a },

A_V(c) = { x in H : c(x)=V(x) }.
```

For `a >= k`, the map from listed codewords to `Supp_V^{>=a}` is injective for
Reed-Solomon codes, because the full agreement support has size at least `k`.

For a `mu`-row received word `U=(U_1,...,U_mu)`, the interleaved list size is
exactly

```text
|Lambda(Int(C,mu),1-a/n,U)|
 =
 |{ (A_1,...,A_mu) :
      A_i in Supp_Ui^{>=a} for every i,
      |A_1 cap ... cap A_mu| >= a }|.
```

Thus L2 is not intrinsically controlled by the Cartesian product of row list
sizes; it is controlled by the intersection profile of the full agreement
supports.  In particular, if the row support families are `a`-wise disjoint in
the sense that no off-diagonal tuple has intersection of size at least `a`,
then the interleaved list contains only the diagonal or otherwise matched
tuples, even when every row list is large.

This formula also repairs the raw-support overcount that appears for low-degree
received words.  If `V` itself is a codeword, then `Supp_V^{>=a}={H}`, whereas
the raw feasible fiber `Fib_V(a)` contains every `a`-subset of `H`.

The relation between the raw feasible fiber and full supports is exact. For
`a >= k`,

```text
|Fib_V(a)|
  = sum_{A in Supp_V^{>=a}} binom(|A|,a).
```

More generally, for `U=(U_1,...,U_mu)`,

```text
|Fib_U^cap(a)|
 =
 sum_{(A_1,...,A_mu)}
   binom(|A_1 cap ... cap A_mu|,a),
```

where the sum ranges over `A_i in Supp_Ui^{>=a}` and terms with intersection
size `<a` are read as zero.  Therefore

```text
|Fib_U^cap(a)| >= |Lambda(Int(C,mu),1-a/n,U)|,
```

with equality exactly when every listed interleaved tuple has common agreement
support of size exactly `a`.  This is the precise overcount factor that a
certificate should print when it uses raw `a`-subset fibers as a proxy for
interleaved lists.

## Intersection-Codegree Certificate

The full-support formula also gives a compact certificate that is sharper than
the Cartesian product.  For two row support families

```text
P = Supp_U1^{>=a},        Q = Supp_U2^{>=a},
```

define the ordered common-intersection profile

```text
C_r(P,Q) = |{(A,B) in P x Q : |A cap B| = r}|.
```

Then the two-row interleaved list size is exactly

```text
sum_{r>=a} C_r(P,Q).
```

Equivalently, with the max common-intersection codegrees

```text
Gamma_{>=a}(P,Q)
  = max_{A in P} |{B in Q : |A cap B| >= a}|,

Gamma_{>=a}(Q,P)
  = max_{B in Q} |{A in P : |A cap B| >= a}|,
```

one has

```text
|Lambda(Int(C,2),1-a/n,U)|
  <= min(|P| Gamma_{>=a}(P,Q), |Q| Gamma_{>=a}(Q,P)).
```

More generally, for `mu` rows the exact count is the number of tuples

```text
(A_1,...,A_mu),        A_i in Supp_Ui^{>=a},
```

whose common intersection has size at least `a`; the corresponding certificate
is any upper bound on the maximum number of completions after fixing one row's
full support.  Thus L2 certificate emitters can record full-support sizes plus
common-intersection codegrees, rather than only row list sizes.

If all full supports in two rows have size at most `a+c`, then every listed
pair satisfies

```text
|A \ B| <= c,        |B \ A| <= c.
```

Thus a small near-exact-support neighborhood already rules out product growth.
The exact-support diagonalization lemma is the case `c=0`: intersection size
at least `a` forces equal supports.

Here is the corresponding quantitative bound.  Suppose every row full-support
family `P_i` contains only sets of sizes between `a` and `a+c`.  For a fixed
support `A` of size `s=a+d`, `0 <= d <= c`, every support `B` with
`|B| <= a+c` and `|A cap B| >= a` is obtained by deleting `i` points from `A`
and adding `j` points outside `A`, with

```text
0 <= i <= d,        0 <= j <= c-d+i.
```

Thus define the Johnson-neighborhood size

```text
J_{n,a,c}(s)
  = sum_{i=0}^{s-a} binom(s,i)
      sum_{j=0}^{c-(s-a)+i} binom(n-s,j).
```

For `mu` rows, fixing one row support `A in P_i` forces every other row support
into this neighborhood, because a common intersection of size at least `a`
implies pairwise intersection at least `a` with `A`.  Hence

```text
|Lambda(Int(C,mu),1-a/n,U)|
  <= min_i sum_{A in P_i} J_{n,a,c}(|A|)^(mu-1).
```

Since every summand has degree at most `2c` in `n`, the crude uniform estimate

```text
J_{n,a,c}(s) <= (c+1)^2 n^(2c)
```

also holds.  Therefore, for fixed `c`, near-exact support profiles cost only a
polynomial completion factor after one row is chosen.  The case `c=0` recovers
exact-support diagonalization: `J_{n,a,0}(a)=1`.

A sharper certificate uses support-size layers instead of only the maximum
excess.  For a row family `P_i`, write

```text
B_i(s) = |{A in P_i : |A|=s}|.
```

For a fixed anchor support `A` of size `r`, the number of all `s`-subsets of
`H` with intersection at least `a` with `A` is the Johnson layer kernel

```text
K_{n,a}(r,s)
  = sum_{u=a}^{min(r,s)} binom(r,u) binom(n-r,s-u).
```

Thus, after fixing an anchor `A in P_i` of size `r`, the number of possible
row-`j` supports of size `s` is at most

```text
min(B_j(s), K_{n,a}(r,s)).
```

Summing over layers and multiplying over the other rows gives

```text
|Lambda(Int(C,mu),1-a/n,U)|
  <= min_i sum_r B_i(r)
       prod_{j != i} sum_s min(B_j(s), K_{n,a}(r,s)).
```

This layered bound is often much sharper than the uniform `c`-excess bound:
large supports only hurt if there are many of them in compatible layers.  In
particular, a row with the single full support `H` has layer count `B(n)=1`,
so repeated-codeword rows are certified diagonally even though their support
excess is `n-a`.

## Random-Received Baseline

The exact support formula has a clean average-case shadow.  Let `|F|=q`, and
sample the `mu` received rows `U_1,...,U_mu` independently and uniformly from
`F^H`.  Then

```text
E |Lambda(Int(C,mu),1-a/n,U)|
 =
 q^(mu k) Pr[Bin(n,q^(-mu)) >= a].
```

For one row,

```text
E |Lambda(C,1-a/n,V)|
 =
 q^k Pr[Bin(n,q^(-1)) >= a],
```

and independent rows give

```text
E prod_i |Lambda(C,1-a/n,U_i)|
 =
 (q^k Pr[Bin(n,q^(-1)) >= a])^mu.
```

The simple union bound over `a`-subsets gives the comparison

```text
E |Lambda(Int(C,mu),1-a/n,U)|
  <= binom(n,a) q^(-mu(a-k)),
```

whereas the corresponding product-of-base-lists baseline is bounded by

```text
binom(n,a)^mu q^(-mu(a-k)).
```

Thus random interleaving pays the polynomial-choice factor `q^k` in each row,
but it pays the support-selection entropy only once.  This is not a worst-case
L2 theorem, because adversarial received rows may align their full supports.
It is the benchmark a worst-case certificate should try to recover after
quotient-core and other structured support packets are separated.

## Repeated-Row and Quotient-Core Diagonalization

There is one exact case where no interleaving exponent can appear.  For any
received word `V:H -> F`,

```text
|Lambda(Int(C,mu),1-a/n,(V,...,V))|
 =
 |Lambda(C,1-a/n,V)|.
```

Indeed, any interleaved tuple listed against the repeated row has a common
agreement set `S` of size at least `a`; all row codewords agree with `V` on
`S`, hence agree with one another on at least `k` points and are equal.

This matters for the quotient-core obstruction.  In the notation of
`tex/slackMCA_v3.tex`, let `K <= H` have order `M`, put `N=n/M`, assume
`M | k`, write `ell=k/M`, and choose a slack set `T` of size `sigma<M` inside
one omitted `K`-coset `C_0`.  The quotient-core packet has one support

```text
S_A = T union U_A
```

for each `ell`-subset `A` of `H/K \ {C_0}`, where `U_A` is the union of the
`K`-cosets in `A`.  Thus the base packet size is

```text
L = binom(N-1,ell).
```

For a `mu`-tuple from this packet,

```text
|S_{A_1} cap ... cap S_{A_mu}|
  = sigma + M |A_1 cap ... cap A_mu|.
```

At the quotient-core agreement threshold `a=k+sigma`, this is at least `a`
iff `A_1=...=A_mu`.  Therefore the aligned quotient-core packet contributes
exactly

```text
L
```

interleaved tuples, not `L^mu`.  If the rows use slack sets `T_i` in the same
omitted coset and `|T_1 cap ... cap T_mu|<sigma`, then this exact-threshold
packet contributes zero tuples.  The known quotient-core lower-bound packet
therefore shares its support parameter under column interleaving; it does not
itself force the Cartesian-product exponent.

The same packet has an exact threshold spectrum below `k+sigma`.  Let

```text
tau = |T_1 cap ... cap T_mu|,        Q = N-1,
h(a,tau) = ceil((a-tau)/M).
```

Interpret `h(a,tau) <= 0` as `0`, and if `h(a,tau)>ell` the count below is
zero.  For `0 <= c <= ell`, put

```text
E_empty(R,b,mu)
  = sum_{j=0}^b (-1)^j binom(R,j) binom(R-j,b-j)^mu.
```

This is the number of `mu` ordered `b`-subsets of an `R`-element quotient
universe with empty common intersection.  Therefore the exact packet count at
agreement threshold `a` is

```text
L_mu(a,tau)
  = sum_{c=h(a,tau)}^ell
      binom(Q,c) E_empty(Q-c,ell-c,mu).
```

Indeed, `c` is the exact size of the common quotient intersection
`A_1 cap ... cap A_mu`; choose that common intersection, then remove it from
each row and require the remaining quotient choices to have no common point.

This formula interpolates between the diagonal and Cartesian extremes:

```text
h=ell      gives L_mu = binom(Q,ell) = L,
h=0        gives L_mu = binom(Q,ell)^mu = L^mu.
```

Thus the aligned quotient-core packet is exactly diagonal at the endpoint
`a=k+sigma`, but as the agreement threshold drops, the growth is controlled by
the common-intersection tail of `mu` quotient subsets rather than by an
unstructured product bound.

## Extension-Coordinate Support Formula

Let `B <= F` be finite fields with `[F:B]=e`, let `H subset B`, and set

```text
C_B = RS[B,H,k],        C_F = RS[F,H,k].
```

Fix a `B`-basis of `F` and write `pi_j:F -> B` for its coordinate maps.  For
an extension-valued received word `U:H -> F`, put `U_j=pi_j(U)`.  Then the
extension-code list is exactly the coordinate-interleaved base list:

```text
|Lambda(C_F,1-a/n,U)|
 =
 |{ (A_1,...,A_e) :
      A_j in Supp_Uj^{>=a} for every j,
      |A_1 cap ... cap A_e| >= a }|.
```

Equivalently, this is the full-support version of the manuscript identity

```text
|Lambda(C_F,delta)| = |Lambda(Int(C_B,e),delta)|.
```

Thus an extension-code list certificate may use the same common-intersection
profile as L2 after expanding in any `B`-basis.  The formula is basis-invariant
as a list count, although the individual coordinate support families printed
by a certificate depend on the chosen basis.

## Proof

Take an interleaved listed codeword

```text
c = (c_1,...,c_mu) in Int(C,mu)
```

that agrees with `U` on at least `a` columns.  Choose a canonical `a`-subset
`S_c` of its common agreement set.  Then `S_c in Fib_Ui(a)` for every row `i`,
so `S_c in Fib_U^cap(a)`.

The map `c -> S_c` is injective when `a >= k`.  Indeed, if two interleaved
codewords map to the same support `S`, then for each row `i` the two row
codewords agree with the same word `U_i` on `S`.  Since two codewords of a
Reed-Solomon code of dimension `k` are equal once they agree on at least `k`
evaluation points, the row codewords are equal for every `i`; hence the
interleaved codewords are equal.

Thus the interleaved list injects into the simultaneous feasible-support fiber.
The `min_i` bound follows from `Fib_U^cap(a) subset Fib_Ui(a)` for every row.

For the full-agreement formula, send an interleaved listed codeword

```text
c = (c_1,...,c_mu)
```

to the tuple

```text
(A_U1(c_1),...,A_Umu(c_mu)).
```

The tuple lies in the displayed set because the common agreement columns of
`c` with `U` are exactly

```text
A_U1(c_1) cap ... cap A_Umu(c_mu),
```

and listing means this intersection has size at least `a`. Conversely, any
tuple in the displayed set comes from unique row codewords, since each support
has size at least `a >= k`; those row codewords form an interleaved codeword
with at least `a` common agreement columns. These two maps are inverse to each
other.

For the raw-to-full decomposition, every raw feasible `a`-subset `S in
Fib_V(a)` is explained by a unique codeword when `a >= k`. Its full agreement
support `A_V(c)` contains `S`, and each `a`-subset of `A_V(c)` is feasible.
Summing over the full supports gives the displayed formula for `|Fib_V(a)|`.
The simultaneous version is the same argument applied to a common raw subset
`S`: it must lie inside each row's unique full agreement support, hence inside
`A_1 cap ... cap A_mu`, and every `a`-subset of that intersection contributes
to `Fib_U^cap(a)`.

The intersection-codegree certificate is just the full-support formula grouped
by the common intersection size.  For two rows, summing the profile `C_r(P,Q)`
over `r>=a` gives the exact list count.  Bounding each row `A in P` by at most
`Gamma_{>=a}(P,Q)` compatible supports in `Q` gives the first max-codegree
bound; reversing the roles gives the symmetric bound.  If `|A|,|B| <= a+c`
and `|A cap B| >= a`, then `|A\B|=|A|-|A cap B| <= c` and similarly
`|B\A| <= c`.

For the random-received baseline, fix an interleaved codeword

```text
c = (c_1,...,c_mu).
```

At each coordinate `x in H`, the random column `U(x)` equals `c(x)` with
probability `q^(-mu)`, independently over coordinates.  Hence the number of
common agreement columns has distribution `Bin(n,q^(-mu))`.  Linearity of
expectation over the `q^(mu k)` interleaved codewords gives the displayed
expectation.  The one-row formula is the same argument with success
probability `q^(-1)`, and independence of the received rows gives the product
expectation.  Finally, the event of at least `a` successes is contained in the
union over `a`-subsets on which all coordinates match, giving
`Pr[Bin(n,theta)>=a] <= binom(n,a)theta^a`.

For repeated rows, let `(c_1,...,c_mu)` be an interleaved listed codeword
against `(V,...,V)`, and let `S` be a common agreement set with `|S|>=a`.  Then
each `c_i` agrees with `V` on `S`.  Since `a>=k`, the codewords `c_i` are all
equal.  The diagonal map from the base list to the repeated-row interleaved
list is therefore a bijection.

For the quotient-core packet, the support formula follows from the construction
itself.  Each packet codeword has full agreement support `S_A=T union U_A`,
because the difference from the received word is `L_T L_A`, whose zeros on
`H` are exactly `T union U_A`.  Intersecting `mu` such supports leaves the
common slack set plus the common quotient cosets, so the size is
`sigma + M |A_1 cap ... cap A_mu|`.  Since each `A_i` has size `ell=k/M`, this
reaches `k+sigma=M ell+sigma` exactly when all `A_i` are equal.  If the row
slack sets have common intersection smaller than `sigma`, even equal quotient
choices give fewer than `k+sigma` common points.

For the extension-coordinate formula, every `P in F[X]_{<k}` has coordinate
polynomials `P_j=pi_j(P) in B[X]_{<k}`, and the map

```text
P <-> (P_1,...,P_e)
```

is a bijection between `C_F` and `Int(C_B,e)` once a basis is fixed.  For each
`x in H`, equality `P(x)=U(x)` in `F` is equivalent to the coordinate
equalities `P_j(x)=U_j(x)` for every `j`.  Hence the extension agreement
support of `P` is exactly the intersection of the coordinate-row agreement
supports.  Applying the full-agreement support formula to the `e` coordinate
rows gives the displayed identity.  Changing the basis composes the coordinate
rows by an invertible `B`-linear transformation and changes the printed
support families, but not the underlying extension codewords or their
agreement sets.

## Ledger Consequence

This bridge does not say that a base-code list-size bound transfers without a
`mu` exponent.  It says that a support-fiber theorem transfers without a `mu`
exponent.

That distinction matters for the L1/L2 program.  The locator local-limit target
in `agents.md` is naturally a bound on feasible agreement supports.  If it is
proved in that form, the interleaved-list ledger in `tex/snarks_v4.tex` can use
the same numerator for every constant arity `mu`, rather than the conservative
product numerator.

For an extension-code presentation `C_F` over an extension `F/B` of degree `e`,
the manuscript identity

```text
|Lambda(C_F,delta)| = |Lambda(Int(C_B,e),delta)|
```

can therefore consume a base-field simultaneous-support bound directly.  The
generated-field entropy ledger is unchanged, but the list-size-over-field term
need not pay a Cartesian-product support exponent if the locator theorem is
available in support-fiber form.

The extension-coordinate formula makes that statement certificate-facing.  A
certificate for an extension-code list can expand the received word in a chosen
`B`-basis, print the coordinate full-support families, and then apply the same
common-intersection or codegree ledger used for ordinary interleaving.  This is
not permission to pay the generated-field entropy bill with `|F|`: the support
families are still base-field locator objects over `B`; only the final
list-size-over-field denominator changes when the protocol really consumes the
extension code.

The full-agreement formula is the sharper finite object for certificate
emitters.  It says that a future L1 theorem should ideally output or bound the
number and intersection profile of full agreement supports, not just the raw
number of feasible `a`-subsets.  This is especially important in the presence
of contained supports: raw fibers can be exponentially larger than the actual
list, while the full-support profile remains in bijection with the listed row
codewords and composes exactly under interleaving.

The raw-to-full identity gives a diagnostic for when a raw support-fiber bound
is still safe for L2 without wasting too much.  If every relevant full
agreement support has size at most `a+c`, then the raw fiber overcounts the
full-support profile by at most `binom(a+c,a)` per row object.  If some row has
near-full agreement supports, the raw fiber can be larger by `binom(n,a)` even
when the actual row list has size one.

The intersection-codegree certificate is the L2 analogue of the strict-overlap
ledgers used in M1.  Once full agreement supports are known, the expensive
quantity is not the product of row list sizes; it is the number of row-support
tuples with common intersection at least `a`.  Exact-support and near-exact
support packets can therefore be certified by small overlap neighborhoods.

The quotient-core packet calculation answers one of the concrete L2 questions
from `agents.md`: the standard aligned quotient-core lower-bound packet does
not multiply under interleaving.  It remains an essential base-list obstruction
and quotient-reserve floor, but its shared support parameter means the L2
ledger should not automatically raise that particular packet size to the
`mu`th power.  A worst-case interleaved theorem still has to rule out other
row alignments, but the known quotient-core packet is a diagonal rather than a
Cartesian source.

## Follow-Up Checks

- Match the manuscript's locator local-limit assumption to `Fib_U(a)` rather
  than only to `|Lambda(C,delta,U)|`.
- Prefer a maximal/full-support version of that assumption when using it for
  L2, because it avoids contained-support overcount and gives the exact
  interleaved intersection profile.
- Test tiny `mu=2` examples where product list bounds are loose but
  simultaneous support fibers are small.
- Record common-intersection histograms and max codegrees for those examples.
- Decide how certificate emitters should print both values: the conservative
  product bound and the sharper support-fiber bridge when its hypothesis is
  available.
- Feed active rows from `experimental/quotient_profile.py` into
  `experimental/quotient_core_interleaving.py` so protocol ledgers can display
  both the base quotient-core packet and its aligned L2 packet count.
