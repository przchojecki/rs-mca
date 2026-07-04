# X83: uniform square-shift obstruction gate

- **DAG node:** `x83_uniform_square_shift_obstruction_gate`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved uniform obstruction-gate packet.
- **Verifier:** `experimental/scripts/verify_x83_uniform_square_shift_obstruction_gate.py`.
- **Certificate:**
  `experimental/data/certificates/x83-uniform-square-shift-obstruction-gate/x83_uniform_square_shift_obstruction_gate.json`.

## Statement

Let `F` have odd characteristic and let

```text
C(X) = X^(2h) + c_(2h-1)X^(2h-1) + ... + c_0
```

be the locator of a split `2h`-support `R`.  There is a unique monic
degree-`h` polynomial

```text
S_R(X) = X^h + s_(h-1)X^(h-1) + ... + s_0
```

whose square agrees with `C` in degrees `2h,2h-1,...,h`.  Define

```text
E_R(X) = S_R(X)^2 - C(X).
```

Then `deg E_R <= h-1`, and `R` underlies a minimal h-trade exactly when

```text
[X^i]E_R = 0       for 1 <= i <= h-1
```

and the constant discrepancy

```text
lambda_R = [X^0]E_R
```

is a nonzero square in the row field.  This is the uniform version of X79's
four h=5 obstruction equations.

For `H=mu_n`, `n=2^s`, over `K=Q(zeta_n)`, the forced-root recursion has
controlled powers of two in its denominators:

```text
s_(h-q) in 2^(-(2q-1)) O_K,       1 <= q <= h.
```

Consequently `2^(4h-2)[X^i]E_R` is a cyclotomic integer for every
`1 <= i <= h-1`.

If `h` is not a power of two, X24 forbids characteristic-zero dyadic trades.
Therefore every finite-row h-trade in this square-shift support currency is
p-specific: after clearing by `2^(4h-2)`, the row prime `p` divides the
cyclotomic norm of at least one nonzero low obstruction, and in fact of every
nonzero cleared low obstruction.

## Proof

The forced root is obtained recursively from the high coefficients.  Matching
the coefficient of `X^(2h-1)` gives

```text
2s_(h-1) = c_(2h-1).
```

Assume `s_(h-1),...,s_(j+1)` have already been determined.  The coefficient
of `X^(h+j)` in `S_R^2` contains the new unknown `s_j` linearly as `2s_j`,
plus terms involving only the already determined higher coefficients.  Since
`2` is invertible, this determines `s_j` uniquely.  Thus `S_R` is forced by
the coefficients in degrees `2h` down to `h`.

Once `S_R` is fixed, the identity

```text
C + lambda = S_R^2
```

can only use `lambda=[X^0]E_R`.  It holds precisely when every nonconstant
coefficient of `E_R` vanishes, i.e. when the `h-1` displayed obstruction
equations hold.  If additionally `lambda` is a nonzero square, X81 factors

```text
C = (S_R-a)(S_R+a),       a^2=lambda,
```

and the two factors give the unique unordered h-trade split.  Conversely,
every minimal h-trade has locators differing by a nonzero constant and hence
gives exactly this square-shift identity.

For denominators, let `e_q` be a safe exponent for the q-th forced coefficient
below the leading term:

```text
s_(h-q) in 2^(-e_q) O_K.
```

The first equation gives `e_1=1`.  At the q-th step, every product term has
index split `a+b=q`, hence denominator exponent at most

```text
(2a-1)+(2b-1)=2q-2
```

by induction; the final division by `2` gives `e_q=2q-1`.  Therefore all
coefficients of `S_R` lie in `2^(-(2h-1))O_K`, so every coefficient of
`S_R^2` lies in `2^(-(4h-2))O_K`.  Since `C` is integral,
`2^(4h-2)E_R` has cyclotomic-integer coefficients.

Now suppose `h` is not a power of two and a row prime realizes an h-trade.
All low obstructions vanish modulo the prime of `O_K` selected by the row.
If all low obstructions vanished already over `K`, then over `C` the nonzero
constant `lambda_R` would have a square root and X81 would give a
characteristic-zero dyadic h-trade, contradicting X24.  Thus at least one low
obstruction is nonzero over `K`; every nonzero cleared obstruction that
vanishes modulo the row prime has norm divisible by `p`.  This proves the
p-specific norm-gate claim.

For power-of-two `h`, the last paragraph is deliberately not asserted:
X24 allows the paid full-fiber characteristic-zero branch.

## Consequence

The terminal minimal-trade residue can now be pushed into a uniform certifier
shape:

```text
split 2h-support R
  -> forced high-coefficient square root S_R
  -> h-1 low obstruction coefficients
  -> nonzero-square constant test
  -> row key / certifier key discipline from X82.
```

At `h=5`, this recovers X79 with clearing exponent `4h-2=18`.  For every
non-power-of-two `h`, it also upgrades the qualitative X24 statement into a
finite-row sparse norm-gate certificate target.

## Replay

The verifier checks:

- the denominator recurrence through `h=12`;
- constructed minimal trades and low-coefficient perturbations for `h=3..8`;
- exhaustive finite-row agreement between actual same-top h-trades and
  square-lambda obstruction supports on:

```text
F17 / mu16, h=3,4,5,6,7
F97 / mu16, h=3,4,5,6
```

## Verification

Run:

```bash
python3 experimental/scripts/verify_x83_uniform_square_shift_obstruction_gate.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x83_uniform_square_shift_obstruction_gate.py --write-certificate
```
