# S3b.iii mechanism 2: displacement / spectral exchange-rigidity (SKETCH)

- **Status:** SKETCH / CONJECTURE / GAP-WALL, labelled per node. NOT rigorous.
- **Parent:** `prize_proof_sketch_spine.md`, node S3b.iii; sibling of
  `s3b_iii_1_divisor_pencil_incidence.md` (mechanism 1). All displayed
  identities and spectra were machine-verified before commit (F_13 toy for
  the factorizations; trace checks for the Johnson spectra).
- **Role:** the dimension-free route. Mechanism 1 stalls because elimination
  degree grows with the deficiency `d`; everything below lives on the
  support side where `d` never appears.

## 1. The exact backbone: subgroup Hankels are Fourier objects [elementary, verified]

For `u` supported on the subgroup `H = mu_n` and syndrome `s_u[m] =
sum_{x in H} u(x) x^m`:

```text
H_{t,j}(u) = V_t^T  D_u  V_{j+1},      D_u = diag(u(x))_{x in H},
V_m[x, r] = x^r  (r < m),
```

verified entrywise on the F_13 / mu_12 toy. (The repo's syndrome indexing
may carry a constant offset `x^{c_0}`; it absorbs into `D_u` — cosmetic.
The PR #171 "subgroup syndrome-section theorem" appears to be this object;
replay pending per standing order 12.)

Consequently, for a locator `l` with root set `T` (co-support) and
`w_Z = u + Z v`:

```text
M(Z) l = 0
   <=>  the function  w_Z * l  on H has vanishing Fourier coefficients
        at frequencies 0..t-1                                  [verified]
   <=>  sum_{x in S} w_Z(x) l(x) x^m = 0,  m < t,  S = H \ T.
```

Alignment is a HARMONIC condition: the windowed product `w_Z * l` misses the
first `t` frequencies. `t` enters only as the window length — no elimination
variables, no deficiency. This is the same factorization that makes the
#170 determinant identity work (`det = det(V)^2 prod(x)^h det(I + Z K_h)`,
Cauchy kernels = `V`-interactions between root sets); mechanism 2 is that
computation promoted to a counting philosophy.

## 2. Exchange calculus [PROVED-cited in instances]

Move one point of the co-support: `T' = T \ {y} u {x'}`. Then

```text
l_{T'}(x) = l_T(x) * (x - x') / (x - y),
```

