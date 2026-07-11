# split-pencil ray collapse: the deduplicated census IS the list count, at every profile

**Status: PROVED (from upstream ingredients) / AUDIT.**
Track: `(split-pencil census)` lane closure into the saturated-BC/ray-dedup
lane. Target files `experimental/cap25_cap_v13_raw.tex` (= cap25) and
`experimental/grande_finale.tex` (= gf) at base `36de5bf`. **No `.tex`/
`.pdf` edited.**

## Theorem (split-pencil ray collapse)

Let `(W1, N1, W2, N2)` be a determinantal representation of `Lambda_D` as
in `prop:capfr1-detrep` (cap25 L7992) with shifted weak-Popov profile
`(d1, d2)`, `d1 + d2 = n - K + 1`. Fix `m >= K`, `omega = n - m`, and let
`SPCen` be the exact census set of `prob:capg-split-pencil-B` (cap25
L9847-9851): monic normalizations of `(A, B)` with `deg A <= omega - d1`,
`deg B <= omega - d2`, `A W1 + B W2 | Lambda_D`, `deg(A W1 + B W2) =
omega`. Then the map

    (A, B)  |->  c := (A N1 + B N2) / (A W1 + B W2)

is well-defined into `C = RS[F, D, K]`; its image is exactly `Ray(U; m)`
(gf `def:saturated-rays` L1792); and its fiber above `c` is
`{H (A0, B0) : H | ell_{S_c(U)}, deg H = s_c(U) - m}`, of size exactly
`C(s_c(U), m)`. Consequently

    #(SPCen / ray-equivalence) = |Ray(U; m)| = #{c : deg c < K, agr(U,c) >= m}

at **every** profile — in particular at every interior balanced profile
`w' + 2 <= d1 <= floor((n-K+1)/2)` — and, summed over a slope set `E`,

    sum_{z in E} #(SPCen(U_z) / rays) = |LineRay_E(u, v; m)|

(gf `def:line-rays` L1857): the repaired split-pencil census at the
deduplicated level is verbatim the **middle object** of
`prop:line-ray-saturation`'s two-loss chain (gf L1874-1881), and is
subsumed by `prob:saturated-bc` alternative (b) — any bound on it is a
"slope, not raw-support" bound via `N_slopes <= |LineRay_E|`.

## Proof

All ingredients are upstream; no new machinery.

1. *Well-definedness and `deg c < K`.* For `(A, B)` in the census set,
   `W := A W1 + B W2` is a monic degree-`omega` divisor of `Lambda_D`
   (D-split, squarefree), and `(W, N) := A (W1, N1) + B (W2, N2)` lies in
   `M_U`. By `lem:capfr1-autodiv` / `lem:capfp-autodiv` (cap25 L7972 /
   L8405), `W | N`; by predictable degrees
   (`prop:capfr1-lattice-census(a)`, cap25 L7885) `deg N <= omega + K - 1`,
   hence `c = N/W` has `deg c < K`.
2. *Image inside the list.* `W (U - c) = 0` on `D`, so `U = c` off the
   `omega` roots of `W`: `agr(U, c) >= n - omega = m`.
3. *Surjectivity and the fiber.* By `thm:saturation`'s fiber statement (gf
   L1816-1826), the census elements of `M_U` above a fixed ray `c` are
   exactly `(W, N) = H (G_c, G_c c)` with `G_c = ell_{D \ S_c(U)}`,
   `H | ell_{S_c(U)}`, `deg H = s_c(U) - m` — `C(s_c(U), m)` of them, one
   per size-`m` subset of the agreement set, nonempty iff `s_c(U) >= m`.
   Pulling through the free-basis coordinates (the representation
   `(W, N) = A g1 + B g2` is unique), every such element lies inside the
   caps by `prop:lattice-split` (gf L1343) — equivalently
   `thm:capfr1-near-rational-dichotomy(ii)` (cap25 L7924-7930), whose
   proof is precisely predictable degrees: a census element has
   `wdeg = omega`, so `deg A <= omega - d1` and `deg B <= omega - d2`
   automatically. Each fiber element has `W = ell_{D \ T}` of exact degree
   `omega` and D-split, so the exact-degree and divisibility conditions
   are automatic. Hence the map is onto `Ray(U; m)` with the stated
   fibers.
4. *Profile independence.* No step above uses `d1` beyond predictable
   degrees, which hold at every profile of a reduced basis. The line-sum
   statement is then `def:line-rays` unwound:
   `|LineRay_E| = sum_z |Ray(U_z; m)|`. QED.

The ray grouping itself is asserted as "Internal structure, fully proved"
in prose at cap25 L8439; this note's content is the *deduplicated count*
consequence, which is never printed upstream as a count, and its wiring to
the corrected problems and the saturated-BC chain.

## Corollary (per-profile multiplicity cap; generalizes the #518 lemma)

