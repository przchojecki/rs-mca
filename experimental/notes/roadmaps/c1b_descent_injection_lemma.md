# C1b: the descent-injection lemma packet

- **DAG node:** `c1b_descent_injection` (consumer: `c1_scalable_certificate`,
  `a_closure_assembly`; sibling gap node: `midlarge_h_certification`, see
  `experimental/notes/roadmaps/midlarge_h_routes.md`).
- **Status:** the descent/injection/soundness chain (Lemmas D1-D4, Theorems
  D5-D7, Lemma D8) is **PROVED** below, uniformly in `h` and in the field,
  with complete written proofs; every statement is instance-checked by the
  verifier (20/20 PASS, ~20 s, <300 MB, including the pinned certificate).
  The **feasibility** of the
  resulting certificate at `n = 1024` is honestly re-priced in section 8 and
  is **narrower than the DAG's estimate**: comfortable at `h = 4`, marginal
  at `h = 5, 6`, dead at `h >= 7` without new census engineering (the DAG
  said "h <= ~8-10").  Named gaps are in section 9.
- **Verifier:** `experimental/scripts/verify_c1b_descent_injection.py`.
- **Certificate:** `experimental/data/certificates/c1b-descent-injection/c1b_descent_injection.json`
  plus the small X12 active-core input certificate under
  `experimental/data/certificates/x12-h3-active-core-census/`.
- **Inputs:** the sympy-verified seed identity (DAG node statement), X81
  (unique split), X24 (char-0 classification; the paid-branch mechanism),
  A3 sections 1.3-1.4 (anchoring, coset-union = paid ledger), the pilot
  censuses (`a_pilot_wh_torsion_data.md`: exact ground truth at n = 16/32/64).

## Critical-path role

This packet closes the proof-theoretic part of blocker C1b in the clean-rate
critical path. It gives the descent map, exact lift soundness, and the paid
collision split needed to turn low-`h` trade exclusion into smaller bottom
censuses. Its important limitation is also part of the integration: the method
comfortably covers `h=4`, is marginal at `h=5,6`, and does **not** cover the
mid/large window `h >= 7` without new census engineering. The companion
`midlarge_h_routes.md` records the resulting gap `(6,A]`, proves the M1/M2
route facts that survive scrutiny, and rejects the failed active-core
pigeonhole shortcut.

## 1. Setting and conventions

`n = 2^s`.  `F` is any field of characteristic `!= 2` in which `X^n - 1`
splits (equivalently `mu_n(F)` has exactly `n` elements); everything below
is uniform in `F` — it applies verbatim to `F_q` rows (`n | q - 1`) and to
`K = Q(zeta_n)`.  Levels are indexed by `k = 0, 1, ..., s`; the level-`k`
root group is `mu_{n_k}`, `n_k = n / 2^k`.  The squaring map
`pi(x) = x^2` sends `mu_{n_k}` onto `mu_{n_{k+1}}`, 2-to-1 with fibers
`{w, -w}` (antipodal pairs; `-1 in mu_{n_k}` for `n_k >= 2`).

A **level-0 h-trade** is a pair of disjoint `h`-subsets `P, Q` of `mu_n(F)`
with `e_i(P) = e_i(Q)` for `1 <= i <= h-1`; equivalently the monic locators
satisfy `B_0 = A_0 + c` with `A_0 = L_P`, `B_0 = L_Q`, `c != 0` constant
(x81/x83 normal form).  A **level-`k` pair** is an ordered pair `(A, B)` of
monic degree-`h` polynomials over `F` whose root multisets lie in
`mu_{n_k}(F)`; its **band** is `deg(B - A) in {-inf, 0, ..., h-1}`.
For a monic `A` write `A = E_A(X^2) + X * O_A(X^2)` (even/odd parts; for
`h` even `E_A` is monic of degree `h/2`; for `h` odd `O_A` is monic of
degree `(h-1)/2`).

## 2. The pushforward and the seed identity (Lemma D1)

**Definition.**  For monic `A` of degree `h` set

```text
A^pi(X^2) := (-1)^h A(X) A(-X).
```

**Lemma D1.**  (i) `A^pi` is a well-defined monic polynomial of degree `h`
(the right side is even in `X` and has leading coefficient `(-1)^h * (-1)^h
= 1`).

(ii) `A^pi(Y) = prod_{x in roots(A)} (Y - x^2)` — the multiset pushforward:
the multiplicity of `y` in `A^pi` is `m_A(w) + m_A(-w)` for `w^2 = y`.  In
particular roots in `mu_{n_k}` map to roots in `mu_{n_{k+1}}`, and after
`k` squarings of a squarefree `A_0` every multiplicity is `<= 2^k`.

