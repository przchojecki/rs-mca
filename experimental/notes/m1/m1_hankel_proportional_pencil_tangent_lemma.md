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

The same classification is also wired into the regular-minor extractor.  The
toy packet

```text
experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/
  f17_n10_k4_a8_scalar5_tangent_residual_packet.json
```

has rank-one `H(v)`, so every maximal regular minor vanishes.  Instead of
leaving the singular bucket as `unknown`, the extractor detects the visible
scalar from ordinary syndrome-pencil data and records `residual_label=tangent`
together with a `proportional_window_tangent` audit: the only possible slope is
`12=-5`, and the supplied syndrome is fully proportional, so the
tangent/common-code-line ledger may pay it.

The packet checker replays this audit from the referenced extractor input: it
checks the input SHA, recomputes the visible scalar `c`, recomputes the slope
`-c`, and independently decides whether proportionality holds on the full
stored syndrome vector.  The negative fixture

```text
experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/
  invalid_bad_proportional_replay_packet.json
```

keeps the same input but claims scalar `6`; it must fail because replay gives
scalar `5` and slope `12`.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_proportional_pencil_tangent_lemma.py \
  --check experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/hankel_proportional_pencil_tangent_lemma_certificate.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_scalar5_rank_pivot_tangent_residual_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/f17_n10_k4_a8_scalar5_tangent_residual_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-proportional-residual-toy/invalid_bad_proportional_replay_packet.json
```

Non-claims: this does not supply actual M3 row root tables, does not bound
non-proportional aperiodic pencils, and does not allow a merely local
proportional window to be charged to the tangent ledger without checking the
tail moments.
