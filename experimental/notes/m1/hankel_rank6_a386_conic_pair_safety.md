# Hankel Rank-6 A386 Conic-Pair Safety

Status: PROVED / AUDIT.

This note records a reusable projective-safety criterion for the separated
rank-6 boundary at

```text
A = 386.
```

It is not an unconditional closure of all `A=386` weights.  It isolates the
generic case where two direction-consistency conics have no common component,
and names the common-component case as the residual.

At `A=386`, the low-degree transfer gives

```text
h = |X union Y|-t = 3,
```

so the auxiliary polynomial `Q` lives in a projective plane:

```text
deg Q < 3,        [Q] in P^2.
```

For each `Q`, the base equations determine `L_Q`.  Choose a direction node
`y0` and two comparison nodes `y1,y2`.  The equality of finite-slope ratios
with `y0` gives two conics in `P^2`:

```text
F_i(Q) =
  Omega_{y_i} Q(y_i) b_{y0} L_Q(y0)
  - Omega_{y0} Q(y0) b_{y_i} L_Q(y_i),
  i=1,2.
```

Every finite root satisfies all direction consistency equations, hence lies in

```text
F_1(Q) = F_2(Q) = 0.
```

If `F_1` and `F_2` have no common component over the algebraic closure, their
intersection in `P^2` has length at most `4` by Bezout.  Therefore there are
at most four `Q`-classes, hence at most four finite ambient roots.  The
null-polynomial split-locator gate can only remove roots, so there are at most
four finite support-wise split-locator roots.

The endpoint-uniform theorem contributes one projective endpoint `[0:1]`.
Thus, under this conic-pair criterion,

```text
finite split-locator roots <= 4,
endpoint contribution       = 1,
total projective contribution <= 5 <= 6.
```

If every useful pair of comparison conics has a common component, that
component is the named `A=386` conic-component residual.  It must be handled by
component classification, exact root tables, or the split-locator divisor gate.
The companion note

```text
experimental/notes/m1/hankel_rank6_a386_component_cut_safety.md
```

narrows this residual: if every irreducible component of such a common
component is cut by some direction-consistency conic, the branch is still
projective-safe with total `<=5<=6`.  The residual after that companion is an
irreducible component contained in all direction-consistency conics.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_conic_pair_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json
```

Nonclaims:

```text
no proof that all A=386 weights satisfy the criterion;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
