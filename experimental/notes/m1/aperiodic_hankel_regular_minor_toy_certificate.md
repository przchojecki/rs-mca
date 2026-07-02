# Aperiodic Hankel regular-minor toy certificate

**Status:** AUDIT / PROVED for this toy certificate.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note supplies a first concrete certificate instance for the Paper D v12
aperiodic Hankel chart atlas, together with a reusable packet checker for
`scripts/aperiodic_eliminant_schema.json`.  It is deliberately small: the row is the
`agents.md` toy case

```text
F = F_17,
D = F_17^*,
n = 16,
k = 8,
agreement threshold a = 13.
```

It is not a prize-row certificate and not a proof of M1.  Its purpose is to
make the new `scripts/aperiodic_eliminant_schema.json` workflow replayable on
a nontrivial exact row where all closed-range exact agreements are in the
regular overdetermined Hankel bucket.

## Certificate object

For the deterministic syndrome pair

```text
u_m = 3 + 5m + 2m^2 + m^3       mod 17,
v_m = 7 + 4m + 6m^2 + 3m^3      mod 17,
0 <= m < 8,
```

the certificate checks exact agreements

```text
A = 13, 14, 15, 16.
```

For each exact agreement,

```text
j = n-A,
t = A-k,
t >= j+1.
```

Thus the regular-minor lemma in Paper D v12 applies.  The verifier chooses the
first `j+1` Hankel rows, computes

```text
Delta_A(Z) = det(H_{t,j}(u) + Z H_{t,j}(v))_{rows 0..j},
```

checks that `Delta_A` is nonzero, checks `deg Delta_A <= j+1`, enumerates all
`D`-split co-support locators of size `j`, and verifies directly that every
finite noncontained bad slope from those locators is a root of `Delta_A`.

## Output

The machine-readable certificate is

```text
experimental/data/certificates/aperiodic-hankel-regular-minor-toy/
  f17_n16_k8_a13_regular_minor_certificate.json
```

It declares

```text
schema_version = aperiodic-hankel-eliminant-v1
sampler = finite_affine_line
status = PROVED
```

and records the regular-minor coefficient lists, root lists, enumerated bad
slopes, and closed-range root union.  The declared aperiodic numerator is the
size of the certified root union for this fixed toy syndrome pair.

## Non-claims

This certificate does not:

```text
prove a prize-row threshold;
remove quotient or tangent branches in a general theorem;
prove the M1 aperiodic local limit;
give a worst-case bound over all received lines;
claim protocol soundness.
```

It is a replayable instance of the regular overdetermined bucket in the new
Paper D v12 atlas.

## Verification

Run:

```sh
python3 experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py
python3 experimental/scripts/verify_aperiodic_hankel_regular_minor_toy.py \
  --check experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/aperiodic-hankel-regular-minor-toy/f17_n16_k8_a13_regular_minor_certificate.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/aperiodic-hankel-regular-minor-toy/invalid_bad_j_packet.json
```

The toy generator also has `--write` and `--json` modes for deterministic
certificate regeneration.  The standalone checker validates JSON-schema
conformance, `j=n-A`, `t=A-k`, residual-obstruction labels, regular-minor
degree/root hashes, and the declared root-union numerator when the packet uses
inline root tables.
