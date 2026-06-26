# M2 High-Agreement Finite-Slope Frontier Gate

Status: PROVED / AUDIT / NOT A NEW LOWER-BOUND MECHANISM.

Agent/model: Codex.

Date: 2026-06-26.

## Purpose

The tangent staircase changes the finite-row frontier.  This note packages its
consequence as a row-level gate and records what remains open after the
`506/507` threshold for the active `F_17^32` row.

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

## Row-Level Gate

Fix a target `2^-eps_bits` and a line field size `q_line`.  Put

```text
B = floor(q_line / 2^eps_bits),
a0 = ceil((2n+k)/3).
```

Equivalently, put

```text
d0 = floor((n-k)/3).
```

Then the exact tangent range is `0 <= d <= d0`, and

```text
LD_sw(C,n-d) = d+1.
```

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

There are two boundary cases:

```text
B = 0:
  no finite agreement in the exact tangent range is within budget, because
  LD_sw(C,n)=1.

B >= n-a0+1:
  the entire exact tangent range is already within budget, so the first unsafe
  crossing, if any, lies below the range where the tangent upper bound is exact.
```

The second boundary case is the same as `B > d0`.

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
B = floor(17^32 / 2^128) = 6.
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
1. audit/formalize the tangent staircase and common residual budget;
2. state whether a projective-infinity slope is included in any external MCA
   convention, and if so account for it separately;
3. keep q_gen, q_line, and q_chal separate when translating the finite row to
   protocol or prize language;
4. study lower agreements a < ceil((2n+k)/3), where the tangent floor is only
   a lower bound and quotient/aperiodic mechanisms may still matter for
   mechanism ledgers and other target budgets, though not for the active row's
   `2^-128` finite-slope threshold because agreement `506` is already unsafe;
5. run the same gate calculation for other prize rows to decide whether their
   budget crossing lies inside or below the exact tangent range.
```

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_m2_high_agreement_frontier_gate.py
```

The verifier checks the active row arithmetic, edge cases for the row-level
gate, and sample parameter rows where the crossing lies inside, below, or
outside the exact tangent range.
