# Mid/large-h routes: the (6, A] certification gap

- **DAG node:** `midlarge_h_certification` (parent: `c1_scalable_certificate`,
  consumer: `a_closure_assembly`).
- **Status:** analysis + two PROVED items + one honest negative.
  PROVED here: (M1) anchored-trade rigidity (an exact reparametrization,
  corollary of banked Lemma 0 + X81) and (M2) the Frobenius frequency-
  doubling / two-value characterization at `p = -1 mod n` extension rows —
  both with complete proofs and exhaustive small-row verification.
  NEGATIVE (with a precise autopsy): the route-(a) "active-core overwhelm"
  pigeonhole does **not** close unconditionally — it is an exact coordinate
  change of the terminal `active_core_count_bound`, not a shortcut.  This
  agrees with and sharpens `h_window_derivation_audit.md` sec 3.2.
- **Verifier:** `experimental/scripts/verify_c1b_descent_injection.py`
  (sections S10, S11, S12 plus the Part-1 gates and pinned certificate;
  20/20 PASS in this packet).
- **Companion:** `experimental/notes/roadmaps/c1b_descent_injection_lemma.md`
  (the low-`h` descent lane; its `h <= ~6` feasibility re-pricing feeds
  section 1 here).

## 0. TL;DR

1. The gap is real and now precisely bounded: certificates cover `h = 4`
   (C1a and C1b, independently), `h = 5, 6` marginally (C1b); the a-priori
   envelope is `h <= A` (**PROVED**, `star_pte_support_bound.md`; the
   `2h <= A` hope is dead).  So the honest uncovered range is
   `h in (6, A]`, nominally `(10, A]`, with `A = 67 / 133 / 261` per rate.
2. Route (a) as sketched (Lemma-0 pigeonhole on top-coefficient tuples)
   yields an exact **bijection**, not a bound: it reproduces the h=3
   calibration counts (18 / 129) instead of bounding them.  The missing
   ingredient is an unconditional count of `F_q`-points of the anchored
   system — which **is** the terminal node.  Detailed autopsy in section 2.
3. New small lever (PROVED): at extension rows `q = p^2`, `p = -1 mod n`,
   every h-trade support satisfies a rigid two-value derivative condition
   (section 3) — the trade sits exactly at the BCH bound of an interval
   code whose zero set Frobenius doubles for free.  No count extracted yet;
   the cleanest new attack surface this note produces.
4. Budget arithmetic (S11c): a **uniform bound of ~3.3e3 active anchored
   cores per h** (at `n = 1024`, any `h >= 11`) would close the entire gap
   through the banked partner cap.  Observed calibration sits 1-2 orders
   below that line (18/129 at `q ~ n^2`; 0 at `q >= n^3`, all h >= 3 rows
   ever measured).  Quantified target, not a proof.
5. Recommendation: the gap stays TARGET.  The only complete lanes remain
   (i) certificate extension per h (A3 machinery, currently compute-bound
   at `h <= ~6`) and (ii) the absorbency retreat (A3 gap G3).  Section 6.

## 1. The corrected gap

Inputs: `h_window_derivation_audit.md` (H_max := A);
`star_pte_support_bound.md` (**PROVED**: the star-PTE trade half-size is
`h = A - r`, `r` = agreement-set overlap `<= k-1`, so `t < h <= A`, both
endpoints realized at `F_101`; the tighter `2h <= A` reading is **wrong**
— the `2h`-support spans two agreement sets); the C1b packet's feasibility
re-pricing (its section 8.2).

```text
rate   A     W3 grammar cap  certificate coverage      uncovered
1/4    261   100 (< A)       h=4 solid; 5,6 marginal   (6, 261]; (100, 261] also outside the grammar window
1/8    133   100 (< A)       same                      (6, 133]; (100, 133] also outside the grammar window
1/16   67    100 (>= A)      same                      (6, 67]  (inside the grammar window)
```

