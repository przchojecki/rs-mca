# X1: the deep-point line is a CS25-free proof of Paper D's universal cap

- **Status:** PROVED-modulo-`lem:fiber` (which is itself elementary and now
  independently audited) / AUDIT. This note *reorganizes* the existing
  deep-point results into a single dependency statement; the mathematics is in
  [`x1_prob_explicit_deep_point.md`](x1_prob_explicit_deep_point.md) (density)
  and [`x1_deep_point_interleaved_bridge.md`](x1_deep_point_interleaved_bridge.md)
  (the identity), and the arithmetic is in the three `verify_x1_prob_explicit_*`
  scripts plus the new `verify_x1_lem_fiber.py`.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Scope:** Paper D (`tex/cs25_cap_v12.tex`) `thm:main`/`cor:grand` (universal
  cap), `thm:A` (the CS25 import being removed), `lem:fiber`. Does not edit
  Papers A--D.

## One-sentence claim

The universal cap `thm:main` admits a **second, CS25-free proof**: the same
bound `emca(C,delta) > (1/(2k))(1-n/q)` under the same hypothesis `eq:hyp`,
proved by an **explicit line** through the deep-point identity, with the only
non-elementary ingredient -- `lem:fiber` -- being elementary locator-fiber
combinatorics that imports nothing from CS25.

## The dependency restructuring (the whole point)

Paper D proves `thm:main` by a contradiction (lines 350--397 of
`cs25_cap_v12.tex`):

```
   ASSUME  eca(C,delta) <= (1/2k)(1-n/q)              [small]
   thm:A   (CS25 Thm 2, contrapositive):  small eca  ==>  Lst(C^+,delta) <= q/k+1   [small list]
   lem:fiber(ii):                          Lst(C^+,delta) >= binom(N,ell2)/|B| >= q/k+1  [large list]
   eq:hyp  makes the two bounds collide   ==>  CONTRADICTION  ==>  eca is large.
```

So `thm:main` rests on **two** ingredients of very different character:

| ingredient | what it gives | character | imports |
|---|---|---|---|
| `lem:fiber`(ii) | the heavy word `u_z` has a list of `>= binom(N,ell2)/|B|` codewords in `C^+` at radius `delta_N` | **elementary** (locator polynomials + pigeonhole over `B`) | none (part (i) cites Cho26a; **part (ii) is self-contained**) |
| `thm:A` | small `eca` forces a small `C^+`-list (used contrapositively) | **external** | **CS25 Thm 2** |

The deep-point route **keeps `lem:fiber` verbatim and deletes `thm:A`**:

```
   lem:fiber(ii):        u_z has a list  L = binom(N,ell2)/|B|  of C^+ codewords at radius delta_N
   deep-point identity:  the simple-pole line  f = u_z/(x-alpha), g = -1/(x-alpha)
                         has  Bad_CA = Bad_MCA = Deep_alpha = { P(alpha) : P in the list }   [DIRECT]
   averaging (Lem 2.1):  best alpha has  M := |Deep_alpha| >= L/(1 + k(L-1)/|Omega|)
   ==>  eca(C,delta) >= M/q >= (1/2k)(1-n/q)             [the cap bound, CONSTRUCTIVELY]
```

The contrapositive "small eca `==>` small list" (which is what `thm:A`/CS25
supplies) is replaced by the **forward, constructive** identity "this explicit
line *has* that many bad slopes." No `eca <= ...` assumption, no augmented-code
conversion, no `eta`. The cap becomes a *witness*, not a contradiction.

## Why "CS25-free modulo `lem:fiber`" is an honest statement

The phrase is only meaningful if `lem:fiber` does not itself re-import CS25.
It does not:

