# M1 half-turn pair-core compression v1 certificate

Status: `PROVED_LOCAL_BRANCH_ALGEBRA_WITH_CONDITIONAL_LEDGER_DECOMPOSITION`.

This certificate records the generated artifacts for the M1 half-turn
pair-core packet.  The characteristic-zero `{1,3}` and `{1,4}` branch
algebra is proved locally; finite-field deployed use is conditional on
the named generated-collision and ledger branches.

The packet localizes one half-turn coefficient-shadow subbranch of
`CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-DETERMINANT-COMPRESSION`; it does
not close the full v13 M1 wall.

## Files

- `m1_half_turn_pair_core_13_v1.json`: machine-readable certificate.
- `README.md`: this generated certificate-directory summary.
- `experimental/notes/certificate_scanner/outputs/m1_half_turn_pair_core_13_v1.report.md`: generated Markdown report.

## Regeneration

```bash
python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --write
python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --check
python3 -m json.tool experimental/data/certificates/m1-half-turn-pair-core-13-v1/m1_half_turn_pair_core_13_v1.json
```

## Claims

- `{1,3}` half-turn pair-core classification over the honest characteristic-zero `2`-power cyclotomic model.
- `{1,3}` finite-field transfer obstruction classified by `F3(R)=e1(R)e2(R)-e3(R)`.
- `{1,4}` residual-core equation and residual-only slope map.
- `{1,4}` primitive residual image bound `n+1` after charging recursive lower-domain and half-turn-balance ledgers.
- Parity-empty subcases and the proved fixed-size `s=2` AB-rigidity base case.
- Exact imbalance-vector reductions for the next `{1,4}` inverse targets.

## Guardrail

The certificate includes a finite-field transfer guardrail:

- `F_17`, `n=16`, generator `3`.
- support exponents `[0, 1, 3, 14]`.
- locator coefficients `c0..cj = [9, 3, 3, 1, 1]`.
- both `{1,3}` rows vanish, but half-turn residual size is `4`.
- `F3(R)` exact key `1,3,3,1,2,0,0,-2` is nonzero over `Q(zeta_16)`.
- `F3(R)` reduces to `0` modulo `17`.

This shows that the characteristic-zero `{1,3}` theorem does not automatically
certify the finite-field KoalaBear slope image without a generated-collision ledger.

## External Evidence

The v3 experiment evidence is recorded as external evidence and is not replayed by
this verifier.  It supports, but does not prove, the next inverse targets.

## Nonclaims

- Does not cover finite-field generated-collision amplification.
- Does not cover finite-field {1,3} generated-collision emptiness or budget-smallness.
- Does not cover deployed KoalaBear finite-field {1,3} slope image.
- Does not cover a standalone numerical cost theorem for the recursive lower-domain ledger.
- Does not cover a standalone numerical cost theorem for the half-turn-balance ledger.
- Does not cover full valid-range half-turn-balance emptiness.
- Does not cover fixed-size imbalance-profile rigidity modulo antipodal symmetry for residual sizes >=3.
- Does not cover arbitrary nonconsecutive coefficient windows.
- Does not cover sparse Hankel-proxy row slices.
- Does not cover full M1 closure or deployed safe-side certificate.