The `(100, A]` tail is outside the frozen W3 v1 grammar window at rates
1/4 **and** 1/8 (nonempty at both), empty only at 1/16.  Prize rows
(`n = 2^41`) have empty small-block windows (`t > 1681`) and need nothing
from this note.  Formally the C1b theorems extend to every `h <= A`
(e.g. `h = 261`: `k* = 8`, bottom `n_8 = 4`, `delta_8 = 259`, one shared
symmetric function — well-defined but computationally meaningless); the
feasibility stop is `h ~ 6`, as tabulated there.

## 2. Route (a): the active-core overwhelm — exact autopsy

### 2.1 What is provable: the rigidity bijection (M1)

**Lemma M1 (anchored trade rigidity).**  Fix a row `(F_q, mu_n)`, any `h`.
Map an anchored unordered minimal `h`-trade `{P, Q}` (`1 in P u Q`,
`L_Q = L_P - c`) to

```text
( a, sigma ) in F_q^{h-1} x F_q,
a = the shared coefficients of L_P, L_Q in degrees 1..h-1,
sigma = L_P(0) + L_Q(0).
```

This map is **injective**, with explicit inverse on its image:

```text
S := X^h + a_{h-1}X^{h-1} + ... + a_1 X + sigma/2      (= (L_P + L_Q)/2),
lambda := S(1)^2,   C := S^2 - lambda,   {P, Q} := the X81 split of C.
```

*Proof.*  `L_P + L_Q = 2S` fixes all of `S` from `(a, sigma)`;
`L_P L_Q = S^2 - c^2/4`; the anchor `C(1) = L_P(1) L_Q(1) = 0` forces
`c^2/4 = S(1)^2`; X81's uniqueness of the square-shift split recovers the
unordered pair.  QED

This is the precise content of "the split-locator tuple is determined by
its top half + the split condition": an anchored trade is `h` field
elements of data, not `2h`.  It is a repackaging of banked Lemma 0
(`a3_good_reduction_lemma.md` sec 1.1) + X81, and it is **verified** as a
bijection-with-reconstruction on every anchored trade at `(16, 3, F_17)`
(132 trades <-> 132 tuples) and `(16, 4, F_17)` (63 <-> 63, an exceptional
row) — gate S10 — and on the 18 anchored h=3 trades at `(128, 3, 17921)`
(18 <-> 18) — gate S11a.

### 2.2 Where the pigeonhole dies

The hoped-for chain was: active core => low `h-1` coefficients of
`C = L_P L_Q` determined by the top `h+1` (Lemma 0) => active cores inject
into realizable top tuples => count `<= n^2`-ish.  The chain's first two
steps are Lemma M1.  The third step fails, precisely:

- The injection lands in `F_q^h`, and `q^h` is astronomically larger than
  any useful bound.  The only cut is the **realizability closure**: the
  determined `C` must divide `X^n - 1`.  In `(S, lambda)`-coordinates that
  is exactly the anchored system `{F_i(s) = 0}` = the coefficients of
  `rem(X^n - 1, S^2 - S(1)^2)` — A3 section 3.2's object.  So

```text
# anchored trades = # F_q-points of the anchored scheme B^a_{n,h},
```

  an **equality** (M1 is a bijection), and route (a) is a coordinate
  change of the terminal counting problem, not an argument.  Every
  unconditional tool available for the right side is super-polynomial:
  the trivial bound `C(n-1, 2h-1)`; Bezout on `{F_i}` (their `s`-degrees
  grow like `~ n/2` through the `log2 n` squarings, giving `~ (n/2)^h`);
  the value-set partner cap (already factored out — it bounds trades per
  core, not cores).  The first moment (`~ n^2/(h!)^2` at `q >= n^2`) is
  heuristic and non-monotone (audit sec 3.3).  **No poly(n) bound uniform
  in h follows.**

- **The h=3 scrutiny demanded by the brief.**  At `(128, 3, p = 17921,
  q ~ n^2)` the row HAS 18 primitive anchored active cores, at
  `(256, 3, 65537)` it has 129 (x12 census, both replayed/read here — gates
  S11a/S11b).  Any claimed theorem "active cores <= f(n) uniformly in h"
  must satisfy `f(128) >= 18`, `f(256) >= 129`.  M1 is consistent — it
  reproduces exactly 18 and exactly 129, because it is a bijection; it
  bounds nothing.  This is the cleanest possible demonstration that the
  counting force must come from arithmetic input beyond Lemma 0/X81, i.e.
  from exactly what `active_core_count_bound` names.  (Also note: the
  discriminating regime for the closure is `q >= n^3`, where all observed
  counts vanish; a bound tight enough to matter at `q ~ n^2` is neither
  needed nor plausible.)

