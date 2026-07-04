# X30: finite-p norm gate for dyadic terminal trades

- **DAG node:** `x30_finite_p_norm_gate`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved reduction.
- **Verifier:** `experimental/scripts/verify_x30_finite_p_norm_gate.py`.
- **Certificate:**
  `experimental/data/certificates/x30-finite-p-norm-gate/x30_finite_p_norm_gate.json`.

## Statement

Let `n=2^s`, let `H=mu_n` in a field of odd characteristic `p`, and let
`zeta` be a primitive `n`-th root.  For two disjoint equal-size supports
`P,Q subset H`, write the signed first-sum word

```text
f(X) = sum_{zeta^i in P} X^i - sum_{zeta^j in Q} X^j   in Z[X],
deg f < n.
```

If the finite-field first-sum equality holds,

```text
f(zeta) = 0 in F_p,
```

then exactly one of the following occurs:

1. **Dyadic descent:** `Phi_n | f` over `Z`.  Since
   `Phi_n(X)=X^(n/2)+1`, this is equivalent to

   ```text
   coeff_i(f) = coeff_{i+n/2}(f),        0 <= i < n/2.
   ```

   Because the coefficients are in `{-1,0,1}`, both `P` and `Q` are unions of
   antipodal pairs.  The trade descends through `x -> x^2`.

2. **Norm gate:** `Phi_n` does not divide `f` over `Z`.  Then `p` divides the
   sparse cyclotomic norm

   ```text
   N_n(f) = Res(Phi_n, f) = product_{Phi_n(alpha)=0} f(alpha).
   ```

Iterating this at every dyadic descent level gives the recursive terminal
dichotomy:

```text
finite-p trade = characteristic-zero dyadic trade
              or a p-specific sparse norm reduction at the first failed level.
```

## Proof

The coefficient criterion is immediate because `n=2m` and

```text
Phi_n(X) = X^m + 1.
```

For a polynomial of degree `<2m`,

```text
f(X) = sum_{i=0}^{m-1} a_i X^i + sum_{i=0}^{m-1} b_i X^{i+m},
```

divisibility by `X^m+1` is equivalent to `a_i=b_i` for every `i`.

Since the supports are disjoint, each coefficient of `f` is `-1`, `0`, or
`1`.  The equality `a_i=b_i` therefore says that a positive coefficient at
`i` occurs exactly with a positive coefficient at `i+m`, and similarly for
negative coefficients.  Thus both supports are antipodal unions.

If `Phi_n` does not divide `f`, then `f` and `Phi_n` are coprime in `Z[X]`.
Their resultant is a nonzero integer.  Reducing modulo `p`, the chosen
primitive root `zeta` is a common zero of the reductions of `Phi_n` and `f`.
Therefore the reductions have a common factor over `F_p`, so

```text
Res(Phi_n,f) = 0 mod p.
```

Equivalently, `p | N_n(f)`.

This proves the one-step dichotomy.  If the first branch holds, the locator
identity

```text
L_{pi^{-1}(A)}(X) = L_A(X^2)
```

descends the remaining top-coefficient equalities to the quotient support.
The same argument can then be applied at `n/2`.

## Consequences

For odd `h`, the descent branch is impossible at the first step, because an
antipodal union has even size.  Thus every finite-p odd-h terminal trade is a
first-level sparse norm reduction.  This is the exact formal meaning of the
X24/X25 h=5 picture:

```text
h=5 characteristic-zero trade: impossible
h=5 finite trade: must be p-specific norm-gate residue
```

For h=4, the first descent branch is possible.  The observed extra finite-p
mass descends once to h=2 quotient sum collisions.  X29 then identifies that
quotient branch exactly.  The nonzero extra quotient rows in X26-X28 are
therefore norm-gate primes at the quotient level, not new h=4 structure.

## Checked Examples

The verifier checks representative norm-gate examples from the h=4 quotient
ledger:

```text
quotient m   p        positive exponents   negative exponents
----------------------------------------------------------------
32           4993     [0, 2]               [8, 21]
64           65537    [0, 3]               [16, 54]
128          65537    [0, 1]               [22, 39]
```

In each row the signed quotient word vanishes at the chosen primitive root
modulo `p`, but is not divisible by `Phi_m` over `Z`.

The verifier also checks that zero-sum quotient words are in the descent branch
and that odd support sizes cannot be antipodal unions.

## What Remains

X30 does not bound the number of norm-gate primes or norm-gate sparse words.
It reduces the remaining finite-p terminal problem to that explicit arithmetic
object:

```text
count sparse words whose cyclotomic norm is divisible by the row prime.
```

This is the p-specific certification problem isolated in the terminal node.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x30_finite_p_norm_gate.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x30_finite_p_norm_gate.py --write-certificate
```

Current replay: **25 PASS, 0 FAIL**.
