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

## Theorem 5. Fiberwise Exchange Kernel

The whole-fiber quotient family is only one occupancy stratum.  The exact
residual bookkeeping can also be written fiber by fiber.

Fix two occupancy vectors

```text
a=(a_1,...,a_N),        b=(b_1,...,b_N),
```

with

```text
0 <= a_i,b_i <= m,        sum_i a_i = sum_i b_i = s.
```

Fix a support `S` satisfying

```text
|S cap B_i| = a_i        for every i.
```

Let `E_{a->b}(j;S)` be the number of supports `T` with

```text
|T cap B_i| = b_i        for every i,
|S \ T| = j.
```

Then `E_{a->b}(j;S)` is independent of the particular support `S` with
occupancy vector `a`, and its generating polynomial is

```text
sum_j E_{a->b}(j;S) x^j
  = prod_{i=1}^N
      sum_{r=max(0,a_i+b_i-m)}^{min(a_i,b_i)}
        binom(a_i,r) binom(m-a_i,b_i-r) x^(a_i-r).
```

### Proof

In fiber `B_i`, the target support `T` has `b_i` points and meets the fixed
set `S cap B_i` in some number `r_i`.  This number must satisfy

```text
max(0,a_i+b_i-m) <= r_i <= min(a_i,b_i).
```

For fixed `r_i`, there are

```text
binom(a_i,r_i) binom(m-a_i,b_i-r_i)
```

choices: keep `r_i` of the `a_i` selected points of `S`, and choose the
remaining `b_i-r_i` target points from the `m-a_i` unselected points of the
fiber.  The fiber contributes `a_i-r_i` removed points to `|S \ T|`.  The
fibers are independent, so multiplying the one-fiber generating functions and
taking the coefficient of `x^j` gives the formula.

## Corollary 6. Internal Partial-Fiber Ledger

For a fixed occupancy vector `a`, the exchange kernel inside the same labeled
occupancy stratum is

```text
K_a^int(x)
  = prod_{i=1}^N
      sum_{e=0}^{min(a_i,m-a_i)}
        binom(a_i,e) binom(m-a_i,e) x^e.
```

In particular,

```text
[x] K_a^int(x) = sum_i a_i(m-a_i).
```

Thus a labeled occupancy vector has no exchange-one internal residual if and
only if every fiber is either empty or full.  Partial fibers are therefore the
first unavoidable source of aperiodic low-exchange mass after the whole-fiber
quotient scales have been removed.

For M1 slack `t`, the exact same-vector internal weighted strict-overlap
ledger is

```text
R_a^int(t,q)
  = sum_{1 <= j <= t-1} [x^j] K_a^int(x) q^(t-j).
```

This does not yet sum over all occupancy vectors or over cross-vector moves.
It gives the local residual kernel that a proof of the aperiodic M1 bound has
to control.

## Theorem 7. Sharp Exchange-One Residual Floor

For an occupancy vector `a=(a_1,...,a_N)`, put

```text
P(a) = [x] K_a^int(x) = sum_i a_i(m-a_i).
```

Write the support size as

```text
s = Lm+b,        0 <= b < m.
```

If `1 <= b < m`, then every occupancy vector of total size `s` satisfies

```text
P(a) >= b(m-b).
```

Equality holds exactly for one-remainder vectors: one fiber has occupancy
`b`, while every other fiber is empty or full.

If `b=0`, then

```text
P(a) >= 0,
```

with equality exactly on whole-fiber vectors.  If additionally `0<s<Nm` and
`a` is not a whole-fiber vector, then

```text
P(a) >= 2(m-1).
```

Equality in this non-whole case means that two partial fibers have occupancies
`1` and `m-1` (the same occupancy value when `m=2`) and every other fiber is
empty or full.

### Proof

Let `f(u)=u(m-u)`.  For two partial occupancies `1<=u,v<=m-1`, if
`u+v<=m` then replacing the two fibers by occupancies `u+v` and `0` preserves
the total support size and changes `P` by

```text
f(u)+f(v)-f(u+v)=2uv>0.
```

If `u+v>=m`, replacing them by `m` and `u+v-m` preserves the total support
size and changes `P` by

```text
f(u)+f(v)-f(u+v-m)=2(m-u)(m-v)>0.
```

