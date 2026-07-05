# Master-Flatness Incidence Engine

## Claim

The packet adds a reusable split-locator incidence enumerator for
`Dloc_j(mu_n)`: every `j`-subset of a multiplicative domain is mapped to the
signed elementary-symmetric coefficient vector of its split locator, tagged by
periodicity scale, and counted against structured affine flats.

## Status

EXPERIMENTAL / AUDIT.

## Parameters

- `q_gen = q_line = q_chal = p` for the recorded prime-field rows.
- Base field `B = F_p`; no extension field is used.
- Full rows: `F_17,n=16` all `j`, `F_17,n=16,j=6,codim=4`,
  `F_31,n=30,j=5,codim=2`, and `F_97,n=96,j=3,codim=2`.
- Large witness row: `F_41,n=40,j=10,codim=3`.

## Existing Paper Dependency

This is the measurement instrument for Conjecture-F / master flatness in
`experimental/cap25_v13_experimental.tex` and the `(A)/(Q)` master-flatness
strategy note. It also records the periodicity-scale split used by
`tex/cs25_cap_v12.tex`.

## Proof Idea Or Experiment

For each subset `A`, the enumerator computes

```text
L_A(X)=prod_{a in A}(X-a)
```

and the signed top coefficient vector
`((-1)^1 e_1(A),...,(-1)^j e_j(A))`. Prefix-affine flats fix an initial segment
of that vector. The verifier reconstructs each row from integer arithmetic,
retags periodicity scale by subgroup-coset invariance, and checks every recorded
witness locator.

## Ledger Impact

The file provides a common exact incidence interface for prefix-affine `(Q)`
rows and later syndrome-annihilator `(A)` rows. The committed certificates are
evidence and infrastructure only.

## Constants

The `F_17,n=16,j=6,codim=4` row matches the existing prefix oracle:
`8008` locators, `7968` prefix values, histogram `{1:7928,2:40}`, and maximum
fiber size `2`.

The `F_41,n=40,j=10` row records `C(40,10)=847660528` as the search volume and
checks one exact split-locator witness, but it does not claim full maximum
occupancy.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/master_flatness_incidence_engine.py --emit-defaults
py -3.13 experimental/scripts/verify_master_flatness_incidence.py --check experimental/data/certificates/master-flatness-incidence/f17_n16_oracle.json experimental/data/certificates/master-flatness-incidence/f17_n16_prefix_oracle.json experimental/data/certificates/master-flatness-incidence/f31_n30_j5.json experimental/data/certificates/master-flatness-incidence/f97_n96_j3.json experimental/data/certificates/master-flatness-incidence/f41_n40_j10.json
```

## Non-Claims

This does not prove a growing-dimensional incidence bound, does not resolve
Conjecture-F, and does not resolve `prob:band`. The `F_41,n=40,j=10` row is
witness-only until a full accelerator run is attached.