- **Self-contained proof.** `lem:fiber`(ii)'s proof (`cs25_cap_v12.tex`
  255--273) is: take `A subseteq Q` with `|A|=ell2`; the locator
  `L_A = prod_{b in A}(X^a - b) = X^{k+2a} - e_1(A) X^{k+a} + R_A` with
  `deg R_A <= k`; set `z_A = -e_1(A) in B`, `c_A = (-R_A(x)) in RS[B,D,k+1]`;
  then `u_{z_A}` agrees with `c_A` on the `k+2a` roots of `L_A`; the map
  `A |-> c_A` is injective on subsets of common slope; pigeonhole over the
  `<= |B|` values of `z_A` gives the count. This uses **only** elementary
  symmetric functions and a pigeonhole. The single citation (Cho26a, "Main
  Thm (d)") is for part **(i)**, the degree rung below, not part (ii).
- **Independently audited.** `verify_x1_lem_fiber.py` reconstructs the entire
  argument by **full enumeration** over `F_17` (`D = F_17^x`, `n=16`, `N=8`,
  `a=2`, `k=4`, `rho=1/4`, `ell2=4`, all `binom(8,4)=70` four-subsets of
  `Q = D^2`): it confirms (1) `deg R_A <= k` for every `A`; (2) `u_{z_A}`
  agrees with `c_A` on `>= k+2a = 8` of the `16` points; (3) `A |-> c_A` is
  injective on each slope class; (4) some `z` has `6 >= 70/17 = 4.12` distinct
  list members. **PASS.**

So the deep-point cap rests on: `lem:fiber` (elementary, checked) + the
deep-point identity (`x1` §1, proved and verified in
`verify_x1_deep_point_*`) + averaging Lemma 2.1 (elementary probabilistic).
**CS25 (`thm:A`) is not used.** `thm:B` (BCHKS/ABF) was already declared
unnecessary for the MCA cap (`rem:import`), so the deep-point route makes the
universal MCA cap depend on **no external list-decoding import at all**.

## Scope and the two honest caveats

1. **Density vs. a pinned witness.** The averaging gives `M >= ...` for the
   *best* `alpha` (and `>= 1/2` of `alpha` via Markov), not a single `alpha`
   certified by direct big-field computation -- a brute density check over
   `F_{p^6}` is infeasible. This is the operative meaning of "explicit": an
   explicit *family* with a proven generic-`alpha` density. Identical in
   spirit to how `thm:main` gives an existence statement, not a pinned line.
2. **The cap bound, not better.** At the saturation boundary `L ~ q/k` the
   deep-image density saturates at exactly `1/(2k)` -- `thm:main`'s constant.
   For `L >> q/k` (e.g. `cor:deployed`) it improves to `~1/k`, matching
   `cor:deployed`'s own `1/k`. So the deep-point route recovers `thm:main`
   throughout its hypothesis region and `cor:deployed` at its sharpened
   constant, never weaker. [`verify_x1_prob_explicit_universal.py`: four
   cap-regime points, all `dens_best >= thm:main bound`, all clear `2^-128`.]

## What this buys the project

- **The negative side no longer rests on CS25 for its headline cap.** The
  universal MCA cap (the prize-facing statement) now has a route whose only
  non-elementary input is the audited `lem:fiber`. This is exactly the
  "isolate the positive core" program: the *negative* side is reduced to
  elementary combinatorics + the verified deep-point identity, so whatever
  remains genuinely open is on the *positive* (L1) side.
- **Constructivity for free.** `prob:explicit` asked for explicit
  non-`B`-rational MCA-bad lines; the same line that proves the cap *is* that
  witness (in the extension regime `v_2(q-1) >= v_2(a_q)`). One construction,
  three jobs: cap proof, `prob:explicit`, and the `lem:confine`/`cor:Fvalued`
  dichotomy `alpha^{a_q} in/notin B`.

## Reproducibility

```bash
python3 experimental/scripts/verify_x1_lem_fiber.py            # lem:fiber(ii), full enumeration (the dependency)
python3 experimental/scripts/verify_x1_prob_explicit_universal.py  # deep-point line recovers thm:main throughout
python3 experimental/scripts/verify_x1_prob_explicit_deployed.py   # cor:deployed-scale density (clears 2^-22)
python3 experimental/scripts/verify_x1_prob_explicit_mechanism.py  # the deep-point bad-slope = deep-image mechanism (F_{17^2})
```

## Ledger impact

- **`thm:main` (alternative proof):** CS25-free route via the deep-point line,
  modulo the (elementary, now-audited) `lem:fiber`. Same bound, same
  hypothesis.
- **Dependency map (clarified):** `thm:main` = `lem:fiber` (elementary) +
  `thm:A` (CS25). The deep-point identity removes the second summand.
