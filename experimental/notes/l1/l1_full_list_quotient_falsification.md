# L1 Full-List Quotient Falsification

Status: CONJECTURAL / EXPERIMENTAL / COUNTEREXAMPLE-FIRST.

Date: 2026-06-24.

Agent/model: Codex.

## Purpose

This note starts falsifying the quotient-budgeted L1 conjecture for the
repaired arbitrary-word object.  The object is the actual Reed--Solomon list,
equivalently the image locator fiber:

```text
ImgFib_U(s) = { P in F_q[X] : deg P < k and |{x in H : U(x)=P(x)}| >= s }.
```

It is not the raw support fiber.  The raw support fiber is already known to be
the wrong arbitrary-word theorem object, because one high-agreement codeword
contributes every `s`-subsupport of its agreement set.

The companion scanner is:

```text
python3 experimental/scripts/scan_l1_full_list_quotient_conjecture.py
```

## Quotient Ledger For The Full List

For `P in ImgFib_U(s)`, let

```text
A_P(U) = { x in H : U(x)=P(x) }.
```

For `s>k`, distinct listed polynomials have distinct agreement sets, so this
is a support-level object without raw multiplicity.  Define

```text
Stab(P;U) = { h in H : h A_P(U) = A_P(U) }.
```

The exact quotient budget is

```text
Q_d^list(U,s) = #{ P in ImgFib_U(s) : |Stab(P;U)| = d },
QuotientBudget^list(U,s) = sum_{d>1} Q_d^list(U,s).
```

The full-list primitive remainder is `Q_1^list(U,s)`.

The full repaired conjectural target is therefore:

```text
Q_1^list(U,k+sigma) <= n^B
```

uniformly in `U`, once the generated-field entropy reserve and the lower
cutoff `sigma >= C n/log n` clear.  Equivalently,

```text
|ImgFib_U(k+sigma)|
  <= QuotientBudget^list(U,k+sigma) + n^B.
```

This is the full-list analogue of the monomial-prefix primitive-remainder
target in `l1_quotient_budgeted_locator_conjecture.md`.

## Sparse-Syndrome Search

The repaired package identifies the list with a sparse syndrome ball.  Let
`M_C` be a parity-check matrix for `RS[F_q,H,k]`, and let
`z=M_C U`.  Then

```text
|ImgFib_U(s)| = #{ e in F_q^n : M_C e = z and wt(e) <= n-s }.
```

Moreover, the agreement set of the listed codeword is the zero set of `e`.
Thus exact quotient and primitive counts can be computed by grouping
low-weight errors by syndrome and then measuring the stabilizer of each zero
set.

This gives an exact all-received-word-coset scan whenever the Hamming ball

```text
sum_{j<=n-s} binom(n,j)(q-1)^j
```

is small enough to enumerate.

## Initial Results

The first exact sparse-syndrome scans are reserve-cleared and find no primitive
alerts at threshold `n`:

```text
F_5,  n=4,  k=2, s=3,  r=1: max list = 1, max Q_1 = 1
F_7,  n=6,  k=3, s=5,  r=1: max list = 1, max Q_1 = 1
F_11, n=10, k=5, s=9,  r=1: max list = 1, max Q_1 = 1
F_13, n=12, k=6, s=10, r=2: max list = 1, max Q_1 = 1
F_17, n=16, k=8, s=13, r=3: max list = 1, max Q_1 = 1
```

These rows are high-agreement enough to be in unique-decoding territory, so
they are sanity checks rather than strong evidence near the entropy boundary.

The sampled near-boundary scans are more informative.  They test random words,
planted near-codeword words, monomial words, and folded quotient words.  In the
first run there were no reserve-cleared primitive alerts.  The largest sampled
primitive remainder was `4`, occurring in the `F_97`, `n=16`, `k=8`, `s=10`
row; the `F_17`, `n=16`, `k=8`, `s=11` row reached primitive remainder `2`.
Folded codewords appear as quotient-budgeted mass rather than primitive mass,
as expected.

## Glued-Codeword Sunflower Attack

The first explicitly adversarial construction is a sunflower of agreement
sets.  Let `C subset H` have size `k-1`, let `T_1,...,T_M` be disjoint petals
in `H \ C` of size

```text
|T_i| = s-k+1 = sigma+1,
```

and assume `M < q`.  Put

```text
L_C(X) = prod_{x in C}(X-x),
P_i(X) = c_i L_C(X)
```

for distinct nonzero scalars `c_i`.  Define `U` by

```text
U(x) = P_i(x)  for x in T_i,
U(x) = 0       for x in C and on the unused background.
```

Since `L_C` vanishes exactly on `C`, each `P_i` agrees with `U` exactly on
`C union T_i`.  Therefore

```text
|ImgFib_U(s)| >= M,
M = min(q-1, floor((n-k+1)/(sigma+1))).
```

If the sets `C union T_i` have trivial cyclic stabilizer, this also gives

```text
Q_1^list(U,s) >= M.
```

