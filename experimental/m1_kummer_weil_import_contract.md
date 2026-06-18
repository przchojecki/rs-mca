# M1 Depth-Two Kummer-Weil Import Contract

**Status:** CONDITIONAL / AUDIT.

This note isolates the single non-elementary character-sum input used by the
M1 slack-two depth-two certificates in
`m1_depth_two_lift_window_theorem.md`. It is not a proof of the imported
estimate; it states the exact import and records which hypotheses are already
checked by the scanner/verifier.

## The Import

Let `p>3`, let `psi` be a multiplicative character of `F_p^*`, extended by
zero at `0`, and put

```text
w = -1-u-v,
A(u,v) = -(u^2 + v^2 + uv + u + v + 1).
```

For exponents `(a,b,c,d)` modulo the order of `psi`, with `d != 0` and
`(a,b,c) != (0,0,0)`, the imported estimate is

```text
| sum_{u,v in F_p} psi(u^a v^b w^c A(u,v)^d) | <= 16p.        (KW_2)
```

Equivalently, on the Kummer open set

```text
U = A^2 - V(u v (-1-u-v) A(u,v)),
```

the rank-one Kummer sheaf with local monodromy vector `(a,b,c,d)` has total
Frobenius trace bounded by `16p`.

This is the only non-elementary estimate still used by the raw, two-fiber,
fixed-window, and quotient-window union saturation certificates. It is now
paid only for mixed terms in which the conic exponent and at least one of the
three coordinate exponents are nonzero. All later coefficients are finite
Fourier bookkeeping around this same input.

When `d=0`, the conic factor is absent and the sum is a three-character
Jacobi sum:

```text
sum_{u+v+w=-1} psi^a(u) psi^b(v) psi^c(w).
```

If `(a,b,c)` is not the zero triple, the standard Jacobi-sum recursion bounds
this by `p`. Indeed, after scaling the right side from `-1` to `1`, it is a
constant of modulus at most one times `J(psi^a,psi^b,psi^c)`, and the usual
two-character Jacobi bounds give absolute value at most `p`, including the
cases where one character or the product character is trivial.

When `d != 0` but `(a,b,c)=(0,0,0)`, the sum is conic-only:

```text
sum_{u,v in F_p} psi^d(A(u,v)).
```

This also has an elementary `p` bound. Completing the square at
`u=v=-1/3` gives

```text
A(u,v) = -Q(U,V) - 2/3,
Q(U,V) = U^2 + UV + V^2.
```

The form `Q` is nondegenerate, and with `epsilon=chi(-3)` its value
distribution is

```text
#{(u,v): A(u,v)=-2/3} = p + epsilon(p-1),
#{(u,v): A(u,v)=t}    = p - epsilon        for t != -2/3.
```

Therefore every nontrivial multiplicative character `eta` satisfies

```text
sum_{u,v} eta(A(u,v)) = epsilon p eta(-2/3),
```

so the conic-only terms have absolute value exactly `p`. Thus the
certificates now pay:

```text
d=0, coordinate nonprincipal:              p     (Jacobi)
d!=0, coordinate principal:                p     (affine conic)
d!=0, coordinate nonprincipal mixed terms: 16p   (imported KW_2)
```

## Audited Hypotheses

The scanner and verifier already check the following finite algebraic
conditions.

The radical divisor is reduced with component degrees

```text
1, 1, 1, 2,
```

so its total degree is `5`. The constant used in the certificates is

```text
(5-1)^2 = 16.
```

The three linear factors are distinct for `p>3`, and the conic `A=0` is a
nonzero smooth conic. The conic shares no component with the three lines.

The projective compactification is also elementary. Homogenize with
coordinates `[U:V:Z]`:

```text
Q(U,V,Z) = U^2 + V^2 + UV + UZ + VZ + Z^2.
```

The compactified boundary consists of

```text
U=0,        V=0,        U+V+Z=0,        Z=0,        Q=0.
```

The conic is smooth because its gradient matrix has determinant `4`, which is
nonzero for `p>3`. The four lines are distinct and have six pairwise
intersection points. At all six of these line-line intersections, `Q=1`, so
there is no triple point involving the conic. Restricting `Q` to each of the
four lines gives a binary quadratic with discriminant `-3`; since `p>3`, the
geometric intersections are simple. Thus the compactified divisor is a simple
normal-crossing line/conic arrangement over the algebraic closure.

The finite verifier

```bash
python3 experimental/verify_m1_kummer_divisor_geometry.py
```

checks these line-line, line-conic, smoothness, and transversality identities
on representative primes. It also checks the affine value distribution of
`A`, which is the finite audit behind the conic-only `p` bound. The symbolic
proof above is what matters for the uniform `p>3` statement.

For every imported mixed character tuple, at least two component exponents
are nonzero: the conic exponent and at least one coordinate-line exponent.
For every such tuple, at least one component exponent among

```text
u=0, v=0, -1-u-v=0, A=0
```

is nonzero. Hence the Kummer sheaf has nontrivial local monodromy around some
boundary component; equivalently, the summand is not a hidden character power
with trivial divisor data. This is the
`*_divisor_nontriviality_check` audited by
`verify_m1_slack_two_depth_two_kummer_saturation.py`.

The principal term and the elementary admissibility loss are independent of
the import and are computed exactly:

```text
|U(F_p)| = p^2 - 4p + 6 + 4 chi(-3),
```

and the six distinctness-failure lines have union size

```text
6p - 11.
```

## Why This Is Not a Direct Nonsingular Citation

Katz's nonsingular multiplicative character-sum theorem is the right
background source for constants of the form `(degree-1)^n q^(n/2)` in smooth
several-variable settings. However, the M1 divisor is the reducible divisor

```text
u v (-1-u-v) A(u,v)=0,
```

a union of three lines and a conic. It is singular at its crossings. Therefore
one should not cite the nonsingular single-hypersurface theorem as if it
directly applied to this product divisor.

The normal-crossing audit narrows the correct route to either:

1. a tame normal-crossing multiplicative character-sum theorem whose
   conductor/Euler-characteristic bound gives `16p` for this line/conic
   arrangement, or
2. a direct cohomology calculation for the rank-one Kummer sheaf on the above
   five-component compactified complement.

Rojas-Leon's singular multiplicative character-sum estimates are a plausible
reference class for this step, but the exact constant must still be checked
before the PR's conditional status can be upgraded to proved.

## Replacement Constant Ledger

If a later proof supplies

```text
|S(a,b,c,d)| <= C p
```

instead of `16p`, all M1 depth-two certificates remain valid after replacing
the scanner parameter `nonprincipal_constant=16` by `C`. The verifier already
checks that the reported radical degree, nontriviality audit, L1 coefficient
ledger, lower numerators, and thresholds are internally consistent for the
chosen constant.

Thus the import dependency is narrow: the rest of PR #79 is finite
character-expansion algebra, exact quotient-window reduction, and exact L1
coefficient accounting.

## Source Pointers

- Nicholas M. Katz, *Estimates for nonsingular multiplicative character
  sums*, International Mathematics Research Notices 2002, no. 7, 333-349,
  DOI `10.1155/S1073792802106088`.
- Antonio Rojas-Leon, *Estimates for singular multiplicative character
  sums*, International Mathematics Research Notices 2005, no. 20, 1221-1234,
  DOI `10.1155/IMRN.2005.1221`.