### 2.3 What would close route (a)

1. Per-(n,h) certificates (A3): at good primes the point count equals the
   char-0 candidate count = 0 primitives.  This is the existing lane; its
   bottleneck is certificate computation, honestly priced at `h <= ~6` by
   the C1b packet.  Route (a) adds nothing to it — same object.
2. A bad-prime multiplicity bound (A3 gaps G3/G4) — no tool.
3. A genuinely new structural point bound for `{F_i = 0}` exploiting the
   2-adic tower or Frobenius — section 3 is a first proved fragment.

## 3. The Frobenius lever at `p = -1 mod n` rows (M2, PROVED)

Write a candidate trade as a signed indicator `u = 1_P - 1_Q`, a function
`mu_n -> {-1, 0, 1} subset F_p`, and let `u^(i) = sum_{x in mu_n} u(x) x^i
in F_q` (the DFT over the row field).

**Lemma M2.**  Let `(F_q, mu_n)` be a row and `(P, Q)` a minimal
`h`-trade.  Then:

(i) `u^(i) = p_i(P) - p_i(Q) = 0` for `0 <= i <= h-1` (`i = 0` by balance;
`1 <= i <= h-1` by Newton's identities in the division-free direction
`e -> p`, valid over any ring).

(ii) `u^(p*i mod n) = ( u^(i) )^p` for all `i` — because `u` takes values
in the prime field and Frobenius is additive: the zero set of `u^` is
closed under multiplication by `p` **for free**.

(iii) If `q = p^2` with `p = -1 (mod n)`: `u^(-i) = (u^(i))^p`, so `u^`
vanishes on the length-`(2h-1)` interval `-(h-1) <= i <= h-1`.

(iv) The evaluation matrix `(x^i)`, `x in R = P u Q`, `i` in that
interval, has rank `2h - 1` (each maximal minor is a monomial times a
Vandermonde determinant on distinct points), and its kernel is spanned by

```text
v_x = x^{h-1} / L_R'(x),        x in R,
```

which has no zero entry.  (Kernel membership: `sum_{x in R} x^m / L_R'(x)
= 0` for `0 <= m <= |R| - 2` — the leading coefficient of the Lagrange
interpolant of `X^m` on `R`, zero because `m < |R| - 1`.)

**Theorem M2'.**  At a row with `q = p^2`, `p = -1 (mod n)`, `p > h`, a
`2h`-subset `R subset mu_n` underlies a minimal `h`-trade **iff** the
function `psi_R(x) = x^{h-1} / L_R'(x)` takes exactly two values `{gamma,
-gamma}` on `R`, each `h` times; the trade split is the sign split.

*Proof.*  (=>) By (i)+(iii), `u` restricted to `R` is a kernel vector of
the interval system, so by (iv) `u = gamma^{-1} psi_R` for some scalar:
`psi_R = gamma u` is two-valued balanced.  (<=) If `psi_R = gamma eps`
with balanced signs `eps`, then `eps` is a kernel vector, so `u^(i) = 0`
for `1 <= i <= h-1` for the sign split, i.e. equal power sums; Newton's
identities in the direction `p -> e` (divisions by `1..h-1`, valid since
`p > h`) give equal `e_1..e_{h-1}`: a trade.  QED

**Verified exhaustively** (gate S12a): at `(n, h, q) = (16, 4, 31^2)`
(`31 = -1 mod 16`), over all `C(16,8) = 12870` supports: the 6 trade
supports are exactly the 6 two-valued supports — no false positives, no
misses.  **The hypothesis `p = -1` is necessary** (gate S12b): at
`(16, 3, q = 7^2)` — `7` has order 2 mod 16 but `7 != -1` — the row has
56 trade supports and `psi` two-valuedness fails on some of them.

