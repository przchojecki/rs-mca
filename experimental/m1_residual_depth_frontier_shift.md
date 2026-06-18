# M1 Residual-Depth Frontier Shift

**Status:** PROVED / AUDIT.

This note isolates the residual-depth hierarchy behind the low-slack M1 packet
templates. It explains why the slack-two depth-two conic and the slack-three
first-superboundary conic are the same object.

## General Shift

Fix slack `T`, residual depth `d>=1`, and a multiplicative subgroup
`D subset F_p^*`. A normalized residual packet of size `T+d` is written

```text
P = {1,u_1,...,u_(T+d-1)}.
```

The depth-`d` catalog is cut out by

```text
e_1(P)=...=e_(T-1)(P)=0.
```

Its first slope coefficient is

```text
c_{T,d}(P)=(-1)^T e_T(P).
```

If `d>=2`, then the zero-slope subcatalog satisfies

```text
c_{T,d}(P)=0
  <=> e_1(P)=...=e_T(P)=0
  <=> P lies in the depth-(d-1) catalog at slack T+1.
```

At fixed exact support size this is the dimension shift

```text
(T,k,d) -> (T+1,k-1,d-1).
```

The quotient-lift gate is unchanged, because both sides have the same residual
packet size `T+d` and the same exact support size.

## Weighted Ladder Identity

Fix a quotient decomposition of `D` into `N` fibers of common size `m`, an
exact support size `s`, and a normalized residual packet size `r`.  For
`1<=T<r`, put

```text
C_T(r) = { P subset D : 1 in P, |P|=r,
           e_1(P)=...=e_(T-1)(P)=0,
           all elements of P are distinct },
Z_T(r) = { P in C_T(r) : e_T(P)=0 },
F_T(r) = { P in C_T(r) : e_T(P)!=0 }.
```

Let `tau(P)` be the number of quotient fibers touched by `P`.  The
exact-support quotient-lift weight is

```text
w_s(P) =
  binom(N-tau(P), (s-r)/m),  if s>=r and m | (s-r),
  0,                         otherwise.
```

Then the zero-frontier shift is the literal set identity

```text
Z_T(r) = C_(T+1)(r).
```

Consequently, for every packet statistic `Phi(P)` independent of the slack
label,

```text
sum_{P in Z_T(r)} w_s(P) Phi(P)
  = sum_{P in C_(T+1)(r)} w_s(P) Phi(P).
```

This applies in particular to `Phi=1`, to exact quotient-lift support weights,
and to shifted frontier slope histograms.  The proof is only the definition:
adding `e_T(P)=0` to the equations cutting out `C_T(r)` gives exactly the
equations cutting out `C_(T+1)(r)`, while `w_s(P)` depends on the packet `P`,
the fixed support size, and the quotient fibers touched by `P`, not on the
slack label used to describe the same packet.

Iterating the identity gives the disjoint weighted decomposition

```text
C_T(r) = F_T(r) disjoint F_(T+1)(r) disjoint ... disjoint F_(r-1)(r)
         disjoint C_r(r).
```

All inherited zero-frontier terms are therefore carried to the next slack with
the same weight.  This removes the bookkeeping source of a multiplicative
depth loss: the only new contribution exposed at rung `T` is `F_T(r)`.

This is only the lossless bookkeeping part of the M1/X1 no-square-root-loss
route.  It does not prove the required nonzero-frontier character-sum estimate.
The remaining analytic target is a depth-uniform `O(sqrt(p))` conductor bound
for the single new frontier exposed at each rung.

## Additive Error Criterion

Let `E` be any nonnegative certificate functional on weighted packet families
which is subadditive on disjoint unions.  Examples include a triangle-inequality
bound for a character-sum error term, a weighted L1 coefficient mass, or a
union-bound slope-image certificate.  Applying `E` to the weighted ladder
identity gives

```text
E(C_T(r)) <= E(F_T(r)) + E(C_(T+1)(r)).
```

Iterating,

```text
E(C_T(r)) <= sum_{a=T}^{r-1} E(F_a(r)) + E(C_r(r)).
```

Thus a uniform nonzero-frontier estimate

```text
E(F_a(r)) <= K_r sqrt(p)       for all T <= a < r
```

implies the additive ladder bound

```text
E(C_T(r)) <= (r-T) K_r sqrt(p) + E(C_r(r)).
```

The terminal term `C_r(r)` is the pure-zero power-coset ledger described in
`experimental/m1_low_slack_packet_template_theorem.md`; it is explicit and
does not require a new character-sum estimate.  Hence the M1/X1 no-loss
question for this packet ladder is reduced to the uniformity of the
nonzero-frontier conductor constants `K_r`.  If such constants are independent
of residual depth, the recursion pays one square-root error per newly exposed
frontier.  A multiplicative blowup can only enter if the analytic
nonzero-frontier estimates themselves deteriorate with the shift.

## Frontier Partition

Iterating the shift partitions a depth-`d` packet by its first nonzero
coefficient. For `0<=j<d`, define

```text
F_{T,d}^{(j)} = { P : |P|=T+d,
                  e_1(P)=...=e_(T+j-1)(P)=0,
                  e_(T+j)(P) != 0 }.
```

The terminal stratum is

```text
F_{T,d}^{(infty)} = { P : |P|=T+d,
                      e_1(P)=...=e_(T+d-1)(P)=0 }.
```

On `F_{T,d}^{(j)}`, after `j` shifts the first nonzero slope is

```text
z_j(P)=(-1)^(T+j) e_(T+j)(P),
```

and scaling by `x in D` sends it to `x^(T+j) z_j(P)`. Thus the `j`-frontier
slope image is a union of `D^(T+j)` cosets. In the original slack-`T`
catalog, only `j=0` contributes nonzero slopes; later frontiers are inherited
zero-slope packets for that original slack.

## First Concrete Interface

For `T=2,d=2`, write

```text
P={1,u,v,w},        w=-1-u-v.
```

The slack-two depth-two slope coefficient is

```text
A(u,v)=-(u^2+v^2+uv+u+v+1).
```

Hence the zero-slope slice `A(u,v)=0` is exactly

```text
C_3(D) = { (u,v) in D^2 :
           w=-1-u-v in D,
           1,u,v,w distinct,
           u^2+v^2+uv+u+v+1=0 },
```

the slack-three first-superboundary conic shape set. This is why the
slack-two depth-two theorem and the slack-three first-superboundary theorem are
not isolated low-slack facts: they are adjacent frontiers in the same
residual-depth hierarchy.

## Verification

The dedicated verifier

```bash
python3 experimental/verify_m1_residual_depth_frontier_shift.py
```

checks the first concrete shift using the scanner's second-superboundary and
next-slack first-superboundary ledgers. It compares parameter counts, active
parameter counts, packet counts, and exact-support weighted support counts in
both active and inactive quotient-lift gates.

The ladder audit

```bash
python3 experimental/verify_m1_residual_depth_ladder.py
```

enumerates normalized residual packets for several small fixed packet sizes and
checks every adjacent shift in the resulting slack ladder.  For each shift it
compares the inherited packet set, exact quotient-lift weight, and shifted
slope histogram against the next-slack catalog.  A mismatch would be a finite
counterexample to the lossless frontier-shift bookkeeping; the current audited
cases find none.
