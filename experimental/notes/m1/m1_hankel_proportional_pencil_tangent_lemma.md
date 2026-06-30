# M1 Hankel Proportional-Window Root-Compression Lemma

Status: **PROVED / AUDIT**.

In a fixed exact-agreement bucket of the v9 Hankel atlas, only the syndrome
moments in the visible Hankel window enter:

```text
m = 0,...,t+j-1.
```

If `u_m=c v_m` on that window, then for every row set `R` of size `j+1`,

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
therefore a one-slope residual, not an aperiodic family.

There is one important ledger distinction.  If `u=c v` holds for the full
stored syndrome vector, then `Z=-c` makes the line syndrome zero and the root is
paid by the tangent/common-code-line ledger.  If the proportionality holds only
on the visible window, the exact bucket is still compressed to one slope, but a
tail check is needed before charging that slope to the tangent ledger.

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
minor; checks affine pivot ratios; checks a local-window proportional example
with a nonzero tail obstruction; and cross-checks the pinned `F_17^32`,
`A=426`, `c=5` full proportional packet and subtraction certificate.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json
```

Non-claims: this does not supply actual M3 row root tables, does not bound
non-proportional aperiodic pencils, and does not allow a merely local
proportional window to be charged to the tangent ledger without checking the
tail moments.