(iii) For `B = A + D`:

```text
B^pi - A^pi = (-1)^h * [ Abar*D + A*Dbar + D*Dbar ]  written in Y = X^2,
```

where `fbar(X) := f(-X)`; the bracket is automatically even.  For a trade
(`D = c` constant) this is the **seed identity**

```text
B^pi - A^pi = (-1)^h ( 2c * E_A + c^2 )       (a polynomial in Y),
```

i.e. `B(X)B(-X) = A(X)A(-X) + c(A(X) + A(-X)) + c^2`.

(iv) `deg( B^pi - A^pi ) <= floor( (h + deg D) / 2 )`.  For a trade with
`h` even the degree is **exactly** `h/2`, with leading coefficient
`(-1)^h 2c != 0`; for `h` odd it is `<= (h-1)/2`, with equality iff
`e_1(P) != 0`.  (This corrects the DAG node's "exactly floor(h/2)": exact
only for `h` even.)

*Proof.*  (i) direct.  (ii) `(-1)^h prod (X - x_i) prod (-X - x_i) =
prod (X - x_i)(X + x_i) = prod (X^2 - x_i^2)`.  (iii) expand
`(A + D)(Abar + Dbar) - A*Abar`; the bracket is invariant under
`X -> -X`.  (iv) `deg_X (Abar*D + A*Dbar + D*Dbar) <= h + deg D`, and an
even polynomial of `X`-degree `2d` has `Y`-degree `d`; for `D = c`, `h`
even, the top term is `2c * X^h` from `c(A + Abar)`, surviving because
`E_A` is monic.  QED

Verifier: S1a, S1b (symbolic, h = 3, 4, 5, generic coefficients).

## 3. The band budget (Lemma D2)

**Lemma D2.**  Define `delta_0 = 0`,
`delta_{k+1} = floor((h + delta_k)/2)` (Lemma D1(iv) applied at each
level).  Then

```text
delta_k = h - ceil( h / 2^k ),
```

`delta_k <= h - 2` ("informative") iff `2^k < h`, and `delta_k = h-1`
(vacuous: any two monic degree-`h` polynomials qualify) iff `2^k >= h`.
The **informative depth** is `k*(h) = ceil(log2 h) - 1`.  At level `k` the
pair shares its coefficients in degrees `> delta_k`, i.e. its first

```text
sig(h, k) = h - 1 - delta_k = ceil( h / 2^k ) - 1
```

elementary symmetric functions.  *Proof.*  Induction with
`ceil(ceil(a/b)/c) = ceil(a/(bc))`.  QED  (Verifier: S2, h <= 300.)

## 4. The exhaustive one-step case split (Lemma D3)

**Lemma D3.**  Let `(P, Q)` be a level-0 `h`-trade, `R = P u Q`.  Exactly
one of the following holds.

**(a) Antipodal-diagonal (the paid branch): `Q = -P`.**  Equivalent
characterizations: `A_0^pi = B_0^pi`; the pushforward pair is diagonal.
Then `R = P u (-P)` is a union of `mu_2`-cosets `{x, -x} = x*mu_2`, i.e.
**coset-union/imprimitive** in the sense of A3 section 1.4 — charged to the
strip/staircase-paid ledger, not to the primitive `n^3` column.  This
branch is **empty for `h` even**; for `h` odd it occurs exactly when the
even part `E_{A_0}` is the constant `a_0` (all even-index coefficients of
`L_P` in degrees `2..h-1` vanish) and `P cap (-P) = 0`, with `c = 2 a_0`.

**(b) Descending: `Q != -P`.**  Then `A_0^pi != B_0^pi` and
`(A_0^pi, B_0^pi)` is a level-1 pair with band `<= floor(h/2)` (exactly
`h/2` for `h` even), multiplicities `<= 2`, and

```text
gcd( A_0^pi, B_0^pi ) = prod_{cross pairs} (Y - x^2),   squarefree,
```

where a **cross pair** is an antipodal pair `{x, -x}` with `x in P`,
`-x in Q`.  Sub-case: `R` antipodal-free (`R cap -R = 0`) iff `A_0^pi`,
`B_0^pi` are squarefree and coprime — a genuine pair of disjoint
`h`-subsets of `mu_{n/2}`.