Thus merging partial occupancies strictly decreases `P` until the partial mass
is concentrated as much as the residue class permits.  For nonzero residue
`b`, the terminal configuration has one partial fiber of size `b`, giving
`b(m-b)`.  For residue zero, the minimum is `0` and occurs precisely when no
partial fibers remain.  A non-whole residue-zero vector has at least two
partial fibers; since every partial fiber contributes at least `m-1`, it has
`P(a)>=2(m-1)`, with equality exactly in the stated endpoint configuration.

## Theorem 8. Large-Fiber One-Remainder Budget

Let

```text
s = Lm+b,        1 <= b < m,
```

and let `A_{L,b}` be the one-remainder family consisting of `L` whole fibers,
one partial fiber of size `b`, and all other fibers empty.  Assume `t<=m`.
For fixed `S in A_{L,b}`, the strict exchange enumerator

```text
H_{L,b}^{<t}(x)
  = sum_{T in A_{L,b}, 0<|S\T|<t} x^|S\T|
```

is exactly

```text
H_{L,b}^{<t}(x)
 =
  sum_{ell=1}^{min(b,m-b,t-1)}
    binom(b,ell) binom(m-b,ell) x^ell

  + 1_{b<t} (N-L-1) binom(m,b) x^b
  + 1_{m-b<t} L binom(m,b) x^(m-b).
```

Consequently the one-remainder strict M1 weighted ledger is

```text
R_{L,b}^{<t}(t,q)
 =
  sum_{ell=1}^{min(b,m-b,t-1)}
    binom(b,ell) binom(m-b,ell) q^(t-ell)

  + 1_{b<t} (N-L-1) binom(m,b) q^(t-b)
  + 1_{m-b<t} L binom(m,b) q^(t-m+b).
```

### Proof

Because `t<=m`, any strict exchange has size below one full fiber.  Thus no
ordinary whole-fiber quotient exchange can occur.  There are only three
possibilities.

First, the partial fiber is the same in `S` and `T`; exchanging `ell` points
inside that fiber gives

```text
binom(b,ell) binom(m-b,ell)
```

choices and exchange size `ell`.  Second, the old partial fiber is removed and
the new partial fiber lies in one of the `N-L-1` empty fibers; this contributes
`b` removed points and `(N-L-1)binom(m,b)` choices.  Third, the old partial
fiber is promoted to a whole fiber, while one of the old whole fibers becomes
the new partial fiber; this contributes `m-b` removed points and
`L binom(m,b)` choices.  These are exactly the three displayed terms.

### Dither Consequence

In a quotient hierarchy with

```text
n=Nm,        k0=Lm,        k=k0-r0,        s=k+t,
d=t-r0,
```

suppose

```text
1 <= d < t,        m >= t+d.
```

Then `b=d`, the third term above is absent, and Vandermonde gives

```text
H_{L,d}^{<t}(1)
  = (N-L) binom(m,d) - 1
  = ((n-k0)/m) binom(m,d) - 1.
```

Thus maximal one-slack dither, `d=1`, gives the linear residual

```text
H_{L,1}^{<t}(x) = (n-k0-1)x,
R_{L,1}^{<t}(t,q) = (n-k0-1)q^(t-1).
```

For the adjacent slack with the same dither, `d=2`, every scale with
`m>=t+2` has unweighted strict mass

```text
((n-k0)/m) binom(m,2) - 1 = (n-k0)(m-1)/2 - 1.
```

So a fixed dither can make the large-fiber one-remainder residual linear at
one slack, but the next slack already restores scale-dependent residual mass.

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
    + one-remainder quotient budgets
    + partial-fiber / aperiodic occupancy residual.
```

The theorem proves the first summand exactly and gives the large-fiber
one-remainder budget in the first residual layer.  It does not control the
remaining mixed partial-fiber or aperiodic residue-line support packings.  The
remaining corrected-reserve M1 task is to show that those residual packings are
small enough after the explicit quotient and one-remainder budgets above have
been charged.

## Verification

The finite verifier

```bash
python3 experimental/scripts/verify_m1_quotient_occupancy_theorem.py
```

checks the occupancy count formula, the whole-fiber exchange profile, and the
strict-overlap quotient budget against brute-force enumeration in small cases.
It also checks the fiberwise exchange kernel for several partial-fiber
occupancy vectors, the sharp exchange-one residual floor, and the large-fiber
one-remainder formula.
