# L1 Prefix Fibers as Divisor-Coefficient Counts, with an Exact Quotient-Core Floor

- **Status:** PROVED (lemma + corollary) / EXPERIMENTAL (scan) / AUDIT (cross-check).
- **Agent/model:** Claude Opus 4.8.
- **Date:** 2026-06-18.
- **Scope:** Paper B `conj:prefix-local` (`tex/slackMCA_v3.tex`) and the L1 target
  in `agents.md`. This note does not edit Papers A--D and does not assert
  Reed--Solomon list decoding, MCA, or protocol safety. It is the list/locator
  side of the program; it does not touch the M1 residue-line work.

## Claim

Two results about the monomial-prefix fiber
`Phi_sigma^{-1}(c)` of Paper B (`def:locator-fiber`, `prop:monomial-fiber`),
recast through the complement-locator bijection of
`l1_aperiodic_prefix_collision.md`:

1. **Divisor-coefficient form (reframing, PROVED).** For `H = mu_n <= F_q^*`,
   `s = k+sigma`, `m = n-s`, the prefix fiber is in canonical bijection with the
   set of monic degree-`m` divisors of `X^n-1` over `F_q` whose top `sigma`
   coefficients are prescribed. So `conj:prefix-local` is exactly a
   *divisor-coefficient counting* statement on `X^n-1`.

2. **Quotient-core floor (PROVED).** For every subgroup order `d` with
   `d \mid \gcd(n, s)` and `d > sigma`,
   ```text
   max_c |Phi_sigma^{-1}(c)|  >=  binom(n/d, m/d).
   ```
   This is the exact list/locator-side image of the quotient-core obstruction.
   It is *forced by coset-union locators alone*, independently of field size, and
   it is removed by dimension dithering whenever `gcd(n, s) <= sigma`.

Both are verified by `verify_l1_prefix_divisor_count.py`, which also reproduces
the `F_17` certificate of `l1_aperiodic_prefix_collision.md`.

## Status

PROVED / EXPERIMENTAL / AUDIT.

## Parameters

`q`, `q_gen = q` (split case `n \mid q-1`), `n = 2^m_0`, `k`, `rho = k/n`,
`sigma`, `s = k+sigma`, `m = n-s`. Toy cases: `q=17, n=16` (this note);
`q=257, n=256` and dyadic `n` flagged for the optimized non-enumerative path.

## Existing paper dependency

- `def:locator-fiber`, `prop:monomial-fiber`, `prop:arb-fiber`,
  `conj:prefix-local`, `conj:arbitrary-local` in `tex/slackMCA_v3.tex`.
- The complement-locator compression (`E_S(Z) E_A(Z) = 1-(-Z)^n`) and the
  divisor-gap picture of `experimental/l1_aperiodic_prefix_collision.md`.
- The honest-list repair (`ImgFib`) of `experimental/l1_arbitrary_fiber_repair.md`:
  the raw `Fib_U` overcounts; the prefix fiber `Phi_sigma^{-1}(c)` is exact only
  for monomial-prefix data, which is the regime treated here.

## 1. Divisor-coefficient reframing

Let `H = mu_n <= F_q^*` (so `n \mid q-1`, `X^n - 1 = prod_{h in H}(X-h)`).
For `S in binom(H, s)` let `A = H \ S`, `|A| = m`. The locator
`L_A(X) = prod_{a in A}(X-a)` is a **monic degree-`m` divisor of `X^n-1`**, and
every such divisor arises this way (its roots are distinct elements of `H`).
The complement-prefix lemma gives, for equal-size supports `S,T`,
```text
Phi_sigma(S) = Phi_sigma(T)
  iff  (e_1(A),...,e_sigma(A)) = (e_1(B),...,e_sigma(B))
  iff  L_A and L_B share their top sigma coefficients,
```
where `B = H \ T`. Writing the prescribed top-`sigma` coefficient vector as the
fiber key, we obtain the canonical bijection
```text
Phi_sigma^{-1}(c)  <->  { monic degree-m D | X^n-1 : top sigma coeffs of D fixed }.
```
Thus the prefix-fiber histogram of `conj:prefix-local` is the histogram of
degree-`m` divisors of `X^n-1` bucketed by their top `sigma` coefficients. This
is the object the scanner computes directly (no codewords, no field-size
enumeration), and it reproduces the `F_17, k=6, sigma=4` certificate exactly
(8008 divisors, 7968 distinct keys, 40 two-point fibers, max fiber 2).

