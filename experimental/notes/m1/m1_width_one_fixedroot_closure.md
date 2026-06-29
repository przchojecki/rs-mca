# M1 Width-One Fixed-Root Closure

**Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-29.

This note extracts a compact width-one consequence from the M1 Hankel-pencil
route.  It does not prove the all-line M1 theorem.  Its purpose is to isolate
the first low-width critical-tail obstruction and show that, in fixed surplus,
that obstruction reduces to the already exposed one-root fixed-divisor
root-slice ledger.

## Setup

Work at a base-free canonical `b=2` node in the Hankel-pencil normal form.  Let

```text
V=span(P,Q) subset F[X]_{<q},        D=D^{can},        |D|=q+s,
```

where `s` is the node surplus.  For a nonzero direction `A in V`, put

```text
Z(A)={x in D : A(x)=0}.
```

A root-free width-one certificate is a direction `A` with the maximal possible
root shadow

```text
|Z(A)|=q-1.
```

Write `Z=Z(A)` and `O=D\Z`.  Then `|O|=s+1`, and the degree gap forces

```text
A=c ell_Z,        c != 0.                         (W1-shadow)
```

Equivalently, width-one certificates are exactly co-small projective fibers in
the descended two-dimensional pencil.

## Bounded-Complement Rank Test

The maximal-shadow condition can be tested on the bounded complement.  For

```text
O subset D,        |O|=s+1,
```

put

```text
L_O=ell_{D\O}.
```

Then `O` supports a width-one certificate if and only if

```text
L_O in V.                                            (W1-rank-test)
```

Indeed, if `L_O in V`, then `L_O` has exactly the root set `D\O` on `D`,
which has size `q-1`, so it gives a width-one maximal shadow.  Conversely,
every width-one direction satisfies (W1-shadow), hence is proportional to
`L_O` for `O=D\Z(A)`.

Equivalently, after choosing any coefficient basis of `F[X]_{<q}`, the rows
`P,Q,L_O` have rank at most two.  Thus all `3 x 3` coefficient minors vanish.
In fixed surplus this is a polynomial family of tests over the active tree:

```text
sum_{S in Active(A_0)} binom(|D_S^{can}|,s_S+1)
 <= (s_0+2) Q^{s_0+1} binom(Q+s_0,s_0+1),      (W1-test-count)
```

using the active-node bound and `|D_S^{can}|<=Q+s_0`, `s_S<=s_0`.  A passing
test may still carry a large co-small flag cube, but the possible complements
are now a bounded-complement algebraic search problem rather than an
unstructured family of projective directions.

## Near-Constant Pencil

Choose `B in V` independent of `A`.  Since the node is base-free, `B(x)!=0`
for every `x in Z`; otherwise both basis directions would vanish at `x`.
Thus the projective evaluation map is constant on the large fiber:

```text
[A(x):B(x)]=[0:1]        for every x in Z.        (W1-constant)
```

For `y in O`, one has `A(y)!=0`, so `[A(y):B(y)]!=[0:1]`.  Hence all
nonconstant projective information is confined to the bounded complement `O`.
In particular the good-pair capacity at this node splits as

```text
G^{can}=(q-1)(s+1)+G_O,        0<=G_O<=binom(s+1,2).  (W1-good)
```

Pairs inside `Z` are bad, every cross pair `Z x O` is good, and the only
undetermined contribution is inside `O`.

## Lossless Descent

Let `P_m subset Z` have size `m`.  In the fixed-root slice obtained by
absorbing `P_m`, the divided direction is

```text
A^{P_m}=A/ell_{P_m}=c ell_{Z\P_m}.              (W1-desc-dir)
```

The descended canonical domain is

```text
D\P_m=(Z\P_m) disjoint union O,
```

so

```text
q^{P_m}=q-m,        |Z\P_m|=q^{P_m}-1,        r^{P_m}=1.  (W1-desc)
```

Thus every rung of a width-one flag is again a width-one maximal shadow with
the same bounded complement `O`.  The operation deletes roots from one fixed
large fiber; it does not create a fresh moving-denominator problem.

## First-Root Injection

Let

```text
a=floor((q-2)/2),        R1Flag(A)=sum_{e=1}^a binom(q-1,e).
```

If `a=0`, the flag count is empty.  Otherwise order `Z` by the ambient root
order and put

```text
Z_{>x}={y in Z : y>x}.
```

