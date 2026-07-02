# FM1: exact aperiodic first moment for split locators

- **Status:** PROVED / local finite-field theorem, with toy verification.
- **DAG node:** `fm1`.
- **Roadmap role:** this proves the first-moment input stated as PROVABLE in
  `experimental/notes/roadmaps/proof_sketch/s2_paid_ledger.md`.  It supports
  the aperiodic safe-side model, but it is not a worst-case theorem.
- **Script:** `experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py`.
- **Artifact:** `experimental/data/certificates/fm1-exact-first-moment/fm1_exact_first_moment.json`.

## Statement

Let `F = F_q`, let `D subset F^*` have size `n`, and let `k < A <= n`.
Put

```text
t = A-k,      j = n-A.
```

For a root set `R subset D` of size `j`, define the split locator

```text
ell_R(X) = prod_{r in R} (X-r).
```

For a word `w : D -> F`, define the locator-syndrome vector

```text
S_R(w) = ( sum_{x in D} w(x) ell_R(x) x^m )_{m=1..t} in F^t.
```

For independent uniform words `u,v : D -> F`, call `R` aligned if

```text
S_R(v) != 0
and
S_R(u) lies in the one-dimensional span F*S_R(v).
```

Then the expected number of aligned split locators is exactly

```text
E[# aligned R] = binom(n,j) * (1 - q^(-t)) * q^(1-t).
```

This is the finite-slope, nondegenerate alignment count.  It deliberately
excludes the `S_R(v)=0` degenerate direction, where the slope parameter is not
unique.

## Proof

Fix `R`, and let `E = D \ R`, so `|E| = A`.  The map

```text
w |-> S_R(w)
```

is linear from `F^D` to `F^t`.  The coordinates on `R` do not contribute,
because `ell_R` vanishes there.  On the remaining coordinates `E`, its matrix
has entries

```text
ell_R(x) x^m,       x in E,  1 <= m <= t.
```

For every `x in E`, both `ell_R(x)` and `x` are nonzero.  After scaling the
`x`-column by the nonzero factor `ell_R(x)x`, the matrix becomes the
Vandermonde row block

```text
x^(m-1),       x in E,  1 <= m <= t.
```

Since the elements of `E` are distinct and `|E|=A >= t`, this block has row
rank `t`.  Therefore `S_R` is surjective.

It follows that, for a uniform word `w`, the vector `S_R(w)` is uniform on
`F^t`.  Since `u` and `v` are independent, the pair

```text
(a,b) = (S_R(u), S_R(v))
```

is uniform on `F^t x F^t`.

The number of pairs `(a,b)` with `b != 0` and `a in F*b` is

```text
(q^t - 1) * q:
```

there are `q^t-1` nonzero choices for `b`, and each span `F*b` contains `q`
choices of `a`.  Thus, for this fixed locator,

```text
Pr[R aligned] = ((q^t - 1)q) / q^(2t)
              = (1 - q^(-t)) q^(1-t).
```

Finally there are `binom(n,j)` choices of `R`, and linearity of expectation
gives the formula.

## Consumer corollary

Let `N_A(u,v)` be the number of aligned split locators at agreement `A`.
For every `M >= 1`, Markov's inequality gives

```text
Pr_{u,v}[ N_A(u,v) >= M ]
    <= binom(n,j) * (1 - q^(-t)) * q^(1-t) / M.
```

In particular,

```text
Pr_{u,v}[ there exists an aligned split locator ]
    <= binom(n,j) * (1 - q^(-t)) * q^(1-t).
```

This is often the right diagnostic for whether a chart is generically empty.
It does **not** say that every pair has few aligned locators; all safe-side
work still needs a worst-case theorem or a paid-structure classification.

## Two-locator joint rank

The first step toward a second moment is to understand when two locator
syndrome maps are independent.  The answer is an exact overlap formula.

Let `R,T subset D` have size `j`, and put

```text
c = |R cap T|.
```

Let

```text
S_{R,T}(w) = (S_R(w), S_T(w)) in F_q^t x F_q^t.
```

Then

```text
rank S_{R,T} = 2t - max(0, t-j+c).
```

Equivalently, the only rank defect comes from the common polynomial identity
between `ell_R` and `ell_T`, and the defect dimension is

```text
h(R,T) = max(0, t-j+|R cap T|).
```

**Proof.**  A linear relation among the rows of the two syndrome matrices has
the form

```text
x ell_R(x) A(x) + x ell_T(x) B(x) = 0      for every x in D,
```

where `deg A, deg B <= t-1`.  Since `D subset F^*`, this is equivalent on `D`
to

```text
ell_R A + ell_T B = 0.
```

The degree of `x(ell_R A + ell_T B)` is at most `j+t=n-k<n`, so vanishing on
all `n` points of `D` forces the polynomial identity above.

