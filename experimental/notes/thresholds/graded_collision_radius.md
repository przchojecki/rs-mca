# Graded Collision Radius

Status: PROVED / CERTIFICATION-ARITHMETIC.

This note packages the DAG node:

```text
graded_collision_radius
```

and subsumes the single-swap base case.  It is a quotient value-set
certification lemma, not a new MCA threshold.  Its role is to identify the
swap-distance range where reduction modulo the prize prime cannot create new
`e_1` collisions.  That range should not be treated as experimental evidence:
inside it, the collision-free conclusion is a theorem.

The companion verifier is:

```text
python3 experimental/scripts/verify_graded_collision_radius.py
```

The emitted certificate is:

```text
experimental/data/certificates/graded-collision-radius/graded_collision_radius.json
```

## Convention Block

```text
object:              quotient e_1 value-set certification
quotient order:      N
locator class:       ell-subsets of Z/NZ, via B -> e_1(B)=sum_{b in B} zeta_N^b
field prime:         p with an order-N root modulo p, so N | p-1
denominator role:    p is the quotient/value-set reduction characteristic
sampler:             not a slope sampler; consumers must print q_line/q_chal
endpoint convention: strict norm gate |Norm(delta)| < p
```

The theorem certifies equality between the characteristic-zero `e_1` value set
and its reduction modulo `p` on the certified pairs.  It does not assert that
the characteristic-zero map `B -> e_1(B)` is injective.  If two distinct
classes already have the same algebraic `e_1` value, this lemma treats their
difference as zero rather than as a modular collision.

## Theorem: Graded Collision Radius

Let `zeta` be a primitive `N`-th root of unity and let

```text
e_1(B) = sum_{b in B} zeta^b
```

for finite subsets `B` of `Z/NZ`.  Suppose `B` and `B'` have the same
cardinality and swap distance

```text
s = |B \ B'| = |B' \ B|.
```

Put

```text
Delta = e_1(B) - e_1(B').
```

If `Delta != 0` in `Z[zeta]`, then

```text
|Norm_{Q(zeta)/Q}(Delta)| <= (2s)^phi(N).
```

Consequently, if `p` is a rational prime and

```text
(2s)^phi(N) < p,
```

then `Delta` cannot vanish modulo any prime of `Z[zeta]` above `p`.  In
particular, reduction modulo `p` creates no new collision between the two
distinct characteristic-zero values `e_1(B)` and `e_1(B')`.

Proof.  For every complex embedding `sigma` of `Q(zeta)`,

```text
sigma(Delta) =
    sum_{b in B\B'} sigma(zeta)^b - sum_{b in B'\B} sigma(zeta)^b.
```

All terms have absolute value `1`, so the triangle inequality gives
`|sigma(Delta)| <= 2s`.  Multiplying over the `phi(N)` embeddings gives the
norm bound.  If `Delta` vanished modulo a prime ideal above `p`, then `p`
would divide the rational integer `Norm(Delta)`.  A nonzero integer with
absolute value strictly less than `p` is not divisible by `p`.

## Corollaries

**Single swaps.**  If `s=1`, then

```text
Delta = zeta^a - zeta^b != 0
```

for `a != b`.  Hence single-swap collisions are impossible whenever

```text
2^phi(N) < p.
```

For the prize-scale primes considered in the quotient corridor this is far
below the available characteristic range on the small quotient orders.

**Full small-scale certification.**  If all pairs in an `ell`-subset value-set
problem have swap distance at most `s_max = min(ell, N-ell)` and

```text
(2 s_max)^phi(N) < p,
```

then reduction modulo `p` creates no new collisions anywhere in that cell.
Equivalently, the modulo-`p` value set has exactly the same cardinality as the
characteristic-zero value set.

This is the precise form of the shorthand "all pairs are certified" used in
the roadmap.  If one uses the more conservative bound `s_max <= ell`, the
condition becomes `(2 ell)^phi(N) < p`.

**Radius table.**  For a lower bit bound `p >= 2^L`, define

```text
d_*(N,L) = max { s >= 0 : (2s)^phi(N) < 2^L }.
```

Then every pair of characteristic-zero distinct `e_1` values at swap distance
`s <= d_*(N,L)` stays distinct modulo every prime `p >= 2^L`.  The verifier
prints the table used by the roadmap.  In particular, for `N=128` and `L=250`,
it obtains `d_*=7`, matching the advertised frontier.

## Non-claims

This note does not prove the hard value-set lower bound in zone `(b)`.  At
`N=128` and prize-scale `p`, the certified radius is only `7`, while the
maximal swap distance in the rate-`1/2` quotient cell is about `N/2`.  The
remaining work is the far-pair certification problem: composing local
collision-free balls, cluster certificates, or generator-economy designs into
a value-set lower bound larger than the prize budget.
