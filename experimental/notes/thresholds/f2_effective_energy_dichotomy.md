# F2 effective energy dichotomy: printed-constant high-energy branch

- **Status:** PROVED composition lemma, with two named external additive
  combinatorics inputs. The constants are symbolic; the table below only
  instantiates advertised exponent/constant classes.
- **Track:** `(Q)` / F2 quotient-prefix flatness lane. This is a finite-row
  effectivization of the high-energy half of
  `experimental/asymptotic_rs_mca.tex` proposition `prop:no-high-energy`.
- **Verifier:** `python3 experimental/scripts/verify_f2_effective_energy_dichotomy.py`

## Inputs

The note imports the following external theorems, and does not claim to prove
them here.

**Quasicube sumset bound.** In the form of
Green--Matolcsi--Ruzsa--Shakan--Zhelezov, after
Matolcsi--Ruzsa--Shakan--Zhelezov: for finite nonempty
`P,Q subset Z^d` and `U subset {0,1}^d`,

```text
|P + Q + U| >= |P|^(1/2) |Q|^(1/2) |U|.
```

Taking `P = -A`, `Q = {0}`, and `U = A` gives the Boolean difference
corollary

```text
|A - A| >= |A|^(3/2)
```

for every nonempty finite `A subset {0,1}^d`.

**BSG with printed constants.** Write `BSG(c1,e1,c2,e2)` for the statement
that if a finite set `A` in an abelian group satisfies

```text
E(A) >= |A|^3 / K,
```

then some `A' subset A` satisfies

```text
|A'| >= |A| / (c1 K^e1)
|A' - A'| <= c2 K^e2 |A'|.
```

The note keeps `(c1,e1,c2,e2)` symbolic. This is deliberately stronger and
more useful for finite rows than the asymptotic `K^C` form in the paper draft,
but it is only as good as the constants one is willing to import.

## Composition Lemma

Let `A subset {0,1}^d` be finite and nonempty. Assume the Boolean difference
corollary and `BSG(c1,e1,c2,e2)`. If

```text
E(A) >= |A|^3 / K,
```

then

```text
|A| <= c1 c2^2 K^(e1 + 2 e2).
```

Proof. BSG gives `A' subset A` with

```text
|A'| >= |A| / (c1 K^e1),
|A' - A'| <= c2 K^e2 |A'|.
```

Since `A'` is still Boolean, the quasicube corollary gives

```text
|A'|^(3/2) <= |A' - A'| <= c2 K^e2 |A'|.
```

Hence `|A'|^(1/2) <= c2 K^e2`, so `|A'| <= c2^2 K^(2 e2)`. Combining this
with the BSG lower bound on `|A'|` yields

```text
|A| <= c1 K^e1 |A'| <= c1 c2^2 K^(e1 + 2 e2).
```

Equivalently, if

```text
K < (|A| / (c1 c2^2))^(1 / (e1 + 2 e2)),
```

then `E(A) < |A|^3 / K`.

The conclusion is dimension-free: `d` does not appear.

## F2 finite-row table

At the prize-max row used in the F2 packet, `n = 2^41`, so the relevant
super-budget threshold is `|A| > n^3 = 2^123`. The composition lemma gives the
following energy deficits:

| Imported BSG row | Constants | Consequence for every `|A| > 2^123` |
| --- | --- | --- |
| idealized Schoen-type | `c1=c2=1`, `e1=1`, `e2=4` | `E(A) < |A|^3 / 2^13.666...` |
| conservative Schoen-type | `c1=c2=2^10`, `e1=1`, `e2=4` | `E(A) < |A|^3 / 2^10.333...` |
| classical-safe polynomial BSG | `c1=c2=2^10`, `e1=2`, `e2=5` | `E(A) < |A|^3 / 2^7.75` |

Thus any F2 accident family exceeding the `2^123` budget is quantitatively far
from maximal additive energy, even under the weakest printed row above.
In particular, a union-of-`c` few-structured-pieces model with
`E(A) >= |A|^3 / c^2` is incompatible with the weakest table row whenever
`c <= 2^3.875` (hence safely for `c <= 2^3.8`).

For scale: a full Boolean subcube of size `2^123` has energy `6^123`, i.e.

```text
6^123 = |A|^3 / 2^(123 log2(4/3)) ~= |A|^3 / 2^51.10,
```

so the lemma is not excluding ordinary Boolean structure. It excludes only the
extreme high-energy branch.

## What This Does And Does Not Claim

This closes the high-energy branch of the F2 quotient-prefix obstruction with
printed constants: a super-budget Boolean fiber cannot be near-maximal-energy,
and few-piece high-energy explanations are ruled out at the stated scale.

It does not close `(Q)`, `def:q-row-atom`, or any finite adjacent row by itself.
The low-energy additively-dissociated residual remains open; that is where the
Fourier-flatness, major-arc, or mode-at-null machinery still has to pay.

The same instrument should be portable to other Boolean support-family
residuals, notably split-pencil far-from-pencil fibers and any F1/B-WEAK joint
budget where the objects really are Boolean supports and the imported BSG row
is acceptable.
