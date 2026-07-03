# C-3 Pullback-Strip Packet

- **Task:** C-3.
- **DAG nodes:** `Q3R.4`, `QL.5`, `E22`, `pma_pullback_lists`,
  `pma_wide_residual`.
- **Status:** PACKET VERIFIED / pullback stratum charged to profile budget.
- **Verifier:** `experimental/scripts/verify_c3_pullback_strip_packet.py`.
- **Artifact:** `experimental/data/certificates/c3-pullback-strip-packet/c3_pullback_strip_packet.json`.

This packet packages the pullback-strip repair requested in Q3R.4 and merges
the E15 challenger information into the list-side QL.5/E22 bookkeeping.

It does three things:

1. Replays the `pma_pullback_lists` construction in small finite fields.
2. Restates the PMA wide residual after quotient pullbacks and low-defect
   challengers are removed.
3. Tests whether the recorded E15 challenger class is the same as the
   quotient-pullback family.

## Pullback Family

Let the petal domain be a union of quotient fibers for the map

```text
x -> x^ell.
```

Choose quotient values `alpha_i`, set

```text
T_i = {x : x^ell = alpha_i},
L_D(X) = H(X^ell),
U*(x) = alpha_i H(alpha_i)  for x in T_i.
```

For each subset `S` of quotient fibers with `|S| = m+1`, define

```text
G_S(Y) = Y H(Y) - prod_{i in S}(Y - alpha_i),
W_S(X) = G_S(X^ell).
```

When `H` is monic of degree `m`, the leading terms in `G_S` cancel, so
`deg G_S <= m` and `deg W_S <= m ell`.  The word `W_S` agrees with `U*`
exactly on the fibers indexed by `S`, hence on

```text
(m+1) ell = d + ell
```

points, where `d = m ell`.  The family has

```text
binom(M, m+1)
```

distinct members on `M` quotient fibers.

The verifier checks this over `F_31` in three cases:

```text
ell=2, m=2, M=6: binom(6,3)=20
ell=3, m=2, M=6: binom(6,3)=20
ell=5, m=2, M=5: binom(5,3)=10
```

All three are sub-Johnson:

```text
((m+1) ell)^2 < (M ell)(m ell)
```

equivalently `(m+1)^2 < M m`.

## Profile Charge

The pullback family is indexed by quotient-fiber subsets.  Its count is
therefore quotient-profile mass, not primitive residual mass.  The strip
bookkeeping should remove this stratum before invoking any correlated-target
or descent argument for the wide PMA residual.

The corrected split is:

```text
L(D) = L_quotient_pullback union L_lowdef_fixed_excess union L_primitive.
```

The charged pieces are:

```text
L_quotient_pullback      -> dyadic / quotient-profile budget
L_lowdef_fixed_excess    -> fixed-excess and E15 challenger column
```

The remaining target is the primitive residual:

```text
non-pullback, non-low-defect wide sub-Johnson auxiliary lists are polynomial.
```

This is a restatement, not a proof of the primitive residual bound.

## E15 Challenger Test

The verifier consumes the stored E15 certificate rather than rerunning the
full E15 search.  The consumed exact `n=16` non-planted counts are:

```text
mixed_petal  323
full_petal    13
total        336
```

The quotient-pullback family above requires petals to be quotient fibers of a
power-map quotient on the cyclic subgroup.  None of the 12 exact E15
non-planted cells has that geometry:

```text
quotient-fiber-compatible E15 cells = 0.
```

Thus the C-3 verdict is:

```text
E15 is not an instance of pma_pullback_lists.
```

The full-petal E15 examples are whole-petal at the agreement-pattern level,
but their recorded layouts are not quotient-fiber layouts.  They should be
priced in the low-defect/fixed-excess challenger column, not charged to the
quotient-pullback profile cell.

## Replay

```bash
python3 experimental/scripts/verify_c3_pullback_strip_packet.py --write
python3 experimental/scripts/verify_c3_pullback_strip_packet.py --check
python3 -m py_compile experimental/scripts/verify_c3_pullback_strip_packet.py
python3 -m json.tool experimental/data/certificates/c3-pullback-strip-packet/c3_pullback_strip_packet.json >/dev/null
```

The packet also checks the source certificate schemas and hashes for:

```text
experimental/data/certificates/l1-pma-auxiliary-johnson/l1_pma_auxiliary_johnson.json
experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json
```

## Nonclaims

This packet does not rerun the full E15 exhaustive/structured search, does not
prove the primitive residual polynomial bound, does not update the DAG JSON or
SVG on `main`, and does not price the final list crossing numerically.
