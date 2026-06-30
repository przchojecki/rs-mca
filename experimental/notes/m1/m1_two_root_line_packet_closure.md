# M1 two-root line-packet closure

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts a compact two-root line-packet closure from the broad
same-slope packet in PR #138.  It complements the already-integrated
`m1_hankel_variable_line_packet_lemma.md`: after fixed-root and full-plane
charges, the only residual affine line packets are fixed-sum and nondegenerate
product-Mobius packets, and in the `t=2` Hankel setting they cannot be
constant-slope residuals.

## Scope and non-claims

This is local algebra in the `t=2` Hankel-pencil normal form.  It does not
prove the all-line M1 aperiodic local limit, does not bound the global
residual slope image, and does not add a leaderboard or threshold row.

Field ledger: the statement is over an arbitrary field `F`.  In an MCA
application the slopes are finite line slopes in `q_line`.  No generated-field,
challenge-field, denominator, or radius endpoint convention enters this local
step.  Domain-root, split-root, quotient-periodic, contained/tangent, and
noncontainment filters remain external filters.

## Two-root line classification

Fix a `(j-2)` core `R`.  A two-root extension through `R` is represented by

```text
T = R union {x,y},        s=x+y,        p=xy.
```

Let

```text
A s + B p + C = 0,        (A,B) != (0,0),
```

be an affine line in the elementary `(s,p)` plane.

If `B=0`, then the line is fixed-sum:

```text
x+y=s_0,        s_0=-C/A,
```

with involution

```text
x |-> s_0-x.
```

If `B != 0`, put

```text
c=-A/B,        beta=-C/B,        mu=c^2+beta.
```

Then the line equation is equivalent to

```text
(x-c)(y-c)=mu.
```

If `mu=0`, every split pair on the line contains the fixed root `c`; this is a
fixed-root line and is charged to the lower root-slice ledger through
`R union {c}`.  If `mu != 0`, the line is a product-Mobius packet with
involution

```text
x |-> c + mu/(x-c).
```

Thus, after full two-root planes and fixed-root lines have been charged, the
only residual non-fixed line packets are fixed-sum packets and nondegenerate
product-Mobius packets.  These are exactly the two models used in
`m1_hankel_variable_line_packet_lemma.md`.

## Mixed boundary trace

The same normal form controls escaped-root traces.  Let `D` be the evaluation
domain, and let

```text
Trace_off(L,R)
 = { (beta,y) in (F\D) x (D\R) : (beta+y,beta y) in L }.
```

If `L` is fixed-sum `x+y=s_0`, then

```text
beta=s_0-y.                                      (FS-OFF)
```

If `L` is nondegenerate product-Mobius `(x-c)(y-c)=mu`, `mu != 0`, then

```text
beta=c+mu/(y-c).                                (PM-OFF)
```

Thus the mixed boundary trace of every surviving non-fixed line packet is the
graph of the same involution used by the all-domain packet, restricted to
domain roots whose partner escapes `D`.  In particular each such line has at
most `|D\R|=n-j+2` mixed boundary pairs.

## Constant-slope collapse

Now assume the `t=2` Hankel setting.  Fix a finite slope `z` and put
`w_z=u+zv`.  Let the shifted scalar landing rows through the `(j-2)` core be

```text
d_i = row_i(H_{4,j-2}(w_z)ell_R),        0 <= i <= 3.
```

For the two-root locator

```text
ell_{T_{s,p}} = (X^2-sX+p)ell_R,
```

the killed equation is

```text
H_{2,j}(w_z)ell_{T_{s,p}}
 =
 (d_2-sd_1+pd_0,  d_3-sd_2+pd_1).                (TLIN)
```

### Fixed-sum collapse

On a fixed-sum line `s=s_0`, if `(TLIN)` vanishes identically as a function of
the free coordinate `p`, then

```text
(d_0,d_1)=0,        (d_2,d_3)=s_0(d_1,d_2).
```

The Hankel overlap forces

```text
d_0=d_1=d_2=d_3=0.
```

Hence

```text
H_{4,j-2}(w_z)ell_R=0.
```

So a constant-slope fixed-sum packet is already charged to the full-plane
`(t+2,j-2)` Hankel lift.

### Product-Mobius collapse

On a nondegenerate product-Mobius line

```text
(x-c)(y-c)=mu,        mu != 0,
```

equivalently

```text
p=cs-c^2+mu,
```

if `(TLIN)` vanishes identically as a function of `s`, then

```text
(d_1,d_2)=c(d_0,d_1),
(d_2,d_3)=(c^2-mu)(d_0,d_1).
```

The first relation gives `d_1=cd_0` and `d_2=c^2d_0`; comparing with the first
coordinate of the second relation gives `mu d_0=0`.  Since `mu != 0`, all four
`d_i` vanish, and again

```text
H_{4,j-2}(w_z)ell_R=0.
```

Therefore, after full planes and fixed-root lines have been charged, no
surviving fixed-sum or nondegenerate product-Mobius packet is killed at one
finite slope.

## Consequence for the variable-line packet lemma

If two distinct points of a surviving non-fixed line packet had the same finite
slope `z`, then the affine-linear restriction `(TLIN)` would vanish at two
distinct line parameters and hence vanish identically on the line.  The
constant-slope collapse above would charge the packet to the full-plane lift,
contradicting survival.

Thus the active finite-slope map on every surviving non-fixed line packet is
injective.  Consequently the variable-line packet inequality in
`m1_hankel_variable_line_packet_lemma.md` applies after fixed-root and
full-plane charges without an extra variable-slope hypothesis.

## Verification

The companion verifier checks the affine-line classification, mixed boundary
trace formulas, fixed-sum and product-Mobius constant-slope collapses, and the
same-slope injectivity consequence over exact small finite fields:

```sh
python3 experimental/scripts/verify_m1_two_root_line_packet_closure.py
```
