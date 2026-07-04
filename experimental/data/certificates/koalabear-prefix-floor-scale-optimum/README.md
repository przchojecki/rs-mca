# KoalaBear Sextic: Prefix-Floor Scale Optimum (+70 a-steps of the band)

- **Status:** PROVED (exact integer certificates, adjacent-tight at every
  scale; deployed anchor reproduced).
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** answers the 2026-07-04 top-priority directive (`cd5e809`):
  shrink the deployed KoalaBear sextic row's open threshold band.

## Use Rule header

```text
object:            graded locator-prefix floor (prop:graded-prefix-floor
                   + thm:A deep-point conversion), optimized over the scale
sampler:           finite_affine
q_line:            p^6, p = 2^31 - 2^24 + 1   (~2^185.932)
agreement/radius:  closed integer grid a = m*c, r = n - a, n = 2^21, k = 2^20
statement type:    closed-grid unsafe-side certificates only; no supremum,
                   no safe-side claim
paid ledgers:      none consumed; this is a floor (lower-bound) family
```

## Result

The deployed exact-verified unsafe edge (`rem:exact-frontier`, handle
`(c,m,w,Delta) = (16, 69748, 4211, 67392)`) fixed the scale at `c = 16`.
`prop:graded-prefix-floor` admits any map-smooth scale `c >= 2`, and on the
order-`2^21` subgroup the admissible power scales are exactly the dyadic
`c | n`. Optimizing exactly over all of them:

| route | deployed | scale optimum | gain | new unsafe edge |
|---|---|---|---|---|
| MCA | `c=16, m=69748, Delta=67392` | `c=2, m=558019, Delta=67462` | `+70` a-steps | `490557/1048576 ~ 0.46783161` |
| list | `c=32, m=34874, Delta=67392` | `c=2, m=558022, Delta=67468` | `+76` a-steps | `245277/524288 ~ 0.46782875` |

Every scan row is adjacent-tight (`m` holds, `m+1` fails) in exact integer
arithmetic; the deployed MCA anchor reproduces `kb_mca_pf` exactly.

**Route exhaustion.** `Delta` increases monotonically toward finer scale and
`c = 2` is the finest admissible scale, so this certificate spends the
graded prefix-floor route's entire dyadic headroom — consistent with the
`rem:entropy-frontier` envelope (`g*(1/2, 31) ~ 0.0321617`; achieved
`67462/2^21 ~ 0.0321646`, leading-order-consistent with mildly favorable
finite-size corrections). The remaining open band below
`490557/1048576` is untouchable by this construction at any scale: the
"new mathematics needed" frontier now starts 70 steps lower and is
route-complete.

## Replay

```text
python3 experimental/scripts/verify_koalabear_prefix_floor_scale_optimum.py --check          # c >= 4, ~6 min
python3 experimental/scripts/verify_koalabear_prefix_floor_scale_optimum.py --check --full   # all scales, ~35 min
```

`--check` recomputes both sides of every inequality from the row parameters
(stdlib `math.comb`, no floats in any verdict) and re-derives the JSON
deterministically; the two `c=2` checks are in `--full` (~1M-bit integers).
Independent discovery + verification chain (two separate exact
computations before this packet) is recorded in the external repository:
`github.com/latifkasuli/mca` commit `605a8b7`
(`scripts/koalabear_prefix_floor_scan.py`,
`runs/koalabear_prefix_floor_scan.json`,
`docs/koalabear-prefix-floor-frontier.md`).

## Non-claims

- Unsafe-side only: no statement about `B_mca(a)` for
  `a > 1116038` beyond what upstream already certifies.
- No claim that non-power map-smooth scales exist on this domain (they
  would need complete uniform fibers within the 2-power subgroup).
- Not an adjacent staircase pin: the safe side of the band is untouched.
