# M1 Support Coefficient Test for Residue-Line Packing

## Claim

Let `C = RS[F,D,k]`, let `S subset D` have size `s > k`, and put
`t = s - k`. For a word `v:D -> F`, let `I_S(v)` be the unique polynomial of
degree `< s` agreeing with `v` on `S`. Define the top-coefficient obstruction

```text
Pi_S(v) = (coeff_X^k I_S(v), ..., coeff_X^(s-1) I_S(v)) in F^t.
```

Then `v|S` is explained by a codeword of `C` if and only if `Pi_S(v) = 0`.
For a line `u_z = f + z g`, a support `S` witnesses that `z` is
support-wise MCA-bad if and only if

```text
Pi_S(f) + z Pi_S(g) = 0
```

and not both `Pi_S(f)` and `Pi_S(g)` vanish. Equivalently:

- if `Pi_S(g) = 0`, then `S` contributes no bad slope;
- if `Pi_S(g) != 0`, then `S` contributes exactly one bad slope precisely when
  `Pi_S(f)` lies in the one-dimensional span of `Pi_S(g)`;
- in that case, if `Pi_S(f) = lambda Pi_S(g)`, the bad slope is `z = -lambda`.

Thus arbitrary-line MCA at fixed agreement size is exactly a collinearity
problem among the support top-coefficient vectors.

## Status

PROVED as a local finite-dimensional lemma. This does not prove the final M1
residue-line local limit; it isolates the exact support invariant that such a
proof or scanner has to control.

## Proof

The first assertion is just interpolation. Since `I_S(v)` is the unique
degree-`< s` interpolant on `S`, the restriction `v|S` agrees with a
degree-`< k` polynomial if and only if all coefficients in degrees
`k, ..., s-1` of `I_S(v)` vanish, i.e. if and only if `Pi_S(v) = 0`.

Linearity of interpolation gives

```text
I_S(f + z g) = I_S(f) + z I_S(g),
```

so

```text
Pi_S(f + z g) = Pi_S(f) + z Pi_S(g).
```

The line point `f + z g` is code-explained on `S` exactly when this vector is
zero. The support-wise MCA noncontainment condition says that there are not
two codewords explaining `f` and `g` separately on `S`, which is exactly the
condition that `Pi_S(f)` and `Pi_S(g)` are not both zero.

The three cases now follow from solving one vector equation in the scalar `z`.
If `Pi_S(g) = 0`, then either `Pi_S(f) = 0`, in which case the line is
explained on `S` for every `z` but the noncontainment condition fails, or
`Pi_S(f) != 0`, in which case no `z` solves the equation. If `Pi_S(g) != 0`,
there is a solution exactly when `Pi_S(f)` is a scalar multiple of `Pi_S(g)`,
and the scalar gives the unique bad slope.

This also recovers Paper B's one-bad-parameter-per-support theorem for
Reed-Solomon codes: a fixed support contributes at most one slope.

## Exact Minimal-Support Reduction

For a radius `delta < 1 - k/n`, put

```text
s_delta = ceil((1 - delta) n).
```

Then `s_delta > k`, and every support-wise MCA-bad slope has a witness of
exactly `s_delta` points.

Indeed, suppose `z` is witnessed by `S` with `|S| >= s_delta`. The line point
is code-explained on every subset of `S`. Since `f` and `g` are not both
code-explained on `S`, at least one of them, say `v`, is not degree-`< k` on
`S`. Hence some `(k+1)`-subset `T subset S` is not degree-`< k` for `v`;
otherwise every `(k+1)`-subset would lie on a degree-`< k` polynomial, forcing
all of `v|S` to do so: fix any `k` points, interpolate the unique degree-`< k`
polynomial through them, and add each remaining point one at a time. Extend `T`
inside `S` to a set `S0` of size `s_delta`. Then `f + z g` is still
code-explained on `S0`, while `f` and `g` are still not both code-explained
there. Thus `S0` is a witness of exact size `s_delta`.

