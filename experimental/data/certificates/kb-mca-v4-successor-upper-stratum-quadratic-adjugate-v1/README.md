# KoalaBear successor upper-stratum quadratic-adjugate reduction

This packet treats only the upper reduced-degree stratum at the first
currently open slack:

```text
r = 67,473
|Sigma| = 134,946
e = 67,474
|Sigma| = 2e - 2.
```

The exact source residue space has dimension four. Base span at most two is
paid by the direct cap

```text
4,180,884,949,033,404
```

against the unchanged reserve

```text
270,780,212,960,575,880.
```

Reciprocal dimension two is already owned by the active C5 cell. Every
remaining higher-span survivor has a nonzero quadratic adjugate quotient
which factors into paired primitive degree-one source and reciprocal
syzygies.

Their `X`-direction vectors lower every corresponding row and column product
by one degree, and their paired product by two degrees. The complete
rank-excess scan also proves a route cut: the induced source map can retain
degree `e-1` (372 of 740 examples), and the paired direction product can
vanish. Thus the degree drop is stronger proof input, but is not by itself
an already-paid source-rational map.

The zero product is no longer untyped: it forces an exact partition of the
source into two disjoint degree-`e-1` root blocks. A nonzero paired product
has degree at most `e-2`, so the combined zero set of its two direction
factors has size at most `e-2`.

Both cases are now contained in one stronger selected-locator normal form.
The actual locator is outside the cyclic source plane, and a unit from the
actual translated source plane can be chosen outside the reciprocal cyclic
plane. Their four product representatives satisfy

```text
wC - AB = c Lambda_Sigma,  c != 0,
deg(w,A,B,C) <= (e-2,e-1,e-1,e).
```

The deterministic scan verifies this saturated identity on all `740`
rank-excess rows. The actual locator occurs in both `B` and `C`. The identity
canonically separates the source into its `q`-zero, `v`-zero, and cyclic
bulk strata.

The split-locator refinement now uses actual occupied locators. Occupied
projective span at most two is paid by the same `(p+1)(n-s)` cap above.
Otherwise three independent actual locators have pairwise zero-locator
exchange at least `e-2`. Their degree-one source syzygy gives exactly one of:

```text
full-source exterior spread >= 2e-3 = 134,945
common core + three pair-petals of size >= e-3 = 67,471,
  with at most one private root per locator.
```

The one-root-swap branch is incompatible with a primitive actual reduced
pair. The `F_19`, `e=5` exhaustive control checks all `3,220` independent
actual-locator triples and all `3,920` degree-one relations on the `2,800`
syzygy triples. An explicit `F_29`, `e=5` primitive post-C5 source plane
attains the three-petal bounds exactly: pair-petal sizes `(2,2,2)` and
private-root sizes `(1,1,1)`.

If four independent actual locators survive C5, the four coordinate triples
give a canonical zero-diagonal `4 x 4` matrix of degree-one syzygies. Its
generic rank is exactly two: rank one contradicts the nonzero off-diagonal
entries, while rank three would force the four-dimensional source multiplier
space to be a punctured cubic cyclic space and contradict coprime exact
degree. The `F_13` scan contains six all-four-rank-excess source pairs, and
all six attain generic rank two. A separate primitive `F_29` four-locator
guardrail has triple reciprocal dimensions `(3,2,3,2)`; it disproves
three-locator closure while confirming that active C5 removes that extension.

The resulting dimension-three spread-or-petal and dimension-four
collective-rank owner branches are not paid by this packet. The companion
lower `e=67,473` Segre packet now pays its complete stratum: its intrinsic
`q, Xq` gate forces every descended source quadric to be split. Thus this
upper actual-locator payment alone keeps the row and the slack open.

```bash
python3 experimental/scripts/verify_kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.py --tamper-selftest
```

```text
payload            964197017c160a16d273a39e631b0d4de489a7ecda9b493b492da1a606a3347b
partition digest   7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
additional charge  0
upper paid         false
lower treated      false
```
