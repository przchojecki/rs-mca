# F17^32 M3 Null-Polynomial Split-Locator Gate

Status: PROVED / AUDIT.

This packet records the finite-root gate needed after an M3 regular root table
has been computed.

For a finite slope `z`, put

```text
s_m(z) = u_m + z v_m.
```

Then

```text
rank H_{t,j}(s(z)) <= j
```

is equivalent to the existence of a nonzero null-polynomial

```text
L(X)=ell_0 + ... + ell_j X^j
```

with

```text
sum_{b=0}^j s_{a+b}(z) ell_b = 0,   0 <= a < t.
```

This is only the ambient Hankel root condition.  It becomes an actual
exact-`A` split locator for the pinned order-512 subgroup `H` only after the
polynomial is normalized to a monic degree-`j` divisor of `X^512-1`.  Since
`512 = 2 mod 17`, `X^512-1` is squarefree over the pinned field, and its roots
are exactly the descriptor subgroup `H`.

The finite support-wise noncontainment gate is then

```text
H_{t,j}(v) ell != 0.
```

Thus future root-table packets can safely start from ambient regular roots and
then filter them by the domain-locator and noncontainment gates.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --write experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json

python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json
```
