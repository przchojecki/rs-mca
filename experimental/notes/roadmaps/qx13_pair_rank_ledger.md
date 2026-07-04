# QX.13 — the pair-rank ledger: c(s,t) = min(s, t-1) (DAG node `xr_ledger_qpower`)

- **Status:** PROVED (Theorems 1–3 below carry full elementary proofs;
  every exact claim is machine-checked at toy scale by exact enumeration —
  no Monte Carlo anywhere) / MOMENT-LEVEL scope only (see S7). This note is
  the repo-standard packaging that `qx14_xr_coverage_table.md` S0.3 pins as
  an INPUT and flags as "[CITATION NEEDED — QX.13 packaging is the intended
  fix]". The mathematical content of that pin is discharged here; the qx14
  text itself is not edited by this packet.
- **Provenance (per execution_queue QX.13):** the derivation was externally
  provided (GPT Pro) and independently checked by the roadmap lane (hand
  algebra + Monte Carlo). This note replaces that provenance with a full
  written proof plus a deterministic exact verifier.
- **DAG node:** `xr_ledger_qpower` (execution_queue Tier D6, QX.13).
- **Parents:** `m1_support_coefficient_test.md` (alignment normal form,
  PROVED), `proof_sketch/s2_paid_ledger.md` SS2 (Lemma FM1 conventions),
  `m1_t2_one_exchange_residual_degree.md` (#152, the t=2 exchange packet).
- **Consumers:** `qx14_xr_coverage_table.md` S0.3/S2 (the pinned
  pair-correlation ledger — consumed verbatim), `proof_sketch/
  s3b_iii_2_displacement_spectral.md` SS5 (averaged XR), the Q3R.1 / X-1
  slack composition (pair-ledger input).
- **Verifier:** `python3 experimental/scripts/verify_qx13_pair_rank_ledger.py`
  (standalone python3, stdlib only, deterministic; exit 0 iff green).

## 0. Pinned notation

### 0.1 Row and support conventions (as in qx14 S0.1 / s2)

Row `(n, k, q)`: `C = RS[F, D, k]` with `D subset F`, `|D| = n`,
`q = |F|` (any prime power; toys below include non-prime fields). Exact
agreement `A = k + t` with `t >= 1`; co-support size `j = n - A`. Supports
are subsets `S subset D` of size exactly `A`; co-supports `D \ S` are the
vertices of `J(n, j)`. For two supports `S, T` of size `A`, the exchange
distance is

```text
s = |S \ T| = |T \ S|,        r = |S cap T| = A - s,
1 <= s <= min(A, n - A)   for S != T,
```

and `s` equals the `J(n,j)` exchange distance of the co-supports
(`(D\S)\(D\T) = T\S`). Note the arithmetic constraint `n >= A + s >= 2s`.

### 0.2 The alignment normal form (support-coefficient test)

For a word `w : D -> F`, `I_S(w)` is the unique polynomial of degree `< A`
agreeing with `w` on `S`, and

```text
Pi_S(w) = (coeff_X^k I_S(w), ..., coeff_X^(A-1) I_S(w)) in F^t
```

is the top-coefficient obstruction (`m1_support_coefficient_test.md`,
PROVED). `Pi_S` is linear in `w` and depends only on `w|_S`; `w|_S` is
explained by a degree-`< k` polynomial iff `Pi_S(w) = 0`. Write

```text
K_S = ker Pi_S <= F^D        (codim t; Lemma A below).
```

For line data `(u, v)` (base `u`, direction `v`), the alignment event is

```text
Align(S) = { Pi_S(v) != 0  and  exists z in F : Pi_S(u) + z Pi_S(v) = 0 }.
```

By the support-coefficient test this is exactly "`S` witnesses a
support-wise bad slope", the slope `z(S)` is then unique, and each support
contributes at most one bad slope. `X = X_{u,v}(A)` = number of aligned
supports at exact agreement `A` (qx14 S0.1 currency). FM scale (Lemma FM1,
s2 SS2): for `(u, v)` uniform and independent,

```text
E[X] = C(n,j) (1 - q^-t) q^(1-t)   exactly,   so   E[X] <= C(n,j) q^(1-t).
```

### 0.3 Probability space and the restriction remark

Throughout, `(u, v)` is uniform on `F^D x F^D` with `u, v` independent —
every probability in this note is an average over the line data
(MOMENT-LEVEL; see S7). All events below depend on `(u, v)` only through
the restrictions to `S union T` (since `Pi_S(w)` depends only on `w|_S`),
so probabilities over `F^D` equal probabilities over `F^(S union T)`; the
verifier enumerates the latter.

## 1. Warm-up: single-support rank [PROVED]

**Lemma A.** For any support `S` of size `A = k + t`, the map
`Pi_S : F^S -> F^t` is surjective, with kernel of dimension `k` (namely
`{f|_S : deg f < k}`). Consequently, for `w` uniform, `Pi_S(w)` is uniform
on `F^t` and `P[w in K_S] = q^-t` exactly.

*Proof.* Interpolation `I_S : F^S -> F[X]_{<A}` is a linear bijection
(existence and uniqueness of the interpolant on `A` distinct points), and
extraction of the coefficients in degrees `k..A-1` is a surjective linear
map `F[X]_{<A} -> F^t`. So `Pi_S`, their composition, is surjective. Its
kernel is `{w : deg I_S(w) < k} = {f|_S : deg f < k}`, and restriction of
degree-`< k` polynomials to `A >= k` distinct points is injective, so the
kernel has dimension exactly `k`. A surjective linear map pushes the
uniform distribution to the uniform distribution (all fibers are cosets of
the kernel, hence equinumerous). QED.

This re-proves the surjectivity step of Lemma FM1 (s2 SS2) in the
coefficient normal form; the FM1 probability
`P[Align(S)] = (1 - q^-t) q^(1-t)` follows as there and is re-checked
exactly by the verifier on every toy cell.

## 2. Theorem 1: the pair rank / codimension formula [PROVED]

**Theorem 1.** Let `S, T` be supports of size `A = k + t` at exchange
distance `s >= 1`, and let

```text
Phi_{S,T} : F^(S union T) -> F^t x F^t,    w -> (Pi_S(w), Pi_T(w))
```

be the joint syndrome map. Then

```text
rank Phi_{S,T} = t + min(s, t),
codim(K_S cap K_T) = t + min(s, t)        (in F^D, equivalently on S u T),
P[w in K_S cap K_T] = q^-(t + min(s,t))   exactly, for w uniform.
```

Moreover `|ker Phi_{S,T}| = q^k` when `s <= t` and `q^(2k-r)` when
`s > t` (`r = A - s`).

*Proof.* Note `|S union T| = A + s = k + t + s`, and `r >= k` iff
`s <= t`. The kernel of `Phi_{S,T}` is the set of `w` on `S union T` that
are explained by some degree-`< k` polynomial on `S` AND by some
degree-`< k` polynomial on `T`. Count it in the two cases.

**Case `r >= k` (i.e. `s <= t`).** Suppose `w|_S = f|_S` and
`w|_T = g|_T` with `deg f, deg g < k`. Then `f` and `g` agree on the
`r >= k` points of `S cap T`; their difference has degree `< k` and
`>= k` roots, hence `f = g`. So the kernel event is "one degree-`< k`
polynomial explains all of `S union T`", and the kernel is
`{f|_(S u T) : deg f < k}`. Distinct `f` restrict to distinct words
(`|S u T| >= A >= k`), so the kernel has exactly `q^k` elements and

```text
rank = (k + t + s) - k = t + s = t + min(s, t).
```

**Case `r < k` (i.e. `s > t`).** Pair counting. Given `w` in the kernel,
the explaining `f` (on `S`) and `g` (on `T`) are unique (Lemma A kernel
injectivity on `>= k` points), so kernel words correspond bijectively to
pairs `(f, g)` of degree-`< k` polynomials with `f = g` on `S cap T`
(the word is `w = f` on `S`, `w = g` on `T \ S`; consistent on `S cap T`).
Count the pairs: `q^k` choices of `f`; given `f`, the set
`{g : deg g < k, g = f on S cap T}` is an affine subspace of dimension
`k - r` (evaluation of degree-`< k` polynomials at `r < k` distinct points
is surjective with kernel of dimension `k - r`). Hence exactly
`q^k * q^(k-r) = q^(2k-r)` kernel words, and

```text
rank = (k + t + s) - (2k - r) = t + s + r - k = 2t = t + min(s, t),
```

using `r = k + t - s`. In this case `Phi_{S,T}` is SURJECTIVE onto
`F^t x F^t` — the two syndromes are independent uniform (the
**independence plateau**).

In both cases, the probability statement follows from linearity: all
fibers of `Phi_{S,T}` are kernel cosets, so
`P[Phi = 0] = q^(-rank)` exactly; and `codim(K_S cap K_T)` in `F^D`
equals `rank Phi_{S,T}` because `Phi` factors through the restriction to
`S union T`. The boundary `s = t` is consistent: `t + s = 2t`. QED.

Probability forms, per the two cases:

```text
s <= t:  P = q^k / q^(k+t+s)      = q^-(t+s)    ("one polynomial explains S u T")
s >  t:  P = q^(2k-r) / q^(k+t+s) = q^-2t       (independence plateau, exact).
```

## 3. Theorem 2: all-slope accounting [PROVED]

For `z in F` write `U_z = u + z v`; by linearity of interpolation,
`Pi_S(U_z) = Pi_S(u) + z Pi_S(v)`.

**Theorem 2.** For `(u, v)` uniform independent and `S, T` supports of
size `A = k + t` at exchange distance `s >= 1`:

```text
(2a)  for each fixed z:      P[ Pi_S(U_z) = 0 and Pi_T(U_z) = 0 ]  = q^-(t+min(s,t))  exactly;
(2b)  for each fixed z != z': P[ Pi_S(U_z) = 0 and Pi_T(U_z') = 0 ] = q^-2t            exactly;
(2c)  P[ Align(S) and Align(T) ]  <=  q^(1-t-min(s,t)) + q^(2-2t).
```

*Proof.* (2a) For fixed `z`, `U_z = u + z v` is uniform on `F^D` (condition
on `v`: `u` is uniform and independent, and translation preserves the
uniform distribution). The event is `U_z in K_S cap K_T`, which has
probability exactly `q^-(t+min(s,t))` by Theorem 1.

(2b) For `z != z'`, the map `(u, v) -> (U_z, U_{z'})` is the invertible
linear change of variables given coordinatewise by the matrix
`[[1, z], [1, z']]` with determinant `z' - z != 0`. An invertible linear
map preserves the uniform distribution on `F^D x F^D`, so `U_z` and
`U_{z'}` are INDEPENDENT and uniform. Hence

```text
P[Pi_S(U_z) = 0 and Pi_T(U_z') = 0] = P[U_z in K_S] P[U_z' in K_T] = q^-t q^-t,
```

using Lemma A for each factor separately.

(2c) On the event `Align(S) and Align(T)` the bad slopes `z(S), z(T)`
exist (each unique). Split by `z(S) = z(T)` or not:

```text
{Align(S), Align(T), z(S) = z(T)}  subset  Union_z {Pi_S(U_z) = 0, Pi_T(U_z) = 0},
{Align(S), Align(T), z(S) != z(T)} subset  Union_{z != z'} {Pi_S(U_z) = 0, Pi_T(U_z') = 0},
```

since `Pi_S(u) + z Pi_S(v) = Pi_S(U_z)`. The union bound over `q` slopes
in the first branch gives `q * q^-(t+min(s,t))`, and over `q(q-1) <= q^2`
ordered pairs in the second gives `q(q-1) q^-2t <= q^(2-2t)`. Add. QED.

Only the slope unions are inequalities; the per-slope probabilities (2a),
(2b) are exact equalities, and the verifier checks them as exact integer
counts for every `z` (resp. every ordered pair `z != z'`) on the toys.

## 4. Theorem 3: packaging, and the ledger exponent c(s,t) = min(s, t-1) [PROVED]

**Theorem 3 (packaging inequality).** For every integer `q >= 2`,
`t >= 1`, `s >= 0`:

```text
q^(1-t-min(s,t)) + q^(2-2t)  <=  2 q^(1-t-min(s,t-1)),
```

with EQUALITY if and only if `s = t - 1`, and strict inequality otherwise.

*Proof.* Put `a = min(s, t)`, `b = min(s, t-1)` and multiply through by
`q^(t-1+a) > 0`; the claim becomes `1 + q^(1-t+a) <= 2 q^(a-b)`.

Case `s <= t - 1`: then `a = b = s`, and the claim reads
`1 + q^(1+s-t) <= 2`, i.e. `q^(1+s-t) <= 1`, i.e. `s <= t - 1`: true, with
equality iff `s = t - 1` (for `s < t - 1` the exponent is negative and the
inequality is strict since `q >= 2`).

Case `s >= t`: then `a = t`, `b = t - 1`, and the claim reads
`1 + q <= 2q`, i.e. `1 <= q`: true, strict for `q >= 2`. QED.

**Definition (the pair-rank ledger exponent).**

```text
c(s, t) = min(s, t - 1).
```

**Corollary (net suppression at the FM scale).** For supports at exchange
distance `s >= 1`,

```text
P[Align(S) and Align(T)]  <=  2 q^(1-t) q^(-c(s,t)):
```

relative to the single-support FM scale `q^(1-t)`, every ordered pair at
exchange distance `s` pays at least `min(s, t-1)` extra `q`-powers. This
is exactly the pinned input of qx14 S0.3 (which consumes the unpackaged
two-branch sum of Theorem 2 plus this packaging inequality verbatim).

Remarks on the shape of `c`:

- **Why `t - 1` and not `t`:** the distinct-slope branch is exactly the
  square of the FM scale, `q^(2-2t) = (q^(1-t))^2` — two independent
  FM-scale alignments. No exchange-distance ledger can suppress below the
  product of two singleton events, so the suppression saturates at
  `t - 1`, and the saturation is reached already at `s = t - 1` (the
  equality case of Theorem 3; the constant `2` is sharp there, the two
  branches contributing equal mass at the exponent level).
- **Head regime `s <= t - 1`:** the same-slope branch dominates and the
  exponent is exactly `s` (one `q`-power per exchange step) — Theorem 1's
  `q^-(t+s)` case ("one polynomial explains `S u T`").
- **`t = 1` is vacuous:** `c(s, 1) = 0` — the ledger gives NO suppression
  at `t = 1` (both branches are already at the `q^0 x FM` scale).
- `c(0, t) = 0` is consistent with the diagonal (`S = T`), where the
  correct statement is FM1 itself; `c` is only used for `s >= 1`.

## 5. Base case: c(1, 2) = 1 and the #152 exchange packet

`c(1, 2) = min(1, 1) = 1`: at `t = 2`, a one-exchange pair (`s = 1`) pays
exactly one extra `q`-power,
`P[Align(S) and Align(T)] <= 2 q^(-1) * q^(1-t) = 2 q^-2`, driven by the
same-slope rank `t + min(s,t) = 3` (Theorem 1 head case).

The grounded worst-case cousin of this row is the #152 exchange packet
(`m1_t2_one_exchange_residual_degree.md`, PROVED-LOCAL): in the `t = 2`
Hankel-pencil normal form, after fixed-slope root slices are charged,
every `(j-1)`-core supports at most one residual one-exchange edge
(`Delta(G_1(A_res)) <= j`). Honest relationship: the two statements live
at different quantifiers — #152 is structural/per-line (fixed line data,
after charging), this note's row is moment-level (averaged over `(u,v)`)
— and NEITHER implies the other. They agree in direction: one-exchange
multiplicity at `t = 2` is suppressed/structured rather than free. The
pair (#152, this row) grounds the `(s, t) = (1, 2)` corner of the ledger
from both the worst-case and the average-case side.

## 6. Bridge-ledger row (support-collinearity model vs LD_sw split-locator conventions)

```text
model here:      support-collinearity / support-wise. Align(S) = "S
                 witnesses a support-wise bad slope for the line (u,v)" —
                 exactly the per-support event of the LD_sw numerator in
                 the m1_support_coefficient_test.md normal form; at most
                 one bad slope per support, so X upper-bounds per-A slope
                 counts and this note prices B_ap(A)-side pair mass in the
                 s2 ledger's currency (same bridge row as qx14 S6).
import direction: FORWARD ONLY. Per m2_ldsw_line_decoding_separation.md
                 (PROVED lemmas + finite counterexample): ABF/GG
                 (delta, a_LD, b) line-decodability => LD_sw bound =>
                 epsilon_mca bound, but LD_sw-side bounds do NOT imply the
                 ABF/GG assignment-collinearity (split-locator) conclusion
                 — the code-direction invisibility lemma makes LD_sw blind
                 to codeword directions. Nothing in this packet may be
                 read backward as split-locator/list-decoding control.
coset sanity:    the model inherits the m2 note's direction-coset
                 invariance: for c in C, Pi_S(v + c) = Pi_S(v) (I_S(v+c) =
                 I_S(v) + c and deg c < k contributes nothing in degrees
                 k..A-1), so Align and the pair bounds see v only mod C —
                 consistent with LD_sw seeing the direction only mod C.
```

## 7. Non-claims (honesty ledger)

- **MOMENT-LEVEL only.** Every probability is an average over uniform
  independent `(u, v)`. The worst-case/fixed-line conversion — turning
  pair-moment control into a statement about THE line at hand — is the
  KMS/globalness branch (QX.10–QX.12) and is untouched here. This note
  supplies the ledger input of the `xr_distance_dichotomy` split, nothing
  more.
- Upper bounds only on the union side: (2a)/(2b) are exact per-slope, but
  the slope unions (2c) and the packaging (Theorem 3, except at
  `s = t - 1`) are one-sided. No matching lower bound for
  `P[Align(S) and Align(T)]` is claimed.
- `t = 1` rows get zero suppression (`c(s,1) = 0`); the ledger is
  contentful only for `t >= 2`.
- No structured absorption: paid (tangent/quotient) mass is not subtracted
  from the pair mass (same conservative stance as qx14).
- The #152 row (S5) is a consistency anchor, not a derivation, in either
  direction.
- No published external reference for `c(s,t) = min(s,t-1)` is known to
  this repo; this note itself is the in-repo proof and is what qx14 S0.3's
  "[CITATION NEEDED]" pointer anticipated. No new external citations are
  introduced.
- Verifier scope honesty: with `q <= 7` the geometry `n >= A + s >= 2s`
  makes `s = 4` IMPOSSIBLE (would need `n >= 8 > q >= n`); the verifier
  proves this arithmetic fact, covers `s = 1..3` by full word enumeration
  at `q in {4, 5, 7}` (plus GF(4) for a non-prime field), and certifies
  the `s = 4` rows exactly on GF(8)/GF(9)/F_11 toys with `n <= 10` via
  Gaussian-elimination rank plus kernel-span enumeration (exact, not
  Monte Carlo). Toy scale only; the theorems themselves are proved for
  all `(n, k, q, s, t)` in S2–S4.
- Everything is per ordered pair `(S, T)` at fixed exact agreement `A`.
  The summed second-moment assembly `E[X^2]` is qx14 S2's job (it
  consumes Theorem 2 + Theorem 3 verbatim); no `E[X^2]` claim is made
  here.