## 2. The quotient-periodic locator lemma

For `d \mid n`, let `K_d <= H` be the unique subgroup of order `d`
(`K_d = mu_d`). Call `A <= H` a **`K_d`-coset-union** if `A K_d = A`.

**Lemma (coset-union locators are `X^d`-polynomials).**
Let `A` be a `K_d`-coset-union with `|A| = m` (so `d \mid m`). Write the cosets
comprising `A` as `zeta_1 K_d, ..., zeta_{m/d} K_d`. Then
```text
L_A(X) = prod_{j=1}^{m/d} (X^d - beta_j),   beta_j := zeta_j^d,
```
a polynomial `G(X^d)` with `G(Y) = prod_j (Y - beta_j)` monic of degree `m/d`.
The `beta_j` are distinct `(n/d)`-th roots of unity, so `G` is a monic
degree-`m/d` divisor of `Y^{n/d}-1`. The map `A \mapsto G` is a bijection from
`K_d`-coset-union divisors of degree `m` onto `(m/d)`-subsets of `mu_{n/d}`; in
particular there are exactly `binom(n/d, m/d)` of them.

*Proof.* For a single coset, `prod_{kappa in K_d}(X - zeta kappa)
= prod_{kappa in mu_d}(X - zeta kappa) = X^d - zeta^d`, because the left side is
monic of degree `d`, vanishes exactly at `zeta mu_d`, and `X^d - zeta^d` has the
same roots. Multiplying over the `m/d` chosen cosets gives the displayed product,
which is a polynomial in `X^d`. Each `beta_j = zeta_j^d` satisfies
`beta_j^{n/d} = zeta_j^n = 1`; distinct cosets give distinct `beta_j` (the `d`-th
power map `mu_n -> mu_{n/d}` has kernel `K_d`, so it is injective on coset
representatives). Conversely any `(m/d)`-subset of `mu_{n/d}` lifts to a unique
`K_d`-coset-union via the surjection `mu_n -> mu_{n/d}`. ∎

**Coefficient corollary.** Since `L_A = G(X^d)` has nonzero coefficients only at
degrees divisible by `d`, and `d \mid m`, the coefficient of `X^{m-i}` vanishes
unless `d \mid i`. Hence the top `sigma` coefficients of `L_A` are:
- forced zeros at all positions `i in {1,...,sigma}` with `d \nmid i`, and
- the top `floor(sigma/d)` coefficients of `G` at positions `i in {d,2d,...}`.

So `Phi_sigma` restricted to `K_d`-coset-unions factors through
`Phi_{floor(sigma/d)}` of the *smaller* divisor problem on `mu_{n/d}`.

**Corollary (quotient-core floor).** If `d > sigma` then `floor(sigma/d) = 0`:
every `K_d`-coset-union of degree `m` has the all-zero top-`sigma` key, so they
all share one fiber. Therefore, for every `d \mid gcd(n, s)` with `d > sigma`,
```text
max_c |Phi_sigma^{-1}(c)|  >=  #{K_d-coset-union divisors of degree m}
                            =  binom(n/d, m/d).
```
(`d \mid m = n-s` and `d \mid n` together are equivalent to `d \mid gcd(n,s)`.)

### Consequences

- **Field-independence.** The floor `binom(n/d, m/d)` does not involve `q`. No
  generated-field entropy reserve can suppress it; this is exactly why the
  arbitrary-word raw conjecture needs the quotient-core carve-out of
  `conj:prefix-local`, on the list side as well as the MCA side.
- **Dithering kills it (link to L3).** If `k` is chosen so that
  `gcd(n, k+sigma) <= sigma`, then no order `d > sigma` divides `gcd(n,s)`, and
  this coset-union floor is empty. This is the locator-side statement of the
  `k = rho n - r` dimension dithering studied in `quotient_profile_dither.md`:
  the dither target is to make `gcd(n, k+sigma) <= sigma`.
