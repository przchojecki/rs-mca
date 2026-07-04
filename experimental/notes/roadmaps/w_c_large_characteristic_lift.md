# W-C: large-characteristic lift and dyadic descent

- **DAG node:** `u2_large_characteristic_lift`.
- **Task:** W-C.
- **Status:** PROVED.
- **Provenance:** X-6 characteristic-zero residue, packaged for upstream.
- **Verifier:** `experimental/scripts/verify_w_c_large_characteristic_lift.py`.
- **Certificate:**
  `experimental/data/certificates/w-c-large-characteristic-lift/w_c_large_characteristic_lift.json`.

## Critical-path role

This is a proof-spine packet for the conditional prize route's U2/moment
residue.  It proves that, above an explicit norm threshold, finite-field
`t`-null blocks are not primitive: they lift to characteristic zero and descend
to dyadic coset unions.  Those coset unions are paid quotient structure rather
than a new post-strip residue.

The official rows still need their own small-characteristic certifier or
resultant exclusion.  This packet supplies the structural large-characteristic
branch and keeps the remaining U2 work localized to the stated finite-row
certifier problem.

## Statement

Let `n=2^s`, let `H=mu_n`, and let `B` be a `b`-subset of `H` over a field
of characteristic `p`.  Fix `t<n`, and set

```text
M = 2^ceil(log2(t+1)).
```

If

```text
p > max_{1 <= r <= min(t,b)} binom(b,r)^phi(n)
```

and

```text
e_1(B) = e_2(B) = ... = e_t(B) = 0,
```

then `B` is a union of full `mu_M`-cosets in `mu_n`.  In particular, if
`M` does not divide `b`, no such `b`-subset exists.

The conclusion is uniform in `b`, but the displayed norm threshold is very
large.  This packet is not the later small-prime or per-row U2 certifier.

## Proof

Choose a primitive complex `n`th root of unity `zeta`, and lift the exponent
set of `B` to the algebraic integer ring `Z[zeta]`.  For each `r`, the
elementary sum `e_r(B)` is a sum of `binom(b,r)` roots of unity.  Every Galois
conjugate therefore has complex absolute value at most `binom(b,r)`, so if
the lifted algebraic integer is nonzero, its norm has absolute value at most

```text
binom(b,r)^phi(n).
```

If the finite-field value of `e_r(B)` is zero, then the lifted algebraic
integer is divisible by a prime of `Z[zeta]` above `p`; hence `p` divides its
norm.  Under the displayed strict bound this is impossible unless the lifted
`e_r(B)` is already zero in characteristic zero.  Thus the finite vanishing
through level `t` lifts to characteristic zero.

Now work in characteristic zero.  The first vanishing relation says

```text
sum_{zeta^i in B} zeta^i = 0.
```

Equivalently, the `0/1` exponent polynomial

```text
P_B(X) = sum_{zeta^i in B} X^i,       deg P_B < n,
```

vanishes at `zeta`.  Since `n` is a power of two,

```text
Phi_n(X) = X^(n/2) + 1.
```

Therefore `Phi_n` divides `P_B`, and the reduced coefficients satisfy

```text
coeff_i(P_B) = coeff_{i+n/2}(P_B),       0 <= i < n/2.
```

So `B` is antipodally closed.

Write `B = pi^{-1}(B_1)` under `pi(x)=x^2`.  Its locator has the form

```text
L_B(X) = L_{B_1}(X^2).
```

Consequently odd elementary coefficients of `B` vanish automatically, and
`e_{2r}(B)=0` is equivalent to `e_r(B_1)=0` up to a harmless sign.  Thus
vanishing through level `t` descends to vanishing through level `floor(t/2)`
on `mu_{n/2}`.

Repeat.  After `a=ceil(log2(t+1))` descents, the original set is a union of
full fibers of

```text
x -> x^M,       M=2^a>t.
```

These fibers are exactly the `mu_M`-cosets in `mu_n`.  The divisibility
condition on `b` follows because every such coset has size `M`.

## Verification

The verifier checks the norm-threshold arithmetic, exhaustively replays the
characteristic-zero dyadic descent on small `2`-power domains, and runs finite
field lifts above the norm threshold on toy rows:

```bash
python3 experimental/scripts/verify_w_c_large_characteristic_lift.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_w_c_large_characteristic_lift.py --write-certificate
```
