# Matching composition — face 2, step (i) of the weight-2 inverse theorem

- **Status:** PROOF PHASE. Theorem 1 (matching composition) and Lemmas
  B, D are **PROVED** (complete proofs below, classical ingredients
  only: Luroth, bidegree Bezout on P^1 x P^1, tame Riemann-Hurwitz,
  GRS duality). Step (ii) of the DAG plan is **FALSIFIED AS STATED**
  at the census scale n = q-1 (explicit counterexample, Section 5);
  its corrected form is OPEN with the gap named. The targeted linear
  threshold W(d) = d+2 is NOT achieved: the proved composition
  threshold is quadratic in j; the linear over-determination seed is
  Lemma D. Honest labels throughout.
- **DAG node:** `f_weight2_inverse` (FACE-2 CORE), step (i) of its
  two-step proof plan; feeds `f_sparse_rank_split`; touches
  `f_dih_subgroup_completeness` (E36) at the corrected step (ii).
- **Predecessors:** E35 census (`e35_weight2_abundance.md`), E30
  machinery, E36 PGL_2 set-stabilizers.
- **Verifier:** `experimental/scripts/verify_f_matching_composition.py`
  (stdlib-only, deterministic, exact at n = 16; checks every claimed
  identity on the E35 census artifacts, the counterexample, both
  lemmas, and randomized exact pullback/background checks — see
  Section 7).

## 1. Setting and objects

`K = F_q`, characteristic `p`; `H` a subset of `K^*` of size `n`
(`H = mu_n` where stated; the census scale is `K = F_17`, `H = mu_16`,
`n = q - 1 = 16`). A FLAT is a linear subspace `P <= K[X]_{<=j}` of
linear dimension `r >= 2` (projective dimension `d = r - 1`), basis
`p_1, ..., p_r`. Write `W = gcd(p_1, ..., p_r)`, `p_i = W P_i` with
`gcd(P_1, ..., P_r) = 1`, and `D = max_i deg P_i`, so `1 <= D <= j`
(`D >= 1` because the `p_i` are independent and `r >= 2`).

POST COMMON-ROOT STRIP: no `x in H` has `p(x) = 0` for all `p in P`
(no weight-1 dual words). In particular `W` has no root in `H`.

Homogenize the reduced tuple to common degree `D`; since the `P_i`
have no common root and at least one attains degree `D`, the tuple has
no common zero on `P^1`, so it defines a MORPHISM

```text
Phi = [P~_1 : ... : P~_r] : P^1 -> P^{r-1},
```

and for `x in H` the evaluation column satisfies `[c_x] = Phi(x)`
(because `W(x) != 0` there).

