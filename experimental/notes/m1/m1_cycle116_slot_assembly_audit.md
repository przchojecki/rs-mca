# M1 Cycle116 Slot-Block Assembly Audit

Status: AUDIT / FINITE-MODEL-SLOT-ASSEMBLY-VERIFIED.

Date: 2026-06-24.

This note verifies the finite-field co-support geometry used by the Cycle116
fixed-jet bridge. It is narrower than the slot-identity replay: it checks that
the stated slot blocks assemble into a `113`-point co-support for every
seven-slot tuple.

## Assembly

Work in

```text
F0 = F_17[X] / (X^16 + X^8 + 3),
eta = 6 X^9,
D0 = <eta>, |D0| = 256.
```

Let

```text
H32 = <eta^8>, |H32| = 32.
```

The verifier checks that the eight cosets

```text
eta^t H32,  t = 0,...,7,
```

are pairwise disjoint and partition `D0`. The singleton `1` lies in the inactive
coset `eta^0 H32`.

For each seed `i=1,2,3` and shift `a mod 16`, define

```text
Y_{i,a} = { y in H32 : y^2 in {3^(a+e) : e in E_i} },
```

where

```text
E_1={0,1,2,3,5,11,12,13},
E_2={0,1,2,3,4,8,9,14},
E_3={0,1,2,4,5,7,11,14}.
```

Each `Y_{i,a}` has size `16`. Therefore each active slot block

```text
eta^t Y_{i,a},  t=1,...,7,
```

has size `16` and lies inside the active coset `eta^t H32`.

For a seven-slot tuple `T=((i_t,a_t))_{t=1}^7`, the co-support is

```text
J_T = {1} union union_{t=1}^7 eta^t Y_{i_t,a_t}.
```

Since the singleton lies in `eta^0 H32` and the seven slot blocks lie in the
seven pairwise disjoint active cosets, every tuple has

```text
|J_T| = 1 + 7*16 = 113.
```

No enumeration of all `48^7` tuples is needed for this size statement.

## Locator Decomposition

The same disjointness gives the locator factorization used by the fixed-jet
bridge:

```text
P_T(X) = prod_{a in J_T}(X-a)
       = (X-1) prod_{t=1}^7 R_{t,i_t,a_t}(X),
```

where

```text
R_{t,i,a}(X) = prod_{y in Y_{i,a}} (X - eta^t y).
```

The verifier checks this polynomial factorization on representative tuples in
the finite-field model. The all-tuple statement follows from the displayed
definition and the coset-disjoint assembly.

The fixed-jet and evaluation identities for the `336` possible slot blocks are
checked separately by:

```sh
python3 experimental/scripts/verify_m1_cycle116_slot_identities.py
```

## Reproducibility

Run:

```sh
python3 experimental/scripts/verify_m1_cycle116_slot_assembly.py
python3 experimental/scripts/verify_m1_cycle116_slot_assembly.py --json
```

The verifier is nonmutating. It checks the `D0` coset partition, singleton
placement, `48` slot choices, `336` active slot blocks, the `113` co-support
size formula, and representative locator products.

## Remaining Boundary

This audit verifies the internal finite assembly. For promotion beyond
conditional audit, a reviewer should still compare the external Cycle116 packet
or source statement against this exact co-support definition.