Write `G=gcd(ell_R,ell_T)`, `ell_R=G r`, `ell_T=G s`; then
`deg G=c` and `r,s` are coprime of degree `j-c`.  The identity is

```text
r A + s B = 0.
```

Thus `s | A` and `r | B`, so

```text
A=sH,       B=-rH,
```

with `deg H <= t-1-(j-c)`.  The space of such `H` has dimension
`max(0,t-j+c)`, and there are no other relations.  Since there are `2t` rows,
the rank formula follows.

In particular, if `t < j-c`, the two locator-syndrome vectors are independent:
`S_{R,T}` is surjective onto `F_q^{2t}`.  If `t >= j-c`, all dependence is
explained by the explicit common-multiple family above.  This is the exact
overlap ledger that a later second-moment or exchange-rigidity calculation
has to price.

## Exact second moment

The joint-rank formula also gives an exact second moment for

```text
N_A(u,v) = #{R subset D : |R|=j and R is aligned}.
```

For two locators `R,T`, put

```text
c = |R cap T|,        h = max(0,t-j+c).
```

The joint image of

```text
w |-> (S_R(w), S_T(w))
```

has codimension `h` in `F_q^t x F_q^t`.  More precisely, after invertible
coordinate changes on the two `F_q^t` factors, it is the standard fiber
product

```text
U_h = { (x,y) in F_q^t x F_q^t : pi_h(x)=pi_h(y) },
```

where `pi_h` is projection to the first `h` coordinates.  This coordinate
normal form follows from the relation calculation above: the `h` relations
project injectively to each of the two locator-syndrome factors, so separate
basis changes put them in equality form.

For independent uniform pairs

```text
(A_R,A_T), (B_R,B_T) in U_h,
```

the probability that both locators align is

```text
P_h =
  [ q(q^h-1)q^{2(t-h)} + q^2(q^{t-h}-1)^2 ] / q^{4t-2h}.
```

Indeed, write a vector of `U_h` as `(z,p; z,q)` with
`z in F_q^h` and `p,q in F_q^{t-h}`.  If the common part `z` of
`(B_R,B_T)` is nonzero, then both `B_R` and `B_T` are nonzero and the two
alignment scalars must be equal, giving

```text
q(q^h-1)q^{2(t-h)}
```

favorable choices for `(A,B)`.  If `z=0`, then the two tails of `B` must both
be nonzero, and the two alignment scalars are independent, giving

```text
q^2(q^{t-h}-1)^2
```

favorable choices.  Since `|U_h|=q^{2t-h}`, the displayed formula follows.
It specializes correctly: `P_0` is the square of the one-locator probability,
while `P_t` is the one-locator probability for the diagonal case `R=T`.

Therefore the exact second moment is

```text
E[N_A^2]
  = sum_c binom(n,j) binom(j,c) binom(n-j,j-c)
      P_{max(0,t-j+c)},
```

where the sum ranges over valid overlaps `c`.  This is an ordered-pair sum:
choose `R`, then choose the `c` common roots and the `j-c` roots of `T`
outside `R`.

## Overlap-excess decomposition

Let

```text
p_1 = (1-q^{-t})q^{1-t}
```

be the one-locator alignment probability.  Since `P_0=p_1^2`, the second
moment can be written as an independent baseline plus an overlap-excess
ledger:

```text
E[N_A^2]
  = binom(n,j)^2 p_1^2
    + sum_{c >= j-t+1}
        binom(n,j) binom(j,c) binom(n-j,j-c)
        ( P_{t-j+c} - p_1^2 ).
```

Terms with invalid `c` are omitted.  Equivalently, all covariance between
distinct locator indicators is supported on high-overlap pairs

```text
|R cap T| >= j-t+1,
```

or, in symmetric-difference language,

```text
|R triangle T| <= 2(t-1).
```

This is the useful form for later exchange or averaged-slope arguments:
away from a thin high-overlap neighborhood in the Johnson graph, the locator
alignment indicators are independent.

Subtracting `E[N_A]^2` gives the exact variance formula

```text
Var(N_A)
  = sum_{c >= j-t+1}
        binom(n,j) binom(j,c) binom(n-j,j-c)
        ( P_{t-j+c} - p_1^2 ).
```

Therefore the relative variance is completely explicit.  For every
`epsilon > 0`, Chebyshev gives

```text
Pr[ |N_A - E[N_A]| >= epsilon E[N_A] ]
  <= Var(N_A) / (epsilon^2 E[N_A]^2),
```

and, in particular,

```text
Pr[N_A = 0] <= Var(N_A) / E[N_A]^2.
```

Thus whenever the high-overlap ledger is small relative to the independent
baseline, the averaged model is genuinely concentrated, not merely correct in
expectation.  This is the exact second-moment form needed by any later
averaged-slope conversion.

