# M1 post-sift residual alternative

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note combines the packet-overlap endpoint sift with the near-star template
localization into one local residual alternative.  It is a theorem about finite
packet systems with two-endpoint supports.  It does not prove the missing
Kummer/cross-ratio estimate and does not prove the M1 aperiodic local-limit
theorem.

## Setup

Let `A` be a finite set of selected packet labels.  Each label `a in A` has:

```text
endpoint support E_a subset Omega,        |E_a|=2,
packet P_a subset Xi,                     |P_a|=s.
```

Assume the endpoint-star pruning has already been performed, so:

```text
each endpoint x lies in at most D endpoint supports E_a,
each endpoint support E carries at most h labels.
```

Put:

```text
K = |A|,
m = #{ endpoint supports E_a },
B = | union_{a in A} P_a |.
```

For labels `a,b` with disjoint endpoint supports, suppose a proposed
disjoint-support overlap cap is

```text
|P_a cap P_b| <= Lambda.
```

## Theorem

Fix integers

```text
L >= 2,        R >= 1,        K >= 2.
```

Define the star-sifted support floor

```text
F_disj(K,s,h,D,Lambda)
 =
 ceil( K s^2 / (s + 2h(D-1)s + (K-1)Lambda) ).   (ALT1)
```

If

```text
F_disj(K,s,h,D,Lambda) > R,                       (ALT2)
```

then every selected packet family as above satisfies at least one of:

```text
large support:       B > R,
near-star:           m < L D,
disjoint overlap:    some disjoint-support pair has |P_a cap P_b| > Lambda.
```

Equivalently, after endpoint-star pruning, a small-support far-from-star
residual must break the disjoint-overlap cap.

## Proof

Assume the contrary:

```text
B <= R,
m >= L D,
all disjoint-support packet pairs have overlap <= Lambda.
```

The near-star conclusion fails by `m >= LD`.  The endpoint-degree and
labels-per-support hypotheses give the endpoint-sharing overlap budget from
`m1_packet_overlap_endpoint_sift.md`:

```text
endpoint-sharing overlap mass <= K h(D-1)s.
```

With the disjoint cap `Lambda`, the full incidence second moment satisfies

```text
sum_x I(x)^2
 <= K s + 2K h(D-1)s + K(K-1)Lambda.
```

Cauchy's inequality gives

```text
(K s)^2 <= B (K s + 2K h(D-1)s + K(K-1)Lambda).
```

Dividing by `K` and taking ceilings yields

```text
B >= F_disj(K,s,h,D,Lambda).
```

This contradicts `B <= R` and `(ALT2)`.  Hence one of the three displayed
alternatives must hold.

## Near-star ledger

When the near-star alternative holds, `m < LD`; by
`m1_near_star_template_localization.md`, the endpoint footprint has size at
most

```text
S_LD = min(|Omega|, max(0, 2LD-1)),
```

and the number of endpoint-palette templates is at most

```text
sum_{r=0}^{S_LD} binom(|Omega|,r) 2^{h binom(r,2)}.
```

Thus a proof of the disjoint-overlap cap, together with `(ALT2)`, reduces the
small-support residual branch to endpoint-star charges plus an explicit
near-star template ledger.

## M1 use

In the M1 residue-line program, this is a precise local interface for Work
package C3/C4.4:

```text
prove a row-basis/core-image bound on disjoint-support packet overlaps,
then the post-sift residual is large-support or near-star/template.
```

The missing global theorem is the disjoint-support high-overlap exclusion for
the actual Hankel/Kummer packet families.

## Verification

The companion verifier samples finite packet systems and checks the alternative
against the exact support floor and near-star template bound:

```sh
python3 experimental/scripts/verify_m1_post_sift_residual_alternative.py
```
