# Step 5: carve the solved high-agreement region of the prize envelope

- **Status:** COMPLETE -- all five items implemented and passing (verifier exits 0:
  5 PASS / 0 PENDING). Closes `towards-prize.md` S1 step 5 ("use the compiler to carve
  out the solved high-agreement region").
- **Lane:** V (verification / packaging), independent of the M1/F1/L1 proof lanes.
- **Branch / PR:** `allen/step5-envelope-map`.
- **Script:** `experimental/scripts/verify_step5_envelope_carving.py`.

## The compiler being applied

For `C = RS[F, L, k]`, `n = |L|`, line/challenge field size `q = q_line`, set
`B_Q = floor(q / 2^128)` and `r = n - a`. The promoted tangent staircase gives the
exact value `LD_sw(C,a) = n-a+1 = r+1` whenever `r = n-a <= floor((n-k)/3)`, and the
target gate is `emca(C,delta) > 2^-128  <=>  LD_sw(C,a) >= B_Q + 1`. Therefore

```text
if  1 <= B_Q <= floor((n-k)/3)   then the grid threshold is pinned EXACTLY:
        r <= B_Q - 1  safe,   r = B_Q  unsafe
        (agreement a >= n - B_Q + 1 safe, a = n - B_Q first unsafe).
```

Rows meeting `1 <= B_Q <= floor((n-k)/3)` are the **solved high-agreement region**.

## Coverage

| # | item | status |
|---|------|--------|
| 1 | compiler formula + flagship anchor | **done** |
| 2 | solved-region boundary (`B_Q <= floor((n-k)/3)`) | **done** |
| 3 | multi-rate envelope grid (rho in {1/2,1/4,1/8,1/16}) | **done** |
| 4 | high-agreement scope vs the Johnson radius | **done** |
| 5 | emit the envelope-map artifact (table / JSON) | **done** |

### Verified so far

- **Flagship anchor.** `B_Q = floor(17^32/2^128) = 6 <= floor(256/3) = 85`, so the
  `F_17^32, n=512, k=256` row is solved and the compiler pins it to `a >= 507` safe,
  `a = 506` first unsafe -- matching the on-`main` board record `tangent506-exact-gate`.
- **Solved-region boundary.** The region is exactly `B_Q <= floor((n-k)/3)`: at
  `n=512, rho=1/2` (cap `85`), `B_Q=85` is solved, `B_Q=86` exits, and `B_Q=0`
  (`q <= 2^128`) means the compiler does not apply.
- **Multi-rate grid.** All four grand-challenge rates at `n=512, q=17^32` (`B_Q=6`) are
  solved, with caps `floor((n-k)/3) = 85, 128, 149, 160` for `rho = 1/2, 1/4, 1/8, 1/16`
  -- the cap GROWS as the rate drops, so lower-rate rows are solved with more room; the
  pinned threshold is `a >= 507` for all (fixed by `B_Q`). Each rate's solved boundary is
  exactly `B_Q <= cap` (`cap` in, `cap+1` out). A large row `n=2^20, rho=1/2` is also
  solved at this `q`, pinned at `a = n - B_Q + 1`.
- **High-agreement scope vs Johnson.** The pinned transition radius `~ B_Q/n` (`6/512 ~
  0.0117` here) is far **below** the Johnson radius `1 - sqrt(rho)` (`0.293, 0.500, 0.646,
  0.750` for the four rates). Verified by the exact integer inequality
  `B_Q/n < 1 - sqrt(k/n)  <=>  k*n < (n - B_Q)^2` (no floats in the assertion). This makes
  explicit that the carved region is the **easy** high-agreement slice; it does not touch
  the near-capacity band where the prize-determining content lives.
- **Envelope-map artifact.** A deterministic JSON map
  `experimental/data/step5-envelope-map/envelope_map.json` records the carved rows
  (the four rates at the flagship row, a large `n=2^20` row, and the solved/unsolved
  boundary rows) with `rho, n, q, B_Q, cap, solved, safe_min_agreement`. The check emits
  it, re-reads it, and recomputes every row via `solved_region` to confirm consistency
  (`6/7` rows solved; the `B_Q=86>cap` row is the deliberate unsolved control).

## Honest scope

The solved region is the **high-agreement** regime: the pinned threshold sits at radius
`~ B_Q / n` (e.g. `6/512 ~ 0.012` for the flagship), **far below** the Johnson radius
`1 - sqrt(rho)` and far from the near-capacity band where the prize-determining content
lives. This artifact carves the **easy** slice of the envelope and turns the compiler
into a concrete "which rows are solved" map; it does **not** resolve the hard
near-capacity content (the aperiodic local limit). No safety/threshold claim is made
beyond the promoted tangent theorem's exact-equality range `r <= floor((n-k)/3)`.

## Reproduce

```bash
python3 experimental/scripts/verify_step5_envelope_carving.py
```
