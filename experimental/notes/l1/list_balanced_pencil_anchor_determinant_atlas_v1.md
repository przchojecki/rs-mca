---
workboard_item: T
row: family-level arbitrary-word Reed-Solomon exact shell
object: LIST
target_epsilon: not_applicable
agreement: symbolic integer m in the balanced band 2m <= n+K-1
B_star: not_applicable
direct_statement: the complete exact shell is one primitive anchor quotient/remainder split graph, with canonical owner gcds and an exact per-owner split-linear-system bound
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: U_list_int balanced interpolation-module interior
quantifier: every field, every n-point evaluation set, every received word, and every nonempty exact shell in the declared band
projection_and_unit: distinct degree-below-K codewords
claimed_bound: per fixed owner E, the minimum of floor(binomial(m,r)/(w+j-r+2)) and floor(binomial(m,j+1)/binomial(w+1+j,j+1))
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: two exact neighbors with the same determinant coordinate, failure of owner recovery by gcd, or a fixed-owner family violating the printed matroid bound
replay: analytic proof; no computational claim
---

# Balanced-pencil anchor determinant atlas for exact LIST shells

## 1. Purpose and scope

This note gives a direct arbitrary-word LIST theorem for the balanced
interpolation-module interior. It does three things exactly:

1. removes coefficient-pair multiplicity by one anchor determinant;
2. recovers the common-complement owner by a gcd; and
3. bounds every fixed owner by a root-matroid basis ledger.

It also places all owners in one received-word-dependent Pade family through
a Bezout dual to the anchor; the owners are gcd strata of that family, not
independently chosen pencils.

The top-intersection stratum is precisely the one-parameter moving-root
pencil already used in BC. The theorem does **not** supply a deployed
`U_list_int`: the number of common-complement owners can be exponential, and
the aggregate owner image remains open.

## 2. Setup

Let `D` be an `n`-point evaluation set over a field `F`, with squarefree
locator

```text
Omega(X)=product_(x in D)(X-x).
```

Fix a received word `U` and an exact agreement shell of size `m>K`. Put

```text
w=m-K,       omega=n-m,       s=omega-w=n-2m+K>=1.     (1)
```

Use the interpolation module

```text
M_U={(W,N): N(x)=W(x)U(x) for every x in D}
```

with shifted degree

```text
sdeg(W,N)=max(deg W,deg N-(K-1)).
```

Let `g_1=(W_1,N_1),g_2=(W_2,N_2)` be a shifted weak-Popov basis with

```text
det(g_1,g_2)=gamma Omega,       gamma in F^x,
d_1+d_2=n-K+1=omega+w+1,
d_1<=d_2<=omega.                                      (2)
```

Put

```text
alpha=omega-d_1,       beta=omega-d_2.
```

Then `alpha+beta=s-1`. Every exact shell member has a unique representation

```text
(W,N)=A g_1+B g_2,
deg A<=alpha,       deg B<=beta,
W monic of degree omega,       N=WP,       deg P<K.   (3)
```

The coefficient pair is primitive:

```text
gcd(A,B)=1.                                            (4)
```

Indeed, a nonconstant common divisor also divides `W`. Dividing the module
vector by it shows that each removed domain root is an additional agreement
of `P`, contrary to exactness.

Conversely, suppose a split support codeword has one extra agreement at a
root `x` of `W`. Since `W` is squarefree, divide `(W,N)` by `X-x`. The
quotient still belongs to `M_U`: the module equations divide at every other
domain point, and at `x` they hold because `P(x)=U(x)`. Uniqueness of basis
coordinates then shows that `X-x` divides both `A` and `B`. Therefore, for
every split support codeword in `(3)`, exactness is equivalent to `(4)`.

## 3. The determinant coordinate

Fix one exact member

```text
(A_0,B_0,W_0,N_0,P_0).
```

For every degree-capped coefficient pair whose denominator is monic of
degree `omega`, define

```text
Delta_0(A,B)=A_0B-B_0A.                               (5)
```

### Theorem 1: affine determinant coordinates

The map in `(5)` is an affine bijection from the monic coefficient body onto

```text
F[X]_(<=s-1),
```

and sends the anchor to zero.

#### Proof

The coefficient-pair space has dimension

```text
(alpha+1)+(beta+1)=s+1.
```

Monicity is one nonzero affine equation, so the source of `(5)` has
dimension `s`; the target has dimension `s` as well.

Suppose two monic pairs have the same determinant. Their difference `(A,B)`
satisfies `A_0B-B_0A=0`. By `(4)` there is a polynomial `T` with

```text
(A,B)=T(A_0,B_0).
```

The corresponding denominator difference is `TW_0`. If `T` is a nonzero
constant, its degree-`omega` coefficient is nonzero, contradicting the
cancellation of the two monic leading coefficients. If `deg T>0`, then
`deg(TW_0)>omega`, contradicting the coefficient caps. Hence `T=0`, proving
injectivity; equal dimensions prove bijectivity. QED.

### Corollary 1.1: global anchor-Pade transport

