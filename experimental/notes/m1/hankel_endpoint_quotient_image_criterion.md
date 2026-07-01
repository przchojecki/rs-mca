# Hankel Endpoint Quotient-Image Criterion

Status: PROVED / AUDIT.

This note extracts the criterion used by the M3 low-rank endpoint
quotient-image audit.  It is deliberately local: it explains when a projective
endpoint that is witnessed on a small co-support is also charged to the
quotient-image ledger by a different quotient-remainder support.

## Criterion

Let `D` be an `n`-point Reed-Solomon domain and let

```text
r = n-k,
h_x = (1,x,...,x^(r-1)).
```

Let `A` be an agreement level and put `j=n-A`.  Suppose:

1. `X subset D` has size `j+1`, and `u=sum_{x in X} h_x`;
2. `Y subset D`, and the projective endpoint syndrome `v` lies in `W_Y`;
3. there is a quotient-remainder support `S` of size `A` with `S cap Y = empty`;
4. for `T=D\S`, the Vandermonde columns indexed by `X union T` are independent.

Then the projective endpoint `[0:1]` is in the quotient-image branch for the
support `S`: `v in W_T`, but `u notin W_T`.

The usual distinct-point Vandermonde test proves hypothesis 4 whenever

```text
|X union T| <= r.
```

## Proof

Since `S` is disjoint from `Y`, the co-support `T=D\S` contains `Y`.  Therefore
`v in W_Y subset W_T`.

If `u in W_T`, then

```text
sum_{x in X} h_x - sum_{t in T} a_t h_t = 0
```

for some coefficients `a_t`.  This is a linear relation among the columns in
`X union T`.  By independence it is the trivial relation.  But `|X|=j+1` and
`|T|=j`, so `X` is not contained in `T`; for some `x in X\T` the coefficient of
`h_x` is `1`, a contradiction.  Hence `u notin W_T`.

The support `S` is quotient-remainder by hypothesis, so this endpoint parameter
is paid by quotient-image accounting even if another, minimal endpoint support
is not quotient-remainder.

## Cyclic quotient-fiber construction

For a cyclic domain of order `n`, quotient fibers of size `c` are exponent
classes modulo `n/c`.  If the update set `Y` hits `h` quotient residues, then
there are `n/c-h` fibers disjoint from `Y`.  A quotient-remainder support of
size `A` disjoint from `Y` exists if

```text
n/c - h >= floor(A/c) + 1_{A mod c != 0}.
```

Choose `floor(A/c)` safe full fibers and, if needed, `A mod c` elements from one
additional safe fiber.

## M3 low-rank instantiation

For the `F_17^32`, `n=512`, `k=256` M3 low-rank ladder:

```text
385 <= A <= 426,
j = 512-A,
|X| = j+1,
2 <= |Y| <= 11,
r = 256.
```

The endpoint-image audit uses `c=2`.  The quotient order is `256`, and a
consecutive update block of length at most `11` hits at most `11` quotient
residues, leaving at least `245` safe fibers.  The largest required number of
safe fibers is

```text
floor(426/2) = 213.
```

For odd `A`, the requirement is still at most `floor(425/2)+1=213`.  Thus the
safe `c=2` quotient-remainder support exists for every checked row.

The independence bound is

```text
|X union T| <= |X|+|T| = (j+1)+j = 2j+1 <= 255 <= r,
```

because `j <= 127` throughout the window.  Therefore the criterion applies to
all `420` rank/agreement endpoint rows.

## Relation to the support exclusion audit

This criterion is compatible with the endpoint quotient-support exclusion.  The
minimal endpoint support `D\Y` is not a nontrivial proper quotient-remainder
support in the M3 low-rank ladder, because `Y` hits too many quotient fibers.
The quotient-image audit uses a different support `S` of size `A`; quotient
image asks whether some quotient-remainder support explains the same endpoint
parameter, not whether the minimal support is quotient-remainder.

Non-claims: this note does not audit finite affine roots, arbitrary M3 rows, or
arbitrary projective endpoint shapes.  It only records a reusable sufficient
criterion and its M3 low-rank instantiation.
