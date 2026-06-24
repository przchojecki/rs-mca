# M1 Cycle120 Support-Wise MCA Bridge

Status: CONDITIONAL / AUDIT / LD-SW-TO-EPSILON-MCA-BRIDGE.

Date: 2026-06-24.

This note isolates the final definition-level implication in the M1 Cycle120
chain. The finite construction is phrased as a support-wise line lower bound

```text
LD_sw(RS[F_17^32,H,256],262) >= N,
N = 52,747,567,092.
```

The ABF-facing quantity is the normalized support-wise MCA error

```text
epsilon_mca(C,delta).
```

The bridge is short but load-bearing: if one fixed line `f1 + gamma f2` has
`M` distinct support-wise bad parameters, and every witness support has size at
least `a`, then for every `delta` with

```text
a >= ceil((1-delta)n)
```

one has

```text
epsilon_mca(C,delta) >= M / |F|.
```

This is exactly the definition in `tex/cs25_cap_v4.tex`: `epsilon_mca` maximizes
over fixed pairs `(f1,f2)` and samples the same line parameter uniformly from
the code field.

## Cycle120 Instance

For the current row

```text
C = RS[F_17^32,H,256],
|H| = 512,
delta = 125/256,
```

the closed support threshold is integral:

```text
ceil((1-delta)|H|)
  = ceil((131/256)512)
  = 262.
```

The Cycle116 smooth-lift statement gives support-wise agreement `262`, so the
finite bad parameters are already bad for the ABF closed threshold at
`delta=125/256`.

The denominator is the line/code field:

```text
|F_17^32| =
2367911594760467245844106297320951247361.
```

Thus the composed lower bound is

```text
epsilon_mca(RS[F_17^32,H,256],125/256)
  >= 52,747,567,092 / 17^32
  > 2^-128.
```

## Verifier

Run:

```sh
python3 experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py
python3 experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py --json
```

The verifier imports the current Cycle84 exact occupancy chain, Cycle116
field/lift contract, and Cycle120 gate arithmetic verifier. It checks that the
same numerator, same line-field denominator, same closed threshold, and same
agreement count are used on both sides of the bridge.

## Remaining Boundaries

This bridge does not remove the source/audit gates already recorded in the
end-to-end chain:

```text
official ABF PDF/source verification for the row gates and Definition 4.3;
reviewer acceptance of the Cycle84 generated source contract;
reviewer acceptance that the compact external Cycle116 contract faithfully
  records the hash-pinned PR #96 files.
```

It only removes a possible notation gap: the finite `LD_sw` statement now has
an explicit executable conversion to the `epsilon_mca` lower bound used in the
Cycle120 counterexample claim.
