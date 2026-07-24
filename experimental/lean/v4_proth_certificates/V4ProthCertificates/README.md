# `v4_proth_certificates`

Kernel-checked replay of the deterministic Proth primality certificates for the
four smooth-domain rows printed in `experimental/proximity_prize_results_v4.tex`
(`tab:proth`, v4:185-188).

## Source binding

The certificates are not new. They are condition `PC1` of
`prop:proth-row-check` in `experimental/rs_mca_thresholds.tex` (lines
1857-1858), with per-row data in
`experimental/data/certificates/proth-rows/proth_rows.json`. This package
replays that data in the source's own notation `(u, s, a0)`, and its values were
independently rederived from the printed primes alone before the certificate
section was read; they agree in every field of every row.

## What is proved

Per row, by kernel-checked arithmetic:

| condition | statement |
|---|---|
| decomposition | `p = u * 2^s + 1` |
| oddness | `u % 2 = 1` |
| Proth size condition | `u < 2^s` |
| witness congruence | `a0 ^ ((p-1)/2) = p - 1 (mod p)` |
| printed budget (`PC2`) | `floor(p / 2^128) = B` |
| smooth subgroup | `2^n | p - 1` |

`ProthRow.check` bundles the six as one Boolean; `allRows_check` states that all
four rows pass together. Each condition is also available as a separate named
theorem (`row41_decomposition`, `row41_odd`, ...) so that a reader matching the
audit note against this source never has to unfold a conjunction.

## What is not proved

Proth's criterion itself — the implication from the four hypotheses to primality
— is classical and is cited, not formalized. `prop:proth-row-check` invokes the
same implication.

The `F_{n,k}` sign conditions and the `r_quad` / `r_rho` identification that
`prop:proth-row-check` also asserts are out of scope here; they are checked in
`experimental/notes/audits/proth_rows_certificate_audit.md`.

No row bound, list size, slope count, MCA statement, or payment is asserted.

## Controls

`modPow` is only useful if it distinguishes, so three controls are included:

- `row41_nonwitness` — `a = 2` is proved **not** to be a Proth witness for the
  rate-`1/2` row;
- `composite_control` — the composite `3 * 2^92 + 1`, of the same shape, has no
  witness among the 62 bases below 64;
- `modPow_small` — the modular-exponentiation routine agrees with `a^e % 97` for
  all `a, e < 12`.

## Replay

```bash
lake clean && lake build
```

Stdlib-only, no dependencies, clean build under one second. Every theorem is
proved by `native_decide`; the axiom census reports exactly one `native_decide`
axiom per theorem and no `sorryAx`.
