# M31 rank-seven effective-deficit one-pivot packet

This certificate banks a local theorem and a sharply scoped route cut.

The local theorem uses the fact that the normalized received table
`P/V` is nowhere zero on `E0`.  One agreement pivot reduces a
rank-at-most-seven linear flat to an affine rank-at-most-six flat, giving
the exact nested-floor cap

```text
H_Q(g) =
floor(
  R/(g-Q) *
  floor(
    binomial(R-g+w+6,6) / binomial(w-Q+6,6)
  )
).
```

The integer order is load-bearing:

```text
inner = numerator // denominator
H_Q   = R * inner // (g-Q)
```

The theorem pays every pure full-`G`, zero-anchored
rank-at-most-seven family for `217543 <= g <= 354972`.  Together with
the existing Johnson and endpoint payments, the remaining pure fixed-`G`
interval is exactly `72860 <= g <= 217542`.

The endpoint route cut constructs only an exact integer marginal:

- `Q*_H = 15186`;
- final bucket `1184`;
- 15,188-row histogram digest
  `7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0`;
- harmonic transport digest
  `c3b09d3958cd5b6ebc4c78c937e3f86e5a5d95d632c3be7db3c136efbde6bb79`.

It is not a source family, a common support layer, a full-gcd realization,
or a row closure.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank7_effective_deficit_one_pivot_route_cut_v1.py --check
python3 experimental/scripts/verify_m31_rank7_effective_deficit_one_pivot_route_cut_v1.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home sage experimental/scripts/verify_m31_rank7_effective_deficit_one_pivot_route_cut_v1.sage
python3 experimental/scripts/verify_m31_rank7_effective_deficit_one_pivot_route_cut_packet_v1.py
python3 experimental/scripts/verify_m31_rank7_effective_deficit_one_pivot_route_cut_packet_v1.py --tamper-selftest
```

The packet verifier reruns the primary verifier in normal and optimized
Python modes, replays the independent Sage implementation, checks all
source hashes, replays the sealed parent packet, and runs hostile JSON and
semantic mutation checks.

## Explicit nonclaims

- No v4 ledger atom or official row value moves.
- Rank seven is not globally closed.
- Rank at least eight is not addressed.
- Fixed-`H` uniqueness does not count the possible `H` locators.
- The exact-gcd subset of a deep fixed-`H` divisibility fiber is not
  asserted to be affine.
- Non-integrated PR #1073 is neither an owner nor a dependency.
- Balanced interlaced support layouts refute an automatic domain adapter;
  they are not source-compatible counterexamples.
