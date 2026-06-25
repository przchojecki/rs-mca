# M1 Quotient Occupancy Theorem

Status: PROVED / AUDIT.

Agent/model: Codex.

Date: 2026-06-25.

This note packages the quotient-occupancy part of the M1 support ledger into a
single theorem.  It does not prove the corrected-reserve M1 local limit.  Its
purpose is to make the quotient-periodic terms exact, so that later work can
separate them cleanly from the aperiodic residue-line target.

## Theorem 1. Exact Fiber-Occupancy Count

Let `D` be partitioned into `N` disjoint fibers

```text
D = B_1 disjoint union ... disjoint union B_N,        |B_i|=m.
```

For a support `S subset D`, define its occupancy profile

```text
c_a(S) = #{ i : |S cap B_i| = a },        0 <= a <= m.
```

Fix a support size `s`.  For every tuple

```text
c=(c_0,...,c_m)
```

with

```text
sum_a c_a = N,        sum_a a c_a = s,
```

the number of supports `S` with occupancy profile `c` is

```text
N! / prod_a c_a!  *  prod_a binom(m,a)^{c_a}.
```

Consequently these profiles partition all exact supports:

```text
sum_c N! / prod_a c_a!  *  prod_a binom(m,a)^{c_a}
  = binom(Nm,s).
```

### Proof

Choose which fibers have occupancy `a`, for every `0<=a<=m`.  This gives the
multinomial factor `N!/prod_a c_a!`.  In each fiber of occupancy `a`, choose
the `a` selected points, giving `binom(m,a)` choices.  Multiplying over fibers
gives the formula.  Summing over all profiles counts every `s`-element support
exactly once.

## Theorem 2. Whole-Fiber Quotient Exchange Ledger

Assume now that `m | s`, put

```text
L=s/m,
```

and consider the exact whole-fiber quotient family

```text
A_m = { union_{i in I} B_i : I subset {1,...,N}, |I|=L }.
```

Then

```text
|A_m| = binom(N,L).
```

For ordered pairs of distinct supports in `A_m`, the exchange profile is

```text
Delta_j(A_m)=0        if m does not divide j,

Delta_{hm}(A_m)
  = binom(N,L) binom(L,h) binom(N-L,h)
```

for

```text
1 <= h <= min(L,N-L).
```

The corresponding maximum exchange codegree is

```text
Gamma_j(A_m)=0        if m does not divide j,

Gamma_{hm}(A_m)=binom(L,h) binom(N-L,h).
```

### Proof

A support in `A_m` is an `L`-subset of the quotient fiber set, hence there are
`binom(N,L)` choices.  Fix one such quotient subset `I`.  A second quotient
subset `J` has exchange size `h` precisely when `J` removes `h` elements of
`I` and inserts `h` elements of the complement.  This gives
`binom(L,h)binom(N-L,h)` choices for `J`.  Lifting from the quotient to `D`
multiplies the exchange size by `m`, since every exchanged quotient point is a
whole fiber.  Multiplying by the number of choices of `I` gives `Delta`, and
maximizing over `I` gives `Gamma`.

## Corollary 3. M1 Strict-Overlap Quotient Budget

Let the exact agreement size be

```text
s = k+t,
```

and let `q` be the line field size used in the support-wise M1 variance
ledger.  The strict M1 high-overlap range is

```text
|S cap T| > k,
```

or equivalently, for equal-size supports,

```text
|S \ T| < t.
```

Therefore the exact whole-fiber family at scale `m` contributes strict
high-overlap terms only when

```text
m | s        and        m <= t-1.
```

When these conditions hold, with `L=s/m`, its strict-overlap weighted
max-codegree ledger is exactly

```text
R_m(t,q)
  = sum_{1 <= h <= min(L,N-L), hm <= t-1}
      binom(L,h) binom(N-L,h) q^(t-hm).
```

Equivalently, with

```text
r = floor((t-1)/m),
```

this is

```text
R_m(t,q)
  = sum_{h=1}^{min(r,L,N-L)}
      binom(L,h) binom(N-L,h) q^(t-hm).
```

In particular, the whole-fiber quotient ledger is zero if `m` does not divide
`s` or if `t<=m`.  In the first active band `m<t<=2m`,

```text
R_m(t,q)=L(N-L) q^(t-m).
```

### Proof

This is Theorem 2 restricted to the exchange levels `j=hm<t`, with the M1
variance weight `q^(t-j)`.

## Corollary 4. Variance-Consumption Form

Let

```text
p_z = q^(-t)(1-q^(-t)).
```

For the whole-fiber quotient family `A_m`, the slope-resolved max-codegree
bound from `m1_average_support_collinearity.md` gives

```text
E[1 - |Bad_t(A_m;f,g)|/q]
  <= (1-p_z)/(binom(N,L)p_z)
     + (4/binom(N,L)) R_m(t,q),
```

whenever `m|s`.  If `m` does not divide `s`, then `A_m` is empty and this
scale contributes no whole-fiber quotient term.

Thus every exact whole-fiber quotient-periodic contribution to the random-line
support ledger is a finite, explicit term.  The non-quotient M1 target is the
remaining support mass after these exact whole-fiber quotient ledgers are
removed or budgeted.

## Dyadic Dither Consequence

Suppose

```text
n=2^nu,        k0=rho n=2^{-b}n,        k=k0-r,
s=k+t=k0+(t-r),
```

and consider a nontrivial dyadic fiber size

```text
m=2^a,        2 <= m <= k0.
```

Since `m|k0`, the exact whole-fiber quotient scale `m` is active only if

```text
m | (t-r)        and        m <= t-1.
```

Consequently, for one fixed slack `t`, the dither `r=t-1` kills every
nontrivial dyadic whole-fiber strict-overlap scale, because then `t-r=1`.

This does not kill a window of adjacent slacks: for any adjacent pair
`t,t+1`, exactly one of `t-r` and `t+1-r` is even, so the scale `m=2` survives
at one of the two slacks whenever the surviving slack is in the active range
and the exact support size is interior.

## Residual M1 Target

The quotient-occupancy theorem separates a budgeted structured term from the
real M1 difficulty:

```text
M1 support ledger
  = exact whole-fiber quotient budgets
    + partial-fiber / aperiodic occupancy residual.
```

The theorem proves the first summand exactly.  It does not control the second.
The remaining corrected-reserve M1 task is to prove that the partial-fiber and
aperiodic residue-line support packings are small enough after the explicit
quotient budgets above have been charged.

## Verification

The finite verifier

```bash
python3 experimental/scripts/verify_m1_quotient_occupancy_theorem.py
```

checks the occupancy count formula, the whole-fiber exchange profile, and the
strict-overlap quotient budget against brute-force enumeration in small cases.
