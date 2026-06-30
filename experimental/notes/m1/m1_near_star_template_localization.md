# M1 near-star template localization

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note packages the finite endpoint-template conclusion which follows after
endpoint-star pruning and any far-from-star exclusion.  It is a local
combinatorial statement for two-endpoint packet supports.  It does not prove
the far-from-star density theorem and does not prove the M1 aperiodic
local-limit theorem.

## Scope

The lemma concerns a finite projective endpoint universe `Omega` of size `q+1`.
Each residual support is a two-element subset of `Omega`.  Over every support
there are at most `h` packet classes, and a residual template records which of
those classes are selected.

No generated-field, line-field, challenge-field, agreement, radius, or
noncontainment convention enters this local counting lemma.

## Endpoint-star pruning

Let `Sigma` be a finite set of two-point endpoint supports.  Fix an endpoint
degree cap `D >= 0`.  Repeatedly choose an endpoint contained in more than `D`
remaining supports and charge all remaining supports through that endpoint.
Since `Sigma` is finite, this process terminates and gives a disjoint
decomposition

```text
Sigma = Sigma_star disjoint Sigma_ap,
```

where:

```text
every support in Sigma_star contains one charged star center,
every endpoint has degree at most D inside Sigma_ap.
```

Thus any uncharged residual support family has maximum endpoint degree at most
`D`.

## Near-star localization

Fix an integer `L >= 2`.  If the residual family has

```text
m = |Sigma_ap| < L D,
```

then its endpoint footprint

```text
U = union_{S in Sigma_ap} S
```

satisfies

```text
|U| <= 2m < 2 L D.
```

Equivalently, because `|U|` is an integer,

```text
|U| <= S_LD := min(q+1, max(0, 2 L D - 1)).       (NS1)
```

Hence a residual branch that has been forced into `m < LD` is a bounded
near-star template branch: it lives on at most `S_LD` endpoints.

## Template count

Once the endpoint footprint `U` is fixed, a palette template is determined by
choosing, for each unordered pair `{x,y} subset U`, a subset of the `h` packet
classes available over that pair.  The empty subset means the pair is absent.
Therefore the number of possible near-star palette templates is at most

```text
T_near(q,D,L,h)
  <= sum_{s=0}^{S_LD} binom(q+1,s) 2^{h binom(s,2)}.      (NS2)
```

The coarser polynomial-in-`q` form is

```text
T_near(q,D,L,h)
  <= (S_LD+1)(q+1)^{S_LD} 2^{h binom(S_LD,2)}.             (NS3)
```

For fixed `D,L,h`, this is `O_{D,L,h}(q^{S_LD})`.  Thus once a separate
far-from-star theorem rules out the `m >= LD` residual branch, the local
packet problem has only a polynomial-size endpoint-template ledger left.

## M1 use

Combined with `m1_packet_overlap_endpoint_sift.md`, this gives the local
shape of the post-sift residual alternative:

```text
selected packet family
  => endpoint-star charges
     + large support
     + disjoint-support high-overlap target
     + one of at most T_near(q,D,L,h) near-star templates.
```

The missing M1 theorem is the global input excluding the far-from-star
high-overlap branch except for quotient-periodic, subfield-confined, or
low-template structure.  This note makes the leftover template branch finite
and explicit once that input is available.

## Verification

The companion verifier checks the pruning invariant, near-star footprint
bound, exact template count, and coarse polynomial bound over sampled finite
endpoint systems:

```sh
python3 experimental/scripts/verify_m1_near_star_template_localization.py
```