The canonical first-root partition gives the exact identity

```text
R1Flag(A)
 =
 sum_{x in Z} sum_{f=0}^{a-1} binom(|Z_{>x}|,f).      (W1-first-root)
```

Indeed, a nonempty flag `E subset Z`, `|E|<=a`, has a unique first root
`x=min(E)` and a remainder `F=E\{x} subset Z_{>x}` with `|F|<=a-1`.

Each summand is a one-root fixed-divisor slice.  After exposing `x`, the
divided direction is

```text
A^x=A/(X-x)=c ell_{Z\{x}},
q^x=q-1,        r^x=1,        s^x=s,        O^x=O.   (W1-one-root)
```

For a remainder `F subset Z_{>x}`, the descendant is

```text
A^{x,F}=A/ell_{{x} union F}
       =c ell_{Z\({x} union F)}.                     (W1-slice-dir)
```

This is exactly the same descendant as the original flag `E={x} union F`,
with the first root exposed as a fixed divisor.  Therefore the whole width-one
cube embeds into the disjoint union of one-root absorbed fixed-divisor
root-slice families, preserving surplus and the bounded complement.

## Large Cubes Have Large One-Root Witnesses

The first-root partition also gives a counterexample-first form: a large
width-one cube cannot be hidden by spreading thinly across many roots.  Put

```text
M_x=# { F subset Z_{>x} : |F|<=a-1 }.
```

Then (W1-first-root) gives

```text
max_{x in Z} M_x >= R1Flag(A)/(q-1).            (W1-root-witness)
```

When `a>=1`, equivalently `q>=4`, `R1Flag(A)>=binom(q-1,a)`.  The
central-binomial lower bound gives

```text
max_{x in Z} M_x >= 2^{q-1}/(2q^2).             (W1-root-witness-exp)
```

Indeed, with `n=q-1`, the level `a=floor((q-2)/2)=floor((n-1)/2)` is central
or one step below central, so `binom(n,a)>=2^n/(2(n+1))`; dividing by
`q-1<=q` gives the displayed bound.

Thus any fixed-surplus counterexample with `q` larger than a constant multiple
of `log Q` already produces a super-polynomial one-root absorbed slice.  The
remaining obstruction is therefore visible at a single fixed root; it is not a
depth-multiplicative or many-root averaging phenomenon.

## Polynomial One-Root Slices Force Logarithmic Width

The preceding witness bound gives an explicit logarithmic-width criterion.
Suppose that, after the quotient-periodic, tangent, fixed-root, and aperiodic
charges under consideration, every first-root slice of the width-one cube is
bounded by

```text
M_x <= C Q^K
```

for constants `C,K` independent of the initial quotient width `Q`.  Then every
uncharged width-one certificate with `q>=4` satisfies

```text
2^{q-1}/(2q^2) <= C Q^K,
```

hence

```text
q <= K log_2 Q + 2 log_2 q + log_2(2C)+1.       (W1-log-width)
```

For fixed `C,K`, this forces `q=O_{C,K}(log Q)`.  Equivalently, any
fixed-surplus width-one family with `q/log Q -> infinity` must create
super-polynomial one-root fixed-divisor slices after the standard charges.  So
large-width counterexamples to the width-one closure criterion are exactly
large one-root slice counterexamples; the width-one cube has no additional
reservoir of growth once those slices are polynomially controlled.

## Explicit One-Root Width-One Ledger

The one-root ledger needed by the closure criterion can be written without a
new primitive.  For an active node `S`, write

```text
D_S=D_S^{can},        V_S=span(P_S,Q_S),
q_S+s_S=|D_S|,        a_S=floor((q_S-2)/2).
```

Let `W1Large(A_0)` be the set of pairs `(S,O)` such that

```text
S is active,        q_S>s_S+2,
O subset D_S,       |O|=s_S+1,
ell_{D_S\O} in V_S.
```

For `(S,O) in W1Large(A_0)`, put `Z_{S,O}=D_S\O`.  The unique-range argument
implies that for each fixed large node `S` there is at most one such
complement `O`.  Order `Z_{S,O}` by the ambient root order and define

```text
M_{S,O,x}^{r1}
 =
 sum_{f=0}^{a_S-1} binom(|{y in Z_{S,O}: y>x}|, f),
        x in Z_{S,O}.
```

The explicit width-one one-root ledger is

