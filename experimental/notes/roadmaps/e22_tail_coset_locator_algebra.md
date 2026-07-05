# E22 Tail-Coset Locator Algebra

- **DAG node:** `e22_tail_coset_locator_algebra`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_tail_coset_locator_algebra/`
- **Verifier:** `python3 experimental/scripts/verify_e22_tail_coset_locator_algebra.py`

## Statement

Let `D` be a multiplicative subgroup domain of size `n`.  If `M | n`, `B`
is a tail with `|B| < M`, and `H` is a set of quotient fibers of

```text
x -> x^M,
```

then the locator of `B` together with the full fibers over `H` has the form

```text
L_B(X) G(X^M).
```

If `M > t`, the top `t` subleading coefficients of this locator depend only
on `B` and the number of selected fibers, not on which quotient fibers are
selected.

## Proof

For a selected quotient value `z`, the corresponding full fiber is the set of
roots in `D` satisfying

```text
X^M - z = 0.
```

Let `B` be a disjoint tail with `|B| = b < M`, and let
`H = {z_1, ..., z_h}` be the selected quotient values.  The locator of the
union of `B` with those full fibers is

```text
L_B(X) prod_{z in H} (X^M - z).
```

Writing

```text
G(Y) = prod_{z in H} (Y - z)
```

gives `L_B(X)G(X^M)`.

For the top-coefficient statement, write `G` as a monic polynomial of degree
`h`:

```text
G(X^M) = X^{hM} + g_1 X^{(h-1)M} + ...
```

Since `deg L_B = b < M`, the leading block of `L_B(X)G(X^M)` is

```text
X^{hM} L_B(X).
```

Every term involving `g_1, g_2, ...` has degree at most

```text
(h-1)M + b = hM + b - M.
```

Thus there is an `M`-coefficient gap below the leading block.  If `M > t`,
none of the lower quotient terms can affect the top `t` subleading
coefficients.  Those coefficients are the corresponding coefficients of
`L_B`, shifted by `X^{hM}`, and depend only on `B` and on `h`, not on the
selected quotient values.

## Role In The Program

This supplies the formal locator algebra behind the E22 quotient-coset
staircase.  It is a small but useful `(Q)` input: once a challenger support is
shown to be a tail plus full quotient fibers, the locator shape and leading
coefficient invariance are immediate and do not require a numerical scan.

