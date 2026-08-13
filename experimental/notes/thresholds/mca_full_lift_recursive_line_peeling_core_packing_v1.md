# Full-lift recursive line peeling and core packing

## Scope

This packet continues the Mersenne-31 full-lift support payment from the
boundary-line-bank wall `e=124806`.  It does not claim that the adjacent
failure is unsafe and does not close the full Mersenne row.

Use

```text
N=1048582, m=67454, K=6, c=5,
B=16777215, Q=N-m+1=981129.
```

## Residual recursion

After `r` affine lines have been removed and charged, let `Z_r` be the
remaining assigned slopes, let `U_r` be their deficit ceiling, and set

```text
T_r = B-rQ.
```

For a legal prefix cutoff `b`, the exact-layer direction-class bank gives

```text
|Z_r| <= C_r + sum_(i=1)^G_r |L_i|,
G_r = sum_(h=b+1)^U_r J_h,
C_r = P_b(e)+(U_r-b)-G_r.
```

If the residual is still unsafe, it forces one line of size

```text
lambda_r = ceil((T_r-C_r+1)/G_r).
```

For `lambda_r>=2`, total-core packing and the inside-support correction give

```text
g_r = max(0,ceil((lambda_r*m-N)/(lambda_r-1))),
u_r = max(g_r-c,0),
U_(r+1) = min(U_r,e-u_r+K-1).
```

Remove every assigned slope on that affine line and repeat.  The next
selected line is distinct even when `U_(r+1)=U_r`.

## Core-packing invariant

Write a peeled line as `c_gamma=a_i+gamma*b_i`.  Its common core is the set
where `(r_0,r_1)=(a_i,b_i)`.  For two distinct lines, at least one codeword
difference `a_i-a_j` and `b_i-b_j` is nonzero, so the two cores meet in at
most `K-1=5` coordinates.  Their inside cores all lie in the same
`e`-coordinate direction support.  Hence

```text
sum_i u_i-C(r,2)*5 <= e.
```

A strict violation contradicts unsafety.  Otherwise, if the recursion
lowers the residual ceiling into a defined suffix-minimum weighted prefix,
that prefix plus the peeled-line charges proves safety.

## Exact Mersenne interval

Start at cutoff `65304`.  If its first boundary layer fails a guard, use
the least legal cutoff plus two guard layers.  Exact replay checks every
prefix and line-bank guard and proves

```text
124806<=e<=130198.
```

The branch census is:

```text
paid supports:       5393
weighted prefix:     3837
core packing:        1556
direct line bank:       0
maximum peels:          5
line counts 1..5:    3534,397,1397,59,6
```

The first packing termination is `e=128340`:

```text
62822+66574-5 = 129391 > 128340.
```

At the last paid support `e=130198`, five forced lines give

```text
37718+33617+28204+20729+12942-10*5
  = 133160 > 130198.
```

At adjacent `e=130199`, nine legal peels only give packing lower bound
`126052`.  The next residual target is `7947054`, below base charge
`8154082`, so the pigeonhole numerator is nonpositive and cannot force
another line.  This is a method wall, not an unsafe certificate.  The
Mersenne residual becomes

```text
130199<=e<=1044241.
```

## Replay

```bash
python3 experimental/verify_mca_full_lift_recursive_line_peeling_core_packing_v1.py
python3 experimental/audit_mca_full_lift_recursive_line_peeling_core_packing_v1.py
cc -O2 -std=c11 -Wall -Wextra -Werror \
  experimental/verify_mca_full_lift_recursive_line_peeling_core_packing_v1.c \
  -o /tmp/verify_m31_recursive_line_peeling
/tmp/verify_m31_recursive_line_peeling
```
