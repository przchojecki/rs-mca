# Height-Only Certification Limit

Status: PROVED / CERTIFICATION-ARITHMETIC / METHOD LIMIT.

This note packages the DAG node:

```text
height_only_impossibility
```

It is a scoping theorem for the quotient value-set problem.  The graded
collision radius proves that a pair at swap distance `s` is certified by the
archimedean norm gate when

```text
(2s)^phi(N) < p.
```

This note records the converse limitation of that method under a field-size
ceiling: a proof that only uses this height gate cannot certify an entire
quotient cell if the worst-pair height bound already exceeds every allowed
prime.  This is why the far-pair problem must use additional `p`-specific or
factorization structure, such as the cluster and generator-economy
certificates.

The companion verifier is:

```text
python3 experimental/scripts/verify_height_only_impossibility.py
```

The emitted certificate is:

```text
experimental/data/certificates/height-only-impossibility/height_only_impossibility.json
```

## Convention Block

```text
object:              quotient e_1 value-set certification
quotient order:      N
locator class:       ell-subsets of Z/NZ
cell diameter:       s_max = min(ell, N-ell)
field prime:         p < 2^L, used as the reduction characteristic
method:              pure triangle-inequality norm gate
denominator role:    p is not a slope denominator; consumers print q_line/q_chal
```

This is a theorem about a certification method.  It does not assert that
collisions exist, and it does not rule out stronger certificates using exact
norms, congruences, factorization, clusters, or generator-economy designs.

## Theorem: Pure Height Full-Cell Criterion

Let `C(N,ell)` be the family of `ell`-subsets of `Z/NZ`, and let

```text
s_max = min(ell, N-ell).
```

The cell contains two subsets at swap distance exactly `s_max`.  Therefore the
graded triangle-height gate can certify every pair in the cell only if

```text
(2 s_max)^phi(N) < p.
```

Equivalently, for a field-size ceiling `p < 2^L`, the pure height gate is
incapable of giving a uniform full-cell certificate whenever

```text
(2 s_max)^phi(N) >= 2^L.
```

Proof.  Choose an `ell`-subset `B`.  If `ell <= N/2`, replace all `ell`
elements of `B` by `ell` elements of its complement.  If `ell > N/2`, keep the
forced overlap of size `2ell-N` and replace the remaining `N-ell` elements by
the complement.  This gives a second `ell`-subset `B'` with
`|B \ B'| = min(ell,N-ell) = s_max`.  The graded collision-radius method
certifies a pair only under `(2s)^phi(N)<p`; applying it to this pair requires
the displayed condition.

## Prize-Range Consequence

For the four official rates with the quotient-cell convention

```text
ell = rho N + 1,
```

the verifier computes the exact worst-pair height requirements:

```text
N = 64:   the full-cell gate is below 2^256, so large enough primes can pass;
N = 128:  all four official-rate cells need p >= 2^256;
N >= 256: the obstruction is stronger.
```

For example, at `N=128`, `phi(N)=64`.  The rate `1/16` cell has `ell=9`, so
the full-cell gate would need

```text
(18)^64 < p,
```

which already exceeds the `p < 2^256` prize range.  Higher rates only increase
`s_max`.  Thus a full-strength zone-`(b)` proof cannot be just a pure-height
full-cell argument from `N=128` onward.

At `N=64`, the largest official-rate full-cell bound has bit length `191`.
Thus those cells are certified only for rows with `p` above the printed bound
(for example `p >= 2^191` suffices for the largest one), not for every smaller
prime below `2^256`.

## Consequence For Strategy

The height gate remains valuable locally: it gives certified balls of radius
`d_*(N,L)` and proves small-scale fullness.  The impossibility is only for
covering the entire cell with that one worst-pair bound.  To pass the
knife-edge value-set lower bound at `N>=128`, one needs additional structure:

```text
cluster certificates
generator-factored differences
exact per-prime norm checks
or another p-specific lower-bound mechanism.
```

This is why generator-economy searches and cluster certificates are not
optional embellishments; they are the natural next layer after the graded
radius theorem.
