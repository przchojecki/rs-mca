# Full-lift lower-aware joint-core charge

## Scope

This packet strengthens the recursive Mersenne-31 affine-line peeling
charge by retaining every forced total-core lower bound.  It pays
`e=130220,130221`; it does not certify the adjacent row unsafe or close the
full Mersenne row.

## Majorization envelope

For `r` previously peeled lines, let `g_i` be the actual total-core sizes
and `ell_i<=g_i` the lower bounds forced when those lines were selected.
The preceding joint-core theorem gives

```text
0<=ell_i<=g_i<=m-1,
sum_i g_i<=S_r:=min(r(m-1),e+C(r+1,2)c).
```

Sort the lower bounds decreasingly.  Starting from that vector, spend all
available excess `S_r-sum ell_i` by filling the first coordinate to `m-1`,
then the second, and so on; call the result `x`.  Since

```text
f(g)=(N-g)/(m-g)=1+(N-m)/(m-g)
```

is increasing and convex, an exchange from a smaller nonterminal coordinate
to a larger one cannot reduce the sum.  Therefore

```text
sum_i f(g_i) <= sum_i f(x_i).
```

The floor of the right side is a valid charge for the removed lines.  Unlike
the preceding endpoint envelope, it cannot erase already forced lower bounds
by moving their mass to unrelated coordinates.

## Exact payment

At both new supports, 37 removed lines have lower-bound runs

```text
15816*4, 2046*33.
```

The maximizing allocations and charges are

```text
e=130220: 18769,15816*3,2046*33; S_37=133735; charge=609,
e=130221: 18770,15816*3,2046*33; S_37=133736; charge=609.
```

One final threshold `20` is forced.  The 38 inside-core lower bounds then
have runs `15811*5,2041*33`, and

```text
5*15811+33*2041-C(38,2)*5 = 142893 > e.
```

At adjacent `e=130222`, the compiler reaches 288 removed lines.  Its
maximizing allocation is `67453*5,1037,0*282`, with charge `4910044`.
The target `11867171` is below the certified base `12148280`, so the line
bank no longer forces another line.  This is a method wall, not an unsafe
certificate.  The residual is

```text
130222<=e<=1044241.
```

## Replay

```bash
python3 experimental/verify_mca_full_lift_lower_aware_joint_core_charge_v1.py
python3 experimental/audit_mca_full_lift_lower_aware_joint_core_charge_v1.py
```
