# F17^32 M3 Support-Uniform One-Spike Theorem

Status: PROVED.

This directory records a support-and-weight uniform version of the one-spike
packet in the M3 regular window.

For every `385 <= A <= 426`, let `j=512-A`.  Choose any support
`X subset D` with `|X|=j+1`, any spike `y in D \ X`, and any nonzero weights.
Set

```text
u_m = sum_{x in X} a_x x^m,
v_m = b_y y^m.
```

Then the full overdetermined Hankel matrix has rank `j+1` at every finite
slope, even after scalar extension.  Hence the v10 canonical finite root table
is empty.

At projective infinity, the split locator with roots at `y` and all but two
base nodes proves that the endpoint `[0:1]` is present.  Therefore this whole
family has finite numerator `0` and exact projective numerator `1`, safely below
the printed `2^-128` budget `6`.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_uniform.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-uniform/f17_32_n512_k256_m3_one_spike_uniform.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_uniform.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-uniform/f17_32_n512_k256_m3_one_spike_uniform.json
```
