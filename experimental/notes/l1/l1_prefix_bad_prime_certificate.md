# L1 Prefix Bad-Prime Certificate

Status: PROVED / FINITE-FIELD REDUCTION / NOT A FULL AGGREGATION BOUND.

Date: 2026-06-24.

Agent/model: Codex.

## Purpose

This note adds a finite-field bad-prime layer to the L1 monomial-prefix
program.  It is designed to sit after the characteristic-zero reductions and
before any density-over-primes theorem.

The result is deliberately narrow:

```text
finite-field prefix collision
  => characteristic-zero collision
     or p divides an explicit integer resultant certificate.
```

Thus every aperiodic finite-field collision template has a computable bad-prime
certificate.  This does not yet prove the L1 local limit, because one still
has to aggregate these certificates over all aperiodic templates.  It does give
the missing algebraic bridge requested in `agents.md`: convert finite-field
collisions into algebraic-integer divisibility or norm events.

The companion verifier is:

```text
python3 experimental/scripts/verify_l1_prefix_bad_prime_certificate.py
```

It is nonmutating and uses only the Python standard library.

## Setup

Fix `n`, let `zeta` be a primitive `n`-th root of unity, and let

```text
A,B subset Z/nZ,        |A|=|B|=m.
```

For `1 <= r <= m`, define the exponent elementary-sum polynomial

```text
E_r(A;T) = sum_{I subset A, |I|=r} T^{sum_{i in I} i}
```

viewed in `Z[T]/(T^n-1)`.  The top locator coefficients of

```text
L_A(X)=prod_{a in A}(X-zeta^a)
```

are, up to signs, the values `E_r(A;zeta)`.

Let `Phi_n(T)` be the cyclotomic polynomial.  For a pair `(A,B)` and prefix
length `sigma`, set

```text
Delta_r(T) = E_r(A;T)-E_r(B;T),        1 <= r <= sigma.
```

If every `Delta_r` vanishes modulo `Phi_n`, then `(A,B)` is a
characteristic-zero prefix collision.  Otherwise define

```text
C_n,sigma(A,B)
  = gcd_{1 <= r <= sigma, Delta_r not 0 mod Phi_n}
      |Res(Phi_n, Delta_r)|.
```

This is a nonzero integer.  It is invariant under the Galois/dilation action
`A -> uA`, `B -> uB` for `u in (Z/nZ)^*`, and under common translations
`A -> A+t`, `B -> B+t`, up to multiplication of each `Delta_r(zeta)` by a
cyclotomic unit.

## Theorem: Split Bad-Prime Certificate

Let `p` be a prime with `p not dividing n` and `n | p-1`, and let
`h in F_p^*` have order `n`.  Suppose the reductions of `A` and `B` collide in
the finite-field monomial-prefix map:

```text
E_r(A;h) = E_r(B;h) in F_p,        1 <= r <= sigma.
```

Then either `(A,B)` is a characteristic-zero prefix collision, or

```text
p | C_n,sigma(A,B).
```

### Proof

The element `h` has order `n`, so it is a root of `Phi_n` modulo `p`.
For each `r <= sigma`, the finite-field collision hypothesis says that `h` is
also a root of `Delta_r` modulo `p`.

If `Delta_r` is not zero modulo `Phi_n`, the two integer polynomials
`Phi_n` and `Delta_r` have a common root modulo `p`.  Therefore their resultant
vanishes modulo `p`:

```text
Res(Phi_n, Delta_r) = 0 mod p.
```

This holds for every nonzero cyclotomic remainder among the `Delta_r`.  Hence
`p` divides their gcd, namely `C_n,sigma(A,B)`.  If no such nonzero remainder
exists, all `Delta_r` vanish at `zeta`, which is exactly a
characteristic-zero prefix collision.  This proves the theorem.

## Norm Size And Finite-Family Aggregation

The same certificate has a simple size bound.  Since

```text
Res(Phi_n, Delta_r) = Norm_{Q(zeta_n)/Q}(Delta_r(zeta_n)),
```

and each conjugate satisfies

```text
|Delta_r(zeta_n^u)| <= 2 binom(m,r),
```

we have

```text
|Res(Phi_n, Delta_r)| <= (2 binom(m,r))^phi(n).
```

Consequently each non-characteristic-zero template has only finitely many split
bad primes, all dividing a computable integer bounded by these norms.  For a
finite normalized template family `T`, all split primes that realize any member
of `T` divide

```text
LCM_T = lcm_{(A,B) in T} C_n,sigma(A,B).
```

This is not yet the desired L1 aggregation theorem, but it is the exact finite
object that such a theorem can try to bound.

## Prime-Ideal Refinement

The rational certificate is a necessary rational-prime filter, not a sufficient
collision test.  If `p` splits, the actual finite-field row also chooses a
prime ideal

```text
(p, zeta_n-h)
```

or equivalently a primitive `n`-th root `h in F_p`.  The exact ideal-level
condition is

