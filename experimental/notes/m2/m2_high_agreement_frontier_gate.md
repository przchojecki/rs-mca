# M2 High-Agreement Finite-Slope Frontier Gate

Status: PROVED / AUDIT / NOT A NEW LOWER-BOUND MECHANISM.

Agent/model: Codex.

Date: 2026-06-26.

## Purpose

The integrated tangent staircase and tangent-star theorem change the active
finite-row frontier.  This note packages their consequence as a row-level gate,
records the endpoint conventions, and checks that the same high-agreement
threshold survives the projective-slope convention.

The object here is finite-slope support-wise line decoding:

```text
LD_sw(C,a)
```

counts finite slopes whose line point has a support-wise noncontained
explanation at agreement at least `a`.  The denominator is the actual line
field `q_line`, not the generated field or a protocol challenge field unless a
separate theorem identifies them.

## Input Theorem

Let `C = RS[F,D,k]` and `n = |D|`.  The high-agreement tangent staircase proves
that, for every `a` with

```text
a >= ceil((2n+k)/3),
```

one has the exact finite-slope identity

```text
LD_sw(C,a) = n - a + 1.
```

This is not only a tangent lower bound in that range.  The upper bound uses the
common-code-line residual budget, so it counts all finite support-wise
noncontained slopes.

The integrated tangent-star refinement proves the extremal structure: whenever
equality holds and `n-a+1>=2`, an extremal finite-slope line has a common
code-line support `S0` of size `a-1`, and each finite bad slope is obtained by
moving exactly one residual root outside `S0`.

## Proof-Dependency Audit

The gate uses the tangent staircase in the following exact form.

1. **Moving-root lower floor.**  For `k+1 <= a <= n`, fix `A subset D` with
   `|A|=a-1`, set `B_A(X)=prod_{x in A}(X-x)`, and take

   ```text
   f = (X B_A)_{>=k},
   g = -(B_A)_{>=k}.
   ```

   For every `t in D\A`, the slope `t` is explained on `A union {t}` by the
   locator `(X-t)B_A(X)`.  Noncontainment uses `|A|=a-1 >= k`: a degree-`<k`
   explanation of `g` on `A union {t}` would be forced to equal `(B_A)_{<k}`
   on `A`, and then would force `B_A(t)=0`, contradiction.

2. **Two-slope common-code-line recovery.**  If two finite bad slopes at
   agreement at least `a` have supports `S_1,S_2`, then

   ```text
   |S_1 cap S_2| >= 2a-n.
   ```

   Under `3a-2n >= k`, one has `2a-n >= k`, so the two explaining codewords
   recover a common code line on the intersection.

3. **Residual-budget upper bound.**  Let `S_0` be a maximal common support for
   that recovered code line, write `b=|S_0|`, `s=n-a`, and `d=n-b`.  Since
   `b >= 2a-n`,

   ```text
   a+b-n >= 3a-2n >= k,
   ```

   so the common-code-line residual budget applies.  Maximality of `S_0` gives
   no common residual-zero coordinate outside `S_0`.  If `b>=a`, every
   noncontained slope needs an outside residual zero and there are at most
   `d<=s` such coordinates.  If `b<a`, each noncontained slope needs

   ```text
   h = a-b = d-s
   ```

   private outside residual zeros, and `s<d<=2s`, hence

   ```text
   floor(d/(d-s)) <= s+1 = n-a+1.
   ```

Together with the moving-root lower floor, this proves the exact identity in
the high-agreement range.  No quotient-periodic or smooth-domain assumption is
used in this exact range.

## Distance-Coordinate Form

It is often cleaner to write the agreement threshold as

```text
a = n-d,
```

where `d` is the integer Hamming distance allowed by a closed ball on the
length-`n` grid.  The exactness condition becomes

```text
3(n-d)-2n >= k,
```

or equivalently

```text
d <= floor((n-k)/3).
```

Thus, with redundancy `r=n-k`, the exact tangent staircase says

```text
LD_sw(C,n-d) = d+1        for every 0 <= d <= floor(r/3).
```

This is the form consumed by the frontier gate: the tangent theorem exactly
settles the first `floor(r/3)+1` distance levels nearest zero distance.

The lower half of the same theorem also remains useful outside the exact range:

```text
LD_sw(C,n-d) >= d+1       for every 0 <= d <= r-1.
```

So even when the budget crossing lies below the exact range, the tangent floor
still gives a first forced unsafe distance.

## Row-Level Gate

