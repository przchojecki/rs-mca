# X82: square-shift row and certifier keys

- **DAG node:** `x82_square_shift_certifier_keys`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved key-discipline packet.
- **Verifier:** `experimental/scripts/verify_x82_square_shift_certifier_keys.py`.
- **Certificate:**
  `experimental/data/certificates/x82-square-shift-certifier-keys/x82_square_shift_certifier_keys.json`.

## Statement

Let `R subset mu_n` be a split `2h`-support in the square-shift normal form
of X81:

```text
L_R(X) + lambda = S(X)^2.
```

There are two useful key operations, but they have different meanings.

1. **Domain scaling is a finite-row symmetry.**  For `gamma in mu_n`,

```text
gamma R = {gamma r : r in R}
```

has

```text
L_{gamma R}(X) + gamma^(2h) lambda
  = (gamma^h S(X/gamma))^2.
```

In particular, the nonzero-square condition on `lambda` is preserved.

2. **Galois/unit exponent relabeling is certifier compression.**  For
`u in (Z/nZ)^*`, the map

```text
zeta^a -> zeta^(ua)
```

applies the cyclotomic automorphism `sigma_u` to the coefficients:

```text
L_{uR} = sigma_u(L_R),     S_{uR}=sigma_u(S),     lambda_{uR}=sigma_u(lambda).
```

Thus the algebraic square-shift identity over the cyclotomic field and the
set of rational primes dividing any cleared obstruction norm are constant on
unit relabeling keys.

## Warning

Scaling by `gamma in mu_n` is a genuine finite-row symmetry.  Unit exponent
maps are not generally fixed-generator row-count symmetries.  They may change
whether `L_R+lambda` has a nonzero-square shift in a fixed finite row with a
chosen generator.  As in X67, use unit keys to reduce resultant or obstruction
computations, not to divide row mass.

## Proof

For scaling, write

```text
L_{gamma R}(X) = prod_{r in R}(X-gamma r)
               = gamma^(2h) L_R(X/gamma).
```

Substituting the X81 identity gives

```text
L_{gamma R}(X) + gamma^(2h)lambda
  = gamma^(2h)(L_R(X/gamma)+lambda)
  = gamma^(2h) S(X/gamma)^2
  = (gamma^h S(X/gamma))^2.
```

Since `gamma^(2h) = (gamma^h)^2`, nonzero-square shifts remain nonzero
squares.

For unit maps, let `sigma_u(zeta)=zeta^u`.  Applying `sigma_u` coefficientwise
to

```text
L_R + lambda = S^2
```

gives

```text
sigma_u(L_R) + sigma_u(lambda) = sigma_u(S)^2.
```

But `sigma_u(L_R)=L_{uR}` because it sends every root `zeta^a` of `R` to
`zeta^(ua)`.  Squares remain squares under field automorphisms, and
cyclotomic norms are invariant under such automorphisms.  Therefore any
cleared obstruction norm has the same rational prime divisors on the unit
orbit.

This does **not** say that the finite-row predicate is unit-invariant for a
fixed embedding `mu_n subset F_q^*`.  In a prime row with `p == 1 mod n`,
Frobenius fixes the chosen `n`-th roots; an arbitrary unit relabeling is not a
finite-field automorphism of that row.

## Consequence

After X81, a minimal-trade certifier can operate in square-shift support
currency.  X82 fixes two keys:

```text
row_key(R)       = min_{gamma in mu_n} gamma R,
certifier_key(R) = min_{u in (Z/nZ)^*, gamma in mu_n} u(gamma R).
```

The row key is safe for row-orbit bookkeeping.  The certifier key is safe for
computing one obstruction/resultant per Galois key, after which any survivor
must be expanded back into row-count currency.  This generalizes the h=4
X66-X68 discipline to the square-shift support formulation and preserves its
central warning.

## Replay

The verifier checks the scaling formula on an algebraic sample, then
exhaustively verifies finite-row scaling invariance and certifier-key
stability on:

```text
F17 / mu16, h=3,4,5
F97 / mu16, h=3,4,5
```

It also records sample unit relabelings that change the fixed-row
square-shift predicate.  Those samples are intentional: they verify that X82
is not being used as a false row-count divisor.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x82_square_shift_certifier_keys.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x82_square_shift_certifier_keys.py --write-certificate
```
