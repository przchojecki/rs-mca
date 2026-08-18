# MCA full-lift boundary line-bank absorption v1

## Status

PROVED / EXACT FINITE CALIBRATION / INTERVAL PAYMENT.

## Compiler

Fix a prefix cutoff `h0`. In every exact layer `h0<h<=min(H,m)`, the
normalized-direction Johnson theorem gives at most

```text
J_h=floor(e(A_h-c)/(A_h^2-e*c)),  A_h=2h-e,
```

direction classes. Each class and the layer anchor lie on one affine
explanation line. Padding with anchor-only slots gives the exact identity

```text
|D_h| = 1-J_h + sum_(j=1)^J_h |L_(h,j)|.
```

Together with the optional synchronized top line,

```text
|Z| <= C_e + sum_(i=1)^G_e |L_i|,
G_e = 1_(H<m) + sum_h J_h,
C_e = P_h0(e) + sum_h (1-J_h).
```

Thus unsafety at budget `B` forces one line to have at least

```text
lambda_e=ceil((B-C_e+1)/G_e)
```

members. Total-core packing and the existing core-absorption theorem put
every sufficiently high-deficit explanation on that line. One punctured
ordinary-Johnson cap pays the remainder. This compiler never closes a
direction class with an outside-core denominator.

## Official interval

For Mersenne-31, `h0=65272` pays

```text
101157<=e<=124805.
```

At the endpoint,

```text
prefix          =  1636955,
line groups     =    34560,
base charge     =  1604577,
forced line     =      440,
forced core     =    65220,
low list cap    =      126,
final bound     = 16706559,
slack           =    70656.
```

At adjacent `e=124806`, the same legal compiler gives `16831491`, above
budget by `54276`. This is a method wall, not an unsafe certificate. The
Mersenne residual interval is `124806<=e<=1044241`.

## Replay

```bash
python3 experimental/verify_mca_full_lift_boundary_line_bank_absorption_v1.py
python3 experimental/audit_mca_full_lift_boundary_line_bank_absorption_v1.py
cc -O2 -std=c11 -Wall -Wextra -Werror \
  experimental/verify_mca_full_lift_boundary_line_bank_absorption_v1.c \
  -o /tmp/verify_m31_line_bank
/tmp/verify_m31_line_bank
```

The C replay checks all `23,650` supports through the adjacent wall in
constant memory and fails closed on endpoint or branch-census drift.
