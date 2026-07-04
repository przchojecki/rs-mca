# Conjecture F, Fiber-Side Scoped Proof (Coordinate/Prefix Planes)

- **Status:** PROVED-LOCAL (elementary, unconditional) + EXPERIMENTAL verifier.
  Honest scope in §5: polynomial only in the logarithmic-reserve regime.
- **DAG nodes:** `f_termination_mds` (discharged: §3 is exactly its statement —
  shortened-MDS dual, no words below the Singleton range, moment count immediate)
  and `f_spread_moment_count` (supplied for the coordinate-prefix family by
  Theorem A′/Corollary B). NOT closed: `f_dual_distance_frame` (QF.6's general
  frame stays conditional for non-MDS families; this note discharges its
  hypothesis only on the prefix family). Roadmap QF.10, the branch-(a) attempt.
- **Roadmap links:** `experimental/notes/roadmaps/execution_queue.md` (QF.10, QF.6);
  `experimental/notes/audits/f_consumer_scoped_audit.md` (QF.9, branches a/b);
  `experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md`
  (`prob:perfiber` = Conjecture F on prefix/coordinate planes).
- **Parent frame:** Corollary 6C of `conjecture_f_reduction_lemmas.md`, the
  dual-distance moment frame, which is *conditional* on a dual-distance gap.
  This note discharges that hypothesis unconditionally for the prefix family.
- **Verifier:** `experimental/scripts/verify_conjecture_f_fiber_scoped.py`.

This settles the **branch-(a)** instance of Conjecture F flagged by the QF.9
audit: the coordinate/prefix-plane fibers of the elementary-symmetric prefix
map. It does not touch branch (b) (Hankel-pencil kernel planes; QF.14 / the
displacement identities), and it is polynomial only for logarithmic reserve
(§5), so it does not close `prob:perfiber`'s hard regime.

## 1. Object: prefix fibers of `D_j(H)`

Let `K` be a field and `H subset K` a set of `n = |H|` distinct elements,
`P_H(X) = prod_{h in H}(X - h)`. For `0 <= j <= n`,

```text
D_j(H) = { L_S : S subset H, |S| = j },   L_S(X) = prod_{h in S}(X - h)
       = X^j - e_1(S) X^{j-1} + ... + (-1)^j e_j(S),
```

the monic squarefree degree-`j` divisors of `P_H`; `e_i(S)` = `i`-th elementary
symmetric function. Fix a prefix length `0 <= sigma <= j`, set the **reserve**
`d = j - sigma`, and let `Phi_sigma(S) = (e_1(S),...,e_sigma(S)) in K^sigma`. For
`p in K^sigma` the **prefix fiber** is

```text
E_p = { S in binom(H,j) : Phi_sigma(S) = p }.
```

In locator-coefficient space `E_p = D_j(H) cap P(W)`, where `P(W)` is the
coordinate plane pinning the `X^j,...,X^{j-sigma}` coefficients (monic + prefix
`p`); it has projective dimension `d`, with direction space
`V = K[X]_{<= d-1}` (`dim V = d`). This is `prob:perfiber`'s object: the `e_i`
are the first locator coefficients, so its fibers are prefix/coordinate planes.

## 2. Theorem (fiber-side scoped Conjecture F)

**Theorem A (sharp fiber bound, unconditional).** For every `p in K^sigma`,

```text
#E_p  <=  binom(n, d) / binom(j, d)  =  binom(n, j - sigma) / binom(j, sigma).
```

**Theorem A' (r-wise moment form).** For every `0 <= r <= d` and every `p`,
`#E_p <= binom(n,r) * binom(n-r,d-r) / binom(j,r)`; `r = d` gives Theorem A.
This is Corollary 6C with its dual-distance hypothesis now a theorem (§3), so it
holds for the whole prefix family without exception ("moments wholesale").

