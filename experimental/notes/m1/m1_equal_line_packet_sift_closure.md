# M1 equal-line packet-sift closure criterion

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note composes the packet-sift combinatorics with the equal-line
popularity gate.  It is meant to make the C3/M1 proof obligation sharper:
once endpoint-independent high-overlap leaves have entered the ordinary
projective equal-line split-fiber chart, the local branch has an explicit
support floor.  What remains is the global model-entry theorem, not another
local root-count constant.

The note is local.  It does not assert a full M1 theorem, a finite-row
threshold, a line-decoding theorem, or protocol soundness.  It also does not
choose the global parameters `K,s,h,D,Lambda,R`; those come from the
residue-line packet family being studied.

## Inputs

Use the setup of `m1_high_overlap_graph_budget.md`.

There are `K` selected packet labels.  Each label has a two-point endpoint
support and a packet of size `s`.  After endpoint-star pruning:

```text
at most h labels lie over one endpoint support,
at most D endpoint supports contain one endpoint.
```

For an integer `0 <= Lambda < s`, the disjoint high-overlap graph puts an edge
between endpoint-disjoint labels whose packets meet in more than `Lambda`
points.  Let `B` be the size of the union of all selected packets.

As in the post-sift alternative, fix `L >= 2` for the near-star branch: fewer
than `L D` residual endpoint supports are treated as a bounded endpoint
template family.

Assume the charged branches have already been removed:

```text
quotient-periodic branches
tangent branches
fixed-root/root-slice branches
endpoint-star branches
singular equal-line fibers
denominator/chart exceptions
```

The remaining conditional input is equal-line model entry:

```text
Every endpoint-disjoint high-overlap star entering the residual branch
reduces to the ordinary projective equal-line split-fiber model.
```

Finally assume that the projective leaf parameter `y` has fiber multiplicity at
most `mu` on the leaves in such a star.

## Equal-line local cap

The equal-line split-fiber package proves:

1. the exceptional projective `y` support has size at most `6`;
2. for every fixed center residue `x`, the equal-line resultant is a nonzero
   quadratic projective gate in `y`;
3. ordinary nonsplit `y` fibers have no base-field phantom gate zeros.

Therefore the popularity divisor gate gives the local cap

```text
U_eq(mu) = mu (6 + 2) = 8 mu.                    (EQ1)
```

If the selected leaves inject into the projective `z` leaf parameter, then the
map

```text
z |-> y = (1 + 3 z^2)/(1 - z)^2
```

has projective degree two, so `mu <= 2` and

```text
U_eq,z = 16.                                    (EQ2)
```

The sharpness audit in `m1_equal_line_generic_popularity_budget.md` shows that
the constant `8mu` cannot be lowered by local root-count bookkeeping alone.

## Closure floor

Insert `U = 8mu` into the popularity-cap support criterion `(PC1)` of
`m1_high_overlap_graph_budget.md`.

Define

```text
T_U = floor(s U / (Lambda + 1)),
d_U = h (2D - 1) T_U.
```

Let

```text
M_degen(K,d) =
  binom(K,2),                 if d >= K-1,
  dK - binom(d+1,2),          if 0 <= d < K-1.
```

Then the equal-line packet-sift floor is

```text
F_eq(K,s,h,D,Lambda,mu)
 =
 ceil(
   K^2 s^2
   /
   (
     K s
     + 2 K h(D-1)s
     + K(K-1)Lambda
     + 2(s-Lambda) M_degen(K,d_U)
   )
 ).
```

Under the equal-line model-entry and multiplicity hypotheses,

```text
B >= F_eq(K,s,h,D,Lambda,mu).                   (EQ3)
```

In the injective-`z` branch, replace `U=8mu` by `U=16`; equivalently use
`F_eq,z = F_pop(K,s,h,D,Lambda,16)`.

## Support-budget alternative

Fix a target support budget `R`.  If

```text
F_eq(K,s,h,D,Lambda,mu) > R,
```

then every selected residual packet family satisfies at least one of:

```text
large support:
  B > R;

near-star:
  the residual endpoint-support family has fewer than L D supports, hence is
  one of the bounded endpoint templates from m1_near_star_template_localization;

model-entry failure:
  some endpoint-independent high-overlap star does not reduce to the ordinary
  projective equal-line split-fiber model after the charged branches are
  removed;

multiplicity failure:
  the projective y-parameter has leaf multiplicity larger than mu;

charged exception:
  a quotient, tangent, fixed-root, endpoint-star, denominator, projective
  boundary, or singular equal-line fiber was not actually removed.
```

Thus the local equal-line branch is closed as soon as the model-entry and
multiplicity hypotheses are proved and the displayed floor beats the intended
support budget.

## Proof

By `m1_equal_line_split_fiber_containment.md`, every ordinary projective
split-fiber leaf containing a fixed center residue is contained in the
quadratic resultant gate in the `y` parameter, after the six singular fibers
are charged.  The nonsplit ledger proves that ordinary nonsplit base-field
fibers add no phantom zeros.  The projective divisor-gate lemma in
`m1_popularity_divisor_gate.md` therefore gives `pop_x <= 8mu` for every
center residue `x`.

The popularity-cap support criterion in `m1_high_overlap_graph_budget.md`
turns any uniform cap `pop_x <= U` into the support floor `(PC1)`.  Substituting
`U=8mu` gives `(EQ3)`.  The injective-`z` version uses the degree-two
projective map `z -> y`, giving `mu<=2` and hence `U=16`.

The support-budget alternative is the contrapositive of the same chain,
together with the endpoint-star and near-star alternatives already isolated in
`m1_packet_overlap_endpoint_sift.md`,
`m1_high_overlap_graph_budget.md`, and
`m1_near_star_template_localization.md`.

## C3 impact

For Work package C3 in `towards-prize.md`, this criterion identifies the next
nonlocal theorem to prove:

```text
after quotient/tangent/fixed-root/endpoint-star charges,
endpoint-independent high-overlap stars enter the ordinary projective
equal-line split-fiber chart with bounded y-multiplicity.
```

If that theorem is true with constants making `F_eq > R`, the equal-line
far-from-star residual branch is no longer a source of super-polynomial
aperiodic bad slopes.  If it is false, the failure mode is now concrete:
produce the model-entry or multiplicity counterexample and charge it as a new
floor.

## Verification

The companion verifier checks the cap `U_eq=8mu`, the injective-`z` cap
`U=16`, the exact substitution into the high-overlap support floor, the
rounding equivalence with the forced-edge formulation, and monotonicity of the
floor under weaker popularity caps:

```sh
python3 experimental/scripts/verify_m1_equal_line_packet_sift_closure.py
```
