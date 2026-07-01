# F17^32 M3 One-Spike Projective-Infinity Witness

Status: PROVED.

This directory records an explicit split-locator witness for the projective
infinity endpoint of the one-spike family in the M3 regular window.

For each exact agreement, let `j=512-A`.  The one-spike family has base support
`X_A={x_0,...,x_j}` and spike `y_A=x_{j+1}`.  The witness locator is the monic
degree-`j` polynomial with roots

```text
y_A, x_0, x_1, ..., x_{j-2}.
```

It splits over the descriptor domain.  Since the spike is a root,
`H(v)ell=0`.  Since only the last two base nodes survive in `H(u)ell`, the
first two rows form an invertible two-node Vandermonde system with nonzero
weights, so `H(u)ell != 0`.

Thus the M5 projective-infinity chart is not merely bounded by one point: the
endpoint `[0:1]` is actually present for this synthetic family.

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_projective_witness.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/f17_32_n512_k256_m3_one_spike_projective_witness.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/f17_32_n512_k256_m3_one_spike_projective_witness.json
```
