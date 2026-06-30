# M1 high-overlap graph budget

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note strengthens the packet-overlap endpoint sift by replacing a uniform
disjoint-pair overlap cap with an edge budget for the high-overlap graph.  It
is still a finite local combinatorial theorem.  It does not prove the M1
aperiodic local-limit theorem, and it does not prove the missing
Hankel/Kummer estimate.

## Setup

Let `A` be a finite set of selected packet labels.  Each label `a in A` has:

```text
endpoint support E_a subset Omega,        |E_a|=2,
packet P_a subset Xi,                     |P_a|=s.
```

Assume endpoint-star pruning has already been performed:

```text
each endpoint x lies in at most D endpoint supports E_a,
each endpoint support E carries at most h labels.
```

Put:

```text
K = |A|,
B = | union_{a in A} P_a |.
```

As in `m1_packet_overlap_endpoint_sift.md`, pairs over the same endpoint
support are residual packet classes on the same support and are treated as
disjoint in this local branch.

Fix an integer `Lambda` with `0 <= Lambda < s`.  Define the disjoint
high-overlap graph `G_Lambda` on the label set `A` by putting an edge
`{a,b}` when:

```text
E_a cap E_b = emptyset,
|P_a cap P_b| > Lambda.
```

Let:

```text
e_Lambda = |E(G_Lambda)|.
```

## Edge-budget support floor

Suppose that:

```text
e_Lambda <= M.
```

Then

```text
B >= ceil(
  K^2 s^2
  /
  (K s + 2 K h(D-1)s + K(K-1)Lambda + 2(s-Lambda)M)
).                                                     (HG1)
```

Thus a small residual support can survive either by producing many
disjoint-support high-overlap edges, or by falling into one of the endpoint
star/near-star branches handled elsewhere.

## Proof

Let

```text
I(x) = #{a in A : x in P_a}.
```

Then

```text
sum_x I(x) = K s,
sum_x I(x)^2 = K s + 2 sum_{a<b} |P_a cap P_b|.
```

The endpoint-sharing overlap mass is at most

```text
K h(D-1)s.
```

For disjoint endpoint supports, every non-edge of `G_Lambda` contributes at
most `Lambda`, and every edge contributes at most `s`.  Since there are at most
`binom(K,2)` disjoint pairs and at most `M` high-overlap edges, the total pair
overlap satisfies

```text
sum_{a<b} |P_a cap P_b|
 <= K h(D-1)s + Lambda binom(K,2) + (s-Lambda)M.
```

Therefore

```text
sum_x I(x)^2
 <= K s + 2K h(D-1)s + K(K-1)Lambda + 2(s-Lambda)M.
```

Cauchy's inequality gives

```text
(K s)^2 <= B sum_x I(x)^2,
```

which is exactly `(HG1)`.

## Forced high-edge count

Equivalently, if `B <= R`, then Cauchy's lower bound on the total pair-overlap
mass forces

```text
e_Lambda >= ceil_+(
  (
    K s(Ks-R)/(2R)
    - K h(D-1)s
    - Lambda binom(K,2)
  )
  /
  (s-Lambda)
).                                                     (HG2)
```

Here `ceil_+(x)=max(0,ceil(x))`.  This is often the more useful form: a
small-support residual must produce a dense enough high-overlap graph.

## Post-sift alternative

Fix integers:

```text
L >= 2,       R >= 1,       M >= 0.
```

If the floor in `(HG1)` is larger than `R`, then every selected packet family
satisfies at least one of:

```text
large support:       B > R,
near-star:           #{endpoint supports E_a} < L D,
many high edges:     e_Lambda > M.
```

The near-star branch is not used in the proof of `(HG1)`.  It is included
because this theorem is meant to be consumed after the endpoint-star sift: the
far-from-star small-support branch is now reduced to proving an algebraic
upper bound on `e_Lambda`.

## Degree and degeneracy corollaries

The edge budget can be filled by any graph-theoretic theorem for
`G_Lambda`.

### Maximum-degree input

Suppose a separate algebraic argument proves

