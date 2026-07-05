# Wild Row Audit

Status: PROVED / AUDIT.

Source DAG node: `wild_row_audit`.

## Statement

The admissible Mersenne wild rows below the official field cap are exactly the
rows

```text
n = 2^r,              r in {13, 17, 19, 31},
p = 2^r - 1,
q = p^(2s) < 2^256.
```

There are `26` such `(n,q)` rows.  Every coset of `mu_n` inherits wildness by
dilation conjugacy.  At wild rows the quotient taxonomy enlarges from the tame
dihedral lattice to the Dickson subgroup lattice of `PGL2(F_{n-1})`.

The fully computable toy row `F_49 / mu_8` confirms that the enlarged Dickson
taxonomy accounts for all invariant support/window strata and that it contains
orbit-window partitions absent from the tame dihedral/Sylow-2 lattice.

## Proof

For a 2-power row to be wild, the domain must be projectively the subfield
circle `P^1(F_p)` with

```text
n = p + 1,       p = 2^r - 1,       q = p^(2s) < 2^256.
```

For `r in {13,17,19,31}`, exact integer comparison gives admissible counts
`9, 7, 6, 4`, respectively, hence `26` total rows.  Dilation by any nonzero
scalar conjugates `mu_n` to its coset and conjugates the stabilizer and every
subgroup stratum, so wildness is coset-independent.

For the toy row `F_49 / mu_8`, the verifier constructs `PGL2(F_7)` acting on
`P^1(F_7)`.  It checks group order `336`, sharp 3-transitivity, subgroup count
`413`, and then verifies for every subgroup that invariant subsets are exactly
unions of subgroup orbits.  Comparing the full Dickson lattice with a selected
tame dihedral/Sylow-2 sublattice shows extra orbit-window partitions:

```text
(1,1,3,3), (1,1,6), (1,7), (2,3,3), (2,6).
```

Thus a dihedral-only ledger is incomplete at wild rows, but the incompleteness
is finite and classified by the Dickson lattice.

## Role

This audit is row-family hygiene for exact certificates.  It prevents a tame
dihedral quotient taxonomy from being silently applied to admissible wild
Mersenne rows.  The clean rows used by the main three-rate campaign remain
tame, but any submitted wild row needs its own Dickson-window census column.

## Non-Claims

This packet does not price every prize-scale Dickson window family, does not
close a wild-row adjacent upper certificate, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_wild_row_audit.py --emit
python3 experimental/scripts/verify_wild_row_audit.py \
  --check experimental/data/certificates/wild-row-audit/wild_row_audit.json
```