## 8. Verifier

`experimental/scripts/verify_qx13_pair_rank_ledger.py` — standalone
python3, stdlib only, deterministic, exit 0 iff green. Check groups:

```text
[0] field axiom tables for F_5, F_7, F_11, GF(4), GF(8), GF(9) (full
    triple loops), and Lagrange basis delta-property per cell;
[1] Theorem 1 EXACTLY: for a sweep of cells (q <= 11, n <= 10, s = 1..4,
    both codim cases), every (S, T) pair at distance s in the toy domain
    has joint rank t + min(s,t) (Gaussian elimination over the field) and
    single-support rank t; per-cell kernel certificates: kernel dimension
    m - t - min(s,t), full kernel-span enumeration maps to zero with
    q^(dim) distinct elements, and — for every q <= 7 cell — full
    enumeration of ALL q^|S u T| words confirms the kernel count
    q^k (head case) / q^(2k-r) (plateau case) exactly;
    plus the s = 4 impossibility arithmetic at q <= 7;
[2] Theorem 2 EXACTLY on toys: exact syndrome distribution from full word
    enumeration (fiber uniformity = uniformity on the image), then exact
    weighted pair accounting: FM1 alignment probability per support,
    per-z same-slope probability q^-(t+min(s,t)) for EVERY z, per-(z,z')
    distinct-slope probability q^-2t for EVERY ordered pair, and the
    (2c) chain including Theorem 3's right-hand side — all as exact
    Fractions;
[3] Theorem 3 for t <= 6, s <= 8: symbolic case reduction (the two
    exponent regions proved in S4, checked as integer conditions valid
    for all q >= 2) plus exact Fraction evaluation over a battery of
    prime-power q up to 2^31, with the equality case s = t-1 checked as
    exact equality and all other cases checked strict;
[4] the base case c(1,2) = 1 with the exact flagship pair probability
    against 2 q^-2.
```