*Proof.*  Diagonal `<=>` `Q = -P`: if `A_0^pi = B_0^pi` then the root
multisets satisfy `pi(P) = pi(Q)`.  A `y` of multiplicity 2 in `A_0^pi`
means `{w, -w} subset P`, so neither is in `Q` (disjointness), giving
multiplicity 0 in `B_0^pi` — contradiction; so all multiplicities are 1,
and for each `y` the unique preimages in `P` and in `Q` are distinct
elements of `{w, -w}`, i.e. `Q = -P`.  Converse: `pi(-P) = pi(P)`.

`h` even empty: `Q = -P` gives `L_Q(X) = L_P(-X)`, so `L_P - L_Q =
2 X * O_{A_0}(X^2) * (odd-part sign)`; a nonzero constant difference forces
`O_{A_0} = 0`, i.e. `P = -P`, contradicting `P cap Q = 0`.  `h` odd:
`L_Q(X) = -L_P(-X)`, so `L_P - L_Q = 2 E_{A_0}(X^2)`, constant iff
`E_{A_0}` constant, and the constant `2a_0 = c != 0` automatically
(`a_0 = +-e_h(P)`, a product of units).  Coset-union: immediate.

(b): multiplicity `<= 2` and the root description are D1(ii); the band is
D1(iv).  A common root `y` of the two pushforwards has a preimage in `P`
and a preimage in `Q`; they are distinct (disjointness), hence `{x, -x}`
with `x in P, -x in Q`, a cross pair, and each such `y` is simple on both
sides (multiplicity 2 on one side would put an antipodal pair inside `P`
and also meet `Q`).  QED

Verifier: S3a/S3b (all 352 trades at `(16, 3, F_17)`: 16 diagonal — all
`mu_2`-coset-unions — and 336 descending, every claimed invariant checked
per trade), S3c (all 126 trades at `(16, 4, F_17)`: zero diagonal).

## 5. The lift characterization (Lemma D4)

**Lemma D4.**  For monic degree-`h` `A` (level `k-1`) and `alpha`
(level `k`): `A^pi = alpha` iff the root multiset of `A` is a
**square-root selection** of that of `alpha`: for each root `y` of `alpha`
of multiplicity `m`, choose multiplicities `m_+ + m_- = m` for the two
preimages `+-w`.  The number of selections is exactly
`prod_y (m_y + 1) <= 2^h`, with equality `2^h` iff `alpha` is squarefree.
Equivalently, in coefficients: `A = E(X^2) + X*O(X^2)` with

```text
h even:  E^2 - Y O^2 = alpha,   E monic of degree h/2;
h odd :  Y O^2 - E^2 = alpha,   O monic of degree (h-1)/2.
```

*Proof.*  D1(ii) for the multiset statement; the count is the product over
distinct roots.  The coefficient form is `(-1)^h A(X)A(-X) =
(-1)^h (E(X^2))^2 - (-1)^h X^2 (O(X^2))^2`.  QED