a CAUCHY factor — on the alignment sums this is a rank-one (displacement-
rank-1) update. Repo instances of exactly this calculus: the `t=2`
one-exchange residual degree packet (#152, integrated), the
replacement-subset / Cauchy-Binet coefficient formulas and the
rank-one-displacement Toeplitz-Cauchy factor (#170), the shift-two transfer
between same-parity shifts (#170). The atomic move of the whole theory is
the one-exchange, and its algebra is completely explicit.

## 3. The rigidity idea [SKETCH — the mechanism]

Consider the aligned set `A_{u,v} = {T in D_j : (H_u l_T) parallel (H_v l_T)}`
as a subset of the JOHNSON GRAPH `J(n, j)` (vertices = co-supports, edges =
one-exchanges). Facts (verified): `J(n,j)` is distance-regular with
eigenvalues `lam_i = (j-i)(n-j-i) - i`, degree `lam_0 = j(n-j)`, and the
remarkable exact gap

```text
lam_0 - lam_1 = n        (independent of j; verified at (5,2), (512,128), (512,247)).
```

The heuristic: alignment at `T` and at a neighbor `T'` differ by a rank-one
Cauchy update, so "aligned AND stays aligned across many exchange edges" is
a strongly over-determined web of rank-one conditions — unless the updates
are degenerate, and the degenerate configurations are precisely the
structured ones (tangent: the update is absorbed by the common codeword
pair; quotient: the update commutes with the subgroup action). An
expansion argument on `J(n,j)` should then force: either `A_{u,v}` is small
(poly), or it has positive edge-density inside itself, which pumps the
rank-one web until a paid structure crystallizes.

**Named wall: XR (exchange-rigidity hypothesis) [GAP-WALL].** Freeze-shape:

```text
If T and a >= 1/poly(n) fraction of its J(n,j)-neighbors are aligned for the
same pair (u,v), then (u,v) carries tangent or quotient structure on a
support refinement — quantitatively enough to charge T to Paid(A).
Consumer: XR + Johnson expansion => |unpaid A_{u,v}| <= n^B * FM-term
=> R2 (same consumer chain as SPI; either wall suffices).
```

The precise per-edge inequality (what exactly the rank-one update forces —
a degree drop, a syndrome collision, a shared root) is the open content;
candidate: the one-exchange residual-degree ledger of #152 generalized from
`t = 2` to the in-band window. That generalization is a concrete,
bottom-up-lane-shaped lemma target.

## 4. Relation to front alpha [SKETCH]

The #170 open target `gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1` compares SHIFT-h
spectra — the shift is the window-direction analogue of an exchange, and
"no common root across shifts" is exactly "alignment does not survive the
atomic move" in the regular window. Front alpha is XR's regular-window
shadow (prediction P1 refines to: alpha holds because generic rank-one
updates kill alignment). An UNPAID alpha collision would falsify XR's
premise directly — a cheap, already-scheduled experiment (WP-2.1 scan).

## 5. Averaged version [SKETCH]

Second moments of `|A_{u,v}|` over `(u,v)` (or over slopes) are explicit
Cauchy double sums over pairs `(T, T')` graded by intersection size — the
Johnson-scheme decomposition applies, and the `lam_0 - lam_1 = n` gap gives
clean variance control. This is exponential-sum-friendly (the Hooley-Katz /
Scott lane): the AVERAGED form of XR looks provable with current tools and
would upgrade the FM model from heuristic to "true for almost all pairs" —
leaving, as always, the worst-case de-correlation as the wall.

## 6. Mechanisms 1 vs 2 [assessment]

```text
same wall, two languages: SPI (incidence geometry) and XR (harmonic /
  exchange dynamics) both formalize "unstructured alignment is rare";
mech 1 strengths: clean classification target for exceptional varieties
  (ES-special = paid); provable base case at d=1 (WP-2.6, PR #172);
mech 2 strengths: dimension-free; atomic move fully explicit (Cauchy
  rank-one); averaged version plausibly provable NOW; direct contact with
  fronts alpha (#170) and the #152 exchange ledger;
bet: the eventual argument uses mech-2 language for the counting and
  mech-1 language for classifying the escapes.
```

## 7. Forks and failure branches

```text
F1: XR false via an unpaid high-neighbor-density configuration -> that
    configuration is a new ledger; S9 branch (prize resolved lower).
F2: per-edge inequality exists only for t <= t_0 (like #152's t=2) ->
    partial XR; pins agreements with small t — NOTE: in-band t is LARGE
    (t ~ n 2^-9 near cap), so small-t XR targets the LOW-t edge A ~ k
    (the A=265 exemplar, t=9!) — unexpectedly, partial XR at small t is
    exactly what prediction P2 needs. High-value partial.
F3: expansion argument needs density above what poly-size A_{u,v} has ->
    the pumping direction fails silently; fall back to moment methods +
    mech-1 classification.
F4: averaged XR provable but worst-case gap impassable -> document as the
    final frozen core (same object as prob:perfiber), hand to monodromy
    (BETA_2) and ES-type programs; the sketch then predicts the prize
    resolution WAITS on that single statement.
```

## 8. Queued refinements from this note

```text
- "#152 t=2 exchange ledger -> general t" as a named bottom-up lemma target
  (hand-off shaped for the Codex lane);
- unpaid-fibers-O(1) sub-sketch (shared with mechanism 1);
- averaged-XR second-moment computation plan (Johnson-scheme grading) —
  candidate for an actual experimental verifier at toy scale;
- prop:noanchor re-read against exchange/expansion arguments (F4 of mech 1,
  F3/F4 here);
- SPI/XR joint freeze note with the common consumer theorem.
```
