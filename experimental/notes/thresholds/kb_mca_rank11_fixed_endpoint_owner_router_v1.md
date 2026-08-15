# KoalaBear rank-eleven fixed-endpoint owner router

Status: **PROVED DIRECT BRANCH PAYMENT / STRUCTURAL ROUTE CUT**.  Exact parent
is PR #1171 head `a3fc2d5aea86577cd50d8b95b6eb2155d4d940f6`.  Active-v4
ledger movement is zero.

For the post-near affine-error-rank-eleven family, use the nonuniform support
margins `theta_gamma` and split at `tau=439`.  If all low minimizing-pair
coefficient matrices have pairwise rank distance at most one, #1171 puts them
in a fixed-right or fixed-left matrix anticode.

The fixed-right branch retains #1171's exact `8147918` ray cap.  In the
fixed-left branch, an invertible endpoint row operation makes one endpoint
codeword common to every pair type.  On its complete agreement set `G` of
size `g`, the varying endpoints form one ordinary affine Reed--Solomon list
with agreement at least `m-439`.  Same-support pair noncontainment forces each
nonexceptional owning slope to use a coordinate outside `G`; for fixed pair
type and coordinate that equation determines one slope.

Thus the low branch is at most

```text
1+max_g (n-g) floor(
 C(g-K+10,10)/C(m-439-K+10,10)
).
```

The analytic binomial envelope has unique `g` maximizer `2001826` and equals
`32215263489919749`.  The high-margin resource contributes
`242314927584173240`; adding `2w=134944` gives

```text
274530191074227933 < 274980728111395087,
```

with slack `450537037167154`.  Cutoff `438` remains over budget, so `439` is
the first paying cutoff.  The same envelope has unique minimum
`81826485385525648` at cutoff `3608`.

Consequently any over-budget line has two low pair types with rank-two
coefficient difference.  Their complete cores each have size at least
`1115609`, intersect in at least `134066` coordinates, and force a common
evaluation-root factor of degree at least `134066` in both endpoint-difference
polynomials.

Nonclaims: no rank-eleven payment, no chronology owner for the common factor,
no sum over different factor edges, and no KoalaBear closure.
