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

These forty collisions have a small structural certificate. Passing to
complements `A = H \ S` and `B = H \ T`, the collisions form exactly three
dilation orbits of unordered complement pairs:

```text
orbit size 16:
  A={1,2,3,4,6,9}, B={5,8,10,11,12,13}, L_A-L_B = 3X+13
orbit size 16:
  A={1,2,4,11,14,15}, B={6,8,9,12,13,16}, L_A-L_B = 16X+5
orbit size 8:
  A={1,2,5,6,7,13}, B={4,10,11,12,15,16}, L_A-L_B = 13X
```

The last orbit has the antipodal stabilizer: multiplication by `-1` swaps the
two complements. Thus the full collision packet is `16 + 16 + 8 = 40`.

The generated-field entropy margin is already positive:

```text
4 log2(17) - log2 binom(16,10) = 3.382625... bits.
```

The Paper B list quotient-core profile is empty: `gcd(n,k)=2`, and the only
nontrivial divisor `M=2` fails the active condition `sigma < M`.

## General Complement-Prefix Lemma

Let `H <= F^*` be a multiplicative subgroup of order `n`, let
`1 <= sigma < n`, and define

```text
E_A(Z) = prod_{a in A} (1 + aZ)
       = sum_j e_j(A) Z^j.
```

For any support `S subset H` and complement `A = H \ S`,

```text
E_S(Z) E_A(Z) = prod_{h in H} (1 + hZ) = 1 - (-Z)^n.
```

Hence

```text
E_S(Z) E_A(Z) = 1 mod Z^(sigma+1).
```

Since both truncated series have constant term `1`, inversion modulo
`Z^(sigma+1)` is unique. Therefore, for equal-size supports `S,T subset H`
with complements `A=H\S` and `B=H\T`,

```text
(e_1(S),...,e_sigma(S)) = (e_1(T),...,e_sigma(T))
iff
(e_1(A),...,e_sigma(A)) = (e_1(B),...,e_sigma(B)).
```

If the complements have size `m`, then

```text
L_A(X) = X^m - e_1(A)X^(m-1) + e_2(A)X^(m-2) - ... + (-1)^m e_m(A).
```

Thus, for `sigma < m`, complement-prefix equality is equivalent to

```text
deg(L_A - L_B) <= m - sigma - 1.
```

For `sigma >= m`, it forces `A=B`.

## Exact Divisor-Gap Parametrization

The complement-locator compression gives an exact scanner target. Fix a support
`S0` in a prefix fiber, put `A0=H\S0`, and let `m=|A0|`. Then the fiber of
`S0` is in bijection with

```text
{ Q in F[X] : deg Q <= m-sigma-1 and L_A0 + Q divides X^n - 1 }.
```

The bijection sends `Q` to the support `H\A`, where
`L_A = L_A0 + Q`. Indeed, every complement locator `L_A` is a monic
degree-`m` divisor of `X^n-1`, and the complement-prefix lemma says that
same-prefix supports are exactly those with `deg(L_A-L_A0) <= m-sigma-1`.
Conversely, any monic degree-`m` divisor of `X^n-1` has its roots in `H`, so
it is the locator of a unique complement `A`.

When `sigma >= m`, the set above contains only `Q=0`; this recovers injectivity
in the very co-large range. When `sigma < m`, it reduces finite-field
collisions to a concrete low-degree divisor perturbation problem.

## Co-Large Prefix Bound

Counting the possible perturbation polynomials gives a finite-field upper bound
in the co-large support range. Let `F = F_q`, let `s = k + sigma`, and set

```text
m = n - s = n - k - sigma.
```

For every prefix target `c in F_q^sigma`,

```text
|Phi_sigma^{-1}(c)| <= q^max(m - sigma, 0)
                    = q^max(n - k - 2 sigma, 0).
```

Indeed, fix one support `S0` in the fiber and let `A0=H\S0`. For any other
support `S` in the same fiber, with complement `A=H\S`, the complement-prefix
lemma gives

```text
deg(L_A - L_A0) <= m - sigma - 1
```

when `sigma < m`, and `A=A0` when `sigma >= m`. The map
`A -> L_A-L_A0` is injective because `L_A` determines `A`, while there are
only `q^(m-sigma)` polynomials of degree at most `m-sigma-1`.

Consequently, for generated-field size `q=poly(n)`, monomial-prefix locator
fibers are polynomially bounded throughout the co-large strip
`n-k-2sigma=O(1)`, without any quotient hypothesis. This strip is much
narrower than the desired final L1 reserve at fixed rate, but it is a proved
anchor and a useful model for low-degree complement-locator scanners.

## Complement-Locator Compression

The orbit certificate is an instance of this lemma. Here `H=F_17^*`,
`n=16`, `m=6`, `sigma=4`, and the co-large bound is `17^(6-4)=289`.
Since

```text
prod_{h in F_17^*} (1 + hZ) = 1 - Z^16,
```

the support elementary series and complement elementary series are inverse to
each other modulo `Z^5`. Therefore two `10`-supports have the same
`Phi_4` value if and only if their `6`-point complements have the same first
four elementary symmetric coefficients.

For complements of size `6`,

```text
L_A(X) = X^6 - e_1(A)X^5 + e_2(A)X^4 - ... + e_6(A).
```

Equal first four elementary coefficients are equivalent to

```text
L_A(X) - L_B(X) = alpha X + beta.
```

In this toy case, every aperiodic prefix collision is exactly one of the three
linear locator-gap orbits listed above. This turns the finite counterexample to
aperiodic injectivity into a small divisor-pair problem inside `X^16 - 1`.

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
checks that all forty nonsingleton fibers are not `M=8` or `M=16`
coset-union collisions, verifies that support-prefix and complement-prefix
partitions agree for all supports, checks the exact divisor-gap
parametrization and the co-large upper bound, and certifies the three
complement-locator dilation orbits.