Choose Bezout polynomials `u,v` with

```text
uA_0+vB_0=1
```

and define the dual module vector

```text
(J,K)=-v g_1+u g_2,       L_0=Omega/W_0.              (5a)
```

Every point of the monic coefficient body has a unique decomposition

```text
(W,N)=T(W_0,N_0)+Delta_0(J,K),                         (5b)
K=JP_0+gamma L_0,
W=T W_0+Delta_0J,
N=WP_0+gamma Delta_0L_0.                               (5c)
```

Moreover,

```text
gcd(J,W_0)=1,
gcd(W,W_0)=gcd(Delta_0,W_0).                           (5d)
```

At every codeword point `N=WP`, this gives the global Pade identity

```text
W(P-P_0)=gamma Delta_0L_0.                             (5e)
```

#### Proof

The coefficient pairs `(A_0,B_0)` and `(-v,u)` have determinant one. Hence
every pair is uniquely

```text
(A,B)=T(A_0,B_0)+Delta_0(-v,u),
```

which proves `(5b)` and the denominator formula. The corresponding module
vectors satisfy

```text
W_0K-JN_0=gamma Omega.
```

Using `N_0=W_0P_0` and cancelling `W_0` gives
`K=JP_0+gamma L_0`; the remaining identities in `(5c)` and `(5e)` follow.

If a root `x` of `W_0` were also a root of `J`, then `(5c)` would give
`K(x)=gamma L_0(x)!=0` by squarefreeness. But `(J,K)` is a module vector, so
`K(x)=J(x)U(x)=0`, a contradiction. Thus `J` is a unit modulo `W_0`.
Reducing the denominator formula modulo `W_0` proves `(5d)`. QED.

### Corollary 1.2: exact primitive quotient/remainder graph

Euclidean-divide

```text
Delta_0J=Q_Delta W_0+R_Delta,       deg R_Delta<omega. (5f)
```

Then the coefficient-body point with determinant `Delta_0` has

```text
T_Delta=1-Q_Delta,
W_Delta=W_0+R_Delta.                                  (5g)
```

The complete exact shell is in bijection with

```text
{Delta_0 in F[X]_(<=s-1):
 W_Delta divides Omega,
 gcd(Delta_0,1-Q_Delta)=1}.                           (5h)
```

For every split point in `(5h)`, divisibility `W_Delta|N_Delta` is
automatic. The gcd is exactly the complete-agreement coefficient-content
guard.

#### Proof

Substitute `(5f)` into `W=T W_0+Delta_0J`. The remainder has degree below
`omega`, while both `W` and `W_0` are monic of degree `omega`; hence
`T+Q_Delta=1`, proving `(5g)`.

The anchor/dual coefficient transformation has determinant one, so it
preserves the coefficient ideal:

```text
(A,B)=(T_Delta,Delta_0)
```

as ideals of `F[X]`. Exactness is therefore precisely the gcd condition in
`(5h)`.

Suppose `W_Delta|Omega`. By `(5d)`, put

```text
E=gcd(W_Delta,W_0)=gcd(Delta_0,W_0).
```

Write `W_Delta=EY`. Since both denominators are squarefree divisors of the
same `Omega`, one has `Y|L_0`; also `E|Delta_0`. Formula `(5c)` now shows
that `W_Delta` divides `N_Delta`. The shifted-degree cap gives
`deg(N_Delta/W_Delta)<K`. Thus every split point gives a support codeword,
and the gcd guard makes that support complete. The converse follows from
the exact member construction. QED.

## 4. Exact owner recovery

Take a distinct exact neighbor and write

```text
E=gcd(W_0,W),       W_0=EX,       W=EY,
Omega=EXYG.                                           (6)
```

Here `G` is the common agreement locator. Since both codewords agree with
`U` on `G`, write

```text
P-P_0=GR.                                              (7)
```

### Theorem 2: canonical common-complement certificate

The neighbor satisfies

```text
Delta_0=E R/gamma,       gcd(Delta_0,W_0)=E.           (8)
```

Thus `Delta_0` determines the neighbor and recovers its exact
common-complement owner by one gcd.

If

```text
j=s-1-deg E,       h=deg X=deg Y,
```

then

```text
0<=j<=min(K-1,s-1),
deg G=K-1-j,       h=w+1+j,       deg R<=j.            (9)
```

Moreover, `R` is nonzero on all roots of `X` and `Y`.

The fixed-owner quotient lies on the explicit linear remainder graph

```text
Y=X+rem_X((R/gamma)J).                                 (9a)
```

#### Proof

Bilinearity of the module determinant gives

```text
W_0N-WN_0=Delta_0 gamma Omega.                        (10)
```

Using `N=WP`, `(6)`, and `(7)`, equation `(10)` becomes

```text
E^2XYGR=Delta_0 gamma EXYG,
```

which proves the first identity in `(8)`. At a root of `X`, the neighbor
agrees with `U` and the anchor does not; at a root of `Y`, the roles reverse.
Hence `R` is nonzero on both exchanged root sets. Since `W_0=EX` is
squarefree, the gcd identity follows.

