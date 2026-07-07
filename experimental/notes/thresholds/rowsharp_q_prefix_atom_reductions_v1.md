# Row-sharp Q prefix atom reductions v1

Status: `REDUCED_NOT_PROVED`.

This packet does not prove `U(1116048) <= B*`, does not certify the
KoalaBear MCA first-safe agreement, and does not prove the row-sharp Q-prefix
atom theorem.  It records the useful reductions from the failed proof attempts,
the exact conditional closure arithmetic, and the precise support certificate
that remains missing.

## Why this matters

This is not a closing theorem, but it is a high-value reduction packet for the
current row-sharp Q wall:

- it turns the KB-MCA `a=1116048` primitive target into a replayable
  support-certificate problem with exact constants;
- it proves the reusable structural lemmas needed by later attempts:
  Newton/power-sum equivalence, Q1 split distance, top-seam marked incidence,
  RS/list reformulations, dyadic folding identities, small signed-defect
  impossibility, and the fixed-subgroup RIM rank-drop guardrail;
- it records the exact conditional closure margin: a support-level Route D
  certificate bounded by `t*p` would imply the row-sharp atom inequality with
  about `10.9006675` bits of slack after the retained exact-lift `11440` term;
- it rules out several tempting but invalid shortcuts, including raw
  constant-list RS capacity import, generated-prefix image-cell support
  payment, zero-defect-only folding descent, and naive fixed-subgroup RIM
  nonsingularity.

## Deployed row

```text
p = 2130706433
n = 2097152
k = 1048576
a = 1116048
j = 981104
t = 67472
w = 67471
B* = 274980728111395087
K_raw = 4807520
K_rem = 4805007
```

The remaining primitive target is

```text
max_z |R_prim(z)| <= 4805007 * binom(2097152,981104) / p^67471.
```

In integer form:

```text
|R_prim(z)| * p^67471 <= 4805007 * binom(2097152,981104).
```

The target floor is

```text
floor(4805007 * binom(2097152,981104) / p^67471)
  = 274836936291722953.
```

The raw average fiber floor is

```text
floor(binomial(n,j) / p^w) = 57198030365,
```

so a constant-list theorem cannot apply to the raw prefix map.

## Proved reductions

### Newton / power-sum equivalence

Since `w < p`, Newton identities are triangular and invertible through depth
`w`.  Equality of the first `w` locator coefficients is equivalent to equality
of the first `w` power sums.

### Q1 collision distance

If two distinct supports have the same first `w` prefixes, write

```text
Lambda_S = G U,
Lambda_T = G V,
deg U = deg V = e.
```

Then

```text
deg(Lambda_S - Lambda_T) <= j-w-1,
Lambda_S - Lambda_T = G(U-V),
deg G = j-e.
```

Thus

```text
e >= w+1 = 67472.
```

### Top-seam marked incidence

The same degree bound gives

```text
deg(U-V) <= e-w-1.
```

At the minimal seam `e=w+1`, this becomes

```text
deg(U-V) <= 0,
```

so

```text
U-V = constant.
```

The common core `G` must remain marked; unmarked side-pair counting can have
many common cores and is not a valid replacement.

### Exact-lift terminal-16 retained class

The imported exact-lift Q2 input gives a retained exact-lift class bound

```text
|E_ret(z)| <= binom(16,7) = 11440.
```

### Folding identities

For an antipodal pair `{x,-x}` with `y=x^2`, define

```text
u_y     = 1_S(x) + 1_S(-x),
sigma_y = 1_S(x) - 1_S(-x).
```

Then

```text
P_{2a}(S)   = sum_y u_y y^a,
P_{2a+1}(S) = sum_y sigma_y x y^a.
```

There are `33736` odd equations, so a nonzero homogeneous signed defect
satisfying all of them has support at least

```text
33737.
```

This excludes small signed defects only; it does not pay large full-rank
signed defects.

### RS/list reformulations

On the support-locator side, the prefix fiber is exactly the list of
polynomials

```text
h in F_p[X]_<913633
```

that agree with the received word `-F_z` on at least `981104` points of `D`.
On the complementary MCA side it is an `RS_D(k+1)` list at agreement
`a=k+t`.  These are exact reformulations, not imported capacity theorems.