**What this buys and does not buy.**  At `p = -1` rows the trade
conditions rigidify from `h-1` to `2h-2` interval conditions at no cost,
and the trade support solves the explicit system `L_R'(x) = gamma^{-1}
eps_x x^{h-1}` (`x in R`) — trades are minimal-weight-at-the-BCH-bound
words of the interval code, a heavily structured class.  A counting
theorem for such supports (over `x in mu_n` with `+-1` weights) would
bound active cores at these rows for **all h at once**.  Not proved;
flagged as the cleanest new attack surface.  Scope limits: only extension
rows `q = p^2` with `p = -1 mod n` (the `f = 2, p = -1` class of A3
Lemma 1's remark); the official Row-C primes are an operator-supplied
class (`c2_gcd_harness.md`), so applicability is parametric; `q = p` rows
(`p = 1 mod n`) get nothing — (ii) is trivial there.

## 4. Route (b): the budget arithmetic (what bound suffices)

Banked inputs: the value-set partner cap `<= floor(n/h)` per active core
(`value_set_partner_cap`, PROVED) and the assembly's absorbency (one
`n^3` column tolerates `~3.1-8.0e5` anchored extras per `h`;
`a_closure_assembly`).  Then per `h`:

```text
# anchored trades <= (# active anchored cores) x floor(n/h)
=> closing bound needed:  # active anchored cores <= 3.1e5 / floor(1024/h)
```

| h | needed core bound | observed calibration |
|---|---|---|
| 11  | ~3.3e3  | (h=3 proxy: 18 at n=128, 129 at n=256, both q ~ n^2; 0 at q >= n^3) |
| 67  | ~2.1e4  | no trade ever observed at h >= 5 at any calibration row |
| 133 | ~4.4e4  | — |
| 261 | ~1.0e5  | — |

(Gate S11c.)  So a **uniform ~3.3e3 active-core bound closes every h in
the gap simultaneously**, with 261 x per-h budgets fitting the priced
column with orders of magnitude to spare — route (d) of the DAG node
needs no aggregation cleverness.  The observed data sit 1-2 orders below
the needed line even in the too-hard `q ~ n^2` regime.  This is a
quantified target; **no such bound is proved** (section 2.2).

## 5. Route (c): the support micro-lemma — resolved, cited

`star_pte_support_bound.md` (PROVED, 5/5, banked): `h = A - r` with
`r = |S_f cap S_g| <= k - 1`, so `t < h <= A` and `H_max = A` is the
correct consumer envelope; `2h <= A` is dead (the `2h`-support spans two
agreement sets).  Consequences for the ranges are in section 1.  Not
re-derived here.

## 6. Honest map of what remains

- **PROVED and banked by this packet:** M1 (rigidity bijection; the exact
  currency in which the terminal count must be fought), M2/M2' (Frobenius
  doubling + two-value characterization at `p = -1` extension rows), the
  budget target arithmetic, and — in the companion packet — the full C1b
  descent/injection/soundness chain with its honest `h <= ~6` feasibility.
- **DEAD:** the unconditional route-(a) pigeonhole; the `2h <= A` reading.
- **OPEN (the gap itself):** any of (1) certificates `D(1024, h)` for
  `h in (6, A]` — needs new elimination technology, not more of the same;
  (2) the terminal active-core bound (`~3.3e3` suffices); (3) a
  minimal-weight/interval-code counting theorem sharpening M2' into a
  core bound at `f = 2` rows; (4) A3's G3 absorbency retreat at bad
  primes.  The node stays **TARGET**; the Fable-brief coverage claim
  should be updated from "C1b h <= ~10" to "C1b h <= ~6, gap (6, A]".

## 7. Verification

```bash
python3 experimental/scripts/verify_c1b_descent_injection.py
```

Part-2 gates: S10 (M1 bijection + reconstruction, two rows, one of them
exceptional), S11a (recompute 18 at `(128,3,17921)`; rigidity on the
anchored trades), S11b (129 at `(256,3,65537)` from the pinned x12
certificate), S11c (budget arithmetic), S12a (M2' exhaustive at
`(16,4,31^2)`), S12b (necessity of `p = -1`).  Current replay: **20 PASS,
0 FAIL** as part of the full suite.
