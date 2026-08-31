# A nonuniform hierarchical `T(509,35,8)` system for RS-MCA

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** exact finite theorem with two independent certificate checks.

## Definitions

Write `[n]={0,...,n-1}`.  A `T(n,s,r)` system is a family
`C subseteq binom([n],r)` such that every `s`-subset of `[n]` contains a
member of `C`.

If a block is split into six color classes and `F` is an eight-subset of the
block, its color pattern is the weak six-composition

```text
(|F intersect color 0|,...,|F intersect color 5|)
```

of eight.

## Fixed-asymptotic packing lemma

Let `K` be a field and `t>=2`.  For `i=1,2`, let `A_i` be monic of degree
`t`, and let `B_i` have degree at most `t-1`.  Write

```text
A_i = X^t + a_i X^(t-1) + lower terms.
```

Assume that, for fixed `q,alpha in K`,

```text
[X^(t-1)] B_i = q,
[X^(t-2)] B_i = alpha + q a_i.
```

If `B_1/A_1` and `B_2/A_2` are distinct rational functions, then they agree
at at most `2t-3` elements of `K` that are not poles of either function.

Indeed, agreement at `x` implies

```text
(A_1 B_2 - A_2 B_1)(x)=0.
```

The coefficients of degrees `2t-1` and `2t-2` in this cross numerator are

```text
q-q=0
```

and

```text
(alpha+q a_2)+q a_1-(alpha+q a_1)-q a_2=0.
```

The cross numerator is nonzero because the rational functions are distinct,
and its degree is therefore at most `2t-3`.  The root bound proves the claim.
In particular, at `t=5`, agreement on eight finite nonpole points determines
the rational function.  If both representations are reduced and their
denominators are monic of degree five, it determines the pair `(A,B)`.

## Nonuniform cover theorem

There is an explicit `T(509,35,8)` system `C` with

```text
|C| = 762,054,269,114.
```

Partition `[509]` into consecutive blocks `B_0,B_1,B_2` of sizes

```text
177, 166, 166.
```

In each block, color its local indices cyclically modulo six.  The resulting
color-class sizes are

```text
B_0: (30,30,30,29,29,29),
B_1: (28,28,28,28,27,27),
B_2: (28,28,28,28,27,27).
```

The certificate freezes `89`, `108`, and `108` weight-eight color patterns
for the three blocks.  The family `C` consists of all eight-subsets that lie
in one block and have a frozen pattern for that block.

### Coverage proof

Set the local witness thresholds to `(13,12,12)`.  If a 35-subset met all
three blocks below their thresholds, it would have size at most

```text
(13-1)+(12-1)+(12-1)=34,
```

a contradiction.  It therefore contains at least `h_j` points in some block
`B_j`, where `h=(13,12,12)`.

Choose `h_j` of those points and record their color composition `u`.  The
certificate checks every weak six-composition of `h_j`: each such `u`
coordinatewise dominates at least one frozen weight-eight pattern `p` for
the same block.  Selecting `p_l` points of color `l` gives a member of `C`
inside the original 35-subset.

The primary verifier exhausts all 666 weak three-compositions of 35 and all
weak six-compositions of the relevant local threshold.  The independent
auditor parses only the frozen pattern file and reconstructs the same checks
with a separate composition generator.

### Exact cardinality

For a pattern `p=(p_0,...,p_5)` in a block with color-class sizes
`c=(c_0,...,c_5)`, the number of represented eight-subsets is

```text
product_l binom(c_l,p_l).
```

Distinct patterns and distinct blocks represent disjoint subsets.  Exact
integer summation gives

```text
|C intersect binom(B_0,8)| = 254,104,519,142,
|C intersect binom(B_1,8)| = 253,974,874,986,
|C intersect binom(B_2,8)| = 253,974,874,986,
|C|                         = 762,054,269,114.
```

This is approximately 16.4229468510 percent smaller than the explicit
uniform six-color cover of size `911,798,442,756`.  It is smaller by factors
`3.5763488281` and `7.1526944775` than the parity and complete four-block
baselines of sizes `2,725,371,892,323` and `5,450,741,362,275`.

## RS-MCA consequence and scope

Suppose the active `t=5` rational sections satisfy the two fixed-asymptotic
coefficient identities above.  Every section with at least 35 agreement rows
then has an agreement support containing a selected eight-face.  On a
nonsingular selected face, the packing lemma permits at most one reduced
section.  Thus `C` gives a false-negative-free candidate-generation reduction,
provided singular faces and denominator poles are retained for separate
analysis.

The theorem proved here is the exact cover, its cardinality, and the packing
reduction.  The recorded CP-SAT result is `FEASIBLE`, not `OPTIMAL`; no
minimality claim is made.  This note does not report an exhaustive scan of all
selected faces, a global `d=474` exclusion, a Paper-D row, or a leaderboard
improvement.
