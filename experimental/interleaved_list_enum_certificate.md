# Tiny Interleaved-List Enumeration Certificate

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies `experimental/interleaved_list_enum.py`, a tiny
  finite-field enumerator for comparing direct interleaved list counts with the
  trivial product bound.

## Claim Audited

For a prime field `F_p`, a finite domain `D`, dimension `k`, received rows
`U_1,...,U_mu`, and agreement threshold `a`, the script enumerates every
degree-`<k` polynomial over `F_p`.  For each row it records the agreement
support mask

```text
{x in D : P(x) = U_i(x)}.
```

The base list count for row `i` is the number of masks of size at least `a`.
The direct interleaved count is the number of polynomial tuples
`(P_1,...,P_mu)` whose support-mask intersection has size at least `a`.
This exactly matches the column-wise interleaved agreement condition for the
tiny instances enumerated by the script.

The script also reports the raw feasible `a`-subset fiber counts:

```text
sum_A m(A) binom(|A|,a)
```

for each row support-mask histogram, and

```text
sum_{A_1,...,A_mu}
  m_1(A_1)...m_mu(A_mu) binom(|A_1 cap ... cap A_mu|,a)
```

for the simultaneous raw fiber.  For Reed-Solomon instances with `a >= k`,
these are the exact raw-to-full support decompositions from
`experimental/l2_interleaved_support_bridge.md`.

For every run the script also emits the common-intersection histogram

```text
C_r = |{(A_1,...,A_mu): |A_1 cap ... cap A_mu| = r}|,
```

with multiplicity from the row support-mask histograms.  The direct
interleaved count is `sum_{r>=a} C_r`, and the raw simultaneous fiber is
`sum_{r>=a} C_r binom(r,a)`.  For two rows, the script additionally emits the
two max common-intersection codegrees, which certify the bound

```text
|Lambda(Int(C,2),1-a/n,U)|
  <= min(|P| Gamma_{>=a}(P,Q), |Q| Gamma_{>=a}(Q,P)).
```

The script also emits a near-exact Johnson-neighborhood certificate when
`a >= k`.  If all listed row supports have size between `a` and `a+c`, then
for a fixed support `A` of size `s` the number of possible supports `B` with
`|B| <= a+c` and `|A cap B| >= a` is

```text
J_{n,a,c}(s)
  = sum_{i=0}^{s-a} binom(s,i)
      sum_{j=0}^{c-(s-a)+i} binom(n-s,j).
```

Fixing one row support forces every other row support into this neighborhood,
so the script reports

```text
min_i sum_{A in P_i} J_{n,a,c}(|A|)^(mu-1).
```

This is a proved upper bound on the direct interleaved count for the
enumerated Reed-Solomon instance, and it becomes the exact diagonal bound when
`c=0`.  The crude estimate `J_{n,a,c}(s) <= (c+1)^2 n^(2c)` shows that fixed
support excess gives only a polynomial completion factor after one row support
is fixed.

The layered Johnson certificate sharpens this further using the actual
support-size histograms

```text
B_i(s) = |{A in P_i : |A|=s}|.
```

For a fixed anchor support of size `r`, the number of all `s`-subsets that
intersect it in at least `a` positions is

```text
K_{n,a}(r,s)
  = sum_{u=a}^{min(r,s)} binom(r,u) binom(n-r,s-u).
```

The script therefore also reports

```text
min_i sum_r B_i(r)
  prod_{j != i} sum_s min(B_j(s), K_{n,a}(r,s)).
```

This bound detects when high-excess support layers are sparse.  For example,
a single full-domain support has large excess but layer count one, so it does
not force product growth.

The trivial product bound is the product of the base list counts.  Comparing
the direct count with that product gives a finite sanity check for the
interleaved-list overcharge discussed in the L2/Paper C ledger.

The script also emits a proved random-received-word baseline.  If the received
rows are sampled independently and uniformly, then

```text
E |Lambda(Int(C,mu),1-a/n,U)|
 =
 p^(mu k) Pr[Bin(n,p^(-mu)) >= a].
```

For comparison it prints the one-row expectation

```text
p^k Pr[Bin(n,p^(-1)) >= a]
```

and the expected product bound for independent rows.  These exact rational
values are not claims about the adversarial row instance being enumerated; they
are a baseline showing how much support entropy is saved when common columns,
rather than independent row supports, drive the interleaved list.

## Reproducible Check

The following enumerates two high-degree received rows on the order-8 subgroup
`<2> <= F_17^*`, with dimension `k=3` and common agreement threshold `4`:

```bash
python3 experimental/interleaved_list_enum.py \
  --p 17 \
  --subgroup-generator 2 \
  --subgroup-order 8 \
  --k 3 \
  --agreement 4 \
  --row-polys '0,0,0,0,1;0,0,0,0,0,1'
```

The JSON output mode is intended for later aggregation into certificate
experiments:

```bash
python3 experimental/interleaved_list_enum.py \
  --p 17 \
  --subgroup-generator 2 \
  --subgroup-order 8 \
  --k 3 \
  --agreement 4 \
  --row-polys '0,0,0,0,1;0,0,0,0,0,1' \
  --format json
```

## Limits

The script is deliberately exhaustive and therefore only for tiny parameters.
It does not prove an asymptotic interleaved-list theorem, and it does not
replace the product or GGR-style bounds in Paper C.  Its purpose is to produce
small exact data for guessing sharper finite-length interleaving behavior.
