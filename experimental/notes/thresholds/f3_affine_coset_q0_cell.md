# F3 shift-pair control: affine coset pairs and the q0 repeat cell

Status: PROVED / CLASSICAL-INPUT, with replayed arithmetic.

This packet records a small reusable F3/SP lemma from the prize critical DAG:
the h=2 shifted-coset Stepanov bound is stable under affine changes of
coordinate.  Two h=3 repeat-branch payments then become immediate:

- the repeat-boundary line-pencil cell `q(r)=r^2+r+1=0`;
- the exceptional `lambda=1` scale branch.

It is intentionally narrower than the full primitive shift-pair ledger.  It
does not prove the generic h=3 repeat boundary, C36', or the HGE4 aggregate
gate.

## H2 affine-coset input

Let `H <= F_p^*` have order `n`.  Let

```text
L_1(X)=a_1 X+b_1,    L_2(X)=a_2 X+b_2
```

with nonzero slopes.  After the bijective change of variable `Y=L_1(X)`,
write

```text
L_2(X)=alpha Y+beta,    alpha != 0, beta != 0.
```

The h=2 Stepanov rich-coset theorem, with the optimized prize-side
bookkeeping constant, gives under

```text
n^4 < p^3
```

the affine pair bound

```text
#{X : L_1(X) in H, L_2(X) in H} <= 66 n^(2/3).        (AC2)
```

Indeed, `Y=L_1(X)` reduces the count to

```text
#{Y in H : alpha Y + beta in H}.
```

Putting `u=-beta/alpha` and scaling `Y=uZ`, the incidence points satisfy

```text
Z^n = u^(-n),        (Z-1)^n = (alpha u)^(-n).
```

This is the same two-shift Stepanov system as the h=2 rich-coset proof; only
the nonzero right-hand constants change.  The auxiliary polynomial
`Phi(Z,Z^n,(Z-1)^n)`, sparse nonvanishing lemma, and parameter count are
unchanged, so the same constant applies.

The excluded case `beta=0` is a proportional-coset case, not the shifted
intersection used by the repeat-boundary line pencil.

## q0 repeat-boundary cell

In the h=3 repeat-boundary line pencil, the exceptional cell

```text
q(r)=r^2+r+1=0
```

has at most two parameters `r`.  For such an `r`,

```text
-r/(r+1)=r^2,
```

so the line forms are

```text
1+t,    1+rt,    1+r^2 t,    1.
```

Dropping the third nonconstant membership condition leaves two affine
multiplicative-coset conditions:

```text
1+t in H,       1+rt in H.
```

By `(AC2)`, each fixed `r` contributes at most `66 n^(2/3)` points.  Therefore
the whole q0 cell obeys

```text
B_q0 <= 132 n^(2/3).
```

The corresponding repeat-residue payment is

```text
12 n B_q0 <= 1584 n^(5/3).
```

For official F3 rows `n=2^s`, `13 <= s <= 41`, this is strictly below `n^3`.
Thus the q0 cell is a paid exceptional cell; the generic LP4/repeat-boundary
statement may exclude `q(r)=0`.

## lambda=1 scale branch

The same affine input also bounds the exceptional scale branch

```text
{x, omega x, omega^2 x}
```

where `omega` is a primitive cube root and

```text
1+x,    1+omega x,    1+omega^2 x in H.
```

Dropping the third condition and normalizing by `Y=1+x` gives

```text
1+omega x = omega Y + (1-omega),
```

with nonzero slope and nonzero offset.  Hence the number of admissible `x`
values is at most `66 n^(2/3)`, and the number of nonzero scale orbits is at
most

```text
K_1 <= floor(ceil(66 n^(2/3))/3).
```

Combining this with the trivial orbit bound `floor((n-1)/3)`, the h=2 cap
first improves the trivial scale count at `n=2^19`; at the largest official
row `n=2^41` it gives `K_1 <= 3720282297`.

## Replay

```bash
python3 experimental/scripts/verify_f3_affine_coset_q0_cell.py
```

Expected digest:

```text
F3_AFFINE_COSET_Q0_CELL_PASS official_rows=29 sample_rows=4 first_lambda_improvement=2^19
```

The replay script checks exact subgroup samples, the q0 algebra, integer
ceilings for the `n^(2/3)` bounds, and the official-row inequality gates.  It
does not reprove the Stepanov auxiliary-polynomial theorem.
