# Official Row Primes Reframe

- **Status:** PROVED / citation reframe.
- **DAG node:** `official_row_primes_pinning`.
- **Certificate:** `experimental/data/certificates/official-row-primes-reframe/official_row_primes_reframe.json`.
- **Verifier:** `python3 experimental/scripts/verify_official_row_primes_reframe.py --check experimental/data/certificates/official-row-primes-reframe/official_row_primes_reframe.json`.

This packet closes the old "missing literal official row primes" ask by
reframing it.  The ABF grand-challenge statement does not publish a finite list
of official prime constants.  It quantifies over admissible Reed-Solomon codes
over fields `F`, with the smooth-domain, rate, dimension, and field-size
conditions recorded in the certificate.

## Claim

There is no hidden finite list of literal official row primes that must be
recovered before row certification can proceed.  Certification obligations are
instead one of:

```text
family-uniform:  prove the statement over the admissible field/domain/rate class
exhibit-specific: name the exact field used by the certificate
```

A computation over a stand-in prime remains useful as an exhibit, calibration,
or harness check.  It becomes an official-row claim only when paired with a
uniform transfer theorem or when the exhibit field itself is the certified
object.

## Citation Pin

The certificate pins the source to ABF26 / IACR ePrint 2026/680, page 5, with
PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The decisive fragments are:

```text
assuming |F| is sufficiently large
for every choice of F, L, and k
k <= 2^40
|F| < 2^256
```

These are quantifier and admissibility conditions, not a table of prescribed
prime constants.

## Consequence For Experimental Packets

Packets that currently say "literal official primes are not in-repo" should be
read under this discipline:

```text
stand-in prime packet: exhibit/calibration unless a transfer theorem is supplied
named-field packet: exact exhibit certificate
uniform packet: official-row certificate over its stated admissible family
```

This is the same convention used by exact exhibit-field certificates such as an
E1 Pocklington field packet: the field is named explicitly, and the packet does
not pretend to be uniform over all fields.

## Non-Claims

- This packet does not certify any stand-in prime as official.
- This packet does not supply a transfer theorem from stand-in primes to all
  admissible fields.
- This packet does not change Papers A-D; it is an experimental audit note for
  certificate semantics.
