# M1 Two-Coordinate Wall: Stdlib Reimplementation and Extended Scan

**Status:** EXPERIMENTAL / AUDIT.

This note records a pure-stdlib (no numpy/sympy) reimplementation and extension
of the slack-two depth-two M1 two-coordinate Kummer-wall stress test originally
in `experimental/scripts/search_m1_remaining_two_coordinate_wall.py` and
`m1_remaining_two_coordinate_wall_experiment.md`. The scanned object is

```text
S_{a,b,0,d} = sum_{u,v != 0, w=-1-u-v != 0, A != 0}
                chi^a(u) chi^b(v) psi^d(A(u,v)),
A(u,v) = -(u^2 + v^2 + u v + u + v + 1),
```

with `chi` of order `e` and `psi` of order `h = e*gcd(2,n)`, `n=(p-1)/e`. The
conjectured remaining-wall target (`m1_kummer_weil_import_contract.md`, the
sharper `4p` replacement of the conditional `9p` `(KW_2)` import) is
`|S_{a,b,0,d}| <= 4p` on the ramified-nonreciprocal asymmetric-nonresonant
class `C_2^anr`.

New script: `experimental/scripts/search_m1_two_coordinate_wall_stdlib.py`.

## Method

`S_{a,b,0,d}` is exactly the 3D finite Fourier transform of the joint
discrete-log histogram

```text
Count[ dlog(u) mod e ][ dlog(v) mod e ][ dlog(A) mod h ],
```

built by a single `O(p^2)` pass per `(p,e)`. The character sum is then a
separable `e x e x h` DFT (`cmath` only). This is both pure-stdlib (so it runs
in environments without numpy, where the original scanner cannot) and faster
than the numpy matmul-per-`d` original, which lets the scan go past the
published `p <= 500, e <= 24` grid.

## Validation (exact reproduction of the published numpy scan)

The deterministic certificate
`experimental/data/certificates/m1-two-coordinate-wall-stdlib/` records, and
`--check` re-verifies:

- **Asymmetric-nonresonant report grid** (`nonres`, `p <= 500`, `e <= 24`):
  **453 cases, 596304 scanned tuples, 0 violations of `4p`, max ratio
  `3.2173609608`** — matching the published numpy counts and maximum exactly.
- **Diagonal grid** (`remaining`, `n=20`, `p <= 500`): max ratio
  `3.9771715522` at `(p=421, e=21)` — matching the published diagonal maximum.
- **Cross-checked datapoints** (independent `O(p^2)` direct summation):
  the published max `(197,14,(6,1,0,17))` gives `3.2173609608`, and the new
  extension max below gives `3.3516589468`.

(The scanner reports `(13,8,0,11)` rather than `(6,1,0,17)` as the order-14
argmax representative; these are the same orbit — `(13,8,0,11)` is the
`u<->v`-swapped complex conjugate `(14-6,14-1, 28-17)` — with identical `|S|`.)

## Extended finding: a new empirical maximum above 3.2173609608

The published experiment reported the asymmetric-nonresonant maximum ratio as
`3.2173609608` (at `p=197`) and asked, as its explicit next step, to extend the
scan and "look specifically for families that push the ratio above the current
`3.2173609608` maximum."

Extending to `p <= 997, e <= 32` and `p in [1000,1500], e <= 24` (pure stdlib;
~4.2M additional scanned tuples) finds a **new asymmetric-nonresonant maximum**

```text
|S_{4,7,0,1}| / p = 3.3516589468   at  (p=601, e=20, h=40),
line monodromies (8,14,16): ramified, nonreciprocal, distinct, nonresonant.
```

This is independently verified by direct summation (`--selftest`), and it is a
genuine member of the clean normal-crossing class `C_2^anr`. It exceeds the
previously published maximum `3.2173609608`, so:

- the prior `3.2173609608` was **not** the supremum of the asymmetric-nonresonant
  wall — the true maximum is at least `3.3516589468`;
- consequently **any conjectured constant in the open interval
  `(3.2173609608, 3.3516589468)` is refuted** by the `(601,20)` example;
- the conjectured `|S| <= 4p` bound still holds: **0 violations of `4p`** were
  found across the whole extended grid (`p <= 1500, e <= 24..32`,
  `> 4.2M` tuples), so the margin to `4p` has narrowed from `~0.78p` to
  `~0.65p` but is not closed.

The new extremal example sits at small slack (`d=1`) with line monodromies
`(8,14,16)`, distinct from the equal-line diagonal family `(c,c,c)` where the
near-`4p` ratios live; so the asymmetric (off-diagonal) wall has its own larger
near-extremal locus than the published `3.2173609608` row suggested.

