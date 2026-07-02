# E1 Collision Norm Criterion

- **Status:** PROVED / experimental verifier.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable execution queue `Q2.15 [collision_norm_criterion]`;
  evidence task `E1`.
- **Verifier:** `experimental/scripts/verify_row_c_e1_collision_norm_criterion.py`.
- **Artifact:** `experimental/data/certificates/row-c-e1-sampling/row_c_e1_collision_norm_criterion.json`.

This note isolates the algebraic gate behind modular collisions in the Row-C
`e_1` value-set experiment.  It complements the birthday sampler: the sampler
looks for collisions, while this criterion says what any genuine collision has
to exploit.

## Setup

Let `N` be even, let `zeta` be a primitive `N`-th root of unity, and let
`ell'` be the quotient agreement size.  The Paper B antipodal-class normal
form represents a characteristic-zero `e_1` value as

```text
E(B) = sum_i eps_i zeta^i,        eps_i in {-1,0,1},
```

where only singleton antipodal pairs contribute; full antipodal pairs have
zero `e_1` sum.

For two classes `B,B'`, put

```text
Delta_{B,B'}(zeta) = E(B)-E(B') in Z[zeta].
```

If `Delta != 0`, define the integer

```text
N_{B,B'} = Norm_{Q(zeta)/Q}(Delta_{B,B'}).
```

Equivalently,

```text
N_{B,B'} = Res(Phi_N(X), Delta_{B,B'}(X)).
```

## Criterion

Let `p` be a prime with `p == 1 mod N`, and choose an embedding

```text
zeta -> omega in F_p^*
```

where `omega` has exact order `N`.

If the two classes are distinct in characteristic zero and collide under this
embedding,

```text
Delta_{B,B'}(omega) = 0 mod p,
```

then

```text
p | N_{B,B'}.
```

Conversely, if `p | N_{B,B'}`, then at least one Galois-conjugate embedding

```text
zeta -> omega^a,      gcd(a,N)=1,
```

has

```text
Delta_{B,B'}(omega^a)=0 mod p.
```

Since the antipodal class set is stable under `zeta -> zeta^a`, this is also a
fixed-embedding collision for the Galois-conjugate pair of classes.  Thus
heavy modular collision structure must come from primes dividing many of these
explicit nonzero cyclotomic norms.

**Proof.**  The fixed embedding corresponds to a prime ideal above `p` in
`Z[zeta]`.  If `Delta(omega)=0`, then `Delta` lies in that prime ideal, so the
rational norm of `Delta` is divisible by `p`.

For the converse, `p == 1 mod N` splits completely in `Q(zeta)`.  Modulo `p`,

```text
Phi_N(X) = product_{gcd(a,N)=1} (X-omega^a).
```

Therefore

```text
N_{B,B'} = product_{gcd(a,N)=1} Delta(omega^a)  mod p.
```

The product vanishes modulo `p` if and only if at least one conjugate factor
vanishes.

## Height Bound

Each difference `Delta` has `l_1` coefficient norm at most `2 ell'`, so every
complex conjugate has absolute value at most `2 ell'`.  Hence

```text
|N_{B,B'}| <= (2 ell')^{phi(N)}.
```

For the Row-C dyadic quotient orders `N=2^a`, this becomes

```text
|N_{B,B'}| <= (2 ell')^{N/2}.
```

This is the bounded-height norm family mentioned in the E1 roadmap.

## Graded Collision Radius

The same argument gives a local injectivity certificate.  If two dyadic
antipodal classes differ by coefficient `l_1` norm at most `2d`, then

```text
|N_{B,B'}| <= (2d)^phi(N).
```

Therefore, for any fixed prime `p == 1 mod N`, the norm criterion forbids a
distinct-class collision whenever

```text
(2d)^phi(N) < p.
```

The verifier computes this radius for the Row-C prime.  For the compatible
quotient orders, it gives:

| `N'` | `ell'` | full class injective? | certified half-`l_1` radius `d` |
|---:|---:|:---:|---:|
| 64 | 33 | yes | 112 |
| 128 | 65 | no | 7 |
| 256 | 129 | no | 1 |

For `N'=64`, the maximum possible half-`l_1` distance between two classes is
at most `ell'=33`, well below the certified radius `112`.  Thus the entire
`N'=64` Row-C value set is injective modulo the Row-C prime: duplicate sampled
values in the birthday run can only come from resampling the same
characteristic-zero class, not from a distinct-class modular collision.  The
actual E1 uncertainty starts at `N' >= 128`, where the height bound certifies
only local neighborhoods.

## Cluster-Certificate Consequences

The same certificate gives the QA.14 cluster machinery recorded separately in
`experimental/notes/roadmaps/e1_cluster_certificates.md`:

- any class set of pairwise half-`l_1` diameter at most the graded radius is a
  free clique;
- if every cross-cluster difference factors as `Delta * Q_xy` with `Q_xy` a
  nonzero algebraic integer of norm strictly between `0` and `p`, then one norm
  check on `Delta` certifies all cross-pairs;
- integer scalar multiples `m Delta` with `0 < m < p` are automatically
  certified once `Delta` is.

The algebraic-integrality/factorization hypothesis in the second item is
deliberate.  The later generator-economy problem is to construct large
families with those factorizations; this note only supplies the reusable
certificate rule after such a factorization is known.

## Exceptional-Prime Counting Corollary

Let `F` be any finite family of unordered pairs of distinct characteristic-zero
classes, and write

```text
M_F = product_{(B,B') in F} |N_{B,B'}|
```

after omitting pairs with zero norm.  For any threshold `P_0 >= 2`, the number
of primes `p >= P_0` that can produce a modular collision for some pair in `F`
is at most

```text
floor(log(M_F) / log(P_0)).
```

Using the height bound above, this gives the uniform estimate

```text
#{exceptional primes p >= P_0}
  <= |F| * phi(N) * log(2 ell') / log(P_0).
```

**Proof.**  By the norm criterion, every such exceptional prime divides at
least one nonzero norm `N_{B,B'}`, hence divides `M_F`.  Distinct primes
`p_1,...,p_s >= P_0` have product at least `P_0^s`, and this product divides
`M_F`.  Therefore `P_0^s <= M_F`, giving the logarithmic bound.  The displayed
height estimate follows by bounding every factor by `(2 ell')^{phi(N)}`.

This is not yet a full zone-(b) density theorem, because the all-pairs family
is enormous at prize scale.  It is the precise finite-prime budget that a
future density argument or adversarial prime search must beat.

## Verification

The verifier performs:

- exhaustive pair checks for `N=8`, `ell'=5`;
- a deterministic `20,000`-pair prefix for `N=16`, `ell'=9`;
- primes `p == 1 mod N` listed in the JSON artifact;
- both implications above;
- the height bound.
- the exact distinct-prime divisor budget and the height-based prime-count
  bound for the checked pair family.
- the Row-C graded collision-radius table above, including full injectivity
  at `N'=64`.
- the QA.14 cluster-certificate lemmas and toy replay.

Replay:

```bash
python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py
python3 experimental/scripts/verify_row_c_e1_collision_norm_criterion.py --emit
python3 -m py_compile experimental/scripts/verify_row_c_e1_collision_norm_criterion.py
```

The computation is intentionally small.  Its role is to pin down the algebraic
gate so future Row-C or zone-(b) work can search for many norm divisibilities
instead of treating collisions as unstructured random events.
