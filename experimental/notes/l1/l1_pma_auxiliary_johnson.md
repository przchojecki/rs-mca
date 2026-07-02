# L1 PMA Auxiliary-List And Johnson Regime

## Status

PROVED-COMPILER, citing Lemma 2 (`Sunflower Core-Defect Reduction`) and
Theorem J (`Full-List Johnson Region`) in
`experimental/notes/l1/l1_full_list_quotient_proof_program.md`.

This note packages two roadmap nodes:

- `pma_aux_list_reduction`;
- `pma_johnson_regime`.

It does not prove mixed-petal sunflower amplification.  It isolates the
few-petal part that is already covered by ordinary Reed--Solomon list-decoding
packing.

## Auxiliary Reduction

Use the sunflower notation of Lemma 2.  Fix:

```text
D subset C,        |D| = d,
R_0 subset R,      |R_0| = r.
```

Let `L_D` be the missed-core locator and define the auxiliary petal word on
the union of petals `T = T_1 union ... union T_M` by

```text
U_D(x) = c_i L_D(x)        for x in T_i.
```

For any non-planted listed codeword in this fixed `D,R_0` layer, Lemma 2 gives
a unique polynomial `W_P` with

```text
deg W_P <= d,
W_P(x)=0                  for x in R_0,
W_P(x)=c_i L_D(x)         for x in S_i subset T_i.
```

The list condition gives

```text
sum_i |S_i| >= sigma + d + 1 - r.
```

Therefore the map

```text
P -> W_P
```

injects the fixed `D,R_0` mixed-petal layer into the auxiliary degree-`<=d`
Reed--Solomon list on the petal domain `T`, at agreement

```text
a = sigma + d + 1 - r.
```

Dropping the extra constraints `W_P=0` on `R_0` and exact nonagreement on `D`
only enlarges this auxiliary list, so it is safe for upper bounds.

## Johnson Regime

The auxiliary petal domain has size

```text
|T| = M(sigma+1).
```

The auxiliary code has effective dimension `d+1`.  By Theorem J, if

```text
a^2 > |T| d,
```

then the fixed `D,R_0` auxiliary list has size at most

```text
|T|(|T|-d) / (a^2-|T|d).
```

Equivalently, for `d>0`, the few-petal Johnson-covered region is

```text
M <= floor((a^2-1)/(d(sigma+1))).
```

Thus the mixed-petal amplification problem only starts after this
sub-Johnson boundary.  Below the boundary, the ordinary list-decoding packing
theorem handles the fixed `D,R_0` layer before any sunflower-specific
amplification argument is needed.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_pma_auxiliary_johnson.py \
  --check experimental/data/certificates/l1-pma-auxiliary-johnson/l1_pma_auxiliary_johnson.json
```

The verifier records exact parameter translations, Johnson denominators, the
few-petal threshold table, and a small finite-field toy replay.

