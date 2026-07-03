# Cluster Certificates For Quotient Value Sets

Status: PROVED / CERTIFICATION-ARITHMETIC.

This note packages the DAG node:

```text
cluster_certificates
```

It builds directly on `graded_collision_radius`.  The purpose is to turn
pairwise norm-height certification into two reusable compression rules:

```text
local balls      -> certified free cliques
factored pairs   -> one norm check for many cross-pairs
```

This is still certification arithmetic.  It does not construct the large
generator-economy designs needed for the far-pair value-set lower bound.

The companion verifier is:

```text
python3 experimental/scripts/verify_cluster_certificates.py
```

The emitted certificate is:

```text
experimental/data/certificates/cluster-certificates/cluster_certificates.json
```

## Convention Block

```text
object:              quotient e_1 value-set certification
number field:        K = Q(zeta_N), ring O = Z[zeta_N]
field prime:         p, used as the reduction characteristic
local metric:        swap distance on ell-subsets of Z/NZ
denominator role:    p is not a slope denominator; consumers print q_line/q_chal
endpoint convention: strict norm gates, all factors nonzero
```

Every statement below is a statement about preserving characteristic-zero
distinctness after reduction modulo `p`.  If the characteristic-zero values
are already equal, these lemmas do not separate them.

## Theorem 1: Local Free Cliques

Let `F` be a family of `ell`-subsets of `Z/NZ`.  Suppose:

1. for every distinct `B,B' in F`, the algebraic difference
   `e_1(B)-e_1(B')` is nonzero in `Z[zeta_N]`;
2. the swap diameter of `F` is at most `d`;
3. `(2d)^phi(N) < p`.

Then the reductions of `e_1(B)` for `B in F` are pairwise distinct modulo
every prime of `Z[zeta_N]` above `p`.

Proof.  Apply the graded collision radius theorem to each pair.  The swap
distance of each pair is at most `d`, and the characteristic-zero difference
is nonzero by hypothesis.

In particular, if `d_*(N,L)` is the certified radius from
`graded_collision_radius.md`, then every characteristic-zero injective family
of swap diameter at most `d_*(N,L)` is certified over every prime `p >= 2^L`.

## Theorem 2: Multiplicative Cross-Cluster Certificates

Let `Delta in O` be nonzero and let `Gamma` be a finite set of nonzero
elements of `O`.  Suppose the cross-pair differences between two clusters all
lie in

```text
{ Delta * gamma : gamma in Gamma }.
```

If

```text
p does not divide Norm(Delta)
```

and, for every `gamma in Gamma`,

```text
p does not divide Norm(gamma),
```

then every cross-pair difference is nonzero modulo every prime above `p`.

Proof.  Norms multiply:

```text
Norm(Delta * gamma) = Norm(Delta) Norm(gamma).
```

The first hypothesis says no prime above `p` divides `Delta`.  The second
hypothesis says no prime above `p` divides any `gamma`.  Therefore no prime
above `p` divides any product `Delta gamma`.

This is the rigorous one-check compression rule: after a design has proved
that all cross-pair differences factor through one base element `Delta` and a
factor set `Gamma` whose norms are already certified away from `p`, only the
modular norm check on `Delta` is row-specific.  A common sufficient condition
for each factor is the printed small-norm bound

```text
0 < |Norm(gamma)| < p.
```

## Corollary: Integer Factors Are Free

Let `Delta in O` be certified at the prime `p`, meaning `p` does not divide
`Norm(Delta)`.  If

```text
0 < |m| < p
```

is a rational integer, then `m Delta` is also certified.

Proof.  Apply Theorem 2 with `Gamma={m}`.  Since

```text
Norm(m) = m^phi(N),
```

the condition `0 < |m| < p` implies `p` does not divide `Norm(m)`.  If one
wants a certificate that avoids even checking divisibility, the stronger
small-norm condition

```text
0 < |m|^phi(N) < p
```

also suffices and is the form used by the verifier's toy packet.

## How This Feeds The Far-Pair Problem

The hard value-set task is not local collision freedom.  At `N=128` and
prize-scale `p`, the local radius is only `7`, while large rate cells have
diameter about `N/2`.  The remaining task is therefore design-theoretic:
construct large families whose far-pair differences are covered by a small
number of certified factors.  This note supplies the proof rule those designs
must satisfy; it does not assert their existence.
