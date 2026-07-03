# Quotient Census Window Compiler

Status: PROVED-COMPILER-ARITHMETIC / 2-POWER QUOTIENT COUNT.

This note packages the exact arithmetic behind three required-path DAG nodes:

```text
census_bounded_scales
census_exact_counts
census_window_arithmetic
dyadic_profile_evaluation
census_dodge_selection
```

The scope is deliberately narrow.  We use the 2-power quotient count from
Paper B, compute it exactly at bounded scales, and turn any certified
lower/upper census gap into exact integer windows for the budget
`floor(q_line/2^128)`.  We do not resolve quotient collisions below the norm
threshold, and we do not count primes inside the windows.

The companion verifier is:

```text
python3 experimental/scripts/verify_quotient_census_window_compiler.py
```

It emits:

```text
experimental/data/certificates/quotient-census-window/quotient_census_window_compiler.json
```

## Convention Block

```text
object:             2-power canonical quotient census
quotient order:     N'
quotient count:     A_2(N', ell')
official rates:     rho in {1/2, 1/4, 1/8, 1/16}
ell':               rho N' + 1, required integral
target budget:      B(q) = floor(q / 2^128)
field range:        q < 2^256 unless a consumer prints a smaller range
status discipline:  exact bignums and exact budget windows; no asymptotic tie decisions
```

## Exact Count

For a 2-power quotient order `N'=2^a`, write `n_1=N'/2`.  Paper B's
characteristic-zero antipodal count is

```text
A_2(N',ell') =
  sum_{u >= 0, t = ell' - 2u >= 0, u <= n_1 - t}
      binom(n_1,t) 2^t.
```

At rate `1/2`, `ell'=n_1+1`, this reduces to

```text
A_2(N',n_1+1) = (3^n_1 - 1)/2.
```

Thus every candidate scale in the prize window is an exact integer calculation.
No second-order asymptotic expansion is needed for a tie decision once a
candidate `N'` is chosen.

## Bounded Scale Census

Let

```text
B_max = floor((2^256 - 1) / 2^128) = 2^128 - 1.
```

The verifier evaluates the same integer formula `A_2(N',rho N'+1)` for all
even relaxed scales `N'` with `rho N'` integral.  This relaxed table is an
arithmetic envelope for scale localization; the Paper B 2-power theorem is
consumed at dyadic quotient orders.  In the relaxed 2-power-count model, the
first scale with `A_2 > B_max` is:

```text
rho = 1/2:   N' = 164
rho = 1/4:   N' = 176
rho = 1/8:   N' = 248
rho = 1/16:  N' = 384
```

So the exact-count crossing is bounded by `N' <= 384` throughout the official
rates and field-size range.  For smaller budgets corresponding to
`q ~= 2^192` and `q ~= 2^224`, the first relaxed crossings are respectively:

```text
budget bits 64:   84, 88, 128, 192
budget bits 96:   124, 132, 184, 288
```

This proves the useful census fact: the exact integer endgame only sees a
bounded scale range independent of the deployed blocklength `n` and dimension
`k`, once the row has been localized to the quotient-count model.

There is one important bookkeeping correction.  Actual 2-power quotient orders
are dyadic.  Dyadic coarsening may jump over the relaxed crossing.  Against
`B_max`, the first dyadic scale above budget is:

```text
rho = 1/2:   N' = 256
rho = 1/4:   N' = 256
rho = 1/8:   N' = 256
rho = 1/16:  N' = 512
```

Thus the relaxed scale window is `<=384`, while a pure dyadic packet should
also inspect the adjacent dyadic scale, which can be `512` at rate `1/16`.
This is still a finite absolute census, and the verifier emits both tables.

## Exact Budget Windows

Let a row-specific proof attempt provide:

```text
L = certified lower count,
K = exact or safe upper count,
0 <= L <= K.
```

The unresolved budget values are exactly

```text
floor(q/2^128) in [L, K).
```

Equivalently, the unresolved line-field sizes are the single integer interval

```text
q in [ L 2^128, K 2^128 - 1 ],
```

with the convention that the interval is empty when `L=K`.  If a row requires
`q == 1 mod n`, the admissible-integer count in any interval `[Q0,Q1]` is

```text
max(0, floor((Q1-r)/n) - floor((Q0-1-r)/n)),
```

where `r=1`.  A prime counter can be applied afterwards, but primality is not
part of this compiler lemma.

This discharges the exact arithmetic of `census_window_arithmetic`: as the
certified lower count `L` rises to the exact count `K`, the unresolved interval
shrinks monotonically and vanishes at `L=K`.

## Dyadic Quotient-Profile Evaluation

Paper B defines the quotient-core profile by

```text
Q_H(eta) =
  max_{M | gcd(n,k), ceil(eta n) < M, k/M <= n/M - 1}
      log2 binom(n/M - 1, k/M),
```

with value `-infinity` when the active set is empty.

For a 2-power row `n=2^m`, `k=rho n`, and integer slack

```text
sigma = ceil(eta n),
```

the exact evaluator is the finite maximum

```text
Q_2(n,k,sigma) =
  max_{M = 2^e | gcd(n,k), sigma < M, k/M <= n/M - 1}
      log2 binom(n/M - 1, k/M).
```

The verifier records the maximizing integer count

```text
K_Q(n,k,sigma) =
  max binom(n/M - 1, k/M)
```

instead of a floating logarithm.  This is equivalent and avoids rounding in
profile comparisons.  At the official rates, `k` is a power of two whenever
`n` is a sufficiently divisible power of two, so this is a direct exact
enumeration of all active dyadic quotient cores.

For near-capacity certificate work, the relevant slacks are large enough that
`n/M` is bounded.  For example, if `sigma >= n/256`, every active scale has
quotient order `N=n/M <= 128`; if `sigma >= n/128`, every active scale has
`N <= 64`.  Thus the profile values needed by the bounded census are exact
small bignums, independent of the ambient deployed blocklength.

## Consumer Schema

A row-specific census packet should print:

```text
rate rho
quotient order N'
ell' = rho N' + 1
exact K = A_2(N',ell') or another certified count
certified lower L
budget interval [L,K)
q interval [L 2^128, K 2^128 - 1]
dyadic profile K_Q(n,k,sigma), if consuming a quotient-profile hypothesis
congruence modulus n, if applicable
admissible-integer count, and optional prime subcount
```

The packet must also print whether it is using the exact 2-power count, a
mixed-radix analogue, or a conditional quotient-collision lower bound.

## DAG Discharge

This note discharges the 2-power compiler part of:

```text
census_bounded_scales       bounded relaxed crossing table, dyadic coarsening table;
census_exact_counts         exact A_2 bignum formula and bounded-scale replay;
census_window_arithmetic    exact budget-to-q interval conversion.
dyadic_profile_evaluation   exact finite max for Q_H on 2-power rows.
census_dodge_selection      the companion note turns exact windows into
                            explicit row-budget dodge certificates.
```

It does not discharge:

```text
mixed-radix exact quotient counts;
zone-b quotient collision resolution;
prime counts inside the admissible-integer windows;
global quotient-periodic branch exhaustion.
```
