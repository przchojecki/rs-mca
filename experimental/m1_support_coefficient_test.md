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

## Suggested Next Step

Build a small M1 scanner around `Pi_S` rather than around guessed residue-line
denominators:

1. fix `q,n,k,delta` and enumerate supports of size `s_delta`;
2. compute `Pi_S(f), Pi_S(g)` for chosen line families;
3. record the distinct slopes produced by collinear supports;
4. label supports by tangent, quotient-periodic, or aperiodic source.

This would make the conjectural aperiodic packing number directly measurable
in tiny fields without first choosing a denominator normal form.
