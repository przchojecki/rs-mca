# Conjecture F Dimension-Two Skeleton

**Status.** PROVED reduction lemma, with an exhaustive finite toy replay.

**DAG node.** `f_dim2_skeleton`.

**Object / sampler / denominators.** This is not a threshold statement.  It is
an algebraic reduction for projective planes inside the degree-`<= j` locator
space.  No MCA/list sampler or `q_gen`, `q_line`, `q_chal` denominator is used.

## Statement

Let `K` be a field, let `H subset K` be finite, and let
`W <= K[X]_{<= j}` be a vector subspace with projective dimension two.  Assume
`W` has no common root on `H`.  For each `h in H`, write

```text
E_h = { [L] in P(W) : L(h)=0 }.
```

Thus the `E_h` are projective lines in the plane `P(W)`.  Group domain points
by equality of these evaluation lines:

```text
h ~ h'  <=>  E_h = E_{h'}.
```

Call a class of size at least two a twin class, and let `s` be the number of
singleton classes.  Then the divisor points

```text
P(W) cap D_j(H)
```

split into two parts.

1. If a divisor point meets a twin class `C`, it contains every root of `C`.
   The `C`-containing branch has common divisor
   `G_C(X)=prod_{h in C}(X-h)` and, after division by `G_C`, injects into a
   projective line section of `D_{j-|C|}(H \ C)`.
2. The residual branch avoiding all twin classes satisfies

```text
# residual <= binom(s,2) / binom(j,2).
```

In particular, repeated evaluation-line classes are not a new primitive
dimension-two source for Conjecture F: they are common-GCD charts one degree
lower, while the genuinely simple part is controlled by pair counting.

## Proof

If `E_h=E_h'`, then the two evaluation functionals on `W` have the same kernel
and hence are proportional.  Therefore, for every `L in W`,

```text
L(h)=0  <=>  L(h')=0.
```

The same argument applies to every member of a twin class `C`.  Any divisor
point meeting `C` is therefore divisible by `G_C`.  Restricting to the shared
line `E_C` cuts the projective plane `P(W)` by one linear equation, so the
subspace of polynomials in `W` divisible by `G_C` has projective dimension at
most one.  Division by `G_C` is the common-GCD reduction, giving an injection
into a projective line section of `D_{j-|C|}(H \ C)`.

Now consider a residual divisor point.  It avoids every twin class, so its `j`
roots lie on `j` distinct singleton evaluation lines.  It is charged by the
`binom(j,2)` unordered pairs of those lines.  Two distinct lines in a
projective plane meet in at most one point, so these pair charges are disjoint
over residual divisor points.  There are only `binom(s,2)` singleton line
pairs, proving the displayed bound.

## Replay

The script
`experimental/scripts/verify_conjecture_f_dim2_skeleton.py` exhaustively checks
the degree-3 model over `F_17` with `H=F_17^*`.  It enumerates all projective
planes in `P(K[X]_{<=3})`, routes common-root planes to the paid common-GCD
case, and verifies on every remaining plane that:

- twin classes are all-or-none for degree-3 locators;
- every nonempty twin branch divides by its class locator and lands in a
  projective line section;
- the residual branch obeys the sharp singleton-pair bound.

Replay:

```bash
python3 experimental/scripts/verify_conjecture_f_dim2_skeleton.py --emit
python3 experimental/scripts/verify_conjecture_f_dim2_skeleton.py --check \
  experimental/data/certificates/conjecture-f-dim2-skeleton/conjecture_f_dim2_skeleton.json
```
