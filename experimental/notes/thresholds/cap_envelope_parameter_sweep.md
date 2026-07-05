# Cap Envelope Parameter Sweep

Status: PROVED.

Source DAG node: `cap_envelope_parameter_sweep`.

## Statement

The quotient-remainder floor used in the cap envelope is scale-free in the
quotient parameter `c`: its hypotheses depend on `(c, m, s, A0)`, not on the
printed convenience scale `N_rho = 1024`.  At full fiber `s = 0`, the only
box-like side condition is vacuous.  Therefore the floor can be replayed at
finer 2-power quotient scales.

Exact big-integer replay gives:

| rate | best `(c,d)` | `N` | net gain | required ledger gain | margin |
| --- | --- | ---: | ---: | ---: | ---: |
| 1/4 | `(2^25, 209)` | `2^16` | `81/128 = 0.6328125` | `0.367` | `+0.2658125` |
| 1/8 | `(2^21, 2251)` | `2^20` | `203/2048 = 0.09912109375` | `0.023` | `+0.07612109375` |
| 1/16 | `(2^28, 11)` | `2^13` | `3/8 = 0.375` | `0.304` | `+0.071` |

The rate-`1/8` template point `(c,d) = (2^28,17)` also replays and gives
`1/16 = 0.0625` grid steps.

## Proof

For each printed point, the replay certificate checks:

- `c | n`, `c | k`, `K = k + 1 < n`, `0 <= m <= N`, `A0 > k`, and `A0 <= n`;
- full-fiber `s = 0`, so `w_c(0, dc - 1) = d - 1`;
- the exact trigger

```text
binom(N, m) > 2^(256 d - e), where e = log2(k);
```

- maximality of `d` at the printed `c`;
- the exact grid-step gain

```text
gain = d * 2^step / N - 1.
```

The trigger is stronger than `L > (q-b)/k` under `q < 2^256`, so the computed
gains are conservative lower bounds for the floor.

## Consequence

The clean-rate cap-envelope deficits are covered by parameter optimization at
all three clean rates.  This is a finite arithmetic input for adjacent
threshold row packets and the corridor ledger.

## Non-Claims

This packet replays the sweep against the existing quotient-remainder floor
lemma.  It does not reprove that lemma, does not by itself close a deployed
adjacent row theorem, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_cap_envelope_parameter_sweep.py --emit
python3 experimental/scripts/verify_cap_envelope_parameter_sweep.py \
  --check experimental/data/certificates/cap-envelope-parameter-sweep/cap_envelope_parameter_sweep.json
```
