# Rank-At-Nodes Regular Bucket Lemma

**Status:** PROVED / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

## Claim

Let \(F\) be a field and let

```text
M(Z) = M_0 + Z M_1
```

be a \(t \times (j+1)\) matrix pencil over \(F\).  For every row set
\(R\) of size \(j+1\), write

```text
Delta_R(Z) = det M(Z)_{R,*}.
```

Then `deg Delta_R <= j+1`.  Hence:

1. if \(M(z_0)\) has column rank \(j+1\) at one tested slope \(z_0\), some
   row set \(R\) has `Delta_R(z0) != 0`, so `Delta_R` is a nonzero regular
   minor;
2. if \(M(z)\) has column rank `< j+1` at \(j+2\) distinct tested slopes, then
   every maximal minor `Delta_R` has \(j+2\) roots while having degree at most
   \(j+1\), so every `Delta_R` is identically zero.

For the Paper D v9 regular overdetermined bucket this gives a deterministic
regular/singular gate: a successful rank specialization supplies a nonzero
minor certificate, while failure at `j+2` distinct nodes is a genuine singular
regular-bucket declaration, not a heuristic.

## Proof

Each entry of \(M(Z)\) is affine-linear in \(Z\).  The determinant of a
\((j+1)\times(j+1)\) submatrix is a sum over permutations of products of
\(j+1\) affine-linear entries, so its degree is at most \(j+1\).

If \(M(z_0)\) has full column rank, elementary linear algebra gives a
\((j+1)\)-row submatrix with nonzero determinant at \(z_0\).  The corresponding
polynomial determinant is therefore not the zero polynomial.

Conversely, if all tested matrices have rank `< j+1`, then every maximal minor
vanishes at each tested node.  A nonzero polynomial of degree at most \(j+1\)
cannot vanish at \(j+2\) distinct field elements.  Therefore all maximal minors
are identically zero.

## Packet Contract

The `rank_at_nodes` selector must record:

```text
rank_pivot_nodes_required = j+2
rank_pivot_nodes_tested
rank_pivot_test_nodes
rank_pivot_node
```

Successful regular-minor packets must name the last tested node as the
successful `rank_pivot_node`.  Singular declarations must test all `j+2` nodes,
set `rank_pivot_node` to null, and record the degree/root-count reason.

The audit certificate

```text
experimental/data/certificates/rank-at-nodes-regular-bucket/
  rank_at_nodes_regular_bucket_audit.json
```

checks this contract for every current v9 packet item using `rank_at_nodes`.
At creation it audited five packet items: three regular-minor witnesses and two
singular/residual declarations.

## Reproduce

```sh
python3 experimental/scripts/verify_m1_rank_at_nodes_regular_bucket.py \
  --check experimental/data/certificates/rank-at-nodes-regular-bucket/rank_at_nodes_regular_bucket_audit.json
```

## Non-Claims

This lemma does not enumerate roots in large fields, does not close the
`F_17^32` M3 actual-row window, and does not build singular pivot charts.  It
only proves and audits the regular-bucket decision gate used before those
steps.
