# Exchange-Compression Extremality Check

## Claim

The packet records finite aligned split-locator families and checks whether
any of them exceed the point-dictator Johnson-exchange RHS or the recorded
anticode packing inequality.

## Status

EXPERIMENTAL / AUDIT. The packet is a finite pass-on-range search; no
exchange-rigidity theorem is claimed.

## Parameters

- Prime fields `F_7`, `F_11`, `F_13`, and `F_17`.
- `q_gen = q_line = q_chal = p` in every row.
- Domains are multiplicative subgroups `mu_n <= F_p^*`.
- Each slope family is the set of split-locator supports aligned for the
  recorded pair of syndrome source vectors.

## Existing Paper Dependency

This checks the exchange-compression route associated with Johnson-exchange
and anticode extremality for algebraically constrained aligned-support
families.

## Proof Idea Or Experiment

The scanner materializes each aligned slope family as a list of `j`-subsets.
For each family it counts exact ordered Johnson-neighbor hits and compares the
resulting rational probability against the point-dictator RHS. It also records
the strongest pairwise-exchange anticode check available from the family.

The verifier reconstructs every family and recomputes all probabilities and
integer inequalities with exact arithmetic.

The committed scanner uses exact CPU enumeration for these small rows. It does
not implement a CuPy or RawKernel accelerator path.

## Ledger Impact

No recorded family beats the point-dictator RHS or violates the anticode check
in the finite range. This is evidence for the compression route on the tested
rows only.

## Constants

```text
F_7,n=6,j=2,codim=1
F_11,n=10,j=3,codim=2
F_13,n=12,j=3,codim=2
F_17,n=16,j=3,codim=2
F_17,n=16,j=4,codim=2
```

The `F_17` rows are included as split-locator oracle gates.

## Reproducibility

```powershell
py -3.13 experimental/scripts/gpu/exchange_compression_search.py --emit-defaults
py -3.13 experimental/scripts/verify_exchange_compression.py --check experimental/data/certificates/exchange-compression/exchange_compression_rows.json
```

## Non-Claims

This does not prove exchange-rigidity, does not resolve `prob:band`, and does
not classify all algebraically constrained support families. It is a finite
pass-on-range search with exact replay.
