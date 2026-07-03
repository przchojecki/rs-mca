# M1 A407/A408 residual-design threshold v1

Status: `PROVED_A407_A408_EXACT_AND_A407_PUBLIC_GATE`.

This note packages the part of the A409 residual-design sweep that is still
fully proved and reviewable after the A406/RNC route was rejected.  The result is
narrow: it proves exact support-wise finite-slope numerators at `A=408` and
`A=407`, then specializes `A=407` to an exact-budget prime field to give a new
public adjacent threshold row.

It does **not** claim `A=406` exactness and does **not** claim M1 closure.

## Proof dependencies

This packet uses four standard RS/MDS support-wise reductions.  They are listed
explicitly here so reviewers can audit or replace them with exact repo lemma
references.

1. **Exact-support reduction.**  For `A >= k+1`, after contained/common-code-line
   branches are separated, a bad support-wise noncontained finite slope may be
   represented by an exact `A`-subset witness.  The usual proof shrinks a larger
   witness until either an exact `A`-subset remains noncontained or overlapping
   exact subsets glue by RS uniqueness into a contained/common-code-line branch.
2. **Per-support uniqueness.**  Two distinct noncontained finite slopes cannot
   use the same exact support.  Subtracting the two support equations would make
   `g|S` an RS word; then `f|S` is also an RS word, contradicting noncontainment.
3. **Moving-root tangent lower floor.**  For `k+1 <= A <= n`, a common zero core
   of size `A-1` plus `n-A+1` moving coordinates gives
   `LD_sw(RS[F,D,k],A) >= n-A+1` whenever the field has enough distinct finite
   slopes.
4. **RS uniqueness on `k` coordinates.**  A degree-`<k` RS codeword is determined
   by its values on any `k` domain points.  This is used for compact triples,
   pair linearization, and the common-code-line paid branch.

## Definitions

Let

```text
C = RS[F,D,256],     |D| = n = 512,
r = n-k = 256,       A = n-j.
```

For a bad finite slope `z`, choose one exact support-wise noncontained witness

```text
S_z subset D, |S_z| = A,
X_z = D \ S_z, |X_z| = j.
```

This uses the exact-support reduction listed above.

Per-support uniqueness is used throughout: two distinct noncontained slopes
cannot use the same exact support.  Otherwise subtracting the two support
equations makes `g|S` an RS word, and then `f|S` is also an RS word, contradicting
support-wise noncontainment.

The common-code-line paid threshold is

```text
tau = n + k - A = k + j.
```

If a common code-line core has size `c >= tau`, then every exact support meets it
in at least `k` points, the residual codeword vanishes identically, and the
standard incidence bound gives

```text
#bad slopes <= floor((n-c)/max(1,A-c)) <= j+1.
```

The moving-root tangent construction gives the matching lower floor `j+1`.
Thus it remains to bound the no-paid residual family by at most `j+1`.

## Pair and triple residual design

For two complements,

```text
|S_i cap S_l| = n - |X_i union X_l| = n - 2j + |X_i cap X_l|.
```

A pair overlap reaches the paid common-code-line threshold exactly when

```text
|X_i cap X_l| >= 3j-r.
```

So, in the no-paid branch,

```text
|X_i cap X_l| <= 3j-r-1.
```

For three complements, write

```text
delta_3(X_1,X_2,X_3) = 3j - |X_1 union X_2 union X_3|.
```

If a triple is compact, meaning `|X_1 union X_2 union X_3| <= r`, then the three
supports share at least `k` coordinates, so the pair-linearized code-lines agree
by RS uniqueness.  Let `T` be the number of coordinates lying in at least two of
the three complements.  The glued core has size `n-T`, so if

```text
T <= r-j,
```

then the common-code-line paid exit applies.  Therefore every compact no-paid
triple belongs to an explicit saturated Venn-type list: it has pair intersections
bounded by the pair cap, union at most `r`, and `T >= r-j+1`.

The verifier enumerates those Venn types exactly.

## High-neighbor graph

For each row, define a graph on residual complements by marking an edge if its
pair intersection is at least the minimum pair intersection appearing in any
compact non-paid saturated triple.

For `A=408`:

```text
j=104, pair_trigger=56, pair_cap=55,
high_edge_threshold=49, q_max=6, sat_delta_cap=159.
```

For `A=407`:

```text
j=105, pair_trigger=59, pair_cap=58,
high_edge_threshold=47, q_max=11, sat_delta_cap=163.
```

Two high-neighbor edges from a fixed complement force a compact triple.  In a
compact saturated triple the two traces inside the fixed complement meet in at
most `q_max` points.  Hence three high neighbors would require at least