Consequently the bad-slope set of a fixed line at radius `delta` is exactly

```text
Union over |S| = s_delta of
{ -lambda : Pi_S(g) != 0 and Pi_S(f) = lambda Pi_S(g) }.
```

This gives a finite scanner target with no larger-support ambiguity.

## Quotient-Occupancy Incidence Decomposition

Suppose now that the domain is partitioned into quotient fibers

```text
D = B_1 disjoint union ... disjoint union B_N,        |B_i|=m.
```

For exact support size `s`, let `A_h` be the supports with quotient-fiber
occupancy histogram `h=(h_0,...,h_m)`, as in
`experimental/m1_quotient_periodic_overlap_profile.md`.  For fixed line data
`f,g`, define

```text
Inc_h(f,g) = {
  (S,z) : S in A_h, Pi_S(f)+z Pi_S(g)=0,
          Pi_S(f),Pi_S(g) not both zero
}.
```

Then the exact-support incidence set decomposes as the disjoint union

```text
Inc_s(f,g) = disjoint union_h Inc_h(f,g),
```

where `h` ranges over all histograms with

```text
sum_a h_a=N,        sum_a a h_a=s.
```

Moreover each support contributes to at most one slope, namely
`z=-lambda` when `Pi_S(f)=lambda Pi_S(g)` and `Pi_S(g) != 0`. Thus a finite
scanner can label every exact-support incidence by quotient-fiber occupancy,
compare the observed support count in each class with the closed formula for
`|A_h|`, and pair the incidence data with the structured overlap ledger
`H_h(y)` from the quotient-profile note.

The proof is only bookkeeping. Every exact support has a unique occupancy
histogram, so the sets `A_h` partition the layer `|S|=s`. Applying the
support-coefficient criterion support by support gives the displayed incidence
partition and the one-slope-per-support assertion.

## Recovery of the Canonical Slack Formula

Take the canonical slack line from Paper B,

```text
u_z = X^(k+T) + z X^k,
```

and a support `S` of size `s = k + T`. Let

```text
L_S(X) = product_{x in S} (X - x)
       = X^s - e_1(S) X^(s-1) + ... + (-1)^T e_T(S) X^k + lower terms.
```

Modulo `L_S`, the top coefficients of `X^s + z X^k` are zero exactly when

```text
e_1(S) = ... = e_(T-1)(S) = 0,
z = (-1)^T e_T(S).
```

Thus the support coefficient test recovers the exact multi-symmetric image
`B_T(D,k)` in Paper B's slack characterization. The general arbitrary-line
case replaces this special elementary-symmetric vector by the pair
`Pi_S(f), Pi_S(g)`.

## Canonical Quotient-Core Factorization

The canonical elementary-symmetric test interacts cleanly with quotient
fibers. Suppose the domain is partitioned into fibers

```text
B_i = {x in D : x^m = y_i},
```

so each whole fiber has vanishing polynomial `X^m-y_i`.  For a support `S`,
let `W(S)` be the union of the whole fibers contained in `S`, and let

```text
R(S) = S \ W(S)
```

be the residual partial-fiber set. Then

```text
L_S(X) = L_{W(S)}(X) L_{R(S)}(X),
L_{W(S)}(X) = product_{B_i subset S} (X^m-y_i) in F[X^m].
```

Since `L_{W(S)}` has no terms whose degree deficit is strictly between `1`
and `m-1`, the low elementary-symmetric coefficients are invisible to the
whole quotient core:

```text
e_d(S) = e_d(R(S))        for 1 <= d < m.
```

Consequently, for the canonical slack line `X^(k+T)+zX^k` with `T <= m`, an
exact support `S` contributes a bad slope if and only if

```text
e_1(R(S)) = ... = e_(T-1)(R(S)) = 0.
```

The slope is still

```text
z = (-1)^T e_T(S).
```