Minimality of `d1` forces `dist(U, c) >= d1` for **every** codeword `c`
(the locator pair `(Lambda_E, Lambda_E c)` is a nonzero element of `M_U`
of shifted degree `dist(U, c)`). Hence at profile `d1` every ray has
`agr <= n - d1` and per-ray census multiplicity `<= C(n - d1, m)` — the
exact per-profile cap on how far the raw census exceeds the deduplicated
one. The `d1 = e` profile-localization lemma of
`capg_split_pencil_refutation.md` (integrated #518) is the matching
attainability statement: the cap is achieved, at any prescribed interior
profile, by a distance-`e` word.

## Consequences for the recorded problems

- **`prob:capg-split-pencil-B` / `prob:capg-active-BC` retire as
  independent problems.** Their with-multiplicity forms are refuted
  (#518); their deduplicated repairs are, by the theorem, verbatim the
  `|Ray|`/`|LineRay|` objects of the saturated-BC lane. The split-pencil
  lane is not a second route to `prob:capfr1-normalized-band`; it *is*
  `prob:saturated-bc` alternative (b) in pencil coordinates.
- **Compile-through.** Any future census-lane bound at the deduplicated
  level converts into a type-(b) slope bound via
  `N_slopes <= |LineRay_E|` (gf L1874-1881, loss-1 side).
- **Moment interface.** With `mult(W) = L(P_W, Q_W)`
  (`split_pencil_wcollision_pair_moment.md` L53-57), the first-moment
  chart identity `sum_{|W|=k} mult(W) = sum_{(z,c) in LineRay}
  C(s_{z,c}, k)` (immediate double count) and the note's second-moment
  identity (L24-28, L43-51) form the exact ledger converting future
  anti-concentration of pencil live counts `L` into bounds on
  `|LineRay_E|` — and only then, after strips, into the XR consumer's
  `R_post <= 16 n^3` (`xr_clean_poly_forcing_reduction.md` L20, L43).

## Statement hygiene pins (found during the hostile read)

1. **Reduced-basis rigidity.** `prop:capfr1-detrep` admits any coprime
   quadruple with the profile "imposed after this representation is
   chosen" (cap25 L8005); predictable degrees require *reduced* bases.
   The statement is saved by an unstated rigidity: shifted row degrees
   summing to `n - K + 1` (zero orthogonality defect) force reducedness.
   `prop:capfp-detrep` says "shifted-reduced" explicitly (L8422);
   `capfr1-detrep` should too.
2. **Exact-degree display inconsistency.** `prob:capfr1-split-pencil`
   (L8019) and `prob:capg-split-pencil-B` (L9848) display
   `deg(A W1 + B W2) = omega`; `prob:capfp-split`'s display (L8436) omits
   it (prose only, L8439). Robustness: dropping exact-degree changes the
   raw count but **not** the ray count (lower-degree members join
   higher-agreement rays; no new directions).
3. **Dedup by direction.** Ray equivalence is proportionality of
   `(A, B)` as a direction (`A/gcd`, `B/gcd`, mod scalars); `gcd(A, B)`
   is the ray parameter `H` (squarefree, roots in the agreement set).
   Deduplicating by gcd-freeness instead of direction would be wrong.
4. **`deg c = K - 1` pivot ties** are an implementation hazard only
   (cap25 L8343-8344 handles the mathematics; Popov pivot conventions
   must break the tie consistently).

## Verification

`experimental/scripts/verify_split_pencil_ray_collapse.py`
(`--emit-defaults` / `--check`) + independent
`verify_split_pencil_ray_collapse_check.py`: F_73 toy (n = 24, K = 12,
m = 15, omega = 9), full `C(24,9) = 1,307,504` divisor enumeration per
word, three-way comparison RAW / RAYS / LIST with the LIST side computed
independently of the pencil (GRS-duality power-sum functionals +
interpolation). Menu of 11 deterministic words: planted `e = 4..9` (the
last three outside the `d1 = e` lemma range), two-codeword words (two
simultaneous list codewords, agr pairs (15,15) and (16,15)), random
controls. Gate: `RAYS == LIST` with matching agreements and
`RAW = sum C(agr, m)` over the list — **11/11 PASS**; plus the tight-ray
cap-exactness check (`deg A0 = omega - d1`, `deg B0 = omega - d2` at a
two-codeword word — the off-by-one detector for pin 2).

## NON-CLAIMS

- No upper bound on `|Ray|`, `|LineRay|`, or any slope count. The open
  core is unchanged and is the prize frontier itself: exact list-size
  control below the Johnson radius at the deployed rows
  (`m/n ~ 0.532 < sqrt(rho) ~ 0.707`).
- No chart verification: `prob:saturated-bc`'s per-row alternatives
  (a)/(b) are not discharged for any chart.
- No progress on `R_post <= 16 n^3` (the strips remain load-bearing, per
  the pair-moment note's own non-claims).
- Nothing about `prob:capfp-R1`. (A separate observation that its
  corrected model may inherit the raw-count trap is deliberately withheld
  pending its own verification; it is not asserted here.)
