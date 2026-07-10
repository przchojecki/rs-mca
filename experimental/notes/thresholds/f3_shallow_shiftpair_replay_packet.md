# F3 shallow shift-pair replay packet

Status: `PROVED` local algebra / `AUDIT` replay packet.

This packet vendors two shallow pieces from the prize critical DAG into the
upstream shift-pair/direct-column interface:

- the `h=3` characteristic-zero classification of equal-prefix 3-trades;
- the `h=2` additive-energy reduction and in-house Stepanov reconstruction
  for multiplicative subgroups.

It is meant as support material for the primitive shift-pair and exact
second-moment program.  It does not prove the full primitive shift-pair
control input, does not close `u1_x4_direct_column_budget`, and does not pay
the `h >= 4` aggregate or finite per-row `h=3` accident problem.

## h=3 Char-Zero Classification

Let `X={x1,x2,x3}` and `Y={y1,y2,y3}` be 3-element subsets of roots of
unity in characteristic zero.  If

```text
x1 + x2 + x3 = y1 + y2 + y3
x1*x2 + x1*x3 + x2*x3 = y1*y2 + y1*y3 + y2*y3
```

and `X != Y`, then both triples have zero sum and both are translates of
the order-three subgroup:

```text
X = a * {1, omega, omega^2},   Y = b * {1, omega, omega^2}.
```

In a cyclic domain `mu_n`, such disjoint pairs occur exactly when `3 | n`,
with unordered count `binom(n/3, 2)`.

The proof is a one-line unit-circle identity.  For a triple `X`, write
`s_X = x1+x2+x3` and `p_X=x1*x2*x3`.  Since all roots lie on the unit
circle,

```text
e2_X = p_X * conjugate(s_X).
```

If `s_X=s_Y=s` and `e2_X=e2_Y`, then `(p_X-p_Y)conjugate(s)=0`.  When
`s != 0`, the two monic cubics have identical elementary coefficients and
the same root multiset, contrary to `X != Y`.  Thus `s=0`, and a zero-sum
triple of unit complex numbers is a rotated `mu_3` coset.

The replay script checks exact cyclotomic rows and the banked finite-field
norm-gate shapes without floating point.

## h=2 Energy Reconstruction

For a multiplicative subgroup `H <= F_p^*` of odd characteristic, let

```text
E(H) = #{(a,b,c,d) in H^4 : a+b=c+d}.
```

Let `T_2` be the unordered disjoint-pair count for the `h=2` F3 stratum,
and let

```text
M_2 = #{(a,{b,c}) : a,b,c in H, b != c, 2a=b+c}.
```

The exact decomposition is

```text
E(H) = 8*T_2 + 4*M_2 + 2*n^2 - n,
```

so `T_2 <= E(H)/8`.  The correction term `4*M_2` is essential: omitting
midpoint collisions gives a false identity already in small rows.

The in-house reconstruction proves an explicit conservative energy bound

```text
E(H) <= 83851 * n^(5/2)
```

from a level-set reduction, a dyadic HBK-style compiler, and a rich-coset
Stepanov lemma with constant `K=129`.  This is weaker than the external
Cochrane-Pinner constant but removes the import for the asymptotic energy
shape.  It closes `T_2 < n^3` asymptotically from this route alone; finite
midrange closure below that threshold remains a separate certificate task.

## Replay

```bash
python3 experimental/scripts/verify_f3_h3_char0_classification.py
python3 experimental/scripts/verify_f3_h2_energy_replay.py
python3 experimental/scripts/verify_f3_h2_levelset_replay.py
python3 experimental/scripts/verify_f3_h2_hbk_conditional_compiler.py
python3 experimental/scripts/verify_f3_h2_rich_coset_stepanov.py
```

Expected digests:

```text
CHAR0_CLASSIFICATION_PASS
H2_ENERGY_REPLAY_PASS
H2_LEVEL_SET_REPLAY_PASS
H2_HBK_CONDITIONAL_COMPILER_PASS
H2_RICH_COSET_STEPANOV_PASS
```

## Nonclaims

- No claim is made for full `h=3` finite-row accident control.
- No claim is made for the `h >= 4` aggregate.
- The `h=2` conservative constant does not by itself certify every finite
  midrange row.
- This packet is shift-pair/direct-column support material, not a promoted
  main-paper theorem.
