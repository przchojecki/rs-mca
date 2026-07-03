# L1 Round-Robin-Coset Petal Rank Theorem and Reconstruction Collapse

## Claim

For the round-robin-coset petal family (petals = `t` distinct cosets
`g_i H` of the order-`ell` subgroup `H` of `F_q^*`, labels `a_i = g_i^ell`
pairwise distinct; the family exhibited as a rank route-cut in
`l1_full_petal_growing_defect_witnesses.md`), the full-petal CRT operator
`pi_{>d} R_{I,d}` of `l1_full_list_quotient_proof_program.md` Lemma 7/8 is
completely characterized:

1. **Graded block decomposition.** Each petal locator is the binomial
   `L_{T_i}(X) = X^ell - a_i`, so the operator is literally block-diagonal
   in the residue-graded basis: writing `F = sum_r X^r F_r(X^ell)` and
   `d_r = floor((d-r)/ell)`,

   ```text
   r_{I,d} = sum_{r=0}^{ell-1} rank B_{d_r},
   K_{I,d} = (+)_r  X^r * ker(B_{d_r})(X^ell),
   ```

   where `B_m` maps `G in F_q[Y]_{<=m}` to the coefficients of
   `Y^{m+1..t-1}` of the degree-`<t` interpolant of `(a_i -> c_i G(a_i))`.
   No hypothesis on the scalars `c_i` is needed.

2. **Rank cap and forced route-cut.** For every scalar vector,
   `r_{I,d} <= B(d) := sum_r min(d_r+1, t-1-d_r) <= ell*floor(t/2)`, with
   `B(d) = min(B(d), ell*floor(t/2))` attained by explicit scalars
   (single-spike moment construction). Hence for `t` odd the exact-rank
   formula `min(d+1, t*ell-d-1)` refuted in PR #169 fails on this family
   for EVERY scalar choice, exactly on the window

   ```text
   d in [ ell(t-1)/2 , ell(t-1)/2 + ell - 2 ]      (length ell-1),
   ```

   and never for `t` even. This upgrades the #169 route-cut from an
   observed coincidence to a structural theorem with its exact scope.

3. **Hankel normal form.** `rank B_m` equals the rank of the
   `(m+1) x (t-1-m)` Hankel section `(s_{j+u})` of the weighted moments
   `s_j = sum_i (c_i / L'(a_i)) a_i^j`, `L(Y) = prod (Y - a_i)` — the
   scalar dependence reduces to classical finite-Hankel theory. (Route-cut
   inside the route-cut: the tempting refinement
   `rank = min(m+1, t-1-m, BM-linear-complexity)` is FALSE; documented
   counterexample `p=7, t=4, m=1, nodes (2,3,1,5), scalars (6,5,0,3)`.)

4. **Reconstruction collapse (t=3): the stratum pays exactly.** For `t=3`,
   `d in [ell, 2ell-1]`, and `s_0 != 0`, the kernel is principal:
   `K_{I,d} = g(X^ell) * V_{d-ell}` with `g(Y) = s_1 - s_0 Y`. Although
   the kernel contains combinatorially many split missed-core locators
   `L_D = const*(X^ell - beta)*h(X)` (`beta = s_1/s_0`), they ALL
   reconstruct to the SAME listed codeword: by CRT uniqueness the residue
   representative of `c_i L_D` is `h * Q_0` (`Q_0` = representative of
   `c_i L_{D_0}`, degree `<= ell`), so

   ```text
   P_D = (h * Q_0) * L_{C \ D} = Q_0 * L_{C \ D_0},
   ```

   independent of `h`. Consequently the number of distinct full-petal
   listed codewords with touched set `I` and exact defect `d in
   [ell, 2ell-1]` is EXACTLY one if `beta` is a nonzero `ell`-th power
   whose root coset `D_0` lies in the core (that codeword has exact defect
   `ell` and missed core `D_0`), and EXACTLY zero otherwise. Lemma 8's
   bound `q^{d+1-r_{I,d}}` is massively non-tight here; the "unusually
   large split-locator concentration" escape route flagged in Lemma 8's
   consequences is CLOSED for this stratum. Degenerate subcases are
   discharged, not scoped out: `s_0 = 0` iff the scalars are affine in the
   labels, forcing count 0 by a degree argument; `Q_0` vanishing on part
   of `D_0` is unreachable for `t=3` (exhaustive scans); `beta` equal to a
   petal label or `D_0 !subset C` give count 0.

5. **Delimitation (t >= 5, EXPERIMENTAL).** The collapse does not extend
   to `t >= 5`: at top defect `d = (t-1)ell` the leading block is the zero
   map and distinct full-petal codewords grow like `C(#cosets, t-1)` plus
   a mixed part, for every scalar choice (exact-decoder-verified counts
   1,5,19,49,108 at `t=5`, m=4..8 core cosets; 7,42 at `t=7`) — polynomial,
   not exponential, hence no threat to Conjecture 1, but the `t=3` "count
   <= 1" is genuinely special. Empirically the number of distinct
   codewords equals the number of divisibility-minimal split kernel
   locators (exact equality in all measured instances), and two full-petal
   codewords always differ by a multiple of `L(X^ell)` (so multiplicity
   requires `|C| >= t*ell`). Interior defects `d < (t-1)ell` collapse to
   <= 1 for generic moments; engineered resonant moments reach >= 2
   (decoder-verified) with evidence for an O(t)-type bound. The equality
   mechanism and interior bound are stated as measured findings, not
   theorems.

## Status

