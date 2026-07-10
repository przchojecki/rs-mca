# Max-fiber control special-case proofs (W51-M2)

## Status
EXPERIMENTAL. **Rung: PROVED-SPECIAL** (subclass R≥m only).

## Phase 0
cube3 **E=216**, Δ=**27/64**.

## Lemma A (PROVED) — Newton injectivity for R ≥ m
Power sums p₁…pₘ determine elementary symmetric e₁…eₘ (Newton–Girard, char>m),
hence the monic polynomial ∏(X−t) and the m-subset S. Thus Φ_R is injective on
m-subsets when R≥m, so max f_s=1 and low-energy max ratio ≤1.

Toy certificate: all R≥m enumerated instances injective (n≥5).

**Discharges:** reduced C9 input on the subclass R≥m.

**Sharpness:** R<m control rows are often non-injective.

## Lemma B (PROVED) — trivial majorant
max_f/barN ≤ L always. Useful only if L=exp(o(N)).

## Lemma C
W50-II: Gsid ≤ (max_f/barN)^q (payment reduces to max-fiber control).

## REDUCED open core
For 1≤R<m on deep charts (R√p not o(N)), prove
max{f_s : Δ_s ≤ exp(−σN)} ≤ exp(o(N))·barN.
Attack: large algebraic fibers vs low additive energy (start at R=2).

## Dual routes
- **generator:** Newton argument + enumeration certificates
- **checker:** re-enum R≥m max_f=1; ratio≤L; four-tuple cube3

## Reproducibility
```text
py -3.13 experimental/scripts/verify_maxfiber_control_proof.py --check
payload_sha256: e919e8f8d91987f7d304c59970b9888adfd27bf14b8c633c7b22e94d28487488
```