```text
Delta_r(h) = 0 in F_p,        1 <= r <= sigma.
```

Equivalently, define the modular common-root factor

```text
G_p(T)=gcd(Phi_n(T), Delta_1(T), ..., Delta_sigma(T)) in F_p[T].
```

Then the template has a finite-field realization over some primitive `n`-th
root in `F_p` if and only if

```text
deg G_p > 0.
```

Indeed, because `p` does not divide `n`, the roots of `Phi_n` in the algebraic
closure are the primitive `n`-th roots and are simple.  A common zero of all
the `Delta_r` is therefore exactly a nonconstant common divisor of `Phi_n` and
the `Delta_r` reductions.

Thus `p | C_n,sigma(A,B)` says that each nonzero `Delta_r(zeta_n)` vanishes
modulo at least one prime ideal above `p`; it need not be the same prime ideal
for all `r`.

The verifier records a small false-positive template:

```text
A = {0,1,2,7,9,13},
B = {0,1,2,3,4,11},
n = 16,
sigma = 4.
```

Its rational certificate is

```text
C_16,4(A,B) = 194 = 2 * 97,
```

so `97` passes the rational split-prime filter.  But evaluating the four
`Delta_r` at all primitive `16`-th roots in `F_97` gives no common zero;
equivalently the modular gcd `G_97` is constant.  Hence there is no
finite-field prefix collision for this template over `F_97`.

This distinction is important for aggregation: lcm certificates produce a
candidate set of rational primes, while the final row-level verifier or theorem
must still impose the common-prime-ideal condition.

## Affine-Orbit Reduction

The template data has an affine symmetry.  For `u in (Z/nZ)^*` and
`t in Z/nZ`, put

```text
A' = uA+t,
B' = uB+t.
```

Then

```text
Delta'_r(T) = T^(rt) Delta_r(T^u).
```

The substitution `T -> T^u` is a Galois automorphism on primitive `n`-th roots,
and `T^(rt)` is a cyclotomic unit.  Therefore:

```text
C_n,sigma(A',B') = C_n,sigma(A,B).
```

For every split prime `p`, the same identity permutes primitive `n`-th roots in
`F_p`, so the modular common-root degree is also invariant:

```text
deg gcd(Phi_n, Delta'_1, ..., Delta'_sigma)
  =
deg gcd(Phi_n, Delta_1, ..., Delta_sigma).
```

Thus any finite bad-prime aggregation can quotient by affine template orbits
without changing either the rational certificate or the ideal-level collision
test.

## Worked L1 Packet: F_17, n=16

The existing aperiodic collision certificate in
`l1_aperiodic_prefix_collision.md` uses

```text
p = 17,
n = 16,
k = 6,
sigma = 4,
m = n-k-sigma = 6.
```

There are `8008` complement locators, `7968` prefix values, and exactly `40`
two-point finite-field collisions.  These forty pairs are not quotient-core
collisions for the active quotient orders.

The bad-prime certificate explains why this finite-field packet can occur
without being a characteristic-zero collision.  For the three dilation orbits
recorded in the earlier note, the certificate values are:

```text
orbit size 16: C = 68     = 2^2 * 17
orbit size 16: C = 272    = 2^4 * 17
orbit size 8:  C = 147968 = 2^9 * 17^2
```

The aggregate lcm for the whole packet is

```text
LCM = 147968 = 2^9 * 17^2.
```

Thus `17` is the only split prime in the certificate of every collision
template and of the complete three-orbit packet.  In particular, the packet is
a genuine finite-field bad-prime event, not evidence for a characteristic-zero
aperiodic family.

The verifier also checks the same row over the next split primes

```text
p = 97, 113, 193,
```

and finds no collisions.  This is not a proof for all primes; it is a finite
sanity check that the certificate is detecting the known exceptional row.

The current verifier also runs a bounded exact row scan:

```text
p <= 5000,
p = 1 mod 16.
```

It enumerates the full prefix-fiber histogram for every such prime and finds
that the only nonzero collision row is:

```text
p = 17, collision pairs = 40, max fiber = 2.
```

This is a finite theorem for the bounded range, not an asymptotic statement.

## Relation To Scott's L1 Characteristic-Zero PR

PR `#99` develops characteristic-zero prefix-fiber structure.  This note does
not repeat that lane.  It supplies the complementary finite-field layer:
once a template is not one of the characteristic-zero structures, any modular
collision has to pay an explicit bad-prime certificate.

This is the local step needed before one can attempt a density-over-primes or
bad-prime aggregation theorem.

## What Remains Open

The theorem is templatewise.  A positive L1 local-limit theorem still needs a
uniform aggregation bound such as:

```text
sum over robustly aperiodic templates of split primes dividing C_n,sigma(A,B)
```

or a sharper incidence theorem proving that, after quotient and
characteristic-zero strata are removed, only polynomially many bad-prime
templates can contribute to any one finite field.

That aggregation problem is the next hard L1 target.
