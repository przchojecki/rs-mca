# L1 Quotient-Budgeted Locator Conjecture

Status: CONJECTURAL / EXPERIMENTAL / COUNTEREXAMPLE-FIRST.

Date: 2026-06-24.

Agent/model: Codex.

## Purpose

This note records a sharper L1 target suggested by the current bad-prime and
prefix-fiber evidence.  The point is to separate all exact cyclic quotient
mass first, then ask for a polynomial bound only on the stabilizer-primitive
remainder.

This is not a proof of L1.  It is a proposed statement plus a falsification
scanner:

```text
python3 experimental/scripts/scan_l1_quotient_budgeted_conjecture.py
```

The scanner is deliberately counterexample-first.  A large primitive remainder
above the entropy reserve would refute the proposed form or force a new
structured stratum into the budget.

## Exact Quotient Ledger

Let `H_n <= F_q^*` be cyclic of order `n`, let `a = k + sigma`, and let
`Fib_U(a)` be the L1 locator fiber:

```text
Fib_U(a) = { S subset H_n :
             |S| = a and U|_S agrees with a polynomial of degree < k }.
```

For a support `S`, write

```text
Stab(S) = { h in H_n : hS = S }.
```

For each divisor `d | n`, let `K_d <= H_n` be the unique subgroup of order
`d`.  Define the containing-stabilizer count

```text
P_d(U,a) = #{ S in Fib_U(a) : K_d <= Stab(S) }.
```

The exact-stabilizer counts are obtained by Mobius inversion on the divisor
lattice:

```text
Q_d(U,a) = sum_{e : d | e | n} mu(e/d) P_e(U,a).
```

Thus `Q_d(U,a)` counts supports whose stabilizer has exact order `d`, and

```text
|Fib_U(a)| = sum_{d | n} Q_d(U,a).
```

The quotient budget of the fiber is

```text
QuotientBudget(U,a) = sum_{d > 1, d | n} Q_d(U,a)
                    = |Fib_U(a)| - Q_1(U,a).
```

The uniform version is

```text
QuotientBudget(H_n,k,a) = sup_U QuotientBudget(U,a).
```

This is an exact support-stabilizer budget, not an asymptotic estimate.  In
the monomial-prefix divisor model, the same definitions apply to complement
supports in a prefix fiber.  The Paper B active quotient cores are the orders
`d > sigma`; this note budgets all `d > 1`, which is stronger as a separation
device and cleaner for falsification.

## Conjectural L1 Form

Fix a rate window `rho in (0,1)` and an entropy slack `epsilon > 0`.  There
should be constants `B = B(rho,epsilon)` and `C = C(rho,epsilon)` such that,
for smooth cyclic domains `H_n` and generated fields `q = poly(n)`, whenever

```text
k = rho n + O(1),
a = k + sigma,
sigma log_2(q) >= (1 + epsilon) log_2 binom(n,a),
sigma >= C n / log n,
```

one has, for every received word `U`,

```text
Q_1(U,a) <= n^B.
```

Equivalently,

```text
|Fib_U(a)| <= QuotientBudget(U,a) + n^B.
```

The monomial-prefix version replaces `Fib_U(a)` by the complement-locator
prefix fiber

```text
Fib_c^pref(m,sigma)
  = { A subset H_n : |A| = m and the top sigma coefficients of
                     prod_{x in A}(X-x) equal c },
```

where `m = n-a`.  The same Mobius ledger gives

```text
|Fib_c^pref| = QuotientBudget_c^pref + Q_1(c),
```

and the toy target is

```text
max_c Q_1(c) <= n^B
```

once the entropy reserve clears.

## Falsification Strategy

The useful failure mode is not a large quotient-periodic fiber; that is already
budgeted.  The useful failure mode is a reserve-cleared prefix fiber with large
primitive mass:

```text
Q_1(c) = |Fib_c^pref| - QuotientBudget_c^pref
```

growing faster than any plausible polynomial exponent allowed by L1.

The scanner therefore reports three classes separately:

1. below-reserve primitive fibers, which show the entropy hypothesis is
   necessary but are not counterexamples to this form;
2. reserve-cleared primitive fibers below the alert threshold, which are
   supporting evidence only;
3. reserve-cleared primitive alerts, which are candidates for a new obstruction
   or a needed refinement of `QuotientBudget`.

The alert threshold in the script is only a scan heuristic.  The conjecture is
the exact `Q_1 <= n^B` statement above.

## First Small-Case Reading

The initial dyadic split-prime scans over `n=16`, `p in {17,97}`, and
`k in {4,...,8}`, `sigma in {1,...,6}` with `m <= 8` do find large primitive
fibers below the entropy reserve.  For example, the `F_17`, `k=7`,
`sigma=1`, `m=8` row has maximum primitive mass `757`.  This confirms that
the reserve condition is doing real work.

In contrast, the first reserve-cleared rows are small.  The known
`F_17`, `n=16`, `k=6`, `sigma=4`, `m=6` row has maximum fiber size `2` and
maximum primitive count `2`; the quotient budget is zero on those two-point
aperiodic collisions.  Across the default `n=16` sweep there are `36`
reserve-cleared rows, no primitive alerts at the threshold `n`, and maximum
reserve-cleared primitive count `5`.

A small `n=24` targeted extension gives the same reading:

```text
p=97,  n=24, k=12, sigma=4, m=8: max Q_1 = 3
p=97,  n=24, k=12, sigma=5, m=7: max Q_1 = 3
p=193, n=24, k=12, sigma=4, m=8: max Q_1 = 3
```

This is not a proof, but it makes the primitive remainder the right object to
attack next.
