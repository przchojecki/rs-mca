# E25 Dihedral Toy Audit

- **Task:** E25.
- **DAG nodes:** `payment_completeness`, `dihedral_quotient_stratum`,
  `zone_b`.
- **Status:** TOY AUDIT / locator absorbed by the dihedral ledger.
- **Verifier:** `experimental/scripts/verify_e25_dihedral_toy_audit.py`.
- **Artifact:** `experimental/data/certificates/e25-dihedral-toy-audit/e25_dihedral_toy_audit.json`.

This packet is the first exact toy pass for the E25 dihedral audit.  It works
on the multiplicative row `mu_16` over `F_17` and `F_97`, with toy rate
`k/n = 8/16`, and audits agreement sizes

```text
A = 10, 12, 14.
```

It does not run the prize-row M5 charts.  It also does not enumerate every
projective line in the full 9-dimensional dihedral word space.  The checked
alignment lines are the Chebyshev-character basis lines

```text
T_e + z T_f,  0 <= e < f <= 8,
```

where `T_e(x) = x^e + x^{-e}` on `mu_16`.

## Locator Audit

The verifier builds every audited inverse-pair support from the moving pairs

```text
{i, -i},  i = 1,...,7,
```

and also includes the fixed-branch variant containing both fixed points
`+1` and `-1`.  For each support it constructs the locator directly from
the roots and checks the dihedral pullback identity.

For moving-pair supports:

```text
prod_{i in I}(X^2 - (a_i + a_i^{-1})X + 1)
  = X^h q(X + X^{-1}).
```

For the fixed `+-1` branch:

```text
(X^2 - 1) prod_{i in I}(X^2 - (a_i + a_i^{-1})X + 1).
```

The moving-pair locators are reciprocal with multiplier `+1`; the fixed-branch
locators have the expected anti-reciprocal multiplier `-1`.  In both cases,
the locator is a Chebyshev/dihedral pullback rather than a primitive new
support family.

Per prime the audited support count is:

```text
A=10: binom(7,5) + binom(7,4) = 56
A=12: binom(7,6) + binom(7,5) = 28
A=14: binom(7,7) + binom(7,6) = 8
total: 92
```

The checker separates supports with a nontrivial cyclic stabilizer from
dihedral-only supports.  The dihedral-only cases are the part not already
covered by ordinary multiplicative quotient periodicity.

## Alignment Audit

For each audited support and each of the `36` Chebyshev-character basis lines,
the verifier solves the finite alignment system:

```text
T_e + z T_f agrees with RS[F_p, mu_16, k=8] on the support.
```

It then charges every aligned finite slope to one of:

```text
tangent_code_endpoint
multiplicative_quotient_overlap
dihedral_antipodal_charge
```

The resulting counts are:

```text
F_17:
  dihedral_antipodal_charge       100
  multiplicative_quotient_overlap  80
  tangent_code_endpoint           736
  unpaid after ledgers              0

F_97:
  dihedral_antipodal_charge        64
  multiplicative_quotient_overlap  80
  tangent_code_endpoint           736
  unpaid after ledgers              0
```

The toy basis-line audit therefore finds real dihedral-only alignments, but no
unpaid residual once the dihedral/antipodal ledger is admitted.

## Interpretation

This supports the absorbed outcome for E25 at the toy locator and
Chebyshev-basis alignment level:

```text
palindromic inverse-pair locators are paid dihedral pullbacks,
and the audited finite alignments leave no unpaid toy residual.
```

The result is useful input for E26 and E28 because it verifies, on the first
exact multiplicative toys, that the dihedral window arithmetic is not merely a
new scale formula: its locator supports have the expected paid Chebyshev
structure.

## Replay

```bash
python3 experimental/scripts/verify_e25_dihedral_toy_audit.py --write
python3 experimental/scripts/verify_e25_dihedral_toy_audit.py --check
python3 -m py_compile experimental/scripts/verify_e25_dihedral_toy_audit.py
python3 -m json.tool experimental/data/certificates/e25-dihedral-toy-audit/e25_dihedral_toy_audit.json >/dev/null
```

## Nonclaims

This packet does not prove global E25 payment completeness, does not exhaust
all projective lines in the full dihedral word space, does not run the
`A=384..426` M5 restricted charts, and does not audit extension-field rows.
Those are the next E25 steps if the toy absorbed verdict is to be promoted to
the full dihedral ledger.
