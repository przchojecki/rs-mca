# Independent Replay of the Four Certified Proth Prime Rows

- **Status:** AUDIT — confirmation only. **No new claim is made and nothing is
  closed.** The theorem and the certificate are the maintainer's.
- **Agent/model:** Claude Opus 5 acting for AllenGrahamHart.
- **Serves:** submission-package item (3) of `proximity_prize_results_v4.tex` —
  *"a reproducibility dossier containing literal row manifests, primality
  certificates, source pins, exact replays, and formal correspondence files."*
- **Artifact:** `experimental/scripts/verify_proth_rows_independent_replay.py`
  (stdlib only, exact integers, no floats; four mutation controls, all caught).
- **Upstream target commit:** `b13de811`.

## What "independent" means here

The replay reads only `p, n, k, s, u` and the Proth witness `a0` out of
`proth_rows.json`. Everything else — `B`, `B*`, `F_{n,k}(B-1)`, `F_{n,k}(B)`, the
sign conditions, `r_quad`, and the compiler-window bound — is **recomputed from
those integers** and only then compared with the packet's recorded values. A replay
that read the derived quantities back out of the certificate would confirm nothing.

## Checks, per row

| tag | check |
|---|---|
| PC1 | `p = u·2^s + 1`, `u` odd, `u < 2^s`, and `a0^((p-1)/2) ≡ -1 (mod p)` — Proth |
| PC2 | `n │ p-1`, `p < 2^256`, `B·2^128 ≤ p < (B+1)·2^128`, remainder in `(0, 2^128)` |
| B | `B = floor(p/2^128)` recomputed, and `B = B*` (full-field affine sampler, `\|Γ\| = \|F_p\| = p`) |
| SGN | `F_{n,k}(B-1) ≥ 0 > F_{n,k}(B)`, `F_{n,k}(r) = r² - 3nr + n(n-k)` |
| RQ | `r_quad = B-1`, located by SGN |
| CW | compiler window `1 ≤ B ≤ min(r_rho+1, n-k-1)` |

All four rows pass every check, with `F` values matching the recorded
`F_B_minus_1` / `F_B` digit-for-digit.

## The load-bearing caveat, reproduced

The packet records:

> `r_quad` must be located by the `F`-sign condition, **not** by
> `floor((3n - isqrt(n(5n+4k)))/2)`: a naive integer-sqrt evaluation of the printed
> closed form overshoots by 1 for `rho ∈ {1/2, 1/4, 1/8}` (correct only for `1/16`).

This replay evaluates the naive closed form independently and reproduces the
overshoot pattern **exactly**:

```text
rate 1/2  : naive - r_quad = 1
rate 1/4  : naive - r_quad = 1
rate 1/8  : naive - r_quad = 1
rate 1/16 : naive - r_quad = 0
```

Worth stating plainly: this is not a cosmetic note. An independent replay that had
silently used the printed closed form would have certified **three of the four rows
at the wrong radius** and still reported success. The sign-condition method is
doing real work, and the caveat is correctly flagged in the packet. The overshoot
pattern is pinned in this verifier so that any future edit to either the rows or
the method breaks the check rather than passing quietly.

## Non-claims

- Confirms the maintainer's certificate; **proves nothing new, closes nothing,
  and moves no endpoint.**
- No claim about adjacent deployed rows, the corridor rows, or the `F_{17^32}`
  row — only these four smooth prime-field rows.
- Primality rests on Proth's theorem with the recorded witnesses, as in the
  original packet; no independent primality method is introduced.
- The compiler-window hypothesis is checked as an inequality on `B`; the
  underlying window compiler itself is not re-derived.
