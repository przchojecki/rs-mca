# MCA full-lift fixed-cutoff boundary stack v1

## Status

PROVED / EXACT FINITE CALIBRATION / INTERVAL PAYMENT.

## Compiler

Fix `h0<H=e-floor((e-K)/3)-1`. Use the independently truncated punctured
Johnson/mean-centered prefix `P_h0(e)` below it. For every exact layer
`h0<h<=H`, put

```text
A_h=2h-e,
J_h=floor(e(A_h-c)/(A_h^2-e*c)),
Q_h=floor((N-e-c)/(m-h-c)),
D_h=1+J_h(Q_h-1).
```

Under `2h>e`, `A_h^2>e*c`, and `N-e>m-h>c`, the normalized-direction
Johnson count permits at most `J_h` classes. Every class and a repeated
anchor lie on one nonzero affine codeword line, and outside-core packing
caps that line by `Q_h`. Thus

```text
|Z|<=F_e+|T|,
F_e=P_h0(e)+sum_(h=h0+1)^H D_h,
```

where `T` is the synchronized top line.

If `F_e+(N-m+1)<=B`, this pays directly. Otherwise unsafety forces
`L_e=B-F_e+1` top members and common core

```text
g_e=ceil((L_e*m-N)/(L_e-1)).
```

At least `u_e=g_e-c` core coordinates lie inside the gauged direction
support. Two top anchors absorb every assigned explanation of deficit at
least `a_e=e-u_e+K` into the same line. One punctured ordinary-Johnson cap
`M_e` at outside agreement `m-a_e+1` pays the lower explanations whenever

```text
e*M_e+(N-m+1)<=B.
```

## Official interval

At Mersenne-31, the fixed cutoff `h0=65200` pays

```text
98232<=e<=101155.
```

The direct branch ends at `e=101149`; the final six supports use absorption.
At `e=101155`,

```text
F_e            = 16667033,
L_e            =   110183,
g_e            =    67446,
M_e            =       28,
final bound    =  3813469,
slack          = 12963746.
```

At adjacent `e=101156`, the fixed-cutoff charge is `16951223`, above budget
by `174008`. This is a method wall, not an unsafe certificate. The Mersenne
full-lift residual interval becomes `101156<=e<=1044241`.

## Replay

```bash
python3 experimental/verify_mca_full_lift_fixed_cutoff_boundary_stack_v1.py
cc -O2 -std=c11 -Wall -Wextra -Werror \
  experimental/verify_mca_full_lift_fixed_cutoff_boundary_stack_v1.c \
  -o /tmp/verify_m31_boundary_stack
/tmp/verify_m31_boundary_stack
```

The C replay checks all 2,925 rows from `98232` through the adjacent wall.