**Corollary B (poly iff logarithmic reserve).** If `j >= theta n` for a constant
`theta in (0,1]` and `d <= theta n / 2`, then `#E_p <= (2/theta)^d`. Hence at
constant rate and reserve `d = j - sigma = O(log n)`, `#E_p = n^{O(1)}` is
polynomial: `prob:perfiber` for prefix planes over `K`, proved unconditionally,
in the logarithmic-reserve (`sigma = j - O(log n)`, i.e. `d = O(log n)`) end.

## 3. The MDS input: shortened-RS duality (Singleton), unconditionally

**Lemma (no sparse dual word).** For any `S, S' in E_p`, `L_S - L_{S'} in V`
(degree `<= d - 1`). Equivalently the difference code
`ev_H(V) = {(v(h))_{h in H} : v in V} = RS_H[n,d]` is the Reed-Solomon code of
length `n`, dimension `d`, which is MDS (minimum distance `n - d + 1`); its dual
has minimum distance `d + 1`, so no `d` points of `H` carry a dependence on `V`.

**Proof.** `L_S, L_{S'}` are monic degree `j`, so `X^j` cancels; the
`X^{j-1},...,X^{j-sigma}` coefficients are the same functions of the shared
prefix `p`; hence `deg(L_S - L_{S'}) <= j - sigma - 1 = d - 1`. Independence of
`d` evaluation functionals on `V` is the non-vanishing of the Vandermonde
determinant `det[t^i]_{t in T, 0<=i<d} = prod_{t<t'}(t' - t) != 0` on `d`
distinct points, i.e. the defining MDS/Singleton property of `RS_H[n,d]`; by
MDS-duality the dual distance is `d + 1 > d`. []

This is the QF.9 chain made unconditional: *shortened RS (the low-degree
difference code) => large dual distance (Singleton) => no sparse dual words =>
the Corollary 6C hypothesis `w_* > r` holds for all `r <= d`.* The prefix
constraints shorten the full locator code `RS_H[n,j+1]` down to `RS_H[n,d]` by
fixing the top `sigma` coefficients; a shortened Reed-Solomon code is again MDS,
so the coordinate-plane form *forces* the gap — no structural hypothesis needed.

## 4. Proofs of the bounds

**Theorem A.** Double-count pairs `(S, T)`, `S in E_p`, `T` a `d`-subset of `S`.

- *Each `d`-subset lies in at most one member of `E_p`.* If `T subset H`,
  `|T| = d`, and `S, S' in E_p` both contain `T`, then `L_S - L_{S'} in V`
  (degree `<= d - 1`) vanishes at the `d` distinct points of `T`; a nonzero
  polynomial of degree `< d` cannot have `d` roots, so `L_S = L_{S'}`, `S = S'`.
- Each `S` gives `binom(j,d)` pairs; each `T` is hit at most once. So
  `#E_p * binom(j,d) <= binom(n,d)`, which is Theorem A. []

Equivalently: **two distinct locators in one prefix fiber share at most
`d - 1 = j - sigma - 1` roots** (their common roots are roots of the nonzero
degree-`<= d-1` difference); Theorem A is the packing bound this spacing forces.

**Theorem A'.** By the Lemma `w_*(W,H) >= d + 1 > r` for `r <= d`, discharging
Corollary 6C's hypothesis; its conclusion is the displayed bound. (Directly: for
fixed `T`, `|T| = r`, dividing by `prod_{t in T}(X - t)` injects the
`T`-containing members into a projective dimension `d - r` flat over `H \ T`, at
most `binom(n - r, d - r)` of them; double-count over the `binom(n,r)` sets `T`.)

**Corollary B.** `binom(n,d)/binom(j,d) = prod_{i=0}^{d-1}(n-i)/(j-i)`. Since
`n >= j`, each factor is nondecreasing in `i`, hence `<= (n-d+1)/(j-d+1) <=
n/(j-d+1)`; so the ratio is `<= (n/(j-d+1))^d`. With `j >= theta n` and
`d <= theta n/2`, `j - d + 1 >= theta n/2`, giving `#E_p <= (2/theta)^d`; for
`d = O(log n)` this is `n^{O(1)}`. []

