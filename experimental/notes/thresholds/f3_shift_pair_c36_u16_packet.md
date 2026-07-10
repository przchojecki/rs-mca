# F3 shift-pair control: C36' and the U16 compiler

Status: PROVED / CONDITIONAL / TARGET, by component.

This packet vendors the current prize-DAG F3/u1_x4 lane into the
CAP25-v13 terminology of **primitive shift-pair control**.  It is not a
paper edit and it does not claim the full SP input.  It records a compact
theorem chain for the direct-column active-core residue after quotient,
dihedral, moment-trade, U2-boundary, and DLI/skew cells have been stripped.

## Interface

Let `R_h` denote the stripped primitive active-core contribution of width
`h` in the direct-column convention consumed by the X4 exact-list split.  The
ground-truth band audit fixes the outer width range

```text
2 <= h <= H_max(row) = min(k+t, floor(n/2)).
```

The consumer arithmetic accepts

```text
R_post < 16 n^3.                                      (U16)
```

This is weaker than the old `R_post <= n^3` sufficient conjecture and matches
the current direct-column budget actually consumed by the finite X4 ledger.
The width partition is

```text
R_post = R_1 + R_2 + R_3 + sum_{h=4}^{H_max} R_h.
```

The packet separates the four payments:

```text
R_1 = 0,                                              PROVED
R_2 < n^3,                                            PROVED
R_3 < n^3,                                            CONDITIONAL on C36'
sum_{h=4}^{H_max} R_h <= 14 n^3.                      TARGET
```

Thus the open HGE4 aggregate gate plus the C36' h=3 premise imply `(U16)`.

## K6 h=2 Payment

For `H = mu_n <= F_p^*`, `n >= 8192`, `p >= n^2`, and nonzero shifts `u`, put

```text
C(u) = {x in H : x-u in H}.
```

If `U` is a set of nonzero shifts, no two in the same multiplicative
`H`-coset, the official-regime rich-coset Stepanov argument proves

```text
sum_{u in U} |C(u)| <= 6 (n |U|)^(2/3).              (K6)
```

The level-set compiler then gives

```text
E_+(H) <= 211 n^(5/2),
T_2 <= (211/8)n^(5/2) < n^3
```

for every official row `n = 2^s`, `13 <= s <= 41`.

## C36' h=3 Premise

For an official row, set

```text
A = (1-H) \ {0},
N_3to1(A) = #{(a1,a2,a3,a4) in A^4 : a1 a2 a3 = a4}.
```

The proposed red premise is

```text
N_3to1(A) < 36 n^2 - 16 n^(4/3) - n/2.              (C36')
```

The correction from `8 n^(4/3)` to `16 n^(4/3)` is load-bearing.  A fresh
audit found that the earlier trace-zero envelope
`A_3^0 <= binom(R,2)` is false at `(p,n)=(7937,64)`, where the pair-orbit
count is `2` but `binom(R,2)=1`.  The corrected envelope is

```text
A_3^0 <= 2 binom(R,2) + R = R^2 <= I^2/36 < (4/9)n^(4/3).
```

Together with

```text
A_3^nz <= N_3to1(A)/36,
T_3 <= n^2/72 + n(A_3^0 + A_3^nz),
```

the substitution gives

```text
T_3
 < n^2/72 + (4/9)n^(7/3)
   + (n/36)(36n^2 - 16n^(4/3) - n/2)
 = n^3.
```

The `n^(7/3)` terms cancel because `4/9 = 16/36`; the `n^2` terms cancel
because `1/72 = (1/2)/36`.

## Evidence And Nonclaims

The replay script verifies the small-row exact arithmetic behind the C36'
repair, including the explicit `(7937,64)` counterexample to the older
`binom(R,2)` envelope.  The prize-side Modal prefix sweep also found no C36'
falsifier among the first twelve official primes for `n=8192`; the worst row
had

```text
p = 67239937,
N_3to1 = 66933997,
N_3to1 / n^2 = 0.9973942786455154.
```

That sweep is evidence only and is not replayed here.

This packet does not prove the full primitive shift-pair ledger, the full
SP input of the frontiers paper, C36', or HGE4.  It contributes:

```text
PROVED:      K6 h=2 official-row payment;
PROVED:      corrected C36' -> h=3 direct-floor compiler;
PROVED:      U16 assembly arithmetic from h=1, h=2, h=3, HGE4;
TARGET:      C36' and HGE4 remain the two open leaves for this local lane.
```

## Replay

```bash
python3 experimental/scripts/verify_f3_shift_pair_c36_u16_packet.py
```

Expected digest:

```text
F3_SHIFT_PAIR_C36_U16_PACKET_PASS rows=29 h2_energy=211
```