In the slack-one case `t=1`, only the diagonal `R=T` has positive defect.
Thus distinct locator indicators are pairwise independent and

```text
Var(N_A) = binom(n,j) p_1(1-p_1).
```

This does not imply higher-order independence, but it identifies the exact
second-moment obstruction at the first slack rung.

## Dependency graph consumer

The overlap-excess formula has a useful graph-theoretic form.  Put the
Johnson distance between two locators `R,T` as

```text
d(R,T) = j - |R cap T|.
```

The joint-rank defect is

```text
h(R,T) = max(0,t-d(R,T)).
```

Therefore the locator indicators are pairwise independent whenever

```text
d(R,T) >= t.
```

Equivalently, all covariance is supported in the radius-`t-1` Johnson ball
around each locator.  The exact dependency degree, excluding the locator
itself, is

```text
Delta_t(n,j)
  =
  sum_{d=1}^{min(t-1,j,n-j)}
      binom(j,d) binom(n-j,d).
```

This is not a worst-case MCA bound, but it is the right local object for
exchange-rigidity and averaged-slope arguments: FM1 is independent outside a
printed Johnson neighborhood, and every remaining covariance edge is exactly
one of the high-overlap terms in the second-moment ledger.

## Dependency-degree concentration criterion

The dependency graph gives a coarser but very portable concentration
criterion.  Let

```text
D_t(n,j)
  =
  sum_{d=0}^{min(t-1,j,n-j)}
      binom(j,d) binom(n-j,d)
```

be the radius-`t-1` Johnson neighborhood size, including the locator itself.
Then

```text
Var(N_A) <= E[N_A] * D_t(n,j),
```

and therefore

```text
Var(N_A) / E[N_A]^2 <= D_t(n,j) / E[N_A].
```

**Proof.**  Write `N_A=sum_R I_R`.  The dependency-graph consumer says
`Cov(I_R,I_T)=0` unless `d(R,T)<t`.  For every remaining ordered pair,

```text
Cov(I_R,I_T) <= Pr[I_R=I_T=1] <= Pr[I_R=1] = p_1.
```

For each fixed `R`, there are exactly `D_t(n,j)` possible `T` in the
dependency neighborhood.  Summing over ordered pairs gives

```text
Var(N_A)
  =
  sum_{R,T} Cov(I_R,I_T)
  <=
  binom(n,j) D_t(n,j) p_1
  =
  E[N_A] D_t(n,j).
```

This criterion is deliberately weaker than the exact second-moment formula,
but it has the right shape for later consumers: if the FM1 mean is larger than
the Johnson dependency neighborhood, then `N_A` is nonzero with positive
average probability, and if the mean dominates that neighborhood by a large
factor, the averaged model is concentrated.

## Exponent-form concentration consumer

For ledger comparisons it is useful to package the previous criterion in
`n^B` form.  Since

```text
D_t(n,j) <= n^{2(t-1)},
```

the dependency-degree criterion gives

```text
Var(N_A) / E[N_A]^2 <= n^{2(t-1)} / E[N_A].
```

Consequently, for every `s >= 0`,

```text
E[N_A] >= n^{2(t-1)+s}
    implies
Var(N_A) / E[N_A]^2 <= n^{-s}.
```

The bound `D_t(n,j) <= n^{2(t-1)}` is the same common-core cover recorded in
the Conjecture F reduction packet: the radius-`t-1` Johnson ball is covered by
charts indexed by `(j-t+1)`-root cores.  Thus the exponent `2(t-1)` is not an
extra probabilistic loss; it is the explicit common-root ledger cost of the
FM1 covariance neighborhood.

## Random-pair phase criterion

Combining the Markov and dependency-degree consumers gives a two-sided
random-pair phase test.

Let

```text
mu = E[N_A],
        D = D_t(n,j).
```

Then

```text
Pr[N_A > 0] <= mu,
```

and

```text
Pr[N_A = 0] <= D/mu,
Pr[ |N_A-mu| >= eps mu ] <= D/(eps^2 mu).
```

Thus a tiny FM1 mean proves random-pair emptiness, while a mean that dominates
the dependency neighborhood proves random-pair nonemptiness and concentration.
In exponent form, for every `s,r >= 0`,

```text
mu <= n^{-s}
    implies
Pr[N_A > 0] <= n^{-s},

mu >= n^{2(t-1)+s}
    implies
Pr[N_A = 0] <= n^{-s},

mu >= n^{2(t-1)+s+2r}
    implies
Pr[ |N_A-mu| >= n^{-r} mu ] <= n^{-s}.
```

This criterion is average-over-word-pairs only.  It does not classify
worst-case pairs.  Its value is that it tells later M5/M6 and XR arguments
exactly where the random model is already theorem-backed and where
worst-case rigidity is genuinely required.

## Averaged-existence consumer

