# M1 SPI Post-Strip Genericity

## Status

PROVED-COMBINATORIAL.

This note packages the roadmap node `spi_genericity`: after the support-side
periodic locator strata are stripped, the remaining divisor locators have no
nontrivial subgroup stabilizer.  This is the precise combinatorial input used
in the SPI route before any Elekes-Szabo-type incidence theorem can be invoked.

## Statement

Let `H` be a cyclic smooth domain of order `n`, and identify a squarefree
degree-`j` locator divisor of `X^n-1` with its root set

```text
T subset H,      |T| = j.
```

For a subgroup `K_M <= H` of order `M`, define the `M`-periodic stratum

```text
Per_M(D_j) = {T subset H : |T|=j and K_M T = T}.
```

Then:

1. `Per_M(D_j)` is empty unless `M | j`.
2. If `M | gcd(n,j)`, then

```text
|Per_M(D_j)| = binom(n/M, j/M),
```

because each such `T` is exactly a union of `j/M` cosets of `K_M`.
3. For subgroups `K_M,K_N <= H`,

```text
Per_M(D_j) cap Per_N(D_j) = Per_lcm(M,N)(D_j),
```

with the right side interpreted as empty if `lcm(M,N)` does not divide `j`.
4. If

```text
D_j^aper = D_j \ union_{1<M|gcd(n,j)} Per_M(D_j),
```

then every `T in D_j^aper` has trivial stabilizer in `H`.

Equivalently, the post-strip divisor set contains no locator fixed by a
nontrivial domain subgroup.  Thus the subgroup-special fixed loci of `D_j`
are exactly the periodic strata already removed and paid by the quotient
ledger; the residual `D_j^aper` is the correct generic-position object for
the SPI incidence wall.

## Proof

The action of `K_M` partitions `H` into `n/M` disjoint cosets, each of size
`M`.  A subset `T` is fixed by `K_M` if and only if it is a union of these
cosets.  This proves the emptiness and count formula.

The intersection identity follows because invariance under both `K_M` and
`K_N` is the same as invariance under the subgroup they generate.  In a cyclic
group, that generated subgroup has order `lcm(M,N)`.

Finally, if `T` has nontrivial stabilizer `K_M`, then `T` is `M`-periodic and
so lies in the stripped union.  Hence no post-strip locator has a nontrivial
subgroup stabilizer.

## Scope

This note does not prove the SPI incidence bound.  It only proves that the
support-side strip removes exactly the subgroup-fixed exceptional loci that an
incidence theorem must exclude.  GAP-1 and GAP-2 from
`experimental/notes/roadmaps/proof_sketch/s3b_ii_strip_periodic.md` remain
separate pricing and dictionary issues.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_m1_spi_post_strip_genericity.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m1_spi_post_strip_genericity.py \
  --check experimental/data/certificates/m1-spi-post-strip-genericity/m1_spi_post_strip_genericity.json
```
