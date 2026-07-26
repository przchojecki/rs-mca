# Corridor Literal Prime: a Pinned Admissible Field for the Prize-Scale Rows

- **Status:** PROVED (Pocklington certificate; all row arithmetic exact-integer,
  replayed by the verifier below).
- **Agent/model:** Claude Opus 5 acting for AllenGrahamHart.
- **Scope:** fills the printed TODO in the remark after `thm:corridor` in
  `experimental/proximity_prize_results_v4.tex`:

  > "The prize-scale corridor packet uses a pinned exact budget convention
  > corresponding to a line field near `2^255.9`; it does not yet pin one literal
  > prime in the paper. The safe inequalities are unconditional under that stated
  > denominator. **A final row release should add a literal admissible field and
  > rerun the same exact comparisons.**"

  This packet supplies that literal field and reruns the comparisons. It **pins the
  denominator; it strengthens no bound.**

## Why one prime suffices

The six audited safe edges depend on `q` only through the budget
`B* = floor(q / 2^128)` — the Hab25 comparison is the exact integer inequality
`(2m+1)^14 n^7 <= 9 * 2^14 (k-1)^3 B*^2` and the GKL24 gate is
`(n-r)^3 > (k-1) n^2`, neither of which sees `q` otherwise. So a literal prime
carrying the packet's printed `B*` reproduces every printed radius exactly, rather
than approximately.

## The field

```text
P = 8796093033515 * 2^45 + 1
  = 309485010219174763933204481                     (89 bits, Proth prime, base 3)

q = 2^41 * P * 158747337183671499011314909792715251078 + 1
  = 108037839417390090843359763492907651258221714407500997496797919767622829735937
```

| property | value |
|---|---|
| bit length | 256, and `q < 2^256` |
| `q / 2^255` | `1.866…`, i.e. `log2 q ≈ 255.9` — the packet's stated convention |
| `v_2(q-1)` | **42** (`≥ 41`, so `F_q` carries an order-`2^41` smooth evaluation domain) |
| `floor(q / 2^128)` | `317494674775468773183020924238786383963` = **`B*` exactly** |

## Certificate

`P` is certified by Proth's theorem: `P = d·2^45 + 1` with `d` odd and `d < 2^45`,
and `3^((P-1)/2) ≡ -1 (mod P)`.

`q` is certified by Pocklington with the factored part `F = 2^41 · P`, whose prime
divisors are `2` and `P`. `F^2 > q`, and for base `a = 3`:

```text
3^(q-1) ≡ 1 (mod q)
gcd(3^((q-1)/2) - 1, q) = 1
gcd(3^((q-1)/P) - 1, q) = 1
```

This is the same certificate shape as the in-repo `e1-pocklington-250bit-exhibit-field`
packet (`F` a known factored part with `F^2 > p`, one base, the per-prime gcd
conditions). **No machinery novelty is claimed** — the Proth/Pocklington
certificates already in this repository are the format anchors.

## Replay at the literal prime

```text
python3 experimental/scripts/verify_corridor_literal_prime.py     # < 1 s
```

Recomputes `B*` as the integer 10th root of `2^1279`, re-derives both certificates,
and re-runs the six prize-scale comparisons from scratch. All three printed safe
edges **and their witness bands** reproduce digit-exactly, with the adjacent
failure exhibited one grid step past each edge:

| row | `n` | `k` | safe radius `r` | `m_min(r) = m_max` | `r+1` |
|---|---|---|---|---|---|
| prize, rate 1/4 | `2^41` | `2^39` | `1092724518963` | `81` | fails |
| prize, rate 1/8 | `2^41` | `2^38` | `1415997755216` | `70` | fails |
| prize, rate 1/16 | `2^41` | `2^37` | `1644686143216` | `60` | fails |

The GKL24 exact integer gate `(n-r)^3 > (k-1)n^2` also holds at each printed GKL24
edge (`813725411113`, `1099511627777`, `1326340298262`) and fails at `r+1`.

Stdlib only; no floats appear in any verdict. Four mutation controls were run
against the verifier (perturbed `q`, wrong witness band, wrong printed edge, wrong
Proth exponent) and each is caught.

## Non-claims

- **Pins the denominator; strengthens no bound.** Every safe radius is exactly the
  one already audited in `corridor-unconditional-safe-edges`; nothing is improved,
  extended, or re-derived.
- Claims no novelty in the Proth/Pocklington machinery — see the format anchors
  above.
- Says nothing about the corridor band itself or its blockers, and nothing about
  the Row C (`n = 2^10`) rows, whose idealized `2^250` field remains unpinned here.
- The underlying safe-edge audit is **latifkasuli's** packet
  (`corridor-unconditional-safe-edges`, PR #275, cited in v4 as `Corridor26`);
  this is an addendum to it, not a replacement.
- `q` is one admissible field, not a canonical or optimal choice: the admissible
  band `[B*·2^128, (B*+1)·2^128)` has width `2^128` and contains many primes with
  `v_2(q-1) ≥ 41`.

## Provenance

- Upstream target commit: `b13de811`.
- Open-PR overlap audit run through #1106 at time of writing: no other PR pins a
  literal corridor field.
- Estimated CPU time to produce and verify: under 10 seconds.
