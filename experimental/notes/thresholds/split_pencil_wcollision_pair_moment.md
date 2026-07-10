# Split-pencil W-collision pair-moment identity

- **Status:** PROVED bookkeeping / INSTRUMENT.  This is not a split-pencil
  anti-concentration bound and does not close `conj:BC`.
- **Track:** `(split-pencil census)` / XR lane, exact second-moment ledger.
- **Verifier:** `python3 experimental/scripts/verify_split_pencil_wcollision_pair_moment.py`

## Statement

Fix a received pair `(u,v)` over a finite base field, with domain `D` and
degree `< k` codewords.  For each slope `z`, put `U_z = u + z v`.  A live ray
is a pair `(z,c)` with `c` a degree `< k` codeword and agreement support

```text
S(z,c) = {x in D : U_z(x) = c(x)}
```

of size at least `A`.  For a `k`-set `W`, let

```text
mult(W) = #{z : the interpolant of U_z on W is a live ray}.
```

Then the W-collision pair moment has the exact double-count

```text
sum_{|W|=k} binom(mult(W), 2)
  = sum_{cross-slope ray pairs {(z,c),(z',c')}} binom(|S(z,c) cap S(z',c')|, k).
```

Moreover every cross-slope pair has a codeword-pair fiber.  With

```text
g = (c - c')/(z - z'),      f = c - z g,
```

the support intersection is exactly

```text
JointAgr(f,g) = {x in D : u(x)=f(x), v(x)=g(x)}.
```

Regrouping by `(f,g)` gives

```text
sum_{cross pairs} binom(J, k)
  = sum_{(f,g)} binom(L(f,g), 2) * binom(J(f,g), k),
```

where `J(f,g)=|JointAgr(f,g)|` and `L(f,g)` is the number of live slopes of the
shifted pair `(u-f, v-g)`.

Finally, for each `W`, if `(P_W,Q_W)` interpolates `(u,v)` on `W`, then

```text
mult(W) = L(P_W,Q_W).
```

Thus W-collisions are not a raw extra bucket.  They are exactly a second moment
of pencil live counts.  This is the split-pencil/XR analogue of the exact
second-moment ledger: the residual problem is the anti-concentration of these
live counts after tangent, quotient, near-pencil, dihedral, and extension
strips have been applied.

## Why this matters

The critical distinction is slope count versus moment.  A large W-collision
moment can be caused by a removable near-pencil fiber and need not by itself
violate the `16 n^3` slope-count target used by the XR/BC consumer.  The
identity is still useful because it tells the split-pencil program exactly how
to aggregate collision mass:

- raw `W` collision cores regroup by codeword-pair fibers;
- the fiber factor is `binom(L(f,g),2) * binom(J(f,g),k)`;
- at the `t=2` boundary, the per-core multiplicity is the pencil live-count
  second moment `sum_W binom(L(P_W,Q_W),2)`;
- planted or near-pencil mass is visible as a single large fiber and belongs
  to the strips, not to the residual anti-concentration claim.

## Verification

The verifier is deliberately small and stdlib-only.  It works over `F_17` with
`n=8`, `k=4`, `A=6`, and checks:

- a random received pair with a small nonzero W-collision moment;
- a planted-pencil pair where all slopes are live, demonstrating the removable
  high-moment fiber.

For each case it independently enumerates rays, scans all `k`-sets, verifies
the pair-moment identity, checks the pointwise `(f,g)` support equality,
regroups by fibers with independently recomputed `L(f,g)`, and checks
`mult(W)=L(P_W,Q_W)` for every `W`.

## Non-claims

- No upper bound on the split-pencil residual.
- No proof of `prob:capg-split-pencil-B`, `prob:capfp-R1`, or `conj:BC`.
- No promotion of a support-pair moment to a closed slope-count ledger.
- No claim that near-pencil/planted mass is residual; the planted verifier row
  is included precisely to show why strips are load-bearing.