```text
Delta(G_Lambda) <= d.
```

Then

```text
e_Lambda <= floor(K d / 2),
```

and `(HG1)` gives the degree-budget floor

```text
F_deg(K,s,h,D,Lambda,d)
 =
 ceil(
   K^2 s^2
   /
   (
     K s + 2 K h(D-1)s + K(K-1)Lambda
     + 2(s-Lambda) floor(Kd/2)
   )
 ).                                                   (DG1)
```

If `F_deg(K,s,h,D,Lambda,d)>R`, then every selected packet family satisfies at
least one of:

```text
large support:       B > R,
near-star:           #{endpoint supports E_a} < L D,
degree break:        Delta(G_Lambda) > d.
```

So an algebraic maximum-degree theorem makes the far-from-star small-support
branch impossible.

### Degeneracy input

A weaker but often more stable input is graph degeneracy.  If every subgraph of
`G_Lambda` has a vertex of degree at most `d`, then

```text
e_Lambda <=
  binom(K,2),                         if d >= K-1,
  dK - binom(d+1,2),                  if 0 <= d < K-1.
```

Write this edge ceiling as `M_degen(K,d)`.  Substituting
`M=M_degen(K,d)` in `(HG1)` gives `F_degen`.  If

```text
F_degen(K,s,h,D,Lambda,d) > R,
```

then every selected packet family satisfies one of:

```text
large support,
near-star,
or degeneracy(G_Lambda) > d.
```

This is useful because many incidence/Kummer estimates naturally rule out
dense induced high-overlap subgraphs rather than bounding the degree of every
single packet.

Proof of the corollaries: the maximum-degree edge ceiling is the handshaking
bound `2e_Lambda <= Kd`.  For degeneracy, remove vertices in an order where
each removed vertex has at most `d` later neighbors.  If `d >= K-1`, the
complete graph ceiling `binom(K,2)` is sharp.  If `0 <= d < K-1`, the first
`K-d-1` removed vertices contribute at most `d` later edges each, and the last
`d+1` vertices contribute at most `binom(d+1,2)` edges, giving
`d(K-d-1)+binom(d+1,2)=dK-binom(d+1,2)`.  Substitution in `(HG1)` gives the
displayed support floors and alternatives.

## Dense-core extraction

The degeneracy alternative can be localized further.  Define the forced
high-edge lower bound

```text
E_forced(K,s,h,D,Lambda,R)
 =
 ceil_+(
   (
     K s(Ks-R)/(2R)
     - K h(D-1)s
     - Lambda binom(K,2)
   )
   /
   (s-Lambda)
 ).
```

If

```text
E_forced(K,s,h,D,Lambda,R) > M_degen(K,d),
```

then every selected packet family satisfies at least one of:

```text
large support:       B > R,
near-star:           #{endpoint supports E_a} < L D,
dense core:          G_Lambda contains a nonempty induced subgraph
                     with minimum degree at least d+1.
```

In the dense-core branch, every packet in the induced core has at least `d+1`
disjoint-support packet neighbors meeting it in more than `Lambda` points.
This is the form intended for the next algebraic attack: rule out one packet
having many independent high-overlap Kummer/cross-ratio partners, or classify
the structured exception as quotient-periodic, tangent, subfield-confined, or
finite-template.

Proof: if `B<=R`, then `(HG2)` gives
`e_Lambda >= E_forced`.  If the near-star alternative is absent and
`E_forced > M_degen(K,d)`, then the degeneracy edge ceiling is impossible for
`G_Lambda`; hence `degeneracy(G_Lambda)>d`.  By the standard peeling
characterization of degeneracy, some induced subgraph has minimum degree at
least `d+1`.

## Endpoint-disjoint star extraction

The dense-core branch can be localized one step further using the endpoint
degree cap.  Suppose `G_Lambda` contains an induced core with minimum degree at
least `delta`.  Then some center packet `a` in that core has a set `N(a)` of at
least `delta` high-overlap neighbors.  Every neighbor support is disjoint from
`E_a`, by definition of `G_Lambda`.

