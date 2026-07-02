# Hankel Rank-6 A385 Fixed-Core Synthesis

Status: PROVED / AUDIT.

This note synthesizes the fixed-core part of the separated `A=385` rank-6
boundary analysis.  It does not add a new local calculation; it composes the
existing fixed four-core, fixed three-core, and fixed two-core packets into one
auditable frontier statement.

The setting is the separated `A=385` rank-6 boundary.  Here `j=127`, `t=129`,
`m=128`, and the low-degree transfer has boundary defect `h=5`, so finite
rank-drop roots are represented by a projective `Q`-space of dimension `4`
before any forced base-root core is imposed.

The synthesis statement is:

```text
Every separated A=385 rank-6 branch whose split-locator candidates share a
fixed forced base-root core of size at least two is projective-budget safe.
```

The proof is a case split by the fixed base-core size.

For a fixed core of size at least four, the fixed base-core packet applies
after choosing any four-point subcore.  Four base evaluations collapse the
`Q`-space to one projective class, giving at most one finite noncontained
parameter plus the projective endpoint:

```text
1 + 1 <= 6.
```

For a fixed three-core branch, the quadratic-cut packet closes the case where
some pairwise direction-consistency equation restricts to a nonzero binary
quadratic on the residual `Q`-line:

```text
2 finite classes + 1 endpoint <= 6.
```

The complementary ratio-identically-consistent residual line is then closed by
the residual-closure packet.  Incidence is safe through `e_G<=70`; product
collapse excludes `71<=e_G<=122`; and the punctured projective tangent tail is
budget-safe for `e_G>=122`.  Thus no fixed three-core residual remains.

For a fixed two-core branch, the packet tree closes the residual `Q`-plane:

```text
no-common-component conic pair     -> Bezout total <= 5;
component cut                      -> component/off-component total <= 5;
global component, constant slope   -> total <= 2;
slope-free locus/component         -> empty;
nonconstant moving-slope component -> incidence plus high-core closure.
```

The high-core closure combines the line product-collapse analogue, the conic
product-collapse packet, and the punctured projective tangent tail.  It closes
all fixed two-core line/conic moving-slope components.

Therefore any remaining separated `A=385` over-budget obstruction must avoid a
fixed forced two-point base core in the counted branch.  The live frontier is
now:

```text
branches without a fixed two-point base core;
moving-core/no-common-core A=385 branches;
overlapping-support rank-6 pencils;
row-level M3 synthesis across all A=385 rank-6 buckets.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_fixed_core_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-fixed-core-synthesis/f17_32_n512_k256_m3_rank6_a385_fixed_core_synthesis.json
```

Nonclaims:

```text
no proof that every A=385 over-budget branch has a fixed two-point base core;
no closure of moving-core or no-common-core A=385 branches;
no overlapping-support rank-6 classification;
no endpoint payment outside the cited projective accounting and tangent-tail packets;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
