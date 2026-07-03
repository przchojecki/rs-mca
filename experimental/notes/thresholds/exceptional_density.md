# Exceptional Density For Quotient Value-Set Collisions

Status: PROVED / CERTIFICATION-ARITHMETIC / PARTIAL.

This note packages the DAG node from the active roadmap branch:

```text
are_exceptional_density
```

It is a density corollary of `graded_collision_radius.md`.  The result is
useful but intentionally weaker than a row-specific certificate: it says that
large modular collision mass can occur at only a bounded number of large
primes, averaged over a dyadic range.  It does not prove that the official
prime in a given row avoids the exceptional set.

The companion verifier is:

```text
python3 experimental/scripts/verify_exceptional_density.py
```

The emitted certificate is:

```text
experimental/data/certificates/exceptional-density/exceptional_density.json
```

## Convention Block

```text
object:              quotient e_1 value-set certification
quotient order:      N
locator class:       ell-subsets of Z/NZ, via B -> e_1(B)=sum zeta_N^b
field prime:         rational primes p in a finite set P, usually dyadic
denominator role:    p is the quotient/value-set reduction characteristic
sampler:             not an MCA/list slope sampler
endpoint convention: rational bad primes divide nonzero algebraic norms
```

Every assertion is conditional on characteristic-zero distinctness of the
pairs being counted.  Characteristic-zero coincidences are upstairs
duplicates, not bad rational primes.

## Theorem: Bad-Prime Incidence Bound

Let `F` be a finite family of `ell`-subsets of `Z/NZ`.  For each unordered
pair `{B,B'}` with

```text
Delta(B,B') = e_1(B)-e_1(B') != 0
```

choose a height bound `H_{B,B'} >= |Norm(Delta(B,B'))|`.  Let `P` be any
finite set of rational primes, all at least `P_min >= 2`.  Then the total
number of bad-prime incidences

```text
I(P,F) = #{ (p,{B,B'}) : p in P, p divides Norm(Delta(B,B')) ) }
```

satisfies

```text
I(P,F) <= sum_{Delta(B,B') != 0} floor(log_{P_min}(H_{B,B'})).
```

In particular, if every pair has swap distance at most `s_max`, then

```text
H_{B,B'} = (2 s(B,B'))^phi(N) <= (2 s_max)^phi(N)
```

is admissible by the graded collision-radius theorem, giving the coarser
uniform bound

```text
I(P,F) <= M * floor( phi(N) log_{P_min}(2s_max) ),
```

where `M` is the number of characteristic-zero distinct unordered pairs.

Proof.  Fix a nonzero `Delta`.  If `k` distinct primes from `P` divide
`Norm(Delta)`, their product is at least `P_min^k` and also divides the
nonzero integer `Norm(Delta)`.  Hence

```text
P_min^k <= |Norm(Delta)| <= H_{B,B'}.
```

Thus `k <= floor(log_{P_min}(H_{B,B'}))`.  Summing over all nonzero pairs
proves the first inequality.  The second follows from
`|Norm(Delta)| <= (2s)^phi(N)`.

## Markov Corollary: Large-Collision Primes Are Sparse

Let `M` be the number of characteristic-zero distinct unordered pairs in
`F`, and let

```text
R = floor(log_{P_min}((2s_max)^phi(N))).
```

For any real `0 < theta <= 1`, the number of primes in `P` that collide at
least `theta M` pairs is at most

```text
floor(MR / ceil(theta M)) <= floor(R/theta).
```

Thus, in a dyadic range with `P_min=2^L`, a quotient cell with `R=1` has at
most two primes colliding at least half of all characteristic-zero distinct
pairs, regardless of how many primes the dyadic range contains.

## Interpretation

This is a partial, dossier-grade statement.  It can make the exceptional-prime
residue explicit and small for large-collision events, and it justifies using
bad-prime accounting as an average-case sanity check.  It is not a substitute
for the row-specific certificates needed by the prize package:

- it does not prove characteristic-zero injectivity of `B -> e_1(B)`;
- it does not identify the official prime as good;
- it does not prove a value-set lower bound at a specified prime;
- it does not close the generator-economy design problem.