Fix a target `2^-eps_bits` and a line field size `q_line`.  Put

```text
B = floor(q_line / 2^eps_bits),
a0 = ceil((2n+k)/3).
```

Equivalently, put

```text
d0 = floor((n-k)/3),
d1 = n-k-1.
```

Then the exact tangent range is `0 <= d <= d0`, and

```text
LD_sw(C,n-d) = d+1.
```

The moving-root lower floor holds throughout `0 <= d <= d1`.

Since `LD_sw(C,a)` is an integer,

```text
LD_sw(C,a) / q_line <= 2^-eps_bits
```

is equivalent to

```text
LD_sw(C,a) <= B.
```

Therefore, if

```text
1 <= B <= d0,
```

then the exact tangent range contains the target crossing and gives

```text
LD_sw(C,n-B)     = B+1      unsafe,
LD_sw(C,n-B+1)   = B        within budget.
```

Equivalently, the largest safe integer Hamming radius in the exact tangent
range is `B-1`, while integer radius `B` is already unsafe.

For closed Hamming balls with real radius `delta`, the integer distance allowed
is `floor(delta n)`.  In the crossing-inside-exact-range case this means:

```text
closed ball:  safe for delta < B/n, unsafe at delta = B/n;
strict ball:  safe at delta = B/n, unsafe for every delta > B/n.
```

Thus `B/n` is the safe real-radius supremum under the closed-ball convention,
but it is not attained there.

There are three boundary cases:

```text
B = 0:
  no finite agreement level is within budget, because LD_sw(C,n)>=1.

d0 < B <= d1:
  the exact tangent range proves safety through distance d0, while the tangent
  floor proves unsafety at distance B.  The distances d0+1,...,B-1 remain a
  genuine gap for other mechanisms or sharper upper bounds.

B > d1:
  the tangent floor never crosses the target in the list-decoding range
  k+1 <= a <= n.  The exact range is safe, and this tangent mechanism alone
  gives no unsafe distance.
```

## Field-Size Window Corollary

Let

```text
Q = 2^eps_bits.
```

For fixed `n,k,eps_bits`, the tangent gate depends on the line field size only
through the integer budget

```text
B = floor(q_line/Q).
```

Thus the four cases above are equivalently the following disjoint `q_line`
windows:

```text
0 < q_line < Q:
  no finite agreement level is within budget;

Q <= q_line < (d0+1)Q:
  the target crossing lies inside the exact tangent range;

(d0+1)Q <= q_line < (d1+1)Q:
  the exact tangent range is safe, but the moving-root floor proves a later
  unsafe distance and leaves the gap d0+1,...,B-1;

(d1+1)Q <= q_line:
  the moving-root tangent floor never crosses the target in the list-decoding
  range k+1 <= a <= n.
```

More finely, for any integer `b` with `1 <= b <= d0`, the exact crossing occurs
at budget `B=b` precisely when

```text
bQ <= q_line < (b+1)Q.
```

In that subwindow one has

```text
LD_sw(C,n-b)   = b+1,
LD_sw(C,n-b+1) = b.
```

This corollary is only integer arithmetic applied to the row-level gate, but it
is useful when comparing candidate rows: it says exactly which field sizes put
the `2^-eps_bits` threshold inside the proved high-agreement staircase.

## Projective-Slope Convention Audit

The theorem above is deliberately finite-slope: the sampler is `z in F`, and
the probability denominator is `q_line=|F|`.  If an external line-decoding or
MCA convention instead samples the projective line `P^1(F)`, there is one extra
point, represented in an affine chart as the direction word `g` at infinity.

Let

```text
LD_sw^P(C,a)
```

be the corresponding support-wise noncontained count over `P^1(F)`.  For every
received line,

```text
finite bad slopes <= projective bad points <= finite bad slopes + 1.
```

The tangent-star structure removes the apparent one-point loss in the exact
range:

```text
LD_sw^P(C,n-d) = d+1        for every 0 <= d <= d0.
```

Proof.  The finite lower bound gives `LD_sw^P(C,n-d) >= d+1`.  For the upper
bound, set `a=n-d`.  If a line has at most `d` finite bad slopes, adding the
single point at infinity gives at most `d+1` projective bad points.

It remains to rule out the case of `d+1` finite bad slopes plus a bad infinity
point.  For `d=0`, a full-support bad infinity point means `g` is a codeword;
then any finite full-support codeword point `f+zg` would force `f` to be a
codeword as well, so the finite point would be contained.  Thus the projective
count is still at most one.

