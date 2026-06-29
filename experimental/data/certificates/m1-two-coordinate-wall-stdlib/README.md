# M1 two-coordinate wall: stdlib scan certificate

Deterministic certificate for `experimental/scripts/search_m1_two_coordinate_wall_stdlib.py`,
a pure-stdlib (no numpy) reimplementation + extension of the slack-two depth-two
M1 two-coordinate Kummer-wall scan (`search_m1_remaining_two_coordinate_wall.py`).
See `experimental/notes/m1/m1_two_coordinate_wall_stdlib_extension.md`.

## What the certificate pins

- **Exact reproduction of the published numpy scan** — asymmetric-nonresonant
  grid `nonres, p<=500, e<=24`: `453` cases, `596304` scanned tuples, `0`
  violations of `4p`, max ratio `3.2173609608`; diagonal grid `n=20, p<=500`:
  max `3.9771715522` at `(421,21)`.
- **Two independently (direct `O(p^2)` summation) cross-checked datapoints** —
  published max `(197,14,(6,1,0,17)) -> 3.2173609608`, and the new extension max
  `(601,20,(4,7,0,1)) -> 3.3516589468`.

## Reproduce

```sh
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py --selftest
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py --check \
  experimental/data/certificates/m1-two-coordinate-wall-stdlib/m1_two_coordinate_wall_certificate.json
```

`--check` reruns the report/diagonal grids and the datapoints and compares the
rendered JSON byte-for-byte (exit 0 on match). Status `EXPERIMENTAL` (finite
numerical evidence, not a proof of the `4p` bound).

## Headline finding

Extending the asymmetric-nonresonant scan past the published `p<=500` grid finds
a **new empirical maximum `3.3516589468` at `(p=601, e=20, (4,7,0,1))`** — above
the previously published `3.2173609608` — with still `0` violations of `4p`
across `p<=1500`. So the prior maximum was not the supremum; any conjectured
constant in `(3.2173609608, 3.3516589468)` is refuted, while `|S| <= 4p` holds
throughout the extended grid.