PROVED-LOCAL for items 1-4 (complete elementary proofs in this note's
companion argument plus exhaustive finite verification, including full
brute-force list decoding on both sides of the resonance dichotomy and on
both sides of the window boundary). EXPERIMENTAL for item 5 (measured,
decoder-validated, equality mechanism not yet proved). Does not change the
status of Conjecture 1 (`l1_full_list_quotient_proof_program.md`), which
remains CONJECTURAL; this note pays one named stratum of its mixed-petal
residual and delimits the adjacent ones.

## Parameters

Generated-field setting, `q = p` prime in all verifications; `ell | p-1`;
petals = `t` distinct `H`-cosets inside a genuine cyclic domain `H_n`
(`ell | n | p-1`, `0` never in the domain); core `C = H_n` minus petals;
sunflower received word `U = c_i * L_C` on petal `i`, `0` on `C`;
`k = |C|+1`, `sigma = ell-1`, `s = k+sigma`. Verified grids: rank/kernel
claims at `p in {13..151}` (22 primes), `ell in {2..20}`, `t in {2..8}`
(166,705 (config,d) points by an independent from-scratch implementation,
plus 1,025 in the shipped verifier); Hankel form ~122k comparisons across
two independent implementations; collapse decode checks at
`p in {19,31,37,43,61,73,97}`, `ell in {2,3}` (hundreds of instances,
resonant and non-resonant, coset-union and junk cores).

## Existing paper dependency

Builds directly on `l1_full_list_quotient_proof_program.md` Lemma 7/8
(CRT compression and rank certificate), Lemma 13 (rank floor `r >= ell`,
which item 4's kernel `dim = d-ell+1` meets with equality), Theorem 21/B11
(the residual frontier); upgrades the route-cut of
`l1_full_petal_growing_defect_witnesses.md` (PR #169); addresses the
mixed-petal amplification target that closes the proof program, in the
repaired ImgFib vocabulary. Chart language: the paid stratum is a
quotient-structured chart in the sense of the CAP25 v13 insert
(rem:v13-higher-excess-cert invites printed certificates for repeated-label
full-petal charts; the resonant codeword's missed core is a full `H`-coset,
descending under `x -> x^ell` to the quotient instance).

## Proof idea or experiment

(1) is the ring isomorphism `F_q[X]/(L(X^ell)) = (+)_r X^r F_q[Y]/(L(Y))`:
reduction mod `X^ell - a_i` is the substitution `X^ell -> a_i`, so the CRT
congruences decouple across residue classes, and `pi_{>d}` respects the
grading (`j*ell + r > d iff j >= d_r + 1`). (2) each block maps a
`(d_r+1)`-dim space to a `(t-1-d_r)`-dim space and the two arguments sum
to `t`; achievability solves the moment system `sum_i (c_i/L'(a_i)) a_i^j
= delta_{j,kappa}` (Vandermonde surjectivity) making the relevant Hankel
sections single-antidiagonal of full rank. (3) Lagrange coefficient
extraction is a unit-lower-triangular transform of the moment functionals
(`q_{u+1}(x) = x q_u(x) + L_{t-1-u}` recursion). (4) is the displayed
h-cancellation; the decode-level statement additionally uses that
`P_D = W_D * L_{C\D}` always agrees with `U` on all petals and on `C\D`,
and that the exact missed core of the collapsed codeword is `D_0`.
Verifier: `experimental/scripts/verify_l1_coset_petal_rank_collapse.py`
(stdlib-only, offline, deterministic) checks all four proved items,
including full exact list decoding of a resonant instance (exactly 1
in-window extra) and a non-resonant instance (exactly 0), with the
top-defect layer `d = (t-1)ell` reported separately (populated without
resonance — deliberately outside item 4's window, which is tight).

## Ledger impact

Mixed-petal residual (Lane B) of Conjecture 1: the `t=3` round-robin-coset
full-petal interior stratum is paid EXACTLY (count in {0,1} per touched
set and scalars — stronger than a quotient charge, and independent of the
stabilizer split). The `d = (t-1)ell` top layer and the `t >= 5` strata are
delimited with measured polynomial growth laws and remain open as named
finite targets. No Paper A/B/C/D text changes; no entropy/quotient ledger
constants change. The rank theory (items 1-3) is reusable Hankel-lane
material in the sense of towards-prize.md (block ranks = finite Hankel
section ranks with explicit weighted moments).

## Constants

All constants explicit: rank cap `ell*floor(t/2)`; forced-drop window
`[ell(t-1)/2, ell(t-1)/2 + ell - 2]` for odd `t`; kernel dimension
`d - ell + 1` at `t=3` (meets Lemma 13's bound with equality); extra count
in `{0,1}` at `t=3` interior; measured top-defect counts 1,5,19,49,108
(`t=5`, m=4..8) and 7,42 (`t=7`, m=7..8).

## Reproducibility

`experimental/scripts/verify_l1_coset_petal_rank_collapse.py` (stdlib-only,
fully offline, deterministic; reuses the modular helpers of
`scan_l1_full_list_quotient_conjecture.py` and the decoder of
`verify_l1_full_petal_growing_defect_witnesses.py`). Checks: (1) block
decomposition on a 1,025-point grid incl. degenerate scalars; (2) cap +
window + spike-scalar achievability (1,132 checks); (3) Hankel normal form
(1,890 checks) + the LC-refinement counterexample; (4) the 79-locator ->
1-codeword collapse instance (p=73, genuine `H_24` domain) and full
brute-force decode of resonant/non-resonant `p=19, H_18` instances with
in-window extras counted by exact defect (1 resp. 0; top layer reported
separately). Exit code 0 iff all checks pass. The `t >= 5` measurements
(item 5) are reported in this note only and are NOT gated by the verifier.