If `g=deg G`, then

```text
deg E=n-2m+g,       h=m-g.
```

Substitution into the definition of `j` gives `(9)`, and
`deg R<=K-1-g=j`. Theorem 1 gives uniqueness from `Delta_0`.

For `(9a)`, reduce `W=T W_0+Delta_0J` modulo `W_0`, substitute
`(W,W_0,Delta_0)=(EY,EX,ER/gamma)`, and cancel `E`. This gives
`Y=(R/gamma)J mod X`. Since `X` and `Y` are monic of the same degree, their
difference is the canonical remainder in `(9a)`. QED.

## 5. Fixed-owner split-linear-system bound

Fix a monic divisor `E|W_0` of degree `s-1-j`. Let `C_E` be the exact
neighbors satisfying `gcd(W_0,W)=E`, and define

```text
V_E=span_F({W_0/E} union {W/E: W in C_E}),
r_E=dim(V_E)-1.                                        (11)
```

### Theorem 3: root-matroid payment

If `C_E` is nonempty, then

```text
1<=r_E<=j+1                                            (12)
```

and

```text
|C_E|<=floor(binomial(m,r_E)/(h-r_E+1)).              (13)
```

At `j=0`, necessarily `r_E=1`, so

```text
|C_E|<=floor(m/(w+1)).                                 (14)
```

This is the list-side one-parameter moving-root bound after deleting the
anchor parameter.

Independently of `r_E`, one also has the rank-free local Johnson packing

```text
|C_E|<=floor(binomial(m,j+1)/binomial(w+1+j,j+1)).    (14a)
```

Use the minimum of `(13)` and `(14a)`; they coincide when `j=0`.

#### Proof

By `(8)`, all determinant coordinates in `C_E` have the form `ER` with
`deg R<=j`. Theorem 1 therefore places their coefficient pairs in affine
dimension at most `j+1`. Taking denominators and dividing by `E` gives
`dim V_E<=j+2`, proving the upper half of `(12)`; a nonempty neighbor set
forces `r_E>=1`.

Put `X=W_0/E`. Every neighbor quotient `Y=W/E` is a monic degree-`h`
locator supported on the anchor's `m` agreement points. Evaluate `V_E` on
the `h` roots of one such `Y`. The evaluation kernel is exactly the line
spanned by `Y`: every polynomial in `V_E` has degree at most `h`, and a
polynomial vanishing on those `h` distinct points is a scalar multiple of
their locator. Thus the evaluation rows have rank `r_E`.

They have no loops, because `X` belongs to `V_E` and is nonzero at every
anchor agreement point. A loopless rank-`r` matroid on `h` elements has at
least `h-r+1` bases: choose one basis, then exchange each outside element
through its fundamental circuit to obtain one distinct additional basis.

An independent `r_E`-subset cannot be a root basis for two different
neighbors. Its evaluation rows have a one-dimensional kernel in `V_E`, so
they determine one projective polynomial and monicity determines one `Y`.
There are only `binomial(m,r_E)` available subsets. This proves `(13)`, and
`j=0` gives `(14)`.

For `(14a)`, take two distinct neighbors in `C_E`. Their degree-below-`K`
codewords agree with each other on at most `K-1` domain points. Since both
individual agreement sets have size `m`, their complement locators satisfy

```text
deg gcd(W_1,W_2)<=n-2m+K-1=s-1.
```

Writing `W_i=EY_i` and `deg E=s-1-j` gives
`deg gcd(Y_1,Y_2)<=j`. Every `Y_i` is an `h=w+1+j` subset of the anchor's
`m` agreement points, so no `(j+1)`-subset belongs to two neighbors.
Counting these subsets proves `(14a)`. QED.

## 6. Aggregate ledger and route boundary

There are `binomial(omega,s-1-j)` possible owners `E` at deficiency `j`.
Therefore the theorem gives the global but generally weak ceiling

```text
N_j <= binomial(omega,s-1-j)
       min{
         floor(binomial(m,j+1)/binomial(w+1+j,j+1)),
         max_(1<=r<=j+1)
         floor(binomial(m,r)/(w+j-r+2))
       }.                                              (15)
```

Equation `(15)` is deliberately not called a list-interior payment. The
owner factor can be exponential at the active rows. The exact next theorem
must do at least one of the following:

- coalesce many `E` into one received-word/Pade payment;
- prove a reserve-sized bound on the realized owner image;
- route growing `j` to an earlier quotient, tangent, prefix, or common
  owner; or
- construct a family showing that such owner coalescence is false.

The theorem therefore supplies a source-bound architecture bridge and the
complete fixed-owner payment. Corollary 1.1 coalesces the *representation* of
all owners into one Pade family, but gives no bound on its realized gcd
strata. Corollary 1.2 identifies the exact global object as one primitive
split-divisor quotient/remainder graph. A row-sharp count of that graph, or a
typed transport to the pruned locator-prefix Q atom, is still the live
`U_list_int` obligation.
