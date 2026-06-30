# M1 Hankel Proportional-Pencil Tangent Lemma

Status: **PROVED / AUDIT**.

In the v9 Hankel atlas, suppose a finite affine line has syndrome pencil

```text
u + Z v
```

with `u=c v`.  Then for every regular bucket and every row set `R` of size
`j+1`,

```text
det((H(u)+Z H(v))_R) = det(H(v)_R) (Z+c)^(j+1).
```

Thus a nonzero regular minor has the single finite root `Z=-c`.  If the minor
vanishes, proportionality is still not a new aperiodic obstruction: for every
locator or co-support `T`,

```text
A_T = H(u) ell_T = c H(v) ell_T = c B_T.
```

So every affine pivot with `B_T != 0` gives the same slope `Z=-c`, and every
`B_T=0` branch is contained because `A_T=0`.  The whole proportional branch is
therefore tangent/common-code-line.  Once the tangent ledger removes `Z=-c`,
the proportional branch contributes no aperiodic roots.

Certificate:

```text
experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/
  hankel_proportional_pencil_tangent_lemma_certificate.json
```

The verifier

```text
experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py
```

checks three prime-field determinant cases, including a singular rank-one
minor; checks affine pivot ratios; and cross-checks the pinned
`F_17^32`, `A=426`, `c=5` proportional packet and subtraction certificate.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json
```

Non-claims: this does not supply actual M3 row root tables, does not bound
non-proportional aperiodic pencils, and does not replace quotient/tangent
deduplication for arbitrary packets.
