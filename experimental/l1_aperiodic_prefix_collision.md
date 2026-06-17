# L1 Aperiodic Prefix-Collision Certificate

Status: PROVED finite certificate; COUNTEREXAMPLE to a proof route.

This note isolates a small monomial-prefix locator-fiber computation for the L1
program in `agents.md`. It does not refute the prefix local-limit conjecture.
It refutes the stronger route that quotient-core removal should make
finite-field monomial-prefix collisions disappear.

## Finite Theorem

Work over `F_17` with

```text
H = F_17^*, n = 16, k = 6, sigma = 4, a = k + sigma = 10.
```

Let

```text
Phi_4(S) = (e_1(S), e_2(S), e_3(S), e_4(S)),
```

for `10`-subsets `S` of `H`, with elementary symmetric functions computed in
`F_17`. Then the complete fiber distribution of `Phi_4` is:

```text
total supports          = binom(16,10) = 8008
distinct prefix values  = 7968
singleton fibers        = 7928
two-point fibers        = 40
maximum fiber size      = 2
```

Every nonsingleton fiber is quotient-separated from the only subgroup orders
that could be charged as `M > sigma` quotient-periodic exceptions, namely
`M = 8` and `M = 16`: if `S != T` lie in the same fiber, then
`S symmetric-diff T` has size `12` and is not a union of cosets of either
subgroup.

The generated-field entropy margin is already positive:

```text
4 log2(17) - log2 binom(16,10) = 3.382625... bits.
```

The Paper B list quotient-core profile is empty: `gcd(n,k)=2`, and the only
nontrivial divisor `M=2` fails the active condition `sigma < M`.

## Example Collision

One of the forty two-point fibers is

```text
c = (8, 12, 13, 7),
S = {1,2,3,4,5,6,7,9,10,12},
T = {1,2,3,8,10,11,13,14,15,16}.
```

Both sets have

```text
Phi_4(S) = Phi_4(T) = (8,12,13,7).
```

For the monomial-prefix word

```text
U_c(X) = X^10 - 8 X^9 + 12 X^8 - 13 X^7 + 7 X^6
        = X^10 + 9 X^9 + 12 X^8 + 4 X^7 + 7 X^6 in F_17[X],
```

the polynomials

```text
P_S = U_c - L_S,  P_T = U_c - L_T,
L_A = product_{x in A} (X - x),
```

have degree `< k = 6`. Thus both are Reed-Solomon codewords agreeing with
`U_c` on their respective `10`-point supports, exactly as in
`tex/slackMCA_v3.tex` `prop:monomial-fiber`.

## Route Cut

This is a useful obstruction, not a large-list counterexample. At this toy
point the maximum prefix fiber has size only `2`, so the polynomial local-limit
shape survives. What fails is a no-collision proof strategy:

```text
entropy clears + quotient cores absent => aperiodic prefix map is injective.
```

The surviving L1 target must allow isolated finite-field aperiodic collisions
and prove a multiplicity bound for them.

## Reproduction

```bash
python3 experimental/verify_l1_aperiodic_prefix_collision.py
python3 experimental/verify_l1_aperiodic_prefix_collision.py --format json
```

The verifier enumerates all `8008` supports, recomputes the fiber histogram,
checks the example codewords, verifies the entropy and quotient-core ledgers,
and checks that all forty nonsingleton fibers are not `M=8` or `M=16`
coset-union collisions.
