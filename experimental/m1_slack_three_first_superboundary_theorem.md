# M1 Slack-Three First-Superboundary Theorem

**Status:** PROVED / CONDITIONAL / AUDIT.

This note extracts the theorem-level content of the slack-three
first-superboundary ledger in `m1_support_occupancy_scan.py`. It is the next
fixed low-slack packet template after the slack-two depth-two window theorem.

## Exact Shape Reduction

Let `p>3` be prime and let `D subset F_p^*` be a multiplicative subgroup. In
the slack-three first-superboundary layer, residual packets have size four and
satisfy the first two zero-prefix equations. After normalizing one point to
`1`, every such packet is

```text
x {1,u,v,w},        w=-1-u-v,
```

with `(u,v)` in the conic shape set

```text
C_3(D) = { (u,v) in D^2 :
           w=-1-u-v in D,
           1,u,v,w distinct,
           u^2+v^2+uv+u+v+1=0 }.
```

The map `(x,u,v) -> x{1,u,v,w}` is twenty-four-to-one. If the quotient
decomposition of `D` has `N` fibers of size `m` and the exact support size is
`s=Lm+4`, then the lifted slope multiset is

```text
M_3(z) = (1/24) sum_{(u,v) in C_3(D)}
         binom(N-tau(u,v), L) * #{x in D : x^3 beta(u,v)=z},
beta(u,v)=-(1+uvw).
```

Thus the nonzero slope image is a union of cube cosets `beta(u,v)D^3`, with
the exact quotient-lift weight carried only by `tau(u,v)`.

## Split-Cubic Compression

The two-variable conic ledger has a one-variable compression. For

```text
G_beta(Y)=Y^3+Y^2+Y+beta+1,
```

a value `beta` is admissible exactly when `G_beta` has three distinct roots in
`D \ {1}`. Each admissible `beta` gives six ordered pairs in `C_3(D)`. Hence

```text
|C_3(D)| = 6 * #{ beta : r_D(beta)=3 },
r_D(beta)=#{ y in D \ {1} : y^3+y^2+y+beta+1=0 }.
```

All abstract cube-coset coverage questions can therefore be audited by one pass
through `D \ {1}`, grouping the values

```text
beta(y)=-(y^3+y^2+y+1).
```

The full conic enumeration remains necessary only for exact-support
quotient-lift weights.

## Full-Domain Consequences

For `D=F_p^*`, the ordered conic shape count is

```text
|C_3(F_p^*)| = p - 9 - 4 chi(-3) - 6 chi(-2).
```

The zero value `beta=0` occurs exactly when `chi(-1)=1`. If `p==2 mod 3`, the
cube map is surjective, so every nonzero admissible `beta` gives every nonzero
slope. Consequently the full-domain slack-three first-superboundary image is

```text
F_p        if p==5 mod 12 and p>=29,
F_p^*      if p==11 mod 12 and p>=23.
```

The small exceptions are explicit: `p=5` and `p=17` contribute only zero, while
`p=11` has no admissible full-domain slack-three shape.

If `p==1 mod 3`, a cubic-character sum on the smooth projective conic gives
all nonzero cube cosets for `p>=271`. The finite split-cubic audit improves
this threshold: every prime `p==1 mod 3` with `p>=103` hits all three nonzero
cube cosets. Thus the full-domain image contains every nonzero slope for every
prime `p>=103` with `p==1 mod 3`, and contains zero exactly when
`chi(-1)=1`.

The finite audit is reproduced by

```bash
python3 experimental/verify_m1_slack_three_full_domain_audit.py
```

## Proper-Subgroup Certificates

For a proper subgroup `D` of index `e=(p-1)/|D|`, the companion genus-zero
Kummer lemma gives the conic-count bound

```text
|C_3(D)| <= ceil((p+1 + 6(e^3-1)sqrt(p))/e^3).
```

This implies the field-capped high-index slope bound

```text
|Bad_{T=3, |P|=4}|
  <= min(p, 1 + ceil(|C_3(D)|/24) * |D|/gcd(3,|D|)).
```

There is also a complementary low-index saturation certificate. Put
`g=gcd(3,|D|)`, `H=D^3`, `h=[F_p^*:H]=eg`, and `M=e^3h`. Every nonzero `H`
coset contains at least

```text
ceil((p - 9 - 4 chi(-3) - (12 sqrt(p)+12)M)/M)
```

admissible ordered slack-three shape parameters, whenever the numerator is
positive. Thus the abstract first-superboundary slack-three catalog hits every
nonzero `D^3` slope coset in that range.

The divisor-support and non-power checks behind the constants `6` and `12` are
isolated in
`experimental/m1_slack_three_genus_zero_kummer_lemma.md`. The finite audit is
reproduced by

```bash
python3 experimental/verify_m1_slack_three_genus_zero_kummer_lemma.py
```

For fixed `M`, let `P_M=(s_M-1)^2+1`, where `s_M` is the least positive
integer with

```text
(s_M-1)^2 + 1 - 13 > (12 s_M + 12) M.
```

Then the low-index certificate fires for every prime `p>=P_M` with that
denominator `M`. In the quadratic-residue case `D=(F_p^*)^2`, `p==5 mod 6`,
one has `M=16` and `P_M=38026`. The finite split-cubic audit below `38026`
improves the practical threshold: every such prime `p>=1049` hits both
nonzero `D^3` cosets, using the genus-zero Kummer lemma in the range
`p>=38026`.

The proper-subgroup audits are reproduced by

```bash
python3 experimental/verify_m1_slack_three_cube_coset_coverage.py
python3 experimental/verify_m1_slack_three_qr_index_two_audit.py
```

## Contribution to M1

This theorem gives the next fixed low-slack residue-packet template after the
slack-two depth-two window theorem. It shows that the slack-three
first-superboundary layer is not a raw support-enumeration problem: it reduces
to a conic shape set, a split-cubic beta ledger, and cube-coset coverage. This
is evidence for the roadmap's fixed-template step toward M1: low-slack
residue-line packing can be decomposed into explicit finite templates before
the genuinely aperiodic packing theorem is attacked.