This is not a counterexample to the polynomial conjecture.  At the corrected
lower cutoff `sigma ~ n/log n`, the construction gives a logarithmic primitive
floor.  It does show that one should not expect a uniform constant bound for
the primitive full-list remainder.

Finite sunflower scans gave:

```text
F_17, n=16, k=8, s=11: planted M=2, max Q_1 = 2.
F_97, n=16, k=8, s=10: planted M=3, max Q_1 = 5.
```

The `F_97` row is useful: random sunflower cores produced accidental extra
primitive codewords beyond the three planted ones, but still no
reserve-cleared alert at threshold `n=16`.

The scanner now has a support-subset decoder for sunflower rows and classifies
extra codewords by how their agreement sets intersect the sunflower core and
petals.  The extras are not new planted petals.  They have exact agreement size
`s`, retain only part of the common core, and mix points from all petals.
With seed `0`, a 20-core sweep reached maximum primitive remainder `5`; the
top row's two extra agreement sets had profiles

```text
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=1
agreement=10, core=4, petal_hits=6, petals=3, max_petal=3, full_petals=1
```

Across all 21 sunflower rows in that seed-`0` sweep, 12 rows had extras and
the aggregate extra-profile histogram was

```text
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=1 : 4
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=2 : 1
agreement=10, core=4, petal_hits=6, petals=3, max_petal=2, full_petals=0 : 3
agreement=10, core=4, petal_hits=6, petals=3, max_petal=3, full_petals=1 : 4
agreement=10, core=5, petal_hits=5, petals=3, max_petal=2, full_petals=0 : 5
```

With seed `3`, a 20-core sweep reached maximum primitive remainder `8` from a
planted floor of `3`.  Across its 21 sunflower rows, 13 had extras and the
aggregate extra-profile histogram was

```text
agreement=10, core=2, petal_hits=8, petals=3, max_petal=3, full_petals=2 : 2
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=1 : 3
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=2 : 1
agreement=10, core=4, petal_hits=6, petals=3, max_petal=2, full_petals=0 : 4
agreement=10, core=4, petal_hits=6, petals=3, max_petal=3, full_petals=1 : 5
agreement=10, core=5, petal_hits=5, petals=3, max_petal=2, full_petals=0 : 10
```

This mixed-petal amplification is the first nontrivial obstruction pattern
seen by the full-list attack.  It does not yet threaten polynomiality, but it
is a concrete subproblem for the conjecture: bound the number of accidental
mixed-petal codewords over a sunflower floor.  In both sweeps every extra
used only core and petal points (`core_hits + petal_hits = s`) and touched all
three petals.

A final seed sweep aggregated seeds `0,1,2,3` with eight random sunflower cores
per seed over `F_97,n=16,k=8,s=10`, using the support decoder and no additional
random samples.  It scanned 84 words, including 36 sunflower rows.  Of those
sunflower rows, 22 had extras, the maximum extra count in a row was `5`, and
the maximum primitive full-list remainder was still `8`, with no
reserve-cleared alert.  The aggregate extra-profile histogram was

```text
agreement=10, core=2, petal_hits=8, petals=3, max_petal=3, full_petals=2 : 1
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=1 : 4
agreement=10, core=3, petal_hits=7, petals=3, max_petal=3, full_petals=2 : 1
agreement=10, core=4, petal_hits=6, petals=2, max_petal=3, full_petals=2 : 1
agreement=10, core=4, petal_hits=6, petals=3, max_petal=2, full_petals=0 : 4
agreement=10, core=4, petal_hits=6, petals=3, max_petal=3, full_petals=1 : 9
agreement=10, core=5, petal_hits=5, petals=3, max_petal=2, full_petals=0 : 16
```

## Proof Target After This Attack

This is the stopping point for broad first-pass falsification.  The conjecture
has survived prefix-fiber scans, full-list exact syndrome checks, random and
folded samples, planted near-codeword samples, and the sunflower attack above.
The useful proof target exposed by the final attack is:

```text
Mixed-petal amplification lemma.
For sunflower received words with core size k-1 and petal size sigma+1,
the number of non-planted primitive listed codewords whose agreement sets
mix several petals is polynomially bounded, and preferably bounded by a
small polynomial in the planted sunflower floor.
```

A proof would not by itself prove full L1, but it would close the first
identified obstruction family for the repaired full-list quotient conjecture.
If this lemma fails, the counterexample should be a growing sunflower family
where mixed-petal extras dominate the planted floor.

## Interpretation

This does not prove the full L1 conjecture.  It does establish that the
current quotient-budgeted formulation passes the first full-list falsification
tests and that the scanner is targeting the correct repaired object.

The next useful step is no longer another broad random sweep.  It is to convert
the observed sunflower obstruction into proof obligations:

1. prove or falsify a mixed-petal amplification bound over sunflower floors;
2. add meet-in-the-middle sparse-syndrome scans for radius `4` and `5`;
3. optimize the interpolation backend enough to test larger high-field rows;
4. record any large primitive family as a new obstruction before attempting a
   proof.
