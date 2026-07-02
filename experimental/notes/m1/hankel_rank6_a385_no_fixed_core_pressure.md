# Hankel Rank-6 A385 No-Fixed-Core Pressure

Status: PROVED / AUDIT.

This note records the first obstruction profile after the fixed-core synthesis
at `A=385`.

The fixed-core synthesis proves that every separated rank-6 branch with a fixed
forced base-root core of size at least two is projective-budget safe.  Thus any
remaining separated over-budget branch must avoid a fixed two-point base core.
This note proves what such a survivor must still contain.

At `A=385`,

```text
j = 127,        m = 128,        h = 5.
```

The direction-rank degree cap gives at most six finite affine roots in a
rank-6 regular bucket.  Since the projective budget is also `6`, any projective
over-budget survivor must have exactly six distinct finite noncontained classes
and an unpaid projective endpoint.

The low-degree transfer represents each finite class by a nonzero polynomial

```text
deg Q < 5.
```

On the base support `X`, the transfer gives `L_Q(x)=0` exactly when `Q(x)=0`.
Hence each finite class has at most four base-support roots.  Across six finite
classes, the total base-root incidence is at most

```text
6 * 4 = 24.
```

Each split locator has degree `127`, so the six classes have at least

```text
6 * 127 - 24 = 738
```

external-root incidences in the complement `H \ X`, which has size

```text
512 - 128 = 384.
```

Distributing `738` incidences over `384` external points forces

```text
sum_{i<j} |E_i cap E_j| >= 738 - 384 = 354.
```

There are `binomial(6,2)=15` pairs of finite classes, so one pair satisfies

```text
|E_i cap E_j| >= ceil(354/15) = 24.
```

Thus any remaining separated `A=385` projective over-budget witness must have
a pair of finite split-locator classes sharing at least `24` external roots.
Equivalently, if every pair of finite classes has external common core at most
`23`, the no-fixed-core branch is projective-budget safe.

This is useful because it turns the vague no-fixed-core/moving-core frontier
into a concrete large pair-core target.  The next closure attempt can try to
show that such a pair-core is quotient-paid, forces product collapse, or is
incompatible with the separated Hankel low-degree transfer.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_no_fixed_core_pressure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-no-fixed-core-pressure/f17_32_n512_k256_m3_rank6_a385_no_fixed_core_pressure.json
```

Nonclaims:

```text
no closure of the no-fixed-core A=385 frontier;
no existence claim for a no-fixed-core over-budget witness;
no overlapping-support rank-6 classification;
no proof that the projective endpoint is unpaid;
no proof that a large external pair-core is quotient-paid or impossible;
no arbitrary A=385 rank-6 root table;
no row-level M3 safe-side bound.
```
