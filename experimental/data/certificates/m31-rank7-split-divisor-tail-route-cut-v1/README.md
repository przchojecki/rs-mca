# M31 rank-seven split-divisor tail route-cut certificate

This packet proves the source-bound cumulative deficit-head inequality

```text
N_{<=Q} <= floor(C(R-g+w+7,7) / C(w-Q+7,7))
```

for every residual rank-seven union size and every legal cutoff.  It then
exhausts all `282,545` residual `g` cells and constructs the sharp abstract
histogram allowed by all such head bounds.

That histogram survives every currently proved scalar slice, colored,
cross-block, affine-line, and codimension-one harmonic constraint.  The
narrowest exact harmonic integer-primal interval has width `122`.  An
explicit integer `q`-by-`b` transport checks the deficit and mismatch
marginals, including every row/column sum and placement inequality.  This
is a route cut: current scalar hypotheses do not close rank seven.

The packet also includes an exact positive-`w` source family over `GF(31)`:

```text
tail words:              7,864
lcm restorer:                1
total list size:         7,865
linear rank:                 7
agreement:                   8
deficit histogram:    h0=1, h1=7,864
```

Every full gcd is exact, the recovered-denominator lcm is the planted
polynomial, and there is no common planted zero.  This small-field family
proves that those algebraic gates alone cannot imply the missing tail
bound.  It is not a deployed M31 lower bound.

The exact remaining theorem is
`JOINT_HEAD_TAIL_FULL_GCD_INCIDENCE`.  Low residual union sizes additionally
need a stronger fixed-`G` ordinary-RS theorem or a genuine coexistence
refund.  No Grande Finale v4 atom, ledger value, or official endpoint moves.

The immediate sealed predecessor payload is:

```text
8135b49370b491cc14defb6c9e62648148fa2420a3d0cc45084ba00410eca239
```

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_v1.py --tamper-selftest
sage experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_v1.sage
python3 experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_packet_v1.py
python3 experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_packet_v1.py --tamper-selftest
```

To regenerate the canonical manifest after an intentional source change:

```bash
python3 experimental/scripts/verify_m31_rank7_split_divisor_tail_route_cut_packet_v1.py --write-manifest
```

Then rerun the full packet verifier and its tamper self-test.

## Interpretation

GREEN scope:

- the cumulative-head theorem;
- the exact all-`g` frontier arithmetic;
- the sharp scalar-histogram and joint-marginal route cut;
- the independent exact `GF(31)` source fixture.

Open scope:

- existence of the abstract extremal histogram on the deployed source;
- realization of the marginal transport by one common support layer,
  rank-six hyperplane, and received word;
- the high-`g` joint head-tail/full-gcd incidence;
- the low-`g` ordinary-RS or coexistence improvement;
- rank seven, all higher ranks, and the M31 LIST row.