Because each endpoint lies in at most `D` endpoint supports and each endpoint
support carries at most `h` labels, any chosen neighbor can conflict by
endpoint intersection with at most

```text
h(2D-1)
```

neighbor labels, including labels over its own endpoint support.  A greedy
packing therefore extracts at least

```text
S_star(delta,D,h) =
  ceil( delta / (h(2D-1)) )
```

neighbors whose endpoint supports are pairwise disjoint.  Hence the dense-core
branch contains a rooted high-overlap star

```text
a; b_1,...,b_m,        m >= S_star(delta,D,h),
```

with:

```text
E_a cap E_{b_i} = emptyset,
E_{b_i} cap E_{b_j} = emptyset        (i != j),
|P_a cap P_{b_i}| > Lambda.
```

Combining this with dense-core extraction, if

```text
E_forced(K,s,h,D,Lambda,R) > M_degen(K,d),
```

then every selected packet family satisfies at least one of:

```text
large support,
near-star,
or an endpoint-disjoint high-overlap star with
  m >= S_star(d+1,D,h).
```

This is the most local target in this packet-sift chain: rule out one packet
having many endpoint-independent high-overlap partners, or classify the
exception.

## Popular residue extraction

The endpoint-disjoint star can be compressed once more to a single point of the
center packet.  Let

```text
a; b_1,...,b_m
```

be a rooted high-overlap star as above.  For `x in P_a`, define its leaf
popularity by

```text
pop_a(x) = #{ i : x in P_{b_i} }.
```

Since each leaf satisfies `|P_a cap P_{b_i}| > Lambda`, the total incidence
between the center packet and the leaves is at least

```text
sum_{x in P_a} pop_a(x) >= m(Lambda+1).
```

As `|P_a|=s`, some center-packet point satisfies

```text
pop_a(x) >= ceil( m(Lambda+1) / s ).                (PR1)
```

Equivalently, if an algebraic input proves the local popularity cap

```text
pop_a(x) <= U
```

for every endpoint-disjoint high-overlap star after the quotient/tangent/root
charges, then every such star has

```text
m <= floor( s U / (Lambda+1) ).                     (PR2)
```

Combining this with the previous section, if

```text
E_forced(K,s,h,D,Lambda,R) > M_degen(K,d)
```

and

```text
S_star(d+1,D,h) > floor( s U / (Lambda+1) ),
```

then every selected packet family satisfies at least one of:

```text
large support,
near-star,
or a popular residue point x in a center packet P_a with
  pop_a(x) > U
```

inside an endpoint-disjoint high-overlap star.

This is the point where the finite packet combinatorics hands off to the
Hankel/Kummer geometry: prove a uniform popularity cap for one center packet
point against endpoint-independent high-overlap partners, or classify the
exception.

## M1 use

For Work package C3 in `towards-prize.md`, this is a sharper interface than a
uniform disjoint-pair cap.  The next global proof obligation can be stated as:

```text
after quotient, tangent, fixed-root, and endpoint-star charges are removed,
the disjoint high-overlap graph G_Lambda has a polynomial/linear edge budget
outside quotient-periodic, subfield-confined, or finite-template branches.
```

For example, a Kummer/cross-ratio theorem proving maximum high-overlap degree
`d` or high-overlap degeneracy `d` can now be inserted into `(DG1)` or
`F_degen` to rule out the far-from-star small-support residual once the
resulting floor exceeds the target support budget.  Equivalently, if the
support remains too small, the dense-core extraction above identifies a
specific high-minimum-degree high-overlap packet core, and then an
endpoint-disjoint high-overlap star.  The popular-residue extraction reduces
that star to one center packet point with many independent high-overlap
partners.

## Verification

The companion verifier checks the exact floor, the forced high-edge lower
bound, the degree/degeneracy substitutions, the dense-core extraction, and
the endpoint-disjoint star/popular-residue extraction on sampled finite packet
systems:

```sh
python3 experimental/scripts/verify_m1_high_overlap_graph_budget.py
```
