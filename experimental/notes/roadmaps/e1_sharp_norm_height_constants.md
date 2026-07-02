# E1 Sharp Norm-Height Constants

- **Status:** PROVED / arithmetic compiler.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** `are_sharp_constant`.
- **Verifier:** `experimental/scripts/verify_e1_sharp_norm_height_constants.py`.
- **Artifact:** `experimental/data/certificates/row-c-e1-sampling/e1_sharp_norm_height_constants.json`.

This note sharpens the height constant in the split-prime transfer gate used by
the quotient `e_1` value-set lane.  It also records exactly where the pure
height argument stops for deployed bit budgets.

## Statement

Let `N'` be a quotient order, let `zeta` be a primitive `N'`-th root of unity,
and let `ell'` be the quotient agreement parameter.  In the antipodal
quotient-core normal form, a difference of two characteristic-zero `e_1`
values is an algebraic integer

```text
Delta in Z[zeta]
```

whose coefficient `l_1` height is at most `2 ell'`.  Therefore every conjugate
of `Delta` has complex absolute value at most `2 ell'`, and

```text
|Norm_{Q(zeta)/Q}(Delta)| <= (2 ell')^phi(N').
```

Consequently, if a split prime `p == 1 mod N'` satisfies

```text
p > (2 ell')^phi(N'),
```

then no nonzero characteristic-zero `e_1` difference can vanish modulo the
chosen embedding into `F_p`.

The true exponent shape is therefore

```text
phi(N') log(2 ell'),
```

and in the dyadic case this is

```text
(N'/2) log(2 ell').
```

This replaces any coarser `n log n / sigma` bookkeeping for this local
transfer gate.

## Frontier Consequence

For each official rate and bit budget, the verifier computes two frontiers:

- all even quotient orders with integral `ell' = rho N' + 1`;
- dyadic quotient orders.

At bit budget `256`, the contiguous all-even-prefix height frontiers are:

```text
rho = 1/2:   N' <= 84,   first failure N'=86
rho = 1/4:   N' <= 100,  first failure N'=104
rho = 1/8:   N' <= 120,  first failure N'=128
rho = 1/16:  N' <= 112,  first failure N'=128
```

This prefix statement is deliberately not phrased as "largest certified even
order": `phi(N')` is nonmonotone, so sporadic larger composite orders can pass
after an earlier failure.  The verifier records the prefix frontier because it
is the safe monotone transfer claim.

For the Row-C compatible dyadic orders at rate `1/2`, the pure height gate
certifies `N'=64` but not `N'=128` or `N'=256`.  This is the intended scoping
negative: height-only transfer resolves the first quotient cell, while the
larger cells need additional structure or direct norm-divisibility control.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_e1_sharp_norm_height_constants.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_e1_sharp_norm_height_constants.py \
  --check experimental/data/certificates/row-c-e1-sampling/e1_sharp_norm_height_constants.json
```

The computation is exact integer arithmetic.
