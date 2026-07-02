# Adjacency Staircase Localization

Status: PROVED / COMPILER-ARITHMETIC.

This note packages three required-path DAG nodes as a small theorem cluster:

```text
crossing_localization
staircase_steepness
list_crossing_localization
```

It is intentionally row-independent.  It does not certify a new safe radius,
unsafe radius, or leaderboard row.  Its purpose is to make the final threshold
step exact: once a row-specific packet gives numerator bounds at a short list
of agreements, the prize threshold is an integer staircase problem with a
unique adjacent transition, except for explicit all-safe or all-unsafe edge
cases.

The companion verifier is:

```text
python3 experimental/scripts/verify_adjacency_staircase_localization.py
```

The emitted arithmetic certificate is:

```text
experimental/data/certificates/adjacency-staircase-localization/adjacency_staircase_localization.json
```

## Convention Block

```text
object:              abstract numerator staircase, with MCA and list consumers
agreement:           integer a
closed radius:       r = n - a on the MCA side
MCA denominator:     q_line, or the printed projective/curve sampler denominator
list denominator:    q_chal or the printed list challenge denominator
target:              epsilon*
integer budget:      B_* = floor(epsilon* denominator)
endpoint convention: closed integer balls; real supremum stated separately
```

For the Proximity Prize target `epsilon* = 2^-128`, an integer numerator `N`
is safe exactly when

```text
N <= floor(denominator / 2^128).
```

The denominator must be printed by any consumer packet.  This note never
identifies `q_gen`, `q_line`, and `q_chal`.

## Theorem 1: Nonincreasing Numerator Staircase

Let `I = {a_min, a_min+1, ..., a_max}` and let

```text
N : I -> Z_{\ge 0}
```

be nonincreasing in `a`.  Fix an integer budget `B_*`.  Define an agreement to
be safe if `N(a) <= B_*` and unsafe if `N(a) > B_*`.

Exactly one of the following holds.

```text
ALL_SAFE:    every a in I is safe;
ALL_UNSAFE:  every a in I is unsafe;
INTERIOR:    there is a unique a_* in I with
             N(a_*-1) > B_* >= N(a_*),
             where a_*-1 is also in I.
```

In the interior case the safe set is the upper interval

```text
{a in I : a >= a_*},
```

and the unsafe set is the lower interval

```text
{a in I : a < a_*}.
```

For MCA, take `N(a)=B_mca(a)`.  If `a_*` is the first safe agreement, then
`a_*-1` is the last unsafe agreement.  The largest safe closed integer radius
is `n-a_*`, the first unsafe closed integer radius is `n-a_*+1`, and the real
closed-ball safe interval has supremum `(n-a_*+1)/n`, not attained at the
unsafe endpoint.

Proof.  Since `N` is nonincreasing, the predicate `N(a) <= B_*` is monotone
nondecreasing in `a`.  Therefore its true set is either empty, all of `I`, or
an upper interval with a unique first element `a_*`.  The displayed adjacent
inequality is exactly the definition of that first element.

This is the precise version of the DAG shorthand "the adjacent crossing
exists unconditionally".  The unconditional statement is the three-way
classification above; an interior adjacent crossing requires at least one
safe and one unsafe grid point.

## Theorem 2: Corridor From Lower And Upper Certificates

Let `L(a) <= N(a) <= U(a)` be certified lower and upper bounds for the same
nonincreasing numerator staircase.  Define

```text
A_unsafe = {a in I : L(a) > B_*},
A_safe   = {a in I : U(a) <= B_*}.
```

Every interior first-safe agreement `a_*` lies in the explicit corridor

```text
1 + max A_unsafe  <=  a_*  <=  min A_safe,
```

with the conventions `1 + max empty = a_min` and `min empty = a_max`.

Proof.  If `L(a) > B_*`, then `N(a) > B_*`, so the first safe agreement is
strictly larger than `a`.  If `U(a) <= B_*`, then `N(a) <= B_*`, so the first
safe agreement is at most `a`.  Taking the strongest certified unsafe and safe
agreements gives the displayed interval.

Thus a safe handle and an unsafe handle reduce the prize-facing endgame to a
finite list of candidate agreements.  If the corridor length is `0`, the row
is adjacent-pinned.  If the corridor has length `2` or `3`, only those
pointwise numerator decisions remain.

## Theorem 3: Coarse Steepness Envelope

Let `M(a)>0` be a positive model count on a consecutive agreement interval,
and suppose a consumer has proved a relative envelope

```text
M(a)/E <= N(a) <= E M(a)        with E >= 1.
```

Suppose also that consecutive model counts are separated by

```text
M(a) / M(a+1) > E^2.
```

Then the ambiguity intervals

```text
[M(a)/E, E M(a)]
```

are pairwise disjoint for consecutive `a`.  Consequently a fixed budget `B_*`
can lie in at most one such ambiguity interval.  At every other agreement,
the sign of `N(a)-B_*` is certified by the coarse envelope:

```text
M(a)/E > B_*      implies N(a) > B_*,
E M(a) <= B_*     implies N(a) <= B_*.
```

Proof.  The separation condition gives

```text
M(a)/E > E M(a+1).
```

So the upper end of the `a+1` ambiguity interval is strictly below the lower
end of the `a` ambiguity interval.  The sign implications are immediate from
the lower and upper envelope bounds.

This is the conservative form of the DAG node `staircase_steepness`.  In
typical leading strata, increasing the exact-agreement parameter changes the
linear-system surplus `t` by one, and model counts have shape comparable to

```text
combinatorial_prefactor(a) * q^(1-t(a)).
```

If the prefactor ratio is bounded by `K`, the consecutive model ratio is at
least `q/K`.  Any relative proof with `E^2 < q/K` then leaves at most one
knife-edge candidate in that stratum.  The consumer must supply the actual
model, prefactor bound, and envelope; this note supplies only the compiler
arithmetic.

## Theorem 4: List Staircase

Let `L_m(r)` be the worst-case list numerator at integer radius `r` for a
fixed row and interleaving/list arity `m`:

```text
L_m(r) = sup_U |Lambda_m(U,r)|.
```

Then `L_m(r)` is nondecreasing in `r`.  Therefore the safe radii

```text
{r : L_m(r) <= B_*}
```

form a lower interval.  Exactly one of the following holds:

```text
ALL_SAFE:    every tested radius is safe;
ALL_UNSAFE:  every tested radius is unsafe;
INTERIOR:    there is a unique adjacent pair r_safe, r_safe+1 with
             L_m(r_safe) <= B_* < L_m(r_safe+1).
```

Equivalently, in agreement coordinates `a=n-r`, the numerator
`N_list(a):=L_m(n-a)` is nonincreasing and Theorem 1 applies verbatim.

Proof.  If a codeword is within radius `r` of a received word, then it is also
within every larger radius.  Hence each list is nested as `r` increases, and
so is the supremum over words.

## Consumer Map

This note discharges the elementary proof obligations in the following DAG
nodes, with the edge-case correction above.

```text
crossing_localization       -> PROVED as Theorems 1 and 2
staircase_steepness         -> PROVED as the envelope compiler, Theorem 3
list_crossing_localization  -> PROVED as Theorem 4
```

It does not discharge `list_planted_arithmetic`: that node needs the exact
planted-count formula and its Diophantine comparison against the printed list
denominator.

## Non-Claims

This note does not prove any row-specific aperiodic upper bound, M5
underdetermined packet, sparse residual bound, or list image-fiber theorem.
It is useful only after a consumer supplies theorem-backed or packet-backed
upper and lower numerators at candidate agreements.