```text
FR_1^{r1}(A_0)
 =
 sum_{(S,O) in W1Large(A_0)}
 sum_{x in Z_{S,O}} M_{S,O,x}^{r1}.             (W1-explicit-ledger)
```

By (W1-first-root), this is exactly the large-node width-one flag contribution:

```text
WO_1^{large}(A_0)=FR_1^{r1}(A_0).               (W1-ledger-identity)
```

Thus `FR_1^{r1}` is not an additional assumption; it is the width-one subledger
of the one-root fixed-divisor/root-slice ledger, written directly in terms of
bounded complements passing the rank test.  Future fixed-root work can attack
this explicit sum by proving that the corresponding first-root slices are
quotient-periodic, tangent, fixed-root/root-slice degenerate, or aperiodically
packable.

## Rank-Test Logarithmic Exclusion Criterion

The previous display also removes the artificial dependence on the chosen root
order.  For any selected surviving subledger
`U(A_0) subset W1Large(A_0)`, define

```text
b(q)=sum_{e=1}^{floor((q-2)/2)} binom(q-1,e).
```

Then the first-root partition gives the order-free identity

```text
sum_{x in Z_{S,O}} M_{S,O,x}^{r1}=b(q_S),
```

and hence

```text
FR_1^{r1}(U)=sum_{(S,O) in U(A_0)} b(q_S).       (W1-weighted-rank)
```

In particular, the width-one one-root ledger is a weighted count of surviving
bounded-complement rank-test witnesses.  The weights satisfy, for `q>=4`,

```text
2^{q-1}/(2q) <= b(q) <= 2^{q-1}.                (W1-weight-bounds)
```

The upper bound is trivial.  For the lower bound, the central level
`a=floor((q-2)/2)` contributes at least
`binom(q-1,a)>=2^{q-1}/(2q)`.

Let

```text
q_*(U)=max { q_S : (S,O) in U(A_0), q_S>=4 },
```

with `q_*(U)=0` if the set is empty.  Since `#U(A_0)` is at most the active
tree size,

```text
FR_1^{r1}(U) <= C_sigma Q^{sigma+1} 2^{q_*(U)-1}.  (W1-log-sufficient)
```

Thus a logarithmic rank-test exclusion

```text
q_*(U) <= K log_2 Q + O_sigma(1)
```

implies a polynomial fixed-surplus bound for the selected width-one subledger.
Conversely, if a polynomial bound

```text
FR_1^{r1}(U) <= C Q^B
```

holds for a fixed-surplus family, then every surviving witness with `q_S>=4`
satisfies

```text
q_S <= B log_2 Q + log_2(2Cq_S)+1.              (W1-log-necessary)
```

So polynomiality of the explicit one-root width-one ledger is equivalent,
up to the already polynomial active-tree factor, to excluding surviving
rank-test complements with `q_S/log Q -> infinity`.  A counterexample-first
search therefore only has to find a sequence of bounded complements `O` with
`ell_{D_S\O} in V_S` and superlogarithmic `q_S` after the standard
quotient-periodic, tangent, fixed-root/root-slice, and aperiodic charges.

## Bounded-Complement Tail Readout

The rank test has one further fixed-surplus compression.  Work at a large node,
so `q>s+2`, and define the tail map

```text
Tail_s(X^{q-1}+c_1X^{q-2}+...+c_{s+1}X^{q-s-2}+...)
   =(c_1,...,c_{s+1}).
```

For `O subset D`, `|O|=s+1`, write `Z=D\O` and

```text
L_O=ell_Z=X^{q-1}+c_1X^{q-2}+... .
```

Then `Tail_s(L_O)` determines `O`.  Indeed, put
`u_i=e_i(Z)=(-1)^i c_i` for `1<=i<=s+1`.  Since `D=Z disjoint union O`,
the elementary symmetric functions satisfy

```text
e_i(D)=sum_{j=0}^i e_j(Z)e_{i-j}(O),       1<=i<=s+1.
```

Starting from `e_0(O)=1`, this triangular system gives the recursion

```text
e_i(O)=e_i(D)-sum_{j=1}^i u_j e_{i-j}(O),  1<=i<=s+1.   (W1-tail-rec)
```

Thus the tail of `L_O` recovers all coefficients of

```text
ell_O=X^{s+1}-e_1(O)X^s+...+(-1)^{s+1}e_{s+1}(O),
```

