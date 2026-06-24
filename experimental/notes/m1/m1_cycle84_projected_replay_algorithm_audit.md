# M1 Cycle84 Projected Replay Algorithm Audit

Status: PROVED / AUDIT / FINITE-MODEL-ALGORITHM.

Date: 2026-06-24.

This note audits the algorithm used by
`experimental/scripts/verify_m1_cycle84_projected_census_shard_replay.py`.
The audit is about the replay algorithm, not about the ABF source gate. It
explains why the generated C++ census is an exact enumeration of the projected
tau-folded duplicate bins once the current `slot_logs.json` certificate is
accepted.

## Objects

Let `M=(17^16-1)/3`. The projected log table gives, for each slot
`t=0,...,6` and slot key `k=0,...,47`, a projected log

```text
L_t(k) in Z/MZ
```

and a color `c_t(k) in Z/16Z`. The tau map on slot keys is a fixed-point-free
involution and each slot has constant tau log sum:

```text
L_t(k) + L_t(tau k) = K_t.
```

The total tau constant is

```text
kappa = K_0 + ... + K_6.
```

The two fixed projected roots are `S0,S1`, with

```text
2 S0 = 2 S1 = kappa mod M,
S1 = S0 + M/2.
```

The replay chooses the oriented half-domain by requiring the first slot key to
be the smaller key in its tau pair:

```text
H = { k : k < tau(k) }, |H| = 24.
```

Every non-fixed projected tau orbit has exactly one representative whose first
slot lies in `H`.

## Five-Two Split

The full oriented color shell is

```text
Omega = { (k_0,...,k_6) :
          k_0 in H,
          c_0(k_0)+...+c_6(k_6)=4 mod 16 }.
```

The replay splits a tuple into a five-slot prefix and two-slot suffix. For each
prefix it stores

```text
B = L_0(k_0)+...+L_4(k_4) mod M,
C = c_0(k_0)+...+c_4(k_4) mod 16,
```

in the sorted bucket `base[C]`. For each suffix it computes

```text
D = L_5(k_5)+L_6(k_6) mod M,
E = c_5(k_5)+c_6(k_6) mod 16.
```

The color equation is then exactly

```text
C = 4 - E mod 16.
```

Therefore the nested loop over suffixes and `base[4-E]` enumerates every tuple
in `Omega` exactly once. The generated C++ also checks that each five-slot
same-color bucket has no repeated projected log; this is a local injectivity
guard for the compressed sorted table.

## Shards And Circular Slices

For a total projected log

```text
X = B + D mod M,
```

write

```text
z = X - S0 mod M,
r = min(z, M-z).
```

The non-fixed canonical interval is `0 <= r < M/2`; the boundary `r=M/2`
corresponds to the second fixed root `S1` and is checked separately. A shard
`s=0,...,S-1` covers the half-open interval

```text
[ floor((M/2)s/S), floor((M/2)(s+1)/S) ).
```

For a fixed suffix log `D`, the condition that `B+D` falls in a shard is
equivalent to either

```text
B in S0-D + [lo,hi)           mod M
```

or

```text
B in S0-D + [M-hi+1,M-lo+1)   mod M.
```

The `+1` terms are the integer half-open form of `z=M-r` for
`r in [lo,hi)`. The helper `circular_slice` returns exactly the elements of a
sorted bucket in such a translated modular interval, splitting into two sorted
ranges when the interval wraps around `M`.

Thus, across all shards, the replay visits every non-fixed oriented tuple in
`Omega` exactly once and records it under its canonical key `r`.

## Duplicate And Energy Accounting

Within one shard, the generated C++ inserts canonical keys into an open-addressed
hash table. On the first occurrence of a key it stores the key but records no
duplicate. On the second occurrence it creates a duplicate counter with value
`1`, then increments by one on each further occurrence. If a key has final
multiplicity `m`, the accumulated ordered off-diagonal energy is

```text
2(1+...+(m-1)) = m(m-1).
```

The final duplicate list stores every key with multiplicity at least `2`. Shard
intervals are disjoint, so a non-fixed canonical key belongs to exactly one
shard. Parallel execution is therefore a disjoint union over shards; atomics sum
the entries and energy, and a mutex only merges per-shard duplicate summaries.

## Mechanical Audit

The companion verifier

```text
python3 experimental/scripts/verify_m1_cycle84_projected_replay_algorithm.py
```

checks:

1. `circular_slice` against brute force over many translated modular intervals.
2. canonical shard partitioning, including the `M-hi+1` second branch.
3. the five-two replay against brute-force enumeration on deterministic toy
   models with tau-pair log sums, colors, fixed-root accounting, and nontrivial
   duplicate bins.
4. the generated-source contract for the Cycle84 C++ source at `--threads 16`,
   including the exact SHA256, injected tables, tau guards, five-two split,
   shard intervals, canonical key, duplicate-energy accounting, and JSON output
   fields.

The generated-source contract is checked separately by

```text
python3 experimental/scripts/verify_m1_cycle84_generated_replay_source.py
```

The full Cycle84 run is still recorded separately by
`projected_census_full_replay_receipt.json`. This note audits the algorithmic
shape of that replay and ties it to the generated source contract. A reviewer
still has to decide whether this contract is enough for promotion beyond
`AUDIT / CONDITIONAL`.
