# M1 Cycle120 Domain-Generated Field Ledger

Status: AUDIT / DOMAIN-GENERATED-FIELD-LEDGER.

Date: 2026-06-24.

This note checks a field-ledger point for the Cycle120 row. The row is stated as

```text
K = F_17^32,
H = <theta> <= K^*,
|H| = 512.
```

For the repository bookkeeping, it matters that `H` is not merely embedded in
`K`: the domain generator `theta` itself generates the full field over `F_17`.
This keeps the generated-field, code-field, and line-field ledgers aligned:

```text
q_gen = q_code = q_line = 17^32.
```

## Verification

The multiplicative-order test gives

```text
ord_256(17) = 16,
ord_512(17) = 32.
```

Thus an element of order `256` over characteristic `17` has degree `16`, and an
element of order `512` has degree `32`. In the concrete model,

```text
eta has order 256 and generates F_17^16,
theta has order 512 and generates F_17^32,
theta^2 = eta.
```

Equivalently, the Frobenius checks are:

```text
eta^(17^16)=eta, but eta^(17^d)!=eta for d=1,2,4,8;
theta^(17^32)=theta, but theta^(17^d)!=theta for d=1,2,4,8,16.
```

So `H=<theta>` is not contained in a proper subfield of `F_17^32`.

## Verifier

Run:

```sh
python3 experimental/scripts/verify_m1_cycle120_domain_field_ledger.py
python3 experimental/scripts/verify_m1_cycle120_domain_field_ledger.py --json
```

The verifier imports the Cycle116 field/lift contract and smooth-padding
domain decomposition, then checks the multiplicative-order and Frobenius
subfield criteria above.

## Scope

This is not an official ABF source-gate check. It only records the local
finite-field ledger:

```text
the smooth domain generator theta generates the full field K=F_17^32;
the line parameter gamma is therefore sampled from the same field used by the
  code and by the domain-generated ledger in this row.
```