## 5. Scope, and why `prob:perfiber` stays open

Theorem A holds for **every** `d`, but is a *polynomial* bound only for
`d = j - sigma = O(log n)` at constant rate (Corollary B) -- the honest QF.6
scope ("poly to LOG dim"):

- **In scope (proved):** logarithmic reserve `sigma = j - O(log n)` (`d = O(log n)`;
  `sigma` itself is large). The field fiber
  `E_p` is genuinely `n^{O(1)}`, with no char-0 escape invoked -- there are not
  exponentially many locators to begin with.
- **Out of scope (open):** `prob:perfiber`'s critical `sigma ~ n/log n`, where
  `d ~ n/2` and `binom(n,d)/binom(j,d) ~ 2^{Theta(n)}`. There the field fiber
  *is* exponential (`verify_x1_perfiber_collisions.py`: fibers blow up as
  `sigma` drops), and the content is that almost all field coincidences are
  already char-0 (quotient-periodic `Z[zeta]` toggles, `cor:upstairs-poly`), so
  the *new*-collision count is small. That is `thm:no-collision` / the
  finite-field local-limit gap `poly(n) <= p <= quasipoly(n)` -- about the lift,
  not a field-level packing bound. QF.10 makes no claim there.

**Scoping consequence (ordered pairs).** All `#E_p^2` ordered pairs in a fiber
are prefix-equal over `K`; `prob:perfiber` subtracts the char-0-equal pairs. By
Theorem A the total is `<= (binom(n,d)/binom(j,d))^2`, so at logarithmic reserve
the per-fiber pair count is `n^{O(1)}` **without even the char-0 subtraction**.
In the hard regime that subtraction is essential and unproved -- the open edge.

## 6. Relation to the DAG

- **Branch (a) only.** Per QF.9, F-consumers split into (a) coordinate/prefix
  and (b) Hankel-pencil kernel flats. This is the complete branch-(a) proof;
  branch (b) is displacement-kernel classification (QF.14, the `#191`
  identities), whose injectivity cousin is `lem:fiber`(ii) of
  `verify_x1_lem_fiber.py`.
- **Discharges QF.6's hypothesis for this family:** Corollary 6C assumes a
  dual-distance gap that can *fail* in general (twins, sparse relations); for
  prefix planes MDS forces `w_* = d + 1`, so no twin/sparse ledger is needed.
- **Does not demote general Conjecture F:** the audit's escaping consumer
  (PMA-wide sunflower amplification, list side) is neither prefix nor kernel and
  is untouched.

## 7. Verification

`verify_conjecture_f_fiber_scoped.py` checks, by exhaustive enumeration over
`F_97` with `H = mu_n` **and** with `H = {0,...,n-1}` (to show group structure
is unused): (A) the fiber bound `max_p #E_p <= binom(n,d)/binom(j,d)`; (B) the
spacing theorem (two locators in one fiber share `<= d-1` roots); (C) the
MDS/Singleton input (`d`-point Vandermonde determinants nonzero, degree-`<d`
polynomials have `<= d-1` roots -- dual distance `> d`); (D) the per-`r`-subset
moment bound `<= binom(n-r,d-r)`; (E) Corollary B's rational inequality; (F) the
scope boundary (at `sigma ~ n/log2 n` the ratio grows like `2^{Theta(n)}`, i.e.
bit-length linear in `n`, so it beats every fixed polynomial).

```bash
python3 experimental/scripts/verify_conjecture_f_fiber_scoped.py
python3 experimental/scripts/verify_conjecture_f_fiber_scoped.py --emit
```

The verifier is supporting evidence; the proofs in §§3-4 are the content.
