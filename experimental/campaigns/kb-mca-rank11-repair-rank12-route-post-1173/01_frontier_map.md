# Frontier map

## Exact parent

PR #1173 head `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

## Repaired joint

The heavy-core rank descent is valid only with a lower-rank theorem uniform in
the ambient shortened dimension.  The former draft compared every descent
path directly to the `K=1` rank-one endpoint without proving that uniformity.

The new weighted projective-line theorem normalizes an arbitrary rank-one
direction polynomial, treats nonzero coordinates as graph lines and remaining
zero coordinates as vertical lines, deletes the universal core, and scans all
residual dimensions `1 <= j <= 1,048,576`.  Its exact maximum is `4,070,947`
at `j=1`.

This supplies the induction base needed by the complete-core descent and pays
affine error rank eleven without assuming delayed rank drops.

## Rank-twelve route

The new dense-core theorem bounds low-margin pair types by a Cauchy
second-moment inequality using:

```text
core size at least h=d+K-T,
pairwise core intersection at most K-1.
```

A fixed barrier schedule forces successive proper rank drops unless the
current family is already below a certified direct cap.  The final source-bound
descendant has at least `8,681,730` slopes and direction dimension at most two.

If rank two persists to `K=2`, the `T=1922` endpoint has:

```text
high slopes                 131,690
low slopes                8,550,040
pair types                  9 to 15
deficiency-one types        at least 3
independent capacity      8,829,951
missing cross-pair saving    279,912
```

If rank two drops earlier, a rank-one descendant of at least `558,412` slopes
is emitted.

## Next theorem

The next load-bearing statement must couple the ratio-fiber matchings of
different fixed pairs.  Independent fixed-pair capacities are no longer
enough.  A successful theorem should either save `279,912` slopes in the
fifteen-type endpoint relaxation or route the near-saturated pair matrices to
one paid rank-one anticode/rational owner.