The exact second moment gives the following immediate averaged-existence
corollary.  For every `0 <= theta < 1`,

```text
Pr[ N_A(u,v) >= theta E[N_A] ]
  >= (1-theta)^2 E[N_A]^2 / E[N_A^2].
```

In particular,

```text
Pr[ N_A(u,v) > 0 ] >= E[N_A]^2 / E[N_A^2].
```

This is just Paley-Zygmund applied to the nonnegative random variable `N_A`.
Its value is not the inequality itself, but that the preceding formula makes
the denominator explicit as a finite ordered-overlap sum.  Thus the FM1 packet
now supplies both sides of an averaged slope-existence test: Markov gives a
generic-emptiness upper tail when the mean is tiny, while this corollary gives
an averaged nonemptiness lower bound when the second moment is comparable to
the square of the mean.

This remains an average-over-word-pairs statement.  It does not classify
worst-case pairs and it does not replace the Conjecture F / exchange-rigidity
work needed for the safe side.

For the finite row

```text
C = RS[F_17^32, H, 256],     n=512,     k=256,
```

in the regular M3 window `385 <= A <= 426`, the verifier records the upper
bound

```text
log2 E[N_A] <= log2 binom(512,512-A) + (1-(A-256)) log2(17^32).
```

At the endpoints:

```text
A=385:  log2 E[N_A] < -16320
A=426:  log2 E[N_A] < -21760
```

and every `A` in the window has

```text
Pr[there exists an aligned split locator] < 2^-16000
```

for a random word-pair.  Thus any obstruction in this window is necessarily a
highly structured worst-case phenomenon, not random-pair mass.  This is a
sanity check for the M3/M5 chart program, not a replacement for root tables.

## Verification

The verifier records ten checks.

1. **Surjectivity check, `F_13`.**  For `D=F_13^*`, `n=12`, `k=3`,
   `A=8`, `t=5`, `j=4`, every one of the `binom(12,4)=495`
   locator-syndrome maps has rank `5`.
2. **Two-locator joint rank check, `F_13`.**  For the same row, every ordered
   pair of split locators satisfies

```text
rank S_{R,T} = 2t - max(0,t-j+|R cap T|).
```

3. **Joint-probability fiber-product check, `F_5`.**  For `t=2`, the verifier
   enumerates the standard fiber products `U_h`, `h=0,1,2`, and checks the
   displayed `P_h` formula exactly.
4. **Overlap-excess decomposition check.**  The verifier checks the baseline
   plus high-overlap correction identity in two finite parameter sets.  In the
   slack-one case it also verifies the pairwise-independence variance formula.
   The JSON artifact records exact relative variance and Chebyshev bounds for
   both examples.
5. **Dependency graph consumer.**  The verifier records exact Johnson-ball
   dependency degrees for small and deployed-shape parameter sets.  In
   particular it checks that covariance is supported precisely at distances
   `d<t`; when `t` exceeds the maximum Johnson distance, the dependency graph
   is complete, as expected.
6. **Dependency-degree concentration criterion.**  The verifier compares the
   exact relative variance against the portable bound `D_t/E[N_A]` in three
   finite parameter sets, including the `F_13` row used for the rank checks.
7. **Exponent-form concentration consumer.**  The verifier checks the
   arithmetic implication
   `E[N_A] >= n^{2(t-1)+s} => Var(N_A)/E[N_A]^2 <= n^{-s}` in small and
   deployed-shape parameter rows.
8. **Random-pair phase criterion.**  The verifier checks one low-mean finite
   row, one dependency-dominated finite row, one borderline finite row, and
   two exponent-form phase implications.
9. **Exact brute-force check, `F_5`.**  For `D=F_5^*`, `n=4`, `k=1`,
   `A=3`, `t=2`, `j=1`, enumeration over all `5^8` word pairs gives

```text
total aligned locators = 300000
mean = 96/125
second moment = 912/625
Pr[N_A > 0] = 332/625
Paley-Zygmund lower bound = 192/475
```

matching the formula

```text
binom(4,1) * (1 - 5^(-2)) * 5^(-1) = 96/125.
```

and the exact second-moment / Paley-Zygmund formulas above.

10. **F17 regular-window consumer scale.**  For `F_17^32`, `n=512`, `k=256`,
   the script computes the FM1/Markov one-locator upper bound across
   `385 <= A <= 426` and verifies the endpoint ranges above.

## Scope

FM1 is a mean statement over random word pairs and aligned locators.  It does
not by itself prove:

```text
worst-case safe-side bounds;
bad-slope bounds;
fiber-to-slope conversion;
or the aperiodic local limit.
```

Those require the separate concentration, fiber-rigidity, and paid-ledger
steps tracked elsewhere in the roadmap.  The contribution here is that the
first-moment input used by those steps is exact rather than heuristic.

## Reproduce

```bash
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py --emit
```
