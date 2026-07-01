# WP-2.6 detail (L3): the underdetermined boundary program

- **Status:** AUDIT / refined plan (L3 leaf per roadmap §0.1). Rung 1 is
  running as PR #172 (turn 1 merged into the branch; turns 2+ follow this note).
- **Parent:** `../proximity_prize_execution_roadmap_post_v10_r2.md`, WP-2.6.
- **Row:** `C = RS[F_17^32, H, 256]`, `n = 512`, `k = 256`, `H = mu_512` (the
  full 2-Sylow, so `X^512 - 1` is separable in char 17: `gcd(17, 512) = 1`).
- **Executability:** AGENT throughout rungs 1-2; rung 3 feeds WP-3.2.

## Notation (pinned)

For exact agreement `A`: `t = A - k` (equations), `j = n - A` (co-support
size), locator coefficient vector `c = (c_0..c_j)`, Hankel pencil

```text
M(Z) = H_{t,j}(u) + Z H_{t,j}(v)  in  F[Z]^{t x (j+1)},
M(Z)[row, col] = S_Z[row + col],  S_Z = syndrome window of u + Z v
```

(extractor convention, `extract_regular_hankel_minors.py`). Underdetermined:
`t < j+1`, deficiency `d = (j+1) - t = n + k + 1 - 2A`. Rung 1 is `A = 384`
(`t = j = 128`, `d = 1`). A locator is **valid** if it has degree exactly `j`
and `j` distinct roots in `H`; a slope `Z_0` is counted at exact agreement `A`
only if its kernel contains a valid locator (necessary condition; the
noncontainment gate is a further filter, see Dedup).

## Rung 1 lemma DAG (deficiency 1, A = 384)

```text
U1 Cramer kernel  ->  U2 pencil nondegeneracy  ->  L(Z,X) defined
L(Z,X) -> U3 validity = divisibility -> U4 pseudo-remainder chart -> U5 dichotomy
side charts: D(Z) rank-drop ; c_j(Z) = 0 low-degree
acid test: exhaustive toy row F_97
instantiation: declared F_17^32 family -> packet
```

### U1 (Cramer kernel)

**Statement.** Let `M_i(Z) = det(M(Z) with column i removed)`, `i = 0..j`,
each in `F[Z]` with `deg_Z M_i <= t = 128`. If `rank M(Z_0) = t` then
`ker M(Z_0)` is 1-dimensional, spanned by `v(Z_0) = ((-1)^i M_i(Z_0))_{i=0..j}`.

**Route.** Standard adjugate/Cramer expansion: for any `(t+1)`-column
submatrix the Laplace expansion of the bordered determinant vanishes;
equivalently append any row of `M` to itself and expand. Elementary, but state
and prove it in the note — no citation-only steps.

**Acceptance test.** Toy row (below): for every slope with `rank = t`,
compare `v(Z_0)` to an RREF-computed kernel vector up to scalar; exact match
required at all such slopes.

**Failure branch.** None expected (classical); if the toy comparison fails,
the extractor convention was misread — fix before proceeding.

### U2 (pencil nondegeneracy of the declared family)

**Statement.** `v(Z)` is not identically zero iff `rank_{F(Z)} M = t` iff
some `M_i != 0` in `F[Z]`. For each declared input family, certify this by
exhibiting one nonzero `M_i` (evaluation at one slope suffices).

**Failure branch.** If all `M_i = 0` (pencil-degenerate family, e.g. low-rank
`H(u)` with `v` proportional): the family belongs to WP-2.3 strata
(proportional / lower-rank containment), not to this chart. Route it there
explicitly; do not force the chart.

### The bivariate candidate locator

```text
L(Z, X) = sum_{i=0..j} (-1)^i M_i(Z) X^i,   deg_X <= j = 128, deg_Z <= t = 128.
```

On the generic chart (`rank M(Z_0) = t`), every locator explaining exact
agreement `A` at slope `Z_0` is a scalar multiple of `L(Z_0, X)`.

### U3 (validity = divisibility)

**Statement.** Since `X^512 - 1` is separable and its root set is exactly
`H`, a specialization `L(Z_0, X)` with `deg_X = j` is valid iff
`L(Z_0, X) | X^512 - 1`. Divisibility automatically yields `j` distinct roots
in `H` — no separate squarefreeness check is needed.

