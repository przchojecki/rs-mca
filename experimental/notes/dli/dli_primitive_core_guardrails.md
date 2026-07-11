# DLI Primitive-Core Guardrails

## Status

PROVED guardrails plus an open frontier interface. This note vendors a
primitive-core packet from the smooth-RS prize DAG into upstream DLI terminology.
It does not close the DLI large-block estimate.

Source nodes in the prize DAG:

- `b2b_dyadic_descent_packet` (PROVED)
- `b2b_near_tail_bound` (PROVED)
- `skew_support_threshold` (PROVED)
- `bounded_coeff_norm_gate` (PROVED)
- `dli_prime_weighted_large_block_support` (TARGET, used here only to identify
  the remaining frontier)

The accompanying replay script is
`experimental/scripts/verify_dli_primitive_core_guardrails.py`.

## Dyadic Descent Packet

Let `n=2^s`, let `mu_n` be the evaluation subgroup, and let
`p_r(A)=sum_{x in A} x^r`. For a subset `A subset mu_n`, the map
`x -> x^{2^j}` gives a bounded-multiplicity multiset `m_j` on
`mu_{n/2^j}` with

```text
0 <= m_j(y) <= 2^j,
p_s(m_j) = p_{2^j s}(A).
```

Thus a `t`-null set descends to a `floor(t/2^j)`-null bounded-multiplicity
multiset at level `j`.

At level `j=1`, fixing the square-root section
`sigma(zeta_{n/2}^i)=zeta_n^i`, the odd equations are retained exactly by the
skew

```text
d(i) = 1_A(zeta_n^i) - 1_A(zeta_n^{i+n/2}),
p_{2s+1}(A) = sum_i d(i) sigma(i)^{2s+1}.
```

This is the formalization-ready split: even equations descend through
`m_1`, while odd equations are precisely a skew-nullity system. No odd
constraint is discarded.

The boundary-scale repair is also part of the packet. At official
`t=2^33+1`, the boundary subgroup scale is

```text
M_0 = 2^{floor(log_2 t)} = 2^33,
```

not `M=t`. The boundary class consists of `mu_{M_0}`-coset unions with the
corresponding quotient `p_1` condition, after stripping the antipodally
invariant patterns already covered by the larger-scale dictionary.

## Near-Tail Bound

For layers just above the nullity threshold, degree-`k-1` interpolation gives

```text
N_{t+k} <= binom(n,k) / binom(t+k,k).
```

At the official scale `n=2^41`, `t=2^33+1`, and `1 <= k <= 15`, this is
strictly below `2^{8k}`. Therefore both near tails

```text
min(|A|, n-|A|) in [t+1, t+15]
```

together contribute less than `2^122`. This removes the first fifteen
layers above `t` unconditionally; the primitive core starts at `t+16`.

## Skew Support Threshold

For a level with `L` odd equations, a nonzero skew supported on at most `L`
section points is impossible. After dividing each column by its nonzero
section point, the constraint matrix is an ordinary Vandermonde matrix in the
distinct squared section points. Every support of size `<= L` therefore has
full column rank.

Consequently every nonzero level-`j` tower skew at prize scale has support at
least

```text
L_j + 1 = 2^{32-j} + 1
```

in the corresponding section. Small-support skew mass is profile-only:
the only skew in that regime is zero, so the branch factor is `{0,1}` by
parity.

## Bounded-Coefficient Norm Gate

Let `omega` have 2-power order `M` in `F_p`, and let

```text
P_c(X) = sum_a c_a X^a,       |c_a| <= C.
```

Fold exponents modulo the relation `X^{M/2}=-1` to obtain the reduced
polynomial `Q_c` of degree `< M/2`. If `P_c(omega)=0`, then either:

- the cyclotomic/coset case holds in characteristic zero, namely the folded
  coefficients vanish identically; or
- `p` divides the integer resultant

```text
Res(X^{M/2}+1, Q_c).
```

For the tower half-sections used by the primitive-core packet, no opposite
pairs occur inside the section. The cyclotomic/coset escape therefore forces
the skew to be zero. Every nonzero bounded-coefficient tower skew is
resultant-gated at every imposed odd harmonic:

```text
p | gcd_r Res(X^N+1, Q_{d,r}).
```

This is a structural guardrail. It does not by itself bound the number of
large-support skews whose folded resultants share the fixed row prime.

## D3 Weighted Identity

For a central level profile with local domains `D_y`, let

```text
A_{ell,y} = x_y^{2ell-1},
Z = {d in prod_y D_y : A d = 0},
U = prod_y |D_y|.
```

Additive-character orthogonality gives the exact identity

```text
rho = q^L |Z| / U
    = sum_{lambda in F_q^L} prod_y
        (1/|D_y|) sum_{u in D_y} psi(u <lambda,A_y>).
```

In the signed or ternary central families, this is equivalently the
nonnegative cosine display used by the DLI near-peak-mass ledger. The
`lambda=0` term is the balanced mean; all excess mass must be controlled in
the weighted aggregate, not by a profilewise supremum.

## Remaining Frontier

The proved packet reduces the primitive-core residue to a large-support,
bounded-coefficient, fixed-prime counting problem:

```text
count/weight the nonzero tower skews of support >= L_j+1
whose full folded-resultant packet is divisible by the row prime p.
```

The prize DAG records several false stronger routes:

- pointwise/sup DLI flatness is false on low-mass profiles;
- uniform per-frequency near-peak bounds are false;
- per-level constant `W <= 3` bounds are false at engineered rows;
- naive independent-orbit models are false because ideal-lattice clusters
  create correlated short ternary points.

The surviving interface is a weighted aggregate/lattice-frame bound. In the
notation of the current DLI frontier, one tracks the weighted low-weight
ternary points in the ideal lattice

```text
I_p = {c in Z[z]/(z^N+1) : c(omega) = 0 mod p}
```

and the residual analytic bulk. The guardrails above are the proved inputs
that any such aggregate proof should consume.

## Replay

Run:

```bash
python3 experimental/scripts/verify_dli_primitive_core_guardrails.py
```

The replay checks:

- complement duality in `mu_n`;
- the dyadic pushforward and odd-skew identities;
- exact near-tail arithmetic for `n=2^41`, `t=2^33+1`, `1 <= k <= 15`;
- the Vandermonde full-rank threshold at a toy 2-power row;
- a concrete resultant-gate example over `F_97`;
- the D3 Fourier/orthogonality identity on signed and ternary toy domains.
