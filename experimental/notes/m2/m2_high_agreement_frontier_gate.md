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

## Row-Level Gate

Fix a target `2^-eps_bits` and a line field size `q_line`.  Put

```text
B = floor(q_line / 2^eps_bits),
a0 = ceil((2n+k)/3).
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
1 <= B < n - a0 + 1,
```

then the exact tangent range contains the target crossing and gives

```text
LD_sw(C,n-B)     = B+1      unsafe,
LD_sw(C,n-B+1)   = B        within budget.
```

Equivalently, the largest safe integer Hamming radius in the exact tangent
range is `B-1`, while integer radius `B` is already unsafe.

There are two boundary cases:

```text
B = 0:
  no finite agreement in the exact tangent range is within budget, because
  LD_sw(C,n)=1.

B >= n-a0+1:
  the entire exact tangent range is already within budget, so the first unsafe
  crossing, if any, lies below the range where the tangent upper bound is exact.
```

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
B = floor(17^32 / 2^128) = 6.
```

Since

```text
1 <= 6 < 512 - 427 + 1 = 86,
```

the exact tangent range contains the crossing:

```text
LD_sw(C,506) = 7       unsafe,
LD_sw(C,507) = 6       within budget.
```

Thus the closed grid radius `6/512 = 3/256` is unsafe under the finite-slope
support-wise convention, while integer radius `5` is safe.  The old
agreement-353 target is superseded: the tangent floor alone gives

```text
LD_sw(C,353) >= 512 - 353 + 1 = 160.
```

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
   a lower bound and quotient/aperiodic mechanisms may still matter;
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