**Dedup rule (exactness).** If `deg_X L(Z_0, .) < j` (i.e. `c_j`-coordinate
vanishes) the explained agreement exceeds `A`; the slope belongs to a
higher-agreement bucket and must be counted there, not here (cross-bucket
dedup line in the packet). The noncontainment gate (`H(v) ell != 0` in the
PR #171 formulation) is applied after root-set extraction, and only ever
*decreases* the count — safe for an upper bound; record it as a refinement,
never as a prerequisite.

### U4 (pseudo-remainder chart)

**Statement.** Work on the chart `U_top = {Z : c_j(Z) := (-1)^j M_j(Z) != 0}`
(finite complement, handled by the side chart below). Pseudo-divide:

```text
lc^delta (X^512 - 1) = Q(Z,X) L(Z,X) + R(Z,X),   delta = 512 - j + 1 = 385,
R(Z,X) = sum_{m=0..j-1} rho_m(Z) X^m,   deg_Z rho_m <= t + delta*t = 49408.
```

For `Z_0 in U_top`: `L(Z_0,X) | X^512 - 1  <=>  rho_m(Z_0) = 0 for all m`.

**Acceptance test.** Toy row: pseudo-division implemented exactly; at every
slope, divisibility checked two ways (pseudo-remainder vanishing vs direct
polynomial division after specialization); must agree at all slopes.

### U5 (chart dichotomy — the packet's end state)

**Statement.** Let `G(Z) = gcd_m(rho_m(Z))`. Exactly one of:

```text
(E) some rho_m != 0: G is a nonzero eliminant; bad slopes in U_top are
    contained in roots(G), a set of size <= deg G <= 49408. End state:
    eliminant, degree printed, root table extracted where feasible.
(V) all rho_m = 0 identically: L(Z,X) | X^512 - 1 in F(Z)[X]; EVERY chart
    slope carries a valid locator for this family — an identically-valid
    pencil. End state: not a defeat but a finding. Immediately test payment:
    is the family tangent-paid or quotient-paid (WP-2.3 strata)? If paid,
    record paid-pencil; if unpaid, this is a candidate_new_obstruction with
    a minimal reproduction — the single most important possible output of
    this program.
```

**Failure branch.** Neither case can fail to occur; the branch structure IS
the deliverable. The risk is computational only (degree ~5*10^4 over
GF(17^32)); see Instantiation.

### Side charts (complete the atlas)

```text
rank-drop locus:  D(Z) = gcd_i(M_i(Z)), deg <= 128. On roots of D the kernel
  has dim >= 2. These are <= 128 explicit slopes: for each, specialize and
  decide by finite linear algebra whether the (now d>=2-dimensional) kernel
  contains a valid locator — for dim 2 this is divisibility of a one-parameter
  pencil, i.e. one resultant in the pencil parameter. End states per slope:
  empty / counted / labelled residual.
low-degree locus:  c_j(Z) = 0 but rank = t: kernel locator has deg_X < j ->
  higher-agreement bucket (dedup rule above). Certify by listing roots of
  M_j(Z) not in D(Z).
```

Chart coverage identity to assert in the verifier: every slope lies in
exactly one of `U_top`, `{c_j = 0, rank = t}`, `{rank < t}`.

## The acid test (toy row, exhaustive ground truth)

Mirror row: `p = 97`, `H = mu_16 <= F_97^*` (`16 | 96`), `n = 16`, `k = 8`.
Regular iff `2A >= 25`, so `A* = 12` is the deficiency-1 boundary
(`t = j = 4`, matrix `4 x 5`) — an exact scale model of A=384.

**Ground truth:** enumerate all `C(16,4) = 1820` co-supports and all 97
slopes; for each pair test directly whether `u + Z v` restricted to the
support is explained by a degree-<8 codeword with exact agreement 12. This
brute force is feasible and INDEPENDENT of the chart machinery.

**Required identity:** brute-force bad-slope set == union over the three
charts of the predicted sets (eliminant roots in `U_top` + rank-drop
decisions + low-degree exclusions), for at least two declared toy families
(one generic random-seeming pair, one structured pair, coefficients pinned in
the verifier). Any mismatch halts the program at the earliest failing lemma.

## Instantiation on the F_17^32 row (declared family)

- Field arithmetic: reuse the #148 independent GF(17^32) tower (pinned
  degree-32 modulus) — no dependence on unintegrated PRs.
- Family: start with the pinned synthetic pair from the on-main row-descriptor
  certificate; print the family in the packet (`declared`, not worst-case).
- Compute strategy for `rho_m` (`deg_Z <= 49408`): evaluation-interpolation —
  evaluate `M(Z_0)` at `>= 49409` distinct slopes, run the U1/U4 chain
  pointwise, interpolate only `G(Z)`-relevant data; fallback if infeasible in
  budget: (i) certify the structural degree bound + (ii) spot-verify
  divisibility at a pinned pseudorandom slope sample + (iii) mark the full
  eliminant `residual: computational`, honestly labelled. The toy acid test,
  not the big row, carries the correctness burden.
- Packet: `experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/`,
  schema-checked; `removed_ledgers` referencing tangent/quotient payment of
  any (V)-branch families; end states per §4.6 of `towards-prize.md`.

## Rung 2 (deficiency d >= 2): measure the growth law early

At deficiency `d`, `ker M(Z_0)` is generically `d`-dimensional: locators form
a projective `(d-1)`-pencil per slope. Validity becomes an elimination in
`(Z, lambda_1..lambda_{d-1})`. Plan: implement at `A = 383, 382` (`d = 3, 5`
— note `d` steps by 2 in `A`) on the TOY row first (`A* - 1 = 11: d = 3`),
measure eliminant degree growth empirically, then state the growth law as a
conjecture with the measured constants. **Expected outcome:** effective
elimination dies within a few rungs; the honest deliverable is the named wall
— "underdetermined elimination wall" — frozen with a consumer theorem
(what closing it at deficiency `d(n)` would yield for in-band `A`), a toy
reproduction, and the connection to the known hard-core instance `A = 265`
(`d = 239`) and F1 slack `t = 9`.

## Rung 3 (symbolic, feeds WP-3.2)

Re-state U1-U5 over an abstract field with an order-`2^s` subgroup
(char coprime to `2^s`): U1/U2 are field-generic; U3 needs only separability
of `X^{2^s} - 1`; U4/U5 degree bounds become `t + (n - j + 1) t` symbolically.
Deliverable: one lemma note usable by any future row, with characteristic
exclusions printed.

## Verifier / file layout (per turn, PR #172)

```text
turn 2:  U1 + U2 on the toy row (exact)            -> check 3 PASS
turn 3:  U3 + U4 pseudo-division (toy, exact)      -> check 4 PASS
turn 4:  U5 dichotomy + side charts (toy)          -> check 5 PASS
turn 5:  ACID TEST (brute force == charts, toy)    -> check 6 PASS
turn 6+: F_17^32 declared family + packet + schema -> checks 7-8 PASS
```

Each turn: verifier green before commit; agents-log entry; honest-scope
lines carried in note + packet. TERMINUS per the loop memory.
