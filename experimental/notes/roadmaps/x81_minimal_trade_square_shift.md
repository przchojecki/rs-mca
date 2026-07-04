# X81: minimal-trade square-shift normal form

- **DAG node:** `x81_minimal_trade_square_shift`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved uniform normal form.
- **Verifier:** `experimental/scripts/verify_x81_minimal_trade_square_shift.py`.
- **Certificate:**
  `experimental/data/certificates/x81-minimal-trade-square-shift/x81_minimal_trade_square_shift.json`.

## Statement

Let `F` be a field of odd characteristic.  For any `h >= 1`, unordered
disjoint h-trades

```text
P cap Q = empty,      |P|=|Q|=h,
L_P and L_Q have the same top h-1 coefficients
```

are in bijection with split `2h`-supports `R=P union Q` whose locator admits
a square shift

```text
L_R(X) + lambda = S(X)^2
```

where `S` is monic of degree `h` and `lambda` is a nonzero square in `F`.
The split is unique up to swapping `P` and `Q`.

Equivalently, minimal PTE trade counting can be performed in support currency:

```text
unordered h-trades
  = split 2h-supports with a nonzero-square shift.
```

For ordered pairs, multiply by `2`.

## Proof

The locator polynomials have the form

```text
L_P(X) = X^h + a_{h-1} X^{h-1} + ... + a_1 X + a_0,
L_Q(X) = X^h + a_{h-1} X^{h-1} + ... + a_1 X + b_0.
```

Thus

```text
L_Q = L_P + delta,        delta=b_0-a_0.
```

Since `P` and `Q` are disjoint, `delta != 0`.  Set

```text
S = (L_P+L_Q)/2.
```

Then

```text
L_R = L_P L_Q
    = (S-delta/2)(S+delta/2)
    = S^2 - delta^2/4.
```

So `L_R + delta^2/4 = S^2`, with nonzero square shift.

Conversely, suppose `R` is a split `2h`-support and

```text
L_R + lambda = S^2,       lambda=a^2,       a != 0.
```

Then

```text
L_R = (S-a)(S+a).
```

The two factors are monic of degree `h` and differ only in their constant
term.  They are coprime because `a != 0`, and their product is the squarefree
locator of `R`; hence each factor is the locator of one h-subset of `R`.
Those two h-subsets form a minimal trade.

Uniqueness is the same argument as in X78.  If

```text
L_R + lambda = S^2,       L_R + mu = T^2
```

with monic degree-`h` polynomials `S,T`, then

```text
(S-T)(S+T) = lambda-mu.
```

Since `S+T` is nonconstant, the left side can be constant only if `S=T`, and
then `lambda=mu`.  Thus the split is unique up to interchanging the two
factors.

## Relation to Existing Nodes

The star-PTE lemma proves that every same-top family decomposes into canonical
minimal PTE trades.  X81 records the support-level normal form for each such
minimal trade.  X78 is the h=5 specialization; X79 then uses the h=5 forced
square-root coefficients to build four low obstruction gates.

The terminal value is that all minimal-trade residues, not only h=5, can be
fed to a square-shift support certifier before any row-count expansion.

## Replay

The verifier checks the algebra directly for `h=3..7`, then compares
independent finite-row counts:

```text
same-top h-subset pairs
    versus
split 2h-supports with nonzero-square shift
```

on:

```text
F17 / mu16, h=3,4,5
F97 / mu16, h=3,4,5,6
```

All rows agree exactly.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x81_minimal_trade_square_shift.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x81_minimal_trade_square_shift.py --write-certificate
```
