# Rate-half cyclic quotient-rotation list floor

```yaml
workboard_item: L
row: F_q, D multiplicative coset of size n=2^41, k=2^40, rho=1/2
object: LIST
target_epsilon: none (DIRECT_LIST lower construction)
agreement: 1116691496959 = 2^40 + 2^34 - 1
B_star: not applicable
direct_statement: the worst ordinary list at this agreement is at least ceil(binomial(255,129)/256)
architecture: DIRECT
partition_digest: not applicable (DIRECT)
atom_or_cell: DIRECT
quantifier: every finite field F_q with 2^41 dividing q-1 and every multiplicative coset D of size 2^41
projection_and_unit: distinct Reed--Solomon codewords in one Hamming ball
claimed_bound: 11092230961998080258863221315535829014398723445840079610908300691051869570
status: PROVED
impact: ROW_COUNTEREXAMPLE
falsifier: a failed locator rotation identity, high-coefficient collision count, distinctness/root-set check, or exact cap inequality
replay: python3 experimental/scripts/verify_rate_half_cyclic_quotient_rotation_floor.py; python3 experimental/scripts/audit_rate_half_cyclic_quotient_rotation_floor.py
```

## Lane-L packet

```text
row:                 (F_q, D, k=2^40, n=2^41, rho=1/2), 2^41 | q-1
object:              ordinary LIST, not MCA
radius/agreement:    delta=(2^40-2^34+1)/2^41; a=2^40+2^34-1
Johnson comparison: delta > 1-sqrt((2^40-1)/2^41), certified by a^2<n(k-1)
bound:               L_C(delta) >= ceil(C(255,129)/256) = the printed 243-bit integer
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS[F_q,D,2^40], no C^+ shift
status:              PROVED
```

Here `L_C(delta)` is the maximum, over received words, of the number of
distinct codewords in the closed relative Hamming ball of radius `delta`.
The result is a lower construction beyond Johnson, not a list-size upper
bound.  The concrete prime

```text
q_0=6,597,069,766,657=3*2^41+1
```

gives one fully declared row.  The verifier supplies a Pocklington
certificate for `q_0` and an element of exact order `2^41`.  The theorem is
stronger: it applies to every field and coset satisfying the displayed
divisibility condition.

## Theorem

Let `F_q` be a finite field, let `D` be a multiplicative coset of size `n`,
and let `C=RS[F_q,D,n/2]`.  Suppose `c | n/2`, put `N=n/c`, and choose

```text
1 <= d <= N/2-1,       m=N/2+d,       0<s<c.
```

There is a received word having at least

```text
ceil(binomial(N-1,m)/(N*q^(d-1)))                    (1)
```

distinct codewords at agreement exactly

```text
n/2+d*c+s.                                           (2)
```

At the Lane-L row, take

```text
n=2^41, c=2^33, N=256, d=1, m=129, s=c-1.
```

Equations (1) and (2) become the exact bound and agreement printed above.
Since

```text
(2^40+2^34-1)^2 < 2^41(2^40-1),
```

the agreement is below the Guruswami--Sudan/Johnson agreement
`sqrt(n(k-1))`; equivalently, its radius is strictly beyond Johnson.  Also,
for every `q<2^256`, the list lower bound is greater than `2^238`, and hence
greater than `q/2^128`.  This last comparison records the proximity-prize
scale but does not convert the list into an MCA statement.

## Proof

Write `D=gamma H` and let `Q=D^c`.  Then `Q` is a multiplicative coset of
size `N`, and every `y in Q` satisfies `y^N=delta`, where
`delta=gamma^n`.  Fix one quotient point `b_0`, and let `L_0(X)` vanish on a
fixed `s`-subset of its `c`-point fiber.

For each `m`-subset `A` of `Q\{b_0}`, write

```text
P_A(Y)=product_(b in A)(Y-b)=sum_(j=0)^m a_j(A)Y^j
```

and cyclically rotate its coefficient arc modulo `Y^N-delta`:

```text
R_A(Y)=rem_(Y^N-delta)(Y^(N-d)P_A(Y))
      =sum_(j=0)^(d-1) a_jY^(N-d+j)
       +delta sum_(j=d)^m a_jY^(j-d).               (3)
```

Set `L_A(X)=L_0(X)R_A(X^c)`.  Because `s<c`, the coefficient blocks do not
overlap.  The complete part of `L_A` in degrees at least `k=n/2` depends
only on `a_0,...,a_(d-1)`; the block arising from `a_m=1` is fixed.

There are at most `N*q^(d-1)` possible such prefixes.  Indeed, `a_0` is,
up to a fixed sign, a product of `m` members of one multiplicative coset and
therefore has at most `N` values; each other coefficient has at most `q`
values.  Pigeonholing the `binomial(N-1,m)` choices of `A` proves (1).

On one resulting prefix fiber, let `U` be the common high-degree part and
write `E_A=L_A-U`.  Then `deg E_A<k`, so `-E_A` is a codeword and
`U-(-E_A)=L_A`.  On `D`, equation (3) differs from `P_A(X^c)` by a nonzero
factor.  Thus `L_A` vanishes exactly on the fixed `s` tail points and the
`m` full fibers selected by `A`, giving (2).  Distinct subsets have distinct
root sets, hence distinct locators and codewords.

## Audit boundary

The primary replay performs two complete toy-field enumerations, checks every
root set and received-word agreement, verifies that the constant coefficient is
load-bearing, audits the cyclic support map over all even `4<=N<=64`, and
checks all large-row inequalities with integers.  The separate audit script
independently reconstructs the support map, small coset-product count, exact
official radius/Johnson/list gates, and Lane-L contract text. Neither script
enumerates the official code or constructs an explicit largest prefix bucket; the
large-row theorem is the proved pigeonhole argument.

This packet makes no list upper-bound, MCA/CA, asymptotic-family, or adjacent
safe-row claim.  Repeating the received word gives the same lower bound for
constant common-support interleaving, but Lane L consumes only the ordinary
list statement above.

**Audit verdict: NO ISSUE.**