and hence recovers the split complement `O` itself.

Consequently the map

```text
O |-> Tail_s(L_O)
```

is injective on bounded complements.  If the leading-coefficient functional is
nonzero on `V`, choose a monic element `M in V` and a generator
`N in ker(lc_{q-1}|_V)`.  Every monic rank-test candidate in `V` has the form

```text
M+lambda N,
```

so every width-one complement must satisfy the necessary tail-line incidence

```text
Tail_s(L_O) in Tail_s(M)+F Tail_s(N).            (W1-tail-line)
```

If `Tail_s(N)=0`, there is at most one possible complement by injectivity.
Otherwise the possible complements inject into the intersection of the
bounded-complement tail cloud with a single affine line in `F^{s+1}`.  Thus a
superlogarithmic surviving rank-test counterexample cannot be hidden in the
`q` moving coefficients of `L_O`: it already appears in this fixed-dimensional
tail incidence before the remaining full-rank-test equations are imposed.

## One-Parameter Rank-Test Factorization

The tail readout gives an exact scalar factorization test.  Keep the notation
above and write

```text
Tail_s(M)=(alpha_1,...,alpha_{s+1}),
Tail_s(N)=(beta_1,...,beta_{s+1}).
```

For `lambda in F`, define

```text
u_i(lambda)=(-1)^i(alpha_i+lambda beta_i),       1<=i<=s+1,
o_0(lambda)=1,
o_i(lambda)=e_i(D)-sum_{j=1}^i u_j(lambda)o_{i-j}(lambda).
```

Put

```text
E_lambda(X)
 = X^{s+1}-o_1(lambda)X^s+...+(-1)^{s+1}o_{s+1}(lambda).
```

Then `lambda` gives a width-one rank-test complement if and only if

```text
ell_D(X)=E_lambda(X)(M(X)+lambda N(X)).          (W1-factor)
```

When this holds, `E_lambda=ell_O` for the unique complement `O`, and
`M+lambda N=ell_{D\O}`.  Conversely, if `O` is any width-one complement with
`ell_{D\O}=M+lambda N`, then `E_lambda=ell_O` by the triangular tail
recursion, so (W1-factor) follows from `ell_D=ell_O ell_{D\O}`.

Thus the full bounded-complement rank test is equivalent to a one-parameter
factorization identity.  The fixed-degree factor `E_lambda` is obtained from
the top `s+1` coefficients alone, and the remaining full-coefficient equations
are precisely the assertion that the recovered complement factor multiplies
the monic pencil element back to `ell_D`.

## Bounded-Degree Residual Equations

The factorization identity is a fixed-degree univariate common-root problem.
Let

```text
R_lambda(X)=ell_D(X)-E_lambda(X)(M(X)+lambda N(X)).
```

By construction, the leading coefficient and the next `s+1` coefficients of
`R_lambda` vanish identically in `lambda`, so

```text
deg_X R_lambda <= q-2.
```

Moreover each coefficient of `R_lambda` is a polynomial in `lambda` of degree
at most `s+2`.  This follows by induction from the recursion above:
`u_i(lambda)` is affine-linear, `o_i(lambda)` has degree at most `i`, and
multiplication by the affine-linear factor `M+lambda N` raises degree by at
most one.

Thus, for a fixed large node, width-one rank-test witnesses are exactly the
common roots of at most `q-1` univariate residual equations, each of degree at
most `s+2`.  If `N!=0`, not all of these residual equations can vanish
identically: otherwise (W1-factor) would hold as a polynomial identity in
`lambda`, giving infinitely many distinct monic degree-`q-1` divisors
`M+lambda N` of the fixed squarefree polynomial `ell_D` over an algebraic
closure.  Hence at least one residual equation is nonzero, and the scalar
candidate set at the node is contained in the root set of a degree-`<=s+2`
polynomial.

The M1 obstruction is therefore not an uncontrolled moving-complement search.
After the monic slice is chosen, a superlogarithmic width-one survivor must be
a scalar common root of a long residual vector of bounded-degree equations.
Ruling out such roots after the standard quotient-periodic, tangent,
fixed-root/root-slice, and aperiodic charges is the sharpened algebraic form of
the logarithmic rank-test exclusion.

## First Residual Gate

The first coefficient not forced by the tail recursion is explicit.  Write