This makes the naive multiplicity claim exact: **per level, per side, the
lift fiber is `prod (m_y + 1) <= 2^h`; per level `<= 4^h`** (the "2^{2h}
per level" of the node statement, now with the exact formula).

## 6. The terminal-lift collapse (Theorem D5) — the true bound

The last descent step is not a generic band step: the level-0 difference is
the rigid constant `c`.  That collapses the `4^h` naive fiber to `O(1)`.

**Theorem D5.**  Let `(alpha, beta)` be a level-1 pair, `D = beta - alpha`.
The level-0 trades `(A_0, B_0 = A_0 + c)` with `A_0^pi = alpha`,
`B_0^pi = beta` are obtained exactly as follows, and their number is

```text
h even:  <= 2      (and the two lifts are the antipodal flip pair
                    (P,Q) <-> (-P,-Q); they coincide iff P = -P);
h odd :  <= 4.
```

Procedure (`h` even): `deg D = h/2` is forced with `c =
[Y^{h/2}] D / 2` **unique**; then `E := (D - c^2)/(2c)` is forced (monic,
degree `h/2`, automatically); then `O^2 := (E^2 - alpha)/Y` is forced (the
division must be exact), and `O` is determined up to global sign — both
signs give monic `A_0 = E(X^2) + X O(X^2)`, and `B_0 := A_0 + c` then
pushes to `beta` **automatically** by the seed identity.  Procedure (`h`
odd): `D = -(2cE + c^2)` with `deg E <= (h-1)/2`; exactness of
`O^2 = (alpha + E^2)/Y` at the constant term forces

```text
c^4 + (2 D(0) + 4 alpha(0)) c^2 + D(0)^2 = 0,
```

a quadratic in `u = c^2` — at most 4 nonzero roots `c`; for each, `E` is
forced and `O` is forced **monic** (monicity of `A_0` fixes the sign), so
at most one candidate per `c`.  In both cases each candidate is then
subjected to the membership checks (both root sets in `mu_n`, squarefree,
sizes `h`); every genuine trade lift passes and is produced.

*Proof.*  Completeness: a trade lift satisfies the seed identity, so its
`(c, E_{A_0}, O_{A_0})` satisfy every displayed equation: `h` even — the
leading coefficient of `2cE + c^2` is `2c`, forcing `c`, then `E`, then
`O^2` by Lemma D4, `O` up to sign; `h` odd — eliminating `E(0)` between
`E(0) = -(D(0) + c^2)/(2c)` and the exactness condition
`alpha(0) + E(0)^2 = 0` (constant term of `Y O^2` is 0) gives the quartic;
per root, D4 forces the rest.  Soundness: reconstruction plus the seed
identity shows the candidate pushes to `(alpha, beta)`; the explicit
membership checks certify it is a trade.  The flip: `-P` has locator
`(-1)^h A_0(-X) = E(X^2) - X O(X^2)` (`h` even), which is the other sign
of `O`; `(-P, -Q)` is a trade with the same pushforward pair.  QED

Verifier: S5a/S5b — the solver output equals the brute-force
selection-times-selection lift on **every** bottom pair arising at
`(16, 3, F_17)` (218 pairs, max fiber observed 4 = the bound) and
`(16, 4, F_17)` (100 pairs, max fiber observed 2 = the bound; `c` unique).

**Multiplicity accounting (node item iv), assembled.**  Per bottom pair at
depth `k`: at most `4^h` chains per intermediate level (Lemma D4, exact
formula `prod (m+1)` per side) times the terminal collapse:

```text
lifts per bottom pair <= 4^{h(k-1)} * 2   (h even),
                          4^{h(k-1)} * 4   (h odd);
k = 1:  <= 2  resp.  <= 4.
```

Intermediate levels do not admit the same clean collapse (the band
difference is a polynomial, not a constant; the resulting quadratic
coefficient system for the B-side increment is overdetermined but its
solution count is only Bezout-bounded — GAP G-C3 in section 9).  For the
practical certificates (`k = 1`, `h = 4, 5, 6`) the terminal collapse is
the whole story: **per-candidate cost is O(1), not `2^{2h}`**.

## 7. The injection (Theorem D6) and soundness (Theorem D7)

Fix, once and for all, the exponent section: level-`k` roots are written
`g_k^e`, `g_k = g^{2^k}` for a fixed generator `g` of `mu_n`, and the two
preimages of exponent `e` are the exponents `e` and `e + n_k` at level
`k-1`.  **Selection data** `sigma_k` for `A_{k-1}` over `A_k` records, for
each root of `A_k`, the multiplicity split between the two preimage
exponents (Lemma D4).

**Theorem D6 (injection).**  For any `k >= 1` the map

```text
Phi : (level-0 trade)  |->  ( (A_k, B_k),  (sigma_j, tau_j)_{j=1..k} )
```

is **injective**, with linear-time inverse: `A_{j-1}` is reconstructed from
`(A_j, sigma_j)`, downward from the bottom pair.  *Proof.*  By Lemma D4
the selection data determines the level-`(j-1)` multiset from the
level-`j` one; induction from `(A_k, B_k)` reconstructs `(A_0, B_0)`,
hence `(P, Q)`.  Two trades with equal image reconstruct identically.  QED
(Verifier: S4 — 704 oriented trades at `(16,3,F_17)` map to 704 distinct
keys and every roundtrip is exact.)

**Theorem D7 (soundness of the certificate algorithm).**  Fix `(n, h, F)`,
a depth `k >= 1`, and let `delta_k`, `sig(h,k)` be as in Lemma D2.  Define
the **bottom census**

```text
C_k = { ordered pairs (alpha, beta) : monic degree h, root multisets in
        mu_{n_k}(F) with multiplicity <= 2^k, alpha != beta,
        deg(beta - alpha) <= delta_k }
```

(equivalently: bucket all such multisets by their first `sig(h,k)`
elementary symmetric functions and take distinct in-bucket pairs).  Let
`j0(T) in {1, ..., k, infinity}` be the first level at which a trade `T`'s
descent chain collides (`A_j = B_j`).  Then every level-0 `h`-trade `T`
over `F` is captured by exactly one branch:

1. **`j0 = 1` (paid):** `T` has `Q = -P` (Lemma D3(a)) — imprimitive,
   coset-union, charged to the paid ledger; only possible for `h` odd; at
   depth-1 it is enumerable per level-1 multiset at cost `<= 2^h`.
2. **`2 <= j0 <= k` (collision):** the level-`(j0-1)` pair of `T` is a
   member of the **non-diagonal** census `C_{j0-1}` (it has band
   `delta_{j0-1}` and `A_{j0-1} != B_{j0-1}`); `T` is recovered there by
   the depth-`(j0-1)` lift checks.
3. **`j0 > k` (full descent):** the bottom pair of `T` lies in `C_k` and
   `T` is recovered by the depth-`k` lift chain (Lemma D4 selections with
   the band check `deg(B_j - A_j) <= delta_j` at every level `j < k`, and
   Theorem D5 at the last step).

**Consequently:** if the lift checks fail on every censused pair of
`C_1, ..., C_k` and the paid branch is accounted, then **no level-0
`h`-trades over `F` exist beyond the paid classes**.  When collisions are
excluded up to depth `k` (Lemma D8 below), only the single bottom census
`C_k` is needed: *bottom census empty modulo paid classes + per-candidate
lift failure  =>  no level-n trades* — the node's item (iii), with exact
parameters `k* = min( ceil(log2 h) - 1, s - log2(n_bottom) )`,
`delta_{k*} = h - ceil(h/2^{k*})`, `n_{k*} = n/2^{k*}`.

*Proof.*  The branches are exhaustive and mutually exclusive by definition
of `j0` and Lemma D3(a) (`j0 = 1 <=> Q = -P`).  Branch 2: minimality of
`j0` gives `A_{j0-1} != B_{j0-1}`; Lemmas D1-D2 give the band and
multiplicity constraints, so the pair is censused.  Branch 3: same at
depth `k`.  Recovery in branches 2-3 is Theorem D6 + D5 completeness.  QED

**Lemma D8 (collision exclusion by 2-adic valuation).**  If `2^j | h` then
**no** level-0 trade collides at level `j` (`A_j != B_j`).  Hence for
`h = 2^a m` (`m` odd) the descent is collision-free through depth
`v_2(h) = a`; in particular for 2-power `h` the entire informative range
`k <= k*(h) = log2(h) - 1 < v_2(h)` is collision-free, and Theorem D7
needs only the bottom census.

*Proof.*  Induction on `j`: claim that if `2^j | h` then `D_j := B_j - A_j`
has exact degree `d_j = h (2^j - 1)/2^j` and leading coefficient
`+- 2^j c != 0`.  Base `j = 1`: seed identity, `D_1 = +-(2c E_{A_0} +
c^2)`, `E` monic of degree `h/2` (`h` even).  Step: a collision at level
`j+1` means `Abar_j D_j + A_j Dbar_j + D_j Dbar_j = 0`; the coefficient
at degree `h + d_j` is `((-1)^h + (-1)^{d_j}) lc(D_j)` (the `D Dbar` term
has degree `2 d_j < h + d_j`); `h` even and — using `2^{j+1} | h` —
`d_j = (h/2^j)(2^j - 1)` even, so this is `2 * lc(D_j) = +- 2^{j+1} c
!= 0` in characteristic `!= 2`: no collision, and the same computation
gives `deg D_{j+1} = (h + d_j)/2 = h(2^{j+1}-1)/2^{j+1}` with leading
coefficient `+- 2^{j+1} c`.  QED

(For `h` odd, only the `j0 = 1` branch is controlled (Lemma D3(a));
level-2 collisions are not excluded — GAP G-C2.  Verifier: S9 — on all 28
trades at `(32, 4)`: `deg D_1 = 2` exactly and no level-2 collision.)

## 8. Validation and honest feasibility at n = 1024

### 8.1 Toy pipeline gates (all PASS)

| gate | world | census + lift result |
|---|---|---|
| S6 | `32 -> 16, h=4, p=32801 (> n^3, 1 mod 32)` | recovered = direct census exactly: 28 trades, all toral (= pilot char-0 count), non-toral **0** |
| S7 | `64 -> 32, h=4, p=262337 (> n^3, 1 mod 64)` | recovered = direct census exactly: 120 toral (= pilot), non-toral **0** |
| S8 | `16 -> 8, h=3, F_17` (heavily exceptional row) | recovered = direct census exactly: **352** trades incl. 16 diagonal `Q = -P` trades via the paid-branch routine |

The toral pairs are recovered exactly through the descent, and the
non-toral residue is empty at both `h=4` ends — the node's validation
demand.  The `(16,3,F_17)` world deliberately tests the pipeline where
p-specific non-toral trades are dense (336 descending + 16 paid), and the
recovery is still exact.  Incidental finding: `p = 17` is also exceptional
at `(16, 4)` — 126 trades vs the char-0 count 6 (all gates run over this
exceptional row too).

### 8.2 Feasibility (the honest correction)

The theorem chain is uniform in `h` (valid to `h = A = 261` and any depth
`k <= s`), but the certificate's cost is the bottom-census hash mass
`#multisets(n_k, h, mult <= 2^k) ~ C(n_k + h - 1, h)`, bucketed by
`sig(h,k)` symmetric functions.  Against the campaign's demonstrated
comfort scale (~`2^35` hash entries, C1a):

| h | k | n_k | delta_k | sig | census mass | verdict |
|---|---|---|---|---|---|---|
| 4 | 1 | 512 | 2 | e_1 | `C(515,4) ~ 2^31.4` | **feasible**; lifts <= 2/pair |
| 5 | 1 | 512 | 2 | e_1,e_2 | `~ 2^38.1` | marginal |
| 5 | 2 | 256 | 3 | e_1 | `~ 2^33.2` | hash feasible; e_1-only pair mass data-dependent; level-2 collision branch open (G-C2) |
| 6 | 2 | 256 | 4 | e_1 | `~ 2^38.6` | marginal; G-C2 (h = 2 mod 4) |
| 7 | 2 | 256 | 5 | e_1 | `~ 2^41.5` | infeasible |
| 8 | 1 | 512 | 4 | e_1..e_3 | `~ 2^56.8` | infeasible |
| 8 | 2 | 256 | 6 | e_1 | `~ 2^48.9` | infeasible (though collision-free to depth 3 by D8) |
| >=9 | any | — | — | — | worse | infeasible |

**Verdict:** C1b delivers `h = 4` now (bottom `n = 512`, band 2, one
shared coefficient, `<= 2` lift checks per candidate pair), `h = 5, 6`
with engineering margin, and **nothing above** — the DAG's "descent covers
h <= ~8-10" was optimistic.  The uncovered range for the (A) closure is
therefore `h in (6, A]` (nominally `(10, A]`), handled in
the sibling `midlarge_h_certification` residue.  Anchoring (`1 in R`,
A3 sec 1.3) gives a
constant-factor reduction (the 1-slot selection is forced at every level)
but does not change the verdicts.

## 9. Gap ledger

- **G-C1 [scope]:** soundness (Theorem D7) is per-field.  For the (A)
  closure it must be run per official prime (mod-p bottom census), or over
  `K` with the pilot's exact engines at reachable sizes; it does not by
  itself produce the char-0-to-F_q bridge (that is A3's job; the two
  compose: A3 needs `D(n,h)`, C1b is a candidate producer of the emptiness
  side at fixed rows).
- **G-C2 [named gap]:** level-`j >= 2` collisions (`A_j = B_j` with
  earlier non-collision) are excluded only when `2^j | h` (Lemma D8).  For
  other `h` the collision branches must be censused at their level
  (Theorem D7 branch 2), whose cost at scale is not priced here; for
  `k = 1` (the `h = 4, 5, 6` designs) the issue is vacuous — only the paid
  `j0 = 1` branch exists and is classified exactly (Lemma D3(a)).
- **G-C3 [named gap]:** no clean intermediate-level lift collapse: between
  levels the per-pair fiber bound is the exact selection count `<= 4^h`,
  not `O(1)`; Bezout-type improvement not proved.  Only relevant for
  `k >= 2` designs.
- **G-C4 [feasibility]:** the `h = 5` depth-2 and `h = 6` designs have
  data-dependent census pair mass (single shared symmetric function);
  bounded in the toys, unpriced at `n = 1024`.
- No citations are load-bearing: every input is proved inline or banked
  in-repo (x81, x83, X24, A3, pilot data).

## 10. Verification

```bash
python3 experimental/scripts/verify_c1b_descent_injection.py
```

Sections S1-S9 (Part 1) and S10-S12 (Part 2 support, see
`midlarge_h_routes.md`).  Current replay: **20 PASS, 0 FAIL** (~20 s,
<300 MB peak).