For `d>=1`, the tangent-star theorem applies to any line with `d+1` finite bad
slopes.  After subtracting the common code line, there is a set `S0` with

```text
|S0| = a-1 = n-d-1
```

on which the direction word is zero, and every coordinate in
`Omega=D\S0` has nonzero direction residual.  Any support `T` of size `a`
meets `S0` in at least

```text
|T|-|Omega| = (n-d)-(d+1) = n-2d-1
```

points.  Since `d <= floor((n-k)/3)` and `d>=1`, this is at least `k`.
Therefore any degree-`<k` codeword agreeing with the direction word on `T`
would be forced to be zero on those `k` points of `S0`; but `T` must also
contain at least one point of `Omega`, where the direction residual is nonzero.
So infinity is not a bad projective point for a finite extremizer.

If the projective sampler is uniform on `P^1(F)`, its integer budget is

```text
B_P = floor((q_line+1)/2^eps_bits).
```

Thus in the exact range the projective convention has the same count `d+1`,
but with denominator `q_line+1`.  It is within budget exactly when

```text
d+1 <= B_P.
```

This is still only a convention audit.  It does not alter finite-slope rows on
the public board, whose denominator is `q_line`.

## Active `F_17^32` Row

For

```text
C = RS[F_17^32,H,256],       |H| = 512,
q_line = 17^32,
eps_bits = 128,
```

the gate data are

```text
n = 512,
k = 256,
a0 = ceil((2n+k)/3) = 427,
d0 = floor((n-k)/3) = 85,
d1 = n-k-1 = 255,
B = floor(17^32 / 2^128) = 6,
B_P = floor((17^32+1) / 2^128) = 6.
```

Since

```text
1 <= 6 <= 85,
```

the exact tangent range contains the crossing:

```text
LD_sw(C,506) = 7       unsafe,
LD_sw(C,507) = 6       within budget.
```

Thus the closed grid radius `6/512 = 3/256` is unsafe under the finite-slope
support-wise convention, while integer radius `5` is safe.  Equivalently,
closed real radii `delta < 3/256` are safe for the finite-slope support-wise
object, and `delta = 3/256` is already unsafe; under a strict-ball convention
the endpoint `3/256` is safe but any larger radius is unsafe.

Under a projective-slope `P^1(F_17^32)` convention, the projective exactness
argument gives the same high-agreement counts in the exact range:

```text
LD_sw^P(C,507) = 6       within projective budget;
LD_sw^P(C,506) = 7       unsafe.
```

So the `506/507` gate survives the projective-slope convention for this row.

The old agreement-353 target is superseded: the tangent floor alone gives

```text
LD_sw(C,353) >= 512 - 353 + 1 = 160.
```

By monotonicity of `LD_sw(C,a)` in the agreement threshold, every lower
agreement `a <= 506` is also unsafe for the active row once `LD_sw(C,506)=7` is
known.  Thus the finite-slope support-wise `2^-128` threshold for this row is
fully pinned by the `506/507` gate, even though the exact tangent formula itself
only starts at agreement `427`.

## What Remains After This Gate

For the finite-slope support-wise object, no non-tangent mechanism can survive
past agreement `507` in this row: the exact theorem already bounds every finite
support-wise noncontained slope by six for all `a >= 507`.

The remaining useful frontier is therefore not "find seven slopes at agreement
353" or "find a non-tangent seventh finite slope at agreement 507".  The
remaining lanes are:

```text
1. formalize the tangent-star and projective-exactness corollaries if they are
   promoted out of experimental notes;
2. decide whether external CA, curve-MCA, or protocol conventions really use
   the finite/projective line-decoding object handled here, or a different
   object;
3. keep q_gen, q_line, and q_chal separate when translating the finite row to
   protocol or prize language;
4. study lower agreements a < ceil((2n+k)/3), where the tangent floor is only
   a lower bound and quotient/aperiodic mechanisms may still matter for
   mechanism ledgers and other target budgets, though not for the active row's
   `2^-128` finite-slope threshold because agreement `506` is already unsafe;
5. run the same gate calculation for other prize rows to decide whether their
   budget crossing lies inside the exact tangent range, below it with a genuine
   gap, or beyond the moving-root tangent floor.
```

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_m2_high_agreement_frontier_gate.py
```

The verifier checks the active row arithmetic, edge cases for the row-level
gate, and sample parameter rows where the crossing lies inside, below, or
outside the exact tangent range.