```text
M(lambda)=M+lambda N
 = X^{q-1}+c_1(lambda)X^{q-2}+...+c_{s+2}(lambda)X^{q-s-3}+...
```

and put

```text
u_i(lambda)=(-1)^i c_i(lambda),        1<=i<=s+2.
```

The tail recursion defines `o_i(lambda)=e_i(O_lambda)` for `1<=i<=s+1`.  The
next elementary-symmetric identity for `D=Z_lambda disjoint union O_lambda` is

```text
e_{s+2}(D)
 =
 u_{s+2}(lambda)
 + sum_{j=1}^{s+1} u_j(lambda)o_{s+2-j}(lambda).     (W1-gate0)
```

Equivalently, define the first residual gate

```text
G_{s+2}(lambda)
 =
 e_{s+2}(D)-u_{s+2}(lambda)
 -sum_{j=1}^{s+1} u_j(lambda)o_{s+2-j}(lambda).       (W1-first-gate)
```

Then `G_{s+2}(lambda)=0` is exactly the coefficient of `X^{q-2}` in

```text
R_lambda(X)=ell_D(X)-E_lambda(X)(M+lambda N),
```

up to the harmless sign `(-1)^{s+2}`.  Since `u_j(lambda)` is affine-linear
and `o_i(lambda)` has degree at most `i`, the gate has degree at most `s+2`.

Thus the first obstruction after tail readout is a single concrete
degree-`<=s+2` polynomial.  If it is not identically zero, then at this node
there are at most `s+2` scalar candidates even before the later residual
coefficients are imposed.  If it vanishes identically, the width-one witness
has passed a specific fixed-degree algebraic degeneracy, and the proof search
continues with the next residual coefficient.  In either case, the first gate
is the canonical place to start a falsification-first search for large
rank-test complements.

## Residual Gate Chain and Node GCD

The later residual coefficients have the same elementary-symmetric form.  Put

```text
u_0(lambda)=1,
u_i(lambda)=(-1)^i [X^{q-1-i}](M+lambda N),      1<=i<=q-1,
u_i(lambda)=0,                                   i>q-1,
o_0(lambda)=1.
```

For `0<=r<=q+s`, define

```text
G_r(lambda)
 =
 e_r(D)-sum_{j=0}^{s+1} o_j(lambda) u_{r-j}(lambda),
```

where `u_i=0` for `i<0` and `e_r(D)=0` for `r>|D|`.  The tail recursion is
exactly the assertion that

```text
G_r(lambda) == 0        for 0<=r<=s+1.           (W1-tail-gates)
```

The remaining factorization test is

```text
G_r(lambda)=0        for s+2<=r<=q+s.            (W1-gate-chain)
```

Indeed, the coefficient of `X^{q+s-r}` in

```text
ell_D(X)-E_lambda(X)(M+lambda N)
```

is `(-1)^r G_r(lambda)`.  Hence the residual vector from the previous section
is exactly the gate chain `(G_{s+2},...,G_{q+s})`, written in symmetric
coordinates.  Every `G_r` has degree at most `s+2`: the factor
`o_j(lambda)` has degree at most `j`, while `u_{r-j}(lambda)` is constant,
affine-linear, or zero.

If `N!=0`, the gate chain is not identically zero.  Otherwise all gates would
vanish as polynomial identities in `lambda`, giving the factorization

```text
ell_D=E_lambda(M+lambda N)
```

for every `lambda` over an algebraic closure, and hence infinitely many
distinct monic degree-`q-1` divisors of the fixed squarefree polynomial
`ell_D`.

Consequently the scalar candidate set at a large node is the zero set of the
single nonzero node polynomial

```text
P_node(lambda)=gcd(G_{s+2},G_{s+3},...,G_{q+s}),     (W1-node-gcd)
```

with zero gates omitted from the gcd.  This polynomial has degree at most
`s+2`, and its roots are exactly the scalar parameters passing the full
bounded-complement rank test.  The rank-test exclusion can therefore be stated
as a concrete node-gcd problem: after the standard charges, no node with
`q/log Q -> infinity` should have a split complement arising from a root of
this fixed-degree polynomial.

## Split-Root Filter for Node-GCD Roots

The split condition gives an additional base-free filter on the node-gcd roots.
Let

```text
Lambda_split={ lambda : ell_D=E_lambda(M+lambda N) }.
```

