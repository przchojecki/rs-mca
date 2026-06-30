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

## M1 use

For Work package C3 in `towards-prize.md`, this is a sharper interface than a
uniform disjoint-pair cap.  The next global proof obligation can be stated as:

```text
after quotient, tangent, fixed-root, and endpoint-star charges are removed,
the disjoint high-overlap graph G_Lambda has a polynomial/linear edge budget
outside quotient-periodic, subfield-confined, or finite-template branches.
```

For example, a Kummer/cross-ratio theorem proving maximum high-overlap degree
`d` would give `M <= Kd/2`; a degeneracy bound `d` would give `M <= dK`.  Either
bound can be inserted into `(HG1)` to rule out the far-from-star small-support
residual once the resulting floor exceeds the target support budget.

## Verification

The companion verifier checks the exact floor, the forced high-edge lower
bound, and sampled finite packet systems:

```sh
python3 experimental/scripts/verify_m1_high_overlap_graph_budget.py
```