If `T < m`, the slope is also `z=(-1)^T e_T(R(S))`; at the boundary `T=m`,
the slope may additionally see the quotient-core coefficient from
`L_{W(S)}`.

This is a useful separation. Whole-fiber quotient structure automatically
satisfies the canonical zero-prefix equations, while dimension dither that
prevents exact whole-fiber supports leaves a residual partial-fiber
zero-prefix problem. For example, in the multiplicative-domain setting a
one-point residual set never satisfies `e_1(R)=0`, so maximal dither removes
the canonical quotient-locator incidence at every slack `T>=2` with `T<=m`;
the one-remainder overlap ledger remains relevant for arbitrary or random
line data, but it is not itself a canonical quotient-locator source in this
range.

This residual problem has an exact low-weight cutoff. Assume `D subset F^*`,
put `b=|R(S)|`, and keep `T<=m`. If

```text
0 < b < T,
```

then `S` cannot contribute to the canonical slack line. Indeed, the zero-prefix
condition on `R(S)` would include `e_b(R(S))=0`, but

```text
e_b(R(S)) = product_{x in R(S)} x != 0.
```

At the boundary `b=T`, the residual zero-prefix condition is also completely
rigid:

```text
e_1(R)=...=e_(T-1)(R)=0
```

if and only if the residual vanishing polynomial has the form

```text
L_R(X) = X^T - c,
```

equivalently all residual points have the same `T`-th power. Thus a boundary
residual contribution is exactly a full root set of `X^T-c` inside the
multiplicative domain, and for `T<m` its slope is `z=-c`. If `T=m`, such a
residual set would be a whole quotient fiber and hence is absorbed into
`W(S)`, so no nonempty residual boundary case remains.

## M1 Impact

This turns the positive M1 problem into a precise incidence question:

```text
How many distinct slopes can arise from support collinearities
Pi_S(f) in span(Pi_S(g))
after tangent and quotient-periodic families are separated?
```

For `t = 1`, every nonzero `Pi_S(g)` is automatically collinear with
`Pi_S(f)`, which is the linear-algebra shadow of the tangent floor. For
`t >= 2`, collinearity has codimension `t - 1` in the random-support model,
which is the heuristic reason the aperiodic packing number should collapse
once the corrected reserve clears the quotient floors.

The note is therefore a bridge between the coordinate definition of
support-wise MCA and the residue-line normal form: denominator closure
parameterizes structured ways in which these top-coefficient vectors can align,
while this test is the exact finite support criterion that a proof or
experiment can check directly.
The quotient-occupancy decomposition adds a second label to the same incidence
problem: after supports are grouped by fiber content, the quotient-structured
part can be compared against the exact `H_h` ledger before any remaining
support-collinearity is called aperiodic.
The canonical quotient-core factorization sharpens this in the monomial
slack line: for `T<=m`, whole quotient fibers can be stripped away before
checking the zero-prefix equations, leaving a concrete residual
partial-fiber symmetric-zero problem.
The low-residual cutoff then proves that residual packets of total size
`1,...,T-1` are harmless for the canonical quotient-locator line over a
multiplicative domain; the first possible residual canonical obstruction is
the rigid boundary case `|R|=T`, where the residual set must itself be a
`T`-power fiber.

## Suggested Next Step

The script `experimental/m1_support_occupancy_scan.py` is the current small M1
scanner around `Pi_S` and quotient-fiber occupancy. It can be run, for example,
as

```bash
python3 experimental/m1_support_occupancy_scan.py \
  --prime 17 --n 8 --k 4 --slack 2 --quotient-order 4
```

The next step is to run this on more tiny fields and line families, then compare
the observed histogram incidence counts with the occupancy-profile random-line
ledger before attacking the genuinely aperiodic packing number. For the default
canonical line, the scanner also verifies the elementary-symmetric slope
formula and the quotient-core invisibility identity `e_d(S)=e_d(R(S))` for
`d<m`. It also checks the low-residual exclusion and the boundary coset
classification on every scanned support.
