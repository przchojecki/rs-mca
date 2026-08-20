# Controls

## Positive controls

1. **Fixed-right-factor family.** Matrices `M_i=M_0+u_i v^T` have every
   pairwise difference of rank at most one and map to one fixed polynomial
   correction ray. The verifier scans every possible universal-core size
   `0<=u<=K-1`; the exact worst case is `8147918` at `u=K-1`.
2. **Fixed-left-factor family.** Matrices `M_i=M_0+u v_i^T` have every
   pairwise difference of rank at most one and map to one correction space.
3. **Maximal-overlap implication.** Two independent degree-`<K`
   polynomials have at most `K-2` common roots. Hence two distinct pair
   types whose cores meet in `K-1` positions have rank-one coefficient
   difference.

## Hostile controls

1. A mixed triple containing both a new left direction and a new right
   direction has a rank-two difference. It is correctly rejected from the
   anticode branch.
2. The fixed-left-factor branch can have correction-space dimension greater
   than one; it cannot be silently charged as one ray.
3. Distinct rank-one anticodes can coexist. The theorem gives no license to
   sum a per-anticode bound without an owner partition.
4. Properness is not assumed automatically. Failure emits an exact
   positive-dimensional affine-linear component.
5. The parent complete-ray theorem is not imported outside its
   nonzero-error scope; the packet keeps and optimizes the universal core.
6. Pairwise rank one is sufficient, not claimed necessary, for large core
   overlap.

## Finite exhaustive control

The Python verifier enumerates the full matrix graph on
`Mat_{2 x 2}(F_3)`. Among the `32` rank-one neighbors of zero it finds
exactly `8` maximal cliques through zero, all of size `9`: four fixed-left
and four fixed-right cliques. No third clique type occurs.

It separately enumerates all `14880` ordered independent pairs of
degree-`<3` polynomials over `F_5` and confirms that their common zero count
on `F_5` is at most `1=K-2`.