**Minimal weight-2 dual word** on support `{a, b} <= H`, `a != b`,
ratio `c in K^*`: `p(b) = c p(a)` for all `p in P`. Post-strip this is
EQUIVALENT to the collision `Phi(a) = Phi(b)`. An (edge-)MATCHING is a
set of `m` pairwise disjoint such supports `{a_i, b_i}`, ratios `c_i`
(E35's statistic `w2m` is the maximum such `m`).

**Collision biforms.** For `i < k` set
`F_ik(x, y) = P~_i(x) P~_k(y) - P~_k(x) P~_i(y)`, bihomogeneous of
bidegree `(D, D)`. For `x != y`: `Phi(x) = Phi(y)` iff `F_ik(x,y) = 0`
for all `i < k` (2x2 minors of a rank-<=1 matrix with nonzero rows).

**Ratio tuple and the composition invariant.** Let
`R_k = P_k / P_1 in K(x)` (k = 2..r), each NONCONSTANT (basis
independence), written reduced (cancellation with `P_1` allowed —
this cancellation is exactly the near-pencil mechanism and is handled
explicitly below). Over the algebraic closure set

```text
L = Kbar(R_2, ..., R_r) <= Kbar(x),    e := [Kbar(x) : L]  (finite).
```

By Luroth's theorem (valid over any field) `L = Kbar(psi)` for a
rational `psi` of degree exactly `e`. The integer `e` is the
COMPOSITION DEGREE of the flat: `e >= 2` says every ratio of members
of `P` factors through the single inner map `psi`. (A remark on
`K`-rationality of `psi` is in Section 6.)

## 2. Lemma B (value rigidity) — PROVED

**Lemma B.** Let `S_2, ..., S_l in Kbar(x)` be nonconstant with
`Kbar(S_2, ..., S_l) = Kbar(x)` and `F := max_k deg S_k`. Then

```text
V(S) := { (x, y) in P^1 x P^1 : x != y, S_k(x) = S_k(y) for all k }
```

(values in `P^1`) is finite, and `|V(S)| <= 2 (F - 1)^2`. If some
`S_k` has degree 1 then `V(S)` is empty.

*Proof.* The degree-1 case is trivial (a Mobius map is injective).
Assume all `deg S_k >= 2`. Write `S_k = u_k / v_k` reduced and let
`G_k(x, y) = u~_k(x) v~_k(y) - u~_k(y) v~_k(x)` (bidegree
`(f_k, f_k)`, `f_k = deg S_k`); since `(u_k, v_k)` have no common zero
on `P^1`, `S_k(x) = S_k(y)` iff `G_k(x, y) = 0`. The diagonal form
`Delta = x_0 y_1 - x_1 y_0` divides `G_k`; let `a_k >= 1` be the exact
power and `G'_k = G_k / Delta^{a_k}` (bidegree
`(f_k - a_k, f_k - a_k)`, not divisible by `Delta`). Off the diagonal,
`Z(G_k)` and `Z(G'_k)` agree, so `V(S) <= INT_k Z(G'_k)`.

*(1) No common component.* Suppose an irreducible curve
`E <= INT_k Z(G'_k)`. `E` is not the diagonal (else `Delta | G'_k`).
`E` is not a vertical line `{x = const = c}`: else `G_k(c, y) = 0`
identically, and since `(u~_k(c), v~_k(c)) != (0,0)` this forces
`[u~_k(y) : v~_k(y)]` constant, i.e. `S_k` constant — excluded.
Symmetrically not horizontal. Let `(tau, sigma)` be the generic point
of `E`: both coordinates are nonconstant on `E`, hence transcendental
over `Kbar`, and `G_k(tau, sigma) = 0` gives `S_k(tau) = S_k(sigma)`
in `Kbar(E)` (denominators nonvanish at transcendentals). Generation
is a field identity: under the isomorphism `Kbar(x) ~ Kbar(tau)`,
`Kbar(S_2(tau), ..., S_l(tau)) = Kbar(tau)`, and likewise for
`sigma`. Equality of the generators gives `Kbar(tau) = Kbar(sigma)`
inside `Kbar(E)`, so `sigma = h(tau)` and `tau = g(sigma)` with
`h, g` rational; `g o h = id` forces `deg h = 1` (Mobius). The
identities `S_k o h = S_k` (they hold at the transcendental `tau`)
say precomposition by `h` is a `Kbar`-automorphism of `Kbar(x)`
fixing every `S_k`, hence fixing `Kbar(S) = Kbar(x)` elementwise; in
particular `x o h = x`, so `h = id` and `E` is the diagonal —
contradiction.

*(2) Explicit bound.* The `G'_k` share no irreducible factor (a
common factor would give a common component). Pad to a common
bidegree `beta <= F - 1`: `H_lam = SUM_k lam_k Delta^{beta - deg} G'_k`.
For each of the finitely many irreducible factors `theta` of `G'_2`
(all `!= Delta`), `{lam : theta | H_lam}` is a proper subspace
(properness: `theta | H_lam` for all `lam` forces `theta | G'_k` for
all `k`). `Kbar` is infinite, so some `lam` avoids all of them:
`gcd(G'_2, H_lam) = 1`. Every point of `V(S)` lies on
`Z(G'_2) INT Z(H_lam)`; two coprime curves of bidegrees
`(b, b), (beta, beta)` on `P^1 x P^1` meet in at most `2 b beta`
points. With `b, beta <= F - 1`: `|V(S)| <= 2 (F - 1)^2`. QED

The generation hypothesis is load-bearing: for a non-generating tuple
(e.g. two rational functions of `x^2`) the correspondence contains the
curve `{y = -x}` and `V` is infinite. The verifier exhibits both sides.

## 3. Theorem 1 (matching composition) — PROVED

**Theorem 1.** Notation of Section 1 (`r >= 2`, post-strip). Let `m`
be the number of pairwise disjoint minimal weight-2 dual supports of
`P` on `H`, and `e` the composition degree. Set

```text
B(j) := j + (j - 1)^2.
```

(i) *(accidental bound)* If `e = 1` then `m <= D + (D-1)^2 <= B(j)`.

(ii) *(composition)* If `m > B(j)` then `e >= 2`, and with `psi` the
degree-`e` Luroth generator:

  (a) *(global factorization)* `Phi = nu o psi` for a morphism
      `nu : P^1 -> P^{r-1}`; equivalently the reduced ratio of any
      two members of `P` lies in `Kbar(psi)`.

  (b) *(global extension — the composed symmetry candidate)* for ALL
      `x, y in H` with `psi(x) = psi(y)` there is `c(x,y) in K^*`
      with `p(y) = c(x,y) p(x)` for every `p in P`. I.e. the
      psi-fiber equivalence relation on `H` is made of flat-wide
      ratio edges; it extends the given matching (up to the
      exceptional edges of (c)).

  (c) *(the matching is psi-fibered)* at least
      `m - D - (D-e)^2/e >= m - j - (j-2)^2/2` of the given edges
      satisfy `psi(a_i) = psi(b_i)`.

  (d) *(regularity of the extension)* if `p = char K > j`, `psi` is
      separable and tame; all fibers of `psi` over `P^1(Kbar)` have
      exactly `e >= 2` points except over at most `2e - 2` branch
      values (Riemann-Hurwitz).

*Proof.*

(i) Fix the basis element `P_1`. `P_1` has at most `deg P_1 <= D`
roots, and the edges are disjoint, so at most `D` edges touch a root
of `P_1`. Any other edge `{a, b}` has `P_1(a) P_1(b) != 0`, and
`Phi(a) = Phi(b)` then reads `R_k(a) = R_k(b)` (finite values) for
all `k`: the ordered pairs land in `V(R_2, ..., R_r)`. All `R_k` are
nonconstant; if some `R_k` is Mobius there are no such edges; else
`e = 1` means the tuple generates `Kbar(x)` and Lemma B (with
`F <= D`) gives at most `(D-1)^2` unordered pairs. Total:
`m <= D + (D-1)^2`, which is at most `j + (j-1)^2` since `D <= j`.

(ii) `m > B(j)` forces `e >= 2` by (i).

(a) Each `R_k in Kbar(psi)`: `R_k = tau_k o psi` with
`deg tau_k = deg R_k / e =: f_k <= D/e` (degree multiplicativity in
the tower `Kbar(x) >= Kbar(psi) >= Kbar(R_k)`). Let `nu` be the
morphism `P^1 -> P^{r-1}` obtained from the tuple
`(1, tau_2, ..., tau_r)` by clearing denominators and common factors.
On the dense open set where `P_1 != 0` and all denominators
nonvanish, both `nu o psi` and `Phi` equal
`[1 : R_2(x) : ... : R_r(x)]`; two morphisms from a smooth complete
curve agreeing on a dense open set are equal, so `Phi = nu o psi`
EVERYWHERE. (This morphism identity is what absorbs all
cancellation/degeneration loci — the near-pencil caveat.)

(b) `psi(x) = psi(y)` gives `Phi(x) = Phi(y)` by (a); for
`x, y in H` post-strip this is `[c_x] = [c_y]` with both columns
nonzero in `K^r`, so the ratio `c(x,y)` exists and lies in `K^*`.

(c) Consider an edge `{a, b}` with `P_1(a) P_1(b) != 0` and
`psi(a) != psi(b)`. Then `tau_k(psi(a)) = tau_k(psi(b))` for all `k`,
so `(psi(a), psi(b))` lies in `V(tau_2, ..., tau_r)`. The tau-tuple
generates `Kbar(t)`: if `Kbar(tau) = Kbar(mu)` with `deg mu >= 2`
then `Kbar(R) = Kbar(mu o psi)` would have index `> e` in `Kbar(x)`.
Each `tau_k` is nonconstant; if one is Mobius there are no such
edges; else Lemma B at value level gives at most `(D/e - 1)^2`
unordered value pairs `{t, s}`. Disjointness lets at most `e` edges
share one value pair (each such edge consumes a point of the fiber
`psi^{-1}(t)`, which has at most `e` points). So the exceptional
edges number at most `D + e (D/e - 1)^2 = D + (D-e)^2 / e`, maximized
over `2 <= e <= D <= j` at `e = 2, D = j`: `<= j + (j-2)^2 / 2`.

(d) `deg psi = e <= D <= j < p`, so `psi` is separable and every
ramification index (`<= e < p`) is tame; Riemann-Hurwitz gives
`2e - 2 = SUM (e_P - 1)`, hence at most `2e - 2` branch values and
full fibers of size exactly `e` elsewhere. QED

**Sharpness comments (honest).** The threshold `B(j)` is quadratic
in `j` and worst-case Bezout; at the census scale (`j <= 5, n = 16`)
it exceeds the maximum possible `m = n/2 = 8`, so Theorem 1(ii) is
vacuous THERE, while the empirically true accidental ceiling is
`m <= 3` (E35 background band). The gap quadratic -> linear is OPEN
(Section 6); what the census DOES exercise nonvacuously is the
converse structure: every abundant census flat has `e >= 2` and its
edges are exactly psi-fibers (verifier CHECK 2), and every
`e = 1` family sits at `m <= 3` (CHECK 3/7).

## 4. Lemma D (over-determination at the linear threshold) — PROVED

This is ingredient (1) of the plan made exact: each disjoint edge is
one linear condition on `K[X]_{<=j}`; past codimension the conditions
must become dependent, and the dependency is itself a polynomial law.

**Lemma D.** Let `H = mu_n <= F_q^*`, `P` a flat of linear dim `r`
(not nec. post-strip), with `m` disjoint weight-2 supports
`{a_i, b_i}`, ratios `c_i`. If `m >= j + 2 - r` then there are a
subset `I` with `|I| >= ceil((j+2)/2)` and a nonzero `g in K[X]`,
`deg g <= n - j - 2`, such that

```text
(D1)  g(x) = 0 for every x in H outside  UNION_{i in I} {a_i, b_i};
(D2)  c_i = - (a_i g(a_i)) / (b_i g(b_i))   for all i in I.
```

*Proof.* The functionals `l_i(f) = f(b_i) - c_i f(a_i)` on
`K[X]_{<=j}` vanish on `P`, so they lie in `Ann(P)`, of dimension
`j + 1 - r`. If `m >= j + 2 - r` they are dependent: some
`SUM t_i l_i = 0` on `K[X]_{<=j}` with `t != 0`. The vector
`v in K^H` with `v_{b_i} = t_i`, `v_{a_i} = -t_i c_i` (well defined
by disjointness) is then orthogonal to `RS[n, j+1] = ev(K[X]_{<=j})`.
For `H = mu_n`, `RS[n, j+1]^perp = { (x g(x))_{x in H} :
deg g <= n - j - 2 }`: the containment is the identity
`SUM_{x in mu_n} h(x) = n h_0` for `deg h <= n - 1` applied to
`h = f X g` (whose constant term is 0), and the dimensions
(`n - j - 1`) match. So `v = (x g(x))_x` up to a scalar absorbed in
`g`. Off the matched points `v = 0` gives (D1); at a matched pair,
`t_i = b_i g(b_i)` and `-t_i c_i = a_i g(a_i)` give (D2) on
`I = { i : t_i != 0 }`. Finally `v` is a nonzero word of the dual
code, whose minimum distance is `j + 2`; its weight is `2|I|`, so
`|I| >= ceil((j+2)/2)`. QED

**Calibration remark (heuristic, not a proof).** With `r = d + 1`
(projective dim `d`) the threshold is `j + 1 - d`: at the census cell
`j = 4, r = 3` this is 3 — exactly E35's observed nonsymmetric
ceiling `w2m = 3`. Lemma D says the ratios of any 4th disjoint edge
are already enslaved to a single polynomial law (D2); the OPEN
strengthening (Section 6) is to convert (D2) plus Lemma B into
`e >= 2` at threshold `j + 2 - r + O(1)` — that would give the
targeted `W(d) = d + 2` shape at full-dimensional flats and match
E35's `W* = 4`.