For `lambda in Lambda_split`, the factor `M+lambda N` is a monic divisor of
the squarefree split polynomial `ell_D`.  Hence

```text
M+lambda N=ell_{Z_lambda}
```

for a unique subset `Z_lambda subset D` of size `q-1`.

If `lambda != mu` in `Lambda_split`, then the root sets `Z_lambda` and
`Z_mu` are disjoint.  Indeed, if `x in Z_lambda cap Z_mu`, then

```text
M(x)+lambda N(x)=M(x)+mu N(x)=0,
```

so `N(x)=0` and then `M(x)=0`.  Since `M` and `N` span the two-dimensional
pencil `V`, every direction in `V` vanishes at `x`, contradicting the
base-free hypothesis.

Thus the true split roots of the node gcd satisfy the sharper packing bound

```text
#Lambda_split <= floor((q+s)/(q-1)).              (W1-split-root-pack)
```

This bound is independent of the degree `s+2` of the node gcd.  The gcd is
still useful as the algebraic scalar equation, but the split-root filter says
that its roots cannot all be genuine width-one split complements unless their
large root shadows are disjoint in `D`.

## Width-One Slope-Count Closure

There is a sharper conclusion for the slope-image count itself.  The
exponential width-one cube is a recursive flag-ledger issue, not a source of
many projective slopes.

At a base-free node, let

```text
W1Slope_S={ [A] in P(V_S) : |Z(A)|=q_S-1 }.
```

If `[A]` and `[B]` are two distinct elements of `W1Slope_S`, then their root
sets in `D_S` are disjoint.  Indeed, a common root `x` would give
`A(x)=B(x)=0`; since `A,B` span the two-dimensional pencil, every element of
`V_S` would vanish at `x`, contradicting base-freeness.  Hence

```text
2(q_S-1)<=|D_S|=q_S+s_S
```

whenever two distinct width-one projective directions exist.  Thus, on the
large range `q_S>s_S+2`, there is at most one width-one projective slope at
the node.

On the complementary range `q_S<=s_S+2`, fixed surplus gives
`q_S+s_S<=2sigma+2`.  A width-one projective direction is determined by its
`q_S-1` roots in `D_S`, so

```text
#W1Slope_S <= binom(2sigma+2,sigma+1)
```

for every small node.  Since the active canonical tree has size at most
`(s_0+2)Q^{s_0+1}`, the total number of width-one projective slopes in fixed
surplus is

```text
O_sigma(Q^{sigma+1}).                              (W1-slope-count)
```

This is the direct M1 slope-packing consequence: width-one shadows cannot by
themselves create super-polynomially many bad slopes.  The later
`FR_1^{r1}` discussion is still needed for recursive flag accounting, because
a single surviving width-one slope carries the large descendant cube
`b(q_S)`.

## Fixed-Surplus Closure Criterion

Now sum over active canonical nodes with initial surplus `s_0<=sigma`.  Let
`WO_1(A_0)` denote the total root-free width-one flag contribution that remains
after quotient-periodic, tangent, fixed-root, and aperiodic charges have
removed the already-accounted cases.

Small quotient-width nodes are polynomial by size alone.  If

```text
q_S<=s_S+2,
```

then `q_S<=sigma+2`, so the local width-one cube is `O_sigma(1)`.  The active
canonical tree has size

```text
#Active(A_0) <= (s_0+2) Q^{s_0+1},
```

where `Q` is the initial quotient width.  Hence all small-`q_S` nodes
contribute `O_sigma(Q^{sigma+1})`.

For large nodes, `q_S>s_S+2`, there is at most one width-one maximal shadow at
the node: two distinct projective fibers of size `q_S-1` would be disjoint and
would force

```text
2(q_S-1)<=q_S+s_S,
```

contradicting `q_S>s_S+2`.

On this large-node range, the first-root injection charges the whole
width-one cube to the one-root fixed-divisor ledger.  Consequently

```text
WO_1(A_0)
 <= FR_1^{r1}(A_0)+O_sigma(Q^{sigma+1}).        (W1-global)
```

Thus, in fixed surplus, the width-one critical-tail branch is closed once the
explicit one-root ledger `FR_1^{r1}` is polynomial.  The remaining target is
not another width-one packing problem; it is to prove or import the
fixed-surplus bound for this one-root fixed-divisor/root-slice subledger after
the standard quotient-periodic, tangent, fixed-root, and aperiodic charges.