- **Aperiodic remainder is the real target.** After removing coset-union
  divisors for all active `d > sigma`, the *aperiodic* prefix count is what
  `conj:prefix-local` predicts to be `binom(n,s)/q^sigma + O(n^B)`. The scan
  isolates and counts this remainder; bounding it is the open analytic step
  (and the direct list-side analogue of Codex's M1 aperiodic residue-line wall).

## 3. Numerical experiment (`F_17`, `n=16`)

Exact full enumeration of all `binom(16,m)` divisors, bucketed by top-`sigma`
coefficients. The coset-union count matches `binom(n/d, m/d)` and the floor is
respected in all 35 `(k,sigma)` cases swept by the verifier. Selected rows:

| rho   | k | sigma | m | entropy margin (bits) | max fiber | quot. floor (d>sigma) | nonsingleton aperiodic |
|-------|---|-------|---|----------------------:|----------:|----------------------:|-----------------------:|
| 6/16  | 6 | 4     | 6 | +3.383                |        2  | 0 (none divides gcd=2)|  80 / 80               |
| 4/16  | 4 | 4     | 8 | +2.698                |        2  | 2  (d=8)              | 480 / 482              |
| 6/16  | 6 | 2     | 8 | -5.477                |       54  | 6  (d=4)              | 12864 / 12870          |
| 7/16  | 7 | 1     | 8 | -9.564                |      758  | 70 (d=2)              | 12800 / 12870          |

Reading: where the generated-field entropy margin is positive (rows 1--2), the
aperiodic prefix fibers are already polynomial (max size 2) and the only
non-aperiodic members are the coset-union divisors flagged by the lemma. Where
the margin is negative (rows 3--4) the random codimension-`sigma` law dominates
and fibers sit near `binom(16,m)/17^sigma`; the coset-union floor is still
present but submerged. `F_17, n=16` is too small to realize a large quotient
floor *and* a cleared entropy margin simultaneously; that separation needs
`n in {32,64}` (next iteration, optimized path).

## 4. Audit cross-check

`verify_l1_prefix_divisor_count.py --self-check` confirms, against
`l1_aperiodic_prefix_collision.md`:

- `total_divisors = 8008`, `distinct_prefix_values = 7968`, `max_fiber = 2`,
  `two_point_fibers = 40`;
- all 40 nonsingleton fibers are aperiodic for the active orders `{8,16}`
  (matching the note's `M=8`/`M=16` coset-union exclusion);
- the `X^d -> Y` injection of the Lemma holds for every order `d in {2,4,8,16}`;
- the coset-union identity `binom(n/d,m/d)` and the quotient-core floor hold
  across a 35-case `(k,sigma)` sweep.

No discrepancy with the existing certificate.

## Ledger impact

- **Quotient (worsens, now explicit):** gives an exact, field-independent
  lower-bound floor `binom(n/d,m/d)` on the worst-case prefix list, on the
  locator side. Quantifies the `Quot_{sigma,c}` term of `conj:prefix-local`.
- **Entropy (clarified):** the floor cannot be paid by `q_gen`; entropy controls
  only the aperiodic remainder.
- **Dimension dithering (improves):** identifies the exact dither target
  `gcd(n, k+sigma) <= sigma` that empties the coset-union floor.

## Constants

Floor `= binom(n/d, m/d)` for each `d \mid gcd(n,k+sigma)`, `d > sigma`.
The dominant floor is at the smallest such `d`. For dyadic `n=2^{m_0}` the active
`d` are powers of two; the largest dither-resistant floor at fixed `(rho,sigma)`
is `binom(n/d*, m/d*)` with `d* = ` smallest power of two `> sigma` dividing
`gcd(n,s)`.

## Reproducibility

```bash
python3 experimental/verify_l1_prefix_divisor_count.py --self-check
python3 experimental/verify_l1_prefix_divisor_count.py --p 17 --n 16 --k 4 --sigma 4
python3 experimental/verify_l1_prefix_divisor_count.py --p 17 --n 16 --k 4 --sigma 4 --format json
```

## What to do next

1. **Aperiodic remainder bound.** Prove `binom(n,s)/q^sigma + O(n^B)` for the
   *aperiodic* divisor count (coset-unions removed) in a region beyond the
   Johnson anchor `a^2 > n(k-1)` of `l1_aperiodic_prefix_collision.md`.
2. **Scale up.** Add a non-enumerative divisor-coefficient counter (transfer over
   the factorization of `X^n-1`, or coset-DP) to reach `n=32,64` and the
   `q=257` toy case, where a cleared entropy margin can coexist with a large
   quotient floor.
3. **Inclusion-exclusion over orders.** The floors for different `d` overlap
   (a divisor can be coset-union for several `d`); compute the exact union via
   Mobius over the subgroup lattice to get the sharp total quotient-core count,
   not just the per-`d` lower bound.
4. **Lift to arbitrary words.** Connect the prefix (monomial) floor to the
   honest list `ImgFib_U` of `l1_arbitrary_fiber_repair.md` for non-prefix `U`.
