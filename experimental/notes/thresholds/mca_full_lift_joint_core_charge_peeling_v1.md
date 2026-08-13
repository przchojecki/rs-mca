# Full-lift joint-core charge peeling

## Scope

This packet strengthens the recursive Mersenne-31 affine-line peeling
route.  It pays `130199<=e<=130219`; it does not certify the adjacent row
unsafe or close the full Mersenne row.

## Joint core budget

For `r` distinct peeled parameterized explanation lines, let `g_i` be
their actual total common-core sizes and `I_i` their parts inside the fixed
`e`-coordinate gauged direction support.  Distinct codeword pairs give

```text
|I_i intersect I_j| <= c=K-1.
```

Each line direction is a nonzero degree-`<K` codeword, so each core has at
most `c` coordinates outside that support.  Pair noncontainment also gives
`g_i<=m-1`.  Hence

```text
sum_i g_i <= S_r := min(r(m-1),e+C(r+1,2)c).
```

## Convex line charge

Off-core agreement sets on a line are disjoint, so a line with core `g`
has at most

```text
f(g)=(N-g)/(m-g)=1+(N-m)/(m-g)
```

assigned slopes.  This function is increasing and convex.  Concentrating
the available core mass at endpoints gives, with

```text
q_r=floor(S_r/(m-1)), z_r=S_r-q_r(m-1), Q=N-m+1,
```

the joint charge

```text
L_r = rQ,                                            if q_r=r,
L_r = floor(q_r Q+f(z_r)+(r-q_r-1)f(0)),            otherwise.
```

Thus an unsafe residual after `r` peels has more than `B-L_r` slopes.  This
is often nearly a full `Q` stronger than the independent charge `B-rQ`.

## Exact interval

Using `B-L_r` in the proved recursive line bank pays all

```text
130199<=e<=130219.
```

All 21 supports terminate by positive inside-core packing.  The line-count
census is

```text
4:2, 5:10, 6:3, 7:2, 8:1, 10:1, 13:2.
```

At the endpoint the thresholds are `21,18,...,18`, and

```text
18393+12*9736-C(13,2)*5 = 134835 > 130219.
```

At adjacent `e=130220`, thresholds `20,16,...,16` for the first 43 lines
give only

```text
15811+42*2041-C(43,2)*5 = 97018.
```

The joint allowance at `r=43` is `134950=2(m-1)+44`, so the joint charge
jumps to `1962895` and the next threshold falls to `13`, with zero forced
core.  Later thresholds cannot increase.  This is a method wall, not an
unsafe certificate.  The residual is

```text
130220<=e<=1044241.
```

## Replay

```bash
python3 experimental/verify_mca_full_lift_joint_core_charge_peeling_v1.py
python3 experimental/audit_mca_full_lift_joint_core_charge_peeling_v1.py
cc -O2 -std=c11 -Wall -Wextra -Werror \
  experimental/verify_mca_full_lift_joint_core_charge_peeling_v1.c \
  -o /tmp/verify_m31_joint_charge
/tmp/verify_m31_joint_charge
```
