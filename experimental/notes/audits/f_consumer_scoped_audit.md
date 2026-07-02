# Conjecture F Consumer-Scope Audit

## Status

AUDIT.

This note records the A0/QF.9 consumer-scope audit requested by the roadmap
lane.  The question is whether every current consumption of Conjecture F lies
in one of two scoped families:

```text
(a) coordinate-slice / prefix-fiber flats;
(b) Hankel-pencil kernel flats.
```

If yes, the broad version of Conjecture F could be demoted and replaced by
scoped statements.  The current repo text supports a more conservative answer:

```text
NO, not globally.
```

The coordinate and Hankel-kernel consumers are real, but the list-side
`ImgFib` sunflower residual is an escaping consumer.

## Audit Table

| Consumer | Source | Classification | Audit result |
|---|---|---|---|
| Paper-B `prob:perfiber` / prefix locator fibers | `s3b_iii_3_fibers_and_noanchor.md` says the first locator coefficients are coordinate-plane sections of `D_j` | coordinate-slice / prefix-fiber flats | scoped |
| MCA slope fiber `fiber(Z)=#(D_j cap P(ker M(Z)))` | `s3b_iii_3_fibers_and_noanchor.md` identifies slope fibers as linear-plane sections cut out by `ker M(Z)` | Hankel-pencil kernel flats | scoped |
| L1 `ImgFib_U` petal/sunflower residual | `s7_list_side.md` identifies the list-side petal battle as Conjecture F for its plane family; `l1_full_list_quotient_proof_program.md` leaves mixed-petal amplification conjectural | petal-structured / auxiliary-list plane family | escaping consumer |

## Consequence

The audit does justify a scoped proof attempt for the already-identified
coordinate and Hankel-kernel uses:

```text
coordinate prefix fibers  -> shortened-RS / MDS-dual moment methods;
Hankel kernel fibers      -> displacement-kernel classification methods.
```

It does not justify deleting or globally demoting Conjecture F, because the
L1 safe side still has a named residual whose plane family is not certified in
the repo as either coordinate-slice/fiber or Hankel-kernel.  That residual is:

```text
maximal mixed-petal / PMA-wide sunflower amplification.
```

The right conservative DAG update is therefore:

```text
f_consumer_scoped = AUDIT / PARTIAL
QF.10 may open only for the coordinate-prefix and Hankel-kernel subfamilies;
general Conjecture F remains live until the PMA-wide consumer is proved,
refuted, or reduced to one of the scoped families.
```

## Source Markers

The companion verifier checks that the source files still contain the markers
used by this audit:

- `prob:perfiber`;
- `COORDINATE-plane sections`;
- `fiber(Z)`;
- `ker M(Z)`;
- `L1 battle is Conjecture F`;
- `Mixed-petal sunflower amplification`;
- `CONJECTURAL`.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_f_consumer_scoped_audit.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_f_consumer_scoped_audit.py \
  --check experimental/data/certificates/f-consumer-scoped-audit/f_consumer_scoped_audit.json
```