## Diagonal (equal-line) family: extended to p <= 3000

The near-`4p` ratios live in the equal-line-monodromy diagonal family
`S_{a,a,0,d}` (the conditional `C_2^eq`/`C_2^peq` slice, ledger `4p+3sqrt(p)`),
where the published scan peaked at `3.9771715522` (`p=421`). Extending the
`n=20` diagonal scan from the published `p <= 1601` to `p <= 3000` (48 cases,
571332 tuples) finds **0 violations of `4p`**; the maximum stays
`3.9771715522` at the small prime `p=421`, and the large-`p` diagonal maxima
settle near `3.91`-`3.93` (e.g. `3.9262` at `p=2141`, `3.9134` at `p=2741`),
comfortably below `4p` -- indeed below `4p - 3sqrt(p)`. So the diagonal family
shows no approach to `4p` at larger scale: the `4p` ceiling is not threatened on
either the asymmetric-nonresonant or the equal-line diagonal side within the
scanned range. (Reproduce: `--scan --diagonal-n 20 --p-max 3000 --mode remaining`.)

## Round-2 extension (broad-`n` sweep; records re-confirmed, not beaten)

A second sharded sweep complements the round-1 single-family (`n=20`) deep-`p`
run above with a *broad* `n in [13,40]` diagonal sweep (3 shards, each with an
`e`-cap that keeps the `~e^4` DFT cost bounded) plus 4 asymmetric-nonresonant
shards, and re-checks both extremal families with an independent
direct-summation verify. Result: **0 violations of `4p` anywhere; both published
maxima are tied, not beaten.**

- **Equal-line diagonal**, now swept across `n <= 40` at `p <= 1481` (~419k
  tuples): the global maximum stays exactly `3.9771715522` at `(p=421, e=21)`.
  The per-`n` band maxima *decrease* — `3.9772 (n<=21) -> 3.9194 (n<=30,
  p=1051, e=35) -> 3.8879 (n<=40, p=1481, e=40)` — so the margin to `4p` *grows*
  as `e` increases. The near-`4p` locus stays pinned at the small prime
  `p=421`, consistent with the equal-line ledger `4p+3sqrt(p)` peaking at small
  `e` and not approaching `4p` at scale.
- **Asymmetric-nonresonant**, extended to `p <= 1600` (`e <= 32`, three bands,
  ~2.30M tuples) plus a deeper-`e` pass `e <= 40`, `p in [503,850]` (~2.13M
  tuples): the maximum stays exactly `3.3516589468` at `(p=601, e=20)`; the
  large-`p` band maxima saturate around `3.12-3.17` (`3.1234 @ p=859`,
  `3.1681 @ p=1117`, `3.1708 @ p=1427`), well under `4p`.

An independent direct-summation check (`direct_S`, a different algorithm than
the histogram-FFT) was wired in to re-confirm any new record or `4p` violation;
none arose, so the FFT maxima stand. Net: the `4p` wall survives a materially
wider grid, and the asymmetric sup `3.3517` / diagonal sup `3.977` are
reaffirmed as the working extremes (margin to `4p` is `~0.65p` asymmetric,
`~0.023p` diagonal, and that diagonal margin only widens at larger `e`).

Reproduce (round-2):
```sh
# equal-line diagonal family, per n (cap p so e=(p-1)/n stays modest):
for N in 13 20 30 40; do
  python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py \
    --scan --mode remaining --diagonal-n $N --p-max 1481
done
# asymmetric-nonresonant bands:
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py \
  --scan --p-min 1300 --p-max 1600 --e-max 32 --mode nonres
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py \
  --scan --p-min 503 --p-max 850 --e-max 40 --mode nonres
```

## Reproduce

```sh
# self-test + validation certificate (re-verifies the published-grid reproduction)
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py --selftest
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py --check \
  experimental/data/certificates/m1-two-coordinate-wall-stdlib/m1_two_coordinate_wall_certificate.json
# the extended asymmetric-nonresonant scan that finds the new maximum:
python3 experimental/scripts/search_m1_two_coordinate_wall_stdlib.py --scan \
  --p-min 503 --p-max 997 --e-max 32 --mode nonres
```

## Limitations

Finite numerical evidence only (floating-point character sums, same methodology
as the original numpy scan). It neither proves the `4p` bound nor a sharper
asymmetric-wall constant, and does not rule out a larger ratio outside the
scanned range. It does sharpen the conditional `(KW_2)` import target: a
conductor argument for `C_2^anr` must now accommodate ratios up to at least
`3.3516589468`, not merely the previously reported `3.2173609608`.