```text
3*49 - 3*6  = 129 > 104      for A=408,
3*47 - 3*11 = 108 > 105      for A=407,
```

points inside one `j`-set, impossible.  Thus the high-neighbor graph has maximum
degree at most two.  Its triangles are therefore disjoint, and there are at most
`floor(m/3)` saturated triples in a residual family of size `m`.

## Third-moment inequality

Let `d_x` be the number of complements containing coordinate `x`.  The exact
third-deficit identity is

```text
sum_{triples} delta_3
  = sum_x [ binom(d_x,2)(m-d_x) + 2 binom(d_x,3) ].
```

Write the bracketed kernel as

```text
phi_m(d) = binom(d,2)(m-d) + 2 binom(d,3).
```

The verifier records the discrete-convexity identity

```text
phi_m(d+2) - 2 phi_m(d+1) + phi_m(d) = m-d-2 >= 0
```

for `0 <= d <= m-2`.  Therefore the usual exchange argument applies: among all
integer coordinate degrees with fixed total degree `sum_x d_x = jm`, the minimum
of `sum_x phi_m(d_x)` is attained by balanced degrees `q` and `q+1`, where
`jm = 512q + s`.  The verifier emits this balanced-minimizer certificate at the
first forbidden `m` and the preceding `m`, then proves positivity for all later
`m` by the `lcm(512,3)=1536` residue-class finite-difference certificate.

The upper bound is

```text
pair_cap * binom(m,3)
  + (sat_delta_cap - pair_cap) * floor(m/3).
```

The certified thresholds are:

| A | j | target `j+1` | no-paid residual bound | first forbidden `m` |
|---:|---:|---:|---:|---:|
| 408 | 104 | 105 | 50 | 51 |
| 407 | 105 | 106 | 93 | 94 |

Both no-paid residual bounds are below `j+1`; the paid branch is also bounded by
`j+1`; and the tangent lower witness gives `j+1`.  Hence

```text
LD_sw(RS[F,D,256],408)=105,
LD_sw(RS[F,D,256],407)=106.
```

## Public exact-budget row

Take

```text
p = 27168*2^120 + 1
  = 36112466189484594435050630213696401440769.
```

The verifier proves primality by Lucas witness `11` with

```text
p-1 = 2^125 * 3 * 283.
```

It also checks

```text
p == 1 mod 512,
floor((p-1)/2^128)=106,
106*2^128 < p < 107*2^128.
```

Let `H` be the order-512 subgroup of `F_p^*`.  For
`C = RS[F_p,H,256]`:

```text
A=407: LD_sw(C,407)=106, safe at delta=105/512.
A=406: LD_sw(C,406)>=107, unsafe at delta=53/256.
```

This is a genuine adjacent closed-grid finite-slope support-wise MCA threshold
row for this new exact-budget prime.  It improves the currently displayed
prime-field safe agreement from `A=426` to `A=407` without relying on any
RNC/Fano-line closure.

## First failure below the row

The same method fails immediately at `A=406`:

```text
A=406, j=106
pair_trigger=62
pair_cap=61
compact_T_paid_cap=150
status=FAIL_HIGH_NEIGHBOR_DEGREE_BOUND
```

The failure is structural: compact non-exiting triples have lower high-edge
threshold and larger triple overlap, so inclusion-exclusion no longer forces the
high-neighbor graph to have degree at most two.  This note does not try to repair
that obstruction.

## Files

```text
experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md
experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py
experimental/scripts/apply_m1_a407_a408_site_entries_v1.py
experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/
experimental/notes/certificate_scanner/outputs/m1_a407_a408_residual_design_threshold_v1.report.md
site/data/frontier_prime_a406_a407_adjacent_gate.entry.json
site/data/updates_m1_a407_a408_residual_design_threshold.entry.json
experimental/agents-log.md
```

## Validation

```bash
python3 -m py_compile experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py
python3 -m py_compile experimental/scripts/apply_m1_a407_a408_site_entries_v1.py
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --check
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --json
python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/m1_a407_a408_residual_design_threshold_v1.json
python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/tangent_witness_A408_A407_A406_v1.json
python3 -m json.tool site/data/frontier_prime_a406_a407_adjacent_gate.entry.json
python3 -m json.tool site/data/updates_m1_a407_a408_residual_design_threshold.entry.json
git diff --check
```

## Non-claims

- Finite-slope support-wise MCA / `LD_sw` only.
- Not ordinary list decoding.
- Not interleaved-list safety.
- Not protocol soundness or query accounting.
- Not an exact `A=406` value.
- Not a full M1 closure.
- Does not use the false global RNC Fano-line classification.