## Provenance

This packet consumes or references the following local sources and open-PR
context.  Experimental sources listed here are not imported as payments.

- `KB adjacent row constants and generated image-cell ledger`: `IMPORTED_PROVED_INPUT_WITH_CONDITIONAL_LEDGER_SCOPE` from `experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md` (local main / prior KB-MCA 1116048 partial ledger packet). p,n,k,agreement,j,t,w,B*,K_raw,K_rem and B_gen<=t*p image-cell arithmetic.
- `Exact-lift terminal-16 retained fiber bound`: `IMPORTED_PROVED_INPUT` from `experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md` (local main / prior KB-MCA 1116048 partial ledger packet). A retained exact lifted prefix class has size at most binom(16,7)=11440.
- `Q-fin / Route gamma strategy context`: `STRATEGY_CONTEXT_NOT_CONSUMED_AS_PAYMENT` from `experimental/cap25_v13_missing_inputs_strategy.md` (local main strategy note). Q-fin needs near-lossless recursion; Route gamma/folding defects are the aligned route.
- `Top-seam marked-incidence guardrail`: `PROVED_LOCAL_LEMMA_DOES_NOT_SUPERSEDE_PR_389` from `experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md` (this packet; conceptually adjacent to open PR #389). At e=w+1, coprime side locators U,V satisfy U-V=constant; common core G remains marked.
- `Composite-prefix gcd(e,N) descent context`: `EXPERIMENTAL_REGRESSION_NOT_CONSUMED_AS_PAYMENT` from `experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md` (this packet; conceptually adjacent to open PR #394). Small-model regressions support c=gcd(e,N) quotient factorization.
- `BC-to-Q and shift-pair route context`: `EXPERIMENTAL_CONTEXT_NOT_CONSUMED_AS_PAYMENT` from `experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md` (this packet; conceptually adjacent to open PRs #393/#395/#396). Toy chart decompositions motivate multiplicity accounting; no BC/SP upper payment is imported here.


## RIM guardrail

The packet includes a small `F_17`, `mu_8`, `k=3` counterexample to the naive
claim that symbolic RIM full rank always survives roots-of-unity
specialization.  Therefore the correct deterministic RIM result is a
first-match routing theorem: if the canonical pivot minor vanishes after
specialization, the packet must enter a rank-drop/pivot branch.  Surviving
packets have full specialized rank by definition of that branch.

This does not pay the rank-drop/pivot branch.

## Conditional closure

If the missing support certificate proves

```text
|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p
```

for every primitive finite prefix target `z`, then

```text
t*p = 143763024447376,
|E_ret(z)| <= 11440,
t*p + |E_ret(z)| = 143763024458816.
```

Since

```text
143763024458816 < 274836936291722953,
```

the row-sharp Q-prefix atom inequality follows with integer slack

```text
274693173267264137
```

and about `10.900667525` bits of slack.

## Missing theorem

The remaining theorem is a support-level primitive fixed-subgroup certificate:

```text
For every primitive finite prefix target z, after first-match deletion of
generated_field, quotient_planted, sparse_pade_hankel, m1_window_shadow,
rank_drop_pivot, bc_chart, sp_shift_pair, and extension_slope branches,
the remaining generated-prefix / primitive full-rank signed-defect support
mass is at most t*p = 143763024447376.
```

Equivalent forms include deterministic fixed-subgroup RIM nonvanishing after
branch deletion, marked-incidence injection into `{0,...,67471} x F_p`, and a
primitive Fourier phase-spread coefficient bound.

## Related experiment packet

The companion evidence packet is:

```text
experimental/scripts/experiment_rowsharp_q_prefix_atom_routes_v1.py
experimental/data/certificates/rowsharp-q-prefix-atom-routes-v1/rowsharp_q_prefix_atom_routes_v1.json
experimental/notes/thresholds/rowsharp_q_prefix_atom_routes_v1.md
```

It is experimental evidence only.  It supports Route D and marked incidence,
while showing that generated-prefix image labels and zero-defect descent do
not pay support multiplicity.
